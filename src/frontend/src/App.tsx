import { BrowserRouter, Route, Routes } from 'react-router'
import Layout from './components/layout/Layout.tsx'
import MensagensProvider from './components/mensagens/MensagensProvider.tsx'
import PaginaInicial from './pages/PaginaInicial.tsx'
import PaginaNaoEncontrada from './pages/PaginaNaoEncontrada.tsx'

function App() {
  return (
    <MensagensProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<PaginaInicial />} />
            <Route path="*" element={<PaginaNaoEncontrada />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </MensagensProvider>
  )
}

export default App
