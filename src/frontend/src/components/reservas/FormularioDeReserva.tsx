import { useCallback, useEffect, useRef, useState, type FormEvent } from 'react'
import { ErroDaApi } from '../../api/cliente.ts'
import type { Espaco } from '../../api/espacos.ts'
import {
  solicitarReserva,
  type DadosDaReserva,
  type HorarioLivre,
  type RegrasDeAgenda,
  type Reserva,
} from '../../api/reservas.ts'
import { useEnvio } from '../../hooks/useEnvio.ts'
import { useFocoNoErro } from '../../hooks/useFocoNoErro.ts'
import { useMensagens } from '../../hooks/useMensagens.ts'
import Campo from '../formulario/Campo.tsx'
import Aviso from '../mensagens/Aviso.tsx'
import AgendaDoDia from './AgendaDoDia.tsx'
import { horarioSugerido } from './agendaDoDia.ts'
import { descreverRegrasDeAgenda } from './dicaDaAgenda.ts'
import estilos from './FormularioDeReserva.module.css'

const CODIGO_DO_CONFLITO_DE_HORARIO = 'CONFLITO_DE_HORARIO'

type PropriedadesDoFormulario = {
  espacos: Espaco[]
  espacoInicial: string
  focarAoAbrir: boolean
  regras: RegrasDeAgenda | null
  aoSolicitar: (reserva: Reserva) => void
}

function FormularioDeReserva({
  espacos,
  espacoInicial,
  focarAoAbrir,
  regras,
  aoSolicitar,
}: PropriedadesDoFormulario) {
  const [dados, setDados] = useState<DadosDaReserva>({
    espaco_id: espacoInicial,
    data: '',
    hora_inicio: '',
    hora_fim: '',
    finalidade: '',
  })
  const [recargasDaAgenda, setRecargasDaAgenda] = useState(0)
  const solicitarEAtualizarAgenda = useCallback(async (dadosDaReserva: DadosDaReserva) => {
    try {
      return await solicitarReserva(dadosDaReserva)
    } catch (erro) {
      if (erro instanceof ErroDaApi && erro.codigo === CODIGO_DO_CONFLITO_DE_HORARIO) {
        setRecargasDaAgenda((anteriores) => anteriores + 1)
      }
      throw erro
    }
  }, [])
  const { enviar, enviando, errosDosCampos, erroGeral, limparErroDoCampo } =
    useEnvio(solicitarEAtualizarAgenda)
  const { mostrarSucesso } = useMensagens()
  const { formulario, aviso, focarNoProximoErro } = useFocoNoErro(errosDosCampos, erroGeral)
  const seletorDeEspaco = useRef<HTMLSelectElement>(null)
  const campoDeTermino = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (focarAoAbrir) seletorDeEspaco.current?.focus()
  }, [focarAoAbrir])

  function alterar(campo: keyof DadosDaReserva, valor: string) {
    setDados((atuais) => ({ ...atuais, [campo]: valor }))
    limparErroDoCampo(campo)
  }

  function usarHorario(livre: HorarioLivre) {
    const { hora_inicio, hora_fim } = horarioSugerido(
      livre,
      regras?.duracao_maxima_em_minutos ?? null,
    )
    alterar('hora_inicio', hora_inicio)
    alterar('hora_fim', hora_fim)
    campoDeTermino.current?.focus()
  }

  async function aoEnviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault()
    focarNoProximoErro()
    const resposta = await enviar(dados)
    if (!resposta) return
    mostrarSucesso(resposta.mensagem)
    aoSolicitar(resposta.dados)
  }

  return (
    <form ref={formulario} className={estilos.formulario} onSubmit={aoEnviar} noValidate>
      {erroGeral && (
        <div ref={aviso} tabIndex={-1}>
          <Aviso variante="erro">{erroGeral}</Aviso>
        </div>
      )}
      <Campo rotulo="Espaço" erro={errosDosCampos.espaco_id}>
        {(controle) => (
          <select
            {...controle}
            ref={seletorDeEspaco}
            name="espaco_id"
            value={dados.espaco_id}
            onChange={(evento) => alterar('espaco_id', evento.target.value)}
          >
            <option value="">Selecione o espaço</option>
            {espacos.map(({ id, nome, tipo_rotulo }) => (
              <option key={id} value={String(id)}>
                {nome} ({tipo_rotulo})
              </option>
            ))}
          </select>
        )}
      </Campo>
      {regras && <p className={estilos.dicaDaAgenda}>{descreverRegrasDeAgenda(regras)}</p>}
      <Campo rotulo="Data" erro={errosDosCampos.data}>
        {(controle) => (
          <input
            {...controle}
            type="date"
            name="data"
            value={dados.data}
            onChange={(evento) => alterar('data', evento.target.value)}
          />
        )}
      </Campo>
      <AgendaDoDia
        espacoId={dados.espaco_id}
        data={dados.data}
        recargas={recargasDaAgenda}
        aoUsarHorario={usarHorario}
      />
      <div className={estilos.horario}>
        <Campo rotulo="Início" erro={errosDosCampos.hora_inicio}>
          {(controle) => (
            <input
              {...controle}
              type="time"
              name="hora_inicio"
              value={dados.hora_inicio}
              onChange={(evento) => alterar('hora_inicio', evento.target.value)}
            />
          )}
        </Campo>
        <Campo rotulo="Término" erro={errosDosCampos.hora_fim}>
          {(controle) => (
            <input
              {...controle}
              ref={campoDeTermino}
              type="time"
              name="hora_fim"
              value={dados.hora_fim}
              onChange={(evento) => alterar('hora_fim', evento.target.value)}
            />
          )}
        </Campo>
      </div>
      <Campo rotulo="Finalidade" dica="Ex.: treino do time de vôlei" erro={errosDosCampos.finalidade}>
        {(controle) => (
          <textarea
            {...controle}
            name="finalidade"
            rows={3}
            value={dados.finalidade}
            onChange={(evento) => alterar('finalidade', evento.target.value)}
          />
        )}
      </Campo>
      <div>
        <button type="submit" disabled={enviando}>
          {enviando ? 'Enviando solicitação...' : 'Solicitar reserva'}
        </button>
      </div>
    </form>
  )
}

export default FormularioDeReserva
