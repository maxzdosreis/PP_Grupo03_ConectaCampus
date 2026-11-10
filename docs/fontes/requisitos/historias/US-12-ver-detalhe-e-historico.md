# US-12 · Ver o detalhe e o histórico de uma reserva

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-12 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-12-ver-detalhe-e-historico.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-19 e TA-20 passam a TA-20 e TA-21, e TA-21 a TA-158 passam a TA-24 a TA-161, para os TA-19, TA-22 e TA-23 novos da US-03 (revogação e troca da credencial de renovação) seguirem a ordem das histórias (AUT-09). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-96 a TA-107 passam a TA-97, TA-98, TA-99, TA-102, TA-103, TA-105, TA-106, TA-107, TA-109, TA-110, TA-113 e TA-114, e TA-108 a TA-161 passam a TA-115 a TA-168, para os TAs novos das US-10 e US-11 (consulta em páginas) seguirem a ordem das histórias (RES-10). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Critérios novos: CA-03, CA-11 novos, com a implementação pendente na tarefa RES-12 ([CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md)). CAs antigos que a regra nova substitui ficam marcados com Situação, sem apagar o texto nem o TA. Renumeração dos TAs: TA-115 a TA-124 passam a TA-125 a TA-136 (e os CAs seguintes na mesma história, quando há CA novo antes deles), para os 25 TAs pendentes novos seguirem a ordem das histórias (REQ-13). A especificação está adiante do código de propósito. Mudança comportamental da especificação nos CAs novos; a renumeração é editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Papéis da história com os três papéis da [DEC-25](../decisoes/DEC-25.md) ([CR-05](../mudancas/CR-05-atendente-e-gestor-nos-artefatos-mistos.md), REQ-13); os CAs seguem dizendo "Gestor" para o perfil. Mudança editorial, sem nova obrigação. Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-12 |
| **Título** | Ver o detalhe e o histórico de uma reserva |
| **História** | Como Solicitante ou Atendente responsável (o Gestor do serviço herda, no perfil Gestor), quero ver uma reserva com todos os dados e a linha do tempo das mudanças de situação para saber quem decidiu, quando e por quê. |
| **Valor** | Cada decisão fica explicada a quem pediu e rastreável para a instituição, com autor, momento e motivo ([NS-07](../visao.md#necessidades), [NS-12](../visao.md#necessidades)). |
| **Origem** | [UC-08 Consultar detalhe da reserva](../casos-de-uso/fichas-resumidas.md#uc-08) ([passos 1 a 3](../casos-de-uso/fichas-resumidas.md#uc08-p1), A3.1 a A3.3, E2.1) e a extensão [UC-09 Consultar histórico da reserva](../casos-de-uso/fichas-resumidas.md#uc-09) ([passos 1 a 3](../casos-de-uso/fichas-resumidas.md#uc09-p1), A3.1, A3.2, E2.1, E3.1), que mostra o que UC-13 grava. Dois casos de uso, uma fatia: o histórico só é visto a partir do detalhe. |
| **Prioridade** | Normal — [RF-14](../requisitos/rf-reservas.md#rf-14), [RF-22](../requisitos/rf-reservas.md#rf-22) e [RF-23](../requisitos/rf-reservas.md#rf-23) são normais. |
| **Estimativa (Custo em Semanas)** | 0,5 (retrospectiva: o histórico da RES-07, com a gravação na mesma transação, e a tela de detalhe com a linha do tempo da FE-06). |
| **Conversa** | "As tentativas recusadas aparecem no histórico?" → sim, desde que a reserva seja visível a quem consulta ([DEC-05](../decisoes/DEC-05.md), decidida na Aula 7; [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md), tarefa RES-12). "Um registro pode ser corrigido depois?" → não, é um fato ([RNF-R05](../requisitos/rnf.md#rnf-r05)). "As reservas antigas têm histórico?" → as gravadas antes do histórico não ([UC-09 A3.1](../casos-de-uso/fichas-resumidas.md#uc09-a3-1)). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). Os CAs marcados com implementação pendente só contam quando a tarefa citada os implementar e criar o TA deles. |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | O histórico só tem o que [US-08](US-08-solicitar-reserva.md) e [US-13](US-13-cancelar-uma-reserva.md) a [US-16](US-16-concluir-uma-reserva.md) gravam; sem elas, mostra só a criação. |
| **N** · Negociável | ✗ | O conteúdo do histórico segue a [DEC-05](../decisoes/DEC-05.md), já decidida: as tentativas recusadas entram, o que muda o CA do registro de fatos e as garantias de UC-10. |
| **V** · Valiosa | ✓ | É onde o Solicitante lê o motivo de uma recusa e a instituição confere quem decidiu. |
| **E** · Estimável | ✓ | Leitura de dados já gravados. |
| **S** · Small | ✗ | Junta duas consultas (detalhe e histórico), cada uma com a sua falha e o seu vazio. O corte seria "detalhe" × "linha do tempo"; não foi feito porque o histórico não tem outro ponto de entrada. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado. |

**Diagnóstico:** valiosa e testável, mas depende das histórias que gravam o histórico, tem o conteúdo definido pela DEC-05 e poderia ser menor.

## Critérios de aceite

#### <a id="us-12-ca-01"></a>US-12 · CA-01 · Detalhe da reserva (sucesso)

- **Dado** uma reserva Cancelada do Solicitante, com motivo
- **Quando** ele escolhe vê-la
- **Então** o sistema mostra o espaço pelo nome, a data e o horário, o solicitante com a matrícula, o momento do pedido (no formato "28/10/2026 às 14:05"), a finalidade, a situação com o motivo e as ações disponíveis para ele (nenhuma, nesta)
- **Origem:** [UC-08 passo 3](../casos-de-uso/fichas-resumidas.md#uc08-p3)
- **RF:** [RF-14](../requisitos/rf-reservas.md#rf-14), [RF-16](../requisitos/rf-reservas.md#rf-16)
- **TA:** [TA-125](#ta-125)

#### <a id="us-12-ca-02"></a>US-12 · CA-02 · Linha do tempo (sucesso)

- **Dado** uma reserva que foi solicitada pela Ana, confirmada e depois concluída pela Carla
- **Quando** alguém que pode vê-la consulta o histórico
- **Então** o sistema mostra, em ordem cronológica, "Solicitada por Ana…", "Confirmada por Carla…" e "Concluída por Carla…", cada um com data e hora no horário de Brasília, a situação anterior e a nova e o motivo, quando houver
- **Origem:** [UC-09 passo 3](../casos-de-uso/fichas-resumidas.md#uc09-p3), [UC-08 A3.1](../casos-de-uso/fichas-resumidas.md#uc08-a3-1)
- **RF:** [RF-22](../requisitos/rf-reservas.md#rf-22)
- **TA:** [TA-126](#ta-126)

#### <a id="us-12-ca-03"></a>US-12 · CA-03 · Tentativa recusada na linha do tempo (sucesso)

- **Dado** uma reserva Confirmada com uma tentativa recusada registrada depois da confirmação
- **Quando** o Gestor consulta o histórico
- **Então** a tentativa aparece na ordem cronológica, distinta das mudanças aceitas, e a situação atual continua Confirmada
- **Origem:** [UC-09 passo 3](../casos-de-uso/fichas-resumidas.md#uc09-p3)
- **RF:** [RF-22](../requisitos/rf-reservas.md#rf-22)
- **TA:** [TA-127](#ta-127)
- **Depende de:** [DEC-05](../decisoes/DEC-05.md) (decidida na Aula 7; regra aplicada na especificação pelo [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md), REQ-13)
- **Implementação:** implementação pendente (tarefa RES-12)

#### <a id="us-12-ca-04"></a>US-12 · CA-04 · Decidir a partir do detalhe (alternativa)

- **Dado** o detalhe de uma reserva Solicitada aberto pelo Gestor
- **Quando** ele escolhe uma das ações e a confirma
- **Então** o detalhe é mostrado de novo, já na situação nova, e o registro da mudança já aparece na linha do tempo; as ações oferecidas no detalhe são as mesmas da lista
- **Origem:** [UC-08 A3.2](../casos-de-uso/fichas-resumidas.md#uc08-a3-2), [UC-10 A1.1](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#a1-1) (pelo detalhe)
- **RF:** [RF-16](../requisitos/rf-reservas.md#rf-16), [RF-22](../requisitos/rf-reservas.md#rf-22)
- **TA:** [TA-128](#ta-128)

#### <a id="us-12-ca-05"></a>US-12 · CA-05 · Voltar às reservas com os mesmos critérios (alternativa)

- **Dado** um detalhe aberto a partir da lista filtrada por espaço e situação
- **Quando** a pessoa pede para voltar às reservas
- **Então** a lista volta com os mesmos critérios; quem abriu o detalhe direto, sem passar pela lista, volta para a lista sem critérios
- **Origem:** [UC-08 A3.3](../casos-de-uso/fichas-resumidas.md#uc08-a3-3), [UC-07 A2.1](../casos-de-uso/fichas-resumidas.md#uc07-a2-1)
- **RF:** [RF-14](../requisitos/rf-reservas.md#rf-14)
- **TA:** [TA-129](#ta-129)

#### <a id="us-12-ca-06"></a>US-12 · CA-06 · Reserva sem registros (alternativa)

- **Dado** uma reserva gravada antes de existir o histórico
- **Quando** o histórico dela é consultado
- **Então** o sistema informa "Nenhuma mudança registrada." e o detalhe continua completo
- **Origem:** [UC-09 A3.1](../casos-de-uso/fichas-resumidas.md#uc09-a3-1)
- **RF:** [RF-22](../requisitos/rf-reservas.md#rf-22)
- **TA:** [TA-130](#ta-130)

#### <a id="us-12-ca-07"></a>US-12 · CA-07 · Reserva inexistente ou de outra pessoa (exceção)

- **Dado** uma reserva de outra pessoa, uma identificação que não existe e uma identificação mal escrita
- **Quando** o Solicitante pede para ver cada uma
- **Então** o sistema responde a mesma coisa nos três casos — "Reserva não encontrada", que ela não existe ou não está disponível para ele —, oferece voltar às reservas e não mostra nem o detalhe nem o histórico, sem revelar que a reserva da outra pessoa existe
- **Origem:** [UC-08 E2.1](../casos-de-uso/fichas-resumidas.md#uc08-e2-1)
- **RF:** [RF-23](../requisitos/rf-reservas.md#rf-23)
- **TA:** [TA-131](#ta-131)

#### <a id="us-12-ca-08"></a>US-12 · CA-08 · Histórico de reserva inexistente ou de outra pessoa (exceção)

- **Dado** uma reserva de outra pessoa e uma identificação que não existe
- **Quando** o Solicitante pede o histórico de cada uma
- **Então** o sistema responde "Reserva de código «n» não encontrada." nos dois casos, e nenhum registro é mostrado
- **Origem:** [UC-09 E2.1](../casos-de-uso/fichas-resumidas.md#uc09-e2-1)
- **RF:** [RF-23](../requisitos/rf-reservas.md#rf-23)
- **TA:** [TA-132](#ta-132)

#### <a id="us-12-ca-09"></a>US-12 · CA-09 · Histórico não pôde ser obtido (exceção)

- **Dado** o detalhe de uma reserva carregado e uma falha de comunicação só ao consultar o histórico
- **Quando** a pessoa olha a reserva
- **Então** o detalhe continua visível, a seção do histórico informa que não foi possível carregá-lo e oferece tentar de novo, e tentar de novo consulta só o histórico
- **Origem:** [UC-09 E3.1](../casos-de-uso/fichas-resumidas.md#uc09-e3-1)
- **RF:** [RF-22](../requisitos/rf-reservas.md#rf-22)
- **TA:** [TA-133](#ta-133)

#### <a id="us-12-ca-10"></a>US-12 · CA-10 · O histórico é um registro de fatos (registro)

- **Dado** uma reserva com histórico e uma tentativa recusada sobre ela (por exemplo, recusar sem motivo)
- **Quando** o histórico é consultado, ou alguém tenta alterar ou excluir um registro dele
- **Então** a tentativa recusada não aparece (só as mudanças aceitas são registradas, diferente do modelo do professor), nenhum registro pode ser alterado nem excluído, e o autor aparece só pelo nome, sem a identificação interna de outra pessoa
- **Origem:** [UC-09 A3.2](../casos-de-uso/fichas-resumidas.md#uc09-a3-2)
- **RF:** [RF-22](../requisitos/rf-reservas.md#rf-22)
- **TA:** [TA-134](#ta-134)
- **Depende de:** [DEC-05](../decisoes/DEC-05.md)
- **Situação:** em parte substituído (a regra das tentativas recusadas) por [CA-11](#us-12-ca-11), [CA-03](#us-12-ca-03), pelo [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md) (REQ-13). Este CA e o TA dele descrevem a regra anterior, que o código ainda cumpre até a tarefa RES-12; não valem como prova da regra nova.

#### <a id="us-12-ca-11"></a>US-12 · CA-11 · O histórico é um registro de fatos, com as tentativas recusadas (registro)

- **Dado** uma reserva com histórico e uma tentativa recusada sobre ela (por exemplo, recusar sem motivo)
- **Quando** o histórico é consultado, ou alguém tenta alterar ou excluir um registro dele
- **Então** a tentativa recusada aparece, com o resultado e o código do erro, nenhum registro pode ser alterado nem excluído, e o autor aparece só pelo nome, sem a identificação interna de outra pessoa
- **Origem:** [UC-09 A3.2](../casos-de-uso/fichas-resumidas.md#uc09-a3-2)
- **RF:** [RF-22](../requisitos/rf-reservas.md#rf-22)
- **TA:** [TA-135](#ta-135)
- **Depende de:** [DEC-05](../decisoes/DEC-05.md) (decidida na Aula 7; regra aplicada na especificação pelo [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md), REQ-13)
- **Implementação:** implementação pendente (tarefa RES-12)

#### <a id="us-12-ca-12"></a>US-12 · CA-12 · Quem vê o detalhe e o histórico (acesso)

- **Dado** uma reserva de um Solicitante
- **Quando** o Gestor, o próprio Solicitante e uma pessoa não identificada pedem o detalhe e o histórico
- **Então** o Gestor e o dono veem os dois; a pessoa não identificada não vê nada e é orientada a entrar
- **Origem:** [UC-08 passo 2](../casos-de-uso/fichas-resumidas.md#uc08-p2), [UC-09 passo 2](../casos-de-uso/fichas-resumidas.md#uc09-p2)
- **RF:** [RF-14](../requisitos/rf-reservas.md#rf-14), [RF-23](../requisitos/rf-reservas.md#rf-23)
- **TA:** [TA-136](#ta-136)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-125"></a>TA-125 | [CA-01](#us-12-ca-01) | automatizado | `reservas/tests/test_api_consulta_reservas.py::test_detalhe_devolve_a_reserva_no_mesmo_formato_da_criacao`; `pages/PaginaReserva.test.tsx`: `mostra os dados da reserva com o nome do espaço e as datas formatadas`; `pages/PaginaReserva.test.tsx`: `mostra o motivo junto da situação quando houver`; `pages/PaginaReserva.test.tsx`: `sem ações, não mostra nenhum botão` |
| <a id="ta-126"></a>TA-126 | [CA-02](#us-12-ca-02) | automatizado | `reservas/tests/test_api_historico.py::test_fluxo_completo_aparece_no_historico_em_ordem`; `reservas/tests/test_api_historico.py::test_registrado_em_sai_em_iso_8601_no_fuso_de_sao_paulo`; `reservas/tests/test_api_historico.py::test_cancelamento_aparece_com_o_motivo`; `pages/PaginaReserva.test.tsx`: `mostra a linha do tempo em ordem, com data e hora, autor e motivo` |
| <a id="ta-127"></a>TA-127 | [CA-03](#us-12-ca-03) | pendente | implementação pendente (tarefa RES-12) — TA a criar junto com o código ([CR-02 · CA-04](../mudancas/CR-02-tentativas-recusadas-no-historico.md#5-critérios-de-aceite)). |
| <a id="ta-128"></a>TA-128 | [CA-04](#us-12-ca-04) | automatizado | `pages/PaginaReserva.test.tsx`: `os botões vêm de acoes_disponiveis, com nome acessível com contexto`; `pages/PaginaReserva.test.tsx`: `uma ação concluída recarrega a reserva e o histórico e põe o foco no título`; `pages/PaginaReserva.test.tsx`: `no 409, o diálogo oferece "Atualizar reserva", que recarrega o detalhe` |
| <a id="ta-129"></a>TA-129 | [CA-05](#us-12-ca-05) | automatizado | `pages/PaginaReserva.test.tsx`: `"Voltar para as reservas" volta para a lista com os filtros de antes`; `pages/PaginaReserva.test.tsx`: `quem entrou direto pelo link volta para /reservas`; `components/reservas/TabelaDeReservas.test.tsx`: `o link leva no state a URL da lista com os filtros, para o "Voltar"` |
| <a id="ta-130"></a>TA-130 | [CA-06](#us-12-ca-06) | automatizado | `pages/PaginaReserva.test.tsx`: `histórico vazio mostra "Nenhuma mudança registrada."` |
| <a id="ta-131"></a>TA-131 | [CA-07](#us-12-ca-07) | automatizado | `reservas/tests/test_api_permissoes.py::test_detalhe_de_outra_pessoa_para_o_solicitante_responde_404`; `reservas/tests/test_api_consulta_reservas.py::test_detalhe_inexistente_responde_404`; `pages/PaginaReserva.test.tsx`: `404 mostra "Reserva não encontrada", sem detalhe nem histórico`; `pages/PaginaReserva.test.tsx`: `id "%s" na URL mostra o mesmo estado, sem chamar a API` |
| <a id="ta-132"></a>TA-132 | [CA-08](#us-12-ca-08) | automatizado | `reservas/tests/test_api_historico.py::test_solicitante_pedindo_historico_de_outra_pessoa_recebe_404`; `reservas/tests/test_api_historico.py::test_historico_de_reserva_inexistente_responde_404` |
| <a id="ta-133"></a>TA-133 | [CA-09](#us-12-ca-09) | automatizado | `pages/PaginaReserva.test.tsx`: `se o histórico falhar, o erro fica só na seção e "Tentar novamente" busca de novo` |
| <a id="ta-134"></a>TA-134 | [CA-10](#us-12-ca-10) | automatizado | `reservas/tests/test_api_historico.py::test_tentativa_recusada_nao_aparece_no_historico`; `reservas/tests/test_api_historico.py::test_historico_nao_aceita_alteracao_nem_exclusao`; `reservas/tests/test_api_historico.py::test_registro_nao_expoe_o_id_do_autor` |
| <a id="ta-135"></a>TA-135 | [CA-11](#us-12-ca-11) | pendente | implementação pendente (tarefa RES-12) — TA a criar junto com o código ([CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md#4-diferença) (seção 4, o "depois")). |
| <a id="ta-136"></a>TA-136 | [CA-12](#us-12-ca-12) | automatizado | `reservas/tests/test_api_permissoes.py::test_gestor_ve_o_detalhe_de_qualquer_reserva`; `reservas/tests/test_api_consulta_reservas.py::test_detalhe_sem_login_responde_401`; `reservas/tests/test_api_historico.py::test_historico_sem_login_responde_401`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]` |
