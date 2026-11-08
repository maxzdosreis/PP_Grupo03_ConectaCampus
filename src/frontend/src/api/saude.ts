import { requisitar } from './cliente.ts'

export type SituacaoDaApi = {
  banco: string
  cache: string
}

export function consultarSaude() {
  return requisitar<SituacaoDaApi>('/health/')
}
