import { screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Route, Routes } from 'react-router'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { ErroDaApi } from '../api/cliente.ts'
import { listarEspacos, type Espaco } from '../api/espacos.ts'
import {
  obterRegrasDeAgenda,
  solicitarReserva,
  type RegrasDeAgenda,
  type Reserva,
} from '../api/reservas.ts'
import type { RespostaSucesso } from '../api/tipos.ts'
import { renderizarComProvedores, valorDaSessao } from '../testes/renderizar.tsx'
import { USUARIO_SOLICITANTE } from '../testes/usuarios.ts'
import PaginaNovaReserva from './PaginaNovaReserva.tsx'

vi.mock('../api/espacos.ts', () => ({
  listarEspacos: vi.fn(),
}))

vi.mock('../api/reservas.ts', () => ({
  solicitarReserva: vi.fn(),
  obterRegrasDeAgenda: vi.fn(),
}))

// Valores fictícios de propósito: os limites reais só existem no backend.
const REGRAS: RegrasDeAgenda = {
  horario_de_abertura: '08:00',
  horario_de_fechamento: '20:00',
  duracao_minima_em_minutos: 60,
  duracao_maxima_em_minutos: 90,
  antecedencia_maxima_em_dias: 15,
  data_limite: '2026-12-01',
}

const DICA_DA_AGENDA = 'Funcionamento das 08:00 às 20:00 · duração de 1 h a 1 h 30 min · até 01/12/2026.'

const GINASIO: Espaco = {
  id: 1,
  nome: 'Ginásio A',
  tipo: 'GINASIO',
  tipo_rotulo: 'Ginásio',
  capacidade: 50,
  ativo: true,
}

const QUADRA: Espaco = {
  id: 3,
  nome: 'Quadra Central',
  tipo: 'QUADRA_POLIESPORTIVA',
  tipo_rotulo: 'Quadra poliesportiva',
  capacidade: 20,
  ativo: true,
}

const DADOS_PREENCHIDOS = {
  espaco_id: '1',
  data: '2026-10-25',
  hora_inicio: '10:00',
  hora_fim: '11:00',
  finalidade: 'Treino do time de vôlei',
}

const RESERVA: Reserva = {
  id: 12,
  espaco_id: 1,
  solicitante: { usuario_id: 7, nome: 'Ana Souza', matricula: '202600123' },
  data: '2026-10-25',
  hora_inicio: '10:00',
  hora_fim: '11:00',
  finalidade: 'Treino do time de vôlei',
  situacao: 'SOLICITADA',
  situacao_rotulo: 'Solicitada',
  motivo_da_situacao: null,
  criada_em: '2026-10-24T09:00:00-03:00',
  acoes_disponiveis: [],
}

const MENSAGEM_DE_SUCESSO = 'Reserva solicitada com sucesso. Aguarde a confirmação do gestor.'

function promessaControlada<T>() {
  let resolver!: (valor: T) => void
  const promessa = new Promise<T>((resolve) => {
    resolver = resolve
  })
  return { promessa, resolver }
}

function renderizar(caminho = '/reservas/nova') {
  renderizarComProvedores(
    <Routes>
      <Route path="/reservas/nova" element={<PaginaNovaReserva />} />
    </Routes>,
    { caminho, sessao: valorDaSessao({ usuario: USUARIO_SOLICITANTE }) },
  )
}

function controle(rotulo: string) {
  return screen.getByLabelText(rotulo) as HTMLInputElement | HTMLSelectElement
}

async function preencherFormulario(dados: Partial<typeof DADOS_PREENCHIDOS> = DADOS_PREENCHIDOS) {
  await screen.findByLabelText('Espaço')
  if (dados.espaco_id) await userEvent.selectOptions(controle('Espaço'), dados.espaco_id)
  if (dados.data) await userEvent.type(controle('Data'), dados.data)
  if (dados.hora_inicio) await userEvent.type(controle('Início'), dados.hora_inicio)
  if (dados.hora_fim) await userEvent.type(controle('Término'), dados.hora_fim)
  if (dados.finalidade) await userEvent.type(controle('Finalidade'), dados.finalidade)
}

async function enviarFormulario() {
  await userEvent.click(screen.getByRole('button', { name: 'Solicitar reserva' }))
}

describe('PaginaNovaReserva', () => {
  beforeEach(() => {
    vi.mocked(listarEspacos).mockReset()
    vi.mocked(solicitarReserva).mockReset()
    vi.mocked(obterRegrasDeAgenda).mockReset()
    vi.mocked(listarEspacos).mockResolvedValue({
      mensagem: '2 espaços encontrados.',
      dados: [GINASIO, QUADRA],
    })
    vi.mocked(obterRegrasDeAgenda).mockResolvedValue({ mensagem: 'Regras de agenda.', dados: REGRAS })
  })

  it('mostra a dica da agenda com os valores vindos da API, sem limites nos campos', async () => {
    renderizar()

    expect(await screen.findByText(DICA_DA_AGENDA)).toBeTruthy()
    for (const rotulo of ['Data', 'Início', 'Término']) {
      const campo = controle(rotulo)
      expect(campo.getAttribute('min')).toBeNull()
      expect(campo.getAttribute('max')).toBeNull()
      expect(campo.getAttribute('step')).toBeNull()
    }
  })

  it('sem as regras de agenda, o formulário funciona sem a dica', async () => {
    vi.mocked(obterRegrasDeAgenda).mockRejectedValue(
      new ErroDaApi(0, 'SEM_CONEXAO', 'Não foi possível conectar ao servidor.'),
    )
    vi.mocked(solicitarReserva).mockResolvedValue({ mensagem: MENSAGEM_DE_SUCESSO, dados: RESERVA })
    renderizar()
    await preencherFormulario()

    await enviarFormulario()

    expect(await screen.findByRole('region', { name: 'Reserva solicitada' })).toBeTruthy()
    expect(screen.queryByText(/^Funcionamento das/)).toBeNull()
    expect(screen.queryByText('Não foi possível conectar ao servidor.')).toBeNull()
  })

  it.each([
    ['FORA_DO_HORARIO_DE_FUNCIONAMENTO', 'hora_inicio', 'Início'],
    ['DURACAO_INVALIDA', 'hora_fim', 'Término'],
    ['ANTECEDENCIA_EXCEDIDA', 'data', 'Data'],
  ])('o erro %s da agenda aparece embaixo do campo do domínio', async (codigo, campo, rotulo) => {
    const mensagem = `Mensagem do domínio para ${codigo}.`
    vi.mocked(solicitarReserva).mockRejectedValue(
      new ErroDaApi(400, codigo, mensagem, { [campo]: [mensagem] }),
    )
    renderizar()
    await preencherFormulario()

    await enviarFormulario()

    const controleComErro = controle(rotulo)
    await waitFor(() => expect(document.activeElement).toBe(controleComErro))
    expect(controleComErro.getAttribute('aria-invalid')).toBe('true')
    const idDoErro = controleComErro.getAttribute('aria-describedby') ?? ''
    expect(document.getElementById(idDoErro)?.textContent).toContain(mensagem)
    expect(screen.queryByRole('alert')).toBeNull()
  })

  it('mostra quem está solicitando, com o nome e a matrícula do usuário logado', async () => {
    renderizar()

    await screen.findByLabelText('Espaço')
    expect(screen.getByText(/^Solicitante:/).textContent).toBe('Solicitante: Bruno Lima (2026101)')
  })

  it('pede só os espaços ativos e mostra "Nome (Tipo)" no seletor', async () => {
    renderizar()

    const espaco = await screen.findByLabelText('Espaço')
    expect(listarEspacos).toHaveBeenCalledWith({ apenasAtivos: true })
    const opcoes = Array.from((espaco as HTMLSelectElement).options).map((opcao) => opcao.text)
    expect(opcoes).toEqual(['Selecione o espaço', 'Ginásio A (Ginásio)', 'Quadra Central (Quadra poliesportiva)'])
    expect(controle('Espaço').value).toBe('')
  })

  it('pré-seleciona o espaço ativo informado em ?espaco=', async () => {
    renderizar('/reservas/nova?espaco=3')

    await screen.findByLabelText('Espaço')
    expect(controle('Espaço').value).toBe('3')
  })

  it('ignora ?espaco= de um espaço inexistente ou inativo', async () => {
    renderizar('/reservas/nova?espaco=99')

    await screen.findByLabelText('Espaço')
    expect(controle('Espaço').value).toBe('')
  })

  it('sem espaços ativos, mostra o estado vazio com um link para os espaços', async () => {
    vi.mocked(listarEspacos).mockResolvedValue({ mensagem: 'Nenhum espaço encontrado.', dados: [] })

    renderizar()

    expect(await screen.findByText('Nenhum espaço disponível para reserva')).toBeTruthy()
    expect(screen.getByRole('link', { name: 'Ver espaços' }).getAttribute('href')).toBe('/espacos')
    expect(screen.queryByRole('button', { name: 'Solicitar reserva' })).toBeNull()
  })

  it('com sucesso, mostra o toast e o resumo; "Solicitar outra reserva" volta ao formulário com o espaço mantido', async () => {
    vi.mocked(solicitarReserva).mockResolvedValue({ mensagem: MENSAGEM_DE_SUCESSO, dados: RESERVA })
    renderizar()
    await preencherFormulario()

    await enviarFormulario()

    expect(await screen.findByText(MENSAGEM_DE_SUCESSO)).toBeTruthy()
    expect(solicitarReserva).toHaveBeenCalledWith(DADOS_PREENCHIDOS)
    const resumo = screen.getByRole('region', { name: 'Reserva solicitada' })
    expect(resumo.textContent).toContain('Ginásio A')
    expect(resumo.textContent).toContain('25/10/2026, 10:00–11:00')
    expect(resumo.textContent).toContain('Treino do time de vôlei')
    expect(resumo.textContent).toContain('Solicitada')
    expect(document.activeElement).toBe(screen.getByRole('heading', { name: 'Reserva solicitada' }))

    await userEvent.click(screen.getByRole('button', { name: 'Solicitar outra reserva' }))

    expect(controle('Espaço').value).toBe('1')
    expect(document.activeElement).toBe(controle('Espaço'))
    expect(controle('Data').value).toBe('')
    expect(controle('Início').value).toBe('')
    expect(controle('Término').value).toBe('')
    expect(controle('Finalidade').value).toBe('')
  })

  it('data retroativa aparece embaixo de Data, que recebe o foco, e some ao editar', async () => {
    const mensagem = 'Não é possível reservar uma data ou horário que já passou.'
    vi.mocked(solicitarReserva).mockRejectedValue(
      new ErroDaApi(400, 'DATA_RETROATIVA', mensagem, { data: [mensagem] }),
    )
    renderizar()
    await preencherFormulario()

    await enviarFormulario()

    const data = controle('Data')
    await waitFor(() => expect(document.activeElement).toBe(data))
    expect(data.getAttribute('aria-invalid')).toBe('true')
    expect(screen.getByText(mensagem)).toBeTruthy()
    expect(screen.queryByRole('alert')).toBeNull()

    await userEvent.clear(data)

    expect(data.getAttribute('aria-invalid')).toBeNull()
    expect(screen.queryByText(mensagem)).toBeNull()
  })

  it('término antes do início aparece embaixo de Término', async () => {
    const mensagem = 'O horário de término deve ser posterior ao de início.'
    vi.mocked(solicitarReserva).mockRejectedValue(
      new ErroDaApi(400, 'HORARIO_INVALIDO', mensagem, { hora_fim: [mensagem] }),
    )
    renderizar()
    await preencherFormulario()

    await enviarFormulario()

    const termino = controle('Término')
    await waitFor(() => expect(document.activeElement).toBe(termino))
    expect(termino.getAttribute('aria-invalid')).toBe('true')
    expect(controle('Início').getAttribute('aria-invalid')).toBeNull()
    expect(screen.getByText(mensagem)).toBeTruthy()
  })

  it('conflito de horário aparece num aviso no topo, que recebe o foco, e mantém os valores', async () => {
    const mensagem =
      'Este espaço já tem uma reserva Confirmada em 25/10/2026 10:00–11:00. Escolha outro horário.'
    vi.mocked(solicitarReserva).mockRejectedValue(
      new ErroDaApi(409, 'CONFLITO_DE_HORARIO', mensagem),
    )
    renderizar()
    await preencherFormulario()

    await enviarFormulario()

    const aviso = await screen.findByRole('alert')
    expect(aviso.textContent).toContain(mensagem)
    await waitFor(() => expect(document.activeElement?.contains(aviso)).toBe(true))
    expect(controle('Espaço').value).toBe('1')
    expect(controle('Data').value).toBe('2026-10-25')
    expect(controle('Início').value).toBe('10:00')
    expect(controle('Término').value).toBe('11:00')
    expect(controle('Finalidade').value).toBe('Treino do time de vôlei')
  })

  it('sem login, mostra a mensagem da API no aviso do topo', async () => {
    vi.mocked(solicitarReserva).mockRejectedValue(
      new ErroDaApi(401, 'NAO_AUTENTICADO', 'Faça login para continuar.'),
    )
    renderizar()
    await preencherFormulario()

    await enviarFormulario()

    expect((await screen.findByRole('alert')).textContent).toContain('Faça login para continuar.')
  })

  it('desabilita o botão enquanto envia', async () => {
    const pendente = promessaControlada<RespostaSucesso<Reserva>>()
    vi.mocked(solicitarReserva).mockReturnValue(pendente.promessa)
    renderizar()
    await preencherFormulario()

    await enviarFormulario()

    const botao = screen.getByRole('button', { name: 'Enviando solicitação...' })
    expect((botao as HTMLButtonElement).disabled).toBe(true)

    pendente.resolver({ mensagem: MENSAGEM_DE_SUCESSO, dados: RESERVA })

    expect(await screen.findByRole('region', { name: 'Reserva solicitada' })).toBeTruthy()
  })

  it('mostra um erro com "Tentar novamente" quando os espaços não carregam', async () => {
    vi.mocked(listarEspacos)
      .mockRejectedValueOnce(new ErroDaApi(0, 'SEM_CONEXAO', 'Não foi possível conectar ao servidor.'))
      .mockResolvedValueOnce({ mensagem: '1 espaço encontrado.', dados: [GINASIO] })
    renderizar()

    await userEvent.click(await screen.findByRole('button', { name: 'Tentar novamente' }))

    expect(await screen.findByLabelText('Espaço')).toBeTruthy()
  })
})
