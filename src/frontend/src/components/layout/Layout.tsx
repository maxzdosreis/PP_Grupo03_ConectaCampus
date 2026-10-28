import { Link, Outlet } from 'react-router'
import { useSessao } from '../../hooks/useSessao.ts'
import { itensVisiveis } from '../../navegacao.ts'
import AreaDoUsuario from './AreaDoUsuario.tsx'
import estilos from './Layout.module.css'
import Navegacao from './Navegacao.tsx'

function Layout() {
  const { autenticado } = useSessao()

  return (
    <div className={estilos.pagina}>
      <a className={estilos.pularParaConteudo} href="#conteudo">
        Pular para o conteúdo
      </a>
      <header className={estilos.cabecalho}>
        <div className={estilos.faixa}>
          <Link to="/" className={estilos.marca}>
            Conecta Campus
          </Link>
          <Navegacao itens={itensVisiveis(autenticado)} />
          <AreaDoUsuario />
        </div>
      </header>
      <main id="conteudo" tabIndex={-1} className={estilos.conteudo}>
        <Outlet />
      </main>
      <footer className={estilos.rodape}>
        <div className={estilos.faixa}>Conecta Campus · Unilasalle RS · 2026/2</div>
      </footer>
    </div>
  )
}

export default Layout
