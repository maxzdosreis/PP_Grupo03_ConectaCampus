import type { AcaoDisponivel, Reserva } from '../../api/reservas.ts'
import estilos from './AcoesDaReserva.module.css'

type PropriedadesDasAcoes = {
  reserva: Reserva
  descricao: string
  aoEscolherAcao: (reserva: Reserva, acao: AcaoDisponivel) => void
}

function AcoesDaReserva({ reserva, descricao, aoEscolherAcao }: PropriedadesDasAcoes) {
  if (reserva.acoes_disponiveis.length === 0) return null
  return (
    <div className={estilos.acoes}>
      {reserva.acoes_disponiveis.map((acao) => (
        <button
          key={acao.situacao}
          type="button"
          className={estilos.acao}
          aria-label={`${acao.rotulo} a reserva de ${descricao}`}
          onClick={() => aoEscolherAcao(reserva, acao)}
        >
          {acao.rotulo}
        </button>
      ))}
    </div>
  )
}

export default AcoesDaReserva
