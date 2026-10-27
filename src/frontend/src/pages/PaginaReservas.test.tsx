import { fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Link, MemoryRouter, Route, Routes, useLocation } from 'react-router'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { ErroDaApi } from '../api/cliente.ts'
import { listarEspacos, type Espaco } from '../api/espacos.ts'
import {
  alterarSituacaoReserva,
  listarReservas,
  listarSituacoesDeReserva,
  type FiltrosDeReservas,
  type Reserva,
} from '../api/reservas.ts'
import type { RespostaSucesso } from '../api/tipos.ts'
import MensagensProvider from '../components/mensagens/MensagensProvider.tsx'
import PaginaReservas, { ATRASO_DO_SOLICITANTE_MS } from './PaginaReservas.tsx'

vi.mock('../api/espacos.ts', () => ({
  listarEspacos: vi.fn(),
}))

vi.mock('../api/reservas.ts', () => ({
  alterarSituacaoReserva: vi.fn(),
  listarReservas: vi.fn(),
  listarSituacoesDeReserva: vi.fn(),
}))

const SITUACOES = [
  { valor: 'SOLICITADA', rotulo: 'Solicitada' },
  { valor: 'CONFIRMADA', rotulo: 'Confirmada' },
  { valor: 'CANCELADA', rotulo: 'Cancelada' },
]

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

const SOLICITADA: Reserva = {
  id: 10,
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
  acoes_disponiveis: [
    { situacao: 'CONFIRMADA', rotulo: 'Confirmar', exige_motivo: false },
    { situacao: 'RECUSADA', rotulo: 'Recusar', exige_motivo: true },
    { situacao: 'CANCELADA', rotulo: 'Cancelar', exige_motivo: true },
  ],
}

const CANCELADA: Reserva = {
  ...SOLICITADA,
  id: 11,
  espaco_id: 2,
  solicitante: { usuario_id: 2, nome: 'Bruno Lima', matricula: '2026002' },
  data: '2026-11-12',
  hora_inicio: '14:00',
  hora_fim: '15:30',
  finalidade: 'Campeonato interno',
  situacao: 'CANCELADA',
  situacao_rotulo: 'Cancelada',
  motivo_da_situacao: 'Chuva forte',
  acoes_disponiveis: [],
}

function filtros(sobrescritas: FiltrosDeReservas = {}): Required<FiltrosDeReservas> {
  return { espaco: '', situacao: '', data: '', solicitante: '', minhas: false, ...sobrescritas }
}

function BuscaAtual() {
  return <output data-testid="busca">{useLocation().search}</output>
}

function renderizar(caminho = '/reservas') {
  render(
    <MensagensProvider>
      <MemoryRouter initialEntries={[caminho]}>
        <Routes>
          <Route
            path="/reservas"
            element={
              <>
                <PaginaReservas />
                <BuscaAtual />
                <Link to="/reservas">Ir para reservas</Link>
              </>
            }
          />
        </Routes>
      </MemoryRouter>
    </MensagensProvider>,
  )
}

function busca() {
  return screen.getByTestId('busca').textContent
}

function controle<T extends HTMLElement = HTMLInputElement>(rotulo: string) {
  return screen.getByLabelText(rotulo) as T
}

async function seletorCarregado(rotulo: string) {
  const seletor = controle<HTMLSelectElement>(rotulo)
  await waitFor(() => expect(seletor.disabled).toBe(false))
  return seletor
}

function esperar(ms: number) {
  return new Promise((resolver) => setTimeout(resolver, ms))
}

describe('PaginaReservas', () => {
  beforeEach(() => {
    vi.mocked(listarEspacos).mockReset()
    vi.mocked(listarSituacoesDeReserva).mockReset()
    vi.mocked(listarReservas).mockReset()
    vi.mocked(listarEspacos).mockResolvedValue({
      mensagem: '2 espaços encontrados.',
      dados: [GINASIO, QUADRA],
    })
    vi.mocked(listarSituacoesDeReserva).mockResolvedValue({
      mensagem: 'Situações de reserva disponíveis.',
      dados: SITUACOES,
    })
    vi.mocked(listarReservas).mockResolvedValue({
      mensagem: '2 reservas encontradas.',
      dados: [SOLICITADA, CANCELADA],
    })
  })

  it('mostra a contagem e cada reserva com data, espaço, solicitante e situação', async () => {
    renderizar()

    const tabela = await screen.findByRole('table', { name: '2 reservas encontradas.' })
    const linhas = within(tabela).getAllByRole('row')
    expect(linhas).toHaveLength(3)
    expect(within(linhas[1]).getByRole('rowheader').textContent).toBe('10/11/2026, 10:00–11:00')
    expect(linhas[1].textContent).toContain('Ginásio A')
    expect(linhas[1].textContent).toContain('Ana Souza')
    expect(linhas[1].textContent).toContain('2026001')
    expect(linhas[1].textContent).toContain('Treino de vôlei')
    expect(within(linhas[1]).getByText('Solicitada')).toBeTruthy()
    expect(listarEspacos).toHaveBeenCalledWith()
    expect(listarReservas).toHaveBeenCalledWith(filtros())
  })

  it('mostra o motivo logo abaixo da situação de uma reserva cancelada', async () => {
    renderizar()

    const tabela = await screen.findByRole('table')
    const linhaCancelada = within(tabela).getAllByRole('row')[2]
    expect(linhaCancelada.textContent).toContain('Quadra Antiga')
    expect(within(linhaCancelada).getByText('Cancelada')).toBeTruthy()
    expect(within(linhaCancelada).getByText('Motivo: Chuva forte')).toBeTruthy()
    expect(within(tabela).getAllByText(/^Motivo:/)).toHaveLength(1)
  })

  it('lista os espaços no filtro, marcando os inativos', async () => {
    renderizar()

    const seletor = await seletorCarregado('Espaço')
    const opcoes = within(seletor)
      .getAllByRole('option')
      .map((opcao) => opcao.textContent)
    expect(opcoes).toEqual(['Todos os espaços', 'Ginásio A', 'Quadra Antiga (inativo)'])
  })

  it('o filtro de espaço grava na URL e consulta com ele', async () => {
    renderizar()

    await userEvent.selectOptions(await seletorCarregado('Espaço'), '2')

    expect(busca()).toBe('?espaco=2')
    expect(listarReservas).toHaveBeenLastCalledWith(filtros({ espaco: '2' }))
  })

  it('o filtro de situação grava na URL e consulta com ele', async () => {
    renderizar()

    await userEvent.selectOptions(await seletorCarregado('Situação'), 'CONFIRMADA')

    expect(busca()).toBe('?situacao=CONFIRMADA')
    expect(listarReservas).toHaveBeenLastCalledWith(filtros({ situacao: 'CONFIRMADA' }))
  })

  it('o filtro de data grava na URL e consulta com ele', async () => {
    renderizar()
    await screen.findByRole('table')

    fireEvent.change(controle('Data'), { target: { value: '2026-11-10' } })

    expect(busca()).toBe('?data=2026-11-10')
    await waitFor(() =>
      expect(listarReservas).toHaveBeenLastCalledWith(filtros({ data: '2026-11-10' })),
    )
  })

  it('combina espaço e situação numa mesma consulta', async () => {
    renderizar()

    await userEvent.selectOptions(await seletorCarregado('Espaço'), '1')
    await userEvent.selectOptions(await seletorCarregado('Situação'), 'SOLICITADA')

    expect(busca()).toBe('?espaco=1&situacao=SOLICITADA')
    expect(listarReservas).toHaveBeenLastCalledWith(
      filtros({ espaco: '1', situacao: 'SOLICITADA' }),
    )
  })

  it('o filtro de solicitante consulta uma vez só, depois que a pessoa para de digitar', async () => {
    renderizar()
    await screen.findByRole('table')

    await userEvent.type(controle('Solicitante'), 'ana')

    await waitFor(() => expect(busca()).toBe('?solicitante=ana'))
    await waitFor(() =>
      expect(listarReservas).toHaveBeenLastCalledWith(filtros({ solicitante: 'ana' })),
    )
    const consultasComSolicitante = vi
      .mocked(listarReservas)
      .mock.calls.filter(([filtrosDaChamada]) => filtrosDaChamada?.solicitante)
    expect(consultasComSolicitante).toHaveLength(1)
  })

  it('"Somente minhas reservas" consulta com minhas=true', async () => {
    renderizar()
    await screen.findByRole('table')

    await userEvent.click(controle('Somente minhas reservas'))

    expect(busca()).toBe('?minhas=true')
    expect(listarReservas).toHaveBeenLastCalledWith(filtros({ minhas: true }))
  })

  it('abrir a página com filtros na URL preenche os campos e consulta com eles', async () => {
    renderizar('/reservas?espaco=2&situacao=CANCELADA&data=2026-11-12&solicitante=bruno&minhas=true')

    expect((await seletorCarregado('Espaço')).value).toBe('2')
    expect((await seletorCarregado('Situação')).value).toBe('CANCELADA')
    expect(controle('Data').value).toBe('2026-11-12')
    expect(controle('Solicitante').value).toBe('bruno')
    expect(controle('Somente minhas reservas').checked).toBe(true)
    expect(listarReservas).toHaveBeenCalledWith(
      filtros({
        espaco: '2',
        situacao: 'CANCELADA',
        data: '2026-11-12',
        solicitante: 'bruno',
        minhas: true,
      }),
    )
  })

  it('"Limpar filtros" só aparece com filtro ativo e limpa a URL e os campos', async () => {
    renderizar('/reservas?situacao=CANCELADA&solicitante=bruno')
    await screen.findByRole('table')

    await userEvent.click(screen.getByRole('button', { name: 'Limpar filtros' }))

    expect(busca()).toBe('')
    expect(controle('Solicitante').value).toBe('')
    expect(screen.queryByRole('button', { name: 'Limpar filtros' })).toBeNull()
    await waitFor(() => expect(listarReservas).toHaveBeenLastCalledWith(filtros()))
  })

  it('um texto de solicitante digitado logo antes de limpar não volta para a URL', async () => {
    renderizar('/reservas?situacao=CANCELADA')
    await screen.findByRole('table')

    await userEvent.type(controle('Solicitante'), 'xyz')
    await userEvent.click(screen.getByRole('button', { name: 'Limpar filtros' }))
    await esperar(ATRASO_DO_SOLICITANTE_MS + 100)

    expect(busca()).toBe('')
    expect(controle('Solicitante').value).toBe('')
  })

  it('quando a URL muda por fora (menu), o campo de solicitante acompanha', async () => {
    renderizar('/reservas?solicitante=ana')
    await screen.findByRole('table')
    expect(controle('Solicitante').value).toBe('ana')

    await userEvent.click(screen.getByRole('link', { name: 'Ir para reservas' }))

    expect(busca()).toBe('')
    expect(controle('Solicitante').value).toBe('')
    await waitFor(() => expect(listarReservas).toHaveBeenLastCalledWith(filtros()))
    await esperar(ATRASO_DO_SOLICITANTE_MS + 100)
    expect(busca()).toBe('')
  })

  it('o texto que chega à URL não apaga o que a pessoa continuou digitando', async () => {
    renderizar()
    await screen.findByRole('table')

    await userEvent.type(controle('Solicitante'), 'ana')
    await waitFor(() => expect(busca()).toBe('?solicitante=ana'))
    await userEvent.type(controle('Solicitante'), ' souza')

    expect(controle('Solicitante').value).toBe('ana souza')
    await waitFor(() => expect(busca()).toBe('?solicitante=ana+souza'))
    expect(controle('Solicitante').value).toBe('ana souza')
  })

  it('sem filtros e sem reservas, convida a solicitar uma reserva', async () => {
    vi.mocked(listarReservas).mockResolvedValue({
      mensagem: 'Nenhuma reserva encontrada.',
      dados: [],
    })

    renderizar()

    expect(await screen.findByText('Nenhuma reserva registrada')).toBeTruthy()
    expect(
      screen.getByRole('link', { name: 'Solicitar reserva' }).getAttribute('href'),
    ).toBe('/reservas/nova')
    expect(screen.queryByRole('button', { name: 'Limpar filtros' })).toBeNull()
  })

  it('com filtros e sem reservas, oferece "Limpar filtros"', async () => {
    vi.mocked(listarReservas).mockResolvedValueOnce({
      mensagem: 'Nenhuma reserva encontrada.',
      dados: [],
    })
    renderizar('/reservas?situacao=CONFIRMADA')

    const vazio = (await screen.findByText('Nenhuma reserva encontrada')).parentElement!
    await userEvent.click(within(vazio).getByRole('button', { name: 'Limpar filtros' }))

    expect(busca()).toBe('')
    expect(await screen.findByRole('table')).toBeTruthy()
  })

  it('falha ao carregar mostra a mensagem e "Tentar novamente" consulta de novo', async () => {
    vi.mocked(listarReservas).mockRejectedValueOnce(
      new ErroDaApi(0, 'SEM_CONEXAO', 'Não foi possível conectar ao servidor.'),
    )
    renderizar()

    expect((await screen.findByRole('alert')).textContent).toContain(
      'Não foi possível conectar ao servidor.',
    )
    await userEvent.click(screen.getByRole('button', { name: 'Tentar novamente' }))

    expect(await screen.findByRole('table')).toBeTruthy()
    expect(listarReservas).toHaveBeenCalledTimes(2)
  })

  it('sem login mostra a mensagem da API no lugar da tabela', async () => {
    vi.mocked(listarReservas).mockRejectedValue(
      new ErroDaApi(401, 'NAO_AUTENTICADO', 'Faça login para continuar.'),
    )

    renderizar()

    expect((await screen.findByRole('alert')).textContent).toContain('Faça login para continuar.')
    expect(screen.queryByRole('table')).toBeNull()
  })

  it('se os espaços falharem, a tabela aparece com "Espaço #<id>" e um aviso', async () => {
    vi.mocked(listarEspacos).mockRejectedValue(
      new ErroDaApi(0, 'SEM_CONEXAO', 'Não foi possível conectar ao servidor.'),
    )

    renderizar()

    const tabela = await screen.findByRole('table')
    const linhas = within(tabela).getAllByRole('row')
    expect(linhas[1].textContent).toContain('Espaço #1')
    expect(linhas[2].textContent).toContain('Espaço #2')
    expect(screen.getByText(/Não foi possível carregar os espaços/)).toBeTruthy()
    expect(controle<HTMLSelectElement>('Espaço').disabled).toBe(true)
    expect((await seletorCarregado('Situação')).disabled).toBe(false)
  })
})

describe('PaginaReservas — ações de situação', () => {
  const RESERVA_ALTERADA: RespostaSucesso<Reserva> = {
    mensagem: 'Reserva recusada com sucesso.',
    dados: { ...SOLICITADA, situacao: 'RECUSADA', situacao_rotulo: 'Recusada' },
  }

  beforeEach(() => {
    vi.mocked(listarEspacos).mockReset()
    vi.mocked(listarSituacoesDeReserva).mockReset()
    vi.mocked(listarReservas).mockReset()
    vi.mocked(alterarSituacaoReserva).mockReset()
    vi.mocked(listarEspacos).mockResolvedValue({
      mensagem: '2 espaços encontrados.',
      dados: [GINASIO, QUADRA],
    })
    vi.mocked(listarSituacoesDeReserva).mockResolvedValue({
      mensagem: 'Situações de reserva disponíveis.',
      dados: SITUACOES,
    })
    vi.mocked(listarReservas).mockResolvedValue({
      mensagem: '2 reservas encontradas.',
      dados: [SOLICITADA, CANCELADA],
    })
    vi.mocked(alterarSituacaoReserva).mockResolvedValue(RESERVA_ALTERADA)
  })

  async function abrir(rotulo: string) {
    renderizar()
    const botao = await screen.findByRole('button', {
      name: `${rotulo} a reserva de 10/11/2026, 10:00–11:00 em Ginásio A`,
    })
    await userEvent.click(botao)
    return { botao, dialogo: screen.getByRole('dialog', { name: `${rotulo} reserva` }) }
  }

  function botaoNoDialogo(dialogo: HTMLElement, nome: string) {
    return within(dialogo).getByRole('button', { name: nome }) as HTMLButtonElement
  }

  it('"Confirmar" abre o diálogo com o resumo e sem campo de motivo', async () => {
    const { dialogo } = await abrir('Confirmar')

    expect((dialogo as HTMLDialogElement).open).toBe(true)
    expect(dialogo.textContent).toContain('Ginásio A')
    expect(dialogo.textContent).toContain('10/11/2026, 10:00–11:00')
    expect(dialogo.textContent).toContain('Ana Souza (2026001)')
    expect(within(dialogo).queryByLabelText('Motivo')).toBeNull()
    expect(document.activeElement).toBe(botaoNoDialogo(dialogo, 'Voltar'))
  })

  it('"Recusar" abre o diálogo com o campo de motivo em foco', async () => {
    const { dialogo } = await abrir('Recusar')

    expect(document.activeElement).toBe(within(dialogo).getByLabelText('Motivo'))
    expect(dialogo.textContent).toContain('Explique ao solicitante o motivo.')
  })

  it('enviar recusa com o motivo, mostra a mensagem da API, fecha e recarrega', async () => {
    const { dialogo } = await abrir('Recusar')

    await userEvent.type(within(dialogo).getByLabelText('Motivo'), 'Quadra em reforma')
    await userEvent.click(botaoNoDialogo(dialogo, 'Recusar reserva'))

    expect(alterarSituacaoReserva).toHaveBeenCalledWith(10, {
      situacao: 'RECUSADA',
      motivo: 'Quadra em reforma',
    })
    expect(await screen.findByText('Reserva recusada com sucesso.')).toBeTruthy()
    expect(screen.queryByRole('dialog')).toBeNull()
    await waitFor(() => expect(listarReservas).toHaveBeenCalledTimes(2))
    const regiao = await screen.findByRole('region', { name: '2 reservas encontradas.' })
    await waitFor(() => expect(document.activeElement).toBe(regiao))
  })

  it('confirmar envia só a situação, sem motivo', async () => {
    const { dialogo } = await abrir('Confirmar')

    await userEvent.click(botaoNoDialogo(dialogo, 'Confirmar reserva'))

    expect(alterarSituacaoReserva).toHaveBeenCalledWith(10, { situacao: 'CONFIRMADA' })
  })

  it('erro no motivo aparece embaixo do campo, que recebe o foco', async () => {
    vi.mocked(alterarSituacaoReserva).mockRejectedValue(
      new ErroDaApi(400, 'MOTIVO_OBRIGATORIO', 'Informe o motivo.', {
        motivo: ['Informe o motivo para recusar a reserva.'],
      }),
    )
    const { dialogo } = await abrir('Recusar')

    await userEvent.click(botaoNoDialogo(dialogo, 'Recusar reserva'))

    const motivo = within(dialogo).getByLabelText('Motivo')
    await waitFor(() => expect(motivo.getAttribute('aria-invalid')).toBe('true'))
    expect(dialogo.textContent).toContain('Informe o motivo para recusar a reserva.')
    expect(document.activeElement).toBe(motivo)
    expect(within(dialogo).queryByRole('alert')).toBeNull()
    expect(listarReservas).toHaveBeenCalledTimes(1)
  })

  it('409 mostra o aviso no diálogo com "Atualizar lista", que fecha e recarrega', async () => {
    vi.mocked(alterarSituacaoReserva).mockRejectedValue(
      new ErroDaApi(
        409,
        'TRANSICAO_DE_SITUACAO_INVALIDA',
        'Não é possível alterar uma reserva Confirmada para Confirmada.',
      ),
    )
    const { dialogo } = await abrir('Confirmar')

    await userEvent.click(botaoNoDialogo(dialogo, 'Confirmar reserva'))

    const aviso = await within(dialogo).findByRole('alert')
    expect(aviso.textContent).toContain('Não é possível alterar uma reserva Confirmada')
    await userEvent.click(botaoNoDialogo(dialogo, 'Atualizar lista'))

    expect(screen.queryByRole('dialog')).toBeNull()
    await waitFor(() => expect(listarReservas).toHaveBeenCalledTimes(2))
    expect(alterarSituacaoReserva).toHaveBeenCalledTimes(1)
  })

  it('401 mostra o aviso no diálogo sem "Atualizar lista"', async () => {
    vi.mocked(alterarSituacaoReserva).mockRejectedValue(
      new ErroDaApi(401, 'NAO_AUTENTICADO', 'Faça login para continuar.'),
    )
    const { dialogo } = await abrir('Confirmar')

    await userEvent.click(botaoNoDialogo(dialogo, 'Confirmar reserva'))

    const aviso = await within(dialogo).findByRole('alert')
    expect(aviso.textContent).toContain('Faça login para continuar.')
    expect(within(dialogo).queryByRole('button', { name: 'Atualizar lista' })).toBeNull()
  })

  it('"Voltar" fecha sem chamar a API e devolve o foco ao botão da linha', async () => {
    const { botao, dialogo } = await abrir('Cancelar')

    await userEvent.click(botaoNoDialogo(dialogo, 'Voltar'))

    expect(screen.queryByRole('dialog')).toBeNull()
    expect(alterarSituacaoReserva).not.toHaveBeenCalled()
    expect(document.activeElement).toBe(botao)
  })

  it('Esc fecha sem chamar a API e devolve o foco ao botão da linha', async () => {
    const { botao } = await abrir('Recusar')

    await userEvent.keyboard('{Escape}')

    expect(screen.queryByRole('dialog')).toBeNull()
    expect(alterarSituacaoReserva).not.toHaveBeenCalled()
    expect(document.activeElement).toBe(botao)
  })

  it('os botões ficam desabilitados, com "Enviando...", enquanto envia', async () => {
    let resolver!: (resposta: RespostaSucesso<Reserva>) => void
    vi.mocked(alterarSituacaoReserva).mockReturnValue(
      new Promise((resolve) => {
        resolver = resolve
      }),
    )
    const { dialogo } = await abrir('Confirmar')

    await userEvent.click(botaoNoDialogo(dialogo, 'Confirmar reserva'))

    expect(botaoNoDialogo(dialogo, 'Enviando...').disabled).toBe(true)
    expect(botaoNoDialogo(dialogo, 'Voltar').disabled).toBe(true)
    resolver({ ...RESERVA_ALTERADA, mensagem: 'Reserva confirmada com sucesso.' })
    expect(await screen.findByText('Reserva confirmada com sucesso.')).toBeTruthy()
    expect(screen.queryByRole('dialog')).toBeNull()
  })
})
