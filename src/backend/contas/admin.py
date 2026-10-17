from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from contas.infrastructure.models import Usuario

CAMPOS_DE_ACESSO = ("perfil", "is_active", "is_staff", "is_superuser")


class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ("email", "nome", "matricula", "perfil")


class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ("email", "nome", "matricula", *CAMPOS_DE_ACESSO)


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    form = UsuarioChangeForm
    add_form = UsuarioCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Dados pessoais", {"fields": ("nome", "matricula")}),
        ("Acesso", {"fields": CAMPOS_DE_ACESSO}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "nome", "matricula", "password1", "password2"),
            },
        ),
        ("Acesso", {"fields": CAMPOS_DE_ACESSO}),
    )
    list_display = ("email", "nome", "matricula", "perfil", "is_active")
    list_filter = ("perfil", "is_active")
    search_fields = ("email", "nome", "matricula")
    ordering = ("nome",)
