from espacos.application.casos_de_uso import (
    AtivarEspaco,
    CadastrarEspaco,
    DesativarEspaco,
    EditarEspaco,
    ListarEspacos,
    ObterEspaco,
)
from espacos.application.leitor_de_espacos_em_cache import LeitorDeEspacosComCache
from espacos.application.repositorio import RepositorioEspacos
from espacos.infrastructure.cache_de_espacos_redis import CacheDeEspacosRedis
from espacos.infrastructure.consulta_de_reservas import consulta_registrada
from espacos.infrastructure.repositorio_django import RepositorioEspacosDjango
from espacos.infrastructure.repositorio_que_invalida import (
    RepositorioEspacosQueInvalida,
)


def cadastrar_espaco() -> CadastrarEspaco:
    return CadastrarEspaco(RepositorioEspacosDjango())


def listar_espacos() -> ListarEspacos:
    return ListarEspacos(RepositorioEspacosDjango())


def obter_espaco() -> ObterEspaco:
    return ObterEspaco(
        LeitorDeEspacosComCache(RepositorioEspacosDjango(), CacheDeEspacosRedis())
    )


def editar_espaco() -> EditarEspaco:
    return EditarEspaco(_que_invalida(), consulta_registrada())


def desativar_espaco() -> DesativarEspaco:
    return DesativarEspaco(_que_invalida())


def ativar_espaco() -> AtivarEspaco:
    return AtivarEspaco(_que_invalida())


def _que_invalida() -> RepositorioEspacos:
    return RepositorioEspacosQueInvalida(
        RepositorioEspacosDjango(), CacheDeEspacosRedis()
    )
