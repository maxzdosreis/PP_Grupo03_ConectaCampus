from dataclasses import dataclass
from typing import Protocol

from contas.domain.cadastro import DadosDeCadastro


@dataclass(frozen=True)
class UsuarioCadastrado:
    id: int
    nome: str
    email: str
    matricula: str
    perfil: str


class RepositorioUsuarios(Protocol):
    def existe_email(self, email: str) -> bool:
        """Diz se algum usuário já usa o e-mail, sem diferenciar maiúsculas."""

    def existe_matricula(self, matricula: str) -> bool:
        """Diz se algum usuário já usa a matrícula."""

    def criar_solicitante(
        self, dados: DadosDeCadastro, senha: str
    ) -> UsuarioCadastrado:
        """Cria um usuário com o perfil Solicitante, sem acesso ao admin.

        A senha é gravada só com hash. E-mail ou matrícula repetidos lançam
        EmailJaCadastrado ou MatriculaJaCadastrada, mesmo numa condição de
        corrida que passe pelas consultas acima.
        """


class PoliticaDeSenha(Protocol):
    def validar(self, senha: str, dados: DadosDeCadastro) -> None:
        """Lança SenhaFraca com todos os motivos quando a senha não é aceita."""
