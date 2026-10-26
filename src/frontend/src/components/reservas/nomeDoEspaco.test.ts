import { describe, expect, it } from 'vitest'
import type { Espaco } from '../../api/espacos.ts'
import { mapaDeNomesDosEspacos, nomeDoEspaco } from './nomeDoEspaco.ts'

const GINASIO: Espaco = {
  id: 1,
  nome: 'Ginásio A',
  tipo: 'GINASIO',
  tipo_rotulo: 'Ginásio',
  capacidade: 50,
  ativo: false,
}

describe('nomeDoEspaco', () => {
  it('devolve o nome de um espaço conhecido, mesmo inativo', () => {
    expect(nomeDoEspaco(mapaDeNomesDosEspacos([GINASIO]), 1)).toBe('Ginásio A')
  })

  it('devolve "Espaço #<id>" para um espaço desconhecido', () => {
    expect(nomeDoEspaco(mapaDeNomesDosEspacos([GINASIO]), 7)).toBe('Espaço #7')
  })

  it('devolve "Espaço #<id>" quando não há espaços carregados', () => {
    expect(nomeDoEspaco(new Map(), 1)).toBe('Espaço #1')
  })
})
