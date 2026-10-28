import { screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Route, Routes } from 'react-router'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cadastrar, entrar } from '../api/autenticacao.ts'
import { ErroDaApi } from '../api/cliente.ts'
import { limparSessao } from '../api/sessao.ts'
import LocalAtual from '../testes/LocalAtual.tsx'
import { renderizarComSessaoReal } from '../testes/renderizar.tsx'
import { USUARIO_SOLICITANTE } from '../testes/usuarios.ts'
import PaginaCadastro from './PaginaCadastro.tsx'

vi.mock('../api/autenticacao.ts', () => ({
  cadastrar: vi.fn(),
  entrar: vi.fn(),
  usuarioAtual: vi.fn(),
}))

const DADOS = {
  nome: 'Bruno Lima',
  matricula: '2026101',
  email: 'bruno.lima@exemplo.com',
  senha: 'Rede-Alta-73',
}

const ROTAS = (
  <Routes>
    <Route path="/cadastro" element={<PaginaCadastro />} />
    <Route path="*" element={<LocalAtual />} />
  </Routes>
)

function controle(rotulo: string) {
  return screen.getByLabelText(rotulo) as HTMLInputElement
}

async function preencherEEnviar() {
  await userEvent.type(controle('Nome'), DADOS.nome)
  await userEvent.type(controle('Matrícula'), DADOS.matricula)
  await userEvent.type(controle('E-mail'), DADOS.email)
  await userEvent.type(controle('Senha'), DADOS.senha)
  await userEvent.click(screen.getByRole('button', { name: 'Criar conta' }))
}

describe('PaginaCadastro', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.mocked(cadastrar).mockReset()
    vi.mocked(entrar).mockReset()
  })

  afterEach(() => {
    limparSessao()
  })

  it('a senha pede uma senha nova e mostra a dica', () => {
    renderizarComSessaoReal(ROTAS, '/cadastro')

    expect(controle('Senha').autocomplete).toBe('new-password')
    expect(controle('Senha').getAttribute('aria-describedby')).toBeTruthy()
    expect(screen.getByText('Use pelo menos 8 caracteres.')).toBeTruthy()
  })

  it('com sucesso, cadastra, entra com as mesmas credenciais e vai para /reservas/nova', async () => {
    vi.mocked(cadastrar).mockResolvedValue({
      mensagem: 'Cadastro realizado com sucesso. Faça login para continuar.',
      dados: USUARIO_SOLICITANTE,
    })
    vi.mocked(entrar).mockResolvedValue({
      mensagem: 'Login realizado com sucesso.',
      dados: { access: 'access-1', refresh: 'refresh-1', usuario: USUARIO_SOLICITANTE },
    })
    renderizarComSessaoReal(ROTAS, '/cadastro')

    await preencherEEnviar()

    expect((await screen.findByTestId('local')).textContent).toBe('/reservas/nova')
    expect(cadastrar).toHaveBeenCalledWith(DADOS)
    expect(entrar).toHaveBeenCalledWith({ email: DADOS.email, senha: DADOS.senha })
    expect(vi.mocked(cadastrar).mock.invocationCallOrder[0]).toBeLessThan(
      vi.mocked(entrar).mock.invocationCallOrder[0],
    )
    expect(screen.getByText('Cadastro realizado com sucesso.')).toBeTruthy()
    expect(screen.getByText('Login realizado com sucesso.')).toBeTruthy()
  })

  it('e-mail já cadastrado aparece embaixo do e-mail, que recebe o foco, e não entra', async () => {
    vi.mocked(cadastrar).mockRejectedValue(
      new ErroDaApi(409, 'EMAIL_JA_CADASTRADO', 'Já existe um usuário com este e-mail.', {
        email: ['Já existe um usuário com este e-mail.'],
      }),
    )
    renderizarComSessaoReal(ROTAS, '/cadastro')

    await preencherEEnviar()

    expect(await screen.findByText('Já existe um usuário com este e-mail.')).toBeTruthy()
    expect(controle('E-mail').getAttribute('aria-invalid')).toBe('true')
    await waitFor(() => expect(document.activeElement).toBe(controle('E-mail')))
    expect(entrar).not.toHaveBeenCalled()
  })

  it('senha fraca aparece embaixo da senha', async () => {
    vi.mocked(cadastrar).mockRejectedValue(
      new ErroDaApi(400, 'SENHA_FRACA', 'Esta senha é muito comum.', {
        senha: ['Esta senha é muito comum.'],
      }),
    )
    renderizarComSessaoReal(ROTAS, '/cadastro')

    await preencherEEnviar()

    expect(await screen.findByText('Esta senha é muito comum.')).toBeTruthy()
    expect(controle('Senha').getAttribute('aria-invalid')).toBe('true')
  })

  it('o link de entrar preserva o ?proximo', () => {
    renderizarComSessaoReal(ROTAS, '/cadastro?proximo=%2Freservas')

    expect(screen.getByRole('link', { name: 'Entrar' }).getAttribute('href')).toBe(
      '/entrar?proximo=%2Freservas',
    )
  })
})
