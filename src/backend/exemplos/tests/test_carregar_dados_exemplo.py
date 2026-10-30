from datetime import timedelta
from io import StringIO

import pytest
from django.core.management import CommandError, call_command
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from contas.domain.perfil import PerfilUsuario
from contas.infrastructure.models import Usuario
from espacos.api.dependencias import listar_espacos
from espacos.domain.tipo_espaco import TipoEspaco
from exemplos.dados import (
    CONFLITO_PARA_DEMONSTRACAO,
    ESPACOS,
    GESTOR,
    RESERVAS,
    SOLICITANTES,
    USUARIOS,
    EspacoDeExemplo,
)
from reservas.api.dependencias import consultar_reservas
from reservas.application.repositorio import FiltrosDeReservas
from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.conflito_de_horario import garantir_horario_livre
from reservas.domain.situacao import SituacaoReserva
from reservas.infrastructure.repositorio_django import RepositorioReservasDjango
from reservas.tests.historico import verificar_historico_coerente

pytestmark = pytest.mark.django_db

URL_LOGIN = reverse("contas:login")
URL_RESERVAS = reverse("reservas:lista")
COMANDO = "carregar_dados_exemplo"
EMAIL_DO_README = "ana@exemplo.com"
MATRICULA_DO_README = "2026001"
QUALQUER_GESTOR = Ator(usuario_id=1, nome="Gestora de Teste", papel=PapelDoAtor.GESTOR)


@pytest.fixture(autouse=True)
def debug_ligado(settings):
    settings.DEBUG = True


def _carregar():
    saida = StringIO()
    call_command(COMANDO, stdout=saida)
    return saida.getvalue()


def _reservas():
    return consultar_reservas().executar(FiltrosDeReservas(), ator=QUALQUER_GESTOR)


def _espacos():
    return listar_espacos().executar()


def _quantidades():
    return Usuario.objects.count(), len(_espacos()), len(_reservas())


def test_cria_um_gestor_e_dois_solicitantes():
    # Act
    _carregar()

    # Assert
    gestores = Usuario.objects.filter(perfil=PerfilUsuario.GESTOR)
    assert gestores.count() == 1
    assert gestores.get().is_staff
    assert gestores.get().is_superuser
    assert Usuario.objects.filter(perfil=PerfilUsuario.SOLICITANTE).count() == 2


def test_cria_um_espaco_de_cada_tipo_e_um_inativo():
    # Act
    _carregar()

    # Assert
    espacos = _espacos()
    assert len(espacos) == len(ESPACOS)
    assert {espaco.tipo for espaco in espacos} == set(TipoEspaco)
    assert [espaco.nome for espaco in espacos if not espaco.ativo] == [
        "Quadra de Tênis 2"
    ]


def test_cria_uma_reserva_de_cada_situacao():
    # Act
    _carregar()

    # Assert
    situacoes = [reserva.situacao for reserva in _reservas()]
    assert sorted(situacoes) == sorted(SituacaoReserva)


def test_reservas_cobrem_os_dois_solicitantes_e_pelo_menos_tres_espacos():
    # Act
    _carregar()

    # Assert
    reservas = _reservas()
    assert {r.solicitante.matricula for r in reservas} == {
        s.matricula for s in SOLICITANTES
    }
    assert len({r.espaco_id for r in reservas}) >= 3


def test_rodar_duas_vezes_nao_duplica_e_informa_que_ja_existiam():
    # Arrange
    _carregar()
    quantidades_depois_da_primeira = _quantidades()

    # Act
    saida = _carregar()

    # Assert
    assert _quantidades() == quantidades_depois_da_primeira
    assert "Usuários: 0 criados, 3 já existiam." in saida
    assert f"Espaços: 0 criados, {len(ESPACOS)} já existiam." in saida
    assert f"Reservas: 0 criadas, {len(RESERVAS)} já existiam." in saida


def test_primeira_execucao_informa_o_que_foi_criado():
    # Act
    saida = _carregar()

    # Assert
    assert "Usuários: 3 criados, 0 já existiam." in saida
    assert f"Reservas: {len(RESERVAS)} criadas, 0 já existiam." in saida
    for usuario in USUARIOS:
        assert usuario.email in saida
        assert usuario.senha in saida


def test_com_debug_desligado_recusa_sem_criar_nada(settings):
    # Arrange
    settings.DEBUG = False

    # Act / Assert
    with pytest.raises(CommandError, match="DJANGO_DEBUG=True"):
        _carregar()
    assert _quantidades() == (0, 0, 0)


def test_falha_no_meio_da_carga_nao_deixa_nada_gravado(monkeypatch):
    # Arrange
    def falhar(*args, **kwargs):
        raise RuntimeError("falha simulada")

    monkeypatch.setattr(
        "exemplos.management.commands.carregar_dados_exemplo.garantir_reservas",
        falhar,
    )

    # Act / Assert
    with pytest.raises(RuntimeError):
        _carregar()
    assert _quantidades() == (0, 0, 0)


def test_dado_de_exemplo_que_viola_regra_faz_o_comando_falhar(monkeypatch):
    # Arrange
    invalido = EspacoDeExemplo("Quadra Vazia", TipoEspaco.GINASIO, 0)
    monkeypatch.setattr("exemplos.carga.ESPACOS", (invalido,))

    # Act / Assert
    with pytest.raises(CommandError, match="Dado de exemplo inválido"):
        _carregar()
    assert _quantidades() == (0, 0, 0)


@pytest.mark.parametrize("usuario", USUARIOS, ids=lambda usuario: usuario.email)
def test_login_com_cada_usuario_de_exemplo(usuario):
    # Arrange
    _carregar()

    # Act
    resposta = APIClient().post(
        URL_LOGIN, {"email": usuario.email, "senha": usuario.senha}, format="json"
    )

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["dados"]["usuario"]["perfil"] == usuario.perfil.value


def test_reservas_em_aberto_sao_futuras_e_a_concluida_e_passada():
    # Arrange
    hoje = timezone.localdate()

    # Act
    _carregar()

    # Assert
    for reserva in _reservas():
        if reserva.situacao == SituacaoReserva.CONCLUIDA:
            assert reserva.intervalo.data < hoje
        else:
            assert reserva.intervalo.data > hoje


def test_todas_as_reservas_de_exemplo_tem_historico_coerente():
    # Act
    _carregar()

    # Assert
    repositorio = RepositorioReservasDjango()
    for reserva in _reservas():
        historico = repositorio.listar_historico(reserva.id)
        verificar_historico_coerente(historico, reserva.situacao)
        assert historico[0].registrado_em == reserva.criada_em


def test_concluida_passou_por_solicitada_e_confirmada_em_dias_diferentes():
    # Arrange
    agora = timezone.now()

    # Act
    _carregar()

    # Assert
    concluida = next(r for r in _reservas() if r.situacao is SituacaoReserva.CONCLUIDA)
    historico = RepositorioReservasDjango().listar_historico(concluida.id)
    assert [r.situacao_nova for r in historico] == [
        SituacaoReserva.SOLICITADA,
        SituacaoReserva.CONFIRMADA,
        SituacaoReserva.CONCLUIDA,
    ]
    solicitada, confirmada, concluida_em = (r.registrado_em for r in historico)
    assert solicitada < confirmada < concluida.intervalo.inicio() < concluida_em
    assert abs(agora - timedelta(days=3) - solicitada) < timedelta(minutes=1)
    assert historico[-1].autor_nome == GESTOR.nome


def test_reservas_que_ocupam_horario_nao_se_sobrepoem():
    # Act
    _carregar()

    # Assert
    reservas = _reservas()
    for reserva in reservas:
        if reserva.situacao.ocupa_horario:
            garantir_horario_livre(reserva, reservas)


def test_horario_de_conflito_documentado_responde_409():
    # Arrange
    _carregar()
    cliente = APIClient()
    cliente.force_authenticate(
        user=Usuario.objects.get_by_natural_key(SOLICITANTES[0].email)
    )
    conflito = CONFLITO_PARA_DEMONSTRACAO
    espaco = next(e for e in _espacos() if e.nome == conflito.espaco)
    data = timezone.localdate() + timedelta(days=conflito.dias_a_partir_de_hoje)

    # Act
    resposta = cliente.post(
        URL_RESERVAS,
        {
            "espaco_id": espaco.id,
            "data": data.isoformat(),
            "hora_inicio": f"{conflito.hora_inicio:%H:%M}",
            "hora_fim": f"{conflito.hora_fim:%H:%M}",
            "finalidade": "Demonstração do conflito",
        },
        format="json",
    )

    # Assert
    assert resposta.status_code == 409
    assert resposta.data["erro"]["codigo"] == "CONFLITO_DE_HORARIO"


def test_horario_de_conflito_documentado_aparece_ocupado_na_agenda_do_dia():
    # Arrange
    _carregar()
    conflito = CONFLITO_PARA_DEMONSTRACAO
    espaco = next(e for e in _espacos() if e.nome == conflito.espaco)
    data = timezone.localdate() + timedelta(days=conflito.dias_a_partir_de_hoje)
    dono = next(r for r in _reservas() if r.espaco_id == espaco.id).solicitante
    outro = next(s for s in SOLICITANTES if s.matricula != dono.matricula)
    cliente = APIClient()
    cliente.force_authenticate(user=Usuario.objects.get_by_natural_key(outro.email))

    # Act
    resposta = cliente.get(
        reverse("reservas:ocupacao"), {"espaco": espaco.id, "data": data.isoformat()}
    )

    # Assert
    assert resposta.status_code == 200
    ocupados = resposta.data["dados"]["ocupados"]
    assert [(o["hora_inicio"], o["hora_fim"]) for o in ocupados] == [("10:00", "11:00")]
    inicio, fim = (f"{conflito.hora_inicio:%H:%M}", f"{conflito.hora_fim:%H:%M}")
    assert ocupados[0]["hora_inicio"] < fim
    assert inicio < ocupados[0]["hora_fim"]
    assert dono.nome not in str(resposta.data)


def test_nenhum_dado_de_exemplo_usa_o_usuario_do_readme():
    # Act
    _carregar()

    # Assert
    assert not Usuario.objects.filter(email__iexact=EMAIL_DO_README).exists()
    assert not Usuario.objects.filter(matricula=MATRICULA_DO_README).exists()
    assert all(u.email != EMAIL_DO_README for u in USUARIOS)
    assert all(u.matricula != MATRICULA_DO_README for u in USUARIOS)
