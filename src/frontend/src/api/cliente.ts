import type { RespostaErro, RespostaSucesso } from './tipos.ts'

const URL_BASE: string = import.meta.env.VITE_API_URL ?? ''

if (!URL_BASE) {
  console.error(
    'VITE_API_URL não está definida. Copie src/.env.example para src/.env, ' +
      'preencha VITE_API_URL e reinicie o frontend.',
  )
}

const MENSAGEM_SEM_CONEXAO =
  'Não foi possível conectar ao servidor. Verifique se a API está em execução.'
export const MENSAGEM_ERRO_INESPERADO = 'Ocorreu um erro inesperado. Tente novamente.'
const MENSAGEM_API_NAO_CONFIGURADA =
  'O endereço da API não foi configurado. Defina VITE_API_URL no arquivo .env.'

export class ErroDaApi extends Error {
  readonly status: number
  readonly codigo: string

  constructor(status: number, codigo: string, mensagem: string) {
    super(mensagem)
    this.name = 'ErroDaApi'
    this.status = status
    this.codigo = codigo
  }
}

function montarCabecalhos(temCorpo: boolean): HeadersInit {
  const cabecalhos: Record<string, string> = { Accept: 'application/json' }
  if (temCorpo) {
    cabecalhos['Content-Type'] = 'application/json'
  }
  return cabecalhos
}

async function lerCorpoJson(resposta: Response): Promise<unknown> {
  try {
    return await resposta.json()
  } catch {
    return null
  }
}

function ehObjeto(valor: unknown): valor is Record<string, unknown> {
  return typeof valor === 'object' && valor !== null
}

function ehRespostaErro(corpo: unknown): corpo is RespostaErro {
  if (!ehObjeto(corpo) || !ehObjeto(corpo.erro)) {
    return false
  }
  return typeof corpo.erro.codigo === 'string' && typeof corpo.erro.mensagem === 'string'
}

function ehRespostaSucesso<T>(corpo: unknown): corpo is RespostaSucesso<T> {
  return ehObjeto(corpo) && typeof corpo.mensagem === 'string'
}

async function enviar(caminho: string, opcoes: RequestInit): Promise<Response> {
  if (!URL_BASE) {
    throw new ErroDaApi(0, 'API_NAO_CONFIGURADA', MENSAGEM_API_NAO_CONFIGURADA)
  }
  try {
    return await fetch(`${URL_BASE}${caminho}`, {
      ...opcoes,
      headers: montarCabecalhos(opcoes.body !== undefined),
    })
  } catch {
    throw new ErroDaApi(0, 'SEM_CONEXAO', MENSAGEM_SEM_CONEXAO)
  }
}

export async function requisitar<T>(
  caminho: string,
  opcoes: RequestInit = {},
): Promise<RespostaSucesso<T>> {
  const resposta = await enviar(caminho, opcoes)
  const corpo = await lerCorpoJson(resposta)

  if (resposta.ok && ehRespostaSucesso<T>(corpo)) {
    return corpo
  }
  if (ehRespostaErro(corpo)) {
    throw new ErroDaApi(resposta.status, corpo.erro.codigo, corpo.erro.mensagem)
  }
  throw new ErroDaApi(resposta.status, 'ERRO_INESPERADO', MENSAGEM_ERRO_INESPERADO)
}
