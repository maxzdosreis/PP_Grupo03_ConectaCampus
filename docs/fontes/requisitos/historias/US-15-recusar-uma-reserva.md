# US-15 · Recusar uma reserva com motivo

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-15 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-15-recusar-uma-reserva.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-19 e TA-20 passam a TA-20 e TA-21, e TA-21 a TA-158 passam a TA-24 a TA-161, para os TA-19, TA-22 e TA-23 novos da US-03 (revogação e troca da credencial de renovação) seguirem a ordem das histórias (AUT-09). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-96 a TA-107 passam a TA-97, TA-98, TA-99, TA-102, TA-103, TA-105, TA-106, TA-107, TA-109, TA-110, TA-113 e TA-114, e TA-108 a TA-161 passam a TA-115 a TA-168, para os TAs novos das US-10 e US-11 (consulta em páginas) seguirem a ordem das histórias (RES-10). Mudança editorial, sem nova obrigação. Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-15 |
| **Título** | Recusar uma reserva com motivo |
| **História** | Como Gestor, quero recusar um pedido Solicitado explicando o motivo para que o solicitante entenda a decisão e o horário fique livre para outra pessoa. |
| **Valor** | Toda recusa é justificada a quem pediu e o período volta a aceitar pedidos ([NS-09](../visao.md#necessidades), [NS-07](../visao.md#necessidades)). |
| **Origem** | [UC-18 Recusar reserva](../casos-de-uso/README.md#uc-18): o fluxo comum de [UC-10, passos 1 a 8](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p1), na [variação UC-18](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-18), com UC-12 ([Informar motivo](../casos-de-uso/README.md#uc-12): passos 4 e 5, E6.6 e E6.7) e UC-13; as exceções E6.4 a E6.7 no contexto da recusa. |
| **Prioridade** | Normal — [RF-18](../requisitos/rf-reservas.md#rf-18) e [RF-24](../requisitos/rf-reservas.md#rf-24) são normais (F4 do enunciado). |
| **Estimativa (Custo em Semanas)** | 0,2 (retrospectiva: a recusa com motivo obrigatório da RES-06 e o campo de motivo do diálogo da FE-05). |
| **Conversa** | "Pode recusar um pedido já confirmado?" → não; para desfazer uma Confirmada, o Gestor cancela ([US-13](US-13-cancelar-uma-reserva.md)). "Pode recusar depois que o horário começou?" → hoje sim ([DEC-13](../decisoes/DEC-13.md)). "A tentativa de recusar sem motivo fica registrada?" → não ([DEC-05](../decisoes/DEC-05.md)). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Precisa de um pedido Solicitado ([US-08](US-08-solicitar-reserva.md)); compartilha o fluxo de [US-14](US-14-confirmar-uma-reserva.md). |
| **N** · Negociável | ✓ | O texto do motivo, o limite de caracteres e se a recusa vale depois do início ([DEC-13](../decisoes/DEC-13.md)) podem ser combinados sem mudar a meta. |
| **V** · Valiosa | ✓ | Sem ela, um pedido indevido ocuparia o horário até alguém cancelá-lo. |
| **E** · Estimável | ✓ | Uma transição com motivo, sobre o fluxo comum. |
| **S** · Small | ✓ | Uma transição sobre o fluxo comum: cabe numa iteração. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado. |

**Diagnóstico:** negociável, valiosa, pequena e testável; só não é independente de US-08.

## Critérios de aceite

#### <a id="us-15-ca-01"></a>US-15 · CA-01 · Pedido recusado com motivo (sucesso)

- **Dado** uma reserva Solicitada e um Gestor identificado
- **Quando** o Gestor escolhe recusá-la, escreve o motivo "Espaço reservado para um evento da instituição" e confirma
- **Então** o sistema informa "Reserva recusada com sucesso.", a reserva passa a Recusada com o motivo visível ao solicitante na lista e no detalhe, e não oferece mais nenhuma ação
- **Origem:** [UC-10 passos 1 a 8, variação UC-18](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-18)
- **RF:** [RF-18](../requisitos/rf-reservas.md#rf-18)
- **TA:** [TA-145](#ta-145)
- **Depende de:** [DEC-13](../decisoes/DEC-13.md) (recusar depois do início também é aceito hoje)

#### <a id="us-15-ca-02"></a>US-15 · CA-02 · O horário é liberado (sucesso)

- **Dado** uma reserva das 10:00 às 11:00 que acabou de ser recusada
- **Quando** outra pessoa pede o mesmo espaço das 10:00 às 11:00
- **Então** o pedido é aceito: uma reserva Recusada não ocupa o horário
- **Origem:** [UC-10 variação UC-18](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-18)
- **RF:** [RF-18](../requisitos/rf-reservas.md#rf-18)
- **TA:** [TA-146](#ta-146)

#### <a id="us-15-ca-03"></a>US-15 · CA-03 · Recusar o que não está Solicitada (exceção)

- **Dado** uma reserva Confirmada, ou numa situação final
- **Quando** o Gestor pede para recusá-la
- **Então** o sistema informa "Não é possível alterar uma reserva Confirmada para Recusada." (com a situação atual), e a reserva continua como estava, com o mesmo motivo e o mesmo histórico
- **Origem:** [UC-10 E6.5](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-5)
- **RF:** [RF-24](../requisitos/rf-reservas.md#rf-24)
- **TA:** [TA-147](#ta-147)

#### <a id="us-15-ca-04"></a>US-15 · CA-04 · Motivo longo demais (exceção)

- **Dado** uma reserva Solicitada
- **Quando** o Gestor a recusa com um motivo de mais de 300 caracteres depois de tirar os espaços das pontas e os repetidos
- **Então** o sistema informa, junto ao motivo, 'O campo "Motivo" deve ter no máximo 300 caracteres.', e a reserva continua Solicitada, ocupando o horário
- **Origem:** [UC-10 E6.6](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-6)
- **RF:** [RF-26](../requisitos/rf-reservas.md#rf-26)
- **TA:** [TA-148](#ta-148)

#### <a id="us-15-ca-05"></a>US-15 · CA-05 · Recusar sem motivo (exceção)

- **Dado** uma reserva Solicitada
- **Quando** o Gestor confirma a recusa sem motivo, ou com um motivo só de espaços
- **Então** o sistema informa, junto ao motivo, "Informe o motivo para recusar ou cancelar a reserva.", o motivo fica pronto para ser escrito, e a reserva continua Solicitada
- **Origem:** [UC-10 E6.7](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-7)
- **RF:** [RF-26](../requisitos/rf-reservas.md#rf-26)
- **TA:** [TA-149](#ta-149)

#### <a id="us-15-ca-06"></a>US-15 · CA-06 · Recusa registrada no histórico (registro)

- **Dado** uma reserva que o Gestor acabou de recusar (CA-01)
- **Quando** o histórico é consultado
- **Então** o último registro é "Recusada por" o nome do Gestor, da situação anterior Solicitada, com o momento e o motivo; a tentativa de recusar sem motivo (CA-05) não aparece — só as mudanças aceitas são registradas, diferente do modelo do professor
- **Origem:** [UC-10 passo 7](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p7)
- **RF:** [RF-22](../requisitos/rf-reservas.md#rf-22)
- **TA:** [TA-150](#ta-150)
- **Depende de:** [DEC-05](../decisoes/DEC-05.md)

#### <a id="us-15-ca-07"></a>US-15 · CA-07 · Só o Gestor recusa (acesso)

- **Dado** uma reserva Solicitada do próprio Solicitante
- **Quando** ele pede para recusá-la
- **Então** o sistema informa "Somente o gestor pode recusar reservas.", a reserva não muda, e a opção de recusar nem é oferecida a ele
- **Origem:** [UC-10 E6.4](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-4)
- **RF:** [RF-27](../requisitos/rf-reservas.md#rf-27)
- **TA:** [TA-151](#ta-151)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-145"></a>TA-145 | [CA-01](#us-15-ca-01) | automatizado | `reservas/tests/test_api_situacao_reserva.py::test_mensagem_de_sucesso_usa_o_rotulo_da_nova_situacao [recusada]`; `reservas/tests/test_alterar_situacao.py::test_transicao_permitida_e_persistida [x]`; `pages/PaginaReservas.test.tsx`: `"Recusar" abre o diálogo com o campo de motivo em foco`; `pages/PaginaReservas.test.tsx`: `enviar recusa com o motivo, mostra a mensagem da API, fecha e recarrega` |
| <a id="ta-146"></a>TA-146 | [CA-02](#us-15-ca-02) | automatizado | `reservas/tests/test_conflito_de_horario.py::test_sobreposicao_com_reserva_que_nao_ocupa_horario_e_aceita [x]` |
| <a id="ta-147"></a>TA-147 | [CA-03](#us-15-ca-03) | automatizado | `reservas/tests/test_reserva.py::test_transicao_proibida_e_recusada_e_preserva_a_situacao [x]`; `reservas/tests/test_situacao.py::test_transicao_permitida_segue_a_tabela [x]`; `reservas/tests/test_reserva.py::test_transicao_proibida_tem_mensagem_com_os_rotulos` |
| <a id="ta-148"></a>TA-148 | [CA-04](#us-15-ca-04) | automatizado | `reservas/tests/test_reserva.py::test_motivo_acima_do_limite_e_recusado_e_nada_muda`; `reservas/tests/test_propriedades_da_reserva.py::TestMaquinaDaReserva` |
| <a id="ta-149"></a>TA-149 | [CA-05](#us-15-ca-05) | automatizado | `reservas/tests/test_api_situacao_reserva.py::test_recusar_sem_motivo_responde_400_no_campo_motivo`; `reservas/tests/test_reserva.py::test_recusar_ou_cancelar_sem_motivo_e_recusado_e_nada_muda [x]`; `pages/PaginaReservas.test.tsx`: `erro no motivo aparece embaixo do campo, que recebe o foco` |
| <a id="ta-150"></a>TA-150 | [CA-06](#us-15-ca-06) | automatizado | `reservas/tests/test_reserva.py::test_transicao_permitida_gera_o_registro_da_mudanca [x]`; `reservas/tests/test_api_historico.py::test_tentativa_recusada_nao_aparece_no_historico`; `reservas/tests/test_alterar_situacao.py::test_alteracao_recusada_nao_registra_no_historico` |
| <a id="ta-151"></a>TA-151 | [CA-07](#us-15-ca-07) | automatizado | `reservas/tests/test_permissoes_reserva.py::test_alterar_situacao_segue_a_matriz_e_preserva_a_reserva_nos_erros [x]`; `reservas/tests/test_api_permissoes.py::test_acoes_do_solicitante_na_propria_solicitada_sao_so_cancelar` |
