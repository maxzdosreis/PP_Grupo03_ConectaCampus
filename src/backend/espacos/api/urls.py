from django.urls import path

from espacos.api.views import (
    AtivarEspacoView,
    DesativarEspacoView,
    EspacoDetalheView,
    EspacosView,
    TiposDeEspacoView,
)

app_name = "espacos"

urlpatterns = [
    path("", EspacosView.as_view(), name="lista"),
    path("tipos/", TiposDeEspacoView.as_view(), name="tipos"),
    path("<int:espaco_id>/", EspacoDetalheView.as_view(), name="detalhe"),
    path("<int:espaco_id>/desativar/", DesativarEspacoView.as_view(), name="desativar"),
    path("<int:espaco_id>/ativar/", AtivarEspacoView.as_view(), name="ativar"),
]
