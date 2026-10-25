export function formatarData(data: string): string {
  const [ano, mes, dia] = data.split('-')
  return `${dia}/${mes}/${ano}`
}

export function formatarIntervalo(data: string, inicio: string, fim: string): string {
  return `${formatarData(data)}, ${inicio}–${fim}`
}
