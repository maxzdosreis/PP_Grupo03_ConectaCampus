import { Navigate, Outlet } from 'react-router'
import { useSessao } from '../../hooks/useSessao.ts'
import { CAMINHO_DAS_RESERVAS } from '../../navegacao.ts'

function RotaDeGestor() {
  const { ehGestor } = useSessao()
  return ehGestor ? <Outlet /> : <Navigate to={CAMINHO_DAS_RESERVAS} replace />
}

export default RotaDeGestor
