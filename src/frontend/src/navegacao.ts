export type ItemDeNavegacao = {
  rotulo: string
  caminho: string
}

export const CAMINHO_DA_NOVA_RESERVA = '/reservas/nova'
export const PARAMETRO_DO_ESPACO = 'espaco'

export const ITENS_DE_NAVEGACAO: ItemDeNavegacao[] = [
  { rotulo: 'Início', caminho: '/' },
  { rotulo: 'Espaços', caminho: '/espacos' },
  { rotulo: 'Nova reserva', caminho: CAMINHO_DA_NOVA_RESERVA },
]

export function caminhoParaReservar(espacoId: number): string {
  return `${CAMINHO_DA_NOVA_RESERVA}?${new URLSearchParams({ [PARAMETRO_DO_ESPACO]: String(espacoId) })}`
}
