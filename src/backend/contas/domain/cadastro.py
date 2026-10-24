from dataclasses import dataclass

from compartilhado.domain.erros import CampoObrigatorioAusente, TextoMuitoLongo
from contas.domain.excecoes import MatriculaInvalida

NOME_MAXIMO_CARACTERES = 150
MATRICULA_MAXIMO_CARACTERES = 20


def normalizar_email(email: str | None) -> str:
    return (email or "").strip().lower()


def normalizar_nome(nome: str | None) -> str:
    return " ".join((nome or "").split())


def _exigir(valor: str, campo: str, rotulo: str) -> str:
    if not valor:
        raise CampoObrigatorioAusente(campo, rotulo)
    return valor


def _validar_nome(nome: str | None) -> str:
    nome = _exigir(normalizar_nome(nome), "nome", "Nome")
    if len(nome) > NOME_MAXIMO_CARACTERES:
        raise TextoMuitoLongo("nome", "Nome", NOME_MAXIMO_CARACTERES)
    return nome


def _validar_matricula(matricula: str | None) -> str:
    matricula = _exigir((matricula or "").strip(), "matricula", "Matrícula")
    if len(matricula) > MATRICULA_MAXIMO_CARACTERES or len(matricula.split()) > 1:
        raise MatriculaInvalida(MATRICULA_MAXIMO_CARACTERES)
    return matricula


@dataclass(frozen=True)
class DadosDeCadastro:
    nome: str
    matricula: str
    email: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "nome", _validar_nome(self.nome))
        object.__setattr__(self, "matricula", _validar_matricula(self.matricula))
        email = _exigir(normalizar_email(self.email), "email", "E-mail")
        object.__setattr__(self, "email", email)
