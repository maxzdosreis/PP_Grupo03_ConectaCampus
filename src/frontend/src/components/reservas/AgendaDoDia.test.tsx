import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { ErroDaApi } from '../../api/cliente.ts'
import { obterOcupacaoDoDia, type OcupacaoDoDia } from '../../api/reservas.ts'
import AgendaDoDia from './AgendaDoDia.tsx'

vi.mock('../../api/reservas.ts', () => ({
  obterOcupacaoDoDia: vi.fn(),
}))

const OCUPACAO: OcupacaoDoDia = {
  data: '2026-10-25',
  horario_de_abertura: '08:00',
  horario_de_fechamento: '20:00',
  reservavel: true,
  motivo_indisponivel: null,
  ocupados: [
    { hora_inicio: '10:00', hora_fim: '11:00', situacao: 'CONFIRMADA', situacao_rotulo: 'Confirmada' },
  ],
  livres: [
    { hora_inicio: '08:00', hora_fim: '10:00' },
    { hora_inicio: '11:00', hora_fim: '20:00' },
  ],
}

const MENSAGEM = '1 horário ocupado neste dia.'

function renderizar(espacoId = '1', data = '2026-10-25', aoUsarHorario = vi.fn()) {
  render(
    <AgendaDoDia espacoId={espacoId} data={data} recargas={0} aoUsarHorario={aoUsarHorario} />,
  )
  return aoUsarHorario
}

describe('AgendaDoDia', () => {
  beforeEach(() => {
    vi.mocked(obterOcupacaoDoDia).mockReset()
    vi.mocked(obterOcupacaoDoDia).mockResolvedValue({ mensagem: MENSAGEM, dados: OCUPACAO })
  })

  it.each([
    ['', '2026-10-25'],
    ['1', ''],
  ])('sem espaço ou sem data (%o, %o), mostra a instrução e não consulta', (espacoId, data) => {
    renderizar(espacoId, data)

    expect(
      screen.getByText('Escolha o espaço e a data para ver os horários ocupados.'),
    ).toBeTruthy()
    expect(obterOcupacaoDoDia).not.toHaveBeenCalled()
  })

  it('mostra os ocupados com a situação e os livres com o horário recebido', async () => {
    renderizar()

    const ocupados = await screen.findByRole('list', { name: 'Ocupados' })
    expect(obterOcupacaoDoDia).toHaveBeenCalledWith('1', '2026-10-25')
    expect(within(ocupados).getByRole('listitem').textContent).toBe('10:00–11:00Confirmada')
    const livres = screen.getByRole('list', { name: 'Livres' })
    expect(within(livres).getAllByRole('listitem').map((item) => item.firstChild?.textContent)).toEqual(
      ['08:00–10:00', '11:00–20:00'],
    )
  })

  it('anuncia a mensagem da API numa região polite', async () => {
    renderizar()

    await screen.findByRole('list', { name: 'Ocupados' })
    const regiao = document.querySelector('[aria-live="polite"]')
    expect(regiao?.textContent).toBe(MENSAGEM)
  })

  it('a faixa é só decoração; o conteúdo acessível são as listas', async () => {
    renderizar()

    await screen.findByRole('list', { name: 'Ocupados' })
    const faixa = screen.getByText('08:00').closest('[aria-hidden="true"]')
    expect(faixa).not.toBeNull()
    expect(faixa?.querySelectorAll('span[style]')).toHaveLength(3)
    expect(screen.getByRole('heading', { name: 'Ocupados' })).toBeTruthy()
    expect(screen.getByRole('heading', { name: 'Livres' })).toBeTruthy()
  })

  it('"Usar este horário" entrega a janela escolhida', async () => {
    const aoUsarHorario = renderizar()

    await userEvent.click(
      await screen.findByRole('button', { name: 'Usar este horário, 11:00–20:00' }),
    )

    expect(aoUsarHorario).toHaveBeenCalledWith({ hora_inicio: '11:00', hora_fim: '20:00' })
  })

  it('data em que não é possível reservar mostra o motivo da API', async () => {
    const motivo = 'Mensagem do domínio sobre a data.'
    vi.mocked(obterOcupacaoDoDia).mockResolvedValue({
      mensagem: 'Nenhum horário ocupado neste dia.',
      dados: { ...OCUPACAO, reservavel: false, motivo_indisponivel: motivo, ocupados: [], livres: [] },
    })

    renderizar()

    expect(await screen.findByText(motivo, { selector: 'div' })).toBeTruthy()
    expect(document.querySelector('[aria-live="polite"]')?.textContent).toBe(motivo)
    expect(screen.queryByRole('list', { name: 'Livres' })).toBeNull()
  })

  it('falha ao carregar mostra um aviso informativo e "Tentar novamente" consulta de novo', async () => {
    vi.mocked(obterOcupacaoDoDia)
      .mockRejectedValueOnce(new ErroDaApi(0, 'SEM_CONEXAO', 'Não foi possível conectar ao servidor.'))
      .mockResolvedValueOnce({ mensagem: MENSAGEM, dados: OCUPACAO })
    renderizar()

    expect(
      await screen.findByText(
        'Não foi possível carregar a agenda. Você ainda pode solicitar normalmente.',
      ),
    ).toBeTruthy()
    expect(screen.queryByRole('alert')).toBeNull()

    await userEvent.click(screen.getByRole('button', { name: 'Tentar novamente' }))

    expect(await screen.findByRole('list', { name: 'Ocupados' })).toBeTruthy()
    expect(obterOcupacaoDoDia).toHaveBeenCalledTimes(2)
  })
})
