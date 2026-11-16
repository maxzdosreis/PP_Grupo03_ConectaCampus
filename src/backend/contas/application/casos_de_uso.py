from compartilhado.domain.erros import CampoObrigatorioAusente
from compartilhado.domain.paginacao import Paginacao, PaginaDeItens
from contas.application.portas import (
    FiltrosDeUsuarios,
    PoliticaDeSenha,
    RepositorioGestaoDeUsuarios,
    RepositorioUsuarios,
    ResultadoDaAlteracao,
    UsuarioCadastrado,
    UsuarioGerenciado,
)
from contas.domain.cadastro import DadosDeCadastro
from contas.domain.excecoes import (
    EmailJaCadastrado,
    MatriculaJaCadastrada,
    NenhumaAlteracaoNoUsuario,
    NovaSenhaIgualAAtual,
    SenhaAtualIncorreta,
    SenhaFraca,
)
from contas.domain.gestao import (
    SituacaoDoUsuario,
    garantir_alteracao_permitida,
    situacao_pedida,
)
from contas.domain.perfil import PerfilUsuario


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


class AlterarSenha:
    def __init__(
        self, repositorio: RepositorioUsuarios, politica_de_senha: PoliticaDeSenha
    ) -> None:
        self._repositorio = repositorio
        self._politica_de_senha = politica_de_senha

    def executar(self, *, usuario_id: int, senha_atual: str, nova_senha: str) -> None:
        if not (senha_atual or "").strip():
            raise CampoObrigatorioAusente("senha_atual", "Senha atual")
        if not (nova_senha or "").strip():
            raise CampoObrigatorioAusente("nova_senha", "Nova senha")
        if not self._repositorio.senha_confere(usuario_id, senha_atual):
            raise SenhaAtualIncorreta()
        if nova_senha == senha_atual:
            raise NovaSenhaIgualAAtual()
        dados = self._repositorio.dados_de_cadastro(usuario_id)
        try:
            self._politica_de_senha.validar(nova_senha, dados)
        except SenhaFraca as erro:
            raise SenhaFraca(erro.motivos, campo="nova_senha") from erro
        self._repositorio.trocar_senha(usuario_id, nova_senha)


class ListarUsuarios:
    def __init__(self, repositorio: RepositorioGestaoDeUsuarios) -> None:
        self._repositorio = repositorio

    def executar(
        self, filtros: FiltrosDeUsuarios, paginacao: Paginacao
    ) -> PaginaDeItens[UsuarioGerenciado]:
        return self._repositorio.listar(filtros, paginacao)


class AlterarUsuario:
    def __init__(self, repositorio: RepositorioGestaoDeUsuarios) -> None:
        self._repositorio = repositorio

    def executar(
        self,
        *,
        usuario_id: int,
        ator_id: int,
        perfil: PerfilUsuario | None = None,
        ativo: bool | None = None,
    ) -> ResultadoDaAlteracao:
        if perfil is None and ativo is None:
            raise NenhumaAlteracaoNoUsuario()

        def decidir(
            atual: UsuarioGerenciado, gestores_ativos: int
        ) -> SituacaoDoUsuario:
            nova = situacao_pedida(atual.situacao, perfil=perfil, ativo=ativo)
            garantir_alteracao_permitida(
                ator_id=ator_id,
                alvo_id=usuario_id,
                atual=atual.situacao,
                nova=nova,
                gestores_ativos=gestores_ativos,
            )
            return nova

        return self._repositorio.alterar_sob_trava(usuario_id, decidir)
