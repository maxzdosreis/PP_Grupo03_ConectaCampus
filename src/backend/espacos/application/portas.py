from typing import Protocol


class ReservasDoEspaco(Protocol):
    """O que o cadastro de espaços precisa saber das reservas (sem importá-las)."""

    def contar_ativas_fora_da_janela(
        self, espaco_id: int, abertura_em_minutos: int, fechamento_em_minutos: int
    ) -> int:
        """Conta as reservas Solicitadas ou Confirmadas, ainda não terminadas, que
        não cabem inteiras na janela diária informada (minutos desde a meia-noite
        local; 1440 é a meia-noite do fim do dia)."""
