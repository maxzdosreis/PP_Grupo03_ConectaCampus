import { useId } from 'react'
import type { Reserva } from '../../api/reservas.ts'
import { formatarIntervalo } from '../../formatacao.ts'
import EtiquetaDeSituacao from './EtiquetaDeSituacao.tsx'
import { nomeDoEspaco, type NomesDosEspacos } from './nomeDoEspaco.ts'
import estilos from './TabelaDeReservas.module.css'

type PropriedadesDaTabela = {
  reservas: Reserva[]
  legenda: string
  nomesDosEspacos: NomesDosEspacos
}

function TabelaDeReservas({ reservas, legenda, nomesDosEspacos }: PropriedadesDaTabela) {
  const idDaLegenda = useId()
  return (
    <div className={estilos.rolagem} role="region" aria-labelledby={idDaLegenda} tabIndex={0}>
      <table className={estilos.tabela}>
        <caption id={idDaLegenda} className={estilos.legenda}>
          {legenda}
        </caption>
        <thead>
          <tr>
            <th scope="col">Data e horário</th>
            <th scope="col">Espaço</th>
            <th scope="col">Solicitante</th>
            <th scope="col">Finalidade</th>
            <th scope="col">Situação</th>
          </tr>
        </thead>
        <tbody>
          {reservas.map((reserva) => (
            <tr key={reserva.id}>
              <th scope="row">
                {formatarIntervalo(reserva.data, reserva.hora_inicio, reserva.hora_fim)}
              </th>
              <td>{nomeDoEspaco(nomesDosEspacos, reserva.espaco_id)}</td>
              <td>
                {reserva.solicitante.nome}
                <span className={estilos.secundario}>{reserva.solicitante.matricula}</span>
              </td>
              <td className={estilos.texto}>{reserva.finalidade}</td>
              <td className={estilos.texto}>
                <EtiquetaDeSituacao situacao={reserva.situacao} rotulo={reserva.situacao_rotulo} />
                {reserva.motivo_da_situacao && (
                  <span className={estilos.secundario}>
                    Motivo: {reserva.motivo_da_situacao}
                  </span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default TabelaDeReservas
