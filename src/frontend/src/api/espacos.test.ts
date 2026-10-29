import { beforeEach, describe, expect, it, vi } from 'vitest'
import { requisitar } from './cliente.ts'
import {
  ativarEspaco,
  cadastrarEspaco,
  desativarEspaco,
  editarEspaco,
  listarEspacos,
  listarTiposDeEspaco,
  obterEspaco,
} from './espacos.ts'

vi.mock('./cliente.ts', async (importarOriginal) => ({
  ...(await importarOriginal<typeof import('./cliente.ts')>()),
  requisitar: vi.fn(),
}))

describe('api de espaços', () => {
  beforeEach(() => {
    vi.mocked(requisitar).mockReset()
    vi.mocked(requisitar).mockResolvedValue({ mensagem: 'ok', dados: [] })
  })

  it.each([
    [{}, '/espacos/'],
    [{ tipo: 'GINASIO' }, '/espacos/?tipo=GINASIO'],
    [{ apenasAtivos: true }, '/espacos/?apenas_ativos=true'],
    [{ tipo: 'GINASIO', apenasAtivos: true }, '/espacos/?tipo=GINASIO&apenas_ativos=true'],
    [{ tipo: '', apenasAtivos: false }, '/espacos/'],
  ])('listarEspacos(%j) pede %s', async (filtros, caminho) => {
    await listarEspacos(filtros)

    expect(requisitar).toHaveBeenCalledWith(caminho)
  })

  it('obterEspaco pede o espaço pelo id', async () => {
    await obterEspaco(3)

    expect(requisitar).toHaveBeenCalledWith('/espacos/3/')
  })

  it('listarTiposDeEspaco pede os tipos', async () => {
    await listarTiposDeEspaco()

    expect(requisitar).toHaveBeenCalledWith('/espacos/tipos/')
  })

  it('cadastrarEspaco envia um POST com a capacidade como foi digitada', async () => {
    await cadastrarEspaco({ nome: 'Ginásio A', tipo: 'GINASIO', capacidade: '50' })

    expect(requisitar).toHaveBeenCalledWith('/espacos/', {
      method: 'POST',
      body: JSON.stringify({ nome: 'Ginásio A', tipo: 'GINASIO', capacidade: '50' }),
    })
  })

  it('editarEspaco envia um PATCH só com os campos informados', async () => {
    await editarEspaco(4, { capacidade: '30', nome: undefined })

    expect(requisitar).toHaveBeenCalledWith('/espacos/4/', {
      method: 'PATCH',
      body: '{"capacidade":"30"}',
    })
  })

  it.each([
    [desativarEspaco, '/espacos/4/desativar/'],
    [ativarEspaco, '/espacos/4/ativar/'],
  ])('%o envia um POST sem corpo para %s', async (acao, caminho) => {
    await acao(4)

    expect(requisitar).toHaveBeenCalledWith(caminho, { method: 'POST' })
  })
})
