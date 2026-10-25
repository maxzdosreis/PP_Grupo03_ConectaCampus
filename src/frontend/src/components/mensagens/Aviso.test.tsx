import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import Aviso from './Aviso.tsx'

describe('Aviso', () => {
  it('anuncia sucesso e informação com role status', () => {
    render(
      <>
        <Aviso variante="sucesso">Espaço cadastrado.</Aviso>
        <Aviso variante="informacao">Nenhum filtro aplicado.</Aviso>
      </>,
    )

    expect(screen.getAllByRole('status')).toHaveLength(2)
    expect(screen.queryByRole('alert')).toBeNull()
  })

  it('anuncia erro com role alert', () => {
    render(<Aviso variante="erro">Não foi possível salvar.</Aviso>)

    expect(screen.getByRole('alert').textContent).toContain('Não foi possível salvar.')
  })

  it('não tem role quando outra região já anuncia o conteúdo', () => {
    render(
      <Aviso variante="erro" anunciar={false}>
        Falhou.
      </Aviso>,
    )

    expect(screen.queryByRole('alert')).toBeNull()
    expect(screen.getByText('Falhou.')).toBeTruthy()
  })

  it('só mostra o botão de fechar quando recebe aoFechar', () => {
    render(<Aviso variante="sucesso">Pronto.</Aviso>)

    expect(screen.queryByRole('button', { name: 'Fechar mensagem' })).toBeNull()
  })

  it('chama aoFechar ao clicar no botão de fechar', async () => {
    const aoFechar = vi.fn()
    render(
      <Aviso variante="erro" aoFechar={aoFechar}>
        Falhou.
      </Aviso>,
    )

    await userEvent.click(screen.getByRole('button', { name: 'Fechar mensagem' }))

    expect(aoFechar).toHaveBeenCalledOnce()
  })
})
