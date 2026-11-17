import logging

import pytest

from compartilhado.domain.erros import CampoObrigatorioAusente, DadosInvalidos
from reservas.application.casos_de_uso import AlterarSituacaoReserva
from reservas.domain.excecoes import (
    AlteracaoDeSituacaoNaoPermitida,
    ConclusaoAntesDoTermino,
    MotivoObrigatorio,
    MudancaAposOInicio,
    ReservaDesatualizada,
    ReservaNaoEncontrada,
    SituacaoInvalida,
    TransicaoDeSituacaoInvalida,
)
from reservas.domain.registro_de_situacao import ResultadoDoRegistro
from reservas.domain.situacao import SituacaoReserva
from reservas.tests.fakes import (
    AGORA,
    ATOR_ANA,
    DEPOIS_DO_TERMINO,
    GESTOR,
    MOTIVO,
    OUTRA_PESSOA,
    RepositorioReservasEmMemoria,
    relogio_em,
    reserva_reconstituida,
)

S = SituacaoReserva


@pytest.fixture
def repositorio():
    return RepositorioReservasEmMemoria()


def _salvar_em(repositorio, situacao):
    return repositorio.salvar(reserva_reconstituida(id=None, situacao=situacao))


def _tentar(repositorio, reserva, nova, ator, *, motivo=None, agora=AGORA):
    return AlterarSituacaoReserva(repositorio, relogio_em(agora)).executar(
        reserva_id=reserva.id, nova_situacao=nova, motivo=motivo, ator=ator
    )


CASOS_RECUSADOS = [
    (S.SOLICITADA, S.CONFIRMADA, ATOR_ANA, None, AGORA,
     AlteracaoDeSituacaoNaoPermitida, "ACAO_NAO_PERMITIDA"),
    (S.CONCLUIDA, S.CANCELADA, GESTOR, MOTIVO, AGORA,
     TransicaoDeSituacaoInvalida, "TRANSICAO_DE_SITUACAO_INVALIDA"),
    (S.CONFIRMADA, S.CONCLUIDA, GESTOR, None, AGORA,
     ConclusaoAntesDoTermino, "CONCLUSAO_ANTES_DO_TERMINO"),
    (S.SOLICITADA, S.RECUSADA, GESTOR, MOTIVO, DEPOIS_DO_TERMINO,
     MudancaAposOInicio, "RECUSA_OU_CANCELAMENTO_APOS_O_INICIO"),
    (S.SOLICITADA, S.RECUSADA, GESTOR, None, AGORA,
     MotivoObrigatorio, "MOTIVO_OBRIGATORIO"),
    (S.SOLICITADA, "ENCERRADA", GESTOR, None, AGORA,
     SituacaoInvalida, "SITUACAO_INVALIDA"),
]  # fmt: skip


@pytest.mark.parametrize(
    ("atual", "pedida", "ator", "motivo", "agora", "erro", "codigo"),
    CASOS_RECUSADOS,
    ids=[caso[-1] for caso in CASOS_RECUSADOS],
)
def test_tentativa_recusada_gera_um_registro_e_relanca_a_excecao_original(
    repositorio, atual, pedida, ator, motivo, agora, erro, codigo
):
    # Arrange
    reserva = _salvar_em(repositorio, atual)

    # Act
    with pytest.raises(erro) as capturada:
        _tentar(repositorio, reserva, pedida, ator, motivo=motivo, agora=agora)

    # Assert
    assert type(capturada.value) is erro
    assert capturada.value.codigo == codigo
    (registro,) = repositorio.listar_historico(reserva.id)
    assert registro.resultado is ResultadoDoRegistro.RECUSADA
    assert registro.codigo_do_erro == codigo
    assert registro.situacao_pedida == str(pedida)
    assert registro.situacao_anterior is registro.situacao_nova is atual
    assert registro.autor_usuario_id == ator.usuario_id
    assert registro.autor_nome == ator.nome
    assert registro.registrado_em == agora
    assert repositorio.obter_por_id(reserva.id).situacao is atual


def test_tentativa_recusada_guarda_o_motivo_informado(repositorio):
    # Arrange
    reserva = _salvar_em(repositorio, S.CONFIRMADA)

    # Act
    with pytest.raises(ConclusaoAntesDoTermino):
        _tentar(repositorio, reserva, S.CONCLUIDA, GESTOR, motivo="  Fim  do   jogo ")

    # Assert
    assert repositorio.listar_historico(reserva.id)[0].motivo == "Fim do jogo"


def test_motivo_longo_demais_e_recusado_e_a_tentativa_guarda_o_texto_cortado(
    repositorio,
):
    # Arrange
    reserva = _salvar_em(repositorio, S.CONFIRMADA)

    # Act
    with pytest.raises(DadosInvalidos) as capturada:
        _tentar(repositorio, reserva, S.CANCELADA, GESTOR, motivo="m" * 400)

    # Assert
    assert capturada.value.codigo == "TEXTO_MUITO_LONGO"
    (registro,) = repositorio.listar_historico(reserva.id)
    assert registro.codigo_do_erro == "TEXTO_MUITO_LONGO"
    assert registro.motivo == "m" * 300


def test_tentativa_aceita_nao_gera_registro_de_recusa(repositorio):
    # Arrange
    reserva = _salvar_em(repositorio, S.SOLICITADA)

    # Act
    _tentar(repositorio, reserva, S.CONFIRMADA, GESTOR)

    # Assert
    (registro,) = repositorio.listar_historico(reserva.id)
    assert registro.resultado is ResultadoDoRegistro.ACEITA
    assert registro.codigo_do_erro is None
    assert repositorio.tentativas_registradas == 0


def test_duas_recusas_seguidas_geram_dois_registros_em_ordem(repositorio):
    # Arrange
    reserva = _salvar_em(repositorio, S.SOLICITADA)

    # Act
    with pytest.raises(AlteracaoDeSituacaoNaoPermitida):
        _tentar(repositorio, reserva, S.CONFIRMADA, ATOR_ANA)
    with pytest.raises(MotivoObrigatorio):
        _tentar(repositorio, reserva, S.RECUSADA, GESTOR)

    # Assert
    registros = repositorio.listar_historico(reserva.id)
    assert [r.codigo_do_erro for r in registros] == [
        "ACAO_NAO_PERMITIDA",
        "MOTIVO_OBRIGATORIO",
    ]


def test_reserva_de_outra_pessoa_nao_gera_registro(repositorio):
    # Arrange
    reserva = _salvar_em(repositorio, S.SOLICITADA)

    # Act
    with pytest.raises(ReservaNaoEncontrada):
        _tentar(repositorio, reserva, S.CANCELADA, OUTRA_PESSOA, motivo=MOTIVO)

    # Assert
    assert repositorio.listar_historico(reserva.id) == []
    assert repositorio.tentativas_registradas == 0


def test_reserva_inexistente_nao_gera_registro(repositorio):
    # Act / Assert
    with pytest.raises(ReservaNaoEncontrada):
        AlterarSituacaoReserva(repositorio, relogio_em(AGORA)).executar(
            reserva_id=9999, nova_situacao=S.CONFIRMADA, ator=GESTOR
        )
    assert repositorio.tentativas_registradas == 0


@pytest.mark.parametrize(
    ("pedida", "erro"),
    [
        ("", CampoObrigatorioAusente),
        (None, CampoObrigatorioAusente),
        ("   ", SituacaoInvalida),
    ],
    ids=["vazia", "nula", "so-espacos"],
)
def test_situacao_nao_informada_nao_gera_registro(repositorio, pedida, erro):
    # Arrange
    reserva = _salvar_em(repositorio, S.SOLICITADA)

    # Act
    with pytest.raises(erro):
        _tentar(repositorio, reserva, pedida, GESTOR)

    # Assert
    assert repositorio.listar_historico(reserva.id) == []
    assert repositorio.tentativas_registradas == 0


class _RepositorioComSalvarQueFalha(RepositorioReservasEmMemoria):
    def __init__(self, erro: Exception) -> None:
        super().__init__()
        self._erro = erro
        self.falhar = False

    def salvar(self, reserva):
        if self.falhar:
            raise self._erro
        return super().salvar(reserva)


def test_excecao_que_nao_e_de_dominio_nao_gera_registro():
    # Arrange
    repositorio = _RepositorioComSalvarQueFalha(RuntimeError("banco fora do ar"))
    reserva = _salvar_em(repositorio, S.SOLICITADA)
    repositorio.falhar = True

    # Act
    with pytest.raises(RuntimeError, match="banco fora do ar"):
        _tentar(repositorio, reserva, S.CONFIRMADA, GESTOR)

    # Assert
    assert repositorio.listar_historico(reserva.id) == []
    assert repositorio.tentativas_registradas == 0


def test_leitura_desatualizada_vira_tentativa_com_a_situacao_que_o_banco_tem():
    # Arrange
    repositorio = _RepositorioComSalvarQueFalha(ReservaDesatualizada(S.CANCELADA))
    reserva = _salvar_em(repositorio, S.SOLICITADA)
    repositorio.falhar = True

    # Act
    with pytest.raises(ReservaDesatualizada) as capturada:
        _tentar(repositorio, reserva, S.CONFIRMADA, GESTOR)

    # Assert
    assert capturada.value.codigo == "RESERVA_DESATUALIZADA"
    (registro,) = repositorio.listar_historico(reserva.id)
    assert registro.codigo_do_erro == "RESERVA_DESATUALIZADA"
    assert registro.situacao_pedida == "CONFIRMADA"
    assert registro.situacao_anterior is registro.situacao_nova is S.SOLICITADA


def test_falha_ao_registrar_a_tentativa_nao_esconde_o_erro_de_negocio(
    repositorio, caplog
):
    # Arrange
    reserva = _salvar_em(repositorio, S.SOLICITADA)

    def falhar(reserva_id, registro):
        raise RuntimeError("banco fora do ar")

    repositorio.gravar_tentativa_recusada = falhar

    # Act
    with (
        caplog.at_level(logging.ERROR),
        pytest.raises(AlteracaoDeSituacaoNaoPermitida),
    ):
        _tentar(repositorio, reserva, S.CONFIRMADA, ATOR_ANA)

    # Assert
    assert f"reserva {reserva.id}" in caplog.text
    assert repositorio.listar_historico(reserva.id) == []
