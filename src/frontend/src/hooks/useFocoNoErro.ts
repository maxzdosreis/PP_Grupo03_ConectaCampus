import { useCallback, useEffect, useRef } from 'react'

export function useFocoNoErro(errosDosCampos: Record<string, string>, erroGeral: string | null) {
  const formulario = useRef<HTMLFormElement>(null)
  const aviso = useRef<HTMLDivElement>(null)
  const focarAoReceberErro = useRef(false)

  useEffect(() => {
    if (!focarAoReceberErro.current) return
    focarAoReceberErro.current = false
    const alvo = erroGeral
      ? aviso.current
      : formulario.current?.querySelector<HTMLElement>('[aria-invalid="true"]')
    alvo?.focus()
  }, [errosDosCampos, erroGeral])

  const focarNoProximoErro = useCallback(() => {
    focarAoReceberErro.current = true
  }, [])

  return { formulario, aviso, focarNoProximoErro }
}
