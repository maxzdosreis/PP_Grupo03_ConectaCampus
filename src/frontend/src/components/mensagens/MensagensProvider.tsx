import { useCallback, useEffect, useMemo, useRef, useState, type ReactNode } from 'react'
import { mensagemDoErro } from '../../api/erros.ts'
import Aviso from './Aviso.tsx'
import {
  ContextoDeMensagens,
  MAXIMO_DE_NOTIFICACOES_VISIVEIS,
  TEMPO_DE_EXIBICAO_DO_SUCESSO_MS,
} from './contextoDeMensagens.ts'
import estilos from './MensagensProvider.module.css'

type Notificacao = {
  id: number
  variante: 'sucesso' | 'erro'
  texto: string
}

function MensagensProvider({ children }: { children: ReactNode }) {
  const [notificacoes, setNotificacoes] = useState<Notificacao[]>([])
  const ultimoId = useRef(0)

  const adicionar = useCallback((variante: Notificacao['variante'], texto: string) => {
    ultimoId.current += 1
    const nova = { id: ultimoId.current, variante, texto }
    setNotificacoes((fila) => [...fila, nova].slice(-MAXIMO_DE_NOTIFICACOES_VISIVEIS))
  }, [])

  const fechar = useCallback((id: number) => {
    setNotificacoes((fila) => fila.filter((notificacao) => notificacao.id !== id))
  }, [])

  const mostrarSucesso = useCallback((texto: string) => adicionar('sucesso', texto), [adicionar])

  const mostrarErro = useCallback(
    (erroOuTexto: unknown) =>
      adicionar('erro', typeof erroOuTexto === 'string' ? erroOuTexto : mensagemDoErro(erroOuTexto)),
    [adicionar],
  )

  const mensagens = useMemo(() => ({ mostrarSucesso, mostrarErro }), [mostrarSucesso, mostrarErro])

  const renderizar = (variante: Notificacao['variante']) =>
    notificacoes
      .filter((notificacao) => notificacao.variante === variante)
      .map((notificacao) => (
        <ItemDeNotificacao key={notificacao.id} notificacao={notificacao} aoFechar={fechar} />
      ))

  return (
    <ContextoDeMensagens.Provider value={mensagens}>
      {children}
      <div className={estilos.regiao}>
        <div aria-live="polite" className={estilos.lista}>
          {renderizar('sucesso')}
        </div>
        <div aria-live="assertive" className={estilos.lista}>
          {renderizar('erro')}
        </div>
      </div>
    </ContextoDeMensagens.Provider>
  )
}

type PropriedadesDoItem = {
  notificacao: Notificacao
  aoFechar: (id: number) => void
}

function ItemDeNotificacao({ notificacao: { id, variante, texto }, aoFechar }: PropriedadesDoItem) {
  useEffect(() => {
    if (variante !== 'sucesso') {
      return
    }
    const temporizador = setTimeout(() => aoFechar(id), TEMPO_DE_EXIBICAO_DO_SUCESSO_MS)
    return () => clearTimeout(temporizador)
  }, [id, variante, aoFechar])

  return (
    <div className={estilos.notificacao}>
      <Aviso variante={variante} anunciar={false} aoFechar={() => aoFechar(id)}>
        {texto}
      </Aviso>
    </div>
  )
}

export default MensagensProvider
