import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import CampoFiltro from './CampoFiltro.tsx'

describe('CampoFiltro', () => {
  it('liga o rótulo ao campo de texto, ao select e à data', () => {
    render(
      <>
        <CampoFiltro rotulo="Busca">
          {(controle) => <input {...controle} type="text" />}
        </CampoFiltro>
        <CampoFiltro rotulo="Perfil">
          {(controle) => <select {...controle} />}
        </CampoFiltro>
        <CampoFiltro rotulo="Data">
          {(controle) => <input {...controle} type="date" />}
        </CampoFiltro>
      </>,
    )

    expect(screen.getByLabelText('Busca').tagName).toBe('INPUT')
    expect(screen.getByLabelText('Perfil').tagName).toBe('SELECT')
    expect((screen.getByLabelText('Data') as HTMLInputElement).type).toBe('date')
  })

  it('o rótulo é um label de verdade, com o texto completo e o title para o corte visual', () => {
    render(
      <CampoFiltro rotulo="Somente minhas reservas muito longas">
        {(controle) => <input {...controle} />}
      </CampoFiltro>,
    )

    const rotulo = screen.getByText('Somente minhas reservas muito longas')
    expect(rotulo.tagName).toBe('LABEL')
    expect(rotulo.getAttribute('title')).toBe('Somente minhas reservas muito longas')
  })

  it('a dica vira placeholder e descrição acessível', () => {
    render(
      <CampoFiltro rotulo="Solicitante" dica="Nome ou matrícula">
        {(controle) => <input {...controle} />}
      </CampoFiltro>,
    )

    const campo = screen.getByLabelText('Solicitante')
    expect(campo.getAttribute('placeholder')).toBe('Nome ou matrícula')
    expect(campo.getAttribute('aria-describedby')).toBe(screen.getByText('Nome ou matrícula', { selector: 'p' }).id)
  })

  it('reflete o valor e o estado desabilitado do controle', () => {
    render(
      <CampoFiltro rotulo="Tipo">
        {(controle) => (
          <select {...controle} value="A" disabled onChange={() => {}}>
            <option value="">Todos</option>
            <option value="A">A</option>
          </select>
        )}
      </CampoFiltro>,
    )

    const select = screen.getByLabelText('Tipo') as HTMLSelectElement
    expect(select.value).toBe('A')
    expect(select.disabled).toBe(true)
  })
})
