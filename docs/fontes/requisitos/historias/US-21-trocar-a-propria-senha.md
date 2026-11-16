# US-21 · Trocar a própria senha

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-21 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-21-trocar-a-propria-senha.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 16/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, sete critérios e testes de aceite (TA-194 a TA-200), a partir da [DEC-26](../decisoes/DEC-26.md) e do [CR-06](../mudancas/CR-06-trocar-a-propria-senha.md) (AUT-10). Mudança posterior à entrega de 13/11/2026. Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-21 |
| **Título** | Trocar a própria senha |
| **História** | Como pessoa identificada (Solicitante, Atendente responsável ou Gestor do serviço), quero trocar a minha senha, informando a atual, para proteger a minha conta sem depender da administração. |
| **Valor** | A pessoa que suspeita de que a senha vazou, ou quer uma melhor, resolve sozinha e na hora, e uma sessão aberta num computador alheio não basta para trocá-la ([NS-15](../visao.md#ns-15), [NS-11](../visao.md#ns-11)). |
| **Origem** | [UC-02 Autenticar](../casos-de-uso/UC-02-autenticar.md): alternativa [A4.4](../casos-de-uso/UC-02-autenticar.md#a4-4) e exceções [E4.3](../casos-de-uso/UC-02-autenticar.md#e4-3), [E4.4](../casos-de-uso/UC-02-autenticar.md#e4-4), [E4.5](../casos-de-uso/UC-02-autenticar.md#e4-5) e [E4.6](../casos-de-uso/UC-02-autenticar.md#e4-6). Um caso de uso, três histórias: a entrada é a [US-02](US-02-entrar-no-sistema.md) e a sessão, a [US-03](US-03-manter-e-encerrar-a-sessao.md). |
| **Prioridade** | Esperado — a classe QFD de [RF-41](../requisitos/rf-contas.md#rf-41), [RF-41.1](../requisitos/rf-contas.md#rf-41-1) e [RF-41.2](../requisitos/rf-contas.md#rf-41-2). |
| **Estimativa (Custo em Semanas)** | 0,4 (retrospectiva: caso de uso, rota, limite de tentativas por conta, revogação das outras sessões e a página Minha conta da AUT-10). |
| **Conversa** | "E se a pessoa errar a senha atual?" → vê o erro junto ao campo e continua identificada; errar a senha não encerra a sessão ([DEC-26](../decisoes/DEC-26.md)). "Quem esqueceu a senha?" → a recuperação por e-mail continua fora do escopo; segue pela administração. "Os outros aparelhos?" → a sessão deles deixa de ser renovada, e a credencial de acesso já emitida vale até expirar, em até 30 minutos ([L-04](../requisitos/srs.md#l-04)). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Só existe depois de [US-02](US-02-entrar-no-sistema.md): não há senha a trocar sem entrada. |
| **N** · Negociável | ✓ | O limite de tentativas vem de configuração, e quais sessões continuam depois da troca pode ser combinado. |
| **V** · Valiosa | ✓ | Sem ela, trocar uma senha comprometida dependeria da Equipe de TI. |
| **E** · Estimável | ✓ | Comportamento conhecido e já medido no custo retrospectivo. |
| **S** · Small | ✓ | Uma capacidade só (trocar a senha), com as recusas dela. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado, no frontend e no backend. |

**Diagnóstico:** pequena, valiosa e testável; só depende de US-02.

## Critérios de aceite

#### <a id="us-21-ca-01"></a>US-21 · CA-01 · Trocar a senha (sucesso)

- **Dado** uma pessoa identificada que sabe a senha atual
- **Quando** ela informa a senha atual e uma senha nova que cumpre a política de senha, e repete a nova para confirmar
- **Então** o sistema informa "Senha alterada com sucesso.", limpa os campos, mantém a pessoa identificada, passa a aceitar só a senha nova na próxima entrada e não guarda a senha, só a sua forma protegida
- **Origem:** [UC-02 A4.4](../casos-de-uso/UC-02-autenticar.md#a4-4)
- **RF:** [RF-41](../requisitos/rf-contas.md#rf-41)
- **TA:** [TA-194](#ta-194)

#### <a id="us-21-ca-02"></a>US-21 · CA-02 · Outros aparelhos deixam de renovar (alternativa)

- **Dado** uma pessoa que trocou a senha e tinha a conta aberta em outro aparelho
- **Quando** o outro aparelho precisa renovar a credencial de acesso
- **Então** a renovação é recusada e a pessoa precisa entrar de novo com a senha nova; no aparelho em que a troca foi feita, a sessão continua renovando; a credencial de acesso já emitida no outro aparelho vale até expirar, em até 30 minutos; as sessões de outras pessoas não mudam
- **Origem:** [UC-02 A4.4](../casos-de-uso/UC-02-autenticar.md#a4-4)
- **RF:** [RF-41](../requisitos/rf-contas.md#rf-41)
- **TA:** [TA-195](#ta-195)

#### <a id="us-21-ca-03"></a>US-21 · CA-03 · Senha atual incorreta (exceção)

- **Dado** uma pessoa identificada que informa uma senha atual que não é a da conta
- **Quando** ela pede a troca
- **Então** o sistema informa "A senha atual está incorreta." junto ao campo, sem dizer nada sobre a política de senha, não troca a senha e **não** encerra a sessão: a pessoa continua identificada e pode tentar de novo
- **Origem:** [UC-02 E4.4](../casos-de-uso/UC-02-autenticar.md#e4-4)
- **RF:** [RF-41.1](../requisitos/rf-contas.md#rf-41-1)
- **TA:** [TA-196](#ta-196)

#### <a id="us-21-ca-04"></a>US-21 · CA-04 · Senha nova fora da política (exceção)

- **Dado** uma pessoa identificada que informa a senha atual correta e uma senha nova curta, só de números, comum ou parecida com o e-mail, o nome ou a matrícula
- **Quando** ela pede a troca
- **Então** o sistema informa os motivos da recusa, nas mesmas palavras do cadastro, junto ao campo da senha nova, e não troca a senha
- **Origem:** [UC-02 E4.6](../casos-de-uso/UC-02-autenticar.md#e4-6)
- **RF:** [RF-41.1](../requisitos/rf-contas.md#rf-41-1)
- **TA:** [TA-197](#ta-197)

#### <a id="us-21-ca-05"></a>US-21 · CA-05 · Senha nova igual à atual (exceção)

- **Dado** uma pessoa identificada que informa a senha atual correta e repete a mesma como senha nova
- **Quando** ela pede a troca
- **Então** o sistema informa "A nova senha deve ser diferente da senha atual." junto ao campo da senha nova e não troca a senha
- **Origem:** [UC-02 E4.5](../casos-de-uso/UC-02-autenticar.md#e4-5)
- **RF:** [RF-41.1](../requisitos/rf-contas.md#rf-41-1)
- **TA:** [TA-198](#ta-198)

#### <a id="us-21-ca-06"></a>US-21 · CA-06 · Tentativas de troca em excesso (exceção)

- **Dado** uma pessoa identificada que já tentou trocar a senha 5 vezes no último minuto
- **Quando** ela tenta de novo, mesmo com a senha atual certa
- **Então** o sistema informa "Muitas tentativas. Tente de novo em N segundos.", com o tempo que falta, sem conferir a senha e sem trocá-la; a contagem é da conta, e a de outra pessoa na mesma origem não é afetada
- **Origem:** [UC-02 E4.3](../casos-de-uso/UC-02-autenticar.md#e4-3)
- **RF:** [RF-41.2](../requisitos/rf-contas.md#rf-41-2)
- **TA:** [TA-199](#ta-199)

#### <a id="us-21-ca-07"></a>US-21 · CA-07 · Só a própria senha, só identificado (acesso)

- **Dado** uma pessoa sem identificação, ou uma pessoa identificada que tenta indicar outra conta no pedido
- **Quando** ela pede a troca de senha
- **Então** quem não está identificado é levado a entrar e nada é trocado; quem está identificado só troca a senha da própria conta, mesmo que o pedido traga o código ou o e-mail de outra pessoa, e a senha digitada não aparece na resposta nem nos registros do sistema
- **Origem:** [UC-02 A4.4](../casos-de-uso/UC-02-autenticar.md#a4-4)
- **RF:** [RF-41](../requisitos/rf-contas.md#rf-41)
- **TA:** [TA-200](#ta-200)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-194"></a>TA-194 | [CA-01](#us-21-ca-01) | automatizado | `contas/tests/test_api_alterar_senha.py::test_troca_com_sucesso_responde_200_e_a_nova_senha_passa_a_valer`; `contas/tests/test_api_alterar_senha.py::test_troca_guarda_so_o_hash_da_senha`; `contas/tests/test_api_alterar_senha.py::test_nova_senha_com_espacos_nas_pontas_vale_do_jeito_que_foi_digitada`; `contas/tests/test_alterar_senha.py::test_troca_valida_passa_a_valer_a_nova_senha_e_nao_a_antiga`; `pages/PaginaMinhaConta.test.tsx`: `sucesso envia a senha e o refresh da sessão, limpa os campos e mantém a pessoa logada`; `pages/PaginaMinhaConta.test.tsx`: `confirmação diferente da nova senha mostra o erro e não chama a API` |
| <a id="ta-195"></a>TA-195 | [CA-02](#us-21-ca-02) | automatizado | `contas/tests/test_api_alterar_senha.py::test_troca_revoga_os_refresh_das_outras_sessoes_e_mantem_a_atual`; `contas/tests/test_api_alterar_senha.py::test_troca_sem_informar_a_sessao_atual_revoga_todos_os_refresh`; `contas/tests/test_api_alterar_senha.py::test_troca_nao_revoga_os_refresh_de_outra_pessoa`; `contas/tests/test_api_alterar_senha.py::test_access_ja_emitido_continua_valendo_depois_da_troca`; `contas/tests/test_api_alterar_senha.py::test_refresh_atual_de_outra_pessoa_responde_400_sem_trocar_a_senha` |
| <a id="ta-196"></a>TA-196 | [CA-03](#us-21-ca-03) | automatizado | `contas/tests/test_api_alterar_senha.py::test_senha_atual_errada_responde_400_com_codigo_proprio_e_nunca_401`; `contas/tests/test_api_alterar_senha.py::test_politica_so_e_revelada_depois_de_provar_a_senha_atual`; `contas/tests/test_alterar_senha.py::test_senha_atual_errada_lanca_senha_atual_incorreta_sem_trocar`; `api/cliente.test.ts`: `400 SENHA_ATUAL_INCORRETA na troca de senha não renova nem encerra a sessão`; `pages/PaginaMinhaConta.test.tsx`: `senha atual errada mostra a mensagem no campo e NÃO desloga` |
| <a id="ta-197"></a>TA-197 | [CA-04](#us-21-ca-04) | automatizado | `contas/tests/test_api_alterar_senha.py::test_nova_senha_que_viola_a_politica_responde_400_senha_fraca [x]`; `contas/tests/test_alterar_senha.py::test_nova_senha_fraca_lanca_senha_fraca_no_campo_da_nova_senha`; `pages/PaginaMinhaConta.test.tsx`: `erro de política mostra a mensagem embaixo da nova senha` |
| <a id="ta-198"></a>TA-198 | [CA-05](#us-21-ca-05) | automatizado | `contas/tests/test_api_alterar_senha.py::test_nova_senha_igual_a_atual_responde_400`; `contas/tests/test_alterar_senha.py::test_nova_senha_igual_a_atual_lanca_nova_senha_igual_a_atual` |
| <a id="ta-199"></a>TA-199 | [CA-06](#us-21-ca-06) | automatizado | `contas/tests/test_api_alterar_senha.py::test_sexta_troca_seguida_responde_429_traduzido_pelo_tratador`; `contas/tests/test_api_alterar_senha.py::test_limite_de_troca_e_por_usuario_e_nao_por_ip`; `contas/tests/test_api_alterar_senha.py::test_limite_de_troca_vem_das_settings_a_cada_requisicao`; `pages/PaginaMinhaConta.test.tsx`: `limite de tentativas aparece no aviso do topo` |
| <a id="ta-200"></a>TA-200 | [CA-07](#us-21-ca-07) | automatizado | `contas/tests/test_api_alterar_senha.py::test_anonimo_recebe_401_nao_autenticado`; `contas/tests/test_api_alterar_senha.py::test_pessoa_so_troca_a_propria_senha_mesmo_enviando_outro_id`; `contas/tests/test_api_alterar_senha.py::test_senha_atual_de_outra_pessoa_nao_serve_para_trocar_a_propria`; `contas/tests/test_api_alterar_senha.py::test_gestor_tambem_troca_a_propria_senha`; `contas/tests/test_api_alterar_senha.py::test_senhas_nao_aparecem_na_resposta_nem_nos_logs`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]`; `components/sessao/RotaProtegida.test.tsx`: `sem sessão, a tela Minha conta leva para /entrar com ?proximo=/conta` |
