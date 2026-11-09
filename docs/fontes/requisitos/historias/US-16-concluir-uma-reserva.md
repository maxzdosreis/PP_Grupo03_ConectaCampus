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

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-16 |
| **Título** | Concluir uma reserva |
| **História** | Como Gestor, quero marcar como concluída uma reserva confirmada para registrar que o uso aconteceu e encerrar o ciclo dela. |
| **Valor** | A instituição sabe quais usos combinados de fato aconteceram, com quem registrou e quando ([NS-09](../visao.md#necessidades), [NS-12](../visao.md#necessidades)). |
| **Origem** | [UC-19 Concluir reserva](../casos-de-uso/README.md#uc-19): o fluxo comum de [UC-10, passos 1 a 8](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p1), na [variação UC-19](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-19), com UC-13; alternativa A8.1 e as exceções E2.1, E6.4 e E6.5 no contexto da conclusão. |
| **Prioridade** | Normal — [RF-19](../requisitos/rf-reservas.md#rf-19) e [RF-24](../requisitos/rf-reservas.md#rf-24) são normais (F4 do enunciado: o terceiro estado). |
| **Estimativa (Custo em Semanas)** | 0,1 (retrospectiva: a transição Confirmada → Concluída da RES-06, sobre o fluxo comum). |
| **Conversa** | "Pode concluir antes de o horário terminar?" → hoje sim, contra o que a NS-09 diz ("o uso aconteceu"): [DEC-13](../decisoes/DEC-13.md), aberta, e [L-01](../requisitos/srs.md#l-01). "Uma reserva concluída pode voltar atrás?" → não, é final. |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Só uma reserva Confirmada pode ser concluída: depende de [US-14](US-14-confirmar-uma-reserva.md). |
| **N** · Negociável | ✗ | O momento em que se pode concluir está preso à [DEC-13](../decisoes/DEC-13.md); a opção b criaria a recusa "concluir antes do término". |
| **V** · Valiosa | ✓ | Fecha o ciclo e libera o horário que sobrou; sem ela, F4 teria só dois estados de chegada. |
| **E** · Estimável | ✓ | Uma transição sobre o fluxo comum. |
| **S** · Small | ✓ | A menor das quatro decisões. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado. |

**Diagnóstico:** pequena, valiosa e testável, mas depende de US-14 e não é negociável enquanto a DEC-13 estiver aberta — é a história mais exposta a ela.

## Critérios de aceite

#### <a id="us-16-ca-01"></a>US-16 · CA-01 · Uso concluído (sucesso)

- **Dado** uma reserva Confirmada e um Gestor identificado
- **Quando** o Gestor escolhe concluí-la e confirma, sem precisar de motivo
- **Então** o sistema informa "Reserva concluída com sucesso.", a reserva passa a Concluída, não oferece mais nenhuma ação e deixa de ocupar o horário
- **Origem:** [UC-10 passos 1 a 8, variação UC-19](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-19)
- **RF:** [RF-19](../requisitos/rf-reservas.md#rf-19)
- **TA:** [TA-152](#ta-152)
- **Depende de:** [DEC-13](../decisoes/DEC-13.md) (hoje é aceito mesmo antes do término do horário)

#### <a id="us-16-ca-02"></a>US-16 · CA-02 · Motivo opcional ao concluir (alternativa)

- **Dado** uma reserva Confirmada com um motivo da confirmação
- **Quando** o Gestor a conclui informando, ou não, um motivo de até 300 caracteres
- **Então** a reserva fica Concluída com o motivo novo, sem espaços nas pontas nem repetidos, ou sem motivo; o motivo da confirmação deixa de aparecer na reserva e continua no histórico
- **Origem:** [UC-10 A8.1](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#a8-1)
- **RF:** [RF-19](../requisitos/rf-reservas.md#rf-19)
- **TA:** [TA-153](#ta-153)

#### <a id="us-16-ca-03"></a>US-16 · CA-03 · Nada mais a fazer numa reserva concluída (exceção)

- **Dado** uma reserva Concluída
- **Quando** o Gestor ou o solicitante a veem, e alguém pede para cancelá-la mesmo assim
- **Então** nenhuma ação é oferecida, e o pedido de cancelamento é recusado com "Não é possível alterar uma reserva Concluída para Cancelada."; a reserva continua Concluída
- **Origem:** [UC-10 E2.1](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e2-1)
- **RF:** [RF-16](../requisitos/rf-reservas.md#rf-16), [RF-24](../requisitos/rf-reservas.md#rf-24)
- **TA:** [TA-154](#ta-154)

#### <a id="us-16-ca-04"></a>US-16 · CA-04 · Concluir uma reserva que não foi confirmada (exceção)

- **Dado** uma reserva Solicitada (ainda não confirmada)
- **Quando** o Gestor pede para concluí-la
- **Então** o sistema informa "Não é possível alterar uma reserva Solicitada para Concluída.", e a reserva continua Solicitada, com o mesmo histórico
- **Origem:** [UC-10 E6.5](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-5)
- **RF:** [RF-24](../requisitos/rf-reservas.md#rf-24)
- **TA:** [TA-155](#ta-155)

#### <a id="us-16-ca-05"></a>US-16 · CA-05 · Ciclo completo no histórico (registro)

- **Dado** uma reserva solicitada, confirmada e concluída
- **Quando** o histórico é consultado
- **Então** ele mostra três registros, em ordem — criação (Solicitada), Confirmada e Concluída —, cada um com o autor e o momento, formando um caminho permitido pela tabela de transições; uma conclusão recusada (CA-04, CA-06) não gera registro, diferente do modelo do professor
- **Origem:** [UC-10 passo 7](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p7)
- **RF:** [RF-22](../requisitos/rf-reservas.md#rf-22)
- **TA:** [TA-156](#ta-156)
- **Depende de:** [DEC-05](../decisoes/DEC-05.md)

#### <a id="us-16-ca-06"></a>US-16 · CA-06 · Só o Gestor conclui (acesso)

- **Dado** uma reserva Solicitada do próprio Solicitante
- **Quando** ele pede para concluí-la
- **Então** o sistema informa "Somente o gestor pode concluir reservas.", e não que a transição é inválida: a resposta não revela a situação da reserva, que não muda
- **Origem:** [UC-10 E6.4](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-4)
- **RF:** [RF-27](../requisitos/rf-reservas.md#rf-27)
- **TA:** [TA-157](#ta-157)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-152"></a>TA-152 | [CA-01](#us-16-ca-01) | automatizado | `reservas/tests/test_api_situacao_reserva.py::test_fluxo_da_demonstracao_ate_concluida`; `reservas/tests/test_api_situacao_reserva.py::test_reserva_concluida_nao_traz_acoes`; `reservas/tests/test_alterar_situacao.py::test_ciclo_solicitada_confirmada_concluida`; `reservas/tests/test_conflito_de_horario.py::test_sobreposicao_com_reserva_que_nao_ocupa_horario_e_aceita [x]` |
| <a id="ta-153"></a>TA-153 | [CA-02](#us-16-ca-02) | automatizado | `reservas/tests/test_reserva.py::test_nova_situacao_limpa_o_motivo_da_anterior`; `reservas/tests/test_propriedades_da_reserva.py::TestMaquinaDaReserva` |
| <a id="ta-154"></a>TA-154 | [CA-03](#us-16-ca-03) | automatizado | `reservas/tests/test_api_situacao_reserva.py::test_reserva_concluida_nao_traz_acoes`; `reservas/tests/test_api_situacao_reserva.py::test_reserva_concluida_nao_pode_ser_cancelada`; `reservas/tests/test_api_permissoes.py::test_solicitante_numa_concluida_nao_tem_acoes` |
| <a id="ta-155"></a>TA-155 | [CA-04](#us-16-ca-04) | automatizado | `reservas/tests/test_api_situacao_reserva.py::test_transicao_proibida_responde_409_e_preserva_a_reserva`; `reservas/tests/test_reserva.py::test_transicao_proibida_e_recusada_e_preserva_a_situacao [x]` |
| <a id="ta-156"></a>TA-156 | [CA-05](#us-16-ca-05) | automatizado | `reservas/tests/test_api_historico.py::test_fluxo_completo_aparece_no_historico_em_ordem`; `exemplos/tests/test_carregar_dados_exemplo.py::test_concluida_passou_por_solicitada_e_confirmada_em_dias_diferentes`; `reservas/tests/test_reserva.py::test_alteracao_recusada_nao_muda_nada_nem_registra [x]` |
| <a id="ta-157"></a>TA-157 | [CA-06](#us-16-ca-06) | automatizado | `reservas/tests/test_permissoes_reserva.py::test_solicitante_concluindo_uma_solicitada_recebe_403_e_nao_409` |
