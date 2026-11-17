from django.apps import AppConfig


class ReservasConfig(AppConfig):
    name = "reservas"
    verbose_name = "Reservas"

    def ready(self) -> None:
        from espacos.publico import registrar_reservas_do_espaco
        from reservas.api.dependencias import ReservasDoEspacoViaCasoDeUso

        registrar_reservas_do_espaco(ReservasDoEspacoViaCasoDeUso())
