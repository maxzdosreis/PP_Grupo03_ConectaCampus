import { describe, expect, it } from 'vitest'
import type { RegrasDeAgenda } from '../../api/reservas.ts'
import { descreverRegrasDeAgenda } from './dicaDaAgenda.ts'

const REGRAS: RegrasDeAgenda = {
  horario_de_abertura: '08:00',
  horario_de_fechamento: '20:00',
  duracao_minima_em_minutos: 60,
  duracao_maxima_em_minutos: 90,
  antecedencia_maxima_em_dias: 15,
  data_limite: '2026-12-01',
}

describe('descreverRegrasDeAgenda', () => {
  it('monta a dica só com os valores recebidos da API', () => {
    expect(descreverRegrasDeAgenda(REGRAS)).toBe(
      'Funcionamento das 08:00 às 20:00 · duração de 1 h a 1 h 30 min · até 01/12/2026.',
    )
  })
})
