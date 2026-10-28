import { createContext } from 'react'
import type {
  DadosDeCadastro,
  DadosDeLogin,
  RespostaDoLogin,
  Usuario,
} from '../../api/autenticacao.ts'
import type { RespostaSucesso } from '../../api/tipos.ts'

export type ValorDaSessao = {
  usuario: Usuario | null
  verificando: boolean
  autenticado: boolean
  ehGestor: boolean
  entrar: (dados: DadosDeLogin) => Promise<RespostaSucesso<RespostaDoLogin>>
  cadastrarEEntrar: (dados: DadosDeCadastro) => Promise<RespostaSucesso<RespostaDoLogin>>
  sair: () => void
}

export const MENSAGEM_DE_CADASTRO = 'Cadastro realizado com sucesso.'
export const MENSAGEM_DE_SAIDA = 'Você saiu da sua conta.'

export const ContextoDeSessao = createContext<ValorDaSessao | null>(null)
