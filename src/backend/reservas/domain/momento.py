from datetime import datetime


def exigir_fuso(momento: datetime, nome: str) -> None:
    if not isinstance(momento, datetime) or momento.utcoffset() is None:
        raise TypeError(f"{nome} deve ser um datetime com fuso horário.")
