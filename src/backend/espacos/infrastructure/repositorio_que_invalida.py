import logging
from collections.abc import Callable
from contextlib import AbstractContextManager

from django.db import transaction

from espacos.application.portas import CacheDeEspacos, CacheDeEspacosIndisponivel
from espacos.application.repositorio import RepositorioEspacos
from espacos.domain.espaco_esportivo import EspacoEsportivo
from espacos.domain.tipo_espaco import TipoEspaco

logger = logging.getLogger(__name__)

AposOCommit = Callable[[Callable[[], None]], None]


def _apos_o_commit(acao: Callable[[], None]) -> None:
    transaction.on_commit(acao, robust=True)


class RepositorioEspacosQueInvalida(RepositorioEspacos):
    def __init__(
        self,
        interno: RepositorioEspacos,
        cache: CacheDeEspacos,
        apos_o_commit: AposOCommit = _apos_o_commit,
    ) -> None:
        self._interno = interno
        self._cache = cache
        self._apos_o_commit = apos_o_commit

    def salvar(self, espaco: EspacoEsportivo) -> EspacoEsportivo:
        salvo = self._interno.salvar(espaco)
        espaco_id = salvo.id
        self._apos_o_commit(lambda: self._invalidar(espaco_id))
        return salvo

    def _invalidar(self, espaco_id: int) -> None:
        try:
            self._cache.invalidar(espaco_id)
        except CacheDeEspacosIndisponivel:
            logger.warning(
                "Cache do espaço %s não invalidado; a leitura informativa pode "
                "mostrar o dado antigo até o TTL.",
                espaco_id,
            )

    def em_transacao(self) -> AbstractContextManager[None]:
        return self._interno.em_transacao()

    def travar(self, espaco_id: int) -> None:
        self._interno.travar(espaco_id)

    def obter_por_id(self, espaco_id: int) -> EspacoEsportivo | None:
        return self._interno.obter_por_id(espaco_id)

    def listar(
        self, *, apenas_ativos: bool = False, tipo: TipoEspaco | None = None
    ) -> list[EspacoEsportivo]:
        return self._interno.listar(apenas_ativos=apenas_ativos, tipo=tipo)

    def existe_com_nome(self, nome: str, *, ignorar_id: int | None = None) -> bool:
        return self._interno.existe_com_nome(nome, ignorar_id=ignorar_id)
