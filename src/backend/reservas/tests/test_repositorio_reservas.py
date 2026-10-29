from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

import pytest
from django.db import IntegrityError, connection
from django.db.models import ProtectedError
from django.test.utils import CaptureQueriesContext

from reservas.application.repositorio import FiltrosDeReservas
from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.excecoes import (
    ConflitoDeHorario,
    ReservaDesatualizada,
    ReservaNaoEncontrada,
)
from reservas.domain.intervalo_de_horario import IntervaloDeHorario
from reservas.domain.registro_de_situacao import RegistroDeSituacao
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import SituacaoReserva
from reservas.domain.solicitante import Solicitante
from reservas.infrastructure.models import (
    CONSTRAINT_SEM_SOBREPOSICAO,
    RegistroDeSituacaoModel,
    ReservaModel,
)
from reservas.infrastructure.repositorio_django import RepositorioReservasDjango
from reservas.tests.fakes import RepositorioReservasEmMemoria
from reservas.tests.historico import verificar_historico_coerente

S = SituacaoReserva
SAO_PAULO = ZoneInfo("America/Sao_Paulo")
AGORA = datetime(2026, 10, 21, 12, 0, tzinfo=SAO_PAULO)
DATA = AGORA.date() + timedelta(days=4)
DIA_SEGUINTE = DATA + timedelta(days=1)
ANA = Solicitante(usuario_id=7, nome="Ana Souza", matricula="2026001")
BRUNO = Solicitante(usuario_id=8, nome="Bruno Lima", matricula="2026002")
GESTOR = Ator(usuario_id=1, nome="Gestora de Teste", papel=PapelDoAtor.GESTOR)
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
        reserva.alterar_situacao(situacao, motivo=motivo, ator=GESTOR, agora=AGORA)
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
    salva.alterar_situacao(situacao, motivo=motivo, ator=GESTOR, agora=AGORA)

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


DEPOIS = AGORA + timedelta(hours=1)


def _pares(registros):
    return [(r.situacao_anterior, r.situacao_nova) for r in registros]


def test_salvar_reserva_nova_grava_o_registro_de_criacao(repositorio):
    # Act
    salva = repositorio.salvar(_solicitar())

    # Assert
    assert repositorio.listar_historico(salva.id) == [
        RegistroDeSituacao(
            situacao_anterior=None,
            situacao_nova=S.SOLICITADA,
            motivo=None,
            autor_usuario_id=ANA.usuario_id,
            autor_nome=ANA.nome,
            registrado_em=AGORA,
        )
    ]


def test_alterar_e_salvar_grava_o_registro_da_mudanca(repositorio):
    # Arrange
    salva = repositorio.salvar(_solicitar())
    salva.alterar_situacao(
        S.RECUSADA, motivo="Quadra em manutenção", ator=GESTOR, agora=DEPOIS
    )

    # Act
    repositorio.salvar(salva)

    # Assert
    historico = repositorio.listar_historico(salva.id)
    assert _pares(historico) == [(None, S.SOLICITADA), (S.SOLICITADA, S.RECUSADA)]
    assert historico[1].motivo == "Quadra em manutenção"
    assert historico[1].autor_nome == GESTOR.nome
    assert historico[1].registrado_em == DEPOIS


def test_listar_historico_desempata_pela_ordem_de_insercao(repositorio):
    # Arrange
    salva = repositorio.salvar(_solicitar())
    salva.alterar_situacao(S.CONFIRMADA, ator=GESTOR, agora=AGORA)
    salva.alterar_situacao(S.CONCLUIDA, ator=GESTOR, agora=AGORA)
    repositorio.salvar(salva)

    # Act
    historico = repositorio.listar_historico(salva.id)

    # Assert
    assert _pares(historico) == [
        (None, S.SOLICITADA),
        (S.SOLICITADA, S.CONFIRMADA),
        (S.CONFIRMADA, S.CONCLUIDA),
    ]
    verificar_historico_coerente(historico, S.CONCLUIDA)


def test_listar_historico_ordena_por_registrado_em(repositorio):
    # Arrange
    salva = repositorio.salvar(_solicitar(agora=AGORA))
    salva.alterar_situacao(S.CONFIRMADA, ator=GESTOR, agora=DEPOIS)
    repositorio.salvar(salva)

    # Act
    historico = repositorio.listar_historico(salva.id)

    # Assert
    assert [r.registrado_em for r in historico] == [AGORA, DEPOIS]


def test_listar_historico_so_traz_os_registros_da_reserva(repositorio):
    # Arrange
    primeira = repositorio.salvar(_solicitar())
    segunda = repositorio.salvar(_solicitar(espaco_id=4))
    segunda.alterar_situacao(S.CONFIRMADA, ator=GESTOR, agora=DEPOIS)
    repositorio.salvar(segunda)

    # Act
    historico = repositorio.listar_historico(primeira.id)

    # Assert
    assert _pares(historico) == [(None, S.SOLICITADA)]


def test_listar_historico_de_id_inexistente_devolve_lista_vazia(repositorio):
    # Act
    historico = repositorio.listar_historico(ID_INEXISTENTE)

    # Assert
    assert historico == []


def test_conflito_ao_salvar_nao_grava_registro_e_mantem_os_pendentes(repositorio):
    # Arrange
    ocupante = repositorio.salvar(_solicitar())
    sobreposta = _solicitar(
        solicitante=BRUNO, hora_inicio=time(10, 30), hora_fim=time(11, 30)
    )

    # Act
    with pytest.raises(ConflitoDeHorario):
        repositorio.salvar(sobreposta)

    # Assert
    assert len(sobreposta.registros_pendentes) == 1
    assert _pares(repositorio.listar_historico(ocupante.id)) == [(None, S.SOLICITADA)]
    assert len(repositorio.listar(FiltrosDeReservas())) == 1


@pytest.mark.django_db
def test_conflito_barrado_pelo_banco_nao_grava_registro():
    # Arrange
    ReservaModel.objects.create(**_dados_do_model())
    sobreposta = _solicitar(hora_inicio=time(10, 30), hora_fim=time(11, 30))

    # Act
    with pytest.raises(ConflitoDeHorario):
        RepositorioReservasDjango().salvar(sobreposta)

    # Assert
    assert RegistroDeSituacaoModel.objects.count() == 0
    assert ReservaModel.objects.count() == 1


def test_salvar_de_novo_sem_mudanca_nao_duplica_registros(repositorio):
    # Arrange
    salva = repositorio.salvar(_solicitar())
    salva.alterar_situacao(S.CONFIRMADA, ator=GESTOR, agora=DEPOIS)
    atualizada = repositorio.salvar(salva)

    # Act
    repositorio.salvar(salva)
    repositorio.salvar(atualizada)
    repositorio.salvar(repositorio.obter_por_id(salva.id))

    # Assert
    assert len(repositorio.listar_historico(salva.id)) == 2
    assert salva.registros_pendentes == ()
    assert atualizada.registros_pendentes == ()


def test_reserva_salva_ou_obtida_nao_tem_pendentes(repositorio):
    # Arrange
    reserva = _solicitar()

    # Act
    salva = repositorio.salvar(reserva)

    # Assert
    assert reserva.registros_pendentes == ()
    assert salva.registros_pendentes == ()
    assert repositorio.obter_por_id(salva.id).registros_pendentes == ()


def _dados_do_registro(reserva_model, **sobrescritas):
    dados = {
        "reserva": reserva_model,
        "situacao_anterior": S.SOLICITADA.value,
        "situacao_nova": S.CONFIRMADA.value,
        "autor_usuario_id": 1,
        "autor_nome": "Gestora de Teste",
        "registrado_em": AGORA,
    }
    dados.update(sobrescritas)
    return dados


@pytest.mark.django_db
def test_banco_nao_deixa_excluir_reserva_com_historico():
    # Arrange
    salva = RepositorioReservasDjango().salvar(_solicitar())

    # Act / Assert
    with pytest.raises(ProtectedError):
        ReservaModel.objects.get(pk=salva.id).delete()
    assert RegistroDeSituacaoModel.objects.filter(reserva_id=salva.id).count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("campos", "constraint"),
    [
        (
            {"situacao_nova": "PENDENTE"},
            "reservas_registro_de_situacao_situacoes_validas",
        ),
        (
            {"situacao_anterior": "PENDENTE"},
            "reservas_registro_de_situacao_situacoes_validas",
        ),
        (
            {"situacao_anterior": S.CONFIRMADA.value},
            "reservas_registro_de_situacao_anterior_diferente_da_nova",
        ),
    ],
    ids=["nova-desconhecida", "anterior-desconhecida", "anterior-igual-a-nova"],
)
def test_banco_recusa_registro_que_a_entidade_nao_aceitaria(campos, constraint):
    # Arrange
    reserva_model = ReservaModel.objects.create(**_dados_do_model())

    # Act / Assert
    with pytest.raises(IntegrityError, match=constraint):
        RegistroDeSituacaoModel.objects.create(
            **_dados_do_registro(reserva_model, **campos)
        )


@pytest.mark.parametrize(
    ("anterior", "texto"),
    [
        ("", "Reserva #12: criada como Confirmada"),
        (S.SOLICITADA.value, "Reserva #12: Solicitada → Confirmada"),
    ],
    ids=["criacao", "mudanca"],
)
def test_registro_model_mostra_a_reserva_e_as_situacoes(anterior, texto):
    # Act
    resultado = str(
        RegistroDeSituacaoModel(
            reserva_id=12, situacao_anterior=anterior, situacao_nova=S.CONFIRMADA.value
        )
    )

    # Assert
    assert resultado == texto


def test_alteracao_sobre_leitura_desatualizada_e_recusada_sem_gravar(repositorio):
    # Arrange
    reserva_id = repositorio.salvar(_solicitar()).id
    primeira = repositorio.obter_por_id(reserva_id)
    segunda = repositorio.obter_por_id(reserva_id)
    primeira.alterar_situacao(S.CONFIRMADA, ator=GESTOR, agora=DEPOIS)
    segunda.alterar_situacao(S.CANCELADA, motivo="Chuva", ator=GESTOR, agora=DEPOIS)
    repositorio.salvar(primeira)

    # Act
    with pytest.raises(ReservaDesatualizada) as erro:
        repositorio.salvar(segunda)

    # Assert
    assert erro.value.situacao_atual is S.CONFIRMADA
    assert repositorio.obter_por_id(reserva_id).situacao is S.CONFIRMADA
    historico = repositorio.listar_historico(reserva_id)
    assert len(historico) == 2
    verificar_historico_coerente(historico, S.CONFIRMADA)
    assert len(segunda.registros_pendentes) == 1


def test_salvar_entidade_que_ficou_para_tras_nao_regride_a_situacao(repositorio):
    # Arrange
    reserva_id = repositorio.salvar(_solicitar()).id
    antiga = repositorio.obter_por_id(reserva_id)
    atual = repositorio.obter_por_id(reserva_id)
    atual.alterar_situacao(S.CONFIRMADA, ator=GESTOR, agora=DEPOIS)
    repositorio.salvar(atual)

    # Act
    with pytest.raises(ReservaDesatualizada):
        repositorio.salvar(antiga)

    # Assert
    assert repositorio.obter_por_id(reserva_id).situacao is S.CONFIRMADA
    assert len(repositorio.listar_historico(reserva_id)) == 2


@pytest.mark.django_db
def test_salvar_reserva_existente_bloqueia_a_linha():
    # Arrange
    repositorio = RepositorioReservasDjango()
    salva = repositorio.salvar(_solicitar())
    salva.alterar_situacao(S.CONFIRMADA, ator=GESTOR, agora=DEPOIS)

    # Act
    with CaptureQueriesContext(connection) as consultas:
        repositorio.salvar(salva)

    # Assert
    assert any(
        'FROM "reservas_reserva"' in consulta["sql"] and "FOR UPDATE" in consulta["sql"]
        for consulta in consultas.captured_queries
    )
