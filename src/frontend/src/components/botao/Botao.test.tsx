import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router'
import { describe, expect, it, vi } from 'vitest'
import { violacoesDeAcessibilidade } from '../../testes/acessibilidade.ts'
import type { VarianteDeBotao } from './acoes.ts'
import { Botao, BotaoDeIcone, LinkBotao, LinkDeIcone } from './Botao.tsx'

const VARIANTES: VarianteDeBotao[] = ['primario', 'neutro', 'editar', 'perigo', 'confirmar']

describe('Botao', () => {
  it.each(VARIANTES)('renderiza a variante %s com ícone e texto', (variante) => {
    render(
      <Botao acao="generica" variante={variante}>
        Fazer algo
      </Botao>,
    )

    const botao = screen.getByRole('button', { name: 'Fazer algo' })
    expect(botao.getAttribute('type')).toBe('button')
    expect(botao.querySelector('svg')).not.toBeNull()
  })

  it('o ícone é decorativo: aria-hidden e fora da ordem de foco', () => {
    render(<Botao acao="entrar">Entrar</Botao>)

    const icone = screen.getByRole('button').querySelector('svg')!
    expect(icone.getAttribute('aria-hidden')).toBe('true')
    expect(icone.getAttribute('focusable')).toBe('false')
  })

  it('usa a variante da ação, e a variante pedida a substitui', () => {
    const { rerender } = render(<Botao acao="desativar">Desativar</Botao>)
    const padrao = screen.getByRole('button').className
    rerender(
      <Botao acao="desativar" variante="neutro">
        Desativar
      </Botao>,
    )

    expect(screen.getByRole('button').className).not.toBe(padrao)
  })

  it('disabled desabilita de verdade e não dispara o clique', async () => {
    const aoClicar = vi.fn()
    render(
      <Botao acao="salvar" disabled onClick={aoClicar}>
        Salvar
      </Botao>,
    )

    const botao = screen.getByRole('button', { name: 'Salvar' }) as HTMLButtonElement
    expect(botao.disabled).toBe(true)
    await userEvent.click(botao)
    expect(aoClicar).not.toHaveBeenCalled()
  })

  it('respeita type="submit"', () => {
    render(
      <Botao acao="salvar" type="submit">
        Salvar
      </Botao>,
    )

    expect(screen.getByRole('button').getAttribute('type')).toBe('submit')
  })
})

describe('BotaoDeIcone', () => {
  it.each(VARIANTES)('renderiza a variante %s só com ícone e nome acessível', (variante) => {
    render(<BotaoDeIcone acao="generica" variante={variante} rotulo="Fazer algo no espaço X" />)

    const botao = screen.getByRole('button', { name: 'Fazer algo no espaço X' })
    expect(botao.textContent).toBe('')
    expect(botao.getAttribute('data-dica')).toBe('Fazer algo no espaço X')
    expect(botao.querySelector('svg')?.getAttribute('aria-hidden')).toBe('true')
  })

  it('o clique funciona e disabled desabilita de verdade', async () => {
    const aoClicar = vi.fn()
    const { rerender } = render(<BotaoDeIcone acao="editar" rotulo="Editar" onClick={aoClicar} />)
    await userEvent.click(screen.getByRole('button', { name: 'Editar' }))
    expect(aoClicar).toHaveBeenCalledOnce()

    rerender(<BotaoDeIcone acao="editar" rotulo="Editar" onClick={aoClicar} disabled />)
    const botao = screen.getByRole('button', { name: 'Editar' }) as HTMLButtonElement
    expect(botao.disabled).toBe(true)
    await userEvent.click(botao)
    expect(aoClicar).toHaveBeenCalledOnce()
  })

  it('não tem violações de acessibilidade', async () => {
    const { container } = render(
      <div>
        <BotaoDeIcone acao="editar" rotulo="Editar o espaço Ginásio A" />
        <BotaoDeIcone acao="desativar" rotulo="Desativar o espaço Ginásio A" disabled />
      </div>,
    )

    expect(await violacoesDeAcessibilidade(container)).toEqual([])
  })
})

describe('LinkDeIcone e LinkBotao', () => {
  it('o link só de ícone tem nome acessível e destino', () => {
    render(
      <MemoryRouter>
        <LinkDeIcone acao="detalhes" to="/reservas/1" rotulo="Ver detalhes da reserva 1" />
      </MemoryRouter>,
    )

    const link = screen.getByRole('link', { name: 'Ver detalhes da reserva 1' })
    expect(link.getAttribute('href')).toBe('/reservas/1')
    expect(link.textContent).toBe('')
    expect(link.querySelector('svg')?.getAttribute('aria-hidden')).toBe('true')
  })

  it('o link com texto mantém o texto como nome e esconde o ícone', () => {
    render(
      <MemoryRouter>
        <LinkBotao acao="conta" to="/conta">
          Minha conta
        </LinkBotao>
      </MemoryRouter>,
    )

    const link = screen.getByRole('link', { name: 'Minha conta' })
    expect(link.querySelector('svg')?.getAttribute('aria-hidden')).toBe('true')
  })
})
