from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from compartilhado.domain.paginacao import Paginacao, PaginaDeItens
from contas.domain.cadastro import DadosDeCadastro
from contas.domain.gestao import SituacaoDoUsuario
from contas.domain.perfil import PerfilUsuario


@dataclass(frozen=True)
class UsuarioCadastrado:
    id: int
    nome: str
    email: str
    matricula: str
    perfil: str


class RepositorioUsuarios(Protocol):
    def existe_email(self, email: str) -> bool:
        """Diz se algum usuário já usa o e-mail, sem diferenciar maiúsculas."""

    def existe_matricula(self, matricula: str) -> bool:
        """Diz se algum usuário já usa a matrícula."""

    def criar_solicitante(
        self, dados: DadosDeCadastro, senha: str
    ) -> UsuarioCadastrado:
        """Cria um usuário com o perfil Solicitante, sem acesso ao admin.

        A senha é gravada só com hash. E-mail ou matrícula repetidos lançam
        EmailJaCadastrado ou MatriculaJaCadastrada, mesmo numa condição de
        corrida que passe pelas consultas acima.
        """

    def dados_de_cadastro(self, usuario_id: int) -> DadosDeCadastro:
        """Devolve nome, matrícula e e-mail do usuário, para a política de senha."""

    def senha_confere(self, usuario_id: int, senha: str) -> bool:
        """Diz se a senha é a atual do usuário (comparação pelo hash)."""

    def trocar_senha(self, usuario_id: int, nova_senha: str) -> None:
        """Grava a nova senha só com hash, numa transação."""


class PoliticaDeSenha(Protocol):
    def validar(self, senha: str, dados: DadosDeCadastro) -> None:
        """Lança SenhaFraca com todos os motivos quando a senha não é aceita."""


@dataclass(frozen=True)
class UsuarioGerenciado:
    """O que a gestão de usuários mostra: nunca senha, hash nem token."""

    id: int
    nome: str
    email: str
    matricula: str
    perfil: PerfilUsuario
    ativo: bool
    cadastrado_em: datetime
    ultimo_acesso: datetime | None

    @property
    def situacao(self) -> SituacaoDoUsuario:
        return SituacaoDoUsuario(perfil=self.perfil, ativo=self.ativo)


@dataclass(frozen=True)
class FiltrosDeUsuarios:
    busca: str | None = None
    perfil: PerfilUsuario | None = None
    ativo: bool | None = None


@dataclass(frozen=True)
class ResultadoDaAlteracao:
    usuario: UsuarioGerenciado
    alterou: bool


class RepositorioGestaoDeUsuarios(Protocol):
    def listar(
        self, filtros: FiltrosDeUsuarios, paginacao: Paginacao
    ) -> PaginaDeItens[UsuarioGerenciado]:
        """Ordenado por nome e, no empate, por id. Só conta e fatia no banco;
        uma página depois da última vem sem itens e com o total certo."""

    def alterar_sob_trava(
        self,
        usuario_id: int,
        decidir: Callable[[UsuarioGerenciado, int], SituacaoDoUsuario],
    ) -> ResultadoDaAlteracao:
        """Numa transação, trava o usuário e todos os Gestores ativos, conta
        esses Gestores e chama `decidir(atual, gestores_ativos)`, que lança a
        recusa ou devolve a situação nova. Só grava se ela for diferente da
        atual. Usuário inexistente lança UsuarioNaoEncontrado."""
