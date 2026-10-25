import { Link } from 'react-router'
import { useTituloDaPagina } from '../hooks/useTituloDaPagina.ts'

function PaginaNaoEncontrada() {
  useTituloDaPagina('Página não encontrada')

  return (
    <>
      <h1>Página não encontrada</h1>
      <p>O endereço acessado não existe no Conecta Campus.</p>
      <p>
        <Link to="/">Voltar para o início</Link>
      </p>
    </>
  )
}

export default PaginaNaoEncontrada
