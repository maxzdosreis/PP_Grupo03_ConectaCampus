import estilos from './Carregando.module.css'

function Carregando({ texto = 'Carregando...' }: { texto?: string }) {
  return (
    <p role="status" className={estilos.carregando}>
      <span className={estilos.indicador} aria-hidden="true" />
      {texto}
    </p>
  )
}

export default Carregando
