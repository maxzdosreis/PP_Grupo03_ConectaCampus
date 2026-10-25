from rest_framework import serializers

from espacos.domain.tipo_espaco import TipoEspaco

_MAIOR_INTEIRO_DO_BANCO = 2_147_483_647


class EspacoEntradaSerializer(serializers.Serializer):
    nome = serializers.CharField(allow_blank=True)
    tipo = serializers.CharField(allow_blank=True)
    capacidade = serializers.IntegerField(max_value=_MAIOR_INTEIRO_DO_BANCO)


class FiltrosEspacosSerializer(serializers.Serializer):
    apenas_ativos = serializers.BooleanField(default=False)
    tipo = serializers.ChoiceField(
        choices=[(tipo.value, tipo.rotulo) for tipo in TipoEspaco],
        required=False,
        allow_blank=True,
    )

    def validate_tipo(self, valor):
        return TipoEspaco(valor) if valor else None


class EspacoSaidaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nome = serializers.CharField()
    tipo = serializers.CharField(source="tipo.value")
    tipo_rotulo = serializers.CharField(source="tipo.rotulo")
    capacidade = serializers.IntegerField()
    ativo = serializers.BooleanField()


class TipoDeEspacoSaidaSerializer(serializers.Serializer):
    valor = serializers.CharField(source="value")
    rotulo = serializers.CharField()
