from contas.application.portas import (
    PoliticaDeSenha,
    RepositorioUsuarios,
    UsuarioCadastrado,
)
from contas.domain.cadastro import DadosDeCadastro
from contas.domain.excecoes import EmailJaCadastrado, MatriculaJaCadastrada, SenhaFraca
from contas.domain.perfil import PerfilUsuario


class RepositorioUsuariosEmMemoria(RepositorioUsuarios):
    def __init__(self) -> None:
        self.criados: dict[int, UsuarioCadastrado] = {}
        self.senhas: dict[int, str] = {}
        self._proximo_id = 1

    def existe_email(self, email: str) -> bool:
        return any(
            usuario.email.casefold() == email.casefold()
            for usuario in self.criados.values()
        )

    def existe_matricula(self, matricula: str) -> bool:
        return any(usuario.matricula == matricula for usuario in self.criados.values())

    def criar_solicitante(
        self, dados: DadosDeCadastro, senha: str
    ) -> UsuarioCadastrado:
        if self.existe_email(dados.email):
            raise EmailJaCadastrado()
        if self.existe_matricula(dados.matricula):
            raise MatriculaJaCadastrada()
        usuario = UsuarioCadastrado(
            id=self._gerar_id(),
            nome=dados.nome,
            email=dados.email,
            matricula=dados.matricula,
            perfil=PerfilUsuario.SOLICITANTE.value,
        )
        self.criados[usuario.id] = usuario
        self.senhas[usuario.id] = senha
        return usuario

    def _gerar_id(self) -> int:
        usuario_id = self._proximo_id
        self._proximo_id += 1
        return usuario_id


class PoliticaDeSenhaFake(PoliticaDeSenha):
    MOTIVO = "Senha fraca para o teste."

    def __init__(self, senhas_fracas: tuple[str, ...] = ()) -> None:
        self._senhas_fracas = frozenset(senhas_fracas)

    def validar(self, senha: str, dados: DadosDeCadastro) -> None:
        if senha in self._senhas_fracas:
            raise SenhaFraca([self.MOTIVO])
