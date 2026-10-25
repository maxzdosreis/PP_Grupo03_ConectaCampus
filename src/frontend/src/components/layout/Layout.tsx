import { Link, Outlet } from 'react-router'
import { ITENS_DE_NAVEGACAO } from '../../navegacao.ts'
import estilos from './Layout.module.css'
import Navegacao from './Navegacao.tsx'

function Layout() {
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
          <Navegacao itens={ITENS_DE_NAVEGACAO} />
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
