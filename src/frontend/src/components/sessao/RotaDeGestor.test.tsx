import { screen } from '@testing-library/react'
import { Route, Routes } from 'react-router'
import { describe, expect, it } from 'vitest'
import LocalAtual from '../../testes/LocalAtual.tsx'
import { renderizarComProvedores, valorDaSessao } from '../../testes/renderizar.tsx'
import { USUARIO_GESTOR, USUARIO_SOLICITANTE } from '../../testes/usuarios.ts'
import RotaDeGestor from './RotaDeGestor.tsx'

function renderizar(usuario = USUARIO_GESTOR) {
  renderizarComProvedores(
    <Routes>
      <Route element={<RotaDeGestor />}>
        <Route path="/usuarios" element={<p>Tela de usuários</p>} />
      </Route>
      <Route path="/reservas" element={<LocalAtual />} />
    </Routes>,
    { caminho: '/usuarios', sessao: valorDaSessao({ usuario }) },
  )
}

describe('RotaDeGestor', () => {
  it('o gestor vê a tela', () => {
    renderizar(USUARIO_GESTOR)

    expect(screen.getByText('Tela de usuários')).toBeTruthy()
  })

  it('quem não é gestor é levado para as reservas, sem ver a tela', () => {
    renderizar(USUARIO_SOLICITANTE)

    expect(screen.queryByText('Tela de usuários')).toBeNull()
    expect(screen.getByTestId('local').textContent).toBe('/reservas')
  })
})
