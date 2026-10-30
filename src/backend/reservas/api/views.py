from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from compartilhado.api.respostas import mensagem_de_contagem, resposta_sucesso
from reservas.api import dependencias
from reservas.api.autenticacao import ator_autenticado, solicitante_autenticado
from reservas.api.serializers import (
    AlteracaoDeSituacaoSerializer,
    FiltrosReservasSerializer,
    RegistroDeSituacaoSaidaSerializer,
    RegrasDeAgendaSaidaSerializer,
    ReservaEntradaSerializer,
    ReservaSaidaSerializer,
    SituacaoDeReservaSaidaSerializer,
)
from reservas.domain.situacao import SituacaoReserva


class ReservasView(APIView):
    def get(self, request):
        ator = ator_autenticado(request)
        filtros = FiltrosReservasSerializer(data=request.query_params)
        filtros.is_valid(raise_exception=True)
        reservas = dependencias.consultar_reservas().executar(
            filtros.para_filtros(ator.usuario_id), ator=ator
        )
        return resposta_sucesso(
            mensagem_de_contagem(
                len(reservas),
                nenhum="Nenhuma reserva encontrada.",
                um="1 reserva encontrada.",
                varios="{total} reservas encontradas.",
            ),
            _saida(reservas, ator, many=True),
        )

    def post(self, request):
        entrada = ReservaEntradaSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        reserva = dependencias.criar_reserva().executar(
            solicitante=solicitante_autenticado(request), **entrada.validated_data
        )
        return resposta_sucesso(
            "Reserva solicitada com sucesso. Aguarde a confirmação do gestor.",
            _saida(reserva, ator_autenticado(request)),
            status=status.HTTP_201_CREATED,
        )


class ReservaDetalheView(APIView):
    def get(self, request, reserva_id):
        ator = ator_autenticado(request)
        reserva = dependencias.obter_reserva().executar(reserva_id, ator=ator)
        return resposta_sucesso("Reserva encontrada.", _saida(reserva, ator))


class ReservaSituacaoView(APIView):
    def patch(self, request, reserva_id):
        ator = ator_autenticado(request)
        entrada = AlteracaoDeSituacaoSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        reserva = dependencias.alterar_situacao_reserva().executar(
            reserva_id=reserva_id,
            nova_situacao=entrada.validated_data["situacao"],
            motivo=entrada.validated_data.get("motivo"),
            ator=ator,
        )
        return resposta_sucesso(
            f"Reserva {reserva.situacao.rotulo.lower()} com sucesso.",
            _saida(reserva, ator),
        )


class HistoricoDaReservaView(APIView):
    def get(self, request, reserva_id):
        registros = dependencias.consultar_historico_da_reserva().executar(
            reserva_id, ator=ator_autenticado(request)
        )
        return resposta_sucesso(
            "Histórico da reserva.",
            RegistroDeSituacaoSaidaSerializer(registros, many=True).data,
        )


class SituacoesDeReservaView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return resposta_sucesso(
            "Situações de reserva disponíveis.",
            SituacaoDeReservaSaidaSerializer(list(SituacaoReserva), many=True).data,
        )


class RegrasDeAgendaView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return resposta_sucesso(
            "Regras de agenda.",
            RegrasDeAgendaSaidaSerializer.vigentes(timezone.now()).data,
        )


def _saida(reservas, ator, *, many=False):
    return ReservaSaidaSerializer(reservas, many=many, context={"ator": ator}).data
