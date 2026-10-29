from espacos.application.repositorio import RepositorioEspacos
from espacos.domain.espaco_esportivo import EspacoEsportivo
from espacos.domain.excecoes import (
    EspacoDesatualizado,
    EspacoNaoEncontrado,
    NomeDeEspacoJaCadastrado,
)
from espacos.domain.tipo_espaco import TipoEspaco


class RepositorioEspacosEmMemoria(RepositorioEspacos):
    def __init__(self) -> None:
        self._espacos: dict[int, EspacoEsportivo] = {}
        self._proximo_id = 1

    def salvar(self, espaco: EspacoEsportivo) -> EspacoEsportivo:
        if espaco.id is not None and espaco.id not in self._espacos:
            raise EspacoNaoEncontrado(espaco.id)
        if (
            espaco.id is not None
            and self._espacos[espaco.id].estado != espaco.estado_de_origem
        ):
            raise EspacoDesatualizado()
        if self.existe_com_nome(espaco.nome, ignorar_id=espaco.id):
            raise NomeDeEspacoJaCadastrado()
        espaco_id = espaco.id if espaco.id is not None else self._gerar_id()
        self._espacos[espaco_id] = _copiar(espaco, espaco_id)
        espaco.marcar_como_gravado()
        return _copiar(espaco, espaco_id)

    def obter_por_id(self, espaco_id: int) -> EspacoEsportivo | None:
        espaco = self._espacos.get(espaco_id)
        return _copiar(espaco, espaco_id) if espaco else None

    def listar(
        self, *, apenas_ativos: bool = False, tipo: TipoEspaco | None = None
    ) -> list[EspacoEsportivo]:
        encontrados = [
            espaco
            for espaco in self._espacos.values()
            if (espaco.ativo or not apenas_ativos) and tipo in (None, espaco.tipo)
        ]
        encontrados.sort(key=lambda espaco: espaco.nome)
        return [_copiar(espaco, espaco.id) for espaco in encontrados]

    def existe_com_nome(self, nome: str, *, ignorar_id: int | None = None) -> bool:
        return any(
            espaco.nome.casefold() == nome.casefold()
            for espaco_id, espaco in self._espacos.items()
            if espaco_id != ignorar_id
        )

    def _gerar_id(self) -> int:
        espaco_id = self._proximo_id
        self._proximo_id += 1
        return espaco_id


def _copiar(espaco: EspacoEsportivo, espaco_id: int | None) -> EspacoEsportivo:
    return EspacoEsportivo(
        id=espaco_id,
        nome=espaco.nome,
        tipo=espaco.tipo,
        capacidade=espaco.capacidade,
        ativo=espaco.ativo,
    )
