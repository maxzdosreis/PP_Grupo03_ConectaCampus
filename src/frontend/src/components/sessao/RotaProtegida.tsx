import { Navigate, Outlet, useLocation } from 'react-router'
import { useSessao } from '../../hooks/useSessao.ts'
import { caminhoParaEntrar } from '../../navegacao.ts'
import Carregando from '../estados/Carregando.tsx'

function RotaProtegida() {
  const { verificando, autenticado } = useSessao()
  const { pathname, search } = useLocation()

  if (verificando) {
    return <Carregando texto="Verificando sua sessão..." />
  }
  if (!autenticado) {
    return <Navigate to={caminhoParaEntrar(`${pathname}${search}`)} replace />
  }
  return <Outlet />
}

export default RotaProtegida
