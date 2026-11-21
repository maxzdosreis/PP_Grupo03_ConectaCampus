import type { AcaoDisponivel, Reserva } from '../../api/reservas.ts'
import { acaoDaSituacao } from '../botao/acoes.ts'
import { BotaoDeIcone } from '../botao/Botao.tsx'
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
        <BotaoDeIcone
          key={acao.situacao}
          acao={acaoDaSituacao(acao.situacao)}
          rotulo={`${acao.rotulo} a reserva de ${descricao}`}
          onClick={() => aoEscolherAcao(reserva, acao)}
        />
      ))}
    </div>
  )
}

export default AcoesDaReserva
