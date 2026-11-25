from datetime import datetime, time, timedelta

import pytest
from django.db import IntegrityError, connection
from django.db.models import ProtectedError
from django.test.utils import CaptureQueriesContext

from reservas.application.repositorio import FiltrosDeReservas, Paginacao
from reservas.domain.excecoes import (
    ConflitoDeHorario,
    ReservaDesatualizada,
    ReservaNaoEncontrada,
)
from reservas.domain.intervalo_de_horario import FUSO_HORARIO, IntervaloDeHorario
from reservas.domain.registro_de_situacao import RegistroDeSituacao
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import SituacaoReserva
from reservas.infrastructure.models import (
    CONSTRAINT_SEM_SOBREPOSICAO,
    RegistroDeSituacaoModel,
    ReservaModel,
)
from reservas.infrastructure.repositorio_django import RepositorioReservasDjango
from reservas.tests.fakes import (
    AGORA,
    ANA,
    BRUNO,
    DEPOIS_DO_TERMINO,
    DIA,
    FUNCIONAMENTO_PADRAO,
    GESTOR,
    ID_INEXISTENTE,
    RepositorioReservasEmMemoria,
    todas_as_reservas,
)
from reservas.tests.historico import verificar_historico_coerente

S = SituacaoReserva
DIA_SEGUINTE = DIA + timedelta(days=1)


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
        "data": DIA,
        "hora_inicio": time(10, 0),
        "hora_fim": time(11, 0),
        "finalidade": "Treino do time de vôlei",
        "agora": AGORA,
        "funcionamento": FUNCIONAMENTO_PADRAO,
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
    assert obtida.intervalo == IntervaloDeHorario(DIA, time(10, 0), time(11, 0))
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
    assert len(todas_as_reservas(repositorio)) == 1


def test_salvar_com_id_inexistente_lanca_reserva_nao_encontrada(repositorio):
    # Arrange
    reserva = _solicitar()
    reserva.id = ID_INEXISTENTE

    # Act
    with pytest.raises(ReservaNaoEncontrada) as erro:
        repositorio.salvar(reserva)

    # Assert
    assert erro.value.reserva_id == ID_INEXISTENTE
    assert todas_as_reservas(repositorio) == []


def test_obter_por_id_inexistente_devolve_none(repositorio):
    # Act
    obtida = repositorio.obter_por_id(ID_INEXISTENTE)

    # Assert
    assert obtida is None


def test_listar_ordena_por_inicio_e_desempata_por_id(repositorio):
    # Arrange
    _salvar_reservas_para_listagem(repositorio)

    # Act
    reservas = todas_as_reservas(repositorio)

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
        (FiltrosDeReservas(data=DIA, solicitante="bruno"), ["Futsal"]),
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
    reservas = todas_as_reservas(repositorio, filtros)

    # Assert
    assert _finalidades(reservas) == finalidades_esperadas


@pytest.mark.parametrize(
    ("espaco_id", "data", "finalidades_esperadas"),
    [
        (3, DIA, ["Futsal", "Vôlei"]),
        (4, DIA, []),
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
    assert len(todas_as_reservas(repositorio)) == 1


def test_salvar_reserva_sobreposta_a_uma_cancelada_salva_normalmente(repositorio):
    # Arrange
    _salvar_na_situacao(repositorio, S.CANCELADA, motivo="Desistência")
    sobreposta = _solicitar(hora_inicio=time(10, 30), hora_fim=time(11, 30))

    # Act
    salva = repositorio.salvar(sobreposta)

    # Assert
    assert salva.id is not None
    assert len(todas_as_reservas(repositorio)) == 2


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
        intervalo=IntervaloDeHorario(DIA, time(10, 30), time(11, 30)),
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
        Reserva(
            espaco_id=3,
            solicitante=ANA,
            intervalo=IntervaloDeHorario(DIA, time(23, 30), time(23, 59)),
            finalidade="Treino do time de vôlei",
            situacao=S.SOLICITADA,
            criada_em=AGORA,
        )
    )

    # Act
    obtida = repositorio.obter_por_id(salva.id)
    do_dia = todas_as_reservas(repositorio, FiltrosDeReservas(data=DIA))

    # Assert
    assert obtida.intervalo == IntervaloDeHorario(DIA, time(23, 30), time(23, 59))
    assert do_dia == [salva]


def test_alterar_entidade_devolvida_nao_altera_o_repositorio(repositorio):
    # Arrange
    salva = repositorio.salvar(_solicitar())

    # Act
    repositorio.obter_por_id(salva.id).finalidade = "Alterada fora"
    todas_as_reservas(repositorio)[0].situacao = S.CONFIRMADA
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
        "inicio": datetime.combine(DIA, time(10, 0), tzinfo=FUSO_HORARIO),
        "fim": datetime.combine(DIA, time(11, 0), tzinfo=FUSO_HORARIO),
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
            {"fim": datetime.combine(DIA, time(10, 0), tzinfo=FUSO_HORARIO)},
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
    salva.alterar_situacao(S.CONFIRMADA, ator=GESTOR, agora=DEPOIS_DO_TERMINO)
    salva.alterar_situacao(S.CONCLUIDA, ator=GESTOR, agora=DEPOIS_DO_TERMINO)
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
    assert len(todas_as_reservas(repositorio)) == 1


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
    dados.setdefault("situacao_pedida", dados["situacao_nova"])
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


def _salvar_sete_com_empates(repositorio):
    """Sete reservas em três espaços; os pares de início igual se desempatam por id.

    Devolve as finalidades na ordem esperada: início e, no empate, id.
    """
    horarios = [
        (5, time(9, 0), "A"),
        (3, time(8, 0), "B"),
        (4, time(9, 0), "C"),
        (3, time(9, 0), "D"),
        (5, time(10, 0), "E"),
        (4, time(8, 0), "F"),
        (3, time(11, 0), "G"),
    ]
    for espaco_id, inicio, finalidade in horarios:
        fim = (datetime.combine(DIA, inicio) + timedelta(minutes=30)).time()
        repositorio.salvar(
            _solicitar(
                espaco_id=espaco_id,
                hora_inicio=inicio,
                hora_fim=fim,
                finalidade=finalidade,
                solicitante=BRUNO if finalidade in "AEG" else ANA,
            )
        )
    return ["B", "F", "A", "C", "D", "E", "G"]


@pytest.mark.parametrize(
    ("numero", "esperadas"),
    [
        (1, ["B", "F", "A"]),
        (2, ["C", "D", "E"]),
        (3, ["G"]),
        (4, []),
        (99, []),
    ],
    ids=["primeira", "do-meio", "ultima-incompleta", "depois-do-fim", "muito-depois"],
)
def test_listar_devolve_a_pagina_pedida_com_o_total(repositorio, numero, esperadas):
    # Arrange
    _salvar_sete_com_empates(repositorio)

    # Act
    pagina = repositorio.listar(
        FiltrosDeReservas(), Paginacao(numero=numero, tamanho=3)
    )

    # Assert
    assert _finalidades(pagina.itens) == esperadas
    assert isinstance(pagina.itens, tuple)
    assert pagina.total == 7
    assert pagina.total_de_paginas() == 3
    assert pagina.paginacao == Paginacao(numero=numero, tamanho=3)


@pytest.mark.parametrize(
    ("filtros", "total", "primeira_pagina"),
    [
        (FiltrosDeReservas(), 7, ["B", "F"]),
        (FiltrosDeReservas(espaco_id=3), 3, ["B", "D"]),
        (FiltrosDeReservas(solicitante="bruno"), 3, ["A", "E"]),
        (FiltrosDeReservas(espaco_id=4, solicitante="bruno"), 0, []),
    ],
    ids=["sem-filtros", "espaco", "solicitante", "sem-resultado"],
)
def test_listar_conta_o_total_com_os_filtros(
    repositorio, filtros, total, primeira_pagina
):
    # Arrange
    _salvar_sete_com_empates(repositorio)

    # Act
    pagina = repositorio.listar(filtros, Paginacao(numero=1, tamanho=2))

    # Assert
    assert pagina.total == total
    assert _finalidades(pagina.itens) == primeira_pagina


def test_listar_pagina_em_ordem_estavel_no_empate_de_inicio(repositorio):
    # Arrange
    esperadas = _salvar_sete_com_empates(repositorio)

    # Act
    paginas = [
        repositorio.listar(FiltrosDeReservas(), Paginacao(numero=numero, tamanho=1))
        for numero in range(1, 8)
    ]

    # Assert
    assert [_finalidades(pagina.itens)[0] for pagina in paginas] == esperadas
    assert _finalidades(todas_as_reservas(repositorio)) == esperadas


@pytest.mark.django_db
def test_listar_pagina_no_banco_com_count_e_limit():
    # Arrange
    repositorio = RepositorioReservasDjango()
    _salvar_sete_com_empates(repositorio)

    # Act
    with CaptureQueriesContext(connection) as consultas:
        repositorio.listar(FiltrosDeReservas(), Paginacao(numero=2, tamanho=3))

    # Assert
    sqls = [consulta["sql"] for consulta in consultas.captured_queries]
    assert len(sqls) == 2
    assert "COUNT(*)" in sqls[0]
    assert "LIMIT 3 OFFSET 3" in sqls[1]
    assert (
        'ORDER BY "reservas_reserva"."inicio" ASC, "reservas_reserva"."id" ASC'
        in (sqls[1])
    )


@pytest.mark.django_db
def test_listar_pagina_depois_do_fim_so_conta():
    # Arrange
    repositorio = RepositorioReservasDjango()
    _salvar_sete_com_empates(repositorio)

    # Act
    with CaptureQueriesContext(connection) as consultas:
        pagina = repositorio.listar(
            FiltrosDeReservas(), Paginacao(numero=10**30, tamanho=100)
        )

    # Assert
    assert pagina.itens == ()
    assert pagina.total == 7
    assert len(consultas.captured_queries) == 1
    assert "COUNT(*)" in consultas.captured_queries[0]["sql"]


def _registro_de_tentativa(reserva, **sobrescritas):
    dados = {
        "situacao_pedida": S.CONFIRMADA,
        "motivo": None,
        "ator": GESTOR,
        "agora": AGORA + timedelta(minutes=5),
        "codigo_do_erro": "TRANSICAO_DE_SITUACAO_INVALIDA",
    }
    dados.update(sobrescritas)
    return reserva.registrar_tentativa_recusada(**dados)


def test_gravar_tentativa_recusada_nao_muda_a_reserva_e_entra_no_historico(
    repositorio,
):
    # Arrange
    salva = _salvar_na_situacao(repositorio, S.SOLICITADA)
    registro = _registro_de_tentativa(salva, codigo_do_erro="ACAO_NAO_PERMITIDA")

    # Act
    repositorio.gravar_tentativa_recusada(salva.id, registro)

    # Assert
    depois = repositorio.obter_por_id(salva.id)
    assert (depois.situacao, depois.motivo_da_situacao) == (S.SOLICITADA, None)
    criacao, tentativa = repositorio.listar_historico(salva.id)
    assert criacao.situacao_nova is S.SOLICITADA
    assert tentativa == registro
    verificar_historico_coerente([criacao, tentativa], depois.situacao)


def test_gravar_tentativa_recusada_de_reserva_inexistente_lanca_nao_encontrada(
    repositorio,
):
    # Arrange
    reserva = _solicitar()
    registro = _registro_de_tentativa(reserva)

    # Act / Assert
    with pytest.raises(ReservaNaoEncontrada):
        repositorio.gravar_tentativa_recusada(ID_INEXISTENTE, registro)


def test_tentativa_recusada_guarda_o_texto_pedido_mesmo_sem_ser_uma_situacao(
    repositorio,
):
    # Arrange
    salva = _salvar_na_situacao(repositorio, S.SOLICITADA)
    registro = _registro_de_tentativa(
        salva, situacao_pedida="em análise", codigo_do_erro="SITUACAO_INVALIDA"
    )

    # Act
    repositorio.gravar_tentativa_recusada(salva.id, registro)

    # Assert
    tentativa = repositorio.listar_historico(salva.id)[-1]
    assert tentativa.situacao_pedida == "em análise"
    assert tentativa.codigo_do_erro == "SITUACAO_INVALIDA"


def test_historico_mistura_aceitas_e_recusadas_na_ordem_de_registro(repositorio):
    # Arrange
    salva = _salvar_na_situacao(repositorio, S.SOLICITADA)
    repositorio.gravar_tentativa_recusada(
        salva.id,
        _registro_de_tentativa(salva, agora=AGORA + timedelta(minutes=1)),
    )
    salva.alterar_situacao(
        S.CONFIRMADA, ator=GESTOR, agora=AGORA + timedelta(minutes=2)
    )
    repositorio.salvar(salva)

    # Act
    historico = repositorio.listar_historico(salva.id)

    # Assert
    assert [r.resultado.value for r in historico] == ["ACEITA", "RECUSADA", "ACEITA"]
    assert [r.registrado_em for r in historico] == sorted(
        r.registrado_em for r in historico
    )


@pytest.mark.django_db
def test_banco_recusa_registro_recusado_incoerente():
    # Arrange
    repositorio = RepositorioReservasDjango()
    salva = _salvar_na_situacao(repositorio, S.SOLICITADA)
    modelo = RegistroDeSituacaoModel.objects.get(reserva_id=salva.id)

    # Act / Assert
    modelo.pk = None
    modelo.resultado = "RECUSADA"
    modelo.codigo_do_erro = ""
    modelo.situacao_pedida = "CONFIRMADA"
    with pytest.raises(IntegrityError, match="resultado_coerente"):
        modelo.save()


@pytest.mark.django_db
def test_texto_do_registro_diz_se_foi_criacao_mudanca_ou_tentativa_recusada():
    # Arrange
    repositorio = RepositorioReservasDjango()
    salva = _salvar_na_situacao(repositorio, S.SOLICITADA)
    salva.alterar_situacao(S.CONFIRMADA, ator=GESTOR, agora=AGORA)
    repositorio.salvar(salva)
    repositorio.gravar_tentativa_recusada(
        salva.id,
        _registro_de_tentativa(
            salva,
            situacao_pedida=S.CONCLUIDA,
            codigo_do_erro="CONCLUSAO_ANTES_DO_TERMINO",
        ),
    )

    # Act
    textos = [
        str(registro)
        for registro in RegistroDeSituacaoModel.objects.filter(reserva_id=salva.id)
    ]

    # Assert
    assert textos == [
        f"Reserva #{salva.id}: criada como Solicitada",
        f"Reserva #{salva.id}: Solicitada → Confirmada",
        f"Reserva #{salva.id}: tentativa recusada de CONCLUIDA "
        "(CONCLUSAO_ANTES_DO_TERMINO)",
    ]


def test_listar_ativas_a_partir_de_traz_as_que_terminam_depois_do_momento(repositorio):
    # Arrange: espaço 3, no dia DIA
    _salvar_na_situacao(repositorio, S.SOLICITADA, finalidade="Cedo")
    _salvar_na_situacao(
        repositorio,
        S.CONFIRMADA,
        finalidade="Em andamento",
        hora_inicio=time(14, 0),
        hora_fim=time(15, 0),
    )
    _salvar_na_situacao(
        repositorio,
        S.SOLICITADA,
        finalidade="Termina a meia-noite",
        hora_inicio=time(23, 0),
        hora_fim=time(0, 0),
    )
    _salvar_na_situacao(
        repositorio,
        S.CANCELADA,
        motivo="Chuva",
        finalidade="Cancelada",
        hora_inicio=time(16, 0),
        hora_fim=time(17, 0),
    )
    _salvar_na_situacao(
        repositorio, S.SOLICITADA, finalidade="Outro espaço", espaco_id=4
    )
    momento = datetime(2026, 10, 25, 14, 30, tzinfo=FUSO_HORARIO)

    # Act
    ativas = repositorio.listar_ativas_a_partir_de(3, momento)

    # Assert
    assert _finalidades(ativas) == ["Em andamento", "Termina a meia-noite"]


def test_listar_ativas_a_partir_de_nao_traz_a_que_ja_terminou_nem_a_que_termina_agora(
    repositorio,
):
    # Arrange
    _salvar_na_situacao(repositorio, S.CONFIRMADA, finalidade="Das 10 as 11")

    # Act
    no_termino = repositorio.listar_ativas_a_partir_de(
        3, datetime(2026, 10, 25, 11, 0, tzinfo=FUSO_HORARIO)
    )
    um_minuto_antes = repositorio.listar_ativas_a_partir_de(
        3, datetime(2026, 10, 25, 10, 59, tzinfo=FUSO_HORARIO)
    )

    # Assert
    assert no_termino == []
    assert _finalidades(um_minuto_antes) == ["Das 10 as 11"]


def test_reserva_que_termina_a_meia_noite_volta_do_banco_com_o_mesmo_intervalo(
    repositorio,
):
    # Arrange
    salva = _salvar_na_situacao(
        repositorio, S.SOLICITADA, hora_inicio=time(23, 0), hora_fim=time(0, 0)
    )

    # Act
    lida = repositorio.obter_por_id(salva.id)

    # Assert
    assert lida.intervalo == salva.intervalo
    assert lida.intervalo.data == DIA
    assert lida.intervalo.hora_fim == time(0, 0)
    assert lida.intervalo.fim() == datetime(2026, 10, 26, 0, 0, tzinfo=FUSO_HORARIO)


def test_reserva_ate_a_meia_noite_so_aparece_no_dia_em_que_comecou(repositorio):
    # Arrange
    _salvar_na_situacao(
        repositorio, S.SOLICITADA, hora_inicio=time(23, 0), hora_fim=time(0, 0)
    )

    # Act
    do_dia = repositorio.listar_que_ocupam_horario(3, DIA)
    do_seguinte = repositorio.listar_que_ocupam_horario(3, DIA_SEGUINTE)

    # Assert
    assert len(do_dia) == 1
    assert do_seguinte == []


def test_listar_dias_com_reservas_que_ocupam_horario_devolve_pares_ordenados(
    repositorio,
):
    # Arrange
    _salvar_reservas_para_listagem(repositorio)
    _salvar_na_situacao(
        repositorio, S.SOLICITADA, hora_inicio=time(14, 0), hora_fim=time(15, 0)
    )

    # Act
    dias = repositorio.listar_dias_com_reservas_que_ocupam_horario(DIA)

    # Assert
    assert dias == [(3, DIA), (3, DIA_SEGUINTE), (4, DIA_SEGUINTE)]


def test_listar_dias_com_reservas_que_ocupam_horario_respeita_a_data_inicial(
    repositorio,
):
    # Arrange
    _salvar_reservas_para_listagem(repositorio)

    # Act
    dias = repositorio.listar_dias_com_reservas_que_ocupam_horario(DIA_SEGUINTE)

    # Assert
    assert dias == [(3, DIA_SEGUINTE), (4, DIA_SEGUINTE)]


def test_listar_dias_com_reservas_que_ocupam_horario_sem_reservas_devolve_vazio(
    repositorio,
):
    assert repositorio.listar_dias_com_reservas_que_ocupam_horario(DIA) == []


def test_listar_dias_com_reservas_que_ocupam_horario_usa_a_data_local_do_inicio(
    repositorio,
):
    # Arrange
    _salvar_na_situacao(
        repositorio, S.SOLICITADA, hora_inicio=time(23, 0), hora_fim=time(0, 0)
    )

    # Act / Assert
    assert repositorio.listar_dias_com_reservas_que_ocupam_horario(DIA) == [(3, DIA)]
    assert repositorio.listar_dias_com_reservas_que_ocupam_horario(DIA_SEGUINTE) == []


def _salvar_varias(repositorio, quantidade):
    return [
        _salvar_na_situacao(
            repositorio,
            S.SOLICITADA,
            espaco_id=indice + 1,
            hora_inicio=time(10, 0),
            hora_fim=time(11, 0),
        )
        for indice in range(quantidade)
    ]


def test_listar_para_indice_devolve_id_situacao_e_criada_em_por_id(repositorio):
    # Arrange
    primeira = _salvar_na_situacao(repositorio, S.SOLICITADA)
    segunda = _salvar_na_situacao(repositorio, S.CANCELADA, motivo="Chuva", espaco_id=4)

    # Act
    registros = repositorio.listar_para_indice(0, 10)

    # Assert
    assert [(r.reserva_id, r.situacao, r.criada_em) for r in registros] == [
        (primeira.id, S.SOLICITADA, AGORA),
        (segunda.id, S.CANCELADA, AGORA),
    ]


def test_listar_para_indice_em_lotes_cobre_todas_sem_repetir(repositorio):
    # Arrange
    salvas = _salvar_varias(repositorio, 5)

    # Act
    lidos, ultimo = [], 0
    while lote := repositorio.listar_para_indice(ultimo, 2):
        assert len(lote) <= 2
        lidos.extend(r.reserva_id for r in lote)
        ultimo = lote[-1].reserva_id

    # Assert
    assert lidos == [reserva.id for reserva in salvas]


def test_listar_para_indice_depois_do_ultimo_id_devolve_vazio(repositorio):
    salvas = _salvar_varias(repositorio, 2)

    assert repositorio.listar_para_indice(salvas[-1].id, 10) == []


@pytest.mark.django_db
def test_listar_para_indice_no_banco_le_so_tres_colunas_em_uma_consulta():
    # Arrange
    repositorio = RepositorioReservasDjango()
    _salvar_varias(repositorio, 3)

    # Act
    with CaptureQueriesContext(connection) as consultas:
        repositorio.listar_para_indice(0, 2)

    # Assert
    assert len(consultas) == 1
    sql = consultas[0]["sql"]
    assert "LIMIT 2" in sql
    assert "finalidade" not in sql
    assert "reservas_registro_de_situacao" not in sql
