import { describe, expect, it } from 'vitest'
import {
  caminhoParaCadastro,
  caminhoParaEntrar,
  itensVisiveis,
  proximoSeguro,
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
    expect(itensVisiveis(false).map(({ rotulo }) => rotulo)).toEqual(['Início'])
    expect(itensVisiveis(true).map(({ rotulo }) => rotulo)).toEqual([
      'Início',
      'Espaços',
      'Reservas',
      'Nova reserva',
    ])
  })
})
