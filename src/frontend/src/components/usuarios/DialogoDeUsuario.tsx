import { useCallback, useRef, type FormEvent, type RefObject } from 'react'
import { alterarUsuario, type UsuarioGerenciado } from '../../api/usuarios.ts'
import { useEnvio } from '../../hooks/useEnvio.ts'
import { useFocoNoErro } from '../../hooks/useFocoNoErro.ts'
import { useMensagens } from '../../hooks/useMensagens.ts'
import { Botao } from '../botao/Botao.tsx'
import Dialogo from '../dialogo/Dialogo.tsx'
import ErroDoDialogo from '../dialogo/ErroDoDialogo.tsx'
import { alteracaoDaAcao, ROTULOS_DAS_ACOES, type AcaoDeUsuario } from './acoesDeUsuario.ts'
import estilos from './DialogoDeUsuario.module.css'

const TEXTOS: Record<AcaoDeUsuario, { titulo: string; enviando: string; explicacao: string }> = {
  promover: {
    titulo: 'Promover a Gestor',
    enviando: 'Promovendo...',
    explicacao:
      'A pessoa passará a cadastrar espaços, decidir sobre as reservas de todos e ' +
      'gerenciar usuários, já na próxima ação dela.',
  },
  rebaixar: {
    titulo: 'Rebaixar a Solicitante',
    enviando: 'Rebaixando...',
    explicacao:
      'A pessoa perderá as funções de Gestor já na próxima ação dela e passará a ver ' +
      'só as próprias reservas.',
  },
  desativar: {
    titulo: 'Desativar conta',
    enviando: 'Desativando...',
    explicacao:
      'A pessoa não conseguirá entrar nem renovar a sessão. As reservas dela continuam ' +
      'como estão; cancele-as na tela de reservas, se precisar.',
  },
  reativar: {
    titulo: 'Reativar conta',
    enviando: 'Reativando...',
    explicacao:
      'A pessoa poderá entrar de novo. Nada é restaurado: as reservas continuam como estão.',
  },
}

type PropriedadesDoDialogoDeUsuario = {
  usuario: UsuarioGerenciado
  acao: AcaoDeUsuario
  alvoAoFechar: RefObject<HTMLElement | null>
  aoFechar: () => void
  aoAtualizarLista: () => void
}

function DialogoDeUsuario({
  usuario,
  acao,
  alvoAoFechar,
  aoFechar,
  aoAtualizarLista,
}: PropriedadesDoDialogoDeUsuario) {
  const textos = TEXTOS[acao]
  const alterar = useCallback(
    () => alterarUsuario(usuario.id, alteracaoDaAcao(acao)),
    [usuario.id, acao],
  )
  const { enviar, enviando, errosDosCampos, erroGeral, statusDoErro } = useEnvio<
    void,
    UsuarioGerenciado
  >(alterar)
  const { mostrarSucesso } = useMensagens()
  const { formulario, aviso, focarNoProximoErro } = useFocoNoErro(errosDosCampos, erroGeral)
  const botaoVoltar = useRef<HTMLButtonElement>(null)

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
        <ErroDoDialogo
          ref={aviso}
          mensagem={erroGeral}
          statusDoErro={statusDoErro}
          aoAtualizar={aoAtualizarLista}
        />
        <p className={estilos.texto}>
          <strong>{usuario.nome}</strong> ({usuario.email})
        </p>
        <p className={estilos.texto}>{textos.explicacao}</p>
        <div className={estilos.botoes}>
          <Botao
            acao={acao}
            type="submit"
            disabled={enviando}
          >
            {enviando ? textos.enviando : ROTULOS_DAS_ACOES[acao]}
          </Botao>
          <Botao
            acao="voltar"
            ref={botaoVoltar}
            type="button"
            onClick={fechar}
            disabled={enviando}
          >
            Voltar
          </Botao>
        </div>
      </form>
    </Dialogo>
  )
}

export default DialogoDeUsuario
