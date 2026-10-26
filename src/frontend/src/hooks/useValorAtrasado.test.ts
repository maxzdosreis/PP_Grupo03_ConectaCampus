import { act, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { useValorAtrasado } from './useValorAtrasado.ts'

const ATRASO_MS = 400

function renderizar(valorInicial: string) {
  return renderHook(({ valor }) => useValorAtrasado(valor, ATRASO_MS), {
    initialProps: { valor: valorInicial },
  })
}

describe('useValorAtrasado', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('entrega o valor inicial na hora', () => {
    const { result } = renderizar('ana')

    expect(result.current).toBe('ana')
  })

  it('só entrega o valor novo depois do atraso', () => {
    const { result, rerender } = renderizar('')

    rerender({ valor: 'ana' })
    act(() => vi.advanceTimersByTime(ATRASO_MS - 1))
    expect(result.current).toBe('')

    act(() => vi.advanceTimersByTime(1))
    expect(result.current).toBe('ana')
  })

  it('cada mudança reinicia o prazo e só o último valor é entregue', () => {
    const { result, rerender } = renderizar('')

    rerender({ valor: 'a' })
    act(() => vi.advanceTimersByTime(ATRASO_MS - 100))
    rerender({ valor: 'an' })
    act(() => vi.advanceTimersByTime(ATRASO_MS - 100))
    rerender({ valor: 'ana' })
    act(() => vi.advanceTimersByTime(ATRASO_MS - 1))
    expect(result.current).toBe('')

    act(() => vi.advanceTimersByTime(1))
    expect(result.current).toBe('ana')
  })
})
