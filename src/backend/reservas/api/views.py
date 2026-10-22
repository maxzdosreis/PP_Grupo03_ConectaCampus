from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from compartilhado.api.respostas import resposta_sucesso
from reservas.api import dependencias
from reservas.api.autenticacao import solicitante_autenticado
from reservas.api.serializers import ReservaEntradaSerializer, ReservaSaidaSerializer


class ReservasView(APIView):
    permission_classes = [IsAuthenticated]

    # RES-05: GET com filtros nesta mesma view.

    def post(self, request):
        entrada = ReservaEntradaSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        reserva = dependencias.criar_reserva().executar(
            solicitante=solicitante_autenticado(request), **entrada.validated_data
        )
        return resposta_sucesso(
            "Reserva solicitada com sucesso. Aguarde a confirmação do gestor.",
            ReservaSaidaSerializer(reserva).data,
            status=status.HTTP_201_CREATED,
        )
