import { describe, expect, it } from 'vitest'
import { formatarData, formatarDataHora, formatarDuracao, formatarIntervalo } from './formatacao.ts'

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

  it.each([
    ['2026-10-28T14:05:12.345678-03:00', '28/10/2026 às 14:05'],
    ['2026-11-01T09:30:00-03:00', '01/11/2026 às 09:30'],
    ['2026-11-01T00:00:00-03:00', '01/11/2026 às 00:00'],
    ['2026-12-31T23:59:59-03:00', '31/12/2026 às 23:59'],
  ])('formatarDataHora(%s) devolve %s no fuso que a API mandou', (iso, esperado) => {
    expect(formatarDataHora(iso)).toBe(esperado)
  })

  it.each([
    [30, '30 min'],
    [60, '1 h'],
    [90, '1 h 30 min'],
    [180, '3 h'],
  ])('formatarDuracao(%i) devolve %s', (minutos, esperado) => {
    expect(formatarDuracao(minutos)).toBe(esperado)
  })
})
