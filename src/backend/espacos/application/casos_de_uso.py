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
        return _obter_ou_falhar(self._repositorio, espaco_id)


class VerificarEspacoDisponivel:
    def __init__(self, repositorio: RepositorioEspacos) -> None:
        self._repositorio = repositorio

    def executar(self, espaco_id: int) -> EspacoEsportivo:
        espaco = _obter_ou_falhar(self._repositorio, espaco_id)
        espaco.garantir_que_esta_ativo()
        return espaco


class EditarEspaco:
    def __init__(self, repositorio: RepositorioEspacos) -> None:
        self._repositorio = repositorio

    def executar(
        self,
        espaco_id: int,
        *,
        nome: str | None = None,
        tipo: TipoEspaco | str | None = None,
        capacidade: int | None = None,
    ) -> EspacoEsportivo:
        espaco = _obter_ou_falhar(self._repositorio, espaco_id)
        nome_anterior = espaco.nome
        espaco.alterar_dados(nome=nome, tipo=tipo, capacidade=capacidade)
        if espaco.nome != nome_anterior and self._repositorio.existe_com_nome(
            espaco.nome, ignorar_id=espaco_id
        ):
            raise NomeDeEspacoJaCadastrado()
        return self._repositorio.salvar(espaco)


class DesativarEspaco:
    def __init__(self, repositorio: RepositorioEspacos) -> None:
        self._repositorio = repositorio

    def executar(self, espaco_id: int) -> EspacoEsportivo:
        espaco = _obter_ou_falhar(self._repositorio, espaco_id)
        espaco.desativar()
        return self._repositorio.salvar(espaco)


class AtivarEspaco:
    def __init__(self, repositorio: RepositorioEspacos) -> None:
        self._repositorio = repositorio

    def executar(self, espaco_id: int) -> EspacoEsportivo:
        espaco = _obter_ou_falhar(self._repositorio, espaco_id)
        espaco.ativar()
        return self._repositorio.salvar(espaco)


def _obter_ou_falhar(
    repositorio: RepositorioEspacos, espaco_id: int
) -> EspacoEsportivo:
    espaco = repositorio.obter_por_id(espaco_id)
    if espaco is None:
        raise EspacoNaoEncontrado(espaco_id)
    return espaco
