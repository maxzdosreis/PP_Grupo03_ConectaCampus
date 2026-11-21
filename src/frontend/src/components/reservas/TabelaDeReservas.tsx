import { useId, type Ref } from 'react'
import { useLocation } from 'react-router'
import type { AcaoDisponivel, Reserva } from '../../api/reservas.ts'
import { formatarIntervalo } from '../../formatacao.ts'
import { caminhoDaReserva, type OrigemDaReserva } from '../../navegacao.ts'
import { LinkDeIcone } from '../botao/Botao.tsx'
import AcoesDaReserva from './AcoesDaReserva.tsx'
import EtiquetaDeSituacao from './EtiquetaDeSituacao.tsx'
import { nomeDoEspaco, type NomesDosEspacos } from './nomeDoEspaco.ts'
import estilos from './TabelaDeReservas.module.css'

type PropriedadesDaTabela = {
  reservas: Reserva[]
  legenda: string
  nomesDosEspacos: NomesDosEspacos
  aoEscolherAcao: (reserva: Reserva, acao: AcaoDisponivel) => void
  ref?: Ref<HTMLDivElement>
}

function TabelaDeReservas({
  reservas,
  legenda,
  nomesDosEspacos,
  aoEscolherAcao,
  ref,
}: PropriedadesDaTabela) {
  const idDaLegenda = useId()
  const { pathname, search } = useLocation()
  const origem: OrigemDaReserva = { voltarPara: `${pathname}${search}` }
  return (
    <div
      ref={ref}
      className={estilos.rolagem}
      role="region"
      aria-labelledby={idDaLegenda}
      tabIndex={0}
    >
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
            <th scope="col">Ações</th>
          </tr>
        </thead>
        <tbody>
          {reservas.map((reserva) => {
            const intervalo = formatarIntervalo(reserva.data, reserva.hora_inicio, reserva.hora_fim)
            const espaco = nomeDoEspaco(nomesDosEspacos, reserva.espaco_id)
            const descricao = `${intervalo} em ${espaco}`
            return (
              <tr key={reserva.id}>
                <th scope="row">
                  {intervalo}
                </th>
                <td>{espaco}</td>
                <td>
                  {reserva.solicitante.nome}
                  <span className={estilos.secundario}>{reserva.solicitante.matricula}</span>
                </td>
                <td className={estilos.texto}>{reserva.finalidade}</td>
                <td className={estilos.texto}>
                  <EtiquetaDeSituacao
                    situacao={reserva.situacao}
                    rotulo={reserva.situacao_rotulo}
                  />
                  {reserva.motivo_da_situacao && (
                    <span className={estilos.secundario}>
                      Motivo: {reserva.motivo_da_situacao}
                    </span>
                  )}
                </td>
                <td>
                  <div className={estilos.acoes}>
                    <LinkDeIcone
                      acao="detalhes"
                      to={caminhoDaReserva(reserva.id)}
                      state={origem}
                      rotulo={`${descricao} — ver detalhes`}
                    />
                    <AcoesDaReserva
                      reserva={reserva}
                      descricao={descricao}
                      aoEscolherAcao={aoEscolherAcao}
                    />
                  </div>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

export default TabelaDeReservas
