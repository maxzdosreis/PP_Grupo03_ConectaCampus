import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import Campo from './Campo.tsx'

function idsDescritos(controle: HTMLElement) {
  return controle.getAttribute('aria-describedby')?.split(' ') ?? []
}

describe('Campo', () => {
  it('liga o rótulo ao controle', () => {
    render(<Campo rotulo="Nome">{(controle) => <input {...controle} />}</Campo>)

    expect(screen.getByLabelText('Nome').tagName).toBe('INPUT')
  })

  it('sem dica nem erro, não tem aria-describedby nem aria-invalid', () => {
    render(<Campo rotulo="Nome">{(controle) => <input {...controle} />}</Campo>)

    const controle = screen.getByLabelText('Nome')
    expect(controle.getAttribute('aria-describedby')).toBeNull()
    expect(controle.getAttribute('aria-invalid')).toBeNull()
  })

  it('descreve o controle pela dica, sem marcá-lo como inválido', () => {
    render(
      <Campo rotulo="Capacidade" dica="Número máximo de pessoas.">
        {(controle) => <input {...controle} />}
      </Campo>,
    )

    const controle = screen.getByLabelText('Capacidade')
    expect(idsDescritos(controle)).toEqual([screen.getByText('Número máximo de pessoas.').id])
    expect(controle.getAttribute('aria-invalid')).toBeNull()
  })

  it('com erro, descreve o controle pela dica e pelo erro e o marca como inválido', () => {
    render(
      <Campo
        rotulo="Capacidade"
        dica="Número máximo de pessoas."
        erro="A capacidade deve ser um número inteiro maior que zero."
      >
        {(controle) => <select {...controle} />}
      </Campo>,
    )

    const controle = screen.getByLabelText('Capacidade')
    const erro = screen.getByText('A capacidade deve ser um número inteiro maior que zero.')
    expect(idsDescritos(controle)).toEqual([
      screen.getByText('Número máximo de pessoas.').id,
      erro.closest('p')?.id,
    ])
    expect(controle.getAttribute('aria-invalid')).toBe('true')
  })

  it('gera ids diferentes para cada campo', () => {
    render(
      <>
        <Campo rotulo="Nome">{(controle) => <input {...controle} />}</Campo>
        <Campo rotulo="Tipo">{(controle) => <input {...controle} />}</Campo>
      </>,
    )

    expect(screen.getByLabelText('Nome').id).not.toBe(screen.getByLabelText('Tipo').id)
  })
})
