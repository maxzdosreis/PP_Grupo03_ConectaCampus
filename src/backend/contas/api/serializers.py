from rest_framework import serializers

from contas.domain.perfil import PerfilUsuario


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
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

    def get_perfil_rotulo(self, usuario):
        return PerfilUsuario(usuario.perfil).rotulo
