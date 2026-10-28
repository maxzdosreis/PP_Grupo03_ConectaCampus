import { Link, Navigate, useSearchParams } from 'react-router'
import FormularioDeCadastro from '../components/sessao/FormularioDeCadastro.tsx'
import { useSessao } from '../hooks/useSessao.ts'
import { useTituloDaPagina } from '../hooks/useTituloDaPagina.ts'
import {
  CAMINHO_DA_NOVA_RESERVA,
  caminhoParaEntrar,
  PARAMETRO_DO_PROXIMO,
  proximoSeguro,
} from '../navegacao.ts'

function PaginaCadastro() {
  useTituloDaPagina('Criar conta')
  const { autenticado } = useSessao()
  const [parametros] = useSearchParams()
  const proximo = parametros.get(PARAMETRO_DO_PROXIMO)

  if (autenticado) {
    return <Navigate to={proximoSeguro(proximo, CAMINHO_DA_NOVA_RESERVA)} replace />
  }
  return (
    <>
      <h1>Criar conta</h1>
      <p>Cadastre-se como solicitante para reservar quadras e espaços esportivos.</p>
      <FormularioDeCadastro />
      <p>
        Já tem conta? <Link to={caminhoParaEntrar(proximo)}>Entrar</Link>
      </p>
    </>
  )
}

export default PaginaCadastro
