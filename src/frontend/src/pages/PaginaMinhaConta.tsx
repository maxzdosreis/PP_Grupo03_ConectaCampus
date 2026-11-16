import FormularioDeTrocaDeSenha from '../components/sessao/FormularioDeTrocaDeSenha.tsx'
import { useSessao } from '../hooks/useSessao.ts'
import { useTituloDaPagina } from '../hooks/useTituloDaPagina.ts'

function PaginaMinhaConta() {
  useTituloDaPagina('Minha conta')
  const { usuario } = useSessao()

  return (
    <>
      <h1>Minha conta</h1>
      {usuario && (
        <p>
          {usuario.nome} · {usuario.email} · matrícula {usuario.matricula}
        </p>
      )}
      <h2>Trocar a senha</h2>
      <p>
        Informe a senha atual e escolha uma nova. Nos outros aparelhos, será preciso entrar de
        novo.
      </p>
      <FormularioDeTrocaDeSenha />
    </>
  )
}

export default PaginaMinhaConta
