# US-03 · Manter e encerrar a sessão

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-03 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-03-manter-e-encerrar-a-sessao.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-03 |
| **Título** | Manter e encerrar a sessão |
| **História** | Como pessoa identificada (Solicitante ou Gestor), quero continuar identificada enquanto uso o sistema e poder sair quando quiser para não digitar a senha a toda hora e não deixar a minha conta aberta. |
| **Valor** | Uso contínuo sem atrito durante o dia; a conta fica protegida ao sair, ao expirar e quando a Equipe de TI a desativa ([NS-11](../visao.md#necessidades)). |
| **Origem** | [UC-02 Autenticar](../casos-de-uso/UC-02-autenticar.md): alternativas [A4.1](../casos-de-uso/UC-02-autenticar.md#a4-1), [A4.2](../casos-de-uso/UC-02-autenticar.md#a4-2) e [A4.3](../casos-de-uso/UC-02-autenticar.md#a4-3) e exceções [E4.1](../casos-de-uso/UC-02-autenticar.md#e4-1) e [E4.2](../casos-de-uso/UC-02-autenticar.md#e4-2). Um caso de uso, duas histórias: a entrada é a [US-02](US-02-entrar-no-sistema.md). |
| **Prioridade** | Esperado — a classe QFD mais alta entre [RF-34](../requisitos/rf-contas.md#rf-34), [RF-34.1](../requisitos/rf-contas.md#rf-34-1), [RF-35](../requisitos/rf-contas.md#rf-35) e [RF-36](../requisitos/rf-contas.md#rf-36). |
| **Estimativa (Custo em Semanas)** | 0,4 (retrospectiva: renovação, restauração e saída da AUT-06 e a correção do refresh de usuário inativo da AUT-07). |
| **Conversa** | "Por quanto tempo a pessoa continua identificada?" → 1 dia, com credencial de 30 minutos renovada sem ela perceber ([DEC-04](../decisoes/DEC-04.md)). "Sair invalida a credencial em outro lugar?" → não ([L-04](../requisitos/srs.md#l-04), aceita). "Se a Equipe de TI mudar o perfil, quando vale?" → na próxima operação ([RNF-F08](../requisitos/rnf.md#rnf-f08)). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Só existe depois de [US-02](US-02-entrar-no-sistema.md): não há sessão a manter sem entrada. |
| **N** · Negociável | ✓ | Os tempos da sessão vêm de configuração e o comportamento sem conexão pode ser combinado. |
| **V** · Valiosa | ✓ | Sem ela, a pessoa entraria a cada 30 minutos e não teria como sair. |
| **E** · Estimável | ✓ | Comportamento conhecido e já medido no custo retrospectivo. |
| **S** · Small | ✗ | Junta duas capacidades (continuar identificado e sair) e três modos de terminar (expiração, conta desativada, falha passageira). O corte natural seria "continuar e expirar" × "sair"; não foi feito porque as duas dependem do mesmo controle da sessão. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado, no frontend e no backend. |

**Diagnóstico:** valiosa e testável, mas depende de US-02 e ainda precisa ser menor.

## Critérios de aceite

#### <a id="us-03-ca-01"></a>US-03 · CA-01 · Continua identificada (sucesso)

- **Dado** uma pessoa que entrou há menos de 1 dia
- **Quando** ela continua usando o sistema, recarrega a página ou o abre de novo em outra janela do mesmo navegador, inclusive depois dos 30 minutos da credencial de acesso
- **Então** o sistema a mantém identificada sem pedir a senha, e a operação que ela pediu acontece normalmente; se várias operações precisarem renovar a credencial ao mesmo tempo, a renovação acontece uma vez só
- **Origem:** [UC-02 A4.1](../casos-de-uso/UC-02-autenticar.md#a4-1)
- **RF:** [RF-34](../requisitos/rf-contas.md#rf-34)
- **TA:** [TA-13](#ta-13)

#### <a id="us-03-ca-02"></a>US-03 · CA-02 · Sair (sucesso)

- **Dado** uma pessoa identificada, em qualquer ponto do sistema
- **Quando** ela pede para sair
- **Então** o sistema encerra a identificação neste navegador, informa "Você saiu da sua conta." e mostra a página inicial sem nenhuma identificação
- **Origem:** [UC-02 A4.3](../casos-de-uso/UC-02-autenticar.md#a4-3)
- **RF:** [RF-36](../requisitos/rf-contas.md#rf-36)
- **TA:** [TA-14](#ta-14)

#### <a id="us-03-ca-03"></a>US-03 · CA-03 · Dados atuais da conta ao voltar (alternativa)

- **Dado** uma pessoa que volta ao sistema com a sessão guardada, e cujo perfil a Equipe de TI mudou nesse meio-tempo (de Gestor para Solicitante ou o contrário)
- **Quando** o sistema é aberto
- **Então** o sistema mostra o nome, o e-mail, a matrícula e o perfil atuais da conta, e as permissões passam a ser as do perfil novo já na próxima operação, sem nova entrada
- **Origem:** [UC-02 A4.2](../casos-de-uso/UC-02-autenticar.md#a4-2)
- **RF:** [RF-35](../requisitos/rf-contas.md#rf-35)
- **TA:** [TA-15](#ta-15)

#### <a id="us-03-ca-04"></a>US-03 · CA-04 · Sem conexão ao voltar (alternativa)

- **Dado** uma pessoa que volta ao sistema com a sessão guardada
- **Quando** a conferência dos dados da conta não pode ser feita por falta de conexão
- **Então** a sessão guardada continua valendo, e a pessoa não é levada a entrar de novo
- **Origem:** [UC-02 A4.2](../casos-de-uso/UC-02-autenticar.md#a4-2)
- **RF:** [RF-35](../requisitos/rf-contas.md#rf-35)
- **TA:** [TA-16](#ta-16)

#### <a id="us-03-ca-05"></a>US-03 · CA-05 · Falha passageira na renovação (alternativa)

- **Dado** uma pessoa identificada cuja credencial de acesso precisa ser renovada
- **Quando** a renovação falha por falta de conexão ou por um erro passageiro do sistema
- **Então** a operação em curso informa o erro, mas a sessão não é encerrada, e a próxima operação tenta renovar de novo
- **Origem:** [UC-02 E4.1](../casos-de-uso/UC-02-autenticar.md#e4-1) (a falta de conexão está fora da exceção)
- **RF:** [RF-34](../requisitos/rf-contas.md#rf-34)
- **TA:** [TA-17](#ta-17)

#### <a id="us-03-ca-06"></a>US-03 · CA-06 · Sessão expirada (exceção)

- **Dado** uma pessoa identificada cuja sessão deixou de valer (passou 1 dia desde a entrada, ou a credencial foi adulterada ou é de outro sistema)
- **Quando** ela pede qualquer operação
- **Então** o sistema informa "Sua sessão expirou. Faça login novamente.", não executa a operação, a leva a entrar de novo e, depois, ao ponto em que estava; nada do que ela já tinha gravado muda
- **Origem:** [UC-02 E4.1](../casos-de-uso/UC-02-autenticar.md#e4-1)
- **RF:** [RF-34.1](../requisitos/rf-contas.md#rf-34-1)
- **TA:** [TA-18](#ta-18)

#### <a id="us-03-ca-07"></a>US-03 · CA-07 · Conta desativada ou excluída durante a sessão (exceção)

- **Dado** uma pessoa identificada cuja conta a Equipe de TI desativou ou excluiu
- **Quando** ela pede a próxima operação, mesmo com a credencial ainda dentro do prazo
- **Então** a operação é recusada e a sessão termina como no CA-06; uma nova tentativa de entrar recebe "E-mail ou senha incorretos." e nada é gravado em nome dela
- **Origem:** [UC-02 E4.2](../casos-de-uso/UC-02-autenticar.md#e4-2)
- **RF:** [RF-34.1](../requisitos/rf-contas.md#rf-34-1)
- **TA:** [TA-19](#ta-19)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-13"></a>TA-13 | [CA-01](#us-03-ca-01) | automatizado | `contas/tests/test_api_autenticacao.py::test_refresh_valido_devolve_access_novo_que_funciona_no_me`; `contas/tests/test_api_autenticacao.py::test_access_dura_o_tempo_configurado`; `contas/tests/test_api_autenticacao.py::test_refresh_dura_o_tempo_configurado`; `api/cliente.test.ts`: `401 NAO_AUTENTICADO renova o access e repete a requisição com o novo`; `api/cliente.test.ts`: `duas requisições recebendo 401 ao mesmo tempo usam uma única renovação`; `components/sessao/SessaoProvider.test.tsx`: `restaura a sessão salva e confirma com /me, que atualiza o usuário` |
| <a id="ta-14"></a>TA-14 | [CA-02](#us-03-ca-02) | automatizado | `components/sessao/SessaoProvider.test.tsx`: `sair numa rota protegida limpa a sessão, avisa e vai para o início`; `api/sessao.test.ts`: `salva, lê e limpa a sessão no localStorage, numa chave única` |
| <a id="ta-15"></a>TA-15 | [CA-03](#us-03-ca-03) | automatizado | `contas/tests/test_api_autenticacao.py::test_me_com_bearer_valido_devolve_usuario_com_perfil`; `config/tests/test_perfil_lido_do_banco.py::test_gestor_rebaixado_perde_as_permissoes_com_o_mesmo_token`; `config/tests/test_perfil_lido_do_banco.py::test_solicitante_promovido_ganha_as_permissoes_com_o_mesmo_token`; `components/sessao/SessaoProvider.test.tsx`: `restaura a sessão salva e confirma com /me, que atualiza o usuário` |
| <a id="ta-16"></a>TA-16 | [CA-04](#us-03-ca-04) | automatizado | `components/sessao/SessaoProvider.test.tsx`: `sem conexão ao confirmar, mantém a sessão` |
| <a id="ta-17"></a>TA-17 | [CA-05](#us-03-ca-05) | automatizado | `api/cliente.test.ts`: `refresh com falha passageira (%s) mantém a sessão, lança o erro e deixa tentar de novo` |
| <a id="ta-18"></a>TA-18 | [CA-06](#us-03-ca-06) | automatizado | `api/cliente.test.ts`: `se a renovação falhar, limpa a sessão, avisa os ouvintes e lança SESSAO_EXPIRADA`; `api/cliente.test.ts`: `a requisição repetida que volta 401 de novo encerra a sessão, sem laço`; `components/sessao/SessaoProvider.test.tsx`: `quando a sessão expira, avisa e leva para o login com o caminho atual`; `contas/tests/test_api_autenticacao.py::test_refresh_invalido_responde_401_no_formato_padrao`; `contas/tests/test_api_autenticacao.py::test_me_com_access_expirado_responde_401`; `contas/tests/test_api_autenticacao.py::test_token_adulterado_responde_401 [x]` |
| <a id="ta-19"></a>TA-19 | [CA-07](#us-03-ca-07) | automatizado | `contas/tests/test_api_autenticacao.py::test_access_de_usuario_desativado_depois_do_login_responde_401`; `contas/tests/test_api_autenticacao.py::test_access_de_usuario_excluido_responde_401`; `contas/tests/test_api_autenticacao.py::test_refresh_de_usuario_inativo_responde_401`; `contas/tests/test_api_autenticacao.py::test_refresh_de_usuario_excluido_responde_401`; `contas/tests/test_api_autenticacao.py::test_senha_errada_email_inexistente_e_inativo_respondem_igual` |
