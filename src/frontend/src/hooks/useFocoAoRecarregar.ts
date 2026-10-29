import { useCallback, useEffect, useEffectEvent, useRef } from 'react'

export function useFocoAoRecarregar(carregando: boolean, alvo: () => HTMLElement | null) {
  const focarAoCarregar = useRef(false)
  const focar = useEffectEvent(() => alvo()?.focus())

  useEffect(() => {
    if (!focarAoCarregar.current || carregando) return
    focarAoCarregar.current = false
    focar()
  }, [carregando])

  return useCallback(() => {
    focarAoCarregar.current = true
  }, [])
}
