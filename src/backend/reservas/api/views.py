from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from compartilhado.api.respostas import mensagem_de_contagem, resposta_sucesso
from reservas.api import dependencias
from reservas.api.autenticacao import solicitante_autenticado
from reservas.api.serializers import (
    AlteracaoDeSituacaoSerializer,
    FiltrosReservasSerializer,
    ReservaEntradaSerializer,
    ReservaSaidaSerializer,
    SituacaoDeReservaSaidaSerializer,
)
from reservas.domain.situacao import SituacaoReserva


# AUT-05: SOLICITANTE só vê as próprias (lista filtrada; detalhe de outra pessoa → 404).
class ReservasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        filtros = FiltrosReservasSerializer(data=request.query_params)
        filtros.is_valid(raise_exception=True)
        reservas = dependencias.consultar_reservas().executar(
            filtros.para_filtros(request.user.pk)
        )
        return resposta_sucesso(
            mensagem_de_contagem(
                len(reservas),
                nenhum="Nenhuma reserva encontrada.",
                um="1 reserva encontrada.",
                varios="{total} reservas encontradas.",
            ),
            ReservaSaidaSerializer(reservas, many=True).data,
        )

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


# AUT-05: SOLICITANTE só vê as próprias (lista filtrada; detalhe de outra pessoa → 404).
class ReservaDetalheView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, reserva_id):
        reserva = dependencias.obter_reserva().executar(reserva_id)
        return resposta_sucesso(
            "Reserva encontrada.", ReservaSaidaSerializer(reserva).data
        )


# AUT-05: GESTOR confirma, recusa, conclui e cancela; SOLICITANTE só cancela as próprias
class ReservaSituacaoView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, reserva_id):
        entrada = AlteracaoDeSituacaoSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        reserva = dependencias.alterar_situacao_reserva().executar(
            reserva_id=reserva_id,
            nova_situacao=entrada.validated_data["situacao"],
            motivo=entrada.validated_data.get("motivo"),
        )
        return resposta_sucesso(
            f"Reserva {reserva.situacao.rotulo.lower()} com sucesso.",
            ReservaSaidaSerializer(reserva).data,
        )


class SituacoesDeReservaView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return resposta_sucesso(
            "Situações de reserva disponíveis.",
            SituacaoDeReservaSaidaSerializer(list(SituacaoReserva), many=True).data,
        )
