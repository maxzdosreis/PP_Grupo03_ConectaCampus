import { Link } from 'react-router'

function PaginaNaoEncontrada() {
  return (
    <main>
      <h1>Página não encontrada</h1>
      <p>O endereço acessado não existe no Conecta Campus.</p>
      <Link to="/">Voltar para o início</Link>
    </main>
  )
}

export default PaginaNaoEncontrada
