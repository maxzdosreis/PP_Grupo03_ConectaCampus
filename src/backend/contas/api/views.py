from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from compartilhado.api.respostas import resposta_erro, resposta_sucesso
from contas.api import dependencias
from contas.api.serializers import (
    CadastroSerializer,
    LoginSerializer,
    RenovacaoDeTokenSerializer,
    UsuarioSaidaSerializer,
)


def _cabecalho_bearer(request):
    return JWTAuthentication().authenticate_header(request)


class _SemAutenticacaoView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_authenticate_header(self, request):
        return _cabecalho_bearer(request)


class CadastroView(_SemAutenticacaoView):
    def post(self, request):
        entrada = CadastroSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        usuario = dependencias.cadastrar_solicitante().executar(
            **entrada.validated_data
        )
        return resposta_sucesso(
            "Cadastro realizado com sucesso. Faça login para continuar.",
            UsuarioSaidaSerializer(usuario).data,
            status=status.HTTP_201_CREATED,
        )


class LoginView(_SemAutenticacaoView):
    def post(self, request):
        entrada = LoginSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        usuario = authenticate(
            request,
            email=get_user_model().objects.normalize_email(
                entrada.validated_data["email"]
            ),
            password=entrada.validated_data["senha"],
        )
        if usuario is None:
            return _credenciais_invalidas(request)
        update_last_login(None, usuario)
        refresh = RefreshToken.for_user(usuario)
        return resposta_sucesso(
            "Login realizado com sucesso.",
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "usuario": UsuarioSaidaSerializer(usuario).data,
            },
        )


def _credenciais_invalidas(request):
    resposta = resposta_erro(
        "CREDENCIAIS_INVALIDAS",
        "E-mail ou senha incorretos.",
        status.HTTP_401_UNAUTHORIZED,
    )
    resposta["WWW-Authenticate"] = _cabecalho_bearer(request)
    return resposta


class RenovarTokenView(_SemAutenticacaoView):
    def post(self, request):
        entrada = RenovacaoDeTokenSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        try:
            refresh = RefreshToken(entrada.validated_data["refresh"])
        except TokenError as erro:
            raise InvalidToken(erro.args[0]) from erro
        return resposta_sucesso(
            "Token renovado.", {"access": str(refresh.access_token)}
        )


class UsuarioAtualView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return resposta_sucesso(
            "Usuário autenticado.", UsuarioSaidaSerializer(request.user).data
        )
