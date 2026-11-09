import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import type { Paginacao } from '../../api/tipos.ts'
import PaginacaoDeReservas from './PaginacaoDeReservas.tsx'

function paginacao(sobrescritas: Partial<Paginacao> = {}): Paginacao {
  return { pagina: 2, tamanho: 20, total: 45, total_de_paginas: 3, ...sobrescritas }
}

function botao(nome: string) {
  return screen.getByRole('button', { name: nome }) as HTMLButtonElement
}

describe('PaginacaoDeReservas', () => {
  it.each([
    [{ total: 0, total_de_paginas: 0, pagina: 1 }],
    [{ total: 20, total_de_paginas: 1, pagina: 1 }],
  ])('não aparece com uma página ou menos: %o', (sobrescritas) => {
    render(<PaginacaoDeReservas paginacao={paginacao(sobrescritas)} aoMudarPagina={vi.fn()} />)

    expect(screen.queryByRole('navigation')).toBeNull()
  })

  it('mostra a página atual, o número de páginas e o total dentro de "Paginação"', () => {
    render(<PaginacaoDeReservas paginacao={paginacao()} aoMudarPagina={vi.fn()} />)

    const navegacao = screen.getByRole('navigation', { name: 'Paginação' })
    expect(navegacao.textContent).toContain('Página 2 de 3 · 45 reservas')
    expect(botao('Anterior').disabled).toBe(false)
    expect(botao('Próxima').disabled).toBe(false)
  })

  it('"Anterior" fica desabilitado na primeira página e "Próxima" na última', () => {
    const { rerender } = render(
      <PaginacaoDeReservas paginacao={paginacao({ pagina: 1 })} aoMudarPagina={vi.fn()} />,
    )
    expect(botao('Anterior').disabled).toBe(true)
    expect(botao('Próxima').disabled).toBe(false)

    rerender(<PaginacaoDeReservas paginacao={paginacao({ pagina: 3 })} aoMudarPagina={vi.fn()} />)
    expect(botao('Anterior').disabled).toBe(false)
    expect(botao('Próxima').disabled).toBe(true)
  })

  it('"Anterior" e "Próxima" pedem a página vizinha', async () => {
    const aoMudarPagina = vi.fn()
    render(<PaginacaoDeReservas paginacao={paginacao()} aoMudarPagina={aoMudarPagina} />)

    await userEvent.click(botao('Próxima'))
    await userEvent.click(botao('Anterior'))

    expect(aoMudarPagina.mock.calls).toEqual([[3], [1]])
  })
})
