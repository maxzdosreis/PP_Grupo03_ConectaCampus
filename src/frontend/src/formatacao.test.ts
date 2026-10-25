import { describe, expect, it } from 'vitest'
import { formatarData, formatarIntervalo } from './formatacao.ts'

describe('formatacao', () => {
  it.each([
    ['2026-10-25', '25/10/2026'],
    ['2026-11-01', '01/11/2026'],
    ['2027-01-01', '01/01/2027'],
  ])('formatarData(%s) devolve %s, sem pular para o dia anterior', (data, esperado) => {
    expect(formatarData(data)).toBe(esperado)
  })

  it('formatarIntervalo junta a data e o horário', () => {
    expect(formatarIntervalo('2026-11-01', '10:00', '11:00')).toBe('01/11/2026, 10:00–11:00')
  })
})
