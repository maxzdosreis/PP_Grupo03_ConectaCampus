import { screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Route, Routes } from 'react-router'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { ErroDaApi } from '../api/cliente.ts'
import { obterEspaco, type Espaco } from '../api/espacos.ts'
import {
  alterarSituacaoReserva,
  listarHistoricoDaReserva,
  obterReserva,
  type RegistroDeSituacao,
  type Reserva,
} from '../api/reservas.ts'
import LocalAtual from '../testes/LocalAtual.tsx'
import {
  renderizarComProvedores,
  valorDaSessao,
  type EntradaDaRota,
} from '../testes/renderizar.tsx'
import { USUARIO_GESTOR, USUARIO_SOLICITANTE } from '../testes/usuarios.ts'
import PaginaReserva from './PaginaReserva.tsx'

vi.mock('../api/espacos.ts', () => ({
  obterEspaco: vi.fn(),
}))

vi.mock('../api/reservas.ts', () => ({
  alterarSituacaoReserva: vi.fn(),
  listarHistoricoDaReserva: vi.fn(),
  obterReserva: vi.fn(),
}))

const GINASIO: Espaco = {
  id: 1,
  nome: 'Ginásio A',
  tipo: 'GINASIO',
  tipo_rotulo: 'Ginásio',
  capacidade: 50,
  ativo: true,
}

const SOLICITADA: Reserva = {
  id: 5,
  espaco_id: 1,
  solicitante: { usuario_id: 2, nome: 'Bruno Lima', matricula: '2026101' },
  data: '2026-11-10',
  hora_inicio: '10:00',
  hora_fim: '11:00',
  finalidade: 'Treino de vôlei',
  situacao: 'SOLICITADA',
  situacao_rotulo: 'Solicitada',
  motivo_da_situacao: null,
  criada_em: '2026-10-25T09:15:42.123456-03:00',
  acoes_disponiveis: [
    { situacao: 'CONFIRMADA', rotulo: 'Confirmar', exige_motivo: false },
    { situacao: 'RECUSADA', rotulo: 'Recusar', exige_motivo: true },
    { situacao: 'CANCELADA', rotulo: 'Cancelar', exige_motivo: true },
  ],
}

const CONFIRMADA: Reserva = {
  ...SOLICITADA,
  situacao: 'CONFIRMADA',
  situacao_rotulo: 'Confirmada',
  acoes_disponiveis: [],
}

const CRIACAO: RegistroDeSituacao = {
  situacao_anterior: null,
  situacao_anterior_rotulo: null,
  situacao_nova: 'SOLICITADA',
  situacao_nova_rotulo: 'Solicitada',
  motivo: null,
  autor: { nome: 'Bruno Lima' },
  registrado_em: '2026-10-25T09:15:42.123456-03:00',
}

const CONFIRMACAO: RegistroDeSituacao = {
  situacao_anterior: 'SOLICITADA',
  situacao_anterior_rotulo: 'Solicitada',
  situacao_nova: 'CONFIRMADA',
  situacao_nova_rotulo: 'Confirmada',
  motivo: null,
  autor: { nome: 'Carla Mendes' },
  registrado_em: '2026-10-26T14:05:00-03:00',
}

const CANCELAMENTO: RegistroDeSituacao = {
  situacao_anterior: 'CONFIRMADA',
  situacao_anterior_rotulo: 'Confirmada',
  situacao_nova: 'CANCELADA',
  situacao_nova_rotulo: 'Cancelada',
  motivo: 'Chuva forte',
  autor: { nome: 'Carla Mendes' },
  registrado_em: '2026-11-01T00:00:00-03:00',
}

function renderizar(caminho: EntradaDaRota = '/reservas/5', usuario = USUARIO_GESTOR) {
  renderizarComProvedores(
    <Routes>
      <Route path="/reservas/:reservaId" element={<PaginaReserva />} />
      <Route path="/reservas" element={<LocalAtual />} />
    </Routes>,
    { caminho, sessao: valorDaSessao({ usuario }) },
  )
}

function titulo() {
  return screen.getByRole('heading', { level: 1 })
}

function secaoDoHistorico() {
  return screen.getByRole('region', { name: 'Histórico' })
}

function valorDoDetalhe(termo: string) {
  const rotulo = screen.getByText(termo, { selector: 'dt' })
  return rotulo.nextElementSibling as HTMLElement
}

describe('PaginaReserva', () => {
  beforeEach(() => {
    vi.mocked(obterReserva).mockReset()
    vi.mocked(listarHistoricoDaReserva).mockReset()
    vi.mocked(obterEspaco).mockReset()
    vi.mocked(alterarSituacaoReserva).mockReset()
    vi.mocked(obterReserva).mockResolvedValue({ mensagem: 'Reserva encontrada.', dados: SOLICITADA })
    vi.mocked(listarHistoricoDaReserva).mockResolvedValue({
      mensagem: 'Histórico da reserva.',
      dados: [CRIACAO],
    })
    vi.mocked(obterEspaco).mockResolvedValue({ mensagem: 'Espaço encontrado.', dados: GINASIO })
  })

  it('mostra os dados da reserva com o nome do espaço e as datas formatadas', async () => {
    renderizar()

    expect(await screen.findByText('Ginásio A')).toBeTruthy()
    expect(titulo().textContent).toBe('Reserva de 10/11/2026')
    expect(document.title).toBe('Reserva de 10/11/2026 · Conecta Campus')
    expect(valorDoDetalhe('Data e horário').textContent).toBe('10/11/2026, 10:00–11:00')
    expect(valorDoDetalhe('Solicitante').textContent).toBe('Bruno Lima (2026101)')
    expect(valorDoDetalhe('Finalidade').textContent).toBe('Treino de vôlei')
    expect(valorDoDetalhe('Situação').textContent).toBe('Solicitada')
    const solicitadaEm = within(valorDoDetalhe('Solicitada em')).getByText('25/10/2026 às 09:15')
    expect(solicitadaEm.tagName).toBe('TIME')
    expect(solicitadaEm.getAttribute('dateTime')).toBe(SOLICITADA.criada_em)
    expect(obterReserva).toHaveBeenCalledWith(5)
    expect(listarHistoricoDaReserva).toHaveBeenCalledWith(5)
    expect(obterEspaco).toHaveBeenCalledWith(1)
  })

  it('mostra o motivo junto da situação quando houver', async () => {
    vi.mocked(obterReserva).mockResolvedValue({
      mensagem: 'Reserva encontrada.',
      dados: { ...CONFIRMADA, situacao: 'CANCELADA', situacao_rotulo: 'Cancelada', motivo_da_situacao: 'Chuva forte' },
    })

    renderizar()

    await screen.findByText('Ginásio A')
    expect(valorDoDetalhe('Situação').textContent).toBe('CanceladaMotivo: Chuva forte')
  })

  it('se o espaço falhar, mostra "Espaço #<id>" e o resto do detalhe', async () => {
    vi.mocked(obterEspaco).mockRejectedValue(
      new ErroDaApi(0, 'SEM_CONEXAO', 'Não foi possível conectar ao servidor.'),
    )

    renderizar()

    expect(await screen.findByText('Espaço #1')).toBeTruthy()
    expect(valorDoDetalhe('Finalidade').textContent).toBe('Treino de vôlei')
  })

  it('mostra a linha do tempo em ordem, com data e hora, autor e motivo', async () => {
    vi.mocked(listarHistoricoDaReserva).mockResolvedValue({
      mensagem: 'Histórico da reserva.',
      dados: [CRIACAO, CONFIRMACAO, CANCELAMENTO],
    })

    renderizar()

    const secao = await screen.findByRole('region', { name: 'Histórico' })
    const itens = await within(secao).findAllByRole('listitem')
    expect(itens.map((item) => item.querySelector('p')?.textContent)).toEqual([
      'Solicitada por Bruno Lima',
      'Confirmada por Carla Mendes',
      'Cancelada por Carla Mendes',
    ])
    const momentos = itens.map((item) => item.querySelector('time')!)
    expect(momentos.map((momento) => momento.textContent)).toEqual([
      '25/10/2026 às 09:15',
      '26/10/2026 às 14:05',
      '01/11/2026 às 00:00',
    ])
    expect(momentos[1].getAttribute('dateTime')).toBe('2026-10-26T14:05:00-03:00')
    expect(itens[2].textContent).toContain('Motivo: Chuva forte')
    expect(itens[0].textContent).not.toContain('Motivo')
  })

  it('se o histórico falhar, o erro fica só na seção e "Tentar novamente" busca de novo', async () => {
    vi.mocked(listarHistoricoDaReserva)
      .mockRejectedValueOnce(new ErroDaApi(0, 'SEM_CONEXAO', 'Não foi possível conectar ao servidor.'))
      .mockResolvedValueOnce({ mensagem: 'Histórico da reserva.', dados: [CRIACAO] })

    renderizar()

    const alerta = await within(await screen.findByRole('region', { name: 'Histórico' })).findByRole(
      'alert',
    )
    expect(alerta.textContent).toContain('Não foi possível conectar ao servidor.')
    expect(await screen.findByText('Ginásio A')).toBeTruthy()

    await userEvent.click(within(secaoDoHistorico()).getByRole('button', { name: 'Tentar novamente' }))

    expect(await within(secaoDoHistorico()).findByText('por Bruno Lima', { exact: false })).toBeTruthy()
    expect(listarHistoricoDaReserva).toHaveBeenCalledTimes(2)
    expect(obterReserva).toHaveBeenCalledTimes(1)
  })

  it('histórico vazio mostra "Nenhuma mudança registrada."', async () => {
    vi.mocked(listarHistoricoDaReserva).mockResolvedValue({
      mensagem: 'Histórico da reserva.',
      dados: [],
    })

    renderizar()

    expect(await screen.findByText('Nenhuma mudança registrada.')).toBeTruthy()
  })

  it('404 mostra "Reserva não encontrada", sem detalhe nem histórico', async () => {
    vi.mocked(obterReserva).mockRejectedValue(
      new ErroDaApi(404, 'RESERVA_NAO_ENCONTRADA', 'Reserva não encontrada.'),
    )
    vi.mocked(listarHistoricoDaReserva).mockRejectedValue(
      new ErroDaApi(404, 'RESERVA_NAO_ENCONTRADA', 'Reserva não encontrada.'),
    )

    renderizar('/reservas/99', USUARIO_SOLICITANTE)

    expect(await screen.findByText('Reserva não encontrada')).toBeTruthy()
    await waitFor(() => expect(document.title).toBe('Reserva não encontrada · Conecta Campus'))
    expect(screen.queryByRole('region', { name: 'Histórico' })).toBeNull()
    expect(screen.queryByRole('alert')).toBeNull()
    expect(
      screen.getByRole('link', { name: 'Voltar para as reservas' }).getAttribute('href'),
    ).toBe('/reservas')
  })

  it.each(['abc', '0', '5a'])('id "%s" na URL mostra o mesmo estado, sem chamar a API', (id) => {
    renderizar(`/reservas/${id}`)

    expect(screen.getByText('Reserva não encontrada')).toBeTruthy()
    expect(obterReserva).not.toHaveBeenCalled()
    expect(listarHistoricoDaReserva).not.toHaveBeenCalled()
  })

  it('outra falha ao carregar a reserva mostra a mensagem e "Tentar novamente"', async () => {
    vi.mocked(obterReserva)
      .mockRejectedValueOnce(new ErroDaApi(0, 'SEM_CONEXAO', 'Não foi possível conectar ao servidor.'))
      .mockResolvedValueOnce({ mensagem: 'Reserva encontrada.', dados: SOLICITADA })

    renderizar()

    expect((await screen.findByRole('alert')).textContent).toContain(
      'Não foi possível conectar ao servidor.',
    )
    await userEvent.click(screen.getByRole('button', { name: 'Tentar novamente' }))

    expect(await screen.findByText('Ginásio A')).toBeTruthy()
  })

  it('os botões vêm de acoes_disponiveis, com nome acessível com contexto', async () => {
    renderizar()

    await screen.findByText('Ginásio A')
    expect(screen.getAllByRole('button').map((botao) => botao.textContent)).toEqual([
      'Confirmar',
      'Recusar',
      'Cancelar',
    ])
    expect(
      screen.getByRole('button', {
        name: 'Confirmar a reserva de 10/11/2026, 10:00–11:00 em Ginásio A',
      }),
    ).toBeTruthy()
  })

  it('sem ações, não mostra nenhum botão', async () => {
    vi.mocked(obterReserva).mockResolvedValue({ mensagem: 'Reserva encontrada.', dados: CONFIRMADA })

    renderizar()

    await screen.findByText('Ginásio A')
    expect(screen.queryAllByRole('button')).toHaveLength(0)
  })

  it('uma ação concluída recarrega a reserva e o histórico e põe o foco no título', async () => {
    vi.mocked(obterReserva)
      .mockResolvedValueOnce({ mensagem: 'Reserva encontrada.', dados: SOLICITADA })
      .mockResolvedValueOnce({ mensagem: 'Reserva encontrada.', dados: CONFIRMADA })
    vi.mocked(listarHistoricoDaReserva)
      .mockResolvedValueOnce({ mensagem: 'Histórico da reserva.', dados: [CRIACAO] })
      .mockResolvedValueOnce({ mensagem: 'Histórico da reserva.', dados: [CRIACAO, CONFIRMACAO] })
    vi.mocked(alterarSituacaoReserva).mockResolvedValue({
      mensagem: 'Reserva confirmada com sucesso.',
      dados: CONFIRMADA,
    })
    renderizar()

    await userEvent.click(await screen.findByRole('button', { name: /^Confirmar a reserva/ }))
    const dialogo = screen.getByRole('dialog', { name: 'Confirmar reserva' })
    await userEvent.click(within(dialogo).getByRole('button', { name: 'Confirmar reserva' }))

    expect(alterarSituacaoReserva).toHaveBeenCalledWith(5, { situacao: 'CONFIRMADA' })
    expect(await screen.findByText('Reserva confirmada com sucesso.')).toBeTruthy()
    expect(await within(secaoDoHistorico()).findByText('por Carla Mendes', { exact: false })).toBeTruthy()
    await waitFor(() => expect(valorDoDetalhe('Situação').textContent).toBe('Confirmada'))
    expect(obterReserva).toHaveBeenCalledTimes(2)
    expect(listarHistoricoDaReserva).toHaveBeenCalledTimes(2)
    await waitFor(() => expect(document.activeElement).toBe(titulo()))
    expect(screen.queryByRole('dialog')).toBeNull()
  })

  it('no 409, o diálogo oferece "Atualizar reserva", que recarrega o detalhe', async () => {
    vi.mocked(alterarSituacaoReserva).mockRejectedValue(
      new ErroDaApi(409, 'RESERVA_DESATUALIZADA', 'A reserva foi alterada por outra pessoa.'),
    )
    renderizar()

    await userEvent.click(await screen.findByRole('button', { name: /^Confirmar a reserva/ }))
    const dialogo = screen.getByRole('dialog', { name: 'Confirmar reserva' })
    await userEvent.click(within(dialogo).getByRole('button', { name: 'Confirmar reserva' }))
    await userEvent.click(await within(dialogo).findByRole('button', { name: 'Atualizar reserva' }))

    await waitFor(() => expect(obterReserva).toHaveBeenCalledTimes(2))
    expect(listarHistoricoDaReserva).toHaveBeenCalledTimes(2)
  })

  it('"Voltar para as reservas" volta para a lista com os filtros de antes', async () => {
    renderizar({ pathname: '/reservas/5', state: { voltarPara: '/reservas?situacao=SOLICITADA' } })

    await screen.findByText('Ginásio A')
    await userEvent.click(screen.getByRole('link', { name: 'Voltar para as reservas' }))

    expect(screen.getByTestId('local').textContent).toBe('/reservas?situacao=SOLICITADA')
  })

  it('quem entrou direto pelo link volta para /reservas', async () => {
    renderizar()

    await screen.findByText('Ginásio A')
    await userEvent.click(screen.getByRole('link', { name: 'Voltar para as reservas' }))

    expect(screen.getByTestId('local').textContent).toBe('/reservas')
  })
})
