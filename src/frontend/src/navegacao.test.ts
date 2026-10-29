import { describe, expect, it } from 'vitest'
import {
  caminhoDaReserva,
  caminhoDeVolta,
  caminhoParaCadastro,
  caminhoParaEntrar,
  itensVisiveis,
  proximoSeguro,
  rotuloDasReservas,
} from './navegacao.ts'

describe('navegacao', () => {
  it.each(['/reservas?minhas=true', '/espacos', '/reservas/nova?espaco=3'])(
    'proximoSeguro aceita o caminho interno %s',
    (caminho) => {
      expect(proximoSeguro(caminho)).toBe(caminho)
    },
  )

  it.each([
    ['//site.com', '//site.com'],
    ['https://site.com', 'https://site.com'],
    ['/\\site.com', '/\\site.com'],
    ['vazio', ''],
    ['nulo', null],
    ['sem barra', 'reservas'],
  ])('proximoSeguro troca %s por /reservas', (_, valor) => {
    expect(proximoSeguro(valor)).toBe('/reservas')
  })

  it('proximoSeguro aceita outro caminho padrão', () => {
    expect(proximoSeguro(null, '/reservas/nova')).toBe('/reservas/nova')
  })

  it('caminhoParaEntrar leva o próximo codificado, e sem próximo vai só para /entrar', () => {
    expect(caminhoParaEntrar('/reservas?minhas=true')).toBe(
      '/entrar?proximo=%2Freservas%3Fminhas%3Dtrue',
    )
    expect(caminhoParaEntrar()).toBe('/entrar')
    expect(caminhoParaCadastro('/espacos')).toBe('/cadastro?proximo=%2Fespacos')
  })

  it('sem sessão, o menu mostra só o Início; com sessão, todos os itens', () => {
    expect(itensVisiveis(false, false).map(({ rotulo }) => rotulo)).toEqual(['Início'])
    expect(itensVisiveis(true, true).map(({ rotulo }) => rotulo)).toEqual([
      'Início',
      'Espaços',
      'Reservas',
      'Nova reserva',
    ])
  })

  it('para quem não é gestor, o item das reservas se chama "Minhas reservas"', () => {
    expect(itensVisiveis(true, false).map(({ rotulo }) => rotulo)).toEqual([
      'Início',
      'Espaços',
      'Minhas reservas',
      'Nova reserva',
    ])
    expect(rotuloDasReservas(false)).toBe('Minhas reservas')
    expect(rotuloDasReservas(true)).toBe('Reservas')
  })

  it('caminhoDaReserva aponta para o detalhe', () => {
    expect(caminhoDaReserva(12)).toBe('/reservas/12')
  })

  it.each([
    ['a origem da lista com filtros', { voltarPara: '/reservas?situacao=SOLICITADA' }, '/reservas?situacao=SOLICITADA'],
    ['sem state', null, '/reservas'],
    ['state sem origem', { outro: 1 }, '/reservas'],
    ['origem que não é texto', { voltarPara: 3 }, '/reservas'],
    ['origem fora do site', { voltarPara: '//site.com' }, '/reservas'],
  ])('caminhoDeVolta com %s', (_, estado, esperado) => {
    expect(caminhoDeVolta(estado)).toBe(esperado)
  })
})
