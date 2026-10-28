from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.solicitante import Solicitante


def solicitante_autenticado(request) -> Solicitante:
    usuario = request.user
    return Solicitante(
        usuario_id=usuario.pk, nome=usuario.nome, matricula=usuario.matricula
    )


def ator_autenticado(request) -> Ator:
    usuario = request.user
    papel = PapelDoAtor.GESTOR if usuario.eh_gestor else PapelDoAtor.SOLICITANTE
    return Ator(usuario_id=usuario.pk, papel=papel)
