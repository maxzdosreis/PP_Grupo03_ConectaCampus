export type ValorDeParametro = string | number | boolean | null | undefined

function estaVazio(valor: ValorDeParametro): valor is null | undefined | '' {
  return valor === undefined || valor === null || valor === ''
}

export function comParametros(
  caminho: string,
  parametros: Record<string, ValorDeParametro>,
): string {
  const busca = new URLSearchParams()
  for (const [nome, valor] of Object.entries(parametros)) {
    if (!estaVazio(valor)) {
      busca.append(nome, String(valor))
    }
  }
  const consulta = busca.toString()
  return consulta ? `${caminho}?${consulta}` : caminho
}
