from compartilhado.domain.erros import (
    ConflitoDeEstado,
    DadosInvalidos,
    RecursoNaoEncontrado,
)
from espacos.domain.tipo_espaco import TipoEspaco

_TIPOS_ACEITOS = ", ".join(tipo.rotulo for tipo in TipoEspaco)


class NomeDeEspacoMuitoLongo(DadosInvalidos):
    codigo = "NOME_DE_ESPACO_MUITO_LONGO"
    campo = "nome"

    def __init__(self, limite: int) -> None:
        self.limite = limite
        super().__init__(f"O nome do espaço deve ter no máximo {limite} caracteres.")


class TipoDeEspacoInvalido(DadosInvalidos):
    codigo = "TIPO_DE_ESPACO_INVALIDO"
    campo = "tipo"
    mensagem_padrao = f"Tipo de espaço inválido. Escolha um destes: {_TIPOS_ACEITOS}."


class CapacidadeInvalida(DadosInvalidos):
    codigo = "CAPACIDADE_INVALIDA"
    campo = "capacidade"
    mensagem_padrao = "A capacidade deve ser um número inteiro maior que zero."


class NomeDeEspacoJaCadastrado(ConflitoDeEstado):
    codigo = "NOME_DE_ESPACO_JA_CADASTRADO"
    campo = "nome"
    mensagem_padrao = "Já existe um espaço com este nome."


class EspacoNaoEncontrado(RecursoNaoEncontrado):
    codigo = "ESPACO_NAO_ENCONTRADO"

    def __init__(self, espaco_id: int) -> None:
        self.espaco_id = espaco_id
        super().__init__(f"Espaço de código {espaco_id} não encontrado.")


class EspacoInativo(ConflitoDeEstado):
    codigo = "ESPACO_INATIVO"
    mensagem_padrao = "Este espaço está inativo e não aceita reservas."
