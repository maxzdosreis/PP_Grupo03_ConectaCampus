from dataclasses import dataclass

from espacos.application.casos_de_uso import VerificarEspacoDisponivel
from espacos.infrastructure.repositorio_django import RepositorioEspacosDjango


@dataclass(frozen=True)
class EspacoDisponivel:
    id: int
    nome: str


def verificar_espaco_disponivel(espaco_id: int) -> EspacoDisponivel:
    espaco = VerificarEspacoDisponivel(RepositorioEspacosDjango()).executar(espaco_id)
    return EspacoDisponivel(id=espaco.id, nome=espaco.nome)
