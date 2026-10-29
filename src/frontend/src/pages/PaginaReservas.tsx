import { useEffect, useEffectEvent, useMemo, useRef, useState, type Ref } from 'react'
import { Link, useSearchParams } from 'react-router'
import { listarEspacos } from '../api/espacos.ts'
import {
  listarReservas,
  listarSituacoesDeReserva,
  type AcaoDisponivel,
  type Reserva,
} from '../api/reservas.ts'
import Carregando from '../components/estados/Carregando.tsx'
import EstadoVazio from '../components/estados/EstadoVazio.tsx'
import FalhaAoCarregar from '../components/estados/FalhaAoCarregar.tsx'
import Aviso from '../components/mensagens/Aviso.tsx'
import DialogoDeSituacao from '../components/reservas/DialogoDeSituacao.tsx'
import FiltrosDeReservas, {
  type ValoresDosFiltros,
} from '../components/reservas/FiltrosDeReservas.tsx'
import {
  mapaDeNomesDosEspacos,
  nomeDoEspaco,
  type NomesDosEspacos,
} from '../components/reservas/nomeDoEspaco.ts'
import TabelaDeReservas from '../components/reservas/TabelaDeReservas.tsx'
import { useConsulta, type EstadoDaConsulta } from '../hooks/useConsulta.ts'
import { useFocoAoRecarregar } from '../hooks/useFocoAoRecarregar.ts'
import { useSessao } from '../hooks/useSessao.ts'
import { useTituloDaPagina } from '../hooks/useTituloDaPagina.ts'
import { useValorAtrasado } from '../hooks/useValorAtrasado.ts'
import { CAMINHO_DA_NOVA_RESERVA, rotuloDasReservas } from '../navegacao.ts'

export const ATRASO_DO_SOLICITANTE_MS = 400

const SEM_ESPACOS: NomesDosEspacos = new Map()

type AlteracaoEmAndamento = {
  reserva: Reserva
  acao: AcaoDisponivel
}

function lerFiltros(parametros: URLSearchParams, ehGestor: boolean): ValoresDosFiltros {
  return {
    espaco: parametros.get('espaco') ?? '',
    situacao: parametros.get('situacao') ?? '',
    data: parametros.get('data') ?? '',
    solicitante: ehGestor ? (parametros.get('solicitante') ?? '') : '',
    minhas: ehGestor && parametros.get('minhas') === 'true',
  }
}

function textoDoParametro(valor: string | boolean): string {
  if (typeof valor === 'boolean') return valor ? 'true' : ''
  return valor
}

function PaginaReservas() {
  const { ehGestor } = useSessao()
  const tituloDaPagina = rotuloDasReservas(ehGestor)
  useTituloDaPagina(tituloDaPagina)
  const [parametros, setParametros] = useSearchParams()
  const filtros = lerFiltros(parametros, ehGestor)
  const { espaco, situacao, data, solicitante, minhas } = filtros
  const temFiltros = Object.values(filtros).some(Boolean)
  const [textoDoSolicitante, setTextoDoSolicitante] = useState(solicitante)
  const solicitanteAtrasado = useValorAtrasado(textoDoSolicitante, ATRASO_DO_SOLICITANTE_MS)
  const [solicitanteAnterior, setSolicitanteAnterior] = useState(solicitante)

  if (solicitante !== solicitanteAnterior) {
    setSolicitanteAnterior(solicitante)
    if (solicitante !== solicitanteAtrasado.trim()) setTextoDoSolicitante(solicitante)
  }

  const espacos = useConsulta(() => listarEspacos(), [])
  const situacoes = useConsulta(listarSituacoesDeReserva, [])
  const { estado, recarregar } = useConsulta(
    () => listarReservas({ espaco, situacao, data, solicitante, minhas }),
    [espaco, situacao, data, solicitante, minhas],
  )
  const nomesDosEspacos = useMemo(
    () =>
      espacos.estado.tipo === 'sucesso' ? mapaDeNomesDosEspacos(espacos.estado.dados) : SEM_ESPACOS,
    [espacos.estado],
  )
  const [emAlteracao, setEmAlteracao] = useState<AlteracaoEmAndamento | null>(null)
  const titulo = useRef<HTMLHeadingElement>(null)
  const regiaoDaTabela = useRef<HTMLDivElement>(null)
  const listaCarregando = estado.tipo === 'carregando' || espacos.estado.tipo === 'carregando'
  const focarNaListaAoCarregar = useFocoAoRecarregar(
    listaCarregando,
    () => regiaoDaTabela.current ?? titulo.current,
  )

  function atualizarLista() {
    setEmAlteracao(null)
    focarNaListaAoCarregar()
    recarregar()
  }

  function alterarFiltro<Filtro extends keyof ValoresDosFiltros>(
    filtro: Filtro,
    valor: ValoresDosFiltros[Filtro],
  ) {
    const texto = textoDoParametro(valor)
    setParametros(
      (atuais) => {
        const novos = new URLSearchParams(atuais)
        if (texto) novos.set(filtro, texto)
        else novos.delete(filtro)
        return novos
      },
      { replace: true },
    )
  }

  const aplicarSolicitante = useEffectEvent((texto: string) => {
    const aplicado = texto.trim()
    if (aplicado !== solicitante) alterarFiltro('solicitante', aplicado)
  })

  useEffect(() => {
    aplicarSolicitante(solicitanteAtrasado)
  }, [solicitanteAtrasado])

  function limparFiltros() {
    setTextoDoSolicitante('')
    setParametros({}, { replace: true })
  }

  return (
    <>
      <h1 ref={titulo} tabIndex={-1}>
        {tituloDaPagina}
      </h1>
      <FiltrosDeReservas
        espacos={espacos.estado.tipo === 'sucesso' ? espacos.estado.dados : null}
        situacoes={situacoes.estado.tipo === 'sucesso' ? situacoes.estado.dados : null}
        filtrarPorSolicitante={ehGestor}
        valores={filtros}
        textoDoSolicitante={textoDoSolicitante}
        temFiltros={temFiltros}
        aoMudar={alterarFiltro}
        aoDigitarSolicitante={setTextoDoSolicitante}
        aoLimpar={limparFiltros}
      />
      {espacos.estado.tipo === 'erro' && (
        <Aviso variante="informacao">
          Não foi possível carregar os espaços. O filtro por espaço está indisponível e as
          reservas mostram o código do espaço.
        </Aviso>
      )}
      {situacoes.estado.tipo === 'erro' && (
        <Aviso variante="informacao">
          Não foi possível carregar as situações. O filtro por situação está indisponível.
        </Aviso>
      )}
      <ResultadoDaLista
        estado={estado}
        carregandoEspacos={espacos.estado.tipo === 'carregando'}
        nomesDosEspacos={nomesDosEspacos}
        temFiltros={temFiltros}
        tituloSemReservas={
          ehGestor ? 'Nenhuma reserva registrada' : 'Você ainda não tem reservas'
        }
        regiaoDaTabela={regiaoDaTabela}
        aoTentarNovamente={recarregar}
        aoLimparFiltros={limparFiltros}
        aoEscolherAcao={(reserva, acao) => setEmAlteracao({ reserva, acao })}
      />
      {emAlteracao && (
        <DialogoDeSituacao
          key={`${emAlteracao.reserva.id}-${emAlteracao.acao.situacao}`}
          reserva={emAlteracao.reserva}
          acao={emAlteracao.acao}
          nomeDoEspaco={nomeDoEspaco(nomesDosEspacos, emAlteracao.reserva.espaco_id)}
          alvoAoFechar={titulo}
          aoFechar={() => setEmAlteracao(null)}
          aoAtualizarLista={atualizarLista}
        />
      )}
    </>
  )
}

type PropriedadesDoResultado = {
  estado: EstadoDaConsulta<Reserva[]>
  carregandoEspacos: boolean
  nomesDosEspacos: NomesDosEspacos
  temFiltros: boolean
  tituloSemReservas: string
  regiaoDaTabela: Ref<HTMLDivElement>
  aoTentarNovamente: () => void
  aoLimparFiltros: () => void
  aoEscolherAcao: (reserva: Reserva, acao: AcaoDisponivel) => void
}

function ResultadoDaLista({
  estado,
  carregandoEspacos,
  nomesDosEspacos,
  temFiltros,
  tituloSemReservas,
  regiaoDaTabela,
  aoTentarNovamente,
  aoLimparFiltros,
  aoEscolherAcao,
}: PropriedadesDoResultado) {
  const botaoLimparFiltros = (
    <button type="button" onClick={aoLimparFiltros}>
      Limpar filtros
    </button>
  )

  if (estado.tipo === 'carregando' || carregandoEspacos) {
    return <Carregando texto="Carregando reservas..." />
  }
  if (estado.tipo === 'erro') {
    return (
      <FalhaAoCarregar mensagem={estado.mensagem} aoTentarNovamente={aoTentarNovamente}>
        {temFiltros && botaoLimparFiltros}
      </FalhaAoCarregar>
    )
  }
  if (estado.dados.length > 0) {
    return (
      <TabelaDeReservas
        ref={regiaoDaTabela}
        reservas={estado.dados}
        legenda={estado.mensagem}
        nomesDosEspacos={nomesDosEspacos}
        aoEscolherAcao={aoEscolherAcao}
      />
    )
  }
  if (temFiltros) {
    return <EstadoVazio titulo="Nenhuma reserva encontrada">{botaoLimparFiltros}</EstadoVazio>
  }
  return (
    <EstadoVazio titulo={tituloSemReservas}>
      <Link to={CAMINHO_DA_NOVA_RESERVA}>Solicitar reserva</Link>
    </EstadoVazio>
  )
}

export default PaginaReservas
