import { BrowserRouter, Route, Routes } from 'react-router'
import PaginaInicial from './pages/PaginaInicial.tsx'
import PaginaNaoEncontrada from './pages/PaginaNaoEncontrada.tsx'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<PaginaInicial />} />
        <Route path="*" element={<PaginaNaoEncontrada />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
