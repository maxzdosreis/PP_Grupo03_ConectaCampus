import { useSessao } from '../../hooks/useSessao.ts'
import { CAMINHO_DA_CONTA, CAMINHO_DE_ENTRAR, CAMINHO_DO_CADASTRO } from '../../navegacao.ts'
import { Botao, LinkBotao } from '../botao/Botao.tsx'
import estilos from './AreaDoUsuario.module.css'

function AreaDoUsuario() {
  const { usuario, verificando, sair } = useSessao()

  if (verificando) {
    return null
  }
  if (!usuario) {
    return (
      <div className={estilos.area}>
        <LinkBotao acao="entrar" variante="neutro" to={CAMINHO_DE_ENTRAR}>
          Entrar
        </LinkBotao>
        <LinkBotao acao="cadastrar" variante="neutro" to={CAMINHO_DO_CADASTRO}>
          Cadastre-se
        </LinkBotao>
      </div>
    )
  }
  return (
    <div className={estilos.area}>
      <LinkBotao acao="conta" to={CAMINHO_DA_CONTA}>
        Minha conta
      </LinkBotao>
      <Botao acao="sair" onClick={sair}>
        Sair
      </Botao>
    </div>
  )
}

export default AreaDoUsuario
