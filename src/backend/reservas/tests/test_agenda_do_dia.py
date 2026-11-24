import logging
from datetime import date, datetime, time, timedelta

import pytest
from django.core.cache import cache
from redis.exceptions import RedisError

from reservas.application.ocupacao_do_dia import HorarioOcupado
from reservas.application.portas import AgendaIndisponivel
from reservas.domain.intervalo_de_horario import FUSO_HORARIO
from reservas.domain.situacao import SituacaoReserva
from reservas.infrastructure.agenda_redis import (
    FOLGA_DO_TTL,
    TTL_MINIMO,
    AgendaDoDiaRedis,
)
from reservas.tests.fakes import DIA, AgendaDoDiaEmMemoria, intervalo

pytestmark = pytest.mark.django_db

ESPACO = 3
OUTRO_DIA = date(2026, 10, 26)
MANHA = HorarioOcupado(intervalo("09:00", "10:00"), SituacaoReserva.CONFIRMADA)
TARDE = HorarioOcupado(intervalo("14:00", "15:00"), SituacaoReserva.SOLICITADA)
NOITE = HorarioOcupado(intervalo("22:00", "00:00"), SituacaoReserva.SOLICITADA)
AGORA = datetime(2026, 10, 21, 12, 0, tzinfo=FUSO_HORARIO)


@pytest.fixture(params=["em_memoria", "redis"])
def agenda(request):
    if request.param == "em_memoria":
        return AgendaDoDiaEmMemoria()
    return AgendaDoDiaRedis(relogio=lambda: AGORA)


def _substituir(agenda, espaco_id, data, ocupados):
    gravou = agenda.substituir(
        espaco_id, data, ocupados, versao=agenda.versao(espaco_id, data)
    )
    assert gravou


def test_listar_sem_projecao_devolve_none(agenda):
    assert agenda.listar(ESPACO, DIA) is None


def test_substituir_com_lista_vazia_cria_projecao_de_dia_vazio(agenda):
    _substituir(agenda, ESPACO, DIA, {})

    assert agenda.listar(ESPACO, DIA) == ()


def test_registrar_sem_projecao_nao_cria_nada(agenda):
    agenda.registrar(ESPACO, 1, MANHA.intervalo, MANHA.situacao)

    assert agenda.listar(ESPACO, DIA) is None


def test_remover_sem_projecao_nao_cria_nada(agenda):
    agenda.remover(ESPACO, 1, DIA)

    assert agenda.listar(ESPACO, DIA) is None


def test_registrar_com_projecao_acrescenta_o_horario(agenda):
    _substituir(agenda, ESPACO, DIA, {})

    agenda.registrar(ESPACO, 1, MANHA.intervalo, MANHA.situacao)

    assert agenda.listar(ESPACO, DIA) == (MANHA,)


def test_remover_com_projecao_tira_o_horario_e_mantem_o_dia_vazio(agenda):
    _substituir(agenda, ESPACO, DIA, {1: MANHA})

    agenda.remover(ESPACO, 1, DIA)

    assert agenda.listar(ESPACO, DIA) == ()


def test_registrar_de_novo_com_outra_situacao_troca_o_membro(agenda):
    solicitada = HorarioOcupado(MANHA.intervalo, SituacaoReserva.SOLICITADA)
    _substituir(agenda, ESPACO, DIA, {1: solicitada})

    agenda.registrar(ESPACO, 1, MANHA.intervalo, SituacaoReserva.CONFIRMADA)

    assert agenda.listar(ESPACO, DIA) == (MANHA,)


def test_registrar_nao_confunde_ids_com_o_mesmo_prefixo(agenda):
    _substituir(agenda, ESPACO, DIA, {12: TARDE})

    agenda.registrar(ESPACO, 1, MANHA.intervalo, MANHA.situacao)

    assert agenda.listar(ESPACO, DIA) == (MANHA, TARDE)


def test_listar_ordena_por_inicio(agenda):
    _substituir(agenda, ESPACO, DIA, {1: TARDE, 2: NOITE, 3: MANHA})

    assert agenda.listar(ESPACO, DIA) == (MANHA, TARDE, NOITE)


def test_reserva_que_termina_a_meia_noite_volta_com_hora_fim_00_00(agenda):
    _substituir(agenda, ESPACO, DIA, {1: NOITE})

    (ocupado,) = agenda.listar(ESPACO, DIA)

    assert ocupado.intervalo.hora_fim == time(0, 0)
    assert ocupado.intervalo.termina_a_meia_noite()


@pytest.mark.parametrize(
    "situacao", [s for s in SituacaoReserva if not s.ocupa_horario]
)
def test_registrar_situacao_que_nao_ocupa_horario_lanca_value_error(agenda, situacao):
    _substituir(agenda, ESPACO, DIA, {})

    with pytest.raises(ValueError, match="não ocupa horário"):
        agenda.registrar(ESPACO, 1, MANHA.intervalo, situacao)

    assert agenda.listar(ESPACO, DIA) == ()


def test_remover_e_idempotente(agenda):
    _substituir(agenda, ESPACO, DIA, {1: MANHA})

    agenda.remover(ESPACO, 1, DIA)
    agenda.remover(ESPACO, 1, DIA)

    assert agenda.listar(ESPACO, DIA) == ()


def test_dias_e_espacos_diferentes_nao_se_misturam(agenda):
    _substituir(agenda, ESPACO, DIA, {1: MANHA})
    _substituir(agenda, ESPACO, OUTRO_DIA, {})
    _substituir(agenda, ESPACO + 1, DIA, {})

    agenda.registrar(ESPACO, 2, TARDE.intervalo, TARDE.situacao)

    assert agenda.listar(ESPACO, DIA) == (MANHA, TARDE)
    assert agenda.listar(ESPACO, OUTRO_DIA) == ()
    assert agenda.listar(ESPACO + 1, DIA) == ()


def test_substituir_apaga_o_que_havia_antes(agenda):
    _substituir(agenda, ESPACO, DIA, {1: MANHA, 2: TARDE})

    _substituir(agenda, ESPACO, DIA, {3: NOITE})

    assert agenda.listar(ESPACO, DIA) == (NOITE,)


def test_substituir_com_versao_atual_grava_e_devolve_true(agenda):
    versao = agenda.versao(ESPACO, DIA)

    gravou = agenda.substituir(ESPACO, DIA, {1: MANHA}, versao=versao)

    assert gravou is True
    assert agenda.listar(ESPACO, DIA) == (MANHA,)


def test_registro_sem_projecao_durante_a_reconstrucao_nao_se_perde(agenda):
    versao = agenda.versao(ESPACO, DIA)
    agenda.registrar(ESPACO, 2, TARDE.intervalo, TARDE.situacao)

    gravou = agenda.substituir(ESPACO, DIA, {1: MANHA}, versao=versao)

    assert gravou is False
    assert agenda.listar(ESPACO, DIA) is None


def test_remocao_sem_projecao_durante_a_reconstrucao_descarta_o_retrato(agenda):
    versao = agenda.versao(ESPACO, DIA)
    agenda.remover(ESPACO, 1, DIA)

    assert agenda.substituir(ESPACO, DIA, {1: MANHA}, versao=versao) is False
    assert agenda.listar(ESPACO, DIA) is None


def test_registro_com_projecao_durante_a_reconstrucao_preserva_o_registro(agenda):
    _substituir(agenda, ESPACO, DIA, {})
    versao = agenda.versao(ESPACO, DIA)
    agenda.registrar(ESPACO, 2, TARDE.intervalo, TARDE.situacao)

    gravou = agenda.substituir(ESPACO, DIA, {1: MANHA}, versao=versao)

    assert gravou is False
    assert agenda.listar(ESPACO, DIA) == (TARDE,)


def test_depois_de_descartar_a_proxima_reconstrucao_com_versao_nova_grava(agenda):
    versao = agenda.versao(ESPACO, DIA)
    agenda.registrar(ESPACO, 2, TARDE.intervalo, TARDE.situacao)
    agenda.substituir(ESPACO, DIA, {}, versao=versao)

    _substituir(agenda, ESPACO, DIA, {2: TARDE})

    assert agenda.listar(ESPACO, DIA) == (TARDE,)


def test_versoes_de_dias_e_espacos_diferentes_sao_independentes(agenda):
    versao = agenda.versao(ESPACO, DIA)
    agenda.registrar(ESPACO, 2, TARDE.intervalo, TARDE.situacao)
    agenda.remover(ESPACO, 2, OUTRO_DIA)
    agenda.remover(ESPACO + 1, 2, DIA)

    assert agenda.versao(ESPACO, DIA) == versao + 1
    assert agenda.versao(ESPACO, OUTRO_DIA) == 1
    assert agenda.versao(ESPACO + 1, DIA) == 1


def _chave(espaco_id=ESPACO, data=DIA):
    return cache.make_key(f"agenda:espaco:{espaco_id}:{data.isoformat()}")


def _cliente(chave, *, escrita=False):
    return cache._cache.get_client(chave, write=escrita)


def test_chave_fisica_tem_o_prefixo_do_projeto_e_o_banco_de_teste():
    _substituir(AgendaDoDiaRedis(relogio=lambda: AGORA), ESPACO, DIA, {})

    chave = _chave()
    cliente = _cliente(chave)

    assert chave == "conecta-campus:1:agenda:espaco:3:2026-10-25"
    assert cliente.exists(chave) == 1
    assert cliente.connection_pool.connection_kwargs["db"] == 1


def test_ttl_vai_ate_o_fim_do_dia_mais_a_folga():
    _substituir(AgendaDoDiaRedis(relogio=lambda: AGORA), ESPACO, DIA, {})

    fim_do_dia = datetime(2026, 10, 26, tzinfo=FUSO_HORARIO)
    esperado = (fim_do_dia - AGORA + FOLGA_DO_TTL).total_seconds()
    assert esperado - 5 <= _cliente(_chave()).ttl(_chave()) <= esperado


def test_ttl_nunca_fica_abaixo_do_piso_para_um_dia_passado():
    depois = AGORA + timedelta(days=30)
    _substituir(AgendaDoDiaRedis(relogio=lambda: depois), ESPACO, DIA, {})

    piso = TTL_MINIMO.total_seconds()
    assert piso - 5 <= _cliente(_chave()).ttl(_chave()) <= piso


def test_chave_da_versao_tem_prazo_para_expirar():
    redis = AgendaDoDiaRedis(relogio=lambda: AGORA)
    redis.remover(ESPACO, 1, DIA)

    chave = cache.make_key("agenda:versao:espaco:3:2026-10-25")
    assert (
        0
        < _cliente(chave).ttl(chave)
        <= (FOLGA_DO_TTL + timedelta(days=5)).total_seconds()
    )


def test_registrar_renova_o_ttl_com_o_mesmo_calculo():
    redis = AgendaDoDiaRedis(relogio=lambda: AGORA)
    _substituir(redis, ESPACO, DIA, {})
    _cliente(_chave(), escrita=True).expire(_chave(), 30)

    redis.registrar(ESPACO, 1, MANHA.intervalo, MANHA.situacao)

    assert _cliente(_chave()).ttl(_chave()) > 3600


OPERACOES = {
    "registrar": lambda a: a.registrar(ESPACO, 1, MANHA.intervalo, MANHA.situacao),
    "remover": lambda a: a.remover(ESPACO, 1, DIA),
    "listar": lambda a: a.listar(ESPACO, DIA),
    "substituir": lambda a: a.substituir(ESPACO, DIA, {}, versao=0),
    "versao": lambda a: a.versao(ESPACO, DIA),
}


@pytest.mark.parametrize("operacao", OPERACOES.values(), ids=OPERACOES.keys())
def test_erro_do_redis_vira_agenda_indisponivel_e_e_logado(
    monkeypatch, caplog, operacao
):
    def falhar(*args, **kwargs):
        raise RedisError("fora do ar")

    monkeypatch.setattr(cache._cache, "get_client", falhar)

    with (
        caplog.at_level(logging.ERROR, logger="reservas.infrastructure.agenda_redis"),
        pytest.raises(AgendaIndisponivel) as erro,
    ):
        operacao(AgendaDoDiaRedis(relogio=lambda: AGORA))

    assert isinstance(erro.value.__cause__, RedisError)
    assert "Redis indisponível na agenda do dia" in caplog.text


@pytest.mark.parametrize("operacao", OPERACOES.values(), ids=OPERACOES.keys())
def test_fake_indisponivel_lanca_agenda_indisponivel(operacao):
    with pytest.raises(AgendaIndisponivel):
        operacao(AgendaDoDiaEmMemoria(indisponivel=True))
