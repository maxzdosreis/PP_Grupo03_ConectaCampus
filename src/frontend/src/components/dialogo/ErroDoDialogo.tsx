import type { Ref } from 'react'
import { Botao } from '../botao/Botao.tsx'
import Aviso from '../mensagens/Aviso.tsx'
import estilos from './ErroDoDialogo.module.css'

const STATUS_DE_LISTA_DESATUALIZADA = [404, 409]

type PropriedadesDoErroDoDialogo = {
  mensagem: string | null
  statusDoErro: number | null
  aoAtualizar: () => void
  rotuloDaAtualizacao?: string
  ref?: Ref<HTMLDivElement>
}

function ErroDoDialogo({
  mensagem,
  statusDoErro,
  aoAtualizar,
  rotuloDaAtualizacao = 'Atualizar lista',
  ref,
}: PropriedadesDoErroDoDialogo) {
  if (!mensagem) return null
  const desatualizado =
    statusDoErro !== null && STATUS_DE_LISTA_DESATUALIZADA.includes(statusDoErro)
  return (
    <div ref={ref} tabIndex={-1} className={estilos.erro}>
      <Aviso variante="erro">{mensagem}</Aviso>
      {desatualizado && (
        <div>
          <Botao acao="atualizar" onClick={aoAtualizar}>
            {rotuloDaAtualizacao}
          </Botao>
        </div>
      )}
    </div>
  )
}

export default ErroDoDialogo
