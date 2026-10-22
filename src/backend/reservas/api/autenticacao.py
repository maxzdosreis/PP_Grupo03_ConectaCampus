from reservas.domain.solicitante import Solicitante


def solicitante_autenticado(request) -> Solicitante:
    usuario = request.user
    return Solicitante(
        usuario_id=usuario.pk, nome=usuario.nome, matricula=usuario.matricula
    )
