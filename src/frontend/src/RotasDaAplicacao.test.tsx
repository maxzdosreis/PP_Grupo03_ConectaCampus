import { screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import RotasDaAplicacao from './RotasDaAplicacao.tsx'
import LocalAtual from './testes/LocalAtual.tsx'
import { renderizarComProvedores, valorDaSessao } from './testes/renderizar.tsx'
import { USUARIO_GESTOR, USUARIO_SOLICITANTE } from './testes/usuarios.ts'

vi.mock('./pages/PaginaReservas.tsx', () => ({
  default: () => <p>Tela de reservas</p>,
}))

function abrir(caminho: string, sessao = valorDaSessao()) {
  renderizarComProvedores(
    <>
      <RotasDaAplicacao />
      <LocalAtual />
    </>,
    { caminho, sessao },
  )
}

function local() {
  return screen.getByTestId('local').textContent
}

describe('RotasDaAplicacao — raiz e rotas desconhecidas', () => {
  it.each(['/', '/nao-existe', '/reservas/nao/existe'])(
    'sem sessão, %s leva ao login',
    async (caminho) => {
      abrir(caminho)

      expect(await screen.findByRole('heading', { name: 'Entrar' })).toBeTruthy()
      expect(local()).toBe(`/entrar?proximo=${encodeURIComponent(caminho)}`)
    },
  )

  it.each([
    ['Gestor', USUARIO_GESTOR, '/'],
    ['Gestor', USUARIO_GESTOR, '/nao-existe'],
    ['Solicitante', USUARIO_SOLICITANTE, '/'],
    ['Solicitante', USUARIO_SOLICITANTE, '/nao-existe'],
  ])('com sessão de %s, %s leva à tela de reservas', async (_, usuario, caminho) => {
    abrir(caminho, valorDaSessao({ usuario }))

    expect(await screen.findByText('Tela de reservas')).toBeTruthy()
    expect(local()).toBe('/reservas')
  })

  it('enquanto verifica a sessão, mostra o carregando e não pisca o login', () => {
    abrir('/', valorDaSessao({ usuario: USUARIO_GESTOR, verificando: true }))

    expect(screen.getByText('Verificando sua sessão...')).toBeTruthy()
    expect(screen.queryByRole('heading', { name: 'Entrar' })).toBeNull()
    expect(local()).toBe('/')
  })

  it('quem já tem sessão e abre /entrar vai para as reservas, sem laço', async () => {
    abrir('/entrar', valorDaSessao({ usuario: USUARIO_SOLICITANTE }))

    expect(await screen.findByText('Tela de reservas')).toBeTruthy()
    expect(local()).toBe('/reservas')
  })

  it('o login e as demais telas continuam sem item "Início" no menu', async () => {
    abrir('/', valorDaSessao({ usuario: USUARIO_GESTOR }))

    await screen.findByText('Tela de reservas')
    expect(screen.queryByRole('link', { name: 'Início' })).toBeNull()
  })
})
