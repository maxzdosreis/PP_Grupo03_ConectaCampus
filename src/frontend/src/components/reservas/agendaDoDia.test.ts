import { describe, expect, it } from 'vitest'
import { horarioSugerido, posicaoNaFaixa } from './agendaDoDia.ts'

describe('horarioSugerido', () => {
  it('limita o término pela duração máxima recebida', () => {
    expect(horarioSugerido({ hora_inicio: '07:00', hora_fim: '00:00' }, 90)).toEqual({
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
    expect(horarioSugerido({ hora_inicio: '12:00', hora_fim: '00:00' }, null)).toEqual({
      hora_inicio: '12:00',
      hora_fim: '00:00',
    })
  })

  it('uma janela que termina à meia-noite não vira um término no começo do dia', () => {
    expect(horarioSugerido({ hora_inicio: '22:30', hora_fim: '00:00' }, 180)).toEqual({
      hora_inicio: '22:30',
      hora_fim: '00:00',
    })
  })

  it('a duração máxima que alcança a meia-noite escreve o término como 00:00', () => {
    expect(horarioSugerido({ hora_inicio: '21:00', hora_fim: '00:00' }, 180)).toEqual({
      hora_inicio: '21:00',
      hora_fim: '00:00',
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

  it('com o fechamento à meia-noite, a faixa vai até o fim do dia', () => {
    expect(posicaoNaFaixa({ hora_inicio: '12:00', hora_fim: '00:00' }, '00:00', '00:00')).toEqual({
      inicio: 50,
      largura: 50,
    })
    expect(posicaoNaFaixa({ hora_inicio: '23:00', hora_fim: '00:00' }, '08:00', '00:00')).toEqual({
      inicio: (15 / 16) * 100,
      largura: (1 / 16) * 100,
    })
  })
})
