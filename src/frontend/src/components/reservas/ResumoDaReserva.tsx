import { useEffect, useId, useRef } from 'react'
import { Link } from 'react-router'
import type { Reserva } from '../../api/reservas.ts'
import { formatarIntervalo } from '../../formatacao.ts'
import { caminhoParaMinhasReservas } from '../../navegacao.ts'
import EtiquetaDeSituacao from './EtiquetaDeSituacao.tsx'
import estilos from './ResumoDaReserva.module.css'

type PropriedadesDoResumo = {
  reserva: Reserva
  nomeDoEspaco: string
  aoSolicitarOutra: () => void
}

function ResumoDaReserva({ reserva, nomeDoEspaco, aoSolicitarOutra }: PropriedadesDoResumo) {
  const idDoTitulo = useId()
  const titulo = useRef<HTMLHeadingElement>(null)

  useEffect(() => {
    titulo.current?.focus()
  }, [])

  return (
    <section className={estilos.resumo} aria-labelledby={idDoTitulo}>
      <h2 id={idDoTitulo} ref={titulo} tabIndex={-1}>
        Reserva solicitada
      </h2>
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
          <dt>Finalidade</dt>
          <dd>{reserva.finalidade}</dd>
        </div>
        <div>
          <dt>Situação</dt>
          <dd>
            <EtiquetaDeSituacao situacao={reserva.situacao} rotulo={reserva.situacao_rotulo} />
          </dd>
        </div>
      </dl>
      <div className={estilos.acoes}>
        <button type="button" onClick={aoSolicitarOutra}>
          Solicitar outra reserva
        </button>
        <Link to={caminhoParaMinhasReservas()}>Ver minhas reservas</Link>
      </div>
    </section>
  )
}

export default ResumoDaReserva
