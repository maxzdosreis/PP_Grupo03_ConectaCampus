from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

import pytest
from django.db import IntegrityError

from reservas.application.repositorio import FiltrosDeReservas
from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.excecoes import ConflitoDeHorario, ReservaNaoEncontrada
from reservas.domain.intervalo_de_horario import IntervaloDeHorario
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import SituacaoReserva
from reservas.domain.solicitante import Solicitante
from reservas.infrastructure.models import CONSTRAINT_SEM_SOBREPOSICAO, ReservaModel
from reservas.infrastructure.repositorio_django import RepositorioReservasDjango
from reservas.tests.fakes import RepositorioReservasEmMemoria

S = SituacaoReserva
SAO_PAULO = ZoneInfo("America/Sao_Paulo")
AGORA = datetime(2026, 10, 21, 12, 0, tzinfo=SAO_PAULO)
DATA = AGORA.date() + timedelta(days=4)
DIA_SEGUINTE = DATA + timedelta(days=1)
ANA = Solicitante(usuario_id=7, nome="Ana Souza", matricula="2026001")
BRUNO = Solicitante(usuario_id=8, nome="Bruno Lima", matricula="2026002")
GESTOR = Ator(usuario_id=1, papel=PapelDoAtor.GESTOR)
ID_INEXISTENTE = 9999


@pytest.fixture(
    params=[
        pytest.param(
            RepositorioReservasDjango, marks=pytest.mark.django_db, id="django"
        ),
        pytest.param(RepositorioReservasEmMemoria, id="memoria"),
    ]
)
def repositorio(request):
    return request.param()


def _solicitar(**sobrescritas):
    dados = {
        "espaco_id": 3,
        "solicitante": ANA,
        "data": DATA,
        "hora_inicio": time(10, 0),
        "hora_fim": time(11, 0),
        "finalidade": "Treino do time de vôlei",
        "agora": AGORA,
    }
    dados.update(sobrescritas)
    return Reserva.solicitar(**dados)


def _salvar_na_situacao(repositorio, situacao, motivo=None, **sobrescritas):
    reserva = _solicitar(**sobrescritas)
    if situacao is not S.SOLICITADA:
        reserva.alterar_situacao(situacao, motivo=motivo, ator=GESTOR)
    return repositorio.salvar(reserva)


def _salvar_reservas_para_listagem(repositorio):
    _salvar_na_situacao(repositorio, S.SOLICITADA, finalidade="Vôlei")
    _salvar_na_situacao(
        repositorio,
        S.CONFIRMADA,
        finalidade="Futsal",
        solicitante=BRUNO,
        hora_inicio=time(8, 0),
        hora_fim=time(9, 0),
    )
    _salvar_na_situacao(
        repositorio,
        S.CANCELADA,
        motivo="Chuva",
        finalidade="Basquete",
        espaco_id=4,
    )
    _salvar_na_situacao(
        repositorio,
        S.SOLICITADA,
        finalidade="Handebol",
        solicitante=BRUNO,
        data=DIA_SEGUINTE,
        hora_inicio=time(9, 0),
        hora_fim=time(10, 0),
    )
    _salvar_na_situacao(
        repositorio,
        S.CONFIRMADA,
        finalidade="Tênis",
        espaco_id=4,
        data=DIA_SEGUINTE,
        hora_inicio=time(7, 0),
        hora_fim=time(8, 0),
    )


def _finalidades(reservas):
    return [reserva.finalidade for reserva in reservas]


def test_salvar_reserva_nova_atribui_id_e_permite_obter_igual(repositorio):
    # Act
    salva = repositorio.salvar(_solicitar())

    # Assert
    obtida = repositorio.obter_por_id(salva.id)
    assert salva.id is not None
    assert obtida == salva
    assert obtida.espaco_id == 3
    assert obtida.solicitante == ANA
    assert obtida.intervalo == IntervaloDeHorario(DATA, time(10, 0), time(11, 0))
    assert obtida.finalidade == "Treino do time de vôlei"
    assert obtida.situacao is S.SOLICITADA
    assert obtida.motivo_da_situacao is None
    assert obtida.criada_em == AGORA


@pytest.mark.parametrize(
    ("situacao", "motivo", "motivo_esperado"),
    [
        (S.CONFIRMADA, None, None),
        (S.RECUSADA, "  Quadra em   manutenção ", "Quadra em manutenção"),
    ],
    ids=["confirmada", "recusada-com-motivo"],
)
def test_salvar_reserva_existente_persiste_situacao_e_motivo(
    repositorio, situacao, motivo, motivo_esperado
):
    # Arrange
    salva = repositorio.salvar(_solicitar())
    salva.alterar_situacao(situacao, motivo=motivo, ator=GESTOR)

    # Act
    atualizada = repositorio.salvar(salva)

    # Assert
    obtida = repositorio.obter_por_id(salva.id)
    assert atualizada.id == salva.id
    assert obtida.situacao is situacao
    assert obtida.motivo_da_situacao == motivo_esperado
    assert len(repositorio.listar(FiltrosDeReservas())) == 1


def test_salvar_com_id_inexistente_lanca_reserva_nao_encontrada(repositorio):
    # Arrange
    reserva = _solicitar()
    reserva.id = ID_INEXISTENTE

    # Act
    with pytest.raises(ReservaNaoEncontrada) as erro:
        repositorio.salvar(reserva)

    # Assert
    assert erro.value.reserva_id == ID_INEXISTENTE
    assert repositorio.listar(FiltrosDeReservas()) == []


def test_obter_por_id_inexistente_devolve_none(repositorio):
    # Act
    obtida = repositorio.obter_por_id(ID_INEXISTENTE)

    # Assert
    assert obtida is None


def test_listar_ordena_por_inicio_e_desempata_por_id(repositorio):
    # Arrange
    _salvar_reservas_para_listagem(repositorio)

    # Act
    reservas = repositorio.listar(FiltrosDeReservas())

    # Assert
    assert _finalidades(reservas) == [
        "Futsal",
        "Vôlei",
        "Basquete",
        "Tênis",
        "Handebol",
    ]


@pytest.mark.parametrize(
    ("filtros", "finalidades_esperadas"),
    [
        (FiltrosDeReservas(espaco_id=4), ["Basquete", "Tênis"]),
        (FiltrosDeReservas(situacao=S.CONFIRMADA), ["Futsal", "Tênis"]),
        (FiltrosDeReservas(data=DIA_SEGUINTE), ["Tênis", "Handebol"]),
        (FiltrosDeReservas(solicitante_usuario_id=8), ["Futsal", "Handebol"]),
        (FiltrosDeReservas(solicitante="ana"), ["Vôlei", "Basquete", "Tênis"]),
        (FiltrosDeReservas(solicitante="SOUZA"), ["Vôlei", "Basquete", "Tênis"]),
        (FiltrosDeReservas(solicitante="2026002"), ["Futsal", "Handebol"]),
        (
            FiltrosDeReservas(espaco_id=3, situacao=S.SOLICITADA),
            ["Vôlei", "Handebol"],
        ),
        (FiltrosDeReservas(data=DATA, solicitante="bruno"), ["Futsal"]),
        (FiltrosDeReservas(espaco_id=4, situacao=S.SOLICITADA), []),
    ],
    ids=[
        "espaco",
        "situacao",
        "data",
        "usuario",
        "nome-minusculo",
        "sobrenome-maiusculo",
        "matricula",
        "espaco-e-situacao",
        "data-e-solicitante",
        "sem-resultado",
    ],
)
def test_listar_aplica_os_filtros(repositorio, filtros, finalidades_esperadas):
    # Arrange
    _salvar_reservas_para_listagem(repositorio)

    # Act
    reservas = repositorio.listar(filtros)

    # Assert
    assert _finalidades(reservas) == finalidades_esperadas


@pytest.mark.parametrize(
    ("espaco_id", "data", "finalidades_esperadas"),
    [
        (3, DATA, ["Futsal", "Vôlei"]),
        (4, DATA, []),
        (4, DIA_SEGUINTE, ["Tênis"]),
    ],
    ids=["solicitada-e-confirmada", "so-cancelada", "outro-dia"],
)
def test_listar_que_ocupam_horario_filtra_espaco_dia_e_situacao(
    repositorio, espaco_id, data, finalidades_esperadas
):
    # Arrange
    _salvar_reservas_para_listagem(repositorio)

    # Act
    reservas = repositorio.listar_que_ocupam_horario(espaco_id, data)

    # Assert
    assert _finalidades(reservas) == finalidades_esperadas


def test_salvar_reserva_sobreposta_a_uma_solicitada_lanca_conflito(repositorio):
    # Arrange
    repositorio.salvar(_solicitar())
    sobreposta = _solicitar(hora_inicio=time(10, 30), hora_fim=time(11, 30))

    # Act
    with pytest.raises(ConflitoDeHorario) as erro:
        repositorio.salvar(sobreposta)

    # Assert
    assert erro.value.situacao is S.SOLICITADA
    assert len(repositorio.listar(FiltrosDeReservas())) == 1


def test_salvar_reserva_sobreposta_a_uma_cancelada_salva_normalmente(repositorio):
    # Arrange
    _salvar_na_situacao(repositorio, S.CANCELADA, motivo="Desistência")
    sobreposta = _solicitar(hora_inicio=time(10, 30), hora_fim=time(11, 30))

    # Act
    salva = repositorio.salvar(sobreposta)

    # Assert
    assert salva.id is not None
    assert len(repositorio.listar(FiltrosDeReservas())) == 2


def test_salvar_reserva_encostada_salva_normalmente(repositorio):
    # Arrange
    repositorio.salvar(_solicitar())
    encostada = _solicitar(hora_inicio=time(11, 0), hora_fim=time(12, 0))

    # Act
    salva = repositorio.salvar(encostada)

    # Assert
    assert salva.id is not None


def test_salvar_reserva_cancelada_sobreposta_a_uma_solicitada_salva_normalmente(
    repositorio,
):
    # Arrange
    repositorio.salvar(_solicitar())
    cancelada = Reserva(
        espaco_id=3,
        solicitante=BRUNO,
        intervalo=IntervaloDeHorario(DATA, time(10, 30), time(11, 30)),
        finalidade="Futsal",
        situacao=S.CANCELADA,
        motivo_da_situacao="Desistência",
        criada_em=AGORA,
    )

    # Act
    salva = repositorio.salvar(cancelada)

    # Assert
    assert salva.id is not None


def test_reserva_no_fim_do_dia_volta_na_mesma_data(repositorio):
    # Arrange
    salva = repositorio.salvar(
        _solicitar(hora_inicio=time(23, 30), hora_fim=time(23, 59))
    )

    # Act
    obtida = repositorio.obter_por_id(salva.id)
    do_dia = repositorio.listar(FiltrosDeReservas(data=DATA))

    # Assert
    assert obtida.intervalo == IntervaloDeHorario(DATA, time(23, 30), time(23, 59))
    assert do_dia == [salva]


def test_alterar_entidade_devolvida_nao_altera_o_repositorio(repositorio):
    # Arrange
    salva = repositorio.salvar(_solicitar())

    # Act
    repositorio.obter_por_id(salva.id).finalidade = "Alterada fora"
    repositorio.listar(FiltrosDeReservas())[0].situacao = S.CONFIRMADA
    salva.motivo_da_situacao = "Alterado fora do repositório"

    # Assert
    guardada = repositorio.obter_por_id(salva.id)
    assert (guardada.finalidade, guardada.situacao, guardada.motivo_da_situacao) == (
        "Treino do time de vôlei",
        S.SOLICITADA,
        None,
    )


def _dados_do_model(**sobrescritas):
    dados = {
        "espaco_id": 3,
        "solicitante_usuario_id": BRUNO.usuario_id,
        "solicitante_nome": BRUNO.nome,
        "solicitante_matricula": BRUNO.matricula,
        "inicio": datetime.combine(DATA, time(10, 0), tzinfo=SAO_PAULO),
        "fim": datetime.combine(DATA, time(11, 0), tzinfo=SAO_PAULO),
        "finalidade": "Futsal",
        "situacao": S.CONFIRMADA.value,
        "criada_em": AGORA,
    }
    dados.update(sobrescritas)
    return dados


@pytest.mark.django_db
def test_banco_barra_sobreposicao_que_escapou_da_checagem_em_codigo():
    # Arrange
    ReservaModel.objects.create(**_dados_do_model())
    sobreposta = _solicitar(hora_inicio=time(10, 30), hora_fim=time(11, 30))

    # Act
    with pytest.raises(ConflitoDeHorario) as erro:
        RepositorioReservasDjango().salvar(sobreposta)

    # Assert
    assert erro.value.mensagem == (
        "Este espaço já tem uma reserva Confirmada em 25/10/2026 10:00–11:00. "
        "Escolha outro horário."
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("campos", "constraint"),
    [
        (
            {"fim": datetime.combine(DATA, time(10, 0), tzinfo=SAO_PAULO)},
            "reservas_reserva_fim_apos_inicio",
        ),
        ({"situacao": "PENDENTE"}, "reservas_reserva_situacao_valida"),
        (
            {"situacao": S.RECUSADA.value, "motivo_da_situacao": ""},
            "reservas_reserva_motivo_obrigatorio",
        ),
    ],
    ids=["fim-igual-ao-inicio", "situacao-desconhecida", "recusada-sem-motivo"],
)
def test_banco_recusa_dados_que_a_entidade_nao_aceitaria(campos, constraint):
    # Act / Assert
    with pytest.raises(IntegrityError, match=constraint):
        ReservaModel.objects.create(**_dados_do_model(**campos))


@pytest.mark.django_db
def test_salvar_repassa_erro_de_sobreposicao_quando_nao_acha_o_ocupante(
    monkeypatch,
):
    # Arrange
    repositorio = RepositorioReservasDjango()
    repositorio.salvar(_solicitar())
    monkeypatch.setattr(
        repositorio, "listar_que_ocupam_horario", lambda espaco_id, data: []
    )
    sobreposta = _solicitar(hora_inicio=time(10, 30), hora_fim=time(11, 30))

    # Act / Assert
    with pytest.raises(IntegrityError, match=CONSTRAINT_SEM_SOBREPOSICAO):
        repositorio.salvar(sobreposta)


@pytest.mark.django_db
def test_salvar_repassa_integrity_error_que_nao_e_de_sobreposicao():
    # Arrange
    reserva = _solicitar()
    reserva.situacao = S.RECUSADA

    # Act / Assert
    with pytest.raises(IntegrityError, match="motivo_obrigatorio"):
        RepositorioReservasDjango().salvar(reserva)


def test_model_mostra_o_numero_e_a_situacao():
    # Act
    texto = str(ReservaModel(id=12, situacao=S.CONFIRMADA.value))

    # Assert
    assert texto == "Reserva #12 (Confirmada)"
