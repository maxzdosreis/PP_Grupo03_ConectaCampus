import type { ReactNode } from 'react'
import Aviso from '../mensagens/Aviso.tsx'
import estilos from './FalhaAoCarregar.module.css'

type PropriedadesDaFalha = {
  mensagem: string
  aoTentarNovamente: () => void
  children?: ReactNode
}

function FalhaAoCarregar({ mensagem, aoTentarNovamente, children }: PropriedadesDaFalha) {
  return (
    <div className={estilos.falha}>
      <Aviso variante="erro">{mensagem}</Aviso>
      <div className={estilos.acoes}>
        <button type="button" onClick={aoTentarNovamente}>
          Tentar novamente
        </button>
        {children}
      </div>
    </div>
  )
}

export default FalhaAoCarregar
