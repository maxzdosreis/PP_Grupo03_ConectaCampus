import type { ReactNode } from 'react'
import estilos from './Etiqueta.module.css'

export type VarianteDaEtiqueta = 'sucesso' | 'neutra' | 'aviso' | 'erro'

type PropriedadesDaEtiqueta = {
  variante: VarianteDaEtiqueta
  children: ReactNode
}

function Etiqueta({ variante, children }: PropriedadesDaEtiqueta) {
  return <span className={`${estilos.etiqueta} ${estilos[variante]}`}>{children}</span>
}

export default Etiqueta
