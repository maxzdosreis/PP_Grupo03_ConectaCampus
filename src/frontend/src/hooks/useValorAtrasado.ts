import { useEffect, useState } from 'react'

export function useValorAtrasado<T>(valor: T, atrasoMs: number): T {
  const [atrasado, setAtrasado] = useState(valor)

  useEffect(() => {
    const temporizador = setTimeout(() => setAtrasado(valor), atrasoMs)
    return () => clearTimeout(temporizador)
  }, [valor, atrasoMs])

  return atrasado
}
