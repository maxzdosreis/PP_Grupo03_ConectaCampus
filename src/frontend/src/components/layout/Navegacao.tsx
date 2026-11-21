import { NavLink } from 'react-router'
import type { ItemDeNavegacao } from '../../navegacao.ts'
import { Icone } from '../botao/Botao.tsx'
import type { NomeDaAcao } from '../botao/acoes.ts'
import estilos from './Navegacao.module.css'

const ICONES_POR_CAMINHO: Record<string, NomeDaAcao> = {
  '/espacos': 'espacos',
  '/reservas': 'reservas',
  '/reservas/nova': 'reservar',
  '/usuarios': 'usuarios',
}

type PropriedadesDaNavegacao = {
  itens: ItemDeNavegacao[]
}

function Navegacao({ itens }: PropriedadesDaNavegacao) {
  if (itens.length === 0) {
    return null
  }
  return (
    <nav aria-label="Navegação principal">
      <ul className={estilos.lista}>
        {itens.map(({ rotulo, caminho }) => (
          <li key={caminho}>
            <NavLink
              to={caminho}
              end
              className={({ isActive }) =>
                isActive ? `${estilos.link} ${estilos.ativo}` : estilos.link
              }
            >
              <Icone acao={ICONES_POR_CAMINHO[caminho] ?? 'generica'} />
              {rotulo}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  )
}

export default Navegacao
