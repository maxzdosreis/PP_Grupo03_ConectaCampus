from django.urls import path

from reservas.api.views import (
    HistoricoDaReservaView,
    RegrasDeAgendaView,
    ReservaDetalheView,
    ReservaSituacaoView,
    ReservasView,
    SituacoesDeReservaView,
)

app_name = "reservas"

urlpatterns = [
    path("", ReservasView.as_view(), name="lista"),
    path("situacoes/", SituacoesDeReservaView.as_view(), name="situacoes"),
    path("regras-de-agenda/", RegrasDeAgendaView.as_view(), name="regras_de_agenda"),
    path("<int:reserva_id>/", ReservaDetalheView.as_view(), name="detalhe"),
    path("<int:reserva_id>/situacao/", ReservaSituacaoView.as_view(), name="situacao"),
    path(
        "<int:reserva_id>/historico/",
        HistoricoDaReservaView.as_view(),
        name="historico",
    ),
]
