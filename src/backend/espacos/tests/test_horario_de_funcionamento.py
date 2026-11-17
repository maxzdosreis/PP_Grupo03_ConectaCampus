from datetime import time

import pytest
from hypothesis import given
from hypothesis import strategies as st

from compartilhado.domain.erros import CampoObrigatorioAusente
from espacos.application.casos_de_uso import CadastrarEspaco, EditarEspaco
from espacos.domain.excecoes import (
    HorarioDeFuncionamentoInvalido,
    HorarioIncompativelComReservas,
    JanelaDeFuncionamentoCurta,
    NenhumaAlteracaoInformada,
)
from espacos.domain.horario_de_funcionamento import (
    JANELA_MINIMA_EM_MINUTOS,
    MINUTOS_NO_DIA,
    HorarioDeFuncionamento,
)
from espacos.tests.fakes import (
    RepositorioEspacosEmMemoria,
    ReservasDoEspacoFake,
    dados_validos,
    novo_espaco,
)


def test_horario_padrao_e_das_07_a_meia_noite_do_fim_do_dia():
    # Act
    horario = HorarioDeFuncionamento.padrao()

    # Assert
    assert (horario.abertura_em_minutos, horario.fechamento_em_minutos) == (420, 1440)
    assert horario.abertura() == time(7, 0)
    assert horario.fechamento() == time(0, 0)
    assert str(horario) == "07:00 às 00:00"


def test_fechamento_00_00_e_o_fim_do_dia_e_a_abertura_00_00_e_o_comeco():
    # Act
    dia_inteiro = HorarioDeFuncionamento.de_horas(time(0, 0), time(0, 0))
    ate_meia_noite = HorarioDeFuncionamento.de_horas(time(7, 0), time(0, 0))

    # Assert
    assert (dia_inteiro.abertura_em_minutos, dia_inteiro.fechamento_em_minutos) == (
        0,
        1440,
    )
    assert ate_meia_noite == HorarioDeFuncionamento.padrao()


@pytest.mark.parametrize(
    ("abertura", "fechamento", "esperado"),
    [
        (time(8, 0), time(22, 0), (480, 1320)),
        (time(10, 0), time(14, 30), (600, 870)),
        (time(23, 29), time(23, 59), (1409, 1439)),
        (time(0, 1), time(0, 31), (1, 31)),
    ],
    ids=[
        "08-22",
        "10-14h30",
        "ultima-janela-do-dia",
        "abre-um-minuto-depois-da-meia-noite",
    ],
)
def test_de_horas_converte_para_minutos_desde_a_meia_noite(
    abertura, fechamento, esperado
):
    # Act
    horario = HorarioDeFuncionamento.de_horas(abertura, fechamento)

    # Assert
    assert (horario.abertura_em_minutos, horario.fechamento_em_minutos) == esperado
    assert (horario.abertura(), horario.fechamento()) == (abertura, fechamento)


def test_janela_de_exatamente_30_minutos_e_aceita():
    # Act
    horario = HorarioDeFuncionamento.de_horas(time(10, 0), time(10, 30))

    # Assert
    assert horario.fechamento_em_minutos - horario.abertura_em_minutos == 30


def test_janela_de_29_minutos_e_recusada_no_fechamento():
    # Act
    with pytest.raises(JanelaDeFuncionamentoCurta) as erro:
        HorarioDeFuncionamento.de_horas(time(10, 0), time(10, 29))

    # Assert
    assert erro.value.codigo == "JANELA_DE_FUNCIONAMENTO_CURTA"
    assert erro.value.campo == "fechamento"
    assert erro.value.minimo_em_minutos == JANELA_MINIMA_EM_MINUTOS == 30
    assert erro.value.mensagem == "O espaço deve funcionar por pelo menos 30 minutos."


@pytest.mark.parametrize(
    ("abertura", "fechamento"),
    [(time(10, 0), time(9, 0)), (time(10, 0), time(10, 0)), (time(23, 0), time(22, 0))],
    ids=["antes", "igual", "noite"],
)
def test_fechamento_que_nao_e_depois_da_abertura_e_recusado(abertura, fechamento):
    # Act
    with pytest.raises(HorarioDeFuncionamentoInvalido) as erro:
        HorarioDeFuncionamento.de_horas(abertura, fechamento)

    # Assert
    assert erro.value.codigo == "HORARIO_DE_FUNCIONAMENTO_INVALIDO"
    assert erro.value.campo == "fechamento"
    assert erro.value.mensagem == "O fechamento deve ser depois da abertura."


@pytest.mark.parametrize(
    ("abertura", "fechamento", "campo", "rotulo"),
    [
        (None, time(22, 0), "abertura", "Abertura"),
        (time(8, 0), None, "fechamento", "Fechamento"),
    ],
)
def test_abertura_e_fechamento_sao_obrigatorios(abertura, fechamento, campo, rotulo):
    # Act
    with pytest.raises(CampoObrigatorioAusente) as erro:
        HorarioDeFuncionamento.de_horas(abertura, fechamento)

    # Assert
    assert erro.value.campo == campo
    assert erro.value.mensagem == f'O campo "{rotulo}" é obrigatório.'


@pytest.mark.parametrize("valor", ["07:00", 7, 7.5])
def test_horas_que_nao_sao_time_sao_recusadas(valor):
    # Act / Assert
    with pytest.raises(HorarioDeFuncionamentoInvalido) as erro:
        HorarioDeFuncionamento.de_horas(valor, time(22, 0))
    assert erro.value.campo == "abertura"
    with pytest.raises(HorarioDeFuncionamentoInvalido) as erro:
        HorarioDeFuncionamento.de_horas(time(8, 0), valor)
    assert erro.value.campo == "fechamento"


@pytest.mark.parametrize(
    ("abertura", "fechamento", "campo"),
    [
        (-1, 600, "abertura"),
        (1440, 1440, "abertura"),
        (True, 600, "abertura"),
        ("420", 600, "abertura"),
        (420, 1441, "fechamento"),
        (420, False, "fechamento"),
        (420, None, "fechamento"),
    ],
    ids=[
        "negativa",
        "abre-no-fim-do-dia",
        "bool",
        "texto",
        "alem-de-24h",
        "bool-fim",
        "nulo",
    ],
)
def test_minutos_fora_do_dia_ou_de_tipo_errado_sao_recusados(
    abertura, fechamento, campo
):
    # Act
    with pytest.raises(HorarioDeFuncionamentoInvalido) as erro:
        HorarioDeFuncionamento(abertura, fechamento)

    # Assert
    assert erro.value.campo == campo


def test_mensagem_de_abertura_invalida_pede_um_horario_do_dia():
    # Act
    with pytest.raises(HorarioDeFuncionamentoInvalido) as erro:
        HorarioDeFuncionamento(1440, 1440)

    # Assert
    assert erro.value.mensagem == "Informe um horário de abertura entre 00:00 e 23:59."


def test_com_troca_so_o_que_foi_informado():
    # Arrange
    horario = HorarioDeFuncionamento.de_horas(time(8, 0), time(18, 0))

    # Act / Assert
    assert horario.com(fechamento=time(22, 0)) == HorarioDeFuncionamento.de_horas(
        time(8, 0), time(22, 0)
    )
    assert horario.com(abertura=time(9, 0)) == HorarioDeFuncionamento.de_horas(
        time(9, 0), time(18, 0)
    )
    assert horario.com(fechamento=time(0, 0)).fechamento_em_minutos == MINUTOS_NO_DIA
    assert horario.com() == horario


def test_horario_e_imutavel_e_comparado_pelo_valor():
    # Arrange
    horario = HorarioDeFuncionamento(480, 1320)

    # Act / Assert
    assert horario == HorarioDeFuncionamento(480, 1320)
    assert hash(horario) == hash(HorarioDeFuncionamento(480, 1320))
    with pytest.raises(AttributeError):
        horario.abertura_em_minutos = 0


@given(
    abertura=st.integers(0, MINUTOS_NO_DIA - JANELA_MINIMA_EM_MINUTOS),
    dados=st.data(),
)
def test_converter_para_horas_e_voltar_devolve_o_mesmo_horario(abertura, dados):
    # Arrange
    fechamento = dados.draw(
        st.integers(abertura + JANELA_MINIMA_EM_MINUTOS, MINUTOS_NO_DIA)
    )
    horario = HorarioDeFuncionamento(abertura, fechamento)

    # Act
    de_volta = HorarioDeFuncionamento.de_horas(horario.abertura(), horario.fechamento())

    # Assert
    assert de_volta == horario
    assert (horario.fechamento() == time(0, 0)) is (fechamento == MINUTOS_NO_DIA)


@given(
    abertura=st.integers(0, MINUTOS_NO_DIA - 1),
    fechamento=st.integers(0, MINUTOS_NO_DIA),
)
def test_so_e_valido_o_horario_com_fechamento_depois_da_abertura_e_janela_minima(
    abertura, fechamento
):
    # Arrange
    valido = fechamento - abertura >= JANELA_MINIMA_EM_MINUTOS

    # Act
    try:
        HorarioDeFuncionamento(abertura, fechamento)
        aceito = True
    except (HorarioDeFuncionamentoInvalido, JanelaDeFuncionamentoCurta):
        aceito = False

    # Assert
    assert aceito is valido


def test_espaco_novo_tem_o_horario_padrao():
    # Act
    espaco = novo_espaco()

    # Assert
    assert espaco.horario == HorarioDeFuncionamento.padrao()
    assert espaco.estado.horario == HorarioDeFuncionamento.padrao()


def test_espaco_com_horario_proprio_guarda_o_horario():
    # Arrange
    horario = HorarioDeFuncionamento.de_horas(time(8, 0), time(22, 0))

    # Act
    espaco = novo_espaco(horario=horario)

    # Assert
    assert espaco.horario is horario
    assert "08:00 às 22:00" in repr(espaco)


def test_alterar_so_o_fechamento_mantem_a_abertura():
    # Arrange
    espaco = novo_espaco()

    # Act
    espaco.alterar_dados(fechamento=time(22, 0))

    # Assert
    assert espaco.horario.abertura() == time(7, 0)
    assert espaco.horario.fechamento() == time(22, 0)


def test_alterar_so_o_horario_conta_como_alteracao():
    # Arrange
    espaco = novo_espaco()

    # Act
    espaco.alterar_dados(abertura=time(9, 0))

    # Assert
    assert espaco.horario.abertura() == time(9, 0)


def test_alterar_dados_sem_nada_informado_continua_recusado():
    # Act / Assert
    with pytest.raises(NenhumaAlteracaoInformada):
        novo_espaco().alterar_dados()


def test_horario_invalido_na_edicao_nao_muda_nada():
    # Arrange
    espaco = novo_espaco(nome="Quadra Central")

    # Act
    with pytest.raises(HorarioDeFuncionamentoInvalido):
        espaco.alterar_dados(
            nome="Outro Nome", abertura=time(23, 0), fechamento=time(22, 0)
        )

    # Assert
    assert espaco.nome == "Quadra Central"
    assert espaco.horario == HorarioDeFuncionamento.padrao()


def test_estado_de_origem_inclui_o_horario():
    # Arrange
    espaco = novo_espaco()
    original = espaco.estado_de_origem

    # Act
    espaco.alterar_dados(fechamento=time(22, 0))

    # Assert
    assert espaco.estado_de_origem == original
    assert espaco.estado != original
    assert espaco.estado.horario.fechamento() == time(22, 0)


def test_cadastrar_sem_horario_grava_o_padrao_das_07_a_meia_noite():
    # Arrange
    repositorio = RepositorioEspacosEmMemoria()

    # Act
    espaco = CadastrarEspaco(repositorio).executar(**dados_validos())

    # Assert
    guardado = repositorio.obter_por_id(espaco.id)
    assert guardado.horario == HorarioDeFuncionamento.padrao()


def test_cadastrar_com_horario_proprio_grava_o_horario():
    # Arrange
    repositorio = RepositorioEspacosEmMemoria()

    # Act
    espaco = CadastrarEspaco(repositorio).executar(
        **dados_validos(abertura=time(8, 0), fechamento=time(22, 0))
    )

    # Assert
    assert repositorio.obter_por_id(espaco.id).horario == (
        HorarioDeFuncionamento.de_horas(time(8, 0), time(22, 0))
    )


def test_cadastrar_so_com_o_fechamento_usa_a_abertura_padrao():
    # Arrange
    repositorio = RepositorioEspacosEmMemoria()

    # Act
    espaco = CadastrarEspaco(repositorio).executar(
        **dados_validos(fechamento=time(22, 0))
    )

    # Assert
    assert espaco.horario.abertura() == time(7, 0)
    assert espaco.horario.fechamento() == time(22, 0)


def test_cadastrar_com_horario_invalido_nao_grava():
    # Arrange
    repositorio = RepositorioEspacosEmMemoria()

    # Act
    with pytest.raises(HorarioDeFuncionamentoInvalido):
        CadastrarEspaco(repositorio).executar(
            **dados_validos(abertura=time(20, 0), fechamento=time(10, 0))
        )

    # Assert
    assert repositorio.chamadas_de_salvar == 0


def _espaco_cadastrado(repositorio):
    return CadastrarEspaco(repositorio).executar(**dados_validos())


def test_editar_o_horario_sem_reservas_fora_da_nova_janela_grava():
    # Arrange
    repositorio = RepositorioEspacosEmMemoria()
    reservas = ReservasDoEspacoFake(fora_da_janela=0)
    cadastrado = _espaco_cadastrado(repositorio)

    # Act
    editado = EditarEspaco(repositorio, reservas).executar(
        cadastrado.id, abertura=time(8, 0), fechamento=time(22, 0)
    )

    # Assert
    assert editado.horario == HorarioDeFuncionamento.de_horas(time(8, 0), time(22, 0))
    assert repositorio.obter_por_id(cadastrado.id).horario == editado.horario
    assert reservas.consultas == [(cadastrado.id, 480, 1320)]


@pytest.mark.parametrize(
    ("fora", "mensagem"),
    [
        (
            1,
            "Não é possível alterar o horário: 1 reserva ativa ficaria fora do novo "
            "horário. Cancele ou conclua essas reservas antes de reduzir o horário.",
        ),
        (
            3,
            "Não é possível alterar o horário: 3 reservas ativas ficariam fora do novo "
            "horário. Cancele ou conclua essas reservas antes de reduzir o horário.",
        ),
    ],
    ids=["uma", "varias"],
)
def test_editar_o_horario_com_reservas_ativas_fora_da_nova_janela_e_recusado(
    fora, mensagem
):
    # Arrange
    repositorio = RepositorioEspacosEmMemoria()
    cadastrado = _espaco_cadastrado(repositorio)
    gravacoes_antes = repositorio.chamadas_de_salvar

    # Act
    with pytest.raises(HorarioIncompativelComReservas) as erro:
        EditarEspaco(repositorio, ReservasDoEspacoFake(fora)).executar(
            cadastrado.id, fechamento=time(18, 0), nome="Nome Novo"
        )

    # Assert
    assert erro.value.codigo == "HORARIO_INCOMPATIVEL_COM_RESERVAS"
    assert erro.value.quantidade == fora
    assert erro.value.mensagem == mensagem
    guardado = repositorio.obter_por_id(cadastrado.id)
    assert guardado.horario == HorarioDeFuncionamento.padrao()
    assert guardado.nome == "Ginásio A"
    assert repositorio.chamadas_de_salvar == gravacoes_antes


def test_editar_sem_mudar_o_horario_nao_consulta_as_reservas():
    # Arrange
    repositorio = RepositorioEspacosEmMemoria()
    reservas = ReservasDoEspacoFake(fora_da_janela=5)
    cadastrado = _espaco_cadastrado(repositorio)

    # Act
    EditarEspaco(repositorio, reservas).executar(cadastrado.id, capacidade=80)
    EditarEspaco(repositorio, reservas).executar(
        cadastrado.id, abertura=time(7, 0), fechamento=time(0, 0)
    )

    # Assert
    assert reservas.consultas == []


def test_ampliar_o_horario_tambem_pergunta_as_reservas_e_aceita_quando_nao_ha_fora():
    # Arrange
    repositorio = RepositorioEspacosEmMemoria()
    reservas = ReservasDoEspacoFake()
    cadastrado = CadastrarEspaco(repositorio).executar(
        **dados_validos(abertura=time(10, 0), fechamento=time(14, 0))
    )

    # Act
    EditarEspaco(repositorio, reservas).executar(
        cadastrado.id, abertura=time(7, 0), fechamento=time(0, 0)
    )

    # Assert
    assert reservas.consultas == [(cadastrado.id, 420, 1440)]
