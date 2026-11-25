import logging
from datetime import datetime, timedelta

import pytest
from django.core.cache import cache
from redis.exceptions import RedisError

from reservas.application.portas import IndiceIndisponivel, RegistroDoIndice
from reservas.domain.intervalo_de_horario import FUSO_HORARIO
from reservas.domain.situacao import SituacaoReserva
from reservas.infrastructure import indice_redis
from reservas.infrastructure.indice_redis import IndiceDeReservasRedis
from reservas.infrastructure.redis_comum import cliente, texto
from reservas.tests.fakes import IndiceDeReservasEmMemoria

pytestmark = pytest.mark.django_db

BASE = datetime(2026, 10, 21, 12, 0, tzinfo=FUSO_HORARIO)
SOLICITADA = SituacaoReserva.SOLICITADA
CONFIRMADA = SituacaoReserva.CONFIRMADA
CANCELADA = SituacaoReserva.CANCELADA
CONCLUIDA = SituacaoReserva.CONCLUIDA
RECUSADA = SituacaoReserva.RECUSADA
ZERADA = dict.fromkeys(SituacaoReserva, 0)


@pytest.fixture(params=["em_memoria", "redis"])
def indice(request):
    if request.param == "em_memoria":
        return IndiceDeReservasEmMemoria()
    return IndiceDeReservasRedis()


def _minutos(quantos: int) -> datetime:
    return BASE + timedelta(minutes=quantos)


def _registro(reserva_id, situacao=SOLICITADA, minutos=0) -> RegistroDoIndice:
    return RegistroDoIndice(reserva_id, situacao, _minutos(minutos))


def _montar(indice, *registros) -> None:
    assert indice.substituir(registros, versao=indice.versao())


def _contagem(**quantidades: int) -> dict[SituacaoReserva, int]:
    return {**ZERADA, **{SituacaoReserva[nome]: n for nome, n in quantidades.items()}}


def _fila(indice) -> tuple[int, ...]:
    return indice.pendentes(1000)


def _confirmar_invariante(indice) -> None:
    fila = _fila(indice)
    assert len(fila) == len(set(fila))
    assert indice.contagem_por_situacao()[SOLICITADA] == len(fila)


def test_pendentes_sem_indice_montado_devolve_none(indice):
    assert indice.pendentes(10) is None


def test_contagem_sem_indice_montado_devolve_none(indice):
    assert indice.contagem_por_situacao() is None


def test_aplicar_sem_indice_montado_nao_grava_nada_mas_avanca_a_versao(indice):
    # Arrange
    antes = indice.versao()

    # Act
    indice.aplicar(1, SOLICITADA, BASE)

    # Assert
    assert indice.versao() == antes + 1
    assert indice.pendentes(10) is None
    assert indice.contagem_por_situacao() is None


def test_versao_inicial_e_zero(indice):
    assert indice.versao() == 0


# ---------- montado e vazio


def test_indice_montado_e_vazio_devolve_fila_vazia_e_cinco_zeros(indice):
    _montar(indice)

    assert indice.pendentes(10) == ()
    assert indice.contagem_por_situacao() == ZERADA


def test_aplicar_coloca_a_reserva_so_no_conjunto_da_situacao(indice):
    _montar(indice)

    indice.aplicar(1, CONFIRMADA, BASE)

    assert indice.contagem_por_situacao() == _contagem(CONFIRMADA=1)
    assert indice.pendentes(10) == ()


def test_aplicar_solicitada_entra_na_fila_e_no_conjunto(indice):
    _montar(indice)

    indice.aplicar(1, SOLICITADA, BASE)

    assert indice.pendentes(10) == (1,)
    assert indice.contagem_por_situacao() == _contagem(SOLICITADA=1)


def test_solicitada_confirmada_cancelada_move_a_reserva_e_tira_da_fila(indice):
    # Arrange
    _montar(indice)

    # Act e Assert
    indice.aplicar(1, SOLICITADA, BASE)
    assert indice.pendentes(10) == (1,)
    indice.aplicar(1, CONFIRMADA, BASE)
    assert indice.pendentes(10) == ()
    assert indice.contagem_por_situacao() == _contagem(CONFIRMADA=1)
    indice.aplicar(1, CANCELADA, BASE)
    assert indice.contagem_por_situacao() == _contagem(CANCELADA=1)


def test_aplicar_o_mesmo_estado_duas_vezes_nao_muda_nada(indice):
    # Arrange
    _montar(indice, _registro(1), _registro(2, minutos=1))
    indice.aplicar(1, CONFIRMADA, BASE)
    antes = (_fila(indice), indice.contagem_por_situacao())

    # Act
    indice.aplicar(1, CONFIRMADA, BASE)

    # Assert
    assert (_fila(indice), indice.contagem_por_situacao()) == antes


def test_chamadas_fora_de_ordem_terminam_no_estado_da_ultima_aplicada(indice):
    # Arrange
    _montar(indice)

    # Act
    indice.aplicar(1, CANCELADA, BASE)
    indice.aplicar(1, SOLICITADA, BASE)
    indice.aplicar(1, CONFIRMADA, BASE)
    indice.aplicar(1, SOLICITADA, BASE)

    # Assert
    assert _fila(indice) == (1,)
    assert indice.contagem_por_situacao() == _contagem(SOLICITADA=1)


def test_cada_aplicar_avanca_a_versao_com_o_indice_montado(indice):
    _montar(indice)
    antes = indice.versao()

    indice.aplicar(1, SOLICITADA, BASE)
    indice.aplicar(1, SOLICITADA, BASE)

    assert indice.versao() == antes + 2


def test_a_fila_e_o_conjunto_de_solicitadas_tem_sempre_os_mesmos_ids(indice):
    # Arrange
    _montar(indice, _registro(1), _registro(2, minutos=1), _registro(3, CONFIRMADA))
    sequencia = [
        (4, SOLICITADA, 5),
        (1, CONFIRMADA, 0),
        (2, CANCELADA, 1),
        (4, RECUSADA, 5),
        (5, SOLICITADA, 6),
        (1, SOLICITADA, 0),
    ]

    # Act e Assert
    for reserva_id, situacao, minutos in sequencia:
        indice.aplicar(reserva_id, situacao, _minutos(minutos))
        _confirmar_invariante(indice)
    assert _fila(indice) == (1, 5)


def test_pendentes_vem_do_mais_antigo_para_o_mais_novo(indice):
    _montar(
        indice,
        _registro(1, minutos=30),
        _registro(2, minutos=10),
        _registro(3, minutos=20),
    )

    assert indice.pendentes(10) == (2, 3, 1)


def test_pendentes_desempata_por_id_numerico_com_ids_de_um_e_dois_digitos(indice):
    # Arrange
    _montar(indice, _registro(10), _registro(9), _registro(100), _registro(2))

    # Assert
    assert indice.pendentes(10) == (2, 9, 10, 100)


def test_pendentes_pagina_com_limite_e_deslocamento(indice):
    _montar(indice, *(_registro(i, minutos=i) for i in range(1, 8)))

    assert indice.pendentes(3) == (1, 2, 3)
    assert indice.pendentes(3, 3) == (4, 5, 6)
    assert indice.pendentes(3, 6) == (7,)
    assert indice.pendentes(3, 20) == ()


@pytest.mark.parametrize(
    ("limite", "deslocamento", "trecho"),
    [(0, 0, "limite"), (-1, 0, "limite"), (5, -1, "deslocamento")],
)
def test_pendentes_com_janela_invalida_lanca_value_error(
    indice, limite, deslocamento, trecho
):
    with pytest.raises(ValueError, match=trecho):
        indice.pendentes(limite, deslocamento)


def test_substituir_monta_fila_e_contagens_do_zero(indice):
    # Act
    _montar(
        indice,
        _registro(1),
        _registro(2, CONFIRMADA),
        _registro(3, CONCLUIDA),
        _registro(4, SOLICITADA, minutos=-5),
    )

    # Assert
    assert indice.pendentes(10) == (4, 1)
    assert indice.contagem_por_situacao() == _contagem(
        SOLICITADA=2, CONFIRMADA=1, CONCLUIDA=1
    )


def test_substituir_remove_o_que_sobrou_de_antes(indice):
    # Arrange
    _montar(indice, _registro(1), _registro(2, CONFIRMADA), _registro(3, CANCELADA))

    # Act
    _montar(indice, _registro(2, SOLICITADA))

    # Assert
    assert indice.pendentes(10) == (2,)
    assert indice.contagem_por_situacao() == _contagem(SOLICITADA=1)


def test_substituir_com_banco_vazio_deixa_o_indice_montado_e_vazio(indice):
    _montar(indice, _registro(1))

    _montar(indice)

    assert indice.pendentes(10) == ()
    assert indice.contagem_por_situacao() == ZERADA


def test_substituir_de_novo_com_os_mesmos_dados_e_idempotente(indice):
    # Arrange
    registros = [_registro(1), _registro(2, CONFIRMADA), _registro(3, minutos=4)]
    _montar(indice, *registros)
    antes = (_fila(indice), indice.contagem_por_situacao())

    # Act
    _montar(indice, *registros)

    # Assert
    assert (_fila(indice), indice.contagem_por_situacao()) == antes


def test_substituir_descarta_e_devolve_false_se_a_versao_avancou(indice):
    # Arrange
    _montar(indice, _registro(1))
    versao_lida = indice.versao()
    indice.aplicar(2, SOLICITADA, BASE)

    # Act
    gravou = indice.substituir([_registro(9)], versao=versao_lida)

    # Assert
    assert gravou is False
    assert indice.pendentes(10) == (1, 2)


def test_substituir_descartado_com_o_indice_nao_montado_continua_nao_montado(indice):
    # Arrange
    versao_lida = indice.versao()
    indice.aplicar(2, SOLICITADA, BASE)

    # Act
    gravou = indice.substituir([_registro(9)], versao=versao_lida)

    # Assert
    assert gravou is False
    assert indice.pendentes(10) is None


def test_substituir_aceita_um_gerador_de_registros(indice):
    # Arrange
    gerador = (_registro(i, minutos=i) for i in range(1, 6))

    # Act
    gravou = indice.substituir(gerador, versao=indice.versao())

    # Assert
    assert gravou is True
    assert indice.pendentes(10) == (1, 2, 3, 4, 5)


def _chave(nome: str) -> str:
    return cache.make_key(nome)


def _chaves_do_indice() -> set[str]:
    padrao = cache.make_key("reservas:*")
    achadas = cliente(padrao, escrita=False).scan_iter(match=padrao, count=100)
    return {texto(chave) for chave in achadas}


def _temporarias() -> set[str]:
    return {chave for chave in _chaves_do_indice() if ":reservas:tmp:" in chave}


def test_as_chaves_seguem_a_grafia_da_dec_28():
    # Arrange
    indice = IndiceDeReservasRedis()

    # Act
    _montar(indice, _registro(1), _registro(2, CONFIRMADA))

    # Assert
    assert _chaves_do_indice() == {
        _chave("reservas:pendentes"),
        _chave("reservas:situacao:SOLICITADA"),
        _chave("reservas:situacao:CONFIRMADA"),
        _chave("reservas:indice:montado"),
    }
    assert _chave("reservas:pendentes").startswith("conecta-campus:1:")


def test_a_fila_guarda_o_id_com_zeros_a_esquerda_e_o_momento_como_score():
    # Arrange
    indice = IndiceDeReservasRedis()

    # Act
    _montar(indice, _registro(12, minutos=3))

    # Assert
    fila = _chave("reservas:pendentes")
    [(membro, score)] = cliente(fila, escrita=False).zrange(
        fila, 0, -1, withscores=True
    )
    assert texto(membro) == "0000000000000000012"
    assert score == _minutos(3).timestamp()


def test_o_conjunto_de_cada_situacao_guarda_o_id_puro():
    indice = IndiceDeReservasRedis()
    _montar(indice, _registro(12, CONFIRMADA))

    conjunto = _chave("reservas:situacao:CONFIRMADA")

    assert {texto(m) for m in cliente(conjunto, escrita=False).smembers(conjunto)} == {
        "12"
    }


def test_sinal_montado_vale_um():
    indice = IndiceDeReservasRedis()
    _montar(indice)

    sinal = _chave("reservas:indice:montado")

    assert texto(cliente(sinal, escrita=False).get(sinal)) == "1"


def test_as_chaves_definitivas_ficam_sem_prazo_de_expiracao():
    # Arrange
    indice = IndiceDeReservasRedis()

    # Act
    _montar(indice, _registro(1), _registro(2, CONFIRMADA))
    indice.aplicar(3, SOLICITADA, BASE)

    # Assert
    for chave in _chaves_do_indice() | {_chave("reservas:indice:versao")}:
        assert cliente(chave, escrita=False).ttl(chave) == -1, chave


def test_substituir_nao_deixa_chave_temporaria_para_tras(monkeypatch):
    # Arrange
    monkeypatch.setattr(indice_redis, "LOTE_DE_GRAVACAO", 2)
    indice = IndiceDeReservasRedis()

    # Act
    _montar(
        indice, *(_registro(i, CONFIRMADA if i % 2 else SOLICITADA) for i in range(9))
    )

    # Assert
    assert _temporarias() == set()


def test_substituir_descartado_nao_deixa_chave_temporaria_para_tras():
    # Arrange
    indice = IndiceDeReservasRedis()
    versao_lida = indice.versao()
    indice.aplicar(1, SOLICITADA, BASE)

    # Act
    gravou = indice.substituir(
        [_registro(1), _registro(2, CONFIRMADA)], versao=versao_lida
    )

    # Assert
    assert gravou is False
    assert _temporarias() == set()


def test_falha_no_meio_apaga_as_temporarias_e_sobe_indice_indisponivel(monkeypatch):
    # Arrange
    monkeypatch.setattr(indice_redis, "LOTE_DE_GRAVACAO", 2)
    indice = IndiceDeReservasRedis()
    _montar(indice, _registro(1))

    def com_falha():
        yield from (_registro(i, minutos=i) for i in range(10, 15))
        raise RedisError("caiu no meio")

    # Act
    with pytest.raises(IndiceIndisponivel):
        indice.substituir(com_falha(), versao=indice.versao())

    # Assert: sobra o índice antigo, inteiro, e nenhuma temporária
    assert _temporarias() == set()
    assert indice.pendentes(10) == (1,)


def test_erro_que_nao_e_do_redis_tambem_apaga_as_temporarias(monkeypatch):
    # Arrange
    monkeypatch.setattr(indice_redis, "LOTE_DE_GRAVACAO", 2)
    indice = IndiceDeReservasRedis()

    def com_falha():
        yield from (_registro(i) for i in range(1, 6))
        raise RuntimeError("falha no banco")

    # Act
    with pytest.raises(RuntimeError):
        indice.substituir(com_falha(), versao=indice.versao())

    # Assert
    assert _temporarias() == set()


def test_a_troca_e_atomica_nenhuma_leitura_ve_metade_nova_metade_velha():
    # Arrange
    indice = IndiceDeReservasRedis()
    _montar(indice, _registro(1), _registro(2, CONFIRMADA))

    # Act
    _montar(indice, _registro(3, CANCELADA), _registro(4))

    # Assert
    assert indice.pendentes(10) == (4,)
    assert indice.contagem_por_situacao() == _contagem(SOLICITADA=1, CANCELADA=1)


OPERACOES = {
    "aplicar": lambda i: i.aplicar(1, SOLICITADA, BASE),
    "pendentes": lambda i: i.pendentes(5),
    "contagem": lambda i: i.contagem_por_situacao(),
    "versao": lambda i: i.versao(),
    "substituir": lambda i: i.substituir([_registro(1)], versao=0),
}


@pytest.mark.parametrize("operacao", OPERACOES.values(), ids=OPERACOES.keys())
def test_erro_do_redis_vira_indice_indisponivel_e_e_logado(
    monkeypatch, caplog, operacao
):
    # Arrange
    def falhar(*args, **kwargs):
        raise RedisError("fora do ar")

    monkeypatch.setattr(cache._cache, "get_client", falhar)

    # Act
    with (
        caplog.at_level(logging.ERROR, logger="reservas.infrastructure.indice_redis"),
        pytest.raises(IndiceIndisponivel) as erro,
    ):
        operacao(IndiceDeReservasRedis())

    # Assert
    assert isinstance(erro.value.__cause__, RedisError)
    assert "Redis indisponível no índice de filas e contagens" in caplog.text


@pytest.mark.parametrize("operacao", OPERACOES.values(), ids=OPERACOES.keys())
def test_fake_indisponivel_lanca_indice_indisponivel(operacao):
    with pytest.raises(IndiceIndisponivel):
        operacao(IndiceDeReservasEmMemoria(indisponivel=True))


def test_temporaria_que_expirou_antes_da_troca_descarta_sem_publicar_contagem_parcial(
    monkeypatch,
):
    # Arrange
    monkeypatch.setattr(indice_redis, "LOTE_DE_GRAVACAO", 2)
    indice = IndiceDeReservasRedis()
    _montar(indice, _registro(1), _registro(2, CONFIRMADA))

    def expira_uma_no_meio():
        yield _registro(10, CONFIRMADA)
        yield _registro(11, CONFIRMADA)
        for chave in _temporarias():
            if chave.endswith(":situacao:CONFIRMADA"):
                cliente(chave, escrita=True).delete(chave)
        yield _registro(12, SOLICITADA)
        yield _registro(13, SOLICITADA)

    # Act
    gravou = indice.substituir(expira_uma_no_meio(), versao=indice.versao())

    # Assert
    assert gravou is False
    assert indice.pendentes(10) == (1,)
    assert indice.contagem_por_situacao() == _contagem(SOLICITADA=1, CONFIRMADA=1)
    assert _temporarias() == set()


def test_cada_lote_renova_o_prazo_das_temporarias_ja_criadas(monkeypatch):
    # Arrange
    monkeypatch.setattr(indice_redis, "LOTE_DE_GRAVACAO", 1)
    indice = IndiceDeReservasRedis()
    prazos = []

    def com_leitura_de_prazo():
        yield _registro(1, CONFIRMADA)
        for i in (2, 3):
            for chave in _temporarias():
                if chave.endswith(":situacao:CONFIRMADA"):
                    cliente(chave, escrita=True).expire(chave, 5)
            yield _registro(i, SOLICITADA)
            prazos.append(
                [
                    cliente(c, escrita=False).ttl(c)
                    for c in _temporarias()
                    if c.endswith(":situacao:CONFIRMADA")
                ]
            )

    # Act
    indice.substituir(com_leitura_de_prazo(), versao=indice.versao())

    # Assert
    assert prazos[-1][0] > 500
