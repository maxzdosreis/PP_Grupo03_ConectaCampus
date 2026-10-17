from django.db import DatabaseError, connection
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except DatabaseError:
        return Response(
            {
                "erro": {
                    "codigo": "BANCO_INDISPONIVEL",
                    "mensagem": "Não foi possível conectar ao banco de dados.",
                }
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    return Response({"mensagem": "API no ar.", "dados": {"banco": "ok"}})
