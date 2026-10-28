import { screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Route, Routes } from 'react-router'
import { describe, expect, it } from 'vitest'
import { renderizarComProvedores, valorDaSessao } from '../../testes/renderizar.tsx'
import { USUARIO_GESTOR } from '../../testes/usuarios.ts'
import Layout from './Layout.tsx'

function renderizar(sessao = valorDaSessao()) {
  return renderizarComProvedores(
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<p>Conteúdo</p>} />
      </Route>
    </Routes>,
    { sessao },
  )
}

function itensDoMenu() {
  const menu = screen.getByRole('navigation', { name: 'Navegação principal' })
  return within(menu)
    .getAllByRole('link')
    .map((link) => link.textContent)
}

describe('Layout', () => {
  it('logado, mostra nome e perfil, o botão Sair e todos os itens do menu', async () => {
    const sessao = renderizar(valorDaSessao({ usuario: USUARIO_GESTOR }))

    const cabecalho = screen.getByRole('banner')
    expect(cabecalho.textContent).toContain('Carla Mendes · Gestor')
    expect(itensDoMenu()).toEqual(['Início', 'Espaços', 'Reservas', 'Nova reserva'])
    expect(within(cabecalho).queryByRole('link', { name: 'Entrar' })).toBeNull()

    await userEvent.click(within(cabecalho).getByRole('button', { name: 'Sair' }))

    expect(sessao.sair).toHaveBeenCalledTimes(1)
  })

  it('deslogado, mostra Entrar e Cadastre-se e esconde os itens que exigem login', () => {
    renderizar()

    const cabecalho = screen.getByRole('banner')
    expect(within(cabecalho).getByRole('link', { name: 'Entrar' }).getAttribute('href')).toBe(
      '/entrar',
    )
    expect(
      within(cabecalho).getByRole('link', { name: 'Cadastre-se' }).getAttribute('href'),
    ).toBe('/cadastro')
    expect(within(cabecalho).queryByRole('button', { name: 'Sair' })).toBeNull()
    expect(itensDoMenu()).toEqual(['Início'])
  })

  it('enquanto verifica a sessão, não mostra nem Entrar nem Sair', () => {
    renderizar(valorDaSessao({ usuario: USUARIO_GESTOR, verificando: true }))

    const cabecalho = screen.getByRole('banner')
    expect(within(cabecalho).queryByRole('button', { name: 'Sair' })).toBeNull()
    expect(within(cabecalho).queryByRole('link', { name: 'Entrar' })).toBeNull()
  })
})
