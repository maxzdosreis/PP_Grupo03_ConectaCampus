import { useState, type FormEvent } from 'react'
import type { DadosDeCadastro } from '../../api/autenticacao.ts'
import { useEnvio } from '../../hooks/useEnvio.ts'
import { useFocoNoErro } from '../../hooks/useFocoNoErro.ts'
import { useSessao } from '../../hooks/useSessao.ts'
import Campo from '../formulario/Campo.tsx'
import Aviso from '../mensagens/Aviso.tsx'
import estilos from './FormularioDeAcesso.module.css'

const FORMULARIO_VAZIO: DadosDeCadastro = { nome: '', matricula: '', email: '', senha: '' }

type DescricaoDoCampo = {
  campo: keyof DadosDeCadastro
  rotulo: string
  tipo: 'text' | 'email' | 'password'
  autoComplete: string
  dica?: string
}

const CAMPOS: DescricaoDoCampo[] = [
  { campo: 'nome', rotulo: 'Nome', tipo: 'text', autoComplete: 'name' },
  { campo: 'matricula', rotulo: 'Matrícula', tipo: 'text', autoComplete: 'off' },
  { campo: 'email', rotulo: 'E-mail', tipo: 'email', autoComplete: 'email' },
  {
    campo: 'senha',
    rotulo: 'Senha',
    tipo: 'password',
    autoComplete: 'new-password',
    dica: 'Use pelo menos 8 caracteres.',
  },
]

function FormularioDeCadastro() {
  const { cadastrarEEntrar } = useSessao()
  const [dados, setDados] = useState(FORMULARIO_VAZIO)
  const { enviar, enviando, errosDosCampos, erroGeral, limparErroDoCampo } =
    useEnvio(cadastrarEEntrar)
  const { formulario, aviso, focarNoProximoErro } = useFocoNoErro(errosDosCampos, erroGeral)

  function alterar(campo: keyof DadosDeCadastro, valor: string) {
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
      {CAMPOS.map(({ campo, rotulo, tipo, autoComplete, dica }) => (
        <Campo key={campo} rotulo={rotulo} dica={dica} erro={errosDosCampos[campo]}>
          {(controle) => (
            <input
              {...controle}
              type={tipo}
              name={campo}
              autoComplete={autoComplete}
              value={dados[campo]}
              onChange={(evento) => alterar(campo, evento.target.value)}
            />
          )}
        </Campo>
      ))}
      <div>
        <button type="submit" disabled={enviando}>
          {enviando ? 'Criando conta...' : 'Criar conta'}
        </button>
      </div>
    </form>
  )
}

export default FormularioDeCadastro
