import os
import re
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from datetime import date, datetime, time
from time import tzset
from zoneinfo import ZoneInfo

from compartilhado.domain.erros import ConflitoDeEstado, RecursoNaoEncontrado
from reservas.application.portas import ConsultaDeEspacos, EspacoReservavel
from reservas.application.repositorio import FiltrosDeReservas, RepositorioReservas
from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.conflito_de_horario import garantir_horario_livre
from reservas.domain.excecoes import ReservaDesatualizada, ReservaNaoEncontrada
from reservas.domain.intervalo_de_horario import FUSO_HORARIO, IntervaloDeHorario
from reservas.domain.registro_de_situacao import RegistroDeSituacao
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import SITUACOES_QUE_EXIGEM_MOTIVO, SituacaoReserva
from reservas.domain.solicitante import Solicitante

UTC = ZoneInfo("UTC")
AGORA = datetime(2026, 10, 21, 12, 0, tzinfo=FUSO_HORARIO)
DIA = date(2026, 10, 25)
ID_INEXISTENTE = 9999
MOTIVO = "Chuva forte"
ANA = Solicitante(usuario_id=7, nome="Ana Souza", matricula="2026001")
BRUNO = Solicitante(usuario_id=8, nome="Bruno Lima", matricula="2026002")
GESTOR = Ator(usuario_id=1, nome="Gestora de Teste", papel=PapelDoAtor.GESTOR)
ATOR_ANA = Ator(usuario_id=ANA.usuario_id, nome=ANA.nome, papel=PapelDoAtor.SOLICITANTE)
OUTRA_PESSOA = Ator(usuario_id=99, nome="Outra Pessoa", papel=PapelDoAtor.SOLICITANTE)


def exatamente(texto: str) -> str:
    return f"^{re.escape(texto)}$"


@contextmanager
def fuso_do_processo(nome: str) -> Iterator[None]:
    anterior = os.environ.get("TZ")
    os.environ["TZ"] = nome
    tzset()
    try:
        yield
    finally:
        if anterior is None:
            del os.environ["TZ"]
        else:
            os.environ["TZ"] = anterior
        tzset()


def motivo_para(situacao: SituacaoReserva) -> str | None:
    return MOTIVO if situacao in SITUACOES_QUE_EXIGEM_MOTIVO else None


def intervalo(
    inicio: str = "10:00", fim: str = "11:00", data: date = DIA
) -> IntervaloDeHorario:
    return IntervaloDeHorario(
        data=data,
        hora_inicio=time.fromisoformat(inicio),
        hora_fim=time.fromisoformat(fim),
    )


def reserva_solicitada(**sobrescritas) -> Reserva:
    dados = {
        "espaco_id": 3,
        "solicitante": ANA,
        "data": DIA,
        "hora_inicio": time(10, 0),
        "hora_fim": time(11, 0),
        "finalidade": "Treino do time de vôlei",
        "agora": AGORA,
    }
    dados.update(sobrescritas)
    return Reserva.solicitar(**dados)


def reserva_reconstituida(**sobrescritas) -> Reserva:
    dados = {
        "id": 12,
        "espaco_id": 3,
        "solicitante": ANA,
        "intervalo": intervalo(),
        "finalidade": "Treino do time de vôlei",
        "situacao": SituacaoReserva.SOLICITADA,
        "criada_em": AGORA,
    }
    dados.update(sobrescritas)
    dados.setdefault("motivo_da_situacao", motivo_para(dados["situacao"]))
    return Reserva(**dados)


class ConsultaDeEspacosEmMemoria(ConsultaDeEspacos):
    def __init__(
        self,
        espacos: Iterable[EspacoReservavel] = (),
        *,
        ids_inativos: Iterable[int] = (),
    ) -> None:
        self._espacos = {espaco.id: espaco for espaco in espacos}
        self._ids_inativos = frozenset(ids_inativos)
        self.ids_consultados: list[int] = []

    def obter_espaco_reservavel(self, espaco_id: int) -> EspacoReservavel:
        self.ids_consultados.append(espaco_id)
        espaco = self._espacos.get(espaco_id)
        if espaco is None:
            raise RecursoNaoEncontrado(f"Espaço de código {espaco_id} não encontrado.")
        if espaco_id in self._ids_inativos:
            raise ConflitoDeEstado("Este espaço está inativo e não aceita reservas.")
        return espaco


class RepositorioReservasEmMemoria(RepositorioReservas):
    def __init__(self) -> None:
        self._reservas: dict[int, Reserva] = {}
        self._historico: dict[int, list[RegistroDeSituacao]] = {}
        self._proximo_id = 1
        self.chamadas_de_salvar = 0

    def salvar(self, reserva: Reserva) -> Reserva:
        self.chamadas_de_salvar += 1
        if reserva.id is not None and reserva.id not in self._reservas:
            raise ReservaNaoEncontrada(reserva.id)
        if reserva.id is not None:
            gravada = self._reservas[reserva.id].situacao
            if gravada is not reserva.situacao_de_origem:
                raise ReservaDesatualizada(gravada)
        if reserva.situacao.ocupa_horario:
            garantir_horario_livre(reserva, self._reservas.values())
        reserva_id = reserva.id if reserva.id is not None else self._gerar_id()
        self._reservas[reserva_id] = _copiar(reserva, reserva_id)
        self._historico.setdefault(reserva_id, []).extend(reserva.registros_pendentes)
        reserva.marcar_registros_como_gravados()
        return _copiar(reserva, reserva_id)

    def listar_historico(self, reserva_id: int) -> list[RegistroDeSituacao]:
        registros = self._historico.get(reserva_id, [])
        return sorted(registros, key=lambda registro: registro.registrado_em)

    def obter_por_id(self, reserva_id: int) -> Reserva | None:
        reserva = self._reservas.get(reserva_id)
        return _copiar(reserva, reserva_id) if reserva else None

    def listar(self, filtros: FiltrosDeReservas) -> list[Reserva]:
        return self._ordenadas(
            reserva
            for reserva in self._reservas.values()
            if _atende_aos_filtros(reserva, filtros)
        )

    def listar_que_ocupam_horario(self, espaco_id: int, data: date) -> list[Reserva]:
        return self._ordenadas(
            reserva
            for reserva in self._reservas.values()
            if reserva.espaco_id == espaco_id
            and reserva.intervalo.data == data
            and reserva.situacao.ocupa_horario
        )

    def _ordenadas(self, reservas: Iterable[Reserva]) -> list[Reserva]:
        encontradas = sorted(
            reservas, key=lambda reserva: (reserva.intervalo.inicio(), reserva.id)
        )
        return [_copiar(reserva, reserva.id) for reserva in encontradas]

    def _gerar_id(self) -> int:
        reserva_id = self._proximo_id
        self._proximo_id += 1
        return reserva_id


def _atende_aos_filtros(reserva: Reserva, filtros: FiltrosDeReservas) -> bool:
    return (
        filtros.espaco_id in (None, reserva.espaco_id)
        and filtros.situacao in (None, reserva.situacao)
        and filtros.data in (None, reserva.intervalo.data)
        and filtros.solicitante_usuario_id in (None, reserva.solicitante.usuario_id)
        and _solicitante_contem(reserva, filtros.solicitante)
    )


def _solicitante_contem(reserva: Reserva, trecho: str | None) -> bool:
    if trecho is None:
        return True
    trecho = trecho.casefold()
    return (
        trecho in reserva.solicitante.nome.casefold()
        or trecho in reserva.solicitante.matricula.casefold()
    )


def _copiar(reserva: Reserva, reserva_id: int | None) -> Reserva:
    return Reserva(
        id=reserva_id,
        espaco_id=reserva.espaco_id,
        solicitante=reserva.solicitante,
        intervalo=reserva.intervalo,
        finalidade=reserva.finalidade,
        situacao=reserva.situacao,
        motivo_da_situacao=reserva.motivo_da_situacao,
        criada_em=reserva.criada_em,
    )
