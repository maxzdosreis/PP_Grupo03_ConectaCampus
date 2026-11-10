# US-13 · Cancelar uma reserva

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-13 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-13-cancelar-uma-reserva.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Marca "Depende de" das DECs confirmadas na Aula 7 (DEC-06, DEC-10, DEC-11) com "(decidida)" (GES-02). Nenhum Dado/Quando/Então muda. Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-19 e TA-20 passam a TA-20 e TA-21, e TA-21 a TA-158 passam a TA-24 a TA-161, para os TA-19, TA-22 e TA-23 novos da US-03 (revogação e troca da credencial de renovação) seguirem a ordem das histórias (AUT-09). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-96 a TA-107 passam a TA-97, TA-98, TA-99, TA-102, TA-103, TA-105, TA-106, TA-107, TA-109, TA-110, TA-113 e TA-114, e TA-108 a TA-161 passam a TA-115 a TA-168, para os TAs novos das US-10 e US-11 (consulta em páginas) seguirem a ordem das histórias (RES-10). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Critérios novos: CA-03, CA-04, CA-10 novos, com a implementação pendente na tarefa RES-11 ([CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md)); CA-12, CA-14 novos, com a implementação pendente na tarefa RES-12 ([CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md)). CAs antigos que a regra nova substitui ficam marcados com Situação, sem apagar o texto nem o TA. Renumeração dos TAs: TA-125 a TA-133 passam a TA-137 a TA-149 (e os CAs seguintes na mesma história, quando há CA novo antes deles), para os 25 TAs pendentes novos seguirem a ordem das histórias (REQ-13). A especificação está adiante do código de propósito. Mudança comportamental da especificação nos CAs novos; a renumeração é editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Divisão pelo [CR-05](../mudancas/CR-05-atendente-e-gestor-nos-artefatos-mistos.md) (REQ-13): os CAs do cancelamento pelo Atendente responsável passam para a [US-20](US-20-cancelar-qualquer-reserva.md), com os mesmos TAs, renumerados; a US-13 fica com o Solicitante. CAs e TAs renumerados. Mudança de escopo da história, sem obrigação nova. Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-13 |
| **Título** | Cancelar uma reserva |
| **História** | Como Solicitante, quero cancelar uma reserva minha, com o motivo, para liberar o horário quando eu desistir. |
| **Valor** | O horário volta a aceitar pedidos na hora, sem procurar o setor, e o motivo fica registrado para quem pediu ([NS-10](../visao.md#necessidades), [NS-09](../visao.md#necessidades)). |
| **Origem** | [UC-11 Cancelar reserva](../casos-de-uso/README.md#uc-11): o fluxo comum de [UC-10, passos 1 a 8](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p1), na [variação UC-11](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-11), com UC-12 (motivo) e UC-13 (histórico); alternativa A5.1 e as exceções E2.1, E6.2, E6.5, E6.7 e E7.1, no contexto do cancelamento. |
| **Prioridade** | Normal — [RF-21](../requisitos/rf-reservas.md#rf-21), [RF-23](../requisitos/rf-reservas.md#rf-23) e [RF-24](../requisitos/rf-reservas.md#rf-24) são normais (F4 do enunciado). |
| **Estimativa (Custo em Semanas)** | 0,2 (retrospectiva: a parte do cancelamento da RES-06, da AUT-05 e do diálogo de confirmação da FE-05). |
| **Conversa** | "Pode cancelar depois que o uso já aconteceu?" → o Gestor, não: só antes do início; o Solicitante, sim ([DEC-13](../decisoes/DEC-13.md), decidida na Aula 7). "O cancelamento tentado sem motivo fica registrado?" → sim, se a reserva for visível a quem tentou ([DEC-05](../decisoes/DEC-05.md), decidida na Aula 7; tarefa RES-12). "E o Atendente responsável cancelando qualquer reserva?" → é a [US-20](US-20-cancelar-qualquer-reserva.md) (divisão pelo CR-05). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). Os CAs marcados com implementação pendente só contam quando a tarefa citada os implementar e criar o TA deles. |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Precisa de uma reserva Solicitada ou Confirmada ([US-08](US-08-solicitar-reserva.md), [US-14](US-14-confirmar-uma-reserva.md)) e de uma forma de localizá-la ([US-10](US-10-acompanhar-minhas-reservas.md) a [US-12](US-12-ver-detalhe-e-historico.md)). |
| **N** · Negociável | ✗ | A [DEC-13](../decisoes/DEC-13.md) decidiu que o Solicitante cancela sem restrição de horário; a regra do Atendente responsável está na [US-20](US-20-cancelar-qualquer-reserva.md). |
| **V** · Valiosa | ✓ | Libera o horário para outra pessoa e é a única ação do Solicitante sobre o próprio pedido. |
| **E** · Estimável | ✓ | Reaproveita o fluxo comum de UC-10. |
| **S** · Small | ✓ | Uma transição, com motivo. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado. |

**Diagnóstico:** valiosa, pequena e testável, mas depende das histórias que criam e mostram a reserva, e teve a regra de horário definida pela DEC-13.

## Critérios de aceite

#### <a id="us-13-ca-01"></a>US-13 · CA-01 · O Solicitante cancela a própria reserva (sucesso)

- **Dado** uma reserva Solicitada (ou Confirmada) do Solicitante, das 10:00 às 11:00
- **Quando** ele escolhe cancelá-la e confirma com o motivo "  Não  vou mais  usar "
- **Então** o sistema informa "Reserva cancelada com sucesso.", a reserva passa a Cancelada com o motivo "Não vou mais usar", não oferece mais nenhuma ação, e o período das 10:00 às 11:00 volta a aceitar pedidos
- **Origem:** [UC-10 passos 1 a 8, variação UC-11](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-11)
- **RF:** [RF-21](../requisitos/rf-reservas.md#rf-21)
- **TA:** [TA-137](#ta-137)
- **Depende de:** [DEC-13](../decisoes/DEC-13.md) (decidida na Aula 7; o cancelamento pelo Solicitante não depende do horário)

#### <a id="us-13-ca-02"></a>US-13 · CA-02 · O Solicitante cancela depois do início (sucesso)

- **Dado** uma reserva própria Confirmada cujo início já chegou
- **Quando** o Solicitante a cancela, com motivo
- **Então** a reserva passa a Cancelada, com o motivo (sem mudança, decisão do grupo)
- **Origem:** [UC-10 passos 1 a 8, variação UC-11](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-11)
- **RF:** [RF-21](../requisitos/rf-reservas.md#rf-21)
- **TA:** [TA-138](#ta-138)
- **Depende de:** [DEC-13](../decisoes/DEC-13.md) (decidida na Aula 7; regra aplicada na especificação pelo [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md), REQ-13)
- **Implementação:** implementação pendente (tarefa RES-11)

#### <a id="us-13-ca-03"></a>US-13 · CA-03 · Desistir de cancelar (alternativa)

- **Dado** o pedido de confirmação do cancelamento, com o resumo da reserva e o motivo a preencher
- **Quando** a pessoa desiste em vez de confirmar
- **Então** nada muda nem é registrado: a reserva continua na situação em que estava, e a pessoa volta à lista
- **Origem:** [UC-10 A5.1](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#a5-1)
- **RF:** [RF-21](../requisitos/rf-reservas.md#rf-21), [RF-20](../requisitos/rf-reservas.md#rf-20)
- **TA:** [TA-139](#ta-139)

#### <a id="us-13-ca-04"></a>US-13 · CA-04 · Nada a cancelar numa reserva encerrada (exceção)

- **Dado** uma reserva do Solicitante que já está Concluída
- **Quando** ele a vê na lista ou no detalhe
- **Então** o sistema não oferece cancelar nem nenhuma outra ação, e indica que não há ação disponível
- **Origem:** [UC-10 E2.1](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e2-1)
- **RF:** [RF-16](../requisitos/rf-reservas.md#rf-16), [RF-24](../requisitos/rf-reservas.md#rf-24)
- **TA:** [TA-140](#ta-140)

#### <a id="us-13-ca-05"></a>US-13 · CA-05 · Cancelar uma reserva já encerrada (exceção)

- **Dado** uma reserva Concluída, Recusada ou já Cancelada
- **Quando** alguém pede para cancelá-la mesmo assim (por exemplo, com uma lista antiga)
- **Então** o sistema informa "Não é possível alterar uma reserva Concluída para Cancelada." (com a situação atual), e a reserva continua na situação, com o motivo e o histórico que tinha
- **Origem:** [UC-10 E6.5](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-5)
- **RF:** [RF-24](../requisitos/rf-reservas.md#rf-24)
- **TA:** [TA-141](#ta-141)
- **Situação:** em parte substituído (a cláusula "o mesmo histórico": a tentativa recusada passa a entrar no histórico) por [US-20 · CA-04](US-20-cancelar-qualquer-reserva.md#us-20-ca-04), pelo [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md) (REQ-13). O TA deste CA verifica a regra anterior, que o código ainda cumpre até a tarefa RES-12.

#### <a id="us-13-ca-06"></a>US-13 · CA-06 · Cancelar sem motivo (exceção)

- **Dado** uma reserva Solicitada do Solicitante
- **Quando** ele confirma o cancelamento sem motivo, ou com um motivo só de espaços
- **Então** o sistema informa, junto ao motivo, "Informe o motivo para recusar ou cancelar a reserva.", e a reserva continua Solicitada, ocupando o horário
- **Origem:** [UC-10 E6.7](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-7)
- **RF:** [RF-26](../requisitos/rf-reservas.md#rf-26)
- **TA:** [TA-142](#ta-142)

#### <a id="us-13-ca-07"></a>US-13 · CA-07 · Cancelar sobre uma lista desatualizada (exceção)

- **Dado** uma reserva Solicitada que o Solicitante vê na lista e que o Gestor recusa nesse meio-tempo
- **Quando** o Solicitante confirma o cancelamento sobre a leitura antiga
- **Então** o sistema informa "Esta reserva já está Recusada: ela foi alterada enquanto você decidia. Atualize a lista e tente de novo." e oferece atualizar a lista; vale só a recusa do Gestor, e o histórico não ganha um registro de cancelamento
- **Origem:** [UC-10 E7.1](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e7-1)
- **RF:** [RF-21](../requisitos/rf-reservas.md#rf-21) (a garantia é o [RNF-R04](../requisitos/rnf.md#rnf-r04))
- **TA:** [TA-143](#ta-143)
- **Situação:** ponto aberto do [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md): se a recusa por leitura desatualizada entra no histórico como tentativa fica para a tarefa RES-12 ("a definir na RES-12"). Até lá, este CA vale como está.

#### <a id="us-13-ca-08"></a>US-13 · CA-08 · Cancelamento registrado no histórico (registro)

- **Dado** uma reserva que acabou de ser cancelada pelo Solicitante (CA-01)
- **Quando** o histórico dela é consultado
- **Então** o último registro mostra a situação anterior, "Cancelada por" o nome dele, o momento e o motivo; um cancelamento recusado (CA-05 a CA-07) não gera registro — diferente do modelo do professor, que registra a tentativa
- **Origem:** [UC-10 passo 7](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p7)
- **RF:** [RF-22](../requisitos/rf-reservas.md#rf-22)
- **TA:** [TA-144](#ta-144)
- **Depende de:** [DEC-05](../decisoes/DEC-05.md)
- **Situação:** em parte substituído (a regra das tentativas recusadas) por [US-20 · CA-04](US-20-cancelar-qualquer-reserva.md#us-20-ca-04), pelo [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md) (REQ-13). Este CA e o TA dele descrevem a regra anterior, que o código ainda cumpre até a tarefa RES-12; não valem como prova da regra nova.

#### <a id="us-13-ca-09"></a>US-13 · CA-09 · Reserva de outra pessoa é tratada como inexistente (acesso)

- **Dado** uma reserva Solicitada do Bruno
- **Quando** a Ana, Solicitante, pede para cancelá-la
- **Então** o sistema responde "Reserva de código «n» não encontrada." — a mesma resposta de uma reserva que não existe —, e a reserva do Bruno não muda
- **Origem:** [UC-10 E6.2](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-2)
- **RF:** [RF-23](../requisitos/rf-reservas.md#rf-23)
- **TA:** [TA-145](#ta-145)

#### <a id="us-13-ca-10"></a>US-13 · CA-10 · Reserva de outra pessoa não é registrada (acesso)

- **Dado** uma reserva de outro Solicitante
- **Quando** um Solicitante tenta cancelá-la
- **Então** o sistema informa que a reserva não foi encontrada e o histórico dela não ganha nenhum registro
- **Origem:** [UC-10 E6.2](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-2)
- **RF:** [RF-22](../requisitos/rf-reservas.md#rf-22), [RF-23](../requisitos/rf-reservas.md#rf-23)
- **TA:** [TA-146](#ta-146)
- **Depende de:** [DEC-05](../decisoes/DEC-05.md) (decidida na Aula 7; regra aplicada na especificação pelo [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md), REQ-13)
- **Implementação:** implementação pendente (tarefa RES-12)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-137"></a>TA-137 | [CA-01](#us-13-ca-01) | automatizado | `reservas/tests/test_api_permissoes.py::test_solicitante_cancela_a_propria`; `reservas/tests/test_alterar_situacao.py::test_solicitante_cancela_a_propria_reserva`; `reservas/tests/test_alterar_situacao.py::test_cancelar_guarda_o_motivo_normalizado`; `reservas/tests/test_api_situacao_reserva.py::test_mensagem_de_sucesso_usa_o_rotulo_da_nova_situacao [x]` |
| <a id="ta-138"></a>TA-138 | [CA-02](#us-13-ca-02) | pendente | implementação pendente (tarefa RES-11) — regra já cumprida pelo código; o teste que a fixa depois do início nasce na tarefa ([CR-01 · CA-06](../mudancas/CR-01-situacao-e-horario-da-reserva.md#5-critérios-de-aceite)). |
| <a id="ta-139"></a>TA-139 | [CA-03](#us-13-ca-03) | automatizado | `pages/PaginaReservas.test.tsx`: `"Voltar" fecha sem chamar a API e devolve o foco ao botão da linha`; `pages/PaginaReservas.test.tsx`: `Esc fecha sem chamar a API e devolve o foco ao botão da linha` |
| <a id="ta-140"></a>TA-140 | [CA-04](#us-13-ca-04) | automatizado | `reservas/tests/test_api_permissoes.py::test_solicitante_numa_concluida_nao_tem_acoes`; `components/reservas/TabelaDeReservas.test.tsx`: `sem ações mostra "—" e "Nenhuma ação disponível" para leitor de tela` |
| <a id="ta-141"></a>TA-141 | [CA-05](#us-13-ca-05) | automatizado | `reservas/tests/test_api_situacao_reserva.py::test_reserva_concluida_nao_pode_ser_cancelada`; `reservas/tests/test_reserva.py::test_transicao_proibida_e_recusada_e_preserva_a_situacao [x]`; `reservas/tests/test_reserva.py::test_transicao_proibida_tem_mensagem_com_os_rotulos` |
| <a id="ta-142"></a>TA-142 | [CA-06](#us-13-ca-06) | automatizado | `reservas/tests/test_reserva.py::test_recusar_ou_cancelar_sem_motivo_e_recusado_e_nada_muda [x]`; `reservas/tests/test_alterar_situacao.py::test_recusar_ou_cancelar_sem_motivo_lanca_erro_e_preserva_a_reserva [x]` |
| <a id="ta-143"></a>TA-143 | [CA-07](#us-13-ca-07) | automatizado | `reservas/tests/test_repositorio_reservas.py::test_alteracao_sobre_leitura_desatualizada_e_recusada_sem_gravar`; `reservas/tests/test_reserva.py::test_reserva_desatualizada_vira_409_com_a_situacao_atual`; `pages/PaginaReservas.test.tsx`: `409 mostra o aviso no diálogo com "Atualizar lista", que fecha e recarrega` |
| <a id="ta-144"></a>TA-144 | [CA-08](#us-13-ca-08) | automatizado | `reservas/tests/test_api_historico.py::test_cancelamento_aparece_com_o_motivo`; `reservas/tests/test_api_historico.py::test_tentativa_recusada_nao_aparece_no_historico`; `reservas/tests/test_alterar_situacao.py::test_alteracao_recusada_nao_registra_no_historico` |
| <a id="ta-145"></a>TA-145 | [CA-09](#us-13-ca-09) | automatizado | `reservas/tests/test_api_permissoes.py::test_solicitante_cancelando_a_de_outra_pessoa_responde_404_sem_mudar_nada`; `reservas/tests/test_alterar_situacao.py::test_reserva_de_outra_pessoa_para_o_solicitante_lanca_nao_encontrada` |
| <a id="ta-146"></a>TA-146 | [CA-10](#us-13-ca-10) | pendente | implementação pendente (tarefa RES-12) — TA a criar junto com o código ([CR-02 · CA-03](../mudancas/CR-02-tentativas-recusadas-no-historico.md#5-critérios-de-aceite)). |
