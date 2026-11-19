import { describe, expect, it } from 'vitest'

const TEXTO = 4.5
const COMPONENTE = 3

type LeituraDeArquivos = { readFileSync(caminho: URL, codificacao: 'utf8'): string }
const MODULO_FS = 'node:fs'
const { readFileSync } = (await import(/* @vite-ignore */ MODULO_FS)) as LeituraDeArquivos

function ler(caminho: string) {
  return readFileSync(new URL(caminho, import.meta.url), 'utf8')
}

const estilosGlobais = ler('./index.css')
const estilosDoLayout = ler('./components/layout/Layout.module.css')
const modulos = Object.fromEntries(
  Object.keys(import.meta.glob('./**/*.module.css')).map((caminho) => [caminho, ler(caminho)]),
)

type Rgb = [number, number, number]

function lerTokens(css: string): Record<string, string> {
  const raiz = css.slice(css.indexOf(':root'), css.indexOf('}', css.indexOf(':root')))
  return Object.fromEntries(
    [...raiz.matchAll(/--(cor-[a-z-]+):\s*(#[0-9a-fA-F]{6})/g)].map(([, nome, cor]) => [nome, cor]),
  )
}

const TOKENS = lerTokens(estilosGlobais)
const FOCO_NO_CABECALHO = /\.cabecalho\s*\{[^}]*--cor-foco:\s*(#[0-9a-fA-F]{6})/.exec(
  estilosDoLayout,
)?.[1]

function cor(nome: string): Rgb {
  const hex = nome.startsWith('#') ? nome : TOKENS[nome]
  if (!hex) {
    throw new Error(`Cor desconhecida: ${nome}`)
  }
  return [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16)) as Rgb
}

function sobre([r, g, b]: Rgb, alfa: number, fundo: Rgb): Rgb {
  return [r, g, b].map((canal, i) => canal * alfa + fundo[i] * (1 - alfa)) as Rgb
}

function luminancia(rgb: Rgb) {
  const [r, g, b] = rgb.map((canal) => {
    const c = canal / 255
    return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4
  })
  return 0.2126 * r + 0.7152 * g + 0.0722 * b
}

function razaoDeContraste(a: Rgb, b: Rgb) {
  const [clara, escura] = [luminancia(a), luminancia(b)].sort((x, y) => y - x)
  return (clara + 0.05) / (escura + 0.05)
}

type Par = { frente: string; fundo: string; onde: string; corDoFundo?: Rgb }

const TINTA_ESCURA: Rgb = [15, 23, 42]
const BRANCO: Rgb = [255, 255, 255]

const PARES_DE_TEXTO: Par[] = [
  { frente: 'cor-texto', fundo: 'cor-fundo', onde: 'corpo da página' },
  { frente: 'cor-texto', fundo: 'cor-superficie', onde: 'cartões, formulários, tabelas, diálogos e campos' },
  { frente: 'cor-texto', fundo: 'cor-sucesso-fundo', onde: 'Aviso de sucesso e toasts' },
  { frente: 'cor-texto', fundo: 'cor-erro-fundo', onde: 'Aviso de erro e toasts' },
  { frente: 'cor-texto', fundo: 'cor-informacao-fundo', onde: 'Aviso informativo' },
  { frente: 'cor-texto-suave', fundo: 'cor-fundo', onde: 'cabeçalho das tabelas, etiqueta neutra, agenda' },
  { frente: 'cor-texto-suave', fundo: 'cor-superficie', onde: 'dicas, legendas, rodapé, carregando, vazio' },
  { frente: 'cor-texto-suave', fundo: 'cor-sucesso-fundo', onde: '"×" do Aviso de sucesso' },
  { frente: 'cor-texto-suave', fundo: 'cor-erro-fundo', onde: '"×" do Aviso de erro' },
  { frente: 'cor-texto-suave', fundo: 'cor-informacao-fundo', onde: '"×" do Aviso informativo' },
  ...['cor-sucesso-fundo', 'cor-erro-fundo', 'cor-informacao-fundo'].map((fundo) => ({
    frente: 'cor-texto',
    fundo,
    onde: `"×" do Aviso em foco ou sob o mouse (tinta de 8% sobre ${fundo})`,
    corDoFundo: sobre(TINTA_ESCURA, 0.08, cor(fundo)),
  })),
  { frente: 'cor-primaria', fundo: 'cor-fundo', onde: 'links na página' },
  { frente: 'cor-primaria', fundo: 'cor-superficie', onde: 'links e botões secundários nos cartões e diálogos' },
  { frente: 'cor-sobre-primaria', fundo: 'cor-primaria', onde: 'botões primários, marcador do Aviso informativo, "Pular para o conteúdo"' },
  { frente: 'cor-sobre-primaria', fundo: 'cor-primaria-escura', onde: 'cabeçalho e botões sob o mouse' },
  {
    frente: 'cor-sobre-primaria',
    fundo: 'cor-primaria-escura',
    onde: '"Sair" sob o mouse (branco de 15% sobre o cabeçalho)',
    corDoFundo: sobre(BRANCO, 0.15, cor('cor-primaria-escura')),
  },
  { frente: 'cor-sucesso', fundo: 'cor-sucesso-fundo', onde: 'etiqueta de sucesso (Confirmada, Ativo, Concluída)' },
  { frente: 'cor-aviso', fundo: 'cor-aviso-fundo', onde: 'etiqueta de aviso (Solicitada)' },
  { frente: 'cor-erro', fundo: 'cor-erro-fundo', onde: 'etiqueta de erro (Recusada, Cancelada, Inativo)' },
  { frente: 'cor-erro', fundo: 'cor-superficie', onde: 'mensagem de erro embaixo do campo' },
  { frente: 'cor-erro', fundo: 'cor-fundo', onde: 'mensagem de erro de campo fora de cartão' },
  { frente: 'cor-sobre-primaria', fundo: 'cor-erro', onde: 'marcador "!" do erro de campo e do Aviso de erro' },
  { frente: 'cor-sobre-primaria', fundo: 'cor-sucesso', onde: 'marcador "✓" do Aviso de sucesso' },
]

const PARES_DE_COMPONENTE: Par[] = [
  { frente: 'cor-borda-forte', fundo: 'cor-superficie', onde: 'borda dos campos (input, select, textarea)' },
  { frente: 'cor-borda-forte', fundo: 'cor-fundo', onde: 'borda dos campos sobre o fundo da página' },
  { frente: 'cor-erro', fundo: 'cor-superficie', onde: 'borda do campo com erro' },
  { frente: 'cor-primaria', fundo: 'cor-superficie', onde: 'botões e caixas de marcar sobre os cartões' },
  { frente: 'cor-primaria', fundo: 'cor-fundo', onde: 'botões sobre o fundo da página' },
  { frente: 'cor-foco', fundo: 'cor-superficie', onde: 'contorno de foco nos cartões e diálogos' },
  { frente: 'cor-foco', fundo: 'cor-fundo', onde: 'contorno de foco sobre o fundo da página' },
  { frente: 'cor-sobre-primaria', fundo: 'cor-primaria-escura', onde: 'borda de "Sair" e traço do item ativo do menu' },
  ...(FOCO_NO_CABECALHO
    ? [
        { frente: FOCO_NO_CABECALHO, fundo: 'cor-primaria-escura', onde: 'contorno de foco no cabeçalho' },
        { frente: FOCO_NO_CABECALHO, fundo: 'cor-primaria', onde: 'contorno de foco de "Pular para o conteúdo"' },
      ]
    : []),
]

const FUNDOS_DECORATIVOS = new Set(['cor-borda'])

function verificar(par: Par, minimo: number) {
  const razao = razaoDeContraste(cor(par.frente), par.corDoFundo ?? cor(par.fundo))
  return { razao, nome: `${par.frente} sobre ${par.fundo} (${par.onde}): ${razao.toFixed(2)}:1 ≥ ${minimo}:1` }
}

function tokensUsadosEm(propriedade: RegExp) {
  const fontes = [estilosGlobais, ...Object.values(modulos)]
  const usados = new Set<string>()
  for (const fonte of fontes) {
    for (const [, nome] of fonte.matchAll(propriedade)) {
      if (nome in TOKENS) {
        usados.add(nome)
      }
    }
  }
  return usados
}

describe('Contraste das cores do tema (RNF-U04)', () => {
  it('lê os tokens de cor do index.css e o foco do cabeçalho', () => {
    expect(Object.keys(TOKENS).length).toBeGreaterThanOrEqual(17)
    expect(FOCO_NO_CABECALHO).toBeDefined()
  })

  describe('texto ≥ 4,5:1', () => {
    it.each(PARES_DE_TEXTO.map((par) => [verificar(par, TEXTO).nome, par]))('%s', (_, par) => {
      expect(verificar(par, TEXTO).razao).toBeGreaterThanOrEqual(TEXTO)
    })
  })

  describe('bordas, foco e indicadores de controles ≥ 3:1', () => {
    it.each(PARES_DE_COMPONENTE.map((par) => [verificar(par, COMPONENTE).nome, par]))(
      '%s',
      (_, par) => {
        expect(verificar(par, COMPONENTE).razao).toBeGreaterThanOrEqual(COMPONENTE)
      },
    )
  })

  it('toda cor usada como texto nos estilos está em algum par verificado', () => {
    const verificadas = new Set(PARES_DE_TEXTO.map((par) => par.frente))
    const usadas = tokensUsadosEm(/(?:^|[\s;{])color:\s*var\(--(cor-[a-z-]+)\)/g)

    expect([...usadas].filter((nome) => !verificadas.has(nome))).toEqual([])
  })

  it('todo fundo usado nos estilos está em algum par verificado ou é decorativo', () => {
    const verificados = new Set([...PARES_DE_TEXTO, ...PARES_DE_COMPONENTE].map((par) => par.fundo))
    const usados = tokensUsadosEm(/background-color:\s*var\(--(cor-[a-z-]+)\)/g)

    expect(
      [...usados].filter((nome) => !verificados.has(nome) && !FUNDOS_DECORATIVOS.has(nome)),
    ).toEqual([])
  })

  it('a fórmula confere com os valores de referência da WCAG', () => {
    expect(razaoDeContraste([0, 0, 0], [255, 255, 255])).toBeCloseTo(21, 5)
    expect(razaoDeContraste([255, 255, 255], [255, 255, 255])).toBeCloseTo(1, 5)
    expect(razaoDeContraste(cor('#767676'), [255, 255, 255])).toBeCloseTo(4.54, 2)
  })
})
