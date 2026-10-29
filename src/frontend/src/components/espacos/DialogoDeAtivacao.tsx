import { useCallback, useRef, type FormEvent, type RefObject } from 'react'
import { ativarEspaco, desativarEspaco, type Espaco } from '../../api/espacos.ts'
import { useEnvio } from '../../hooks/useEnvio.ts'
import { useFocoNoErro } from '../../hooks/useFocoNoErro.ts'
import { useMensagens } from '../../hooks/useMensagens.ts'
import Dialogo from '../dialogo/Dialogo.tsx'
import Aviso from '../mensagens/Aviso.tsx'
import estilos from './DialogoDeEspaco.module.css'

const STATUS_DE_LISTA_DESATUALIZADA = [404, 409]

const TEXTOS = {
  desativar: {
    titulo: 'Desativar espaço',
    enviando: 'Desativando...',
    explicacao:
      'Novas reservas ficarão bloqueadas. As reservas já existentes continuam valendo; ' +
      'cancele-as na tela de reservas, se precisar.',
  },
  reativar: {
    titulo: 'Reativar espaço',
    enviando: 'Reativando...',
    explicacao: 'O espaço voltará a aceitar novas reservas.',
  },
}

type PropriedadesDoDialogoDeAtivacao = {
  espaco: Espaco
  alvoAoFechar: RefObject<HTMLElement | null>
  aoFechar: () => void
  aoAtualizarLista: () => void
}

function DialogoDeAtivacao({
  espaco,
  alvoAoFechar,
  aoFechar,
  aoAtualizarLista,
}: PropriedadesDoDialogoDeAtivacao) {
  const textos = espaco.ativo ? TEXTOS.desativar : TEXTOS.reativar
  const alternar = useCallback(
    () => (espaco.ativo ? desativarEspaco(espaco.id) : ativarEspaco(espaco.id)),
    [espaco.ativo, espaco.id],
  )
  const { enviar, enviando, errosDosCampos, erroGeral, statusDoErro } = useEnvio<void, Espaco>(alternar)
  const { mostrarSucesso } = useMensagens()
  const { formulario, aviso, focarNoProximoErro } = useFocoNoErro(errosDosCampos, erroGeral)
  const botaoVoltar = useRef<HTMLButtonElement>(null)
  const listaDesatualizada =
    statusDoErro !== null && STATUS_DE_LISTA_DESATUALIZADA.includes(statusDoErro)

  function fechar() {
    if (!enviando) aoFechar()
  }

  async function aoEnviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault()
    focarNoProximoErro()
    const resposta = await enviar()
    if (!resposta) return
    mostrarSucesso(resposta.mensagem)
    aoAtualizarLista()
  }

  return (
    <Dialogo
      titulo={textos.titulo}
      aoFechar={fechar}
      focoInicial={botaoVoltar}
      alvoAoFechar={alvoAoFechar}
    >
      <form ref={formulario} className={estilos.formulario} onSubmit={aoEnviar} noValidate>
        {erroGeral && (
          <div ref={aviso} tabIndex={-1} className={estilos.erro}>
            <Aviso variante="erro">{erroGeral}</Aviso>
            {listaDesatualizada && (
              <div>
                <button type="button" onClick={aoAtualizarLista}>
                  Atualizar lista
                </button>
              </div>
            )}
          </div>
        )}
        <p className={estilos.texto}>
          <strong>{espaco.nome}</strong> ({espaco.tipo_rotulo})
        </p>
        <p className={estilos.texto}>{textos.explicacao}</p>
        <div className={estilos.botoes}>
          <button type="submit" disabled={enviando}>
            {enviando ? textos.enviando : textos.titulo}
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

export default DialogoDeAtivacao
