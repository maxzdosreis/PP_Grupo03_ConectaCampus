import type { ReactNode } from 'react'
import { Botao } from '../botao/Botao.tsx'
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
        <Botao acao="atualizar" onClick={aoTentarNovamente}>
          Tentar novamente
        </Botao>
        {children}
      </div>
    </div>
  )
}

export default FalhaAoCarregar
