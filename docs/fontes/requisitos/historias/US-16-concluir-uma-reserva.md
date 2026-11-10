# US-16 · Concluir uma reserva

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-16 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-16-concluir-uma-reserva.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-19 e TA-20 passam a TA-20 e TA-21, e TA-21 a TA-158 passam a TA-24 a TA-161, para os TA-19, TA-22 e TA-23 novos da US-03 (revogação e troca da credencial de renovação) seguirem a ordem das histórias (AUT-09). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-96 a TA-107 passam a TA-97, TA-98, TA-99, TA-102, TA-103, TA-105, TA-106, TA-107, TA-109, TA-110, TA-113 e TA-114, e TA-108 a TA-161 passam a TA-115 a TA-168, para os TAs novos das US-10 e US-11 (consulta em páginas) seguirem a ordem das histórias (RES-10). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Index Card: o papel da história passa a ser Atendente responsável ([DEC-25](../decisoes/DEC-25.md)); meta, valor, critérios e testes de aceite iguais (REQ-12). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Critérios novos: CA-02, CA-04, CA-07 novos, com a implementação pendente na tarefa RES-11 ([CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md)). CAs antigos que a regra nova substitui ficam marcados com Situação, sem apagar o texto nem o TA. Renumeração dos TAs: TA-152 a TA-157 passam a TA-174 a TA-182 (e os CAs seguintes na mesma história, quando há CA novo antes deles), para os 25 TAs pendentes novos seguirem a ordem das histórias (REQ-13). A especificação está adiante do código de propósito. Mudança comportamental da especificação nos CAs novos; a renumeração é editorial, sem nova obrigação. Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-16 |
| **Título** | Concluir uma reserva |
| **História** | Como Atendente responsável, quero marcar como concluída uma reserva confirmada para registrar que o uso aconteceu e encerrar o ciclo dela. |
| **Valor** | A instituição sabe quais usos combinados de fato aconteceram, com quem registrou e quando ([NS-09](../visao.md#necessidades), [NS-12](../visao.md#necessidades)). |
| **Origem** | [UC-19 Concluir reserva](../casos-de-uso/README.md#uc-19): o fluxo comum de [UC-10, passos 1 a 8](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p1), na [variação UC-19](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-19), com UC-13; alternativa A8.1 e as exceções E2.1, E6.4 e E6.5 no contexto da conclusão. |
| **Prioridade** | Normal — [RF-19](../requisitos/rf-reservas.md#rf-19) e [RF-24](../requisitos/rf-reservas.md#rf-24) são normais (F4 do enunciado: o terceiro estado). |
| **Estimativa (Custo em Semanas)** | 0,1 (retrospectiva: a transição Confirmada → Concluída da RES-06, sobre o fluxo comum). |
| **Conversa** | "Pode concluir antes de o horário terminar?" → não, só a partir do término, como a NS-09 pede ("o uso aconteceu"): [DEC-13](../decisoes/DEC-13.md), decidida na Aula 7 (tarefa RES-11), e [L-01](../requisitos/srs.md#l-01). "Uma reserva concluída pode voltar atrás?" → não, é final. |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). Os CAs marcados com implementação pendente só contam quando a tarefa citada os implementar e criar o TA deles. |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Só uma reserva Confirmada pode ser concluída: depende de [US-14](US-14-confirmar-uma-reserva.md). |
| **N** · Negociável | ✗ | O momento em que se pode concluir foi decidido na [DEC-13](../decisoes/DEC-13.md) (a partir do término); a recusa "concluir antes do término" é o CA novo da tarefa RES-11. |
| **V** · Valiosa | ✓ | Fecha o ciclo e libera o horário que sobrou; sem ela, F4 teria só dois estados de chegada. |
| **E** · Estimável | ✓ | Uma transição sobre o fluxo comum. |
| **S** · Small | ✓ | A menor das quatro decisões. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado. |

**Diagnóstico:** pequena, valiosa e testável, mas depende de US-14 e é a história mais exposta à DEC-13, já decidida.

## Critérios de aceite

#### <a id="us-16-ca-01"></a>US-16 · CA-01 · Uso concluído (sucesso)

- **Dado** uma reserva Confirmada e um Gestor identificado
- **Quando** o Gestor escolhe concluí-la e confirma, sem precisar de motivo
- **Então** o sistema informa "Reserva concluída com sucesso.", a reserva passa a Concluída, não oferece mais nenhuma ação e deixa de ocupar o horário
- **Origem:** [UC-10 passos 1 a 8, variação UC-19](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-19)
- **RF:** [RF-19](../requisitos/rf-reservas.md#rf-19)
- **TA:** [TA-170](#ta-170)
- **Depende de:** [DEC-13](../decisoes/DEC-13.md) (decidida na Aula 7; concluir só vale a partir do término: ver a Situação abaixo)
- **Situação:** substituído por [CA-02](#us-16-ca-02), pelo [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md) (REQ-13). Este CA e o TA dele descrevem a regra anterior, que o código ainda cumpre até a tarefa RES-11; não valem como prova da regra nova.

#### <a id="us-16-ca-02"></a>US-16 · CA-02 · Uso concluído a partir do término (sucesso)

- **Dado** uma reserva Confirmada cujo término já chegou (a borda vale: concluir é possível a partir do instante do término) e um Gestor identificado
- **Quando** o Gestor escolhe concluí-la e confirma, sem precisar de motivo
- **Então** o sistema informa "Reserva concluída com sucesso.", a reserva passa a Concluída, não oferece mais nenhuma ação e deixa de ocupar o horário
- **Origem:** [UC-10 passos 1 a 8, variação UC-19](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-19)
- **RF:** [RF-19](../requisitos/rf-reservas.md#rf-19)
- **TA:** [TA-171](#ta-171)
- **Depende de:** [DEC-13](../decisoes/DEC-13.md) (decidida na Aula 7; regra aplicada na especificação pelo [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md), REQ-13)
- **Implementação:** implementação pendente (tarefa RES-11)

#### <a id="us-16-ca-03"></a>US-16 · CA-03 · Motivo opcional ao concluir (alternativa)

- **Dado** uma reserva Confirmada com um motivo da confirmação
- **Quando** o Gestor a conclui informando, ou não, um motivo de até 300 caracteres
- **Então** a reserva fica Concluída com o motivo novo, sem espaços nas pontas nem repetidos, ou sem motivo; o motivo da confirmação deixa de aparecer na reserva e continua no histórico
- **Origem:** [UC-10 A8.1](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#a8-1)
- **RF:** [RF-19](../requisitos/rf-reservas.md#rf-19)
- **TA:** [TA-172](#ta-172)

#### <a id="us-16-ca-04"></a>US-16 · CA-04 · Ações oferecidas conforme o horário (alternativa)

- **Dado** uma reserva Confirmada cujo início já chegou e cujo término ainda não chegou
- **Quando** o Gestor a consulta
- **Então** nem concluir nem cancelar são oferecidos a ele; depois do término, concluir passa a ser oferecido
- **Origem:** [UC-10 passo 2](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p2)
- **RF:** [RF-16](../requisitos/rf-reservas.md#rf-16), [RF-19](../requisitos/rf-reservas.md#rf-19)
- **TA:** [TA-173](#ta-173)
- **Depende de:** [DEC-13](../decisoes/DEC-13.md) (decidida na Aula 7; regra aplicada na especificação pelo [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md), REQ-13)
- **Implementação:** implementação pendente (tarefa RES-11)

#### <a id="us-16-ca-05"></a>US-16 · CA-05 · Nada mais a fazer numa reserva concluída (exceção)

- **Dado** uma reserva Concluída
- **Quando** o Gestor ou o solicitante a veem, e alguém pede para cancelá-la mesmo assim
- **Então** nenhuma ação é oferecida, e o pedido de cancelamento é recusado com "Não é possível alterar uma reserva Concluída para Cancelada."; a reserva continua Concluída
- **Origem:** [UC-10 E2.1](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e2-1)
- **RF:** [RF-16](../requisitos/rf-reservas.md#rf-16), [RF-24](../requisitos/rf-reservas.md#rf-24)
- **TA:** [TA-174](#ta-174)

#### <a id="us-16-ca-06"></a>US-16 · CA-06 · Concluir uma reserva que não foi confirmada (exceção)

- **Dado** uma reserva Solicitada (ainda não confirmada)
- **Quando** o Gestor pede para concluí-la
- **Então** o sistema informa "Não é possível alterar uma reserva Solicitada para Concluída.", e a reserva continua Solicitada, com o mesmo histórico
- **Origem:** [UC-10 E6.5](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-5)
- **RF:** [RF-24](../requisitos/rf-reservas.md#rf-24)
- **TA:** [TA-175](#ta-175)
- **Situação:** em parte substituído (a cláusula "o mesmo histórico": a tentativa recusada passa a entrar no histórico) por [US-20 · CA-04](US-20-cancelar-qualquer-reserva.md#us-20-ca-04), pelo [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md) (REQ-13). O TA deste CA verifica a regra anterior, que o código ainda cumpre até a tarefa RES-12.

#### <a id="us-16-ca-07"></a>US-16 · CA-07 · Concluir antes do término (exceção)

- **Dado** uma reserva Confirmada cujo término ainda não chegou
- **Quando** o Gestor tenta concluí-la
- **Então** o sistema recusa, informa a partir de quando pode concluir (a data e a hora do término) e a reserva continua Confirmada
- **Origem:** [UC-10 E6.8](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-8)
- **RF:** [RF-24.1](../requisitos/rf-reservas.md#rf-24-1)
- **TA:** [TA-176](#ta-176)
- **Depende de:** [DEC-13](../decisoes/DEC-13.md) (decidida na Aula 7; regra aplicada na especificação pelo [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md), REQ-13)
- **Implementação:** implementação pendente (tarefa RES-11)

#### <a id="us-16-ca-08"></a>US-16 · CA-08 · Ciclo completo no histórico (registro)

- **Dado** uma reserva solicitada, confirmada e concluída
- **Quando** o histórico é consultado
- **Então** ele mostra três registros, em ordem — criação (Solicitada), Confirmada e Concluída —, cada um com o autor e o momento, formando um caminho permitido pela tabela de transições; uma conclusão recusada (CA-06, CA-09) não gera registro, diferente do modelo do professor
- **Origem:** [UC-10 passo 7](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p7)
- **RF:** [RF-22](../requisitos/rf-reservas.md#rf-22)
- **TA:** [TA-177](#ta-177)
- **Depende de:** [DEC-05](../decisoes/DEC-05.md)
- **Situação:** em parte substituído (a regra das tentativas recusadas) por [US-14 · CA-12](US-14-confirmar-uma-reserva.md#us-14-ca-12), pelo [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md) (REQ-13). Este CA e o TA dele descrevem a regra anterior, que o código ainda cumpre até a tarefa RES-12; não valem como prova da regra nova.

#### <a id="us-16-ca-09"></a>US-16 · CA-09 · Só o Gestor conclui (acesso)

- **Dado** uma reserva Solicitada do próprio Solicitante
- **Quando** ele pede para concluí-la
- **Então** o sistema informa "Somente o gestor pode concluir reservas.", e não que a transição é inválida: a resposta não revela a situação da reserva, que não muda
- **Origem:** [UC-10 E6.4](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-4)
- **RF:** [RF-27](../requisitos/rf-reservas.md#rf-27)
- **TA:** [TA-178](#ta-178)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-170"></a>TA-170 | [CA-01](#us-16-ca-01) | automatizado | `reservas/tests/test_api_situacao_reserva.py::test_fluxo_da_demonstracao_ate_concluida`; `reservas/tests/test_api_situacao_reserva.py::test_reserva_concluida_nao_traz_acoes`; `reservas/tests/test_alterar_situacao.py::test_ciclo_solicitada_confirmada_concluida`; `reservas/tests/test_conflito_de_horario.py::test_sobreposicao_com_reserva_que_nao_ocupa_horario_e_aceita [x]` |
| <a id="ta-171"></a>TA-171 | [CA-02](#us-16-ca-02) | pendente | implementação pendente (tarefa RES-11) — TA a criar junto com o código ([CR-01 · CA-02](../mudancas/CR-01-situacao-e-horario-da-reserva.md#5-critérios-de-aceite)). |
| <a id="ta-172"></a>TA-172 | [CA-03](#us-16-ca-03) | automatizado | `reservas/tests/test_reserva.py::test_nova_situacao_limpa_o_motivo_da_anterior`; `reservas/tests/test_propriedades_da_reserva.py::TestMaquinaDaReserva` |
| <a id="ta-173"></a>TA-173 | [CA-04](#us-16-ca-04) | pendente | implementação pendente (tarefa RES-11) — TA a criar junto com o código ([CR-01 · CA-05](../mudancas/CR-01-situacao-e-horario-da-reserva.md#5-critérios-de-aceite)). |
| <a id="ta-174"></a>TA-174 | [CA-05](#us-16-ca-05) | automatizado | `reservas/tests/test_api_situacao_reserva.py::test_reserva_concluida_nao_traz_acoes`; `reservas/tests/test_api_situacao_reserva.py::test_reserva_concluida_nao_pode_ser_cancelada`; `reservas/tests/test_api_permissoes.py::test_solicitante_numa_concluida_nao_tem_acoes` |
| <a id="ta-175"></a>TA-175 | [CA-06](#us-16-ca-06) | automatizado | `reservas/tests/test_api_situacao_reserva.py::test_transicao_proibida_responde_409_e_preserva_a_reserva`; `reservas/tests/test_reserva.py::test_transicao_proibida_e_recusada_e_preserva_a_situacao [x]` |
| <a id="ta-176"></a>TA-176 | [CA-07](#us-16-ca-07) | pendente | implementação pendente (tarefa RES-11) — TA a criar junto com o código ([CR-01 · CA-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md#5-critérios-de-aceite)). |
| <a id="ta-177"></a>TA-177 | [CA-08](#us-16-ca-08) | automatizado | `reservas/tests/test_api_historico.py::test_fluxo_completo_aparece_no_historico_em_ordem`; `exemplos/tests/test_carregar_dados_exemplo.py::test_concluida_passou_por_solicitada_e_confirmada_em_dias_diferentes`; `reservas/tests/test_reserva.py::test_alteracao_recusada_nao_muda_nada_nem_registra [x]` |
| <a id="ta-178"></a>TA-178 | [CA-09](#us-16-ca-09) | automatizado | `reservas/tests/test_permissoes_reserva.py::test_solicitante_concluindo_uma_solicitada_recebe_403_e_nao_409` |
