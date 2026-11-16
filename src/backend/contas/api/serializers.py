from rest_framework import serializers

from compartilhado.api.paginacao import FiltrosDePaginaSerializer
from contas.application.portas import FiltrosDeUsuarios
from contas.domain.perfil import PerfilUsuario


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True, trim_whitespace=False)


class CadastroSerializer(serializers.Serializer):
    nome = serializers.CharField(allow_blank=True)
    matricula = serializers.CharField(allow_blank=True)
    email = serializers.EmailField(max_length=254)
    senha = serializers.CharField(write_only=True, trim_whitespace=False)


class AlteracaoDeSenhaSerializer(serializers.Serializer):
    senha_atual = serializers.CharField(
        write_only=True, trim_whitespace=False, allow_blank=True
    )
    nova_senha = serializers.CharField(
        write_only=True, trim_whitespace=False, allow_blank=True
    )
    refresh_atual = serializers.CharField(write_only=True, required=False)


class RenovacaoDeTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UsuarioSaidaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nome = serializers.CharField()
    email = serializers.EmailField()
    matricula = serializers.CharField()
    perfil = serializers.CharField()
    perfil_rotulo = serializers.SerializerMethodField()
    eh_gestor = serializers.SerializerMethodField()

    def get_perfil_rotulo(self, usuario):
        return PerfilUsuario(usuario.perfil).rotulo

    def get_eh_gestor(self, usuario):
        return PerfilUsuario(usuario.perfil).eh_gestor


class FiltrosDeUsuariosSerializer(FiltrosDePaginaSerializer):
    busca = serializers.CharField(required=False, allow_blank=True)
    perfil = serializers.ChoiceField(
        choices=[(perfil.value, perfil.rotulo) for perfil in PerfilUsuario],
        required=False,
        allow_blank=True,
    )
    ativo = serializers.ChoiceField(
        choices=["true", "false"], required=False, allow_blank=True
    )

    def para_filtros(self) -> FiltrosDeUsuarios:
        dados = self.validated_data
        return FiltrosDeUsuarios(
            busca=dados.get("busca") or None,
            perfil=PerfilUsuario(dados["perfil"]) if dados.get("perfil") else None,
            ativo={"true": True, "false": False}.get(dados.get("ativo")),
        )


class AlteracaoDeUsuarioSerializer(serializers.Serializer):
    perfil = serializers.CharField(required=False)
    ativo = serializers.BooleanField(required=False)


class UsuarioGerenciadoSaidaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nome = serializers.CharField()
    email = serializers.EmailField()
    matricula = serializers.CharField()
    perfil = serializers.CharField(source="perfil.value")
    perfil_rotulo = serializers.CharField(source="perfil.rotulo")
    eh_gestor = serializers.BooleanField(source="perfil.eh_gestor")
    ativo = serializers.BooleanField()
    cadastrado_em = serializers.DateTimeField()
    ultimo_acesso = serializers.DateTimeField(allow_null=True)
