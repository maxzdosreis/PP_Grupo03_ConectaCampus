import { screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Route, Routes } from 'react-router'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { entrar } from '../api/autenticacao.ts'
import { ErroDaApi } from '../api/cliente.ts'
import { limparSessao } from '../api/sessao.ts'
import LocalAtual from '../testes/LocalAtual.tsx'
import {
  renderizarComProvedores,
  renderizarComSessaoReal,
  valorDaSessao,
} from '../testes/renderizar.tsx'
import { USUARIO_SOLICITANTE } from '../testes/usuarios.ts'
import PaginaEntrar from './PaginaEntrar.tsx'

vi.mock('../api/autenticacao.ts', () => ({
  cadastrar: vi.fn(),
  entrar: vi.fn(),
  usuarioAtual: vi.fn(),
}))

const LOGIN = {
  mensagem: 'Login realizado com sucesso.',
  dados: { access: 'access-1', refresh: 'refresh-1', usuario: USUARIO_SOLICITANTE },
}

const ROTAS = (
  <Routes>
    <Route path="/entrar" element={<PaginaEntrar />} />
    <Route path="*" element={<LocalAtual />} />
  </Routes>
)

function controle(rotulo: string) {
  return screen.getByLabelText(rotulo) as HTMLInputElement
}

async function entrarCom(email: string, senha: string) {
  await userEvent.type(controle('E-mail'), email)
  await userEvent.type(controle('Senha'), senha)
  await userEvent.click(screen.getByRole('button', { name: 'Entrar' }))
}

describe('PaginaEntrar', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.mocked(entrar).mockReset()
  })

  afterEach(() => {
    limparSessao()
  })

  it('tem e-mail e senha com os tipos e o autocomplete certos, sem validação do navegador', () => {
    renderizarComSessaoReal(ROTAS, '/entrar')

    expect(controle('E-mail').type).toBe('email')
    expect(controle('E-mail').autocomplete).toBe('email')
    expect(controle('Senha').type).toBe('password')
    expect(controle('Senha').autocomplete).toBe('current-password')
    expect(screen.getByRole('heading', { level: 1, name: 'Entrar' })).toBeTruthy()
    expect(controle('E-mail').form?.noValidate).toBe(true)
  })

  it('com sucesso, mostra a mensagem da API e volta para o ?proximo', async () => {
    vi.mocked(entrar).mockResolvedValue(LOGIN)
    renderizarComSessaoReal(ROTAS, '/entrar?proximo=%2Freservas%3Fminhas%3Dtrue')

    await entrarCom('bruno.lima@exemplo.com', 'Rede-Alta-73')

    expect(await screen.findByTestId('local')).toBeTruthy()
    expect(screen.getByTestId('local').textContent).toBe('/reservas?minhas=true')
    expect(screen.getByText('Login realizado com sucesso.')).toBeTruthy()
    expect(entrar).toHaveBeenCalledWith({ email: 'bruno.lima@exemplo.com', senha: 'Rede-Alta-73' })
  })

  it('um ?proximo para fora do site cai em /reservas', async () => {
    vi.mocked(entrar).mockResolvedValue(LOGIN)
    renderizarComSessaoReal(ROTAS, '/entrar?proximo=%2F%2Fsite.com')

    await entrarCom('bruno.lima@exemplo.com', 'Rede-Alta-73')

    expect((await screen.findByTestId('local')).textContent).toBe('/reservas')
  })

  it('credenciais inválidas aparecem num aviso no topo, que recebe o foco', async () => {
    vi.mocked(entrar).mockRejectedValue(
      new ErroDaApi(401, 'CREDENCIAIS_INVALIDAS', 'E-mail ou senha incorretos.'),
    )
    renderizarComSessaoReal(ROTAS, '/entrar')

    await entrarCom('bruno.lima@exemplo.com', 'errada')

    const aviso = await screen.findByRole('alert')
    expect(aviso.textContent).toContain('E-mail ou senha incorretos.')
    await waitFor(() => expect(document.activeElement?.contains(aviso)).toBe(true))
    expect(controle('E-mail').value).toBe('bruno.lima@exemplo.com')
    expect(screen.queryByTestId('local')).toBeNull()
  })

  it('erros de campo aparecem embaixo do campo, que recebe o foco', async () => {
    vi.mocked(entrar).mockRejectedValue(
      new ErroDaApi(400, 'DADOS_INVALIDOS', 'Verifique os dados informados.', {
        email: ['Insira um endereço de email válido.'],
      }),
    )
    renderizarComSessaoReal(ROTAS, '/entrar')

    await entrarCom('bruno', 'Rede-Alta-73')

    expect(await screen.findByText('Insira um endereço de email válido.')).toBeTruthy()
    expect(controle('E-mail').getAttribute('aria-invalid')).toBe('true')
    await waitFor(() => expect(document.activeElement).toBe(controle('E-mail')))
  })

  it('já logado, vai direto para /reservas', () => {
    renderizarComProvedores(ROTAS, {
      caminho: '/entrar',
      sessao: valorDaSessao({ usuario: USUARIO_SOLICITANTE }),
    })

    expect(screen.getByTestId('local').textContent).toBe('/reservas')
  })

  it('o link de cadastro preserva o ?proximo', () => {
    renderizarComSessaoReal(ROTAS, '/entrar?proximo=%2Fespacos')

    expect(screen.getByRole('link', { name: 'Cadastre-se' }).getAttribute('href')).toBe(
      '/cadastro?proximo=%2Fespacos',
    )
  })
})
