import axe from 'axe-core'

const REGRAS_DESLIGADAS_NO_JSDOM = { 'color-contrast': { enabled: false } }

export async function violacoesDeAcessibilidade(alvo: Element = document.body) {
  const resultado = await axe.run(alvo, {
    rules: REGRAS_DESLIGADAS_NO_JSDOM,
    resultTypes: ['violations'],
  })
  return resultado.violations.map(
    (violacao) =>
      `${violacao.id} (${violacao.impact}): ${violacao.help} — ` +
      violacao.nodes.map((no) => no.target.join(' ')).join(' | '),
  )
}
