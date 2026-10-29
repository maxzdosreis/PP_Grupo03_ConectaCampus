from collections.abc import Iterable

from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import (
    DateTimeRangeField,
    RangeBoundary,
    RangeOperators,
)
from django.db import models

from reservas.domain.reserva import (
    FINALIDADE_MAXIMO_CARACTERES,
    MOTIVO_MAXIMO_CARACTERES,
)
from reservas.domain.situacao import (
    SITUACOES_QUE_EXIGEM_MOTIVO,
    SITUACOES_QUE_OCUPAM_HORARIO,
    SituacaoReserva,
)

SITUACAO_CHOICES = [(situacao.value, situacao.rotulo) for situacao in SituacaoReserva]
_VALORES_DAS_SITUACOES = [situacao.value for situacao in SituacaoReserva]

_SITUACAO_MAXIMO_CARACTERES = max(len(situacao.value) for situacao in SituacaoReserva)

SOLICITANTE_NOME_MAXIMO_CARACTERES = 150
SOLICITANTE_MATRICULA_MAXIMO_CARACTERES = 20

CONSTRAINT_SEM_SOBREPOSICAO = "reservas_reserva_sem_sobreposicao_no_espaco"


def _valores(situacoes: Iterable[SituacaoReserva]) -> list[str]:
    return sorted(situacao.value for situacao in situacoes)


class TsTzRange(models.Func):
    function = "TSTZRANGE"
    output_field = DateTimeRangeField()


class ReservaModel(models.Model):
    espaco_id = models.BigIntegerField("espaço")
    solicitante_usuario_id = models.BigIntegerField(
        "usuário solicitante", db_index=True
    )
    solicitante_nome = models.CharField(
        "nome do solicitante", max_length=SOLICITANTE_NOME_MAXIMO_CARACTERES
    )
    solicitante_matricula = models.CharField(
        "matrícula do solicitante", max_length=SOLICITANTE_MATRICULA_MAXIMO_CARACTERES
    )
    inicio = models.DateTimeField("início")
    fim = models.DateTimeField("fim")
    finalidade = models.CharField("finalidade", max_length=FINALIDADE_MAXIMO_CARACTERES)
    situacao = models.CharField(
        "situação", max_length=_SITUACAO_MAXIMO_CARACTERES, choices=SITUACAO_CHOICES
    )
    motivo_da_situacao = models.CharField(
        "motivo da situação",
        max_length=MOTIVO_MAXIMO_CARACTERES,
        blank=True,
        default="",
    )
    criada_em = models.DateTimeField("criada em")

    class Meta:
        db_table = "reservas_reserva"
        ordering = ("inicio", "id")
        verbose_name = "reserva"
        verbose_name_plural = "reservas"
        indexes = (
            models.Index(
                fields=("espaco_id", "inicio"),
                name="reservas_espaco_inicio_idx",
            ),
        )
        constraints = (
            models.CheckConstraint(
                condition=models.Q(fim__gt=models.F("inicio")),
                name="reservas_reserva_fim_apos_inicio",
            ),
            models.CheckConstraint(
                condition=models.Q(situacao__in=_VALORES_DAS_SITUACOES),
                name="reservas_reserva_situacao_valida",
            ),
            models.CheckConstraint(
                condition=~models.Q(situacao__in=_valores(SITUACOES_QUE_EXIGEM_MOTIVO))
                | ~models.Q(motivo_da_situacao=""),
                name="reservas_reserva_motivo_obrigatorio",
            ),
            ExclusionConstraint(
                name=CONSTRAINT_SEM_SOBREPOSICAO,
                expressions=(
                    (
                        TsTzRange(
                            "inicio",
                            "fim",
                            RangeBoundary(inclusive_lower=True, inclusive_upper=False),
                        ),
                        RangeOperators.OVERLAPS,
                    ),
                    ("espaco_id", RangeOperators.EQUAL),
                ),
                condition=models.Q(situacao__in=_valores(SITUACOES_QUE_OCUPAM_HORARIO)),
            ),
        )

    def __str__(self):
        return f"Reserva #{self.pk} ({self.get_situacao_display()})"


class RegistroDeSituacaoModel(models.Model):
    reserva = models.ForeignKey(
        ReservaModel,
        on_delete=models.PROTECT,
        related_name="registros_de_situacao",
        verbose_name="reserva",
        db_index=False,
    )
    situacao_anterior = models.CharField(
        "situação anterior",
        max_length=_SITUACAO_MAXIMO_CARACTERES,
        choices=SITUACAO_CHOICES,
        blank=True,
        default="",
    )
    situacao_nova = models.CharField(
        "situação nova",
        max_length=_SITUACAO_MAXIMO_CARACTERES,
        choices=SITUACAO_CHOICES,
    )
    motivo = models.CharField(
        "motivo", max_length=MOTIVO_MAXIMO_CARACTERES, blank=True, default=""
    )
    autor_usuario_id = models.BigIntegerField("usuário autor")
    autor_nome = models.CharField(
        "nome do autor", max_length=SOLICITANTE_NOME_MAXIMO_CARACTERES
    )
    registrado_em = models.DateTimeField("registrado em")

    class Meta:
        db_table = "reservas_registro_de_situacao"
        ordering = ("registrado_em", "id")
        verbose_name = "registro de situação"
        verbose_name_plural = "registros de situação"
        indexes = (
            models.Index(
                fields=("reserva", "registrado_em"), name="reservas_historico_idx"
            ),
        )
        constraints = (
            models.CheckConstraint(
                condition=models.Q(situacao_nova__in=_VALORES_DAS_SITUACOES)
                & (
                    models.Q(situacao_anterior="")
                    | models.Q(situacao_anterior__in=_VALORES_DAS_SITUACOES)
                ),
                name="reservas_registro_de_situacao_situacoes_validas",
            ),
            models.CheckConstraint(
                condition=~models.Q(situacao_anterior=models.F("situacao_nova")),
                name="reservas_registro_de_situacao_anterior_diferente_da_nova",
            ),
        )

    def __str__(self):
        nova = self.get_situacao_nova_display()
        if not self.situacao_anterior:
            return f"Reserva #{self.reserva_id}: criada como {nova}"
        anterior = self.get_situacao_anterior_display()
        return f"Reserva #{self.reserva_id}: {anterior} → {nova}"
