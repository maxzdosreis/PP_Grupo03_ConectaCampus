import json

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from conftest import SENHA_DE_TESTE

pytestmark = pytest.mark.django_db

Usuario = get_user_model()


@pytest.fixture(autouse=True)
def _hash_de_senha_rapido(settings):
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


@pytest.fixture
def outra_gestora(db):
    return Usuario.objects.create_superuser(
        "outra.gestora@exemplo.com",
        SENHA_DE_TESTE,
        nome="Dora Gestora",
        matricula="G0002",
    )


def _lista(cliente, **consulta):
    return cliente.get(reverse("usuarios:lista"), consulta)


def _alterar(cliente, usuario, corpo):
    return cliente.patch(
        reverse("usuarios:detalhe", args=[usuario.pk]), corpo, format="json"
    )


def _login(email, senha=SENHA_DE_TESTE):
    return APIClient().post(
        reverse("contas:login"), {"email": email, "senha": senha}, format="json"
    )


def _codigo(resposta):
    return resposta.data["erro"]["codigo"]


def _criar_varios(quantidade):
    for numero in range(quantidade):
        Usuario.objects.create_user(
            f"lote{numero:02d}@exemplo.com",
            SENHA_DE_TESTE,
            nome=f"Lote {numero:02d}",
            matricula=f"L{numero:04d}",
        )


def test_gestor_lista_os_usuarios_no_formato_padrao(
    cliente_com_token, usuario_gestor, usuario_solicitante
):
    # Act
    resposta = _lista(cliente_com_token(usuario_gestor))

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == "2 usuários encontrados."
    assert resposta.data["paginacao"] == {
        "pagina": 1,
        "tamanho": 20,
        "total": 2,
        "total_de_paginas": 1,
    }
    ana = next(u for u in resposta.data["dados"] if u["id"] == usuario_solicitante.pk)
    assert set(ana) == {
        "id",
        "nome",
        "email",
        "matricula",
        "perfil",
        "perfil_rotulo",
        "eh_gestor",
        "ativo",
        "cadastrado_em",
        "ultimo_acesso",
    }
    assert ana["perfil"] == "SOLICITANTE"
    assert ana["perfil_rotulo"] == "Solicitante"
    assert ana["eh_gestor"] is False
    assert ana["ativo"] is True
    assert ana["ultimo_acesso"] is None


def test_mensagem_de_contagem_para_um_e_para_nenhum(cliente_gestor):
    # Act
    um = _lista(cliente_gestor)
    nenhum = _lista(cliente_gestor, busca="nao-existe")

    # Assert
    assert um.data["mensagem"] == "1 usuário encontrado."
    assert nenhum.data["mensagem"] == "Nenhum usuário encontrado."
    assert nenhum.data["dados"] == []
    assert nenhum.data["paginacao"]["total_de_paginas"] == 0


def test_resposta_nunca_traz_hash_de_senha_nem_token(
    cliente_com_token, usuario_gestor, usuario_solicitante
):
    # Arrange
    cliente = cliente_com_token(usuario_gestor)
    _login(usuario_solicitante.email)

    # Act
    listagem = _lista(cliente)
    alteracao = _alterar(cliente, usuario_solicitante, {"ativo": False})

    # Assert
    for resposta in (listagem, alteracao):
        texto = json.dumps(resposta.data).lower()
        for proibido in ("password", "senha", "hash", "pbkdf2", "md5$", "token"):
            assert proibido not in texto
        assert usuario_solicitante.password.lower() not in texto


def test_listagem_pagina_e_depois_da_ultima_devolve_vazio_com_200(
    cliente_gestor, usuario_gestor
):
    # Arrange
    _criar_varios(24)

    # Act
    primeira = _lista(cliente_gestor)
    segunda = _lista(cliente_gestor, pagina=2)
    alem = _lista(cliente_gestor, pagina=9)

    # Assert
    assert len(primeira.data["dados"]) == 20
    assert len(segunda.data["dados"]) == 5
    assert primeira.data["paginacao"]["total"] == 25
    assert primeira.data["paginacao"]["total_de_paginas"] == 2
    assert alem.status_code == 200
    assert alem.data["dados"] == []
    assert alem.data["paginacao"]["pagina"] == 9
    assert alem.data["paginacao"]["total"] == 25


def test_listagem_respeita_o_tamanho_pedido(cliente_gestor):
    # Arrange
    _criar_varios(5)

    # Act
    resposta = _lista(cliente_gestor, tamanho=2, pagina=3)

    # Assert
    assert len(resposta.data["dados"]) == 2
    assert resposta.data["paginacao"]["tamanho"] == 2
    assert resposta.data["paginacao"]["total_de_paginas"] == 3


@pytest.mark.parametrize(
    "consulta",
    [
        {"pagina": 0},
        {"pagina": "abc"},
        {"tamanho": 0},
        {"tamanho": 101},
        {"perfil": "ADMIN"},
        {"ativo": "talvez"},
    ],
)
def test_parametros_invalidos_respondem_400_com_o_campo(cliente_gestor, consulta):
    # Act
    resposta = _lista(cliente_gestor, **consulta)

    # Assert
    assert resposta.status_code == 400
    assert _codigo(resposta) == "DADOS_INVALIDOS"
    assert list(consulta)[0] in resposta.data["erro"]["campos"]


def test_parametros_em_branco_valem_o_padrao(cliente_gestor):
    # Act
    resposta = _lista(cliente_gestor, pagina="", tamanho="", busca="", ativo="")

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["paginacao"]["tamanho"] == 20


def test_ordem_e_estavel_por_nome_e_depois_por_id(cliente_gestor):
    # Arrange
    for numero in range(3):
        Usuario.objects.create_user(
            f"igual{numero}@exemplo.com",
            SENHA_DE_TESTE,
            nome="Nome Igual",
            matricula=f"I{numero}",
        )

    # Act
    primeira = _lista(cliente_gestor, busca="Nome Igual")
    segunda = _lista(cliente_gestor, busca="Nome Igual")

    # Assert
    ids = [u["id"] for u in primeira.data["dados"]]
    assert ids == sorted(ids)
    assert ids == [u["id"] for u in segunda.data["dados"]]


def test_busca_por_nome_email_e_matricula(
    cliente_gestor, usuario_solicitante, outro_solicitante
):
    # Act / Assert
    por_nome = _lista(cliente_gestor, busca="souza")
    por_email = _lista(cliente_gestor, busca="BRUNO@")
    por_matricula = _lista(cliente_gestor, busca="2026002")
    assert [u["email"] for u in por_nome.data["dados"]] == [usuario_solicitante.email]
    assert [u["email"] for u in por_email.data["dados"]] == [outro_solicitante.email]
    assert [u["email"] for u in por_matricula.data["dados"]] == [
        outro_solicitante.email
    ]


def test_filtros_por_perfil_e_por_ativo(
    cliente_gestor, usuario_gestor, usuario_solicitante, outro_solicitante
):
    # Arrange
    Usuario.objects.filter(pk=outro_solicitante.pk).update(is_active=False)

    # Act
    gestores = _lista(cliente_gestor, perfil="GESTOR")
    inativos = _lista(cliente_gestor, ativo="false")
    ativos = _lista(cliente_gestor, ativo="true", perfil="SOLICITANTE")

    # Assert
    assert [u["id"] for u in gestores.data["dados"]] == [usuario_gestor.pk]
    assert [u["id"] for u in inativos.data["dados"]] == [outro_solicitante.pk]
    assert [u["id"] for u in ativos.data["dados"]] == [usuario_solicitante.pk]


def test_solicitante_nao_lista_usuarios(cliente_com_token, usuario_solicitante):
    # Act
    resposta = _lista(cliente_com_token(usuario_solicitante))

    # Assert
    assert resposta.status_code == 403
    assert _codigo(resposta) == "ACAO_NAO_PERMITIDA"


def test_anonimo_nao_lista_usuarios():
    # Act
    resposta = APIClient().get(reverse("usuarios:lista"))

    # Assert
    assert resposta.status_code == 401
    assert _codigo(resposta) == "NAO_AUTENTICADO"


def test_gestor_promove_um_solicitante(
    cliente_com_token, usuario_gestor, usuario_solicitante
):
    # Act
    resposta = _alterar(
        cliente_com_token(usuario_gestor), usuario_solicitante, {"perfil": "GESTOR"}
    )

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == "Usuário atualizado."
    assert resposta.data["dados"]["perfil"] == "GESTOR"
    assert resposta.data["dados"]["eh_gestor"] is True
    usuario_solicitante.refresh_from_db()
    assert usuario_solicitante.eh_gestor


def test_gestor_rebaixa_outro_gestor_havendo_dois_ativos(cliente_gestor, outra_gestora):
    # Act
    resposta = _alterar(cliente_gestor, outra_gestora, {"perfil": "SOLICITANTE"})

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["dados"]["perfil"] == "SOLICITANTE"


def test_gestor_desativa_e_reativa_um_solicitante(cliente_gestor, usuario_solicitante):
    # Act
    desativado = _alterar(cliente_gestor, usuario_solicitante, {"ativo": False})
    reativado = _alterar(cliente_gestor, usuario_solicitante, {"ativo": True})

    # Assert
    assert desativado.data["dados"]["ativo"] is False
    assert reativado.data["dados"]["ativo"] is True
    usuario_solicitante.refresh_from_db()
    assert usuario_solicitante.is_active


def test_perfil_e_ativo_podem_vir_juntos(cliente_gestor, usuario_solicitante):
    # Act
    resposta = _alterar(
        cliente_gestor, usuario_solicitante, {"perfil": "GESTOR", "ativo": False}
    )

    # Assert
    assert (resposta.data["dados"]["perfil"], resposta.data["dados"]["ativo"]) == (
        "GESTOR",
        False,
    )


def test_pedir_o_estado_atual_responde_200_sem_mudar_nada(
    cliente_gestor, usuario_solicitante
):
    # Act
    resposta = _alterar(
        cliente_gestor, usuario_solicitante, {"perfil": "SOLICITANTE", "ativo": True}
    )

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == "Nenhuma mudança: o usuário já estava assim."
    assert resposta.data["dados"]["perfil"] == "SOLICITANTE"


def test_corpo_vazio_responde_400(cliente_gestor, usuario_solicitante):
    # Act
    resposta = _alterar(cliente_gestor, usuario_solicitante, {})

    # Assert
    assert resposta.status_code == 400
    assert _codigo(resposta) == "NENHUMA_ALTERACAO_INFORMADA"


def test_perfil_invalido_responde_400_no_campo(cliente_gestor, usuario_solicitante):
    # Act
    resposta = _alterar(cliente_gestor, usuario_solicitante, {"perfil": "ADMIN"})

    # Assert
    assert resposta.status_code == 400
    assert _codigo(resposta) == "PERFIL_INVALIDO"
    assert "perfil" in resposta.data["erro"]["campos"]


def test_ativo_que_nao_e_booleano_responde_400(cliente_gestor, usuario_solicitante):
    # Act
    resposta = _alterar(cliente_gestor, usuario_solicitante, {"ativo": "quem sabe"})

    # Assert
    assert resposta.status_code == 400
    assert _codigo(resposta) == "DADOS_INVALIDOS"


def test_campos_extras_do_corpo_sao_ignorados(cliente_gestor, usuario_solicitante):
    # Act
    resposta = _alterar(
        cliente_gestor,
        usuario_solicitante,
        {"ativo": False, "is_superuser": True, "is_staff": True, "email": "x@x.com"},
    )

    # Assert
    assert resposta.status_code == 200
    usuario_solicitante.refresh_from_db()
    assert not usuario_solicitante.is_superuser
    assert not usuario_solicitante.is_staff
    assert usuario_solicitante.email == "ana@exemplo.com"


def test_usuario_inexistente_responde_404(cliente_gestor):
    # Act
    resposta = cliente_gestor.patch(
        reverse("usuarios:detalhe", args=[999_999]), {"ativo": False}, format="json"
    )

    # Assert
    assert resposta.status_code == 404
    assert _codigo(resposta) == "USUARIO_NAO_ENCONTRADO"


def test_gestor_nao_rebaixa_a_si_mesmo(
    cliente_com_token, usuario_gestor, outra_gestora
):
    # Act
    resposta = _alterar(
        cliente_com_token(usuario_gestor), usuario_gestor, {"perfil": "SOLICITANTE"}
    )

    # Assert
    assert resposta.status_code == 403
    assert _codigo(resposta) == "NAO_PODE_REBAIXAR_A_SI_MESMO"
    usuario_gestor.refresh_from_db()
    assert usuario_gestor.eh_gestor


def test_gestor_nao_desativa_a_si_mesmo(
    cliente_com_token, usuario_gestor, outra_gestora
):
    # Act
    resposta = _alterar(
        cliente_com_token(usuario_gestor), usuario_gestor, {"ativo": False}
    )

    # Assert
    assert resposta.status_code == 403
    assert _codigo(resposta) == "NAO_PODE_DESATIVAR_A_SI_MESMO"
    usuario_gestor.refresh_from_db()
    assert usuario_gestor.is_active


def test_unico_gestor_nao_se_rebaixa_nem_se_desativa(cliente_gestor, usuario_gestor):
    # Act
    rebaixar = _alterar(cliente_gestor, usuario_gestor, {"perfil": "SOLICITANTE"})
    desativar = _alterar(cliente_gestor, usuario_gestor, {"ativo": False})

    # Assert
    assert rebaixar.status_code == desativar.status_code == 403
    usuario_gestor.refresh_from_db()
    assert usuario_gestor.eh_gestor
    assert usuario_gestor.is_active


def test_pedir_o_proprio_estado_nao_e_recusado(cliente_gestor, usuario_gestor):
    # Act
    resposta = _alterar(
        cliente_gestor, usuario_gestor, {"perfil": "GESTOR", "ativo": True}
    )

    # Assert
    assert resposta.status_code == 200


@pytest.mark.parametrize("corpo", [{"perfil": "SOLICITANTE"}, {"ativo": False}])
def test_ultimo_gestor_ativo_nao_e_rebaixado_nem_desativado_por_quem_ja_perdeu_o_perfil(
    cliente_gestor, usuario_gestor, outra_gestora, corpo
):
    # Arrange
    Usuario.objects.filter(pk=usuario_gestor.pk).update(perfil="SOLICITANTE")

    # Act
    resposta = _alterar(cliente_gestor, outra_gestora, corpo)

    # Assert
    assert resposta.status_code == 409
    assert _codigo(resposta) == "ULTIMO_GESTOR_ATIVO"
    outra_gestora.refresh_from_db()
    assert outra_gestora.eh_gestor
    assert outra_gestora.is_active


def test_solicitante_nao_altera_usuarios(
    cliente_com_token, usuario_solicitante, outro_solicitante
):
    # Act
    resposta = _alterar(
        cliente_com_token(usuario_solicitante), outro_solicitante, {"ativo": False}
    )

    # Assert
    assert resposta.status_code == 403
    assert _codigo(resposta) == "ACAO_NAO_PERMITIDA"
    outro_solicitante.refresh_from_db()
    assert outro_solicitante.is_active


def test_solicitante_nao_se_promove(cliente_com_token, usuario_solicitante):
    # Act
    resposta = _alterar(
        cliente_com_token(usuario_solicitante),
        usuario_solicitante,
        {"perfil": "GESTOR"},
    )

    # Assert
    assert resposta.status_code == 403
    usuario_solicitante.refresh_from_db()
    assert not usuario_solicitante.eh_gestor


def test_anonimo_nao_altera_usuarios(usuario_solicitante):
    # Act
    resposta = _alterar(APIClient(), usuario_solicitante, {"ativo": False})

    # Assert
    assert resposta.status_code == 401
    assert _codigo(resposta) == "NAO_AUTENTICADO"


@pytest.mark.parametrize("metodo", ["get", "put", "delete", "post"])
def test_outros_metodos_do_detalhe_respondem_405(
    cliente_gestor, usuario_solicitante, metodo
):
    # Act
    resposta = getattr(cliente_gestor, metodo)(
        reverse("usuarios:detalhe", args=[usuario_solicitante.pk])
    )

    # Assert
    assert resposta.status_code == 405
    assert _codigo(resposta) == "METODO_NAO_PERMITIDO"


@pytest.mark.parametrize("metodo", ["post", "put", "patch", "delete"])
def test_outros_metodos_da_lista_respondem_405(cliente_gestor, metodo):
    # Act
    resposta = getattr(cliente_gestor, metodo)(reverse("usuarios:lista"))

    # Assert
    assert resposta.status_code == 405


def test_alteracoes_tem_limite_de_tentativas_por_usuario(
    cliente_com_token, usuario_gestor, usuario_solicitante, settings
):
    # Arrange
    settings.LIMITE_GESTAO_DE_USUARIOS_POR_USUARIO = "2/min"
    cliente = cliente_com_token(usuario_gestor)
    for _ in range(2):
        assert (
            _alterar(cliente, usuario_solicitante, {"ativo": True}).status_code == 200
        )

    # Act
    resposta = _alterar(cliente, usuario_solicitante, {"ativo": True})

    # Assert
    assert resposta.status_code == 429
    assert _codigo(resposta) == "LIMITE_DE_TENTATIVAS"
    assert resposta["Retry-After"]
    assert _lista(cliente).status_code == 200


def test_desativado_nao_entra_e_recebe_a_mesma_resposta_de_credenciais_invalidas(
    cliente_gestor, usuario_solicitante
):
    # Arrange
    erradas = _login(usuario_solicitante.email, "senha-errada-123")
    _alterar(cliente_gestor, usuario_solicitante, {"ativo": False})

    # Act
    resposta = _login(usuario_solicitante.email)

    # Assert
    assert resposta.status_code == 401
    assert _codigo(resposta) == "CREDENCIAIS_INVALIDAS"
    assert resposta.data == erradas.data


def test_access_de_quem_foi_desativado_deixa_de_funcionar(
    cliente_gestor, tokens_de, usuario_solicitante
):
    # Arrange
    cliente = APIClient()
    cliente.credentials(
        HTTP_AUTHORIZATION=f"Bearer {tokens_de(usuario_solicitante)['access']}"
    )
    assert cliente.get(reverse("contas:me")).status_code == 200
    _alterar(cliente_gestor, usuario_solicitante, {"ativo": False})

    # Act
    resposta = cliente.get(reverse("contas:me"))

    # Assert
    assert resposta.status_code == 401
    assert _codigo(resposta) == "NAO_AUTENTICADO"


def test_refresh_de_quem_foi_desativado_nao_renova_e_nao_rotaciona(
    cliente_gestor, tokens_de, usuario_solicitante
):
    # Arrange
    refresh = tokens_de(usuario_solicitante)["refresh"]
    _alterar(cliente_gestor, usuario_solicitante, {"ativo": False})
    registros_antes = _quantidade_de_tokens()

    # Act
    resposta = APIClient().post(
        reverse("contas:refresh"), {"refresh": refresh}, format="json"
    )

    # Assert
    assert resposta.status_code == 401
    assert _codigo(resposta) == "NAO_AUTENTICADO"
    assert _quantidade_de_tokens() == registros_antes


def _quantidade_de_tokens():
    from rest_framework_simplejwt.token_blacklist.models import (
        BlacklistedToken,
        OutstandingToken,
    )

    return OutstandingToken.objects.count(), BlacklistedToken.objects.count()


def test_reativado_volta_a_entrar_sem_restaurar_nada(
    cliente_gestor, tokens_de, usuario_solicitante
):
    # Arrange
    antigo = tokens_de(usuario_solicitante)
    _alterar(cliente_gestor, usuario_solicitante, {"ativo": False})
    _alterar(cliente_gestor, usuario_solicitante, {"ativo": True})

    # Act
    entrada = _login(usuario_solicitante.email)

    # Assert: volta a entrar; a sessão antiga continua sendo só o que era
    assert entrada.status_code == 200
    assert entrada.data["dados"]["usuario"]["email"] == usuario_solicitante.email
    cliente = APIClient()
    cliente.credentials(HTTP_AUTHORIZATION=f"Bearer {antigo['access']}")
    assert cliente.get(reverse("contas:me")).status_code == 200


def test_gestor_rebaixado_perde_os_poderes_na_proxima_requisicao_com_o_mesmo_token(
    cliente_com_token, usuario_gestor, outra_gestora
):
    # Arrange
    cliente_da_outra = cliente_com_token(outra_gestora)
    assert _lista(cliente_da_outra).status_code == 200
    cliente_da_primeira = cliente_com_token(usuario_gestor)

    # Act
    rebaixamento = _alterar(
        cliente_da_primeira, outra_gestora, {"perfil": "SOLICITANTE"}
    )
    resposta = _lista(cliente_da_outra)

    # Assert
    assert rebaixamento.status_code == 200
    assert resposta.status_code == 403
    assert _codigo(resposta) == "ACAO_NAO_PERMITIDA"


def test_promovido_ganha_os_poderes_na_proxima_requisicao_com_o_mesmo_token(
    cliente_com_token, usuario_gestor, usuario_solicitante
):
    # Arrange
    cliente_da_ana = cliente_com_token(usuario_solicitante)
    assert _lista(cliente_da_ana).status_code == 403

    # Act
    _alterar(
        cliente_com_token(usuario_gestor), usuario_solicitante, {"perfil": "GESTOR"}
    )

    # Assert
    assert _lista(cliente_da_ana).status_code == 200


def test_desativar_nao_mexe_nas_reservas_da_pessoa(
    cliente_com_token, usuario_gestor, usuario_solicitante, espaco_id
):
    # Arrange
    from datetime import timedelta

    from django.utils import timezone

    amanha = (timezone.localdate() + timedelta(days=1)).isoformat()
    cliente_da_ana = cliente_com_token(usuario_solicitante)
    criada = cliente_da_ana.post(
        reverse("reservas:lista"),
        {
            "espaco_id": espaco_id,
            "data": amanha,
            "hora_inicio": "10:00",
            "hora_fim": "11:00",
            "finalidade": "Treino",
        },
        format="json",
    )
    assert criada.status_code == 201
    gestor = cliente_com_token(usuario_gestor)

    # Act
    _alterar(gestor, usuario_solicitante, {"ativo": False})
    reserva = gestor.get(reverse("reservas:detalhe", args=[criada.data["dados"]["id"]]))

    # Assert
    assert reserva.status_code == 200
    assert reserva.data["dados"]["situacao"] == "SOLICITADA"
    assert [a["situacao"] for a in reserva.data["dados"]["acoes_disponiveis"]] == [
        "CONFIRMADA",
        "RECUSADA",
        "CANCELADA",
    ]
