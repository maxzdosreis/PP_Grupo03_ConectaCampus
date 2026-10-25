import { ErroDaApi, MENSAGEM_ERRO_INESPERADO } from './cliente.ts'

export function mensagemDoErro(erro: unknown): string {
  return erro instanceof ErroDaApi ? erro.message : MENSAGEM_ERRO_INESPERADO
}

export function errosDosCampos(erro: unknown): Record<string, string> {
  if (!(erro instanceof ErroDaApi)) {
    return {}
  }
  return Object.fromEntries(
    Object.entries(erro.campos)
      .filter(([, mensagens]) => mensagens.length > 0)
      .map(([campo, mensagens]) => [campo, mensagens[0]]),
  )
}
