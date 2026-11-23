import { useLocation } from 'react-router'
import { LinkBotao } from '../botao/Botao.tsx'
import { caminhoDeVolta, ESTADO_DE_VOLTA } from '../../navegacao.ts'

function BotaoVoltar() {
  const { state } = useLocation()
  return (
    <p>
      <LinkBotao
        acao="voltar"
        to={caminhoDeVolta(state)}
        state={ESTADO_DE_VOLTA}
        aria-label="Voltar para a lista de reservas"
      >
        Voltar
      </LinkBotao>
    </p>
  )
}

export default BotaoVoltar
