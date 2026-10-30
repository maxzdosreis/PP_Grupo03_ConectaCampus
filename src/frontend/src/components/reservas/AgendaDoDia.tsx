import { useId } from 'react'
import {
  obterOcupacaoDoDia,
  type HorarioLivre,
  type OcupacaoDoDia,
} from '../../api/reservas.ts'
import { useConsulta, type EstadoDaConsulta } from '../../hooks/useConsulta.ts'
import Carregando from '../estados/Carregando.tsx'
import Aviso from '../mensagens/Aviso.tsx'
import { posicaoNaFaixa } from './agendaDoDia.ts'
import estilos from './AgendaDoDia.module.css'
import EtiquetaDeSituacao from './EtiquetaDeSituacao.tsx'

type PropriedadesDaAgenda = {
  espacoId: string
  data: string
  recargas: number
  aoUsarHorario: (livre: HorarioLivre) => void
}

function AgendaDoDia({ espacoId, data, recargas, aoUsarHorario }: PropriedadesDaAgenda) {
  const titulo = useId()
  return (
    <section aria-labelledby={titulo} className={estilos.agenda}>
      <h2 id={titulo} className={estilos.titulo}>
        Agenda do dia
      </h2>
      {espacoId && data ? (
        <AgendaConsultada
          key={recargas}
          espacoId={espacoId}
          data={data}
          aoUsarHorario={aoUsarHorario}
        />
      ) : (
        <p className={estilos.instrucao}>Escolha o espaço e a data para ver os horários ocupados.</p>
      )}
    </section>
  )
}

type PropriedadesDaConsulta = Omit<PropriedadesDaAgenda, 'recargas'>

function AgendaConsultada({ espacoId, data, aoUsarHorario }: PropriedadesDaConsulta) {
  const { estado, recarregar } = useConsulta(
    () => obterOcupacaoDoDia(espacoId, data),
    [espacoId, data],
  )

  function conteudo() {
    if (estado.tipo === 'carregando') {
      return <Carregando texto="Carregando agenda..." />
    }
    if (estado.tipo === 'erro') {
      return (
        <div className={estilos.falha}>
          <Aviso variante="informacao" anunciar={false}>
            Não foi possível carregar a agenda. Você ainda pode solicitar normalmente.
          </Aviso>
          <div>
            <button type="button" className={estilos.botao} onClick={recarregar}>
              Tentar novamente
            </button>
          </div>
        </div>
      )
    }
    const ocupacao = estado.dados
    if (!ocupacao.reservavel) {
      return (
        <Aviso variante="informacao" anunciar={false}>
          {ocupacao.motivo_indisponivel}
        </Aviso>
      )
    }
    return <Ocupacao ocupacao={ocupacao} aoUsarHorario={aoUsarHorario} />
  }

  return (
    <>
      <p aria-live="polite" className="somente-leitor-de-tela">
        {anuncio(estado)}
      </p>
      {conteudo()}
    </>
  )
}

function anuncio(estado: EstadoDaConsulta<OcupacaoDoDia>) {
  if (estado.tipo === 'erro') return 'Não foi possível carregar a agenda.'
  if (estado.tipo === 'carregando') return ''
  return estado.dados.reservavel ? estado.mensagem : estado.dados.motivo_indisponivel
}

function horario({ hora_inicio, hora_fim }: HorarioLivre) {
  return `${hora_inicio}–${hora_fim}`
}

type PropriedadesDaOcupacao = {
  ocupacao: OcupacaoDoDia
  aoUsarHorario: (livre: HorarioLivre) => void
}

function Ocupacao({ ocupacao, aoUsarHorario }: PropriedadesDaOcupacao) {
  const tituloDosOcupados = useId()
  const tituloDosLivres = useId()
  return (
    <>
      <Faixa ocupacao={ocupacao} />
      <div className={estilos.listas}>
        <div>
          <h3 id={tituloDosOcupados} className={estilos.subtitulo}>
            Ocupados
          </h3>
          {ocupacao.ocupados.length === 0 ? (
            <p className={estilos.vazio}>Nenhum horário ocupado.</p>
          ) : (
            <ul aria-labelledby={tituloDosOcupados} className={estilos.lista}>
              {ocupacao.ocupados.map((ocupado) => (
                <li key={horario(ocupado)} className={estilos.item}>
                  <span>{horario(ocupado)}</span>
                  <EtiquetaDeSituacao situacao={ocupado.situacao} rotulo={ocupado.situacao_rotulo} />
                </li>
              ))}
            </ul>
          )}
        </div>
        <div>
          <h3 id={tituloDosLivres} className={estilos.subtitulo}>
            Livres
          </h3>
          {ocupacao.livres.length === 0 ? (
            <p className={estilos.vazio}>Nenhum horário livre neste dia.</p>
          ) : (
            <ul aria-labelledby={tituloDosLivres} className={estilos.lista}>
              {ocupacao.livres.map((livre) => (
                <li key={horario(livre)} className={estilos.item}>
                  <span>{horario(livre)}</span>
                  <button
                    type="button"
                    className={estilos.botao}
                    aria-label={`Usar este horário, ${horario(livre)}`}
                    onClick={() => aoUsarHorario(livre)}
                  >
                    Usar este horário
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </>
  )
}

function Faixa({ ocupacao }: { ocupacao: OcupacaoDoDia }) {
  const { horario_de_abertura: abertura, horario_de_fechamento: fechamento } = ocupacao
  const blocos = [
    ...ocupacao.livres.map((livre) => ({ horario: livre, classe: estilos.livre })),
    ...ocupacao.ocupados.map((ocupado) => ({ horario: ocupado, classe: estilos.ocupado })),
  ]
  return (
    <div className={estilos.faixa} aria-hidden="true">
      <div className={estilos.trilho}>
        {blocos.map(({ horario: intervalo, classe }) => {
          const { inicio, largura } = posicaoNaFaixa(intervalo, abertura, fechamento)
          return (
            <span
              key={`${classe}-${horario(intervalo)}`}
              className={`${estilos.bloco} ${classe}`}
              style={{ left: `${inicio}%`, width: `${largura}%` }}
            />
          )
        })}
      </div>
      <div className={estilos.extremos}>
        <span>{abertura}</span>
        <span>{fechamento}</span>
      </div>
    </div>
  )
}

export default AgendaDoDia
