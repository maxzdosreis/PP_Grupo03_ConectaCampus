from django.core.management.base import BaseCommand, CommandError

from reservas.api.dependencias import reconstruir_agenda
from reservas.application.portas import AgendaIndisponivel
from reservas.application.reconstruir_agenda import ResultadoDaReconstrucao

MENSAGEM_REDIS_INDISPONIVEL = (
    "O Redis ficou indisponível durante a reconstrução da agenda. Os dias já "
    "refeitos continuam válidos; rode o comando de novo quando ele voltar."
)


class Command(BaseCommand):
    help = (
        "Refaz a agenda do Redis (de hoje em diante) a partir do PostgreSQL. "
        "É seguro rodar várias vezes e pode ser usado depois de reiniciar o Redis."
    )

    def handle(self, *args, **options):
        try:
            resultado = reconstruir_agenda().executar()
        except AgendaIndisponivel as erro:
            raise CommandError(MENSAGEM_REDIS_INDISPONIVEL) from erro
        self.stdout.write(self.style.SUCCESS(_resumo(resultado)))
        if resultado.dias_descartados:
            self.stdout.write(self.style.WARNING(_aviso(resultado.dias_descartados)))


def _plural(quantidade: int, singular: str, plural: str) -> str:
    return f"{quantidade} {singular if quantidade == 1 else plural}"


def _resumo(resultado: ResultadoDaReconstrucao) -> str:
    dias = _plural(resultado.dias_refeitos, "dia", "dias")
    reservas = _plural(resultado.reservas_gravadas, "reserva", "reservas")
    esvaziados = _plural(resultado.dias_esvaziados, "dia esvaziado", "dias esvaziados")
    return f"Agenda reconstruída: {dias}, {reservas}, {esvaziados}."


def _aviso(descartados: int) -> str:
    dias = _plural(descartados, "dia foi descartado", "dias foram descartados")
    return (
        f"{dias.capitalize()} porque as reservas mudaram durante a reconstrução; "
        "rode o comando de novo."
    )
