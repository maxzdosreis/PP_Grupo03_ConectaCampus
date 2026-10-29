import { useId, useRef, useState, type Ref } from 'react'
import { useSearchParams } from 'react-router'
import { listarEspacos, listarTiposDeEspaco, type Espaco } from '../api/espacos.ts'
import DialogoDeAtivacao from '../components/espacos/DialogoDeAtivacao.tsx'
import DialogoDeEdicaoDeEspaco from '../components/espacos/DialogoDeEdicaoDeEspaco.tsx'
import FiltrosDeEspacos from '../components/espacos/FiltrosDeEspacos.tsx'
import FormularioDeEspaco from '../components/espacos/FormularioDeEspaco.tsx'
import TabelaDeEspacos, { type AcoesDeGestao } from '../components/espacos/TabelaDeEspacos.tsx'
import Carregando from '../components/estados/Carregando.tsx'
import EstadoVazio from '../components/estados/EstadoVazio.tsx'
import FalhaAoCarregar from '../components/estados/FalhaAoCarregar.tsx'
import Aviso from '../components/mensagens/Aviso.tsx'
import { useConsulta, type EstadoDaConsulta } from '../hooks/useConsulta.ts'
import { useFocoAoRecarregar } from '../hooks/useFocoAoRecarregar.ts'
import { useSessao } from '../hooks/useSessao.ts'
import { useTituloDaPagina } from '../hooks/useTituloDaPagina.ts'

const PARAMETRO_TIPO = 'tipo'
const PARAMETRO_APENAS_ATIVOS = 'apenas_ativos'

function PaginaEspacos() {
  useTituloDaPagina('Espaços')
  const idDoCadastro = useId()
  const idDaLista = useId()
  const { ehGestor } = useSessao()
  const tipos = useConsulta(listarTiposDeEspaco, [])
  const [parametros, setParametros] = useSearchParams()
  const tipo = parametros.get(PARAMETRO_TIPO) ?? ''
  const apenasAtivos = parametros.get(PARAMETRO_APENAS_ATIVOS) === 'true'
  const { estado, recarregar } = useConsulta(
    () => listarEspacos({ tipo, apenasAtivos }),
    [tipo, apenasAtivos],
  )
  const [emAcao, setEmAcao] = useState<AcaoNoEspaco | null>(null)
  const titulo = useRef<HTMLHeadingElement>(null)
  const regiaoDaTabela = useRef<HTMLDivElement>(null)
  const focarNaListaAoCarregar = useFocoAoRecarregar(
    estado.tipo === 'carregando',
    () => regiaoDaTabela.current ?? titulo.current,
  )
  const gestao: AcoesDeGestao | undefined = ehGestor
    ? {
        aoEditar: (espaco) => setEmAcao({ tipo: 'edicao', espaco }),
        aoAlterarAtivacao: (espaco) => setEmAcao({ tipo: 'ativacao', espaco }),
      }
    : undefined

  function atualizarLista() {
    setEmAcao(null)
    focarNaListaAoCarregar()
    recarregar()
  }

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
      <h1 ref={titulo} tabIndex={-1}>
        Espaços
      </h1>
      {ehGestor ? (
        <section aria-labelledby={idDoCadastro}>
          <h2 id={idDoCadastro}>Cadastrar espaço</h2>
          <FormularioDeEspaco
            tipos={tipos.estado}
            aoTentarCarregarOsTiposDeNovo={tipos.recarregar}
            aoCadastrar={recarregar}
          />
        </section>
      ) : (
        <Aviso variante="informacao">Somente o gestor cadastra espaços.</Aviso>
      )}
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
          podeCadastrar={ehGestor}
          gestao={gestao}
          regiaoDaTabela={regiaoDaTabela}
          aoTentarNovamente={recarregar}
          aoLimparFiltros={limparFiltros}
        />
      </section>
      {emAcao?.tipo === 'edicao' && (
        <DialogoDeEdicaoDeEspaco
          key={emAcao.espaco.id}
          espaco={emAcao.espaco}
          tipos={tipos.estado.tipo === 'sucesso' ? tipos.estado.dados : []}
          alvoAoFechar={titulo}
          aoFechar={() => setEmAcao(null)}
          aoAtualizarLista={atualizarLista}
        />
      )}
      {emAcao?.tipo === 'ativacao' && (
        <DialogoDeAtivacao
          key={emAcao.espaco.id}
          espaco={emAcao.espaco}
          alvoAoFechar={titulo}
          aoFechar={() => setEmAcao(null)}
          aoAtualizarLista={atualizarLista}
        />
      )}
    </>
  )
}

type AcaoNoEspaco = { tipo: 'edicao' | 'ativacao'; espaco: Espaco }

type PropriedadesDoResultado = {
  estado: EstadoDaConsulta<Espaco[]>
  temFiltros: boolean
  podeCadastrar: boolean
  gestao: AcoesDeGestao | undefined
  regiaoDaTabela: Ref<HTMLDivElement>
  aoTentarNovamente: () => void
  aoLimparFiltros: () => void
}

function ResultadoDaLista({
  estado,
  temFiltros,
  podeCadastrar,
  gestao,
  regiaoDaTabela,
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
    return (
      <TabelaDeEspacos
        ref={regiaoDaTabela}
        espacos={estado.dados}
        legenda={estado.mensagem}
        gestao={gestao}
      />
    )
  }
  if (temFiltros) {
    return <EstadoVazio titulo="Nenhum espaço encontrado">{botaoLimparFiltros}</EstadoVazio>
  }
  return (
    <EstadoVazio
      titulo="Nenhum espaço cadastrado"
      descricao={podeCadastrar ? 'Use o formulário acima para cadastrar o primeiro.' : undefined}
    />
  )
}

export default PaginaEspacos
