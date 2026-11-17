from django.core.exceptions import ImproperlyConfigured

from espacos.application.portas import ReservasDoEspaco

_registrada: ReservasDoEspaco | None = None


def registrar(consulta: ReservasDoEspaco) -> None:
    global _registrada
    _registrada = consulta


def consulta_registrada() -> ReservasDoEspaco:
    if _registrada is None:
        raise ImproperlyConfigured(
            "Nenhuma consulta de reservas foi registrada em espacos.publico."
        )
    return _registrada
