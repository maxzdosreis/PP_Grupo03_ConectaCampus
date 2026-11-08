# Requisitos funcionais — Contas e acesso

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **Parte da [SRS-01](srs.md) • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/requisitos/rf-contas.md` |

Fichas dos RF de cadastro, identificação e [sessão](../glossario.md#sessao), derivados da NS-11 e da NS-15 da [Visão](../visao.md#necessidades). São o extra da [DEC-04](../decisoes/DEC-04.md): não substituem nenhuma das seis funcionalidades mínimas. As garantias de segurança (hash, validade da sessão, acesso por perfil) são RNF de funcionalidade em [`rnf.md`](rnf.md#1-funcionalidade-f). Como ler as fichas: [SRS, seção 3](srs.md#3-requisitos-funcionais).

Caminhos de teste a partir de `src/backend/`, salvo os do frontend (`src/frontend/src/`); `[x]` = teste parametrizado.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Criação: RF-32 a RF-37 (REQ-02). Sem aprovação. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Vínculos: o UC de cada ficha preenchido, com link para o [índice de casos de uso](../casos-de-uso/README.md#índice-dos-casos-de-uso) (REQ-03). Sem aprovação. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Vínculos: o passo, a alternativa ou a exceção exata de cada RF nas [fichas de caso de uso](../casos-de-uso/README.md#fichas-dos-casos-de-uso); US e CA ficam para a REQ-05 (REQ-04). Sem aprovação. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Vínculos: as US e os CAs de cada RF, com o TA, no lugar de "a definir" ([histórias](../historias/README.md)) (REQ-05). Sem aprovação. |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Campo **Código (complementar)** em cada ficha (caso de uso da aplicação e regra do domínio, como `arquivo::Símbolo`), lido pela [matriz de rastreabilidade](../rastreabilidade/matriz.md) (REQ-06). Evidência do RF-36 passa a citar a tela de início, para onde "Sair" leva (correção editorial achada pela matriz). Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | RF-33.2 · Recusar tentativas de entrada em excesso, que fecha a lacuna L-03; vínculo do RF-33.1 passa a UC-02 E3.3, com a exceção nova antes dele; o CA de acesso da US-02 passa a CA-07 (TA-13) e os TAs seguintes andam uma posição (AUT-08). Sem aprovação. |

## Cadastro

### <a id="rf-32"></a>RF-32 · Cadastrar-se como Solicitante

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao visitante cadastrar-se com nome, matrícula, e-mail e senha e entrar no sistema identificado com o perfil Solicitante. |
| **Origem** | NS-15 |
| **Funcionalidade** | Extra (AUT-04) |
| **Prioridade (QFD)** | Esperado — sem cadastro próprio, cada aluno dependeria da Equipe de TI para começar a pedir. |
| **Vínculos** | UC: [UC-01 Cadastrar-se](../casos-de-uso/README.md#uc-01) (fluxo principal) — na ficha: [UC-01 passos 1 a 4](../casos-de-uso/fichas-resumidas.md#uc01-p1) · US/CA: [US-01 · CA-01](../historias/US-01-criar-minha-conta.md#us-01-ca-01) (TA-01), [US-01 · CA-02](../historias/US-01-criar-minha-conta.md#us-01-ca-02) (TA-02), [US-01 · CA-06](../historias/US-01-criar-minha-conta.md#us-01-ca-06) (TA-06), [US-02 · CA-03](../historias/US-02-entrar-no-sistema.md#us-02-ca-03) (TA-09) |
| **Evidência (complementar)** | `POST /api/auth/cadastro/` → 201, seguido do login; tela `/cadastro`. `contas/tests/test_api_cadastro.py::test_cadastro_valido_responde_201_com_solicitante_sem_senha`, `::test_usuario_recem_cadastrado_consegue_fazer_login`, `::test_campos_de_privilegio_no_corpo_sao_ignorados`; `pages/PaginaCadastro.test.tsx` ("com sucesso, cadastra, entra com as mesmas credenciais e vai para /reservas/nova") |
| **Código (complementar)** | `contas/application/casos_de_uso.py::CadastrarSolicitante.executar`, `contas/domain/cadastro.py::DadosDeCadastro` |
| **Regras de negócio** | [Usuário](../glossario.md#usuario), [matrícula](../glossario.md#matricula), [perfil](../glossario.md#perfil), [Solicitante](../glossario.md#solicitante) |
| **Decisões** | [DEC-04](../decisoes/DEC-04.md) (o cadastro público nunca cria Gestor), [DEC-09](../decisoes/DEC-09.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-32-1"></a>RF-32.1 · Recusar cadastro com dados inválidos

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o visitante se cadastre sem nome, matrícula, e-mail ou senha, com nome de mais de 150 caracteres, com matrícula de mais de 20 caracteres ou com espaço no meio, ou com e-mail em formato inválido, sem criar a conta, e informar a regra violada no campo correspondente. |
| **Pai** | [RF-32](#rf-32) |
| **Origem** | NS-15 (principal); NS-13 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — a matrícula identifica quem pediu cada reserva (NS-11). |
| **Vínculos** | UC: [UC-01 Cadastrar-se](../casos-de-uso/README.md#uc-01) (exceção) — na ficha: [UC-01 E3.1](../casos-de-uso/fichas-resumidas.md#uc01-e3-1) · US/CA: [US-01 · CA-03](../historias/US-01-criar-minha-conta.md#us-01-ca-03) (TA-03) |
| **Evidência (complementar)** | 400 com `campos`. `contas/tests/test_api_cadastro.py::test_campos_ausentes_respondem_400_com_cada_campo`, `::test_nome_so_com_espacos_responde_400_campo_obrigatorio`, `::test_matricula_com_espaco_responde_400`, `::test_email_malformado_responde_400`; `contas/tests/test_cadastro_dominio.py::test_nome_acima_do_limite_lanca_texto_muito_longo`, `::test_matricula_longa_ou_com_espaco_no_meio_lanca_matricula_invalida [x]` |
| **Código (complementar)** | `contas/domain/cadastro.py::DadosDeCadastro`, `contas/domain/excecoes.py::MatriculaInvalida` |
| **Regras de negócio** | [Matrícula](../glossario.md#matricula), [usuário](../glossario.md#usuario) |
| **Decisões** | [DEC-09](../decisoes/DEC-09.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-32-2"></a>RF-32.2 · Recusar senha fraca

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o visitante se cadastre com uma senha que a política de senha recusa ([RNF-F02](rnf.md#rnf-f02)), sem criar a conta, e informar no campo senha cada motivo da recusa. |
| **Pai** | [RF-32](#rf-32) |
| **Origem** | NS-15 (principal); NS-11 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — uma conta com senha curta ou comum exporia as reservas da pessoa. |
| **Vínculos** | UC: [UC-01 Cadastrar-se](../casos-de-uso/README.md#uc-01) (exceção) — na ficha: [UC-01 E3.2](../casos-de-uso/fichas-resumidas.md#uc01-e3-2) · US/CA: [US-01 · CA-04](../historias/US-01-criar-minha-conta.md#us-01-ca-04) (TA-04) |
| **Evidência (complementar)** | 400 `SENHA_FRACA` em `campos.senha`. `contas/tests/test_api_cadastro.py::test_senha_fraca_responde_400_com_motivos_em_senha`; `contas/tests/test_cadastrar_solicitante.py::test_senha_fraca_lanca_senha_fraca_sem_criar_usuario`; `pages/PaginaCadastro.test.tsx` ("senha fraca aparece embaixo da senha") |
| **Código (complementar)** | `contas/application/portas.py::PoliticaDeSenha.validar`, `contas/infrastructure/politica_de_senha.py::PoliticaDeSenhaDjango` |
| **Regras de negócio** | [Política de senha](../glossario.md#politica-de-senha) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-32-3"></a>RF-32.3 · Recusar e-mail ou matrícula já cadastrados

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o visitante se cadastre com um e-mail (sem diferenciar maiúsculas de minúsculas) ou uma matrícula que já pertencem a outro usuário, sem criar a conta, e informar no campo correspondente que o valor já está cadastrado. |
| **Pai** | [RF-32](#rf-32) |
| **Origem** | NS-15 (principal); NS-11 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — duas contas com a mesma matrícula tornariam ambíguo quem pediu uma reserva. |
| **Vínculos** | UC: [UC-01 Cadastrar-se](../casos-de-uso/README.md#uc-01) (exceção) — na ficha: [UC-01 E3.3](../casos-de-uso/fichas-resumidas.md#uc01-e3-3) · US/CA: [US-01 · CA-05](../historias/US-01-criar-minha-conta.md#us-01-ca-05) (TA-05) |
| **Evidência (complementar)** | 409 `EMAIL_JA_CADASTRADO` ou `MATRICULA_JA_CADASTRADA`. `contas/tests/test_api_cadastro.py::test_email_repetido_com_caixa_diferente_responde_409`, `::test_matricula_repetida_responde_409`; `contas/tests/test_repositorio_usuarios.py::test_email_repetido_lanca_email_ja_cadastrado [x]` |
| **Código (complementar)** | `contas/application/casos_de_uso.py::CadastrarSolicitante.executar`, `contas/infrastructure/repositorio_django.py::RepositorioUsuariosDjango.criar_solicitante` |
| **Regras de negócio** | [Usuário](../glossario.md#usuario), [matrícula](../glossario.md#matricula) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

## Identificação e sessão

### <a id="rf-33"></a>RF-33 · Entrar com e-mail e senha

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao visitante cadastrado entrar com e-mail e senha e ver-se identificado pelo nome e pelo perfil. |
| **Origem** | NS-11 |
| **Funcionalidade** | Extra (AUT-03) |
| **Prioridade (QFD)** | Esperado — sem identificação o sistema não sabe quem pediu cada reserva nem quem decidiu. |
| **Vínculos** | UC: [UC-02 Autenticar](../casos-de-uso/README.md#uc-02) (fluxo principal) — na ficha: [UC-02 passos 1 a 4](../casos-de-uso/UC-02-autenticar.md#p1) · US/CA: [US-02 · CA-01](../historias/US-02-entrar-no-sistema.md#us-02-ca-01) (TA-07), [US-02 · CA-02](../historias/US-02-entrar-no-sistema.md#us-02-ca-02) (TA-08), [US-02 · CA-03](../historias/US-02-entrar-no-sistema.md#us-02-ca-03) (TA-09), [US-02 · CA-04](../historias/US-02-entrar-no-sistema.md#us-02-ca-04) (TA-10), [US-02 · CA-07](../historias/US-02-entrar-no-sistema.md#us-02-ca-07) (TA-13) |
| **Evidência (complementar)** | `POST /api/auth/login/`; tela `/entrar` e "Nome · Perfil" no cabeçalho. `contas/tests/test_api_autenticacao.py::test_login_valido_devolve_tokens_e_usuario_sem_senha`, `::test_login_aceita_email_com_caixa_diferente_e_espacos`; `exemplos/tests/test_carregar_dados_exemplo.py::test_login_com_cada_usuario_de_exemplo [x]`; `pages/PaginaEntrar.test.tsx`; `components/layout/Layout.test.tsx` ("logado, mostra nome e perfil, o botão Sair e todos os itens do menu") |
| **Código (complementar)** | `contas/api/views.py::LoginView.post` |
| **Regras de negócio** | [Usuário](../glossario.md#usuario), [perfil](../glossario.md#perfil), [sessão](../glossario.md#sessao) |
| **Decisões** | [DEC-04](../decisoes/DEC-04.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-33-1"></a>RF-33.1 · Recusar credenciais inválidas

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o visitante entre com e-mail inexistente, senha errada ou conta desativada e informar "E-mail ou senha incorretos.", com a mesma resposta nos três casos. |
| **Pai** | [RF-33](#rf-33) |
| **Origem** | NS-11 (principal); NS-13 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — uma resposta diferente por caso revelaria quais e-mails estão cadastrados ([RNF-F05](rnf.md#rnf-f05)). |
| **Vínculos** | UC: [UC-02 Autenticar](../casos-de-uso/README.md#uc-02) (exceção) — na ficha: [UC-02 E3.3](../casos-de-uso/UC-02-autenticar.md#e3-3) · US/CA: [US-02 · CA-05](../historias/US-02-entrar-no-sistema.md#us-02-ca-05) (TA-11) |
| **Evidência (complementar)** | 401 `CREDENCIAIS_INVALIDAS`. `contas/tests/test_api_autenticacao.py::test_senha_errada_email_inexistente_e_inativo_respondem_igual`; `pages/PaginaEntrar.test.tsx` ("credenciais inválidas aparecem num aviso no topo, que recebe o foco") |
| **Código (complementar)** | `contas/api/views.py::LoginView.post` |
| **Regras de negócio** | [Credenciais inválidas](../glossario.md#credenciais-invalidas) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-33-2"></a>RF-33.2 · Recusar tentativas de entrada em excesso

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o visitante tente entrar mais de 5 vezes com o mesmo e-mail, ou mais de 20 vezes a partir da mesma origem, dentro de 1 minuto, sem conferir as credenciais (nem a senha certa) e sem iniciar sessão, e informar em quantos segundos ele pode tentar de novo, sem dizer qual limite foi atingido nem se o e-mail existe. |
| **Pai** | [RF-33](#rf-33) |
| **Origem** | NS-11 (principal); NS-13 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — sem limite, qualquer pessoa poderia adivinhar a senha de uma conta por tentativa e erro ([L-03](srs.md#l-03), resolvida; limites em [RNF-F12](rnf.md#rnf-f12)). |
| **Vínculos** | UC: [UC-02 Autenticar](../casos-de-uso/README.md#uc-02) (exceção) — na ficha: [UC-02 E3.1](../casos-de-uso/UC-02-autenticar.md#e3-1) · US/CA: [US-02 · CA-06](../historias/US-02-entrar-no-sistema.md#us-02-ca-06) (TA-12) |
| **Evidência (complementar)** | 429 `LIMITE_DE_TENTATIVAS` com `Retry-After`. `contas/tests/test_limites_de_tentativas.py::test_sexta_tentativa_com_o_mesmo_email_responde_429_com_a_espera`, `::test_senha_certa_tambem_e_recusada_depois_do_limite`, `::test_limite_por_ip_vale_para_varios_emails`, `::test_resposta_429_nao_revela_o_limite_nem_se_o_email_existe`; `pages/PaginaEntrar.test.tsx` ("muitas tentativas mostram a mensagem do servidor no aviso do topo, que recebe o foco") |
| **Código (complementar)** | `contas/api/limites.py::LimiteDeLoginPorEmail`, `contas/api/limites.py::LimiteDeLoginPorIp` |
| **Regras de negócio** | [Tentativas em excesso](../glossario.md#tentativas-em-excesso), [credenciais inválidas](../glossario.md#credenciais-invalidas) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-34"></a>RF-34 · Continuar identificado sem informar a senha de novo

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao usuário autenticado continuar usando o sistema, inclusive depois de recarregar a página ou abrir outra aba, sem informar a senha de novo enquanto a sessão não expirar (1 dia depois da entrada). |
| **Origem** | NS-11 |
| **Funcionalidade** | Extra (AUT-06) |
| **Prioridade (QFD)** | Esperado — pedir a senha a cada 30 minutos de uso atrapalharia a operação do dia a dia. |
| **Vínculos** | UC: [UC-02 Autenticar](../casos-de-uso/README.md#uc-02) (alternativa) — na ficha: [UC-02 A4.1](../casos-de-uso/UC-02-autenticar.md#a4-1) · US/CA: [US-03 · CA-01](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-01) (TA-14), [US-03 · CA-05](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-05) (TA-18) |
| **Evidência (complementar)** | `POST /api/auth/refresh/` chamado pelo frontend no 401. `contas/tests/test_api_autenticacao.py::test_refresh_valido_devolve_access_novo_que_funciona_no_me`, `::test_refresh_dura_o_tempo_configurado`; `api/cliente.test.ts` ("401 NAO_AUTENTICADO renova o access e repete a requisição com o novo"); `components/sessao/SessaoProvider.test.tsx` ("restaura a sessão salva e confirma com /me, que atualiza o usuário") |
| **Código (complementar)** | `contas/api/views.py::RenovarTokenView.post`, `contas/api/views.py::_refresh_de_usuario_ativo` |
| **Regras de negócio** | [Sessão](../glossario.md#sessao) |
| **Decisões** | [DEC-04](../decisoes/DEC-04.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-34-1"></a>RF-34.1 · Encerrar a sessão expirada

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o usuário continue usando uma sessão expirada ou recusada e informar "Sua sessão expirou. Faça login novamente.", levando-o a entrar de novo e depois de volta à tela em que estava. |
| **Pai** | [RF-34](#rf-34) |
| **Origem** | NS-11 (principal); NS-13 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — sem a explicação, as telas só passariam a falhar. |
| **Vínculos** | UC: [UC-02 Autenticar](../casos-de-uso/README.md#uc-02) (exceção) — na ficha: [UC-02 E4.1](../casos-de-uso/UC-02-autenticar.md#e4-1), [E4.2](../casos-de-uso/UC-02-autenticar.md#e4-2) · US/CA: [US-03 · CA-06](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-06) (TA-19), [US-03 · CA-07](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-07) (TA-20) |
| **Evidência (complementar)** | `api/cliente.test.ts` ("se a renovação falhar, limpa a sessão, avisa os ouvintes e lança SESSAO_EXPIRADA"); `components/sessao/SessaoProvider.test.tsx` ("quando a sessão expira, avisa e leva para o login com o caminho atual"); `contas/tests/test_api_autenticacao.py::test_refresh_invalido_responde_401_no_formato_padrao` |
| **Código (complementar)** | `api/cliente.ts::tentarRenovar`, `api/cliente.ts::encerrarSessaoExpirada` |
| **Regras de negócio** | [Sessão](../glossario.md#sessao) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-35"></a>RF-35 · Consultar os próprios dados

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao usuário autenticado consultar os próprios dados e ver o nome, o e-mail, a matrícula e o perfil atuais. |
| **Origem** | NS-11 |
| **Funcionalidade** | Extra (AUT-03) |
| **Prioridade (QFD)** | Esperado — a tela mostra quem está agindo e confirma o perfil, que a Equipe de TI pode ter mudado. |
| **Vínculos** | UC: [UC-02 Autenticar](../casos-de-uso/README.md#uc-02) (alternativa) — na ficha: [UC-02 A4.2](../casos-de-uso/UC-02-autenticar.md#a4-2) · US/CA: [US-03 · CA-03](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-03) (TA-16), [US-03 · CA-04](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-04) (TA-17) |
| **Evidência (complementar)** | `GET /api/auth/me/`; "Solicitante: nome (matrícula)" em `/reservas/nova`. `contas/tests/test_api_autenticacao.py::test_me_com_bearer_valido_devolve_usuario_com_perfil`; `components/sessao/SessaoProvider.test.tsx` ("restaura a sessão salva e confirma com /me, que atualiza o usuário") |
| **Código (complementar)** | `contas/api/views.py::UsuarioAtualView.get` |
| **Regras de negócio** | [Usuário](../glossario.md#usuario), [perfil](../glossario.md#perfil) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-36"></a>RF-36 · Sair

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao usuário autenticado sair e ver a página inicial sem nenhuma identificação, com a mensagem "Você saiu da sua conta.". |
| **Origem** | NS-11 (principal); NS-14 |
| **Funcionalidade** | Extra (AUT-06) |
| **Prioridade (QFD)** | Esperado — num computador compartilhado, sem sair, a próxima pessoa agiria em nome da anterior. |
| **Vínculos** | UC: [UC-02 Autenticar](../casos-de-uso/README.md#uc-02) (alternativa) — na ficha: [UC-02 A4.3](../casos-de-uso/UC-02-autenticar.md#a4-3) · US/CA: [US-03 · CA-02](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-02) (TA-15) |
| **Evidência (complementar)** | Só no navegador (sem chamada à API: os tokens são descartados); "Sair" no cabeçalho de toda tela, que leva ao início `/`. `components/sessao/SessaoProvider.test.tsx` ("sair numa rota protegida limpa a sessão, avisa e vai para o início"); `api/sessao.test.ts` |
| **Código (complementar)** | `components/sessao/SessaoProvider.tsx::SessaoProvider`, `api/sessao.ts::limparSessao` |
| **Regras de negócio** | [Sessão](../glossario.md#sessao) |
| **Decisões** | [DEC-04](../decisoes/DEC-04.md) (sem revogação de tokens: lacuna [L-04](srs.md#lacunas)) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

## Administração

### <a id="rf-37"></a>RF-37 · Criar usuário Gestor

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir à Equipe de TI criar um usuário com nome, matrícula, e-mail e senha e perfil Gestor e ver o usuário com acesso à administração do sistema. |
| **Origem** | NS-11 |
| **Funcionalidade** | Extra ([DEC-04](../decisoes/DEC-04.md)) |
| **Prioridade (QFD)** | Normal — sem pelo menos um Gestor, nenhum espaço é cadastrado e nenhum pedido é decidido. |
| **Vínculos** | UC: [UC-20 Criar usuário Gestor](../casos-de-uso/README.md#uc-20) (fluxo principal) — na ficha: [UC-20 passos 1 a 4](../casos-de-uso/fichas-resumidas.md#uc20-p1) · US/CA: [US-17 · CA-01](../historias/US-17-criar-o-primeiro-gestor.md#us-17-ca-01) (TA-148), [US-17 · CA-02](../historias/US-17-criar-o-primeiro-gestor.md#us-17-ca-02) (TA-149), [US-17 · CA-03](../historias/US-17-criar-o-primeiro-gestor.md#us-17-ca-03) (TA-150) |
| **Evidência (complementar)** | `python manage.py createsuperuser`; administração em `/admin/`. `contas/tests/test_usuario_manager.py::test_create_superuser_cria_gestor_com_staff_e_superuser`, `::test_superusuario_e_gestor_e_usuario_comum_nao`; `exemplos/tests/test_carregar_dados_exemplo.py::test_cria_um_gestor_e_dois_solicitantes` |
| **Código (complementar)** | `contas/infrastructure/models.py::UsuarioManager.create_superuser` |
| **Regras de negócio** | [Gestor](../glossario.md#gestor), [Equipe de TI](../glossario.md#equipe-de-ti) |
| **Decisões** | [DEC-04](../decisoes/DEC-04.md); premissa P-06 da [Visão](../visao.md#premissas) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |
