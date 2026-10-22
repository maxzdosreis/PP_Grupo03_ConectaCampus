from rest_framework import serializers

_MAIOR_IDENTIFICADOR_DO_BANCO = 9_223_372_036_854_775_807
_FORMATO_DA_HORA = "%H:%M"


class ReservaEntradaSerializer(serializers.Serializer):
    espaco_id = serializers.IntegerField(max_value=_MAIOR_IDENTIFICADOR_DO_BANCO)
    data = serializers.DateField()
    hora_inicio = serializers.TimeField()
    hora_fim = serializers.TimeField()
    finalidade = serializers.CharField(allow_blank=True)


class SolicitanteSaidaSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    nome = serializers.CharField()
    matricula = serializers.CharField()


class ReservaSaidaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    espaco_id = serializers.IntegerField()
    solicitante = SolicitanteSaidaSerializer()
    data = serializers.DateField(source="intervalo.data")
    hora_inicio = serializers.TimeField(
        source="intervalo.hora_inicio", format=_FORMATO_DA_HORA
    )
    hora_fim = serializers.TimeField(
        source="intervalo.hora_fim", format=_FORMATO_DA_HORA
    )
    finalidade = serializers.CharField()
    situacao = serializers.CharField(source="situacao.value")
    situacao_rotulo = serializers.CharField(source="situacao.rotulo")
    motivo_da_situacao = serializers.CharField(allow_null=True)
    criada_em = serializers.DateTimeField()
