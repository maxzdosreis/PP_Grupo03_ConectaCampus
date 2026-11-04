"""Mede o tempo da consulta de reservas e da agenda do dia (RNF-P01 e RNF-P02, DEC-12).

Roda dentro do container do backend, lendo o script pela entrada padrão (a pasta
scripts/ não é montada no container). A partir de src/:

    docker compose exec -T backend python - --reservas 1000 < ../scripts/medir_desempenho.py

Cria um banco de teste separado (test_<nome do banco>), aplica as migrations, grava
usuários, espaços e reservas, mede as consultas pela API com um token de acesso de
verdade e apaga o banco no fim. O banco de desenvolvimento não é tocado.
"""

from __future__ import annotations

import argparse
import os
import platform
import statistics
import sys
import time as relogio
import warnings
from dataclasses import dataclass
from datetime import time, timedelta

META_DA_CONSULTA_MS = 1000  # DEC-12
META_DA_AGENDA_MS = 500  # DEC-12
SENHA = "senha-da-medicao-123"
HORAS_POR_DIA = 10


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
    itens: int
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
    parser.add_argument("--repeticoes", type=int, default=50)
    parser.add_argument("--aquecimento", type=int, default=5)
    return parser.parse_args()


def _preparar_django() -> None:
    sys.path.insert(0, os.getcwd())
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    import django

    django.setup()


def _carregar(args: argparse.Namespace) -> Cenario:
    from django.contrib.auth import get_user_model
    from django.utils import timezone

    from espacos.api.dependencias import cadastrar_espaco
    from espacos.domain.tipo_espaco import TipoEspaco
    from reservas.domain.intervalo_de_horario import IntervaloDeHorario
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
    repositorio = RepositorioReservasDjango()
    amanha = timezone.localdate() + timedelta(days=1)
    agora = timezone.now()
    for indice in range(args.reservas):
        espaco = espacos[indice % len(espacos)]
        posicao = indice // len(espacos)
        dia, hora = divmod(posicao, HORAS_POR_DIA)
        usuario = solicitantes[indice % len(solicitantes)]
        situacao, motivo = situacoes[posicao % len(situacoes)]
        repositorio.salvar(
            Reserva(
                espaco_id=espaco.id,
                solicitante=Solicitante(
                    usuario_id=usuario.pk, nome=usuario.nome, matricula=usuario.matricula
                ),
                intervalo=IntervaloDeHorario(
                    data=amanha + timedelta(days=dia),
                    hora_inicio=time(8 + hora),
                    hora_fim=time(9 + hora),
                ),
                finalidade="Treino da medição de desempenho",
                situacao=situacao,
                motivo_da_situacao=motivo,
                criada_em=agora,
            )
        )
    return Cenario(gestor=gestor, solicitante=solicitantes[0], espaco_id=espacos[0].id, data=amanha)


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
        itens=contar(resposta.data["dados"]),
        bytes_=len(resposta.content),
        consultas_sql=len(consultas),
    )


def _cenarios(cenario: Cenario, args) -> list[Resultado]:
    from django.urls import reverse

    gestor = _cliente(cenario.gestor)
    solicitante = _cliente(cenario.solicitante)
    lista = reverse("reservas:lista")
    filtro = {"espaco": cenario.espaco_id, "data": cenario.data.isoformat()}
    return [
        _medir("Consulta: Gestor, sem critério", META_DA_CONSULTA_MS, gestor, lista, {}, len, args),
        _medir("Consulta: Gestor, espaço + data", META_DA_CONSULTA_MS, gestor, lista, filtro, len, args),
        _medir("Consulta: Solicitante, só as próprias", META_DA_CONSULTA_MS, solicitante, lista, {}, len, args),
        _medir(
            "Agenda do dia (espaço + data)",
            META_DA_AGENDA_MS,
            solicitante,
            reverse("reservas:ocupacao"),
            filtro,
            lambda dados: len(dados["ocupados"]),
            args,
        ),
    ]


def _ambiente(args, segundos_de_carga: float) -> list[str]:
    import django
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute("SELECT version()")
        versao_do_banco = cursor.fetchone()[0].split(" on ")[0]
    return [
        f"- Sistema: {platform.platform()} ({os.cpu_count()} CPUs visíveis no container)",
        f"- Python {platform.python_version()}, Django {django.get_version()}, {versao_do_banco}",
        f"- Carga: {args.reservas} reservas, {args.espacos} espaços, {args.solicitantes} solicitantes"
        f" (gravadas em {segundos_de_carga:.1f} s)",
        f"- Medição: {args.aquecimento} chamadas de aquecimento e {args.repeticoes} medidas por cenário,"
        " pela API em processo (APIClient com token de acesso), sem rede nem navegador",
    ]


def _imprimir(resultados: list[Resultado], ambiente: list[str]) -> None:
    print("\n".join(ambiente))
    print()
    print("| Cenário | Itens | Resposta | Consultas SQL | Mín | Mediana | p95 | Máx | Meta (p95) | Atende |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for r in resultados:
        print(
            f"| {r.nome} | {r.itens} | {r.bytes_ / 1024:.0f} KiB | {r.consultas_sql} "
            f"| {min(r.amostras_ms):.0f} ms | {statistics.median(r.amostras_ms):.0f} ms "
            f"| {r.p95:.0f} ms | {max(r.amostras_ms):.0f} ms | ≤ {r.meta_ms} ms "
            f"| {'✔' if r.atendido else '✘'} |"
        )


def main() -> int:
    warnings.filterwarnings("ignore", message="The HMAC key")
    args = _argumentos()
    _preparar_django()
    from django.conf import settings
    from django.db import connection
    from django.test.utils import setup_test_environment, teardown_test_environment

    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
    setup_test_environment(debug=False)
    nome_original = connection.settings_dict["NAME"]
    connection.creation.create_test_db(verbosity=0, autoclobber=True)
    try:
        inicio = relogio.perf_counter()
        cenario = _carregar(args)
        segundos_de_carga = relogio.perf_counter() - inicio
        resultados = _cenarios(cenario, args)
        _imprimir(resultados, _ambiente(args, segundos_de_carga))
    finally:
        connection.creation.destroy_test_db(nome_original, verbosity=0)
        teardown_test_environment()
    return 0 if all(r.atendido for r in resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
