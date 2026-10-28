from datetime import date, datetime, time

from compartilhado.domain.erros import CampoObrigatorioAusente
from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.excecoes import (
    AlteracaoDeSituacaoNaoPermitida,
    DataRetroativa,
    IdentificadorDeEspacoInvalido,
    MotivoObrigatorio,
    ReservaNaoEncontrada,
    SituacaoInvalida,
    TransicaoDeSituacaoInvalida,
)
from reservas.domain.intervalo_de_horario import IntervaloDeHorario
from reservas.domain.momento import exigir_fuso
from reservas.domain.registro_de_situacao import RegistroDeSituacao
from reservas.domain.situacao import (
    DESTINOS_DE_TRANSICAO,
    SITUACOES_QUE_EXIGEM_MOTIVO,
    SituacaoReserva,
    papel_pode_levar_a,
    transicao_permitida,
    transicoes_a_partir_de,
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
        criada_em: datetime,
        motivo_da_situacao: str | None = None,
        id: int | None = None,
    ) -> None:
        self.id = id
        self.espaco_id = _validar_espaco_id(espaco_id)
        self.solicitante = _exigir(solicitante, "solicitante", "Solicitante")
        self.intervalo = _exigir(intervalo, "intervalo", "Horário")
        self.finalidade = _normalizar_finalidade(finalidade)
        self.situacao = _converter_situacao(situacao)
        self.motivo_da_situacao = _normalizar_motivo(motivo_da_situacao)
        _exigir_motivo_se_necessario(self.situacao, self.motivo_da_situacao)
        exigir_fuso(criada_em, "criada_em")
        self.criada_em = criada_em
        self._registros_pendentes: list[RegistroDeSituacao] = []

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
        exigir_fuso(agora, "agora")
        intervalo = IntervaloDeHorario(
            data=data, hora_inicio=hora_inicio, hora_fim=hora_fim
        )
        if intervalo.inicio() <= agora:
            raise DataRetroativa()
        reserva = cls(
            espaco_id=espaco_id,
            solicitante=solicitante,
            intervalo=intervalo,
            finalidade=finalidade,
            situacao=SituacaoReserva.SOLICITADA,
            criada_em=agora,
        )
        reserva._registros_pendentes.append(
            RegistroDeSituacao(
                situacao_anterior=None,
                situacao_nova=SituacaoReserva.SOLICITADA,
                motivo=None,
                autor_usuario_id=solicitante.usuario_id,
                autor_nome=solicitante.nome,
                registrado_em=agora,
            )
        )
        return reserva

    @property
    def registros_pendentes(self) -> tuple[RegistroDeSituacao, ...]:
        return tuple(self._registros_pendentes)

    def marcar_registros_como_gravados(self) -> None:
        self._registros_pendentes.clear()

    def visivel_para(self, ator: Ator) -> bool:
        if ator.papel is PapelDoAtor.GESTOR:
            return True
        return self.solicitante.usuario_id == ator.usuario_id

    def acoes_permitidas_para(self, ator: Ator) -> list[SituacaoReserva]:
        if not self.visivel_para(ator):
            return []
        return [
            nova
            for nova in transicoes_a_partir_de(self.situacao)
            if papel_pode_levar_a(ator.papel, nova)
        ]

    def alterar_situacao(
        self,
        nova: SituacaoReserva | str,
        *,
        motivo: str | None = None,
        ator: Ator,
        agora: datetime,
    ) -> None:
        exigir_fuso(agora, "agora")
        if not self.visivel_para(ator):
            raise ReservaNaoEncontrada(self.id)
        nova = _converter_situacao(nova)
        _exigir_permissao(ator.papel, nova)
        if not transicao_permitida(self.situacao, nova):
            raise TransicaoDeSituacaoInvalida(self.situacao, nova)
        motivo_normalizado = _normalizar_motivo(motivo)
        _exigir_motivo_se_necessario(nova, motivo_normalizado)
        registro = RegistroDeSituacao(
            situacao_anterior=self.situacao,
            situacao_nova=nova,
            motivo=motivo_normalizado,
            autor_usuario_id=ator.usuario_id,
            autor_nome=ator.nome,
            registrado_em=agora,
        )
        self.situacao = nova
        self.motivo_da_situacao = motivo_normalizado
        self._registros_pendentes.append(registro)

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


def _exigir_motivo_se_necessario(situacao: SituacaoReserva, motivo: str | None) -> None:
    if situacao in SITUACOES_QUE_EXIGEM_MOTIVO and motivo is None:
        raise MotivoObrigatorio()


def _exigir_permissao(papel: PapelDoAtor, nova: SituacaoReserva) -> None:
    if nova in DESTINOS_DE_TRANSICAO and not papel_pode_levar_a(papel, nova):
        raise AlteracaoDeSituacaoNaoPermitida(nova)


def _converter_situacao(situacao: SituacaoReserva | str | None) -> SituacaoReserva:
    if not situacao:
        raise CampoObrigatorioAusente("situacao", "Situação")
    try:
        return SituacaoReserva(situacao)
    except ValueError:
        raise SituacaoInvalida() from None
