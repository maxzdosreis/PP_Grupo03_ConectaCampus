import { useId, type Ref } from 'react'
import { Link } from 'react-router'
import type { Espaco } from '../../api/espacos.ts'
import { caminhoParaReservar } from '../../navegacao.ts'
import Etiqueta from '../etiqueta/Etiqueta.tsx'
import estilos from './TabelaDeEspacos.module.css'

export type AcoesDeGestao = {
  aoEditar: (espaco: Espaco) => void
  aoAlterarAtivacao: (espaco: Espaco) => void
}

type PropriedadesDaTabela = {
  espacos: Espaco[]
  legenda: string
  gestao?: AcoesDeGestao
  ref?: Ref<HTMLDivElement>
}

function TabelaDeEspacos({ espacos, legenda, gestao, ref }: PropriedadesDaTabela) {
  const idDaLegenda = useId()
  return (
    <div
      ref={ref}
      className={estilos.rolagem}
      role="region"
      aria-labelledby={idDaLegenda}
      tabIndex={0}
    >
      <table className={estilos.tabela}>
        <caption id={idDaLegenda} className={estilos.legenda}>
          {legenda}
        </caption>
        <thead>
          <tr>
            <th scope="col">Nome</th>
            <th scope="col">Tipo</th>
            <th scope="col" className={estilos.numero}>
              Capacidade
            </th>
            <th scope="col">Situação</th>
            <th scope="col">Ações</th>
          </tr>
        </thead>
        <tbody>
          {espacos.map((espaco) => (
            <tr key={espaco.id}>
              <th scope="row">{espaco.nome}</th>
              <td>{espaco.tipo_rotulo}</td>
              <td className={estilos.numero}>{espaco.capacidade}</td>
              <td>
                <Etiqueta variante={espaco.ativo ? 'sucesso' : 'neutra'}>
                  {espaco.ativo ? 'Ativo' : 'Inativo'}
                </Etiqueta>
              </td>
              <td>
                <div className={estilos.acoes}>
                  {espaco.ativo && (
                    <Link
                      to={caminhoParaReservar(espaco.id)}
                      aria-label={`Reservar ${espaco.nome}`}
                    >
                      Reservar
                    </Link>
                  )}
                  {gestao && <BotoesDeGestao espaco={espaco} gestao={gestao} />}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function BotoesDeGestao({ espaco, gestao }: { espaco: Espaco; gestao: AcoesDeGestao }) {
  const ativacao = espaco.ativo ? 'Desativar' : 'Reativar'
  return (
    <>
      <button
        type="button"
        className={estilos.acao}
        aria-label={`Editar o espaço ${espaco.nome}`}
        onClick={() => gestao.aoEditar(espaco)}
      >
        Editar
      </button>
      <button
        type="button"
        className={estilos.acao}
        aria-label={`${ativacao} o espaço ${espaco.nome}`}
        onClick={() => gestao.aoAlterarAtivacao(espaco)}
      >
        {ativacao}
      </button>
    </>
  )
}

export default TabelaDeEspacos
