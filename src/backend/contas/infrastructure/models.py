from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.functions import Lower

from contas.domain.cadastro import (
    MATRICULA_MAXIMO_CARACTERES,
    NOME_MAXIMO_CARACTERES,
    normalizar_email,
    normalizar_nome,
)
from contas.domain.excecoes import EmailJaCadastrado, MatriculaJaCadastrada
from contas.domain.perfil import PerfilUsuario

PERFIL_CHOICES = [(perfil.value, perfil.rotulo) for perfil in PerfilUsuario]

MENSAGEM_EMAIL_REPETIDO = EmailJaCadastrado.mensagem_padrao

_EXIGENCIAS_DO_SUPERUSUARIO = {
    "perfil": (PerfilUsuario.GESTOR, "O superusuário precisa ter o perfil Gestor."),
    "is_staff": (True, "O superusuário precisa ter is_staff=True."),
    "is_superuser": (True, "O superusuário precisa ter is_superuser=True."),
}


def _exigir(valor, mensagem):
    valor = (valor or "").strip()
    if not valor:
        raise ValueError(mensagem)
    return valor


class UsuarioManager(BaseUserManager):
    @classmethod
    def normalize_email(cls, email):
        return normalizar_email(email)

    def get_by_natural_key(self, email):
        return self.get(email=self.normalize_email(email))

    def create_user(self, email, senha=None, **campos):
        email = _exigir(self.normalize_email(email), "Informe o e-mail.")
        campos["nome"] = _exigir(normalizar_nome(campos.get("nome")), "Informe o nome.")
        campos["matricula"] = _exigir(campos.get("matricula"), "Informe a matrícula.")
        usuario = self.model(email=email, **campos)
        usuario.set_password(senha)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, password=None, **campos):
        for campo, (exigido, mensagem) in _EXIGENCIAS_DO_SUPERUSUARIO.items():
            campos.setdefault(campo, exigido)
            if campos[campo] != exigido:
                raise ValueError(mensagem)
        return self.create_user(email, password, **campos)


class Usuario(AbstractUser):
    username = None
    first_name = None
    last_name = None

    nome = models.CharField("nome", max_length=NOME_MAXIMO_CARACTERES)
    matricula = models.CharField(
        "matrícula",
        max_length=MATRICULA_MAXIMO_CARACTERES,
        unique=True,
        error_messages={"unique": MatriculaJaCadastrada.mensagem_padrao},
    )
    email = models.EmailField(
        "e-mail",
        unique=True,
        error_messages={"unique": MENSAGEM_EMAIL_REPETIDO},
    )
    perfil = models.CharField(
        "perfil",
        max_length=20,
        choices=PERFIL_CHOICES,
        default=PerfilUsuario.SOLICITANTE.value,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("nome", "matricula")

    objects = UsuarioManager()

    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"
        constraints = (
            models.UniqueConstraint(
                Lower("email"),
                name="contas_usuario_email_unico_sem_caixa",
                violation_error_message=MENSAGEM_EMAIL_REPETIDO,
            ),
        )

    def __str__(self):
        return f"{self.nome} ({self.matricula})"

    def clean(self):
        super().clean()
        self.nome = normalizar_nome(self.nome)
        self.matricula = self.matricula.strip()

    @property
    def eh_gestor(self) -> bool:
        return PerfilUsuario(self.perfil).eh_gestor

    def get_full_name(self):
        return self.nome

    def get_short_name(self):
        return self.nome
