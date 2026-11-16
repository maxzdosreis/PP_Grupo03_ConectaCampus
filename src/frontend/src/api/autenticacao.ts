import { requisitar } from './cliente.ts'

export type Usuario = {
  id: number
  nome: string
  email: string
  matricula: string
  perfil: string
  perfil_rotulo: string
  eh_gestor: boolean
}

export type DadosDeLogin = {
  email: string
  senha: string
}

export type DadosDeCadastro = {
  nome: string
  matricula: string
  email: string
  senha: string
}

export type RespostaDoLogin = {
  access: string
  refresh: string
  usuario: Usuario
}

export function entrar(dados: DadosDeLogin) {
  return requisitar<RespostaDoLogin>('/auth/login/', {
    method: 'POST',
    body: JSON.stringify(dados),
    autenticar: false,
  })
}

export function cadastrar(dados: DadosDeCadastro) {
  return requisitar<Usuario>('/auth/cadastro/', {
    method: 'POST',
    body: JSON.stringify(dados),
    autenticar: false,
  })
}

export function sair(refresh: string) {
  return requisitar<null>('/auth/logout/', {
    method: 'POST',
    body: JSON.stringify({ refresh }),
    autenticar: false,
  })
}

export type DadosDaTrocaDeSenha = {
  senha_atual: string
  nova_senha: string
  refresh_atual?: string
}

export function alterarSenha(dados: DadosDaTrocaDeSenha) {
  return requisitar<null>('/auth/senha/', {
    method: 'POST',
    body: JSON.stringify(dados),
  })
}

export function usuarioAtual() {
  return requisitar<Usuario>('/auth/me/')
}
