# US-10 · Acompanhar minhas reservas

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-10 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-10-acompanhar-minhas-reservas.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-19 e TA-20 passam a TA-20 e TA-21, e TA-21 a TA-158 passam a TA-24 a TA-161, para os TA-19, TA-22 e TA-23 novos da US-03 (revogação e troca da credencial de renovação) seguirem a ordem das histórias (AUT-09). Mudança editorial, sem nova obrigação. Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-10 |
| **Título** | Acompanhar minhas reservas |
| **História** | Como Solicitante, quero ver as minhas reservas, com a situação e o motivo de cada uma, para saber o que foi confirmado, recusado ou cancelado sem perguntar a ninguém. |
| **Valor** | O Solicitante acompanha os próprios pedidos e vê o que ainda pode fazer com cada um ([NS-07](../visao.md#necessidades)); os pedidos de outras pessoas ficam protegidos ([NS-14](../visao.md#necessidades)). |
| **Origem** | [UC-07 Consultar reservas](../casos-de-uso/fichas-resumidas.md#uc-07), no papel do Solicitante: [passos 1 a 4](../casos-de-uso/fichas-resumidas.md#uc07-p1), alternativas [A3.1](../casos-de-uso/fichas-resumidas.md#uc07-a3-1) e [A4.1](../casos-de-uso/fichas-resumidas.md#uc07-a4-1) e a exceção [E3.1](../casos-de-uso/fichas-resumidas.md#uc07-e3-1). O mesmo caso de uso, no papel do Gestor, é a [US-11](US-11-acompanhar-todas-as-reservas.md). |
| **Prioridade** | Normal — [RF-12](../requisitos/rf-reservas.md#rf-12) e [RF-13](../requisitos/rf-reservas.md#rf-13) são normais (F3 do enunciado). |
| **Estimativa (Custo em Semanas)** | 0,3 (retrospectiva: a consulta da RES-05, a visibilidade da AUT-05 e "Minhas reservas" da FE-06). |
| **Conversa** | "O Solicitante pode ver as reservas de outras pessoas?" → não; a agenda do dia mostra só que o horário está ocupado ([DEC-11](../decisoes/DEC-11.md)). "A lista precisa de paginação?" → não para 1.000 reservas ([L-05](../requisitos/srs.md#l-05), [DEC-12](../decisoes/DEC-12.md)). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Sem reservas pedidas ([US-08](US-08-solicitar-reserva.md)) só mostra o estado vazio. |
| **N** · Negociável | ✓ | Os critérios e a apresentação podem ser combinados sem mudar a meta. |
| **V** · Valiosa | ✓ | É onde o Solicitante fica sabendo da decisão do Gestor. |
| **E** · Estimável | ✓ | Consulta com critérios conhecidos. |
| **S** · Small | ✓ | Uma consulta, no papel de um ator; o Gestor ficou noutra história. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado. |

**Diagnóstico:** pequena, valiosa e testável; depende de US-08 para ter o que mostrar.

## Critérios de aceite

#### <a id="us-10-ca-01"></a>US-10 · CA-01 · Só as próprias, como "Minhas reservas" (sucesso)

- **Dado** um Solicitante com duas reservas e outras pessoas com reservas no mesmo espaço
- **Quando** ele pede para ver as reservas
- **Então** o sistema mostra só as dele, sob o título "Minhas reservas", ordenadas pelo início, cada uma com data e horário, espaço, solicitante, finalidade e situação (com o motivo, quando houver), e informa quantas foram encontradas
- **Origem:** [UC-07 passo 2](../casos-de-uso/fichas-resumidas.md#uc07-p2)
- **RF:** [RF-13](../requisitos/rf-reservas.md#rf-13)
- **TA:** [TA-93](#ta-93)

#### <a id="us-10-ca-02"></a>US-10 · CA-02 · O que ainda pode fazer em cada uma (sucesso)

- **Dado** as reservas do Solicitante, uma Solicitada, uma Confirmada e uma Concluída
- **Quando** ele as vê na lista
- **Então** a Solicitada e a Confirmada oferecem só "Cancelar", e a Concluída não oferece nenhuma ação, indicando que não há ação disponível
- **Origem:** [UC-07 passo 2](../casos-de-uso/fichas-resumidas.md#uc07-p2)
- **RF:** [RF-16](../requisitos/rf-reservas.md#rf-16)
- **TA:** [TA-94](#ta-94)

#### <a id="us-10-ca-03"></a>US-10 · CA-03 · Filtrar por espaço, situação e data (sucesso)

- **Dado** a lista de reservas do Solicitante
- **Quando** ele escolhe um espaço, uma situação (entre as situações de reserva, na ordem do ciclo de vida), uma data, ou uma combinação deles
- **Então** o sistema mostra só as reservas dele que atendem a todos os critérios, com a quantidade
- **Origem:** [UC-07 passo 3](../casos-de-uso/fichas-resumidas.md#uc07-p3)
- **RF:** [RF-12](../requisitos/rf-reservas.md#rf-12), [RF-15](../requisitos/rf-reservas.md#rf-15)
- **TA:** [TA-95](#ta-95)

#### <a id="us-10-ca-04"></a>US-10 · CA-04 · Critérios de solicitante ignorados (alternativa)

- **Dado** um Solicitante
- **Quando** a consulta dele traz o nome de outro solicitante, ou "somente as minhas = não"
- **Então** o critério é ignorado e ele continua vendo só as próprias reservas; os critérios de solicitante nem são oferecidos a ele
- **Origem:** [UC-07 A3.1](../casos-de-uso/fichas-resumidas.md#uc07-a3-1)
- **RF:** [RF-13](../requisitos/rf-reservas.md#rf-13)
- **TA:** [TA-96](#ta-96)

#### <a id="us-10-ca-05"></a>US-10 · CA-05 · Nenhuma reserva atende aos critérios (alternativa)

- **Dado** critérios que nenhuma reserva do Solicitante atende (inclusive um espaço que não existe)
- **Quando** ele consulta
- **Então** o sistema informa "Nenhuma reserva encontrada." e oferece limpar os critérios; um espaço inexistente no critério dá lista vazia, não recusa
- **Origem:** [UC-07 A4.1](../casos-de-uso/fichas-resumidas.md#uc07-a4-1)
- **RF:** [RF-12](../requisitos/rf-reservas.md#rf-12)
- **TA:** [TA-97](#ta-97)

#### <a id="us-10-ca-06"></a>US-10 · CA-06 · Ainda não tem reservas (alternativa)

- **Dado** um Solicitante que nunca pediu uma reserva
- **Quando** ele consulta sem nenhum critério
- **Então** o sistema informa "Você ainda não tem reservas" e oferece solicitar uma reserva
- **Origem:** [UC-07 A4.1](../casos-de-uso/fichas-resumidas.md#uc07-a4-1)
- **RF:** [RF-13](../requisitos/rf-reservas.md#rf-13)
- **TA:** [TA-98](#ta-98)

#### <a id="us-10-ca-07"></a>US-10 · CA-07 · Critério em formato inválido (exceção)

- **Dado** a lista de reservas
- **Quando** a consulta traz uma situação fora da lista, uma data que não existe ou um espaço que não é um número
- **Então** o sistema informa "Verifique os dados informados." apontando o critério com problema, e nenhuma reserva muda
- **Origem:** [UC-07 E3.1](../casos-de-uso/fichas-resumidas.md#uc07-e3-1)
- **RF:** [RF-12.1](../requisitos/rf-reservas.md#rf-12-1)
- **TA:** [TA-99](#ta-99)

#### <a id="us-10-ca-08"></a>US-10 · CA-08 · Reservas de outras pessoas nunca aparecem (acesso)

- **Dado** reservas de outras pessoas e, à parte, uma pessoa que não entrou
- **Quando** o Solicitante consulta com qualquer critério, e a pessoa não identificada pede a lista
- **Então** o Solicitante nunca vê reservas de outras pessoas, e a pessoa não identificada não vê nenhuma reserva e é orientada a entrar
- **Origem:** [UC-07 passo 2](../casos-de-uso/fichas-resumidas.md#uc07-p2)
- **RF:** [RF-13](../requisitos/rf-reservas.md#rf-13), [RF-23](../requisitos/rf-reservas.md#rf-23)
- **TA:** [TA-100](#ta-100)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-93"></a>TA-93 | [CA-01](#us-10-ca-01) | automatizado | `reservas/tests/test_api_permissoes.py::test_solicitante_so_lista_as_proprias`; `reservas/tests/test_api_permissoes.py::test_solicitante_sem_filtros_ve_a_propria`; `reservas/tests/test_api_consulta_reservas.py::test_mensagem_informa_a_quantidade_encontrada`; `pages/PaginaReservas.test.tsx`: `o título é "Minhas reservas" e não há os filtros de solicitante`; `pages/PaginaReservas.test.tsx`: `mostra o motivo logo abaixo da situação de uma reserva cancelada`; `components/layout/Layout.test.tsx`: `logado como solicitante, o item das reservas se chama "Minhas reservas"` |
| <a id="ta-94"></a>TA-94 | [CA-02](#us-10-ca-02) | automatizado | `reservas/tests/test_api_permissoes.py::test_acoes_do_solicitante_na_propria_solicitada_sao_so_cancelar`; `reservas/tests/test_api_permissoes.py::test_solicitante_numa_concluida_nao_tem_acoes`; `components/reservas/TabelaDeReservas.test.tsx`: `mostra exatamente as ações recebidas da API`; `components/reservas/TabelaDeReservas.test.tsx`: `sem ações mostra "—" e "Nenhuma ação disponível" para leitor de tela` |
| <a id="ta-95"></a>TA-95 | [CA-03](#us-10-ca-03) | automatizado | `reservas/tests/test_api_consulta_reservas.py::test_cada_criterio_sozinho_devolve_so_as_correspondentes`; `reservas/tests/test_api_consulta_reservas.py::test_situacoes_de_reserva_listam_todas_na_ordem_do_enum_sem_login`; `pages/PaginaReservas.test.tsx`: `os outros filtros continuam valendo` |
| <a id="ta-96"></a>TA-96 | [CA-04](#us-10-ca-04) | automatizado | `pages/PaginaReservas.test.tsx`: `ignora solicitante e minhas vindos da URL`; `reservas/tests/test_api_permissoes.py::test_solicitante_so_lista_as_proprias` |
| <a id="ta-97"></a>TA-97 | [CA-05](#us-10-ca-05) | automatizado | `reservas/tests/test_api_consulta_reservas.py::test_espaco_inexistente_no_filtro_devolve_lista_vazia`; `pages/PaginaReservas.test.tsx`: `com filtros e sem reservas, oferece "Limpar filtros"` |
| <a id="ta-98"></a>TA-98 | [CA-06](#us-10-ca-06) | automatizado | `pages/PaginaReservas.test.tsx`: `sem filtros e sem reservas, mostra "Você ainda não tem reservas"` |
| <a id="ta-99"></a>TA-99 | [CA-07](#us-10-ca-07) | automatizado | `reservas/tests/test_api_consulta_reservas.py::test_filtro_invalido_responde_400_com_o_campo` |
| <a id="ta-100"></a>TA-100 | [CA-08](#us-10-ca-08) | automatizado | `reservas/tests/test_api_permissoes.py::test_solicitante_so_lista_as_proprias`; `reservas/tests/test_api_consulta_reservas.py::test_consulta_sem_login_responde_401`; `pages/PaginaReservas.test.tsx`: `sem login mostra a mensagem da API no lugar da tabela`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]` |
