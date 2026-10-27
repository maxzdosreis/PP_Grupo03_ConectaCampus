import { useCallback, useEffect, useRef, useState } from 'react'
import { ErroDaApi } from '../api/cliente.ts'
import { errosDosCampos as extrairErrosDosCampos, mensagemDoErro } from '../api/erros.ts'
import type { RespostaSucesso } from '../api/tipos.ts'

export type Envio<E, R> = {
  enviar: (dados: E) => Promise<RespostaSucesso<R> | null>
  enviando: boolean
  errosDosCampos: Record<string, string>
  erroGeral: string | null
  statusDoErro: number | null
  limparErroDoCampo: (campo: string) => void
}

export function useEnvio<E, R>(
  enviarDados: (dados: E) => Promise<RespostaSucesso<R>>,
): Envio<E, R> {
  const [enviando, setEnviando] = useState(false)
  const [errosDosCampos, setErrosDosCampos] = useState<Record<string, string>>({})
  const [erroGeral, setErroGeral] = useState<string | null>(null)
  const [statusDoErro, setStatusDoErro] = useState<number | null>(null)
  const montado = useRef(false)

  useEffect(() => {
    montado.current = true
    return () => {
      montado.current = false
    }
  }, [])

  const registrarErro = useCallback((erro: unknown) => {
    const campos = extrairErrosDosCampos(erro)
    const temCampos = Object.keys(campos).length > 0
    setErrosDosCampos(campos)
    setErroGeral(temCampos ? null : mensagemDoErro(erro))
    setStatusDoErro(erro instanceof ErroDaApi ? erro.status : null)
  }, [])

  const enviar = useCallback(
    async (dados: E) => {
      setEnviando(true)
      try {
        const resposta = await enviarDados(dados)
        if (!montado.current) return null
        setErrosDosCampos({})
        setErroGeral(null)
        setStatusDoErro(null)
        return resposta
      } catch (erro) {
        if (montado.current) registrarErro(erro)
        return null
      } finally {
        if (montado.current) setEnviando(false)
      }
    },
    [enviarDados, registrarErro],
  )

  const limparErroDoCampo = useCallback((campo: string) => {
    setErrosDosCampos((atuais) =>
      campo in atuais
        ? Object.fromEntries(Object.entries(atuais).filter(([nome]) => nome !== campo))
        : atuais,
    )
  }, [])

  return { enviar, enviando, errosDosCampos, erroGeral, statusDoErro, limparErroDoCampo }
}
