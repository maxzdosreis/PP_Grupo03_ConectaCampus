import { act, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Route, Routes } from 'react-router'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cadastrar, entrar, usuarioAtual } from '../../api/autenticacao.ts'
import { ErroDaApi } from '../../api/cliente.ts'
import { lerSessao, limparSessao, salvarSessao, type Sessao } from '../../api/sessao.ts'
import { useSessao } from '../../hooks/useSessao.ts'
import LocalAtual from '../../testes/LocalAtual.tsx'
import { renderizarComSessaoReal } from '../../testes/renderizar.tsx'
import { USUARIO_GESTOR, USUARIO_SOLICITANTE } from '../../testes/usuarios.ts'
import RotaProtegida from './RotaProtegida.tsx'

vi.mock('../../api/autenticacao.ts', () => ({
  cadastrar: vi.fn(),
  entrar: vi.fn(),
  usuarioAtual: vi.fn(),
}))

const SESSAO: Sessao = { access: 'access-1', refresh: 'refresh-1', usuario: USUARIO_SOLICITANTE }

const LOGIN = {
  mensagem: 'Login realizado com sucesso.',
  dados: { access: 'access-9', refresh: 'refresh-9', usuario: USUARIO_GESTOR },
}

function EstadoDaSessao() {
  const { usuario, verificando, ehGestor, entrar: entrarNaSessao, cadastrarEEntrar, sair } =
    useSessao()
  const descricao = verificando
    ? 'verificando'
    : usuario
      ? `${usuario.nome}${ehGestor ? ' (gestor)' : ''}`
      : 'sem sessão'
  return (
    <>
      <output data-testid="sessao">{descricao}</output>
      <button
        type="button"
        onClick={() => entrarNaSessao({ email: 'carla.mendes@exemplo.com', senha: 'Apito-Dourado-48' })}
      >
        Entrar
      </button>
      <button
        type="button"
        onClick={() =>
          cadastrarEEntrar({
            nome: 'Carla Mendes',
            matricula: '2026900',
            email: 'carla.mendes@exemplo.com',
            senha: 'Apito-Dourado-48',
          })
        }
      >
        Cadastrar
      </button>
      <button type="button" onClick={sair}>
        Sair
      </button>
      <LocalAtual />
    </>
  )
}

function renderizar(caminho = '/') {
  renderizarComSessaoReal(
    <Routes>
      <Route path="/" element={<EstadoDaSessao />} />
      <Route path="/entrar" element={<EstadoDaSessao />} />
      <Route element={<RotaProtegida />}>
        <Route path="/reservas" element={<EstadoDaSessao />} />
      </Route>
    </Routes>,
    caminho,
  )
}

function sessao() {
  return screen.getByTestId('sessao').textContent
}

function local() {
  return screen.getByTestId('local').textContent
}

describe('SessaoProvider', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.mocked(cadastrar).mockReset()
    vi.mocked(entrar).mockReset()
    vi.mocked(usuarioAtual).mockReset()
  })

  afterEach(() => {
    limparSessao()
  })

  it('sem sessão salva, começa deslogado e não consulta o usuário', () => {
    renderizar()

    expect(sessao()).toBe('sem sessão')
    expect(usuarioAtual).not.toHaveBeenCalled()
  })

  it('restaura a sessão salva e confirma com /me, que atualiza o usuário', async () => {
    salvarSessao(SESSAO)
    const promovido = { ...USUARIO_SOLICITANTE, perfil: 'GESTOR', perfil_rotulo: 'Gestor', eh_gestor: true }
    vi.mocked(usuarioAtual).mockResolvedValue({ mensagem: 'Usuário autenticado.', dados: promovido })

    renderizar()

    expect(sessao()).toBe('verificando')
    await waitFor(() => expect(sessao()).toBe('Bruno Lima (gestor)'))
    expect(lerSessao()).toEqual({ ...SESSAO, usuario: promovido })
  })

  it('se /me responder 401, limpa a sessão', async () => {
    salvarSessao(SESSAO)
    vi.mocked(usuarioAtual).mockRejectedValue(
      new ErroDaApi(401, 'NAO_AUTENTICADO', 'Faça login para continuar.'),
    )

    renderizar()

    await waitFor(() => expect(sessao()).toBe('sem sessão'))
    expect(lerSessao()).toBeNull()
  })

  it('sem conexão ao confirmar, mantém a sessão', async () => {
    salvarSessao(SESSAO)
    vi.mocked(usuarioAtual).mockRejectedValue(new ErroDaApi(0, 'SEM_CONEXAO', 'Sem conexão.'))

    renderizar()

    await waitFor(() => expect(sessao()).toBe('Bruno Lima'))
    expect(lerSessao()).toEqual(SESSAO)
  })

  it('entrar salva a sessão, mostra a mensagem da API e libera o usuário', async () => {
    vi.mocked(entrar).mockResolvedValue(LOGIN)
    renderizar()

    await userEvent.click(screen.getByRole('button', { name: 'Entrar' }))

    expect(await screen.findByText('Login realizado com sucesso.')).toBeTruthy()
    expect(sessao()).toBe('Carla Mendes (gestor)')
    expect(lerSessao()).toEqual(LOGIN.dados)
    expect(entrar).toHaveBeenCalledWith({
      email: 'carla.mendes@exemplo.com',
      senha: 'Apito-Dourado-48',
    })
  })

  it('cadastrarEEntrar cadastra, depois entra com as mesmas credenciais', async () => {
    vi.mocked(cadastrar).mockResolvedValue({ mensagem: 'Cadastro realizado.', dados: USUARIO_GESTOR })
    vi.mocked(entrar).mockResolvedValue(LOGIN)
    renderizar()

    await userEvent.click(screen.getByRole('button', { name: 'Cadastrar' }))

    expect(await screen.findByText('Cadastro realizado com sucesso.')).toBeTruthy()
    expect(await screen.findByText('Login realizado com sucesso.')).toBeTruthy()
    expect(vi.mocked(cadastrar).mock.invocationCallOrder[0]).toBeLessThan(
      vi.mocked(entrar).mock.invocationCallOrder[0],
    )
    expect(entrar).toHaveBeenCalledWith({
      email: 'carla.mendes@exemplo.com',
      senha: 'Apito-Dourado-48',
    })
  })

  it('sair numa rota protegida limpa a sessão, avisa e vai para o início', async () => {
    salvarSessao(SESSAO)
    vi.mocked(usuarioAtual).mockResolvedValue({ mensagem: 'ok', dados: USUARIO_SOLICITANTE })
    renderizar('/reservas')
    await waitFor(() => expect(sessao()).toBe('Bruno Lima'))

    await userEvent.click(screen.getByRole('button', { name: 'Sair' }))

    expect(await screen.findByText('Você saiu da sua conta.')).toBeTruthy()
    expect(local()).toBe('/')
    expect(sessao()).toBe('sem sessão')
    expect(lerSessao()).toBeNull()
  })

  it('quando a sessão expira, avisa e leva para o login com o caminho atual', async () => {
    salvarSessao(SESSAO)
    vi.mocked(usuarioAtual).mockResolvedValue({ mensagem: 'ok', dados: USUARIO_SOLICITANTE })
    renderizar('/reservas?minhas=true')
    await waitFor(() => expect(sessao()).toBe('Bruno Lima'))

    act(() => limparSessao({ expirou: true }))

    expect(await screen.findByText('Sua sessão expirou. Faça login novamente.')).toBeTruthy()
    expect(local()).toBe('/entrar?proximo=%2Freservas%3Fminhas%3Dtrue')
    expect(sessao()).toBe('sem sessão')
  })
})
