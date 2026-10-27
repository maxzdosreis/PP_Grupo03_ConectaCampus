from datetime import date, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from compartilhado.domain.erros import ErroDeDominio
from exemplos.carga import (
    ResultadoDaEtapa,
    garantir_espacos,
    garantir_reservas,
    garantir_usuarios,
)
from exemplos.dados import CONFLITO_PARA_DEMONSTRACAO, USUARIOS

MENSAGEM_SEM_DEBUG = (
    "Os dados de exemplo só podem ser carregados com DJANGO_DEBUG=True, "
    "porque criam usuários com senhas conhecidas."
)


class Command(BaseCommand):
    help = (
        "Carrega usuários, espaços e reservas de exemplo para a correção e a "
        "demonstração. Pode ser executado mais de uma vez sem duplicar dados. "
        "Só roda com DJANGO_DEBUG=True."
    )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError(MENSAGEM_SEM_DEBUG)
        hoje = timezone.localdate()
        resultados = self._carregar(hoje)
        self._escrever_resumo(resultados)
        self._escrever_usuarios()
        self._escrever_conflito(hoje)

    def _carregar(self, hoje: date) -> dict[tuple[str, str, str], ResultadoDaEtapa]:
        try:
            with transaction.atomic():
                return {
                    ("Usuários", "criado", "criados"): garantir_usuarios(),
                    ("Espaços", "criado", "criados"): garantir_espacos(),
                    ("Reservas", "criada", "criadas"): garantir_reservas(
                        hoje, timezone.now()
                    ),
                }
        except ErroDeDominio as erro:
            raise CommandError(f"Dado de exemplo inválido: {erro.mensagem}") from erro

    def _escrever_resumo(self, resultados) -> None:
        for (rotulo, singular, plural), resultado in resultados.items():
            criados = singular if resultado.criados == 1 else plural
            existiam = "já existia" if resultado.existentes == 1 else "já existiam"
            linha = (
                f"{rotulo}: {resultado.criados} {criados}, "
                f"{resultado.existentes} {existiam}."
            )
            estilo = self.style.SUCCESS if resultado.criados else self.style.WARNING
            self.stdout.write(estilo(linha))

    def _escrever_usuarios(self) -> None:
        self.stdout.write("")
        self.stdout.write("Usuários de exemplo (senhas só para teste local):")
        self.stdout.write(f"  {'E-mail':<28}{'Perfil':<13}Senha")
        for usuario in USUARIOS:
            self.stdout.write(
                f"  {usuario.email:<28}{usuario.perfil.rotulo:<13}{usuario.senha}"
            )

    def _escrever_conflito(self, hoje: date) -> None:
        conflito = CONFLITO_PARA_DEMONSTRACAO
        data = hoje + timedelta(days=conflito.dias_a_partir_de_hoje)
        self.stdout.write("")
        self.stdout.write(
            "Horário para demonstrar o conflito (409): "
            f"{conflito.espaco}, {data:%d/%m/%Y}, "
            f"{conflito.hora_inicio:%H:%M}–{conflito.hora_fim:%H:%M}."
        )
