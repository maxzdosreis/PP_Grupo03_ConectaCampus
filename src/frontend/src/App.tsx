import { BrowserRouter, Route, Routes } from 'react-router'
import Layout from './components/layout/Layout.tsx'
import MensagensProvider from './components/mensagens/MensagensProvider.tsx'
import RotaProtegida from './components/sessao/RotaProtegida.tsx'
import SessaoProvider from './components/sessao/SessaoProvider.tsx'
import PaginaCadastro from './pages/PaginaCadastro.tsx'
import PaginaEntrar from './pages/PaginaEntrar.tsx'
import PaginaEspacos from './pages/PaginaEspacos.tsx'
import PaginaInicial from './pages/PaginaInicial.tsx'
import PaginaNaoEncontrada from './pages/PaginaNaoEncontrada.tsx'
import PaginaNovaReserva from './pages/PaginaNovaReserva.tsx'
import PaginaReservas from './pages/PaginaReservas.tsx'

function App() {
  return (
    <MensagensProvider>
      <BrowserRouter>
        <SessaoProvider>
          <Routes>
            <Route element={<Layout />}>
              <Route index element={<PaginaInicial />} />
              <Route path="entrar" element={<PaginaEntrar />} />
              <Route path="cadastro" element={<PaginaCadastro />} />
              <Route element={<RotaProtegida />}>
                <Route path="espacos" element={<PaginaEspacos />} />
                <Route path="reservas" element={<PaginaReservas />} />
                <Route path="reservas/nova" element={<PaginaNovaReserva />} />
              </Route>
              <Route path="*" element={<PaginaNaoEncontrada />} />
            </Route>
          </Routes>
        </SessaoProvider>
      </BrowserRouter>
    </MensagensProvider>
  )
}

export default App
