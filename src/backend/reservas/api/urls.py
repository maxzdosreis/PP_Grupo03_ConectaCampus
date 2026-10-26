from django.urls import path

from reservas.api.views import (
    ReservaDetalheView,
    ReservaSituacaoView,
    ReservasView,
    SituacoesDeReservaView,
)

app_name = "reservas"

urlpatterns = [
    path("", ReservasView.as_view(), name="lista"),
    path("situacoes/", SituacoesDeReservaView.as_view(), name="situacoes"),
    path("<int:reserva_id>/", ReservaDetalheView.as_view(), name="detalhe"),
    path("<int:reserva_id>/situacao/", ReservaSituacaoView.as_view(), name="situacao"),
]
