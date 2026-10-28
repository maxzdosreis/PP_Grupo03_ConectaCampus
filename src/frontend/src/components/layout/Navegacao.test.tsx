import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router'
import { describe, expect, it } from 'vitest'
import Navegacao from './Navegacao.tsx'

const ITENS = [
  { rotulo: 'Início', caminho: '/', exigeLogin: false },
  { rotulo: 'Espaços', caminho: '/espacos', exigeLogin: true },
  { rotulo: 'Reservas', caminho: '/reservas', exigeLogin: true },
  { rotulo: 'Nova reserva', caminho: '/reservas/nova', exigeLogin: true },
]

function renderizarEm(caminho: string) {
  render(
    <MemoryRouter initialEntries={[caminho]}>
      <Navegacao itens={ITENS} />
    </MemoryRouter>,
  )
}

describe('Navegacao', () => {
  it('marca como ativo só o item da página atual', () => {
    renderizarEm('/espacos')

    expect(screen.getByRole('link', { name: 'Espaços' }).getAttribute('aria-current')).toBe('page')
    expect(screen.getByRole('link', { name: 'Início' }).getAttribute('aria-current')).toBeNull()
  })

  it('marca o início como ativo na raiz', () => {
    renderizarEm('/')

    expect(screen.getByRole('link', { name: 'Início' }).getAttribute('aria-current')).toBe('page')
    expect(screen.getByRole('link', { name: 'Espaços' }).getAttribute('aria-current')).toBeNull()
  })

  it('em "/reservas/nova" marca só "Nova reserva", e não "Reservas"', () => {
    renderizarEm('/reservas/nova')

    expect(
      screen.getByRole('link', { name: 'Nova reserva' }).getAttribute('aria-current'),
    ).toBe('page')
    expect(screen.getByRole('link', { name: 'Reservas' }).getAttribute('aria-current')).toBeNull()
  })
})
