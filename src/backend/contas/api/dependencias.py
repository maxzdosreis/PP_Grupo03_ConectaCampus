from contas.application.casos_de_uso import (
    AlterarSenha,
    AlterarUsuario,
    CadastrarSolicitante,
    ListarUsuarios,
)
from contas.infrastructure.politica_de_senha import PoliticaDeSenhaDjango
from contas.infrastructure.repositorio_django import (
    RepositorioGestaoDeUsuariosDjango,
    RepositorioUsuariosDjango,
)


def cadastrar_solicitante() -> CadastrarSolicitante:
    return CadastrarSolicitante(RepositorioUsuariosDjango(), PoliticaDeSenhaDjango())


def alterar_senha() -> AlterarSenha:
    return AlterarSenha(RepositorioUsuariosDjango(), PoliticaDeSenhaDjango())


def listar_usuarios() -> ListarUsuarios:
    return ListarUsuarios(RepositorioGestaoDeUsuariosDjango())


def alterar_usuario() -> AlterarUsuario:
    return AlterarUsuario(RepositorioGestaoDeUsuariosDjango())
