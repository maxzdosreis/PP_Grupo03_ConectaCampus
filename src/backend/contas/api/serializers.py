from rest_framework import serializers

from contas.domain.perfil import PerfilUsuario


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True, trim_whitespace=False)


class CadastroSerializer(serializers.Serializer):
    nome = serializers.CharField(allow_blank=True)
    matricula = serializers.CharField(allow_blank=True)
    email = serializers.EmailField(max_length=254)
    senha = serializers.CharField(write_only=True, trim_whitespace=False)


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
