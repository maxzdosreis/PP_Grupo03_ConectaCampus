from espacos.application.casos_de_uso import (
    AtivarEspaco,
    CadastrarEspaco,
    DesativarEspaco,
    EditarEspaco,
    ListarEspacos,
    ObterEspaco,
)
from espacos.infrastructure.repositorio_django import RepositorioEspacosDjango


def cadastrar_espaco() -> CadastrarEspaco:
    return CadastrarEspaco(RepositorioEspacosDjango())


def listar_espacos() -> ListarEspacos:
    return ListarEspacos(RepositorioEspacosDjango())


def obter_espaco() -> ObterEspaco:
    return ObterEspaco(RepositorioEspacosDjango())


def editar_espaco() -> EditarEspaco:
    return EditarEspaco(RepositorioEspacosDjango())


def desativar_espaco() -> DesativarEspaco:
    return DesativarEspaco(RepositorioEspacosDjango())


def ativar_espaco() -> AtivarEspaco:
    return AtivarEspaco(RepositorioEspacosDjango())
