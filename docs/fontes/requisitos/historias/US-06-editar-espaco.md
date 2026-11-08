# US-06 · Editar espaço

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-06 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-06-editar-espaco.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Marca "Depende de" das DECs confirmadas na Aula 7 (DEC-06, DEC-10, DEC-11) com "(decidida)" (GES-02). Nenhum Dado/Quando/Então muda. Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-06 |
| **Título** | Editar espaço |
| **História** | Como Gestor, quero corrigir o nome, o tipo ou a capacidade de um espaço para que a lista continue igual à realidade, sem cadastrar um espaço novo. |
| **Valor** | Uma reforma ou um erro de digitação não obriga a desativar um espaço e cadastrar outro, e as reservas dele continuam ligadas ao mesmo espaço ([NS-02](../visao.md#necessidades)). |
| **Origem** | [UC-15 Editar espaço, passos 1 a 5](../casos-de-uso/fichas-resumidas.md#uc15-p1), alternativas [A3.1](../casos-de-uso/fichas-resumidas.md#uc15-a3-1) e [A3.2](../casos-de-uso/fichas-resumidas.md#uc15-a3-2) e exceções [E1.1](../casos-de-uso/fichas-resumidas.md#uc15-e1-1) a [E5.1](../casos-de-uso/fichas-resumidas.md#uc15-e5-1). |
| **Prioridade** | Normal — por [RF-09](../requisitos/rf-espacos.md#rf-09) (espaço inexistente), a recusa comum normal que esta história também cobre; os RF próprios da edição ([RF-06](../requisitos/rf-espacos.md#rf-06), [RF-06.1](../requisitos/rf-espacos.md#rf-06-1), [RF-06.2](../requisitos/rf-espacos.md#rf-06-2)) são esperados e extras ao enunciado. |
| **Estimativa (Custo em Semanas)** | 0,3 (retrospectiva: a edição e a proteção contra alterações simultâneas da ESP-04, com o diálogo de edição). |
| **Conversa** | "Mudar o nome de um espaço muda as reservas já feitas?" → não; a reserva referencia o espaço, e o nome novo aparece nela. "O que acontece se duas pessoas editam ao mesmo tempo?" → só a primeira grava (achado de revisão da ESP-04). "Pode repetir o nome de outro espaço?" → não ([DEC-10](../decisoes/DEC-10.md)). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Precisa de um espaço cadastrado ([US-05](US-05-cadastrar-espaco.md)) e reaproveita as regras dele. |
| **N** · Negociável | ✓ | Quais dados podem ser editados e como a edição simultânea é tratada foram combinados, não impostos. |
| **V** · Valiosa | ✓ | Evita perder o histórico de um espaço só para corrigir um dado. |
| **E** · Estimável | ✓ | As regras são as do cadastro, já conhecidas. |
| **S** · Small | ✓ | Uma operação, com as recusas herdadas do cadastro. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado, inclusive a edição simultânea. |

**Diagnóstico:** pequena, valiosa e testável, mas depende de US-05.

## Critérios de aceite

#### <a id="us-06-ca-01"></a>US-06 · CA-01 · Espaço atualizado (sucesso)

- **Dado** um espaço cadastrado e um Gestor identificado
- **Quando** o Gestor altera um ou mais dados (nome, tipo ou capacidade), dentro das regras do cadastro
- **Então** o sistema informa "Espaço atualizado com sucesso.", grava só os dados alterados, mantém os outros como estavam e a lista passa a mostrar o espaço atualizado
- **Origem:** [UC-15 passos 1 a 5](../casos-de-uso/fichas-resumidas.md#uc15-p1)
- **RF:** [RF-06](../requisitos/rf-espacos.md#rf-06), [RF-04](../requisitos/rf-espacos.md#rf-04)
- **TA:** [TA-40](#ta-40)

#### <a id="us-06-ca-02"></a>US-06 · CA-02 · Manter o próprio nome ou só trocar maiúsculas (alternativa)

- **Dado** um espaço chamado "Ginásio A"
- **Quando** o Gestor o edita mantendo o mesmo nome, ou trocando só maiúsculas por minúsculas
- **Então** o sistema não acusa nome repetido e grava a edição
- **Origem:** [UC-15 A3.1](../casos-de-uso/fichas-resumidas.md#uc15-a3-1)
- **RF:** [RF-06](../requisitos/rf-espacos.md#rf-06), [RF-05.2](../requisitos/rf-espacos.md#rf-05-2)
- **TA:** [TA-41](#ta-41)

#### <a id="us-06-ca-03"></a>US-06 · CA-03 · Ativo ou inativo no pedido de edição (alternativa)

- **Dado** um espaço ativo
- **Quando** o pedido de edição traz também que ele deve ficar inativo
- **Então** o sistema ignora essa parte: o espaço continua ativo, e ativar ou desativar só acontece pela [US-07](US-07-desativar-e-reativar-espaco.md)
- **Origem:** [UC-15 A3.2](../casos-de-uso/fichas-resumidas.md#uc15-a3-2)
- **RF:** [RF-06](../requisitos/rf-espacos.md#rf-06)
- **TA:** [TA-42](#ta-42)

#### <a id="us-06-ca-04"></a>US-06 · CA-04 · Capacidade em formato inválido (exceção)

- **Dado** um Gestor editando um espaço
- **Quando** a capacidade nova não é um número inteiro
- **Então** o sistema informa "Verifique os dados informados." com o problema junto à capacidade, e o espaço não muda
- **Origem:** [UC-15 E4.1](../casos-de-uso/fichas-resumidas.md#uc15-e4-1)
- **RF:** [RF-06.2](../requisitos/rf-espacos.md#rf-06-2)
- **TA:** [TA-43](#ta-43)

#### <a id="us-06-ca-05"></a>US-06 · CA-05 · Espaço inexistente (exceção)

- **Dado** uma identificação de espaço que não existe
- **Quando** o Gestor pede para editá-lo
- **Então** o sistema informa "Espaço de código «n» não encontrado." e nenhum espaço muda
- **Origem:** [UC-15 E4.2](../casos-de-uso/fichas-resumidas.md#uc15-e4-2)
- **RF:** [RF-09](../requisitos/rf-espacos.md#rf-09)
- **TA:** [TA-44](#ta-44)

#### <a id="us-06-ca-06"></a>US-06 · CA-06 · Nenhum dado alterado (exceção)

- **Dado** um Gestor editando um espaço
- **Quando** ele envia a edição sem alterar nome, tipo nem capacidade (ou alterando só se o espaço está ativo)
- **Então** o sistema informa "Informe ao menos um campo para alterar." e o espaço não muda
- **Origem:** [UC-15 E4.3](../casos-de-uso/fichas-resumidas.md#uc15-e4-3)
- **RF:** [RF-06.1](../requisitos/rf-espacos.md#rf-06-1)
- **TA:** [TA-45](#ta-45)

#### <a id="us-06-ca-07"></a>US-06 · CA-07 · Dado fora das regras do cadastro (exceção)

- **Dado** um Gestor editando um espaço
- **Quando** ele deixa o nome em branco ou longo demais, escolhe um tipo desconhecido ou informa capacidade menor que 1, junto com outro dado válido
- **Então** o sistema mostra, junto ao dado, a mesma mensagem do cadastro ([US-05 · CA-05 a CA-08](US-05-cadastrar-espaco.md#us-05-ca-05)), e nenhum dado do espaço muda, nem o válido do mesmo pedido
- **Origem:** [UC-15 E4.4](../casos-de-uso/fichas-resumidas.md#uc15-e4-4)
- **RF:** [RF-06.2](../requisitos/rf-espacos.md#rf-06-2)
- **TA:** [TA-46](#ta-46)

#### <a id="us-06-ca-08"></a>US-06 · CA-08 · Nome de outro espaço (exceção)

- **Dado** os espaços "Ginásio A" e "Ginásio B"
- **Quando** o Gestor tenta renomear o "Ginásio B" para "ginásio a"
- **Então** o sistema informa, junto ao nome, "Já existe um espaço com este nome.", e nenhum dos dois espaços muda
- **Origem:** [UC-15 E4.5](../casos-de-uso/fichas-resumidas.md#uc15-e4-5)
- **RF:** [RF-05.2](../requisitos/rf-espacos.md#rf-05-2), [RF-06.2](../requisitos/rf-espacos.md#rf-06-2)
- **TA:** [TA-47](#ta-47)
- **Depende de:** [DEC-10](../decisoes/DEC-10.md) (decidida)

#### <a id="us-06-ca-09"></a>US-06 · CA-09 · Espaço alterado por outra pessoa (exceção)

- **Dado** dois Gestores que leram o mesmo espaço; um deles o desativa
- **Quando** o outro envia uma edição feita sobre a leitura anterior
- **Então** o sistema informa "Este espaço foi alterado por outra pessoa enquanto você decidia. Atualize a lista e tente de novo." e oferece atualizar a lista; vale só a primeira alteração, e o espaço não volta a ficar ativo por engano
- **Origem:** [UC-15 E5.1](../casos-de-uso/fichas-resumidas.md#uc15-e5-1)
- **RF:** [RF-06](../requisitos/rf-espacos.md#rf-06) (a garantia é o [RNF-R04](../requisitos/rnf.md#rnf-r04))
- **TA:** [TA-48](#ta-48)

#### <a id="us-06-ca-10"></a>US-06 · CA-10 · Só o Gestor edita (acesso)

- **Dado** um Solicitante identificado
- **Quando** ele tenta editar um espaço
- **Então** o sistema informa "Você não tem permissão para realizar esta ação.", o espaço não muda e a lista do Solicitante nem oferece editar
- **Origem:** [UC-15 E1.1](../casos-de-uso/fichas-resumidas.md#uc15-e1-1)
- **RF:** [RF-10](../requisitos/rf-espacos.md#rf-10)
- **TA:** [TA-49](#ta-49)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-40"></a>TA-40 | [CA-01](#us-06-ca-01) | automatizado | `espacos/tests/test_api_edicao_de_espaco.py::test_editar_responde_200_e_a_listagem_mostra_os_dados_novos`; `espacos/tests/test_api_edicao_de_espaco.py::test_editar_so_a_capacidade_mantem_os_outros_campos`; `espacos/tests/test_casos_de_uso.py::test_editar_o_tipo_grava_o_tipo_novo_e_mantem_o_resto`; `pages/PaginaEspacos.test.tsx`: `envia só o campo alterado; no sucesso, mostra o toast, fecha e recarrega a lista` |
| <a id="ta-41"></a>TA-41 | [CA-02](#us-06-ca-02) | automatizado | `espacos/tests/test_casos_de_uso.py::test_editar_mantendo_o_proprio_nome_nao_acusa_duplicidade [x]` |
| <a id="ta-42"></a>TA-42 | [CA-03](#us-06-ca-03) | automatizado | `espacos/tests/test_api_edicao_de_espaco.py::test_ativo_no_corpo_do_patch_e_ignorado` |
| <a id="ta-43"></a>TA-43 | [CA-04](#us-06-ca-04) | automatizado | `espacos/tests/test_api_edicao_de_espaco.py::test_editar_com_dado_invalido_responde_erro_no_campo_e_nao_grava [x]`; `pages/PaginaEspacos.test.tsx`: `a capacidade inválida aparece embaixo do campo, que recebe o foco` |
| <a id="ta-44"></a>TA-44 | [CA-05](#us-06-ca-05) | automatizado | `espacos/tests/test_api_edicao_de_espaco.py::test_acoes_em_espaco_inexistente_respondem_404 [x]`; `espacos/tests/test_casos_de_uso.py::test_acoes_em_espaco_inexistente_lancam_espaco_nao_encontrado [x]` |
| <a id="ta-45"></a>TA-45 | [CA-06](#us-06-ca-06) | automatizado | `espacos/tests/test_api_edicao_de_espaco.py::test_editar_sem_nenhum_campo_responde_400`; `espacos/tests/test_api_edicao_de_espaco.py::test_so_ativo_no_corpo_do_patch_conta_como_nenhuma_alteracao`; `pages/PaginaEspacos.test.tsx`: `sem mudança, envia um corpo vazio e mostra a mensagem da API num aviso` |
| <a id="ta-46"></a>TA-46 | [CA-07](#us-06-ca-07) | automatizado | `espacos/tests/test_espaco_esportivo.py::test_alterar_dados_invalidos_lanca_o_erro_do_construtor_sem_mudar_nada [x]`; `espacos/tests/test_casos_de_uso.py::test_editar_com_dado_invalido_nao_grava`; `espacos/tests/test_api_edicao_de_espaco.py::test_editar_com_dado_invalido_responde_erro_no_campo_e_nao_grava [x]` |
| <a id="ta-47"></a>TA-47 | [CA-08](#us-06-ca-08) | automatizado | `espacos/tests/test_casos_de_uso.py::test_editar_para_o_nome_de_outro_espaco_lanca_conflito_sem_gravar`; `pages/PaginaEspacos.test.tsx`: `o nome repetido aparece no campo Nome` |
| <a id="ta-48"></a>TA-48 | [CA-09](#us-06-ca-09) | automatizado | `espacos/tests/test_concorrencia_de_espaco.py::test_edicao_e_desativacao_simultaneas_gravam_so_uma`; `espacos/tests/test_repositorio_espacos.py::test_edicao_sobre_leitura_anterior_a_uma_desativacao_e_recusada`; `pages/PaginaEspacos.test.tsx`: `se outra pessoa alterou o espaço, mostra o aviso e "Atualizar lista", que recarrega` |
| <a id="ta-49"></a>TA-49 | [CA-10](#us-06-ca-10) | automatizado | `espacos/tests/test_api_edicao_de_espaco.py::test_solicitante_nao_edita_desativa_nem_ativa_e_nada_muda [x]`; `pages/PaginaEspacos.test.tsx`: `para o solicitante, a tabela não tem editar, desativar nem reativar`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]` |
