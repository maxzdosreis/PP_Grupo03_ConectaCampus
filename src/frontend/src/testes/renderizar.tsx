import { render } from '@testing-library/react'
import type { ReactNode } from 'react'
import { MemoryRouter, type MemoryRouterProps } from 'react-router'
import { vi } from 'vitest'
import type { Usuario } from '../api/autenticacao.ts'
import MensagensProvider from '../components/mensagens/MensagensProvider.tsx'
import { ContextoDeSessao, type ValorDaSessao } from '../components/sessao/contextoDeSessao.ts'
import SessaoProvider from '../components/sessao/SessaoProvider.tsx'

type EstadoDaSessaoDeTeste = {
  usuario?: Usuario | null
  verificando?: boolean
}

export function valorDaSessao({
  usuario = null,
  verificando = false,
}: EstadoDaSessaoDeTeste = {}): ValorDaSessao {
  return {
    usuario,
    verificando,
    autenticado: usuario !== null,
    ehGestor: usuario?.eh_gestor ?? false,
    entrar: vi.fn(),
    cadastrarEEntrar: vi.fn(),
    sair: vi.fn(),
  }
}

export type EntradaDaRota = NonNullable<MemoryRouterProps['initialEntries']>[number]

type OpcoesDeRenderizacao = {
  caminho?: EntradaDaRota
  sessao?: ValorDaSessao
}

export function renderizarComProvedores(
  elemento: ReactNode,
  { caminho = '/', sessao = valorDaSessao() }: OpcoesDeRenderizacao = {},
) {
  render(
    <MensagensProvider>
      <MemoryRouter initialEntries={[caminho]}>
        <ContextoDeSessao.Provider value={sessao}>{elemento}</ContextoDeSessao.Provider>
      </MemoryRouter>
    </MensagensProvider>,
  )
  return sessao
}

export function renderizarComSessaoReal(elemento: ReactNode, caminho = '/') {
  render(
    <MensagensProvider>
      <MemoryRouter initialEntries={[caminho]}>
        <SessaoProvider>{elemento}</SessaoProvider>
      </MemoryRouter>
    </MensagensProvider>,
  )
}
