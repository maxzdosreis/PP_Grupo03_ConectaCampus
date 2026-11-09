import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { USUARIO_SOLICITANTE } from '../testes/usuarios.ts'
import { entrar } from './autenticacao.ts'
import { ErroDaApi, NOME_DA_TRAVA_DE_RENOVACAO, requisitar } from './cliente.ts'
import {
  aoMudarSessao,
  CHAVE_DA_SESSAO,
  lerSessao,
  limparSessao,
  salvarSessao,
} from './sessao.ts'

const URL_DA_API = 'http://localhost:8000/api'
const URL_DA_RENOVACAO = `${URL_DA_API}/auth/refresh/`

type Chamada = [string, RequestInit]

function resposta(status: number, corpo: unknown): Response {
  return { ok: status >= 200 && status < 300, status, json: async () => corpo } as Response
}

function respostaSemJson(status: number): Response {
  return {
    ok: false,
    status,
    json: async () => {
      throw new SyntaxError('Unexpected token <')
    },
  } as unknown as Response
}

const SUCESSO =resposta(200, { mensagem: 'ok', dados: [] })
const NAO_AUTENTICADO = resposta(401, {
  erro: { codigo: 'NAO_AUTENTICADO', mensagem: 'Faça login para continuar.' },
})
const REFRESH_RECUSADO = resposta(401, {
  erro: { codigo: 'NAO_AUTENTICADO', mensagem: 'Token inválido ou expirado.' },
})

function renovado(access: string, refresh = 'refresh-2') {
  return resposta(200, { mensagem: 'Token renovado.', dados: { access, refresh } })
}

const SESSAO_DE_OUTRA_ABA = {
  access: 'access-9',
  refresh: 'refresh-9',
  usuario: USUARIO_SOLICITANTE,
}

function outraAbaGravou(sessao: unknown = SESSAO_DE_OUTRA_ABA) {
  const valor = JSON.stringify(sessao)
  localStorage.setItem(CHAVE_DA_SESSAO, valor)
  return valor
}

function deferido<T>() {
  let resolver!: (valor: T) => void
  const promessa = new Promise<T>((resolve) => {
    resolver = resolve
  })
  return { promessa, resolver }
}

function instalarTravasFalsas() {
  const nomes: string[] = []
  let ocupada = false
  let fila: Promise<unknown> = Promise.resolve()
  const travas = {
    request(nome: string, tarefa: () => Promise<unknown>) {
      nomes.push(nome)
      const resultado = fila.then(async () => {
        ocupada = true
        try {
          return await tarefa()
        } finally {
          ocupada = false
        }
      })
      fila = resultado.catch(() => undefined)
      return resultado
    },
  }
  Object.defineProperty(navigator, 'locks', { value: travas, configurable: true })
  return {
    nomes,
    ocupada: () => ocupada,
    segurarComoOutraAba() {
      const solta = deferido<void>()
      travas.request(NOME_DA_TRAVA_DE_RENOVACAO, () => solta.promessa)
      return () => solta.resolver()
    },
  }
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
    vi.useRealTimers()
    Reflect.deleteProperty(navigator, 'locks')
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

  it('a renovação guarda o access e o refresh novos na sessão', async () => {
    apiQueAceitaSo('access-2', () => renovado('access-2', 'refresh-2'))
    const ouvinte = vi.fn()
    const cancelar = aoMudarSessao(ouvinte)

    await requisitar('/reservas/')
    cancelar()

    expect(lerSessao()).toEqual({
      access: 'access-2',
      refresh: 'refresh-2',
      usuario: USUARIO_SOLICITANTE,
    })
    expect(ouvinte).toHaveBeenCalledWith(lerSessao(), 'atualizacao')
  })

  it('renovação recusada com outro refresh já salvo por outra aba repete com a sessão nova e não desloga', async () => {
    apiQueAceitaSo('access-9', () => {
      outraAbaGravou()
      return REFRESH_RECUSADO
    })
    const ouvinte = vi.fn()
    const cancelar = aoMudarSessao(ouvinte)

    const resultado = await requisitar('/reservas/')
    cancelar()

    expect(resultado).toEqual({ mensagem: 'ok', dados: [] })
    expect(chamadasDeRenovacao()).toHaveLength(1)
    expect(autorizacao(chamadas()[2])).toBe('Bearer access-9')
    expect(lerSessao()).toEqual(SESSAO_DE_OUTRA_ABA)
    expect(ouvinte).not.toHaveBeenCalled()
  })

  it('a renovação roda dentro da trava entre abas', async () => {
    const travas = instalarTravasFalsas()
    let renovouComATrava = false
    apiQueAceitaSo('access-2', () => {
      renovouComATrava = travas.ocupada()
      return renovado('access-2', 'refresh-2')
    })

    await requisitar('/reservas/')

    expect(travas.nomes).toEqual([NOME_DA_TRAVA_DE_RENOVACAO])
    expect(renovouComATrava).toBe(true)
    expect(lerSessao()?.refresh).toBe('refresh-2')
  })

  it('com a renovação de outra aba em andamento, espera a trava e usa a sessão nova sem renovar, por mais que ela demore', async () => {
    vi.useFakeTimers({ toFake: ['setTimeout', 'clearTimeout'] })
    const travas = instalarTravasFalsas()
    const soltarOutraAba = travas.segurarComoOutraAba()
    apiQueAceitaSo('access-9', () => REFRESH_RECUSADO)
    const ouvinte = vi.fn()
    const cancelar = aoMudarSessao(ouvinte)

    const pedido = requisitar('/reservas/')
    await vi.advanceTimersByTimeAsync(5000)
    expect(lerSessao()?.access).toBe('access-1')
    outraAbaGravou()
    soltarOutraAba()
    const resultado = await pedido
    cancelar()

    expect(resultado).toEqual({ mensagem: 'ok', dados: [] })
    expect(chamadasDeRenovacao()).toHaveLength(0)
    expect(autorizacao(chamadas()[1])).toBe('Bearer access-9')
    expect(lerSessao()).toEqual(SESSAO_DE_OUTRA_ABA)
    expect(ouvinte).not.toHaveBeenCalled()
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

  it('refresh vazio recusado com 400 também encerra a sessão', async () => {
    apiQueAceitaSo('access-2', () =>
      resposta(400, {
        erro: {
          codigo: 'DADOS_INVALIDOS',
          mensagem: 'Verifique os dados informados.',
          campos: { refresh: ['Este campo não pode ser em branco.'] },
        },
      }),
    )

    const erro = await erroDe(requisitar('/reservas/'))

    expect(erro.codigo).toBe('SESSAO_EXPIRADA')
    expect(lerSessao()).toBeNull()
  })

  const FALHAS_PASSAGEIRAS: [string, () => Response, string][] = [
    [
      'sem conexão',
      () => {
        throw new TypeError('Failed to fetch')
      },
      'SEM_CONEXAO',
    ],
    [
      '429',
      () =>
        resposta(429, {
          erro: { codigo: 'MUITAS_REQUISICOES', mensagem: 'Muitas requisições. Tente de novo.' },
        }),
      'MUITAS_REQUISICOES',
    ],
    [
      '500',
      () => resposta(500, { erro: { codigo: 'ERRO_INTERNO', mensagem: 'Erro interno.' } }),
      'ERRO_INTERNO',
    ],
    ['503 sem JSON', () => respostaSemJson(503), 'ERRO_INESPERADO'],
  ]

  it.each(FALHAS_PASSAGEIRAS)(
    'refresh com falha passageira (%s) mantém a sessão, lança o erro e deixa tentar de novo',
    async (_, falhar, codigo) => {
      let recuperada = false
      apiQueAceitaSo('access-2', () => (recuperada ? renovado('access-2') : falhar()))
      const ouvinte = vi.fn()
      const cancelar = aoMudarSessao(ouvinte)

      const erro = await erroDe(requisitar('/reservas/'))
      cancelar()

      expect(erro.codigo).toBe(codigo)
      expect(lerSessao()?.access).toBe('access-1')
      expect(ouvinte).not.toHaveBeenCalled()

      recuperada = true
      await expect(requisitar('/reservas/')).resolves.toEqual({ mensagem: 'ok', dados: [] })
      expect(chamadasDeRenovacao()).toHaveLength(2)
      expect(lerSessao()?.access).toBe('access-2')
    },
  )

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
  const LIMITE_DE_TENTATIVAS = resposta(429, {
    erro: { codigo: 'LIMITE_DE_TENTATIVAS', mensagem: 'Muitas tentativas. Tente de novo em 42 segundos.' },
  })

  it('429 LIMITE_DE_TENTATIVAS no login vira o erro com a mensagem do servidor, sem renovar', async () => {
    fetchFalso.mockResolvedValue(LIMITE_DE_TENTATIVAS)
    const ouvinte = vi.fn()
    const cancelar = aoMudarSessao(ouvinte)

    const erro = await erroDe(entrar({ email: 'bruno.lima@exemplo.com', senha: 'errada' }))
    cancelar()

    expect(erro.status).toBe(429)
    expect(erro.codigo).toBe('LIMITE_DE_TENTATIVAS')
    expect(erro.message).toBe('Muitas tentativas. Tente de novo em 42 segundos.')
    expect(chamadas()).toHaveLength(1)
    expect(ouvinte).not.toHaveBeenCalled()
    expect(lerSessao()?.access).toBe('access-1')
  })

  it('429 numa requisição autenticada não renova o token nem limpa a sessão', async () => {
    fetchFalso.mockResolvedValue(LIMITE_DE_TENTATIVAS)
    const ouvinte = vi.fn()
    const cancelar = aoMudarSessao(ouvinte)

    const erro = await erroDe(requisitar('/reservas/'))
    cancelar()

    expect(erro.status).toBe(429)
    expect(chamadasDeRenovacao()).toHaveLength(0)
    expect(ouvinte).not.toHaveBeenCalled()
    expect(lerSessao()).toMatchObject({ access: 'access-1', refresh: 'refresh-1' })
  })
  it('503 SERVICO_INDISPONIVEL no login vira o erro com a mensagem do servidor, sem renovar nem limpar a sessão', async () => {
    fetchFalso.mockResolvedValue(
      resposta(503, {
        erro: {
          codigo: 'SERVICO_INDISPONIVEL',
          mensagem: 'Serviço temporariamente indisponível. Tente de novo em alguns instantes.',
        },
      }),
    )
    const ouvinte = vi.fn()
    const cancelar = aoMudarSessao(ouvinte)

    const erro = await erroDe(entrar({ email: 'bruno.lima@exemplo.com', senha: 'errada' }))
    cancelar()

    expect(erro.status).toBe(503)
    expect(erro.codigo).toBe('SERVICO_INDISPONIVEL')
    expect(chamadas()).toHaveLength(1)
    expect(ouvinte).not.toHaveBeenCalled()
    expect(lerSessao()?.access).toBe('access-1')
  })
})
