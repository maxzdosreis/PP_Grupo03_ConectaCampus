import type { Espaco } from '../../api/espacos.ts'
import type { RegrasDeAgenda } from '../../api/reservas.ts'
import { formatarData, formatarDuracao, formatarFuncionamento } from '../../formatacao.ts'

export function descreverRegrasDeAgenda(regras: RegrasDeAgenda): string {
  const sugerida = `duração sugerida de ${formatarDuracao(regras.duracao_sugerida_em_minutos)}`
  const limites = `de ${formatarDuracao(regras.duracao_minima_em_minutos)} a ${formatarDuracao(regras.duracao_maxima_em_minutos)}`
  return `${sugerida} · ${limites} · até ${formatarData(regras.data_limite)}.`
}

export function descreverFuncionamento(espaco: Pick<Espaco, 'abertura' | 'fechamento'>): string {
  return `Este espaço funciona das ${formatarFuncionamento(espaco.abertura, espaco.fechamento)}.`
}
