from rest_framework import serializers

from reservas.application.repositorio import FiltrosDeReservas
from reservas.domain.situacao import SituacaoReserva

_MAIOR_IDENTIFICADOR_DO_BANCO = 9_223_372_036_854_775_807
_FORMATO_DA_HORA = "%H:%M"


class ReservaEntradaSerializer(serializers.Serializer):
    espaco_id = serializers.IntegerField(max_value=_MAIOR_IDENTIFICADOR_DO_BANCO)
    data = serializers.DateField()
    hora_inicio = serializers.TimeField()
    hora_fim = serializers.TimeField()
    finalidade = serializers.CharField(allow_blank=True)


class FiltrosReservasSerializer(serializers.Serializer):
    espaco = serializers.IntegerField(
        required=False, min_value=1, max_value=_MAIOR_IDENTIFICADOR_DO_BANCO
    )
    situacao = serializers.ChoiceField(
        choices=[(situacao.value, situacao.rotulo) for situacao in SituacaoReserva],
        required=False,
        allow_blank=True,
    )
    data = serializers.DateField(required=False)
    solicitante = serializers.CharField(required=False, allow_blank=True)
    minhas = serializers.BooleanField(default=False)

    def validate_situacao(self, valor):
        return SituacaoReserva(valor) if valor else None

    def validate_solicitante(self, valor):
        return valor or None

    def para_filtros(self, usuario_id: int) -> FiltrosDeReservas:
        dados = self.validated_data
        return FiltrosDeReservas(
            espaco_id=dados.get("espaco"),
            situacao=dados.get("situacao"),
            data=dados.get("data"),
            solicitante_usuario_id=usuario_id if dados["minhas"] else None,
            solicitante=dados.get("solicitante"),
        )


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
