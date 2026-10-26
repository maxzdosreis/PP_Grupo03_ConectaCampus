import { beforeEach, describe, expect, it, vi } from 'vitest'
import { requisitar } from './cliente.ts'
import { listarReservas, listarSituacoesDeReserva, solicitarReserva } from './reservas.ts'

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

  it('listarReservas sem filtros consulta /reservas/ sem parâmetros', async () => {
    await listarReservas()

    expect(requisitar).toHaveBeenCalledWith('/reservas/')
  })

  it.each([
    [{ espaco: '3' }, '/reservas/?espaco=3'],
    [{ situacao: 'CONFIRMADA' }, '/reservas/?situacao=CONFIRMADA'],
    [{ data: '2026-11-10' }, '/reservas/?data=2026-11-10'],
    [{ solicitante: 'ana souza' }, '/reservas/?solicitante=ana+souza'],
    [{ minhas: true }, '/reservas/?minhas=true'],
  ])('listarReservas envia o filtro %o', async (filtros, url) => {
    await listarReservas(filtros)

    expect(requisitar).toHaveBeenCalledWith(url)
  })

  it('listarReservas combina os filtros e ignora os vazios', async () => {
    await listarReservas({
      espaco: '3',
      situacao: 'SOLICITADA',
      data: '',
      solicitante: '',
      minhas: false,
    })

    expect(requisitar).toHaveBeenCalledWith('/reservas/?espaco=3&situacao=SOLICITADA')
  })

  it('listarReservas combina todos os filtros', async () => {
    await listarReservas({
      espaco: '3',
      situacao: 'CANCELADA',
      data: '2026-11-10',
      solicitante: '2026001',
      minhas: true,
    })

    expect(requisitar).toHaveBeenCalledWith(
      '/reservas/?espaco=3&situacao=CANCELADA&data=2026-11-10&solicitante=2026001&minhas=true',
    )
  })

  it('listarSituacoesDeReserva consulta o vocabulário de situações', async () => {
    await listarSituacoesDeReserva()

    expect(requisitar).toHaveBeenCalledWith('/reservas/situacoes/')
  })
})
