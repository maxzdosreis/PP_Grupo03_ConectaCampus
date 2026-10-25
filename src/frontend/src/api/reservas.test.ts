import { beforeEach, describe, expect, it, vi } from 'vitest'
import { requisitar } from './cliente.ts'
import { solicitarReserva } from './reservas.ts'

vi.mock('./cliente.ts', async (importarOriginal) => ({
  ...(await importarOriginal<typeof import('./cliente.ts')>()),
  requisitar: vi.fn(),
}))

describe('api de reservas', () => {
  beforeEach(() => {
    vi.mocked(requisitar).mockReset()
    vi.mocked(requisitar).mockResolvedValue({ mensagem: 'ok', dados: null })
  })

  it('solicitarReserva envia um POST com os dados como foram preenchidos', async () => {
    const dados = {
      espaco_id: '1',
      data: '2026-10-25',
      hora_inicio: '10:00',
      hora_fim: '11:00',
      finalidade: 'Treino do time de vôlei',
    }

    await solicitarReserva(dados)

    expect(requisitar).toHaveBeenCalledWith('/reservas/', {
      method: 'POST',
      body: JSON.stringify(dados),
    })
  })
})
