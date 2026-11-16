from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime

from compartilhado.domain.paginacao import Paginacao, PaginaDeItens
from contas.application.portas import (
    FiltrosDeUsuarios,
    PoliticaDeSenha,
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
    SenhaFraca,
    UsuarioNaoEncontrado,
)
from contas.domain.gestao import SituacaoDoUsuario
from contas.domain.perfil import PerfilUsuario


class RepositorioUsuariosEmMemoria(RepositorioUsuarios):
    def __init__(self) -> None:
        self.criados: dict[int, UsuarioCadastrado] = {}
        self.senhas: dict[int, str] = {}
        self._proximo_id = 1

    def existe_email(self, email: str) -> bool:
        return any(
            usuario.email.casefold() == email.casefold()
            for usuario in self.criados.values()
        )

    def existe_matricula(self, matricula: str) -> bool:
        return any(usuario.matricula == matricula for usuario in self.criados.values())

    def criar_solicitante(
        self, dados: DadosDeCadastro, senha: str
    ) -> UsuarioCadastrado:
        if self.existe_email(dados.email):
            raise EmailJaCadastrado()
        if self.existe_matricula(dados.matricula):
            raise MatriculaJaCadastrada()
        usuario = UsuarioCadastrado(
            id=self._gerar_id(),
            nome=dados.nome,
            email=dados.email,
            matricula=dados.matricula,
            perfil=PerfilUsuario.SOLICITANTE.value,
        )
        self.criados[usuario.id] = usuario
        self.senhas[usuario.id] = senha
        return usuario

    def dados_de_cadastro(self, usuario_id: int) -> DadosDeCadastro:
        usuario = self.criados[usuario_id]
        return DadosDeCadastro(
            nome=usuario.nome, matricula=usuario.matricula, email=usuario.email
        )

    def senha_confere(self, usuario_id: int, senha: str) -> bool:
        return self.senhas[usuario_id] == senha

    def trocar_senha(self, usuario_id: int, nova_senha: str) -> None:
        self.senhas[usuario_id] = nova_senha

    def _gerar_id(self) -> int:
        usuario_id = self._proximo_id
        self._proximo_id += 1
        return usuario_id


class PoliticaDeSenhaFake(PoliticaDeSenha):
    MOTIVO = "Senha fraca para o teste."

    def __init__(self, senhas_fracas: tuple[str, ...] = ()) -> None:
        self._senhas_fracas = frozenset(senhas_fracas)

    def validar(self, senha: str, dados: DadosDeCadastro) -> None:
        if senha in self._senhas_fracas:
            raise SenhaFraca([self.MOTIVO])


CADASTRADO_EM = datetime(2026, 11, 1, 9, 0, tzinfo=UTC)


def novo_usuario_gerenciado(
    usuario_id: int,
    *,
    perfil: PerfilUsuario = PerfilUsuario.SOLICITANTE,
    ativo: bool = True,
    nome: str | None = None,
    matricula: str | None = None,
) -> UsuarioGerenciado:
    return UsuarioGerenciado(
        id=usuario_id,
        nome=nome or f"Pessoa {usuario_id:03d}",
        email=f"pessoa{usuario_id}@exemplo.com",
        matricula=matricula or f"M{usuario_id:05d}",
        perfil=perfil,
        ativo=ativo,
        cadastrado_em=CADASTRADO_EM,
        ultimo_acesso=None,
    )


class RepositorioGestaoDeUsuariosEmMemoria(RepositorioGestaoDeUsuarios):
    def __init__(self, usuarios: list[UsuarioGerenciado] | None = None) -> None:
        self.usuarios: dict[int, UsuarioGerenciado] = {
            usuario.id: usuario for usuario in usuarios or []
        }
        self.gestores_contados: list[int] = []
        self.chamadas_de_gravar = 0

    def listar(
        self, filtros: FiltrosDeUsuarios, paginacao: Paginacao
    ) -> PaginaDeItens[UsuarioGerenciado]:
        filtrados = sorted(
            (u for u in self.usuarios.values() if _atende(u, filtros)),
            key=lambda usuario: (usuario.nome, usuario.id),
        )
        inicio = paginacao.deslocamento()
        return PaginaDeItens(
            itens=tuple(filtrados[inicio : inicio + paginacao.tamanho]),
            total=len(filtrados),
            paginacao=paginacao,
        )

    def alterar_sob_trava(
        self,
        usuario_id: int,
        decidir: Callable[[UsuarioGerenciado, int], SituacaoDoUsuario],
    ) -> ResultadoDaAlteracao:
        atual = self.usuarios.get(usuario_id)
        if atual is None:
            raise UsuarioNaoEncontrado()
        gestores_ativos = sum(
            1 for u in self.usuarios.values() if u.situacao.eh_gestor_ativo
        )
        self.gestores_contados.append(gestores_ativos)
        nova = decidir(atual, gestores_ativos)
        if nova == atual.situacao:
            return ResultadoDaAlteracao(usuario=atual, alterou=False)
        alterado = replace(atual, perfil=nova.perfil, ativo=nova.ativo)
        self.usuarios[usuario_id] = alterado
        self.chamadas_de_gravar += 1
        return ResultadoDaAlteracao(usuario=alterado, alterou=True)


def _atende(usuario: UsuarioGerenciado, filtros: FiltrosDeUsuarios) -> bool:
    busca = (filtros.busca or "").casefold()
    campos = f"{usuario.nome}\n{usuario.email}\n{usuario.matricula}".casefold()
    return (
        busca in campos
        and (filtros.perfil is None or usuario.perfil == filtros.perfil)
        and (filtros.ativo is None or usuario.ativo == filtros.ativo)
    )
