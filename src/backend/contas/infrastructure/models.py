from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    """Usuário do sistema (AUTH_USER_MODEL). Matrícula, nome e perfil entram na AUT-02."""

    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"
