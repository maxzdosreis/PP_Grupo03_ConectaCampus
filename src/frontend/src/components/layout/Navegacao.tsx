import { NavLink } from 'react-router'
import type { ItemDeNavegacao } from '../../navegacao.ts'
import estilos from './Navegacao.module.css'

type PropriedadesDaNavegacao = {
  itens: ItemDeNavegacao[]
}

function Navegacao({ itens }: PropriedadesDaNavegacao) {
  return (
    <nav aria-label="Navegação principal">
      <ul className={estilos.lista}>
        {itens.map(({ rotulo, caminho }) => (
          <li key={caminho}>
            <NavLink
              to={caminho}
              end={caminho === '/'}
              className={({ isActive }) =>
                isActive ? `${estilos.link} ${estilos.ativo}` : estilos.link
              }
            >
              {rotulo}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  )
}

export default Navegacao
