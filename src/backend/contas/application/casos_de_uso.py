from compartilhado.domain.erros import CampoObrigatorioAusente
from contas.application.portas import (
    PoliticaDeSenha,
    RepositorioUsuarios,
    UsuarioCadastrado,
)
from contas.domain.cadastro import DadosDeCadastro
from contas.domain.excecoes import EmailJaCadastrado, MatriculaJaCadastrada


class CadastrarSolicitante:
    def __init__(
        self, repositorio: RepositorioUsuarios, politica_de_senha: PoliticaDeSenha
    ) -> None:
        self._repositorio = repositorio
        self._politica_de_senha = politica_de_senha

    def executar(
        self, *, nome: str, matricula: str, email: str, senha: str
    ) -> UsuarioCadastrado:
        dados = DadosDeCadastro(nome=nome, matricula=matricula, email=email)
        # Só espaços conta como vazia: os validadores do Django aceitariam.
        if not (senha or "").strip():
            raise CampoObrigatorioAusente("senha", "Senha")
        self._politica_de_senha.validar(senha, dados)
        if self._repositorio.existe_email(dados.email):
            raise EmailJaCadastrado()
        if self._repositorio.existe_matricula(dados.matricula):
            raise MatriculaJaCadastrada()
        return self._repositorio.criar_solicitante(dados, senha)
