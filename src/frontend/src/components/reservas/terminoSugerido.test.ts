import { describe, expect, it } from 'vitest'
import { terminoSugerido } from './terminoSugerido.ts'

describe('terminoSugerido', () => {
  it('soma a duração sugerida ao início', () => {
    expect(terminoSugerido('10:00', '00:00', 60)).toEqual({
      termino: '11:00',
      limitadoPeloFechamento: false,
    })
  })

  it('aceita terminar exatamente no fechamento', () => {
    expect(terminoSugerido('23:00', '00:00', 60)).toEqual({
      termino: '00:00',
      limitadoPeloFechamento: false,
    })
    expect(terminoSugerido('21:00', '22:00', 60)).toEqual({
      termino: '22:00',
      limitadoPeloFechamento: false,
    })
  })

  it('se passaria do fechamento, usa o fechamento do espaço', () => {
    expect(terminoSugerido('23:30', '00:00', 60)).toEqual({
      termino: '00:00',
      limitadoPeloFechamento: true,
    })
    expect(terminoSugerido('21:30', '22:00', 60)).toEqual({
      termino: '22:00',
      limitadoPeloFechamento: true,
    })
  })

  it('segue a duração recebida, não um número fixo', () => {
    expect(terminoSugerido('10:00', '00:00', 90)?.termino).toBe('11:30')
  })

  it.each([
    ['início ainda incompleto', '', '00:00'],
    ['início depois do fechamento do espaço', '22:30', '22:00'],
    ['início no próprio fechamento', '22:00', '22:00'],
    ['fechamento desconhecido', '10:00', ''],
  ])('não sugere nada com %s', (_descricao, inicio, fechamento) => {
    expect(terminoSugerido(inicio, fechamento, 60)).toBeNull()
  })
})
