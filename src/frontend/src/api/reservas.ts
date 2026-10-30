import { requisitar } from './cliente.ts'
import { comParametros } from './parametros.ts'

export type Solicitante = {
  usuario_id: number
  nome: string
  matricula: string
}

export type AcaoDisponivel = {
  situacao: string
  rotulo: string
  exige_motivo: boolean
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
  acoes_disponiveis: AcaoDisponivel[]
}

export type AlteracaoDeSituacao = {
  situacao: string
  motivo?: string
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

export type RegrasDeAgenda = {
  horario_de_abertura: string
  horario_de_fechamento: string
  duracao_minima_em_minutos: number
  duracao_maxima_em_minutos: number
  antecedencia_maxima_em_dias: number
  data_limite: string
}

export type RegistroDeSituacao = {
  situacao_anterior: string | null
  situacao_anterior_rotulo: string | null
  situacao_nova: string
  situacao_nova_rotulo: string
  motivo: string | null
  autor: { nome: string }
  registrado_em: string
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

export function obterReserva(id: number) {
  return requisitar<Reserva>(`/reservas/${id}/`)
}

export function listarHistoricoDaReserva(id: number) {
  return requisitar<RegistroDeSituacao[]>(`/reservas/${id}/historico/`)
}

export function alterarSituacaoReserva(id: number, dados: AlteracaoDeSituacao) {
  return requisitar<Reserva>(`/reservas/${id}/situacao/`, {
    method: 'PATCH',
    body: JSON.stringify(dados),
  })
}

export function listarSituacoesDeReserva() {
  return requisitar<SituacaoDeReserva[]>('/reservas/situacoes/')
}

export function obterRegrasDeAgenda() {
  return requisitar<RegrasDeAgenda>('/reservas/regras-de-agenda/')
}
