import type { ComponentPropsWithRef, ReactNode } from 'react'
import { Link, type LinkProps } from 'react-router'
import { ACOES, type NomeDaAcao, type VarianteDeBotao } from './acoes.ts'
import estilos from './Botao.module.css'

type PropriedadesVisuais = {
  acao: NomeDaAcao
  variante?: VarianteDeBotao
}

function classes({ acao, variante }: PropriedadesVisuais, soIcone: boolean, extra?: string) {
  return [
    estilos.botao,
    estilos[variante ?? ACOES[acao].variante],
    soIcone && estilos.soIcone,
    extra,
  ]
    .filter(Boolean)
    .join(' ')
}

export function Icone({ acao }: { acao: NomeDaAcao }) {
  const Componente = ACOES[acao].icone
  return <Componente size={20} aria-hidden="true" focusable="false" />
}

type PropriedadesDoBotao = PropriedadesVisuais &
  Omit<ComponentPropsWithRef<'button'>, 'children'> & { children: ReactNode; iconeAoFinal?: boolean }

export function Botao({
  acao,
  variante,
  className,
  children,
  iconeAoFinal = false,
  type = 'button',
  ...resto
}: PropriedadesDoBotao) {
  return (
    <button type={type} className={classes({ acao, variante }, false, className)} {...resto}>
      {!iconeAoFinal && <Icone acao={acao} />}
      {children}
      {iconeAoFinal && <Icone acao={acao} />}
    </button>
  )
}

type PropriedadesDoBotaoDeIcone = PropriedadesVisuais &
  Omit<ComponentPropsWithRef<'button'>, 'children' | 'aria-label'> & { rotulo: string }

export function BotaoDeIcone({
  acao,
  variante,
  rotulo,
  className,
  type = 'button',
  ...resto
}: PropriedadesDoBotaoDeIcone) {
  return (
    <button
      type={type}
      className={classes({ acao, variante }, true, className)}
      aria-label={rotulo}
      data-dica={rotulo}
      {...resto}
    >
      <Icone acao={acao} />
    </button>
  )
}

type PropriedadesDoLinkDeIcone = PropriedadesVisuais &
  Omit<LinkProps, 'children' | 'aria-label'> & { rotulo: string }

export function LinkDeIcone({
  acao,
  variante,
  rotulo,
  className,
  ...resto
}: PropriedadesDoLinkDeIcone) {
  return (
    <Link
      className={classes({ acao, variante }, true, className)}
      aria-label={rotulo}
      data-dica={rotulo}
      {...resto}
    >
      <Icone acao={acao} />
    </Link>
  )
}

type PropriedadesDoLinkBotao = PropriedadesVisuais &
  Omit<LinkProps, 'children'> & { children: ReactNode }

export function LinkBotao({ acao, variante, className, children, ...resto }: PropriedadesDoLinkBotao) {
  return (
    <Link className={classes({ acao, variante }, false, className)} {...resto}>
      <Icone acao={acao} />
      {children}
    </Link>
  )
}
