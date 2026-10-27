import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { useRef, useState } from 'react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import Dialogo from './Dialogo.tsx'

type PropriedadesDoTeste = {
  aoFechar?: () => void
  removerQuemAbriuAoFechar?: boolean
}

function DialogoDeTeste({ aoFechar, removerQuemAbriuAoFechar = false }: PropriedadesDoTeste) {
  const [aberto, setAberto] = useState(false)
  const [mostrarBotao, setMostrarBotao] = useState(true)
  const alvo = useRef<HTMLHeadingElement>(null)

  function fechar() {
    aoFechar?.()
    setAberto(false)
    if (removerQuemAbriuAoFechar) setMostrarBotao(false)
  }

  return (
    <>
      <h1 ref={alvo} tabIndex={-1}>
        Página
      </h1>
      {mostrarBotao && (
        <button type="button" onClick={() => setAberto(true)}>
          Abrir
        </button>
      )}
      {aberto && (
        <Dialogo titulo="Confirmar reserva" aoFechar={fechar} alvoAoFechar={alvo}>
          <p>Conteúdo</p>
          <button type="button">Primeira ação</button>
        </Dialogo>
      )}
    </>
  )
}

describe('Dialogo', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('abre com showModal, nomeado pelo título, com foco no primeiro do conteúdo', async () => {
    const showModal = vi.spyOn(HTMLDialogElement.prototype, 'showModal')
    render(<DialogoDeTeste />)

    await userEvent.click(screen.getByRole('button', { name: 'Abrir' }))

    const dialogo = screen.getByRole('dialog', { name: 'Confirmar reserva' }) as HTMLDialogElement
    expect(showModal).toHaveBeenCalled()
    expect(dialogo.open).toBe(true)
    expect(document.activeElement).toBe(screen.getByRole('button', { name: 'Primeira ação' }))
  })

  it('Esc chama aoFechar', async () => {
    const aoFechar = vi.fn()
    render(<DialogoDeTeste aoFechar={aoFechar} />)
    await userEvent.click(screen.getByRole('button', { name: 'Abrir' }))

    await userEvent.keyboard('{Escape}')

    expect(aoFechar).toHaveBeenCalledTimes(1)
    expect(screen.queryByRole('dialog')).toBeNull()
  })

  it('o botão de fechar chama aoFechar', async () => {
    const aoFechar = vi.fn()
    render(<DialogoDeTeste aoFechar={aoFechar} />)
    await userEvent.click(screen.getByRole('button', { name: 'Abrir' }))

    await userEvent.click(screen.getByRole('button', { name: 'Fechar' }))

    expect(aoFechar).toHaveBeenCalledTimes(1)
  })

  it('ao fechar, o foco volta para quem abriu', async () => {
    render(<DialogoDeTeste />)
    const abrir = screen.getByRole('button', { name: 'Abrir' })
    await userEvent.click(abrir)

    await userEvent.keyboard('{Escape}')

    expect(document.activeElement).toBe(abrir)
  })

  it('se quem abriu sumiu, o foco vai para o alvo informado', async () => {
    render(<DialogoDeTeste removerQuemAbriuAoFechar />)
    await userEvent.click(screen.getByRole('button', { name: 'Abrir' }))

    await userEvent.click(screen.getByRole('button', { name: 'Fechar' }))

    expect(document.activeElement).toBe(screen.getByRole('heading', { name: 'Página' }))
  })
})
