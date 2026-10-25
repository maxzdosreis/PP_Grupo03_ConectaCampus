import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router'
import { describe, expect, it } from 'vitest'
import Navegacao from './Navegacao.tsx'

const ITENS = [
  { rotulo: 'Início', caminho: '/' },
  { rotulo: 'Espaços', caminho: '/espacos' },
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
})
