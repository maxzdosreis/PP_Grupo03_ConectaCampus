import { screen } from '@testing-library/react'
import { Route, Routes } from 'react-router'
import { describe, expect, it } from 'vitest'
import LocalAtual from '../../testes/LocalAtual.tsx'
import { renderizarComProvedores, valorDaSessao } from '../../testes/renderizar.tsx'
import { USUARIO_SOLICITANTE } from '../../testes/usuarios.ts'
import RotaProtegida from './RotaProtegida.tsx'

function renderizar(sessao = valorDaSessao()) {
  renderizarComProvedores(
    <Routes>
      <Route element={<RotaProtegida />}>
        <Route path="/reservas" element={<p>Página protegida</p>} />
      </Route>
      <Route path="/entrar" element={<LocalAtual />} />
    </Routes>,
    { caminho: '/reservas?situacao=SOLICITADA', sessao },
  )
}

describe('RotaProtegida', () => {
  it('sem sessão, leva para /entrar com o caminho atual em ?proximo', () => {
    renderizar()

    expect(screen.getByTestId('local').textContent).toBe(
      '/entrar?proximo=%2Freservas%3Fsituacao%3DSOLICITADA',
    )
    expect(screen.queryByText('Página protegida')).toBeNull()
  })

  it('enquanto verifica a sessão, mostra o carregando e não redireciona', () => {
    renderizar(valorDaSessao({ usuario: USUARIO_SOLICITANTE, verificando: true }))

    expect(screen.getByRole('status').textContent).toContain('Verificando sua sessão...')
    expect(screen.queryByText('Página protegida')).toBeNull()
    expect(screen.queryByTestId('local')).toBeNull()
  })

  it('com sessão, mostra a página', () => {
    renderizar(valorDaSessao({ usuario: USUARIO_SOLICITANTE }))

    expect(screen.getByText('Página protegida')).toBeTruthy()
  })
})
