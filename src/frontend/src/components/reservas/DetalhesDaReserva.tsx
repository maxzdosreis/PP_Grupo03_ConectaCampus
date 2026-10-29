import type { Reserva } from '../../api/reservas.ts'
import { formatarDataHora, formatarIntervalo } from '../../formatacao.ts'
import estilos from './DetalhesDaReserva.module.css'
import EtiquetaDeSituacao from './EtiquetaDeSituacao.tsx'

type PropriedadesDosDetalhes = {
  reserva: Reserva
  nomeDoEspaco: string
}

function DetalhesDaReserva({ reserva, nomeDoEspaco }: PropriedadesDosDetalhes) {
  return (
    <dl className={estilos.detalhes}>
      <div>
        <dt>Espaço</dt>
        <dd>{nomeDoEspaco}</dd>
      </div>
      <div>
        <dt>Data e horário</dt>
        <dd>{formatarIntervalo(reserva.data, reserva.hora_inicio, reserva.hora_fim)}</dd>
      </div>
      <div>
        <dt>Solicitante</dt>
        <dd>
          {reserva.solicitante.nome} ({reserva.solicitante.matricula})
        </dd>
      </div>
      <div>
        <dt>Solicitada em</dt>
        <dd>
          <time dateTime={reserva.criada_em}>{formatarDataHora(reserva.criada_em)}</time>
        </dd>
      </div>
      <div className={estilos.inteira}>
        <dt>Finalidade</dt>
        <dd>{reserva.finalidade}</dd>
      </div>
      <div className={estilos.inteira}>
        <dt>Situação</dt>
        <dd>
          <EtiquetaDeSituacao situacao={reserva.situacao} rotulo={reserva.situacao_rotulo} />
          {reserva.motivo_da_situacao && (
            <span className={estilos.motivo}>Motivo: {reserva.motivo_da_situacao}</span>
          )}
        </dd>
      </div>
    </dl>
  )
}

export default DetalhesDaReserva
