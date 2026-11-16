"""Paginação por número e tamanho, igual à da consulta de reservas (RES-10).

Python puro: o repositório de cada contexto faz a contagem e o fatiamento no
banco; aqui ficam só os limites e a aritmética.
"""

from dataclasses import dataclass

TAMANHO_PADRAO_DA_PAGINA = 20
TAMANHO_MAXIMO_DA_PAGINA = 100


@dataclass(frozen=True)
class Paginacao:
    numero: int = 1
    tamanho: int = TAMANHO_PADRAO_DA_PAGINA

    def __post_init__(self) -> None:
        _exigir_inteiro("numero", self.numero)
        _exigir_inteiro("tamanho", self.tamanho)
        if self.numero < 1:
            raise ValueError("O número da página deve ser 1 ou maior.")
        if not 1 <= self.tamanho <= TAMANHO_MAXIMO_DA_PAGINA:
            raise ValueError(
                f"O tamanho da página deve ficar entre 1 e {TAMANHO_MAXIMO_DA_PAGINA}."
            )

    def deslocamento(self) -> int:
        return (self.numero - 1) * self.tamanho


@dataclass(frozen=True)
class PaginaDeItens[Item]:
    itens: tuple[Item, ...]
    total: int
    paginacao: Paginacao

    def total_de_paginas(self) -> int:
        return -(-self.total // self.paginacao.tamanho)


def _exigir_inteiro(nome: str, valor: object) -> None:
    if not isinstance(valor, int) or isinstance(valor, bool):
        raise TypeError(f"{nome} da paginação deve ser int, recebido {valor!r}.")
