import logging

import pytest
from django.core.cache import cache
from redis.exceptions import RedisError

from reservas.application.portas import RankingIndisponivel, RegistroDoRanking
from reservas.domain.situacao import SituacaoReserva
from reservas.infrastructure import ranking_redis
from reservas.infrastructure.ranking_redis import RankingDeEspacosRedis
from reservas.infrastructure.redis_comum import cliente, texto
from reservas.tests.fakes import RankingDeEspacosEmMemoria

pytestmark = pytest.mark.django_db

SOLICITADA = SituacaoReserva.SOLICITADA
CONFIRMADA = SituacaoReserva.CONFIRMADA
RECUSADA = SituacaoReserva.RECUSADA
CANCELADA = SituacaoReserva.CANCELADA
CONCLUIDA = SituacaoReserva.CONCLUIDA


@pytest.fixture(params=["em_memoria", "redis"])
def ranking(request):
    if request.param == "em_memoria":
        return RankingDeEspacosEmMemoria()
    return RankingDeEspacosRedis()


def _registro(reserva_id, espaco_id=1, situacao=CONFIRMADA) -> RegistroDoRanking:
    return RegistroDoRanking(reserva_id, espaco_id, situacao)


def _montar(ranking, *registros) -> None:
    assert ranking.substituir(registros, versao=ranking.versao())


def _confirmadas(espaco_id: int, quantidade: int, a_partir_de: int):
    return [
        _registro(a_partir_de + i, espaco_id, CONFIRMADA) for i in range(quantidade)
    ]


def test_top_sem_o_ranking_montado_devolve_none(ranking):
    assert ranking.top(5) is None


def test_versao_inicial_e_zero(ranking):
    assert ranking.versao() == 0


def test_aplicar_sem_o_ranking_montado_nao_grava_mas_avanca_a_versao(ranking):
    # Act
    ranking.aplicar(1, 7, CONFIRMADA)

    # Assert
    assert ranking.versao() == 1
    assert ranking.top(5) is None
    _montar(ranking)
    assert ranking.top(5) == ()


def test_ranking_montado_e_vazio_devolve_tupla_vazia(ranking):
    _montar(ranking)

    assert ranking.top(5) == ()


def test_reserva_confirmada_conta_uma_vez(ranking):
    # Arrange
    _montar(ranking)

    # Act
    ranking.aplicar(1, 7, CONFIRMADA)

    # Assert
    assert ranking.top(5) == ((7, 1),)


def test_confirmada_que_vira_concluida_continua_contando_uma_vez(ranking):
    # Arrange
    _montar(ranking)
    ranking.aplicar(1, 7, CONFIRMADA)

    # Act
    ranking.aplicar(1, 7, CONCLUIDA)

    # Assert
    assert ranking.top(5) == ((7, 1),)


def test_confirmada_que_vira_cancelada_deixa_de_contar_e_o_espaco_some(ranking):
    # Arrange
    _montar(ranking)
    ranking.aplicar(1, 7, CONFIRMADA)

    # Act
    ranking.aplicar(1, 7, CANCELADA)

    # Assert
    assert ranking.top(5) == ()


def test_cancelar_uma_de_duas_deixa_o_espaco_com_uma(ranking):
    # Arrange
    _montar(ranking)
    ranking.aplicar(1, 7, CONFIRMADA)
    ranking.aplicar(2, 7, CONFIRMADA)

    # Act
    ranking.aplicar(1, 7, CANCELADA)

    # Assert
    assert ranking.top(5) == ((7, 1),)


@pytest.mark.parametrize("situacao", [SOLICITADA, RECUSADA, CANCELADA])
def test_situacao_que_nao_conta_nao_entra_no_ranking(ranking, situacao):
    # Arrange
    _montar(ranking)

    # Act
    ranking.aplicar(1, 7, situacao)

    # Assert
    assert ranking.top(5) == ()


def test_aplicar_o_mesmo_estado_varias_vezes_nao_soma(ranking):
    # Arrange
    _montar(ranking)

    # Act
    for _ in range(5):
        ranking.aplicar(1, 7, CONFIRMADA)

    # Assert
    assert ranking.top(5) == ((7, 1),)


def test_remover_o_que_nunca_contou_nao_deixa_total_negativo(ranking):
    # Arrange
    _montar(ranking, *_confirmadas(7, 1, 1))

    # Act
    ranking.aplicar(99, 7, CANCELADA)
    ranking.aplicar(99, 7, CANCELADA)

    # Assert
    assert ranking.top(5) == ((7, 1),)


def test_chamadas_fora_de_ordem_terminam_no_estado_da_ultima_aplicada(ranking):
    # Arrange
    _montar(ranking)

    # Act
    for situacao in (CANCELADA, CONFIRMADA, CONFIRMADA, CANCELADA, CONFIRMADA):
        ranking.aplicar(1, 7, situacao)

    # Assert
    assert ranking.top(5) == ((7, 1),)


def test_cada_aplicar_avanca_a_versao_com_o_ranking_montado(ranking):
    # Arrange
    _montar(ranking)
    antes = ranking.versao()

    # Act
    ranking.aplicar(1, 7, CONFIRMADA)
    ranking.aplicar(1, 7, CONFIRMADA)

    # Assert
    assert ranking.versao() == antes + 2


def test_ordem_e_total_decrescente_e_no_empate_id_do_espaco_crescente(ranking):
    # Arrange
    _montar(
        ranking,
        *_confirmadas(30, 2, 1),
        *_confirmadas(5, 3, 10),
        *_confirmadas(20, 2, 20),
    )

    # Assert
    assert ranking.top(10) == ((5, 3), (20, 2), (30, 2))


def test_empate_com_ids_de_um_e_dois_digitos_segue_o_valor_numerico(ranking):
    # Arrange: como texto, "10" < "9"
    _montar(ranking, *_confirmadas(10, 1, 1), *_confirmadas(9, 1, 5))

    # Assert
    assert ranking.top(10) == ((9, 1), (10, 1))


def test_empate_que_atravessa_o_limite_fica_com_os_menores_ids(ranking):
    # Arrange: texto reverso "100" > "11" > "10", numérico 10 < 11 < 100
    _montar(
        ranking,
        *_confirmadas(100, 1, 1),
        *_confirmadas(11, 1, 5),
        *_confirmadas(10, 1, 10),
        *_confirmadas(9, 1, 15),
    )

    # Assert
    assert ranking.top(1) == ((9, 1),)
    assert ranking.top(2) == ((9, 1), (10, 1))
    assert ranking.top(3) == ((9, 1), (10, 1), (11, 1))


def test_empate_na_fronteira_com_espacos_acima_do_corte(ranking):
    # Arrange
    _montar(
        ranking,
        *_confirmadas(50, 3, 1),
        *_confirmadas(100, 2, 10),
        *_confirmadas(11, 2, 20),
        *_confirmadas(10, 2, 30),
        *_confirmadas(9, 1, 40),
    )

    # Assert
    assert ranking.top(2) == ((50, 3), (10, 2))
    assert ranking.top(3) == ((50, 3), (10, 2), (11, 2))
    assert ranking.top(4) == ((50, 3), (10, 2), (11, 2), (100, 2))


def test_limite_maior_que_os_espacos_devolve_todos(ranking):
    _montar(ranking, *_confirmadas(1, 1, 1), *_confirmadas(2, 1, 5))

    assert ranking.top(20) == ((1, 1), (2, 1))


@pytest.mark.parametrize("limite", [0, -1])
def test_top_com_limite_invalido_lanca_value_error(ranking, limite):
    with pytest.raises(ValueError, match="limite"):
        ranking.top(limite)


def test_substituir_monta_do_zero_so_com_as_reservas_que_contam(ranking):
    # Act
    _montar(
        ranking,
        _registro(1, 7, CONFIRMADA),
        _registro(2, 7, CONCLUIDA),
        _registro(3, 8, CONFIRMADA),
        _registro(4, 8, SOLICITADA),
        _registro(5, 9, RECUSADA),
        _registro(6, 9, CANCELADA),
    )

    # Assert
    assert ranking.top(10) == ((7, 2), (8, 1))


def test_substituir_remove_o_que_sobrou_de_antes(ranking):
    # Arrange
    _montar(ranking, *_confirmadas(7, 3, 1))

    # Act
    _montar(ranking, *_confirmadas(8, 1, 10))

    # Assert
    assert ranking.top(10) == ((8, 1),)


def test_substituir_com_banco_sem_reservas_que_contam_deixa_montado_e_vazio(ranking):
    # Arrange
    _montar(ranking, *_confirmadas(7, 3, 1))

    # Act
    _montar(ranking, _registro(1, 7, CANCELADA))

    # Assert
    assert ranking.top(10) == ()


def test_substituir_de_novo_com_os_mesmos_dados_e_idempotente(ranking):
    # Arrange
    registros = [*_confirmadas(7, 2, 1), *_confirmadas(8, 1, 5)]
    _montar(ranking, *registros)
    antes = ranking.top(10)

    # Act
    _montar(ranking, *registros)

    # Assert
    assert ranking.top(10) == antes == ((7, 2), (8, 1))


def test_substituir_descarta_e_devolve_false_se_a_versao_avancou(ranking):
    # Arrange
    _montar(ranking, *_confirmadas(7, 1, 1))
    versao_lida = ranking.versao()
    ranking.aplicar(50, 7, CONFIRMADA)

    # Act
    trocou = ranking.substituir(_confirmadas(8, 4, 100), versao=versao_lida)

    # Assert
    assert trocou is False
    assert ranking.top(10) == ((7, 2),)


def test_substituir_descartado_com_o_ranking_nao_montado_continua_nao_montado(
    ranking,
):
    # Arrange
    versao_lida = ranking.versao()
    ranking.aplicar(1, 7, CONFIRMADA)

    # Act
    trocou = ranking.substituir(_confirmadas(8, 1, 10), versao=versao_lida)

    # Assert
    assert trocou is False
    assert ranking.top(10) is None


def test_substituir_aceita_um_gerador_de_registros(ranking):
    # Arrange
    gerador = (_registro(i, 7, CONFIRMADA) for i in range(1, 4))

    # Act
    trocou = ranking.substituir(gerador, versao=ranking.versao())

    # Assert
    assert trocou is True
    assert ranking.top(10) == ((7, 3),)


def test_depois_de_substituir_o_livro_vale_para_as_proximas_aplicacoes(ranking):
    # Arrange
    _montar(ranking, *_confirmadas(7, 2, 1))

    # Act
    ranking.aplicar(1, 7, CONFIRMADA)
    ranking.aplicar(2, 7, CANCELADA)

    # Assert
    assert ranking.top(10) == ((7, 1),)


def test_fake_indisponivel_lanca_ranking_indisponivel():
    # Arrange
    ranking = RankingDeEspacosEmMemoria(indisponivel=True)

    # Act e Assert
    for operacao in (
        lambda: ranking.aplicar(1, 7, CONFIRMADA),
        lambda: ranking.top(5),
        lambda: ranking.versao(),
        lambda: ranking.substituir([], versao=0),
    ):
        with pytest.raises(RankingIndisponivel):
            operacao()


def _chave(nome: str) -> str:
    return cache.make_key(nome)


def _redis():
    return cliente(_chave("ranking:montado"), escrita=True)


def _chaves_do_ranking() -> set[str]:
    return {texto(chave) for chave in _redis().keys(_chave("ranking:*"))}


def test_as_chaves_seguem_a_grafia_da_dec_28():
    # Arrange
    ranking = RankingDeEspacosRedis()

    # Act
    _montar(ranking, *_confirmadas(7, 1, 1))
    ranking.aplicar(2, 7, CONFIRMADA)

    # Assert
    assert _chaves_do_ranking() == {
        _chave("ranking:espacos"),
        _chave("ranking:contadas"),
        _chave("ranking:montado"),
        _chave("ranking:versao"),
    }


def test_o_conjunto_guarda_o_id_do_espaco_com_o_total_como_score():
    # Arrange
    ranking = RankingDeEspacosRedis()
    _montar(ranking, *_confirmadas(7, 3, 1))

    # Act
    pontuacao = _redis().zscore(_chave("ranking:espacos"), "7")

    # Assert
    assert pontuacao == 3


def test_o_livro_liga_cada_reserva_contada_ao_seu_espaco():
    # Arrange
    ranking = RankingDeEspacosRedis()
    _montar(ranking, _registro(41, 7, CONFIRMADA), _registro(42, 7, SOLICITADA))

    # Act
    livro = {
        texto(campo): texto(valor)
        for campo, valor in _redis().hgetall(_chave("ranking:contadas")).items()
    }

    # Assert
    assert livro == {"41": "7"}


def test_sinal_montado_vale_um():
    # Arrange
    _montar(RankingDeEspacosRedis())

    # Assert
    assert texto(_redis().get(_chave("ranking:montado"))) == "1"


def test_as_chaves_definitivas_ficam_sem_prazo_de_expiracao():
    # Arrange
    _montar(RankingDeEspacosRedis(), *_confirmadas(7, 2, 1))

    # Assert
    for nome in ("espacos", "contadas", "montado"):
        assert _redis().ttl(_chave(f"ranking:{nome}")) == -1


def test_substituir_nao_deixa_chave_temporaria_para_tras():
    # Arrange
    ranking = RankingDeEspacosRedis()

    # Act
    _montar(ranking, *_confirmadas(7, 3, 1))
    ranking.substituir(_confirmadas(7, 1, 50), versao=-1)

    # Assert
    assert _redis().keys(_chave("ranking:tmp:*")) == []


def test_as_temporarias_nascem_com_prazo(monkeypatch):
    # Arrange
    prazos = []
    original = RankingDeEspacosRedis._montar_temporarias

    def espiar(self, registros, ranking, livro):
        criadas = original(self, registros, ranking, livro)
        prazos.extend(_redis().ttl(chave) for chave in criadas)
        return criadas

    monkeypatch.setattr(RankingDeEspacosRedis, "_montar_temporarias", espiar)

    # Act
    _montar(RankingDeEspacosRedis(), *_confirmadas(7, 1, 1))

    # Assert
    assert len(prazos) == 2
    assert all(0 < prazo <= ranking_redis.TTL_DAS_TEMPORARIAS for prazo in prazos)


def test_lote_sem_reserva_que_conta_renova_o_prazo_do_livro_temporario(monkeypatch):
    # Arrange
    monkeypatch.setattr(ranking_redis, "LOTE_DE_GRAVACAO", 1)
    prazo_quase_vencido = 5

    def registros():
        yield _registro(1, 7, CONFIRMADA)
        for chave in _redis().keys(_chave("ranking:tmp:*")):
            _redis().expire(chave, prazo_quase_vencido)
        yield _registro(2, 7, RECUSADA)

    prazos = []
    original = RankingDeEspacosRedis._montar_temporarias

    def espiar(self, registros, ranking, livro):
        criadas = original(self, registros, ranking, livro)
        prazos.append(_redis().ttl(livro))
        return criadas

    monkeypatch.setattr(RankingDeEspacosRedis, "_montar_temporarias", espiar)

    # Act
    resultado = RankingDeEspacosRedis().substituir(registros(), versao=0)

    # Assert
    assert resultado is True
    assert prazos[0] > prazo_quase_vencido


def test_falha_no_meio_apaga_as_temporarias_e_sobe_ranking_indisponivel(monkeypatch):
    # Arrange
    ranking = RankingDeEspacosRedis()

    def registros_com_falha():
        yield _registro(1, 7, CONFIRMADA)
        raise RedisError("caiu no meio")

    # Act
    with pytest.raises(RankingIndisponivel):
        ranking.substituir(registros_com_falha(), versao=0)

    # Assert
    assert _redis().keys(_chave("ranking:tmp:*")) == []
    assert ranking.top(5) is None


def test_a_troca_e_atomica_nenhuma_leitura_ve_metade_nova_metade_velha():
    # Arrange
    ranking = RankingDeEspacosRedis()
    _montar(ranking, *_confirmadas(7, 2, 1))

    # Act
    _montar(ranking, *_confirmadas(8, 3, 100))

    # Assert
    assert ranking.top(5) == ((8, 3),)
    assert _redis().hlen(_chave("ranking:contadas")) == 3


def test_script_flush_nao_quebra_aplicar_nem_substituir():
    # Arrange
    ranking = RankingDeEspacosRedis()
    _montar(ranking, *_confirmadas(7, 1, 1))

    # Act
    _redis().script_flush()
    ranking.aplicar(2, 7, CONFIRMADA)
    _redis().script_flush()
    _montar(ranking, *_confirmadas(7, 2, 1))

    # Assert
    assert ranking.top(5) == ((7, 2),)


def test_chave_com_tipo_errado_vira_ranking_indisponivel():
    # Arrange
    ranking = RankingDeEspacosRedis()
    _montar(ranking)
    _redis().delete(_chave("ranking:espacos"))
    _redis().set(_chave("ranking:espacos"), "lixo")

    # Act e Assert
    with pytest.raises(RankingIndisponivel):
        ranking.top(5)
    with pytest.raises(RankingIndisponivel):
        ranking.aplicar(1, 7, CONFIRMADA)


@pytest.mark.parametrize(
    "operacao",
    [
        lambda r: r.aplicar(1, 7, CONFIRMADA),
        lambda r: r.top(5),
        lambda r: r.versao(),
        lambda r: r.substituir([_registro(1)], versao=0),
    ],
)
def test_erro_do_redis_vira_ranking_indisponivel_e_e_logado(
    monkeypatch, caplog, operacao
):
    # Arrange
    def falhar(*args, **kwargs):
        raise RedisError("Redis fora do ar")

    monkeypatch.setattr(ranking_redis, "cliente", falhar)

    # Act
    with caplog.at_level(logging.ERROR), pytest.raises(RankingIndisponivel):
        operacao(RankingDeEspacosRedis())

    # Assert
    assert "Redis indisponível no ranking de espaços" in caplog.text


def test_temporarias_que_nao_puderam_ser_apagadas_ficam_para_o_ttl(monkeypatch, caplog):
    # Arrange
    def falhar(*args, **kwargs):
        raise RedisError("sem conexão")

    # Act
    monkeypatch.setattr(ranking_redis, "cliente", falhar)
    with caplog.at_level(logging.WARNING):
        ranking_redis._apagar(["chave"])

    # Assert
    assert "o TTL as remove" in caplog.text
