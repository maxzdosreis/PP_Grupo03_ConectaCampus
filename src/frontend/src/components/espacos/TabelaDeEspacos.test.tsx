import { render, screen, within } from '@testing-library/react'
import { MemoryRouter } from 'react-router'
import { describe, expect, it } from 'vitest'
import type { Espaco } from '../../api/espacos.ts'
import TabelaDeEspacos from './TabelaDeEspacos.tsx'

const GINASIO: Espaco = {
  id: 1,
  nome: 'Ginásio A',
  tipo: 'GINASIO',
  tipo_rotulo: 'Ginásio',
  capacidade: 50,
  ativo: true,
}

const QUADRA: Espaco = {
  id: 2,
  nome: 'Quadra Antiga',
  tipo: 'QUADRA_POLIESPORTIVA',
  tipo_rotulo: 'Quadra poliesportiva',
  capacidade: 20,
  ativo: false,
}

describe('TabelaDeEspacos', () => {
  it('mostra "Reservar" só nos espaços ativos, apontando para a nova reserva', () => {
    render(
      <MemoryRouter>
        <TabelaDeEspacos espacos={[GINASIO, QUADRA]} legenda="2 espaços encontrados." />
      </MemoryRouter>,
    )

    const reservar = screen.getByRole('link', { name: 'Reservar Ginásio A' })
    expect(reservar.textContent).toBe('Reservar')
    expect(reservar.getAttribute('href')).toBe('/reservas/nova?espaco=1')

    const linhaDoInativo = screen.getByRole('row', { name: /Quadra Antiga/ })
    expect(within(linhaDoInativo).queryByRole('link')).toBeNull()
    expect(screen.getAllByRole('link')).toHaveLength(1)
  })
})
