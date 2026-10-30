import type { RegrasDeAgenda } from '../../api/reservas.ts'
import { formatarData, formatarDuracao } from '../../formatacao.ts'

export function descreverRegrasDeAgenda(regras: RegrasDeAgenda): string {
  const funcionamento = `Funcionamento das ${regras.horario_de_abertura} às ${regras.horario_de_fechamento}`
  const duracao = `duração de ${formatarDuracao(regras.duracao_minima_em_minutos)} a ${formatarDuracao(regras.duracao_maxima_em_minutos)}`
  return `${funcionamento} · ${duracao} · até ${formatarData(regras.data_limite)}.`
}
