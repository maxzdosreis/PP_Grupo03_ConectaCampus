import { useEffect } from 'react'

export function useTituloDaPagina(titulo: string) {
  useEffect(() => {
    document.title = `${titulo} · Conecta Campus`
  }, [titulo])
}
