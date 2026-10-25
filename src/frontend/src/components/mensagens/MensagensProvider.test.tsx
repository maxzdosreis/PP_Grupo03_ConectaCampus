import { act, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { ErroDaApi } from '../../api/cliente.ts'
import { useMensagens } from '../../hooks/useMensagens.ts'
import {
  MAXIMO_DE_NOTIFICACOES_VISIVEIS,
  TEMPO_DE_EXIBICAO_DO_SUCESSO_MS,
  type Mensagens,
} from './contextoDeMensagens.ts'
import MensagensProvider from './MensagensProvider.tsx'

function Disparador({ acao }: { acao: (mensagens: Mensagens) => void }) {
  const mensagens = useMensagens()
  return <button onClick={() => acao(mensagens)}>Disparar</button>
}

function renderizarComDisparador(acao: (mensagens: Mensagens) => void) {
  render(
    <MensagensProvider>
      <Disparador acao={acao} />
    </MensagensProvider>,
  )
  return () => fireEvent.click(screen.getByRole('button', { name: 'Disparar' }))
}

describe('MensagensProvider e useMensagens', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('mostra o sucesso e o remove depois do tempo de exibição', () => {
    const disparar = renderizarComDisparador((m) => m.mostrarSucesso('Espaço cadastrado.'))

    disparar()
    expect(screen.getByText('Espaço cadastrado.')).toBeTruthy()

    act(() => vi.advanceTimersByTime(TEMPO_DE_EXIBICAO_DO_SUCESSO_MS))
    expect(screen.queryByText('Espaço cadastrado.')).toBeNull()
  })

  it('mantém o erro visível até a pessoa fechar', () => {
    const disparar = renderizarComDisparador((m) => m.mostrarErro('Não foi possível salvar.'))

    disparar()
    act(() => vi.advanceTimersByTime(TEMPO_DE_EXIBICAO_DO_SUCESSO_MS * 10))
    expect(screen.getByText('Não foi possível salvar.')).toBeTruthy()

    fireEvent.click(screen.getByRole('button', { name: 'Fechar mensagem' }))
    expect(screen.queryByText('Não foi possível salvar.')).toBeNull()
  })

  it('mostra no máximo três mensagens, descartando as mais antigas', () => {
    let contador = 0
    const disparar = renderizarComDisparador((m) => {
      contador += 1
      m.mostrarErro(`Erro ${contador}`)
    })

    for (let vez = 0; vez <= MAXIMO_DE_NOTIFICACOES_VISIVEIS; vez += 1) {
      disparar()
    }

    expect(screen.queryByText('Erro 1')).toBeNull()
    expect(screen.getByText('Erro 2')).toBeTruthy()
    expect(screen.getByText('Erro 4')).toBeTruthy()
    expect(screen.getAllByRole('button', { name: 'Fechar mensagem' })).toHaveLength(
      MAXIMO_DE_NOTIFICACOES_VISIVEIS,
    )
  })

  it('mostra a mensagem da API quando recebe um ErroDaApi', () => {
    const erro = new ErroDaApi(409, 'CONFLITO_DE_HORARIO', 'Este horário já está ocupado.')
    const disparar = renderizarComDisparador((m) => m.mostrarErro(erro))

    disparar()

    expect(screen.getByText('Este horário já está ocupado.')).toBeTruthy()
  })

  it('anuncia sucesso numa região polite e erro numa região assertive', () => {
    const disparar = renderizarComDisparador((m) => {
      m.mostrarSucesso('Salvo.')
      m.mostrarErro('Falhou.')
    })

    disparar()

    expect(screen.getByText('Salvo.').closest('[aria-live]')?.getAttribute('aria-live')).toBe(
      'polite',
    )
    expect(screen.getByText('Falhou.').closest('[aria-live]')?.getAttribute('aria-live')).toBe(
      'assertive',
    )
  })
})
