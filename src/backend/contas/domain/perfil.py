from enum import StrEnum


class PerfilUsuario(StrEnum):
    SOLICITANTE = "SOLICITANTE"
    GESTOR = "GESTOR"

    @property
    def rotulo(self) -> str:
        return _ROTULOS[self]

    @property
    def eh_gestor(self) -> bool:
        return self is PerfilUsuario.GESTOR


_ROTULOS = {
    PerfilUsuario.SOLICITANTE: "Solicitante",
    PerfilUsuario.GESTOR: "Gestor",
}
