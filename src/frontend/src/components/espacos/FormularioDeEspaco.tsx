import { useState, type FormEvent } from 'react'
import { cadastrarEspaco, type DadosDoEspaco, type TipoDeEspaco } from '../../api/espacos.ts'
import { useEnvio } from '../../hooks/useEnvio.ts'
import { useFocoNoErro } from '../../hooks/useFocoNoErro.ts'
import { useMensagens } from '../../hooks/useMensagens.ts'
import type { EstadoDaConsulta } from '../../hooks/useConsulta.ts'
import Carregando from '../estados/Carregando.tsx'
import FalhaAoCarregar from '../estados/FalhaAoCarregar.tsx'
import Aviso from '../mensagens/Aviso.tsx'
import CamposDoEspaco from './CamposDoEspaco.tsx'
import estilos from './FormularioDeEspaco.module.css'

const FORMULARIO_VAZIO: DadosDoEspaco = { nome: '', tipo: '', capacidade: '' }

type PropriedadesDoFormulario = {
  tipos: EstadoDaConsulta<TipoDeEspaco[]>
  aoTentarCarregarOsTiposDeNovo: () => void
  aoCadastrar: () => void
}

function FormularioDeEspaco({
  tipos,
  aoTentarCarregarOsTiposDeNovo,
  aoCadastrar,
}: PropriedadesDoFormulario) {
  if (tipos.tipo === 'carregando') {
    return <Carregando texto="Carregando os tipos de espaço..." />
  }
  if (tipos.tipo === 'erro') {
    return (
      <FalhaAoCarregar
        mensagem={tipos.mensagem}
        aoTentarNovamente={aoTentarCarregarOsTiposDeNovo}
      />
    )
  }
  return <Formulario tipos={tipos.dados} aoCadastrar={aoCadastrar} />
}

type PropriedadesDoCadastro = {
  tipos: TipoDeEspaco[]
  aoCadastrar: () => void
}

function Formulario({ tipos, aoCadastrar }: PropriedadesDoCadastro) {
  const [dados, setDados] = useState(FORMULARIO_VAZIO)
  const { enviar, enviando, errosDosCampos, erroGeral, limparErroDoCampo } =
    useEnvio(cadastrarEspaco)
  const { mostrarSucesso } = useMensagens()
  const { formulario, aviso, focarNoProximoErro } = useFocoNoErro(errosDosCampos, erroGeral)

  function alterar(campo: keyof DadosDoEspaco, valor: string) {
    setDados((atuais) => ({ ...atuais, [campo]: valor }))
    limparErroDoCampo(campo)
  }

  async function aoEnviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault()
    focarNoProximoErro()
    const resposta = await enviar(dados)
    if (!resposta) return
    mostrarSucesso(resposta.mensagem)
    setDados(FORMULARIO_VAZIO)
    aoCadastrar()
  }

  return (
    <form ref={formulario} className={estilos.formulario} onSubmit={aoEnviar} noValidate>
      {erroGeral && (
        <div ref={aviso} tabIndex={-1}>
          <Aviso variante="erro">{erroGeral}</Aviso>
        </div>
      )}
      <CamposDoEspaco
        dados={dados}
        tipos={tipos}
        errosDosCampos={errosDosCampos}
        aoAlterar={alterar}
      />
      <div>
        <button type="submit" disabled={enviando}>
          {enviando ? 'Cadastrando...' : 'Cadastrar espaço'}
        </button>
      </div>
    </form>
  )
}

export default FormularioDeEspaco
