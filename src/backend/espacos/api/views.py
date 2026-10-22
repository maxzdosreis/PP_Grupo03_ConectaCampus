from rest_framework import status
from rest_framework.views import APIView

from compartilhado.api.respostas import mensagem_de_contagem, resposta_sucesso
from espacos.api import dependencias
from espacos.api.serializers import (
    EspacoEntradaSerializer,
    EspacoSaidaSerializer,
    FiltrosEspacosSerializer,
)


class EspacosView(APIView):
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
        # AUT-05: restringir a GESTOR.
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
