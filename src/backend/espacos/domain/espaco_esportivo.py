from compartilhado.domain.erros import CampoObrigatorioAusente
from espacos.domain.excecoes import (
    CapacidadeInvalida,
    EspacoInativo,
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
        self.nome = _normalizar_nome(nome)
        self.tipo = _converter_tipo(tipo)
        self.capacidade = _validar_capacidade(capacidade)
        self.ativo = ativo

    def garantir_que_esta_ativo(self) -> None:
        if not self.ativo:
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
