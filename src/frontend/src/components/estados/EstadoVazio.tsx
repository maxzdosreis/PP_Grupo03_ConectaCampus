import type { ReactNode } from 'react'
import estilos from './EstadoVazio.module.css'

type PropriedadesDoEstadoVazio = {
  titulo: string
  descricao?: string
  children?: ReactNode
}

function EstadoVazio({ titulo, descricao, children }: PropriedadesDoEstadoVazio) {
  return (
    <div className={estilos.estadoVazio}>
      <p className={estilos.titulo}>{titulo}</p>
      {descricao && <p className={estilos.descricao}>{descricao}</p>}
      {children}
    </div>
  )
}

export default EstadoVazio
