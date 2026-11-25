from __future__ import annotations

import argparse
import difflib
import json
import math
import os
import platform
import random
import statistics
import sys
import threading
import time as relogio
import warnings
from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import time, timedelta
from pathlib import Path
from urllib.parse import urlsplit

META_DA_CONSULTA_MS = 1000
META_DA_AGENDA_MS = 500
SENHA = "senha-da-medicao-123"
HORAS_POR_DIA = 10
BANCO_DO_REDIS_DA_MEDICAO = 2
BANCOS_DO_REDIS_PROTEGIDOS = (0, 1)
LIMITE_DA_CARGA_EM_LOTE = 5000
TAMANHO_DO_LOTE = 2000
RODADAS_PADRAO = 5
REAMOSTRAGENS = 2000
SEMENTE_DO_BOOTSTRAP = 20261125
CENARIOS_DA_OCUPACAO = ("PG", "REDIS_ACERTO", "REDIS_ERRO")
NIVEIS = ("API", "Caso de uso")


@dataclass
class Cenario:
    gestor: object
    solicitante: object
    espaco_id: int
    data: object


@dataclass
class Resultado:
    nome: str
    meta_ms: int
    amostras_ms: list[float]
    itens: str
    bytes_: int
    consultas_sql: int

    @property
    def p95(self) -> float:
        return statistics.quantiles(self.amostras_ms, n=100, method="inclusive")[94]

    @property
    def atendido(self) -> bool:
        return self.p95 <= self.meta_ms


def _argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--reservas", type=int, default=1000)
    parser.add_argument("--espacos", type=int, default=5)
    parser.add_argument("--solicitantes", type=int, default=20)
    parser.add_argument("--repeticoes", type=int, default=300)
    parser.add_argument("--aquecimento", type=int, default=5)
    parser.add_argument("--rodadas", type=int, default=RODADAS_PADRAO)
    parser.add_argument("--concorrencia", type=int, default=0, metavar="N")
    parser.add_argument("--saida", help="grava o Markdown aqui e as amostras em .json")
    return parser.parse_args()


def _url_do_banco(url: str, banco: int) -> str:
    return urlsplit(url)._replace(path=f"/{banco}").geturl()


def _apontar_para_o_banco_dedicado() -> str:
    original = os.environ.get("REDIS_URL", "").strip()
    if not original:
        raise SystemExit("REDIS_URL não está definida; rode pelo docker compose.")
    os.environ["REDIS_URL"] = _url_do_banco(original, BANCO_DO_REDIS_DA_MEDICAO)
    return original


def _preparar_django() -> None:
    sys.path.insert(0, os.getcwd())
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    import django

    django.setup()


def _exigir_banco_dedicado() -> None:
    from django.conf import settings

    from reservas.infrastructure.redis_comum import cliente

    local = settings.CACHES["default"]["LOCATION"]
    sufixo = f"/{BANCO_DO_REDIS_DA_MEDICAO}"
    banco_real = cliente("trava", escrita=True).connection_pool.connection_kwargs.get("db")
    if not isinstance(local, str) or not local.endswith(sufixo) or banco_real != BANCO_DO_REDIS_DA_MEDICAO:
        raise SystemExit(
            f"Abortado: o cache aponta para {local!r} (banco {banco_real}), e a medição só "
            f"pode usar o banco {BANCO_DO_REDIS_DA_MEDICAO} do Redis."
        )


def _limpar_banco_dedicado() -> None:
    from reservas.infrastructure.redis_comum import cliente

    _exigir_banco_dedicado()
    cliente("limpeza", escrita=True).flushdb()


def _tamanhos_dos_bancos_protegidos(url_original: str) -> dict[int, dict]:
    """Só leitura: DBSIZE e a linha do INFO keyspace dos bancos 0 e 1."""
    import redis

    tamanhos = {}
    for banco in BANCOS_DO_REDIS_PROTEGIDOS:
        conexao = redis.Redis.from_url(_url_do_banco(url_original, banco), socket_timeout=2)
        try:
            tamanhos[banco] = {
                "dbsize": conexao.dbsize(),
                "keyspace": conexao.info("keyspace").get(f"db{banco}"),
            }
        finally:
            conexao.close()
    return tamanhos


def _carregar(args: argparse.Namespace) -> Cenario:
    from django.contrib.auth import get_user_model
    from django.utils import timezone

    from espacos.api.dependencias import cadastrar_espaco
    from espacos.domain.tipo_espaco import TipoEspaco
    from reservas.domain.reserva import Reserva
    from reservas.domain.situacao import SituacaoReserva
    from reservas.domain.solicitante import Solicitante
    from reservas.infrastructure.repositorio_django import RepositorioReservasDjango

    usuarios = get_user_model().objects
    gestor = usuarios.create_superuser(
        "gestor@medicao.test", SENHA, nome="Gestor da Medição", matricula="M0000"
    )
    solicitantes = [
        usuarios.create_user(
            f"solicitante{n}@medicao.test",
            SENHA,
            nome=f"Solicitante {n}",
            matricula=f"M{n:04d}",
        )
        for n in range(1, args.solicitantes + 1)
    ]
    tipos = list(TipoEspaco)
    espacos = [
        cadastrar_espaco().executar(
            nome=f"Espaço de medição {n}", tipo=tipos[n % len(tipos)], capacidade=20
        )
        for n in range(args.espacos)
    ]
    situacoes = [
        (SituacaoReserva.SOLICITADA, None),
        (SituacaoReserva.CONFIRMADA, None),
        (SituacaoReserva.CONFIRMADA, None),
        (SituacaoReserva.CANCELADA, "Cancelada na medição."),
        (SituacaoReserva.RECUSADA, "Recusada na medição."),
    ]
    amanha = timezone.localdate() + timedelta(days=1)
    agora = timezone.now()
    plano = _plano_das_reservas(args, espacos, solicitantes, situacoes, amanha)
    if args.reservas > LIMITE_DA_CARGA_EM_LOTE:
        _gravar_em_lote(plano, agora)
    else:
        repositorio = RepositorioReservasDjango()
        for espaco, usuario, (situacao, motivo), intervalo in plano:
            repositorio.salvar(
                Reserva(
                    espaco_id=espaco.id,
                    solicitante=Solicitante(
                        usuario_id=usuario.pk, nome=usuario.nome, matricula=usuario.matricula
                    ),
                    intervalo=intervalo,
                    finalidade="Treino da medição de desempenho",
                    situacao=situacao,
                    motivo_da_situacao=motivo,
                    criada_em=agora,
                )
            )
    return Cenario(gestor=gestor, solicitante=solicitantes[0], espaco_id=espacos[0].id, data=amanha)


def _plano_das_reservas(args, espacos, solicitantes, situacoes, amanha):
    """Mesma distribuição nos dois caminhos de carga: sem sobreposição e, no
    primeiro espaço e dia, 6 reservas que ocupam horário (a ocupação medida)."""
    from reservas.domain.intervalo_de_horario import IntervaloDeHorario

    for indice in range(args.reservas):
        espaco = espacos[indice % len(espacos)]
        posicao = indice // len(espacos)
        dia, hora = divmod(posicao, HORAS_POR_DIA)
        intervalo = IntervaloDeHorario(
            data=amanha + timedelta(days=dia),
            hora_inicio=time(8 + hora),
            hora_fim=time(9 + hora),
        )
        yield (
            espaco,
            solicitantes[indice % len(solicitantes)],
            situacoes[posicao % len(situacoes)],
            intervalo,
        )


def _gravar_em_lote(plano, agora) -> None:
    """Caminho rápido: bulk_create sem passar pela entidade e SEM histórico.

    O histórico (RegistroDeSituacao) não entra na leitura da ocupação, então a
    medição dessa leitura não muda; as constraints do banco continuam valendo.
    """
    from reservas.infrastructure.models import ReservaModel

    lote = []
    for espaco, usuario, (situacao, motivo), intervalo in plano:
        lote.append(
            ReservaModel(
                espaco_id=espaco.id,
                solicitante_usuario_id=usuario.pk,
                solicitante_nome=usuario.nome,
                solicitante_matricula=usuario.matricula,
                inicio=intervalo.inicio(),
                fim=intervalo.fim(),
                finalidade="Treino da medição de desempenho",
                situacao=situacao,
                motivo_da_situacao=motivo or "",
                criada_em=agora,
            )
        )
        if len(lote) == TAMANHO_DO_LOTE:
            ReservaModel.objects.bulk_create(lote)
            lote = []
    if lote:
        ReservaModel.objects.bulk_create(lote)


def _cliente(usuario):
    from rest_framework.test import APIClient
    from rest_framework_simplejwt.tokens import RefreshToken

    cliente = APIClient()
    acesso = RefreshToken.for_user(usuario).access_token
    cliente.credentials(HTTP_AUTHORIZATION=f"Bearer {acesso}")
    return cliente


def _medir(nome, meta_ms, cliente, url, parametros, contar, args) -> Resultado:
    from django.db import connection

    def chamar():
        resposta = cliente.get(url, parametros)
        if resposta.status_code != 200:
            raise SystemExit(f"{nome}: status {resposta.status_code}: {resposta.content[:300]!r}")
        return resposta

    for _ in range(args.aquecimento):
        chamar()
    consultas = []
    with connection.execute_wrapper(lambda executar, sql, *resto: consultas.append(sql) or executar(sql, *resto)):
        resposta = chamar()
    amostras = []
    for _ in range(args.repeticoes):
        inicio = relogio.perf_counter()
        chamar()
        amostras.append((relogio.perf_counter() - inicio) * 1000)
    return Resultado(
        nome=nome,
        meta_ms=meta_ms,
        amostras_ms=amostras,
        itens=contar(resposta.data),
        bytes_=len(resposta.content),
        consultas_sql=len(consultas),
    )


def _itens_da_pagina(corpo) -> str:
    return f"{len(corpo['dados'])} de {corpo['paginacao']['total']}"


def _ultima_pagina(cliente, url) -> dict:
    paginacao = cliente.get(url).data["paginacao"]
    return {"pagina": max(paginacao["total_de_paginas"], 1)}


def _cenarios(cenario: Cenario, args) -> list[Resultado]:
    from django.urls import reverse

    gestor = _cliente(cenario.gestor)
    solicitante = _cliente(cenario.solicitante)
    lista = reverse("reservas:lista")
    filtro = {"espaco": cenario.espaco_id, "data": cenario.data.isoformat()}
    ultima = _ultima_pagina(gestor, lista)
    consulta = META_DA_CONSULTA_MS
    return [
        _medir("Consulta: Gestor, sem critério", consulta, gestor, lista, {}, _itens_da_pagina, args),
        _medir(
            f"Consulta: Gestor, sem critério, última página ({ultima['pagina']})",
            consulta,
            gestor,
            lista,
            ultima,
            _itens_da_pagina,
            args,
        ),
        _medir("Consulta: Gestor, espaço + data", consulta, gestor, lista, filtro, _itens_da_pagina, args),
        _medir("Consulta: Solicitante, só as próprias", consulta, solicitante, lista, {}, _itens_da_pagina, args),
    ]


class AgendaSempreIndisponivel:
    """Só para a medição: o Redis "fora do ar", então tudo vai ao PostgreSQL.

    Equivale à leitura anterior à RDS-05: nenhuma chamada ao Redis.
    """

    def _falhar(self, *_, **__):
        from reservas.application.portas import AgendaIndisponivel

        raise AgendaIndisponivel

    listar = versao = substituir = registrar = remover = dias_projetados = _falhar


@dataclass
class Reconstrucao:
    nome: str
    segundos: float
    detalhes: dict


@dataclass
class Concorrente:
    nome: str
    threads: int
    chamadas: int
    segundos: float
    amostras_ms: list[float] = field(repr=False)

    @property
    def vazao(self) -> float:
        return self.chamadas / self.segundos

    @property
    def p95(self) -> float:
        return statistics.quantiles(self.amostras_ms, n=100, method="inclusive")[94]


def _montar_casos():
    from django.utils import timezone

    from reservas.application.casos_de_uso import ConsultarOcupacaoDoDia
    from reservas.infrastructure.agenda_redis import AgendaDoDiaRedis
    from reservas.infrastructure.consulta_de_espacos import ConsultaDeEspacosViaFachada
    from reservas.infrastructure.repositorio_django import RepositorioReservasDjango

    def caso(agenda):
        return ConsultarOcupacaoDoDia(
            RepositorioReservasDjango(), ConsultaDeEspacosViaFachada(), agenda, timezone.now
        )

    return {
        "PG": caso(AgendaSempreIndisponivel()),
        "REDIS_ACERTO": caso(AgendaDoDiaRedis()),
        "REDIS_ERRO": caso(AgendaDoDiaRedis()),
    }


class _ComposicaoDaApi:
    def __init__(self, nome, casos):
        self.nome, self.casos = nome, casos

    def __enter__(self):
        from reservas.api import dependencias

        self.original = dependencias.consultar_ocupacao_do_dia
        if self.nome == "PG":
            caso = self.casos["PG"]
            dependencias.consultar_ocupacao_do_dia = lambda *_, **__: caso

    def __exit__(self, *_):
        from reservas.api import dependencias

        dependencias.consultar_ocupacao_do_dia = self.original


def _reconstruir() -> list[Reconstrucao]:
    from reservas.api.dependencias import reconstruir_agenda, reconstruir_indice

    reconstrucoes = []
    for nome, montar in (
        ("reconstruir_agenda", reconstruir_agenda),
        ("reconstruir_indice", reconstruir_indice),
    ):
        inicio = relogio.perf_counter()
        resultado = montar().executar()
        reconstrucoes.append(
            Reconstrucao(nome, relogio.perf_counter() - inicio, asdict(resultado))
        )
    return reconstrucoes


def _garantir_projecao(cenario) -> None:
    from reservas.infrastructure.agenda_redis import AgendaDoDiaRedis

    if AgendaDoDiaRedis().listar(cenario.espaco_id, cenario.data) is None:
        raise SystemExit("A projeção do dia medido não existe no Redis.")


def _apagar_a_chave_do_dia(cenario) -> None:
    from reservas.infrastructure.agenda_redis import _chave
    from reservas.infrastructure.redis_comum import cliente

    chave = _chave(cenario.espaco_id, cenario.data)
    cliente(chave, escrita=True).delete(chave)


def _como_texto(valor) -> str:
    if is_dataclass(valor):
        valor = asdict(valor)
    return json.dumps(valor, indent=1, sort_keys=True, default=str, ensure_ascii=False)


def _exigir_respostas_identicas(respostas: dict) -> None:
    referencia = respostas["PG"]
    for nome, resposta in respostas.items():
        if resposta != referencia:
            diff = difflib.unified_diff(
                _como_texto(referencia).splitlines(),
                _como_texto(resposta).splitlines(),
                "PG",
                nome,
                lineterm="",
            )
            raise SystemExit("As respostas diferem entre os cenários:\n" + "\n".join(diff))


def _contar_sql(chamar) -> int:
    from django.db import connection

    consultas = []
    with connection.execute_wrapper(lambda executar, sql, *resto: consultas.append(sql) or executar(sql, *resto)):
        chamar()
    return len(consultas)


def _ocupacao(cenario, args) -> tuple[list[Resultado], list[Reconstrucao]]:
    from django.urls import reverse

    reconstrucoes = _reconstruir()
    _garantir_projecao(cenario)
    casos = _montar_casos()
    cliente = _cliente(cenario.solicitante)
    url = reverse("reservas:ocupacao")
    filtro = {"espaco": cenario.espaco_id, "data": cenario.data.isoformat()}

    def preparar(nome):
        if nome == "REDIS_ERRO":
            _apagar_a_chave_do_dia(cenario)
        elif nome == "REDIS_ACERTO":
            _garantir_projecao(cenario)

    def pela_api(nome):
        with _ComposicaoDaApi(nome, casos):
            preparar(nome)
            resposta = cliente.get(url, filtro)
        if resposta.status_code != 200:
            raise SystemExit(f"{nome}: status {resposta.status_code}: {resposta.content[:300]!r}")
        return resposta

    def pelo_caso(nome):
        preparar(nome)
        return casos[nome].executar(espaco_id=cenario.espaco_id, data=cenario.data)

    respostas_api = {nome: pela_api(nome) for nome in CENARIOS_DA_OCUPACAO}
    _exigir_respostas_identicas({n: r.data for n, r in respostas_api.items()})
    _exigir_respostas_identicas({n: pelo_caso(n) for n in CENARIOS_DA_OCUPACAO})
    _garantir_projecao(cenario)

    series = {(n, nivel): [] for n in CENARIOS_DA_OCUPACAO for nivel in NIVEIS}
    for nome, nivel in series:
        for _ in range(args.aquecimento):
            (pela_api if nivel == "API" else pelo_caso)(nome)
    por_rodada = math.ceil(args.repeticoes / args.rodadas)
    for rodada in range(args.rodadas):
        giro = rodada % len(CENARIOS_DA_OCUPACAO)
        ordem = CENARIOS_DA_OCUPACAO[giro:] + CENARIOS_DA_OCUPACAO[:giro]
        for nome in ordem:
            for nivel in NIVEIS:
                for _ in range(por_rodada):
                    series[(nome, nivel)].append(
                        _cronometrar(nome, nivel, preparar, casos, cliente, url, filtro, cenario)
                    )
    corpo = respostas_api["PG"].data["dados"]
    itens = f"{len(corpo['ocupados'])} ocupados, {len(corpo['livres'])} livres"
    resultados = []
    for (nome, nivel), amostras in series.items():
        chamar = pela_api if nivel == "API" else pelo_caso
        resultados.append(
            Resultado(
                nome=f"Ocupação do dia: {nome}, {nivel}",
                meta_ms=META_DA_AGENDA_MS,
                amostras_ms=amostras,
                itens=itens,
                bytes_=len(respostas_api[nome].content),
                consultas_sql=_contar_sql(lambda n=nome, c=chamar: c(n)),
            )
        )
    _garantir_projecao(cenario)
    return resultados, reconstrucoes


def _cronometrar(nome, nivel, preparar, casos, cliente, url, filtro, cenario) -> float:
    if nivel == "API":
        with _ComposicaoDaApi(nome, casos):
            preparar(nome)
            inicio = relogio.perf_counter()
            cliente.get(url, filtro)
            return (relogio.perf_counter() - inicio) * 1000
    preparar(nome)
    inicio = relogio.perf_counter()
    casos[nome].executar(espaco_id=cenario.espaco_id, data=cenario.data)
    return (relogio.perf_counter() - inicio) * 1000


def _ic_da_diferenca(a: list[float], b: list[float]) -> tuple[float, float, float]:
    sorteio = random.Random(SEMENTE_DO_BOOTSTRAP)
    diferencas = sorted(
        statistics.median(sorteio.choices(a, k=len(a)))
        - statistics.median(sorteio.choices(b, k=len(b)))
        for _ in range(REAMOSTRAGENS)
    )
    inferior = diferencas[int(0.025 * REAMOSTRAGENS)]
    superior = diferencas[int(0.975 * REAMOSTRAGENS) - 1]
    return statistics.median(a) - statistics.median(b), inferior, superior


def _comparacoes(resultados: list[Resultado]) -> list[dict]:
    amostras = {r.nome: r.amostras_ms for r in resultados}
    comparacoes = []
    for nivel in NIVEIS:
        pg = amostras[f"Ocupação do dia: PG, {nivel}"]
        acerto = amostras[f"Ocupação do dia: REDIS_ACERTO, {nivel}"]
        erro = amostras[f"Ocupação do dia: REDIS_ERRO, {nivel}"]
        for rotulo, a, b in (
            ("PG − REDIS_ACERTO (ganho do acerto)", pg, acerto),
            ("REDIS_ERRO − PG (custo extra do miss)", erro, pg),
        ):
            diferenca, inferior, superior = _ic_da_diferenca(a, b)
            comparacoes.append(
                {
                    "nivel": nivel,
                    "comparacao": rotulo,
                    "diferenca_das_medianas_ms": diferenca,
                    "ic95_inferior_ms": inferior,
                    "ic95_superior_ms": superior,
                    "inclui_zero": inferior <= 0 <= superior,
                }
            )
    return comparacoes


def _concorrencia(cenario, args) -> list[Concorrente]:
    from django.db import connections

    casos = _montar_casos()
    resultados = []
    for nome in ("PG", "REDIS_ACERTO"):
        _garantir_projecao(cenario)
        amostras, erros = [], []
        barreira = threading.Barrier(args.concorrencia + 1)

        def trabalhar(caso=casos[nome]):
            minhas = []
            try:
                barreira.wait()
                for _ in range(args.repeticoes):
                    inicio = relogio.perf_counter()
                    caso.executar(espaco_id=cenario.espaco_id, data=cenario.data)
                    minhas.append((relogio.perf_counter() - inicio) * 1000)
            except Exception as erro:
                erros.append(erro)
            finally:
                connections.close_all()
            amostras.extend(minhas)

        threads = [threading.Thread(target=trabalhar) for _ in range(args.concorrencia)]
        for t in threads:
            t.start()
        barreira.wait()
        inicio = relogio.perf_counter()
        for t in threads:
            t.join()
        segundos = relogio.perf_counter() - inicio
        if erros:
            raise SystemExit(f"Concorrência {nome}: {erros[0]!r}")
        resultados.append(Concorrente(nome, args.concorrencia, len(amostras), segundos, amostras))
    return resultados


def _plano_de_execucao(cenario) -> tuple[list[str], dict]:
    from django.db import connection

    from reservas.domain.situacao import SITUACOES_QUE_OCUPAM_HORARIO
    from reservas.infrastructure.models import ReservaModel

    with connection.cursor() as cursor:
        cursor.execute("ANALYZE reservas_reserva")
        cursor.execute(
            "SELECT count(*), pg_size_pretty(pg_total_relation_size('reservas_reserva'))"
            " FROM reservas_reserva"
        )
        total, tamanho = cursor.fetchone()
        cursor.execute("SELECT indexname FROM pg_indexes WHERE tablename = 'reservas_reserva' ORDER BY 1")
        indices = [linha[0] for linha in cursor.fetchall()]
    consulta = ReservaModel.objects.filter(
        espaco_id=cenario.espaco_id,
        inicio__date=cenario.data,
        situacao__in=SITUACOES_QUE_OCUPAM_HORARIO,
    ).order_by("inicio", "id")
    list(consulta)
    plano = consulta.explain(analyze=True, buffers=True).splitlines()
    return plano, {"linhas": total, "tamanho_total": tamanho, "indices": indices}


def _informacoes_do_redis() -> dict:
    from reservas.infrastructure.redis_comum import cliente

    info = cliente("info", escrita=False).info("server")
    return {"redis_version": info["redis_version"], "os": info["os"]}


def _ambiente(args, segundos_de_carga: float, extras: dict) -> list[str]:
    import django
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute("SELECT version()")
        versao_do_banco = cursor.fetchone()[0].split(" on ")[0]
    if args.reservas > LIMITE_DA_CARGA_EM_LOTE:
        carga = "bulk_create em lotes, sem histórico"
    else:
        carga = "repositório, com histórico"
    return [
        f"- Sistema: {platform.platform()} ({os.cpu_count()} CPUs visíveis no container)",
        f"- Python {platform.python_version()}, Django {django.get_version()}, {versao_do_banco}",
        f"- Redis {extras['redis']['redis_version']} ({extras['redis']['os']}),"
        f" banco {BANCO_DO_REDIS_DA_MEDICAO} dedicado à medição",
        f"- Carga: {args.reservas} reservas ({carga}), {args.espacos} espaços, {args.solicitantes} solicitantes"
        f" (gravadas em {segundos_de_carga:.1f} s); tabela: {extras['tabela']['tamanho_total']}",
        f"- Medição: {args.aquecimento} chamadas de aquecimento e {args.repeticoes} medidas por cenário"
        f" ({args.rodadas} rodadas intercaladas nos cenários de ocupação),"
        " pela API em processo (APIClient com token de acesso), sem rede nem navegador",
    ]


def _imprimir(resultados: list[Resultado], ambiente: list[str], extras: dict) -> str:
    linhas = ["\n".join(ambiente), ""]
    linhas.append("| Cenário | Itens | Resposta | Consultas SQL | Mín | Mediana | p95 | Máx | Meta (p95) | Atende |")
    linhas.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in resultados:
        linhas.append(
            f"| {r.nome} | {r.itens} | {r.bytes_ / 1024:.0f} KiB | {r.consultas_sql} "
            f"| {min(r.amostras_ms):.1f} ms | {statistics.median(r.amostras_ms):.1f} ms "
            f"| {r.p95:.1f} ms | {max(r.amostras_ms):.1f} ms | ≤ {r.meta_ms} ms "
            f"| {'✔' if r.atendido else '✘'} |"
        )
    linhas += [
        "",
        f"Diferença das medianas e IC 95% (bootstrap, {REAMOSTRAGENS} reamostragens, semente {SEMENTE_DO_BOOTSTRAP}):",
        "",
        "| Nível | Comparação | Diferença | IC 95% | O IC inclui zero? |",
        "|---|---|---|---|---|",
    ]
    for c in extras["comparacoes"]:
        linhas.append(
            f"| {c['nivel']} | {c['comparacao']} | {c['diferenca_das_medianas_ms']:+.2f} ms "
            f"| [{c['ic95_inferior_ms']:+.2f}; {c['ic95_superior_ms']:+.2f}] ms "
            f"| {'sim' if c['inclui_zero'] else 'não'} |"
        )
    linhas += ["", "Reconstrução das projeções (Redis vazio → montado):", "", "| Comando | Tempo | Resultado |", "|---|---|---|"]
    for rec in extras["reconstrucoes"]:
        linhas.append(f"| {rec.nome} | {rec.segundos:.2f} s | {rec.detalhes} |")
    if extras["concorrencia"]:
        linhas += [
            "",
            "Concorrência (caso de uso direto, uma conexão por thread):",
            "",
            "| Cenário | Threads | Chamadas | Vazão | p95 |",
            "|---|---|---|---|---|",
        ]
        for c in extras["concorrencia"]:
            linhas.append(f"| {c.nome} | {c.threads} | {c.chamadas} | {c.vazao:.0f} req/s | {c.p95:.1f} ms |")
    tabela = extras["tabela"]
    linhas += [
        "",
        f"Tabela: {tabela['linhas']} linhas; índices: {', '.join(tabela['indices'])}.",
        "",
        "EXPLAIN (ANALYZE, BUFFERS) de `listar_que_ocupam_horario`:",
        "",
        "```",
        *extras["plano"],
        "```",
    ]
    protegidos = extras["bancos_protegidos"]
    linhas += [
        "",
        "Bancos do Redis que a medição não pode tocar (DBSIZE antes → depois): "
        + "; ".join(
            f"banco {b}: {protegidos['antes'][b]['dbsize']} → {protegidos['depois'][b]['dbsize']}"
            for b in BANCOS_DO_REDIS_PROTEGIDOS
        ),
    ]
    texto = "\n".join(linhas)
    print(texto)
    return texto


def _gravar(args, texto: str, resultados: list[Resultado], extras: dict) -> None:
    if not args.saida:
        return
    caminho = Path(args.saida)
    caminho.write_text(texto + "\n", encoding="utf-8")
    bruto = {
        "argumentos": vars(args),
        "series_ms": {r.nome: r.amostras_ms for r in resultados},
        "comparacoes": extras["comparacoes"],
        "reconstrucoes": [asdict(r) for r in extras["reconstrucoes"]],
        "concorrencia": [{**asdict(c), "vazao": c.vazao} for c in extras["concorrencia"]],
        "plano": extras["plano"],
        "tabela": extras["tabela"],
        "redis": extras["redis"],
        "bancos_protegidos": extras["bancos_protegidos"],
    }
    caminho.with_suffix(".json").write_text(
        json.dumps(bruto, indent=1, ensure_ascii=False), encoding="utf-8"
    )


def main() -> int:
    warnings.filterwarnings("ignore", message="The HMAC key")
    args = _argumentos()
    url_original = _apontar_para_o_banco_dedicado()
    _preparar_django()
    from django.conf import settings
    from django.db import connection
    from django.test.utils import setup_test_environment, teardown_test_environment

    _exigir_banco_dedicado()
    antes = _tamanhos_dos_bancos_protegidos(url_original)
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
    setup_test_environment(debug=False)
    nome_original = connection.settings_dict["NAME"]
    connection.creation.create_test_db(verbosity=0, autoclobber=True)
    try:
        _limpar_banco_dedicado()
        inicio = relogio.perf_counter()
        cenario = _carregar(args)
        segundos_de_carga = relogio.perf_counter() - inicio
        plano, tabela = _plano_de_execucao(cenario)
        extras = {"plano": plano, "tabela": tabela, "redis": _informacoes_do_redis()}
        resultados = _cenarios(cenario, args)
        ocupacao, extras["reconstrucoes"] = _ocupacao(cenario, args)
        resultados += ocupacao
        extras["comparacoes"] = _comparacoes(ocupacao)
        extras["concorrencia"] = _concorrencia(cenario, args) if args.concorrencia else []
    finally:
        _limpar_banco_dedicado()
        connection.creation.destroy_test_db(nome_original, verbosity=0)
        teardown_test_environment()
    extras["bancos_protegidos"] = {
        "antes": antes,
        "depois": _tamanhos_dos_bancos_protegidos(url_original),
    }
    texto = _imprimir(resultados, _ambiente(args, segundos_de_carga, extras), extras)
    _gravar(args, texto, resultados, extras)
    return 0 if all(r.atendido for r in resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
