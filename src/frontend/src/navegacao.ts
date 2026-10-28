export type ItemDeNavegacao = {
  rotulo: string
  caminho: string
  exigeLogin: boolean
}

export const CAMINHO_DAS_RESERVAS = '/reservas'
export const CAMINHO_DA_NOVA_RESERVA = '/reservas/nova'
export const CAMINHO_DE_ENTRAR = '/entrar'
export const CAMINHO_DO_CADASTRO = '/cadastro'
export const PARAMETRO_DO_ESPACO = 'espaco'
export const PARAMETRO_DO_PROXIMO = 'proximo'

export const ITENS_DE_NAVEGACAO: ItemDeNavegacao[] = [
  { rotulo: 'Início', caminho: '/', exigeLogin: false },
  { rotulo: 'Espaços', caminho: '/espacos', exigeLogin: true },
  { rotulo: 'Reservas', caminho: CAMINHO_DAS_RESERVAS, exigeLogin: true },
  { rotulo: 'Nova reserva', caminho: CAMINHO_DA_NOVA_RESERVA, exigeLogin: true },
]

export function itensVisiveis(autenticado: boolean): ItemDeNavegacao[] {
  return ITENS_DE_NAVEGACAO.filter(({ exigeLogin }) => autenticado || !exigeLogin)
}

export function caminhoParaReservar(espacoId: number): string {
  return `${CAMINHO_DA_NOVA_RESERVA}?${new URLSearchParams({ [PARAMETRO_DO_ESPACO]: String(espacoId) })}`
}

export function caminhoParaMinhasReservas(): string {
  return `${CAMINHO_DAS_RESERVAS}?${new URLSearchParams({ minhas: 'true' })}`
}

function comProximo(caminho: string, proximo: string | null): string {
  return proximo ? `${caminho}?${new URLSearchParams({ [PARAMETRO_DO_PROXIMO]: proximo })}` : caminho
}

export function caminhoParaEntrar(proximo: string | null = null): string {
  return comProximo(CAMINHO_DE_ENTRAR, proximo)
}

export function caminhoParaCadastro(proximo: string | null = null): string {
  return comProximo(CAMINHO_DO_CADASTRO, proximo)
}

export function proximoSeguro(
  valor: string | null,
  padrao: string = CAMINHO_DAS_RESERVAS,
): string {
  if (!valor || !valor.startsWith('/') || valor.startsWith('//') || valor.startsWith('/\\')) {
    return padrao
  }
  return valor
}
