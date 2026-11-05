# DEC-13 — Mudança de situação em relação ao horário da reserva

| Identificação | Responsabilidade |
|---|---|
| **DEC-13 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Adotada provisoriamente (o código já implementa a opção a; falta a confirmação). |
| **Pergunta** | A mudança de situação deve depender do horário da reserva? Em especial: (1) o Gestor pode [concluir](../glossario.md#concluida) uma reserva cujo término ainda não chegou? (2) pode [confirmar](../glossario.md#confirmada) ou [recusar](../glossario.md#recusada) uma reserva cujo início já passou? (3) o Solicitante ou o Gestor podem [cancelar](../glossario.md#cancelada) depois do início? (4) o que acontece com uma reserva [Solicitada](../glossario.md#solicitada) que ninguém decidiu até a data dela passar? |
| **Opção adotada hoje** | **a)** A mudança não depende do horário. Valem só a [tabela de transições](../glossario.md#transicao-de-situacao), o [perfil](../glossario.md#perfil) e o [motivo](../glossario.md#motivo). Uma Solicitada não decidida continua Solicitada (e continua sendo [reserva que ocupa horário](../glossario.md#reserva-que-ocupa-horario)) depois da data. O momento da mudança só é usado para o [registro de situação](../glossario.md#registro-de-situacao). |
| **Motivo** | Achado ao escrever o [RF-19](../requisitos/rf-reservas.md#rf-19) na REQ-02: a NS-09 fala em "registrar que o uso aprovado aconteceu", o que sugere concluir só depois do término, mas o sistema aceita concluir a qualquer momento. Nenhuma tarefa anterior tratou o assunto; a resposta depende das regras de uso da instituição. |
| **Alternativas** | **b)** Concluir só depois do término; confirmar e recusar só antes do início; cancelar só antes do início. **c)** Como b, e as Solicitadas não decididas passam a não ocupar horário depois da data (ou são recusadas automaticamente). **d)** Só a regra de concluir (b1), mantendo as demais livres. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor como representante do cliente. |
| **Prazo sugerido** | 06/11/2026 (Aula 7). |
| **Artefatos afetados** | `Reserva.alterar_situacao` (`reservas/domain/reserva.py`); [RF-17](../requisitos/rf-reservas.md#rf-17), [RF-18](../requisitos/rf-reservas.md#rf-18), [RF-19](../requisitos/rf-reservas.md#rf-19), [RF-20](../requisitos/rf-reservas.md#rf-20), [RF-21](../requisitos/rf-reservas.md#rf-21) e [RF-16](../requisitos/rf-reservas.md#rf-16) (ações disponíveis); [Visão](../visao.md) (NS-09); máquina de estados da reserva nos testes; dados de exemplo (a Concluída); ficha de [UC-10](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#questões-em-aberto) (onde nasceriam as exceções novas) e [UC-04](../casos-de-uso/UC-04-solicitar-reserva.md#e9-1) (E9.1) (REQ-04). · **REQ-06:** histórias [US-07](../historias/US-07-desativar-e-reativar-espaco.md), [US-08](../historias/US-08-solicitar-reserva.md), [US-10](../historias/US-10-acompanhar-minhas-reservas.md), [US-11](../historias/US-11-acompanhar-todas-as-reservas.md), [US-12](../historias/US-12-ver-detalhe-e-historico.md), [US-13](../historias/US-13-cancelar-uma-reserva.md), [US-14](../historias/US-14-confirmar-uma-reserva.md), [US-15](../historias/US-15-recusar-uma-reserva.md), [US-16](../historias/US-16-concluir-uma-reserva.md); 21 critérios de aceite e 21 testes de aceite ([mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-13)). |
| **Origem** | REQ-02 (SRS), lacuna L-01. |
| **Observações** | Qualquer opção diferente de a) é mudança comportamental e passa por CR com regressão dos testes de transição. Os dados de exemplo já concluem a reserva depois do término, então continuam válidos em b). |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Registro da pergunta encontrada na REQ-02. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as fichas de caso de uso que dependem desta decisão (REQ-04). |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as histórias e o número de critérios e testes de aceite, a partir do [mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-13) (REQ-06). Estado e opção sem mudança. |
