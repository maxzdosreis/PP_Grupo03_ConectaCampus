from collections.abc import Iterable
from contextlib import contextmanager

from espacos.application.portas import (
    CacheDeEspacos,
    CacheDeEspacosIndisponivel,
    ReservasDoEspaco,
)
from espacos.application.repositorio import RepositorioEspacos
from espacos.domain.espaco_esportivo import EspacoEsportivo
from espacos.domain.excecoes import (
    EspacoDesatualizado,
    EspacoNaoEncontrado,
    NomeDeEspacoJaCadastrado,
)
from espacos.domain.tipo_espaco import TipoEspaco

ID_INEXISTENTE = 9999


class ReservasDoEspacoFake(ReservasDoEspaco):
    def __init__(
        self, fora_da_janela: int = 0, eventos: list[str] | None = None
    ) -> None:
        self.fora_da_janela = fora_da_janela
        self.consultas: list[tuple[int, int, int]] = []
        self.eventos = eventos if eventos is not None else []

    def contar_ativas_fora_da_janela(
        self, espaco_id: int, abertura_em_minutos: int, fechamento_em_minutos: int
    ) -> int:
        self.eventos.append("contar")
        self.consultas.append((espaco_id, abertura_em_minutos, fechamento_em_minutos))
        return self.fora_da_janela


def novo_espaco(**sobrescritas) -> EspacoEsportivo:
    dados = {"nome": "Quadra Central", "tipo": TipoEspaco.GINASIO, "capacidade": 20}
    dados.update(sobrescritas)
    return EspacoEsportivo(**dados)


def dados_validos(**sobrescritas) -> dict:
    dados = {"nome": "Ginásio A", "tipo": "GINASIO", "capacidade": 50}
    dados.update(sobrescritas)
    return dados


def nomes(espacos: list[EspacoEsportivo]) -> list[str]:
    return [espaco.nome for espaco in espacos]


class RepositorioEspacosEmMemoria(RepositorioEspacos):
    def __init__(self, eventos: list[str] | None = None) -> None:
        self._espacos: dict[int, EspacoEsportivo] = {}
        self._proximo_id = 1
        self.chamadas_de_salvar = 0
        self.leituras = 0
        self.eventos = eventos if eventos is not None else []
        self.ids_travados: list[int] = []
        self.transacoes_abertas = 0

    @contextmanager
    def em_transacao(self):
        self.eventos.append("abrir")
        self.transacoes_abertas += 1
        try:
            yield
        finally:
            self.transacoes_abertas -= 1
            self.eventos.append("fechar")

    def travar(self, espaco_id: int) -> None:
        assert self.transacoes_abertas, "travar fora de uma transação"
        self.eventos.append("travar")
        self.ids_travados.append(espaco_id)

    def salvar(self, espaco: EspacoEsportivo) -> EspacoEsportivo:
        self.chamadas_de_salvar += 1
        self.eventos.append("salvar")
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
        self.leituras += 1
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

    def listar_nomes(self, ids: Iterable[int]) -> dict[int, str]:
        return {
            espaco_id: self._espacos[espaco_id].nome
            for espaco_id in set(ids)
            if espaco_id in self._espacos
        }

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
        horario=espaco.horario,
    )


class CacheDeEspacosEmMemoria(CacheDeEspacos):
    def __init__(self) -> None:
        self._guardados: dict[int, EspacoEsportivo] = {}
        self._versoes: dict[int, int] = {}
        self.indisponivel = False
        self.quebrados: set[int] = set()
        self.invalidacoes: list[int] = []

    def obter(self, espaco_id: int) -> EspacoEsportivo | None:
        self._exigir_disponivel()
        if espaco_id in self.quebrados:
            self.quebrados.discard(espaco_id)
            self._guardados.pop(espaco_id, None)
            return None
        espaco = self._guardados.get(espaco_id)
        return _copiar(espaco, espaco_id) if espaco else None

    def versao(self, espaco_id: int) -> int:
        self._exigir_disponivel()
        return self._versoes.get(espaco_id, 0)

    def guardar(self, espaco: EspacoEsportivo, *, versao: int) -> bool:
        self._exigir_disponivel()
        if self._versoes.get(espaco.id, 0) != versao:
            return False
        self._guardados[espaco.id] = _copiar(espaco, espaco.id)
        return True

    def invalidar(self, espaco_id: int) -> None:
        self._exigir_disponivel()
        self.invalidacoes.append(espaco_id)
        self._guardados.pop(espaco_id, None)
        self._versoes[espaco_id] = self._versoes.get(espaco_id, 0) + 1

    def guardado(self, espaco_id: int) -> bool:
        return espaco_id in self._guardados

    def _exigir_disponivel(self) -> None:
        if self.indisponivel:
            raise CacheDeEspacosIndisponivel
