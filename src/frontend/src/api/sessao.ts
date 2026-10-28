import type { Usuario } from './autenticacao.ts'

export type Sessao = {
  access: string
  refresh: string
  usuario: Usuario
}

export type MotivoDaMudanca = 'atualizacao' | 'saida' | 'expiracao'

type OuvinteDaSessao = (sessao: Sessao | null, motivo: MotivoDaMudanca) => void

export const CHAVE_DA_SESSAO = 'conecta-campus:sessao'

const ouvintes = new Set<OuvinteDaSessao>()

let copiaEmMemoria: Sessao | null = null

function ehSessao(valor: unknown): valor is Sessao {
  if (typeof valor !== 'object' || valor === null) return false
  const { access, refresh, usuario } = valor as Record<string, unknown>
  return (
    typeof access === 'string' &&
    typeof refresh === 'string' &&
    typeof usuario === 'object' &&
    usuario !== null
  )
}

function interpretar(texto: string | null): Sessao | null {
  try {
    const valor: unknown = JSON.parse(texto ?? 'null')
    return ehSessao(valor) ? valor : null
  } catch {
    return null
  }
}

function avisar(sessao: Sessao | null, motivo: MotivoDaMudanca) {
  ouvintes.forEach((ouvinte) => ouvinte(sessao, motivo))
}

export function lerSessao(): Sessao | null {
  let texto: string | null
  try {
    texto = localStorage.getItem(CHAVE_DA_SESSAO)
  } catch {
    return copiaEmMemoria
  }
  return interpretar(texto)
}

export function salvarSessao(sessao: Sessao) {
  copiaEmMemoria = sessao
  try {
    localStorage.setItem(CHAVE_DA_SESSAO, JSON.stringify(sessao))
  } catch {
    // Fica só a cópia em memória.
  }
  avisar(sessao, 'atualizacao')
}

export function atualizarAccess(access: string) {
  const atual = lerSessao()
  if (atual) salvarSessao({ ...atual, access })
}

export function limparSessao({ expirou = false }: { expirou?: boolean } = {}) {
  if (!lerSessao()) return
  copiaEmMemoria = null
  try {
    localStorage.removeItem(CHAVE_DA_SESSAO)
  } catch {
    // Sem armazenamento, basta descartar a cópia em memória.
  }
  avisar(null, expirou ? 'expiracao' : 'saida')
}

export function aoMudarSessao(ouvinte: OuvinteDaSessao): () => void {
  ouvintes.add(ouvinte)
  return () => {
    ouvintes.delete(ouvinte)
  }
}
