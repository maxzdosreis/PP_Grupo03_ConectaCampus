# US-03 · Manter e encerrar a sessão

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-03 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-03-manter-e-encerrar-a-sessao.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | CA-06 · Duas janelas renovam ao mesmo tempo (alternativa), CA-09 · Sessão encerrada não volta (exceção) e CA-10 · Credencial de renovação já trocada (exceção), com os TA-19, TA-22 e TA-23; as antigas CA-06 e CA-07 passam a CA-07 e CA-08 (TA-20 e TA-21), e os TA-21 a TA-158 das outras histórias passam a TA-24 a TA-161; CA-01, CA-02 e Conversa com a troca e a revogação da credencial de renovação (AUT-09). Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-03 |
| **Título** | Manter e encerrar a sessão |
| **História** | Como pessoa identificada (Solicitante ou Gestor), quero continuar identificada enquanto uso o sistema e poder sair quando quiser para não digitar a senha a toda hora e não deixar a minha conta aberta. |
| **Valor** | Uso contínuo sem atrito durante o dia; a conta fica protegida ao sair, ao expirar e quando a Equipe de TI a desativa ([NS-11](../visao.md#necessidades)). |
| **Origem** | [UC-02 Autenticar](../casos-de-uso/UC-02-autenticar.md): alternativas [A4.1](../casos-de-uso/UC-02-autenticar.md#a4-1), [A4.2](../casos-de-uso/UC-02-autenticar.md#a4-2) e [A4.3](../casos-de-uso/UC-02-autenticar.md#a4-3) e exceções [E4.1](../casos-de-uso/UC-02-autenticar.md#e4-1) e [E4.2](../casos-de-uso/UC-02-autenticar.md#e4-2). Um caso de uso, duas histórias: a entrada é a [US-02](US-02-entrar-no-sistema.md). |
| **Prioridade** | Esperado — a classe QFD mais alta entre [RF-34](../requisitos/rf-contas.md#rf-34), [RF-34.1](../requisitos/rf-contas.md#rf-34-1), [RF-35](../requisitos/rf-contas.md#rf-35) e [RF-36](../requisitos/rf-contas.md#rf-36). |
| **Estimativa (Custo em Semanas)** | 0,6 (retrospectiva: renovação, restauração e saída da AUT-06, a correção do refresh de usuário inativo da AUT-07 e a revogação e a troca da credencial de renovação da AUT-09). |
| **Conversa** | "Por quanto tempo a pessoa continua identificada?" → 1 dia, com credencial de 30 minutos renovada sem ela perceber ([DEC-04](../decisoes/DEC-04.md)). "Sair invalida a credencial em outro lugar?" → a de renovação sim, em qualquer lugar; a de acesso continua valendo até expirar, em até 30 minutos ([L-04](../requisitos/srs.md#l-04), aceita). "E com duas janelas abertas?" → uma não encerra a outra ([RNF-F13](../requisitos/rnf.md#rnf-f13)). "Se a Equipe de TI mudar o perfil, quando vale?" → na próxima operação ([RNF-F08](../requisitos/rnf.md#rnf-f08)). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Só existe depois de [US-02](US-02-entrar-no-sistema.md): não há sessão a manter sem entrada. |
| **N** · Negociável | ✓ | Os tempos da sessão vêm de configuração e o comportamento sem conexão pode ser combinado. |
| **V** · Valiosa | ✓ | Sem ela, a pessoa entraria a cada 30 minutos e não teria como sair. |
| **E** · Estimável | ✓ | Comportamento conhecido e já medido no custo retrospectivo. |
| **S** · Small | ✗ | Junta duas capacidades (continuar identificado e sair) e cinco modos de terminar ou falhar (expiração, conta desativada, falha passageira, sessão encerrada e credencial de renovação já trocada). O corte natural seria "continuar e expirar" × "sair"; não foi feito porque as duas dependem do mesmo controle da sessão. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado, no frontend e no backend. |

**Diagnóstico:** valiosa e testável, mas depende de US-02 e ainda precisa ser menor.

## Critérios de aceite

#### <a id="us-03-ca-01"></a>US-03 · CA-01 · Continua identificada (sucesso)

- **Dado** uma pessoa que entrou há menos de 1 dia
- **Quando** ela continua usando o sistema, recarrega a página ou o abre de novo em outra janela do mesmo navegador, inclusive depois dos 30 minutos da credencial de acesso
- **Então** o sistema a mantém identificada sem pedir a senha, e a operação que ela pediu acontece normalmente; a cada renovação, a credencial de renovação é trocada por outra, com o mesmo prazo final de 1 dia desde a entrada; se várias operações precisarem renovar a credencial ao mesmo tempo, a renovação acontece uma vez só
- **Origem:** [UC-02 A4.1](../casos-de-uso/UC-02-autenticar.md#a4-1)
- **RF:** [RF-34](../requisitos/rf-contas.md#rf-34)
- **TA:** [TA-14](#ta-14)

#### <a id="us-03-ca-02"></a>US-03 · CA-02 · Sair (sucesso)

- **Dado** uma pessoa identificada, em qualquer ponto do sistema
- **Quando** ela pede para sair
- **Então** o sistema encerra a identificação neste navegador e a sessão no sistema, informa "Você saiu da sua conta." e mostra a página inicial sem nenhuma identificação, mesmo que o sistema não responda no momento
- **Origem:** [UC-02 A4.3](../casos-de-uso/UC-02-autenticar.md#a4-3)
- **RF:** [RF-36](../requisitos/rf-contas.md#rf-36)
- **TA:** [TA-15](#ta-15)

#### <a id="us-03-ca-03"></a>US-03 · CA-03 · Dados atuais da conta ao voltar (alternativa)

- **Dado** uma pessoa que volta ao sistema com a sessão guardada, e cujo perfil a Equipe de TI mudou nesse meio-tempo (de Gestor para Solicitante ou o contrário)
- **Quando** o sistema é aberto
- **Então** o sistema mostra o nome, o e-mail, a matrícula e o perfil atuais da conta, e as permissões passam a ser as do perfil novo já na próxima operação, sem nova entrada
- **Origem:** [UC-02 A4.2](../casos-de-uso/UC-02-autenticar.md#a4-2)
- **RF:** [RF-35](../requisitos/rf-contas.md#rf-35)
- **TA:** [TA-16](#ta-16)

#### <a id="us-03-ca-04"></a>US-03 · CA-04 · Sem conexão ao voltar (alternativa)

- **Dado** uma pessoa que volta ao sistema com a sessão guardada
- **Quando** a conferência dos dados da conta não pode ser feita por falta de conexão
- **Então** a sessão guardada continua valendo, e a pessoa não é levada a entrar de novo
- **Origem:** [UC-02 A4.2](../casos-de-uso/UC-02-autenticar.md#a4-2)
- **RF:** [RF-35](../requisitos/rf-contas.md#rf-35)
- **TA:** [TA-17](#ta-17)

#### <a id="us-03-ca-05"></a>US-03 · CA-05 · Falha passageira na renovação (alternativa)

- **Dado** uma pessoa identificada cuja credencial de acesso precisa ser renovada
- **Quando** a renovação falha por falta de conexão ou por um erro passageiro do sistema
- **Então** a operação em curso informa o erro, mas a sessão não é encerrada, e a próxima operação tenta renovar de novo
- **Origem:** [UC-02 E4.1](../casos-de-uso/UC-02-autenticar.md#e4-1) (a falta de conexão está fora da exceção)
- **RF:** [RF-34](../requisitos/rf-contas.md#rf-34)
- **TA:** [TA-18](#ta-18)

#### <a id="us-03-ca-06"></a>US-03 · CA-06 · Duas janelas renovam ao mesmo tempo (alternativa)

- **Dado** uma pessoa identificada com o sistema aberto em duas janelas do mesmo navegador, que dividem a mesma sessão
- **Quando** as duas precisam renovar a credencial de acesso ao mesmo tempo, e o sistema troca a credencial de renovação para uma delas e recusa a mesma credencial para a outra
- **Então** a janela recusada passa a usar a credencial que a outra recebeu e refaz uma vez a operação que a pessoa pediu; nenhuma das duas é encerrada e ninguém precisa entrar de novo
- **Origem:** [UC-02 A4.1](../casos-de-uso/UC-02-autenticar.md#a4-1)
- **RF:** [RF-34](../requisitos/rf-contas.md#rf-34)
- **TA:** [TA-19](#ta-19)

#### <a id="us-03-ca-07"></a>US-03 · CA-07 · Sessão expirada (exceção)

- **Dado** uma pessoa identificada cuja sessão deixou de valer (passou 1 dia desde a entrada, ou a credencial foi adulterada ou é de outro sistema)
- **Quando** ela pede qualquer operação
- **Então** o sistema informa "Sua sessão expirou. Faça login novamente.", não executa a operação, a leva a entrar de novo e, depois, ao ponto em que estava; nada do que ela já tinha gravado muda
- **Origem:** [UC-02 E4.1](../casos-de-uso/UC-02-autenticar.md#e4-1)
- **RF:** [RF-34.1](../requisitos/rf-contas.md#rf-34-1)
- **TA:** [TA-20](#ta-20)

#### <a id="us-03-ca-08"></a>US-03 · CA-08 · Conta desativada ou excluída durante a sessão (exceção)

- **Dado** uma pessoa identificada cuja conta a Equipe de TI desativou ou excluiu
- **Quando** ela pede a próxima operação, mesmo com a credencial ainda dentro do prazo
- **Então** a operação é recusada e a sessão termina como no CA-07; uma nova tentativa de entrar recebe "E-mail ou senha incorretos." e nada é gravado em nome dela
- **Origem:** [UC-02 E4.2](../casos-de-uso/UC-02-autenticar.md#e4-2)
- **RF:** [RF-34.1](../requisitos/rf-contas.md#rf-34-1)
- **TA:** [TA-21](#ta-21)

#### <a id="us-03-ca-09"></a>US-03 · CA-09 · Sessão encerrada não volta (exceção)

- **Dado** uma pessoa que saiu, e uma cópia da credencial de renovação daquela sessão guardada em outro lugar
- **Quando** alguém usa essa cópia para continuar identificado
- **Então** o sistema recusa a renovação e a sessão não volta: quem usou a cópia precisa entrar de novo com e-mail e senha; pedir para sair de novo com a mesma credencial, ou com uma já vencida, tem a mesma resposta "Você saiu da sua conta.", e a credencial de acesso já emitida continua valendo até expirar, em até 30 minutos
- **Origem:** [UC-02 A4.3](../casos-de-uso/UC-02-autenticar.md#a4-3)
- **RF:** [RF-36](../requisitos/rf-contas.md#rf-36)
- **TA:** [TA-22](#ta-22)

#### <a id="us-03-ca-10"></a>US-03 · CA-10 · Credencial de renovação já trocada (exceção)

- **Dado** uma credencial de renovação que já foi usada numa renovação e trocada por outra
- **Quando** ela é usada de novo para renovar a credencial de acesso
- **Então** o sistema recusa a renovação como numa sessão expirada ("Sua sessão expirou. Faça login novamente." para quem a usou), e a credencial que a substituiu continua valendo
- **Origem:** [UC-02 E4.1](../casos-de-uso/UC-02-autenticar.md#e4-1)
- **RF:** [RF-34.1](../requisitos/rf-contas.md#rf-34-1)
- **TA:** [TA-23](#ta-23)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-14"></a>TA-14 | [CA-01](#us-03-ca-01) | automatizado | `contas/tests/test_api_autenticacao.py::test_refresh_valido_devolve_access_novo_que_funciona_no_me`; `contas/tests/test_api_autenticacao.py::test_access_dura_o_tempo_configurado`; `contas/tests/test_api_autenticacao.py::test_refresh_dura_o_tempo_configurado`; `contas/tests/test_api_autenticacao.py::test_refresh_novo_renova_de_novo_em_cadeia`; `contas/tests/test_api_autenticacao.py::test_refresh_trocado_mantem_o_prazo_final_da_entrada`; `api/cliente.test.ts`: `401 NAO_AUTENTICADO renova o access e repete a requisição com o novo`; `api/cliente.test.ts`: `a renovação guarda o access e o refresh novos na sessão`; `api/cliente.test.ts`: `duas requisições recebendo 401 ao mesmo tempo usam uma única renovação`; `components/sessao/SessaoProvider.test.tsx`: `restaura a sessão salva e confirma com /me, que atualiza o usuário` |
| <a id="ta-15"></a>TA-15 | [CA-02](#us-03-ca-02) | automatizado | `components/sessao/SessaoProvider.test.tsx`: `sair numa rota protegida limpa a sessão, avisa e vai para o início`; `components/sessao/SessaoProvider.test.tsx`: `sair revoga o refresh na API sem esperar a resposta`; `components/sessao/SessaoProvider.test.tsx`: `sair com a API fora do ar sai do mesmo jeito, só com um aviso no console`; `contas/tests/test_api_sair.py::test_sair_revoga_o_refresh_e_ele_deixa_de_renovar`; `api/sessao.test.ts`: `salva, lê e limpa a sessão no localStorage, numa chave única` |
| <a id="ta-16"></a>TA-16 | [CA-03](#us-03-ca-03) | automatizado | `contas/tests/test_api_autenticacao.py::test_me_com_bearer_valido_devolve_usuario_com_perfil`; `config/tests/test_perfil_lido_do_banco.py::test_gestor_rebaixado_perde_as_permissoes_com_o_mesmo_token`; `config/tests/test_perfil_lido_do_banco.py::test_solicitante_promovido_ganha_as_permissoes_com_o_mesmo_token`; `components/sessao/SessaoProvider.test.tsx`: `restaura a sessão salva e confirma com /me, que atualiza o usuário` |
| <a id="ta-17"></a>TA-17 | [CA-04](#us-03-ca-04) | automatizado | `components/sessao/SessaoProvider.test.tsx`: `sem conexão ao confirmar, mantém a sessão` |
| <a id="ta-18"></a>TA-18 | [CA-05](#us-03-ca-05) | automatizado | `api/cliente.test.ts`: `refresh com falha passageira (%s) mantém a sessão, lança o erro e deixa tentar de novo` |
| <a id="ta-19"></a>TA-19 | [CA-06](#us-03-ca-06) | automatizado | `api/cliente.test.ts`: `renovação recusada com outro refresh já salvo por outra aba repete com a sessão nova e não desloga`; `api/cliente.test.ts`: `renovação recusada enquanto outra aba ainda grava a sessão nova espera o aviso dela e não desloga`; `contas/tests/test_api_autenticacao.py::test_duas_trocas_do_mesmo_refresh_so_a_primeira_vale` |
| <a id="ta-20"></a>TA-20 | [CA-07](#us-03-ca-07) | automatizado | `api/cliente.test.ts`: `se a renovação falhar, limpa a sessão, avisa os ouvintes e lança SESSAO_EXPIRADA`; `api/cliente.test.ts`: `a requisição repetida que volta 401 de novo encerra a sessão, sem laço`; `components/sessao/SessaoProvider.test.tsx`: `quando a sessão expira, avisa e leva para o login com o caminho atual`; `contas/tests/test_api_autenticacao.py::test_refresh_invalido_responde_401_no_formato_padrao`; `contas/tests/test_api_autenticacao.py::test_me_com_access_expirado_responde_401`; `contas/tests/test_api_autenticacao.py::test_token_adulterado_responde_401 [x]` |
| <a id="ta-21"></a>TA-21 | [CA-08](#us-03-ca-08) | automatizado | `contas/tests/test_api_autenticacao.py::test_access_de_usuario_desativado_depois_do_login_responde_401`; `contas/tests/test_api_autenticacao.py::test_access_de_usuario_excluido_responde_401`; `contas/tests/test_api_autenticacao.py::test_refresh_de_usuario_inativo_responde_401`; `contas/tests/test_api_autenticacao.py::test_refresh_de_usuario_excluido_responde_401`; `contas/tests/test_api_autenticacao.py::test_senha_errada_email_inexistente_e_inativo_respondem_igual` |
| <a id="ta-22"></a>TA-22 | [CA-09](#us-03-ca-09) | automatizado | `contas/tests/test_api_sair.py::test_sair_revoga_o_refresh_e_ele_deixa_de_renovar`; `contas/tests/test_api_sair.py::test_sair_de_novo_com_o_mesmo_refresh_responde_200`; `contas/tests/test_api_sair.py::test_sair_com_refresh_vencido_responde_200_sem_revogar`; `contas/tests/test_api_sair.py::test_access_emitido_antes_de_sair_continua_valendo_ate_expirar`; `contas/tests/test_api_sair.py::test_refresh_de_outra_pessoa_e_revogado_sem_dados_dela`; `contas/tests/test_api_sair.py::test_refresh_emitido_antes_da_lista_negra_tambem_e_revogado` |
| <a id="ta-23"></a>TA-23 | [CA-10](#us-03-ca-10) | automatizado | `contas/tests/test_api_autenticacao.py::test_renovacao_troca_o_refresh_e_o_antigo_passa_a_ser_recusado`; `contas/tests/test_api_autenticacao.py::test_refresh_trocado_de_usuario_desativado_continua_recusado`; `contas/tests/test_api_autenticacao.py::test_refresh_emitido_antes_da_lista_negra_e_trocado_sem_erro`; `api/cliente.test.ts`: `se a renovação falhar, limpa a sessão, avisa os ouvintes e lança SESSAO_EXPIRADA` |
