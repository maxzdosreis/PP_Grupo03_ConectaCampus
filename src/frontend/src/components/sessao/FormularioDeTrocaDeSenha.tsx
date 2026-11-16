import { useRef, useState, type FormEvent } from 'react'
import { alterarSenha, type DadosDaTrocaDeSenha } from '../../api/autenticacao.ts'
import { lerSessao } from '../../api/sessao.ts'
import { useEnvio } from '../../hooks/useEnvio.ts'
import { useFocoNoErro } from '../../hooks/useFocoNoErro.ts'
import { useMensagens } from '../../hooks/useMensagens.ts'
import Campo from '../formulario/Campo.tsx'
import Aviso from '../mensagens/Aviso.tsx'
import estilos from './FormularioDeAcesso.module.css'

const MENSAGEM_DE_CONFIRMACAO = 'A confirmação não é igual à nova senha.'

type DadosDoFormulario = {
  senha_atual: string
  nova_senha: string
  confirmacao: string
}

const FORMULARIO_VAZIO: DadosDoFormulario = { senha_atual: '', nova_senha: '', confirmacao: '' }

type DescricaoDoCampo = {
  campo: keyof DadosDoFormulario
  rotulo: string
  autoComplete: string
  dica?: string
}

const CAMPOS: DescricaoDoCampo[] = [
  { campo: 'senha_atual', rotulo: 'Senha atual', autoComplete: 'current-password' },
  {
    campo: 'nova_senha',
    rotulo: 'Nova senha',
    autoComplete: 'new-password',
    dica: 'Use pelo menos 8 caracteres.',
  },
  { campo: 'confirmacao', rotulo: 'Confirme a nova senha', autoComplete: 'new-password' },
]

function FormularioDeTrocaDeSenha() {
  const { mostrarSucesso } = useMensagens()
  const [dados, setDados] = useState(FORMULARIO_VAZIO)
  const [erroDaConfirmacao, setErroDaConfirmacao] = useState<string | null>(null)
  const confirmacao = useRef<HTMLInputElement>(null)
  const { enviar, enviando, errosDosCampos, erroGeral, limparErroDoCampo } = useEnvio(
    (corpo: DadosDaTrocaDeSenha) => alterarSenha(corpo),
  )
  const { formulario, aviso, focarNoProximoErro } = useFocoNoErro(errosDosCampos, erroGeral)

  function alterar(campo: keyof DadosDoFormulario, valor: string) {
    setDados((atuais) => ({ ...atuais, [campo]: valor }))
    if (campo === 'confirmacao') {
      setErroDaConfirmacao(null)
    } else {
      limparErroDoCampo(campo)
    }
  }

  async function aoEnviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault()
    if (dados.nova_senha !== dados.confirmacao) {
      setErroDaConfirmacao(MENSAGEM_DE_CONFIRMACAO)
      confirmacao.current?.focus()
      return
    }
    focarNoProximoErro()
    const resposta = await enviar({
      senha_atual: dados.senha_atual,
      nova_senha: dados.nova_senha,
      refresh_atual: lerSessao()?.refresh,
    })
    if (!resposta) return
    mostrarSucesso(resposta.mensagem)
    setDados(FORMULARIO_VAZIO)
  }

  return (
    <form ref={formulario} className={estilos.formulario} onSubmit={aoEnviar} noValidate>
      {erroGeral && (
        <div ref={aviso} tabIndex={-1}>
          <Aviso variante="erro">{erroGeral}</Aviso>
        </div>
      )}
      {CAMPOS.map(({ campo, rotulo, autoComplete, dica }) => (
        <Campo
          key={campo}
          rotulo={rotulo}
          dica={dica}
          erro={campo === 'confirmacao' ? (erroDaConfirmacao ?? undefined) : errosDosCampos[campo]}
        >
          {(controle) => (
            <input
              {...controle}
              ref={campo === 'confirmacao' ? confirmacao : undefined}
              type="password"
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
          {enviando ? 'Alterando...' : 'Alterar senha'}
        </button>
      </div>
    </form>
  )
}

export default FormularioDeTrocaDeSenha
