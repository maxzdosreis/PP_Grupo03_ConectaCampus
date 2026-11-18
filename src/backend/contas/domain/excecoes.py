from collections.abc import Sequence

from compartilhado.domain.erros import (
    AcaoNaoPermitida,
    ConflitoDeEstado,
    DadosInvalidos,
    RecursoNaoEncontrado,
)


class MatriculaInvalida(DadosInvalidos):
    codigo = "MATRICULA_INVALIDA"
    campo = "matricula"

    def __init__(self, mensagem: str, limite: int | None = None) -> None:
        self.limite = limite
        super().__init__(mensagem)

    @classmethod
    def so_digitos(cls) -> "MatriculaInvalida":
        return cls(
            "A matrícula deve ter só dígitos (0 a 9), sem letras, espaços nem símbolos."
        )

    @classmethod
    def acima_do_limite_tecnico(cls, limite: int) -> "MatriculaInvalida":
        return cls(f"A matrícula pode ter no máximo {limite} dígitos.", limite)


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


class UsuarioNaoEncontrado(RecursoNaoEncontrado):
    codigo = "USUARIO_NAO_ENCONTRADO"
    mensagem_padrao = "Usuário não encontrado."


class PerfilInvalido(DadosInvalidos):
    codigo = "PERFIL_INVALIDO"
    campo = "perfil"
    mensagem_padrao = "Perfil inválido. Use SOLICITANTE ou GESTOR."


class NenhumaAlteracaoNoUsuario(DadosInvalidos):
    codigo = "NENHUMA_ALTERACAO_INFORMADA"
    mensagem_padrao = "Informe o perfil ou a situação (ativo) para alterar."


class NaoPodeRebaixarASiMesmo(AcaoNaoPermitida):
    codigo = "NAO_PODE_REBAIXAR_A_SI_MESMO"
    mensagem_padrao = (
        "Você não pode rebaixar o seu próprio perfil. "
        "Peça a outro Gestor que faça a alteração."
    )


class NaoPodeDesativarASiMesmo(AcaoNaoPermitida):
    codigo = "NAO_PODE_DESATIVAR_A_SI_MESMO"
    mensagem_padrao = (
        "Você não pode desativar a sua própria conta. "
        "Peça a outro Gestor que faça a alteração."
    )


class UltimoGestorAtivo(ConflitoDeEstado):
    codigo = "ULTIMO_GESTOR_ATIVO"
    mensagem_padrao = (
        "Esta é a última conta de Gestor ativa. Promova ou reative outro Gestor "
        "antes de rebaixar ou desativar esta."
    )
