from dataclasses import dataclass

from contas.domain.excecoes import (
    NaoPodeDesativarASiMesmo,
    NaoPodeRebaixarASiMesmo,
    PerfilInvalido,
    UltimoGestorAtivo,
)
from contas.domain.perfil import PerfilUsuario


@dataclass(frozen=True)
class SituacaoDoUsuario:
    perfil: PerfilUsuario
    ativo: bool

    @property
    def eh_gestor_ativo(self) -> bool:
        return self.perfil.eh_gestor and self.ativo


def converter_perfil(valor: str) -> PerfilUsuario:
    try:
        return PerfilUsuario(valor)
    except ValueError:
        raise PerfilInvalido() from None


def situacao_pedida(
    atual: SituacaoDoUsuario, *, perfil: PerfilUsuario | None, ativo: bool | None
) -> SituacaoDoUsuario:
    return SituacaoDoUsuario(
        perfil=atual.perfil if perfil is None else perfil,
        ativo=atual.ativo if ativo is None else ativo,
    )


def garantir_alteracao_permitida(
    *,
    ator_id: int,
    alvo_id: int,
    atual: SituacaoDoUsuario,
    nova: SituacaoDoUsuario,
    gestores_ativos: int,
) -> None:
    if atual == nova:
        return
    if ator_id == alvo_id:
        _garantir_que_nao_age_sobre_si(atual, nova)
    if atual.eh_gestor_ativo and not nova.eh_gestor_ativo and gestores_ativos <= 1:
        raise UltimoGestorAtivo()


def _garantir_que_nao_age_sobre_si(
    atual: SituacaoDoUsuario, nova: SituacaoDoUsuario
) -> None:
    if atual.perfil.eh_gestor and not nova.perfil.eh_gestor:
        raise NaoPodeRebaixarASiMesmo()
    if atual.ativo and not nova.ativo:
        raise NaoPodeDesativarASiMesmo()
