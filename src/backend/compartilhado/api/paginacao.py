from rest_framework import serializers

from compartilhado.domain.paginacao import (
    TAMANHO_MAXIMO_DA_PAGINA,
    TAMANHO_PADRAO_DA_PAGINA,
    Paginacao,
)


class FiltrosDePaginaSerializer(serializers.Serializer):
    pagina = serializers.IntegerField(required=False, allow_null=True, min_value=1)
    tamanho = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=1,
        max_value=TAMANHO_MAXIMO_DA_PAGINA,
    )

    def para_paginacao(self) -> Paginacao:
        dados = self.validated_data
        return Paginacao(
            numero=dados.get("pagina") or 1,
            tamanho=dados.get("tamanho") or TAMANHO_PADRAO_DA_PAGINA,
        )


class PaginacaoSaidaSerializer(serializers.Serializer):
    pagina = serializers.IntegerField(source="paginacao.numero")
    tamanho = serializers.IntegerField(source="paginacao.tamanho")
    total = serializers.IntegerField()
    total_de_paginas = serializers.IntegerField()
