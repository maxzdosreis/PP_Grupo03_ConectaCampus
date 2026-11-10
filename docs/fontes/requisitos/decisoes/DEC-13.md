# DEC-13 — Mudança de situação em relação ao horário da reserva

| Identificação | Responsabilidade |
|---|---|
| **DEC-13 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Decidida. Resposta do professor na Aula 7 (06/11/2026); a resposta muda o comportamento implementado e segue pelo [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md). |
| **Pergunta** | A mudança de situação deve depender do horário da reserva? Em especial: (1) o Gestor pode [concluir](../glossario.md#concluida) uma reserva cujo término ainda não chegou? (2) pode [confirmar](../glossario.md#confirmada) ou [recusar](../glossario.md#recusada) uma reserva cujo início já passou? (3) o Solicitante ou o Gestor podem [cancelar](../glossario.md#cancelada) depois do início? (4) o que acontece com uma reserva [Solicitada](../glossario.md#solicitada) que ninguém decidiu até a data dela passar? |
| **Opção implementada até o CR-01** | **a)** A mudança não depende do horário. Valem só a [tabela de transições](../glossario.md#transicao-de-situacao), o [perfil](../glossario.md#perfil) e o [motivo](../glossario.md#motivo). Uma Solicitada não decidida continua Solicitada (e continua sendo [reserva que ocupa horário](../glossario.md#reserva-que-ocupa-horario)) depois da data. O momento da mudança só é usado para o [registro de situação](../glossario.md#registro-de-situacao). |
| **Resposta do professor** | "Temos que alterar, deve poder concluir somente depois do término, e recusar e cancelar somente antes do início (isso para Gestor)." |
| **Decisão do grupo** | Nos pontos que a resposta não abordou, fica a opção atual: confirmar continua sem restrição de horário; o cancelamento pelo Solicitante continua sem restrição de horário; a Solicitada não decidida continua ocupando o horário depois da data. Nas bordas: concluir vale a partir do instante do término; recusar e cancelar (Gestor) valem só enquanto o início ainda não chegou. |
| **Decisão** | O Gestor só conclui uma reserva a partir do término dela e só recusa ou cancela uma reserva antes do início dela; confirmar, o cancelamento pelo Solicitante e a ocupação do horário pela Solicitada não decidida não dependem do horário. |
| **Implementação** | [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md), tarefa RES-11. Até ela, o código continua com a opção a. |
| **Motivo** | Achado ao escrever o [RF-19](../requisitos/rf-reservas.md#rf-19) na REQ-02: a NS-09 fala em "registrar que o uso aprovado aconteceu", o que sugere concluir só depois do término, mas o sistema aceita concluir a qualquer momento. Nenhuma tarefa anterior tratou o assunto; a resposta depende das regras de uso da instituição. |
| **Alternativas** | **b)** Concluir só depois do término; confirmar e recusar só antes do início; cancelar só antes do início. **c)** Como b, e as Solicitadas não decididas passam a não ocupar horário depois da data (ou são recusadas automaticamente). **d)** Só a regra de concluir (b1), mantendo as demais livres. A decisão não é nenhuma delas por inteiro: fica a parte de b que vale para o Gestor (concluir, recusar e cancelar), sem a restrição de confirmar nem a do Solicitante. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor como representante do cliente. |
| **Prazo** | Decidida em 06/11/2026. |
| **Artefatos afetados** | `Reserva.alterar_situacao` (`reservas/domain/reserva.py`); [RF-17](../requisitos/rf-reservas.md#rf-17), [RF-18](../requisitos/rf-reservas.md#rf-18), [RF-19](../requisitos/rf-reservas.md#rf-19), [RF-20](../requisitos/rf-reservas.md#rf-20), [RF-21](../requisitos/rf-reservas.md#rf-21) e [RF-16](../requisitos/rf-reservas.md#rf-16) (ações disponíveis); [Visão](../visao.md) (NS-09); máquina de estados da reserva nos testes; dados de exemplo (a Concluída); ficha de [UC-10](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#questões-em-aberto) (onde nasceriam as exceções novas) e [UC-04](../casos-de-uso/UC-04-solicitar-reserva.md#e9-1) (E9.1) (REQ-04). · **REQ-06:** histórias [US-07](../historias/US-07-desativar-e-reativar-espaco.md), [US-08](../historias/US-08-solicitar-reserva.md), [US-10](../historias/US-10-acompanhar-minhas-reservas.md), [US-11](../historias/US-11-acompanhar-todas-as-reservas.md), [US-12](../historias/US-12-ver-detalhe-e-historico.md), [US-13](../historias/US-13-cancelar-uma-reserva.md), [US-14](../historias/US-14-confirmar-uma-reserva.md), [US-15](../historias/US-15-recusar-uma-reserva.md), [US-16](../historias/US-16-concluir-uma-reserva.md), [US-20](../historias/US-20-cancelar-qualquer-reserva.md); 31 critérios de aceite e 31 testes de aceite ([mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-13)). |
| **Origem** | REQ-02 (SRS), lacuna L-01. |
| **Observações** | Mudança comportamental: o [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md) traz o mapa de impacto, a diferença antes e depois e os critérios de aceite, e a RES-11 aplica o CR (RF, UC, CAs e código) no mesmo PR. Os dados de exemplo já concluem a reserva depois do término, então continuam válidos. |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Registro da pergunta encontrada na REQ-02. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as fichas de caso de uso que dependem desta decisão (REQ-04). |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as histórias e o número de critérios e testes de aceite, a partir do [mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-13) (REQ-06). Estado e opção sem mudança. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Decidida na Aula 7: resposta do professor e decisão do grupo registradas; a opção a passa a "implementada até o CR-01"; CR-01 aberto, implementação na RES-11 (GES-02). |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Artefatos afetados com 31 critérios e 31 testes de aceite, depois de aplicar o CR-01 na especificação, com os CAs novos das US-13 a US-16 (REQ-13). Estado e opção sem mudança. Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | US-20 nova (divisão da US-13 pelo CR-05, REQ-13) entre as histórias afetadas. Estado e opção sem mudança. Sem aprovação. |
