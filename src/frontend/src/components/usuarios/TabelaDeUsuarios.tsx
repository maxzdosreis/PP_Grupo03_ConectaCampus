import { useId, type Ref } from 'react'
import type { UsuarioGerenciado } from '../../api/usuarios.ts'
import { formatarDataHora } from '../../formatacao.ts'
import { BotaoDeIcone } from '../botao/Botao.tsx'
import Etiqueta from '../etiqueta/Etiqueta.tsx'
import {
  acaoDePerfil,
  acaoDeSituacao,
  ROTULOS_DAS_ACOES,
  type AcaoDeUsuario,
} from './acoesDeUsuario.ts'
import estilos from './TabelaDeUsuarios.module.css'

type PropriedadesDaTabela = {
  usuarios: UsuarioGerenciado[]
  legenda: string
  idDoUsuarioLogado: number | null
  aoEscolherAcao: (usuario: UsuarioGerenciado, acao: AcaoDeUsuario) => void
  ref?: Ref<HTMLDivElement>
}

function TabelaDeUsuarios({
  usuarios,
  legenda,
  idDoUsuarioLogado,
  aoEscolherAcao,
  ref,
}: PropriedadesDaTabela) {
  const idDaLegenda = useId()
  const idDaAjuda = useId()
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
            <th scope="col">E-mail</th>
            <th scope="col">Matrícula</th>
            <th scope="col">Perfil</th>
            <th scope="col">Situação</th>
            <th scope="col">Último acesso</th>
            <th scope="col">Ações</th>
          </tr>
        </thead>
        <tbody>
          {usuarios.map((usuario) => {
            const ehOProprio = usuario.id === idDoUsuarioLogado
            const idDaAjudaDaLinha = `${idDaAjuda}-${usuario.id}`
            return (
              <tr key={usuario.id}>
                <th scope="row">
                  {usuario.nome}
                  {ehOProprio && ' (você)'}
                </th>
                <td>{usuario.email}</td>
                <td>{usuario.matricula}</td>
                <td>
                  <Etiqueta variante={usuario.eh_gestor ? 'aviso' : 'neutra'}>
                    {usuario.perfil_rotulo}
                  </Etiqueta>
                </td>
                <td>
                  <Etiqueta variante={usuario.ativo ? 'sucesso' : 'neutra'}>
                    {usuario.ativo ? 'Ativo' : 'Inativo'}
                  </Etiqueta>
                </td>
                <td>{usuario.ultimo_acesso ? formatarDataHora(usuario.ultimo_acesso) : '—'}</td>
                <td>
                  <div className={estilos.acoes}>
                    {[acaoDePerfil(usuario), acaoDeSituacao(usuario)].map((acao) => (
                      <BotaoDeIcone
                        key={acao}
                        acao={acao}
                        rotulo={`${ROTULOS_DAS_ACOES[acao]}: ${usuario.nome}`}
                        aria-describedby={ehOProprio ? idDaAjudaDaLinha : undefined}
                        disabled={ehOProprio && (acao === 'rebaixar' || acao === 'desativar')}
                        onClick={() => aoEscolherAcao(usuario, acao)}
                      />
                    ))}
                  </div>
                  {ehOProprio && (
                    <p id={idDaAjudaDaLinha} className={estilos.ajuda}>
                      Você não pode rebaixar nem desativar a sua própria conta. Peça a outro
                      Gestor.
                    </p>
                  )}
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

export default TabelaDeUsuarios
