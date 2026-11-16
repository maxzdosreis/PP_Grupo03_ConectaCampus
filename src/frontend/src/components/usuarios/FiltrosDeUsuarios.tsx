import type { FiltrosDeUsuarios as FiltrosDaApi } from '../../api/usuarios.ts'
import Campo from '../formulario/Campo.tsx'
import estilos from './FiltrosDeUsuarios.module.css'

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
    <fieldset className={estilos.filtros}>
      <legend className={estilos.legenda}>Filtros</legend>
      <div className={estilos.campos}>
        <Campo rotulo="Busca" dica="Nome, e-mail ou matrícula">
          {(controle) => (
            <input
              {...controle}
              type="text"
              value={textoDaBusca}
              onChange={(evento) => aoDigitarBusca(evento.target.value)}
            />
          )}
        </Campo>
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
      </div>
      {temFiltros && (
        <div className={estilos.rodape}>
          <button type="button" onClick={aoLimpar}>
            Limpar filtros
          </button>
        </div>
      )}
    </fieldset>
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
    <Campo rotulo={rotulo}>
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
    </Campo>
  )
}

export default FiltrosDeUsuarios
