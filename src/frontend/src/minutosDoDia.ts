export const MINUTOS_NO_DIA = 24 * 60
const MINUTOS_POR_HORA = 60

function minutosDe(horario: string): number {
  const [horas, minutos] = horario.split(':').map(Number)
  return horas * MINUTOS_POR_HORA + minutos
}

export function minutosDoInicio(horario: string): number {
  return minutosDe(horario)
}

export function minutosDoTermino(horario: string): number {
  const minutos = minutosDe(horario)
  return minutos === 0 ? MINUTOS_NO_DIA : minutos
}

export function comoHorario(minutos: number): string {
  const doDia = minutos % MINUTOS_NO_DIA
  const horas = Math.floor(doDia / MINUTOS_POR_HORA)
  const restantes = doDia % MINUTOS_POR_HORA
  return `${String(horas).padStart(2, '0')}:${String(restantes).padStart(2, '0')}`
}

export function ehHorarioValido(horario: string): boolean {
  return /^\d{2}:\d{2}$/.test(horario)
}
