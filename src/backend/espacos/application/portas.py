from typing import Protocol

from espacos.domain.espaco_esportivo import EspacoEsportivo


class ReservasDoEspaco(Protocol):
    """O que o cadastro de espaços precisa saber das reservas (sem importá-las)."""

    def contar_ativas_fora_da_janela(
        self, espaco_id: int, abertura_em_minutos: int, fechamento_em_minutos: int
    ) -> int:
        """Conta as reservas Solicitadas ou Confirmadas, ainda não terminadas, que
        não cabem inteiras na janela diária informada (minutos desde a meia-noite
        local; 1440 é a meia-noite do fim do dia)."""


class CacheDeEspacosIndisponivel(Exception):
    """O cache de espaços não pôde ser lido ou gravado.

    Não é erro de domínio e nunca chega à API: quem lê cai para o PostgreSQL e
    quem invalida só registra no log.
    """


class CacheDeEspacos(Protocol):
    """Cópia de leitura dos espaços (RDS-11). Nunca serve a uma decisão."""

    def obter(self, espaco_id: int) -> EspacoEsportivo | None:
        """O espaço guardado, ou None (ausente, vencido ou entrada quebrada)."""

    def versao(self, espaco_id: int) -> int:
        """Versão atual do espaço; a invalidação a avança."""

    def guardar(self, espaco: EspacoEsportivo, *, versao: int) -> bool:
        """Grava só se a versão ainda é a lida; False se alguém invalidou."""

    def invalidar(self, espaco_id: int) -> None:
        """Apaga o espaço guardado e avança a versão, numa operação só."""
