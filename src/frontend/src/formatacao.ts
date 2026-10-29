export function formatarData(data: string): string {
  const [ano, mes, dia] = data.split('-')
  return `${dia}/${mes}/${ano}`
}

export function formatarIntervalo(data: string, inicio: string, fim: string): string {
  return `${formatarData(data)}, ${inicio}–${fim}`
}

export function formatarDataHora(iso: string): string {
  const [data, horario] = iso.split('T')
  return `${formatarData(data)} às ${horario.slice(0, 5)}`
}
