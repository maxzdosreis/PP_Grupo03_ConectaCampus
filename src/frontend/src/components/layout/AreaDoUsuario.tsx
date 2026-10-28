import { Link } from 'react-router'
import { useSessao } from '../../hooks/useSessao.ts'
import { CAMINHO_DE_ENTRAR, CAMINHO_DO_CADASTRO } from '../../navegacao.ts'
import estilos from './AreaDoUsuario.module.css'

function AreaDoUsuario() {
  const { usuario, verificando, sair } = useSessao()

  if (verificando) {
    return null
  }
  if (!usuario) {
    return (
      <div className={estilos.area}>
        <Link to={CAMINHO_DE_ENTRAR} className={estilos.link}>
          Entrar
        </Link>
        <Link to={CAMINHO_DO_CADASTRO} className={estilos.link}>
          Cadastre-se
        </Link>
      </div>
    )
  }
  return (
    <div className={estilos.area}>
      <p className={estilos.usuario}>
        <span className="somente-leitor-de-tela">Conectado como </span>
        {usuario.nome} · {usuario.perfil_rotulo}
      </p>
      <button type="button" className={estilos.sair} onClick={sair}>
        Sair
      </button>
    </div>
  )
}

export default AreaDoUsuario
