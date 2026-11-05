# US-01 · Criar minha conta

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-01 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-01-criar-minha-conta.md` |

História do [índice](README.md#índice-das-histórias). Como ler o Index Card, o INVEST, os critérios e os testes de aceite: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-01 |
| **Título** | Criar minha conta |
| **História** | Como visitante da comunidade acadêmica, quero criar minha conta com nome, matrícula, e-mail e senha para pedir reservas sem depender de um Gestor. |
| **Valor** | Acesso imediato para quem quer usar um espaço; o setor dos espaços não precisa cadastrar cada pessoa, e todo pedido fica ligado a alguém identificado ([NS-15](../visao.md#necessidades)). |
| **Origem** | [UC-01 Cadastrar-se, passos 1 a 4](../casos-de-uso/fichas-resumidas.md#uc01-p1), com [A1.1](../casos-de-uso/fichas-resumidas.md#uc01-a1-1) e as exceções [E3.1 a E3.3](../casos-de-uso/fichas-resumidas.md#uc01-e3-1). |
| **Prioridade** | Esperado — a classe QFD mais alta entre [RF-32](../requisitos/rf-contas.md#rf-32), [RF-32.1](../requisitos/rf-contas.md#rf-32-1), [RF-32.2](../requisitos/rf-contas.md#rf-32-2) e [RF-32.3](../requisitos/rf-contas.md#rf-32-3), todos esperados ([SRS, seção 7](../requisitos/srs.md#7-análise-qfd)). |
| **Estimativa (Custo em Semanas)** | 0,3 (retrospectiva: o cadastro da AUT-04 e a tela de cadastro da AUT-06). |
| **Conversa** | "Qual é o formato real da matrícula?" → [DEC-09](../decisoes/DEC-09.md), adotada provisoriamente como "até 20 caracteres, sem espaços". "Alguém pode se cadastrar já como Gestor?" → não; o Gestor só é criado pela Equipe de TI ([DEC-04](../decisoes/DEC-04.md), [US-17](US-17-criar-o-primeiro-gestor.md)). "A matrícula é conferida com a instituição?" → não, fora do escopo ([L-06](../requisitos/srs.md#l-06)). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando (os automatizados na verificação do PR; o manual executado e registrado no ensaio), esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✓ | Não depende de nenhuma outra história: é a porta de entrada do Solicitante. [US-02](US-02-entrar-no-sistema.md) depende dela só para quem ainda não tem conta. |
| **N** · Negociável | ✓ | O formato da matrícula está aberto ([DEC-09](../decisoes/DEC-09.md)) e a política de senha pode mudar sem mudar a história. |
| **V** · Valiosa | ✓ | Sem ela, ninguém além dos usuários criados pela Equipe de TI consegue pedir uma reserva. |
| **E** · Estimável | ✓ | Escopo fechado (quatro dados, três recusas); custo retrospectivo conhecido. |
| **S** · Small | ✓ | Cabe numa iteração curta: uma conta, sem decisões de outro papel. |
| **T** · Testável | ✓ | Cada CA tem TA; só o retorno ao ponto de origem (CA-02) depende de roteiro manual ([L-15](../requisitos/srs.md#l-15)). |

**Diagnóstico:** US-01 atende às seis letras; o único ponto fraco é o CA-02, verificado só à mão.

## Critérios de aceite

#### <a id="us-01-ca-01"></a>US-01 · CA-01 · Conta criada (sucesso)

- **Dado** um visitante que ainda não tem conta
- **Quando** ele informa nome, matrícula, e-mail e uma senha que respeitam as regras do cadastro
- **Então** o sistema cria a conta com o perfil Solicitante, informa "Cadastro realizado com sucesso.", já o identifica, sem pedir a senha de novo, e o leva a pedir uma reserva
- **Origem:** [UC-01 passos 1 a 4](../casos-de-uso/fichas-resumidas.md#uc01-p1)
- **RF:** [RF-32](../requisitos/rf-contas.md#rf-32)
- **TA:** [TA-01](#ta-01)

#### <a id="us-01-ca-02"></a>US-01 · CA-02 · Volta ao ponto em que estava (alternativa)

- **Dado** um visitante que tentou ver algo que exige identificação e, no caminho para entrar, escolheu criar a conta
- **Quando** o cadastro termina
- **Então** o sistema o leva de volta ao ponto em que estava, e não ao pedido de reserva; um destino de fora do sistema é ignorado, e ele segue para o pedido de reserva
- **Origem:** [UC-01 A1.1](../casos-de-uso/fichas-resumidas.md#uc01-a1-1)
- **RF:** [RF-32](../requisitos/rf-contas.md#rf-32)
- **TA:** [TA-02](#ta-02)

#### <a id="us-01-ca-03"></a>US-01 · CA-03 · Dados ausentes ou inválidos (exceção)

- **Dado** um visitante preenchendo o cadastro
- **Quando** falta um dos dados, o nome só tem espaços ou passa do limite, a matrícula tem espaço ou passa do limite, ou o e-mail está mal formado
- **Então** o sistema aponta, junto a cada dado com problema, a regra violada (por exemplo, 'O campo "Nome" é obrigatório.'), não o identifica e nenhuma conta é criada
- **Origem:** [UC-01 E3.1](../casos-de-uso/fichas-resumidas.md#uc01-e3-1)
- **RF:** [RF-32.1](../requisitos/rf-contas.md#rf-32-1)
- **TA:** [TA-03](#ta-03)
- **Depende de:** [DEC-09](../decisoes/DEC-09.md) (o formato da matrícula pode mudar)

#### <a id="us-01-ca-04"></a>US-01 · CA-04 · Senha fraca (exceção)

- **Dado** um visitante preenchendo o cadastro com os outros dados corretos
- **Quando** a senha tem menos de 8 caracteres, é uma senha comum, só tem números ou se parece com o nome, o e-mail ou a matrícula
- **Então** o sistema mostra, junto à senha, cada motivo da recusa, e nenhuma conta é criada
- **Origem:** [UC-01 E3.2](../casos-de-uso/fichas-resumidas.md#uc01-e3-2)
- **RF:** [RF-32.2](../requisitos/rf-contas.md#rf-32-2)
- **TA:** [TA-04](#ta-04)

#### <a id="us-01-ca-05"></a>US-01 · CA-05 · E-mail ou matrícula já usados (exceção)

- **Dado** que já existe uma conta com um e-mail (mesmo escrito com maiúsculas diferentes) ou com uma matrícula
- **Quando** um visitante tenta se cadastrar com esse e-mail ou essa matrícula
- **Então** o sistema informa, junto ao dado, que ele já está cadastrado, não identifica o visitante, nenhuma conta é criada e a conta que já existia não muda
- **Origem:** [UC-01 E3.3](../casos-de-uso/fichas-resumidas.md#uc01-e3-3)
- **RF:** [RF-32.3](../requisitos/rf-contas.md#rf-32-3)
- **TA:** [TA-05](#ta-05)

#### <a id="us-01-ca-06"></a>US-01 · CA-06 · O cadastro nunca cria um Gestor (acesso)

- **Dado** um visitante criando a conta
- **Quando** o pedido de cadastro diz que ele deve ser Gestor ou administrador
- **Então** a conta é criada como Solicitante comum, sem nenhum poder de Gestor nem de administração
- **Origem:** [UC-01 passo 4](../casos-de-uso/fichas-resumidas.md#uc01-p4)
- **RF:** [RF-32](../requisitos/rf-contas.md#rf-32)
- **TA:** [TA-06](#ta-06)
- **Depende de:** [DEC-04](../decisoes/DEC-04.md) (decidida)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-01"></a>TA-01 | [CA-01](#us-01-ca-01) | automatizado | `contas/tests/test_api_cadastro.py::test_cadastro_valido_responde_201_com_solicitante_sem_senha`; `contas/tests/test_api_cadastro.py::test_usuario_recem_cadastrado_consegue_fazer_login`; `contas/tests/test_cadastrar_solicitante.py::test_cadastro_valido_cria_solicitante_com_dados_normalizados`; `pages/PaginaCadastro.test.tsx`: `com sucesso, cadastra, entra com as mesmas credenciais e vai para /reservas/nova` |
| <a id="ta-02"></a>TA-02 | [CA-02](#us-01-ca-02) | manual | **Precondição:** nenhuma sessão aberta. **Passos:** pedir para ver as reservas; no caminho para entrar, escolher criar a conta; cadastrar com dados novos e válidos. **Resultado esperado:** a pessoa termina identificada na lista das próprias reservas, e não no pedido de reserva. Apoio parcial automatizado (o destino é preservado até o cadastro, mas o retorno depois dele não é testado): `pages/PaginaEntrar.test.tsx`: `o link de cadastro preserva o ?proximo`; `navegacao.test.ts`: `proximoSeguro aceita o caminho interno %s`. Lacuna [L-15](../requisitos/srs.md#l-15). |
| <a id="ta-03"></a>TA-03 | [CA-03](#us-01-ca-03) | automatizado | `contas/tests/test_api_cadastro.py::test_campos_ausentes_respondem_400_com_cada_campo`; `contas/tests/test_api_cadastro.py::test_nome_so_com_espacos_responde_400_campo_obrigatorio`; `contas/tests/test_api_cadastro.py::test_matricula_com_espaco_responde_400`; `contas/tests/test_api_cadastro.py::test_email_malformado_responde_400`; `contas/tests/test_cadastro_dominio.py::test_nome_acima_do_limite_lanca_texto_muito_longo`; `contas/tests/test_cadastro_dominio.py::test_matricula_longa_ou_com_espaco_no_meio_lanca_matricula_invalida [x]` |
| <a id="ta-04"></a>TA-04 | [CA-04](#us-01-ca-04) | automatizado | `contas/tests/test_api_cadastro.py::test_senha_fraca_responde_400_com_motivos_em_senha`; `contas/tests/test_cadastrar_solicitante.py::test_senha_fraca_lanca_senha_fraca_sem_criar_usuario`; `pages/PaginaCadastro.test.tsx`: `senha fraca aparece embaixo da senha` |
| <a id="ta-05"></a>TA-05 | [CA-05](#us-01-ca-05) | automatizado | `contas/tests/test_api_cadastro.py::test_email_repetido_com_caixa_diferente_responde_409`; `contas/tests/test_api_cadastro.py::test_matricula_repetida_responde_409`; `pages/PaginaCadastro.test.tsx`: `e-mail já cadastrado aparece embaixo do e-mail, que recebe o foco, e não entra` |
| <a id="ta-06"></a>TA-06 | [CA-06](#us-01-ca-06) | automatizado | `contas/tests/test_api_cadastro.py::test_campos_de_privilegio_no_corpo_sao_ignorados` |
