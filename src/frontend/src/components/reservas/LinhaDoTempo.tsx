import type { RegistroDeSituacao } from '../../api/reservas.ts'
import { formatarDataHora } from '../../formatacao.ts'
import EtiquetaDeSituacao from './EtiquetaDeSituacao.tsx'
import estilos from './LinhaDoTempo.module.css'

type PropriedadesDaLinhaDoTempo = {
  registros: RegistroDeSituacao[]
}

function LinhaDoTempo({ registros }: PropriedadesDaLinhaDoTempo) {
  return (
    <ol className={estilos.linha}>
      {registros.map((registro) => (
        <li
          key={`${registro.registrado_em}-${registro.situacao_nova}`}
          className={estilos.item}
        >
          <time dateTime={registro.registrado_em} className={estilos.momento}>
            {formatarDataHora(registro.registrado_em)}
          </time>
          <p>
            <EtiquetaDeSituacao
              situacao={registro.situacao_nova}
              rotulo={registro.situacao_nova_rotulo}
            />{' '}
            por {registro.autor.nome}
          </p>
          {registro.motivo && <p className={estilos.motivo}>Motivo: {registro.motivo}</p>}
        </li>
      ))}
    </ol>
  )
}

export default LinhaDoTempo
