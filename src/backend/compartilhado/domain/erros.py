class ErroDeDominio(Exception):
    codigo = "ERRO_DE_DOMINIO"
    mensagem_padrao = "Não foi possível concluir a operação."
    campo: str | None = None

    def __init__(self, mensagem: str | None = None) -> None:
        self.mensagem = mensagem or self.mensagem_padrao
        super().__init__(self.mensagem)


class DadosInvalidos(ErroDeDominio):
    codigo = "DADOS_INVALIDOS"
    mensagem_padrao = "Verifique os dados informados."


class RecursoNaoEncontrado(ErroDeDominio):
    codigo = "NAO_ENCONTRADO"
    mensagem_padrao = "O recurso solicitado não foi encontrado."


class ConflitoDeEstado(ErroDeDominio):
    codigo = "CONFLITO_DE_ESTADO"
    mensagem_padrao = "A operação não é compatível com a situação atual."


class AcaoNaoPermitida(ErroDeDominio):
    codigo = "ACAO_NAO_PERMITIDA"
    mensagem_padrao = "Você não tem permissão para realizar esta ação."


class CampoObrigatorioAusente(DadosInvalidos):
    codigo = "CAMPO_OBRIGATORIO_AUSENTE"

    def __init__(self, campo: str, rotulo: str) -> None:
        self.campo = campo
        super().__init__(f'O campo "{rotulo}" é obrigatório.')
