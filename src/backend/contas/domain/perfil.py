from enum import StrEnum


class PerfilUsuario(StrEnum):
    SOLICITANTE = "SOLICITANTE"
    GESTOR = "GESTOR"

    @property
    def rotulo(self) -> str:
        return _ROTULOS[self]


_ROTULOS = {
    PerfilUsuario.SOLICITANTE: "Solicitante",
    PerfilUsuario.GESTOR: "Gestor",
}
