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


class HorarioDeFuncionamentoInvalido(DadosInvalidos):
    codigo = "HORARIO_DE_FUNCIONAMENTO_INVALIDO"

    def __init__(self, campo: str) -> None:
        self.campo = campo
        if campo == "fechamento":
            mensagem = "O fechamento deve ser depois da abertura."
        else:
            mensagem = "Informe um horário de abertura entre 00:00 e 23:59."
        super().__init__(mensagem)


class JanelaDeFuncionamentoCurta(DadosInvalidos):
    codigo = "JANELA_DE_FUNCIONAMENTO_CURTA"
    campo = "fechamento"

    def __init__(self, minimo_em_minutos: int) -> None:
        self.minimo_em_minutos = minimo_em_minutos
        super().__init__(
            f"O espaço deve funcionar por pelo menos {minimo_em_minutos} minutos."
        )


class HorarioIncompativelComReservas(ConflitoDeEstado):
    codigo = "HORARIO_INCOMPATIVEL_COM_RESERVAS"

    def __init__(self, quantidade: int) -> None:
        self.quantidade = quantidade
        reservas = (
            "1 reserva ativa ficaria fora"
            if quantidade == 1
            else f"{quantidade} reservas ativas ficariam fora"
        )
        super().__init__(
            f"Não é possível alterar o horário: {reservas} do novo horário. "
            "Cancele ou conclua essas reservas antes de reduzir o horário."
        )


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


class NenhumaAlteracaoInformada(DadosInvalidos):
    codigo = "NENHUMA_ALTERACAO_INFORMADA"
    mensagem_padrao = "Informe ao menos um campo para alterar."


class EspacoJaInativo(ConflitoDeEstado):
    codigo = "ESPACO_JA_INATIVO"
    mensagem_padrao = "Este espaço já está inativo."


class EspacoJaAtivo(ConflitoDeEstado):
    codigo = "ESPACO_JA_ATIVO"
    mensagem_padrao = "Este espaço já está ativo."


class EspacoDesatualizado(ConflitoDeEstado):
    codigo = "ESPACO_DESATUALIZADO"
    mensagem_padrao = (
        "Este espaço foi alterado por outra pessoa enquanto você decidia. "
        "Atualize a lista e tente de novo."
    )
