from contextlib import ExitStack, contextmanager
from datetime import time, timedelta
from time import perf_counter

import pytest
from django.core.cache import cache
from django.urls import reverse
from django.utils import timezone

from reservas.api import dependencias
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import SituacaoReserva
from reservas.infrastructure.agenda_redis import AgendaDoDiaRedis
from reservas.infrastructure.indice_redis import IndiceDeReservasRedis
from reservas.infrastructure.redis_comum import cliente
from reservas.infrastructure.repositorio_django import RepositorioReservasDjango
from reservas.tests.fakes import ANA, FUNCIONAMENTO_PADRAO, intervalo
from reservas.tests.redis_de_teste import (
    afirmar_indice_igual_ao_postgres,
    membros_da_agenda,
    montar_indice,
    ocupados_do_postgres,
    ocupados_do_redis,
    projetar_dia,
    redis_em,
    redis_limpo_depois,
    servidor_que_nao_responde,
    url_de_porta_fechada,
)

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures("redis_limpo_depois"),
]

S = SituacaoReserva
URL_RESERVAS = reverse("reservas:lista")
URL_OCUPACAO = reverse("reservas:ocupacao")
URL_FILA = reverse("reservas:pendentes")
URL_CONTAGEM = reverse("reservas:contagem_por_situacao")
# Folga larga sobre o medido (~1 s por leitura, ~2 s na criação).
LIMITE_POR_CHAMADA_S = 10


def _amanha():
    return timezone.localdate() + timedelta(days=1)


def _guardar(espaco_id, hora):
    reserva = Reserva.solicitar(
        espaco_id=espaco_id,
        solicitante=ANA,
        data=_amanha(),
        hora_inicio=time(hora, 0),
        hora_fim=time(hora + 1, 0),
        finalidade="Treino do time",
        agora=timezone.now(),
        funcionamento=FUNCIONAMENTO_PADRAO,
    )
    return RepositorioReservasDjango().salvar(reserva)


def _solicitar(cliente_http, espaco_id, hora):
    return cliente_http.post(
        URL_RESERVAS,
        {
            "espaco_id": espaco_id,
            "data": _amanha().isoformat(),
            "hora_inicio": f"{hora:02d}:00",
            "hora_fim": f"{hora + 1:02d}:00",
            "finalidade": "Treino de vôlei",
        },
        format="json",
    )


def _ocupacao(cliente_http, espaco_id):
    return cliente_http.get(
        URL_OCUPACAO, {"espaco": espaco_id, "data": _amanha().isoformat()}
    )


def _quebrar(chave_logica, valor="texto no lugar do tipo certo"):
    chave = _chave(chave_logica)
    cliente(chave, escrita=True).set(chave, valor)


def _chave(chave_logica):
    return cache.make_key(chave_logica)


def _ids(resposta):
    return [reserva["id"] for reserva in resposta.data["dados"]]


def test_chave_da_agenda_com_tipo_errado_nao_derruba_leitura_nem_escrita(
    cliente_solicitante, espaco_id, django_capture_on_commit_callbacks
):
    # Arrange
    existente = _guardar(espaco_id, 10)
    dependencias.reconstruir_agenda().executar()
    _quebrar(f"agenda:espaco:{espaco_id}:{_amanha().isoformat()}")

    # Act
    leitura = _ocupacao(cliente_solicitante, espaco_id)
    with django_capture_on_commit_callbacks(execute=True):
        escrita = _solicitar(cliente_solicitante, espaco_id, 14)

    # Assert
    assert leitura.status_code == 200
    assert len(leitura.data["dados"]["ocupados"]) == 1
    assert escrita.status_code == 201
    assert RepositorioReservasDjango().obter_por_id(escrita.data["dados"]["id"])
    assert RepositorioReservasDjango().obter_por_id(existente.id)

    dependencias.reconstruir_agenda().executar()
    assert len(ocupados_do_postgres(espaco_id, _amanha())) == 2
    assert ocupados_do_redis(espaco_id, _amanha()) == ocupados_do_postgres(
        espaco_id, _amanha()
    )


def test_fila_e_contagem_com_tipo_errado_caem_no_postgresql_e_a_escrita_segue(
    cliente_gestor, cliente_solicitante, espaco_id, django_capture_on_commit_callbacks
):
    # Arrange
    _guardar(espaco_id, 9)
    _guardar(espaco_id, 11)
    montar_indice()
    fila_esperada = afirmar_indice_igual_ao_postgres()
    contagem_esperada = cliente_gestor.get(URL_CONTAGEM).json()
    _quebrar("reservas:pendentes")
    _quebrar("reservas:situacao:SOLICITADA")

    # Act
    fila = cliente_gestor.get(URL_FILA)
    contagem = cliente_gestor.get(URL_CONTAGEM)
    with django_capture_on_commit_callbacks(execute=True):
        escrita = _solicitar(cliente_solicitante, espaco_id, 14)

    # Assert
    assert fila.status_code == contagem.status_code == 200
    assert _ids(fila) == fila_esperada
    assert contagem.json() == contagem_esperada
    assert escrita.status_code == 201
    montar_indice()
    assert afirmar_indice_igual_ao_postgres() == [
        *fila_esperada,
        escrita.data["dados"]["id"],
    ]


def test_script_flush_entre_operacoes_recarrega_os_scripts_sozinho():
    # Arrange
    agenda, indice = AgendaDoDiaRedis(), IndiceDeReservasRedis()
    espaco_id, hoje = 31, _amanha()
    horario = intervalo("10:00", "11:00", hoje)

    def esvaziar_o_cache_de_scripts():
        cliente(_chave("qualquer"), escrita=True).script_flush()

    projetar_dia(espaco_id, hoje)
    montar_indice()

    # Act e Assert, operação por operação
    esvaziar_o_cache_de_scripts()
    agenda.registrar(espaco_id, 5, horario, S.SOLICITADA)
    assert membros_da_agenda(espaco_id, hoje) == ["5:660:SOLICITADA"]

    esvaziar_o_cache_de_scripts()
    agenda.registrar(espaco_id, 5, horario, S.CONFIRMADA)
    assert membros_da_agenda(espaco_id, hoje) == ["5:660:CONFIRMADA"]

    esvaziar_o_cache_de_scripts()
    agenda.remover(espaco_id, 5, hoje)
    assert membros_da_agenda(espaco_id, hoje) == []

    esvaziar_o_cache_de_scripts()
    assert agenda.substituir(espaco_id, hoje, {}, versao=agenda.versao(espaco_id, hoje))

    esvaziar_o_cache_de_scripts()
    indice.aplicar(5, S.SOLICITADA, timezone.now())
    assert indice.pendentes(10) == (5,)

    esvaziar_o_cache_de_scripts()
    assert indice.substituir([], versao=indice.versao())
    assert indice.pendentes(10) == ()


@pytest.mark.parametrize("modo", ["recusa", "travado"])
def test_redis_inalcancavel_nao_derruba_leituras_nem_a_criacao_e_se_recupera(
    modo,
    settings,
    cliente_gestor,
    cliente_solicitante,
    espaco_id,
    django_capture_on_commit_callbacks,
    capsys,
):
    # Arrange: dados e projeções montados ANTES de o cache apontar para outro lugar
    _guardar(espaco_id, 10)
    dependencias.reconstruir_agenda().executar()
    montar_indice()
    fila_esperada = afirmar_indice_igual_ao_postgres()
    tempos = {}

    def medir(nome, chamada):
        inicio = perf_counter()
        resultado = chamada()
        tempos[nome] = perf_counter() - inicio
        return resultado

    def criar():
        with django_capture_on_commit_callbacks(execute=True):
            return _solicitar(cliente_solicitante, espaco_id, 14)

    # Act
    with _redis_inalcancavel(settings, modo):
        ocupacao = medir("ocupação", lambda: _ocupacao(cliente_solicitante, espaco_id))
        fila = medir("fila", lambda: cliente_gestor.get(URL_FILA))
        contagem = medir("contagem", lambda: cliente_gestor.get(URL_CONTAGEM))
        criacao = medir("criação (201 + agenda + índice)", criar)

    # Assert
    with capsys.disabled():
        resumo = ", ".join(
            f"{nome}: {segundos:.2f}s" for nome, segundos in tempos.items()
        )
        print(f"\n[TST-01] Redis {modo} -> {resumo}")  # noqa: T201 - vai ao relatório
    assert all(s < LIMITE_POR_CHAMADA_S for s in tempos.values()), tempos
    assert ocupacao.status_code == 200
    assert len(ocupacao.data["dados"]["ocupados"]) == 1
    assert fila.status_code == contagem.status_code == 200
    assert _ids(fila) == fila_esperada
    assert contagem.data["dados"]["total"] == 1
    assert criacao.status_code == 201
    nova = RepositorioReservasDjango().obter_por_id(criacao.data["dados"]["id"])
    assert nova is not None
    assert nova.situacao is S.SOLICITADA

    dependencias.reconstruir_agenda().executar()
    montar_indice()
    assert ocupados_do_redis(espaco_id, _amanha()) == ocupados_do_postgres(
        espaco_id, _amanha()
    )
    afirmar_indice_igual_ao_postgres()


@contextmanager
def _redis_inalcancavel(settings, modo):
    with ExitStack() as pilha:
        if modo == "travado":
            url = pilha.enter_context(servidor_que_nao_responde())
        else:
            url = url_de_porta_fechada()
        pilha.enter_context(redis_em(settings, url))
        yield
