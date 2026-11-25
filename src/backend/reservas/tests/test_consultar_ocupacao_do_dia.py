from datetime import datetime, time, timedelta

import pytest

from compartilhado.domain.erros import ConflitoDeEstado, RecursoNaoEncontrado
from reservas.application.casos_de_uso import ConsultarOcupacaoDoDia
from reservas.application.ocupacao_do_dia import HorarioOcupado
from reservas.domain.excecoes import AntecedenciaExcedida, DataRetroativa
from reservas.domain.intervalo_de_horario import FUSO_HORARIO
from reservas.domain.regras_de_agenda import data_limite_para_reservar
from reservas.domain.situacao import SituacaoReserva
from reservas.tests.fakes import (
    AGORA,
    BRUNO,
    DIA,
    ID_INEXISTENTE,
    AgendaDoDiaEmMemoria,
    ConsultaDeEspacosEmMemoria,
    RepositorioReservasEmMemoria,
    espaco_reservavel,
    funcionamento,
    intervalo,
    reserva_reconstituida,
)

S = SituacaoReserva
QUADRA = espaco_reservavel(1, "Quadra Coberta")
CAMPO = espaco_reservavel(2, "Campo Norte")
GINASIO_INATIVO = espaco_reservavel(3, "Ginásio Antigo")
QUADRA_DE_DIA = espaco_reservavel(4, "Quadra de Dia", funcionamento("08:00", "18:00"))


@pytest.fixture
def repositorio():
    return RepositorioReservasEmMemoria()


@pytest.fixture
def consulta():
    return ConsultaDeEspacosEmMemoria(
        [QUADRA, CAMPO, GINASIO_INATIVO, QUADRA_DE_DIA],
        ids_inativos=[GINASIO_INATIVO.id],
    )


@pytest.fixture
def agenda():
    return AgendaDoDiaEmMemoria()


@pytest.fixture
def consultar(repositorio, consulta, agenda):
    return ConsultarOcupacaoDoDia(repositorio, consulta, agenda, lambda: AGORA)


def _salvar(repositorio, situacao, inicio, fim, *, espaco_id=QUADRA.id, data=DIA):
    return repositorio.salvar(
        reserva_reconstituida(
            id=None,
            espaco_id=espaco_id,
            solicitante=BRUNO,
            intervalo=intervalo(inicio, fim, data),
            situacao=situacao,
        )
    )


def _livres_como_texto(ocupacao):
    return [
        f"{livre.hora_inicio:%H:%M}–{livre.hora_fim:%H:%M}" for livre in ocupacao.livres
    ]


def test_espaco_desconhecido_e_recurso_nao_encontrado(consultar):
    # Act / Assert
    with pytest.raises(RecursoNaoEncontrado):
        consultar.executar(espaco_id=ID_INEXISTENTE, data=DIA)


def test_espaco_inativo_e_conflito_de_estado(consultar, consulta):
    # Act / Assert
    with pytest.raises(ConflitoDeEstado):
        consultar.executar(espaco_id=GINASIO_INATIVO.id, data=DIA)
    assert consulta.ids_consultados == [GINASIO_INATIVO.id]


def test_dia_sem_reservas_tem_o_funcionamento_inteiro_livre(consultar):
    # Act
    ocupacao = consultar.executar(espaco_id=QUADRA.id, data=DIA)

    # Assert
    assert ocupacao.data == DIA
    assert ocupacao.horario_de_abertura == time(7, 0)
    assert ocupacao.horario_de_fechamento == time(0, 0)
    assert ocupacao.ocupados == ()
    assert _livres_como_texto(ocupacao) == ["07:00–00:00"]
    assert ocupacao.reservavel is True
    assert ocupacao.motivo_indisponivel is None


def test_so_solicitadas_e_confirmadas_ocupam_e_o_resto_fica_livre(
    consultar, repositorio
):
    # Arrange
    _salvar(repositorio, S.CONFIRMADA, "10:00", "11:00")
    _salvar(repositorio, S.SOLICITADA, "08:00", "09:00")
    _salvar(repositorio, S.CANCELADA, "14:00", "15:00")
    _salvar(repositorio, S.RECUSADA, "16:00", "17:00")
    _salvar(repositorio, S.CONFIRMADA, "18:00", "19:00", espaco_id=CAMPO.id)
    _salvar(repositorio, S.CONFIRMADA, "12:00", "13:00", data=DIA + timedelta(days=1))

    # Act
    ocupacao = consultar.executar(espaco_id=QUADRA.id, data=DIA)

    # Assert
    assert ocupacao.ocupados == (
        HorarioOcupado(intervalo=intervalo("08:00", "09:00"), situacao=S.SOLICITADA),
        HorarioOcupado(intervalo=intervalo("10:00", "11:00"), situacao=S.CONFIRMADA),
    )
    assert _livres_como_texto(ocupacao) == [
        "07:00–08:00",
        "09:00–10:00",
        "11:00–00:00",
    ]


@pytest.mark.parametrize(
    ("data", "mensagem"),
    [
        (AGORA.date() - timedelta(days=1), DataRetroativa().mensagem),
        (
            AGORA.date() + timedelta(days=31),
            AntecedenciaExcedida(30, data_limite_para_reservar(AGORA)).mensagem,
        ),
    ],
    ids=["ontem", "alem-da-antecedencia"],
)
def test_data_indisponivel_nao_tem_livres_e_traz_o_motivo(
    consultar, repositorio, data, mensagem
):
    # Arrange
    _salvar(repositorio, S.CONFIRMADA, "10:00", "11:00", data=data)

    # Act
    ocupacao = consultar.executar(espaco_id=QUADRA.id, data=data)

    # Assert
    assert ocupacao.reservavel is False
    assert ocupacao.motivo_indisponivel == mensagem
    assert ocupacao.livres == ()
    assert len(ocupacao.ocupados) == 1


def test_espaco_com_horario_proprio_mostra_a_sua_janela_e_os_livres_dela(
    consultar, repositorio
):
    # Arrange
    _salvar(repositorio, S.CONFIRMADA, "12:00", "13:00", espaco_id=QUADRA_DE_DIA.id)

    # Act
    ocupacao = consultar.executar(espaco_id=QUADRA_DE_DIA.id, data=DIA)

    # Assert
    assert ocupacao.horario_de_abertura == time(8, 0)
    assert ocupacao.horario_de_fechamento == time(18, 0)
    assert _livres_como_texto(ocupacao) == ["08:00–12:00", "13:00–18:00"]


def test_reserva_ate_a_meia_noite_aparece_na_agenda_do_dia_dela_e_nao_na_do_seguinte(
    consultar, repositorio
):
    # Arrange
    _salvar(repositorio, S.SOLICITADA, "23:00", "00:00")

    # Act
    do_dia = consultar.executar(espaco_id=QUADRA.id, data=DIA)
    do_seguinte = consultar.executar(espaco_id=QUADRA.id, data=DIA + timedelta(days=1))

    # Assert
    assert [h.intervalo for h in do_dia.ocupados] == [intervalo("23:00", "00:00")]
    assert _livres_como_texto(do_dia) == ["07:00–23:00"]
    assert do_seguinte.ocupados == ()
    assert _livres_como_texto(do_seguinte) == ["07:00–00:00"]


def test_hoje_depois_do_fechamento_do_espaco_nao_e_reservavel(
    repositorio, consulta, agenda
):
    # Arrange
    agora = datetime(2026, 10, 21, 18, 30, tzinfo=FUSO_HORARIO)
    consultar = ConsultarOcupacaoDoDia(repositorio, consulta, agenda, lambda: agora)

    # Act
    de_dia = consultar.executar(espaco_id=QUADRA_DE_DIA.id, data=agora.date())
    padrao = consultar.executar(espaco_id=QUADRA.id, data=agora.date())

    # Assert
    assert de_dia.reservavel is False
    assert de_dia.motivo_indisponivel == DataRetroativa().mensagem
    assert padrao.reservavel is True


class RepositorioQueContaConsultas(RepositorioReservasEmMemoria):
    def __init__(self):
        super().__init__()
        self.consultas_de_ocupacao = 0

    def listar_que_ocupam_horario(self, espaco_id, data):
        self.consultas_de_ocupacao += 1
        return super().listar_que_ocupam_horario(espaco_id, data)


class AgendaQueContaChamadas(AgendaDoDiaEmMemoria):
    def __init__(self, *, falha_em=None, antes_de_substituir=None):
        super().__init__()
        self.chamadas = []
        self._falha_em = falha_em
        self._antes_de_substituir = antes_de_substituir

    def _chamar(self, nome):
        self.chamadas.append(nome)
        self.indisponivel = nome == self._falha_em

    def listar(self, espaco_id, data):
        self._chamar("listar")
        return super().listar(espaco_id, data)

    def versao(self, espaco_id, data):
        self._chamar("versao")
        return super().versao(espaco_id, data)

    def substituir(self, espaco_id, data, ocupados, *, versao):
        self._chamar("substituir")
        if self._antes_de_substituir and not self.indisponivel:
            self._antes_de_substituir(self, espaco_id, data)
        return super().substituir(espaco_id, data, ocupados, versao=versao)


def _montar(consulta, agenda, repositorio=None, agora=AGORA):
    repositorio = repositorio or RepositorioQueContaConsultas()
    return repositorio, ConsultarOcupacaoDoDia(
        repositorio, consulta, agenda, lambda: agora
    )


def test_com_a_agenda_presente_a_resposta_vem_dela_sem_consultar_o_repositorio(
    consulta,
):
    # Arrange
    agenda = AgendaDoDiaEmMemoria()
    repositorio, consultar = _montar(consulta, agenda)
    _salvar(repositorio, S.CONFIRMADA, "10:00", "11:00")
    consultar.executar(espaco_id=QUADRA.id, data=DIA)
    repositorio.consultas_de_ocupacao = 0

    # Act
    ocupacao = consultar.executar(espaco_id=QUADRA.id, data=DIA)

    # Assert
    assert repositorio.consultas_de_ocupacao == 0
    assert [h.situacao for h in ocupacao.ocupados] == [S.CONFIRMADA]


def test_sem_a_agenda_le_do_repositorio_e_repovoa_para_a_proxima_leitura(consulta):
    # Arrange
    agenda = AgendaDoDiaEmMemoria()
    repositorio, consultar = _montar(consulta, agenda)
    _salvar(repositorio, S.SOLICITADA, "10:00", "11:00")
    assert agenda.listar(QUADRA.id, DIA) is None

    # Act
    primeira = consultar.executar(espaco_id=QUADRA.id, data=DIA)
    segunda = consultar.executar(espaco_id=QUADRA.id, data=DIA)

    # Assert
    assert repositorio.consultas_de_ocupacao == 1
    assert agenda.listar(QUADRA.id, DIA) == primeira.ocupados
    assert segunda == primeira


def test_dia_sem_reservas_repovoa_com_agenda_vazia_e_a_proxima_leitura_e_hit(consulta):
    # Arrange
    agenda = AgendaDoDiaEmMemoria()
    repositorio, consultar = _montar(consulta, agenda)

    # Act
    consultar.executar(espaco_id=QUADRA.id, data=DIA)
    segunda = consultar.executar(espaco_id=QUADRA.id, data=DIA)

    # Assert
    assert repositorio.consultas_de_ocupacao == 1
    assert agenda.listar(QUADRA.id, DIA) == ()
    assert segunda.ocupados == ()


def test_versao_velha_descarta_a_gravacao_e_a_leitura_seguinte_volta_ao_repositorio(
    consulta,
):
    # Arrange
    def alguem_registra_no_meio(agenda, espaco_id, data):
        agenda.remover(espaco_id, 999, data)

    agenda = AgendaQueContaChamadas(antes_de_substituir=alguem_registra_no_meio)
    repositorio, consultar = _montar(consulta, agenda)
    _salvar(repositorio, S.CONFIRMADA, "10:00", "11:00")

    # Act
    primeira = consultar.executar(espaco_id=QUADRA.id, data=DIA)
    agenda._antes_de_substituir = None
    segunda = consultar.executar(espaco_id=QUADRA.id, data=DIA)

    # Assert
    assert [h.situacao for h in primeira.ocupados] == [S.CONFIRMADA]
    assert segunda == primeira
    assert repositorio.consultas_de_ocupacao == 2
    assert agenda.listar(QUADRA.id, DIA) is not None


@pytest.mark.parametrize("falha_em", ["listar", "versao", "substituir"])
def test_agenda_indisponivel_responde_pelo_repositorio_sem_nova_chamada_a_agenda(
    consulta, falha_em
):
    # Arrange
    agenda = AgendaQueContaChamadas(falha_em=falha_em)
    repositorio, consultar = _montar(consulta, agenda)
    _salvar(repositorio, S.CONFIRMADA, "10:00", "11:00")
    esperado = {
        "listar": ["listar"],
        "versao": ["listar", "versao"],
        "substituir": ["listar", "versao", "substituir"],
    }[falha_em]

    # Act
    ocupacao = consultar.executar(espaco_id=QUADRA.id, data=DIA)

    # Assert
    assert [h.situacao for h in ocupacao.ocupados] == [S.CONFIRMADA]
    assert agenda.chamadas == esperado
    assert repositorio.consultas_de_ocupacao == 1


@pytest.mark.parametrize("espaco_id", [ID_INEXISTENTE, GINASIO_INATIVO.id])
def test_espaco_invalido_nao_toca_a_agenda(consulta, espaco_id):
    # Arrange
    agenda = AgendaQueContaChamadas()
    _, consultar = _montar(consulta, agenda)

    # Act
    with pytest.raises((RecursoNaoEncontrado, ConflitoDeEstado)):
        consultar.executar(espaco_id=espaco_id, data=DIA)

    # Assert
    assert agenda.chamadas == []


def _com_reservas(repositorio, data):
    _salvar(repositorio, S.SOLICITADA, "08:00", "09:00", data=data)
    _salvar(repositorio, S.CONFIRMADA, "10:00", "11:00", data=data)
    _salvar(repositorio, S.SOLICITADA, "23:00", "00:00", data=data)
    _salvar(repositorio, S.RECUSADA, "12:00", "13:00", data=data)
    _salvar(repositorio, S.CANCELADA, "14:00", "15:00", data=data)
    _salvar(repositorio, S.CONCLUIDA, "16:00", "17:00", data=data)


@pytest.mark.parametrize(
    "data",
    [
        DIA,
        AGORA.date() - timedelta(days=1),
        AGORA.date() + timedelta(days=31),
    ],
    ids=["dia-comum", "dia-passado", "alem-do-limite"],
)
def test_resposta_e_igual_com_hit_miss_e_agenda_indisponivel(consulta, data):
    # Arrange
    base = RepositorioQueContaConsultas()
    _com_reservas(base, data)
    agenda = AgendaDoDiaEmMemoria()
    _, com_agenda = _montar(consulta, agenda, base)
    _, sem_agenda = _montar(consulta, AgendaDoDiaEmMemoria(indisponivel=True), base)

    # Act
    miss = com_agenda.executar(espaco_id=QUADRA.id, data=data)
    hit = com_agenda.executar(espaco_id=QUADRA.id, data=data)
    fora = sem_agenda.executar(espaco_id=QUADRA.id, data=data)

    # Assert
    assert miss == hit == fora
    assert [h.situacao for h in hit.ocupados] == [
        S.SOLICITADA,
        S.CONFIRMADA,
        S.SOLICITADA,
    ]


def test_segundos_do_banco_nao_fazem_hit_e_miss_divergirem(consulta):
    # Arrange
    repositorio, consultar = _montar(consulta, AgendaDoDiaEmMemoria())
    repositorio.salvar(
        reserva_reconstituida(
            id=None,
            espaco_id=QUADRA.id,
            solicitante=BRUNO,
            intervalo=intervalo("10:00:30", "11:00:45"),
            situacao=S.CONFIRMADA,
        )
    )

    # Act
    miss = consultar.executar(espaco_id=QUADRA.id, data=DIA)
    hit = consultar.executar(espaco_id=QUADRA.id, data=DIA)

    # Assert
    assert miss == hit
    assert miss.ocupados[0].intervalo == intervalo("10:00", "11:00")
