import type { Espaco } from '../../api/espacos.ts'

export type NomesDosEspacos = ReadonlyMap<number, string>

export function mapaDeNomesDosEspacos(espacos: Espaco[]): NomesDosEspacos {
  return new Map(espacos.map(({ id, nome }) => [id, nome]))
}

export function rotuloDoEspacoDesconhecido(espacoId: number | string): string {
  return `Espaço #${espacoId}`
}

export function nomeDoEspaco(nomes: NomesDosEspacos, espacoId: number): string {
  return nomes.get(espacoId) ?? rotuloDoEspacoDesconhecido(espacoId)
}
