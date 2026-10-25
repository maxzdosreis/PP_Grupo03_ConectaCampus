import { useId, type ReactNode } from 'react'
import estilos from './Campo.module.css'

export type AtributosDoControle = {
  id: string
  'aria-describedby': string | undefined
  'aria-invalid': true | undefined
}

type PropriedadesDoCampo = {
  rotulo: string
  dica?: string
  erro?: string
  children: (controle: AtributosDoControle) => ReactNode
}

function Campo({ rotulo, dica, erro, children }: PropriedadesDoCampo) {
  const id = useId()
  const idDaDica = `${id}-dica`
  const idDoErro = `${id}-erro`
  const descricao = [dica && idDaDica, erro && idDoErro].filter(Boolean).join(' ')

  return (
    <div className={estilos.campo}>
      <label htmlFor={id} className={estilos.rotulo}>
        {rotulo}
      </label>
      {dica && (
        <p id={idDaDica} className={estilos.dica}>
          {dica}
        </p>
      )}
      {children({
        id,
        'aria-describedby': descricao || undefined,
        'aria-invalid': erro ? true : undefined,
      })}
      {erro && (
        <p id={idDoErro} className={estilos.erro}>
          <span className={estilos.marcador} aria-hidden="true">
            !
          </span>
          <span className="somente-leitor-de-tela">Erro:</span> {erro}
        </p>
      )}
    </div>
  )
}

export default Campo
