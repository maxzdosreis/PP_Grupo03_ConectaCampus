from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import pytest

from compartilhado.api.tratador_de_erros import tratar_excecao
from compartilhado.domain.erros import CampoObrigatorioAusente, TextoMuitoLongo
from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.excecoes import (
    AlteracaoDeSituacaoNaoPermitida,
    DataRetroativa,
    DuracaoInvalida,
    ForaDoHorarioDeFuncionamento,
    IdentificadorDeEspacoInvalido,
    MotivoObrigatorio,
    ReservaDesatualizada,
    ReservaNaoEncontrada,
    SituacaoInvalida,
    TransicaoDeSituacaoInvalida,
)
from reservas.domain.intervalo_de_horario import IntervaloDeHorario
from reservas.domain.registro_de_situacao import RegistroDeSituacao
from reservas.domain.reserva import (
    FINALIDADE_MAXIMO_CARACTERES,
    MOTIVO_MAXIMO_CARACTERES,
    Reserva,
)
from reservas.domain.situacao import SituacaoReserva
from reservas.domain.solicitante import Solicitante
from reservas.tests.historico import verificar_historico_coerente

S = SituacaoReserva
SAO_PAULO = ZoneInfo("America/Sao_Paulo")
AGORA = datetime(2026, 10, 21, 12, 0, tzinfo=SAO_PAULO)
SOLICITANTE = Solicitante(usuario_id=7, nome="Ana Souza", matricula="2026001")
GESTOR = Ator(usuario_id=1, nome="Gestora de Teste", papel=PapelDoAtor.GESTOR)

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


def test_solicitar_fora_do_horario_de_funcionamento_e_recusado():
    # Act
    with pytest.raises(ForaDoHorarioDeFuncionamento) as erro:
        _solicitar(hora_inicio=time(22, 0), hora_fim=time(23, 0))

    # Assert
    assert erro.value.campo == "hora_fim"


def test_data_retroativa_e_checada_antes_do_horario_de_funcionamento():
    # Act / Assert
    with pytest.raises(DataRetroativa):
        _solicitar(
            data=AGORA.date() - timedelta(days=1),
            hora_inicio=time(5, 0),
            hora_fim=time(6, 0),
        )


def test_horario_de_funcionamento_e_checado_antes_da_duracao():
    # Act / Assert
    with pytest.raises(ForaDoHorarioDeFuncionamento):
        _solicitar(hora_inicio=time(5, 0), hora_fim=time(9, 0))


def test_duracao_e_checada_antes_da_antecedencia():
    # Act / Assert
    with pytest.raises(DuracaoInvalida):
        _solicitar(
            data=AGORA.date() + timedelta(days=31),
            hora_inicio=time(10, 0),
            hora_fim=time(14, 0),
        )


def test_reconstituir_reserva_fora_das_regras_de_agenda_e_aceito():
    # Arrange
    tarde_da_noite_e_distante = IntervaloDeHorario(
        data=AGORA.date() + timedelta(days=60),
        hora_inicio=time(23, 30),
        hora_fim=time(23, 59),
    )

    # Act
    reserva = _reconstituir(intervalo=tarde_da_noite_e_distante)

    # Assert
    assert reserva.intervalo == tarde_da_noite_e_distante
    assert reserva.situacao is S.SOLICITADA


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
    reserva.alterar_situacao(nova, motivo=_motivo_para(nova), ator=GESTOR, agora=AGORA)

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
        reserva.alterar_situacao(nova, motivo="Outro motivo", ator=GESTOR, agora=AGORA)

    # Assert
    assert reserva.situacao is atual
    assert reserva.motivo_da_situacao == motivo_antes
    assert (erro.value.atual, erro.value.nova) == (atual, nova)


def test_transicao_proibida_tem_mensagem_com_os_rotulos():
    # Arrange
    reserva = _reconstituir(situacao=S.CONCLUIDA)

    # Act
    with pytest.raises(TransicaoDeSituacaoInvalida) as erro:
        reserva.alterar_situacao(
            S.CANCELADA, motivo="Desistência", ator=GESTOR, agora=AGORA
        )

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
        reserva.alterar_situacao(nova, motivo=motivo, ator=GESTOR, agora=AGORA)

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
            S.RECUSADA,
            motivo="A" * (MOTIVO_MAXIMO_CARACTERES + 1),
            ator=GESTOR,
            agora=AGORA,
        )

    # Assert
    assert erro.value.campo == "motivo"
    assert reserva.situacao is S.SOLICITADA


def test_motivo_opcional_ao_confirmar_e_guardado_normalizado():
    # Arrange
    reserva = _reconstituir(situacao=S.SOLICITADA)

    # Act
    reserva.alterar_situacao(
        S.CONFIRMADA,
        motivo="  Liberada   pela gestão ",
        ator=GESTOR,
        agora=AGORA,
    )

    # Assert
    assert reserva.motivo_da_situacao == "Liberada pela gestão"


def test_nova_situacao_limpa_o_motivo_da_anterior():
    # Arrange
    reserva = _reconstituir(situacao=S.CONFIRMADA, motivo_da_situacao="Liberada")

    # Act
    reserva.alterar_situacao(S.CONCLUIDA, ator=GESTOR, agora=AGORA)

    # Assert
    assert reserva.motivo_da_situacao is None


def test_situacao_como_texto_e_aceita():
    # Arrange
    reserva = _reconstituir(situacao=S.SOLICITADA)

    # Act
    reserva.alterar_situacao("CONFIRMADA", ator=GESTOR, agora=AGORA)

    # Assert
    assert reserva.situacao is S.CONFIRMADA


def test_situacao_desconhecida_e_recusada_e_nada_muda():
    # Arrange
    reserva = _reconstituir(situacao=S.SOLICITADA)

    # Act
    with pytest.raises(SituacaoInvalida) as erro:
        reserva.alterar_situacao("PENDENTE", ator=GESTOR, agora=AGORA)

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


ATOR_SOLICITANTE = Ator(
    usuario_id=SOLICITANTE.usuario_id,
    nome=SOLICITANTE.nome,
    papel=PapelDoAtor.SOLICITANTE,
)
OUTRO_SOLICITANTE = Ator(
    usuario_id=99, nome="Outra Pessoa", papel=PapelDoAtor.SOLICITANTE
)
DEPOIS = AGORA + timedelta(hours=2)


def test_solicitar_gera_o_registro_de_criacao_pendente():
    # Act
    reserva = _solicitar()

    # Assert
    assert reserva.registros_pendentes == (
        RegistroDeSituacao(
            situacao_anterior=None,
            situacao_nova=S.SOLICITADA,
            motivo=None,
            autor_usuario_id=SOLICITANTE.usuario_id,
            autor_nome=SOLICITANTE.nome,
            registrado_em=AGORA,
        ),
    )


def test_reconstituir_comeca_sem_registros_pendentes():
    # Assert
    assert _reconstituir().registros_pendentes == ()


@pytest.mark.parametrize(("atual", "nova"), TRANSICOES_PERMITIDAS)
def test_transicao_permitida_gera_o_registro_da_mudanca(atual, nova):
    # Arrange
    reserva = _reconstituir(situacao=atual)

    # Act
    reserva.alterar_situacao(
        nova, motivo=f"  {_motivo_para(nova) or ''} ", ator=GESTOR, agora=DEPOIS
    )

    # Assert
    assert reserva.registros_pendentes == (
        RegistroDeSituacao(
            situacao_anterior=atual,
            situacao_nova=nova,
            motivo=_motivo_para(nova),
            autor_usuario_id=GESTOR.usuario_id,
            autor_nome=GESTOR.nome,
            registrado_em=DEPOIS,
        ),
    )


def test_cada_mudanca_acrescenta_um_registro_na_ordem():
    # Arrange
    reserva = _solicitar()

    # Act
    reserva.alterar_situacao(S.CONFIRMADA, ator=GESTOR, agora=DEPOIS)
    reserva.alterar_situacao(S.CONCLUIDA, ator=GESTOR, agora=DEPOIS)

    # Assert
    verificar_historico_coerente(reserva.registros_pendentes, reserva.situacao)
    assert len(reserva.registros_pendentes) == 3


def test_solicitante_cancelando_a_propria_aparece_como_autor():
    # Arrange
    reserva = _reconstituir()

    # Act
    reserva.alterar_situacao(
        S.CANCELADA, motivo="Desistência", ator=ATOR_SOLICITANTE, agora=DEPOIS
    )

    # Assert
    (registro,) = reserva.registros_pendentes
    assert (registro.autor_usuario_id, registro.autor_nome) == (7, "Ana Souza")
    assert registro.motivo == "Desistência"


@pytest.mark.parametrize(
    ("nova", "motivo", "ator", "erro"),
    [
        (S.CONFIRMADA, None, ATOR_SOLICITANTE, AlteracaoDeSituacaoNaoPermitida),
        (S.SOLICITADA, None, GESTOR, TransicaoDeSituacaoInvalida),
        (S.RECUSADA, None, GESTOR, MotivoObrigatorio),
        ("PENDENTE", None, GESTOR, SituacaoInvalida),
        (S.CANCELADA, "Desistência", OUTRO_SOLICITANTE, ReservaNaoEncontrada),
    ],
    ids=["403", "409", "motivo-ausente", "situacao-invalida", "nao-visivel"],
)
def test_alteracao_recusada_nao_muda_nada_nem_registra(nova, motivo, ator, erro):
    # Arrange
    reserva = _solicitar()
    antes = (reserva.situacao, reserva.motivo_da_situacao, reserva.registros_pendentes)

    # Act
    with pytest.raises(erro):
        reserva.alterar_situacao(nova, motivo=motivo, ator=ator, agora=DEPOIS)

    # Assert
    depois = (reserva.situacao, reserva.motivo_da_situacao, reserva.registros_pendentes)
    assert depois == antes


@pytest.mark.parametrize(
    "agora", [None, datetime(2026, 10, 21, 14, 0)], ids=["ausente", "sem-fuso"]
)
def test_alterar_situacao_sem_agora_com_fuso_e_erro_de_programacao(agora):
    # Arrange
    reserva = _reconstituir()

    # Act / Assert
    with pytest.raises(TypeError, match="agora"):
        reserva.alterar_situacao(S.CONFIRMADA, ator=GESTOR, agora=agora)
    assert reserva.situacao is S.SOLICITADA
    assert reserva.registros_pendentes == ()


def test_marcar_registros_como_gravados_esvazia_os_pendentes():
    # Arrange
    reserva = _solicitar()

    # Act
    reserva.marcar_registros_como_gravados()

    # Assert
    assert reserva.registros_pendentes == ()


def test_situacao_de_origem_sem_mudancas_e_a_situacao_atual():
    # Assert
    assert _reconstituir(situacao=S.CONFIRMADA).situacao_de_origem is S.CONFIRMADA


def test_situacao_de_origem_e_a_anterior_a_primeira_mudanca_pendente():
    # Arrange
    reserva = _reconstituir()

    # Act
    reserva.alterar_situacao(S.CONFIRMADA, ator=GESTOR, agora=DEPOIS)
    depois_de_uma = reserva.situacao_de_origem
    reserva.alterar_situacao(S.CONCLUIDA, ator=GESTOR, agora=DEPOIS)

    # Assert
    assert depois_de_uma is S.SOLICITADA
    assert reserva.situacao_de_origem is S.SOLICITADA


def test_situacao_de_origem_de_reserva_nova_e_none():
    # Assert
    assert _solicitar().situacao_de_origem is None


def test_reserva_desatualizada_vira_409_com_a_situacao_atual():
    # Act
    resposta = tratar_excecao(ReservaDesatualizada(S.CONFIRMADA), {})

    # Assert
    assert resposta.status_code == 409
    assert resposta.data == {
        "erro": {
            "codigo": "RESERVA_DESATUALIZADA",
            "mensagem": (
                "Esta reserva já está Confirmada: ela foi alterada enquanto você "
                "decidia. Atualize a lista e tente de novo."
            ),
        }
    }
