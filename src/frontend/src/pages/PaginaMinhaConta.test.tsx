import { act, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Route, Routes } from 'react-router'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { alterarSenha, usuarioAtual } from '../api/autenticacao.ts'
import { ErroDaApi } from '../api/cliente.ts'
import { lerSessao, limparSessao, salvarSessao } from '../api/sessao.ts'
import LocalAtual from '../testes/LocalAtual.tsx'
import { renderizarComSessaoReal } from '../testes/renderizar.tsx'
import { USUARIO_SOLICITANTE } from '../testes/usuarios.ts'
import PaginaMinhaConta from './PaginaMinhaConta.tsx'

vi.mock('../api/autenticacao.ts', () => ({
  alterarSenha: vi.fn(),
  entrar: vi.fn(),
  cadastrar: vi.fn(),
  sair: vi.fn(),
  usuarioAtual: vi.fn(),
}))

const SESSAO = { access: 'access-1', refresh: 'refresh-1', usuario: USUARIO_SOLICITANTE }

const ROTAS = (
  <Routes>
    <Route path="/conta" element={<PaginaMinhaConta />} />
    <Route path="*" element={<LocalAtual />} />
  </Routes>
)

function controle(rotulo: string) {
  return screen.getByLabelText(rotulo) as HTMLInputElement
}

async function preencher(atual = 'Rede-Alta-73', nova = 'Cesta-Tripla-59', confirmacao = nova) {
  await userEvent.type(controle('Senha atual'), atual)
  await userEvent.type(controle('Nova senha'), nova)
  await userEvent.type(controle('Confirme a nova senha'), confirmacao)
}

const enviar = () => userEvent.click(screen.getByRole('button', { name: 'Alterar senha' }))

function renderizar() {
  return renderizarComSessaoReal(ROTAS, '/conta')
}

describe('PaginaMinhaConta', () => {
  beforeEach(() => {
    localStorage.clear()
    salvarSessao(SESSAO)
    vi.mocked(alterarSenha).mockReset()
    vi.mocked(usuarioAtual)
      .mockReset()
      .mockResolvedValue({ mensagem: 'ok', dados: USUARIO_SOLICITANTE })
  })

  afterEach(() => {
    limparSessao()
  })

  it('mostra os dados da conta e o formulário com os três campos de senha', async () => {
    renderizar()

    expect(screen.getByRole('heading', { name: 'Minha conta' })).toBeTruthy()
    expect(screen.getByText(/bruno\.lima@exemplo\.com/)).toBeTruthy()
    expect(controle('Senha atual').type).toBe('password')
    expect(controle('Senha atual').autocomplete).toBe('current-password')
    expect(controle('Nova senha').autocomplete).toBe('new-password')
    expect(controle('Nova senha').getAttribute('aria-describedby')).toBeTruthy()
    expect(controle('Confirme a nova senha').type).toBe('password')
    await waitFor(() => expect(usuarioAtual).toHaveBeenCalled())
  })

  it('confirmação diferente da nova senha mostra o erro e não chama a API', async () => {
    renderizar()

    await preencher('Rede-Alta-73', 'Cesta-Tripla-59', 'Cesta-Tripla-00')
    await enviar()

    expect(await screen.findByText('A confirmação não é igual à nova senha.')).toBeTruthy()
    expect(controle('Confirme a nova senha').getAttribute('aria-invalid')).toBe('true')
    expect(document.activeElement).toBe(controle('Confirme a nova senha'))
    expect(alterarSenha).not.toHaveBeenCalled()
  })

  it('sucesso envia a senha e o refresh da sessão, limpa os campos e mantém a pessoa logada', async () => {
    vi.mocked(alterarSenha).mockResolvedValue({ mensagem: 'Senha alterada com sucesso.', dados: null })
    renderizar()

    await preencher()
    await enviar()

    expect(await screen.findByText('Senha alterada com sucesso.')).toBeTruthy()
    expect(alterarSenha).toHaveBeenCalledWith({
      senha_atual: 'Rede-Alta-73',
      nova_senha: 'Cesta-Tripla-59',
      refresh_atual: 'refresh-1',
    })
    expect(controle('Senha atual').value).toBe('')
    expect(controle('Nova senha').value).toBe('')
    expect(controle('Confirme a nova senha').value).toBe('')
    expect(lerSessao()?.access).toBe('access-1')
  })

  it('senha atual errada mostra a mensagem no campo e NÃO desloga', async () => {
    vi.mocked(alterarSenha).mockRejectedValue(
      new ErroDaApi(400, 'SENHA_ATUAL_INCORRETA', 'A senha atual está incorreta.', {
        senha_atual: ['A senha atual está incorreta.'],
      }),
    )
    renderizar()

    await preencher('errada-errada-1')
    await enviar()

    expect(await screen.findByText('A senha atual está incorreta.')).toBeTruthy()
    expect(controle('Senha atual').getAttribute('aria-invalid')).toBe('true')
    await waitFor(() => expect(document.activeElement).toBe(controle('Senha atual')))
    expect(lerSessao()).toEqual(SESSAO)
    expect(screen.queryByTestId('local')).toBeNull()
    expect(screen.getByRole('heading', { name: 'Minha conta' })).toBeTruthy()
  })

  it('erro de política mostra a mensagem embaixo da nova senha', async () => {
    vi.mocked(alterarSenha).mockRejectedValue(
      new ErroDaApi(400, 'SENHA_FRACA', 'Esta senha é muito comum.', {
        nova_senha: ['Esta senha é muito comum.'],
      }),
    )
    renderizar()

    await preencher('Rede-Alta-73', 'password')
    await enviar()

    expect(await screen.findByText('Esta senha é muito comum.')).toBeTruthy()
    expect(controle('Nova senha').getAttribute('aria-invalid')).toBe('true')
  })

  it('limite de tentativas aparece no aviso do topo', async () => {
    vi.mocked(alterarSenha).mockRejectedValue(
      new ErroDaApi(429, 'LIMITE_DE_TENTATIVAS', 'Muitas tentativas. Tente de novo em 42 segundos.'),
    )
    renderizar()

    await preencher()
    await enviar()

    const aviso = await screen.findByRole('alert')
    expect(aviso.textContent).toContain('Muitas tentativas. Tente de novo em 42 segundos.')
    expect(lerSessao()).toEqual(SESSAO)
  })

  it('durante o envio, o botão fica desabilitado com o texto "Alterando..."', async () => {
    let concluir!: () => void
    vi.mocked(alterarSenha).mockReturnValue(
      new Promise((resolver) => {
        concluir = () => resolver({ mensagem: 'Senha alterada com sucesso.', dados: null })
      }),
    )
    renderizar()

    await preencher()
    await enviar()

    const botao = await screen.findByRole('button', { name: 'Alterando...' })
    expect((botao as HTMLButtonElement).disabled).toBe(true)

    await act(async () => concluir())
    expect(
      (await screen.findByRole('button', { name: 'Alterar senha' }) as HTMLButtonElement).disabled,
    ).toBe(false)
  })
})
