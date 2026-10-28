import { useContext } from 'react'
import { ContextoDeSessao, type ValorDaSessao } from '../components/sessao/contextoDeSessao.ts'

export function useSessao(): ValorDaSessao {
  const sessao = useContext(ContextoDeSessao)
  if (!sessao) {
    throw new Error('useSessao precisa estar dentro de <SessaoProvider>.')
  }
  return sessao
}
