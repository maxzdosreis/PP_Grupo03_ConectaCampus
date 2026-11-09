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

export type TokensDaSessao = Pick<Sessao, 'access' | 'refresh'>

export function atualizarTokens({ access, refresh }: TokensDaSessao) {
  const atual = lerSessao()
  if (atual) salvarSessao({ ...atual, access, refresh })
}

export function aguardarSessaoDeOutraAba(
  refreshRecusado: string,
  esperaMs: number,
): Promise<Sessao | null> {
  return new Promise((resolver) => {
    const terminar = (sessao: Sessao | null) => {
      clearTimeout(tempo)
      window.removeEventListener('storage', aoMudar)
      resolver(sessao)
    }
    const aoMudar = (evento: StorageEvent) => {
      if (evento.key !== CHAVE_DA_SESSAO) return
      const sessao = interpretar(evento.newValue)
      if (sessao === null || sessao.refresh !== refreshRecusado) terminar(sessao)
    }
    const tempo = setTimeout(() => terminar(null), esperaMs)
    window.addEventListener('storage', aoMudar)
  })
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
