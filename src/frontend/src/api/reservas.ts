import { requisitar } from './cliente.ts'

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

export function solicitarReserva(dados: DadosDaReserva) {
  return requisitar<Reserva>('/reservas/', { method: 'POST', body: JSON.stringify(dados) })
}
