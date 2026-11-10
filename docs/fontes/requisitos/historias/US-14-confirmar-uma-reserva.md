# US-14 · Confirmar uma reserva

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-14 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-14-confirmar-uma-reserva.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-19 e TA-20 passam a TA-20 e TA-21, e TA-21 a TA-158 passam a TA-24 a TA-161, para os TA-19, TA-22 e TA-23 novos da US-03 (revogação e troca da credencial de renovação) seguirem a ordem das histórias (AUT-09). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-96 a TA-107 passam a TA-97, TA-98, TA-99, TA-102, TA-103, TA-105, TA-106, TA-107, TA-109, TA-110, TA-113 e TA-114, e TA-108 a TA-161 passam a TA-115 a TA-168, para os TAs novos das US-10 e US-11 (consulta em páginas) seguirem a ordem das histórias (RES-10). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Index Card: o papel da história passa a ser Atendente responsável ([DEC-25](../decisoes/DEC-25.md)); meta, valor, critérios e testes de aceite iguais (REQ-12). Mudança editorial, sem nova obrigação. Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-14 |
| **Título** | Confirmar uma reserva |
| **História** | Como Atendente responsável, quero confirmar um pedido Solicitado para garantir ao solicitante que o espaço é dele naquele horário. |
| **Valor** | O solicitante sabe que pode contar com o espaço, e a decisão fica registrada com quem decidiu e quando ([NS-09](../visao.md#necessidades), [NS-11](../visao.md#necessidades)). |
| **Origem** | [UC-17 Confirmar reserva](../casos-de-uso/README.md#uc-17): o fluxo comum de [UC-10, passos 1 a 8](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p1), na [variação UC-17](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-17), com UC-13; alternativa A8.1 e as exceções E6.1 a E6.6 e E7.1 no contexto da confirmação. As recusas de formato do pedido de mudança (E6.1 e E6.3), comuns aos quatro filhos, ficam nesta história, a primeira decisão do Gestor. |
| **Prioridade** | Normal — [RF-17](../requisitos/rf-reservas.md#rf-17), [RF-23](../requisitos/rf-reservas.md#rf-23), [RF-24](../requisitos/rf-reservas.md#rf-24) e [RF-25](../requisitos/rf-reservas.md#rf-25) são normais (F4 do enunciado). |
| **Estimativa (Custo em Semanas)** | 0,4 (retrospectiva: a alteração de situação da RES-06, a proteção contra decisões simultâneas da RES-07, as permissões da AUT-05 e os botões e o diálogo da FE-05). |
| **Conversa** | "Pode confirmar depois que o horário começou?" → hoje sim ([DEC-13](../decisoes/DEC-13.md), aberta). "O motivo é obrigatório ao confirmar?" → não, mas, se informado, tem o mesmo limite de 300 caracteres ([L-13](../requisitos/srs.md#l-13)). "E se dois gestores decidirem ao mesmo tempo?" → só o primeiro grava; o segundo fica sabendo. |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Precisa de um pedido Solicitado ([US-08](US-08-solicitar-reserva.md)) e de um Gestor ([US-17](US-17-criar-o-primeiro-gestor.md)). |
| **N** · Negociável | ✗ | Confirmar depois do início depende da [DEC-13](../decisoes/DEC-13.md); se a opção mudar, nasce uma recusa nova. |
| **V** · Valiosa | ✓ | É a decisão mais comum do Gestor e o que o solicitante espera. |
| **E** · Estimável | ✓ | Reaproveita o fluxo comum de UC-10. |
| **S** · Small | ✗ | Leva também as recusas comuns de formato (CA-04 e CA-05) e a decisão simultânea; sem elas seria só uma transição. O corte seria tirar as recusas comuns para uma história técnica, o que não entrega valor a ninguém, por isso ficaram aqui. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado, inclusive duas threads decidindo ao mesmo tempo. |

**Diagnóstico:** valiosa e testável, mas depende de US-08, não é negociável enquanto a DEC-13 estiver aberta e ficou maior por concentrar as recusas comuns.

## Critérios de aceite

#### <a id="us-14-ca-01"></a>US-14 · CA-01 · Pedido confirmado (sucesso)

- **Dado** uma reserva Solicitada e um Gestor identificado
- **Quando** o Gestor escolhe confirmá-la e confirma a decisão, depois de ver o espaço, a data e o horário e o solicitante, sem precisar de motivo
- **Então** o sistema informa "Reserva confirmada com sucesso.", a reserva passa a Confirmada e passa a oferecer ao Gestor "Cancelar" e "Concluir" (e ao solicitante, só "Cancelar")
- **Origem:** [UC-10 passos 1 a 8, variação UC-17](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-17)
- **RF:** [RF-17](../requisitos/rf-reservas.md#rf-17)
- **TA:** [TA-134](#ta-134)
- **Depende de:** [DEC-13](../decisoes/DEC-13.md) (confirmar depois do início também é aceito hoje)

#### <a id="us-14-ca-02"></a>US-14 · CA-02 · O horário continua ocupado (sucesso)

- **Dado** uma reserva confirmada das 10:00 às 11:00
- **Quando** outra pessoa pede o mesmo espaço com algum momento em comum
- **Então** o pedido é recusado por conflito de horário, como em [US-08 · CA-18](US-08-solicitar-reserva.md#us-08-ca-18): a confirmação não liberou o horário
- **Origem:** [UC-10 variação UC-17](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-17)
- **RF:** [RF-17](../requisitos/rf-reservas.md#rf-17)
- **TA:** [TA-135](#ta-135)

#### <a id="us-14-ca-03"></a>US-14 · CA-03 · Motivo opcional ao confirmar (alternativa)

- **Dado** uma reserva Solicitada
- **Quando** o Gestor a confirma informando o motivo "  Uso  aprovado pelo setor "
- **Então** a reserva fica Confirmada com o motivo "Uso aprovado pelo setor", e um motivo da situação anterior deixa de aparecer na reserva (continua no histórico)
- **Origem:** [UC-10 A8.1](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#a8-1)
- **RF:** [RF-17](../requisitos/rf-reservas.md#rf-17)
- **TA:** [TA-136](#ta-136)

#### <a id="us-14-ca-04"></a>US-14 · CA-04 · Pedido de mudança sem a situação nova (exceção)

- **Dado** uma reserva Solicitada
- **Quando** chega um pedido de mudança sem dizer para qual situação, ou com ela em branco
- **Então** o sistema informa "Verifique os dados informados.", indicando junto à situação que ela é obrigatória, sem nem procurar a reserva; a reserva não muda
- **Origem:** [UC-10 E6.1](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-1)
- **RF:** [RF-25](../requisitos/rf-reservas.md#rf-25)
- **TA:** [TA-137](#ta-137)

#### <a id="us-14-ca-05"></a>US-14 · CA-05 · Situação desconhecida (exceção)

- **Dado** uma reserva Solicitada
- **Quando** o pedido de mudança traz uma situação que não é uma das situações de reserva
- **Então** o sistema informa, junto à situação, "Situação inválida. Escolha uma destas: Solicitada, Confirmada, Recusada, Cancelada, Concluída.", e a reserva não muda
- **Origem:** [UC-10 E6.3](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-3)
- **RF:** [RF-25](../requisitos/rf-reservas.md#rf-25)
- **TA:** [TA-138](#ta-138)

#### <a id="us-14-ca-06"></a>US-14 · CA-06 · Confirmar o que não está Solicitada (exceção)

- **Dado** uma reserva já Confirmada, ou numa situação final (Concluída, Recusada ou Cancelada)
- **Quando** o Gestor pede para confirmá-la (por exemplo, com uma lista antiga)
- **Então** o sistema informa "Não é possível alterar uma reserva «situação atual» para Confirmada.", e a reserva continua na situação, com o motivo e o histórico que tinha
- **Origem:** [UC-10 E6.5](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-5)
- **RF:** [RF-24](../requisitos/rf-reservas.md#rf-24)
- **TA:** [TA-139](#ta-139)

#### <a id="us-14-ca-07"></a>US-14 · CA-07 · Motivo opcional longo demais (exceção)

- **Dado** uma reserva Solicitada
- **Quando** o Gestor a confirma com um motivo de mais de 300 caracteres, mesmo o motivo sendo opcional
- **Então** o sistema informa, junto ao motivo, 'O campo "Motivo" deve ter no máximo 300 caracteres.', e a reserva continua Solicitada
- **Origem:** [UC-10 E6.6](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-6)
- **RF:** [RF-17](../requisitos/rf-reservas.md#rf-17) (o limite ao confirmar não está escrito no RF: [L-13](../requisitos/srs.md#l-13))
- **TA:** [TA-140](#ta-140)

#### <a id="us-14-ca-08"></a>US-14 · CA-08 · Dois gestores decidindo ao mesmo tempo (exceção)

- **Dado** uma reserva Solicitada que dois Gestores leram ao mesmo tempo
- **Quando** um a confirma e o outro, logo depois e sobre a mesma leitura, a recusa
- **Então** só a primeira decisão vale; o segundo recebe "Esta reserva já está Confirmada: ela foi alterada enquanto você decidia. Atualize a lista e tente de novo.", e o histórico tem um registro só, sem dois registros saindo da mesma situação
- **Origem:** [UC-10 E7.1](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e7-1)
- **RF:** [RF-17](../requisitos/rf-reservas.md#rf-17) (a garantia é o [RNF-R04](../requisitos/rnf.md#rnf-r04))
- **TA:** [TA-141](#ta-141)

#### <a id="us-14-ca-09"></a>US-14 · CA-09 · Confirmação registrada no histórico (registro)

- **Dado** uma reserva que a Carla, Gestora, acabou de confirmar
- **Quando** o histórico é consultado
- **Então** o último registro é "Confirmada por Carla", da situação anterior Solicitada, com o momento da decisão e o motivo, se houver; uma confirmação recusada (CA-04 a CA-08, CA-10, CA-11) não gera registro — diferente do modelo do professor
- **Origem:** [UC-10 passo 7](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p7)
- **RF:** [RF-22](../requisitos/rf-reservas.md#rf-22)
- **TA:** [TA-142](#ta-142)
- **Depende de:** [DEC-05](../decisoes/DEC-05.md)

#### <a id="us-14-ca-10"></a>US-14 · CA-10 · Só o Gestor confirma (acesso)

- **Dado** uma reserva do próprio Solicitante, em qualquer situação
- **Quando** ele pede para confirmá-la
- **Então** o sistema informa "Somente o gestor pode confirmar reservas." — a mesma resposta qualquer que seja a situação atual —, a reserva não muda, e a opção de confirmar nem é oferecida a ele
- **Origem:** [UC-10 E6.4](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-4)
- **RF:** [RF-27](../requisitos/rf-reservas.md#rf-27)
- **TA:** [TA-143](#ta-143)

#### <a id="us-14-ca-11"></a>US-14 · CA-11 · Confirmar a reserva de outra pessoa sendo Solicitante (acesso)

- **Dado** uma reserva Solicitada do Bruno
- **Quando** a Ana, Solicitante, pede para confirmá-la
- **Então** o sistema responde "Reserva de código «n» não encontrada.", e não "Somente o gestor…", para não revelar que a reserva existe; ela não muda
- **Origem:** [UC-10 E6.2](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-2)
- **RF:** [RF-23](../requisitos/rf-reservas.md#rf-23)
- **TA:** [TA-144](#ta-144)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-134"></a>TA-134 | [CA-01](#us-14-ca-01) | automatizado | `reservas/tests/test_api_situacao_reserva.py::test_confirmar_responde_200_com_a_reserva_atualizada`; `reservas/tests/test_api_permissoes.py::test_gestor_confirma`; `reservas/tests/test_api_situacao_reserva.py::test_reserva_confirmada_traz_cancelar_e_concluir`; `pages/PaginaReservas.test.tsx`: `"Confirmar" abre o diálogo com o resumo e sem campo de motivo`; `pages/PaginaReservas.test.tsx`: `confirmar envia só a situação, sem motivo` |
| <a id="ta-135"></a>TA-135 | [CA-02](#us-14-ca-02) | automatizado | `reservas/tests/test_conflito_de_horario.py::test_sobreposicao_com_reserva_que_ocupa_horario_e_conflito [x]`; `reservas/tests/test_api_reservas.py::test_horario_ocupado_responde_409_e_preserva_as_reservas` |
| <a id="ta-136"></a>TA-136 | [CA-03](#us-14-ca-03) | automatizado | `reservas/tests/test_reserva.py::test_motivo_opcional_ao_confirmar_e_guardado_normalizado`; `reservas/tests/test_reserva.py::test_nova_situacao_limpa_o_motivo_da_anterior` |
| <a id="ta-137"></a>TA-137 | [CA-04](#us-14-ca-04) | automatizado | `reservas/tests/test_api_situacao_reserva.py::test_situacao_ausente_ou_invalida_responde_400 [x]` |
| <a id="ta-138"></a>TA-138 | [CA-05](#us-14-ca-05) | automatizado | `reservas/tests/test_api_situacao_reserva.py::test_situacao_ausente_ou_invalida_responde_400 [x]`; `reservas/tests/test_alterar_situacao.py::test_situacao_desconhecida_lanca_erro_e_preserva_a_reserva`; `reservas/tests/test_reserva.py::test_situacao_desconhecida_e_recusada_e_nada_muda` |
| <a id="ta-139"></a>TA-139 | [CA-06](#us-14-ca-06) | automatizado | `reservas/tests/test_reserva.py::test_transicao_proibida_e_recusada_e_preserva_a_situacao [x]`; `reservas/tests/test_situacao.py::test_transicao_permitida_segue_a_tabela [x]`; `reservas/tests/test_permissoes_reserva.py::test_solicitada_como_destino_e_transicao_invalida_para_os_dois_papeis [x]` |
| <a id="ta-140"></a>TA-140 | [CA-07](#us-14-ca-07) | automatizado | `reservas/tests/test_reserva.py::test_motivo_acima_do_limite_e_recusado_e_nada_muda`; `reservas/tests/test_propriedades_da_reserva.py::TestMaquinaDaReserva` (motivo acima do limite em qualquer destino) |
| <a id="ta-141"></a>TA-141 | [CA-08](#us-14-ca-08) | automatizado | `reservas/tests/test_concorrencia_de_situacao.py::test_alteracoes_simultaneas_gravam_so_uma_e_o_historico_fica_coerente`; `reservas/tests/test_repositorio_reservas.py::test_salvar_entidade_que_ficou_para_tras_nao_regride_a_situacao`; `reservas/tests/test_repositorio_reservas.py::test_salvar_reserva_existente_bloqueia_a_linha` |
| <a id="ta-142"></a>TA-142 | [CA-09](#us-14-ca-09) | automatizado | `reservas/tests/test_reserva.py::test_transicao_permitida_gera_o_registro_da_mudanca [x]`; `reservas/tests/test_alterar_situacao.py::test_registro_da_mudanca_usa_o_relogio_injetado_e_o_ator`; `reservas/tests/test_api_historico.py::test_fluxo_completo_aparece_no_historico_em_ordem`; `reservas/tests/test_reserva.py::test_alteracao_recusada_nao_muda_nada_nem_registra [x]` |
| <a id="ta-143"></a>TA-143 | [CA-10](#us-14-ca-10) | automatizado | `reservas/tests/test_api_permissoes.py::test_solicitante_confirmando_a_propria_responde_403_sem_mudar_nada`; `reservas/tests/test_permissoes_reserva.py::test_alterar_situacao_segue_a_matriz_e_preserva_a_reserva_nos_erros [x]`; `reservas/tests/test_api_permissoes.py::test_acoes_do_solicitante_na_propria_solicitada_sao_so_cancelar` |
| <a id="ta-144"></a>TA-144 | [CA-11](#us-14-ca-11) | automatizado | `reservas/tests/test_permissoes_reserva.py::test_quem_nao_ve_a_reserva_recebe_nao_encontrada_com_o_codigo_dela` |
