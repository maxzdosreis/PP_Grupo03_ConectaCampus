# US-23 · Consultar a fila de pendentes e as contagens

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-23 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-23-consultar-a-fila-de-pendentes.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 25/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, oito critérios e testes de aceite (TA-209 a TA-216), a partir do [CR-09](../mudancas/CR-09-fila-de-pendentes-e-contagens.md) (RDS-08). Mudança posterior à entrega de 13/11/2026. Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-23 |
| **Título** | Consultar a fila de pendentes e as contagens |
| **História** | Como Atendente responsável, quero ver as reservas que esperam a minha decisão, da mais antiga para a mais nova, e quantas reservas há em cada situação, para atender os pedidos na ordem em que chegaram e saber o tamanho do trabalho. |
| **Valor** | O Gestor decide primeiro o que está esperando há mais tempo, sem filtrar a lista inteira, e vê de relance quantos pedidos estão abertos ([NS-08](../visao.md#ns-08), [NS-09](../visao.md#ns-09)). |
| **Origem** | [UC-24 Consultar a fila de pendentes e as contagens](../casos-de-uso/README.md#uc-24) ([ficha resumida](../casos-de-uso/fichas-resumidas.md#uc-24)). A decisão sobre cada pendente continua no [UC-10](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md). |
| **Prioridade** | Normal — a classe QFD de [RF-44](../requisitos/rf-reservas.md#rf-44) e [RF-44.1](../requisitos/rf-reservas.md#rf-44-1); a recusa ([RF-44.2](../requisitos/rf-reservas.md#rf-44-2)) é Esperado. |
| **Estimativa (Custo em Semanas)** | 0,3 (retrospectiva: casos de uso, consultas do repositório, duas rotas e a matriz de acesso da RDS-08). |
| **Conversa** | "Isto substitui a lista de reservas?" → não: a lista continua igual, com seus filtros; a fila é só das Solicitadas, na ordem de chegada. "E o Solicitante?" → não vê, porque a fila mostra pedidos de todos. "Se o sistema estiver lento ou com parte dele fora do ar?" → o resultado é o mesmo, só que lido do cadastro. "Tem tela?" → não nesta entrega. |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Só existe depois de [US-02](US-02-entrar-no-sistema.md) (entrar como Gestor) e faz sentido com [US-08](US-08-solicitar-reserva.md), que cria as pendentes. |
| **N** · Negociável | ✓ | O tamanho da página e quais dados cada reserva mostra seguem a consulta de reservas e podem ser combinados. |
| **V** · Valiosa | ✓ | Sem ela, achar o que espera decisão exigiria filtrar e ordenar a lista inteira. |
| **E** · Estimável | ✓ | Comportamento conhecido e já medido no custo retrospectivo. |
| **S** · Small | ✓ | Uma capacidade (acompanhar o que espera decisão), com as recusas dela; a tela e as decisões ficam de fora. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado. |

**Diagnóstico:** pequena, valiosa e testável; só depende de US-02 e US-08.

## Critérios de aceite

#### <a id="us-23-ca-01"></a>US-23 · CA-01 · Ver a fila em ordem de solicitação (sucesso)

- **Dado** um Gestor identificado e reservas Solicitadas, pedidas em momentos diferentes e para horários diferentes, ao lado de reservas em outras situações
- **Quando** ele pede a fila de reservas pendentes
- **Então** o sistema mostra só as reservas Solicitadas, da pedida há mais tempo para a mais recente (e, se foram pedidas no mesmo instante, na ordem em que foram registradas), com os mesmos dados e as ações disponíveis da consulta de reservas, e informa quantas estão pendentes; uma reserva nova entra no fim da fila
- **Origem:** [UC-24 passos 1 e 2](../casos-de-uso/fichas-resumidas.md#uc24-p1)
- **RF:** [RF-44](../requisitos/rf-reservas.md#rf-44)
- **TA:** [TA-209](#ta-209)

#### <a id="us-23-ca-02"></a>US-23 · CA-02 · Ver a contagem por situação (sucesso)

- **Dado** um Gestor identificado, com reservas em algumas das cinco situações
- **Quando** ele pede a contagem de reservas por situação
- **Então** o sistema mostra as cinco situações (Solicitada, Confirmada, Recusada, Cancelada e Concluída), nessa ordem, cada uma com a quantidade de reservas e zero quando não há nenhuma, e o total de reservas; sem nenhuma reserva, as cinco mostram zero
- **Origem:** [UC-24 passos 3 e 4](../casos-de-uso/fichas-resumidas.md#uc24-p3)
- **RF:** [RF-44.1](../requisitos/rf-reservas.md#rf-44-1)
- **TA:** [TA-210](#ta-210)

#### <a id="us-23-ca-03"></a>US-23 · CA-03 · A reserva que sai de Solicitada some da fila (sucesso)

- **Dado** um Gestor identificado e uma reserva Solicitada que aparece na fila
- **Quando** a reserva é confirmada, recusada ou cancelada e o Gestor consulta a fila e a contagem de novo
- **Então** a reserva não aparece mais na fila, a quantidade de pendentes diminui, e a contagem passa a mostrar a reserva na situação nova, sem que nada precise ser refeito
- **Origem:** [UC-24 passo 5](../casos-de-uso/fichas-resumidas.md#uc24-p5)
- **RF:** [RF-44](../requisitos/rf-reservas.md#rf-44), [RF-44.1](../requisitos/rf-reservas.md#rf-44-1)
- **TA:** [TA-211](#ta-211)

#### <a id="us-23-ca-04"></a>US-23 · CA-04 · Passar de página da fila (alternativa)

- **Dado** um Gestor identificado e mais reservas pendentes do que cabem numa página
- **Quando** ele pede outra página, ou uma página depois da última
- **Então** o sistema mostra aquela página da mesma fila, com o mesmo total e o número de páginas; depois da última, mostra a lista vazia, sem erro, com o total certo
- **Origem:** [UC-24 A2.1](../casos-de-uso/fichas-resumidas.md#uc24-a2-1)
- **RF:** [RF-44](../requisitos/rf-reservas.md#rf-44)
- **TA:** [TA-212](#ta-212)

#### <a id="us-23-ca-05"></a>US-23 · CA-05 · Fila vazia (alternativa)

- **Dado** um Gestor identificado e nenhuma reserva Solicitada
- **Quando** ele pede a fila de reservas pendentes
- **Então** o sistema informa "Nenhuma reserva pendente." e mostra a lista vazia, sem erro; com uma só pendente, informa "1 reserva pendente."
- **Origem:** [UC-24 A2.2](../casos-de-uso/fichas-resumidas.md#uc24-a2-2)
- **RF:** [RF-44](../requisitos/rf-reservas.md#rf-44)
- **TA:** [TA-213](#ta-213)

#### <a id="us-23-ca-06"></a>US-23 · CA-06 · Mesmo resultado quando o apoio de consulta não está disponível (alternativa)

- **Dado** um Gestor identificado e o sistema sem poder usar o seu apoio de consulta, por estar fora do ar ou ainda sem os dados
- **Quando** ele consulta a fila de pendentes e a contagem por situação
- **Então** o sistema responde com sucesso, sem aviso de falha, e a fila e os números são exatamente os mesmos que seriam mostrados com o apoio disponível, inclusive a ordem e o total; a consulta não tenta refazer o apoio
- **Origem:** [UC-24 A4.1](../casos-de-uso/fichas-resumidas.md#uc24-a4-1)
- **RF:** [RF-44](../requisitos/rf-reservas.md#rf-44), [RF-44.1](../requisitos/rf-reservas.md#rf-44-1)
- **TA:** [TA-214](#ta-214)

#### <a id="us-23-ca-07"></a>US-23 · CA-07 · Recusar página ou tamanho inválidos (exceção)

- **Dado** um Gestor identificado
- **Quando** ele pede a fila com uma página que não é um número inteiro a partir de 1, ou um tamanho de página fora de 1 a 100
- **Então** o sistema informa "Verifique os dados informados.", com o campo com problema, e não mostra a fila
- **Origem:** [UC-24 E2.1](../casos-de-uso/fichas-resumidas.md#uc24-e2-1)
- **RF:** [RF-44.2](../requisitos/rf-reservas.md#rf-44-2)
- **TA:** [TA-215](#ta-215)

#### <a id="us-23-ca-08"></a>US-23 · CA-08 · Recusar quem não é Gestor (acesso)

- **Dado** uma pessoa sem identificação, ou um Solicitante, mesmo com reservas pendentes dele
- **Quando** ela pede a fila de pendentes ou a contagem por situação, com ou sem página válida
- **Então** o sistema pede que a pessoa entre (sem identificação) ou informa que ela não tem permissão (Solicitante), sem mostrar reserva nem número algum; outra forma de pedir (que não seja consultar) é recusada como operação inexistente
- **Origem:** [UC-24 E1.1](../casos-de-uso/fichas-resumidas.md#uc24-e1-1)
- **RF:** [RF-44.2](../requisitos/rf-reservas.md#rf-44-2)
- **TA:** [TA-216](#ta-216)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-209"></a>TA-209 | [CA-01](#us-23-ca-01) | automatizado | `reservas/tests/test_api_fila_de_pendentes.py::test_fila_vem_em_ordem_de_solicitacao_com_o_formato_da_reserva`; `reservas/tests/test_api_fila_de_pendentes.py::test_nova_solicitacao_entra_no_fim_da_fila_sem_reconstruir`; `reservas/tests/test_repositorio_reservas.py::test_listar_pendentes_ordena_por_criada_em_e_nao_por_id_nem_por_horario`; `reservas/tests/test_repositorio_reservas.py::test_listar_pendentes_desempata_pelo_id_com_ids_de_um_e_dois_digitos`; `reservas/tests/test_repositorio_reservas.py::test_listar_pendentes_ignora_as_que_nao_estao_solicitadas`; `reservas/tests/test_fila_de_pendentes.py::test_fila_preserva_a_ordem_de_solicitacao_com_ids_de_um_e_dois_digitos` |
| <a id="ta-210"></a>TA-210 | [CA-02](#us-23-ca-02) | automatizado | `reservas/tests/test_api_fila_de_pendentes.py::test_contagem_traz_as_cinco_situacoes_na_ordem_com_zeros`; `reservas/tests/test_api_fila_de_pendentes.py::test_contagem_sem_reservas_traz_tudo_zerado`; `reservas/tests/test_repositorio_reservas.py::test_contar_por_situacao_sem_reservas_traz_as_cinco_com_zero`; `reservas/tests/test_repositorio_reservas.py::test_contar_por_situacao_conta_cada_situacao`; `reservas/tests/test_fila_de_pendentes.py::test_contagem_traz_as_cinco_situacoes_com_zero` |
| <a id="ta-211"></a>TA-211 | [CA-03](#us-23-ca-03) | automatizado | `reservas/tests/test_api_fila_de_pendentes.py::test_confirmar_pela_api_tira_da_fila_e_muda_a_contagem_sem_reconstruir`; `reservas/tests/test_api_fila_de_pendentes.py::test_projecao_atrasada_nao_mostra_reserva_que_ja_saiu_de_solicitada`; `reservas/tests/test_fila_de_pendentes.py::test_reserva_que_ja_nao_e_solicitada_no_banco_some_da_pagina`; `reservas/tests/test_fila_de_pendentes.py::test_pagina_cheia_com_id_velho_traz_as_proximas_pendentes_e_o_total_certo`; `reservas/tests/test_fila_de_pendentes.py::test_id_do_indice_que_nao_existe_no_banco_cai_para_o_repositorio` |
| <a id="ta-212"></a>TA-212 | [CA-04](#us-23-ca-04) | automatizado | `reservas/tests/test_api_fila_de_pendentes.py::test_fila_pagina_e_depois_da_ultima_vem_vazia_com_o_total`; `reservas/tests/test_repositorio_reservas.py::test_listar_pendentes_pagina_e_a_ultima_pagina_vem_com_o_resto`; `reservas/tests/test_repositorio_reservas.py::test_listar_pendentes_depois_da_ultima_pagina_vem_vazio_com_o_total`; `reservas/tests/test_fila_de_pendentes.py::test_fila_pagina_e_depois_da_ultima_vem_vazia_com_o_total_certo` |
| <a id="ta-213"></a>TA-213 | [CA-05](#us-23-ca-05) | automatizado | `reservas/tests/test_api_fila_de_pendentes.py::test_fila_vazia_diz_que_nao_ha_pendentes`; `reservas/tests/test_api_fila_de_pendentes.py::test_fila_com_uma_reserva_usa_o_singular`; `reservas/tests/test_repositorio_reservas.py::test_listar_pendentes_sem_reservas_vem_vazio`; `reservas/tests/test_fila_de_pendentes.py::test_fila_vazia_com_o_indice_montado` |
| <a id="ta-214"></a>TA-214 | [CA-06](#us-23-ca-06) | automatizado | `reservas/tests/test_api_fila_de_pendentes.py::test_resposta_com_a_projecao_montada_e_a_do_banco_sao_iguais`; `reservas/tests/test_api_fila_de_pendentes.py::test_resposta_com_a_projecao_fora_do_ar_e_a_mesma_e_nunca_503`; `reservas/tests/test_api_fila_de_pendentes.py::test_ler_a_fila_nao_repovoa_a_projecao`; `reservas/tests/test_fila_de_pendentes.py::test_fila_e_igual_com_o_indice_montado_sem_indice_ou_indisponivel [x]`; `reservas/tests/test_fila_de_pendentes.py::test_fila_com_indice_indisponivel_cai_para_o_repositorio_sem_erro`; `reservas/tests/test_fila_de_pendentes.py::test_contagem_sem_indice_ou_com_indice_indisponivel_cai_para_o_repositorio [x]` |
| <a id="ta-215"></a>TA-215 | [CA-07](#us-23-ca-07) | automatizado | `reservas/tests/test_api_fila_de_pendentes.py::test_parametro_invalido_recebe_400_com_o_campo [x]` |
| <a id="ta-216"></a>TA-216 | [CA-08](#us-23-ca-08) | automatizado | `reservas/tests/test_api_fila_de_pendentes.py::test_anonimo_recebe_401 [x]`; `reservas/tests/test_api_fila_de_pendentes.py::test_solicitante_recebe_403_mesmo_com_reservas_proprias [x]`; `reservas/tests/test_api_fila_de_pendentes.py::test_solicitante_com_parametro_invalido_recebe_403_e_nao_400`; `reservas/tests/test_api_fila_de_pendentes.py::test_outros_metodos_recebem_405 [x]`; `reservas/tests/test_fila_de_pendentes.py::test_solicitante_nao_consulta_a_fila`; `reservas/tests/test_fila_de_pendentes.py::test_solicitante_nao_consulta_a_contagem`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]` |
