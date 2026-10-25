import { useId } from 'react'
import type { Espaco } from '../../api/espacos.ts'
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
          </tr>
        </thead>
        <tbody>
          {espacos.map((espaco) => (
            <tr key={espaco.id}>
              <th scope="row">{espaco.nome}</th>
              <td>{espaco.tipo_rotulo}</td>
              <td className={estilos.numero}>{espaco.capacidade}</td>
              <td>
                <Situacao ativo={espaco.ativo} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function Situacao({ ativo }: { ativo: boolean }) {
  return (
    <span className={`${estilos.etiqueta} ${ativo ? estilos.ativo : estilos.inativo}`}>
      {ativo ? 'Ativo' : 'Inativo'}
    </span>
  )
}

export default TabelaDeEspacos
