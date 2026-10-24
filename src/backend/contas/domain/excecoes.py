from collections.abc import Sequence

from compartilhado.domain.erros import ConflitoDeEstado, DadosInvalidos


class MatriculaInvalida(DadosInvalidos):
    codigo = "MATRICULA_INVALIDA"
    campo = "matricula"

    def __init__(self, limite: int) -> None:
        self.limite = limite
        super().__init__(
            f"A matrícula deve ter no máximo {limite} caracteres e não pode "
            "conter espaços."
        )


class SenhaFraca(DadosInvalidos):
    codigo = "SENHA_FRACA"
    campo = "senha"

    def __init__(self, motivos: Sequence[str]) -> None:
        self.motivos = tuple(motivos)
        super().__init__(" ".join(_terminar_com_ponto(m) for m in self.motivos))


def _terminar_com_ponto(frase: str) -> str:
    return frase if frase.endswith(".") else f"{frase}."


class EmailJaCadastrado(ConflitoDeEstado):
    codigo = "EMAIL_JA_CADASTRADO"
    campo = "email"
    mensagem_padrao = "Já existe um usuário com este e-mail."


class MatriculaJaCadastrada(ConflitoDeEstado):
    codigo = "MATRICULA_JA_CADASTRADA"
    campo = "matricula"
    mensagem_padrao = "Já existe um usuário com esta matrícula."
