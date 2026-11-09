from django.urls import path

from contas.api.views import (
    CadastroView,
    LoginView,
    RenovarTokenView,
    SairView,
    UsuarioAtualView,
)

app_name = "contas"

urlpatterns = [
    path("cadastro/", CadastroView.as_view(), name="cadastro"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RenovarTokenView.as_view(), name="refresh"),
    path("logout/", SairView.as_view(), name="logout"),
    path("me/", UsuarioAtualView.as_view(), name="me"),
]
