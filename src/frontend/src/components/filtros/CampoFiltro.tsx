import { useId, type ReactNode } from 'react'
import estilos from './CampoFiltro.module.css'

export type AtributosDoCampoDeFiltro = {
  id: string
  'aria-describedby': string | undefined
  placeholder?: string
}

type PropriedadesDoCampoDeFiltro = {
  rotulo: string
  dica?: string
  children: (controle: AtributosDoCampoDeFiltro) => ReactNode
}

function CampoFiltro({ rotulo, dica, children }: PropriedadesDoCampoDeFiltro) {
  const id = useId()
  const idDaDica = `${id}-dica`
  const controle: AtributosDoCampoDeFiltro = { id, 'aria-describedby': dica ? idDaDica : undefined }
  if (dica) {
    controle.placeholder = dica
  }

  return (
    <div className={estilos.campo}>
      <label htmlFor={id} className={estilos.rotulo} title={rotulo}>
        {rotulo}
      </label>
      {children(controle)}
      {dica && (
        <p id={idDaDica} className="somente-leitor-de-tela">
          {dica}
        </p>
      )}
    </div>
  )
}

export default CampoFiltro
