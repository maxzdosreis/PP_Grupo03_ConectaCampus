from django.db import IntegrityError, transaction

from contas.application.portas import RepositorioUsuarios, UsuarioCadastrado
from contas.domain.cadastro import DadosDeCadastro
from contas.domain.excecoes import EmailJaCadastrado, MatriculaJaCadastrada
from contas.domain.perfil import PerfilUsuario
from contas.infrastructure.models import Usuario

_TABELA = Usuario._meta.db_table


_EXCECAO_POR_PREFIXO = {
    f"{_TABELA}_email": EmailJaCadastrado,
    f"{_TABELA}_matricula": MatriculaJaCadastrada,
}


class RepositorioUsuariosDjango(RepositorioUsuarios):
    def existe_email(self, email: str) -> bool:
        return Usuario.objects.filter(email__iexact=email).exists()

    def existe_matricula(self, matricula: str) -> bool:
        return Usuario.objects.filter(matricula=matricula).exists()

    def criar_solicitante(
        self, dados: DadosDeCadastro, senha: str
    ) -> UsuarioCadastrado:
        try:
            with transaction.atomic():
                usuario = Usuario.objects.create_user(
                    dados.email,
                    senha,
                    nome=dados.nome,
                    matricula=dados.matricula,
                    perfil=PerfilUsuario.SOLICITANTE.value,
                )
        except IntegrityError as erro:
            excecao = _excecao_de_unicidade(erro)
            if excecao is None:
                raise
            raise excecao() from erro
        return _para_cadastrado(usuario)

    def dados_de_cadastro(self, usuario_id: int) -> DadosDeCadastro:
        usuario = Usuario.objects.get(pk=usuario_id)
        return DadosDeCadastro(
            nome=usuario.nome, matricula=usuario.matricula, email=usuario.email
        )

    def senha_confere(self, usuario_id: int, senha: str) -> bool:
        return Usuario.objects.get(pk=usuario_id).check_password(senha)

    def trocar_senha(self, usuario_id: int, nova_senha: str) -> None:
        with transaction.atomic():
            usuario = Usuario.objects.select_for_update().get(pk=usuario_id)
            usuario.set_password(nova_senha)
            usuario.save(update_fields=["password"])


def _excecao_de_unicidade(erro: IntegrityError):
    diagnostico = getattr(erro.__cause__, "diag", None)
    constraint = getattr(diagnostico, "constraint_name", None) or ""
    for prefixo, excecao in _EXCECAO_POR_PREFIXO.items():
        if constraint.startswith(prefixo):
            return excecao
    return None


def _para_cadastrado(usuario: Usuario) -> UsuarioCadastrado:
    return UsuarioCadastrado(
        id=usuario.pk,
        nome=usuario.nome,
        email=usuario.email,
        matricula=usuario.matricula,
        perfil=usuario.perfil,
    )
