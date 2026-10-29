import { act, renderHook, waitFor } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { ErroDaApi, MENSAGEM_ERRO_INESPERADO } from '../api/cliente.ts'
import type { RespostaSucesso } from '../api/tipos.ts'
import { useConsulta } from './useConsulta.ts'

function resposta<T>(dados: T, mensagem = 'Tudo certo.'): RespostaSucesso<T> {
  return { mensagem, dados }
}

function promessaControlada<T>() {
  let resolver!: (valor: T) => void
  const promessa = new Promise<T>((resolve) => {
    resolver = resolve
  })
  return { promessa, resolver }
}

describe('useConsulta', () => {
  it('começa carregando e passa para sucesso com os dados e a mensagem', async () => {
    const buscar = vi.fn(() => Promise.resolve(resposta([1, 2], '2 espaços encontrados.')))

    const { result } = renderHook(() => useConsulta(buscar, []))

    expect(result.current.estado.tipo).toBe('carregando')
    await waitFor(() =>
      expect(result.current.estado).toEqual({
        tipo: 'sucesso',
        dados: [1, 2],
        mensagem: '2 espaços encontrados.',
      }),
    )
  })

  it('passa de carregando para erro com a mensagem e o status da API', async () => {
    const erro = new ErroDaApi(404, 'RESERVA_NAO_ENCONTRADA', 'Reserva não encontrada.')

    const { result } = renderHook(() => useConsulta(() => Promise.reject(erro), []))

    expect(result.current.estado.tipo).toBe('carregando')
    await waitFor(() =>
      expect(result.current.estado).toEqual({
        tipo: 'erro',
        mensagem: 'Reserva não encontrada.',
        status: 404,
      }),
    )
  })

  it('usa a mensagem de erro inesperado e status nulo para um erro que não é da API', async () => {
    const { result } = renderHook(() =>
      useConsulta(() => Promise.reject(new Error('falhou')), []),
    )

    await waitFor(() =>
      expect(result.current.estado).toEqual({
        tipo: 'erro',
        mensagem: MENSAGEM_ERRO_INESPERADO,
        status: null,
      }),
    )
  })

  it('recarregar volta a carregando e busca de novo', async () => {
    const buscar = vi
      .fn<() => Promise<RespostaSucesso<string>>>()
      .mockRejectedValueOnce(new ErroDaApi(0, 'SEM_CONEXAO', 'Sem conexão.'))
      .mockResolvedValueOnce(resposta('ok', 'API no ar.'))
    const { result } = renderHook(() => useConsulta(buscar, []))
    await waitFor(() => expect(result.current.estado.tipo).toBe('erro'))

    act(() => result.current.recarregar())

    expect(result.current.estado.tipo).toBe('carregando')
    await waitFor(() =>
      expect(result.current.estado).toEqual({ tipo: 'sucesso', dados: 'ok', mensagem: 'API no ar.' }),
    )
    expect(buscar).toHaveBeenCalledTimes(2)
  })

  it('ignora a resposta de uma consulta antiga que chega depois da nova', async () => {
    const antiga = promessaControlada<RespostaSucesso<string>>()
    const nova = promessaControlada<RespostaSucesso<string>>()
    const promessas: Record<string, Promise<RespostaSucesso<string>>> = {
      futebol: antiga.promessa,
      tenis: nova.promessa,
    }
    const { result, rerender } = renderHook(
      ({ tipo }) => useConsulta(() => promessas[tipo], [tipo]),
      { initialProps: { tipo: 'futebol' } },
    )

    rerender({ tipo: 'tenis' })
    await act(async () => nova.resolver(resposta('tenis')))
    await act(async () => antiga.resolver(resposta('futebol')))

    expect(result.current.estado).toEqual({ tipo: 'sucesso', dados: 'tenis', mensagem: 'Tudo certo.' })
  })
})
