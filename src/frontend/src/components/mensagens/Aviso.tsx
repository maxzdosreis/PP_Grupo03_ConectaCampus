import type { ReactNode } from 'react'
import estilos from './Aviso.module.css'

export type VarianteDoAviso = 'sucesso' | 'erro' | 'informacao'

type PropriedadesDoAviso = {
  variante: VarianteDoAviso
  children: ReactNode
  aoFechar?: () => void
  anunciar?: boolean
}

const APRESENTACAO: Record<
  VarianteDoAviso,
  { papel: 'status' | 'alert'; marcador: string; rotulo: string }
> = {
  sucesso: { papel: 'status', marcador: '✓', rotulo: 'Sucesso' },
  erro: { papel: 'alert', marcador: '!', rotulo: 'Erro' },
  informacao: { papel: 'status', marcador: 'i', rotulo: 'Informação' },
}

function Aviso({ variante, children, aoFechar, anunciar = true }: PropriedadesDoAviso) {
  const { papel, marcador, rotulo } = APRESENTACAO[variante]
  return (
    <div role={anunciar ? papel : undefined} className={`${estilos.aviso} ${estilos[variante]}`}>
      <span className={estilos.marcador} aria-hidden="true">
        {marcador}
      </span>
      <span className="somente-leitor-de-tela">{rotulo}:</span>
      <div className={estilos.texto}>{children}</div>
      {aoFechar && (
        <button
          type="button"
          className={estilos.fechar}
          onClick={aoFechar}
          aria-label="Fechar mensagem"
        >
          ×
        </button>
      )}
    </div>
  )
}

export default Aviso
