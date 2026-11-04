# Requisitos funcionais — Espaços

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **Parte da [SRS-01](srs.md) • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/requisitos/rf-espacos.md` |

Fichas dos RF do cadastro de [espaços esportivos](../glossario.md#espaco-esportivo), derivados da NS-01 e da NS-02 da [Visão](../visao.md#necessidades). Como ler as fichas (sintaxe, decomposição, recusas e evidência): [SRS, seção 3](srs.md#3-requisitos-funcionais).

Caminhos de teste a partir de `src/backend/`; `[x]` = teste parametrizado.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Criação: RF-01 a RF-10 (REQ-02). Sem aprovação. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Vínculos: o UC de cada ficha preenchido, com link para o [índice de casos de uso](../casos-de-uso/README.md#índice-dos-casos-de-uso) (REQ-03). Sem aprovação. |

## Consulta de espaços

### <a id="rf-01"></a>RF-01 · Listar espaços

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao usuário autenticado listar os espaços esportivos e ver, de cada um, o nome, o tipo, a capacidade e se está ativo, ordenados pelo nome, com a quantidade encontrada. |
| **Origem** | NS-01 |
| **Funcionalidade** | F1 |
| **Prioridade (QFD)** | Normal — "listar os itens do recorte" é a primeira funcionalidade do enunciado. |
| **Vínculos** | UC: [UC-03 Consultar espaços](../casos-de-uso/README.md#uc-03) (fluxo principal) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | `GET /api/espacos/`; tela `/espacos`. `espacos/tests/test_api_espacos.py::test_listar_ordena_por_nome`, `::test_espaco_cadastrado_aparece_na_listagem`, `::test_listar_informa_a_quantidade_encontrada [x]`, `::test_solicitante_lista_espacos` |
| **Regras de negócio** | [Espaço esportivo](../glossario.md#espaco-esportivo), [tipo de espaço](../glossario.md#tipo-de-espaco), [capacidade](../glossario.md#capacidade), [espaço ativo](../glossario.md#espaco-ativo) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-02"></a>RF-02 · Filtrar espaços

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao usuário autenticado filtrar a lista de espaços por tipo de espaço, por "somente ativos" ou pelos dois juntos, e ver só os espaços que atendem a todos os critérios informados. |
| **Origem** | NS-01 |
| **Funcionalidade** | F1 |
| **Prioridade (QFD)** | Esperado — o Solicitante procura onde pode reservar; sem o filtro, teria de percorrer espaços inativos. |
| **Vínculos** | UC: [UC-03 Consultar espaços](../casos-de-uso/README.md#uc-03) (alternativa) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | `GET /api/espacos/?tipo=&apenas_ativos=`; tela `/espacos` (filtros no endereço). `espacos/tests/test_api_espacos.py::test_listar_aplica_os_filtros_da_query_string [x]`; `espacos/tests/test_repositorio_espacos.py::test_listar_aplica_os_filtros [x]` |
| **Regras de negócio** | [Tipo de espaço](../glossario.md#tipo-de-espaco), [espaço ativo](../glossario.md#espaco-ativo) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-02-1"></a>RF-02.1 · Recusar filtro com tipo inexistente

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o usuário autenticado filtre a lista de espaços por um tipo fora da lista de tipos de espaço e informar, no critério tipo, que o valor não é aceito. |
| **Pai** | [RF-02](#rf-02) |
| **Origem** | NS-01 (principal); NS-13 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — um filtro silenciosamente ignorado mostraria espaços que a pessoa não pediu. |
| **Vínculos** | UC: [UC-03 Consultar espaços](../casos-de-uso/README.md#uc-03) (exceção) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | 400 `DADOS_INVALIDOS` com `campos.tipo`. `espacos/tests/test_api_espacos.py::test_listar_com_tipo_desconhecido_no_filtro_responde_400` |
| **Regras de negócio** | [Tipo de espaço](../glossario.md#tipo-de-espaco) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-03"></a>RF-03 · Consultar um espaço

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao usuário autenticado escolher um espaço esportivo e ver o nome, o tipo, a capacidade e se ele está ativo. |
| **Origem** | NS-01 |
| **Funcionalidade** | F1 |
| **Prioridade (QFD)** | Normal — a reserva e o detalhe da reserva mostram o espaço pelo nome a partir desta consulta. |
| **Vínculos** | UC: [UC-03 Consultar espaços](../casos-de-uso/README.md#uc-03) (alternativa) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | `GET /api/espacos/{id}/`; detalhe da reserva `/reservas/:reservaId`. `espacos/tests/test_api_espacos.py::test_obter_espaco_existente_responde_200_com_o_espaco`, `::test_solicitante_obtem_o_detalhe_de_um_espaco` |
| **Regras de negócio** | [Espaço esportivo](../glossario.md#espaco-esportivo) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-04"></a>RF-04 · Consultar os tipos de espaço

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao visitante consultar os tipos de espaço e ver o nome de cada um, na ordem da lista fechada de cinco tipos. |
| **Origem** | NS-01 |
| **Funcionalidade** | F1 |
| **Prioridade (QFD)** | Esperado — quem cadastra ou filtra escolhe o tipo de uma lista, sem digitar. |
| **Vínculos** | UC: [UC-03 Consultar espaços](../casos-de-uso/README.md#uc-03) (fluxo principal); também em [UC-14 Cadastrar espaço](../casos-de-uso/README.md#uc-14), [UC-15 Editar espaço](../casos-de-uso/README.md#uc-15) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | `GET /api/espacos/tipos/` (sem login); seletor de tipo em `/espacos`. `espacos/tests/test_api_espacos.py::test_tipos_de_espaco_lista_todos_os_tipos_na_ordem_do_enum`, `::test_tipos_de_espaco_nao_exigem_login` |
| **Regras de negócio** | [Tipo de espaço](../glossario.md#tipo-de-espaco), [vocabulário público](../glossario.md#vocabulario-publico) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

## Manutenção do cadastro (Gestor)

### <a id="rf-05"></a>RF-05 · Cadastrar espaço

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao Gestor cadastrar um espaço esportivo com nome, tipo e capacidade e ver o espaço cadastrado, ativo, na lista de espaços. |
| **Origem** | NS-02 |
| **Funcionalidade** | F1 |
| **Prioridade (QFD)** | Normal — "cadastrar os itens do recorte" é a primeira funcionalidade do enunciado. |
| **Vínculos** | UC: [UC-14 Cadastrar espaço](../casos-de-uso/README.md#uc-14) (fluxo principal) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | `POST /api/espacos/` → 201; formulário em `/espacos` (só para o Gestor). `espacos/tests/test_api_espacos.py::test_cadastrar_espaco_valido_responde_201_com_o_espaco`, `::test_espaco_cadastrado_aparece_na_listagem`; `espacos/tests/test_casos_de_uso.py::test_cadastrar_espaco_valido_devolve_com_id_e_aparece_na_listagem` |
| **Regras de negócio** | [Espaço esportivo](../glossario.md#espaco-esportivo), [espaço ativo](../glossario.md#espaco-ativo) |
| **Decisões** | [DEC-04](../decisoes/DEC-04.md) (só o Gestor) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-05-1"></a>RF-05.1 · Recusar espaço com dados inválidos

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o Gestor cadastre um espaço sem nome, com nome de mais de 100 caracteres, sem tipo, com tipo fora da lista ou com capacidade que não seja um número inteiro de pelo menos 1, sem gravar nada, e informar a regra violada no campo correspondente. |
| **Pai** | [RF-05](#rf-05) |
| **Origem** | NS-02 (principal); NS-13 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Normal — "campos obrigatórios vazios" é uma das operações inválidas do enunciado. |
| **Vínculos** | UC: [UC-14 Cadastrar espaço](../casos-de-uso/README.md#uc-14) (exceção) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | 400 com `campos`. `espacos/tests/test_api_espacos.py::test_cadastro_invalido_responde_erro_e_preserva_a_listagem [x]`; `espacos/tests/test_espaco_esportivo.py::test_nome_vazio_e_recusado_como_campo_obrigatorio [x]`, `::test_nome_acima_do_limite_de_caracteres_e_recusado`, `::test_tipo_desconhecido_e_recusado_listando_os_tipos_aceitos`, `::test_capacidade_que_nao_e_inteiro_positivo_e_recusada [x]`; `espacos/tests/test_propriedades_do_espaco.py::test_entrada_invalida_lanca_so_o_erro_de_dominio_do_primeiro_campo_invalido` |
| **Regras de negócio** | [Espaço esportivo](../glossario.md#espaco-esportivo) (nome normalizado, até 100 caracteres), [tipo de espaço](../glossario.md#tipo-de-espaco), [capacidade](../glossario.md#capacidade) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-05-2"></a>RF-05.2 · Recusar nome de espaço repetido

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o Gestor cadastre um espaço com o nome de outro espaço já cadastrado, sem diferenciar maiúsculas de minúsculas e depois de tirar os espaços repetidos, sem gravar nada, e informar no campo nome que o nome já existe. |
| **Pai** | [RF-05](#rf-05) |
| **Origem** | NS-02 (principal); NS-01 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — dois espaços com o mesmo nome tornariam a reserva ambígua para quem pede. |
| **Vínculos** | UC: [UC-14 Cadastrar espaço](../casos-de-uso/README.md#uc-14) (exceção); também em [UC-15 Editar espaço](../casos-de-uso/README.md#uc-15) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | 409 `NOME_DE_ESPACO_JA_CADASTRADO` com `campos.nome`. `espacos/tests/test_casos_de_uso.py::test_cadastrar_nome_repetido_com_caixa_e_espacos_diferentes_lanca_conflito`; `espacos/tests/test_repositorio_espacos.py::test_salvar_nome_repetido_com_caixa_diferente_lanca_nome_ja_cadastrado`; `espacos/tests/test_api_espacos.py::test_cadastro_invalido_responde_erro_e_preserva_a_listagem [nome-repetido]` |
| **Regras de negócio** | [Espaço esportivo](../glossario.md#espaco-esportivo) (nome único) |
| **Decisões** | [DEC-10](../decisoes/DEC-10.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-06"></a>RF-06 · Editar espaço

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao Gestor alterar o nome, o tipo ou a capacidade de um espaço, em qualquer combinação, e ver o espaço com os valores novos e os não informados mantidos. |
| **Origem** | NS-02 |
| **Funcionalidade** | Extra (ESP-04) |
| **Prioridade (QFD)** | Esperado — sem editar, um erro de digitação no cadastro só se corrigiria com outro espaço. |
| **Vínculos** | UC: [UC-15 Editar espaço](../casos-de-uso/README.md#uc-15) (fluxo principal) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | `PATCH /api/espacos/{id}/`; diálogo "Editar espaço" em `/espacos`. `espacos/tests/test_api_edicao_de_espaco.py::test_editar_responde_200_e_a_listagem_mostra_os_dados_novos`, `::test_editar_so_a_capacidade_mantem_os_outros_campos`, `::test_ativo_no_corpo_do_patch_e_ignorado`; `espacos/tests/test_espaco_esportivo.py::test_alterar_dados_muda_so_os_campos_informados [x]` |
| **Regras de negócio** | [Espaço esportivo](../glossario.md#espaco-esportivo), [espaço desatualizado](../glossario.md#espaco-desatualizado) ([RNF-R04](rnf.md#rnf-r04)) |
| **Decisões** | [DEC-06](../decisoes/DEC-06.md) (espaço nunca é excluído) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-06-1"></a>RF-06.1 · Recusar edição sem alteração

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o Gestor envie uma edição de espaço sem nome, tipo nem capacidade e informar que é preciso informar ao menos um campo para alterar. |
| **Pai** | [RF-06](#rf-06) |
| **Origem** | NS-02 (principal); NS-13 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — uma edição vazia que respondesse como aceita esconderia um erro de quem edita. |
| **Vínculos** | UC: [UC-15 Editar espaço](../casos-de-uso/README.md#uc-15) (exceção) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | 400 `NENHUMA_ALTERACAO_INFORMADA`. `espacos/tests/test_api_edicao_de_espaco.py::test_editar_sem_nenhum_campo_responde_400`, `::test_so_ativo_no_corpo_do_patch_conta_como_nenhuma_alteracao`; `espacos/tests/test_espaco_esportivo.py::test_alterar_dados_sem_nenhum_campo_e_recusado` |
| **Regras de negócio** | [Espaço esportivo](../glossario.md#espaco-esportivo) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-06-2"></a>RF-06.2 · Recusar edição que viola as regras do cadastro

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o Gestor altere um espaço para um valor que o cadastro recusaria ([RF-05.1](#rf-05-1)) ou para o nome de outro espaço ([RF-05.2](#rf-05-2)), sem alterar nenhum campo do espaço, e informar a regra violada no campo correspondente. |
| **Pai** | [RF-06](#rf-06) |
| **Origem** | NS-02 (principal); NS-13 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — as regras do espaço precisam valer igual no cadastro e na edição. |
| **Vínculos** | UC: [UC-15 Editar espaço](../casos-de-uso/README.md#uc-15) (exceção) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | 400 ou 409 com `campos`. `espacos/tests/test_api_edicao_de_espaco.py::test_editar_com_dado_invalido_responde_erro_no_campo_e_nao_grava [x]`; `espacos/tests/test_espaco_esportivo.py::test_alterar_dados_invalidos_lanca_o_erro_do_construtor_sem_mudar_nada [x]`; `espacos/tests/test_casos_de_uso.py::test_editar_para_o_nome_de_outro_espaco_lanca_conflito_sem_gravar`, `::test_editar_mantendo_o_proprio_nome_nao_acusa_duplicidade [x]` |
| **Regras de negócio** | [Espaço esportivo](../glossario.md#espaco-esportivo) |
| **Decisões** | [DEC-10](../decisoes/DEC-10.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-07"></a>RF-07 · Desativar espaço

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao Gestor desativar um espaço ativo e ver o espaço como inativo, sem aceitar novas reservas, enquanto as reservas que ele já tinha continuam com a mesma situação. |
| **Origem** | NS-02 |
| **Funcionalidade** | Extra (ESP-04) |
| **Prioridade (QFD)** | Esperado — retirar um espaço de uso (reforma, interdição) é parte de manter o cadastro igual à realidade, e o espaço nunca é excluído. |
| **Vínculos** | UC: [UC-16 Desativar ou reativar espaço](../casos-de-uso/README.md#uc-16) (fluxo principal) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | `POST /api/espacos/{id}/desativar/`; diálogo "Desativar espaço" em `/espacos`. `espacos/tests/test_api_edicao_de_espaco.py::test_desativar_espaco_ativo_responde_200_e_a_listagem_mostra_inativo`; `espacos/tests/test_api_desativacao_e_reservas.py::test_espaco_desativado_recusa_nova_reserva_com_409`, `::test_reserva_existente_continua_listada_com_as_acoes_depois_de_desativar`, `::test_reserva_existente_pode_ser_confirmada_depois_de_desativar` |
| **Regras de negócio** | [Espaço inativo](../glossario.md#espaco-inativo), [espaço reservável](../glossario.md#espaco-reservavel) |
| **Decisões** | [DEC-06](../decisoes/DEC-06.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-07-1"></a>RF-07.1 · Recusar desativar espaço já inativo

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o Gestor desative um espaço que já está inativo, sem alterar o espaço, e informar que ele já está inativo. |
| **Pai** | [RF-07](#rf-07) |
| **Origem** | NS-02 (principal); NS-13 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — repetir a ação em silêncio esconderia que outra pessoa já a fez. |
| **Vínculos** | UC: [UC-16 Desativar ou reativar espaço](../casos-de-uso/README.md#uc-16) (exceção) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | 409 `ESPACO_JA_INATIVO`. `espacos/tests/test_api_edicao_de_espaco.py::test_desativar_espaco_ja_inativo_responde_409_e_ele_continua_inativo`; `espacos/tests/test_espaco_esportivo.py::test_desativar_espaco_ja_inativo_e_recusado` |
| **Regras de negócio** | [Espaço inativo](../glossario.md#espaco-inativo) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-08"></a>RF-08 · Reativar espaço

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao Gestor reativar um espaço inativo e ver o espaço como ativo, aceitando novas reservas de novo. |
| **Origem** | NS-02 |
| **Funcionalidade** | Extra (ESP-04) |
| **Prioridade (QFD)** | Esperado — sem reativar, o fim de uma interdição exigiria cadastrar o espaço de novo com outro nome. |
| **Vínculos** | UC: [UC-16 Desativar ou reativar espaço](../casos-de-uso/README.md#uc-16) (alternativa) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | `POST /api/espacos/{id}/ativar/`; diálogo "Reativar espaço" em `/espacos`. `espacos/tests/test_api_edicao_de_espaco.py::test_ativar_espaco_inativo_responde_200_com_o_espaco_ativo`; `espacos/tests/test_api_desativacao_e_reservas.py::test_reativar_volta_a_aceitar_reservas` |
| **Regras de negócio** | [Espaço ativo](../glossario.md#espaco-ativo) |
| **Decisões** | [DEC-06](../decisoes/DEC-06.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-08-1"></a>RF-08.1 · Recusar reativar espaço já ativo

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o Gestor reative um espaço que já está ativo, sem alterar o espaço, e informar que ele já está ativo. |
| **Pai** | [RF-08](#rf-08) |
| **Origem** | NS-02 (principal); NS-13 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — mesmo motivo do [RF-07.1](#rf-07-1). |
| **Vínculos** | UC: [UC-16 Desativar ou reativar espaço](../casos-de-uso/README.md#uc-16) (exceção) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | 409 `ESPACO_JA_ATIVO`. `espacos/tests/test_api_edicao_de_espaco.py::test_ativar_espaco_ja_ativo_responde_409`; `espacos/tests/test_espaco_esportivo.py::test_ativar_espaco_ja_ativo_e_recusado` |
| **Regras de negócio** | [Espaço ativo](../glossario.md#espaco-ativo) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

## Recusas comuns às operações de espaço

### <a id="rf-09"></a>RF-09 · Recusar operação sobre espaço inexistente

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o usuário autenticado consulte, edite, desative ou reative um espaço que não existe, sem alterar nenhum espaço, e informar que o espaço não foi encontrado. |
| **Operações protegidas** | [RF-03](#rf-03), [RF-06](#rf-06), [RF-07](#rf-07), [RF-08](#rf-08) |
| **Origem** | NS-01 (principal); NS-13 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Normal — "item inexistente" é uma das operações inválidas do enunciado. |
| **Vínculos** | UC: [UC-03 Consultar espaços](../casos-de-uso/README.md#uc-03) (exceção); também em [UC-15 Editar espaço](../casos-de-uso/README.md#uc-15), [UC-16 Desativar ou reativar espaço](../casos-de-uso/README.md#uc-16) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | 404 `ESPACO_NAO_ENCONTRADO`. `espacos/tests/test_api_espacos.py::test_obter_espaco_inexistente_responde_404`; `espacos/tests/test_api_edicao_de_espaco.py::test_acoes_em_espaco_inexistente_respondem_404 [x]`; `espacos/tests/test_casos_de_uso.py::test_acoes_em_espaco_inexistente_lancam_espaco_nao_encontrado [x]` |
| **Regras de negócio** | [Espaço esportivo](../glossario.md#espaco-esportivo) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-10"></a>RF-10 · Recusar manutenção de espaço por quem não é Gestor

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o Solicitante cadastre, edite, desative ou reative um espaço, sem alterar nenhum espaço, e informar que ele não tem permissão para a ação. |
| **Operações protegidas** | [RF-05](#rf-05), [RF-06](#rf-06), [RF-07](#rf-07), [RF-08](#rf-08) |
| **Origem** | NS-11 (principal); NS-02 |
| **Funcionalidade** | F5 (regra do extra de perfis, [DEC-04](../decisoes/DEC-04.md)) |
| **Prioridade (QFD)** | Esperado — a instituição não aceitaria que qualquer pessoa mude o cadastro de espaços. |
| **Vínculos** | UC: [UC-14 Cadastrar espaço](../casos-de-uso/README.md#uc-14) (exceção); também em [UC-15 Editar espaço](../casos-de-uso/README.md#uc-15), [UC-16 Desativar ou reativar espaço](../casos-de-uso/README.md#uc-16) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | 403 `ACAO_NAO_PERMITIDA`. `espacos/tests/test_api_espacos.py::test_solicitante_nao_cadastra_espaco_e_nada_e_gravado`; `espacos/tests/test_api_edicao_de_espaco.py::test_solicitante_nao_edita_desativa_nem_ativa_e_nada_muda [x]`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]` (linhas de `espacos:lista` POST, `espacos:detalhe` PATCH, `espacos:desativar` e `espacos:ativar`) |
| **Regras de negócio** | [Perfil](../glossario.md#perfil), [Gestor](../glossario.md#gestor) |
| **Decisões** | [DEC-04](../decisoes/DEC-04.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |
