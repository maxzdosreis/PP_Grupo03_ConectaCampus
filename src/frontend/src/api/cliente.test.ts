import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { USUARIO_SOLICITANTE } from '../testes/usuarios.ts'
import { entrar } from './autenticacao.ts'
import { ErroDaApi, requisitar } from './cliente.ts'
import { aoMudarSessao, lerSessao, limparSessao, salvarSessao } from './sessao.ts'

const URL_DA_API = 'http://localhost:8000/api'
const URL_DA_RENOVACAO = `${URL_DA_API}/auth/refresh/`

type Chamada = [string, RequestInit]

function resposta(status: number, corpo: unknown): Response {
  return { ok: status >= 200 && status < 300, status, json: async () => corpo } as Response
}

const SUCESSO = resposta(200, { mensagem: 'ok', dados: [] })
const NAO_AUTENTICADO = resposta(401, {
  erro: { codigo: 'NAO_AUTENTICADO', mensagem: 'Faça login para continuar.' },
})
const REFRESH_RECUSADO = resposta(401, {
  erro: { codigo: 'NAO_AUTENTICADO', mensagem: 'Token inválido ou expirado.' },
})

function renovado(access: string) {
  return resposta(200, { mensagem: 'Token renovado.', dados: { access } })
}

function deferido<T>() {
  let resolver!: (valor: T) => void
  const promessa = new Promise<T>((resolve) => {
    resolver = resolve
  })
  return { promessa, resolver }
}

const fetchFalso = vi.fn<(url: string, opcoes: RequestInit) => Promise<Response>>()

function chamadas(): Chamada[] {
  return fetchFalso.mock.calls
}

function autorizacao([, opcoes]: Chamada): string | undefined {
  return (opcoes.headers as Record<string, string>).Authorization
}

function chamadasDeRenovacao() {
  return chamadas().filter(([url]) => url === URL_DA_RENOVACAO)
}

function apiQueAceitaSo(accessValido: string, renovar: () => Response | Promise<Response>) {
  fetchFalso.mockImplementation(async (url, opcoes) => {
    if (url === URL_DA_RENOVACAO) return renovar()
    return autorizacao([url, opcoes]) === `Bearer ${accessValido}` ? SUCESSO : NAO_AUTENTICADO
  })
}

async function erroDe(promessa: Promise<unknown>): Promise<ErroDaApi> {
  try {
    await promessa
  } catch (erro) {
    if (erro instanceof ErroDaApi) return erro
    throw erro
  }
  throw new Error('A requisição deveria ter falhado.')
}

describe('cliente da API', () => {
  beforeEach(() => {
    localStorage.clear()
    fetchFalso.mockReset()
    vi.stubGlobal('fetch', fetchFalso)
    salvarSessao({ access: 'access-1', refresh: 'refresh-1', usuario: USUARIO_SOLICITANTE })
  })

  afterEach(() => {
    limparSessao()
    vi.unstubAllGlobals()
  })

  it('envia o access da sessão no cabeçalho Authorization', async () => {
    fetchFalso.mockResolvedValue(SUCESSO)

    await requisitar('/reservas/')

    expect(autorizacao(chamadas()[0])).toBe('Bearer access-1')
  })

  it('com autenticar: false, não envia o token', async () => {
    fetchFalso.mockResolvedValue(SUCESSO)

    await requisitar('/auth/login/', { method: 'POST', body: '{}', autenticar: false })

    expect(autorizacao(chamadas()[0])).toBeUndefined()
  })

  it('sem sessão, não envia token e um 401 não tenta renovar', async () => {
    limparSessao()
    fetchFalso.mockResolvedValue(NAO_AUTENTICADO)

    const erro = await erroDe(requisitar('/reservas/'))

    expect(erro.codigo).toBe('NAO_AUTENTICADO')
    expect(chamadas()).toHaveLength(1)
    expect(autorizacao(chamadas()[0])).toBeUndefined()
  })

  it('401 NAO_AUTENTICADO renova o access e repete a requisição com o novo', async () => {
    apiQueAceitaSo('access-2', () => renovado('access-2'))

    const resultado = await requisitar('/reservas/')

    expect(resultado).toEqual({ mensagem: 'ok', dados: [] })
    expect(chamadas().map(([url]) => url)).toEqual([
      `${URL_DA_API}/reservas/`,
      URL_DA_RENOVACAO,
      `${URL_DA_API}/reservas/`,
    ])
    const [, renovacao, repetida] = chamadas()
    expect(autorizacao(renovacao)).toBeUndefined()
    expect(renovacao[1].body).toBe(JSON.stringify({ refresh: 'refresh-1' }))
    expect(autorizacao(repetida)).toBe('Bearer access-2')
    expect(lerSessao()?.access).toBe('access-2')
  })

  it('duas requisições recebendo 401 ao mesmo tempo usam uma única renovação', async () => {
    const renovacao = deferido<Response>()
    apiQueAceitaSo('access-2', () => renovacao.promessa)

    const pedidos = Promise.all([requisitar('/reservas/'), requisitar('/espacos/')])
    await vi.waitFor(() => expect(chamadasDeRenovacao()).toHaveLength(1))
    renovacao.resolver(renovado('access-2'))
    await pedidos

    expect(chamadasDeRenovacao()).toHaveLength(1)
    expect(chamadas()).toHaveLength(5)
  })

  it('se outra requisição já trocou o access, só repete com o atual, sem renovar', async () => {
    const primeira = deferido<Response>()
    fetchFalso.mockImplementationOnce(() => primeira.promessa).mockResolvedValue(SUCESSO)

    const pedido = requisitar('/reservas/')
    salvarSessao({ access: 'access-2', refresh: 'refresh-2', usuario: USUARIO_SOLICITANTE })
    primeira.resolver(NAO_AUTENTICADO)
    await pedido

    expect(chamadasDeRenovacao()).toHaveLength(0)
    expect(autorizacao(chamadas()[1])).toBe('Bearer access-2')
  })

  it('se a renovação falhar, limpa a sessão, avisa os ouvintes e lança SESSAO_EXPIRADA', async () => {
    apiQueAceitaSo('access-2', () => REFRESH_RECUSADO)
    const ouvinte = vi.fn()
    const cancelar = aoMudarSessao(ouvinte)

    const erro = await erroDe(requisitar('/reservas/'))
    cancelar()

    expect(erro.status).toBe(401)
    expect(erro.codigo).toBe('SESSAO_EXPIRADA')
    expect(erro.message).toBe('Sua sessão expirou. Faça login novamente.')
    expect(lerSessao()).toBeNull()
    expect(ouvinte).toHaveBeenCalledWith(null, 'expiracao')
    expect(chamadas()).toHaveLength(2)
  })

  it('a requisição repetida que volta 401 de novo encerra a sessão, sem laço', async () => {
    apiQueAceitaSo('nenhum', () => renovado('access-2'))

    const erro = await erroDe(requisitar('/reservas/'))

    expect(erro.codigo).toBe('SESSAO_EXPIRADA')
    expect(chamadas()).toHaveLength(3)
    expect(lerSessao()).toBeNull()
  })

  it('sem conexão na renovação, mantém a sessão e lança SEM_CONEXAO', async () => {
    apiQueAceitaSo('access-2', () => {
      throw new TypeError('Failed to fetch')
    })

    const erro = await erroDe(requisitar('/reservas/'))

    expect(erro.codigo).toBe('SEM_CONEXAO')
    expect(lerSessao()?.access).toBe('access-1')
  })

  it('401 CREDENCIAIS_INVALIDAS no login não dispara renovação', async () => {
    fetchFalso.mockResolvedValue(
      resposta(401, {
        erro: { codigo: 'CREDENCIAIS_INVALIDAS', mensagem: 'E-mail ou senha incorretos.' },
      }),
    )

    const erro = await erroDe(entrar({ email: 'bruno.lima@exemplo.com', senha: 'errada' }))

    expect(erro.codigo).toBe('CREDENCIAIS_INVALIDAS')
    expect(chamadas()).toHaveLength(1)
    expect(autorizacao(chamadas()[0])).toBeUndefined()
    expect(lerSessao()?.access).toBe('access-1')
  })
})
