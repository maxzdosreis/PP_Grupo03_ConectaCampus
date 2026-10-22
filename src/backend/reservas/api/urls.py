from django.urls import path

from reservas.api.views import ReservasView

app_name = "reservas"

urlpatterns = [
    path("", ReservasView.as_view(), name="lista"),
]
