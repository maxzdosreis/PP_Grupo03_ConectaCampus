from django.core.cache import cache


def cliente(chave: str, *, escrita: bool):
    return cache._cache.get_client(chave, write=escrita)


def texto(valor: bytes | str) -> str:
    return valor.decode() if isinstance(valor, bytes) else valor
