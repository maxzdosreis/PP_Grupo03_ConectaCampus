import { Link, Navigate, useSearchParams } from 'react-router'
import FormularioDeEntrada from '../components/sessao/FormularioDeEntrada.tsx'
import { useSessao } from '../hooks/useSessao.ts'
import { useTituloDaPagina } from '../hooks/useTituloDaPagina.ts'
import { caminhoParaCadastro, PARAMETRO_DO_PROXIMO, proximoSeguro } from '../navegacao.ts'

function PaginaEntrar() {
  useTituloDaPagina('Entrar')
  const { autenticado } = useSessao()
  const [parametros] = useSearchParams()
  const proximo = parametros.get(PARAMETRO_DO_PROXIMO)

  if (autenticado) {
    return <Navigate to={proximoSeguro(proximo)} replace />
  }
  return (
    <>
      <h1>Entrar</h1>
      <p>Use o e-mail e a senha da sua conta.</p>
      <FormularioDeEntrada />
      <p>
        Ainda não tem conta? <Link to={caminhoParaCadastro(proximo)}>Cadastre-se</Link>
      </p>
    </>
  )
}

export default PaginaEntrar
