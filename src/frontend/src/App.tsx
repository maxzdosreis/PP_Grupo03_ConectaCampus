import { BrowserRouter, Route, Routes } from 'react-router'
import Layout from './components/layout/Layout.tsx'
import MensagensProvider from './components/mensagens/MensagensProvider.tsx'
import PaginaEspacos from './pages/PaginaEspacos.tsx'
import PaginaInicial from './pages/PaginaInicial.tsx'
import PaginaNaoEncontrada from './pages/PaginaNaoEncontrada.tsx'
import PaginaNovaReserva from './pages/PaginaNovaReserva.tsx'
import PaginaReservas from './pages/PaginaReservas.tsx'

function App() {
  return (
    <MensagensProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<PaginaInicial />} />
            <Route path="espacos" element={<PaginaEspacos />} />
            <Route path="reservas" element={<PaginaReservas />} />
            <Route path="reservas/nova" element={<PaginaNovaReserva />} />
            <Route path="*" element={<PaginaNaoEncontrada />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </MensagensProvider>
  )
}

export default App
