import { Navigate, Route, Routes } from 'react-router'
import Layout from './components/layout/Layout.tsx'
import RotaDeGestor from './components/sessao/RotaDeGestor.tsx'
import RotaProtegida from './components/sessao/RotaProtegida.tsx'
import { CAMINHO_DAS_RESERVAS } from './navegacao.ts'
import PaginaCadastro from './pages/PaginaCadastro.tsx'
import PaginaEntrar from './pages/PaginaEntrar.tsx'
import PaginaEspacos from './pages/PaginaEspacos.tsx'
import PaginaMinhaConta from './pages/PaginaMinhaConta.tsx'
import PaginaNovaReserva from './pages/PaginaNovaReserva.tsx'
import PaginaReserva from './pages/PaginaReserva.tsx'
import PaginaReservas from './pages/PaginaReservas.tsx'
import PaginaUsuarios from './pages/PaginaUsuarios.tsx'

function RotasDaAplicacao() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="entrar" element={<PaginaEntrar />} />
        <Route path="cadastro" element={<PaginaCadastro />} />
        <Route element={<RotaProtegida />}>
          <Route index element={<Navigate to={CAMINHO_DAS_RESERVAS} replace />} />
          <Route path="conta" element={<PaginaMinhaConta />} />
          <Route path="espacos" element={<PaginaEspacos />} />
          <Route path="reservas" element={<PaginaReservas />} />
          <Route path="reservas/nova" element={<PaginaNovaReserva />} />
          <Route path="reservas/:reservaId" element={<PaginaReserva />} />
          <Route element={<RotaDeGestor />}>
            <Route path="usuarios" element={<PaginaUsuarios />} />
          </Route>
          <Route path="*" element={<Navigate to={CAMINHO_DAS_RESERVAS} replace />} />
        </Route>
      </Route>
    </Routes>
  )
}

export default RotasDaAplicacao
