# US-20 · Cancelar qualquer reserva

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-20 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-20-cancelar-qualquer-reserva.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05). Nasceu da divisão da [US-13](US-13-cancelar-uma-reserva.md) pelo [CR-05](../mudancas/CR-05-atendente-e-gestor-nos-artefatos-mistos.md) (REQ-13): a US-13 ficou com o Solicitante; esta é do Atendente responsável.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Criação pela divisão da US-13 (CR-05, REQ-13): os critérios do cancelamento pelo Atendente responsável (os CAs de cancelar qualquer reserva, só antes do início, a recusa depois do início, e a tentativa de cancelar uma Concluída no histórico) saem da US-13 com os mesmos TAs, renumerados. Nenhuma obrigação nova. Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-20 |
| **Título** | Cancelar qualquer reserva |
| **História** | Como Atendente responsável, quero cancelar qualquer reserva, com o motivo, para desfazer um uso que não vai mais acontecer. |
| **Valor** | O horário volta a aceitar pedidos e quem pediu fica sabendo o motivo, mesmo quando o espaço precisa ser interditado ([NS-09](../visao.md#necessidades), [NS-10](../visao.md#necessidades)). |
| **Origem** | [UC-11 Cancelar reserva](../casos-de-uso/README.md#uc-11), pelo Atendente responsável: o fluxo comum de [UC-10, passos 1 a 8](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p1), na [variação UC-11](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-11), com UC-12 (motivo) e UC-13 (histórico); a exceção E6.8 e as outras do cancelamento estão na [US-13](US-13-cancelar-uma-reserva.md). |
| **Prioridade** | Normal — [RF-20](../requisitos/rf-reservas.md#rf-20) é normal (F4 do enunciado). |
| **Estimativa (Custo em Semanas)** | 0,1 (retrospectiva: a parte do Atendente responsável no cancelamento da RES-06). |
| **Conversa** | "Pode cancelar depois do início?" → não, só antes ([DEC-13](../decisoes/DEC-13.md), decidida na Aula 7; tarefa RES-11). "O Atendente precisa cancelar as reservas de um espaço desativado?" → sim, uma a uma, se quiser ([DEC-06](../decisoes/DEC-06.md)). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). Os CAs marcados com implementação pendente só contam quando a tarefa citada os implementar e criar o TA deles. |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Precisa de uma reserva Solicitada ou Confirmada ([US-08](US-08-solicitar-reserva.md), [US-14](US-14-confirmar-uma-reserva.md)) e de uma forma de localizá-la ([US-11](US-11-acompanhar-todas-as-reservas.md), [US-12](US-12-ver-detalhe-e-historico.md)). |
| **N** · Negociável | ✗ | A regra de horário (só antes do início) foi decidida na [DEC-13](../decisoes/DEC-13.md) e não é renegociada só entre o grupo. |
| **V** · Valiosa | ✓ | Desfaz um uso que não vai acontecer e libera o horário para outra pessoa. |
| **E** · Estimável | ✓ | Reaproveita o fluxo comum de UC-10, só com o perfil do Atendente responsável. |
| **S** · Small | ✓ | Uma transição, com motivo, num só perfil. |
| **T** · Testável | ✓ | Os CAs vigentes têm TA automatizado e os novos têm TA pendente da tarefa de código. |

**Diagnóstico:** valiosa, pequena e testável, mas depende das histórias que criam e mostram a reserva.

## Critérios de aceite

#### <a id="us-20-ca-01"></a>US-20 · CA-01 · O Gestor cancela a reserva de qualquer pessoa (sucesso)

- **Dado** uma reserva Confirmada de um Solicitante, num espaço que o Gestor vai interditar
- **Quando** o Gestor a cancela, com motivo
- **Então** a reserva passa a Cancelada com o motivo, o horário é liberado e um novo pedido no mesmo período é aceito
- **Origem:** [UC-10 passos 1 a 8, variação UC-11](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-11)
- **RF:** [RF-20](../requisitos/rf-reservas.md#rf-20)
- **TA:** [TA-190](#ta-190)
- **Depende de:** [DEC-06](../decisoes/DEC-06.md) (decidida; é assim que as reservas de um espaço desativado são desfeitas)
- **Situação:** substituído por [CA-02](#us-20-ca-02), pelo [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md) (REQ-13). Este CA e o TA dele descrevem a regra anterior, que o código ainda cumpre até a tarefa RES-11; não valem como prova da regra nova.

#### <a id="us-20-ca-02"></a>US-20 · CA-02 · O Gestor cancela antes do início a reserva de qualquer pessoa (sucesso)

- **Dado** uma reserva Confirmada de um Solicitante, cujo início ainda não chegou, num espaço que o Gestor vai interditar
- **Quando** o Gestor a cancela, com motivo
- **Então** a reserva passa a Cancelada com o motivo, o horário é liberado e um novo pedido no mesmo período é aceito
- **Origem:** [UC-10 passos 1 a 8, variação UC-11](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-11)
- **RF:** [RF-20](../requisitos/rf-reservas.md#rf-20)
- **TA:** [TA-191](#ta-191)
- **Depende de:** [DEC-13](../decisoes/DEC-13.md) (decidida na Aula 7; regra aplicada na especificação pelo [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md), REQ-13); [DEC-06](../decisoes/DEC-06.md) (decidida; é assim que as reservas de um espaço desativado são desfeitas)
- **Implementação:** implementação pendente (tarefa RES-11)

#### <a id="us-20-ca-03"></a>US-20 · CA-03 · Cancelar pelo Gestor depois do início (exceção)

- **Dado** uma reserva Confirmada cujo início já chegou
- **Quando** o Gestor tenta cancelá-la, com motivo
- **Então** o sistema recusa, informa que só é possível cancelar antes do início e a reserva continua Confirmada
- **Origem:** [UC-10 E6.8](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-8)
- **RF:** [RF-24.1](../requisitos/rf-reservas.md#rf-24-1)
- **TA:** [TA-192](#ta-192)
- **Depende de:** [DEC-13](../decisoes/DEC-13.md) (decidida na Aula 7; regra aplicada na especificação pelo [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md), REQ-13)
- **Implementação:** implementação pendente (tarefa RES-11)

#### <a id="us-20-ca-04"></a>US-20 · CA-04 · Cancelamento recusado fica no histórico (registro)

- **Dado** uma reserva Concluída
- **Quando** o Gestor tenta cancelá-la, com motivo
- **Então** o sistema recusa, a reserva continua Concluída e o histórico mostra a tentativa com o código do erro da transição não permitida
- **Origem:** [UC-10 passo 7](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p7), [UC-10 E6.5](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-5)
- **RF:** [RF-22](../requisitos/rf-reservas.md#rf-22), [RF-24](../requisitos/rf-reservas.md#rf-24)
- **TA:** [TA-193](#ta-193)
- **Depende de:** [DEC-05](../decisoes/DEC-05.md) (decidida na Aula 7; regra aplicada na especificação pelo [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md), REQ-13)
- **Implementação:** implementação pendente (tarefa RES-12)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-190"></a>TA-190 | [CA-01](#us-20-ca-01) | automatizado | `reservas/tests/test_api_situacao_reserva.py::test_cancelar_libera_o_horario_para_nova_reserva`; `reservas/tests/test_alterar_situacao.py::test_transicao_permitida_e_persistida [x]` |
| <a id="ta-191"></a>TA-191 | [CA-02](#us-20-ca-02) | pendente | implementação pendente (tarefa RES-11) — TA a criar junto com o código ([CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md#4-diferença) (seção 4, o "depois")). |
| <a id="ta-192"></a>TA-192 | [CA-03](#us-20-ca-03) | pendente | implementação pendente (tarefa RES-11) — TA a criar junto com o código ([CR-01 · CA-04](../mudancas/CR-01-situacao-e-horario-da-reserva.md#5-critérios-de-aceite)). |
| <a id="ta-193"></a>TA-193 | [CA-04](#us-20-ca-04) | pendente | implementação pendente (tarefa RES-12) — TA a criar junto com o código ([CR-02 · CA-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md#5-critérios-de-aceite)). |
