import type { Espaco } from '../../api/espacos.ts'
import type { FiltrosDeReservas as FiltrosDaApi, SituacaoDeReserva } from '../../api/reservas.ts'
import Campo from '../formulario/Campo.tsx'
import estilos from './FiltrosDeReservas.module.css'
import { rotuloDoEspacoDesconhecido } from './nomeDoEspaco.ts'

export type ValoresDosFiltros = Required<FiltrosDaApi>

type FiltroImediato = Exclude<keyof ValoresDosFiltros, 'solicitante'>

type Opcao = {
  valor: string
  rotulo: string
}

type PropriedadesDosFiltros = {
  espacos: Espaco[] | null
  situacoes: SituacaoDeReserva[] | null
  filtrarPorSolicitante: boolean
  valores: ValoresDosFiltros
  textoDoSolicitante: string
  temFiltros: boolean
  aoMudar: <Filtro extends FiltroImediato>(
    filtro: Filtro,
    valor: ValoresDosFiltros[Filtro],
  ) => void
  aoDigitarSolicitante: (texto: string) => void
  aoLimpar: () => void
}

function opcaoDoEspaco({ id, nome, ativo }: Espaco): Opcao {
  return { valor: String(id), rotulo: ativo ? nome : `${nome} (inativo)` }
}

function FiltrosDeReservas({
  espacos,
  situacoes,
  filtrarPorSolicitante,
  valores,
  textoDoSolicitante,
  temFiltros,
  aoMudar,
  aoDigitarSolicitante,
  aoLimpar,
}: PropriedadesDosFiltros) {
  return (
    <fieldset className={estilos.filtros}>
      <legend className={estilos.legenda}>Filtros</legend>
      <div className={estilos.campos}>
        <SeletorDoFiltro
          rotulo="Espaço"
          rotuloDeTodos="Todos os espaços"
          opcoes={espacos?.map(opcaoDoEspaco) ?? null}
          valor={valores.espaco}
          rotuloDoValorAusente={rotuloDoEspacoDesconhecido}
          aoMudar={(espaco) => aoMudar('espaco', espaco)}
        />
        <SeletorDoFiltro
          rotulo="Situação"
          rotuloDeTodos="Todas as situações"
          opcoes={situacoes}
          valor={valores.situacao}
          rotuloDoValorAusente={(situacao) => situacao}
          aoMudar={(situacao) => aoMudar('situacao', situacao)}
        />
        <Campo rotulo="Data">
          {(controle) => (
            <input
              {...controle}
              type="date"
              value={valores.data}
              onChange={(evento) => aoMudar('data', evento.target.value)}
            />
          )}
        </Campo>
        {filtrarPorSolicitante && (
          <Campo rotulo="Solicitante" dica="Nome ou matrícula">
            {(controle) => (
              <input
                {...controle}
                type="text"
                value={textoDoSolicitante}
                onChange={(evento) => aoDigitarSolicitante(evento.target.value)}
              />
            )}
          </Campo>
        )}
      </div>
      <div className={estilos.rodape}>
        {filtrarPorSolicitante && (
          <label className={estilos.marcavel}>
            <input
              type="checkbox"
              checked={valores.minhas}
              onChange={(evento) => aoMudar('minhas', evento.target.checked)}
            />
            Somente minhas reservas
          </label>
        )}
        {temFiltros && (
          <button type="button" onClick={aoLimpar}>
            Limpar filtros
          </button>
        )}
      </div>
    </fieldset>
  )
}

type PropriedadesDoSeletor = {
  rotulo: string
  rotuloDeTodos: string
  opcoes: Opcao[] | null
  valor: string
  rotuloDoValorAusente: (valor: string) => string
  aoMudar: (valor: string) => void
}

function SeletorDoFiltro({
  rotulo,
  rotuloDeTodos,
  opcoes,
  valor,
  rotuloDoValorAusente,
  aoMudar,
}: PropriedadesDoSeletor) {
  const valorAusente = valor !== '' && !opcoes?.some((opcao) => opcao.valor === valor)
  return (
    <Campo rotulo={rotulo}>
      {(controle) => (
        <select
          {...controle}
          value={valor}
          disabled={opcoes === null}
          onChange={(evento) => aoMudar(evento.target.value)}
        >
          <option value="">{rotuloDeTodos}</option>
          {valorAusente && <option value={valor}>{rotuloDoValorAusente(valor)}</option>}
          {opcoes?.map((opcao) => (
            <option key={opcao.valor} value={opcao.valor}>
              {opcao.rotulo}
            </option>
          ))}
        </select>
      )}
    </Campo>
  )
}

export default FiltrosDeReservas
