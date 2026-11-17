from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from compartilhado.domain.erros import ErroDeDominio
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
    MudancaDeExemplo,
    ReservaDeExemplo,
    TentativaRecusadaDeExemplo,
    UsuarioDeExemplo,
)
from reservas.api.dependencias import (
    alterar_situacao_reserva,
    consultar_reservas,
    criar_reserva,
)
from reservas.application.repositorio import FiltrosDeReservas, Paginacao
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
        nome=exemplo.nome,
        tipo=exemplo.tipo,
        capacidade=exemplo.capacidade,
        abertura=exemplo.abertura,
        fechamento=exemplo.fechamento,
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
    ator_do_solicitante = Ator(
        usuario_id=solicitante.usuario_id,
        nome=solicitante.nome,
        papel=PapelDoAtor.SOLICITANTE,
    )
    for passo in exemplo.mudancas:
        momento = agora - timedelta(days=passo.ha_dias)
        if isinstance(passo, MudancaDeExemplo):
            _alterar_situacao(reserva.id, passo, momento, gestor)
        else:
            ator = ator_do_solicitante if passo.pelo_solicitante else gestor
            _tentar_e_ser_recusado(reserva.id, passo, momento, ator)


def _alterar_situacao(
    reserva_id: int, mudanca: MudancaDeExemplo, momento: datetime, ator: Ator
) -> None:
    alterar_situacao_reserva(relogio=_relogio_em(momento)).executar(
        reserva_id=reserva_id,
        nova_situacao=mudanca.situacao,
        motivo=mudanca.motivo,
        ator=ator,
    )


def _tentar_e_ser_recusado(
    reserva_id: int,
    tentativa: TentativaRecusadaDeExemplo,
    momento: datetime,
    ator: Ator,
) -> None:
    try:
        alterar_situacao_reserva(relogio=_relogio_em(momento)).executar(
            reserva_id=reserva_id,
            nova_situacao=tentativa.situacao,
            motivo=tentativa.motivo,
            ator=ator,
        )
    except ErroDeDominio:
        return
    raise RuntimeError(
        "A tentativa de exemplo deveria ser recusada, mas foi aceita: "
        f"{tentativa.situacao} na reserva {reserva_id}."
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
        consulta.executar(
            FiltrosDeReservas(solicitante_usuario_id=s.usuario_id),
            Paginacao(numero=1, tamanho=1),
            ator=gestor,
        ).total
        for s in solicitantes
    )


def _ids_dos_espacos() -> dict[str, int]:
    return {_chave(espaco.nome): espaco.id for espaco in listar_espacos().executar()}


def _chave(nome: str) -> str:
    return nome.casefold()
