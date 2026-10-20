from espacos.application.repositorio import RepositorioEspacos
from espacos.domain.espaco_esportivo import EspacoEsportivo
from espacos.domain.excecoes import EspacoNaoEncontrado, NomeDeEspacoJaCadastrado
from espacos.domain.tipo_espaco import TipoEspaco


class CadastrarEspaco:
    def __init__(self, repositorio: RepositorioEspacos) -> None:
        self._repositorio = repositorio

    def executar(
        self, *, nome: str, tipo: TipoEspaco | str, capacidade: int
    ) -> EspacoEsportivo:
        espaco = EspacoEsportivo(nome=nome, tipo=tipo, capacidade=capacidade)
        if self._repositorio.existe_com_nome(espaco.nome):
            raise NomeDeEspacoJaCadastrado()
        return self._repositorio.salvar(espaco)


class ListarEspacos:
    def __init__(self, repositorio: RepositorioEspacos) -> None:
        self._repositorio = repositorio

    def executar(
        self, *, apenas_ativos: bool = False, tipo: TipoEspaco | None = None
    ) -> list[EspacoEsportivo]:
        return self._repositorio.listar(apenas_ativos=apenas_ativos, tipo=tipo)


class ObterEspaco:
    def __init__(self, repositorio: RepositorioEspacos) -> None:
        self._repositorio = repositorio

    def executar(self, espaco_id: int) -> EspacoEsportivo:
        espaco = self._repositorio.obter_por_id(espaco_id)
        if espaco is None:
            raise EspacoNaoEncontrado(espaco_id)
        return espaco
