import { createContext } from 'react'

export type Mensagens = {
  mostrarSucesso: (texto: string) => void
  mostrarErro: (erroOuTexto: unknown) => void
}

export const TEMPO_DE_EXIBICAO_DO_SUCESSO_MS = 5000
export const MAXIMO_DE_NOTIFICACOES_VISIVEIS = 3

export const ContextoDeMensagens = createContext<Mensagens | null>(null)
