import { useState, type FormEvent } from 'react'
import type { DadosDeLogin } from '../../api/autenticacao.ts'
import { useEnvio } from '../../hooks/useEnvio.ts'
import { useFocoNoErro } from '../../hooks/useFocoNoErro.ts'
import { useSessao } from '../../hooks/useSessao.ts'
import Campo from '../formulario/Campo.tsx'
import Aviso from '../mensagens/Aviso.tsx'
import estilos from './FormularioDeAcesso.module.css'

const FORMULARIO_VAZIO: DadosDeLogin = { email: '', senha: '' }

function FormularioDeEntrada() {
  const { entrar } = useSessao()
  const [dados, setDados] = useState(FORMULARIO_VAZIO)
  const { enviar, enviando, errosDosCampos, erroGeral, limparErroDoCampo } = useEnvio(entrar)
  const { formulario, aviso, focarNoProximoErro } = useFocoNoErro(errosDosCampos, erroGeral)

  function alterar(campo: keyof DadosDeLogin, valor: string) {
    setDados((atuais) => ({ ...atuais, [campo]: valor }))
    limparErroDoCampo(campo)
  }

  async function aoEnviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault()
    focarNoProximoErro()
    await enviar(dados)
  }

  return (
    <form ref={formulario} className={estilos.formulario} onSubmit={aoEnviar} noValidate>
      {erroGeral && (
        <div ref={aviso} tabIndex={-1}>
          <Aviso variante="erro">{erroGeral}</Aviso>
        </div>
      )}
      <Campo rotulo="E-mail" erro={errosDosCampos.email}>
        {(controle) => (
          <input
            {...controle}
            type="email"
            name="email"
            autoComplete="email"
            value={dados.email}
            onChange={(evento) => alterar('email', evento.target.value)}
          />
        )}
      </Campo>
      <Campo rotulo="Senha" erro={errosDosCampos.senha}>
        {(controle) => (
          <input
            {...controle}
            type="password"
            name="senha"
            autoComplete="current-password"
            value={dados.senha}
            onChange={(evento) => alterar('senha', evento.target.value)}
          />
        )}
      </Campo>
      <div>
        <button type="submit" disabled={enviando}>
          {enviando ? 'Entrando...' : 'Entrar'}
        </button>
      </div>
    </form>
  )
}

export default FormularioDeEntrada
