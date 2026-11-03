from copy import deepcopy
from datetime import timedelta

from hypothesis import settings
from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, initialize, invariant, rule

from compartilhado.domain.erros import (
    CampoObrigatorioAusente,
    ErroDeDominio,
    TextoMuitoLongo,
)
from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.excecoes import (
    AlteracaoDeSituacaoNaoPermitida,
    MotivoObrigatorio,
    ReservaNaoEncontrada,
    SituacaoInvalida,
    TransicaoDeSituacaoInvalida,
)
from reservas.domain.reserva import MOTIVO_MAXIMO_CARACTERES
from reservas.domain.situacao import (
    SITUACOES_QUE_EXIGEM_MOTIVO,
    TRANSICOES_PERMITIDAS,
    SituacaoReserva,
)
from reservas.tests.fakes import (
    AGORA,
    ANA,
    ATOR_ANA,
    BRUNO,
    GESTOR,
    MOTIVO,
    reserva_solicitada,
)
from reservas.tests.historico import verificar_historico_coerente

S = SituacaoReserva
OUTRO = Ator(
    usuario_id=BRUNO.usuario_id, nome=BRUNO.nome, papel=PapelDoAtor.SOLICITANTE
)
ATORES = {"gestor": GESTOR, "dono": ATOR_ANA, "outro": OUTRO}

_DESTINOS = [*SituacaoReserva, "INVALIDA", ""]
_MOTIVOS = [
    None,
    "",
    "   ",
    MOTIVO,
    "  Chuva   forte ",
    "A" * (MOTIVO_MAXIMO_CARACTERES + 1),
]
_RECUSAS_ESPERADAS = (
    ReservaNaoEncontrada,
    CampoObrigatorioAusente,
    SituacaoInvalida,
    AlteracaoDeSituacaoNaoPermitida,
    TransicaoDeSituacaoInvalida,
    MotivoObrigatorio,
    TextoMuitoLongo,
)


def _retrato(reserva):
    return reserva.situacao, reserva.motivo_da_situacao, reserva.registros_pendentes


def _aceita(reserva, destino, ator, agora):
    copia = deepcopy(reserva)
    try:
        copia.alterar_situacao(destino, motivo=MOTIVO, ator=ator, agora=agora)
    except ErroDeDominio:
        return False
    return True


class MaquinaDaReserva(RuleBasedStateMachine):
    @initialize()
    def solicitar(self):
        self.agora = AGORA
        self.reserva = reserva_solicitada(agora=self.agora)
        self.retrato_final = None

    @rule(
        ator=st.sampled_from(sorted(ATORES)),
        destino=st.sampled_from(_DESTINOS),
        motivo=st.sampled_from(_MOTIVOS),
        minutos_depois=st.integers(min_value=1, max_value=24 * 60),
    )
    def tentar_alterar(self, ator, destino, motivo, minutos_depois):
        self.agora += timedelta(minutes=minutos_depois)
        antes = _retrato(self.reserva)

        try:
            self.reserva.alterar_situacao(
                destino, motivo=motivo, ator=ATORES[ator], agora=self.agora
            )
        except _RECUSAS_ESPERADAS:
            assert _retrato(self.reserva) == antes
            return

        ultimo = self.reserva.registros_pendentes[-1]
        assert self.reserva.situacao == destino
        assert (ultimo.autor_usuario_id, ultimo.registrado_em) == (
            ATORES[ator].usuario_id,
            self.agora,
        )

    @invariant()
    def historico_e_um_caminho_da_tabela_ate_a_situacao_atual(self):
        registros = self.reserva.registros_pendentes
        verificar_historico_coerente(registros, self.reserva.situacao)
        for registro in registros[1:]:
            assert (
                registro.situacao_nova
                in TRANSICOES_PERMITIDAS[registro.situacao_anterior]
            )
        momentos = [registro.registrado_em for registro in registros]
        assert momentos == sorted(momentos)

    @invariant()
    def de_um_estado_final_nada_mais_muda(self):
        if self.retrato_final is not None:
            assert _retrato(self.reserva) == self.retrato_final
        elif self.reserva.situacao.eh_final:
            self.retrato_final = _retrato(self.reserva)

    @invariant()
    def solicitante_so_cancela_e_so_a_propria(self):
        for registro in self.reserva.registros_pendentes[1:]:
            if registro.autor_usuario_id != GESTOR.usuario_id:
                assert registro.autor_usuario_id == ANA.usuario_id
                assert registro.situacao_nova is S.CANCELADA

    @invariant()
    def o_outro_solicitante_nunca_muda_nada(self):
        autores = {r.autor_usuario_id for r in self.reserva.registros_pendentes}
        assert OUTRO.usuario_id not in autores

    @invariant()
    def recusada_e_cancelada_sempre_tem_motivo(self):
        if self.reserva.situacao in SITUACOES_QUE_EXIGEM_MOTIVO:
            assert self.reserva.motivo_da_situacao

    @invariant()
    def acoes_permitidas_sao_exatamente_as_alteracoes_aceitas(self):
        depois = self.agora + timedelta(minutes=1)
        for ator in ATORES.values():
            acoes = self.reserva.acoes_permitidas_para(ator)
            for destino in SituacaoReserva:
                aceita = _aceita(self.reserva, destino, ator, depois)
                assert (destino in acoes) is aceita, (ator.papel, destino)


TestMaquinaDaReserva = MaquinaDaReserva.TestCase
TestMaquinaDaReserva.settings = settings(stateful_step_count=20)
