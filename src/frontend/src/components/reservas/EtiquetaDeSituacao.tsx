import Etiqueta, { type VarianteDaEtiqueta } from '../etiqueta/Etiqueta.tsx'

const VARIANTE_DA_SITUACAO: Record<string, VarianteDaEtiqueta> = {
  SOLICITADA: 'aviso',
  CONFIRMADA: 'sucesso',
  RECUSADA: 'erro',
  CONCLUIDA: 'neutra',
  CANCELADA: 'neutra',
}

type PropriedadesDaEtiquetaDeSituacao = {
  situacao: string
  rotulo: string
}

function EtiquetaDeSituacao({ situacao, rotulo }: PropriedadesDaEtiquetaDeSituacao) {
  return <Etiqueta variante={VARIANTE_DA_SITUACAO[situacao] ?? 'neutra'}>{rotulo}</Etiqueta>
}

export default EtiquetaDeSituacao
