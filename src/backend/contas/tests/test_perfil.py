import pytest

from contas.domain.perfil import PerfilUsuario


@pytest.mark.parametrize(
    ("perfil", "eh_gestor"),
    [(PerfilUsuario.GESTOR, True), (PerfilUsuario.SOLICITANTE, False)],
)
def test_so_o_perfil_gestor_eh_gestor(perfil, eh_gestor):
    # Assert
    assert perfil.eh_gestor is eh_gestor


def test_perfil_lido_do_banco_como_texto_tambem_responde_eh_gestor():
    # Act
    perfil = PerfilUsuario("GESTOR")

    # Assert
    assert perfil.eh_gestor is True
