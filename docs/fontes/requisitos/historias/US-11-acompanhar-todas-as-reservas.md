# US-11 · Acompanhar todas as reservas

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-11 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-11-acompanhar-todas-as-reservas.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-19 e TA-20 passam a TA-20 e TA-21, e TA-21 a TA-158 passam a TA-24 a TA-161, para os TA-19, TA-22 e TA-23 novos da US-03 (revogação e troca da credencial de renovação) seguirem a ordem das histórias (AUT-09). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Consulta em páginas (RES-10, [RF-12.2](../requisitos/rf-reservas.md#rf-12-2)): CAs novos CA-04 (todas em páginas, com o total), CA-07 (outra página com os mesmos critérios) e CA-08 (mudar um critério volta à primeira página), com os TA-108, TA-111 e TA-112; o CA-09 (antigo CA-06) inclui a página e o tamanho inválidos. Renumeração: os CA-04 a CA-07 passam a CA-05, CA-06, CA-09 e CA-10, e os TA-101 a TA-107 passam a TA-105, TA-106, TA-107, TA-109, TA-110, TA-113 e TA-114, para os TA novos da US-10 e desta história seguirem a ordem das histórias. Conversa: a pergunta sobre milhares de reservas respondida pela RES-10 ([L-05](../requisitos/srs.md#l-05) resolvida). Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-11 |
| **Título** | Acompanhar todas as reservas |
| **História** | Como Gestor, quero localizar reservas por espaço, situação, data e solicitante, combinados, para encontrar rápido os pedidos que esperam a minha decisão. |
| **Valor** | O Gestor decide sobre os pedidos sem conferir um calendário à mão, e vê em cada um só as ações que fazem sentido ([NS-08](../visao.md#necessidades), [NS-09](../visao.md#necessidades)). |
| **Origem** | [UC-07 Consultar reservas](../casos-de-uso/fichas-resumidas.md#uc-07), no papel do Gestor: [passos 1 a 4](../casos-de-uso/fichas-resumidas.md#uc07-p1), alternativas [A2.3](../casos-de-uso/fichas-resumidas.md#uc07-a2-3), [A3.2](../casos-de-uso/fichas-resumidas.md#uc07-a3-2) e [A4.1](../casos-de-uso/fichas-resumidas.md#uc07-a4-1) e exceção [E3.1](../casos-de-uso/fichas-resumidas.md#uc07-e3-1). O papel do Solicitante é a [US-10](US-10-acompanhar-minhas-reservas.md). |
| **Prioridade** | Normal — [RF-12](../requisitos/rf-reservas.md#rf-12) e [RF-13](../requisitos/rf-reservas.md#rf-13) são normais (F3 do enunciado: "pelo menos dois critérios"); [RF-12.2](../requisitos/rf-reservas.md#rf-12-2), a consulta em páginas, é esperado. |
| **Estimativa (Custo em Semanas)** | 0,4 (retrospectiva: os filtros combinados da RES-05 e a tela de consulta da FE-04, com os filtros no endereço e o solicitante digitado). |
| **Conversa** | "Quais são os dois critérios do enunciado?" → todos funcionam sozinhos e combinados, o que atende às duas leituras. "O Gestor também pede reservas e quer ver só as dele?" → sim, com "somente as minhas" ([L-10](../requisitos/srs.md#l-10)). "E se forem milhares de reservas?" → a lista vem em páginas de até 20, na ordem pelo início, com o total; medida com 5.000 reservas dentro da meta ([L-05](../requisitos/srs.md#l-05), resolvida pela RES-10). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Precisa de reservas ([US-08](US-08-solicitar-reserva.md)) e repete a mesma consulta de [US-10](US-10-acompanhar-minhas-reservas.md), com mais critérios. |
| **N** · Negociável | ✓ | Os critérios, a busca por trecho do nome e a ordem podem ser combinados com o setor. |
| **V** · Valiosa | ✓ | É a fila de trabalho do Gestor. |
| **E** · Estimável | ✓ | Critérios conhecidos e somados. |
| **S** · Small | ✓ | Uma consulta, com os mesmos critérios somados. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado. |

**Diagnóstico:** pequena, valiosa e testável, mas não é independente de US-08 e US-10.

## Critérios de aceite

#### <a id="us-11-ca-01"></a>US-11 · CA-01 · Todas as reservas (sucesso)

- **Dado** reservas de vários solicitantes e um Gestor identificado
- **Quando** o Gestor pede para ver as reservas, sem critério
- **Então** o sistema mostra todas, sob o título "Reservas", ordenadas pelo início, cada uma com data e horário, espaço, solicitante (nome e matrícula), finalidade e situação, informa quantas foram encontradas, e a consulta não muda nenhuma reserva
- **Origem:** [UC-07 passo 2](../casos-de-uso/fichas-resumidas.md#uc07-p2)
- **RF:** [RF-12](../requisitos/rf-reservas.md#rf-12)
- **TA:** [TA-105](#ta-105)

#### <a id="us-11-ca-02"></a>US-11 · CA-02 · Critérios combinados (sucesso)

- **Dado** a lista de todas as reservas
- **Quando** o Gestor informa espaço, situação, data e um trecho do nome ou da matrícula do solicitante (sem diferenciar maiúsculas), sozinhos ou combinados
- **Então** o sistema mostra só as reservas que atendem a todos os critérios, com a quantidade; o trecho do solicitante só é aplicado depois que ele para de digitar, numa consulta só
- **Origem:** [UC-07 passos 3 e 4](../casos-de-uso/fichas-resumidas.md#uc07-p3)
- **RF:** [RF-12](../requisitos/rf-reservas.md#rf-12), [RF-15](../requisitos/rf-reservas.md#rf-15)
- **TA:** [TA-106](#ta-106)

#### <a id="us-11-ca-03"></a>US-11 · CA-03 · As ações do Gestor em cada reserva (sucesso)

- **Dado** reservas Solicitada, Confirmada e Concluída
- **Quando** o Gestor as vê na lista
- **Então** a Solicitada oferece "Confirmar", "Recusar" e "Cancelar"; a Confirmada, "Cancelar" e "Concluir"; e a Concluída, nenhuma ação
- **Origem:** [UC-07 passo 2](../casos-de-uso/fichas-resumidas.md#uc07-p2), [UC-10 A1.1](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#a1-1) (pela consulta)
- **RF:** [RF-16](../requisitos/rf-reservas.md#rf-16)
- **TA:** [TA-107](#ta-107)

#### <a id="us-11-ca-04"></a>US-11 · CA-04 · Todas em páginas, com o total (sucesso)

- **Dado** mais reservas do que cabem numa página, de vários solicitantes
- **Quando** o Gestor pede para ver as reservas, sem critério
- **Então** o sistema mostra a primeira página, com até 20 reservas ordenadas pelo início, e informa o total de reservas, a página atual e o número de páginas
- **Origem:** [UC-07 passo 2](../casos-de-uso/fichas-resumidas.md#uc07-p2)
- **RF:** [RF-12.2](../requisitos/rf-reservas.md#rf-12-2)
- **TA:** [TA-108](#ta-108)

#### <a id="us-11-ca-05"></a>US-11 · CA-05 · Somente as minhas (alternativa)

- **Dado** um Gestor que também pediu reservas em nome próprio
- **Quando** ele escolhe "somente as minhas"
- **Então** o sistema mostra só as reservas em que ele é o solicitante
- **Origem:** [UC-07 passo 3](../casos-de-uso/fichas-resumidas.md#uc07-p3)
- **RF:** [RF-13](../requisitos/rf-reservas.md#rf-13)
- **TA:** [TA-109](#ta-109)

#### <a id="us-11-ca-06"></a>US-11 · CA-06 · Nenhuma reserva atende (alternativa)

- **Dado** critérios que nenhuma reserva atende
- **Quando** o Gestor consulta
- **Então** o sistema informa "Nenhuma reserva encontrada." e oferece limpar os critérios, que só aparece quando há algum critério e volta à lista completa
- **Origem:** [UC-07 A4.1](../casos-de-uso/fichas-resumidas.md#uc07-a4-1)
- **RF:** [RF-12](../requisitos/rf-reservas.md#rf-12)
- **TA:** [TA-110](#ta-110)

#### <a id="us-11-ca-07"></a>US-11 · CA-07 · Outra página, com os mesmos critérios (alternativa)

- **Dado** o Gestor com um critério informado e um resultado de três páginas
- **Quando** ele pede a página seguinte, depois a anterior, ou abre uma reserva da segunda página e volta
- **Então** o sistema mostra aquela página do mesmo resultado, com o mesmo total e os mesmos critérios, e a volta do detalhe leva de novo à segunda página
- **Origem:** [UC-07 A2.3](../casos-de-uso/fichas-resumidas.md#uc07-a2-3)
- **RF:** [RF-12.2](../requisitos/rf-reservas.md#rf-12-2)
- **TA:** [TA-111](#ta-111)

#### <a id="us-11-ca-08"></a>US-11 · CA-08 · Mudar um critério volta à primeira página (alternativa)

- **Dado** o Gestor vendo a terceira página do resultado
- **Quando** ele escolhe outra situação
- **Então** o sistema mostra a primeira página do novo resultado, e não a terceira
- **Origem:** [UC-07 A3.2](../casos-de-uso/fichas-resumidas.md#uc07-a3-2)
- **RF:** [RF-12.2](../requisitos/rf-reservas.md#rf-12-2)
- **TA:** [TA-112](#ta-112)

#### <a id="us-11-ca-09"></a>US-11 · CA-09 · Critério em formato inválido (exceção)

- **Dado** a lista de todas as reservas
- **Quando** a consulta do Gestor traz uma situação desconhecida, uma data que não existe, um espaço que não é um número, uma página que não é um número inteiro a partir de 1 ou um tamanho de página fora de 1 a 100
- **Então** o sistema informa "Verifique os dados informados." apontando o critério com problema, e nenhuma reserva muda
- **Origem:** [UC-07 E3.1](../casos-de-uso/fichas-resumidas.md#uc07-e3-1)
- **RF:** [RF-12.1](../requisitos/rf-reservas.md#rf-12-1)
- **TA:** [TA-113](#ta-113)

#### <a id="us-11-ca-10"></a>US-11 · CA-10 · Ver todas depende do perfil atual (acesso)

- **Dado** um Gestor que a Equipe de TI rebaixou a Solicitante enquanto ele estava identificado
- **Quando** ele consulta as reservas de novo, sem entrar outra vez
- **Então** ele passa a ver só as próprias, e a reserva de outra pessoa que via antes passa a ser tratada como inexistente
- **Origem:** [UC-07 passo 2](../casos-de-uso/fichas-resumidas.md#uc07-p2)
- **RF:** [RF-13](../requisitos/rf-reservas.md#rf-13), [RF-23](../requisitos/rf-reservas.md#rf-23)
- **TA:** [TA-114](#ta-114)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-105"></a>TA-105 | [CA-01](#us-11-ca-01) | automatizado | `reservas/tests/test_api_consulta_reservas.py::test_consulta_sem_filtros_devolve_todas_ordenadas_por_inicio`; `reservas/tests/test_api_consulta_reservas.py::test_consulta_nao_altera_as_reservas`; `reservas/tests/test_api_permissoes.py::test_gestor_lista_todas_e_filtra_por_solicitante`; `pages/PaginaReservas.test.tsx`: `mostra a contagem e cada reserva com data, espaço, solicitante e situação`; `pages/PaginaReservas.test.tsx`: `para o gestor, o título é "Reservas" e há os filtros de solicitante` |
| <a id="ta-106"></a>TA-106 | [CA-02](#us-11-ca-02) | automatizado | `reservas/tests/test_api_consulta_reservas.py::test_criterios_combinados_se_somam`; `reservas/tests/test_api_consulta_reservas.py::test_cada_criterio_sozinho_devolve_so_as_correspondentes`; `reservas/tests/test_api_consulta_reservas.py::test_filtro_em_branco_e_ignorado`; `pages/PaginaReservas.test.tsx`: `combina espaço e situação numa mesma consulta`; `pages/PaginaReservas.test.tsx`: `o filtro de solicitante consulta uma vez só, depois que a pessoa para de digitar` |
| <a id="ta-107"></a>TA-107 | [CA-03](#us-11-ca-03) | automatizado | `reservas/tests/test_api_situacao_reserva.py::test_reserva_solicitada_traz_confirmar_recusar_e_cancelar`; `reservas/tests/test_api_situacao_reserva.py::test_reserva_confirmada_traz_cancelar_e_concluir`; `reservas/tests/test_api_situacao_reserva.py::test_reserva_concluida_nao_traz_acoes`; `reservas/tests/test_api_permissoes.py::test_acoes_do_gestor_na_solicitada_sao_confirmar_recusar_e_cancelar` |
| <a id="ta-108"></a>TA-108 | [CA-04](#us-11-ca-04) | automatizado | `reservas/tests/test_api_paginacao_de_reservas.py::test_sem_parametros_devolve_a_primeira_pagina_de_20_com_o_total`; `reservas/tests/test_api_paginacao_de_reservas.py::test_pagina_e_tamanho_escolhem_o_trecho_na_ordem_por_inicio`; `reservas/tests/test_api_paginacao_de_reservas.py::test_tamanho_no_maximo_e_aceito`; `reservas/tests/test_repositorio_reservas.py::test_listar_pagina_no_banco_com_count_e_limit`; `reservas/tests/test_consultar_reservas.py::test_consultar_devolve_a_pagina_pedida_com_o_total`; `pages/PaginaReservas.test.tsx`: `a navegação só aparece quando há mais de uma página` |
| <a id="ta-109"></a>TA-109 | [CA-05](#us-11-ca-05) | automatizado | `pages/PaginaReservas.test.tsx`: `"Somente minhas reservas" consulta com minhas=true`; `reservas/tests/test_api_consulta_reservas.py::test_cada_criterio_sozinho_devolve_so_as_correspondentes` |
| <a id="ta-110"></a>TA-110 | [CA-06](#us-11-ca-06) | automatizado | `pages/PaginaReservas.test.tsx`: `com filtros e sem reservas, oferece "Limpar filtros"`; `pages/PaginaReservas.test.tsx`: `"Limpar filtros" só aparece com filtro ativo e limpa a URL e os campos` |
| <a id="ta-111"></a>TA-111 | [CA-07](#us-11-ca-07) | automatizado | `reservas/tests/test_api_paginacao_de_reservas.py::test_filtros_combinados_com_a_paginacao`; `pages/PaginaReservas.test.tsx`: `"Próxima" e "Anterior" mudam a página na URL e consultam com ela`; `pages/PaginaReservas.test.tsx`: `desabilita "Próxima" na última página`; `pages/PaginaReservas.test.tsx`: `depois de mudar de página, o foco vai para a região da tabela`; `pages/PaginaReservas.test.tsx`: `mudar de página entra no histórico, e voltar no navegador volta à página anterior`; `pages/PaginaReservas.test.tsx`: `abrir uma reserva da página 2 e voltar leva de novo à página 2`; `components/reservas/PaginacaoDeReservas.test.tsx`: `"Anterior" fica desabilitado na primeira página e "Próxima" na última` |
| <a id="ta-112"></a>TA-112 | [CA-08](#us-11-ca-08) | automatizado | `pages/PaginaReservas.test.tsx`: `trocar um filtro volta à primeira página` |
| <a id="ta-113"></a>TA-113 | [CA-09](#us-11-ca-09) | automatizado | `reservas/tests/test_api_consulta_reservas.py::test_filtro_invalido_responde_400_com_o_campo`; `reservas/tests/test_api_paginacao_de_reservas.py::test_pagina_ou_tamanho_invalidos_respondem_400_com_o_campo`; `reservas/tests/test_api_paginacao_de_reservas.py::test_pagina_ou_tamanho_em_branco_valem_o_padrao` |
| <a id="ta-114"></a>TA-114 | [CA-10](#us-11-ca-10) | automatizado | `config/tests/test_perfil_lido_do_banco.py::test_gestor_rebaixado_deixa_de_ver_reserva_de_outra_pessoa` |
