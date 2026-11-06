# DEC-11 — Períodos ocupados por outras pessoas na agenda do dia

| Identificação | Responsabilidade |
|---|---|
| **DEC-11 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Decidida. Resposta do professor na Aula 7 (06/11/2026), que confirma a opção já implementada; nenhum CR. |
| **Pergunta** | Um Solicitante pode ver, antes de pedir, os períodos de um espaço já ocupados por reservas de outras pessoas? Com quais dados? |
| **Resposta do professor** | "É isso aí mesmo, está bom assim." |
| **Decisão** | **a)** Sim. A [agenda do dia](../glossario.md#agenda-do-dia) mostra a qualquer usuário identificado o início, o término e a situação de cada [horário ocupado](../glossario.md#horario-ocupado), nunca quem pediu, a finalidade nem o motivo. Fora da agenda, a reserva de outra pessoa continua inexistente para o Solicitante. |
| **Motivo** | Sem a agenda, o Solicitante só descobre o conflito ao enviar o pedido. A mensagem de conflito já mostrava o horário e a situação da reserva que ocupa o período; a agenda mostra o mesmo dado antes, sem acrescentar dados pessoais. |
| **Alternativas** | **b)** Não mostrar: o conflito só aparece na recusa do pedido. **c)** Mostrar só "ocupado", sem a situação. **d)** Mostrar também quem reservou. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor como representante do cliente. |
| **Prazo** | Decidida em 06/11/2026. |
| **Artefatos afetados** | `OcupacaoDoDia` e `HorarioOcupado` (`reservas/application/ocupacao_do_dia.py`); `ConsultarOcupacaoDoDia`; `GET /api/reservas/ocupacao/`; mensagem de `ConflitoDeHorario`; `AgendaDoDia` (frontend); [matriz de acesso](../../matriz_de_acesso.md); [Visão](../visao.md) (NS-05, NS-14, R-14); fichas de [UC-04](../casos-de-uso/UC-04-solicitar-reserva.md#a3-1) (A3.1) e de [UC-06](../casos-de-uso/fichas-resumidas.md#uc-06) (REQ-04). · **REQ-06:** histórias [US-09](../historias/US-09-ver-a-agenda-do-dia.md); 5 critérios de aceite e 5 testes de aceite ([mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-11)). |
| **Origem** | FE-07, decisão a (exceção à regra de visibilidade da AUT-05, decisão f). |
| **Observações** | ID novo: decisão de privacidade encontrada na revisão das tarefas, sem DEC proposta no `CLAUDE.md`. |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Registro da decisão tomada na FE-07 (REQ-01). |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as fichas de caso de uso que dependem desta decisão (REQ-04). |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as histórias e o número de critérios e testes de aceite, a partir do [mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-11) (REQ-06). Estado e opção sem mudança. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Decidida na Aula 7: resposta do professor registrada, confirmando a opção adotada (que passa ao campo Decisão); nenhum CR (GES-02). |
