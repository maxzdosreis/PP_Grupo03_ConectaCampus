import { describe, expect, it } from 'vitest'
import {
  comoHorario,
  ehHorarioValido,
  MINUTOS_NO_DIA,
  minutosDoInicio,
  minutosDoTermino,
} from './minutosDoDia.ts'

describe('minutosDoDia', () => {
  it('00:00 é o começo do dia como início e o fim do dia como término', () => {
    expect(minutosDoInicio('00:00')).toBe(0)
    expect(minutosDoTermino('00:00')).toBe(MINUTOS_NO_DIA)
  })

  it('as outras horas valem igual nos dois sentidos', () => {
    expect(minutosDoInicio('07:30')).toBe(450)
    expect(minutosDoTermino('07:30')).toBe(450)
    expect(minutosDoTermino('23:59')).toBe(1439)
  })

  it('1440 volta a ser escrito como 00:00', () => {
    expect(comoHorario(MINUTOS_NO_DIA)).toBe('00:00')
    expect(comoHorario(450)).toBe('07:30')
    expect(comoHorario(0)).toBe('00:00')
  })

  it('só aceita HH:MM completo', () => {
    expect(ehHorarioValido('10:00')).toBe(true)
    expect(ehHorarioValido('')).toBe(false)
    expect(ehHorarioValido('10:0')).toBe(false)
  })
})
