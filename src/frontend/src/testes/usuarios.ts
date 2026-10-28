import type { Usuario } from '../api/autenticacao.ts'

export const USUARIO_GESTOR: Usuario = {
  id: 1,
  nome: 'Carla Mendes',
  email: 'carla.mendes@exemplo.com',
  matricula: '2026900',
  perfil: 'GESTOR',
  perfil_rotulo: 'Gestor',
  eh_gestor: true,
}

export const USUARIO_SOLICITANTE: Usuario = {
  id: 2,
  nome: 'Bruno Lima',
  email: 'bruno.lima@exemplo.com',
  matricula: '2026101',
  perfil: 'SOLICITANTE',
  perfil_rotulo: 'Solicitante',
  eh_gestor: false,
}
