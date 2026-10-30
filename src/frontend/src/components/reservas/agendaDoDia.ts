import type { HorarioLivre } from '../../api/reservas.ts'

const MINUTOS_POR_HORA = 60

function emMinutos(horario: string): number {
  const [horas, minutos] = horario.split(':').map(Number)
  return horas * MINUTOS_POR_HORA + minutos
}

function comoHorario(minutos: number): string {
  const horas = Math.floor(minutos / MINUTOS_POR_HORA)
  const restantes = minutos % MINUTOS_POR_HORA
  return `${String(horas).padStart(2, '0')}:${String(restantes).padStart(2, '0')}`
}

export function horarioSugerido(
  livre: HorarioLivre,
  duracaoMaximaEmMinutos: number | null,
): HorarioLivre {
  if (duracaoMaximaEmMinutos === null) return livre
  const fim = Math.min(emMinutos(livre.hora_fim), emMinutos(livre.hora_inicio) + duracaoMaximaEmMinutos)
  return { hora_inicio: livre.hora_inicio, hora_fim: comoHorario(fim) }
}

export type PosicaoNaFaixa = { inicio: number; largura: number }

export function posicaoNaFaixa(
  { hora_inicio, hora_fim }: HorarioLivre,
  abertura: string,
  fechamento: string,
): PosicaoNaFaixa {
  const comeco = emMinutos(abertura)
  const total = emMinutos(fechamento) - comeco
  const limitar = (minutos: number) => Math.min(Math.max(minutos - comeco, 0), total)
  const inicio = limitar(emMinutos(hora_inicio))
  const fim = limitar(emMinutos(hora_fim))
  return { inicio: (inicio / total) * 100, largura: ((fim - inicio) / total) * 100 }
}
