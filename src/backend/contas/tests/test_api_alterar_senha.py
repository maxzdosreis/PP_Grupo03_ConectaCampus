import logging

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from contas.infrastructure.models import Usuario

pytestmark = pytest.mark.django_db

URL_LOGIN = reverse("contas:login")
URL_REFRESH = reverse("contas:refresh")
URL_SENHA = reverse("contas:senha")
SENHA = "senha-de-teste-123"
NOVA_SENHA = "Rede-Alta-73-nova"
LIMITE_DE_TROCAS = 5


@pytest.fixture(autouse=True)
def _hash_de_senha_rapido(settings):
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


@pytest.fixture
def usuario():
    return Usuario.objects.create_user(
        "ana@x.com", SENHA, nome="Ana Souza", matricula="2026001"
    )


@pytest.fixture
def outro_usuario():
    return Usuario.objects.create_user(
        "bruno@x.com", SENHA, nome="Bruno Lima", matricula="2026002"
    )


def _entrar(usuario, senha=SENHA):
    resposta = APIClient().post(
        URL_LOGIN, {"email": usuario.email, "senha": senha}, format="json"
    )
    return resposta


def _sessao(usuario):
    dados = _entrar(usuario).data["dados"]
    cliente = APIClient()
    cliente.credentials(HTTP_AUTHORIZATION=f"Bearer {dados['access']}")
    return cliente, dados["refresh"]


def _corpo(**alteracoes):
    corpo = {"senha_atual": SENHA, "nova_senha": NOVA_SENHA}
    corpo.update(alteracoes)
    return corpo


def _trocar(cliente, **alteracoes):
    return cliente.post(URL_SENHA, _corpo(**alteracoes), format="json")


def _renovar(refresh):
    return APIClient().post(URL_REFRESH, {"refresh": refresh}, format="json")


def _assert_erro(resposta, status, codigo, campo=None):
    assert resposta.status_code == status
    erro = resposta.data["erro"]
    assert erro["codigo"] == codigo
    if campo:
        assert campo in erro["campos"]


def test_troca_com_sucesso_responde_200_e_a_nova_senha_passa_a_valer(usuario):
    # Arrange
    cliente, _ = _sessao(usuario)

    # Act
    resposta = _trocar(cliente)

    # Assert
    assert resposta.status_code == 200
    assert resposta.data == {"mensagem": "Senha alterada com sucesso.", "dados": None}
    assert _entrar(usuario, SENHA).status_code == 401
    assert _entrar(usuario, NOVA_SENHA).status_code == 200


def test_troca_guarda_so_o_hash_da_senha(usuario):
    # Arrange
    cliente, _ = _sessao(usuario)

    # Act
    _trocar(cliente)

    # Assert
    usuario.refresh_from_db()
    assert usuario.password != NOVA_SENHA
    assert usuario.check_password(NOVA_SENHA)


def test_anonimo_recebe_401_nao_autenticado():
    # Act
    resposta = APIClient().post(URL_SENHA, _corpo(), format="json")

    # Assert
    _assert_erro(resposta, 401, "NAO_AUTENTICADO")


def test_senha_atual_errada_responde_400_com_codigo_proprio_e_nunca_401(usuario):
    # Arrange
    cliente, _ = _sessao(usuario)

    # Act
    resposta = _trocar(cliente, senha_atual="errada-errada-1")

    # Assert
    _assert_erro(resposta, 400, "SENHA_ATUAL_INCORRETA", "senha_atual")
    assert resposta.data["erro"]["mensagem"] == "A senha atual está incorreta."
    assert "WWW-Authenticate" not in resposta
    assert _entrar(usuario, SENHA).status_code == 200


def test_nova_senha_igual_a_atual_responde_400(usuario):
    # Arrange
    cliente, _ = _sessao(usuario)

    # Act
    resposta = _trocar(cliente, nova_senha=SENHA)

    # Assert
    _assert_erro(resposta, 400, "NOVA_SENHA_IGUAL_A_ATUAL", "nova_senha")


@pytest.mark.parametrize(
    ("nova_senha", "trecho"),
    [
        ("curta1A", "muito curta"),
        ("12345678", "inteiramente numérica"),
        ("password", "muito comum"),
        ("ana@x.comA1", "muito parecida"),
    ],
    ids=["curta", "numerica", "comum", "parecida_com_o_email"],
)
def test_nova_senha_que_viola_a_politica_responde_400_senha_fraca(
    usuario, nova_senha, trecho
):
    # Arrange
    cliente, _ = _sessao(usuario)

    # Act
    resposta = _trocar(cliente, nova_senha=nova_senha)

    # Assert
    _assert_erro(resposta, 400, "SENHA_FRACA", "nova_senha")
    assert trecho in resposta.data["erro"]["campos"]["nova_senha"][0]
    assert _entrar(usuario, SENHA).status_code == 200


def test_politica_so_e_revelada_depois_de_provar_a_senha_atual(usuario):
    # Arrange
    cliente, _ = _sessao(usuario)

    # Act
    resposta = _trocar(cliente, senha_atual="errada-errada-1", nova_senha="123")

    # Assert
    _assert_erro(resposta, 400, "SENHA_ATUAL_INCORRETA")


@pytest.mark.parametrize("campo", ["senha_atual", "nova_senha"])
@pytest.mark.parametrize("valor", ["", "   "])
def test_campo_em_branco_responde_400_campo_obrigatorio_ausente(usuario, campo, valor):
    # Arrange
    cliente, _ = _sessao(usuario)

    # Act
    resposta = _trocar(cliente, **{campo: valor})

    # Assert
    _assert_erro(resposta, 400, "CAMPO_OBRIGATORIO_AUSENTE", campo)


@pytest.mark.parametrize("campo", ["senha_atual", "nova_senha"])
def test_campo_ausente_responde_400_dados_invalidos(usuario, campo):
    # Arrange
    cliente, _ = _sessao(usuario)
    corpo = _corpo()
    del corpo[campo]

    # Act
    resposta = cliente.post(URL_SENHA, corpo, format="json")

    # Assert
    _assert_erro(resposta, 400, "DADOS_INVALIDOS", campo)


@pytest.mark.parametrize("valor", [["a"], {"a": 1}, None])
def test_campo_de_tipo_errado_responde_400_dados_invalidos(usuario, valor):
    # Arrange
    cliente, _ = _sessao(usuario)

    # Act
    resposta = _trocar(cliente, nova_senha=valor)

    # Assert
    _assert_erro(resposta, 400, "DADOS_INVALIDOS", "nova_senha")


def test_nova_senha_com_espacos_nas_pontas_vale_do_jeito_que_foi_digitada(usuario):
    # Arrange
    cliente, _ = _sessao(usuario)
    nova = f"  {NOVA_SENHA}  "

    # Act
    resposta = _trocar(cliente, nova_senha=nova)

    # Assert
    assert resposta.status_code == 200
    assert _entrar(usuario, nova).status_code == 200
    assert _entrar(usuario, NOVA_SENHA).status_code == 401


def test_pessoa_so_troca_a_propria_senha_mesmo_enviando_outro_id(
    usuario, outro_usuario
):
    # Arrange
    cliente, _ = _sessao(usuario)

    # Act
    resposta = cliente.post(
        URL_SENHA,
        _corpo(id=outro_usuario.pk, usuario_id=outro_usuario.pk, email="bruno@x.com"),
        format="json",
    )

    # Assert
    assert resposta.status_code == 200
    assert _entrar(outro_usuario, SENHA).status_code == 200
    assert _entrar(usuario, NOVA_SENHA).status_code == 200


def test_senha_atual_de_outra_pessoa_nao_serve_para_trocar_a_propria(
    usuario, outro_usuario
):
    # Arrange
    outro_usuario.set_password("Senha-do-Bruno-99")
    outro_usuario.save()
    cliente, _ = _sessao(usuario)

    # Act
    resposta = _trocar(cliente, senha_atual="Senha-do-Bruno-99")

    # Assert
    _assert_erro(resposta, 400, "SENHA_ATUAL_INCORRETA")


def test_gestor_tambem_troca_a_propria_senha():
    # Arrange
    gestor = Usuario.objects.create_superuser(
        "gestora@x.com", SENHA, nome="Carla Dias", matricula="9000001"
    )
    cliente, _ = _sessao(gestor)

    # Act
    resposta = _trocar(cliente)

    # Assert
    assert resposta.status_code == 200
    assert _entrar(gestor, NOVA_SENHA).status_code == 200


def test_sexta_troca_seguida_responde_429_traduzido_pelo_tratador(usuario):
    # Arrange
    cliente, _ = _sessao(usuario)
    for _ in range(LIMITE_DE_TROCAS):
        assert _trocar(cliente, senha_atual="errada-errada-1").status_code == 400

    # Act
    resposta = _trocar(cliente)

    # Assert
    _assert_erro(resposta, 429, "LIMITE_DE_TENTATIVAS")
    assert resposta["Retry-After"]
    assert _entrar(usuario, SENHA).status_code == 200


def test_limite_de_troca_e_por_usuario_e_nao_por_ip(usuario, outro_usuario):
    # Arrange
    cliente, _ = _sessao(usuario)
    for _ in range(LIMITE_DE_TROCAS):
        _trocar(cliente, senha_atual="errada-errada-1")
    outro_cliente, _ = _sessao(outro_usuario)

    # Act
    resposta = _trocar(outro_cliente)

    # Assert
    assert resposta.status_code == 200


def test_limite_de_troca_vem_das_settings_a_cada_requisicao(usuario, settings):
    # Arrange
    settings.LIMITE_TROCA_DE_SENHA_POR_USUARIO = "1/min"
    cliente, _ = _sessao(usuario)
    _trocar(cliente, senha_atual="errada-errada-1")

    # Act
    resposta = _trocar(cliente, senha_atual="errada-errada-1")

    # Assert
    _assert_erro(resposta, 429, "LIMITE_DE_TENTATIVAS")


def test_troca_revoga_os_refresh_das_outras_sessoes_e_mantem_a_atual(usuario):
    # Arrange
    cliente, refresh_atual = _sessao(usuario)
    _, refresh_de_outro_aparelho = _sessao(usuario)

    # Act
    resposta = _trocar(cliente, refresh_atual=refresh_atual)

    # Assert
    assert resposta.status_code == 200
    assert _renovar(refresh_de_outro_aparelho).status_code == 401
    assert _renovar(refresh_atual).status_code == 200


def test_troca_sem_informar_a_sessao_atual_revoga_todos_os_refresh(usuario):
    # Arrange
    cliente, refresh_atual = _sessao(usuario)
    _, refresh_de_outro_aparelho = _sessao(usuario)

    # Act
    resposta = _trocar(cliente)

    # Assert
    assert resposta.status_code == 200
    assert _renovar(refresh_de_outro_aparelho).status_code == 401
    assert _renovar(refresh_atual).status_code == 401


def test_troca_nao_revoga_os_refresh_de_outra_pessoa(usuario, outro_usuario):
    # Arrange
    cliente, refresh_atual = _sessao(usuario)
    _, refresh_do_outro = _sessao(outro_usuario)

    # Act
    _trocar(cliente, refresh_atual=refresh_atual)

    # Assert
    assert _renovar(refresh_do_outro).status_code == 200


def test_access_ja_emitido_continua_valendo_depois_da_troca(usuario):
    # Arrange
    cliente, _ = _sessao(usuario)
    cliente_de_outro_aparelho, _ = _sessao(usuario)

    # Act
    _trocar(cliente)

    # Assert
    assert cliente_de_outro_aparelho.get(reverse("contas:me")).status_code == 200


def test_refresh_atual_de_outra_pessoa_responde_400_sem_trocar_a_senha(
    usuario, outro_usuario
):
    # Arrange
    cliente, _ = _sessao(usuario)
    _, refresh_do_outro = _sessao(outro_usuario)

    # Act
    resposta = _trocar(cliente, refresh_atual=refresh_do_outro)

    # Assert
    _assert_erro(resposta, 400, "DADOS_INVALIDOS", "refresh_atual")
    assert _entrar(usuario, SENHA).status_code == 200
    assert BlacklistedToken.objects.count() == 0


def test_refresh_atual_invalido_responde_400_sem_trocar_a_senha(usuario):
    # Arrange
    cliente, _ = _sessao(usuario)

    # Act
    resposta = _trocar(cliente, refresh_atual="isto-nao-e-um-token")

    # Assert
    _assert_erro(resposta, 400, "DADOS_INVALIDOS", "refresh_atual")
    assert _entrar(usuario, SENHA).status_code == 200


def test_refresh_atual_com_access_no_lugar_do_refresh_responde_400(usuario):
    # Arrange
    cliente, _ = _sessao(usuario)
    access = str(RefreshToken.for_user(usuario).access_token)

    # Act
    resposta = _trocar(cliente, refresh_atual=access)

    # Assert
    _assert_erro(resposta, 400, "DADOS_INVALIDOS", "refresh_atual")


def test_senhas_nao_aparecem_na_resposta_nem_nos_logs(usuario, caplog):
    # Arrange
    cliente, _ = _sessao(usuario)
    caplog.set_level(logging.DEBUG)
    senhas = [SENHA, NOVA_SENHA, "errada-errada-1", "123"]

    # Act
    respostas = [
        _trocar(cliente, senha_atual="errada-errada-1"),
        _trocar(cliente, nova_senha="123"),
        _trocar(cliente, nova_senha=SENHA),
        _trocar(cliente),
    ]

    # Assert
    for resposta in respostas:
        texto = resposta.content.decode()
        for senha in senhas:
            assert senha not in texto
    for senha in senhas:
        assert senha not in caplog.text
