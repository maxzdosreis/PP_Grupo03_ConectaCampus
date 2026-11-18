import threading

import pytest
from django.contrib.auth import get_user_model
from django.db import connection

from contas.application.casos_de_uso import AlterarUsuario
from contas.domain.excecoes import UltimoGestorAtivo
from contas.domain.perfil import PerfilUsuario
from contas.infrastructure.models import Usuario
from contas.infrastructure.repositorio_django import RepositorioGestaoDeUsuariosDjango

ESPERA_MAXIMA_S = 10
SENHA = "senha-de-teste-123"

REBAIXAR = {"perfil": PerfilUsuario.SOLICITANTE}
DESATIVAR = {"ativo": False}


class _RepositorioQueSincronizaAntesDaTrava(RepositorioGestaoDeUsuariosDjango):
    def __init__(self, barreira: threading.Barrier) -> None:
        self._barreira = barreira

    def _travar(self, usuario_id):
        self._barreira.wait(timeout=ESPERA_MAXIMA_S)
        return super()._travar(usuario_id)


class _RepositorioSemTrava(RepositorioGestaoDeUsuariosDjango):
    def __init__(self, barreira: threading.Barrier) -> None:
        self._barreira = barreira

    def _travar(self, usuario_id):
        linhas = list(Usuario.objects.filter(pk=usuario_id)) + list(
            Usuario.objects.filter(perfil="GESTOR", is_active=True).exclude(
                pk=usuario_id
            )
        )
        self._barreira.wait(timeout=ESPERA_MAXIMA_S)
        return linhas


@pytest.fixture(autouse=True)
def _hash_de_senha_rapido(settings):
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


def _duas_gestoras():
    modelo = get_user_model()
    primeira = modelo.objects.create_superuser(
        "gestora.um@exemplo.com", SENHA, nome="Gestora Um", matricula="9100001"
    )
    segunda = modelo.objects.create_superuser(
        "gestora.dois@exemplo.com", SENHA, nome="Gestora Dois", matricula="9100002"
    )
    return primeira, segunda


def _executar_em_paralelo(repositorio_de, pedidos):
    barreira = threading.Barrier(len(pedidos))
    resultados = {}

    def executar(nome, ator, alvo, mudanca):
        try:
            AlterarUsuario(repositorio_de(barreira)).executar(
                usuario_id=alvo.pk, ator_id=ator.pk, **mudanca
            )
            resultados[nome] = "ok"
        except UltimoGestorAtivo as erro:
            resultados[nome] = erro
        finally:
            connection.close()

    threads = [threading.Thread(target=executar, args=pedido) for pedido in pedidos]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=ESPERA_MAXIMA_S)
    assert len(resultados) == len(pedidos), "uma das threads não terminou"
    return resultados


def _gestores_ativos():
    return Usuario.objects.filter(perfil="GESTOR", is_active=True).count()


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(
    ("mudanca_de_um", "mudanca_do_outro"),
    [
        pytest.param(REBAIXAR, REBAIXAR, id="rebaixam-um-ao-outro"),
        pytest.param(DESATIVAR, DESATIVAR, id="desativam-um-ao-outro"),
        pytest.param(REBAIXAR, DESATIVAR, id="rebaixa-e-desativa"),
    ],
)
def test_dois_gestores_se_tirando_do_cargo_ao_mesmo_tempo_deixam_um_ativo(
    mudanca_de_um, mudanca_do_outro
):
    # Arrange
    primeira, segunda = _duas_gestoras()

    # Act
    resultados = _executar_em_paralelo(
        _RepositorioQueSincronizaAntesDaTrava,
        [
            ("primeira", primeira, segunda, mudanca_de_um),
            ("segunda", segunda, primeira, mudanca_do_outro),
        ],
    )

    # Assert
    vencedores = [nome for nome, valor in resultados.items() if valor == "ok"]
    assert len(vencedores) == 1, f"os dois passaram: {resultados}"
    (recusa,) = [valor for valor in resultados.values() if valor != "ok"]
    assert isinstance(recusa, UltimoGestorAtivo)
    assert _gestores_ativos() == 1


@pytest.mark.django_db(transaction=True)
def test_sem_a_trava_os_dois_pedidos_passariam_e_nao_sobraria_gestor():
    # Arrange
    primeira, segunda = _duas_gestoras()

    # Act
    resultados = _executar_em_paralelo(
        _RepositorioSemTrava,
        [
            ("primeira", primeira, segunda, REBAIXAR),
            ("segunda", segunda, primeira, REBAIXAR),
        ],
    )

    # Assert
    assert list(resultados.values()) == ["ok", "ok"]
    assert _gestores_ativos() == 0
