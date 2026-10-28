from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import pytest

from compartilhado.api.tratador_de_erros import tratar_excecao
from compartilhado.domain.erros import CampoObrigatorioAusente, TextoMuitoLongo
from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.excecoes import (
    DataRetroativa,
    IdentificadorDeEspacoInvalido,
    MotivoObrigatorio,
    ReservaNaoEncontrada,
    SituacaoInvalida,
    TransicaoDeSituacaoInvalida,
)
from reservas.domain.intervalo_de_horario import IntervaloDeHorario
from reservas.domain.reserva import (
    FINALIDADE_MAXIMO_CARACTERES,
    MOTIVO_MAXIMO_CARACTERES,
    Reserva,
)
from reservas.domain.situacao import SituacaoReserva
from reservas.domain.solicitante import Solicitante

S = SituacaoReserva
SAO_PAULO = ZoneInfo("America/Sao_Paulo")
AGORA = datetime(2026, 10, 21, 12, 0, tzinfo=SAO_PAULO)
SOLICITANTE = Solicitante(usuario_id=7, nome="Ana Souza", matricula="2026001")
GESTOR = Ator(usuario_id=1, papel=PapelDoAtor.GESTOR)

TRANSICOES_PERMITIDAS = [
    (S.SOLICITADA, S.CONFIRMADA),
    (S.SOLICITADA, S.RECUSADA),
    (S.SOLICITADA, S.CANCELADA),
    (S.CONFIRMADA, S.CONCLUIDA),
    (S.CONFIRMADA, S.CANCELADA),
]
TRANSICOES_PROIBIDAS = [
    (atual, nova)
    for atual in SituacaoReserva
    for nova in SituacaoReserva
    if (atual, nova) not in TRANSICOES_PERMITIDAS
]


def _solicitar(**sobrescritas):
    dados = {
        "espaco_id": 3,
        "solicitante": SOLICITANTE,
        "data": date(2026, 10, 25),
        "hora_inicio": time(10, 0),
        "hora_fim": time(11, 0),
        "finalidade": "Treino do time de vôlei",
        "agora": AGORA,
    }
    dados.update(sobrescritas)
    return Reserva.solicitar(**dados)


def _reconstituir(**sobrescritas):
    dados = {
        "id": 12,
        "espaco_id": 3,
        "solicitante": SOLICITANTE,
        "intervalo": IntervaloDeHorario(
            data=date(2026, 10, 25), hora_inicio=time(10, 0), hora_fim=time(11, 0)
        ),
        "finalidade": "Treino do time de vôlei",
        "situacao": S.SOLICITADA,
        "criada_em": AGORA,
    }
    dados.update(sobrescritas)
    dados.setdefault("motivo_da_situacao", _motivo_para(dados["situacao"]))
    return Reserva(**dados)


def _motivo_para(situacao):
    return "Motivo informado" if situacao in (S.RECUSADA, S.CANCELADA) else None


def test_solicitar_cria_reserva_solicitada_com_criada_em_igual_a_agora():
    # Act
    reserva = _solicitar(finalidade="  Treino   do time ")

    # Assert
    assert reserva.id is None
    assert reserva.situacao is S.SOLICITADA
    assert reserva.criada_em == AGORA
    assert reserva.motivo_da_situacao is None
    assert reserva.finalidade == "Treino do time"
    assert reserva.solicitante == SOLICITANTE
    assert reserva.intervalo.inicio() == datetime(2026, 10, 25, 10, tzinfo=SAO_PAULO)


def test_solicitar_com_inicio_igual_a_agora_e_recusado():
    # Act
    with pytest.raises(DataRetroativa) as erro:
        _solicitar(data=AGORA.date(), hora_inicio=time(12, 0), hora_fim=time(13, 0))

    # Assert
    assert erro.value.campo == "data"


def test_solicitar_um_minuto_depois_de_agora_e_aceito():
    # Act
    reserva = _solicitar(
        data=AGORA.date(), hora_inicio=time(12, 1), hora_fim=time(13, 0)
    )

    # Assert
    assert reserva.situacao is S.SOLICITADA


def test_solicitar_para_ontem_e_recusado():
    # Act / Assert
    with pytest.raises(DataRetroativa):
        _solicitar(data=AGORA.date() - timedelta(days=1))


def test_solicitar_compara_agora_em_outro_fuso_pelo_mesmo_instante():
    # Arrange
    agora_utc = datetime(2026, 10, 21, 15, 0, tzinfo=ZoneInfo("UTC"))

    # Act / Assert
    with pytest.raises(DataRetroativa):
        _solicitar(
            data=AGORA.date(),
            hora_inicio=time(11, 30),
            hora_fim=time(12, 30),
            agora=agora_utc,
        )


@pytest.mark.parametrize("agora", [datetime(2026, 10, 21, 12, 0), None])
def test_solicitar_com_agora_sem_fuso_e_erro_de_programacao(agora):
    # Act / Assert
    with pytest.raises(TypeError):
        _solicitar(agora=agora)


@pytest.mark.parametrize("finalidade", ["", "   ", None])
def test_finalidade_vazia_e_recusada(finalidade):
    # Act
    with pytest.raises(CampoObrigatorioAusente) as erro:
        _solicitar(finalidade=finalidade)

    # Assert
    assert erro.value.campo == "finalidade"


def test_finalidade_no_limite_e_aceita():
    # Arrange
    finalidade = "A" * FINALIDADE_MAXIMO_CARACTERES

    # Act
    reserva = _solicitar(finalidade=finalidade)

    # Assert
    assert reserva.finalidade == finalidade


def test_finalidade_acima_do_limite_e_recusada():
    # Act
    with pytest.raises(TextoMuitoLongo) as erro:
        _solicitar(finalidade="A" * (FINALIDADE_MAXIMO_CARACTERES + 1))

    # Assert
    assert erro.value.campo == "finalidade"
    assert erro.value.mensagem == (
        'O campo "Finalidade" deve ter no máximo 200 caracteres.'
    )


def test_espaco_id_vazio_e_recusado_como_obrigatorio():
    # Act
    with pytest.raises(CampoObrigatorioAusente) as erro:
        _solicitar(espaco_id=None)

    # Assert
    assert erro.value.campo == "espaco_id"


@pytest.mark.parametrize("espaco_id", [0, -1, "1", True])
def test_espaco_id_que_nao_e_inteiro_positivo_e_recusado(espaco_id):
    # Act
    with pytest.raises(IdentificadorDeEspacoInvalido) as erro:
        _solicitar(espaco_id=espaco_id)

    # Assert
    assert erro.value.campo == "espaco_id"


def test_reconstituir_reserva_com_data_passada_e_aceito():
    # Arrange
    ontem = IntervaloDeHorario(
        data=AGORA.date() - timedelta(days=1),
        hora_inicio=time(10, 0),
        hora_fim=time(11, 0),
    )

    # Act
    reserva = _reconstituir(intervalo=ontem, situacao=S.CONCLUIDA)

    # Assert
    assert reserva.intervalo == ontem
    assert reserva.situacao is S.CONCLUIDA


def test_reconstituir_aceita_situacao_e_motivo_como_texto():
    # Act
    reserva = _reconstituir(situacao="RECUSADA", motivo_da_situacao="  Chuva  ")

    # Assert
    assert reserva.situacao is S.RECUSADA
    assert reserva.motivo_da_situacao == "Chuva"


@pytest.mark.parametrize("situacao", [S.RECUSADA, S.CANCELADA])
@pytest.mark.parametrize("motivo", [None, "", "   "])
def test_reconstituir_recusada_ou_cancelada_sem_motivo_e_recusado(situacao, motivo):
    # Act
    with pytest.raises(MotivoObrigatorio) as erro:
        _reconstituir(situacao=situacao, motivo_da_situacao=motivo)

    # Assert
    assert erro.value.campo == "motivo"


@pytest.mark.parametrize("situacao", [S.SOLICITADA, S.CONFIRMADA, S.CONCLUIDA])
def test_reconstituir_situacao_que_nao_exige_motivo_sem_motivo_e_aceito(situacao):
    # Act
    reserva = _reconstituir(situacao=situacao, motivo_da_situacao=None)

    # Assert
    assert reserva.situacao is situacao
    assert reserva.motivo_da_situacao is None


@pytest.mark.parametrize(("campo"), ["solicitante", "intervalo", "situacao"])
def test_reconstituir_sem_campo_obrigatorio_e_recusado(campo):
    # Act
    with pytest.raises(CampoObrigatorioAusente) as erro:
        _reconstituir(**{campo: None})

    # Assert
    assert erro.value.campo == campo


def test_reconstituir_com_situacao_desconhecida_e_recusado():
    # Act / Assert
    with pytest.raises(SituacaoInvalida):
        _reconstituir(situacao="PENDENTE")


@pytest.mark.parametrize(
    "criada_em",
    [None, datetime(2026, 10, 21, 12, 0)],
    ids=["ausente", "sem-fuso"],
)
def test_reconstituir_sem_criada_em_com_fuso_e_erro_de_programacao(criada_em):
    # Act / Assert
    with pytest.raises(TypeError, match="criada_em"):
        _reconstituir(criada_em=criada_em)


@pytest.mark.parametrize(("atual", "nova"), TRANSICOES_PERMITIDAS)
def test_transicao_permitida_altera_a_situacao(atual, nova):
    # Arrange
    reserva = _reconstituir(situacao=atual)

    # Act
    reserva.alterar_situacao(nova, motivo=_motivo_para(nova), ator=GESTOR)

    # Assert
    assert reserva.situacao is nova
    assert reserva.motivo_da_situacao == _motivo_para(nova)


@pytest.mark.parametrize(("atual", "nova"), TRANSICOES_PROIBIDAS)
def test_transicao_proibida_e_recusada_e_preserva_a_situacao(atual, nova):
    # Arrange
    reserva = _reconstituir(situacao=atual)
    motivo_antes = reserva.motivo_da_situacao

    # Act
    with pytest.raises(TransicaoDeSituacaoInvalida) as erro:
        reserva.alterar_situacao(nova, motivo="Outro motivo", ator=GESTOR)

    # Assert
    assert reserva.situacao is atual
    assert reserva.motivo_da_situacao == motivo_antes
    assert (erro.value.atual, erro.value.nova) == (atual, nova)


def test_transicao_proibida_tem_mensagem_com_os_rotulos():
    # Arrange
    reserva = _reconstituir(situacao=S.CONCLUIDA)

    # Act
    with pytest.raises(TransicaoDeSituacaoInvalida) as erro:
        reserva.alterar_situacao(S.CANCELADA, motivo="Desistência", ator=GESTOR)

    # Assert
    assert erro.value.mensagem == (
        "Não é possível alterar uma reserva Concluída para Cancelada."
    )


@pytest.mark.parametrize("nova", [S.RECUSADA, S.CANCELADA])
@pytest.mark.parametrize("motivo", [None, "", "   "])
def test_recusar_ou_cancelar_sem_motivo_e_recusado_e_nada_muda(nova, motivo):
    # Arrange
    reserva = _reconstituir(situacao=S.SOLICITADA)

    # Act
    with pytest.raises(MotivoObrigatorio) as erro:
        reserva.alterar_situacao(nova, motivo=motivo, ator=GESTOR)

    # Assert
    assert erro.value.campo == "motivo"
    assert reserva.situacao is S.SOLICITADA
    assert reserva.motivo_da_situacao is None


def test_motivo_acima_do_limite_e_recusado_e_nada_muda():
    # Arrange
    reserva = _reconstituir(situacao=S.SOLICITADA)

    # Act
    with pytest.raises(TextoMuitoLongo) as erro:
        reserva.alterar_situacao(
            S.RECUSADA, motivo="A" * (MOTIVO_MAXIMO_CARACTERES + 1), ator=GESTOR
        )

    # Assert
    assert erro.value.campo == "motivo"
    assert reserva.situacao is S.SOLICITADA


def test_motivo_opcional_ao_confirmar_e_guardado_normalizado():
    # Arrange
    reserva = _reconstituir(situacao=S.SOLICITADA)

    # Act
    reserva.alterar_situacao(
        S.CONFIRMADA, motivo="  Liberada   pela gestão ", ator=GESTOR
    )

    # Assert
    assert reserva.motivo_da_situacao == "Liberada pela gestão"


def test_nova_situacao_limpa_o_motivo_da_anterior():
    # Arrange
    reserva = _reconstituir(situacao=S.CONFIRMADA, motivo_da_situacao="Liberada")

    # Act
    reserva.alterar_situacao(S.CONCLUIDA, ator=GESTOR)

    # Assert
    assert reserva.motivo_da_situacao is None


def test_situacao_como_texto_e_aceita():
    # Arrange
    reserva = _reconstituir(situacao=S.SOLICITADA)

    # Act
    reserva.alterar_situacao("CONFIRMADA", ator=GESTOR)

    # Assert
    assert reserva.situacao is S.CONFIRMADA


def test_situacao_desconhecida_e_recusada_e_nada_muda():
    # Arrange
    reserva = _reconstituir(situacao=S.SOLICITADA)

    # Act
    with pytest.raises(SituacaoInvalida) as erro:
        reserva.alterar_situacao("PENDENTE", ator=GESTOR)

    # Assert
    assert erro.value.campo == "situacao"
    assert erro.value.mensagem == (
        "Situação inválida. Escolha uma destas: "
        "Solicitada, Confirmada, Recusada, Cancelada, Concluída."
    )
    assert reserva.situacao is S.SOLICITADA


def test_reservas_com_mesmo_id_sao_iguais_e_tem_mesmo_hash():
    # Arrange
    primeira = _reconstituir(id=12)
    segunda = _reconstituir(id=12, finalidade="Outra finalidade")

    # Assert
    assert primeira == segunda
    assert hash(primeira) == hash(segunda)


def test_reservas_com_ids_diferentes_sao_diferentes():
    # Assert
    assert _reconstituir(id=12) != _reconstituir(id=13)


def test_reservas_sem_id_so_sao_iguais_a_si_mesmas():
    # Arrange
    reserva = _solicitar()

    # Assert
    assert reserva == reserva
    assert reserva != _solicitar()
    assert hash(reserva) == hash(reserva)


def test_reserva_nao_e_igual_a_outro_tipo():
    # Assert
    assert _reconstituir() != 12


def test_str_mostra_id_horario_e_situacao():
    # Assert
    assert str(_reconstituir()) == "Reserva #12 — 25/10/2026 10:00–11:00 (Solicitada)"


def test_str_de_reserva_sem_id():
    # Assert
    assert str(_solicitar()) == "Reserva nova — 25/10/2026 10:00–11:00 (Solicitada)"


def test_repr_mostra_id_e_situacao():
    # Act
    texto = repr(_reconstituir())

    # Assert
    assert texto.startswith("Reserva(id=12, espaco_id=3, ")
    assert "situacao=<SituacaoReserva.SOLICITADA: 'SOLICITADA'>" in texto


def test_transicao_invalida_vira_409_sem_campos():
    # Act
    resposta = tratar_excecao(TransicaoDeSituacaoInvalida(S.CONCLUIDA, S.CANCELADA), {})

    # Assert
    assert resposta.status_code == 409
    assert resposta.data == {
        "erro": {
            "codigo": "TRANSICAO_DE_SITUACAO_INVALIDA",
            "mensagem": "Não é possível alterar uma reserva Concluída para Cancelada.",
        }
    }


def test_motivo_obrigatorio_vira_400_marcando_o_campo():
    # Act
    resposta = tratar_excecao(MotivoObrigatorio(), {})

    # Assert
    mensagem = "Informe o motivo para recusar ou cancelar a reserva."
    assert resposta.status_code == 400
    assert resposta.data == {
        "erro": {
            "codigo": "MOTIVO_OBRIGATORIO",
            "mensagem": mensagem,
            "campos": {"motivo": [mensagem]},
        }
    }


def test_data_retroativa_vira_400_marcando_o_campo():
    # Act
    resposta = tratar_excecao(DataRetroativa(), {})

    # Assert
    mensagem = "Não é possível reservar um horário que já passou."
    assert resposta.status_code == 400
    assert resposta.data == {
        "erro": {
            "codigo": "DATA_RETROATIVA",
            "mensagem": mensagem,
            "campos": {"data": [mensagem]},
        }
    }


def test_reserva_nao_encontrada_vira_404():
    # Act
    resposta = tratar_excecao(ReservaNaoEncontrada(99), {})

    # Assert
    assert resposta.status_code == 404
    assert resposta.data == {
        "erro": {
            "codigo": "RESERVA_NAO_ENCONTRADA",
            "mensagem": "Reserva de código 99 não encontrada.",
        }
    }
