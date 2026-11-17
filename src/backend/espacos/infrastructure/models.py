from django.db import models
from django.db.models.functions import Lower

from espacos.domain.espaco_esportivo import CAPACIDADE_MINIMA, NOME_MAXIMO_CARACTERES
from espacos.domain.horario_de_funcionamento import (
    ABERTURA_PADRAO_EM_MINUTOS,
    FECHAMENTO_PADRAO_EM_MINUTOS,
    JANELA_MINIMA_EM_MINUTOS,
    MINUTOS_NO_DIA,
)
from espacos.domain.tipo_espaco import TipoEspaco

TIPO_CHOICES = [(tipo.value, tipo.rotulo) for tipo in TipoEspaco]

_TIPO_MAXIMO_CARACTERES = max(len(tipo.value) for tipo in TipoEspaco)

CONSTRAINT_NOME_UNICO = "espacos_espaco_esportivo_nome_unico_sem_caixa"


class EspacoEsportivoModel(models.Model):
    nome = models.CharField("nome", max_length=NOME_MAXIMO_CARACTERES)
    tipo = models.CharField(
        "tipo", max_length=_TIPO_MAXIMO_CARACTERES, choices=TIPO_CHOICES
    )
    capacidade = models.PositiveIntegerField("capacidade")
    ativo = models.BooleanField("ativo", default=True)
    abertura_em_minutos = models.PositiveSmallIntegerField(
        "abertura (minutos)", default=ABERTURA_PADRAO_EM_MINUTOS
    )
    fechamento_em_minutos = models.PositiveSmallIntegerField(
        "fechamento (minutos)", default=FECHAMENTO_PADRAO_EM_MINUTOS
    )

    class Meta:
        db_table = "espacos_espaco_esportivo"
        ordering = ("nome",)
        verbose_name = "espaço esportivo"
        verbose_name_plural = "espaços esportivos"
        constraints = (
            models.UniqueConstraint(Lower("nome"), name=CONSTRAINT_NOME_UNICO),
            models.CheckConstraint(
                condition=models.Q(capacidade__gte=CAPACIDADE_MINIMA),
                name="espacos_espaco_esportivo_capacidade_minima",
            ),
            models.CheckConstraint(
                condition=models.Q(tipo__in=[tipo.value for tipo in TipoEspaco]),
                name="espacos_espaco_esportivo_tipo_valido",
            ),
            models.CheckConstraint(
                condition=models.Q(abertura_em_minutos__lt=MINUTOS_NO_DIA)
                & models.Q(fechamento_em_minutos__lte=MINUTOS_NO_DIA)
                & models.Q(
                    fechamento_em_minutos__gte=models.F("abertura_em_minutos")
                    + JANELA_MINIMA_EM_MINUTOS
                ),
                name="espacos_espaco_esportivo_horario_valido",
            ),
        )

    def __str__(self):
        return self.nome
