from espacos.application.casos_de_uso import CadastrarEspaco, ListarEspacos, ObterEspaco
from espacos.infrastructure.repositorio_django import RepositorioEspacosDjango


def cadastrar_espaco() -> CadastrarEspaco:
    return CadastrarEspaco(RepositorioEspacosDjango())


def listar_espacos() -> ListarEspacos:
    return ListarEspacos(RepositorioEspacosDjango())


def obter_espaco() -> ObterEspaco:
    return ObterEspaco(RepositorioEspacosDjango())
