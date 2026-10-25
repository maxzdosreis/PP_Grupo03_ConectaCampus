import { useId } from 'react'
import { useSearchParams } from 'react-router'
import { listarEspacos, listarTiposDeEspaco, type Espaco } from '../api/espacos.ts'
import FiltrosDeEspacos from '../components/espacos/FiltrosDeEspacos.tsx'
import FormularioDeEspaco from '../components/espacos/FormularioDeEspaco.tsx'
import TabelaDeEspacos from '../components/espacos/TabelaDeEspacos.tsx'
import Carregando from '../components/estados/Carregando.tsx'
import EstadoVazio from '../components/estados/EstadoVazio.tsx'
import FalhaAoCarregar from '../components/estados/FalhaAoCarregar.tsx'
import { useConsulta, type EstadoDaConsulta } from '../hooks/useConsulta.ts'
import { useTituloDaPagina } from '../hooks/useTituloDaPagina.ts'

const PARAMETRO_TIPO = 'tipo'
const PARAMETRO_APENAS_ATIVOS = 'apenas_ativos'

function PaginaEspacos() {
  useTituloDaPagina('Espaços')
  const idDoCadastro = useId()
  const idDaLista = useId()
  const tipos = useConsulta(listarTiposDeEspaco, [])
  const [parametros, setParametros] = useSearchParams()
  const tipo = parametros.get(PARAMETRO_TIPO) ?? ''
  const apenasAtivos = parametros.get(PARAMETRO_APENAS_ATIVOS) === 'true'
  const { estado, recarregar } = useConsulta(
    () => listarEspacos({ tipo, apenasAtivos }),
    [tipo, apenasAtivos],
  )

  function alterarParametro(nome: string, valor: string | null) {
    setParametros(
      (atuais) => {
        const novos = new URLSearchParams(atuais)
        if (valor) novos.set(nome, valor)
        else novos.delete(nome)
        return novos
      },
      { replace: true },
    )
  }

  const limparFiltros = () => setParametros({}, { replace: true })

  return (
    <>
      <h1>Espaços</h1>
      <section aria-labelledby={idDoCadastro}>
        <h2 id={idDoCadastro}>Cadastrar espaço</h2>
        <FormularioDeEspaco
          tipos={tipos.estado}
          aoTentarCarregarOsTiposDeNovo={tipos.recarregar}
          aoCadastrar={recarregar}
        />
      </section>
      <section aria-labelledby={idDaLista}>
        <h2 id={idDaLista}>Espaços cadastrados</h2>
        <FiltrosDeEspacos
          tipos={tipos.estado.tipo === 'sucesso' ? tipos.estado.dados : null}
          tipo={tipo}
          apenasAtivos={apenasAtivos}
          aoMudarTipo={(novo) => alterarParametro(PARAMETRO_TIPO, novo)}
          aoMudarApenasAtivos={(marcado) =>
            alterarParametro(PARAMETRO_APENAS_ATIVOS, marcado ? 'true' : null)
          }
        />
        <ResultadoDaLista
          estado={estado}
          temFiltros={tipo !== '' || apenasAtivos}
          aoTentarNovamente={recarregar}
          aoLimparFiltros={limparFiltros}
        />
      </section>
    </>
  )
}

type PropriedadesDoResultado = {
  estado: EstadoDaConsulta<Espaco[]>
  temFiltros: boolean
  aoTentarNovamente: () => void
  aoLimparFiltros: () => void
}

function ResultadoDaLista({
  estado,
  temFiltros,
  aoTentarNovamente,
  aoLimparFiltros,
}: PropriedadesDoResultado) {
  const botaoLimparFiltros = (
    <button type="button" onClick={aoLimparFiltros}>
      Limpar filtros
    </button>
  )

  if (estado.tipo === 'carregando') {
    return <Carregando texto="Carregando espaços..." />
  }
  if (estado.tipo === 'erro') {
    return (
      <FalhaAoCarregar mensagem={estado.mensagem} aoTentarNovamente={aoTentarNovamente}>
        {temFiltros && botaoLimparFiltros}
      </FalhaAoCarregar>
    )
  }
  if (estado.dados.length > 0) {
    return <TabelaDeEspacos espacos={estado.dados} legenda={estado.mensagem} />
  }
  if (temFiltros) {
    return <EstadoVazio titulo="Nenhum espaço encontrado">{botaoLimparFiltros}</EstadoVazio>
  }
  return (
    <EstadoVazio
      titulo="Nenhum espaço cadastrado"
      descricao="Use o formulário acima para cadastrar o primeiro."
    />
  )
}

export default PaginaEspacos
