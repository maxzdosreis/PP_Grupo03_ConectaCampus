import type { Paginacao } from '../../api/tipos.ts'
import estilos from './PaginacaoDeReservas.module.css'

type PropriedadesDaPaginacao = {
  paginacao: Paginacao
  aoMudarPagina: (pagina: number) => void
}

function PaginacaoDeReservas({ paginacao, aoMudarPagina }: PropriedadesDaPaginacao) {
  const { pagina, total, total_de_paginas: totalDePaginas } = paginacao
  if (totalDePaginas <= 1) return null

  return (
    <nav aria-label="Paginação" className={estilos.paginacao}>
      <button
        type="button"
        disabled={pagina <= 1}
        onClick={() => aoMudarPagina(pagina - 1)}
      >
        Anterior
      </button>
      <p className={estilos.posicao}>
        Página {pagina} de {totalDePaginas} · {total} reservas
      </p>
      <button
        type="button"
        disabled={pagina >= totalDePaginas}
        onClick={() => aoMudarPagina(pagina + 1)}
      >
        Próxima
      </button>
    </nav>
  )
}

export default PaginacaoDeReservas
