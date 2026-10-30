from datetime import datetime, timedelta

from rest_framework import serializers

from reservas.application.repositorio import FiltrosDeReservas
from reservas.domain.regras_de_agenda import (
    ANTECEDENCIA_MAXIMA_EM_DIAS,
    DURACAO_MAXIMA,
    DURACAO_MINIMA,
    HORARIO_DE_ABERTURA,
    HORARIO_DE_FECHAMENTO,
    data_limite_para_reservar,
)
from reservas.domain.situacao import SITUACOES_QUE_EXIGEM_MOTIVO, SituacaoReserva

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


class FiltrosDeOcupacaoSerializer(serializers.Serializer):
    espaco = serializers.IntegerField(
        min_value=1, max_value=_MAIOR_IDENTIFICADOR_DO_BANCO
    )
    data = serializers.DateField()


class AlteracaoDeSituacaoSerializer(serializers.Serializer):
    situacao = serializers.CharField()
    motivo = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class SituacaoDeReservaSaidaSerializer(serializers.Serializer):
    valor = serializers.CharField(source="value")
    rotulo = serializers.CharField()


class RegrasDeAgendaSaidaSerializer(serializers.Serializer):
    horario_de_abertura = serializers.TimeField(format=_FORMATO_DA_HORA)
    horario_de_fechamento = serializers.TimeField(format=_FORMATO_DA_HORA)
    duracao_minima_em_minutos = serializers.IntegerField()
    duracao_maxima_em_minutos = serializers.IntegerField()
    antecedencia_maxima_em_dias = serializers.IntegerField()
    data_limite = serializers.DateField()

    @classmethod
    def vigentes(cls, agora: datetime) -> "RegrasDeAgendaSaidaSerializer":
        return cls(
            {
                "horario_de_abertura": HORARIO_DE_ABERTURA,
                "horario_de_fechamento": HORARIO_DE_FECHAMENTO,
                "duracao_minima_em_minutos": _em_minutos(DURACAO_MINIMA),
                "duracao_maxima_em_minutos": _em_minutos(DURACAO_MAXIMA),
                "antecedencia_maxima_em_dias": ANTECEDENCIA_MAXIMA_EM_DIAS,
                "data_limite": data_limite_para_reservar(agora),
            }
        )


def _em_minutos(duracao: timedelta) -> int:
    return duracao // timedelta(minutes=1)


class HorarioLivreSaidaSerializer(serializers.Serializer):
    hora_inicio = serializers.TimeField(format=_FORMATO_DA_HORA)
    hora_fim = serializers.TimeField(format=_FORMATO_DA_HORA)


class HorarioOcupadoSaidaSerializer(serializers.Serializer):
    hora_inicio = serializers.TimeField(
        source="intervalo.hora_inicio", format=_FORMATO_DA_HORA
    )
    hora_fim = serializers.TimeField(
        source="intervalo.hora_fim", format=_FORMATO_DA_HORA
    )
    situacao = serializers.CharField(source="situacao.value")
    situacao_rotulo = serializers.CharField(source="situacao.rotulo")


class OcupacaoDoDiaSaidaSerializer(serializers.Serializer):
    data = serializers.DateField()
    horario_de_abertura = serializers.TimeField(format=_FORMATO_DA_HORA)
    horario_de_fechamento = serializers.TimeField(format=_FORMATO_DA_HORA)
    reservavel = serializers.BooleanField()
    motivo_indisponivel = serializers.CharField(allow_null=True)
    ocupados = HorarioOcupadoSaidaSerializer(many=True)
    livres = HorarioLivreSaidaSerializer(many=True)


class AcaoDisponivelSaidaSerializer(serializers.Serializer):
    situacao = serializers.CharField(source="value")
    rotulo = serializers.CharField(source="rotulo_da_acao")
    exige_motivo = serializers.SerializerMethodField()

    def get_exige_motivo(self, situacao):
        return situacao in SITUACOES_QUE_EXIGEM_MOTIVO


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
    acoes_disponiveis = serializers.SerializerMethodField()

    def get_acoes_disponiveis(self, reserva):
        destinos = reserva.acoes_permitidas_para(self.context["ator"])
        return AcaoDisponivelSaidaSerializer(destinos, many=True).data


class AutorDoRegistroSaidaSerializer(serializers.Serializer):
    nome = serializers.CharField(source="autor_nome")


class RegistroDeSituacaoSaidaSerializer(serializers.Serializer):
    situacao_anterior = serializers.SerializerMethodField()
    situacao_anterior_rotulo = serializers.SerializerMethodField()
    situacao_nova = serializers.CharField(source="situacao_nova.value")
    situacao_nova_rotulo = serializers.CharField(source="situacao_nova.rotulo")
    motivo = serializers.CharField(allow_null=True)
    autor = AutorDoRegistroSaidaSerializer(source="*")
    registrado_em = serializers.DateTimeField()

    def get_situacao_anterior(self, registro):
        anterior = registro.situacao_anterior
        return anterior.value if anterior else None

    def get_situacao_anterior_rotulo(self, registro):
        anterior = registro.situacao_anterior
        return anterior.rotulo if anterior else None
