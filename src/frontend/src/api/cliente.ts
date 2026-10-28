import { atualizarAccess, lerSessao, limparSessao } from './sessao.ts'
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
export const MENSAGEM_SESSAO_EXPIRADA = 'Sua sessão expirou. Faça login novamente.'

const CAMINHO_DA_RENOVACAO = '/auth/refresh/'

export type OpcoesDaRequisicao = RequestInit & {
  autenticar?: boolean
}

type Retorno = {
  resposta: Response
  corpo: unknown
}

export class ErroDaApi extends Error {
  readonly status: number
  readonly codigo: string
  readonly campos: Record<string, string[]>

  constructor(
    status: number,
    codigo: string,
    mensagem: string,
    campos: Record<string, string[]> = {},
  ) {
    super(mensagem)
    this.name = 'ErroDaApi'
    this.status = status
    this.codigo = codigo
    this.campos = campos
  }
}

function montarCabecalhos(temCorpo: boolean, access: string | null): HeadersInit {
  const cabecalhos: Record<string, string> = { Accept: 'application/json' }
  if (temCorpo) {
    cabecalhos['Content-Type'] = 'application/json'
  }
  if (access) {
    cabecalhos.Authorization = `Bearer ${access}`
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

async function enviar(
  caminho: string,
  opcoes: RequestInit,
  access: string | null,
): Promise<Response> {
  if (!URL_BASE) {
    throw new ErroDaApi(0, 'API_NAO_CONFIGURADA', MENSAGEM_API_NAO_CONFIGURADA)
  }
  try {
    return await fetch(`${URL_BASE}${caminho}`, {
      ...opcoes,
      headers: montarCabecalhos(opcoes.body !== undefined, access),
    })
  } catch {
    throw new ErroDaApi(0, 'SEM_CONEXAO', MENSAGEM_SEM_CONEXAO)
  }
}

async function buscar(
  caminho: string,
  opcoes: RequestInit,
  access: string | null,
): Promise<Retorno> {
  const resposta = await enviar(caminho, opcoes, access)
  return { resposta, corpo: await lerCorpoJson(resposta) }
}

function tokenRecusado({ resposta, corpo }: Retorno): boolean {
  return (
    resposta.status === 401 && ehRespostaErro(corpo) && corpo.erro.codigo === 'NAO_AUTENTICADO'
  )
}

function refreshRecusado(erro: unknown): boolean {
  return erro instanceof ErroDaApi && (erro.status === 400 || erro.status === 401)
}

let renovacaoEmAndamento: Promise<string | null> | null = null

async function renovar(): Promise<string | null> {
  const sessao = lerSessao()
  if (!sessao) return null
  try {
    const { dados } = await requisitar<{ access: string }>(CAMINHO_DA_RENOVACAO, {
      method: 'POST',
      body: JSON.stringify({ refresh: sessao.refresh }),
      autenticar: false,
    })
    atualizarAccess(dados.access)
    return dados.access
  } catch (erro) {
    if (refreshRecusado(erro)) return null
    throw erro
  }
}

function tentarRenovar(accessRecusado: string): Promise<string | null> {
  const atual = lerSessao()?.access
  if (atual && atual !== accessRecusado) return Promise.resolve(atual)
  renovacaoEmAndamento ??= renovar().finally(() => {
    renovacaoEmAndamento = null
  })
  return renovacaoEmAndamento
}

function encerrarSessaoExpirada(): never {
  limparSessao({ expirou: true })
  throw new ErroDaApi(401, 'SESSAO_EXPIRADA', MENSAGEM_SESSAO_EXPIRADA)
}

async function repetirUmaVez(
  caminho: string,
  opcoes: RequestInit,
  accessRecusado: string,
): Promise<Retorno> {
  const novoAccess = await tentarRenovar(accessRecusado)
  if (!novoAccess) encerrarSessaoExpirada()
  const repetida = await buscar(caminho, opcoes, novoAccess)
  if (tokenRecusado(repetida)) encerrarSessaoExpirada()
  return repetida
}

async function obterResposta(
  caminho: string,
  opcoes: RequestInit,
  autenticar: boolean,
): Promise<Retorno> {
  const access = autenticar ? (lerSessao()?.access ?? null) : null
  const retorno = await buscar(caminho, opcoes, access)
  if (access === null || !tokenRecusado(retorno)) return retorno
  return repetirUmaVez(caminho, opcoes, access)
}

export async function requisitar<T>(
  caminho: string,
  { autenticar = true, ...opcoes }: OpcoesDaRequisicao = {},
): Promise<RespostaSucesso<T>> {
  const { resposta, corpo } = await obterResposta(caminho, opcoes, autenticar)

  if (resposta.ok && ehRespostaSucesso<T>(corpo)) {
    return corpo
  }
  if (ehRespostaErro(corpo)) {
    const { codigo, mensagem, campos } = corpo.erro
    throw new ErroDaApi(resposta.status, codigo, mensagem, campos)
  }
  throw new ErroDaApi(resposta.status, 'ERRO_INESPERADO', MENSAGEM_ERRO_INESPERADO)
}
