import { screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { useEffect, useRef } from 'react'
import { Link, Route, Routes } from 'react-router'
import { describe, expect, it } from 'vitest'
import { renderizarComProvedores, valorDaSessao } from '../../testes/renderizar.tsx'
import { USUARIO_GESTOR, USUARIO_SOLICITANTE } from '../../testes/usuarios.ts'
import Layout from './Layout.tsx'

function FocaNoTitulo() {
  const titulo = useRef<HTMLHeadingElement>(null)
  useEffect(() => titulo.current?.focus(), [])
  return (
    <h1 ref={titulo} tabIndex={-1}>
      Outra
    </h1>
  )
}

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
    expect(itensDoMenu()).toEqual(['Início', 'Espaços', 'Reservas', 'Nova reserva', 'Usuários'])
    expect(within(cabecalho).queryByRole('link', { name: 'Entrar' })).toBeNull()
    expect(within(cabecalho).getByRole('link', { name: 'Minha conta' }).getAttribute('href')).toBe(
      '/conta',
    )

    await userEvent.click(within(cabecalho).getByRole('button', { name: 'Sair' }))

    expect(sessao.sair).toHaveBeenCalledTimes(1)
  })

  it('logado como solicitante, o item das reservas se chama "Minhas reservas"', () => {
    renderizar(valorDaSessao({ usuario: USUARIO_SOLICITANTE }))

    expect(itensDoMenu()).toEqual(['Início', 'Espaços', 'Minhas reservas', 'Nova reserva'])
    expect(itensDoMenu()).not.toContain('Usuários')
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

  describe('foco ao trocar de tela', () => {
    function renderizarComDuasTelas() {
      renderizarComProvedores(
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<Link to="/outra">Ir para a outra tela</Link>} />
            <Route path="outra" element={<FocaNoTitulo />} />
          </Route>
        </Routes>,
        { sessao: valorDaSessao({ usuario: USUARIO_GESTOR }) },
      )
    }

    it('na primeira carga, o foco não sai do lugar', () => {
      renderizarComDuasTelas()

      expect(document.activeElement).toBe(document.body)
    })

    it('se o elemento com o foco sumiu, o foco vai para o conteúdo', async () => {
      renderizarComProvedores(
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<Link to="/mantem">Ir para a outra tela</Link>} />
            <Route path="mantem" element={<p>Outra tela</p>} />
          </Route>
        </Routes>,
        { sessao: valorDaSessao({ usuario: USUARIO_GESTOR }) },
      )

      await userEvent.click(screen.getByRole('link', { name: 'Ir para a outra tela' }))

      await screen.findByText('Outra tela')
      expect(document.activeElement).toBe(screen.getByRole('main'))
    })

    it('não tira o foco que a própria tela pôs', async () => {
      renderizarComDuasTelas()

      await userEvent.click(screen.getByRole('link', { name: 'Ir para a outra tela' }))

      expect(document.activeElement).toBe(await screen.findByRole('heading', { name: 'Outra' }))
    })
  })

  it('enquanto verifica a sessão, não mostra nem Entrar nem Sair', () => {
    renderizar(valorDaSessao({ usuario: USUARIO_GESTOR, verificando: true }))

    const cabecalho = screen.getByRole('banner')
    expect(within(cabecalho).queryByRole('button', { name: 'Sair' })).toBeNull()
    expect(within(cabecalho).queryByRole('link', { name: 'Entrar' })).toBeNull()
  })
})
