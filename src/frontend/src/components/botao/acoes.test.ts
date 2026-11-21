import { describe, expect, it } from 'vitest'
import { ROTULOS_DAS_ACOES } from '../usuarios/acoesDeUsuario.ts'
import { ACOES, acaoDaSituacao, type NomeDaAcao } from './acoes.ts'

const VARIANTES_CONHECIDAS = ['primario', 'neutro', 'editar', 'perigo', 'confirmar']

describe('mapa de ações', () => {
  it.each(Object.entries(ACOES))('a ação %s tem ícone e variante definidos', (_, definicao) => {
    expect(definicao.icone).toBeDefined()
    expect(VARIANTES_CONHECIDAS).toContain(definicao.variante)
  })

  it('editar é o lápis sobre amarelo e as ações destrutivas são vermelhas', () => {
    expect(ACOES.editar.variante).toBe('editar')
    for (const acao of ['recusar', 'cancelar', 'desativar', 'rebaixar'] as NomeDaAcao[]) {
      expect(ACOES[acao].variante).toBe('perigo')
    }
    for (const acao of ['confirmar', 'concluir', 'reativar'] as NomeDaAcao[]) {
      expect(ACOES[acao].variante).toBe('confirmar')
    }
  })

  it('ações diferentes do mesmo contexto têm ícones diferentes', () => {
    const grupos: NomeDaAcao[][] = [
      ['confirmar', 'concluir', 'recusar', 'cancelar', 'desativar', 'reativar'],
      ['promover', 'rebaixar', 'editar', 'detalhes'],
    ]
    for (const grupo of grupos) {
      const icones = grupo.map((nome) => ACOES[nome].icone)
      expect(new Set(icones).size).toBe(grupo.length)
    }
  })

  it('toda situação de reserva que a API oferece como ação tem ação própria', () => {
    expect(acaoDaSituacao('CONFIRMADA')).toBe('confirmar')
    expect(acaoDaSituacao('RECUSADA')).toBe('recusar')
    expect(acaoDaSituacao('CANCELADA')).toBe('cancelar')
    expect(acaoDaSituacao('CONCLUIDA')).toBe('concluir')
  })

  it('uma situação desconhecida cai na ação genérica', () => {
    expect(acaoDaSituacao('REABRIR')).toBe('generica')
  })

  it('toda ação de usuário tem ícone no mapa', () => {
    for (const acao of Object.keys(ROTULOS_DAS_ACOES)) {
      expect(ACOES).toHaveProperty(acao)
    }
  })
})
