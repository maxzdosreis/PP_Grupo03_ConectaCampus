from datetime import date

from django.db import IntegrityError, transaction
from django.db.models import Q, QuerySet

from reservas.application.repositorio import FiltrosDeReservas, RepositorioReservas
from reservas.domain.conflito_de_horario import garantir_horario_livre
from reservas.domain.excecoes import ReservaDesatualizada, ReservaNaoEncontrada
from reservas.domain.intervalo_de_horario import FUSO_HORARIO, IntervaloDeHorario
from reservas.domain.registro_de_situacao import RegistroDeSituacao
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import SITUACOES_QUE_OCUPAM_HORARIO, SituacaoReserva
from reservas.domain.solicitante import Solicitante
from reservas.infrastructure.models import (
    CONSTRAINT_SEM_SOBREPOSICAO,
    RegistroDeSituacaoModel,
    ReservaModel,
)


class RepositorioReservasDjango(RepositorioReservas):
    def salvar(self, reserva: Reserva) -> Reserva:
        try:
            with transaction.atomic():
                model = _obter_model_para_salvar(reserva)
                _exigir_situacao_de_origem(reserva, model)
                _aplicar_no_model(reserva, model)
                model.save()
                RegistroDeSituacaoModel.objects.bulk_create(
                    [
                        _registro_para_model(registro, model)
                        for registro in reserva.registros_pendentes
                    ]
                )
        except IntegrityError as erro:
            if CONSTRAINT_SEM_SOBREPOSICAO not in str(erro):
                raise
            self._lancar_conflito_de_horario(reserva)
            raise
        reserva.marcar_registros_como_gravados()
        return _para_entidade(model)

    def obter_por_id(self, reserva_id: int) -> Reserva | None:
        model = ReservaModel.objects.filter(pk=reserva_id).first()
        return _para_entidade(model) if model else None

    def listar(self, filtros: FiltrosDeReservas) -> list[Reserva]:
        consulta = ReservaModel.objects.order_by("inicio", "id")
        for filtrar in _FILTROS:
            consulta = filtrar(consulta, filtros)
        return [_para_entidade(model) for model in consulta]

    def listar_que_ocupam_horario(self, espaco_id: int, data: date) -> list[Reserva]:
        consulta = ReservaModel.objects.filter(
            espaco_id=espaco_id,
            inicio__date=data,
            situacao__in=SITUACOES_QUE_OCUPAM_HORARIO,
        ).order_by("inicio", "id")
        return [_para_entidade(model) for model in consulta]

    def listar_historico(self, reserva_id: int) -> list[RegistroDeSituacao]:
        consulta = RegistroDeSituacaoModel.objects.filter(
            reserva_id=reserva_id
        ).order_by("registrado_em", "id")
        return [_para_registro(model) for model in consulta]

    def _lancar_conflito_de_horario(self, reserva: Reserva) -> None:
        existentes = self.listar_que_ocupam_horario(
            reserva.espaco_id, reserva.intervalo.data
        )
        garantir_horario_livre(reserva, existentes)


def _filtrar_por_espaco(consulta: QuerySet, filtros: FiltrosDeReservas) -> QuerySet:
    if filtros.espaco_id is None:
        return consulta
    return consulta.filter(espaco_id=filtros.espaco_id)


def _filtrar_por_situacao(consulta: QuerySet, filtros: FiltrosDeReservas) -> QuerySet:
    if filtros.situacao is None:
        return consulta
    return consulta.filter(situacao=filtros.situacao)


def _filtrar_por_data(consulta: QuerySet, filtros: FiltrosDeReservas) -> QuerySet:
    if filtros.data is None:
        return consulta
    return consulta.filter(inicio__date=filtros.data)


def _filtrar_por_usuario(consulta: QuerySet, filtros: FiltrosDeReservas) -> QuerySet:
    if filtros.solicitante_usuario_id is None:
        return consulta
    return consulta.filter(solicitante_usuario_id=filtros.solicitante_usuario_id)


def _filtrar_por_solicitante(
    consulta: QuerySet, filtros: FiltrosDeReservas
) -> QuerySet:
    if filtros.solicitante is None:
        return consulta
    return consulta.filter(
        Q(solicitante_nome__icontains=filtros.solicitante)
        | Q(solicitante_matricula__icontains=filtros.solicitante)
    )


_FILTROS = (
    _filtrar_por_espaco,
    _filtrar_por_situacao,
    _filtrar_por_data,
    _filtrar_por_usuario,
    _filtrar_por_solicitante,
)


def _obter_model_para_salvar(reserva: Reserva) -> ReservaModel:
    if reserva.id is None:
        return ReservaModel()
    try:
        # O bloqueio da linha faz uma alteração simultânea esperar esta terminar
        # e, ao continuar, ler a situação já gravada (ver _exigir_situacao_de_origem).
        return ReservaModel.objects.select_for_update().get(pk=reserva.id)
    except ReservaModel.DoesNotExist:
        raise ReservaNaoEncontrada(reserva.id) from None


def _exigir_situacao_de_origem(reserva: Reserva, model: ReservaModel) -> None:
    # As transições não voltam a uma situação anterior, então a situação gravada
    # diferente da de origem só acontece se outra operação alterou a reserva.
    if model.pk is None:
        return
    if model.situacao != reserva.situacao_de_origem:
        raise ReservaDesatualizada(SituacaoReserva(model.situacao))


def _para_entidade(model: ReservaModel) -> Reserva:
    return Reserva(
        id=model.pk,
        espaco_id=model.espaco_id,
        solicitante=_para_solicitante(model),
        intervalo=_para_intervalo(model),
        finalidade=model.finalidade,
        situacao=model.situacao,
        motivo_da_situacao=model.motivo_da_situacao or None,
        criada_em=model.criada_em.astimezone(FUSO_HORARIO),
    )


def _para_solicitante(model: ReservaModel) -> Solicitante:
    return Solicitante(
        usuario_id=model.solicitante_usuario_id,
        nome=model.solicitante_nome,
        matricula=model.solicitante_matricula,
    )


def _para_intervalo(model: ReservaModel) -> IntervaloDeHorario:
    inicio = model.inicio.astimezone(FUSO_HORARIO)
    fim = model.fim.astimezone(FUSO_HORARIO)
    return IntervaloDeHorario(
        data=inicio.date(), hora_inicio=inicio.time(), hora_fim=fim.time()
    )


def _aplicar_no_model(entidade: Reserva, model: ReservaModel) -> None:
    model.espaco_id = entidade.espaco_id
    model.solicitante_usuario_id = entidade.solicitante.usuario_id
    model.solicitante_nome = entidade.solicitante.nome
    model.solicitante_matricula = entidade.solicitante.matricula
    model.inicio = entidade.intervalo.inicio()
    model.fim = entidade.intervalo.fim()
    model.finalidade = entidade.finalidade
    model.situacao = entidade.situacao.value
    model.motivo_da_situacao = entidade.motivo_da_situacao or ""
    model.criada_em = entidade.criada_em


def _para_registro(model: RegistroDeSituacaoModel) -> RegistroDeSituacao:
    return RegistroDeSituacao(
        situacao_anterior=SituacaoReserva(model.situacao_anterior)
        if model.situacao_anterior
        else None,
        situacao_nova=SituacaoReserva(model.situacao_nova),
        motivo=model.motivo or None,
        autor_usuario_id=model.autor_usuario_id,
        autor_nome=model.autor_nome,
        registrado_em=model.registrado_em.astimezone(FUSO_HORARIO),
    )


def _registro_para_model(
    registro: RegistroDeSituacao, reserva: ReservaModel
) -> RegistroDeSituacaoModel:
    anterior = registro.situacao_anterior
    return RegistroDeSituacaoModel(
        reserva=reserva,
        situacao_anterior=anterior.value if anterior else "",
        situacao_nova=registro.situacao_nova.value,
        motivo=registro.motivo or "",
        autor_usuario_id=registro.autor_usuario_id,
        autor_nome=registro.autor_nome,
        registrado_em=registro.registrado_em,
    )
