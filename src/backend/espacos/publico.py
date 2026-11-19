from dataclasses import dataclass

from espacos.application.casos_de_uso import (
    VerificarEspacoDisponivel,
    VerificarEspacoParaReservar,
)
from espacos.application.portas import ReservasDoEspaco
from espacos.infrastructure import consulta_de_reservas
from espacos.infrastructure.repositorio_django import RepositorioEspacosDjango


@dataclass(frozen=True)
class EspacoDisponivel:
    id: int
    nome: str
    abertura: str
    fechamento: str
    abertura_em_minutos: int
    fechamento_em_minutos: int


def verificar_espaco_disponivel(espaco_id: int) -> EspacoDisponivel:
    espaco = VerificarEspacoDisponivel(RepositorioEspacosDjango()).executar(espaco_id)
    return _como_disponivel(espaco)


def verificar_espaco_disponivel_para_reserva(espaco_id: int) -> EspacoDisponivel:
    espaco = VerificarEspacoParaReservar(RepositorioEspacosDjango()).executar(espaco_id)
    return _como_disponivel(espaco)


def _como_disponivel(espaco) -> EspacoDisponivel:
    horario = espaco.horario
    return EspacoDisponivel(
        id=espaco.id,
        nome=espaco.nome,
        abertura=f"{horario.abertura():%H:%M}",
        fechamento=f"{horario.fechamento():%H:%M}",
        abertura_em_minutos=horario.abertura_em_minutos,
        fechamento_em_minutos=horario.fechamento_em_minutos,
    )


def registrar_reservas_do_espaco(reservas: ReservasDoEspaco) -> None:
    consulta_de_reservas.registrar(reservas)
