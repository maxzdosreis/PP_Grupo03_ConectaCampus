import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router'
import { describe, expect, it, vi } from 'vitest'
import type { Espaco } from '../../api/espacos.ts'
import TabelaDeEspacos, { type AcoesDeGestao } from './TabelaDeEspacos.tsx'

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

function renderizar(gestao?: AcoesDeGestao) {
  render(
    <MemoryRouter>
      <TabelaDeEspacos espacos={[GINASIO, QUADRA]} legenda="2 espaços encontrados." gestao={gestao} />
    </MemoryRouter>,
  )
}

describe('TabelaDeEspacos', () => {
  it('mostra "Reservar" só nos espaços ativos, apontando para a nova reserva', () => {
    renderizar()

    const reservar = screen.getByRole('link', { name: 'Reservar Ginásio A' })
    expect(reservar.textContent).toBe('Reservar')
    expect(reservar.getAttribute('href')).toBe('/reservas/nova?espaco=1')

    const linhaDoInativo = screen.getByRole('row', { name: /Quadra Antiga/ })
    expect(within(linhaDoInativo).queryByRole('link')).toBeNull()
    expect(screen.getAllByRole('link')).toHaveLength(1)
  })

  it('sem as ações de gestão, não mostra botões', () => {
    renderizar()

    expect(screen.queryByRole('button')).toBeNull()
  })

  it('com as ações de gestão, oferece editar e a ativação válida para cada espaço', async () => {
    const gestao = { aoEditar: vi.fn(), aoAlterarAtivacao: vi.fn() }
    renderizar(gestao)

    const linhaDoAtivo = within(screen.getByRole('row', { name: /Ginásio A/ }))
    const linhaDoInativo = within(screen.getByRole('row', { name: /Quadra Antiga/ }))
    expect(linhaDoAtivo.getByRole('button', { name: 'Desativar o espaço Ginásio A' }).textContent).toBe(
      'Desativar',
    )
    expect(linhaDoAtivo.queryByRole('button', { name: /Reativar/ })).toBeNull()
    expect(
      linhaDoInativo.getByRole('button', { name: 'Reativar o espaço Quadra Antiga' }).textContent,
    ).toBe('Reativar')
    expect(linhaDoInativo.queryByRole('button', { name: /Desativar/ })).toBeNull()
    expect(linhaDoAtivo.getByRole('link', { name: 'Reservar Ginásio A' })).toBeTruthy()

    await userEvent.click(linhaDoAtivo.getByRole('button', { name: 'Editar o espaço Ginásio A' }))
    await userEvent.click(
      linhaDoInativo.getByRole('button', { name: 'Reativar o espaço Quadra Antiga' }),
    )

    expect(gestao.aoEditar).toHaveBeenCalledWith(GINASIO)
    expect(gestao.aoAlterarAtivacao).toHaveBeenCalledWith(QUADRA)
  })
})
