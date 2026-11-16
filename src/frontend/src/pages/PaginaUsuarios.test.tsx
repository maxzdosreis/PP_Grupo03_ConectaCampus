import { screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Route, Routes, useLocation } from 'react-router'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { ErroDaApi } from '../api/cliente.ts'
import type { Paginacao, RespostaSucesso } from '../api/tipos.ts'
import {
  alterarUsuario,
  listarUsuarios,
  type ListaDeUsuarios,
  type UsuarioGerenciado,
} from '../api/usuarios.ts'
import { renderizarComProvedores, valorDaSessao } from '../testes/renderizar.tsx'
import { USUARIO_GESTOR } from '../testes/usuarios.ts'
import PaginaUsuarios from './PaginaUsuarios.tsx'

vi.mock('../api/usuarios.ts', () => ({
  listarUsuarios: vi.fn(),
  alterarUsuario: vi.fn(),
}))

function usuario(sobrescritas: Partial<UsuarioGerenciado>): UsuarioGerenciado {
  return {
    id: 2,
    nome: 'Bruno Lima',
    email: 'bruno.lima@exemplo.com',
    matricula: '2026101',
    perfil: 'SOLICITANTE',
    perfil_rotulo: 'Solicitante',
    eh_gestor: false,
    ativo: true,
    cadastrado_em: '2026-11-01T09:00:00-03:00',
    ultimo_acesso: null,
    ...sobrescritas,
  }
}

const CARLA = usuario({
  id: 1,
  nome: 'Carla Mendes',
  email: 'carla.mendes@exemplo.com',
  matricula: '2026900',
  perfil: 'GESTOR',
  perfil_rotulo: 'Gestor',
  eh_gestor: true,
  ultimo_acesso: '2026-11-16T08:30:00-03:00',
})
const BRUNO = usuario({})
const DANIELA = usuario({
  id: 3,
  nome: 'Daniela Rocha',
  email: 'daniela.rocha@exemplo.com',
  matricula: '2026102',
  ativo: false,
})
const OUTRA_GESTORA = usuario({
  id: 4,
  nome: 'Eva Gestora',
  email: 'eva.gestora@exemplo.com',
  matricula: '2026901',
  perfil: 'GESTOR',
  perfil_rotulo: 'Gestor',
  eh_gestor: true,
})

function paginacao(sobrescritas: Partial<Paginacao> = {}): Paginacao {
  return { pagina: 1, tamanho: 20, total: 3, total_de_paginas: 1, ...sobrescritas }
}

function lista(
  usuarios: UsuarioGerenciado[],
  mensagem = `${usuarios.length} usuários encontrados.`,
  sobrescritas: Partial<Paginacao> = {},
): RespostaSucesso<ListaDeUsuarios> {
  return {
    mensagem,
    dados: { usuarios, paginacao: paginacao({ total: usuarios.length, ...sobrescritas }) },
  }
}

function atualizado(dados: UsuarioGerenciado): RespostaSucesso<UsuarioGerenciado> {
  return { mensagem: 'Usuário atualizado.', dados }
}

function BuscaAtual() {
  return <output data-testid="busca">{useLocation().search}</output>
}

function renderizar(caminho = '/usuarios') {
  const sessao = valorDaSessao({ usuario: USUARIO_GESTOR })
  renderizarComProvedores(
    <Routes>
      <Route
        path="/usuarios"
        element={
          <>
            <PaginaUsuarios />
            <BuscaAtual />
          </>
        }
      />
    </Routes>,
    { caminho, sessao },
  )
  return sessao
}

function tabela() {
  return within(screen.getByRole('region', { name: /usuários? encontrados?\./ }))
}

async function abrirDialogo(nomeDoBotao: string, tituloDoDialogo: string) {
  await userEvent.click(await screen.findByRole('button', { name: nomeDoBotao }))
  return within(screen.getByRole('dialog', { name: tituloDoDialogo }))
}

describe('PaginaUsuarios', () => {
  beforeEach(() => {
    vi.mocked(listarUsuarios).mockReset()
    vi.mocked(alterarUsuario).mockReset()
    vi.mocked(listarUsuarios).mockResolvedValue(lista([CARLA, BRUNO, DANIELA]))
  })

  it('mostra a tabela com a contagem da API como legenda e o perfil e a situação em texto', async () => {
    renderizar()

    const regiao = await screen.findByRole('region', { name: '3 usuários encontrados.' })
    expect(within(regiao).getByRole('row', { name: /Bruno Lima/ })).toBeTruthy()
    const linhaDaDaniela = within(regiao).getByRole('row', { name: /Daniela Rocha/ })
    expect(within(linhaDaDaniela).getByText('Inativo')).toBeTruthy()
    expect(within(linhaDaDaniela).getByText('Solicitante')).toBeTruthy()
    const linhaDaCarla = within(regiao).getByRole('row', { name: /Carla Mendes/ })
    expect(within(linhaDaCarla).getByText('Gestor')).toBeTruthy()
    expect(listarUsuarios).toHaveBeenCalledWith({
      busca: '',
      perfil: '',
      ativo: '',
      pagina: '1',
    })
  })

  it('enquanto carrega, mostra o estado de carregamento', () => {
    vi.mocked(listarUsuarios).mockReturnValue(new Promise(() => {}))

    renderizar()

    expect(screen.getByText('Carregando usuários...')).toBeTruthy()
  })

  it('cada linha oferece só a ação válida de perfil e de situação, com o nome da pessoa', async () => {
    renderizar()

    await screen.findByRole('region', { name: '3 usuários encontrados.' })
    expect(screen.getByRole('button', { name: 'Promover a Gestor: Bruno Lima' })).toBeTruthy()
    expect(screen.getByRole('button', { name: 'Desativar: Bruno Lima' })).toBeTruthy()
    expect(screen.getByRole('button', { name: 'Reativar: Daniela Rocha' })).toBeTruthy()
    expect(screen.queryByRole('button', { name: 'Desativar: Daniela Rocha' })).toBeNull()
  })

  it('as ações do próprio usuário ficam desabilitadas, com a explicação em texto', async () => {
    renderizar()

    const rebaixar = (await screen.findByRole('button', {
      name: 'Rebaixar a Solicitante: Carla Mendes',
    })) as HTMLButtonElement
    const desativar = screen.getByRole('button', {
      name: 'Desativar: Carla Mendes',
    }) as HTMLButtonElement
    expect(rebaixar.disabled).toBe(true)
    expect(desativar.disabled).toBe(true)
    expect(rebaixar.getAttribute('aria-describedby')).toBeTruthy()
    expect(
      screen.getByText(/Você não pode rebaixar nem desativar a sua própria conta/),
    ).toBeTruthy()
    expect(screen.getByRole('row', { name: /Carla Mendes \(você\)/ })).toBeTruthy()
  })

  it('outro Gestor tem as ações habilitadas', async () => {
    vi.mocked(listarUsuarios).mockResolvedValue(lista([CARLA, OUTRA_GESTORA]))
    renderizar()

    const rebaixar = (await screen.findByRole('button', {
      name: 'Rebaixar a Solicitante: Eva Gestora',
    })) as HTMLButtonElement
    expect(rebaixar.disabled).toBe(false)
  })

  it('pede confirmação e não chama a API antes dela; "Voltar" fecha sem alterar', async () => {
    renderizar()

    const dialogo = await abrirDialogo('Promover a Gestor: Bruno Lima', 'Promover a Gestor')

    expect(alterarUsuario).not.toHaveBeenCalled()
    expect(dialogo.getByText('Bruno Lima')).toBeTruthy()
    await userEvent.click(dialogo.getByRole('button', { name: 'Voltar' }))
    expect(screen.queryByRole('dialog')).toBeNull()
    expect(alterarUsuario).not.toHaveBeenCalled()
  })

  it('promover: confirma, chama a API com o perfil, mostra a mensagem e recarrega a lista', async () => {
    vi.mocked(alterarUsuario).mockResolvedValue(
      atualizado(usuario({ perfil: 'GESTOR', eh_gestor: true })),
    )
    renderizar()
    const dialogo = await abrirDialogo('Promover a Gestor: Bruno Lima', 'Promover a Gestor')

    await userEvent.click(dialogo.getByRole('button', { name: 'Promover a Gestor' }))

    await waitFor(() => expect(alterarUsuario).toHaveBeenCalledWith(2, { perfil: 'GESTOR' }))
    expect(await screen.findByText('Usuário atualizado.')).toBeTruthy()
    await waitFor(() => expect(listarUsuarios).toHaveBeenCalledTimes(2))
    expect(screen.queryByRole('dialog')).toBeNull()
  })

  it('desativar chama a API com ativo falso e reativar, com ativo verdadeiro', async () => {
    vi.mocked(alterarUsuario).mockResolvedValue(atualizado(BRUNO))
    renderizar()

    const desativacao = await abrirDialogo('Desativar: Bruno Lima', 'Desativar conta')
    expect(desativacao.getByText(/reservas dela continuam como estão/)).toBeTruthy()
    await userEvent.click(desativacao.getByRole('button', { name: 'Desativar' }))
    await waitFor(() => expect(alterarUsuario).toHaveBeenCalledWith(2, { ativo: false }))

    const reativacao = await abrirDialogo('Reativar: Daniela Rocha', 'Reativar conta')
    await userEvent.click(reativacao.getByRole('button', { name: 'Reativar' }))
    await waitFor(() => expect(alterarUsuario).toHaveBeenCalledWith(3, { ativo: true }))
  })

  it('rebaixar outro Gestor chama a API com o perfil Solicitante', async () => {
    vi.mocked(listarUsuarios).mockResolvedValue(lista([CARLA, OUTRA_GESTORA]))
    vi.mocked(alterarUsuario).mockResolvedValue(atualizado(OUTRA_GESTORA))
    renderizar()
    const dialogo = await abrirDialogo(
      'Rebaixar a Solicitante: Eva Gestora',
      'Rebaixar a Solicitante',
    )

    await userEvent.click(dialogo.getByRole('button', { name: 'Rebaixar a Solicitante' }))

    await waitFor(() => expect(alterarUsuario).toHaveBeenCalledWith(4, { perfil: 'SOLICITANTE' }))
  })

  it.each([
    [409, 'ULTIMO_GESTOR_ATIVO', 'Esta é a última conta de Gestor ativa.'],
    [403, 'NAO_PODE_DESATIVAR_A_SI_MESMO', 'Você não pode desativar a sua própria conta.'],
  ])(
    'erro de regra %i %s aparece no diálogo, que continua aberto, sem sair da conta',
    async (status, codigo, mensagem) => {
      vi.mocked(alterarUsuario).mockRejectedValue(new ErroDaApi(status, codigo, mensagem))
      const sessao = renderizar()
      const dialogo = await abrirDialogo('Desativar: Bruno Lima', 'Desativar conta')

      await userEvent.click(dialogo.getByRole('button', { name: 'Desativar' }))

      expect(await dialogo.findByRole('alert')).toBeTruthy()
      expect(dialogo.getByRole('alert').textContent).toContain(mensagem)
      expect(screen.getByRole('dialog')).toBeTruthy()
      expect(sessao.sair).not.toHaveBeenCalled()
      expect(listarUsuarios).toHaveBeenCalledTimes(1)
    },
  )

  it('no 409 o diálogo oferece "Atualizar lista", que recarrega e fecha', async () => {
    vi.mocked(alterarUsuario).mockRejectedValue(
      new ErroDaApi(409, 'ULTIMO_GESTOR_ATIVO', 'Esta é a última conta de Gestor ativa.'),
    )
    renderizar()
    const dialogo = await abrirDialogo('Desativar: Bruno Lima', 'Desativar conta')
    await userEvent.click(dialogo.getByRole('button', { name: 'Desativar' }))

    await userEvent.click(await dialogo.findByRole('button', { name: 'Atualizar lista' }))

    await waitFor(() => expect(listarUsuarios).toHaveBeenCalledTimes(2))
    expect(screen.queryByRole('dialog')).toBeNull()
  })

  it('filtrar por perfil e por situação chama a API e guarda o filtro na URL', async () => {
    renderizar()
    await screen.findByRole('region', { name: '3 usuários encontrados.' })

    await userEvent.selectOptions(screen.getByLabelText('Perfil'), 'GESTOR')
    await waitFor(() =>
      expect(listarUsuarios).toHaveBeenLastCalledWith({
        busca: '',
        perfil: 'GESTOR',
        ativo: '',
        pagina: '1',
      }),
    )
    await userEvent.selectOptions(screen.getByLabelText('Situação'), 'false')

    await waitFor(() =>
      expect(listarUsuarios).toHaveBeenLastCalledWith({
        busca: '',
        perfil: 'GESTOR',
        ativo: 'false',
        pagina: '1',
      }),
    )
    expect(screen.getByTestId('busca').textContent).toBe('?perfil=GESTOR&ativo=false')
  })

  it('a busca só vai para a API depois de a pessoa parar de digitar', async () => {
    renderizar()
    await screen.findByRole('region', { name: '3 usuários encontrados.' })
    vi.mocked(listarUsuarios).mockClear()

    await userEvent.type(screen.getByLabelText('Busca'), ' bruno ')

    expect(listarUsuarios).not.toHaveBeenCalled()
    await waitFor(() => expect(listarUsuarios).toHaveBeenCalledTimes(1))
    expect(listarUsuarios).toHaveBeenCalledWith({
      busca: 'bruno',
      perfil: '',
      ativo: '',
      pagina: '1',
    })
    expect(screen.getByTestId('busca').textContent).toBe('?busca=bruno')
  })

  it('os filtros vindos da URL já são aplicados na primeira consulta', async () => {
    renderizar('/usuarios?busca=ana&perfil=SOLICITANTE&ativo=true&pagina=2')

    await screen.findByRole('region', { name: '3 usuários encontrados.' })

    expect(listarUsuarios).toHaveBeenCalledWith({
      busca: 'ana',
      perfil: 'SOLICITANTE',
      ativo: 'true',
      pagina: '2',
    })
    expect((screen.getByLabelText('Busca') as HTMLInputElement).value).toBe('ana')
  })

  it('"Limpar filtros" zera a busca, os seletores e a URL', async () => {
    renderizar('/usuarios?busca=ana&perfil=GESTOR')
    await screen.findByRole('region', { name: '3 usuários encontrados.' })

    await userEvent.click(screen.getByRole('button', { name: 'Limpar filtros' }))

    await waitFor(() => expect(screen.getByTestId('busca').textContent).toBe(''))
    expect((screen.getByLabelText('Busca') as HTMLInputElement).value).toBe('')
    expect((screen.getByLabelText('Perfil') as HTMLSelectElement).value).toBe('')
  })

  it('a paginação aparece com mais de uma página e "Próxima" pede a página seguinte', async () => {
    vi.mocked(listarUsuarios).mockResolvedValue(
      lista([CARLA, BRUNO], '45 usuários encontrados.', {
        total: 45,
        total_de_paginas: 3,
        tamanho: 20,
      }),
    )
    renderizar()
    const navegacao = await screen.findByRole('navigation', { name: 'Paginação' })
    expect(navegacao.textContent).toContain('Página 1 de 3 · 45 usuários')

    await userEvent.click(within(navegacao).getByRole('button', { name: 'Próxima' }))

    await waitFor(() =>
      expect(listarUsuarios).toHaveBeenLastCalledWith({
        busca: '',
        perfil: '',
        ativo: '',
        pagina: '2',
      }),
    )
    expect(screen.getByTestId('busca').textContent).toBe('?pagina=2')
  })

  it('mudar um filtro volta para a primeira página', async () => {
    vi.mocked(listarUsuarios).mockResolvedValue(
      lista([CARLA], '45 usuários encontrados.', {
        pagina: 3,
        total: 45,
        total_de_paginas: 3,
      }),
    )
    renderizar('/usuarios?pagina=3')
    await screen.findByRole('navigation', { name: 'Paginação' })

    await userEvent.selectOptions(screen.getByLabelText('Perfil'), 'GESTOR')

    await waitFor(() => expect(screen.getByTestId('busca').textContent).toBe('?perfil=GESTOR'))
  })

  it('uma página depois da última leva para a última página', async () => {
    vi.mocked(listarUsuarios).mockResolvedValue(
      lista([], 'Nenhum usuário encontrado.', { pagina: 9, total: 45, total_de_paginas: 3 }),
    )
    renderizar('/usuarios?pagina=9')

    await waitFor(() => expect(screen.getByTestId('busca').textContent).toBe('?pagina=3'))
  })

  it('número de página inválido na URL vale a primeira página', async () => {
    renderizar('/usuarios?pagina=abc')

    await screen.findByRole('region', { name: '3 usuários encontrados.' })

    expect(listarUsuarios).toHaveBeenCalledWith(expect.objectContaining({ pagina: '1' }))
  })

  it('lista vazia sem filtros mostra "Nenhum usuário cadastrado"', async () => {
    vi.mocked(listarUsuarios).mockResolvedValue(lista([], 'Nenhum usuário encontrado.'))
    renderizar()

    expect(await screen.findByText('Nenhum usuário cadastrado')).toBeTruthy()
    expect(screen.queryByRole('button', { name: 'Limpar filtros' })).toBeNull()
  })

  it('lista vazia com filtro mostra "Nenhum usuário encontrado" e o botão de limpar', async () => {
    vi.mocked(listarUsuarios).mockResolvedValue(lista([], 'Nenhum usuário encontrado.'))
    renderizar('/usuarios?busca=zzz')

    expect(await screen.findByText('Nenhum usuário encontrado')).toBeTruthy()
    expect(screen.getAllByRole('button', { name: 'Limpar filtros' })).toHaveLength(2)
  })

  it('falha ao carregar mostra a mensagem da API e "Tentar novamente"', async () => {
    vi.mocked(listarUsuarios).mockRejectedValueOnce(
      new ErroDaApi(403, 'ACAO_NAO_PERMITIDA', 'Você não tem permissão para realizar esta ação.'),
    )
    renderizar()

    expect(await screen.findByText('Você não tem permissão para realizar esta ação.')).toBeTruthy()
    await userEvent.click(screen.getByRole('button', { name: 'Tentar novamente' }))

    expect(await screen.findByRole('region', { name: '3 usuários encontrados.' })).toBeTruthy()
    expect(tabela().getByRole('row', { name: /Bruno Lima/ })).toBeTruthy()
  })
})
