from django.db import DatabaseError, connection
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny

from compartilhado.api.respostas import resposta_erro, resposta_sucesso


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except DatabaseError:
        return resposta_erro(
            "BANCO_INDISPONIVEL",
            "Não foi possível conectar ao banco de dados.",
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    return resposta_sucesso("API no ar.", {"banco": "ok"})
