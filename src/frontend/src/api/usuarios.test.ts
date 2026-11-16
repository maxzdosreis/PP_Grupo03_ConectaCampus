import { beforeEach, describe, expect, it, vi } from 'vitest'
import { ErroDaApi, requisitar } from './cliente.ts'
import { alterarUsuario, listarUsuarios } from './usuarios.ts'

vi.mock('./cliente.ts', async (importarOriginal) => ({
  ...(await importarOriginal<typeof import('./cliente.ts')>()),
  requisitar: vi.fn(),
}))

const PAGINACAO = { pagina: 1, tamanho: 20, total: 0, total_de_paginas: 0 }

describe('api de usuários', () => {
  beforeEach(() => {
    vi.mocked(requisitar).mockReset()
    vi.mocked(requisitar).mockResolvedValue({ mensagem: 'ok', dados: [], paginacao: PAGINACAO })
  })

  it('listarUsuarios sem filtros consulta /usuarios/ sem parâmetros', async () => {
    await listarUsuarios()

    expect(requisitar).toHaveBeenCalledWith('/usuarios/')
  })

  it('listarUsuarios envia só os filtros preenchidos, com os nomes da API', async () => {
    await listarUsuarios({ busca: 'ana', perfil: 'GESTOR', ativo: 'false', pagina: '3' })

    expect(requisitar).toHaveBeenCalledWith(
      '/usuarios/?busca=ana&perfil=GESTOR&ativo=false&pagina=3',
    )
  })

  it('listarUsuarios ignora filtros em branco', async () => {
    await listarUsuarios({ busca: '', perfil: '', ativo: '', pagina: '' })

    expect(requisitar).toHaveBeenCalledWith('/usuarios/')
  })

  it('listarUsuarios devolve os usuários e a paginação juntos', async () => {
    vi.mocked(requisitar).mockResolvedValue({
      mensagem: '1 usuário encontrado.',
      dados: [{ id: 7 }],
      paginacao: { ...PAGINACAO, total: 1, total_de_paginas: 1 },
    })

    const resposta = await listarUsuarios()

    expect(resposta.mensagem).toBe('1 usuário encontrado.')
    expect(resposta.dados.usuarios).toEqual([{ id: 7 }])
    expect(resposta.dados.paginacao.total).toBe(1)
  })

  it('listarUsuarios sem paginação na resposta é um erro inesperado', async () => {
    vi.mocked(requisitar).mockResolvedValue({ mensagem: 'ok', dados: [] })

    await expect(listarUsuarios()).rejects.toBeInstanceOf(ErroDaApi)
  })

  it('alterarUsuario envia um PATCH só com o que mudou', async () => {
    await alterarUsuario(7, { perfil: 'GESTOR' })
    await alterarUsuario(7, { ativo: false })

    expect(requisitar).toHaveBeenNthCalledWith(1, '/usuarios/7/', {
      method: 'PATCH',
      body: JSON.stringify({ perfil: 'GESTOR' }),
    })
    expect(requisitar).toHaveBeenNthCalledWith(2, '/usuarios/7/', {
      method: 'PATCH',
      body: JSON.stringify({ ativo: false }),
    })
  })
})
