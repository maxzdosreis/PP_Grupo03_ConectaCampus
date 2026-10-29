from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from contas.api.dependencias import cadastrar_solicitante
from contas.domain.cadastro import DadosDeCadastro
from contas.domain.perfil import PerfilUsuario
from contas.infrastructure.models import Usuario
from contas.infrastructure.politica_de_senha import PoliticaDeSenhaDjango
from contas.infrastructure.repositorio_django import RepositorioUsuariosDjango
from espacos.api.dependencias import (
    cadastrar_espaco,
    desativar_espaco,
    listar_espacos,
)
from exemplos.dados import (
    ESPACOS,
    GESTOR,
    RESERVAS,
    SOLICITANTES,
    USUARIOS,
    EspacoDeExemplo,
    ReservaDeExemplo,
    UsuarioDeExemplo,
)
from reservas.api.dependencias import (
    alterar_situacao_reserva,
    consultar_reservas,
    criar_reserva,
)
from reservas.application.repositorio import FiltrosDeReservas
from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.solicitante import Solicitante


@dataclass(frozen=True)
class ResultadoDaEtapa:
    criados: int
    existentes: int


def garantir_usuarios() -> ResultadoDaEtapa:
    repositorio = RepositorioUsuariosDjango()
    novos = [u for u in USUARIOS if not repositorio.existe_email(u.email)]
    for usuario in novos:
        _CRIAR_POR_PERFIL[usuario.perfil](usuario)
    return ResultadoDaEtapa(criados=len(novos), existentes=len(USUARIOS) - len(novos))


def garantir_espacos() -> ResultadoDaEtapa:
    cadastrados = {_chave(espaco.nome) for espaco in listar_espacos().executar()}
    novos = [espaco for espaco in ESPACOS if _chave(espaco.nome) not in cadastrados]
    for espaco in novos:
        _criar_espaco(espaco)
    return ResultadoDaEtapa(criados=len(novos), existentes=len(ESPACOS) - len(novos))


def garantir_reservas(hoje: date, agora: datetime) -> ResultadoDaEtapa:
    gestor = _ator_do_gestor()
    solicitantes = _solicitantes_de_exemplo()
    ja_existentes = _contar_reservas_de(solicitantes.values(), gestor)
    if ja_existentes:
        return ResultadoDaEtapa(criados=0, existentes=ja_existentes)
    ids_dos_espacos = _ids_dos_espacos()
    for exemplo in RESERVAS:
        _criar_reserva(
            exemplo,
            solicitante=solicitantes[exemplo.solicitante_email],
            espaco_id=ids_dos_espacos[_chave(exemplo.espaco)],
            data=hoje + timedelta(days=exemplo.dias_a_partir_de_hoje),
            agora=agora,
            gestor=gestor,
        )
    return ResultadoDaEtapa(criados=len(RESERVAS), existentes=0)


def _criar_gestor(usuario: UsuarioDeExemplo) -> None:
    dados = DadosDeCadastro(
        nome=usuario.nome, matricula=usuario.matricula, email=usuario.email
    )
    PoliticaDeSenhaDjango().validar(usuario.senha, dados)
    Usuario.objects.create_superuser(
        dados.email, usuario.senha, nome=dados.nome, matricula=dados.matricula
    )


def _criar_solicitante(usuario: UsuarioDeExemplo) -> None:
    cadastrar_solicitante().executar(
        nome=usuario.nome,
        matricula=usuario.matricula,
        email=usuario.email,
        senha=usuario.senha,
    )


_CRIAR_POR_PERFIL = {
    PerfilUsuario.GESTOR: _criar_gestor,
    PerfilUsuario.SOLICITANTE: _criar_solicitante,
}


def _criar_espaco(exemplo: EspacoDeExemplo) -> None:
    espaco = cadastrar_espaco().executar(
        nome=exemplo.nome, tipo=exemplo.tipo, capacidade=exemplo.capacidade
    )
    if not exemplo.ativo:
        desativar_espaco().executar(espaco.id)


def _criar_reserva(
    exemplo: ReservaDeExemplo,
    *,
    solicitante: Solicitante,
    espaco_id: int,
    data: date,
    agora: datetime,
    gestor: Ator,
) -> None:
    solicitada_em = agora - timedelta(days=exemplo.solicitada_ha_dias)
    reserva = criar_reserva(relogio=_relogio_em(solicitada_em)).executar(
        espaco_id=espaco_id,
        solicitante=solicitante,
        data=data,
        hora_inicio=exemplo.hora_inicio,
        hora_fim=exemplo.hora_fim,
        finalidade=exemplo.finalidade,
    )
    for mudanca in exemplo.mudancas:
        alterada_em = agora - timedelta(days=mudanca.ha_dias)
        alterar_situacao_reserva(relogio=_relogio_em(alterada_em)).executar(
            reserva_id=reserva.id,
            nova_situacao=mudanca.situacao,
            motivo=mudanca.motivo,
            ator=gestor,
        )


def _relogio_em(momento: datetime) -> Callable[[], datetime]:
    return lambda: momento


def _solicitantes_de_exemplo() -> dict[str, Solicitante]:
    return {exemplo.email: _solicitante_de(exemplo.email) for exemplo in SOLICITANTES}


def _solicitante_de(email: str) -> Solicitante:
    usuario = Usuario.objects.get_by_natural_key(email)
    return Solicitante(
        usuario_id=usuario.pk, nome=usuario.nome, matricula=usuario.matricula
    )


def _ator_do_gestor() -> Ator:
    usuario = Usuario.objects.get_by_natural_key(GESTOR.email)
    return Ator(usuario_id=usuario.pk, nome=usuario.nome, papel=PapelDoAtor.GESTOR)


def _contar_reservas_de(solicitantes: Iterable[Solicitante], gestor: Ator) -> int:
    consulta = consultar_reservas()
    return sum(
        len(
            consulta.executar(
                FiltrosDeReservas(solicitante_usuario_id=s.usuario_id), ator=gestor
            )
        )
        for s in solicitantes
    )


def _ids_dos_espacos() -> dict[str, int]:
    return {_chave(espaco.nome): espaco.id for espaco in listar_espacos().executar()}


def _chave(nome: str) -> str:
    return nome.casefold()
