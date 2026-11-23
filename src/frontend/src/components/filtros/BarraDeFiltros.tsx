import type { ReactNode } from 'react'
import estilos from './BarraDeFiltros.module.css'

type PropriedadesDaBarra = {
  children: ReactNode
  acoes?: ReactNode
  rodape?: ReactNode
}

function BarraDeFiltros({ children, acoes, rodape }: PropriedadesDaBarra) {
  return (
    <fieldset className={estilos.barra}>
      <legend className={estilos.legenda}>Filtros</legend>
      <div className={estilos.linha}>
        {children}
        {acoes}
      </div>
      {rodape && <div className={estilos.rodape}>{rodape}</div>}
    </fieldset>
  )
}

type PropriedadesDaCaixa = {
  rotulo: string
  marcada: boolean
  aoMudar: (marcada: boolean) => void
}

export function CaixaDeFiltro({ rotulo, marcada, aoMudar }: PropriedadesDaCaixa) {
  return (
    <label className={estilos.marcavel}>
      <input type="checkbox" checked={marcada} onChange={(evento) => aoMudar(evento.target.checked)} />
      {rotulo}
    </label>
  )
}

export default BarraDeFiltros
