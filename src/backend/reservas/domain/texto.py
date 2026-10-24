from compartilhado.domain.erros import TextoMuitoLongo


def normalizar_espacos(texto: str | None) -> str:
    return " ".join((texto or "").split())


def exigir_tamanho_maximo(texto: str, *, campo: str, rotulo: str, limite: int) -> str:
    if len(texto) > limite:
        raise TextoMuitoLongo(campo, rotulo, limite)
    return texto
