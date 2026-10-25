import { useCallback, useEffect, useState, type DependencyList } from 'react'
import { mensagemDoErro } from '../api/erros.ts'
import type { RespostaSucesso } from '../api/tipos.ts'

export type EstadoDaConsulta<T> =
  | { tipo: 'carregando' }
  | { tipo: 'sucesso'; dados: T; mensagem: string }
  | { tipo: 'erro'; mensagem: string }

type Resultado<T> = {
  dependencias: DependencyList
  tentativa: number
  estado: EstadoDaConsulta<T>
}

const CARREGANDO = { tipo: 'carregando' } as const

function mesmasDependencias(anteriores: DependencyList, atuais: DependencyList) {
  return (
    anteriores.length === atuais.length &&
    anteriores.every((valor, indice) => Object.is(valor, atuais[indice]))
  )
}

export function useConsulta<T>(
  buscar: () => Promise<RespostaSucesso<T>>,
  dependencias: DependencyList,
): { estado: EstadoDaConsulta<T>; recarregar: () => void } {
  const [tentativa, setTentativa] = useState(0)
  const [resultado, setResultado] = useState<Resultado<T> | null>(null)

  useEffect(() => {
    let ativo = true
    const concluir = (estado: EstadoDaConsulta<T>) => {
      if (ativo) setResultado({ dependencias, tentativa, estado })
    }
    buscar()
      .then(({ dados, mensagem }) => concluir({ tipo: 'sucesso', dados, mensagem }))
      .catch((erro: unknown) => concluir({ tipo: 'erro', mensagem: mensagemDoErro(erro) }))
    return () => {
      ativo = false
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...dependencias, tentativa])

  const recarregar = useCallback(() => setTentativa((anterior) => anterior + 1), [])

  const atual =
    resultado !== null &&
    resultado.tentativa === tentativa &&
    mesmasDependencias(resultado.dependencias, dependencias)

  return { estado: atual ? resultado.estado : CARREGANDO, recarregar }
}
