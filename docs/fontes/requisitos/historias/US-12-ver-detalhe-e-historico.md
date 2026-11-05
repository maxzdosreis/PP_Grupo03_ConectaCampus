# US-12 · Ver o detalhe e o histórico de uma reserva

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-12 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-12-ver-detalhe-e-historico.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-12 |
| **Título** | Ver o detalhe e o histórico de uma reserva |
| **História** | Como Solicitante (ou Gestor), quero ver uma reserva com todos os dados e a linha do tempo das mudanças de situação para saber quem decidiu, quando e por quê. |
| **Valor** | Cada decisão fica explicada a quem pediu e rastreável para a instituição, com autor, momento e motivo ([NS-07](../visao.md#necessidades), [NS-12](../visao.md#necessidades)). |
| **Origem** | [UC-08 Consultar detalhe da reserva](../casos-de-uso/fichas-resumidas.md#uc-08) ([passos 1 a 3](../casos-de-uso/fichas-resumidas.md#uc08-p1), A3.1 a A3.3, E2.1) e a extensão [UC-09 Consultar histórico da reserva](../casos-de-uso/fichas-resumidas.md#uc-09) ([passos 1 a 3](../casos-de-uso/fichas-resumidas.md#uc09-p1), A3.1, A3.2, E2.1, E3.1), que mostra o que UC-13 grava. Dois casos de uso, uma fatia: o histórico só é visto a partir do detalhe. |
| **Prioridade** | Normal — [RF-14](../requisitos/rf-reservas.md#rf-14), [RF-22](../requisitos/rf-reservas.md#rf-22) e [RF-23](../requisitos/rf-reservas.md#rf-23) são normais. |
| **Estimativa (Custo em Semanas)** | 0,5 (retrospectiva: o histórico da RES-07, com a gravação na mesma transação, e a tela de detalhe com a linha do tempo da FE-06). |
| **Conversa** | "As tentativas recusadas aparecem no histórico?" → não, só as mudanças aceitas ([DEC-05](../decisoes/DEC-05.md), adotada provisoriamente; difere do modelo do professor). "Um registro pode ser corrigido depois?" → não, é um fato ([RNF-R05](../requisitos/rnf.md#rnf-r05)). "As reservas antigas têm histórico?" → as gravadas antes do histórico não ([UC-09 A3.1](../casos-de-uso/fichas-resumidas.md#uc09-a3-1)). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | O histórico só tem o que [US-08](US-08-solicitar-reserva.md) e [US-13](US-13-cancelar-uma-reserva.md) a [US-16](US-16-concluir-uma-reserva.md) gravam; sem elas, mostra só a criação. |
| **N** · Negociável | ✗ | O conteúdo do histórico está preso à [DEC-05](../decisoes/DEC-05.md): registrar as tentativas recusadas mudaria o CA-09 e as garantias de UC-10. |
| **V** · Valiosa | ✓ | É onde o Solicitante lê o motivo de uma recusa e a instituição confere quem decidiu. |
| **E** · Estimável | ✓ | Leitura de dados já gravados. |
| **S** · Small | ✗ | Junta duas consultas (detalhe e histórico), cada uma com a sua falha e o seu vazio. O corte seria "detalhe" × "linha do tempo"; não foi feito porque o histórico não tem outro ponto de entrada. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado. |

**Diagnóstico:** valiosa e testável, mas depende das histórias que gravam o histórico, ainda não é negociável (DEC-05) e poderia ser menor.

## Critérios de aceite

#### <a id="us-12-ca-01"></a>US-12 · CA-01 · Detalhe da reserva (sucesso)

- **Dado** uma reserva Cancelada do Solicitante, com motivo
- **Quando** ele escolhe vê-la
- **Então** o sistema mostra o espaço pelo nome, a data e o horário, o solicitante com a matrícula, o momento do pedido (no formato "28/10/2026 às 14:05"), a finalidade, a situação com o motivo e as ações disponíveis para ele (nenhuma, nesta)
- **Origem:** [UC-08 passo 3](../casos-de-uso/fichas-resumidas.md#uc08-p3)
- **RF:** [RF-14](../requisitos/rf-reservas.md#rf-14), [RF-16](../requisitos/rf-reservas.md#rf-16)
- **TA:** [TA-104](#ta-104)

#### <a id="us-12-ca-02"></a>US-12 · CA-02 · Linha do tempo (sucesso)

- **Dado** uma reserva que foi solicitada pela Ana, confirmada e depois concluída pela Carla
- **Quando** alguém que pode vê-la consulta o histórico
- **Então** o sistema mostra, em ordem cronológica, "Solicitada por Ana…", "Confirmada por Carla…" e "Concluída por Carla…", cada um com data e hora no horário de Brasília, a situação anterior e a nova e o motivo, quando houver
- **Origem:** [UC-09 passo 3](../casos-de-uso/fichas-resumidas.md#uc09-p3), [UC-08 A3.1](../casos-de-uso/fichas-resumidas.md#uc08-a3-1)
- **RF:** [RF-22](../requisitos/rf-reservas.md#rf-22)
- **TA:** [TA-105](#ta-105)

#### <a id="us-12-ca-03"></a>US-12 · CA-03 · Decidir a partir do detalhe (alternativa)

- **Dado** o detalhe de uma reserva Solicitada aberto pelo Gestor
- **Quando** ele escolhe uma das ações e a confirma
- **Então** o detalhe é mostrado de novo, já na situação nova, e o registro da mudança já aparece na linha do tempo; as ações oferecidas no detalhe são as mesmas da lista
- **Origem:** [UC-08 A3.2](../casos-de-uso/fichas-resumidas.md#uc08-a3-2), [UC-10 A1.1](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#a1-1) (pelo detalhe)
- **RF:** [RF-16](../requisitos/rf-reservas.md#rf-16), [RF-22](../requisitos/rf-reservas.md#rf-22)
- **TA:** [TA-106](#ta-106)

#### <a id="us-12-ca-04"></a>US-12 · CA-04 · Voltar às reservas com os mesmos critérios (alternativa)

- **Dado** um detalhe aberto a partir da lista filtrada por espaço e situação
- **Quando** a pessoa pede para voltar às reservas
- **Então** a lista volta com os mesmos critérios; quem abriu o detalhe direto, sem passar pela lista, volta para a lista sem critérios
- **Origem:** [UC-08 A3.3](../casos-de-uso/fichas-resumidas.md#uc08-a3-3), [UC-07 A2.1](../casos-de-uso/fichas-resumidas.md#uc07-a2-1)
- **RF:** [RF-14](../requisitos/rf-reservas.md#rf-14)
- **TA:** [TA-107](#ta-107)

#### <a id="us-12-ca-05"></a>US-12 · CA-05 · Reserva sem registros (alternativa)

- **Dado** uma reserva gravada antes de existir o histórico
- **Quando** o histórico dela é consultado
- **Então** o sistema informa "Nenhuma mudança registrada." e o detalhe continua completo
- **Origem:** [UC-09 A3.1](../casos-de-uso/fichas-resumidas.md#uc09-a3-1)
- **RF:** [RF-22](../requisitos/rf-reservas.md#rf-22)
- **TA:** [TA-108](#ta-108)

#### <a id="us-12-ca-06"></a>US-12 · CA-06 · Reserva inexistente ou de outra pessoa (exceção)

- **Dado** uma reserva de outra pessoa, uma identificação que não existe e uma identificação mal escrita
- **Quando** o Solicitante pede para ver cada uma
- **Então** o sistema responde a mesma coisa nos três casos — "Reserva não encontrada", que ela não existe ou não está disponível para ele —, oferece voltar às reservas e não mostra nem o detalhe nem o histórico, sem revelar que a reserva da outra pessoa existe
- **Origem:** [UC-08 E2.1](../casos-de-uso/fichas-resumidas.md#uc08-e2-1)
- **RF:** [RF-23](../requisitos/rf-reservas.md#rf-23)
- **TA:** [TA-109](#ta-109)

#### <a id="us-12-ca-07"></a>US-12 · CA-07 · Histórico de reserva inexistente ou de outra pessoa (exceção)

- **Dado** uma reserva de outra pessoa e uma identificação que não existe
- **Quando** o Solicitante pede o histórico de cada uma
- **Então** o sistema responde "Reserva de código «n» não encontrada." nos dois casos, e nenhum registro é mostrado
- **Origem:** [UC-09 E2.1](../casos-de-uso/fichas-resumidas.md#uc09-e2-1)
- **RF:** [RF-23](../requisitos/rf-reservas.md#rf-23)
- **TA:** [TA-110](#ta-110)

#### <a id="us-12-ca-08"></a>US-12 · CA-08 · Histórico não pôde ser obtido (exceção)

- **Dado** o detalhe de uma reserva carregado e uma falha de comunicação só ao consultar o histórico
- **Quando** a pessoa olha a reserva
- **Então** o detalhe continua visível, a seção do histórico informa que não foi possível carregá-lo e oferece tentar de novo, e tentar de novo consulta só o histórico
- **Origem:** [UC-09 E3.1](../casos-de-uso/fichas-resumidas.md#uc09-e3-1)
- **RF:** [RF-22](../requisitos/rf-reservas.md#rf-22)
- **TA:** [TA-111](#ta-111)

#### <a id="us-12-ca-09"></a>US-12 · CA-09 · O histórico é um registro de fatos (registro)

- **Dado** uma reserva com histórico e uma tentativa recusada sobre ela (por exemplo, recusar sem motivo)
- **Quando** o histórico é consultado, ou alguém tenta alterar ou excluir um registro dele
- **Então** a tentativa recusada não aparece (só as mudanças aceitas são registradas, diferente do modelo do professor), nenhum registro pode ser alterado nem excluído, e o autor aparece só pelo nome, sem a identificação interna de outra pessoa
- **Origem:** [UC-09 A3.2](../casos-de-uso/fichas-resumidas.md#uc09-a3-2)
- **RF:** [RF-22](../requisitos/rf-reservas.md#rf-22)
- **TA:** [TA-112](#ta-112)
- **Depende de:** [DEC-05](../decisoes/DEC-05.md)

#### <a id="us-12-ca-10"></a>US-12 · CA-10 · Quem vê o detalhe e o histórico (acesso)

- **Dado** uma reserva de um Solicitante
- **Quando** o Gestor, o próprio Solicitante e uma pessoa não identificada pedem o detalhe e o histórico
- **Então** o Gestor e o dono veem os dois; a pessoa não identificada não vê nada e é orientada a entrar
- **Origem:** [UC-08 passo 2](../casos-de-uso/fichas-resumidas.md#uc08-p2), [UC-09 passo 2](../casos-de-uso/fichas-resumidas.md#uc09-p2)
- **RF:** [RF-14](../requisitos/rf-reservas.md#rf-14), [RF-23](../requisitos/rf-reservas.md#rf-23)
- **TA:** [TA-113](#ta-113)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-104"></a>TA-104 | [CA-01](#us-12-ca-01) | automatizado | `reservas/tests/test_api_consulta_reservas.py::test_detalhe_devolve_a_reserva_no_mesmo_formato_da_criacao`; `pages/PaginaReserva.test.tsx`: `mostra os dados da reserva com o nome do espaço e as datas formatadas`; `pages/PaginaReserva.test.tsx`: `mostra o motivo junto da situação quando houver`; `pages/PaginaReserva.test.tsx`: `sem ações, não mostra nenhum botão` |
| <a id="ta-105"></a>TA-105 | [CA-02](#us-12-ca-02) | automatizado | `reservas/tests/test_api_historico.py::test_fluxo_completo_aparece_no_historico_em_ordem`; `reservas/tests/test_api_historico.py::test_registrado_em_sai_em_iso_8601_no_fuso_de_sao_paulo`; `reservas/tests/test_api_historico.py::test_cancelamento_aparece_com_o_motivo`; `pages/PaginaReserva.test.tsx`: `mostra a linha do tempo em ordem, com data e hora, autor e motivo` |
| <a id="ta-106"></a>TA-106 | [CA-03](#us-12-ca-03) | automatizado | `pages/PaginaReserva.test.tsx`: `os botões vêm de acoes_disponiveis, com nome acessível com contexto`; `pages/PaginaReserva.test.tsx`: `uma ação concluída recarrega a reserva e o histórico e põe o foco no título`; `pages/PaginaReserva.test.tsx`: `no 409, o diálogo oferece "Atualizar reserva", que recarrega o detalhe` |
| <a id="ta-107"></a>TA-107 | [CA-04](#us-12-ca-04) | automatizado | `pages/PaginaReserva.test.tsx`: `"Voltar para as reservas" volta para a lista com os filtros de antes`; `pages/PaginaReserva.test.tsx`: `quem entrou direto pelo link volta para /reservas`; `components/reservas/TabelaDeReservas.test.tsx`: `o link leva no state a URL da lista com os filtros, para o "Voltar"` |
| <a id="ta-108"></a>TA-108 | [CA-05](#us-12-ca-05) | automatizado | `pages/PaginaReserva.test.tsx`: `histórico vazio mostra "Nenhuma mudança registrada."` |
| <a id="ta-109"></a>TA-109 | [CA-06](#us-12-ca-06) | automatizado | `reservas/tests/test_api_permissoes.py::test_detalhe_de_outra_pessoa_para_o_solicitante_responde_404`; `reservas/tests/test_api_consulta_reservas.py::test_detalhe_inexistente_responde_404`; `pages/PaginaReserva.test.tsx`: `404 mostra "Reserva não encontrada", sem detalhe nem histórico`; `pages/PaginaReserva.test.tsx`: `id "%s" na URL mostra o mesmo estado, sem chamar a API` |
| <a id="ta-110"></a>TA-110 | [CA-07](#us-12-ca-07) | automatizado | `reservas/tests/test_api_historico.py::test_solicitante_pedindo_historico_de_outra_pessoa_recebe_404`; `reservas/tests/test_api_historico.py::test_historico_de_reserva_inexistente_responde_404` |
| <a id="ta-111"></a>TA-111 | [CA-08](#us-12-ca-08) | automatizado | `pages/PaginaReserva.test.tsx`: `se o histórico falhar, o erro fica só na seção e "Tentar novamente" busca de novo` |
| <a id="ta-112"></a>TA-112 | [CA-09](#us-12-ca-09) | automatizado | `reservas/tests/test_api_historico.py::test_tentativa_recusada_nao_aparece_no_historico`; `reservas/tests/test_api_historico.py::test_historico_nao_aceita_alteracao_nem_exclusao`; `reservas/tests/test_api_historico.py::test_registro_nao_expoe_o_id_do_autor` |
| <a id="ta-113"></a>TA-113 | [CA-10](#us-12-ca-10) | automatizado | `reservas/tests/test_api_permissoes.py::test_gestor_ve_o_detalhe_de_qualquer_reserva`; `reservas/tests/test_api_consulta_reservas.py::test_detalhe_sem_login_responde_401`; `reservas/tests/test_api_historico.py::test_historico_sem_login_responde_401`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]` |
