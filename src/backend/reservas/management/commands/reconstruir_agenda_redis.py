from django.core.management.base import BaseCommand, CommandError

from reservas.api.dependencias import reconstruir_agenda, reconstruir_indice
from reservas.application.portas import AgendaIndisponivel, IndiceIndisponivel
from reservas.application.reconstruir_agenda import ResultadoDaReconstrucao
from reservas.application.reconstruir_indice import ResultadoDaReconstrucaoDoIndice

MENSAGEM_REDIS_INDISPONIVEL = (
    "O Redis ficou indisponível durante a reconstrução da agenda. Os dias já "
    "refeitos continuam válidos; rode o comando de novo quando ele voltar."
)
MENSAGEM_INDICE_INDISPONIVEL = (
    "A agenda foi reconstruída, mas o Redis ficou indisponível durante a "
    "reconstrução das filas e contagens, que continuam como estavam; rode o "
    "comando de novo quando ele voltar."
)


class Command(BaseCommand):
    help = (
        "Refaz no Redis, a partir do PostgreSQL, a agenda (de hoje em diante) e "
        "as filas e contagens de reservas por situação. É seguro rodar várias "
        "vezes e pode ser usado depois de reiniciar o Redis."
    )

    def handle(self, *args, **options):
        try:
            resultado = reconstruir_agenda().executar()
        except AgendaIndisponivel as erro:
            raise CommandError(MENSAGEM_REDIS_INDISPONIVEL) from erro
        self.stdout.write(self.style.SUCCESS(_resumo(resultado)))
        if resultado.dias_descartados:
            self.stdout.write(self.style.WARNING(_aviso(resultado.dias_descartados)))
        self._reconstruir_o_indice()

    def _reconstruir_o_indice(self) -> None:
        try:
            indice = reconstruir_indice().executar()
        except IndiceIndisponivel as erro:
            raise CommandError(MENSAGEM_INDICE_INDISPONIVEL) from erro
        if indice.descartado:
            self.stdout.write(self.style.WARNING(_aviso_do_indice()))
        else:
            self.stdout.write(self.style.SUCCESS(_resumo_do_indice(indice)))


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


def _resumo_do_indice(resultado: ResultadoDaReconstrucaoDoIndice) -> str:
    reservas = _plural(resultado.reservas_indexadas, "reserva", "reservas")
    pendentes = _plural(resultado.pendentes, "pendente", "pendentes")
    return f"Filas e contagens reconstruídas: {reservas}, {pendentes}."


def _aviso_do_indice() -> str:
    return (
        "As filas e contagens foram descartadas porque as reservas mudaram "
        "durante a reconstrução; rode o comando de novo."
    )
