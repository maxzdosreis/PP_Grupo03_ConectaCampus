import { useEffect, useEffectEvent, useMemo, useState } from 'react'
import { Link, useSearchParams } from 'react-router'
import { listarEspacos } from '../api/espacos.ts'
import { listarReservas, listarSituacoesDeReserva, type Reserva } from '../api/reservas.ts'
import Carregando from '../components/estados/Carregando.tsx'
import EstadoVazio from '../components/estados/EstadoVazio.tsx'
import FalhaAoCarregar from '../components/estados/FalhaAoCarregar.tsx'
import Aviso from '../components/mensagens/Aviso.tsx'
import FiltrosDeReservas, {
  type ValoresDosFiltros,
} from '../components/reservas/FiltrosDeReservas.tsx'
import { mapaDeNomesDosEspacos, type NomesDosEspacos } from '../components/reservas/nomeDoEspaco.ts'
import TabelaDeReservas from '../components/reservas/TabelaDeReservas.tsx'
import { useConsulta, type EstadoDaConsulta } from '../hooks/useConsulta.ts'
import { useTituloDaPagina } from '../hooks/useTituloDaPagina.ts'
import { useValorAtrasado } from '../hooks/useValorAtrasado.ts'
import { CAMINHO_DA_NOVA_RESERVA } from '../navegacao.ts'

export const ATRASO_DO_SOLICITANTE_MS = 400

const SEM_ESPACOS: NomesDosEspacos = new Map()

function lerFiltros(parametros: URLSearchParams): ValoresDosFiltros {
  return {
    espaco: parametros.get('espaco') ?? '',
    situacao: parametros.get('situacao') ?? '',
    data: parametros.get('data') ?? '',
    solicitante: parametros.get('solicitante') ?? '',
    minhas: parametros.get('minhas') === 'true',
  }
}

function textoDoParametro(valor: string | boolean): string {
  if (typeof valor === 'boolean') return valor ? 'true' : ''
  return valor
}

function PaginaReservas() {
  useTituloDaPagina('Reservas')
  const [parametros, setParametros] = useSearchParams()
  const filtros = lerFiltros(parametros)
  const { espaco, situacao, data, solicitante, minhas } = filtros
  const temFiltros = Object.values(filtros).some(Boolean)
  const [textoDoSolicitante, setTextoDoSolicitante] = useState(solicitante)
  const solicitanteAtrasado = useValorAtrasado(textoDoSolicitante, ATRASO_DO_SOLICITANTE_MS)

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
      <h1>Reservas</h1>
      <FiltrosDeReservas
        espacos={espacos.estado.tipo === 'sucesso' ? espacos.estado.dados : null}
        situacoes={situacoes.estado.tipo === 'sucesso' ? situacoes.estado.dados : null}
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
        aoTentarNovamente={recarregar}
        aoLimparFiltros={limparFiltros}
      />
    </>
  )
}

type PropriedadesDoResultado = {
  estado: EstadoDaConsulta<Reserva[]>
  carregandoEspacos: boolean
  nomesDosEspacos: NomesDosEspacos
  temFiltros: boolean
  aoTentarNovamente: () => void
  aoLimparFiltros: () => void
}

function ResultadoDaLista({
  estado,
  carregandoEspacos,
  nomesDosEspacos,
  temFiltros,
  aoTentarNovamente,
  aoLimparFiltros,
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
        reservas={estado.dados}
        legenda={estado.mensagem}
        nomesDosEspacos={nomesDosEspacos}
      />
    )
  }
  if (temFiltros) {
    return <EstadoVazio titulo="Nenhuma reserva encontrada">{botaoLimparFiltros}</EstadoVazio>
  }
  return (
    <EstadoVazio titulo="Nenhuma reserva registrada">
      <Link to={CAMINHO_DA_NOVA_RESERVA}>Solicitar reserva</Link>
    </EstadoVazio>
  )
}

export default PaginaReservas
