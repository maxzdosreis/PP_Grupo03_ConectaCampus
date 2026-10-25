import { useContext } from 'react'
import { ContextoDeMensagens, type Mensagens } from '../components/mensagens/contextoDeMensagens.ts'

export function useMensagens(): Mensagens {
  const mensagens = useContext(ContextoDeMensagens)
  if (!mensagens) {
    throw new Error('useMensagens precisa estar dentro de <MensagensProvider>.')
  }
  return mensagens
}
