import { useCallback, useRef, useState, type FormEvent, type RefObject } from 'react'
import {
  alterarSituacaoReserva,
  type AcaoDisponivel,
  type AlteracaoDeSituacao,
  type Reserva,
} from '../../api/reservas.ts'
import { formatarIntervalo } from '../../formatacao.ts'
import { useEnvio } from '../../hooks/useEnvio.ts'
import { useFocoNoErro } from '../../hooks/useFocoNoErro.ts'
import { useMensagens } from '../../hooks/useMensagens.ts'
import Dialogo from '../dialogo/Dialogo.tsx'
import ErroDoDialogo from '../dialogo/ErroDoDialogo.tsx'
import Campo from '../formulario/Campo.tsx'
import estilos from './DialogoDeSituacao.module.css'

type PropriedadesDoDialogoDeSituacao = {
  reserva: Reserva
  acao: AcaoDisponivel
  nomeDoEspaco: string
  alvoAoFechar: RefObject<HTMLElement | null>
  aoFechar: () => void
  aoAtualizarLista: () => void
  rotuloDaAtualizacao?: string
}

function DialogoDeSituacao({
  reserva,
  acao,
  nomeDoEspaco,
  alvoAoFechar,
  aoFechar,
  aoAtualizarLista,
  rotuloDaAtualizacao = 'Atualizar lista',
}: PropriedadesDoDialogoDeSituacao) {
  const [motivo, setMotivo] = useState('')
  const alterar = useCallback(
    (dados: AlteracaoDeSituacao) => alterarSituacaoReserva(reserva.id, dados),
    [reserva.id],
  )
  const { enviar, enviando, errosDosCampos, erroGeral, statusDoErro, limparErroDoCampo } =
    useEnvio(alterar)
  const { mostrarSucesso } = useMensagens()
  const { formulario, aviso, focarNoProximoErro } = useFocoNoErro(errosDosCampos, erroGeral)
  const campoDoMotivo = useRef<HTMLTextAreaElement>(null)
  const botaoVoltar = useRef<HTMLButtonElement>(null)
  const textoDaAcao = `${acao.rotulo} reserva`

  function fechar() {
    if (!enviando) aoFechar()
  }

  async function aoEnviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault()
    focarNoProximoErro()
    const resposta = await enviar(
      acao.exige_motivo ? { situacao: acao.situacao, motivo } : { situacao: acao.situacao },
    )
    if (!resposta) return
    mostrarSucesso(resposta.mensagem)
    aoAtualizarLista()
  }

  return (
    <Dialogo
      titulo={textoDaAcao}
      aoFechar={fechar}
      focoInicial={acao.exige_motivo ? campoDoMotivo : botaoVoltar}
      alvoAoFechar={alvoAoFechar}
    >
      <form ref={formulario} className={estilos.formulario} onSubmit={aoEnviar} noValidate>
        <ErroDoDialogo
          ref={aviso}
          mensagem={erroGeral}
          statusDoErro={statusDoErro}
          aoAtualizar={aoAtualizarLista}
          rotuloDaAtualizacao={rotuloDaAtualizacao}
        />
        <dl className={estilos.detalhes}>
          <div>
            <dt>Espaço</dt>
            <dd>{nomeDoEspaco}</dd>
          </div>
          <div>
            <dt>Data e horário</dt>
            <dd>{formatarIntervalo(reserva.data, reserva.hora_inicio, reserva.hora_fim)}</dd>
          </div>
          <div>
            <dt>Solicitante</dt>
            <dd>
              {reserva.solicitante.nome} ({reserva.solicitante.matricula})
            </dd>
          </div>
        </dl>
        {acao.exige_motivo && (
          <Campo
            rotulo="Motivo"
            dica="Explique ao solicitante o motivo."
            erro={errosDosCampos.motivo}
          >
            {(controle) => (
              <textarea
                {...controle}
                ref={campoDoMotivo}
                name="motivo"
                rows={3}
                value={motivo}
                onChange={(evento) => {
                  setMotivo(evento.target.value)
                  limparErroDoCampo('motivo')
                }}
              />
            )}
          </Campo>
        )}
        <div className={estilos.botoes}>
          <button type="submit" disabled={enviando}>
            {enviando ? 'Enviando...' : textoDaAcao}
          </button>
          <button
            ref={botaoVoltar}
            type="button"
            className={estilos.secundario}
            onClick={fechar}
            disabled={enviando}
          >
            Voltar
          </button>
        </div>
      </form>
    </Dialogo>
  )
}

export default DialogoDeSituacao
