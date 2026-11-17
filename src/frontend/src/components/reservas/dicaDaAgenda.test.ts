import { describe, expect, it } from 'vitest'
import type { RegrasDeAgenda } from '../../api/reservas.ts'
import { descreverFuncionamento, descreverRegrasDeAgenda } from './dicaDaAgenda.ts'

const REGRAS: RegrasDeAgenda = {
  duracao_sugerida_em_minutos: 60,
  duracao_minima_em_minutos: 30,
  duracao_maxima_em_minutos: 90,
  antecedencia_maxima_em_dias: 15,
  data_limite: '2026-12-01',
}

describe('descreverRegrasDeAgenda', () => {
  it('monta a dica só com os valores recebidos da API', () => {
    expect(descreverRegrasDeAgenda(REGRAS)).toBe(
      'duração sugerida de 1 h · de 30 min a 1 h 30 min · até 01/12/2026.',
    )
  })
})

describe('descreverFuncionamento', () => {
  it('escreve a meia-noite do fechamento por extenso', () => {
    expect(descreverFuncionamento({ abertura: '07:00', fechamento: '00:00' })).toBe(
      'Este espaço funciona das 07:00 às meia-noite.',
    )
  })

  it('mostra o horário próprio do espaço', () => {
    expect(descreverFuncionamento({ abertura: '08:00', fechamento: '22:00' })).toBe(
      'Este espaço funciona das 08:00 às 22:00.',
    )
  })
})
