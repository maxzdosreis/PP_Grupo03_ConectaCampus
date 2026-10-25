import { describe, expect, it } from 'vitest'
import { ErroDaApi, MENSAGEM_ERRO_INESPERADO } from './cliente.ts'
import { errosDosCampos, mensagemDoErro } from './erros.ts'

describe('mensagemDoErro', () => {
  it('usa a mensagem de um ErroDaApi', () => {
    const erro = new ErroDaApi(409, 'CONFLITO_DE_HORARIO', 'Este espaço já tem uma reserva.')

    expect(mensagemDoErro(erro)).toBe('Este espaço já tem uma reserva.')
  })

  it('usa a mensagem de erro inesperado para um Error comum', () => {
    expect(mensagemDoErro(new Error('detalhe interno'))).toBe(MENSAGEM_ERRO_INESPERADO)
  })

  it('usa a mensagem de erro inesperado para um valor qualquer', () => {
    expect(mensagemDoErro('texto')).toBe(MENSAGEM_ERRO_INESPERADO)
    expect(mensagemDoErro(null)).toBe(MENSAGEM_ERRO_INESPERADO)
  })
})

describe('errosDosCampos', () => {
  it('devolve a primeira mensagem de cada campo do ErroDaApi', () => {
    const erro = new ErroDaApi(400, 'DADOS_INVALIDOS', 'Verifique os dados informados.', {
      nome: ['Informe o nome.', 'Outro erro do nome.'],
      capacidade: ['A capacidade deve ser pelo menos 1.'],
      vazio: [],
    })

    expect(errosDosCampos(erro)).toEqual({
      nome: 'Informe o nome.',
      capacidade: 'A capacidade deve ser pelo menos 1.',
    })
  })

  it('devolve um objeto vazio para um ErroDaApi sem campos', () => {
    expect(errosDosCampos(new ErroDaApi(404, 'NAO_ENCONTRADO', 'Não encontrado.'))).toEqual({})
  })

  it('devolve um objeto vazio para um Error comum ou um valor qualquer', () => {
    expect(errosDosCampos(new Error('falhou'))).toEqual({})
    expect(errosDosCampos(undefined)).toEqual({})
  })
})
