import {
  startTransition,
  useCallback,
  useEffect,
  useEffectEvent,
  useMemo,
  useState,
  type ReactNode,
} from 'react'
import { useLocation, useNavigate } from 'react-router'
import {
  cadastrar,
  entrar as entrarNaApi,
  usuarioAtual,
  type DadosDeCadastro,
  type DadosDeLogin,
  type Usuario,
} from '../../api/autenticacao.ts'
import { ErroDaApi, MENSAGEM_SESSAO_EXPIRADA } from '../../api/cliente.ts'
import { aoMudarSessao, lerSessao, limparSessao, salvarSessao } from '../../api/sessao.ts'
import { useMensagens } from '../../hooks/useMensagens.ts'
import { caminhoParaEntrar } from '../../navegacao.ts'
import {
  ContextoDeSessao,
  MENSAGEM_DE_CADASTRO,
  MENSAGEM_DE_SAIDA,
  type ValorDaSessao,
} from './contextoDeSessao.ts'

type Estado = {
  usuario: Usuario | null
  verificando: boolean
}

function estadoInicial(): Estado {
  const sessao = lerSessao()
  return { usuario: sessao?.usuario ?? null, verificando: sessao !== null }
}

function SessaoProvider({ children }: { children: ReactNode }) {
  const [{ usuario, verificando }, setEstado] = useState(estadoInicial)
  const { mostrarSucesso, mostrarErro } = useMensagens()
  const navegar = useNavigate()
  const { pathname, search } = useLocation()

  const aoExpirar = useEffectEvent(() => {
    mostrarErro(MENSAGEM_SESSAO_EXPIRADA)
    navegar(caminhoParaEntrar(`${pathname}${search}`), { replace: true })
  })

  useEffect(
    () =>
      aoMudarSessao((sessao, motivo) => {
        setEstado((atual) => ({ ...atual, usuario: sessao?.usuario ?? null }))
        if (motivo === 'expiracao') aoExpirar()
      }),
    [],
  )

  useEffect(() => {
    if (!lerSessao()) return
    let ativo = true
    usuarioAtual()
      .then(({ dados }) => {
        const atual = lerSessao()
        if (atual) salvarSessao({ ...atual, usuario: dados })
      })
      .catch((erro: unknown) => {
        if (erro instanceof ErroDaApi && erro.status === 401) limparSessao()
      })
      .finally(() => {
        if (ativo) setEstado((atual) => ({ ...atual, verificando: false }))
      })
    return () => {
      ativo = false
    }
  }, [])

  const entrar = useCallback(
    async (dados: DadosDeLogin) => {
      const resposta = await entrarNaApi(dados)
      salvarSessao(resposta.dados)
      setEstado({ usuario: resposta.dados.usuario, verificando: false })
      mostrarSucesso(resposta.mensagem)
      return resposta
    },
    [mostrarSucesso],
  )

  const cadastrarEEntrar = useCallback(
    async (dados: DadosDeCadastro) => {
      await cadastrar(dados)
      mostrarSucesso(MENSAGEM_DE_CADASTRO)
      return entrar({ email: dados.email, senha: dados.senha })
    },
    [entrar, mostrarSucesso],
  )

  const sair = useCallback(() => {
    startTransition(() => {
      limparSessao()
      navegar('/')
    })
    mostrarSucesso(MENSAGEM_DE_SAIDA)
  }, [mostrarSucesso, navegar])

  const valor = useMemo<ValorDaSessao>(
    () => ({
      usuario,
      verificando,
      autenticado: usuario !== null,
      ehGestor: usuario?.eh_gestor ?? false,
      entrar,
      cadastrarEEntrar,
      sair,
    }),
    [usuario, verificando, entrar, cadastrarEEntrar, sair],
  )

  return <ContextoDeSessao.Provider value={valor}>{children}</ContextoDeSessao.Provider>
}

export default SessaoProvider
