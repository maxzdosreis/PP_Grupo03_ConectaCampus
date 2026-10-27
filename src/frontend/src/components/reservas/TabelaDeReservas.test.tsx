import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import type { Reserva } from '../../api/reservas.ts'
import TabelaDeReservas from './TabelaDeReservas.tsx'

const SOLICITADA: Reserva = {
  id: 10,
  espaco_id: 1,
  solicitante: { usuario_id: 1, nome: 'Ana Souza', matricula: '2026001' },
  data: '2026-10-25',
  hora_inicio: '10:00',
  hora_fim: '11:00',
  finalidade: 'Treino de vôlei',
  situacao: 'SOLICITADA',
  situacao_rotulo: 'Solicitada',
  motivo_da_situacao: null,
  criada_em: '2026-10-20T10:00:00-03:00',
  acoes_disponiveis: [
    { situacao: 'CONFIRMADA', rotulo: 'Confirmar', exige_motivo: false },
    { situacao: 'RECUSADA', rotulo: 'Recusar', exige_motivo: true },
  ],
}

const CONCLUIDA: Reserva = {
  ...SOLICITADA,
  id: 11,
  espaco_id: 9,
  hora_inicio: '14:00',
  hora_fim: '15:00',
  situacao: 'CONCLUIDA',
  situacao_rotulo: 'Concluída',
  acoes_disponiveis: [],
}

const NOMES = new Map([[1, 'Ginásio A']])

function renderizar(reservas: Reserva[], aoEscolherAcao = vi.fn()) {
  render(
    <TabelaDeReservas
      reservas={reservas}
      legenda={`${reservas.length} reservas encontradas.`}
      nomesDosEspacos={NOMES}
      aoEscolherAcao={aoEscolherAcao}
    />,
  )
  return aoEscolherAcao
}

function botoesDaLinha(reservaDaLinha: string) {
  const linha = screen.getByRole('row', { name: new RegExp(reservaDaLinha) })
  return within(linha)
    .queryAllByRole('button')
    .map((botao) => botao.textContent)
}

describe('TabelaDeReservas', () => {
  it('mostra exatamente as ações recebidas da API', () => {
    renderizar([SOLICITADA])

    expect(screen.getByRole('columnheader', { name: 'Ações' })).toBeTruthy()
    expect(botoesDaLinha('10:00–11:00')).toEqual(['Confirmar', 'Recusar'])
  })

  it('não tem tabela própria: renderiza até uma ação que o frontend não conhece', () => {
    renderizar([
      {
        ...CONCLUIDA,
        acoes_disponiveis: [{ situacao: 'REABRIR', rotulo: 'Reabrir', exige_motivo: false }],
      },
    ])

    expect(botoesDaLinha('14:00–15:00')).toEqual(['Reabrir'])
  })

  it('sem ações mostra "—" e "Nenhuma ação disponível" para leitor de tela', () => {
    renderizar([CONCLUIDA])

    const linha = screen.getByRole('row', { name: /14:00–15:00/ })
    expect(within(linha).queryByRole('button')).toBeNull()
    expect(linha.textContent).toContain('—')
    expect(within(linha).getByText('Nenhuma ação disponível').className).toBe(
      'somente-leitor-de-tela',
    )
  })

  it('cada botão tem nome acessível com a data, o horário e o espaço', () => {
    renderizar([SOLICITADA, { ...CONCLUIDA, acoes_disponiveis: SOLICITADA.acoes_disponiveis }])

    const confirmar = screen.getByRole('button', {
      name: 'Confirmar a reserva de 25/10/2026, 10:00–11:00 em Ginásio A',
    })
    expect(confirmar.textContent).toBe('Confirmar')
    expect(
      screen.getByRole('button', {
        name: 'Recusar a reserva de 25/10/2026, 14:00–15:00 em Espaço #9',
      }),
    ).toBeTruthy()
  })

  it('o clique entrega a reserva e a ação escolhidas', async () => {
    const aoEscolherAcao = renderizar([SOLICITADA])

    await userEvent.click(screen.getByRole('button', { name: /^Recusar a reserva/ }))

    expect(aoEscolherAcao).toHaveBeenCalledWith(SOLICITADA, SOLICITADA.acoes_disponiveis[1])
  })
})
