from collections.abc import Callable

from django.db import IntegrityError, transaction
from django.db.models import Q

from compartilhado.domain.paginacao import Paginacao, PaginaDeItens
from contas.application.portas import (
    FiltrosDeUsuarios,
    RepositorioGestaoDeUsuarios,
    RepositorioUsuarios,
    ResultadoDaAlteracao,
    UsuarioCadastrado,
    UsuarioGerenciado,
)
from contas.domain.cadastro import DadosDeCadastro
from contas.domain.excecoes import (
    EmailJaCadastrado,
    MatriculaJaCadastrada,
    UsuarioNaoEncontrado,
)
from contas.domain.gestao import SituacaoDoUsuario
from contas.domain.perfil import PerfilUsuario
from contas.infrastructure.models import Usuario

_TABELA = Usuario._meta.db_table


_EXCECAO_POR_PREFIXO = {
    f"{_TABELA}_email": EmailJaCadastrado,
    f"{_TABELA}_matricula": MatriculaJaCadastrada,
}


class RepositorioUsuariosDjango(RepositorioUsuarios):
    def existe_email(self, email: str) -> bool:
        return Usuario.objects.filter(email__iexact=email).exists()

    def existe_matricula(self, matricula: str) -> bool:
        return Usuario.objects.filter(matricula=matricula).exists()

    def criar_solicitante(
        self, dados: DadosDeCadastro, senha: str
    ) -> UsuarioCadastrado:
        try:
            with transaction.atomic():
                usuario = Usuario.objects.create_user(
                    dados.email,
                    senha,
                    nome=dados.nome,
                    matricula=dados.matricula,
                    perfil=PerfilUsuario.SOLICITANTE.value,
                )
        except IntegrityError as erro:
            excecao = _excecao_de_unicidade(erro)
            if excecao is None:
                raise
            raise excecao() from erro
        return _para_cadastrado(usuario)

    def dados_de_cadastro(self, usuario_id: int) -> DadosDeCadastro:
        usuario = Usuario.objects.get(pk=usuario_id)
        return DadosDeCadastro(
            nome=usuario.nome, matricula=usuario.matricula, email=usuario.email
        )

    def senha_confere(self, usuario_id: int, senha: str) -> bool:
        return Usuario.objects.get(pk=usuario_id).check_password(senha)

    def trocar_senha(self, usuario_id: int, nova_senha: str) -> None:
        with transaction.atomic():
            usuario = Usuario.objects.select_for_update().get(pk=usuario_id)
            usuario.set_password(nova_senha)
            usuario.save(update_fields=["password"])


class RepositorioGestaoDeUsuariosDjango(RepositorioGestaoDeUsuarios):
    def listar(
        self, filtros: FiltrosDeUsuarios, paginacao: Paginacao
    ) -> PaginaDeItens[UsuarioGerenciado]:
        consulta = _aplicar_filtros(Usuario.objects.order_by("nome", "id"), filtros)
        total = consulta.count()
        deslocamento = paginacao.deslocamento()
        if deslocamento >= total:
            return PaginaDeItens(itens=(), total=total, paginacao=paginacao)
        modelos = consulta[deslocamento : deslocamento + paginacao.tamanho]
        return PaginaDeItens(
            itens=tuple(_para_gerenciado(model) for model in modelos),
            total=total,
            paginacao=paginacao,
        )

    def alterar_sob_trava(
        self,
        usuario_id: int,
        decidir: Callable[[UsuarioGerenciado, int], SituacaoDoUsuario],
    ) -> ResultadoDaAlteracao:
        with transaction.atomic():
            travados = self._travar(usuario_id)
            alvo = next((model for model in travados if model.pk == usuario_id), None)
            if alvo is None:
                raise UsuarioNaoEncontrado()
            gestores_ativos = sum(1 for model in travados if _eh_gestor_ativo(model))
            atual = _para_gerenciado(alvo)
            nova = decidir(atual, gestores_ativos)
            if nova == atual.situacao:
                return ResultadoDaAlteracao(usuario=atual, alterou=False)
            alvo.perfil = nova.perfil.value
            alvo.is_active = nova.ativo
            alvo.save(update_fields=["perfil", "is_active"])
            return ResultadoDaAlteracao(usuario=_para_gerenciado(alvo), alterou=True)

    def _travar(self, usuario_id: int) -> list[Usuario]:
        return list(
            Usuario.objects.select_for_update()
            .filter(
                Q(pk=usuario_id) | Q(perfil=PerfilUsuario.GESTOR.value, is_active=True)
            )
            .order_by("pk")
        )


def _aplicar_filtros(consulta, filtros: FiltrosDeUsuarios):
    if filtros.busca:
        consulta = consulta.filter(
            Q(nome__icontains=filtros.busca)
            | Q(email__icontains=filtros.busca)
            | Q(matricula__icontains=filtros.busca)
        )
    if filtros.perfil is not None:
        consulta = consulta.filter(perfil=filtros.perfil.value)
    if filtros.ativo is not None:
        consulta = consulta.filter(is_active=filtros.ativo)
    return consulta


def _eh_gestor_ativo(model: Usuario) -> bool:
    return model.perfil == PerfilUsuario.GESTOR.value and model.is_active


def _para_gerenciado(model: Usuario) -> UsuarioGerenciado:
    return UsuarioGerenciado(
        id=model.pk,
        nome=model.nome,
        email=model.email,
        matricula=model.matricula,
        perfil=PerfilUsuario(model.perfil),
        ativo=model.is_active,
        cadastrado_em=model.date_joined,
        ultimo_acesso=model.last_login,
    )


def _excecao_de_unicidade(erro: IntegrityError):
    diagnostico = getattr(erro.__cause__, "diag", None)
    constraint = getattr(diagnostico, "constraint_name", None) or ""
    for prefixo, excecao in _EXCECAO_POR_PREFIXO.items():
        if constraint.startswith(prefixo):
            return excecao
    return None


def _para_cadastrado(usuario: Usuario) -> UsuarioCadastrado:
    return UsuarioCadastrado(
        id=usuario.pk,
        nome=usuario.nome,
        email=usuario.email,
        matricula=usuario.matricula,
        perfil=usuario.perfil,
    )
