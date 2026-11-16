import pytest

from compartilhado.domain.erros import AcaoNaoPermitida, ConflitoDeEstado
from contas.domain.excecoes import (
    NaoPodeDesativarASiMesmo,
    NaoPodeRebaixarASiMesmo,
    PerfilInvalido,
    UltimoGestorAtivo,
)
from contas.domain.gestao import (
    SituacaoDoUsuario,
    converter_perfil,
    garantir_alteracao_permitida,
    situacao_pedida,
)
from contas.domain.perfil import PerfilUsuario

GESTOR = PerfilUsuario.GESTOR
SOLICITANTE = PerfilUsuario.SOLICITANTE
ATOR = 1
OUTRO = 2

GESTOR_ATIVO = SituacaoDoUsuario(GESTOR, True)
GESTOR_INATIVO = SituacaoDoUsuario(GESTOR, False)
SOLICITANTE_ATIVO = SituacaoDoUsuario(SOLICITANTE, True)
SOLICITANTE_INATIVO = SituacaoDoUsuario(SOLICITANTE, False)


def _garantir(*, alvo, atual, nova, gestores_ativos=2, ator=ATOR):
    garantir_alteracao_permitida(
        ator_id=ator,
        alvo_id=alvo,
        atual=atual,
        nova=nova,
        gestores_ativos=gestores_ativos,
    )


def test_eh_gestor_ativo_exige_perfil_e_situacao():
    # Assert
    assert GESTOR_ATIVO.eh_gestor_ativo
    assert not GESTOR_INATIVO.eh_gestor_ativo
    assert not SOLICITANTE_ATIVO.eh_gestor_ativo


def test_o_proprio_ator_nao_se_rebaixa():
    # Act / Assert
    with pytest.raises(NaoPodeRebaixarASiMesmo) as erro:
        _garantir(alvo=ATOR, atual=GESTOR_ATIVO, nova=SOLICITANTE_ATIVO)
    assert isinstance(erro.value, AcaoNaoPermitida)
    assert erro.value.codigo == "NAO_PODE_REBAIXAR_A_SI_MESMO"


def test_o_proprio_ator_nao_se_desativa():
    # Act / Assert
    with pytest.raises(NaoPodeDesativarASiMesmo) as erro:
        _garantir(alvo=ATOR, atual=GESTOR_ATIVO, nova=GESTOR_INATIVO)
    assert isinstance(erro.value, AcaoNaoPermitida)
    assert erro.value.codigo == "NAO_PODE_DESATIVAR_A_SI_MESMO"


def test_rebaixar_e_desativar_a_si_na_mesma_alteracao_recusa_o_rebaixamento_primeiro():
    # Act / Assert
    with pytest.raises(NaoPodeRebaixarASiMesmo):
        _garantir(alvo=ATOR, atual=GESTOR_ATIVO, nova=SOLICITANTE_INATIVO)


def test_regra_do_proprio_ator_vem_antes_da_do_ultimo_gestor():
    # Act / Assert
    with pytest.raises(NaoPodeRebaixarASiMesmo):
        _garantir(
            alvo=ATOR, atual=GESTOR_ATIVO, nova=SOLICITANTE_ATIVO, gestores_ativos=1
        )


def test_rebaixar_o_ultimo_gestor_ativo_e_recusado_mesmo_sendo_outra_pessoa():
    # Act / Assert
    with pytest.raises(UltimoGestorAtivo) as erro:
        _garantir(
            alvo=OUTRO, atual=GESTOR_ATIVO, nova=SOLICITANTE_ATIVO, gestores_ativos=1
        )
    assert isinstance(erro.value, ConflitoDeEstado)
    assert erro.value.codigo == "ULTIMO_GESTOR_ATIVO"


def test_desativar_o_ultimo_gestor_ativo_e_recusado():
    # Act / Assert
    with pytest.raises(UltimoGestorAtivo):
        _garantir(
            alvo=OUTRO, atual=GESTOR_ATIVO, nova=GESTOR_INATIVO, gestores_ativos=1
        )


def test_rebaixar_e_desativar_o_ultimo_gestor_juntos_e_recusado():
    # Act / Assert
    with pytest.raises(UltimoGestorAtivo):
        _garantir(
            alvo=OUTRO, atual=GESTOR_ATIVO, nova=SOLICITANTE_INATIVO, gestores_ativos=1
        )


@pytest.mark.parametrize("nova", [SOLICITANTE_ATIVO, GESTOR_INATIVO])
def test_rebaixar_ou_desativar_um_gestor_com_outro_ativo_e_permitido(nova):
    # Act / Assert
    _garantir(alvo=OUTRO, atual=GESTOR_ATIVO, nova=nova, gestores_ativos=2)


def test_o_limite_e_exatamente_um_gestor_ativo():
    # Act / Assert
    _garantir(alvo=OUTRO, atual=GESTOR_ATIVO, nova=GESTOR_INATIVO, gestores_ativos=2)
    with pytest.raises(UltimoGestorAtivo):
        _garantir(
            alvo=OUTRO, atual=GESTOR_ATIVO, nova=GESTOR_INATIVO, gestores_ativos=1
        )


def test_rebaixar_gestor_inativo_nao_conta_como_perder_gestor_ativo():
    # Act / Assert
    _garantir(
        alvo=OUTRO, atual=GESTOR_INATIVO, nova=SOLICITANTE_INATIVO, gestores_ativos=1
    )


def test_o_ator_pode_se_promover_ou_se_reativar_sem_efeito_de_regra():
    # Act / Assert
    _garantir(alvo=ATOR, atual=SOLICITANTE_ATIVO, nova=GESTOR_ATIVO, gestores_ativos=0)
    _garantir(alvo=ATOR, atual=GESTOR_INATIVO, nova=GESTOR_ATIVO, gestores_ativos=0)


@pytest.mark.parametrize(
    ("atual", "nova"),
    [
        (SOLICITANTE_ATIVO, GESTOR_ATIVO),
        (SOLICITANTE_INATIVO, SOLICITANTE_ATIVO),
        (GESTOR_INATIVO, GESTOR_ATIVO),
        (SOLICITANTE_INATIVO, GESTOR_ATIVO),
    ],
)
def test_promover_e_reativar_sao_sempre_permitidos(atual, nova):
    # Act / Assert
    _garantir(alvo=OUTRO, atual=atual, nova=nova, gestores_ativos=0)


@pytest.mark.parametrize(
    "situacao", [GESTOR_ATIVO, GESTOR_INATIVO, SOLICITANTE_ATIVO, SOLICITANTE_INATIVO]
)
def test_pedir_o_estado_atual_nao_e_alteracao_e_nunca_e_recusado(situacao):
    # Act / Assert: nem o próprio ator, nem o último Gestor
    _garantir(alvo=ATOR, atual=situacao, nova=situacao, gestores_ativos=1)
    _garantir(alvo=OUTRO, atual=situacao, nova=situacao, gestores_ativos=1)


def test_converter_perfil_aceita_os_valores_do_enum():
    # Act / Assert
    assert converter_perfil("GESTOR") is GESTOR
    assert converter_perfil("SOLICITANTE") is SOLICITANTE


@pytest.mark.parametrize("valor", ["gestor", "ADMIN", "", " GESTOR"])
def test_converter_perfil_recusa_valor_fora_do_enum(valor):
    # Act / Assert
    with pytest.raises(PerfilInvalido) as erro:
        converter_perfil(valor)
    assert erro.value.campo == "perfil"
    assert erro.value.mensagem == "Perfil inválido. Use SOLICITANTE ou GESTOR."


def test_situacao_pedida_mantem_o_que_nao_foi_informado():
    # Act / Assert
    assert situacao_pedida(GESTOR_ATIVO, perfil=None, ativo=None) == GESTOR_ATIVO
    assert (
        situacao_pedida(GESTOR_ATIVO, perfil=SOLICITANTE, ativo=None)
        == SOLICITANTE_ATIVO
    )
    assert situacao_pedida(GESTOR_ATIVO, perfil=None, ativo=False) == GESTOR_INATIVO
    assert (
        situacao_pedida(GESTOR_ATIVO, perfil=SOLICITANTE, ativo=False)
        == SOLICITANTE_INATIVO
    )
