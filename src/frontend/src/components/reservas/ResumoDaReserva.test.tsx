import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router'
import { describe, expect, it, vi } from 'vitest'
import type { Reserva } from '../../api/reservas.ts'
import ResumoDaReserva from './ResumoDaReserva.tsx'

const RESERVA: Reserva = {
  id: 12,
  espaco_id: 1,
  solicitante: { usuario_id: 1, nome: 'Ana Souza', matricula: '2026001' },
  data: '2026-11-10',
  hora_inicio: '10:00',
  hora_fim: '11:00',
  finalidade: 'Treino de vôlei',
  situacao: 'SOLICITADA',
  situacao_rotulo: 'Solicitada',
  motivo_da_situacao: null,
  criada_em: '2026-10-25T10:00:00-03:00',
}

describe('ResumoDaReserva', () => {
  it('tem o link "Ver minhas reservas" para a consulta filtrada', () => {
    render(
      <MemoryRouter>
        <ResumoDaReserva reserva={RESERVA} nomeDoEspaco="Ginásio A" aoSolicitarOutra={vi.fn()} />
      </MemoryRouter>,
    )

    expect(
      screen.getByRole('link', { name: 'Ver minhas reservas' }).getAttribute('href'),
    ).toBe('/reservas?minhas=true')
  })
})
