import type { AlteracaoDeUsuario, UsuarioGerenciado } from '../../api/usuarios.ts'

export type AcaoDeUsuario = 'promover' | 'rebaixar' | 'desativar' | 'reativar'

export const ROTULOS_DAS_ACOES: Record<AcaoDeUsuario, string> = {
  promover: 'Promover a Gestor',
  rebaixar: 'Rebaixar a Solicitante',
  desativar: 'Desativar',
  reativar: 'Reativar',
}

const ALTERACOES: Record<AcaoDeUsuario, AlteracaoDeUsuario> = {
  promover: { perfil: 'GESTOR' },
  rebaixar: { perfil: 'SOLICITANTE' },
  desativar: { ativo: false },
  reativar: { ativo: true },
}

export function alteracaoDaAcao(acao: AcaoDeUsuario): AlteracaoDeUsuario {
  return ALTERACOES[acao]
}

export function acaoDePerfil(usuario: UsuarioGerenciado): AcaoDeUsuario {
  return usuario.eh_gestor ? 'rebaixar' : 'promover'
}

export function acaoDeSituacao(usuario: UsuarioGerenciado): AcaoDeUsuario {
  return usuario.ativo ? 'desativar' : 'reativar'
}
