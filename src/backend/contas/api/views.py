from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import (
    ExpiredTokenError,
    InvalidToken,
    TokenError,
)
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken

from compartilhado.api.respostas import resposta_erro, resposta_sucesso
from contas.api import dependencias
from contas.api.limites import (
    LimiteDeCadastroPorIp,
    LimiteDeLoginPorEmail,
    LimiteDeLoginPorIp,
    LimiteDeTrocaDeSenhaPorUsuario,
)
from contas.api.serializers import (
    AlteracaoDeSenhaSerializer,
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
    throttle_classes = [LimiteDeCadastroPorIp]

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
    throttle_classes = [LimiteDeLoginPorIp, LimiteDeLoginPorEmail]

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
        refresh = _trocar_refresh(
            _refresh_de_usuario_ativo(entrada.validated_data["refresh"])
        )
        return resposta_sucesso(
            "Token renovado.",
            {"access": str(refresh.access_token), "refresh": str(refresh)},
        )


def _refresh_de_usuario_ativo(token):
    try:
        refresh = RefreshToken(token)
    except TokenError as erro:
        raise InvalidToken(erro.args[0]) from erro
    usuario = (
        get_user_model()
        .objects.filter(
            **{api_settings.USER_ID_FIELD: refresh.get(api_settings.USER_ID_CLAIM)}
        )
        .first()
    )
    if not api_settings.USER_AUTHENTICATION_RULE(usuario):
        raise InvalidToken("Usuário inativo ou inexistente.")
    return refresh


def _trocar_refresh(refresh):
    with transaction.atomic():
        _revogar_uma_vez(refresh)
        refresh.set_jti()
        refresh.set_iat()
        refresh.outstand()
    return refresh


def _revogar_uma_vez(refresh):
    refresh.outstand()
    registro = OutstandingToken.objects.get(jti=refresh[api_settings.JTI_CLAIM])
    _, revogado_agora = BlacklistedToken.objects.get_or_create(token=registro)
    if not revogado_agora:
        raise InvalidToken("Token de renovação já usado.")


class SairView(_SemAutenticacaoView):
    def post(self, request):
        entrada = RenovacaoDeTokenSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        refresh = _refresh_para_revogar(entrada.validated_data["refresh"])
        if refresh is not None:
            refresh.blacklist()
        return resposta_sucesso("Você saiu da sua conta.")


def _refresh_para_revogar(texto):
    try:
        lido = UntypedToken(texto)
    except ExpiredTokenError:
        return None
    except TokenError as erro:
        raise _refresh_invalido() from erro
    if lido.get(api_settings.TOKEN_TYPE_CLAIM) != RefreshToken.token_type:
        raise _refresh_invalido()
    try:
        return RefreshToken(texto)
    except TokenError:
        return None


def _refresh_invalido(campo="refresh"):
    return serializers.ValidationError(
        {campo: ["Informe um token de renovação válido."]}
    )


class AlterarSenhaView(APIView):
    """Troca a senha de quem está logado: o usuário vem sempre do token."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [LimiteDeTrocaDeSenhaPorUsuario]

    def post(self, request):
        entrada = AlteracaoDeSenhaSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        dados = entrada.validated_data
        jti_atual = _jti_da_sessao_atual(dados.get("refresh_atual"), request.user)
        with transaction.atomic():
            dependencias.alterar_senha().executar(
                usuario_id=request.user.pk,
                senha_atual=dados["senha_atual"],
                nova_senha=dados["nova_senha"],
            )
            _revogar_outras_sessoes(request.user, manter=jti_atual)
        return resposta_sucesso("Senha alterada com sucesso.")


def _jti_da_sessao_atual(texto, usuario):
    if texto is None:
        return None
    try:
        refresh = RefreshToken(texto)
    except TokenError as erro:
        raise _refresh_invalido("refresh_atual") from erro
    if str(refresh.get(api_settings.USER_ID_CLAIM)) != str(usuario.pk):
        raise _refresh_invalido("refresh_atual")
    return refresh[api_settings.JTI_CLAIM]


def _revogar_outras_sessoes(usuario, *, manter):
    registros = OutstandingToken.objects.filter(
        user=usuario, expires_at__gt=timezone.now(), blacklistedtoken__isnull=True
    )
    if manter is not None:
        registros = registros.exclude(jti=manter)
    BlacklistedToken.objects.bulk_create(
        [BlacklistedToken(token=registro) for registro in registros]
    )


class UsuarioAtualView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return resposta_sucesso(
            "Usuário autenticado.", UsuarioSaidaSerializer(request.user).data
        )
