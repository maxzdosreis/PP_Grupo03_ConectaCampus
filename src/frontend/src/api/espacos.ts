import { requisitar } from './cliente.ts'
import { comParametros } from './parametros.ts'

export type Espaco = {
  id: number
  nome: string
  tipo: string
  tipo_rotulo: string
  capacidade: number
  ativo: boolean
}

export type TipoDeEspaco = {
  valor: string
  rotulo: string
}

export type FiltrosDeEspacos = {
  tipo?: string
  apenasAtivos?: boolean
}

export type DadosDoEspaco = {
  nome: string
  tipo: string
  capacidade: string
}

export function listarEspacos({ tipo, apenasAtivos }: FiltrosDeEspacos = {}) {
  return requisitar<Espaco[]>(
    comParametros('/espacos/', { tipo, apenas_ativos: apenasAtivos ? 'true' : undefined }),
  )
}

export function obterEspaco(id: number) {
  return requisitar<Espaco>(`/espacos/${id}/`)
}

export function listarTiposDeEspaco() {
  return requisitar<TipoDeEspaco[]>('/espacos/tipos/')
}

export function cadastrarEspaco(dados: DadosDoEspaco) {
  return requisitar<Espaco>('/espacos/', { method: 'POST', body: JSON.stringify(dados) })
}
