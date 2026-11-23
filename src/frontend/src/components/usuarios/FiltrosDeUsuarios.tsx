import type { FiltrosDeUsuarios as FiltrosDaApi } from '../../api/usuarios.ts'
import { BotaoDeIcone } from '../botao/Botao.tsx'
import BarraDeFiltros from '../filtros/BarraDeFiltros.tsx'
import CampoFiltro from '../filtros/CampoFiltro.tsx'

export type ValoresDosFiltrosDeUsuarios = Required<Omit<FiltrosDaApi, 'pagina'>>

const PERFIS = [
  { valor: 'SOLICITANTE', rotulo: 'Solicitante' },
  { valor: 'GESTOR', rotulo: 'Gestor' },
]

const SITUACOES = [
  { valor: 'true', rotulo: 'Ativos' },
  { valor: 'false', rotulo: 'Inativos' },
]

type PropriedadesDosFiltros = {
  valores: ValoresDosFiltrosDeUsuarios
  textoDaBusca: string
  temFiltros: boolean
  aoMudar: (filtro: 'perfil' | 'ativo', valor: string) => void
  aoDigitarBusca: (texto: string) => void
  aoLimpar: () => void
}

function FiltrosDeUsuarios({
  valores,
  textoDaBusca,
  temFiltros,
  aoMudar,
  aoDigitarBusca,
  aoLimpar,
}: PropriedadesDosFiltros) {
  return (
    <BarraDeFiltros
      acoes={
        temFiltros && <BotaoDeIcone acao="limpar" rotulo="Limpar filtros" onClick={aoLimpar} />
      }
    >
      <CampoFiltro rotulo="Busca" dica="Nome, e-mail ou matrícula">
        {(controle) => (
          <input
            {...controle}
            type="text"
            value={textoDaBusca}
            onChange={(evento) => aoDigitarBusca(evento.target.value)}
          />
        )}
      </CampoFiltro>
      <Seletor
        rotulo="Perfil"
        rotuloDeTodos="Todos os perfis"
        opcoes={PERFIS}
        valor={valores.perfil}
        aoMudar={(perfil) => aoMudar('perfil', perfil)}
      />
      <Seletor
        rotulo="Situação"
        rotuloDeTodos="Todas as situações"
        opcoes={SITUACOES}
        valor={valores.ativo}
        aoMudar={(ativo) => aoMudar('ativo', ativo)}
      />
    </BarraDeFiltros>
  )
}

type PropriedadesDoSeletor = {
  rotulo: string
  rotuloDeTodos: string
  opcoes: { valor: string; rotulo: string }[]
  valor: string
  aoMudar: (valor: string) => void
}

function Seletor({ rotulo, rotuloDeTodos, opcoes, valor, aoMudar }: PropriedadesDoSeletor) {
  const valorAusente = valor !== '' && !opcoes.some((opcao) => opcao.valor === valor)
  return (
    <CampoFiltro rotulo={rotulo}>
      {(controle) => (
        <select {...controle} value={valor} onChange={(evento) => aoMudar(evento.target.value)}>
          <option value="">{rotuloDeTodos}</option>
          {valorAusente && <option value={valor}>{valor}</option>}
          {opcoes.map((opcao) => (
            <option key={opcao.valor} value={opcao.valor}>
              {opcao.rotulo}
            </option>
          ))}
        </select>
      )}
    </CampoFiltro>
  )
}

export default FiltrosDeUsuarios
