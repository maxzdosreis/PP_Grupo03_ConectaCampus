import type { RegistroDeSituacao } from '../../api/reservas.ts'
import { formatarDataHora } from '../../formatacao.ts'
import EtiquetaDeSituacao from './EtiquetaDeSituacao.tsx'
import estilos from './LinhaDoTempo.module.css'
import { motivoDaTentativa } from './motivosDasTentativas.ts'

type PropriedadesDaLinhaDoTempo = {
  registros: RegistroDeSituacao[]
}

function LinhaDoTempo({ registros }: PropriedadesDaLinhaDoTempo) {
  return (
    <ol className={estilos.linha}>
      {registros.map((registro, posicao) => {
        const recusada = registro.resultado === 'RECUSADA'
        return (
          <li
            key={`${registro.registrado_em}-${posicao}`}
            className={recusada ? `${estilos.item} ${estilos.recusada}` : estilos.item}
          >
            <time dateTime={registro.registrado_em} className={estilos.momento}>
              {formatarDataHora(registro.registrado_em)}
            </time>
            {recusada ? <TentativaRecusada registro={registro} /> : <MudancaAceita registro={registro} />}
            {registro.motivo && <p className={estilos.motivo}>Motivo: {registro.motivo}</p>}
          </li>
        )
      })}
    </ol>
  )
}

function MudancaAceita({ registro }: { registro: RegistroDeSituacao }) {
  return (
    <p>
      <EtiquetaDeSituacao
        situacao={registro.situacao_nova}
        rotulo={registro.situacao_nova_rotulo}
      />{' '}
      por {registro.autor.nome}
    </p>
  )
}

function TentativaRecusada({ registro }: { registro: RegistroDeSituacao }) {
  const pedida = registro.situacao_pedida_rotulo ?? registro.situacao_pedida ?? ''
  return (
    <p>
      <span aria-hidden="true" className={estilos.icone}>
        ⚠
      </span>
      <strong>Tentativa recusada:</strong> {registro.autor.nome} tentou {pedida}. Motivo:{' '}
      {motivoDaTentativa(registro.codigo_do_erro)}
    </p>
  )
}

export default LinhaDoTempo
