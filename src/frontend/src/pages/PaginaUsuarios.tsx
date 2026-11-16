import { useEffect, useEffectEvent, useRef, useState, type Ref } from 'react'
import { useSearchParams } from 'react-router'
import { listarUsuarios, type ListaDeUsuarios, type UsuarioGerenciado } from '../api/usuarios.ts'
import Carregando from '../components/estados/Carregando.tsx'
import EstadoVazio from '../components/estados/EstadoVazio.tsx'
import FalhaAoCarregar from '../components/estados/FalhaAoCarregar.tsx'
import PaginacaoDeReservas from '../components/reservas/PaginacaoDeReservas.tsx'
import type { AcaoDeUsuario } from '../components/usuarios/acoesDeUsuario.ts'
import DialogoDeUsuario from '../components/usuarios/DialogoDeUsuario.tsx'
import FiltrosDeUsuarios, {
  type ValoresDosFiltrosDeUsuarios,
} from '../components/usuarios/FiltrosDeUsuarios.tsx'
import TabelaDeUsuarios from '../components/usuarios/TabelaDeUsuarios.tsx'
import { useConsulta, type EstadoDaConsulta } from '../hooks/useConsulta.ts'
import { useFocoAoRecarregar } from '../hooks/useFocoAoRecarregar.ts'
import { useSessao } from '../hooks/useSessao.ts'
import { useTituloDaPagina } from '../hooks/useTituloDaPagina.ts'
import { useValorAtrasado } from '../hooks/useValorAtrasado.ts'

export const ATRASO_DA_BUSCA_MS = 400
const PARAMETRO_DA_PAGINA = 'pagina'
const PAGINA_VALIDA = /^[1-9]\d*$/

type AlteracaoEmAndamento = {
  usuario: UsuarioGerenciado
  acao: AcaoDeUsuario
}

function lerFiltros(parametros: URLSearchParams): ValoresDosFiltrosDeUsuarios {
  return {
    busca: parametros.get('busca') ?? '',
    perfil: parametros.get('perfil') ?? '',
    ativo: parametros.get('ativo') ?? '',
  }
}

function lerPagina(parametros: URLSearchParams): number {
  const valor = parametros.get(PARAMETRO_DA_PAGINA) ?? ''
  return PAGINA_VALIDA.test(valor) ? Number(valor) : 1
}

function paginaAlemDoFim(estado: EstadoDaConsulta<ListaDeUsuarios>): number | null {
  if (estado.tipo !== 'sucesso') return null
  const { usuarios, paginacao } = estado.dados
  const ultima = paginacao.total_de_paginas
  return usuarios.length === 0 && ultima > 0 && paginacao.pagina > ultima ? ultima : null
}

function PaginaUsuarios() {
  useTituloDaPagina('Usuários')
  const { usuario: usuarioLogado } = useSessao()
  const [parametros, setParametros] = useSearchParams()
  const filtros = lerFiltros(parametros)
  const { busca, perfil, ativo } = filtros
  const temFiltros = Object.values(filtros).some(Boolean)
  const pagina = lerPagina(parametros)
  const [textoDaBusca, setTextoDaBusca] = useState(busca)
  const buscaAtrasada = useValorAtrasado(textoDaBusca, ATRASO_DA_BUSCA_MS)
  const [buscaAnterior, setBuscaAnterior] = useState(busca)

  if (busca !== buscaAnterior) {
    setBuscaAnterior(busca)
    if (busca !== buscaAtrasada.trim()) setTextoDaBusca(busca)
  }

  const { estado, recarregar } = useConsulta(
    () => listarUsuarios({ busca, perfil, ativo, pagina: String(pagina) }),
    [busca, perfil, ativo, pagina],
  )
  const ultimaPagina = paginaAlemDoFim(estado)
  const [emAlteracao, setEmAlteracao] = useState<AlteracaoEmAndamento | null>(null)
  const titulo = useRef<HTMLHeadingElement>(null)
  const regiaoDaTabela = useRef<HTMLDivElement>(null)
  const listaCarregando = estado.tipo === 'carregando' || ultimaPagina !== null
  const focarNaListaAoCarregar = useFocoAoRecarregar(
    listaCarregando,
    () => regiaoDaTabela.current ?? titulo.current,
  )

  function atualizarLista() {
    setEmAlteracao(null)
    focarNaListaAoCarregar()
    recarregar()
  }

  function alterarFiltro(filtro: keyof ValoresDosFiltrosDeUsuarios, valor: string) {
    setParametros(
      (atuais) => {
        const novos = new URLSearchParams(atuais)
        if (valor) novos.set(filtro, valor)
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

  const aplicarBusca = useEffectEvent((texto: string) => {
    const aplicado = texto.trim()
    if (aplicado !== busca) alterarFiltro('busca', aplicado)
  })

  useEffect(() => {
    aplicarBusca(buscaAtrasada)
  }, [buscaAtrasada])

  function limparFiltros() {
    setTextoDaBusca('')
    setParametros({}, { replace: true })
  }

  return (
    <>
      <h1 ref={titulo} tabIndex={-1}>
        Usuários
      </h1>
      <FiltrosDeUsuarios
        valores={filtros}
        textoDaBusca={textoDaBusca}
        temFiltros={temFiltros}
        aoMudar={alterarFiltro}
        aoDigitarBusca={setTextoDaBusca}
        aoLimpar={limparFiltros}
      />
      <ResultadoDaLista
        estado={estado}
        carregando={listaCarregando}
        temFiltros={temFiltros}
        idDoUsuarioLogado={usuarioLogado?.id ?? null}
        regiaoDaTabela={regiaoDaTabela}
        aoTentarNovamente={recarregar}
        aoLimparFiltros={limparFiltros}
        aoEscolherAcao={(usuario, acao) => setEmAlteracao({ usuario, acao })}
        aoMudarPagina={mudarDePagina}
      />
      {emAlteracao && (
        <DialogoDeUsuario
          key={`${emAlteracao.usuario.id}-${emAlteracao.acao}`}
          usuario={emAlteracao.usuario}
          acao={emAlteracao.acao}
          alvoAoFechar={titulo}
          aoFechar={() => setEmAlteracao(null)}
          aoAtualizarLista={atualizarLista}
        />
      )}
    </>
  )
}

type PropriedadesDoResultado = {
  estado: EstadoDaConsulta<ListaDeUsuarios>
  carregando: boolean
  temFiltros: boolean
  idDoUsuarioLogado: number | null
  regiaoDaTabela: Ref<HTMLDivElement>
  aoTentarNovamente: () => void
  aoLimparFiltros: () => void
  aoEscolherAcao: (usuario: UsuarioGerenciado, acao: AcaoDeUsuario) => void
  aoMudarPagina: (pagina: number) => void
}

function ResultadoDaLista({
  estado,
  carregando,
  temFiltros,
  idDoUsuarioLogado,
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
    return <Carregando texto="Carregando usuários..." />
  }
  if (estado.tipo === 'erro') {
    return (
      <FalhaAoCarregar mensagem={estado.mensagem} aoTentarNovamente={aoTentarNovamente}>
        {temFiltros && botaoLimparFiltros}
      </FalhaAoCarregar>
    )
  }
  const { usuarios, paginacao } = estado.dados
  if (usuarios.length > 0) {
    return (
      <>
        <TabelaDeUsuarios
          ref={regiaoDaTabela}
          usuarios={usuarios}
          legenda={estado.mensagem}
          idDoUsuarioLogado={idDoUsuarioLogado}
          aoEscolherAcao={aoEscolherAcao}
        />
        <PaginacaoDeReservas
          paginacao={paginacao}
          nomeDosItens="usuários"
          aoMudarPagina={aoMudarPagina}
        />
      </>
    )
  }
  if (temFiltros) {
    return <EstadoVazio titulo="Nenhum usuário encontrado">{botaoLimparFiltros}</EstadoVazio>
  }
  return <EstadoVazio titulo="Nenhum usuário cadastrado" />
}

export default PaginaUsuarios
