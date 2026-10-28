import { useState, type FormEvent } from 'react'
import { cadastrarEspaco, type DadosDoEspaco, type TipoDeEspaco } from '../../api/espacos.ts'
import { useEnvio } from '../../hooks/useEnvio.ts'
import { useFocoNoErro } from '../../hooks/useFocoNoErro.ts'
import { useMensagens } from '../../hooks/useMensagens.ts'
import type { EstadoDaConsulta } from '../../hooks/useConsulta.ts'
import Carregando from '../estados/Carregando.tsx'
import FalhaAoCarregar from '../estados/FalhaAoCarregar.tsx'
import Campo from '../formulario/Campo.tsx'
import Aviso from '../mensagens/Aviso.tsx'
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

type PropriedadesDosCampos = {
  tipos: TipoDeEspaco[]
  aoCadastrar: () => void
}

function Formulario({ tipos, aoCadastrar }: PropriedadesDosCampos) {
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
      <Campo rotulo="Nome" erro={errosDosCampos.nome}>
        {(controle) => (
          <input
            {...controle}
            type="text"
            name="nome"
            autoComplete="off"
            value={dados.nome}
            onChange={(evento) => alterar('nome', evento.target.value)}
          />
        )}
      </Campo>
      <Campo rotulo="Tipo" erro={errosDosCampos.tipo}>
        {(controle) => (
          <select
            {...controle}
            name="tipo"
            value={dados.tipo}
            onChange={(evento) => alterar('tipo', evento.target.value)}
          >
            <option value="">Selecione o tipo</option>
            {tipos.map(({ valor, rotulo }) => (
              <option key={valor} value={valor}>
                {rotulo}
              </option>
            ))}
          </select>
        )}
      </Campo>
      <Campo
        rotulo="Capacidade"
        dica="Número máximo de pessoas."
        erro={errosDosCampos.capacidade}
      >
        {(controle) => (
          <input
            {...controle}
            type="number"
            inputMode="numeric"
            name="capacidade"
            value={dados.capacidade}
            onChange={(evento) => alterar('capacidade', evento.target.value)}
          />
        )}
      </Campo>
      <div>
        <button type="submit" disabled={enviando}>
          {enviando ? 'Cadastrando...' : 'Cadastrar espaço'}
        </button>
      </div>
    </form>
  )
}

export default FormularioDeEspaco
