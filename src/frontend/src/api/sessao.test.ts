import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { USUARIO_SOLICITANTE } from '../testes/usuarios.ts'
import {
  aguardarSessaoDeOutraAba,
  aoMudarSessao,
  atualizarTokens,
  CHAVE_DA_SESSAO,
  lerSessao,
  limparSessao,
  salvarSessao,
  type Sessao,
} from './sessao.ts'

const SESSAO: Sessao = { access: 'access-1', refresh: 'refresh-1', usuario: USUARIO_SOLICITANTE }

describe('sessao', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  afterEach(() => {
    vi.restoreAllMocks()
    limparSessao()
  })

  it('salva, lê e limpa a sessão no localStorage, numa chave única', () => {
    salvarSessao(SESSAO)

    expect(JSON.parse(localStorage.getItem(CHAVE_DA_SESSAO) ?? 'null')).toEqual(SESSAO)
    expect(lerSessao()).toEqual(SESSAO)

    limparSessao()

    expect(localStorage.getItem(CHAVE_DA_SESSAO)).toBeNull()
    expect(lerSessao()).toBeNull()
  })

  it('atualizarTokens troca o access e o refresh e mantém o usuário', () => {
    salvarSessao(SESSAO)

    atualizarTokens({ access: 'access-2', refresh: 'refresh-2' })

    expect(lerSessao()).toEqual({ ...SESSAO, access: 'access-2', refresh: 'refresh-2' })
  })

  it('atualizarTokens sem sessão não cria uma', () => {
    atualizarTokens({ access: 'access-2', refresh: 'refresh-2' })

    expect(lerSessao()).toBeNull()
  })

  function avisoDeOutraAba(valor: unknown, key = CHAVE_DA_SESSAO) {
    window.dispatchEvent(
      new StorageEvent('storage', { key, newValue: valor === null ? null : JSON.stringify(valor) }),
    )
  }

  it('aguardarSessaoDeOutraAba entrega a sessão que outra aba gravou com outro refresh', async () => {
    const outra = { ...SESSAO, access: 'access-9', refresh: 'refresh-9' }
    const espera = aguardarSessaoDeOutraAba('refresh-1', 1000)

    avisoDeOutraAba({ ...SESSAO, access: 'access-5' })
    avisoDeOutraAba(outra, 'outra-chave')
    avisoDeOutraAba(outra)

    await expect(espera).resolves.toEqual(outra)
  })

  it('aguardarSessaoDeOutraAba entrega null se a outra aba saiu', async () => {
    const espera = aguardarSessaoDeOutraAba('refresh-1', 1000)

    avisoDeOutraAba(null)

    await expect(espera).resolves.toBeNull()
  })

  it('aguardarSessaoDeOutraAba entrega null quando o tempo acaba', async () => {
    vi.useFakeTimers({ toFake: ['setTimeout', 'clearTimeout'] })
    const espera = aguardarSessaoDeOutraAba('refresh-1', 1000)

    await vi.advanceTimersByTimeAsync(1000)

    await expect(espera).resolves.toBeNull()
    vi.useRealTimers()
  })

  it('ignora um valor corrompido ou com outro formato', () => {
    localStorage.setItem(CHAVE_DA_SESSAO, '{isto não é json')
    expect(lerSessao()).toBeNull()

    localStorage.setItem(CHAVE_DA_SESSAO, JSON.stringify({ access: 'a' }))
    expect(lerSessao()).toBeNull()
  })

  it('com o localStorage recusado, não quebra e guarda a sessão em memória', () => {
    const recusar = () => {
      throw new DOMException('Acesso negado', 'SecurityError')
    }
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(recusar)
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(recusar)
    vi.spyOn(Storage.prototype, 'removeItem').mockImplementation(recusar)

    expect(lerSessao()).toBeNull()
    expect(() => salvarSessao(SESSAO)).not.toThrow()
    expect(lerSessao()).toEqual(SESSAO)
    expect(() => limparSessao()).not.toThrow()
    expect(lerSessao()).toBeNull()
  })

  it('avisa os ouvintes com a sessão e o motivo, até cancelarem', () => {
    const ouvinte = vi.fn()
    const cancelar = aoMudarSessao(ouvinte)

    salvarSessao(SESSAO)
    limparSessao({ expirou: true })
    salvarSessao(SESSAO)
    limparSessao()
    cancelar()
    salvarSessao(SESSAO)

    expect(ouvinte.mock.calls).toEqual([
      [SESSAO, 'atualizacao'],
      [null, 'expiracao'],
      [SESSAO, 'atualizacao'],
      [null, 'saida'],
    ])
  })

  it('limpar sem sessão não avisa ninguém', () => {
    const ouvinte = vi.fn()
    const cancelar = aoMudarSessao(ouvinte)

    limparSessao({ expirou: true })
    cancelar()

    expect(ouvinte).not.toHaveBeenCalled()
  })
})
