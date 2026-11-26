import os
import re
from collections import Counter
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from datetime import date, datetime, time
from time import tzset
from zoneinfo import ZoneInfo

from compartilhado.domain.erros import ConflitoDeEstado, RecursoNaoEncontrado
from reservas.application.ocupacao_do_dia import HorarioOcupado
from reservas.application.portas import (
    AgendaDoDia,
    AgendaIndisponivel,
    ConsultaDeEspacos,
    EspacoReservavel,
    IndiceDeReservas,
    IndiceIndisponivel,
    RankingDeEspacos,
    RankingIndisponivel,
    RegistroDoIndice,
    RegistroDoRanking,
    validar_janela,
)
from reservas.application.repositorio import (
    TAMANHO_MAXIMO_DA_PAGINA,
    FiltrosDeReservas,
    Paginacao,
    PaginaDeReservas,
    RepositorioReservas,
)
from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.conflito_de_horario import garantir_horario_livre
from reservas.domain.excecoes import ReservaDesatualizada, ReservaNaoEncontrada
from reservas.domain.funcionamento import FuncionamentoDoEspaco
from reservas.domain.intervalo_de_horario import FUSO_HORARIO, IntervaloDeHorario
from reservas.domain.registro_de_situacao import RegistroDeSituacao
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import SITUACOES_QUE_EXIGEM_MOTIVO, SituacaoReserva
from reservas.domain.solicitante import Solicitante

UTC = ZoneInfo("UTC")
FUNCIONAMENTO_PADRAO = FuncionamentoDoEspaco(
    abertura_em_minutos=7 * 60, fechamento_em_minutos=24 * 60
)
AGORA = datetime(2026, 10, 21, 12, 0, tzinfo=FUSO_HORARIO)
DIA = date(2026, 10, 25)
DEPOIS_DO_TERMINO = datetime(2026, 10, 25, 12, 0, tzinfo=FUSO_HORARIO)
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


def relogio_em(momento: datetime) -> Callable[[], datetime]:
    return lambda: momento


def momento_para(nova: SituacaoReserva) -> datetime:
    return DEPOIS_DO_TERMINO if nova is SituacaoReserva.CONCLUIDA else AGORA


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
        "funcionamento": FUNCIONAMENTO_PADRAO,
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


def funcionamento(abertura: str = "07:00", fechamento: str = "00:00"):
    """Funcionamento a partir de "HH:MM"; "00:00" no fechamento é o fim do dia."""
    return FuncionamentoDoEspaco(
        abertura_em_minutos=_minutos(abertura),
        fechamento_em_minutos=_minutos(fechamento) or 24 * 60,
    )


def _minutos(horario: str) -> int:
    hora = time.fromisoformat(horario)
    return hora.hour * 60 + hora.minute


def espaco_reservavel(
    id: int, nome: str, funcionamento_do_espaco: FuncionamentoDoEspaco | None = None
) -> EspacoReservavel:
    return EspacoReservavel(
        id=id, nome=nome, funcionamento=funcionamento_do_espaco or FUNCIONAMENTO_PADRAO
    )


class ConsultaDeEspacosEmMemoria(ConsultaDeEspacos):
    def __init__(
        self,
        espacos: Iterable[EspacoReservavel] = (),
        *,
        ids_inativos: Iterable[int] = (),
        eventos: list[str] | None = None,
    ) -> None:
        self._espacos = {espaco.id: espaco for espaco in espacos}
        self._ids_inativos = frozenset(ids_inativos)
        self.ids_consultados: list[int] = []
        self.eventos = eventos if eventos is not None else []

    def obter_espaco_reservavel(self, espaco_id: int) -> EspacoReservavel:
        self.ids_consultados.append(espaco_id)
        espaco = self._espacos.get(espaco_id)
        if espaco is None:
            raise RecursoNaoEncontrado(f"Espaço de código {espaco_id} não encontrado.")
        if espaco_id in self._ids_inativos:
            raise ConflitoDeEstado("Este espaço está inativo e não aceita reservas.")
        return espaco

    def obter_espaco_reservavel_travado(self, espaco_id: int) -> EspacoReservavel:
        self.eventos.append("travar")
        return self.obter_espaco_reservavel(espaco_id)

    def nomes_dos_espacos(self, ids: Iterable[int]) -> Mapping[int, str]:
        self.ids_com_nome_consultados = list(ids)
        return {
            espaco_id: self._espacos[espaco_id].nome
            for espaco_id in self.ids_com_nome_consultados
            if espaco_id in self._espacos
        }


class AgendaDoDiaEmMemoria(AgendaDoDia):
    def __init__(self, *, indisponivel: bool = False) -> None:
        self.indisponivel = indisponivel
        self._dias: dict[tuple[int, date], dict[int, HorarioOcupado]] = {}
        self._versoes: dict[tuple[int, date], int] = {}

    def registrar(
        self,
        espaco_id: int,
        reserva_id: int,
        intervalo: IntervaloDeHorario,
        situacao: SituacaoReserva,
    ) -> None:
        if not situacao.ocupa_horario:
            raise ValueError(f"A situação {situacao.value} não ocupa horário.")
        self._exigir_disponivel()
        self._avancar_versao(espaco_id, intervalo.data)
        dia = self._dias.get((espaco_id, intervalo.data))
        if dia is not None:
            dia[reserva_id] = HorarioOcupado(intervalo=intervalo, situacao=situacao)

    def remover(self, espaco_id: int, reserva_id: int, data: date) -> None:
        self._exigir_disponivel()
        self._avancar_versao(espaco_id, data)
        dia = self._dias.get((espaco_id, data))
        if dia is not None:
            dia.pop(reserva_id, None)

    def listar(self, espaco_id: int, data: date) -> tuple[HorarioOcupado, ...] | None:
        self._exigir_disponivel()
        dia = self._dias.get((espaco_id, data))
        if dia is None:
            return None
        ordenados = sorted(dia.items(), key=lambda item: _ordem_no_redis(*item))
        return tuple(ocupado for _, ocupado in ordenados)

    def dias_projetados(self, a_partir_de: date) -> frozenset[tuple[int, date]]:
        self._exigir_disponivel()
        return frozenset(chave for chave in self._dias if chave[1] >= a_partir_de)

    def versao(self, espaco_id: int, data: date) -> int:
        self._exigir_disponivel()
        return self._versoes.get((espaco_id, data), 0)

    def substituir(
        self,
        espaco_id: int,
        data: date,
        ocupados: Mapping[int, HorarioOcupado],
        *,
        versao: int,
    ) -> bool:
        self._exigir_disponivel()
        if self._versoes.get((espaco_id, data), 0) != versao:
            return False
        self._dias[(espaco_id, data)] = dict(ocupados)
        return True

    def _avancar_versao(self, espaco_id: int, data: date) -> None:
        chave = (espaco_id, data)
        self._versoes[chave] = self._versoes.get(chave, 0) + 1

    def _exigir_disponivel(self) -> None:
        if self.indisponivel:
            raise AgendaIndisponivel


def _ordem_no_redis(reserva_id: int, ocupado: HorarioOcupado) -> tuple[int, str]:
    """Score (início em minutos) e, no empate, o membro, como o Sorted Set."""
    horario = ocupado.intervalo
    fim = (
        24 * 60
        if horario.termina_a_meia_noite()
        else _minutos(f"{horario.hora_fim:%H:%M}")
    )
    inicio = _minutos(f"{horario.hora_inicio:%H:%M}")
    return inicio, f"{reserva_id}:{fim}:{ocupado.situacao.value}"


class IndiceDeReservasEmMemoria(IndiceDeReservas):
    def __init__(self, *, indisponivel: bool = False) -> None:
        self.indisponivel = indisponivel
        self._montado = False
        self._versao = 0
        self._situacoes: dict[int, SituacaoReserva] = {}
        self._criadas_em: dict[int, datetime] = {}

    def aplicar(
        self, reserva_id: int, situacao: SituacaoReserva, criada_em: datetime
    ) -> None:
        self._exigir_disponivel()
        self._versao += 1
        if self._montado:
            self._situacoes[reserva_id] = situacao
            self._criadas_em[reserva_id] = criada_em

    def pendentes(self, limite: int, deslocamento: int = 0) -> tuple[int, ...] | None:
        validar_janela(limite, deslocamento)
        self._exigir_disponivel()
        if not self._montado:
            return None
        fila = sorted(
            (
                reserva_id
                for reserva_id, situacao in self._situacoes.items()
                if situacao is SituacaoReserva.SOLICITADA
            ),
            key=lambda reserva_id: (
                self._criadas_em[reserva_id].timestamp(),
                reserva_id,
            ),
        )
        return tuple(fila[deslocamento : deslocamento + limite])

    def contagem_por_situacao(self) -> dict[SituacaoReserva, int] | None:
        self._exigir_disponivel()
        if not self._montado:
            return None
        situacoes = list(self._situacoes.values())
        return {situacao: situacoes.count(situacao) for situacao in SituacaoReserva}

    def versao(self) -> int:
        self._exigir_disponivel()
        return self._versao

    def substituir(self, registros: Iterable[RegistroDoIndice], *, versao: int) -> bool:
        self._exigir_disponivel()
        materializados = list(registros)
        if self._versao != versao:
            return False
        self._situacoes = {r.reserva_id: r.situacao for r in materializados}
        self._criadas_em = {r.reserva_id: r.criada_em for r in materializados}
        self._montado = True
        return True

    def _exigir_disponivel(self) -> None:
        if self.indisponivel:
            raise IndiceIndisponivel


class RankingDeEspacosEmMemoria(RankingDeEspacos):
    def __init__(self, *, indisponivel: bool = False) -> None:
        self.indisponivel = indisponivel
        self._montado = False
        self._versao = 0
        self._livro: dict[int, int] = {}

    def aplicar(
        self, reserva_id: int, espaco_id: int, situacao: SituacaoReserva
    ) -> None:
        self._exigir_disponivel()
        self._versao += 1
        if not self._montado:
            return
        if situacao.conta_no_ranking:
            self._livro.setdefault(reserva_id, espaco_id)
        else:
            self._livro.pop(reserva_id, None)

    def top(self, limite: int) -> tuple[tuple[int, int], ...] | None:
        validar_janela(limite, 0)
        self._exigir_disponivel()
        if not self._montado:
            return None
        totais = Counter(self._livro.values())
        ordem = sorted(totais.items(), key=lambda par: (-par[1], par[0]))
        return tuple(ordem[:limite])

    def versao(self) -> int:
        self._exigir_disponivel()
        return self._versao

    def substituir(
        self, registros: Iterable[RegistroDoRanking], *, versao: int
    ) -> bool:
        self._exigir_disponivel()
        materializados = list(registros)
        if self._versao != versao:
            return False
        self._livro = {
            r.reserva_id: r.espaco_id
            for r in materializados
            if r.situacao.conta_no_ranking
        }
        self._montado = True
        return True

    def _exigir_disponivel(self) -> None:
        if self.indisponivel:
            raise RankingIndisponivel


class RepositorioReservasEmMemoria(RepositorioReservas):
    def __init__(self, eventos: list[str] | None = None) -> None:
        self.eventos = eventos if eventos is not None else []
        self.transacoes_abertas = 0
        self._reservas: dict[int, Reserva] = {}
        self._historico: dict[int, list[RegistroDeSituacao]] = {}
        self._proximo_id = 1
        self.chamadas_de_salvar = 0
        self.tentativas_registradas = 0
        self.chamadas_de_listar_pendentes = 0
        self.chamadas_de_listar_por_ids = 0
        self.chamadas_de_contar_por_situacao = 0
        self.chamadas_de_contar_por_espaco = 0

    @contextmanager
    def em_transacao(self) -> Iterator[None]:
        self.eventos.append("abrir")
        self.transacoes_abertas += 1
        try:
            yield
        finally:
            self.transacoes_abertas -= 1
            self.eventos.append("fechar")

    def salvar(self, reserva: Reserva) -> Reserva:
        self.chamadas_de_salvar += 1
        self.eventos.append("salvar")
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

    def gravar_tentativa_recusada(
        self, reserva_id: int, registro: RegistroDeSituacao
    ) -> None:
        if reserva_id not in self._reservas:
            raise ReservaNaoEncontrada(reserva_id)
        self.tentativas_registradas += 1
        self._historico.setdefault(reserva_id, []).append(registro)

    def listar_historico(self, reserva_id: int) -> list[RegistroDeSituacao]:
        registros = self._historico.get(reserva_id, [])
        return sorted(registros, key=lambda registro: registro.registrado_em)

    def obter_por_id(self, reserva_id: int) -> Reserva | None:
        reserva = self._reservas.get(reserva_id)
        return _copiar(reserva, reserva_id) if reserva else None

    def listar(
        self, filtros: FiltrosDeReservas, paginacao: Paginacao
    ) -> PaginaDeReservas:
        encontradas = self._ordenadas(
            reserva
            for reserva in self._reservas.values()
            if _atende_aos_filtros(reserva, filtros)
        )
        inicio = paginacao.deslocamento()
        return PaginaDeReservas(
            itens=tuple(encontradas[inicio : inicio + paginacao.tamanho]),
            total=len(encontradas),
            paginacao=paginacao,
        )

    def listar_pendentes(self, paginacao: Paginacao) -> PaginaDeReservas:
        self.chamadas_de_listar_pendentes += 1
        fila = sorted(
            (
                r
                for r in self._reservas.values()
                if r.situacao is SituacaoReserva.SOLICITADA
            ),
            key=lambda reserva: (reserva.criada_em, reserva.id),
        )
        inicio = paginacao.deslocamento()
        return PaginaDeReservas(
            itens=tuple(
                _copiar(r, r.id) for r in fila[inicio : inicio + paginacao.tamanho]
            ),
            total=len(fila),
            paginacao=paginacao,
        )

    def listar_por_ids(self, ids: Sequence[int]) -> list[Reserva]:
        self.chamadas_de_listar_por_ids += 1
        return [
            _copiar(self._reservas[reserva_id], reserva_id)
            for reserva_id in dict.fromkeys(ids)
            if reserva_id in self._reservas
        ]

    def contar_por_situacao(self) -> dict[SituacaoReserva, int]:
        self.chamadas_de_contar_por_situacao += 1
        situacoes = [reserva.situacao for reserva in self._reservas.values()]
        return {situacao: situacoes.count(situacao) for situacao in SituacaoReserva}

    def listar_que_ocupam_horario(self, espaco_id: int, data: date) -> list[Reserva]:
        self.eventos.append("listar")
        return self._ordenadas(
            reserva
            for reserva in self._reservas.values()
            if reserva.espaco_id == espaco_id
            and reserva.intervalo.data == data
            and reserva.situacao.ocupa_horario
        )

    def listar_dias_com_reservas_que_ocupam_horario(
        self, a_partir_de: date
    ) -> list[tuple[int, date]]:
        return sorted(
            {
                (reserva.espaco_id, reserva.intervalo.data)
                for reserva in self._reservas.values()
                if reserva.situacao.ocupa_horario
                and reserva.intervalo.data >= a_partir_de
            }
        )

    def listar_ativas_a_partir_de(
        self, espaco_id: int, momento: datetime
    ) -> list[Reserva]:
        return self._ordenadas(
            reserva
            for reserva in self._reservas.values()
            if reserva.espaco_id == espaco_id
            and reserva.situacao.ocupa_horario
            and reserva.intervalo.fim() > momento
        )

    def listar_para_indice(
        self, depois_de_id: int, limite: int
    ) -> list[RegistroDoIndice]:
        ids = sorted(i for i in self._reservas if i > depois_de_id)[:limite]
        return [
            RegistroDoIndice(i, self._reservas[i].situacao, self._reservas[i].criada_em)
            for i in ids
        ]

    def contar_por_espaco_que_contam_no_ranking(
        self, limite: int
    ) -> tuple[tuple[int, int], ...]:
        validar_janela(limite, 0)
        self.chamadas_de_contar_por_espaco += 1
        totais = Counter(
            reserva.espaco_id
            for reserva in self._reservas.values()
            if reserva.situacao.conta_no_ranking
        )
        ordem = sorted(totais.items(), key=lambda par: (-par[1], par[0]))
        return tuple(ordem[:limite])

    def listar_para_ranking(
        self, depois_de_id: int, limite: int
    ) -> list[RegistroDoRanking]:
        ids = sorted(i for i in self._reservas if i > depois_de_id)[:limite]
        return [
            RegistroDoRanking(
                i, self._reservas[i].espaco_id, self._reservas[i].situacao
            )
            for i in ids
        ]

    def _ordenadas(self, reservas: Iterable[Reserva]) -> list[Reserva]:
        encontradas = sorted(
            reservas, key=lambda reserva: (reserva.intervalo.inicio(), reserva.id)
        )
        return [_copiar(reserva, reserva.id) for reserva in encontradas]

    def _gerar_id(self) -> int:
        reserva_id = self._proximo_id
        self._proximo_id += 1
        return reserva_id


def todas_as_reservas(
    repositorio: RepositorioReservas, filtros: FiltrosDeReservas | None = None
) -> list[Reserva]:
    filtros = filtros or FiltrosDeReservas()
    reservas: list[Reserva] = []
    numero = 1
    while True:
        pagina = repositorio.listar(
            filtros, Paginacao(numero=numero, tamanho=TAMANHO_MAXIMO_DA_PAGINA)
        )
        reservas.extend(pagina.itens)
        if numero >= pagina.total_de_paginas():
            return reservas
        numero += 1


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
