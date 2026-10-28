import { Link } from 'react-router'
import { consultarSaude, type SituacaoDaApi as DadosDaSaude } from '../api/saude.ts'
import Carregando from '../components/estados/Carregando.tsx'
import FalhaAoCarregar from '../components/estados/FalhaAoCarregar.tsx'
import Aviso from '../components/mensagens/Aviso.tsx'
import { useConsulta, type EstadoDaConsulta } from '../hooks/useConsulta.ts'
import { useSessao } from '../hooks/useSessao.ts'
import { useTituloDaPagina } from '../hooks/useTituloDaPagina.ts'
import { CAMINHO_DE_ENTRAR, CAMINHO_DO_CADASTRO, caminhoParaMinhasReservas } from '../navegacao.ts'
import estilos from './PaginaInicial.module.css'

function PaginaInicial() {
  useTituloDaPagina('Início')
  const { autenticado } = useSessao()
  const { estado, recarregar } = useConsulta(consultarSaude, [])

  return (
    <>
      <h1>Conecta Campus</h1>
      <p>
        Reserva de quadras e espaços esportivos para a comunidade acadêmica: cadastre espaços,
        solicite reservas e acompanhe a situação de cada uma.
      </p>
      <p className={estilos.atalhos}>
        {autenticado ? (
          <Link to={caminhoParaMinhasReservas()}>Ir para minhas reservas</Link>
        ) : (
          <>
            <Link to={CAMINHO_DE_ENTRAR}>Entrar</Link>
            <Link to={CAMINHO_DO_CADASTRO}>Criar conta</Link>
          </>
        )}
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
