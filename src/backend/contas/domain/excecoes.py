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

    def __init__(self, motivos: Sequence[str], campo: str = "senha") -> None:
        self.motivos = tuple(motivos)
        self.campo = campo
        super().__init__(" ".join(_terminar_com_ponto(m) for m in self.motivos))


class SenhaAtualIncorreta(DadosInvalidos):
    codigo = "SENHA_ATUAL_INCORRETA"
    campo = "senha_atual"
    mensagem_padrao = "A senha atual está incorreta."


class NovaSenhaIgualAAtual(DadosInvalidos):
    codigo = "NOVA_SENHA_IGUAL_A_ATUAL"
    campo = "nova_senha"
    mensagem_padrao = "A nova senha deve ser diferente da senha atual."


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
