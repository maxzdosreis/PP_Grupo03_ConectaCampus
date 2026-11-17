import type { HorarioLivre } from '../../api/reservas.ts'
import { comoHorario, minutosDoInicio, minutosDoTermino } from '../../minutosDoDia.ts'

export function horarioSugerido(
  livre: HorarioLivre,
  duracaoMaximaEmMinutos: number | null,
): HorarioLivre {
  if (duracaoMaximaEmMinutos === null) return livre
  const fim = Math.min(
    minutosDoTermino(livre.hora_fim),
    minutosDoInicio(livre.hora_inicio) + duracaoMaximaEmMinutos,
  )
  return { hora_inicio: livre.hora_inicio, hora_fim: comoHorario(fim) }
}

export type PosicaoNaFaixa = { inicio: number; largura: number }

export function posicaoNaFaixa(
  { hora_inicio, hora_fim }: HorarioLivre,
  abertura: string,
  fechamento: string,
): PosicaoNaFaixa {
  const comeco = minutosDoInicio(abertura)
  const total = minutosDoTermino(fechamento) - comeco
  const limitar = (minutos: number) => Math.min(Math.max(minutos - comeco, 0), total)
  const inicio = limitar(minutosDoInicio(hora_inicio))
  const fim = limitar(minutosDoTermino(hora_fim))
  return { inicio: (inicio / total) * 100, largura: ((fim - inicio) / total) * 100 }
}
