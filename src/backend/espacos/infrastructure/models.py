from django.db import models
from django.db.models.functions import Lower

from espacos.domain.espaco_esportivo import CAPACIDADE_MINIMA, NOME_MAXIMO_CARACTERES
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
        )

    def __str__(self):
        return self.nome
