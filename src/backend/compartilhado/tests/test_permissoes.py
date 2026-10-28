from types import SimpleNamespace

import pytest

from compartilhado.api.permissoes import ApenasGestor


def _requisicao_de(usuario):
    return SimpleNamespace(user=usuario)


@pytest.mark.parametrize(
    ("usuario", "permitido"),
    [
        (SimpleNamespace(eh_gestor=True), True),
        (SimpleNamespace(eh_gestor=False), False),
        (SimpleNamespace(), False),
    ],
    ids=["gestor", "nao-gestor", "sem-o-atributo"],
)
def test_apenas_gestor_le_eh_gestor_do_usuario(usuario, permitido):
    # Act
    resultado = ApenasGestor().has_permission(_requisicao_de(usuario), view=None)

    # Assert
    assert resultado is permitido
