from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from compartilhado.api.permissoes import ApenasGestor
from compartilhado.api.respostas import mensagem_de_contagem, resposta_sucesso
from espacos.api import dependencias
from espacos.api.serializers import (
    EspacoEdicaoSerializer,
    EspacoEntradaSerializer,
    EspacoSaidaSerializer,
    FiltrosEspacosSerializer,
    TipoDeEspacoSaidaSerializer,
)
from espacos.domain.tipo_espaco import TipoEspaco


class _ViewComMetodosDoGestor(APIView):
    # Os outros métodos ficam com o padrão (IsAuthenticated): um método não
    # implementado responde 405 a qualquer pessoa logada, e não 403.
    metodos_do_gestor: tuple[str, ...] = ()

    def get_permissions(self):
        if self.request.method in self.metodos_do_gestor:
            return [IsAuthenticated(), ApenasGestor()]
        return super().get_permissions()


class EspacosView(_ViewComMetodosDoGestor):
    metodos_do_gestor = ("POST",)

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


class EspacoDetalheView(_ViewComMetodosDoGestor):
    metodos_do_gestor = ("PATCH",)

    def get(self, request, espaco_id):
        espaco = dependencias.obter_espaco().executar(espaco_id)
        return resposta_sucesso(
            "Espaço encontrado.", EspacoSaidaSerializer(espaco).data
        )

    def patch(self, request, espaco_id):
        entrada = EspacoEdicaoSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        espaco = dependencias.editar_espaco().executar(
            espaco_id, **entrada.validated_data
        )
        return resposta_sucesso(
            "Espaço atualizado com sucesso.", EspacoSaidaSerializer(espaco).data
        )


class DesativarEspacoView(_ViewComMetodosDoGestor):
    metodos_do_gestor = ("POST",)

    def post(self, request, espaco_id):
        espaco = dependencias.desativar_espaco().executar(espaco_id)
        return resposta_sucesso(
            "Espaço desativado. Novas reservas ficam bloqueadas; "
            "as existentes continuam valendo.",
            EspacoSaidaSerializer(espaco).data,
        )


class AtivarEspacoView(_ViewComMetodosDoGestor):
    metodos_do_gestor = ("POST",)

    def post(self, request, espaco_id):
        espaco = dependencias.ativar_espaco().executar(espaco_id)
        return resposta_sucesso("Espaço reativado.", EspacoSaidaSerializer(espaco).data)


class TiposDeEspacoView(APIView):
    # Vocabulário público: não é dado de ninguém.
    permission_classes = [AllowAny]

    def get(self, request):
        return resposta_sucesso(
            "Tipos de espaço disponíveis.",
            TipoDeEspacoSaidaSerializer(list(TipoEspaco), many=True).data,
        )
