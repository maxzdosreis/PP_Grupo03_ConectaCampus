# US-05 · Cadastrar espaço

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-05 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-05-cadastrar-espaco.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Marca "Depende de" das DECs confirmadas na Aula 7 (DEC-06, DEC-10, DEC-11) com "(decidida)" (GES-02). Nenhum Dado/Quando/Então muda. Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-19 e TA-20 passam a TA-20 e TA-21, e TA-21 a TA-158 passam a TA-24 a TA-161, para os TA-19, TA-22 e TA-23 novos da US-03 (revogação e troca da credencial de renovação) seguirem a ordem das histórias (AUT-09). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Index Card: o papel da história passa a ser Gestor do serviço ([DEC-25](../decisoes/DEC-25.md)); meta, valor, critérios e testes de aceite iguais (REQ-12). Mudança editorial, sem nova obrigação. Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-05 |
| **Título** | Cadastrar espaço |
| **História** | Como Gestor do serviço, quero cadastrar um espaço esportivo com nome, tipo e capacidade para que ele passe a aceitar pedidos de reserva. |
| **Valor** | A lista de espaços fica igual à realidade do campus, e cada espaço novo já pode ser pedido ([NS-02](../visao.md#necessidades)). |
| **Origem** | [UC-14 Cadastrar espaço, passos 1 a 8](../casos-de-uso/UC-14-cadastrar-espaco.md#p1), alternativa [A8.1](../casos-de-uso/UC-14-cadastrar-espaco.md#a8-1) e exceções [E1.1](../casos-de-uso/UC-14-cadastrar-espaco.md#e1-1) a [E7.1](../casos-de-uso/UC-14-cadastrar-espaco.md#e7-1). |
| **Prioridade** | Normal — [RF-05](../requisitos/rf-espacos.md#rf-05) e [RF-05.1](../requisitos/rf-espacos.md#rf-05-1) são normais (F1 do enunciado). |
| **Estimativa (Custo em Semanas)** | 0,5 (retrospectiva: domínio, persistência e API das ESP-01 a ESP-03 e o formulário da FE-02). |
| **Conversa** | "Dois espaços podem ter o mesmo nome, em prédios diferentes?" → não, adotado provisoriamente ([DEC-10](../decisoes/DEC-10.md)). "Um espaço pode ser excluído?" → nunca, só desativado ([DEC-06](../decisoes/DEC-06.md), [US-07](US-07-desativar-e-reativar-espaco.md)). "Os tipos são fixos?" → sim, cinco tipos na ordem do negócio. |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✓ | Só precisa de um Gestor ([US-17](US-17-criar-o-primeiro-gestor.md)), que é instalação; nenhuma história de negócio vem antes. |
| **N** · Negociável | ✗ | O nome único depende da [DEC-10](../decisoes/DEC-10.md), ainda sem resposta do cliente; se mudar, dois CAs (CA-09 e CA-10) deixam de existir. |
| **V** · Valiosa | ✓ | Sem espaços, nenhum pedido é possível: [US-04](US-04-consultar-os-espacos.md) e [US-08](US-08-solicitar-reserva.md) dependem dela. |
| **E** · Estimável | ✓ | Três dados, regras conhecidas. |
| **S** · Small | ✓ | Uma entidade e as recusas dela. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado, inclusive a corrida de dois cadastros com o mesmo nome. |

**Diagnóstico:** independente, valiosa e testável; só não é negociável enquanto a DEC-10 estiver aberta.

## Critérios de aceite

#### <a id="us-05-ca-01"></a>US-05 · CA-01 · Espaço cadastrado (sucesso)

- **Dado** um Gestor identificado
- **Quando** ele informa um nome que nenhum espaço usa, escolhe um dos tipos e informa uma capacidade de pelo menos 1
- **Então** o sistema informa "Espaço cadastrado com sucesso." e o espaço aparece na lista, ativo, com o nome sem espaços nas pontas nem repetidos, e passa a aceitar pedidos de reserva
- **Origem:** [UC-14 passos 1 a 8](../casos-de-uso/UC-14-cadastrar-espaco.md#p1)
- **RF:** [RF-05](../requisitos/rf-espacos.md#rf-05)
- **TA:** [TA-32](#ta-32)

#### <a id="us-05-ca-02"></a>US-05 · CA-02 · Tipos apresentados na ordem do negócio (sucesso)

- **Dado** um Gestor que vai cadastrar um espaço
- **Quando** ele escolhe o tipo
- **Então** o sistema apresenta os cinco tipos de espaço, nesta ordem: Quadra poliesportiva, Campo de futebol, Ginásio, Quadra de areia, Quadra de tênis
- **Origem:** [UC-14 passo 2](../casos-de-uso/UC-14-cadastrar-espaco.md#p2)
- **RF:** [RF-04](../requisitos/rf-espacos.md#rf-04)
- **TA:** [TA-33](#ta-33)

#### <a id="us-05-ca-03"></a>US-05 · CA-03 · Cadastrar outro espaço (alternativa)

- **Dado** um espaço que acabou de ser cadastrado
- **Quando** o Gestor vai cadastrar o próximo
- **Então** os dados do cadastro anterior não estão mais preenchidos, e a lista já mostra o espaço novo
- **Origem:** [UC-14 A8.1](../casos-de-uso/UC-14-cadastrar-espaco.md#a8-1)
- **RF:** [RF-05](../requisitos/rf-espacos.md#rf-05)
- **TA:** [TA-34](#ta-34)

#### <a id="us-05-ca-04"></a>US-05 · CA-04 · Dados ausentes ou em formato inválido (exceção)

- **Dado** um Gestor cadastrando um espaço
- **Quando** falta o nome, o tipo ou a capacidade, ou a capacidade não é um número inteiro (ou passa do maior valor que o sistema guarda)
- **Então** o sistema informa "Verifique os dados informados." e aponta o problema junto a cada dado, todos de uma vez; nenhum espaço é criado e a lista fica como estava
- **Origem:** [UC-14 E5.1](../casos-de-uso/UC-14-cadastrar-espaco.md#e5-1)
- **RF:** [RF-05.1](../requisitos/rf-espacos.md#rf-05-1)
- **TA:** [TA-35](#ta-35)

#### <a id="us-05-ca-05"></a>US-05 · CA-05 · Nome em branco (exceção)

- **Dado** um Gestor cadastrando um espaço
- **Quando** o nome só tem espaços
- **Então** o sistema informa, junto ao nome, 'O campo "Nome" é obrigatório.' e nenhum espaço é criado
- **Origem:** [UC-14 E5.2](../casos-de-uso/UC-14-cadastrar-espaco.md#e5-2)
- **RF:** [RF-05.1](../requisitos/rf-espacos.md#rf-05-1)
- **TA:** [TA-36](#ta-36)

#### <a id="us-05-ca-06"></a>US-05 · CA-06 · Nome longo demais (exceção)

- **Dado** um Gestor cadastrando um espaço
- **Quando** o nome passa de 100 caracteres depois de tirar os espaços das pontas e os repetidos (com exatamente 100, é aceito)
- **Então** o sistema informa, junto ao nome, "O nome do espaço deve ter no máximo 100 caracteres." e nenhum espaço é criado
- **Origem:** [UC-14 E5.3](../casos-de-uso/UC-14-cadastrar-espaco.md#e5-3)
- **RF:** [RF-05.1](../requisitos/rf-espacos.md#rf-05-1)
- **TA:** [TA-37](#ta-37)

#### <a id="us-05-ca-07"></a>US-05 · CA-07 · Tipo em branco ou desconhecido (exceção)

- **Dado** um Gestor cadastrando um espaço
- **Quando** o tipo não foi escolhido, ou não é um dos tipos de espaço
- **Então** o sistema informa, junto ao tipo, 'O campo "Tipo" é obrigatório.' ou que o tipo é inválido, listando os cinco tipos aceitos; nenhum espaço é criado
- **Origem:** [UC-14 E5.4](../casos-de-uso/UC-14-cadastrar-espaco.md#e5-4)
- **RF:** [RF-05.1](../requisitos/rf-espacos.md#rf-05-1), [RF-04](../requisitos/rf-espacos.md#rf-04)
- **TA:** [TA-38](#ta-38)

#### <a id="us-05-ca-08"></a>US-05 · CA-08 · Capacidade menor que 1 (exceção)

- **Dado** um Gestor cadastrando um espaço
- **Quando** a capacidade é zero ou negativa (com 1, é aceita)
- **Então** o sistema informa, junto à capacidade, "A capacidade deve ser um número inteiro maior que zero." e nenhum espaço é criado
- **Origem:** [UC-14 E5.5](../casos-de-uso/UC-14-cadastrar-espaco.md#e5-5)
- **RF:** [RF-05.1](../requisitos/rf-espacos.md#rf-05-1)
- **TA:** [TA-39](#ta-39)

#### <a id="us-05-ca-09"></a>US-05 · CA-09 · Nome já usado por outro espaço (exceção)

- **Dado** um espaço chamado "Ginásio A", ativo ou inativo
- **Quando** o Gestor tenta cadastrar outro com o nome "ginásio  a" (outras maiúsculas e espaços repetidos)
- **Então** o sistema informa, junto ao nome, "Já existe um espaço com este nome."; nenhum espaço é criado e o "Ginásio A" não muda
- **Origem:** [UC-14 E6.1](../casos-de-uso/UC-14-cadastrar-espaco.md#e6-1)
- **RF:** [RF-05.2](../requisitos/rf-espacos.md#rf-05-2)
- **TA:** [TA-40](#ta-40)
- **Depende de:** [DEC-10](../decisoes/DEC-10.md) (decidida)

#### <a id="us-05-ca-10"></a>US-05 · CA-10 · Nome repetido por um cadastro simultâneo (exceção)

- **Dado** dois Gestores cadastrando, quase ao mesmo tempo, espaços com o mesmo nome (sem diferenciar maiúsculas)
- **Quando** os dois enviam o cadastro
- **Então** só o primeiro espaço existe; o segundo recebe a mesma mensagem do CA-09, junto ao nome
- **Origem:** [UC-14 E7.1](../casos-de-uso/UC-14-cadastrar-espaco.md#e7-1)
- **RF:** [RF-05.2](../requisitos/rf-espacos.md#rf-05-2)
- **TA:** [TA-41](#ta-41)
- **Depende de:** [DEC-10](../decisoes/DEC-10.md) (decidida)

#### <a id="us-05-ca-11"></a>US-05 · CA-11 · Só o Gestor cadastra (acesso)

- **Dado** um Solicitante identificado, ou um Gestor que a Equipe de TI acabou de rebaixar a Solicitante
- **Quando** ele tenta cadastrar um espaço
- **Então** o sistema informa "Você não tem permissão para realizar esta ação." antes de conferir qualquer dado, nenhum espaço é criado e, para o Solicitante, o cadastro nem é oferecido: ele vê o aviso de que somente o gestor cadastra espaços
- **Origem:** [UC-14 E1.1](../casos-de-uso/UC-14-cadastrar-espaco.md#e1-1)
- **RF:** [RF-10](../requisitos/rf-espacos.md#rf-10)
- **TA:** [TA-42](#ta-42)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-32"></a>TA-32 | [CA-01](#us-05-ca-01) | automatizado | `espacos/tests/test_api_espacos.py::test_cadastrar_espaco_valido_responde_201_com_o_espaco`; `espacos/tests/test_api_espacos.py::test_espaco_cadastrado_aparece_na_listagem`; `espacos/tests/test_api_espacos.py::test_cadastrar_aceita_capacidade_numerica_em_texto`; `espacos/tests/test_casos_de_uso.py::test_cadastrar_espaco_valido_devolve_com_id_e_aparece_na_listagem`; `espacos/tests/test_espaco_esportivo.py::test_criacao_valida_normaliza_nome_e_converte_tipo` |
| <a id="ta-33"></a>TA-33 | [CA-02](#us-05-ca-02) | automatizado | `espacos/tests/test_api_espacos.py::test_tipos_de_espaco_lista_todos_os_tipos_na_ordem_do_enum`; `espacos/tests/test_api_espacos.py::test_tipos_de_espaco_nao_exigem_login` |
| <a id="ta-34"></a>TA-34 | [CA-03](#us-05-ca-03) | automatizado | `pages/PaginaEspacos.test.tsx`: `cadastro com sucesso mostra o toast, limpa o formulário e recarrega a lista` |
| <a id="ta-35"></a>TA-35 | [CA-04](#us-05-ca-04) | automatizado | `espacos/tests/test_api_espacos.py::test_cadastro_invalido_responde_erro_e_preserva_a_listagem [sem-nome, capacidade-texto, capacidade-acima-do-banco]`; `pages/PaginaEspacos.test.tsx`: `erro de campo aparece embaixo do campo, recebe o foco e some ao editar` |
| <a id="ta-36"></a>TA-36 | [CA-05](#us-05-ca-05) | automatizado | `espacos/tests/test_espaco_esportivo.py::test_nome_vazio_e_recusado_como_campo_obrigatorio [x]`; `espacos/tests/test_api_espacos.py::test_cadastro_invalido_responde_erro_e_preserva_a_listagem [nome-so-com-espacos]` |
| <a id="ta-37"></a>TA-37 | [CA-06](#us-05-ca-06) | automatizado | `espacos/tests/test_espaco_esportivo.py::test_nome_no_limite_de_caracteres_e_aceito`; `espacos/tests/test_espaco_esportivo.py::test_nome_acima_do_limite_de_caracteres_e_recusado`; `espacos/tests/test_api_espacos.py::test_cadastro_invalido_responde_erro_e_preserva_a_listagem [nome-longo]` |
| <a id="ta-38"></a>TA-38 | [CA-07](#us-05-ca-07) | automatizado | `espacos/tests/test_espaco_esportivo.py::test_tipo_vazio_e_recusado_como_campo_obrigatorio [x]`; `espacos/tests/test_espaco_esportivo.py::test_tipo_desconhecido_e_recusado_listando_os_tipos_aceitos`; `espacos/tests/test_api_espacos.py::test_cadastro_invalido_responde_erro_e_preserva_a_listagem [tipo-vazio, tipo-desconhecido]` |
| <a id="ta-39"></a>TA-39 | [CA-08](#us-05-ca-08) | automatizado | `espacos/tests/test_espaco_esportivo.py::test_capacidade_que_nao_e_inteiro_positivo_e_recusada [x]`; `espacos/tests/test_espaco_esportivo.py::test_capacidade_minima_e_aceita`; `espacos/tests/test_api_espacos.py::test_cadastro_invalido_responde_erro_e_preserva_a_listagem [capacidade-zero]` |
| <a id="ta-40"></a>TA-40 | [CA-09](#us-05-ca-09) | automatizado | `espacos/tests/test_casos_de_uso.py::test_cadastrar_nome_repetido_com_caixa_e_espacos_diferentes_lanca_conflito`; `espacos/tests/test_api_espacos.py::test_cadastro_invalido_responde_erro_e_preserva_a_listagem [nome-repetido]`; `espacos/tests/test_propriedades_do_espaco.py::test_cadastrar_varios_nomes_termina_com_nomes_unicos_sem_diferenciar_caixa`; `pages/PaginaEspacos.test.tsx`: `nome repetido aparece no campo Nome` |
| <a id="ta-41"></a>TA-41 | [CA-10](#us-05-ca-10) | automatizado | `espacos/tests/test_repositorio_espacos.py::test_salvar_nome_repetido_com_caixa_diferente_lanca_nome_ja_cadastrado` (simula a corrida: a gravação recusa o nome que passou pela conferência) |
| <a id="ta-42"></a>TA-42 | [CA-11](#us-05-ca-11) | automatizado | `espacos/tests/test_api_espacos.py::test_solicitante_nao_cadastra_espaco_e_nada_e_gravado`; `config/tests/test_perfil_lido_do_banco.py::test_gestor_rebaixado_perde_as_permissoes_com_o_mesmo_token`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]`; `pages/PaginaEspacos.test.tsx`: `para o solicitante, troca o formulário por um aviso e lista os espaços` |
