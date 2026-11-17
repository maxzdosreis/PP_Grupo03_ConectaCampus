import { comoHorario, ehHorarioValido, minutosDoInicio, minutosDoTermino } from '../../minutosDoDia.ts'

export type TerminoSugerido = { termino: string; limitadoPeloFechamento: boolean }

export function terminoSugerido(
  inicio: string,
  fechamento: string,
  duracaoSugeridaEmMinutos: number,
): TerminoSugerido | null {
  if (!ehHorarioValido(inicio) || !ehHorarioValido(fechamento)) return null
  const comeco = minutosDoInicio(inicio)
  const limite = minutosDoTermino(fechamento)
  if (comeco >= limite) return null
  const alvo = comeco + duracaoSugeridaEmMinutos
  if (alvo > limite) return { termino: comoHorario(limite), limitadoPeloFechamento: true }
  return { termino: comoHorario(alvo), limitadoPeloFechamento: false }
}
