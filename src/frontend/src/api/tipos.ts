export type RespostaSucesso<T> = {
  mensagem: string
  dados: T
}

export type RespostaErro = {
  erro: {
    codigo: string
    mensagem: string
    campos?: Record<string, string[]>
  }
}
