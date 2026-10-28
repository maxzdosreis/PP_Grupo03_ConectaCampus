from dataclasses import dataclass
from datetime import time

from contas.domain.perfil import PerfilUsuario
from espacos.domain.tipo_espaco import TipoEspaco
from reservas.domain.situacao import SituacaoReserva


@dataclass(frozen=True)
class UsuarioDeExemplo:
    nome: str
    email: str
    matricula: str
    senha: str
    perfil: PerfilUsuario


@dataclass(frozen=True)
class EspacoDeExemplo:
    nome: str
    tipo: TipoEspaco
    capacidade: int
    ativo: bool = True


@dataclass(frozen=True)
class MudancaDeExemplo:
    situacao: SituacaoReserva
    motivo: str | None = None
    ha_dias: int = 0


@dataclass(frozen=True)
class ReservaDeExemplo:
    espaco: str
    solicitante_email: str
    dias_a_partir_de_hoje: int
    hora_inicio: time
    hora_fim: time
    finalidade: str
    mudancas: tuple[MudancaDeExemplo, ...] = ()
    solicitada_ha_dias: int = 0


@dataclass(frozen=True)
class HorarioDeExemplo:
    espaco: str
    dias_a_partir_de_hoje: int
    hora_inicio: time
    hora_fim: time


GESTOR = UsuarioDeExemplo(
    nome="Carla Mendes",
    email="carla.mendes@exemplo.com",
    matricula="2026900",
    senha="Apito-Dourado-48",
    perfil=PerfilUsuario.GESTOR,
)

BRUNO = UsuarioDeExemplo(
    nome="Bruno Lima",
    email="bruno.lima@exemplo.com",
    matricula="2026101",
    senha="Rede-Alta-73",
    perfil=PerfilUsuario.SOLICITANTE,
)

DANIELA = UsuarioDeExemplo(
    nome="Daniela Rocha",
    email="daniela.rocha@exemplo.com",
    matricula="2026102",
    senha="Cesta-Tripla-59",
    perfil=PerfilUsuario.SOLICITANTE,
)

SOLICITANTES = (BRUNO, DANIELA)
USUARIOS = (GESTOR, *SOLICITANTES)

QUADRA_CENTRAL = "Quadra Poliesportiva Central"
CAMPO_PRINCIPAL = "Campo de Futebol Principal"
GINASIO_COBERTO = "Ginásio Coberto"
QUADRA_DE_AREIA = "Quadra de Areia Norte"
QUADRA_DE_TENIS = "Quadra de Tênis 1"

ESPACOS = (
    EspacoDeExemplo(QUADRA_CENTRAL, TipoEspaco.QUADRA_POLIESPORTIVA, 30),
    EspacoDeExemplo(CAMPO_PRINCIPAL, TipoEspaco.CAMPO_DE_FUTEBOL, 22),
    EspacoDeExemplo(GINASIO_COBERTO, TipoEspaco.GINASIO, 200),
    EspacoDeExemplo(QUADRA_DE_AREIA, TipoEspaco.QUADRA_DE_AREIA, 12),
    EspacoDeExemplo(QUADRA_DE_TENIS, TipoEspaco.QUADRA_DE_TENIS, 4),
    EspacoDeExemplo("Quadra de Tênis 2", TipoEspaco.QUADRA_DE_TENIS, 4, ativo=False),
)

RESERVAS = (
    ReservaDeExemplo(
        espaco=QUADRA_CENTRAL,
        solicitante_email=BRUNO.email,
        dias_a_partir_de_hoje=1,
        hora_inicio=time(10, 0),
        hora_fim=time(11, 0),
        finalidade="Treino de vôlei do time da Computação",
    ),
    ReservaDeExemplo(
        espaco=CAMPO_PRINCIPAL,
        solicitante_email=DANIELA.email,
        dias_a_partir_de_hoje=1,
        hora_inicio=time(14, 0),
        hora_fim=time(16, 0),
        finalidade="Partida do campeonato intercursos",
        solicitada_ha_dias=1,
        mudancas=(MudancaDeExemplo(SituacaoReserva.CONFIRMADA),),
    ),
    ReservaDeExemplo(
        espaco=GINASIO_COBERTO,
        solicitante_email=BRUNO.email,
        dias_a_partir_de_hoje=2,
        hora_inicio=time(19, 0),
        hora_fim=time(21, 0),
        finalidade="Festival de basquete",
        solicitada_ha_dias=1,
        mudancas=(
            MudancaDeExemplo(
                SituacaoReserva.RECUSADA,
                motivo="O ginásio estará fechado para um evento institucional.",
            ),
        ),
    ),
    ReservaDeExemplo(
        espaco=QUADRA_DE_AREIA,
        solicitante_email=DANIELA.email,
        dias_a_partir_de_hoje=3,
        hora_inicio=time(8, 0),
        hora_fim=time(9, 0),
        finalidade="Treino de beach tennis",
        solicitada_ha_dias=1,
        mudancas=(
            MudancaDeExemplo(
                SituacaoReserva.CANCELADA, motivo="Previsão de chuva forte."
            ),
        ),
    ),
    ReservaDeExemplo(
        espaco=QUADRA_DE_TENIS,
        solicitante_email=BRUNO.email,
        dias_a_partir_de_hoje=-1,
        hora_inicio=time(18, 0),
        hora_fim=time(19, 30),
        finalidade="Aula de tênis",
        solicitada_ha_dias=3,
        mudancas=(
            MudancaDeExemplo(SituacaoReserva.CONFIRMADA, ha_dias=2),
            MudancaDeExemplo(SituacaoReserva.CONCLUIDA),
        ),
    ),
)

CONFLITO_PARA_DEMONSTRACAO = HorarioDeExemplo(
    espaco=QUADRA_CENTRAL,
    dias_a_partir_de_hoje=1,
    hora_inicio=time(10, 30),
    hora_fim=time(11, 30),
)
