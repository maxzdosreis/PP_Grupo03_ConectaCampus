import type { TipoDeEspaco } from '../../api/espacos.ts'
import BarraDeFiltros, { CaixaDeFiltro } from '../filtros/BarraDeFiltros.tsx'
import CampoFiltro from '../filtros/CampoFiltro.tsx'

type PropriedadesDosFiltros = {
  tipos: TipoDeEspaco[] | null
  tipo: string
  apenasAtivos: boolean
  aoMudarTipo: (tipo: string) => void
  aoMudarApenasAtivos: (apenasAtivos: boolean) => void
}

function FiltrosDeEspacos({
  tipos,
  tipo,
  apenasAtivos,
  aoMudarTipo,
  aoMudarApenasAtivos,
}: PropriedadesDosFiltros) {
  return (
    <BarraDeFiltros
      rodape={
        <CaixaDeFiltro rotulo="Somente ativos" marcada={apenasAtivos} aoMudar={aoMudarApenasAtivos} />
      }
    >
      <CampoFiltro rotulo="Tipo">
        {(controle) => (
          <select
            {...controle}
            value={tipo}
            disabled={tipos === null}
            onChange={(evento) => aoMudarTipo(evento.target.value)}
          >
            <option value="">Todos os tipos</option>
            {tipos?.map(({ valor, rotulo }) => (
              <option key={valor} value={valor}>
                {rotulo}
              </option>
            ))}
          </select>
        )}
      </CampoFiltro>
    </BarraDeFiltros>
  )
}

export default FiltrosDeEspacos
