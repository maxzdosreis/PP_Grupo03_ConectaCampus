export function formatarData(data: string): string {
  const [ano, mes, dia] = data.split('-')
  return `${dia}/${mes}/${ano}`
}

export function formatarIntervalo(data: string, inicio: string, fim: string): string {
  return `${formatarData(data)}, ${inicio}–${fim}`
}

const MINUTOS_POR_HORA = 60

export function formatarDuracao(minutos: number): string {
  const horas = Math.floor(minutos / MINUTOS_POR_HORA)
  const restantes = minutos % MINUTOS_POR_HORA
  const partes = [horas > 0 && `${horas} h`, restantes > 0 && `${restantes} min`]
  return partes.filter(Boolean).join(' ')
}

export function formatarDataHora(iso: string): string {
  const [data, horario] = iso.split('T')
  return `${formatarData(data)} às ${horario.slice(0, 5)}`
}
