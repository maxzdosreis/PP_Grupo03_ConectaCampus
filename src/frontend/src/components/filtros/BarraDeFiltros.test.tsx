import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import BarraDeFiltros, { CaixaDeFiltro } from './BarraDeFiltros.tsx'
import CampoFiltro from './CampoFiltro.tsx'

describe('BarraDeFiltros', () => {
  it('é um grupo "Filtros" com os campos e as ações', () => {
    render(
      <BarraDeFiltros acoes={<button type="button">Limpar filtros</button>}>
        <CampoFiltro rotulo="Busca">
          {(controle) => <input {...controle} />}
        </CampoFiltro>
      </BarraDeFiltros>,
    )

    const grupo = screen.getByRole('group', { name: 'Filtros' })
    expect(grupo.contains(screen.getByLabelText('Busca'))).toBe(true)
    expect(grupo.contains(screen.getByRole('button', { name: 'Limpar filtros' }))).toBe(true)
  })

  it('a caixa de marcar avisa a mudança', async () => {
    const aoMudar = vi.fn()
    render(<CaixaDeFiltro rotulo="Somente ativos" marcada={false} aoMudar={aoMudar} />)

    await userEvent.click(screen.getByLabelText('Somente ativos'))

    expect(aoMudar).toHaveBeenCalledWith(true)
  })
})
