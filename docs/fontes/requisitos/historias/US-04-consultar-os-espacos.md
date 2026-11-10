# US-04 · Consultar os espaços

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-04 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-04-consultar-os-espacos.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-19 e TA-20 passam a TA-20 e TA-21, e TA-21 a TA-158 passam a TA-24 a TA-161, para os TA-19, TA-22 e TA-23 novos da US-03 (revogação e troca da credencial de renovação) seguirem a ordem das histórias (AUT-09). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-24 a TA-31 passam a TA-28 a TA-35 (e os CAs seguintes na mesma história, quando há CA novo antes deles), para os 25 TAs pendentes novos seguirem a ordem das histórias (REQ-13). A especificação está adiante do código de propósito. Mudança comportamental da especificação nos CAs novos; a renumeração é editorial, sem nova obrigação. Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-04 |
| **Título** | Consultar os espaços |
| **História** | Como Solicitante, quero ver os espaços esportivos, com o tipo, a capacidade e se aceitam pedidos, para escolher onde pedir uma reserva. |
| **Valor** | Saber o que existe antes de pedir, sem perguntar ao setor dos espaços ([NS-01](../visao.md#necessidades)). |
| **Origem** | [UC-03 Consultar espaços, passos 1 a 3](../casos-de-uso/fichas-resumidas.md#uc03-p1), alternativas [A2.1 a A2.3](../casos-de-uso/fichas-resumidas.md#uc03-a2-1) e exceções [E2.1](../casos-de-uso/fichas-resumidas.md#uc03-e2-1) e [E2.2](../casos-de-uso/fichas-resumidas.md#uc03-e2-2). Vale também para o Gestor, por herança. |
| **Prioridade** | Normal — [RF-01](../requisitos/rf-espacos.md#rf-01), [RF-03](../requisitos/rf-espacos.md#rf-03) e [RF-09](../requisitos/rf-espacos.md#rf-09) são normais (F1 do enunciado). |
| **Estimativa (Custo em Semanas)** | 0,3 (retrospectiva: a listagem e os filtros da ESP-03 e a tela da FE-02). |
| **Conversa** | "Os espaços inativos aparecem para o Solicitante?" → sim, marcados como inativos e sem a opção de reservar. "Em que ordem?" → pelo nome, na ordem do banco: maiúsculas antes das minúsculas e letras acentuadas no fim ([auditoria do RF-01](../requisitos/srs.md#requisitos-funcionais)). "Precisa de paginação?" → não para o volume esperado ([L-05](../requisitos/srs.md#l-05)). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Para mostrar algo precisa de espaços cadastrados ([US-05](US-05-cadastrar-espaco.md)) e de uma pessoa identificada ([US-02](US-02-entrar-no-sistema.md)). |
| **N** · Negociável | ✓ | Os critérios de filtro e a ordem podem ser combinados sem mudar a meta. |
| **V** · Valiosa | ✓ | É por aqui que o Solicitante escolhe onde pedir. |
| **E** · Estimável | ✓ | Uma lista, dois filtros e um detalhe. |
| **S** · Small | ✓ | Cabe numa iteração curta, sem regra de negócio nova. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado. |

**Diagnóstico:** pequena, valiosa e testável; só depende de haver espaços (US-05) e de entrar (US-02).

## Critérios de aceite

#### <a id="us-04-ca-01"></a>US-04 · CA-01 · Lista de espaços (sucesso)

- **Dado** um Solicitante identificado e espaços cadastrados, ativos e inativos
- **Quando** ele pede para ver os espaços
- **Então** o sistema mostra todos, ordenados pelo nome (maiúsculas antes das minúsculas, letras acentuadas no fim), cada um com nome, tipo, capacidade e se está ativo, e informa quantos foram encontrados
- **Origem:** [UC-03 passo 2](../casos-de-uso/fichas-resumidas.md#uc03-p2)
- **RF:** [RF-01](../requisitos/rf-espacos.md#rf-01)
- **TA:** [TA-28](#ta-28)

#### <a id="us-04-ca-02"></a>US-04 · CA-02 · Escolher um espaço para reservar (sucesso)

- **Dado** a lista de espaços
- **Quando** o Solicitante escolhe reservar um espaço ativo
- **Então** o sistema abre o pedido de reserva com esse espaço já escolhido; os espaços inativos não oferecem essa opção
- **Origem:** [UC-03 passo 3](../casos-de-uso/fichas-resumidas.md#uc03-p3)
- **RF:** [RF-01](../requisitos/rf-espacos.md#rf-01)
- **TA:** [TA-29](#ta-29)

#### <a id="us-04-ca-03"></a>US-04 · CA-03 · Filtrar por tipo e por ativos (alternativa)

- **Dado** a lista de espaços
- **Quando** o Solicitante escolhe um dos tipos de espaço (que o sistema apresenta, na ordem do negócio), "somente ativos" ou os dois
- **Então** o sistema mostra só os espaços que atendem a todos os critérios escolhidos, com a quantidade, e os critérios continuam aplicados se a pessoa recarregar ou voltar à lista
- **Origem:** [UC-03 A2.1](../casos-de-uso/fichas-resumidas.md#uc03-a2-1)
- **RF:** [RF-02](../requisitos/rf-espacos.md#rf-02), [RF-04](../requisitos/rf-espacos.md#rf-04)
- **TA:** [TA-30](#ta-30)

#### <a id="us-04-ca-04"></a>US-04 · CA-04 · Filtro sem resultado (alternativa)

- **Dado** critérios que nenhum espaço atende
- **Quando** o Solicitante filtra a lista
- **Então** o sistema informa "Nenhum espaço encontrado." e oferece limpar os critérios, que volta à lista completa
- **Origem:** [UC-03 A2.1](../casos-de-uso/fichas-resumidas.md#uc03-a2-1)
- **RF:** [RF-02](../requisitos/rf-espacos.md#rf-02)
- **TA:** [TA-31](#ta-31)

#### <a id="us-04-ca-05"></a>US-04 · CA-05 · Ver um espaço (alternativa)

- **Dado** um espaço existente
- **Quando** o Solicitante pede para vê-lo
- **Então** o sistema mostra o nome, o tipo, a capacidade e se ele está ativo
- **Origem:** [UC-03 A2.2](../casos-de-uso/fichas-resumidas.md#uc03-a2-2)
- **RF:** [RF-03](../requisitos/rf-espacos.md#rf-03)
- **TA:** [TA-32](#ta-32)

#### <a id="us-04-ca-06"></a>US-04 · CA-06 · Tipo desconhecido no filtro (exceção)

- **Dado** a lista de espaços
- **Quando** o filtro pede um tipo que não é um dos tipos de espaço
- **Então** o sistema informa, no critério tipo, que o valor não é aceito; a lista não é filtrada e nenhum espaço muda
- **Origem:** [UC-03 E2.1](../casos-de-uso/fichas-resumidas.md#uc03-e2-1)
- **RF:** [RF-02.1](../requisitos/rf-espacos.md#rf-02-1)
- **TA:** [TA-33](#ta-33)

#### <a id="us-04-ca-07"></a>US-04 · CA-07 · Espaço inexistente (exceção)

- **Dado** uma identificação de espaço que não existe
- **Quando** o Solicitante pede para ver esse espaço
- **Então** o sistema informa "Espaço de código «n» não encontrado." e nenhum espaço muda
- **Origem:** [UC-03 E2.2](../casos-de-uso/fichas-resumidas.md#uc03-e2-2)
- **RF:** [RF-09](../requisitos/rf-espacos.md#rf-09)
- **TA:** [TA-34](#ta-34)

#### <a id="us-04-ca-08"></a>US-04 · CA-08 · Só o Gestor mantém espaços; sem identificação, nada (acesso)

- **Dado** um Solicitante identificado e, à parte, uma pessoa que não entrou
- **Quando** cada um pede para ver os espaços
- **Então** o Solicitante vê a lista sem nenhuma opção de cadastrar, editar, desativar ou reativar (essas ficam só com o Gestor), e quem não entrou não vê nenhum espaço e é levado a se identificar
- **Origem:** [UC-03 A2.3](../casos-de-uso/fichas-resumidas.md#uc03-a2-3)
- **RF:** [RF-01](../requisitos/rf-espacos.md#rf-01), [RF-10](../requisitos/rf-espacos.md#rf-10)
- **TA:** [TA-35](#ta-35)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-28"></a>TA-28 | [CA-01](#us-04-ca-01) | automatizado | `espacos/tests/test_api_espacos.py::test_listar_ordena_por_nome`; `espacos/tests/test_api_espacos.py::test_listar_informa_a_quantidade_encontrada [x]`; `espacos/tests/test_api_espacos.py::test_solicitante_lista_espacos`; `pages/PaginaEspacos.test.tsx`: `mostra a mensagem de contagem e os espaços na tabela` |
| <a id="ta-29"></a>TA-29 | [CA-02](#us-04-ca-02) | automatizado | `components/espacos/TabelaDeEspacos.test.tsx`: `mostra "Reservar" só nos espaços ativos, apontando para a nova reserva` |
| <a id="ta-30"></a>TA-30 | [CA-03](#us-04-ca-03) | automatizado | `espacos/tests/test_api_espacos.py::test_listar_aplica_os_filtros_da_query_string [x]`; `espacos/tests/test_api_espacos.py::test_tipos_de_espaco_lista_todos_os_tipos_na_ordem_do_enum`; `pages/PaginaEspacos.test.tsx`: `mudar os filtros grava na URL e busca com eles` |
| <a id="ta-31"></a>TA-31 | [CA-04](#us-04-ca-04) | automatizado | `pages/PaginaEspacos.test.tsx`: `lê os filtros da URL e, sem resultado, "Limpar filtros" limpa a URL e busca de novo` |
| <a id="ta-32"></a>TA-32 | [CA-05](#us-04-ca-05) | automatizado | `espacos/tests/test_api_espacos.py::test_obter_espaco_existente_responde_200_com_o_espaco`; `espacos/tests/test_api_espacos.py::test_solicitante_obtem_o_detalhe_de_um_espaco` |
| <a id="ta-33"></a>TA-33 | [CA-06](#us-04-ca-06) | automatizado | `espacos/tests/test_api_espacos.py::test_listar_com_tipo_desconhecido_no_filtro_responde_400` |
| <a id="ta-34"></a>TA-34 | [CA-07](#us-04-ca-07) | automatizado | `espacos/tests/test_api_espacos.py::test_obter_espaco_inexistente_responde_404` |
| <a id="ta-35"></a>TA-35 | [CA-08](#us-04-ca-08) | automatizado | `pages/PaginaEspacos.test.tsx`: `para o solicitante, a tabela não tem editar, desativar nem reativar`; `pages/PaginaEspacos.test.tsx`: `para o solicitante, troca o formulário por um aviso e lista os espaços`; `espacos/tests/test_api_espacos.py::test_consultar_espacos_sem_login_responde_401`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]` |
