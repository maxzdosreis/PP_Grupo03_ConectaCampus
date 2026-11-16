from django.urls import path

from contas.api.views import UsuarioDetalheView, UsuariosView

app_name = "usuarios"

urlpatterns = [
    path("", UsuariosView.as_view(), name="lista"),
    path("<int:usuario_id>/", UsuarioDetalheView.as_view(), name="detalhe"),
]
