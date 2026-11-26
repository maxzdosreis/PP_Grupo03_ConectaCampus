# US-24 · Consultar o ranking de espaços mais reservados

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-24 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-24-consultar-o-ranking-de-espacos.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 25/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, dez critérios e testes de aceite (TA-217 a TA-226), a partir do [CR-10](../mudancas/CR-10-ranking-de-espacos.md) (RDS-12). Mudança posterior à entrega de 13/11/2026. Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-24 |
| **Título** | Consultar o ranking de espaços mais reservados |
| **História** | Como Atendente responsável, quero ver quais espaços têm mais reservas confirmadas, em ordem, para saber onde está a procura e onde sobra horário. |
| **Valor** | O Gestor enxerga, de relance, os espaços mais usados e os esquecidos, sem montar a conta a partir da lista de reservas ([NS-08](../visao.md#ns-08)). |
| **Origem** | [UC-25 Consultar o ranking de espaços](../casos-de-uso/README.md#uc-25) ([ficha resumida](../casos-de-uso/fichas-resumidas.md#uc-25)). |
| **Prioridade** | Normal — a classe QFD de [RF-45](../requisitos/rf-reservas.md#rf-45); a recusa ([RF-45.1](../requisitos/rf-reservas.md#rf-45-1)) é Esperado. |
| **Estimativa (Custo em Semanas)** | 0,3 (retrospectiva: casos de uso, consulta do repositório, uma rota e a matriz de acesso da RDS-12). |
| **Conversa** | "Conta a reserva que ainda espera decisão?" → não: só conta a que o Gestor aceitou e que não foi cancelada (Confirmada ou Concluída). "De que período?" → de todo o tempo; não há filtro por período. "O Solicitante vê?" → não. "O ranking decide alguma coisa?" → não: é só informação de apoio. "Se parte do sistema estiver fora do ar?" → o resultado é o mesmo. |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Só existe depois de [US-02](US-02-entrar-no-sistema.md) (entrar como Gestor) e faz sentido com [US-14](US-14-confirmar-uma-reserva.md), que cria as reservas confirmadas. |
| **N** · Negociável | ✓ | A quantidade máxima de espaços e o desempate podem ser combinados. |
| **V** · Valiosa | ✓ | Sem ela, achar os espaços mais procurados exigiria contar a lista de reservas à mão. |
| **E** · Estimável | ✓ | Comportamento conhecido e já medido no custo retrospectivo. |
| **S** · Small | ✓ | Uma capacidade (ver o ranking), com as recusas dela; período, gráficos e telas ficam de fora. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado. |

**Diagnóstico:** pequena, valiosa e testável; só depende de US-02 e das decisões sobre reservas.

## Critérios de aceite

#### <a id="us-24-ca-01"></a>US-24 · CA-01 · Ver o ranking em ordem (sucesso)

- **Dado** um Gestor identificado e espaços com quantidades diferentes de reservas Confirmadas ou Concluídas
- **Quando** ele pede o ranking de espaços
- **Então** o sistema mostra os espaços do que tem mais reservas para o que tem menos, cada um com a posição, o código, o nome e o total, e informa quantos espaços estão no ranking; o nome vem do cadastro de espaços, inclusive o de um espaço desativado
- **Origem:** [UC-25 passos 1 e 2](../casos-de-uso/fichas-resumidas.md#uc25-p1)
- **RF:** [RF-45](../requisitos/rf-reservas.md#rf-45)
- **TA:** [TA-217](#ta-217)

#### <a id="us-24-ca-02"></a>US-24 · CA-02 · Empate resolvido pelo código do espaço (sucesso)

- **Dado** um Gestor identificado e dois ou mais espaços com o mesmo total, inclusive códigos de um e de dois algarismos (como 9 e 10) e o empate caindo no limite de espaços pedido
- **Quando** ele pede o ranking
- **Então** os espaços empatados aparecem do menor para o maior código numérico, e o recorte do limite fica com os de menor código
- **Origem:** [UC-25 passo 2](../casos-de-uso/fichas-resumidas.md#uc25-p2)
- **RF:** [RF-45](../requisitos/rf-reservas.md#rf-45)
- **TA:** [TA-218](#ta-218)

#### <a id="us-24-ca-03"></a>US-24 · CA-03 · Só contam as reservas Confirmadas e Concluídas (sucesso)

- **Dado** um Gestor identificado e reservas Solicitadas, Recusadas e Canceladas ao lado de reservas Confirmadas e Concluídas
- **Quando** ele pede o ranking
- **Então** só as Confirmadas e as Concluídas entram na conta, e um espaço sem nenhuma delas não aparece, mesmo que tenha reservas em outras situações
- **Origem:** [UC-25 passo 2](../casos-de-uso/fichas-resumidas.md#uc25-p2)
- **RF:** [RF-45](../requisitos/rf-reservas.md#rf-45)
- **TA:** [TA-219](#ta-219)

#### <a id="us-24-ca-04"></a>US-24 · CA-04 · Confirmada que é concluída conta uma vez (sucesso)

- **Dado** um Gestor identificado e uma reserva Confirmada que já conta no total do espaço
- **Quando** a reserva é concluída e o Gestor consulta o ranking de novo
- **Então** o total do espaço continua o mesmo: a reserva conta uma só vez, e repetir o mesmo pedido de mudança não a conta de novo
- **Origem:** [UC-25 passo 3](../casos-de-uso/fichas-resumidas.md#uc25-p3)
- **RF:** [RF-45](../requisitos/rf-reservas.md#rf-45)
- **TA:** [TA-220](#ta-220)

#### <a id="us-24-ca-05"></a>US-24 · CA-05 · Cancelar uma reserva Confirmada a tira do ranking (sucesso)

- **Dado** um Gestor identificado e uma reserva Confirmada que conta no total do espaço
- **Quando** a reserva é cancelada, com motivo, e o Gestor consulta o ranking de novo, sem que nada seja refeito
- **Então** o total do espaço diminui em um, e o espaço sai do ranking se ficou sem nenhuma reserva que conta
- **Origem:** [UC-25 passo 3](../casos-de-uso/fichas-resumidas.md#uc25-p3)
- **RF:** [RF-45](../requisitos/rf-reservas.md#rf-45)
- **TA:** [TA-221](#ta-221)

#### <a id="us-24-ca-06"></a>US-24 · CA-06 · Escolher quantos espaços ver (alternativa)

- **Dado** um Gestor identificado e mais espaços no ranking do que o pedido
- **Quando** ele pede o ranking com um limite de 1 a 20 espaços, ou sem informar limite
- **Então** o sistema mostra só esse número de espaços, do primeiro para baixo, e, sem limite informado, mostra cinco
- **Origem:** [UC-25 A2.1](../casos-de-uso/fichas-resumidas.md#uc25-a2-1)
- **RF:** [RF-45](../requisitos/rf-reservas.md#rf-45)
- **TA:** [TA-222](#ta-222)

#### <a id="us-24-ca-07"></a>US-24 · CA-07 · Ranking vazio (alternativa)

- **Dado** um Gestor identificado e nenhuma reserva Confirmada ou Concluída
- **Quando** ele pede o ranking
- **Então** o sistema informa "Nenhuma reserva confirmada ainda." e mostra a lista vazia, sem erro; com um só espaço, informa "1 espaço no ranking."
- **Origem:** [UC-25 A2.2](../casos-de-uso/fichas-resumidas.md#uc25-a2-2)
- **RF:** [RF-45](../requisitos/rf-reservas.md#rf-45)
- **TA:** [TA-223](#ta-223)

#### <a id="us-24-ca-08"></a>US-24 · CA-08 · Mesmo resultado quando o apoio de consulta não está disponível (alternativa)

- **Dado** um Gestor identificado e o sistema sem poder usar o seu apoio de consulta, por estar fora do ar ou ainda sem os dados
- **Quando** ele consulta o ranking de espaços
- **Então** o sistema responde com sucesso, sem aviso de falha, e o ranking é exatamente o mesmo que seria mostrado com o apoio disponível, inclusive a ordem e o desempate; a consulta não tenta refazer o apoio
- **Origem:** [UC-25 A3.1](../casos-de-uso/fichas-resumidas.md#uc25-a3-1)
- **RF:** [RF-45](../requisitos/rf-reservas.md#rf-45)
- **TA:** [TA-224](#ta-224)

#### <a id="us-24-ca-09"></a>US-24 · CA-09 · Recusar limite inválido (exceção)

- **Dado** um Gestor identificado
- **Quando** ele pede o ranking com um limite que não é um número inteiro de 1 a 20
- **Então** o sistema informa "Verifique os dados informados.", com o campo com problema, e não mostra o ranking
- **Origem:** [UC-25 E2.1](../casos-de-uso/fichas-resumidas.md#uc25-e2-1)
- **RF:** [RF-45.1](../requisitos/rf-reservas.md#rf-45-1)
- **TA:** [TA-225](#ta-225)

#### <a id="us-24-ca-10"></a>US-24 · CA-10 · Recusar quem não é Gestor (acesso)

- **Dado** uma pessoa sem identificação, ou um Solicitante, mesmo com reservas confirmadas dele
- **Quando** ela pede o ranking de espaços, com ou sem limite válido
- **Então** o sistema pede que a pessoa entre (sem identificação) ou informa que ela não tem permissão (Solicitante), sem mostrar espaço nem número algum; outra forma de pedir (que não seja consultar) é recusada como operação inexistente
- **Origem:** [UC-25 E1.1](../casos-de-uso/fichas-resumidas.md#uc25-e1-1)
- **RF:** [RF-45.1](../requisitos/rf-reservas.md#rf-45-1)
- **TA:** [TA-226](#ta-226)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-217"></a>TA-217 | [CA-01](#us-24-ca-01) | automatizado | `reservas/tests/test_api_ranking_de_espacos.py::test_ranking_vem_em_ordem_com_posicao_nome_e_total`; `reservas/tests/test_api_ranking_de_espacos.py::test_espaco_desativado_continua_no_ranking_com_o_nome`; `reservas/tests/test_ranking_de_espacos_caso_de_uso.py::test_com_o_ranking_montado_le_da_projecao_e_nao_do_repositorio`; `reservas/tests/test_ranking_de_espacos_caso_de_uso.py::test_espaco_sem_nome_conhecido_recebe_o_nome_de_reserva` |
| <a id="ta-218"></a>TA-218 | [CA-02](#us-24-ca-02) | automatizado | `reservas/tests/test_ranking_de_espacos.py::test_empate_com_ids_de_um_e_dois_digitos_segue_o_valor_numerico [x]`; `reservas/tests/test_ranking_de_espacos.py::test_empate_que_atravessa_o_limite_fica_com_os_menores_ids [x]`; `reservas/tests/test_ranking_de_espacos.py::test_empate_na_fronteira_com_espacos_acima_do_corte [x]`; `reservas/tests/test_repositorio_reservas.py::test_ranking_ordena_por_total_decrescente_e_no_empate_por_id_do_espaco [x]`; `reservas/tests/test_repositorio_reservas.py::test_ranking_respeita_o_limite_com_empate_na_fronteira [x]`; `reservas/tests/test_ranking_de_espacos_caso_de_uso.py::test_empate_vai_para_o_menor_id_do_espaco_com_ids_de_um_e_dois_digitos` |
| <a id="ta-219"></a>TA-219 | [CA-03](#us-24-ca-03) | automatizado | `reservas/tests/test_ranking_de_espacos.py::test_situacao_que_nao_conta_nao_entra_no_ranking [x]`; `reservas/tests/test_ranking_de_espacos.py::test_substituir_monta_do_zero_so_com_as_reservas_que_contam [x]`; `reservas/tests/test_repositorio_reservas.py::test_ranking_conta_so_confirmadas_e_concluidas [x]`; `reservas/tests/test_situacao.py::test_conta_no_ranking_segue_o_conjunto [x]` |
| <a id="ta-220"></a>TA-220 | [CA-04](#us-24-ca-04) | automatizado | `reservas/tests/test_ranking_de_espacos.py::test_confirmada_que_vira_concluida_continua_contando_uma_vez [x]`; `reservas/tests/test_ranking_de_espacos.py::test_aplicar_o_mesmo_estado_varias_vezes_nao_soma [x]`; `reservas/tests/test_concorrencia_do_ranking.py::test_vinte_aplicacoes_da_mesma_reserva_contam_uma_vez`; `reservas/tests/test_api_ranking_de_espacos.py::test_repetir_o_mesmo_pedido_nao_conta_duas_vezes` |
| <a id="ta-221"></a>TA-221 | [CA-05](#us-24-ca-05) | automatizado | `reservas/tests/test_api_ranking_de_espacos.py::test_cancelar_uma_confirmada_pela_api_tira_do_ranking_sem_reconstruir`; `reservas/tests/test_api_ranking_de_espacos.py::test_cancelar_a_unica_confirmada_do_espaco_o_tira_do_ranking`; `reservas/tests/test_ranking_de_espacos.py::test_confirmada_que_vira_cancelada_deixa_de_contar_e_o_espaco_some [x]`; `reservas/tests/test_repositorio_com_agenda.py::test_cancelar_a_confirmada_tira_o_espaco_do_ranking` |
| <a id="ta-222"></a>TA-222 | [CA-06](#us-24-ca-06) | automatizado | `reservas/tests/test_api_ranking_de_espacos.py::test_limite_corta_a_lista_e_o_padrao_e_cinco`; `reservas/tests/test_api_ranking_de_espacos.py::test_limites_nas_bordas_sao_aceitos [x]`; `reservas/tests/test_ranking_de_espacos_caso_de_uso.py::test_respeita_o_limite_pedido` |
| <a id="ta-223"></a>TA-223 | [CA-07](#us-24-ca-07) | automatizado | `reservas/tests/test_api_ranking_de_espacos.py::test_sem_reservas_confirmadas_diz_que_nao_ha_ranking`; `reservas/tests/test_api_ranking_de_espacos.py::test_ranking_com_um_espaco_usa_o_singular`; `reservas/tests/test_ranking_de_espacos_caso_de_uso.py::test_sem_reservas_que_contam_a_resposta_e_vazia` |
| <a id="ta-224"></a>TA-224 | [CA-08](#us-24-ca-08) | automatizado | `reservas/tests/test_api_ranking_de_espacos.py::test_resposta_com_o_ranking_montado_e_a_do_banco_sao_iguais`; `reservas/tests/test_api_ranking_de_espacos.py::test_resposta_com_o_redis_fora_do_ar_e_a_mesma_e_nunca_503`; `reservas/tests/test_api_ranking_de_espacos.py::test_ler_o_ranking_nao_repovoa_a_projecao`; `reservas/tests/test_ranking_de_espacos_caso_de_uso.py::test_sem_o_ranking_montado_cai_para_o_repositorio_com_o_mesmo_resultado`; `reservas/tests/test_ranking_de_espacos_caso_de_uso.py::test_ranking_indisponivel_cai_para_o_repositorio_e_deixa_um_aviso`; `reservas/tests/test_propriedades_das_projecoes.py::TestMaquinaDasProjecoes` |
| <a id="ta-225"></a>TA-225 | [CA-09](#us-24-ca-09) | automatizado | `reservas/tests/test_api_ranking_de_espacos.py::test_limite_invalido_recebe_400_com_o_campo [x]` |
| <a id="ta-226"></a>TA-226 | [CA-10](#us-24-ca-10) | automatizado | `reservas/tests/test_api_ranking_de_espacos.py::test_anonimo_recebe_401`; `reservas/tests/test_api_ranking_de_espacos.py::test_solicitante_recebe_403_mesmo_com_reservas_confirmadas`; `reservas/tests/test_api_ranking_de_espacos.py::test_solicitante_com_limite_invalido_recebe_403_e_nao_400`; `reservas/tests/test_api_ranking_de_espacos.py::test_outros_metodos_recebem_405 [x]`; `reservas/tests/test_ranking_de_espacos_caso_de_uso.py::test_solicitante_nao_consulta_o_ranking`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]` |

## Como verificar

Os mesmos passos das demais histórias: `docker compose exec backend pytest <arquivo>` para cada teste citado, e `python scripts/verificar_historias.py` na raiz do repositório.
