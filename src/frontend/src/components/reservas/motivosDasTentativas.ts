const MOTIVOS_POR_CODIGO: Record<string, string> = {
  ACAO_NAO_PERMITIDA: 'o perfil não pode fazer essa mudança.',
  TRANSICAO_DE_SITUACAO_INVALIDA: 'a mudança não é permitida na situação em que a reserva estava.',
  CONCLUSAO_ANTES_DO_TERMINO: 'só é possível concluir a reserva a partir do término dela.',
  RECUSA_OU_CANCELAMENTO_APOS_O_INICIO:
    'recusar ou cancelar só é possível antes do início da reserva.',
  MOTIVO_OBRIGATORIO: 'faltou informar o motivo.',
  TEXTO_MUITO_LONGO: 'o motivo informado passou do tamanho máximo.',
  SITUACAO_INVALIDA: 'a situação pedida não existe.',
  RESERVA_DESATUALIZADA: 'a reserva foi alterada por outra pessoa enquanto se decidia.',
}

export const MOTIVO_DA_TENTATIVA_DESCONHECIDO = 'a mudança foi recusada.'

export function motivoDaTentativa(codigo: string | null | undefined): string {
  return (codigo && MOTIVOS_POR_CODIGO[codigo]) || MOTIVO_DA_TENTATIVA_DESCONHECIDO
}
