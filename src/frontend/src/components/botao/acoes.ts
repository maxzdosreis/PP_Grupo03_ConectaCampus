import {
  ArrowLeft,
  Ban,
  CalendarDays,
  CalendarX,
  CalendarPlus,
  Check,
  CheckCheck,
  ChevronLeft,
  ChevronRight,
  CircleCheck,
  Clock,
  Eye,
  FilterX,
  LayoutList,
  LogIn,
  LogOut,
  Pencil,
  RefreshCw,
  Save,
  Search,
  ShieldCheck,
  ShieldOff,
  UserPlus,
  UserRound,
  Users,
  X,
  Zap,
  type LucideIcon,
} from 'lucide-react'

export type VarianteDeBotao = 'primario' | 'neutro' | 'editar' | 'perigo' | 'confirmar'

export type DefinicaoDaAcao = {
  icone: LucideIcon
  variante: VarianteDeBotao
}

// Um ícone fixo e uma variante por ação, reutilizados em todas as telas.
export const ACOES = {
  editar: { icone: Pencil, variante: 'editar' },
  detalhes: { icone: Eye, variante: 'neutro' },
  reservar: { icone: CalendarPlus, variante: 'primario' },
  confirmar: { icone: Check, variante: 'confirmar' },
  concluir: { icone: CheckCheck, variante: 'confirmar' },
  recusar: { icone: X, variante: 'perigo' },
  cancelar: { icone: CalendarX, variante: 'perigo' },
  desativar: { icone: Ban, variante: 'perigo' },
  reativar: { icone: CircleCheck, variante: 'confirmar' },
  promover: { icone: ShieldCheck, variante: 'primario' },
  rebaixar: { icone: ShieldOff, variante: 'perigo' },
  limpar: { icone: FilterX, variante: 'neutro' },
  filtrar: { icone: Search, variante: 'neutro' },
  atualizar: { icone: RefreshCw, variante: 'neutro' },
  voltar: { icone: ArrowLeft, variante: 'neutro' },
  fechar: { icone: X, variante: 'neutro' },
  anterior: { icone: ChevronLeft, variante: 'neutro' },
  proxima: { icone: ChevronRight, variante: 'neutro' },
  usarHorario: { icone: Clock, variante: 'neutro' },
  salvar: { icone: Save, variante: 'primario' },
  entrar: { icone: LogIn, variante: 'primario' },
  cadastrar: { icone: UserPlus, variante: 'primario' },
  sair: { icone: LogOut, variante: 'neutro' },
  conta: { icone: UserRound, variante: 'neutro' },
  reservas: { icone: CalendarDays, variante: 'neutro' },
  espacos: { icone: LayoutList, variante: 'neutro' },
  usuarios: { icone: Users, variante: 'neutro' },
  generica: { icone: Zap, variante: 'neutro' },
} as const satisfies Record<string, DefinicaoDaAcao>

export type NomeDaAcao = keyof typeof ACOES

const ACAO_POR_SITUACAO: Record<string, NomeDaAcao> = {
  CONFIRMADA: 'confirmar',
  RECUSADA: 'recusar',
  CANCELADA: 'cancelar',
  CONCLUIDA: 'concluir',
}

export function acaoDaSituacao(situacao: string): NomeDaAcao {
  return ACAO_POR_SITUACAO[situacao] ?? 'generica'
}
