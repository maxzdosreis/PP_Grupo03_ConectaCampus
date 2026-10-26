import { requisitar } from './cliente.ts'
import { comParametros } from './parametros.ts'

export type Solicitante = {
  usuario_id: number
  nome: string
  matricula: string
}

export type Reserva = {
  id: number
  espaco_id: number
  solicitante: Solicitante
  data: string
  hora_inicio: string
  hora_fim: string
  finalidade: string
  situacao: string
  situacao_rotulo: string
  motivo_da_situacao: string | null
  criada_em: string
}

export type DadosDaReserva = {
  espaco_id: string
  data: string
  hora_inicio: string
  hora_fim: string
  finalidade: string
}

export type FiltrosDeReservas = {
  espaco?: string
  situacao?: string
  data?: string
  solicitante?: string
  minhas?: boolean
}

export type SituacaoDeReserva = {
  valor: string
  rotulo: string
}

export function solicitarReserva(dados: DadosDaReserva) {
  return requisitar<Reserva>('/reservas/', { method: 'POST', body: JSON.stringify(dados) })
}

export function listarReservas({
  espaco,
  situacao,
  data,
  solicitante,
  minhas,
}: FiltrosDeReservas = {}) {
  return requisitar<Reserva[]>(
    comParametros('/reservas/', {
      espaco,
      situacao,
      data,
      solicitante,
      minhas: minhas ? 'true' : undefined,
    }),
  )
}

export function listarSituacoesDeReserva() {
  return requisitar<SituacaoDeReserva[]>('/reservas/situacoes/')
}
