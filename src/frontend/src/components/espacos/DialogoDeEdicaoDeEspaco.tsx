import { useCallback, useState, type FormEvent, type RefObject } from 'react'
import {
  editarEspaco,
  type DadosDoEspaco,
  type Espaco,
  type TipoDeEspaco,
} from '../../api/espacos.ts'
import { useEnvio } from '../../hooks/useEnvio.ts'
import { useFocoNoErro } from '../../hooks/useFocoNoErro.ts'
import { useMensagens } from '../../hooks/useMensagens.ts'
import Dialogo from '../dialogo/Dialogo.tsx'
import ErroDoDialogo from '../dialogo/ErroDoDialogo.tsx'
import CamposDoEspaco from './CamposDoEspaco.tsx'
import estilos from './DialogoDeEspaco.module.css'

type PropriedadesDoDialogoDeEdicao = {
  espaco: Espaco
  tipos: TipoDeEspaco[]
  alvoAoFechar: RefObject<HTMLElement | null>
  aoFechar: () => void
  aoAtualizarLista: () => void
}

function dadosDo(espaco: Espaco): DadosDoEspaco {
  return { nome: espaco.nome, tipo: espaco.tipo, capacidade: String(espaco.capacidade) }
}

function camposAlterados(original: DadosDoEspaco, dados: DadosDoEspaco) {
  const campos = Object.keys(dados) as (keyof DadosDoEspaco)[]
  return Object.fromEntries(
    campos.filter((campo) => dados[campo] !== original[campo]).map((campo) => [campo, dados[campo]]),
  ) as Partial<DadosDoEspaco>
}

function tiposComOAtual(tipos: TipoDeEspaco[], espaco: Espaco) {
  return tipos.some(({ valor }) => valor === espaco.tipo)
    ? tipos
    : [{ valor: espaco.tipo, rotulo: espaco.tipo_rotulo }, ...tipos]
}

function DialogoDeEdicaoDeEspaco({
  espaco,
  tipos,
  alvoAoFechar,
  aoFechar,
  aoAtualizarLista,
}: PropriedadesDoDialogoDeEdicao) {
  const original = dadosDo(espaco)
  const [dados, setDados] = useState(original)
  const editar = useCallback(
    (alteracoes: Partial<DadosDoEspaco>) => editarEspaco(espaco.id, alteracoes),
    [espaco.id],
  )
  const { enviar, enviando, errosDosCampos, erroGeral, statusDoErro, limparErroDoCampo } =
    useEnvio(editar)
  const { mostrarSucesso } = useMensagens()
  const { formulario, aviso, focarNoProximoErro } = useFocoNoErro(errosDosCampos, erroGeral)

  function alterar(campo: keyof DadosDoEspaco, valor: string) {
    setDados((atuais) => ({ ...atuais, [campo]: valor }))
    limparErroDoCampo(campo)
  }

  function fechar() {
    if (!enviando) aoFechar()
  }

  async function aoEnviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault()
    focarNoProximoErro()
    const resposta = await enviar(camposAlterados(original, dados))
    if (!resposta) return
    mostrarSucesso(resposta.mensagem)
    aoAtualizarLista()
  }

  return (
    <Dialogo titulo="Editar espaço" aoFechar={fechar} alvoAoFechar={alvoAoFechar}>
      <form ref={formulario} className={estilos.formulario} onSubmit={aoEnviar} noValidate>
        <ErroDoDialogo
          ref={aviso}
          mensagem={erroGeral}
          statusDoErro={statusDoErro}
          aoAtualizar={aoAtualizarLista}
        />
        <CamposDoEspaco
          dados={dados}
          tipos={tiposComOAtual(tipos, espaco)}
          errosDosCampos={errosDosCampos}
          aoAlterar={alterar}
        />
        <div className={estilos.botoes}>
          <button type="submit" disabled={enviando}>
            {enviando ? 'Salvando...' : 'Salvar alterações'}
          </button>
          <button
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

export default DialogoDeEdicaoDeEspaco
