import { BrowserRouter } from 'react-router'
import MensagensProvider from './components/mensagens/MensagensProvider.tsx'
import SessaoProvider from './components/sessao/SessaoProvider.tsx'
import RotasDaAplicacao from './RotasDaAplicacao.tsx'

function App() {
  return (
    <MensagensProvider>
      <BrowserRouter>
        <SessaoProvider>
          <RotasDaAplicacao />
        </SessaoProvider>
      </BrowserRouter>
    </MensagensProvider>
  )
}

export default App
