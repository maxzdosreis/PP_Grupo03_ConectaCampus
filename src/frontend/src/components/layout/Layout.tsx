import { useEffect, useRef } from 'react'
import { Link, Outlet, useLocation } from 'react-router'
import { useSessao } from '../../hooks/useSessao.ts'
import { itensVisiveis } from '../../navegacao.ts'
import AreaDoUsuario from './AreaDoUsuario.tsx'
import estilos from './Layout.module.css'
import Navegacao from './Navegacao.tsx'

function useFocoNoConteudoAoTrocarDeTela() {
  const { pathname } = useLocation()
  const conteudo = useRef<HTMLElement>(null)
  const telaAnterior = useRef(pathname)

  useEffect(() => {
    if (telaAnterior.current === pathname) {
      return
    }
    telaAnterior.current = pathname
    if (document.activeElement === null || document.activeElement === document.body) {
      conteudo.current?.focus({ preventScroll: true })
    }
  }, [pathname])

  return conteudo
}

function Layout() {
  const { autenticado, ehGestor } = useSessao()
  const conteudo = useFocoNoConteudoAoTrocarDeTela()

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
          <Navegacao itens={itensVisiveis(autenticado, ehGestor)} />
          <AreaDoUsuario />
        </div>
      </header>
      <main id="conteudo" ref={conteudo} tabIndex={-1} className={estilos.conteudo}>
        <Outlet />
      </main>
      <footer className={estilos.rodape}>
        <div className={estilos.faixa}>Conecta Campus · Unilasalle RS · 2026/2</div>
      </footer>
    </div>
  )
}

export default Layout
