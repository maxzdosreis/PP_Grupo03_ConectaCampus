import { useEffect, useEffectEvent, useMemo, useRef, useState, type Ref } from 'react'
import { Link, useSearchParams } from 'react-router'
import { listarEspacos } from '../api/espacos.ts'
import {
  listarReservas,
  listarSituacoesDeReserva,
  type AcaoDisponivel,
  type ListaDeReservas,
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
import PaginacaoDeReservas from '../components/reservas/PaginacaoDeReservas.tsx'
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
const PARAMETRO_DA_PAGINA = 'pagina'
const PAGINA_VALIDA = /^[1-9]\d*$/

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

function lerPagina(parametros: URLSearchParams): number {
  const valor = parametros.get(PARAMETRO_DA_PAGINA) ?? ''
  return PAGINA_VALIDA.test(valor) ? Number(valor) : 1
}

function paginaAlemDoFim(estado: EstadoDaConsulta<ListaDeReservas>): number | null {
  if (estado.tipo !== 'sucesso') return null
  const { reservas, paginacao } = estado.dados
  const ultima = paginacao.total_de_paginas
  return reservas.length === 0 && ultima > 0 && paginacao.pagina > ultima ? ultima : null
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
  const pagina = lerPagina(parametros)
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
    () =>
      listarReservas({ espaco, situacao, data, solicitante, minhas, pagina: String(pagina) }),
    [espaco, situacao, data, solicitante, minhas, pagina],
  )
  const ultimaPagina = paginaAlemDoFim(estado)
  const nomesDosEspacos = useMemo(
    () =>
      espacos.estado.tipo === 'sucesso' ? mapaDeNomesDosEspacos(espacos.estado.dados) : SEM_ESPACOS,
    [espacos.estado],
  )
  const [emAlteracao, setEmAlteracao] = useState<AlteracaoEmAndamento | null>(null)
  const titulo = useRef<HTMLHeadingElement>(null)
  const regiaoDaTabela = useRef<HTMLDivElement>(null)
  const listaCarregando =
    estado.tipo === 'carregando' || espacos.estado.tipo === 'carregando' || ultimaPagina !== null
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
        novos.delete(PARAMETRO_DA_PAGINA)
        return novos
      },
      { replace: true },
    )
  }

  function irParaPagina(numero: number, opcoes?: { replace: boolean }) {
    setParametros((atuais) => {
      const novos = new URLSearchParams(atuais)
      if (numero > 1) novos.set(PARAMETRO_DA_PAGINA, String(numero))
      else novos.delete(PARAMETRO_DA_PAGINA)
      return novos
    }, opcoes)
  }

  function mudarDePagina(numero: number) {
    focarNaListaAoCarregar()
    irParaPagina(numero)
  }

  const corrigirPagina = useEffectEvent((ultima: number) =>
    irParaPagina(ultima, { replace: true }),
  )

  useEffect(() => {
    if (ultimaPagina !== null) corrigirPagina(ultimaPagina)
  }, [ultimaPagina])

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
        carregando={listaCarregando}
        nomesDosEspacos={nomesDosEspacos}
        temFiltros={temFiltros}
        tituloSemReservas={
          ehGestor ? 'Nenhuma reserva registrada' : 'Você ainda não tem reservas'
        }
        regiaoDaTabela={regiaoDaTabela}
        aoTentarNovamente={recarregar}
        aoLimparFiltros={limparFiltros}
        aoEscolherAcao={(reserva, acao) => setEmAlteracao({ reserva, acao })}
        aoMudarPagina={mudarDePagina}
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
  estado: EstadoDaConsulta<ListaDeReservas>
  carregando: boolean
  nomesDosEspacos: NomesDosEspacos
  temFiltros: boolean
  tituloSemReservas: string
  regiaoDaTabela: Ref<HTMLDivElement>
  aoTentarNovamente: () => void
  aoLimparFiltros: () => void
  aoEscolherAcao: (reserva: Reserva, acao: AcaoDisponivel) => void
  aoMudarPagina: (pagina: number) => void
}

function ResultadoDaLista({
  estado,
  carregando,
  nomesDosEspacos,
  temFiltros,
  tituloSemReservas,
  regiaoDaTabela,
  aoTentarNovamente,
  aoLimparFiltros,
  aoEscolherAcao,
  aoMudarPagina,
}: PropriedadesDoResultado) {
  const botaoLimparFiltros = (
    <button type="button" onClick={aoLimparFiltros}>
      Limpar filtros
    </button>
  )

  if (estado.tipo === 'carregando' || carregando) {
    return <Carregando texto="Carregando reservas..." />
  }
  if (estado.tipo === 'erro') {
    return (
      <FalhaAoCarregar mensagem={estado.mensagem} aoTentarNovamente={aoTentarNovamente}>
        {temFiltros && botaoLimparFiltros}
      </FalhaAoCarregar>
    )
  }
  const { reservas, paginacao } = estado.dados
  if (reservas.length > 0) {
    return (
      <>
        <TabelaDeReservas
          ref={regiaoDaTabela}
          reservas={reservas}
          legenda={estado.mensagem}
          nomesDosEspacos={nomesDosEspacos}
          aoEscolherAcao={aoEscolherAcao}
        />
        <PaginacaoDeReservas paginacao={paginacao} aoMudarPagina={aoMudarPagina} />
      </>
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
