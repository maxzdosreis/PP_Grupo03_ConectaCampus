import { useId, useRef, useState, type RefObject } from 'react'
import { Link, useLocation, useParams } from 'react-router'
import { obterEspaco } from '../api/espacos.ts'
import {
  listarHistoricoDaReserva,
  obterReserva,
  type AcaoDisponivel,
  type RegistroDeSituacao,
  type Reserva,
} from '../api/reservas.ts'
import Carregando from '../components/estados/Carregando.tsx'
import EstadoVazio from '../components/estados/EstadoVazio.tsx'
import FalhaAoCarregar from '../components/estados/FalhaAoCarregar.tsx'
import AcoesDaReserva from '../components/reservas/AcoesDaReserva.tsx'
import DetalhesDaReserva from '../components/reservas/DetalhesDaReserva.tsx'
import DialogoDeSituacao from '../components/reservas/DialogoDeSituacao.tsx'
import LinhaDoTempo from '../components/reservas/LinhaDoTempo.tsx'
import { rotuloDoEspacoDesconhecido } from '../components/reservas/nomeDoEspaco.ts'
import { useConsulta, type EstadoDaConsulta } from '../hooks/useConsulta.ts'
import { useFocoAoRecarregar } from '../hooks/useFocoAoRecarregar.ts'
import { useTituloDaPagina } from '../hooks/useTituloDaPagina.ts'
import { formatarData, formatarIntervalo } from '../formatacao.ts'
import { caminhoDeVolta } from '../navegacao.ts'
import estilos from './PaginaReserva.module.css'

const ID_DE_RESERVA = /^[1-9]\d*$/
const STATUS_NAO_ENCONTRADA = 404
const TITULO_PADRAO = 'Reserva'
const TITULO_NAO_ENCONTRADA = 'Reserva não encontrada'

function PaginaReserva() {
  const { reservaId = '' } = useParams()
  if (!ID_DE_RESERVA.test(reservaId)) {
    return <IdentificadorInvalido />
  }
  const id = Number(reservaId)
  return <DetalheDaReserva key={id} id={id} />
}

function IdentificadorInvalido() {
  useTituloDaPagina(TITULO_NAO_ENCONTRADA)
  return <ReservaNaoEncontrada />
}

function LinkDeVolta() {
  const { state } = useLocation()
  return (
    <p>
      <Link to={caminhoDeVolta(state)}>Voltar para as reservas</Link>
    </p>
  )
}

function ReservaNaoEncontrada() {
  return (
    <>
      <LinkDeVolta />
      <h1>{TITULO_PADRAO}</h1>
      <EstadoVazio
        titulo={TITULO_NAO_ENCONTRADA}
        descricao="Ela não existe ou não está disponível para você."
      />
    </>
  )
}

function DetalheDaReserva({ id }: { id: number }) {
  const reserva = useConsulta(() => obterReserva(id), [id])
  const historico = useConsulta(() => listarHistoricoDaReserva(id), [id])
  const titulo = useRef<HTMLHeadingElement>(null)
  const reservaCarregando = reserva.estado.tipo === 'carregando'
  const focarNoTituloAoCarregar = useFocoAoRecarregar(reservaCarregando, () => titulo.current)
  const naoEncontrada =
    reserva.estado.tipo === 'erro' && reserva.estado.status === STATUS_NAO_ENCONTRADA
  const textoDoTitulo =
    reserva.estado.tipo === 'sucesso'
      ? `Reserva de ${formatarData(reserva.estado.dados.data)}`
      : TITULO_PADRAO
  useTituloDaPagina(naoEncontrada ? TITULO_NAO_ENCONTRADA : textoDoTitulo)

  function recarregarTudo() {
    reserva.recarregar()
    historico.recarregar()
  }

  function aoAlterarSituacao() {
    focarNoTituloAoCarregar()
    recarregarTudo()
  }

  if (naoEncontrada) {
    return <ReservaNaoEncontrada />
  }

  return (
    <>
      <LinkDeVolta />
      <h1 ref={titulo} tabIndex={-1}>
        {textoDoTitulo}
      </h1>
      {reserva.estado.tipo === 'carregando' && <Carregando texto="Carregando reserva..." />}
      {reserva.estado.tipo === 'erro' && (
        <FalhaAoCarregar mensagem={reserva.estado.mensagem} aoTentarNovamente={recarregarTudo} />
      )}
      {reserva.estado.tipo === 'sucesso' && (
        <>
          <ReservaCarregada
            reserva={reserva.estado.dados}
            titulo={titulo}
            aoAlterarSituacao={aoAlterarSituacao}
          />
          <Historico estado={historico.estado} aoTentarNovamente={historico.recarregar} />
        </>
      )}
    </>
  )
}

type AlteracaoEmAndamento = {
  reserva: Reserva
  acao: AcaoDisponivel
}

type PropriedadesDaReservaCarregada = {
  reserva: Reserva
  titulo: RefObject<HTMLHeadingElement | null>
  aoAlterarSituacao: () => void
}

function ReservaCarregada({ reserva, titulo, aoAlterarSituacao }: PropriedadesDaReservaCarregada) {
  const espaco = useConsulta(() => obterEspaco(reserva.espaco_id), [reserva.espaco_id])
  const [emAlteracao, setEmAlteracao] = useState<AlteracaoEmAndamento | null>(null)

  if (espaco.estado.tipo === 'carregando') {
    return <Carregando texto="Carregando reserva..." />
  }
  const nomeDoEspaco =
    espaco.estado.tipo === 'sucesso'
      ? espaco.estado.dados.nome
      : rotuloDoEspacoDesconhecido(reserva.espaco_id)
  const intervalo = formatarIntervalo(reserva.data, reserva.hora_inicio, reserva.hora_fim)

  function aoConcluirAlteracao() {
    setEmAlteracao(null)
    aoAlterarSituacao()
  }

  return (
    <>
      <DetalhesDaReserva reserva={reserva} nomeDoEspaco={nomeDoEspaco} />
      <AcoesDaReserva
        reserva={reserva}
        descricao={`${intervalo} em ${nomeDoEspaco}`}
        aoEscolherAcao={(alvo, acao) => setEmAlteracao({ reserva: alvo, acao })}
      />
      {emAlteracao && (
        <DialogoDeSituacao
          key={emAlteracao.acao.situacao}
          reserva={emAlteracao.reserva}
          acao={emAlteracao.acao}
          nomeDoEspaco={nomeDoEspaco}
          alvoAoFechar={titulo}
          aoFechar={() => setEmAlteracao(null)}
          aoAtualizarLista={aoConcluirAlteracao}
          rotuloDaAtualizacao="Atualizar reserva"
        />
      )}
    </>
  )
}

type PropriedadesDoHistorico = {
  estado: EstadoDaConsulta<RegistroDeSituacao[]>
  aoTentarNovamente: () => void
}

function Historico({ estado, aoTentarNovamente }: PropriedadesDoHistorico) {
  const idDoTitulo = useId()

  function conteudo() {
    if (estado.tipo === 'carregando') {
      return <Carregando texto="Carregando histórico..." />
    }
    if (estado.tipo === 'erro') {
      return <FalhaAoCarregar mensagem={estado.mensagem} aoTentarNovamente={aoTentarNovamente} />
    }
    if (estado.dados.length === 0) {
      return <p className={estilos.semHistorico}>Nenhuma mudança registrada.</p>
    }
    return <LinhaDoTempo registros={estado.dados} />
  }

  return (
    <section className={estilos.historico} aria-labelledby={idDoTitulo}>
      <h2 id={idDoTitulo}>Histórico</h2>
      {conteudo()}
    </section>
  )
}

export default PaginaReserva
