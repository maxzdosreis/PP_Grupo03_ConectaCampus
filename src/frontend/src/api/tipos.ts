export type Paginacao = {
  pagina: number
  tamanho: number
  total: number
  total_de_paginas: number
}

export type RespostaSucesso<T> = {
  mensagem: string
  dados: T
  paginacao?: Paginacao
}

export type RespostaErro = {
  erro: {
    codigo: string
    mensagem: string
    campos?: Record<string, string[]>
  }
}
