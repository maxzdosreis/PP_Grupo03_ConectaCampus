import { useState } from 'react'
import { Link, useSearchParams } from 'react-router'
import { listarEspacos, type Espaco } from '../api/espacos.ts'
import type { Reserva } from '../api/reservas.ts'
import Carregando from '../components/estados/Carregando.tsx'
import EstadoVazio from '../components/estados/EstadoVazio.tsx'
import FalhaAoCarregar from '../components/estados/FalhaAoCarregar.tsx'
import FormularioDeReserva from '../components/reservas/FormularioDeReserva.tsx'
import ResumoDaReserva from '../components/reservas/ResumoDaReserva.tsx'
import { useConsulta } from '../hooks/useConsulta.ts'
import { useTituloDaPagina } from '../hooks/useTituloDaPagina.ts'
import { PARAMETRO_DO_ESPACO } from '../navegacao.ts'

function PaginaNovaReserva() {
  useTituloDaPagina('Nova reserva')
  const [parametros] = useSearchParams()
  const espacoDaUrl = parametros.get(PARAMETRO_DO_ESPACO) ?? ''
  const { estado, recarregar } = useConsulta(() => listarEspacos({ apenasAtivos: true }), [])

  function conteudo() {
    if (estado.tipo === 'carregando') {
      return <Carregando texto="Carregando espaços..." />
    }
    if (estado.tipo === 'erro') {
      return <FalhaAoCarregar mensagem={estado.mensagem} aoTentarNovamente={recarregar} />
    }
    if (estado.dados.length === 0) {
      return (
        <EstadoVazio
          titulo="Nenhum espaço disponível para reserva"
          descricao="Só espaços ativos podem ser reservados."
        >
          <Link to="/espacos">Ver espaços</Link>
        </EstadoVazio>
      )
    }
    return <Solicitacao key={espacoDaUrl} espacos={estado.dados} espacoDaUrl={espacoDaUrl} />
  }

  return (
    <>
      <h1>Nova reserva</h1>
      {/* AUT-06: mostrar quem está solicitando (nome e matrícula do usuário logado). */}
      {conteudo()}
    </>
  )
}

type PropriedadesDaSolicitacao = {
  espacos: Espaco[]
  espacoDaUrl: string
}

function Solicitacao({ espacos, espacoDaUrl }: PropriedadesDaSolicitacao) {
  const [espacoEscolhido, setEspacoEscolhido] = useState(() =>
    espacos.some(({ id }) => String(id) === espacoDaUrl) ? espacoDaUrl : '',
  )
  const [reservaCriada, setReservaCriada] = useState<Reserva | null>(null)
  const [voltouDoResumo, setVoltouDoResumo] = useState(false)

  function aoSolicitar(reserva: Reserva) {
    setEspacoEscolhido(String(reserva.espaco_id))
    setReservaCriada(reserva)
  }

  function aoSolicitarOutra() {
    setReservaCriada(null)
    setVoltouDoResumo(true)
  }

  if (reservaCriada) {
    const espaco = espacos.find(({ id }) => id === reservaCriada.espaco_id)
    return (
      <ResumoDaReserva
        reserva={reservaCriada}
        nomeDoEspaco={espaco?.nome ?? `Espaço #${reservaCriada.espaco_id}`}
        aoSolicitarOutra={aoSolicitarOutra}
      />
    )
  }
  return (
    <FormularioDeReserva
      espacos={espacos}
      espacoInicial={espacoEscolhido}
      focarAoAbrir={voltouDoResumo}
      aoSolicitar={aoSolicitar}
    />
  )
}

export default PaginaNovaReserva
