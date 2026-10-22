from django.urls import path

from reservas.api.views import ReservaDetalheView, ReservasView

app_name = "reservas"

urlpatterns = [
    path("", ReservasView.as_view(), name="lista"),
    path("<int:reserva_id>/", ReservaDetalheView.as_view(), name="detalhe"),
]
