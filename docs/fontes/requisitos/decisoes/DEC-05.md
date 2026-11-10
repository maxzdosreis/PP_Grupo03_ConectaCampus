# DEC-05 — Histórico só com mudanças efetivas

| Identificação | Responsabilidade |
|---|---|
| **DEC-05 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Decidida. Resposta do professor na Aula 7 (06/11/2026); a resposta muda o comportamento implementado e segue pelo [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md). |
| **Pergunta** | Uma tentativa recusada de mudar a situação de uma reserva (perfil sem permissão, transição não permitida, motivo ausente) precisa ficar registrada? Se sim, onde e quem a consulta? |
| **Opção implementada até o CR-02** | **a)** Não registrar. O [histórico](../glossario.md#historico) guarda só a criação e as mudanças aceitas. Uma recusa não altera a reserva e não gera [registro de situação](../glossario.md#registro-de-situacao). |
| **Resposta do professor** | "Deve ficar registrado sim, para ter o histórico completo da reserva." |
| **Decisão do grupo** | As tentativas recusadas entram no próprio histórico da reserva (não num log separado), com ator, momento, situação pedida, resultado e código do erro. Só se registram tentativas sobre uma reserva visível ao ator: a de outro Solicitante continua "não encontrada" e não é registrada, para não revelar a reserva. |
| **Decisão** | Toda tentativa recusada de mudar a situação de uma reserva visível ao ator fica no histórico dessa reserva, com ator, momento, situação pedida, resultado e código do erro, sem mudar a situação. |
| **Implementação** | [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md), tarefa RES-12. Até ela, o código continua com a opção a. |
| **Motivo** | O histórico é o registro de negócio da reserva; uma recusa não muda nada nela. O modelo de critério de aceite do professor (CA-04: "tentativa registrada com data, ator e resultado", A3·s23–24) fica atendido só em parte. |
| **Alternativas** | **b)** Registrar só em log técnico, sem tela, consultado pela Equipe de TI. **c)** Registrar no histórico de negócio também as recusas, com o resultado, visíveis na linha do tempo. A decisão é a c, com a restrição da reserva visível ao ator. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor. |
| **Prazo** | Decidida em 06/11/2026. |
| **Artefatos afetados** | `RegistroDeSituacao` e `Reserva.alterar_situacao` (`reservas/domain/`); `RepositorioReservas` e a tabela do histórico; `GET /api/reservas/{id}/historico/`; linha do tempo do detalhe da reserva; README ("Limitações conhecidas"); caso de uso e critérios de aceite de "Alterar situação" (REQ-03/REQ-04); [Visão](../visao.md) (NS-12, R-08); `docs/fontes/testes_de_reservas.md`; fichas de [UC-10](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#questões-em-aberto) (garantia mínima) e de [UC-09](../casos-de-uso/fichas-resumidas.md#uc-09) (REQ-04). · **REQ-06:** histórias [US-08](../historias/US-08-solicitar-reserva.md), [US-12](../historias/US-12-ver-detalhe-e-historico.md), [US-13](../historias/US-13-cancelar-uma-reserva.md), [US-14](../historias/US-14-confirmar-uma-reserva.md), [US-15](../historias/US-15-recusar-uma-reserva.md), [US-16](../historias/US-16-concluir-uma-reserva.md), [US-20](../historias/US-20-cancelar-qualquer-reserva.md); 15 critérios de aceite e 15 testes de aceite ([mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-05)). |
| **Origem** | RES-07, decisão c ("proposta DEC-05" no `CLAUDE.md`). |
| **Observações** | Mudança comportamental: muda o significado do histórico. O [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md) traz o impacto e o aceite, e a RES-12 aplica o CR (RF, UC, CAs e código) no mesmo PR. |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Registro da decisão proposta na RES-07 (REQ-01). |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as fichas de caso de uso que dependem desta decisão (REQ-04). |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as histórias e o número de critérios e testes de aceite, a partir do [mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-05) (REQ-06). Estado e opção sem mudança. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Decidida na Aula 7: resposta do professor e decisão do grupo registradas; a opção a passa a "implementada até o CR-02"; CR-02 aberto, implementação na RES-12 (GES-02). |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Artefatos afetados com 15 critérios e 15 testes de aceite, depois de aplicar o CR-02 na especificação, com os CAs novos das US-12 a US-14 (REQ-13). Estado e opção sem mudança. Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | US-20 nova (divisão da US-13 pelo CR-05, REQ-13) entre as histórias afetadas. Estado e opção sem mudança. Sem aprovação. |
