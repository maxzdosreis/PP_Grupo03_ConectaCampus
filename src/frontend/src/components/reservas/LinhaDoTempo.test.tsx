import { render, screen, within } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import type { RegistroDeSituacao } from '../../api/reservas.ts'
import LinhaDoTempo from './LinhaDoTempo.tsx'
import { MOTIVO_DA_TENTATIVA_DESCONHECIDO } from './motivosDasTentativas.ts'

const CRIACAO: RegistroDeSituacao = {
  situacao_anterior: null,
  situacao_anterior_rotulo: null,
  situacao_nova: 'SOLICITADA',
  situacao_nova_rotulo: 'Solicitada',
  motivo: null,
  autor: { nome: 'Bruno Lima' },
  registrado_em: '2026-10-25T09:15:00-03:00',
  resultado: 'ACEITA',
  situacao_pedida: 'SOLICITADA',
  situacao_pedida_rotulo: 'Solicitada',
  codigo_do_erro: null,
}

const CONFIRMACAO: RegistroDeSituacao = {
  ...CRIACAO,
  situacao_anterior: 'SOLICITADA',
  situacao_anterior_rotulo: 'Solicitada',
  situacao_nova: 'CONFIRMADA',
  situacao_nova_rotulo: 'Confirmada',
  autor: { nome: 'Carla Mendes' },
  registrado_em: '2026-10-26T14:05:00-03:00',
  situacao_pedida: 'CONFIRMADA',
  situacao_pedida_rotulo: 'Confirmada',
}

function recusada(codigo: string | null, sobrescritas: Partial<RegistroDeSituacao> = {}) {
  return {
    ...CRIACAO,
    situacao_anterior: 'CONFIRMADA',
    situacao_anterior_rotulo: 'Confirmada',
    situacao_nova: 'CONFIRMADA',
    situacao_nova_rotulo: 'Confirmada',
    autor: { nome: 'Carla Mendes' },
    registrado_em: '2026-10-27T10:00:00-03:00',
    resultado: 'RECUSADA',
    situacao_pedida: 'CONCLUIDA',
    situacao_pedida_rotulo: 'Concluída',
    codigo_do_erro: codigo,
    ...sobrescritas,
  } satisfies RegistroDeSituacao
}

describe('LinhaDoTempo', () => {
  it('mostra a mudança aceita como antes: etiqueta da nova situação e o autor', () => {
    render(<LinhaDoTempo registros={[CRIACAO, CONFIRMACAO]} />)

    const itens = screen.getAllByRole('listitem')
    expect(itens).toHaveLength(2)
    expect(within(itens[1]).getByText('Confirmada')).toBeTruthy()
    expect(itens[1].textContent).toContain('por Carla Mendes')
    expect(screen.queryByText(/Tentativa recusada/)).toBeNull()
  })

  it('mostra a tentativa recusada com texto, ícone e o motivo legível do código', () => {
    render(<LinhaDoTempo registros={[recusada('CONCLUSAO_ANTES_DO_TERMINO')]} />)

    const item = screen.getByRole('listitem')
    expect(item.textContent).toContain(
      'Tentativa recusada: Carla Mendes tentou Concluída. Motivo: só é possível concluir a reserva a partir do término dela.',
    )
    expect(item.querySelector('[aria-hidden="true"]')?.textContent).toBe('⚠')
  })

  it.each([
    ['ACAO_NAO_PERMITIDA', 'o perfil não pode fazer essa mudança.'],
    ['TRANSICAO_DE_SITUACAO_INVALIDA', 'não é permitida na situação em que a reserva estava'],
    ['RECUSA_OU_CANCELAMENTO_APOS_O_INICIO', 'antes do início da reserva'],
    ['MOTIVO_OBRIGATORIO', 'faltou informar o motivo.'],
    ['TEXTO_MUITO_LONGO', 'passou do tamanho máximo'],
    ['SITUACAO_INVALIDA', 'a situação pedida não existe.'],
    ['RESERVA_DESATUALIZADA', 'alterada por outra pessoa'],
  ])('traduz o código %s', (codigo, trecho) => {
    render(<LinhaDoTempo registros={[recusada(codigo)]} />)

    expect(screen.getByRole('listitem').textContent).toContain(trecho)
  })

  it.each([['CODIGO_QUE_NAO_EXISTE'], [null]])(
    'usa uma mensagem genérica para o código %s, sem quebrar',
    (codigo) => {
      render(<LinhaDoTempo registros={[recusada(codigo)]} />)

      expect(screen.getByRole('listitem').textContent).toContain(
        `Motivo: ${MOTIVO_DA_TENTATIVA_DESCONHECIDO}`,
      )
    },
  )

  it('mostra o texto pedido como veio quando ele não é uma situação conhecida', () => {
    render(
      <LinhaDoTempo
        registros={[
          recusada('SITUACAO_INVALIDA', {
            situacao_pedida: 'em análise',
            situacao_pedida_rotulo: null,
          }),
        ]}
      />,
    )

    expect(screen.getByRole('listitem').textContent).toContain('tentou em análise.')
  })

  it('mostra o motivo informado na tentativa, além do motivo do erro', () => {
    render(
      <LinhaDoTempo
        registros={[recusada('TRANSICAO_DE_SITUACAO_INVALIDA', { motivo: 'Chuva forte' })]}
      />,
    )

    expect(screen.getByRole('listitem').textContent).toContain('Motivo: Chuva forte')
  })

  it('mantém a ordem que o backend mandou, sem reordenar', () => {
    const tarde = recusada('MOTIVO_OBRIGATORIO', { registrado_em: '2026-12-01T10:00:00-03:00' })
    const cedo = recusada('ACAO_NAO_PERMITIDA', { registrado_em: '2026-10-01T10:00:00-03:00' })

    render(<LinhaDoTempo registros={[tarde, CRIACAO, cedo]} />)

    const itens = screen.getAllByRole('listitem')
    expect(itens[0].textContent).toContain('faltou informar o motivo')
    expect(itens[1].textContent).toContain('por Bruno Lima')
    expect(itens[2].textContent).toContain('o perfil não pode')
  })

  it('trata registros sem os campos novos como mudanças aceitas', () => {
    const antigo: RegistroDeSituacao = {
      situacao_anterior: null,
      situacao_anterior_rotulo: null,
      situacao_nova: 'SOLICITADA',
      situacao_nova_rotulo: 'Solicitada',
      motivo: null,
      autor: { nome: 'Bruno Lima' },
      registrado_em: '2026-10-25T09:15:00-03:00',
    }

    render(<LinhaDoTempo registros={[antigo]} />)

    expect(screen.getByRole('listitem').textContent).toContain('Solicitada por Bruno Lima')
  })

  it('lista vazia não quebra', () => {
    render(<LinhaDoTempo registros={[]} />)

    expect(screen.queryAllByRole('listitem')).toHaveLength(0)
  })
})
