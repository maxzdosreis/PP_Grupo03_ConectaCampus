from enum import StrEnum


class TipoEspaco(StrEnum):
    QUADRA_POLIESPORTIVA = "QUADRA_POLIESPORTIVA"
    CAMPO_DE_FUTEBOL = "CAMPO_DE_FUTEBOL"
    GINASIO = "GINASIO"
    QUADRA_DE_AREIA = "QUADRA_DE_AREIA"
    QUADRA_DE_TENIS = "QUADRA_DE_TENIS"

    @property
    def rotulo(self) -> str:
        return _ROTULOS[self]


_ROTULOS = {
    TipoEspaco.QUADRA_POLIESPORTIVA: "Quadra poliesportiva",
    TipoEspaco.CAMPO_DE_FUTEBOL: "Campo de futebol",
    TipoEspaco.GINASIO: "Ginásio",
    TipoEspaco.QUADRA_DE_AREIA: "Quadra de areia",
    TipoEspaco.QUADRA_DE_TENIS: "Quadra de tênis",
}
