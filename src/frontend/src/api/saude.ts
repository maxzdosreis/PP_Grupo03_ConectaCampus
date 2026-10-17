import { requisitar } from './cliente.ts'

export type SituacaoDaApi = {
  banco: string
}

export function consultarSaude() {
  return requisitar<SituacaoDaApi>('/health/')
}
