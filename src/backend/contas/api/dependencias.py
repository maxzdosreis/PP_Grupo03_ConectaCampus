from contas.application.casos_de_uso import CadastrarSolicitante
from contas.infrastructure.politica_de_senha import PoliticaDeSenhaDjango
from contas.infrastructure.repositorio_django import RepositorioUsuariosDjango


def cadastrar_solicitante() -> CadastrarSolicitante:
    return CadastrarSolicitante(RepositorioUsuariosDjango(), PoliticaDeSenhaDjango())
