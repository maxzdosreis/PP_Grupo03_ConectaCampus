import { describe, expect, it } from 'vitest'
import { comParametros } from './parametros.ts'

describe('comParametros', () => {
  it('devolve o caminho sem "?" quando não há parâmetros', () => {
    expect(comParametros('/espacos/', {})).toBe('/espacos/')
  })

  it('ignora undefined, null e texto vazio', () => {
    expect(comParametros('/espacos/', { tipo: undefined, data: null, solicitante: '' })).toBe(
      '/espacos/',
    )
  })

  it('monta a query string na ordem dos parâmetros, mantendo zero e false', () => {
    expect(
      comParametros('/reservas/', { espaco: 3, situacao: 'CONFIRMADA', vazio: '', zero: 0, nao: false }),
    ).toBe('/reservas/?espaco=3&situacao=CONFIRMADA&zero=0&nao=false')
  })

  it('codifica espaços, acentos e caracteres reservados', () => {
    expect(comParametros('/reservas/', { solicitante: 'Ana Souza & Conceição' })).toBe(
      '/reservas/?solicitante=Ana+Souza+%26+Concei%C3%A7%C3%A3o',
    )
  })
})
