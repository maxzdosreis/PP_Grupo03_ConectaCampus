# US-02 · Entrar no sistema

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-02 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-02-entrar-no-sistema.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | CA-06 · Tentativas em excesso, com o TA-12, antes do CA de acesso (agora CA-07, TA-13), como pede a ordem sucesso → alternativa → exceção → acesso; os TAs seguintes, em todas as histórias, andam uma posição (TA-13 a TA-157), porque a numeração global segue a ordem das histórias ([decisão b](README.md#decisao-b)); os CAs de exceção apontam para UC-02 E3.2 e E3.3, renumeradas; a Conversa e o INVEST deixam de citar a L-03 como aceita (AUT-08). Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | TA-12 cita o teste de tentativas simultâneas (contagem atômica, AUT-08). Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-07 a TA-13 passam a TA-11 a TA-17 (e os CAs seguintes na mesma história, quando há CA novo antes deles), para os 25 TAs pendentes novos seguirem a ordem das histórias (REQ-13). A especificação está adiante do código de propósito. Mudança comportamental da especificação nos CAs novos; a renumeração é editorial, sem nova obrigação. Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-02 |
| **Título** | Entrar no sistema |
| **História** | Como pessoa que já tem conta, quero entrar com meu e-mail e minha senha para agir com o meu nome e o meu perfil. |
| **Valor** | O sistema sabe quem pede e quem decide; só quem tem autoridade decide sobre os pedidos ([NS-11](../visao.md#necessidades)). |
| **Origem** | [UC-02 Autenticar, passos 1 a 4](../casos-de-uso/UC-02-autenticar.md#p1), alternativas [A1.1](../casos-de-uso/UC-02-autenticar.md#a1-1) e [A1.2](../casos-de-uso/UC-02-autenticar.md#a1-2) e exceções [E3.1](../casos-de-uso/UC-02-autenticar.md#e3-1), [E3.2](../casos-de-uso/UC-02-autenticar.md#e3-2) e [E3.3](../casos-de-uso/UC-02-autenticar.md#e3-3). A sessão depois da entrada é a [US-03](US-03-manter-e-encerrar-a-sessao.md). |
| **Prioridade** | Esperado — a classe QFD mais alta entre [RF-33](../requisitos/rf-contas.md#rf-33), [RF-33.1](../requisitos/rf-contas.md#rf-33-1) e [RF-33.2](../requisitos/rf-contas.md#rf-33-2). |
| **Estimativa (Custo em Semanas)** | 0,3 (retrospectiva: login da AUT-03, tela e redirecionamento da AUT-06). |
| **Conversa** | "Quantas tentativas erradas são permitidas?" → 5 por minuto com o mesmo e-mail e 20 por minuto da mesma origem ([RNF-F12](../requisitos/rnf.md#rnf-f12); a [L-03](../requisitos/srs.md#l-03) foi resolvida pela AUT-08). "A resposta deve dizer se o e-mail existe?" → não ([RNF-F05](../requisitos/rnf.md#rnf-f05)). "A entrada sem e-mail ou senha precisa de um requisito próprio?" → sim, na 0.2 ([L-14](../requisitos/srs.md#l-14)). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Depende de existir uma conta: [US-01](US-01-criar-minha-conta.md) para o Solicitante ou [US-17](US-17-criar-o-primeiro-gestor.md) para o Gestor. |
| **N** · Negociável | ✓ | O destino depois da entrada e os valores do limite de tentativas ([RNF-F12](../requisitos/rnf.md#rnf-f12), configuráveis) podem ser combinados sem mudar a meta. |
| **V** · Valiosa | ✓ | É a precondição de todas as histórias do Solicitante e do Gestor. |
| **E** · Estimável | ✓ | Fluxo curto e conhecido. |
| **S** · Small | ✓ | Uma entrada, três recusas. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado. |

**Diagnóstico:** valiosa, pequena e testável, mas não é independente: só tem sentido depois de US-01 ou US-17.

## Critérios de aceite

#### <a id="us-02-ca-01"></a>US-02 · CA-01 · Entrada aceita (sucesso)

- **Dado** uma pessoa com conta ativa
- **Quando** ela informa o e-mail (mesmo com maiúsculas diferentes ou espaços nas pontas) e a senha certa
- **Então** o sistema informa "Login realizado com sucesso.", passa a mostrar quem está identificado, pelo nome e pelo perfil, e a leva às próprias reservas
- **Origem:** [UC-02 passos 1 a 4](../casos-de-uso/UC-02-autenticar.md#p1)
- **RF:** [RF-33](../requisitos/rf-contas.md#rf-33)
- **TA:** [TA-11](#ta-11)

#### <a id="us-02-ca-02"></a>US-02 · CA-02 · Volta ao ponto em que estava (alternativa)

- **Dado** uma pessoa não identificada que tentou ver algo que exige identificação, com critérios escolhidos
- **Quando** ela entra
- **Então** o sistema a leva de volta ao mesmo ponto, com os mesmos critérios; se o destino pedido for de fora do sistema, ele é ignorado e ela segue para as próprias reservas
- **Origem:** [UC-02 A1.1](../casos-de-uso/UC-02-autenticar.md#a1-1)
- **RF:** [RF-33](../requisitos/rf-contas.md#rf-33)
- **TA:** [TA-12](#ta-12)

#### <a id="us-02-ca-03"></a>US-02 · CA-03 · Ainda não tem conta (alternativa)

- **Dado** um visitante que ainda não tem conta e chegou para entrar
- **Quando** ele escolhe criar a conta
- **Então** o sistema o leva ao cadastro mantendo o destino que ele queria, e ao fim do cadastro ele já está identificado, sem passar de novo pela entrada
- **Origem:** [UC-02 A1.2](../casos-de-uso/UC-02-autenticar.md#a1-2)
- **RF:** [RF-33](../requisitos/rf-contas.md#rf-33), [RF-32](../requisitos/rf-contas.md#rf-32)
- **TA:** [TA-13](#ta-13)

#### <a id="us-02-ca-04"></a>US-02 · CA-04 · E-mail ou senha não informados (exceção)

- **Dado** uma pessoa tentando entrar
- **Quando** ela não informa o e-mail ou a senha, ou o e-mail não tem formato de e-mail
- **Então** o sistema informa "Verifique os dados informados." e, junto a cada dado, o que falta ou está mal formado; as credenciais nem são conferidas e nenhuma sessão é iniciada
- **Origem:** [UC-02 E3.2](../casos-de-uso/UC-02-autenticar.md#e3-2)
- **RF:** [RF-33](../requisitos/rf-contas.md#rf-33) (sem RF de recusa próprio: [L-14](../requisitos/srs.md#l-14))
- **TA:** [TA-14](#ta-14)

#### <a id="us-02-ca-05"></a>US-02 · CA-05 · Credenciais inválidas (exceção)

- **Dado** um e-mail que não está cadastrado, uma senha errada ou uma conta desativada
- **Quando** a pessoa tenta entrar
- **Então** o sistema responde "E-mail ou senha incorretos." — a mesma mensagem nos três casos, sem revelar se o e-mail existe —, nenhuma sessão é iniciada e o último acesso da conta não muda
- **Origem:** [UC-02 E3.3](../casos-de-uso/UC-02-autenticar.md#e3-3)
- **RF:** [RF-33.1](../requisitos/rf-contas.md#rf-33-1)
- **TA:** [TA-15](#ta-15)

#### <a id="us-02-ca-06"></a>US-02 · CA-06 · Tentativas em excesso (exceção)

- **Dado** que já houve 5 tentativas de entrada com o mesmo e-mail no último minuto, certas ou erradas (ou 20 a partir do mesmo computador, com qualquer e-mail)
- **Quando** a pessoa tenta entrar de novo com esse e-mail, mesmo com a senha certa
- **Então** o sistema recusa sem conferir a senha, informa "Muitas tentativas. Tente de novo em N segundos." com o tempo que falta, não diz qual limite foi atingido nem se o e-mail existe, e nenhuma sessão é iniciada; depois desse tempo, a entrada volta a ser aceita, e outro e-mail continua entrando normalmente
- **Origem:** [UC-02 E3.1](../casos-de-uso/UC-02-autenticar.md#e3-1)
- **RF:** [RF-33.2](../requisitos/rf-contas.md#rf-33-2)
- **TA:** [TA-16](#ta-16)

#### <a id="us-02-ca-07"></a>US-02 · CA-07 · Sem identificação, nada além do que é público (acesso)

- **Dado** uma pessoa que não entrou
- **Quando** ela tenta consultar espaços ou reservas
- **Então** o sistema não mostra nenhum dado e pede que ela se identifique; só os tipos de espaço, as situações de reserva, as regras de agenda e a verificação do sistema continuam abertos
- **Origem:** [UC-02 A1.1](../casos-de-uso/UC-02-autenticar.md#a1-1) (disparador: algo que exige identificação)
- **RF:** [RF-33](../requisitos/rf-contas.md#rf-33)
- **TA:** [TA-17](#ta-17)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-11"></a>TA-11 | [CA-01](#us-02-ca-01) | automatizado | `contas/tests/test_api_autenticacao.py::test_login_valido_devolve_tokens_e_usuario_sem_senha`; `contas/tests/test_api_autenticacao.py::test_login_aceita_email_com_caixa_diferente_e_espacos`; `contas/tests/test_api_autenticacao.py::test_login_preenche_last_login`; `exemplos/tests/test_carregar_dados_exemplo.py::test_login_com_cada_usuario_de_exemplo [x]`; `components/layout/Layout.test.tsx`: `logado, mostra nome e perfil, o botão Sair e todos os itens do menu` |
| <a id="ta-12"></a>TA-12 | [CA-02](#us-02-ca-02) | automatizado | `components/sessao/RotaProtegida.test.tsx`: `sem sessão, leva para /entrar com o caminho atual em ?proximo`; `pages/PaginaEntrar.test.tsx`: `com sucesso, mostra a mensagem da API e volta para o ?proximo`; `pages/PaginaEntrar.test.tsx`: `um ?proximo para fora do site cai em /reservas`; `navegacao.test.ts`: `proximoSeguro troca %s por /reservas` |
| <a id="ta-13"></a>TA-13 | [CA-03](#us-02-ca-03) | automatizado | `pages/PaginaEntrar.test.tsx`: `o link de cadastro preserva o ?proximo`; `pages/PaginaCadastro.test.tsx`: `com sucesso, cadastra, entra com as mesmas credenciais e vai para /reservas/nova`; `contas/tests/test_api_cadastro.py::test_usuario_recem_cadastrado_consegue_fazer_login` |
| <a id="ta-14"></a>TA-14 | [CA-04](#us-02-ca-04) | automatizado | `contas/tests/test_api_autenticacao.py::test_login_sem_campos_responde_400_com_cada_campo`; `pages/PaginaEntrar.test.tsx`: `erros de campo aparecem embaixo do campo, que recebe o foco` |
| <a id="ta-15"></a>TA-15 | [CA-05](#us-02-ca-05) | automatizado | `contas/tests/test_api_autenticacao.py::test_senha_errada_email_inexistente_e_inativo_respondem_igual`; `pages/PaginaEntrar.test.tsx`: `credenciais inválidas aparecem num aviso no topo, que recebe o foco` |
| <a id="ta-16"></a>TA-16 | [CA-06](#us-02-ca-06) | automatizado | `contas/tests/test_limites_de_tentativas.py::test_sexta_tentativa_com_o_mesmo_email_responde_429_com_a_espera`; `contas/tests/test_limites_de_tentativas.py::test_senha_certa_tambem_e_recusada_depois_do_limite`; `contas/tests/test_limites_de_tentativas.py::test_outro_email_continua_entrando_depois_do_limite_de_um_email`; `contas/tests/test_limites_de_tentativas.py::test_limite_por_ip_vale_para_varios_emails`; `contas/tests/test_limites_de_tentativas.py::test_tentativas_simultaneas_nao_passam_do_limite [x]`; `contas/tests/test_limites_de_tentativas.py::test_depois_da_janela_o_login_volta_a_ser_aceito`; `contas/tests/test_limites_de_tentativas.py::test_resposta_429_nao_revela_o_limite_nem_se_o_email_existe`; `pages/PaginaEntrar.test.tsx`: `muitas tentativas mostram a mensagem do servidor no aviso do topo, que recebe o foco` |
| <a id="ta-17"></a>TA-17 | [CA-07](#us-02-ca-07) | automatizado | `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]`; `espacos/tests/test_api_espacos.py::test_consultar_espacos_sem_login_responde_401`; `reservas/tests/test_api_consulta_reservas.py::test_consulta_sem_login_responde_401`; `reservas/tests/test_api_permissoes.py::test_vocabularios_e_health_nao_exigem_login [x]` |
