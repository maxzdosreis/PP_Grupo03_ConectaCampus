import { useEffect, useState } from 'react'
import { ErroDaApi, MENSAGEM_ERRO_INESPERADO } from '../api/cliente.ts'
import { consultarSaude } from '../api/saude.ts'

type EstadoDaApi =
  | { tipo: 'carregando' }
  | { tipo: 'sucesso'; mensagem: string }
  | { tipo: 'erro'; mensagem: string }

function PaginaInicial() {
  const [estado, setEstado] = useState<EstadoDaApi>({ tipo: 'carregando' })

  useEffect(() => {
    let ativo = true
    consultarSaude()
      .then((resposta) => {
        if (ativo) setEstado({ tipo: 'sucesso', mensagem: resposta.mensagem })
      })
      .catch((erro: unknown) => {
        const mensagem = erro instanceof ErroDaApi ? erro.message : MENSAGEM_ERRO_INESPERADO
        if (ativo) setEstado({ tipo: 'erro', mensagem })
      })
    return () => {
      ativo = false
    }
  }, [])

  return (
    <main>
      <h1>Conecta Campus</h1>
      <p>
        Reserva de quadras e espaços esportivos para a comunidade acadêmica: cadastre espaços,
        solicite reservas e acompanhe a situação de cada uma.
      </p>
      <section>
        <h2>Situação da API</h2>
        <SituacaoDaApi estado={estado} />
      </section>
    </main>
  )
}

function SituacaoDaApi({ estado }: { estado: EstadoDaApi }) {
  if (estado.tipo === 'carregando') {
    return <p role="status">Verificando a conexão com a API...</p>
  }
  const sucesso = estado.tipo === 'sucesso'
  return (
    <p
      role={sucesso ? 'status' : 'alert'}
      style={{ color: sucesso ? 'var(--cor-sucesso)' : 'var(--cor-erro)' }}
    >
      {estado.mensagem}
    </p>
  )
}

export default PaginaInicial
