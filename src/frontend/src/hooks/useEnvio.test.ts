import { act, renderHook } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { ErroDaApi } from '../api/cliente.ts'
import type { RespostaSucesso } from '../api/tipos.ts'
import { useEnvio } from './useEnvio.ts'

type Dados = { nome: string }

const RESPOSTA: RespostaSucesso<number> = { mensagem: 'Espaço cadastrado com sucesso.', dados: 1 }

const ERRO_COM_CAMPOS = new ErroDaApi(400, 'CAPACIDADE_INVALIDA', 'Capacidade inválida.', {
  capacidade: ['A capacidade deve ser um número inteiro maior que zero.'],
  nome: ['Informe o nome.'],
})

const ERRO_SEM_CAMPOS = new ErroDaApi(0, 'SEM_CONEXAO', 'Não foi possível conectar ao servidor.')

function promessaControlada<T>() {
  let resolver!: (valor: T) => void
  const promessa = new Promise<T>((resolve) => {
    resolver = resolve
  })
  return { promessa, resolver }
}

function renderizar(enviar: (dados: Dados) => Promise<RespostaSucesso<number>>) {
  return renderHook(() => useEnvio(enviar))
}

describe('useEnvio', () => {
  it('no sucesso devolve a resposta e limpa os erros', async () => {
    const enviar = vi
      .fn<(dados: Dados) => Promise<RespostaSucesso<number>>>()
      .mockRejectedValueOnce(ERRO_COM_CAMPOS)
      .mockResolvedValueOnce(RESPOSTA)
    const { result } = renderizar(enviar)
    await act(() => result.current.enviar({ nome: '' }))

    let resposta: RespostaSucesso<number> | null = null
    await act(async () => {
      resposta = await result.current.enviar({ nome: 'Ginásio' })
    })

    expect(resposta).toEqual(RESPOSTA)
    expect(enviar).toHaveBeenLastCalledWith({ nome: 'Ginásio' })
    expect(result.current.errosDosCampos).toEqual({})
    expect(result.current.erroGeral).toBeNull()
  })

  it('erro com campos vai para errosDosCampos e devolve null', async () => {
    const { result } = renderizar(() => Promise.reject(ERRO_COM_CAMPOS))

    let resposta: RespostaSucesso<number> | null = RESPOSTA
    await act(async () => {
      resposta = await result.current.enviar({ nome: '' })
    })

    expect(resposta).toBeNull()
    expect(result.current.errosDosCampos).toEqual({
      capacidade: 'A capacidade deve ser um número inteiro maior que zero.',
      nome: 'Informe o nome.',
    })
    expect(result.current.erroGeral).toBeNull()
  })

  it('erro sem campos vai para erroGeral', async () => {
    const { result } = renderizar(() => Promise.reject(ERRO_SEM_CAMPOS))

    await act(() => result.current.enviar({ nome: 'Ginásio' }))

    expect(result.current.erroGeral).toBe('Não foi possível conectar ao servidor.')
    expect(result.current.errosDosCampos).toEqual({})
  })

  it('guarda o status HTTP do erro e o limpa no sucesso', async () => {
    const conflito = new ErroDaApi(409, 'TRANSICAO_DE_SITUACAO_INVALIDA', 'Já foi alterada.')
    const enviar = vi
      .fn<(dados: Dados) => Promise<RespostaSucesso<number>>>()
      .mockRejectedValueOnce(conflito)
      .mockRejectedValueOnce(new Error('falha qualquer'))
      .mockResolvedValueOnce(RESPOSTA)
    const { result } = renderizar(enviar)

    await act(() => result.current.enviar({ nome: 'Ginásio' }))
    expect(result.current.statusDoErro).toBe(409)

    await act(() => result.current.enviar({ nome: 'Ginásio' }))
    expect(result.current.statusDoErro).toBeNull()

    await act(() => result.current.enviar({ nome: 'Ginásio' }))
    expect(result.current.statusDoErro).toBeNull()
    expect(result.current.erroGeral).toBeNull()
  })

  it('limparErroDoCampo remove só o erro daquele campo', async () => {
    const { result } = renderizar(() => Promise.reject(ERRO_COM_CAMPOS))
    await act(() => result.current.enviar({ nome: '' }))

    act(() => result.current.limparErroDoCampo('capacidade'))

    expect(result.current.errosDosCampos).toEqual({ nome: 'Informe o nome.' })
  })

  it('fica enviando até a resposta chegar', async () => {
    const pendente = promessaControlada<RespostaSucesso<number>>()
    const { result } = renderizar(() => pendente.promessa)
    expect(result.current.enviando).toBe(false)

    let envio!: Promise<unknown>
    act(() => {
      envio = result.current.enviar({ nome: 'Ginásio' })
    })
    expect(result.current.enviando).toBe(true)

    await act(async () => {
      pendente.resolver(RESPOSTA)
      await envio
    })
    expect(result.current.enviando).toBe(false)
  })

  it('ignora a resposta se o componente desmontar no meio do envio', async () => {
    const pendente = promessaControlada<RespostaSucesso<number>>()
    const { result, unmount } = renderizar(() => pendente.promessa)
    let envio!: Promise<RespostaSucesso<number> | null>
    act(() => {
      envio = result.current.enviar({ nome: 'Ginásio' })
    })

    unmount()
    pendente.resolver(RESPOSTA)

    expect(await envio).toBeNull()
  })
})
