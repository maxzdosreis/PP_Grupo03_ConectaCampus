import type { TipoDeEspaco } from '../../api/espacos.ts'
import estilos from './FiltrosDeEspacos.module.css'

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
    <fieldset className={estilos.filtros}>
      <legend className={estilos.legenda}>Filtros</legend>
      <label className={estilos.tipo}>
        Tipo
        <select
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
      </label>
      <label className={estilos.marcavel}>
        <input
          type="checkbox"
          checked={apenasAtivos}
          onChange={(evento) => aoMudarApenasAtivos(evento.target.checked)}
        />
        Somente ativos
      </label>
    </fieldset>
  )
}

export default FiltrosDeEspacos
