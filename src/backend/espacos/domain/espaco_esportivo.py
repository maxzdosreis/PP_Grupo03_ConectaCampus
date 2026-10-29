from compartilhado.domain.erros import CampoObrigatorioAusente
from espacos.domain.excecoes import (
    CapacidadeInvalida,
    EspacoInativo,
    EspacoJaAtivo,
    EspacoJaInativo,
    NenhumaAlteracaoInformada,
    NomeDeEspacoMuitoLongo,
    TipoDeEspacoInvalido,
)
from espacos.domain.tipo_espaco import TipoEspaco

NOME_MAXIMO_CARACTERES = 100
CAPACIDADE_MINIMA = 1


class EspacoEsportivo:
    def __init__(
        self,
        *,
        nome: str,
        tipo: TipoEspaco | str,
        capacidade: int,
        ativo: bool = True,
        id: int | None = None,
    ) -> None:
        self.id = id
        self._nome = _normalizar_nome(nome)
        self._tipo = _converter_tipo(tipo)
        self._capacidade = _validar_capacidade(capacidade)
        self._ativo = ativo

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def tipo(self) -> TipoEspaco:
        return self._tipo

    @property
    def capacidade(self) -> int:
        return self._capacidade

    @property
    def ativo(self) -> bool:
        return self._ativo

    def alterar_dados(
        self,
        *,
        nome: str | None = None,
        tipo: TipoEspaco | str | None = None,
        capacidade: int | None = None,
    ) -> None:
        if nome is None and tipo is None and capacidade is None:
            raise NenhumaAlteracaoInformada()
        novo_nome = self._nome if nome is None else _normalizar_nome(nome)
        novo_tipo = self._tipo if tipo is None else _converter_tipo(tipo)
        nova_capacidade = (
            self._capacidade if capacidade is None else _validar_capacidade(capacidade)
        )
        self._nome, self._tipo, self._capacidade = novo_nome, novo_tipo, nova_capacidade

    def desativar(self) -> None:
        if not self._ativo:
            raise EspacoJaInativo()
        self._ativo = False

    def ativar(self) -> None:
        if self._ativo:
            raise EspacoJaAtivo()
        self._ativo = True

    def garantir_que_esta_ativo(self) -> None:
        if not self._ativo:
            raise EspacoInativo()

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, EspacoEsportivo):
            return NotImplemented
        if self.id is None or outro.id is None:
            return self is outro
        return self.id == outro.id

    def __hash__(self) -> int:
        if self.id is None:
            return object.__hash__(self)
        return hash(self.id)

    def __repr__(self) -> str:
        return (
            f"EspacoEsportivo(id={self.id!r}, nome={self.nome!r}, "
            f"tipo={self.tipo!r}, capacidade={self.capacidade!r}, "
            f"ativo={self.ativo!r})"
        )

    def __str__(self) -> str:
        return f"{self.nome} ({self.tipo.rotulo})"


def _normalizar_nome(nome: str | None) -> str:
    nome_normalizado = " ".join((nome or "").split())
    if not nome_normalizado:
        raise CampoObrigatorioAusente("nome", "Nome")
    if len(nome_normalizado) > NOME_MAXIMO_CARACTERES:
        raise NomeDeEspacoMuitoLongo(NOME_MAXIMO_CARACTERES)
    return nome_normalizado


def _converter_tipo(tipo: TipoEspaco | str | None) -> TipoEspaco:
    if not tipo:
        raise CampoObrigatorioAusente("tipo", "Tipo")
    try:
        return TipoEspaco(tipo)
    except ValueError:
        raise TipoDeEspacoInvalido() from None


def _validar_capacidade(capacidade: int | None) -> int:
    if capacidade is None:
        raise CampoObrigatorioAusente("capacidade", "Capacidade")
    if isinstance(capacidade, bool) or not isinstance(capacidade, int):
        raise CapacidadeInvalida()
    if capacidade < CAPACIDADE_MINIMA:
        raise CapacidadeInvalida()
    return capacidade
