import {
  useEffect,
  useEffectEvent,
  useId,
  useRef,
  type ReactNode,
  type RefObject,
  type SyntheticEvent,
} from 'react'
import estilos from './Dialogo.module.css'

const SELETOR_DE_FOCAVEIS = [
  'button:not(:disabled)',
  'a[href]',
  'input:not(:disabled)',
  'select:not(:disabled)',
  'textarea:not(:disabled)',
  '[tabindex]:not([tabindex="-1"])',
].join(', ')

type Alvo = RefObject<HTMLElement | null>

type PropriedadesDoDialogo = {
  titulo: string
  aoFechar: () => void
  focoInicial?: Alvo
  alvoAoFechar?: Alvo
  children: ReactNode
}

function elementoFocado(): HTMLElement | null {
  const ativo = document.activeElement
  return ativo instanceof HTMLElement && ativo !== document.body ? ativo : null
}

function Dialogo({ titulo, aoFechar, focoInicial, alvoAoFechar, children }: PropriedadesDoDialogo) {
  const idDoTitulo = useId()
  const dialogo = useRef<HTMLDialogElement>(null)
  const conteudo = useRef<HTMLDivElement>(null)
  const botaoFechar = useRef<HTMLButtonElement>(null)

  const focarAoAbrir = useEffectEvent(() => {
    const primeiroFocavel = conteudo.current?.querySelector<HTMLElement>(SELETOR_DE_FOCAVEIS)
    ;(focoInicial?.current ?? primeiroFocavel ?? botaoFechar.current)?.focus()
  })

  const devolverFoco = useEffectEvent((quemAbriu: HTMLElement | null) => {
    const destino = quemAbriu?.isConnected ? quemAbriu : alvoAoFechar?.current
    destino?.focus()
  })

  useEffect(() => {
    const elemento = dialogo.current
    if (!elemento) return
    const quemAbriu = elementoFocado()
    elemento.showModal()
    focarAoAbrir()
    return () => {
      if (elemento.open) elemento.close()
      devolverFoco(quemAbriu)
    }
  }, [])

  function aoCancelar(evento: SyntheticEvent<HTMLDialogElement>) {
    evento.preventDefault()
    aoFechar()
  }

  return (
    <dialog
      ref={dialogo}
      className={estilos.dialogo}
      aria-labelledby={idDoTitulo}
      onCancel={aoCancelar}
    >
      <div className={estilos.cabecalho}>
        <h2 id={idDoTitulo} className={estilos.titulo}>
          {titulo}
        </h2>
        <button
          ref={botaoFechar}
          type="button"
          className={estilos.fechar}
          onClick={aoFechar}
          aria-label="Fechar"
        >
          ×
        </button>
      </div>
      <div ref={conteudo}>{children}</div>
    </dialog>
  )
}

export default Dialogo
