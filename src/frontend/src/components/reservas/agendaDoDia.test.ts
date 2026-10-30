import { describe, expect, it } from 'vitest'
import { horarioSugerido, posicaoNaFaixa } from './agendaDoDia.ts'

describe('horarioSugerido', () => {
  it('limita o término pela duração máxima recebida', () => {
    expect(horarioSugerido({ hora_inicio: '07:00', hora_fim: '22:00' }, 90)).toEqual({
      hora_inicio: '07:00',
      hora_fim: '08:30',
    })
  })

  it('não passa do fim da janela', () => {
    expect(horarioSugerido({ hora_inicio: '09:15', hora_fim: '10:00' }, 90)).toEqual({
      hora_inicio: '09:15',
      hora_fim: '10:00',
    })
  })

  it('sem a duração máxima, usa a janela inteira', () => {
    expect(horarioSugerido({ hora_inicio: '12:00', hora_fim: '22:00' }, null)).toEqual({
      hora_inicio: '12:00',
      hora_fim: '22:00',
    })
  })
})

describe('posicaoNaFaixa', () => {
  it('converte o horário em porcentagem do funcionamento', () => {
    expect(posicaoNaFaixa({ hora_inicio: '10:00', hora_fim: '12:00' }, '08:00', '18:00')).toEqual({
      inicio: 20,
      largura: 20,
    })
  })

  it('recorta o que passa do funcionamento', () => {
    expect(posicaoNaFaixa({ hora_inicio: '06:00', hora_fim: '20:00' }, '08:00', '18:00')).toEqual({
      inicio: 0,
      largura: 100,
    })
  })
})
