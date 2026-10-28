from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from compartilhado.api.permissoes import ApenasGestor
from compartilhado.api.respostas import mensagem_de_contagem, resposta_sucesso
from espacos.api import dependencias
from espacos.api.serializers import (
    EspacoEntradaSerializer,
    EspacoSaidaSerializer,
    FiltrosEspacosSerializer,
    TipoDeEspacoSaidaSerializer,
)
from espacos.domain.tipo_espaco import TipoEspaco


class EspacosView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), ApenasGestor()]
        return super().get_permissions()

    def get(self, request):
        filtros = FiltrosEspacosSerializer(data=request.query_params)
        filtros.is_valid(raise_exception=True)
        espacos = dependencias.listar_espacos().executar(**filtros.validated_data)
        return resposta_sucesso(
            mensagem_de_contagem(
                len(espacos),
                nenhum="Nenhum espaço encontrado.",
                um="1 espaço encontrado.",
                varios="{total} espaços encontrados.",
            ),
            EspacoSaidaSerializer(espacos, many=True).data,
        )

    def post(self, request):
        entrada = EspacoEntradaSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        espaco = dependencias.cadastrar_espaco().executar(**entrada.validated_data)
        return resposta_sucesso(
            "Espaço cadastrado com sucesso.",
            EspacoSaidaSerializer(espaco).data,
            status=status.HTTP_201_CREATED,
        )


class EspacoDetalheView(APIView):
    def get(self, request, espaco_id):
        espaco = dependencias.obter_espaco().executar(espaco_id)
        return resposta_sucesso(
            "Espaço encontrado.", EspacoSaidaSerializer(espaco).data
        )


class TiposDeEspacoView(APIView):
    # Vocabulário público: não é dado de ninguém.
    permission_classes = [AllowAny]

    def get(self, request):
        return resposta_sucesso(
            "Tipos de espaço disponíveis.",
            TipoDeEspacoSaidaSerializer(list(TipoEspaco), many=True).data,
        )
