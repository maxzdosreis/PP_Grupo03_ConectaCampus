from datetime import datetime

import pytest

from reservas.domain.excecoes import ReservaNaoEncontrada
from reservas.domain.registro_de_situacao import (
    SITUACAO_PEDIDA_MAXIMO_CARACTERES,
    RegistroDeSituacao,
    ResultadoDoRegistro,
)
from reservas.domain.reserva import MOTIVO_MAXIMO_CARACTERES
from reservas.domain.situacao import SituacaoReserva
from reservas.tests.fakes import (
    AGORA,
    ATOR_ANA,
    GESTOR,
    OUTRA_PESSOA,
    exatamente,
    reserva_reconstituida,
)

S = SituacaoReserva
R = ResultadoDoRegistro
CODIGO = "ACAO_NAO_PERMITIDA"
PEDIDA_NO_LIMITE = "X" * SITUACAO_PEDIDA_MAXIMO_CARACTERES


def _registro_recusado(**sobrescritas) -> RegistroDeSituacao:
    dados = {
        "situacao_anterior": S.SOLICITADA,
        "situacao_nova": S.SOLICITADA,
        "motivo": None,
        "autor_usuario_id": 7,
        "autor_nome": "Ana Souza",
        "registrado_em": AGORA,
        "resultado": R.RECUSADA,
        "codigo_do_erro": CODIGO,
        "situacao_pedida": "CONFIRMADA",
    }
    dados.update(sobrescritas)
    return RegistroDeSituacao(**dados)


def _registro_aceito(**sobrescritas) -> RegistroDeSituacao:
    dados = {
        "situacao_anterior": S.SOLICITADA,
        "situacao_nova": S.CONFIRMADA,
        "motivo": None,
        "autor_usuario_id": 1,
        "autor_nome": "Gestora de Teste",
        "registrado_em": AGORA,
    }
    dados.update(sobrescritas)
    return RegistroDeSituacao(**dados)


def _tentativa(reserva, pedida=S.CONFIRMADA, **sobrescritas):
    dados = {
        "motivo": None,
        "ator": ATOR_ANA,
        "agora": AGORA,
        "codigo_do_erro": CODIGO,
    }
    dados.update(sobrescritas)
    return reserva.registrar_tentativa_recusada(pedida, **dados)


def test_registro_recusado_guarda_o_que_foi_pedido_e_o_codigo_do_erro():
    # Act
    registro = _registro_recusado(motivo="Preciso do espaço")

    # Assert
    assert registro.resultado is R.RECUSADA
    assert registro.codigo_do_erro == CODIGO
    assert registro.situacao_pedida == "CONFIRMADA"
    assert registro.situacao_anterior is registro.situacao_nova is S.SOLICITADA
    assert registro.motivo == "Preciso do espaço"


def test_registro_aceito_mantem_o_comportamento_anterior():
    # Act
    registro = _registro_aceito()

    # Assert
    assert registro.resultado is R.ACEITA
    assert registro.codigo_do_erro is None
    assert registro.situacao_pedida == "CONFIRMADA"


def test_registro_aceito_pode_informar_a_situacao_pedida_igual_a_nova():
    # Act
    registro = _registro_aceito(
        situacao_anterior=None,
        situacao_nova=S.SOLICITADA,
        situacao_pedida="SOLICITADA",
    )

    # Assert
    assert registro.situacao_pedida == "SOLICITADA"


@pytest.mark.parametrize(
    ("sobrescritas", "mensagem"),
    [
        ({"codigo_do_erro": "X"}, "Um registro aceito não tem codigo_do_erro."),
        (
            {"situacao_pedida": "CANCELADA"},
            "Um registro aceito pede a própria situacao_nova.",
        ),
        (
            {"situacao_anterior": S.CONFIRMADA},
            "situacao_anterior deve ser diferente de situacao_nova.",
        ),
    ],
    ids=["com-codigo", "pedida-diferente", "anterior-igual-a-nova"],
)
def test_registro_aceito_invalido_e_erro_de_programacao(sobrescritas, mensagem):
    # Act / Assert
    with pytest.raises(ValueError, match=exatamente(mensagem)):
        _registro_aceito(**sobrescritas)


MUDA = "Uma tentativa recusada não muda a situação da reserva."
SEM_CODIGO = "codigo_do_erro é obrigatório numa tentativa recusada."
SEM_PEDIDA = "situacao_pedida é obrigatória numa tentativa recusada."
PEDIDA_LONGA = (
    f"situacao_pedida deve ter até {SITUACAO_PEDIDA_MAXIMO_CARACTERES} caracteres."
)


@pytest.mark.parametrize(
    ("sobrescritas", "mensagem"),
    [
        ({"situacao_anterior": S.CONFIRMADA}, MUDA),
        ({"situacao_anterior": None}, MUDA),
        ({"codigo_do_erro": None}, SEM_CODIGO),
        ({"codigo_do_erro": ""}, SEM_CODIGO),
        ({"situacao_pedida": None}, SEM_PEDIDA),
        ({"situacao_pedida": ""}, SEM_PEDIDA),
        ({"situacao_pedida": PEDIDA_NO_LIMITE + "X"}, PEDIDA_LONGA),
    ],
    ids=[
        "muda-a-situacao",
        "sem-anterior",
        "sem-codigo-none",
        "sem-codigo-vazio",
        "sem-pedida-none",
        "sem-pedida-vazia",
        "pedida-longa-demais",
    ],
)
def test_registro_recusado_invalido_e_erro_de_programacao(sobrescritas, mensagem):
    # Act / Assert
    with pytest.raises(ValueError, match=exatamente(mensagem)):
        _registro_recusado(**sobrescritas)


def test_registro_recusado_aceita_o_texto_no_limite():
    # Act
    registro = _registro_recusado(situacao_pedida=PEDIDA_NO_LIMITE)

    # Assert
    assert registro.situacao_pedida == PEDIDA_NO_LIMITE


def test_tentativa_recusada_tem_ator_momento_pedida_resultado_e_codigo():
    # Arrange
    reserva = reserva_reconstituida()

    # Act
    registro = _tentativa(reserva)

    # Assert
    assert registro == RegistroDeSituacao(
        situacao_anterior=S.SOLICITADA,
        situacao_nova=S.SOLICITADA,
        motivo=None,
        autor_usuario_id=ATOR_ANA.usuario_id,
        autor_nome=ATOR_ANA.nome,
        registrado_em=AGORA,
        resultado=R.RECUSADA,
        codigo_do_erro=CODIGO,
        situacao_pedida="CONFIRMADA",
    )


def test_tentativa_recusada_nao_altera_a_reserva_nem_os_pendentes():
    # Arrange
    reserva = reserva_reconstituida(situacao=S.CONFIRMADA)

    # Act
    _tentativa(reserva, S.CONCLUIDA, ator=GESTOR)

    # Assert
    assert reserva.situacao is S.CONFIRMADA
    assert reserva.registros_pendentes == ()


def test_tentativa_recusada_usa_o_agora_recebido_e_nao_o_relogio_do_sistema():
    # Arrange
    reserva = reserva_reconstituida()
    no_passado = datetime(2001, 1, 1, 8, 0, tzinfo=AGORA.tzinfo)

    # Act
    registro = _tentativa(reserva, agora=no_passado)

    # Assert
    assert registro.registrado_em is no_passado


def test_tentativa_recusada_sem_fuso_e_erro_de_programacao():
    # Arrange
    reserva = reserva_reconstituida()

    # Act / Assert
    with pytest.raises(
        TypeError, match=exatamente("agora deve ser um datetime com fuso horário.")
    ):
        _tentativa(reserva, agora=datetime(2026, 10, 21, 12, 0))


def test_tentativa_de_quem_nao_ve_a_reserva_e_nao_encontrada():
    # Arrange
    reserva = reserva_reconstituida()

    # Act / Assert
    with pytest.raises(ReservaNaoEncontrada):
        _tentativa(reserva, ator=OUTRA_PESSOA)


@pytest.mark.parametrize(
    ("pedida", "esperada"),
    [
        (S.CONFIRMADA, "CONFIRMADA"),
        ("CONFIRMADA", "CONFIRMADA"),
        ("  situação   estranha ", "situação estranha"),
        ("X" * 50, PEDIDA_NO_LIMITE),
    ],
    ids=["enum", "texto", "espacos-normalizados", "truncada"],
)
def test_situacao_pedida_e_gravada_como_texto_normalizado_e_limitado(pedida, esperada):
    # Arrange
    reserva = reserva_reconstituida()

    # Act
    registro = _tentativa(reserva, pedida)

    # Assert
    assert registro.situacao_pedida == esperada


@pytest.mark.parametrize(
    ("motivo", "esperado"),
    [
        (None, None),
        ("   ", None),
        ("  Chuva   forte ", "Chuva forte"),
        ("m" * (MOTIVO_MAXIMO_CARACTERES + 50), "m" * MOTIVO_MAXIMO_CARACTERES),
    ],
    ids=["ausente", "so-espacos", "normalizado", "truncado"],
)
def test_motivo_da_tentativa_e_normalizado_e_cortado_em_vez_de_recusado(
    motivo, esperado
):
    # Arrange
    reserva = reserva_reconstituida()

    # Act
    registro = _tentativa(reserva, motivo=motivo)

    # Assert
    assert registro.motivo == esperado
