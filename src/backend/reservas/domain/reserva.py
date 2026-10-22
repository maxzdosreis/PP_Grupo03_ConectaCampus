from datetime import date, datetime, time

from compartilhado.domain.erros import CampoObrigatorioAusente
from reservas.domain.excecoes import (
    DataRetroativa,
    IdentificadorDeEspacoInvalido,
    MotivoObrigatorio,
    SituacaoInvalida,
    TransicaoDeSituacaoInvalida,
)
from reservas.domain.intervalo_de_horario import IntervaloDeHorario
from reservas.domain.situacao import (
    SITUACOES_QUE_EXIGEM_MOTIVO,
    SituacaoReserva,
    transicao_permitida,
)
from reservas.domain.solicitante import Solicitante
from reservas.domain.texto import exigir_tamanho_maximo, normalizar_espacos

FINALIDADE_MAXIMO_CARACTERES = 200
MOTIVO_MAXIMO_CARACTERES = 300


class Reserva:
    def __init__(
        self,
        *,
        espaco_id: int,
        solicitante: Solicitante,
        intervalo: IntervaloDeHorario,
        finalidade: str,
        situacao: SituacaoReserva | str,
        motivo_da_situacao: str | None = None,
        criada_em: datetime | None = None,
        id: int | None = None,
    ) -> None:
        self.id = id
        self.espaco_id = _validar_espaco_id(espaco_id)
        self.solicitante = _exigir(solicitante, "solicitante", "Solicitante")
        self.intervalo = _exigir(intervalo, "intervalo", "Horário")
        self.finalidade = _normalizar_finalidade(finalidade)
        self.situacao = _converter_situacao(situacao)
        self.motivo_da_situacao = _normalizar_motivo(motivo_da_situacao)
        self.criada_em = _validar_criada_em(criada_em)

    @classmethod
    def solicitar(
        cls,
        *,
        espaco_id: int,
        solicitante: Solicitante,
        data: date,
        hora_inicio: time,
        hora_fim: time,
        finalidade: str,
        agora: datetime,
    ) -> "Reserva":
        _exigir_fuso(agora, "agora")
        intervalo = IntervaloDeHorario(
            data=data, hora_inicio=hora_inicio, hora_fim=hora_fim
        )
        if intervalo.inicio() <= agora:
            raise DataRetroativa()
        return cls(
            espaco_id=espaco_id,
            solicitante=solicitante,
            intervalo=intervalo,
            finalidade=finalidade,
            situacao=SituacaoReserva.SOLICITADA,
            criada_em=agora,
        )

    def alterar_situacao(
        self, nova: SituacaoReserva | str, *, motivo: str | None = None
    ) -> None:
        nova = _converter_situacao(nova)
        if not transicao_permitida(self.situacao, nova):
            raise TransicaoDeSituacaoInvalida(self.situacao, nova)
        motivo_normalizado = _normalizar_motivo(motivo)
        if nova in SITUACOES_QUE_EXIGEM_MOTIVO and motivo_normalizado is None:
            raise MotivoObrigatorio()
        self.situacao = nova
        self.motivo_da_situacao = motivo_normalizado

    def __eq__(self, outra: object) -> bool:
        if not isinstance(outra, Reserva):
            return NotImplemented
        if self.id is None or outra.id is None:
            return self is outra
        return self.id == outra.id

    def __hash__(self) -> int:
        if self.id is None:
            return object.__hash__(self)
        return hash(self.id)

    def __repr__(self) -> str:
        return (
            f"Reserva(id={self.id!r}, espaco_id={self.espaco_id!r}, "
            f"solicitante={self.solicitante!r}, intervalo={self.intervalo!r}, "
            f"finalidade={self.finalidade!r}, situacao={self.situacao!r}, "
            f"motivo_da_situacao={self.motivo_da_situacao!r}, "
            f"criada_em={self.criada_em!r})"
        )

    def __str__(self) -> str:
        identificacao = f"#{self.id}" if self.id is not None else "nova"
        return f"Reserva {identificacao} — {self.intervalo} ({self.situacao.rotulo})"


def _exigir(valor, campo: str, rotulo: str):
    if valor is None:
        raise CampoObrigatorioAusente(campo, rotulo)
    return valor


def _validar_espaco_id(espaco_id: int | None) -> int:
    if espaco_id is None:
        raise CampoObrigatorioAusente("espaco_id", "Espaço")
    if isinstance(espaco_id, bool) or not isinstance(espaco_id, int):
        raise IdentificadorDeEspacoInvalido()
    if espaco_id < 1:
        raise IdentificadorDeEspacoInvalido()
    return espaco_id


def _normalizar_finalidade(finalidade: str | None) -> str:
    finalidade_normalizada = normalizar_espacos(finalidade)
    if not finalidade_normalizada:
        raise CampoObrigatorioAusente("finalidade", "Finalidade")
    return exigir_tamanho_maximo(
        finalidade_normalizada,
        campo="finalidade",
        rotulo="Finalidade",
        limite=FINALIDADE_MAXIMO_CARACTERES,
    )


def _normalizar_motivo(motivo: str | None) -> str | None:
    motivo_normalizado = normalizar_espacos(motivo)
    if not motivo_normalizado:
        return None
    return exigir_tamanho_maximo(
        motivo_normalizado,
        campo="motivo",
        rotulo="Motivo",
        limite=MOTIVO_MAXIMO_CARACTERES,
    )


def _converter_situacao(situacao: SituacaoReserva | str | None) -> SituacaoReserva:
    if not situacao:
        raise CampoObrigatorioAusente("situacao", "Situação")
    try:
        return SituacaoReserva(situacao)
    except ValueError:
        raise SituacaoInvalida() from None


def _validar_criada_em(criada_em: datetime | None) -> datetime | None:
    if criada_em is not None:
        _exigir_fuso(criada_em, "criada_em")
    return criada_em


def _exigir_fuso(momento: datetime, nome: str) -> None:
    if not isinstance(momento, datetime) or momento.utcoffset() is None:
        raise TypeError(f"{nome} deve ser um datetime com fuso horário.")
