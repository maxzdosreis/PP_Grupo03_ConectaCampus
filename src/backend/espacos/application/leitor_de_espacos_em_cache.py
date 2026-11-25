import logging

from espacos.application.portas import CacheDeEspacos, CacheDeEspacosIndisponivel
from espacos.application.repositorio import LeitorDeEspacos
from espacos.domain.espaco_esportivo import EspacoEsportivo

logger = logging.getLogger(__name__)


class LeitorDeEspacosComCache(LeitorDeEspacos):
    def __init__(self, repositorio: LeitorDeEspacos, cache: CacheDeEspacos) -> None:
        self._repositorio = repositorio
        self._cache = cache

    def obter_por_id(self, espaco_id: int) -> EspacoEsportivo | None:
        try:
            guardado = self._cache.obter(espaco_id)
            if guardado is not None:
                return guardado
            versao = self._cache.versao(espaco_id)
        except CacheDeEspacosIndisponivel:
            logger.warning("Cache de espaços indisponível; lendo do PostgreSQL.")
            return self._repositorio.obter_por_id(espaco_id)
        espaco = self._repositorio.obter_por_id(espaco_id)
        if espaco is not None:
            self._guardar(espaco, versao)
        return espaco

    def _guardar(self, espaco: EspacoEsportivo, versao: int) -> None:
        try:
            self._cache.guardar(espaco, versao=versao)
        except CacheDeEspacosIndisponivel:
            logger.warning("Espaço %s não guardado no cache.", espaco.id)
