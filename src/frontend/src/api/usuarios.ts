import { ErroDaApi, MENSAGEM_ERRO_INESPERADO, requisitar } from './cliente.ts'
import { comParametros } from './parametros.ts'
import type { Paginacao, RespostaSucesso } from './tipos.ts'

export type UsuarioGerenciado = {
  id: number
  nome: string
  email: string
  matricula: string
  perfil: string
  perfil_rotulo: string
  eh_gestor: boolean
  ativo: boolean
  cadastrado_em: string
  ultimo_acesso: string | null
}

export type FiltrosDeUsuarios = {
  busca?: string
  perfil?: string
  ativo?: string
  pagina?: string
}

export type ListaDeUsuarios = {
  usuarios: UsuarioGerenciado[]
  paginacao: Paginacao
}

export type AlteracaoDeUsuario = {
  perfil?: 'SOLICITANTE' | 'GESTOR'
  ativo?: boolean
}

export async function listarUsuarios({
  busca,
  perfil,
  ativo,
  pagina,
}: FiltrosDeUsuarios = {}): Promise<RespostaSucesso<ListaDeUsuarios>> {
  const { mensagem, dados, paginacao } = await requisitar<UsuarioGerenciado[]>(
    comParametros('/usuarios/', { busca, perfil, ativo, pagina }),
  )
  if (!paginacao) throw new ErroDaApi(200, 'ERRO_INESPERADO', MENSAGEM_ERRO_INESPERADO)
  return { mensagem, dados: { usuarios: dados, paginacao } }
}

export function alterarUsuario(id: number, alteracao: AlteracaoDeUsuario) {
  return requisitar<UsuarioGerenciado>(`/usuarios/${id}/`, {
    method: 'PATCH',
    body: JSON.stringify(alteracao),
  })
}
