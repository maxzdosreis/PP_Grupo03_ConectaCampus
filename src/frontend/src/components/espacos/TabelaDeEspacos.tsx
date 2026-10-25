import { useId } from 'react'
import { Link } from 'react-router'
import type { Espaco } from '../../api/espacos.ts'
import { caminhoParaReservar } from '../../navegacao.ts'
import Etiqueta from '../etiqueta/Etiqueta.tsx'
import estilos from './TabelaDeEspacos.module.css'

type PropriedadesDaTabela = {
  espacos: Espaco[]
  legenda: string
}

function TabelaDeEspacos({ espacos, legenda }: PropriedadesDaTabela) {
  const idDaLegenda = useId()
  return (
    <div className={estilos.rolagem} role="region" aria-labelledby={idDaLegenda} tabIndex={0}>
      <table className={estilos.tabela}>
        <caption id={idDaLegenda} className={estilos.legenda}>
          {legenda}
        </caption>
        <thead>
          <tr>
            <th scope="col">Nome</th>
            <th scope="col">Tipo</th>
            <th scope="col" className={estilos.numero}>
              Capacidade
            </th>
            <th scope="col">Situação</th>
            <th scope="col">Ações</th>
          </tr>
        </thead>
        <tbody>
          {espacos.map((espaco) => (
            <tr key={espaco.id}>
              <th scope="row">{espaco.nome}</th>
              <td>{espaco.tipo_rotulo}</td>
              <td className={estilos.numero}>{espaco.capacidade}</td>
              <td>
                <Etiqueta variante={espaco.ativo ? 'sucesso' : 'neutra'}>
                  {espaco.ativo ? 'Ativo' : 'Inativo'}
                </Etiqueta>
              </td>
              <td>
                {espaco.ativo && (
                  <Link to={caminhoParaReservar(espaco.id)} aria-label={`Reservar ${espaco.nome}`}>
                    Reservar
                  </Link>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default TabelaDeEspacos
