import { consultarSaude, type SituacaoDaApi as DadosDaSaude } from '../api/saude.ts'
import Carregando from '../components/estados/Carregando.tsx'
import FalhaAoCarregar from '../components/estados/FalhaAoCarregar.tsx'
import Aviso from '../components/mensagens/Aviso.tsx'
import { useConsulta, type EstadoDaConsulta } from '../hooks/useConsulta.ts'
import { useTituloDaPagina } from '../hooks/useTituloDaPagina.ts'

function PaginaInicial() {
  useTituloDaPagina('Início')
  const { estado, recarregar } = useConsulta(consultarSaude, [])

  return (
    <>
      <h1>Conecta Campus</h1>
      <p>
        Reserva de quadras e espaços esportivos para a comunidade acadêmica: cadastre espaços,
        solicite reservas e acompanhe a situação de cada uma.
      </p>
      <section>
        <h2>Situação da API</h2>
        <SituacaoDaApi estado={estado} aoTentarNovamente={recarregar} />
      </section>
    </>
  )
}

type PropriedadesDaSituacao = {
  estado: EstadoDaConsulta<DadosDaSaude>
  aoTentarNovamente: () => void
}

function SituacaoDaApi({ estado, aoTentarNovamente }: PropriedadesDaSituacao) {
  if (estado.tipo === 'carregando') {
    return <Carregando texto="Verificando a conexão com a API..." />
  }
  if (estado.tipo === 'sucesso') {
    return <Aviso variante="sucesso">{estado.mensagem}</Aviso>
  }
  return <FalhaAoCarregar mensagem={estado.mensagem} aoTentarNovamente={aoTentarNovamente} />
}

export default PaginaInicial
