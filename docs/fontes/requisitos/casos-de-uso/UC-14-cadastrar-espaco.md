# UC-14 · Cadastrar espaço

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **UC-14 • 0.1 • Rascunho** (ficha completa, formato Cockburn) | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/casos-de-uso/UC-14-cadastrar-espaco.md` |

Ficha do caso de uso UC-14 do [índice](README.md#uc-14). Editar, desativar e reativar um espaço são os casos de uso UC-15 e UC-16, nas [fichas resumidas](fichas-resumidas.md#uc-15), e reaproveitam as regras desta ficha. Como ler a numeração: [decisões h e i](README.md#decisao-h).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: fluxo principal, exceções na ordem real das verificações, garantias, RF cobertos e evidência (REQ-04). Sem aprovação. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Linha "Histórias derivadas" (REQ-05), sem mudar o fluxo. Sem aprovação. |

## Sumário

1. [Identificação do caso de uso](#identificação-do-caso-de-uso)
2. [Stakeholders e interesses](#stakeholders-e-interesses)
3. [Fluxo principal](#fluxo-principal)
4. [Alternativas](#alternativas)
5. [Exceções](#exceções)
6. [Pós-condições e garantias](#pós-condições-e-garantias)
7. [Regras de negócio](#regras-de-negócio)
8. [RFs cobertos](#rfs-cobertos)
9. [RNFs relacionados](#rnfs-relacionados)
10. [Questões em aberto](#questões-em-aberto)
11. [Anexo — Evidência (complementar)](#anexo--evidência-complementar)

## Identificação do caso de uso

| Campo | Conteúdo |
|---|---|
| **Escopo** | Conecta Campus (caixa-preta). |
| **Nível** | Objetivo do usuário. |
| **Ator primário** | [Gestor](../glossario.md#gestor). |
| **Atores secundários** | Nenhum ([decisão f](README.md#decisao-f)). |
| **Meta de contexto** | Incluir um [espaço esportivo](../glossario.md#espaco-esportivo) novo na lista, para que ele passe a aceitar pedidos de reserva. |
| **Precondições** | O ator é um [usuário autenticado](../glossario.md#usuario-autenticado) com o perfil Gestor ([UC-02 Autenticar](UC-02-autenticar.md); [decisão d](README.md#decisao-d)). |
| **Disparador** | Um espaço passou a poder ser usado pela comunidade (uma quadra nova, um espaço que ainda não estava no sistema). |

## Stakeholders e interesses

| Stakeholder | Interesse neste caso de uso |
|---|---|
| **Gestor** | Cadastrar em uma ação, escolhendo o tipo entre os existentes; ser avisado na hora se o nome já existe ou se algum dado está fora das regras, sem perder o que digitou. |
| **Solicitante** | Encontrar o espaço novo pelo nome e pelo tipo e poder pedir reservas nele logo depois do cadastro; não confundir dois espaços com o mesmo nome. |
| **Cliente** (instituição) | Só o setor responsável mantém a lista de espaços; a lista corresponde à realidade, sem nomes repetidos nem capacidades impossíveis. |

## Fluxo principal

1. <a id="p1"></a>O Gestor pede para cadastrar um espaço.
2. <a id="p2"></a>O sistema apresenta os [tipos de espaço](../glossario.md#tipo-de-espaco) existentes, na ordem do negócio (Quadra poliesportiva, Campo de futebol, Ginásio, Quadra de areia, Quadra de tênis).
3. <a id="p3"></a>O Gestor informa o nome, escolhe o tipo e informa a [capacidade](../glossario.md#capacidade).
4. <a id="p4"></a>O Gestor envia o cadastro.
5. <a id="p5"></a>O sistema confere os dados, nesta ordem: todos presentes e no formato esperado; nome; tipo; capacidade.
6. <a id="p6"></a>O sistema confere que nenhum espaço já tem esse nome, sem diferenciar maiúsculas de minúsculas e comparando o nome já sem espaços nas pontas nem repetidos.
7. <a id="p7"></a>O sistema grava o espaço [ativo](../glossario.md#espaco-ativo), com o nome normalizado.
8. <a id="p8"></a>O sistema informa "Espaço cadastrado com sucesso." e mostra o espaço na lista, ativo e aceitando pedidos de reserva.

## Alternativas

A meta ainda é alcançada.

#### <a id="a8-1"></a>A8.1 · Cadastrar outro espaço

Depois do passo 8, o Gestor cadastra outro espaço. O sistema volta ao passo 3, com os dados em branco.

#### <a id="a8-2"></a>A8.2 · Pedir uma reserva no espaço recém-cadastrado

Depois do passo 8, o Gestor (ou qualquer Solicitante) pede uma reserva no espaço novo: segue em [UC-04 A1.1](UC-04-solicitar-reserva.md#a1-1), com o espaço já escolhido.

## Exceções

A meta é interrompida: **nenhum espaço é criado** e a lista de espaços fica exatamente como estava; os dados informados continuam com o Gestor para ele corrigir só o que foi apontado (volta ao passo 3). A ordem é a ordem real das verificações ([evidência da ordem](#evidencia-da-ordem)): no passo 5, os dados ausentes ou mal formados aparecem todos de uma vez; daí em diante, uma regra por vez.

#### <a id="e1-1"></a>E1.1 · Ator sem o perfil Gestor

- **Condição:** no passo 1 (ou ao enviar, no passo 4), quem pede não tem o perfil Gestor. A permissão é conferida antes de qualquer dado.
- **Resultado para o ator:** "Você não tem permissão para realizar esta ação."; para o Solicitante, o sistema também indica que somente o gestor cadastra espaços e não oferece o cadastro.
- **Estado depois:** nenhum espaço é criado; os dados enviados nem são conferidos.
- **Requisito:** [RF-10](../requisitos/rf-espacos.md#rf-10).

#### <a id="e5-1"></a>E5.1 · Dados ausentes ou em formato inválido

- **Condição:** no passo 5, falta o nome, o tipo ou a capacidade, ou a capacidade não é um número inteiro (ou passa do maior valor que o sistema guarda).
- **Resultado para o ator:** "Verifique os dados informados.", com o problema junto a cada dado, todos de uma vez.
- **Estado depois:** nenhum espaço é criado.
- **Requisito:** [RF-05.1](../requisitos/rf-espacos.md#rf-05-1).

#### <a id="e5-2"></a>E5.2 · Nome em branco

- **Condição:** no passo 5, o nome só tem espaços.
- **Resultado para o ator:** junto ao nome, 'O campo "Nome" é obrigatório.'
- **Estado depois:** nenhum espaço é criado.
- **Requisito:** [RF-05.1](../requisitos/rf-espacos.md#rf-05-1).

#### <a id="e5-3"></a>E5.3 · Nome longo demais

- **Condição:** no passo 5, o nome passa de 100 caracteres depois de tirar os espaços das pontas e os repetidos.
- **Resultado para o ator:** junto ao nome, "O nome do espaço deve ter no máximo 100 caracteres."
- **Estado depois:** nenhum espaço é criado.
- **Requisito:** [RF-05.1](../requisitos/rf-espacos.md#rf-05-1).

#### <a id="e5-4"></a>E5.4 · Tipo em branco ou desconhecido

- **Condição:** no passo 5, o tipo não foi escolhido, ou não é um dos tipos de espaço.
- **Resultado para o ator:** junto ao tipo, 'O campo "Tipo" é obrigatório.' ou "Tipo de espaço inválido. Escolha um destes: Quadra poliesportiva, Campo de futebol, Ginásio, Quadra de areia, Quadra de tênis."
- **Estado depois:** nenhum espaço é criado.
- **Requisito:** [RF-05.1](../requisitos/rf-espacos.md#rf-05-1) (os tipos aceitos são os de [RF-04](../requisitos/rf-espacos.md#rf-04)).

#### <a id="e5-5"></a>E5.5 · Capacidade inválida

- **Condição:** no passo 5, a capacidade é menor que 1.
- **Resultado para o ator:** junto à capacidade, "A capacidade deve ser um número inteiro maior que zero."
- **Estado depois:** nenhum espaço é criado.
- **Requisito:** [RF-05.1](../requisitos/rf-espacos.md#rf-05-1).

#### <a id="e6-1"></a>E6.1 · Nome já usado por outro espaço

- **Condição:** no passo 6, já existe um espaço com o mesmo nome, sem diferenciar maiúsculas de minúsculas (por exemplo, "ginásio  a" e "Ginásio A"), ativo ou inativo.
- **Resultado para o ator:** junto ao nome, "Já existe um espaço com este nome." O Gestor escolhe outro nome.
- **Estado depois:** nenhum espaço é criado; o espaço que já tinha o nome não muda.
- **Requisito:** [RF-05.2](../requisitos/rf-espacos.md#rf-05-2) ([DEC-10](../decisoes/DEC-10.md)).

#### <a id="e7-1"></a>E7.1 · Nome repetido descoberto na gravação, por um cadastro simultâneo

- **Condição:** no passo 7, outro cadastro com o mesmo nome (sem diferenciar maiúsculas) foi gravado depois da conferência do passo 6 deste.
- **Resultado para o ator:** a mesma mensagem de [E6.1](#e6-1), junto ao nome.
- **Estado depois:** só o primeiro espaço existe.
- **Requisito:** [RF-05.2](../requisitos/rf-espacos.md#rf-05-2) (a garantia final é a do banco de dados, [DEC-10](../decisoes/DEC-10.md)).

**Fora das exceções:** sem identificação, o pedido não chega ao passo 1 (precondição; [UC-02 E4.1](UC-02-autenticar.md#e4-1)). Informar o espaço como inativo no cadastro não é possível: todo espaço nasce ativo, e desativar é [UC-16](fichas-resumidas.md#uc-16).

## Pós-condições e garantias

| Campo | Conteúdo |
|---|---|
| **Pós-condições (sucesso)** | Existe um espaço novo, ativo, com o nome normalizado, o tipo escolhido e a capacidade informada. Ele aparece na lista de espaços (em ordem de nome), no filtro por tipo e entre os espaços que aceitam pedidos de reserva. |
| **Garantia de sucesso** | O espaço respeita todas as regras do cadastro e tem um nome que nenhum outro espaço usa, sem diferenciar maiúsculas de minúsculas. |
| **Garantia mínima** | Mesmo quando a meta falha: nenhum espaço é criado pela metade ou fora das regras; a lista de espaços não muda; só um Gestor consegue cadastrar. |

## Regras de negócio

- [Espaço esportivo](../glossario.md#espaco-esportivo): nome obrigatório, normalizado, até 100 caracteres; [tipo de espaço](../glossario.md#tipo-de-espaco) entre os existentes; [capacidade](../glossario.md#capacidade) inteira e no mínimo 1.
- Nome único sem diferenciar maiúsculas de minúsculas ([DEC-10](../decisoes/DEC-10.md)).
- Todo espaço nasce [ativo](../glossario.md#espaco-ativo) e nunca é excluído, só desativado ([DEC-06](../decisoes/DEC-06.md)).
- Só o [Gestor](../glossario.md#gestor) mantém espaços ([DEC-04](../decisoes/DEC-04.md)).

## RFs cobertos

Todos os RF que a [rastreabilidade RF → UC](README.md#rastreabilidade-rf--uc) atribui a UC-14, inclusive em "também em".

| RF | Título | Onde entra nesta ficha |
|---|---|---|
| [RF-04](../requisitos/rf-espacos.md#rf-04) | Consultar os tipos de espaço | [passo 2](#p2); [E5.4](#e5-4) |
| [RF-05](../requisitos/rf-espacos.md#rf-05) | Cadastrar espaço | fluxo principal, [passos 1 a 8](#p1) |
| [RF-05.1](../requisitos/rf-espacos.md#rf-05-1) | Recusar espaço com dados inválidos | [E5.1](#e5-1), [E5.2](#e5-2), [E5.3](#e5-3), [E5.4](#e5-4), [E5.5](#e5-5) |
| [RF-05.2](../requisitos/rf-espacos.md#rf-05-2) | Recusar nome de espaço repetido | [E6.1](#e6-1), [E7.1](#e7-1) |
| [RF-10](../requisitos/rf-espacos.md#rf-10) | Recusar manutenção de espaço por quem não é Gestor | [E1.1](#e1-1) |

[RF-38](../requisitos/rf-gerais.md#rf-38) é transversal ([passo 8](#p8) e todas as exceções).

## RNFs relacionados

| RNF | Onde pesa nesta ficha |
|---|---|
| [RNF-F04](../requisitos/rnf.md#rnf-f04) · Identificação obrigatória por padrão | precondição |
| [RNF-F08](../requisitos/rnf.md#rnf-f08) · Perfil relido a cada operação | [E1.1](#e1-1): um Gestor rebaixado perde o cadastro na hora |
| [RNF-U01](../requisitos/rnf.md#rnf-u01) · Mensagens em português que orientam a correção | todas as exceções |
| [RNF-R03](../requisitos/rnf.md#rnf-r03) · Operação recusada não muda nada | garantia mínima |
| [RNF-R05](../requisitos/rnf.md#rnf-r05) · Nada é excluído | não há exclusão de espaço |
| [RNF-R06](../requisitos/rnf.md#rnf-r06) · Nenhuma regra violada vira erro interno | todas as exceções |

## Questões em aberto

| DEC | Como afeta este caso de uso |
|---|---|
| [DEC-10](../decisoes/DEC-10.md) · Nome de espaço único | Se o cliente aceitar nomes repetidos (por exemplo, em prédios diferentes), [E6.1](#e6-1) e [E7.1](#e7-1) deixam de existir. |
| [DEC-06](../decisoes/DEC-06.md) · Reservas de um espaço desativado | Define o que acontece com o espaço depois, em [UC-16](fichas-resumidas.md#uc-16). |
| [DEC-04](../decisoes/DEC-04.md) · Autenticação e perfis (decidida) | Só o Gestor cadastra ([E1.1](#e1-1)). |

## Anexo — Evidência (complementar)

Ponte para os critérios e testes de aceite (REQ-05 e REQ-06). Testes a partir de `src/backend/`, salvo os do frontend (`src/frontend/src/`); `[x]` = teste parametrizado. Fontes: [`testes_de_espacos.md`](../../testes_de_espacos.md) e [rf-espacos](../requisitos/rf-espacos.md).

| Item | Testes que o comprovam |
|---|---|
| [Fluxo principal](#p1) | `espacos/tests/test_api_espacos.py::test_cadastrar_espaco_valido_responde_201_com_o_espaco`, `::test_espaco_cadastrado_aparece_na_listagem`, `::test_cadastrar_aceita_capacidade_numerica_em_texto`; `espacos/tests/test_casos_de_uso.py::test_cadastrar_espaco_valido_devolve_com_id_e_aparece_na_listagem`; `espacos/tests/test_espaco_esportivo.py::test_criacao_valida_normaliza_nome_e_converte_tipo`; `pages/PaginaEspacos.test.tsx` |
| [Passo 2](#p2) | `espacos/tests/test_api_espacos.py::test_tipos_de_espaco_lista_todos_os_tipos_na_ordem_do_enum`, `::test_tipos_de_espaco_nao_exigem_login` |
| [E1.1](#e1-1) | `espacos/tests/test_api_espacos.py::test_solicitante_nao_cadastra_espaco_e_nada_e_gravado`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]` (`espacos:lista` POST); `config/tests/test_perfil_lido_do_banco.py::test_gestor_rebaixado_perde_as_permissoes_com_o_mesmo_token`; `pages/PaginaEspacos.test.tsx` |
| [E5.1](#e5-1) | `espacos/tests/test_api_espacos.py::test_cadastro_invalido_responde_erro_e_preserva_a_listagem [sem-nome, capacidade-texto, capacidade-acima-do-banco]` |
| [E5.2](#e5-2) | `espacos/tests/test_espaco_esportivo.py::test_nome_vazio_e_recusado_como_campo_obrigatorio [x]`; `espacos/tests/test_api_espacos.py::test_cadastro_invalido_responde_erro_e_preserva_a_listagem [nome-so-com-espacos]` |
| [E5.3](#e5-3) | `espacos/tests/test_espaco_esportivo.py::test_nome_no_limite_de_caracteres_e_aceito`, `::test_nome_acima_do_limite_de_caracteres_e_recusado`; `espacos/tests/test_api_espacos.py::test_cadastro_invalido_responde_erro_e_preserva_a_listagem [nome-longo]` |
| [E5.4](#e5-4) | `espacos/tests/test_espaco_esportivo.py::test_tipo_vazio_e_recusado_como_campo_obrigatorio [x]`, `::test_tipo_desconhecido_e_recusado_listando_os_tipos_aceitos`; `espacos/tests/test_api_espacos.py::test_cadastro_invalido_responde_erro_e_preserva_a_listagem [tipo-vazio, tipo-desconhecido]` |
| [E5.5](#e5-5) | `espacos/tests/test_espaco_esportivo.py::test_capacidade_que_nao_e_inteiro_positivo_e_recusada [x]`, `::test_capacidade_minima_e_aceita`; `espacos/tests/test_api_espacos.py::test_cadastro_invalido_responde_erro_e_preserva_a_listagem [capacidade-zero]` |
| [E6.1](#e6-1) | `espacos/tests/test_casos_de_uso.py::test_cadastrar_nome_repetido_com_caixa_e_espacos_diferentes_lanca_conflito`; `espacos/tests/test_api_espacos.py::test_cadastro_invalido_responde_erro_e_preserva_a_listagem [nome-repetido]`; `espacos/tests/test_propriedades_do_espaco.py::test_cadastrar_varios_nomes_termina_com_nomes_unicos_sem_diferenciar_caixa` |
| [E7.1](#e7-1) | `espacos/tests/test_repositorio_espacos.py::test_salvar_nome_repetido_com_caixa_diferente_lanca_nome_ja_cadastrado` |

<a id="evidencia-da-ordem"></a>**Ordem das exceções.** E1.1 antes dos dados: a permissão do Gestor é aplicada a todo pedido de cadastro antes de lê-lo (`EspacosView`, `metodos_do_gestor`). E5.1 é a conferência de formato, que aponta todos os dados de uma vez. E5.2 → E5.3 → E5.4 → E5.5 é a ordem do construtor de `EspacoEsportivo` (nome, tipo, capacidade), provada por `espacos/tests/test_propriedades_do_espaco.py::test_entrada_invalida_lanca_so_o_erro_de_dominio_do_primeiro_campo_invalido`. E6.1 só depois dos dados válidos (`CadastrarEspaco.executar`: entidade, `existe_com_nome`, `salvar`), provado por `espacos/tests/test_casos_de_uso.py::test_cadastrar_com_dado_invalido_propaga_erro_do_dominio_sem_salvar`.

**Histórias derivadas:** [US-05 Cadastrar espaço](../historias/US-05-cadastrar-espaco.md). Cobertura de cada alternativa e exceção: [historias/README.md](../historias/README.md#cobertura-uc--usca).
