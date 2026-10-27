import { useId, type Ref } from 'react'
import type { AcaoDisponivel, Reserva } from '../../api/reservas.ts'
import { formatarIntervalo } from '../../formatacao.ts'
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

type PropriedadesDasAcoes = {
  reserva: Reserva
  descricao: string
  aoEscolherAcao: PropriedadesDaTabela['aoEscolherAcao']
}

function AcoesDaReserva({ reserva, descricao, aoEscolherAcao }: PropriedadesDasAcoes) {
  if (reserva.acoes_disponiveis.length === 0) {
    return (
      <>
        <span aria-hidden="true">—</span>
        <span className="somente-leitor-de-tela">Nenhuma ação disponível</span>
      </>
    )
  }
  return (
    <div className={estilos.acoes}>
      {reserva.acoes_disponiveis.map((acao) => (
        <button
          key={acao.situacao}
          type="button"
          className={estilos.acao}
          aria-label={`${acao.rotulo} a reserva de ${descricao}`}
          onClick={() => aoEscolherAcao(reserva, acao)}
        >
          {acao.rotulo}
        </button>
      ))}
    </div>
  )
}

function TabelaDeReservas({
  reservas,
  legenda,
  nomesDosEspacos,
  aoEscolherAcao,
  ref,
}: PropriedadesDaTabela) {
  const idDaLegenda = useId()
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
            return (
              <tr key={reserva.id}>
                <th scope="row">{intervalo}</th>
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
                  <AcoesDaReserva
                    reserva={reserva}
                    descricao={`${intervalo} em ${espaco}`}
                    aoEscolherAcao={aoEscolherAcao}
                  />
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
