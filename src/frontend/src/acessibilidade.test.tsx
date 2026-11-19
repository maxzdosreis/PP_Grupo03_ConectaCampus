import { fireEvent, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeAll, beforeEach, describe, expect, it, vi } from 'vitest'
import paginaHtml from '../index.html?raw'
import type { Usuario } from './api/autenticacao.ts'
import { alterarSenha } from './api/autenticacao.ts'
import { ErroDaApi } from './api/cliente.ts'
import {
  cadastrarEspaco,
  listarEspacos,
  listarTiposDeEspaco,
  obterEspaco,
  type Espaco,
} from './api/espacos.ts'
import {
  listarHistoricoDaReserva,
  listarReservas,
  listarSituacoesDeReserva,
  obterOcupacaoDoDia,
  obterRegrasDeAgenda,
  obterReserva,
  solicitarReserva,
  type RegistroDeSituacao,
  type Reserva,
} from './api/reservas.ts'
import { consultarSaude } from './api/saude.ts'
import type { Paginacao, RespostaSucesso } from './api/tipos.ts'
import { listarUsuarios, type UsuarioGerenciado } from './api/usuarios.ts'
import RotasDaAplicacao from './RotasDaAplicacao.tsx'
import { violacoesDeAcessibilidade } from './testes/acessibilidade.ts'
import { renderizarComProvedores, valorDaSessao } from './testes/renderizar.tsx'
import { USUARIO_GESTOR, USUARIO_SOLICITANTE } from './testes/usuarios.ts'

vi.mock('./api/autenticacao.ts', () => ({ alterarSenha: vi.fn() }))
vi.mock('./api/saude.ts', () => ({ consultarSaude: vi.fn() }))
vi.mock('./api/espacos.ts', () => ({
  ativarEspaco: vi.fn(),
  cadastrarEspaco: vi.fn(),
  desativarEspaco: vi.fn(),
  editarEspaco: vi.fn(),
  listarEspacos: vi.fn(),
  listarTiposDeEspaco: vi.fn(),
  obterEspaco: vi.fn(),
}))
vi.mock('./api/reservas.ts', () => ({
  alterarSituacaoReserva: vi.fn(),
  listarHistoricoDaReserva: vi.fn(),
  listarReservas: vi.fn(),
  listarSituacoesDeReserva: vi.fn(),
  obterOcupacaoDoDia: vi.fn(),
  obterRegrasDeAgenda: vi.fn(),
  obterReserva: vi.fn(),
  solicitarReserva: vi.fn(),
}))
vi.mock('./api/usuarios.ts', () => ({ alterarUsuario: vi.fn(), listarUsuarios: vi.fn() }))

const GINASIO: Espaco = {
  id: 1,
  nome: 'Ginásio A',
  tipo: 'GINASIO',
  tipo_rotulo: 'Ginásio',
  capacidade: 50,
  ativo: true,
  abertura: '07:00',
  fechamento: '00:00',
}

const QUADRA_INATIVA: Espaco = {
  ...GINASIO,
  id: 2,
  nome: 'Quadra de Tênis 2',
  tipo: 'QUADRA_DE_TENIS',
  tipo_rotulo: 'Quadra de tênis',
  capacidade: 4,
  ativo: false,
}

const RESERVA: Reserva = {
  id: 5,
  espaco_id: 1,
  solicitante: { usuario_id: 2, nome: 'Bruno Lima', matricula: '2026101' },
  data: '2026-11-25',
  hora_inicio: '10:00',
  hora_fim: '11:00',
  finalidade: 'Treino de vôlei',
  situacao: 'SOLICITADA',
  situacao_rotulo: 'Solicitada',
  motivo_da_situacao: null,
  criada_em: '2026-11-19T09:15:42-03:00',
  acoes_disponiveis: [
    { situacao: 'CONFIRMADA', rotulo: 'Confirmar', exige_motivo: false },
    { situacao: 'RECUSADA', rotulo: 'Recusar', exige_motivo: true },
    { situacao: 'CANCELADA', rotulo: 'Cancelar', exige_motivo: true },
  ],
}

const RESERVA_CANCELADA: Reserva = {
  ...RESERVA,
  id: 6,
  data: '2026-11-26',
  situacao: 'CANCELADA',
  situacao_rotulo: 'Cancelada',
  motivo_da_situacao: 'Chuva prevista.',
  acoes_disponiveis: [],
}

const HISTORICO: RegistroDeSituacao[] = [
  {
    situacao_anterior: null,
    situacao_anterior_rotulo: null,
    situacao_nova: 'SOLICITADA',
    situacao_nova_rotulo: 'Solicitada',
    motivo: null,
    autor: { nome: 'Bruno Lima' },
    registrado_em: '2026-11-19T09:15:42-03:00',
    resultado: 'ACEITA',
  },
  {
    situacao_anterior: 'SOLICITADA',
    situacao_anterior_rotulo: 'Solicitada',
    situacao_nova: 'SOLICITADA',
    situacao_nova_rotulo: 'Solicitada',
    motivo: null,
    autor: { nome: 'Bruno Lima' },
    registrado_em: '2026-11-19T10:00:00-03:00',
    resultado: 'RECUSADA',
    situacao_pedida: 'CONFIRMADA',
    situacao_pedida_rotulo: 'Confirmada',
    codigo_do_erro: 'ACAO_NAO_PERMITIDA',
  },
]

const USUARIOS: UsuarioGerenciado[] = [
  {
    id: 1,
    nome: 'Carla Mendes',
    email: 'carla.mendes@exemplo.com',
    matricula: '2026900',
    perfil: 'GESTOR',
    perfil_rotulo: 'Gestor',
    eh_gestor: true,
    ativo: true,
    cadastrado_em: '2026-11-01T08:00:00-03:00',
    ultimo_acesso: '2026-11-19T08:00:00-03:00',
  },
  {
    id: 2,
    nome: 'Bruno Lima',
    email: 'bruno.lima@exemplo.com',
    matricula: '2026101',
    perfil: 'SOLICITANTE',
    perfil_rotulo: 'Solicitante',
    eh_gestor: false,
    ativo: true,
    cadastrado_em: '2026-11-01T08:00:00-03:00',
    ultimo_acesso: null,
  },
]

function paginacao(total: number): Paginacao {
  return { pagina: 1, tamanho: 20, total, total_de_paginas: total ? 1 : 0 }
}

function sucesso<T>(dados: T, extra: Partial<RespostaSucesso<T>> = {}): RespostaSucesso<T> {
  return { mensagem: 'Mensagem da API.', dados, ...extra }
}

function nuncaResponde() {
  return new Promise<never>(() => {})
}

const SEM_CONEXAO = new ErroDaApi(0, 'SEM_CONEXAO', 'Não foi possível falar com o servidor.')

function abrir(caminho: string, usuario: Usuario | null = USUARIO_GESTOR) {
  return renderizarComProvedores(<RotasDaAplicacao />, {
    caminho,
    sessao: valorDaSessao({ usuario }),
  })
}

async function esperarSemViolacoes() {
  expect(await violacoesDeAcessibilidade()).toEqual([])
}

vi.setConfig({ testTimeout: 30_000 })

beforeAll(() => {
  document.documentElement.lang = 'pt-BR'
})

beforeEach(() => {
  vi.mocked(consultarSaude).mockResolvedValue(sucesso({ banco: 'ok', cache: 'ok' }))
  vi.mocked(listarEspacos).mockResolvedValue(sucesso([GINASIO, QUADRA_INATIVA]))
  vi.mocked(listarTiposDeEspaco).mockResolvedValue(
    sucesso([
      { valor: 'GINASIO', rotulo: 'Ginásio' },
      { valor: 'QUADRA_DE_TENIS', rotulo: 'Quadra de tênis' },
    ]),
  )
  vi.mocked(obterEspaco).mockResolvedValue(sucesso(GINASIO))
  vi.mocked(listarSituacoesDeReserva).mockResolvedValue(
    sucesso([
      { valor: 'SOLICITADA', rotulo: 'Solicitada' },
      { valor: 'CANCELADA', rotulo: 'Cancelada' },
    ]),
  )
  vi.mocked(listarReservas).mockResolvedValue(
    sucesso(
      { reservas: [RESERVA, RESERVA_CANCELADA], paginacao: paginacao(2) },
      { mensagem: '2 reservas encontradas.' },
    ),
  )
  vi.mocked(obterReserva).mockResolvedValue(sucesso(RESERVA))
  vi.mocked(listarHistoricoDaReserva).mockResolvedValue(sucesso(HISTORICO))
  vi.mocked(obterRegrasDeAgenda).mockResolvedValue(
    sucesso({
      duracao_sugerida_em_minutos: 60,
      duracao_minima_em_minutos: 30,
      duracao_maxima_em_minutos: 180,
      antecedencia_maxima_em_dias: 30,
      data_limite: '2026-12-19',
    }),
  )
  vi.mocked(obterOcupacaoDoDia).mockResolvedValue(
    sucesso(
      {
        data: '2026-11-25',
        horario_de_abertura: '07:00',
        horario_de_fechamento: '00:00',
        reservavel: true,
        motivo_indisponivel: null,
        ocupados: [
          { hora_inicio: '10:00', hora_fim: '11:00', situacao: 'SOLICITADA', situacao_rotulo: 'Solicitada' },
        ],
        livres: [
          { hora_inicio: '07:00', hora_fim: '10:00' },
          { hora_inicio: '11:00', hora_fim: '00:00' },
        ],
      },
      { mensagem: '1 horário ocupado neste dia.' },
    ),
  )
  vi.mocked(listarUsuarios).mockResolvedValue(
    sucesso({ usuarios: USUARIOS, paginacao: paginacao(2) }, { mensagem: '2 usuários encontrados.' }),
  )
})

describe('Acessibilidade (axe, sem contraste) — página inicial e 404', () => {
  it('inicial para o visitante, com a API no ar', async () => {
    abrir('/', null)
    await screen.findByRole('heading', { level: 1 })
    await screen.findByText('Mensagem da API.')
    await esperarSemViolacoes()
  })

  it('inicial carregando a situação da API', async () => {
    vi.mocked(consultarSaude).mockReturnValue(nuncaResponde())
    abrir('/', USUARIO_SOLICITANTE)
    await screen.findByRole('heading', { level: 1 })
    await esperarSemViolacoes()
  })

  it('inicial com a API fora do ar', async () => {
    vi.mocked(consultarSaude).mockRejectedValue(SEM_CONEXAO)
    abrir('/', null)
    await screen.findByText('Não foi possível falar com o servidor.')
    await esperarSemViolacoes()
  })

  it('página não encontrada', async () => {
    abrir('/nao-existe', null)
    await screen.findByRole('heading', { level: 1 })
    await esperarSemViolacoes()
  })
})

describe('Acessibilidade — entrar e cadastrar', () => {
  it('entrar, vazio', async () => {
    abrir('/entrar', null)
    await screen.findByRole('button', { name: 'Entrar' })
    await esperarSemViolacoes()
  })

  it('entrar com erro de campo e com erro geral da API', async () => {
    const sessao = valorDaSessao()
    vi.mocked(sessao.entrar)
      .mockRejectedValueOnce(
        new ErroDaApi(400, 'DADOS_INVALIDOS', 'Verifique os dados informados.', {
          email: ['Informe um endereço de email válido.'],
        }),
      )
      .mockRejectedValueOnce(new ErroDaApi(401, 'CREDENCIAIS_INVALIDAS', 'E-mail ou senha incorretos.'))
    renderizarComProvedores(<RotasDaAplicacao />, { caminho: '/entrar', sessao })
    await userEvent.click(await screen.findByRole('button', { name: 'Entrar' }))
    await screen.findByText('Informe um endereço de email válido.')
    await esperarSemViolacoes()
    await userEvent.click(screen.getByRole('button', { name: 'Entrar' }))
    await screen.findByText('E-mail ou senha incorretos.')
    await esperarSemViolacoes()
  })

  it('cadastro com erros de campo', async () => {
    const sessao = valorDaSessao()
    vi.mocked(sessao.cadastrarEEntrar).mockRejectedValueOnce(
      new ErroDaApi(400, 'SENHA_FRACA', 'Esta senha é muito curta.', {
        senha: ['Esta senha é muito curta.'],
        matricula: ['A matrícula deve ter só dígitos de 0 a 9.'],
      }),
    )
    renderizarComProvedores(<RotasDaAplicacao />, { caminho: '/cadastro', sessao })
    await esperarSemViolacoes()
    await userEvent.click(await screen.findByRole('button', { name: 'Criar conta' }))
    await screen.findByText('Esta senha é muito curta.')
    await esperarSemViolacoes()
  })
})

describe('Acessibilidade — Minha conta', () => {
  it('troca de senha, vazia e com erro de campo', async () => {
    vi.mocked(alterarSenha).mockRejectedValueOnce(
      new ErroDaApi(400, 'SENHA_ATUAL_INCORRETA', 'A senha atual está incorreta.', {
        senha_atual: ['A senha atual está incorreta.'],
      }),
    )
    abrir('/conta', USUARIO_SOLICITANTE)
    await esperarSemViolacoes()
    await userEvent.click(await screen.findByRole('button', { name: 'Alterar senha' }))
    await screen.findByText('A senha atual está incorreta.')
    await esperarSemViolacoes()
  })
})

describe('Acessibilidade — espaços', () => {
  it('lista do Gestor, com formulário, filtros e ações', async () => {
    abrir('/espacos')
    await screen.findByRole('button', { name: 'Editar o espaço Ginásio A' })
    await esperarSemViolacoes()
  })

  it('lista do Solicitante', async () => {
    abrir('/espacos', USUARIO_SOLICITANTE)
    await screen.findByRole('link', { name: 'Reservar Ginásio A' })
    await esperarSemViolacoes()
  })

  it('carregando', async () => {
    vi.mocked(listarEspacos).mockReturnValueOnce(nuncaResponde())
    abrir('/espacos')
    await screen.findAllByText(/Carregando/)
    await esperarSemViolacoes()
  })

  it('vazio', async () => {
    vi.mocked(listarEspacos).mockResolvedValue(sucesso([]))
    abrir('/espacos')
    await screen.findByText(/Nenhum espaço cadastrado/)
    await esperarSemViolacoes()
  })

  it('falha ao carregar', async () => {
    vi.mocked(listarEspacos).mockRejectedValue(SEM_CONEXAO)
    abrir('/espacos')
    await screen.findByRole('button', { name: 'Tentar novamente' })
    await esperarSemViolacoes()
  })

  it('cadastro com erro de campo', async () => {
    vi.mocked(cadastrarEspaco).mockRejectedValueOnce(
      new ErroDaApi(400, 'CAMPO_OBRIGATORIO_AUSENTE', 'Informe o nome.', { nome: ['Informe o nome.'] }),
    )
    abrir('/espacos')
    await screen.findByRole('button', { name: 'Editar o espaço Ginásio A' })
    await userEvent.click(screen.getByRole('button', { name: /^Cadastrar/ }))
    await screen.findByText('Informe o nome.')
    await esperarSemViolacoes()
  })

  it('diálogos de edição e de desativação abertos', async () => {
    abrir('/espacos')
    await userEvent.click(await screen.findByRole('button', { name: 'Editar o espaço Ginásio A' }))
    await screen.findByRole('dialog', { name: 'Editar espaço' })
    await esperarSemViolacoes()
    await userEvent.click(screen.getByRole('button', { name: 'Voltar' }))
    await userEvent.click(screen.getByRole('button', { name: 'Desativar o espaço Ginásio A' }))
    await screen.findByRole('dialog', { name: 'Desativar espaço' })
    await esperarSemViolacoes()
  })
})

describe('Acessibilidade — nova reserva', () => {
  it('formulário com a dica e a agenda do dia', async () => {
    abrir('/reservas/nova?espaco=1', USUARIO_SOLICITANTE)
    fireEvent.change(await screen.findByLabelText('Data'), { target: { value: '2026-11-25' } })
    await screen.findByRole('button', { name: /^Usar este horário, 07:00/ })
    await esperarSemViolacoes()
  })

  it('erro do backend (conflito) e erro de campo', async () => {
    vi.mocked(solicitarReserva)
      .mockRejectedValueOnce(
        new ErroDaApi(
          409,
          'CONFLITO_DE_HORARIO',
          'Este espaço já tem uma reserva Solicitada em 25/11/2026 10:00–11:00. Escolha outro horário.',
        ),
      )
      .mockRejectedValueOnce(
        new ErroDaApi(400, 'CAMPO_OBRIGATORIO_AUSENTE', 'Informe a finalidade.', {
          finalidade: ['Informe a finalidade.'],
        }),
      )
    abrir('/reservas/nova?espaco=1', USUARIO_SOLICITANTE)
    const enviar = await screen.findByRole('button', { name: /^Solicitar/ })
    await userEvent.click(enviar)
    await screen.findByText(/já tem uma reserva Solicitada/)
    await esperarSemViolacoes()
    await userEvent.click(enviar)
    await screen.findByText('Informe a finalidade.')
    await esperarSemViolacoes()
  })

  it('sem espaços ativos', async () => {
    vi.mocked(listarEspacos).mockResolvedValue(sucesso([]))
    abrir('/reservas/nova', USUARIO_SOLICITANTE)
    await screen.findByText(/Nenhum espaço disponível/)
    await esperarSemViolacoes()
  })
})

describe('Acessibilidade — consulta de reservas', () => {
  it('lista do Gestor com filtros e ações', async () => {
    abrir('/reservas?situacao=SOLICITADA')
    await screen.findByRole('button', { name: /^Confirmar a reserva de/ })
    await esperarSemViolacoes()
  })

  it('Minhas reservas do Solicitante', async () => {
    abrir('/reservas', USUARIO_SOLICITANTE)
    await screen.findByRole('heading', { name: 'Minhas reservas' })
    await screen.findAllByRole('link', { name: /ver detalhes/ })
    await esperarSemViolacoes()
  })

  it('carregando', async () => {
    vi.mocked(listarReservas).mockReturnValue(nuncaResponde())
    abrir('/reservas')
    await screen.findByText('Carregando reservas...')
    await esperarSemViolacoes()
  })

  it('vazio com filtro', async () => {
    vi.mocked(listarReservas).mockResolvedValue(
      sucesso({ reservas: [], paginacao: paginacao(0) }, { mensagem: 'Nenhuma reserva encontrada.' }),
    )
    abrir('/reservas?situacao=CANCELADA')
    await screen.findByText(/Nenhuma reserva encontrada/)
    await esperarSemViolacoes()
  })

  it('falha ao carregar', async () => {
    vi.mocked(listarReservas).mockRejectedValue(SEM_CONEXAO)
    abrir('/reservas')
    await screen.findByRole('button', { name: 'Tentar novamente' })
    await esperarSemViolacoes()
  })

  it('diálogo de recusa aberto, com o campo de motivo', async () => {
    abrir('/reservas')
    await userEvent.click(await screen.findByRole('button', { name: /^Recusar a reserva de/ }))
    await screen.findByRole('dialog', { name: 'Recusar reserva' })
    await esperarSemViolacoes()
  })
})

describe('Acessibilidade — detalhe da reserva', () => {
  it('detalhe com a linha do tempo (aceita e recusada) e as ações', async () => {
    abrir('/reservas/5')
    await screen.findByText(/Tentativa recusada/)
    await esperarSemViolacoes()
  })

  it('diálogo de confirmação aberto', async () => {
    abrir('/reservas/5')
    await userEvent.click(await screen.findByRole('button', { name: /^Confirmar a reserva de/ }))
    const dialogo = await screen.findByRole('dialog', { name: 'Confirmar reserva' })
    expect(within(dialogo).getByRole('button', { name: 'Voltar' })).toBeTruthy()
    await esperarSemViolacoes()
  })

  it('reserva não encontrada', async () => {
    vi.mocked(obterReserva).mockRejectedValue(
      new ErroDaApi(404, 'RESERVA_NAO_ENCONTRADA', 'Reserva não encontrada.'),
    )
    abrir('/reservas/99', USUARIO_SOLICITANTE)
    await screen.findByText('Reserva não encontrada')
    await esperarSemViolacoes()
  })
})

describe('Acessibilidade — usuários (Gestor)', () => {
  it('lista com filtros e ações', async () => {
    abrir('/usuarios')
    await screen.findByRole('button', { name: 'Desativar: Bruno Lima' })
    await esperarSemViolacoes()
  })

  it('vazio', async () => {
    vi.mocked(listarUsuarios).mockResolvedValue(
      sucesso({ usuarios: [], paginacao: paginacao(0) }, { mensagem: 'Nenhum usuário encontrado.' }),
    )
    abrir('/usuarios?busca=zzz')
    await screen.findAllByText(/Nenhum usuário/)
    await esperarSemViolacoes()
  })

  it('diálogo de desativação aberto', async () => {
    abrir('/usuarios')
    await userEvent.click(await screen.findByRole('button', { name: 'Desativar: Bruno Lima' }))
    await screen.findByRole('dialog')
    await esperarSemViolacoes()
  })
})

describe('Situação nunca indicada só por cor (RNF-U05)', () => {
  it('a situação de cada reserva aparece como texto na lista, com o motivo', async () => {
    abrir('/reservas')
    const tabela = await screen.findByRole('table')
    expect(within(tabela).getByText('Solicitada')).toBeTruthy()
    expect(within(tabela).getByText('Cancelada')).toBeTruthy()
    expect(within(tabela).getByText(/Motivo: Chuva prevista\./)).toBeTruthy()
  })

  it('o estado de cada espaço aparece como texto', async () => {
    abrir('/espacos')
    const tabela = await screen.findByRole('table')
    expect(within(tabela).getByText('Ativo')).toBeTruthy()
    expect(within(tabela).getByText('Inativo')).toBeTruthy()
  })

  it('o tipo de cada aviso aparece como texto, além da cor e do marcador', async () => {
    vi.mocked(consultarSaude).mockRejectedValue(SEM_CONEXAO)
    abrir('/', null)
    const aviso = await screen.findByRole('alert')
    expect(aviso.textContent).toContain('Erro:')
  })

  it('na linha do tempo, a tentativa recusada se distingue da mudança aceita pelo texto', async () => {
    abrir('/reservas/5')
    const linha = (await screen.findByText(/Tentativa recusada:/)).closest('ol')
    expect(linha).not.toBeNull()
    const [aceita, recusada] = within(linha as HTMLElement).getAllByRole('listitem')
    expect(aceita.textContent).toContain('Solicitada por Bruno Lima')
    expect(aceita.textContent).not.toContain('Tentativa recusada')
    expect(recusada.textContent).toContain('Tentativa recusada: Bruno Lima tentou Confirmada.')
  })
})

describe('index.html', () => {
  it('declara o idioma pt-BR e uma viewport que não bloqueia o zoom', () => {
    expect(paginaHtml).toContain('<html lang="pt-BR">')
    expect(paginaHtml).toContain('<meta name="viewport" content="width=device-width, initial-scale=1.0" />')
    expect(paginaHtml).not.toMatch(/user-scalable\s*=\s*no|maximum-scale/)
    expect(paginaHtml).toMatch(/<title>.+<\/title>/)
  })
})
