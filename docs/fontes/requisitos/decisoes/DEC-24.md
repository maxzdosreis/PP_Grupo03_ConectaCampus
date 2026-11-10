# DEC-24 — A necessidade de ser avisado de mudanças (NS-17) fica fora do 1.0

| Identificação | Responsabilidade |
|---|---|
| **DEC-24 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Decidida pelo grupo em 10/11/2026, na síntese do levantamento (REQ-11). Não depende de resposta do professor: mantém o escopo da [Visão](../visao.md#fora-do-escopo). Nenhum CR. |
| **Pergunta** | A necessidade [NS-17](../visao.md#ns-17) (ficar sabendo que a situação de um pedido próprio mudou, em especial quando um uso confirmado é cancelado) entra no 1.0 ou fica fora dele? |
| **Resposta do professor** | Não perguntada. |
| **Decisão** | **a)** A NS-17 fica registrada na Visão e **fora do 1.0**. O aviso ativo (e-mail, SMS ou aplicativo de mensagens) segue no fora do escopo "Notificações" da Visão. **b)** O Solicitante continua acompanhando a situação do pedido consultando o sistema ([NS-07](../visao.md#ns-07), [RF-13](../requisitos/rf-reservas.md#rf-13) e [RF-14](../requisitos/rf-reservas.md#rf-14)); isso atende a NS-17 só em parte. **c)** Nenhum RF, UC, US, CA, TA nem código muda. A NS-17 fica sem RF derivado até a REQ-13. **d)** O item "Bloqueio de períodos para manutenção ou eventos da instituição" (ACH-19) **continua fora do escopo**, sem NS própria; a evidência fica na [síntese do levantamento](../levantamento/sintese-do-levantamento.md) como motivo para reavaliá-lo com um cliente real. |
| **Motivo** | A necessidade apareceu nas duas técnicas: 8 de 18 respondentes do questionário marcaram "ser avisado se algo mudar" ([QST-01-P09](../levantamento/questionario/QST-01-resultados.md#3-resultados-por-pergunta)) e a [ENT-03](../levantamento/entrevistas/ENT-03-solicitante-servidor-simulada.md) (P04) relatou um uso cancelado na véspera. Por isso merece registro. Mas o aviso ativo exigiria um canal de envio, que a Visão deixa fora do escopo, e as seis funcionalidades mínimas e o prazo de 20/11/2026 têm prioridade ([R-01](../visao.md#riscos)). |
| **Achados** | ACH-16 (NS-17) e ACH-19 (bloqueio de períodos), da [síntese do levantamento](../levantamento/sintese-do-levantamento.md#2-achados-e-destinos). |
| **Alternativas** | **e)** NS-17 entra no 1.0: exigiria o CR-05, um RF novo, um canal de aviso e casos de uso e histórias novos, com risco para o prazo. **f)** Não registrar a NS-17: o achado ficaria só como "fora do escopo" e a necessidade se perderia. **g)** Registrar também uma NS-18 para o bloqueio de períodos: descartada, porque só as entrevistas citam o tema e o questionário não. |
| **Responsável** | Max Zimmermann dos Reis (grupo). |
| **Prazo** | Decidida em 10/11/2026. |
| **Artefatos afetados** | [Visão](../visao.md) (NS-17 e a auditoria das necessidades); [síntese do levantamento](../levantamento/sintese-do-levantamento.md). A NS-17 não tem RF: a REQ-13 decide se cria um RF ou se a verificação NS ↔ RF passa a reconhecer necessidade fora do 1.0. · **REQ-06:** nenhuma história depende desta decisão; 0 critérios de aceite e 0 testes de aceite a rever ([mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-24)). |
| **Origem** | Levantamento (REQ-11): [QST-01](../levantamento/questionario/QST-01-resultados.md) e [ENT-03](../levantamento/entrevistas/ENT-03-solicitante-servidor-simulada.md). |
| **Observações** | Se o grupo trouxer a NS-17 para o 1.0, abre-se o CR-05 pelo [modelo de CR](../mudancas/modelo-cr.md) e esta DEC passa a **Substituída** por uma nova. |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Criação e decisão do grupo, a partir da síntese do levantamento (REQ-11). |
