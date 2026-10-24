from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from contas.application.portas import PoliticaDeSenha
from contas.domain.cadastro import DadosDeCadastro
from contas.domain.excecoes import SenhaFraca
from contas.infrastructure.models import Usuario


class PoliticaDeSenhaDjango(PoliticaDeSenha):
    def validar(self, senha: str, dados: DadosDeCadastro) -> None:
        usuario = Usuario(email=dados.email, nome=dados.nome, matricula=dados.matricula)
        try:
            validate_password(senha, user=usuario)
        except ValidationError as erro:
            raise SenhaFraca(erro.messages) from erro
