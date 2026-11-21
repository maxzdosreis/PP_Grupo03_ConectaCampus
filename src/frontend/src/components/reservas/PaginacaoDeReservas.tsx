import type { Paginacao } from '../../api/tipos.ts'
import { Botao } from '../botao/Botao.tsx'
import estilos from './PaginacaoDeReservas.module.css'

type PropriedadesDaPaginacao = {
  paginacao: Paginacao
  nomeDosItens?: string
  aoMudarPagina: (pagina: number) => void
}

function PaginacaoDeReservas({
  paginacao,
  nomeDosItens = 'reservas',
  aoMudarPagina,
}: PropriedadesDaPaginacao) {
  const { pagina, total, total_de_paginas: totalDePaginas } = paginacao
  if (totalDePaginas <= 1) return null

  return (
    <nav aria-label="Paginação" className={estilos.paginacao}>
      <Botao acao="anterior" disabled={pagina <= 1} onClick={() => aoMudarPagina(pagina - 1)}>
        Anterior
      </Botao>
      <p className={estilos.posicao}>
        Página {pagina} de {totalDePaginas} · {total} {nomeDosItens}
      </p>
      <Botao
        acao="proxima"
        iconeAoFinal
        disabled={pagina >= totalDePaginas}
        onClick={() => aoMudarPagina(pagina + 1)}
      >
        Próxima
      </Botao>
    </nav>
  )
}

export default PaginacaoDeReservas
