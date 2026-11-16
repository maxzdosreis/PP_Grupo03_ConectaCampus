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
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | RF-36 passa a encerrar a sessão também no sistema: depois de sair, a credencial de renovação é recusada (a de acesso vale até expirar, lacuna L-04); RF-34 com a troca da credencial de renovação a cada uso e as duas janelas; vínculos com US-03 · CA-06, CA-09 e CA-10 e os TAs renumerados (TA-19 e TA-20 passam a TA-20 e TA-21; TA-21 a TA-158 passam a TA-24 a TA-161) (AUT-09). Sem aprovação. |
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | RF-34: evidência e código da trava entre janelas na renovação (achado da revisão do PR: uma renovação da outra janela que demorasse mais de 1 s encerrava as duas, AUT-09). Sem aprovação. |
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-96 a TA-107 passam a TA-97, TA-98, TA-99, TA-102, TA-103, TA-105, TA-106, TA-107, TA-109, TA-110, TA-113 e TA-114, e TA-108 a TA-161 passam a TA-115 a TA-168, para os TAs novos das US-10 e US-11 (consulta em páginas) seguirem a ordem das histórias (RES-10). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Aplicação na especificação do CR-04 (DEC-09), com a implementação pendente na tarefa AUT-12 (REQ-13): RF-32.1 com a matrícula só de dígitos (o limite de 20 fica como limite técnico); Vínculos do RF-32 e do RF-32.1 com os CAs novos. A especificação está adiante do código de propósito. Sem aprovação. |
| 0.1 | 16/11/2026 | Max Zimmermann dos Reis | RF-41 · Trocar a própria senha, RF-41.1 · Recusar a troca de senha inválida e RF-41.2 · Recusar tentativas de troca de senha em excesso, a partir da NS-15 ([DEC-26](../decisoes/DEC-26.md), [CR-06](../mudancas/CR-06-trocar-a-propria-senha.md)); [US-21](../historias/US-21-trocar-a-propria-senha.md) e UC-02 A4.4 e E4.3 a E4.6 (AUT-10). Mudança posterior à entrega de 13/11/2026: a especificação entregue não foi alterada. Sem aprovação. |
| 0.1 | 16/11/2026 | Max Zimmermann dos Reis | RF-42 · Listar os usuários, RF-43 · Alterar o perfil e a situação da conta de um usuário, RF-43.1 · Recusar que o Gestor rebaixe ou desative a própria conta e RF-43.2 · Recusar que o sistema fique sem Gestor ativo, a partir da NS-11 ([DEC-27](../decisoes/DEC-27.md), [CR-07](../mudancas/CR-07-gestao-de-usuarios.md)); [US-22](../historias/US-22-gerir-usuarios.md), UC-23 e as RN-18 e RN-19 (AUT-11). Mudança posterior à entrega de 13/11/2026: a especificação entregue não foi alterada. Sem aprovação. |

## Cadastro

### <a id="rf-32"></a>RF-32 · Cadastrar-se como Solicitante

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao visitante cadastrar-se com nome, matrícula, e-mail e senha e entrar no sistema identificado com o perfil Solicitante. |
| **Origem** | NS-15 |
| **Funcionalidade** | Extra (AUT-04) |
| **Prioridade (QFD)** | Esperado — sem cadastro próprio, cada aluno dependeria da Equipe de TI para começar a pedir. |
| **Vínculos** | UC: [UC-01 Cadastrar-se](../casos-de-uso/README.md#uc-01) (fluxo principal) — na ficha: [UC-01 passos 1 a 4](../casos-de-uso/fichas-resumidas.md#uc01-p1) · US/CA: [US-01 · CA-01](../historias/US-01-criar-minha-conta.md#us-01-ca-01) (TA-01), [US-01 · CA-02](../historias/US-01-criar-minha-conta.md#us-01-ca-02) (TA-02), [US-01 · CA-03](../historias/US-01-criar-minha-conta.md#us-01-ca-03) (TA-03), [US-01 · CA-04](../historias/US-01-criar-minha-conta.md#us-01-ca-04) (TA-04), [US-01 · CA-10](../historias/US-01-criar-minha-conta.md#us-01-ca-10) (TA-10), [US-02 · CA-03](../historias/US-02-entrar-no-sistema.md#us-02-ca-03) (TA-13) |
| **Evidência (complementar)** | `POST /api/auth/cadastro/` → 201, seguido do login; tela `/cadastro`. `contas/tests/test_api_cadastro.py::test_cadastro_valido_responde_201_com_solicitante_sem_senha`, `::test_usuario_recem_cadastrado_consegue_fazer_login`, `::test_campos_de_privilegio_no_corpo_sao_ignorados`; `pages/PaginaCadastro.test.tsx` ("com sucesso, cadastra, entra com as mesmas credenciais e vai para /reservas/nova") |
| **Código (complementar)** | `contas/application/casos_de_uso.py::CadastrarSolicitante.executar`, `contas/domain/cadastro.py::DadosDeCadastro` |
| **Regras de negócio** | [RN-13](regras-de-negocio.md#rn-13). Glossário e detalhes: [Usuário](../glossario.md#usuario), [matrícula](../glossario.md#matricula), [perfil](../glossario.md#perfil), [Solicitante](../glossario.md#solicitante) |
| **Decisões** | [DEC-04](../decisoes/DEC-04.md) (o cadastro público nunca cria Gestor), [DEC-09](../decisoes/DEC-09.md) (decidida na Aula 7: matrícula só com dígitos; [CR-04](../mudancas/CR-04-matricula-so-digitos.md), tarefa AUT-12) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-32-1"></a>RF-32.1 · Recusar cadastro com dados inválidos

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o visitante se cadastre sem nome, matrícula, e-mail ou senha, com nome de mais de 150 caracteres, com matrícula que não seja formada só por dígitos ou de mais de 20 caracteres (limite técnico), ou com e-mail em formato inválido, sem criar a conta, e informar a regra violada no campo correspondente. |
| **Pai** | [RF-32](#rf-32) |
| **Origem** | NS-15 (principal); NS-13 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — a matrícula identifica quem pediu cada reserva (NS-11). |
| **Vínculos** | UC: [UC-01 Cadastrar-se](../casos-de-uso/README.md#uc-01) (exceção) — na ficha: [UC-01 E3.1](../casos-de-uso/fichas-resumidas.md#uc01-e3-1) · US/CA: [US-01 · CA-05](../historias/US-01-criar-minha-conta.md#us-01-ca-05) (TA-05), [US-01 · CA-06](../historias/US-01-criar-minha-conta.md#us-01-ca-06) (TA-06), [US-01 · CA-07](../historias/US-01-criar-minha-conta.md#us-01-ca-07) (TA-07) |
| **Evidência (complementar)** | 400 com `campos`. `contas/tests/test_api_cadastro.py::test_campos_ausentes_respondem_400_com_cada_campo`, `::test_nome_so_com_espacos_responde_400_campo_obrigatorio`, `::test_matricula_com_espaco_responde_400`, `::test_email_malformado_responde_400`; `contas/tests/test_cadastro_dominio.py::test_nome_acima_do_limite_lanca_texto_muito_longo`, `::test_matricula_longa_ou_com_espaco_no_meio_lanca_matricula_invalida [x]` **Regra nova ([CR-04](../mudancas/CR-04-matricula-so-digitos.md), aplicada na especificação em 10/11/2026):** a matrícula só com dígitos — implementação pendente (tarefa AUT-12); os testes citados acima verificam a regra anterior. |
| **Código (complementar)** | `contas/domain/cadastro.py::DadosDeCadastro`, `contas/domain/excecoes.py::MatriculaInvalida` |
| **Regras de negócio** | [RN-13](regras-de-negocio.md#rn-13). Glossário e detalhes: [Matrícula](../glossario.md#matricula), [usuário](../glossario.md#usuario) |
| **Decisões** | [DEC-09](../decisoes/DEC-09.md) (decidida na Aula 7: só dígitos, sem quantidade mínima; [CR-04](../mudancas/CR-04-matricula-so-digitos.md), tarefa AUT-12) |
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
| **Vínculos** | UC: [UC-01 Cadastrar-se](../casos-de-uso/README.md#uc-01) (exceção) — na ficha: [UC-01 E3.2](../casos-de-uso/fichas-resumidas.md#uc01-e3-2) · US/CA: [US-01 · CA-08](../historias/US-01-criar-minha-conta.md#us-01-ca-08) (TA-08) |
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
| **Vínculos** | UC: [UC-01 Cadastrar-se](../casos-de-uso/README.md#uc-01) (exceção) — na ficha: [UC-01 E3.3](../casos-de-uso/fichas-resumidas.md#uc01-e3-3) · US/CA: [US-01 · CA-09](../historias/US-01-criar-minha-conta.md#us-01-ca-09) (TA-09) |
| **Evidência (complementar)** | 409 `EMAIL_JA_CADASTRADO` ou `MATRICULA_JA_CADASTRADA`. `contas/tests/test_api_cadastro.py::test_email_repetido_com_caixa_diferente_responde_409`, `::test_matricula_repetida_responde_409`; `contas/tests/test_repositorio_usuarios.py::test_email_repetido_lanca_email_ja_cadastrado [x]` |
| **Código (complementar)** | `contas/application/casos_de_uso.py::CadastrarSolicitante.executar`, `contas/infrastructure/repositorio_django.py::RepositorioUsuariosDjango.criar_solicitante` |
| **Regras de negócio** | [RN-13](regras-de-negocio.md#rn-13). Glossário e detalhes: [Usuário](../glossario.md#usuario), [matrícula](../glossario.md#matricula) |
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
| **Vínculos** | UC: [UC-02 Autenticar](../casos-de-uso/README.md#uc-02) (fluxo principal) — na ficha: [UC-02 passos 1 a 4](../casos-de-uso/UC-02-autenticar.md#p1) · US/CA: [US-02 · CA-01](../historias/US-02-entrar-no-sistema.md#us-02-ca-01) (TA-11), [US-02 · CA-02](../historias/US-02-entrar-no-sistema.md#us-02-ca-02) (TA-12), [US-02 · CA-03](../historias/US-02-entrar-no-sistema.md#us-02-ca-03) (TA-13), [US-02 · CA-04](../historias/US-02-entrar-no-sistema.md#us-02-ca-04) (TA-14), [US-02 · CA-07](../historias/US-02-entrar-no-sistema.md#us-02-ca-07) (TA-17) |
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
| **Vínculos** | UC: [UC-02 Autenticar](../casos-de-uso/README.md#uc-02) (exceção) — na ficha: [UC-02 E3.3](../casos-de-uso/UC-02-autenticar.md#e3-3) · US/CA: [US-02 · CA-05](../historias/US-02-entrar-no-sistema.md#us-02-ca-05) (TA-15) |
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
| **Vínculos** | UC: [UC-02 Autenticar](../casos-de-uso/README.md#uc-02) (exceção) — na ficha: [UC-02 E3.1](../casos-de-uso/UC-02-autenticar.md#e3-1) · US/CA: [US-02 · CA-06](../historias/US-02-entrar-no-sistema.md#us-02-ca-06) (TA-16) |
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
| **Vínculos** | UC: [UC-02 Autenticar](../casos-de-uso/README.md#uc-02) (alternativa) — na ficha: [UC-02 A4.1](../casos-de-uso/UC-02-autenticar.md#a4-1) · US/CA: [US-03 · CA-01](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-01) (TA-18), [US-03 · CA-05](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-05) (TA-22), [US-03 · CA-06](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-06) (TA-23) |
| **Evidência (complementar)** | `POST /api/auth/refresh/` chamado pelo frontend no 401; cada renovação devolve também um `refresh` novo, com o mesmo prazo final, e revoga o usado (AUT-09). `contas/tests/test_api_autenticacao.py::test_refresh_valido_devolve_access_novo_que_funciona_no_me`, `::test_refresh_dura_o_tempo_configurado`, `::test_refresh_trocado_mantem_o_prazo_final_da_entrada`, `::test_refresh_novo_renova_de_novo_em_cadeia`; `api/cliente.test.ts` ("renovação recusada com outro refresh já salvo por outra aba repete com a sessão nova e não desloga", "com a renovação de outra aba em andamento, espera a trava e usa a sessão nova sem renovar, por mais que ela demore"); `api/cliente.test.ts` ("401 NAO_AUTENTICADO renova o access e repete a requisição com o novo"); `components/sessao/SessaoProvider.test.tsx` ("restaura a sessão salva e confirma com /me, que atualiza o usuário") |
| **Código (complementar)** | `contas/api/views.py::RenovarTokenView.post`, `contas/api/views.py::_refresh_de_usuario_ativo`, `contas/api/views.py::_trocar_refresh`, `api/cliente.ts::comTravaEntreAbas`, `api/cliente.ts::renovarSeAindaPreciso`, `api/cliente.ts::accessDeOutraAba` |
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
| **Vínculos** | UC: [UC-02 Autenticar](../casos-de-uso/README.md#uc-02) (exceção) — na ficha: [UC-02 E4.1](../casos-de-uso/UC-02-autenticar.md#e4-1), [E4.2](../casos-de-uso/UC-02-autenticar.md#e4-2) · US/CA: [US-03 · CA-07](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-07) (TA-24), [US-03 · CA-08](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-08) (TA-25), [US-03 · CA-10](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-10) (TA-27) |
| **Evidência (complementar)** | `api/cliente.test.ts` ("se a renovação falhar, limpa a sessão, avisa os ouvintes e lança SESSAO_EXPIRADA"); `components/sessao/SessaoProvider.test.tsx` ("quando a sessão expira, avisa e leva para o login com o caminho atual"); `contas/tests/test_api_autenticacao.py::test_refresh_invalido_responde_401_no_formato_padrao`, `::test_renovacao_troca_o_refresh_e_o_antigo_passa_a_ser_recusado` |
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
| **Vínculos** | UC: [UC-02 Autenticar](../casos-de-uso/README.md#uc-02) (alternativa) — na ficha: [UC-02 A4.2](../casos-de-uso/UC-02-autenticar.md#a4-2) · US/CA: [US-03 · CA-03](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-03) (TA-20), [US-03 · CA-04](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-04) (TA-21) |
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
| **Enunciado** | O sistema deve permitir ao usuário autenticado sair e ver a página inicial sem nenhuma identificação, com a mensagem "Você saiu da sua conta."; depois de sair, a sessão não pode mais ser renovada, em nenhum lugar. |
| **Origem** | NS-11 (principal); NS-14 |
| **Funcionalidade** | Extra (AUT-06) |
| **Prioridade (QFD)** | Esperado — num computador compartilhado, sem sair, a próxima pessoa agiria em nome da anterior. |
| **Vínculos** | UC: [UC-02 Autenticar](../casos-de-uso/README.md#uc-02) (alternativa) — na ficha: [UC-02 A4.3](../casos-de-uso/UC-02-autenticar.md#a4-3) · US/CA: [US-03 · CA-02](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-02) (TA-19), [US-03 · CA-09](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-09) (TA-26) |
| **Evidência (complementar)** | `POST /api/auth/logout/` com o `refresh`, chamado pelo frontend sem esperar a resposta (AUT-09); "Sair" no cabeçalho de toda tela, que leva ao início `/`. `contas/tests/test_api_sair.py::test_sair_revoga_o_refresh_e_ele_deixa_de_renovar`, `::test_sair_de_novo_com_o_mesmo_refresh_responde_200`; `components/sessao/SessaoProvider.test.tsx` ("sair numa rota protegida limpa a sessão, avisa e vai para o início", "sair revoga o refresh na API sem esperar a resposta"); `api/sessao.test.ts` |
| **Código (complementar)** | `contas/api/views.py::SairView.post`, `components/sessao/SessaoProvider.tsx::SessaoProvider`, `api/sessao.ts::limparSessao` |
| **Regras de negócio** | [Sessão](../glossario.md#sessao) |
| **Decisões** | [DEC-04](../decisoes/DEC-04.md) (a credencial de acesso não é revogada ao sair: lacuna [L-04](srs.md#lacunas)) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

## Conta

### <a id="rf-41"></a>RF-41 · Trocar a própria senha

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao usuário autenticado trocar a própria senha, informando a senha atual e a nova, e ver a mensagem "Senha alterada com sucesso." sem sair da conta; a senha nova segue a mesma política de senha do cadastro, e a sessão aberta continua valendo enquanto as sessões abertas em outros aparelhos deixam de ser renovadas. |
| **Origem** | NS-15 (principal); NS-11 |
| **Funcionalidade** | Extra (AUT-10) |
| **Prioridade (QFD)** | Esperado — sem a troca, quem suspeita que a senha vazou, ou quer uma melhor, depende da administração (a mesma [NS-15](../visao.md#ns-15) de não depender de um gestor). |
| **Vínculos** | UC: [UC-02 Autenticar](../casos-de-uso/README.md#uc-02) (alternativa) — na ficha: [UC-02 A4.4](../casos-de-uso/UC-02-autenticar.md#a4-4) · US/CA: [US-21 · CA-01](../historias/US-21-trocar-a-propria-senha.md#us-21-ca-01) (TA-194), [US-21 · CA-02](../historias/US-21-trocar-a-propria-senha.md#us-21-ca-02) (TA-195), [US-21 · CA-07](../historias/US-21-trocar-a-propria-senha.md#us-21-ca-07) (TA-200) |
| **Evidência (complementar)** | `POST /api/auth/senha/` com `senha_atual`, `nova_senha` e, opcional, `refresh_atual`; tela `/conta` ("Minha conta"), com o link "Minha conta" no cabeçalho. `contas/tests/test_api_alterar_senha.py::test_troca_com_sucesso_responde_200_e_a_nova_senha_passa_a_valer`, `::test_troca_revoga_os_refresh_das_outras_sessoes_e_mantem_a_atual`, `::test_pessoa_so_troca_a_propria_senha_mesmo_enviando_outro_id`; `contas/tests/test_alterar_senha.py::test_troca_valida_passa_a_valer_a_nova_senha_e_nao_a_antiga`; `pages/PaginaMinhaConta.test.tsx` ("sucesso envia a senha e o refresh da sessão, limpa os campos e mantém a pessoa logada") |
| **Código (complementar)** | `contas/application/casos_de_uso.py::AlterarSenha`, `contas/api/views.py::AlterarSenhaView`, `components/sessao/FormularioDeTrocaDeSenha.tsx::FormularioDeTrocaDeSenha`, `pages/PaginaMinhaConta.tsx::PaginaMinhaConta` |
| **Regras de negócio** | [Troca de senha](../glossario.md#troca-de-senha), [política de senha](../glossario.md#politica-de-senha), [sessão](../glossario.md#sessao) |
| **Decisões** | [DEC-26](../decisoes/DEC-26.md) (a troca entra no 1.0, como extra de autenticação; a credencial de acesso já emitida não é revogada, [L-04](srs.md#l-04)) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-41-1"></a>RF-41.1 · Recusar a troca de senha inválida

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que a senha seja trocada quando a senha atual informada não é a da conta, quando a senha nova é igual à atual ou quando ela não cumpre a política de senha, informando o motivo junto ao campo, sem encerrar a sessão e sem mudar a senha. |
| **Pai** | [RF-41](#rf-41) |
| **Origem** | NS-15 (principal); NS-11 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — sem conferir a senha atual, quem usasse um computador deixado aberto trocaria a senha da dona da conta; recusada, a pessoa não pode ser deslogada por errar a senha. |
| **Vínculos** | UC: [UC-02 Autenticar](../casos-de-uso/README.md#uc-02) (exceção) — na ficha: [UC-02 E4.4](../casos-de-uso/UC-02-autenticar.md#e4-4), [UC-02 E4.5](../casos-de-uso/UC-02-autenticar.md#e4-5), [UC-02 E4.6](../casos-de-uso/UC-02-autenticar.md#e4-6) · US/CA: [US-21 · CA-03](../historias/US-21-trocar-a-propria-senha.md#us-21-ca-03) (TA-196), [US-21 · CA-04](../historias/US-21-trocar-a-propria-senha.md#us-21-ca-04) (TA-197), [US-21 · CA-05](../historias/US-21-trocar-a-propria-senha.md#us-21-ca-05) (TA-198) |
| **Evidência (complementar)** | 400 `SENHA_ATUAL_INCORRETA`, `NOVA_SENHA_IGUAL_A_ATUAL` e `SENHA_FRACA`, nunca 401. `contas/tests/test_api_alterar_senha.py::test_senha_atual_errada_responde_400_com_codigo_proprio_e_nunca_401`, `::test_nova_senha_igual_a_atual_responde_400`, `::test_nova_senha_que_viola_a_politica_responde_400_senha_fraca [x]`; `api/cliente.test.ts` ("400 SENHA_ATUAL_INCORRETA na troca de senha não renova nem encerra a sessão"); `pages/PaginaMinhaConta.test.tsx` ("senha atual errada mostra a mensagem no campo e NÃO desloga") |
| **Código (complementar)** | `contas/application/casos_de_uso.py::AlterarSenha`, `contas/domain/excecoes.py::SenhaAtualIncorreta`, `contas/domain/excecoes.py::NovaSenhaIgualAAtual`, `contas/domain/excecoes.py::SenhaFraca` |
| **Regras de negócio** | [Troca de senha](../glossario.md#troca-de-senha), [política de senha](../glossario.md#politica-de-senha) |
| **Decisões** | [DEC-26](../decisoes/DEC-26.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-41-2"></a>RF-41.2 · Recusar tentativas de troca de senha em excesso

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o usuário tente trocar a senha mais de 5 vezes dentro de 1 minuto, sem conferir a senha atual (nem a certa) e sem trocar a senha, e informar em quantos segundos ele pode tentar de novo. |
| **Pai** | [RF-41](#rf-41) |
| **Origem** | NS-15 (principal); NS-11 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — a troca confere a senha atual; sem limite, uma sessão aberta num computador alheio serviria para adivinhá-la por tentativa e erro ([RNF-F12](rnf.md#rnf-f12)). |
| **Vínculos** | UC: [UC-02 Autenticar](../casos-de-uso/README.md#uc-02) (exceção) — na ficha: [UC-02 E4.3](../casos-de-uso/UC-02-autenticar.md#e4-3) · US/CA: [US-21 · CA-06](../historias/US-21-trocar-a-propria-senha.md#us-21-ca-06) (TA-199) |
| **Evidência (complementar)** | 429 `LIMITE_DE_TENTATIVAS` com `Retry-After`, contado por usuário e não por origem. `contas/tests/test_api_alterar_senha.py::test_sexta_troca_seguida_responde_429_traduzido_pelo_tratador`, `::test_limite_de_troca_e_por_usuario_e_nao_por_ip`, `::test_limite_de_troca_vem_das_settings_a_cada_requisicao` |
| **Código (complementar)** | `contas/api/limites.py::LimiteDeTrocaDeSenhaPorUsuario` |
| **Regras de negócio** | [Tentativas em excesso](../glossario.md#tentativas-em-excesso) |
| **Decisões** | [DEC-26](../decisoes/DEC-26.md) |
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
| **Vínculos** | UC: [UC-20 Criar usuário Gestor](../casos-de-uso/README.md#uc-20) (fluxo principal) — na ficha: [UC-20 passos 1 a 4](../casos-de-uso/fichas-resumidas.md#uc20-p1) · US/CA: [US-17 · CA-01](../historias/US-17-criar-o-primeiro-gestor.md#us-17-ca-01) (TA-179), [US-17 · CA-02](../historias/US-17-criar-o-primeiro-gestor.md#us-17-ca-02) (TA-180), [US-17 · CA-03](../historias/US-17-criar-o-primeiro-gestor.md#us-17-ca-03) (TA-181) |
| **Evidência (complementar)** | `python manage.py createsuperuser`; administração em `/admin/`. `contas/tests/test_usuario_manager.py::test_create_superuser_cria_gestor_com_staff_e_superuser`, `::test_superusuario_e_gestor_e_usuario_comum_nao`; `exemplos/tests/test_carregar_dados_exemplo.py::test_cria_um_gestor_e_dois_solicitantes` |
| **Código (complementar)** | `contas/infrastructure/models.py::UsuarioManager.create_superuser` |
| **Regras de negócio** | [Gestor](../glossario.md#gestor), [Equipe de TI](../glossario.md#equipe-de-ti) |
| **Decisões** | [DEC-04](../decisoes/DEC-04.md); premissa P-06 da [Visão](../visao.md#premissas) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

## Gestão de usuários

### <a id="rf-42"></a>RF-42 · Listar os usuários

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao Gestor listar os usuários, em páginas de 20 (até 100) e em ordem de nome, buscando por nome, e-mail ou matrícula e filtrando por perfil e por situação da conta, e ver de cada um o nome, o e-mail, a matrícula, o perfil, se a conta está ativa e as datas de cadastro e do último acesso, sem nunca ver senha nem credencial de ninguém. |
| **Origem** | NS-11 |
| **Funcionalidade** | Extra (AUT-11) |
| **Prioridade (QFD)** | Normal — sem a lista, o Gestor não sabe quem pode promover ou bloquear; só quem cuida do serviço a vê. |
| **Vínculos** | UC: [UC-23 Gerir usuários](../casos-de-uso/README.md#uc-23) (fluxo principal) — na ficha: [UC-23 passos 1 a 3](../casos-de-uso/fichas-resumidas.md#uc23-p1) · US/CA: [US-22 · CA-01](../historias/US-22-gerir-usuarios.md#us-22-ca-01) (TA-201), [US-22 · CA-08](../historias/US-22-gerir-usuarios.md#us-22-ca-08) (TA-208) |
| **Evidência (complementar)** | `GET /api/usuarios/?busca=&perfil=&ativo=&pagina=&tamanho=`; tela `/usuarios` ("Usuários"), com o item no menu só para o Gestor; o Solicitante recebe 403 `ACAO_NAO_PERMITIDA` e o anônimo, 401. `contas/tests/test_api_gestao_de_usuarios.py::test_gestor_lista_os_usuarios_no_formato_padrao`, `::test_listagem_pagina_e_depois_da_ultima_devolve_vazio_com_200`, `::test_busca_por_nome_email_e_matricula`, `::test_resposta_nunca_traz_hash_de_senha_nem_token`, `::test_solicitante_nao_lista_usuarios`; `pages/PaginaUsuarios.test.tsx` ("mostra a tabela com a contagem da API como legenda e o perfil e a situação em texto") |
| **Código (complementar)** | `contas/application/casos_de_uso.py::ListarUsuarios`, `contas/infrastructure/repositorio_django.py::RepositorioGestaoDeUsuariosDjango`, `contas/api/views.py::UsuariosView`, `compartilhado/domain/paginacao.py::Paginacao`, `pages/PaginaUsuarios.tsx::PaginaUsuarios` |
| **Regras de negócio** | [Usuário](../glossario.md#usuario), [perfil](../glossario.md#perfil), [usuário ativo](../glossario.md#usuario-ativo) |
| **Decisões** | [DEC-27](../decisoes/DEC-27.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-43"></a>RF-43 · Alterar o perfil e a situação da conta de um usuário

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao Gestor promover um Solicitante a Gestor, rebaixar outro Gestor a Solicitante, desativar e reativar a conta de outra pessoa, depois de confirmar, e ver o usuário atualizado; pedir o estado em que o usuário já está não muda nada, a conta desativada deixa de entrar e de renovar a sessão e as reservas da pessoa continuam como estão. |
| **Origem** | NS-11 |
| **Funcionalidade** | Extra (AUT-11) |
| **Prioridade (QFD)** | Normal — sem a alteração pela tela, dar ou tirar um acesso depende da Equipe de TI, que não é ator do negócio ([L-10](srs.md#l-10)). |
| **Vínculos** | UC: [UC-23 Gerir usuários](../casos-de-uso/README.md#uc-23) (fluxo principal) — na ficha: [UC-23 passos 4 a 6](../casos-de-uso/fichas-resumidas.md#uc23-p4) · US/CA: [US-22 · CA-02](../historias/US-22-gerir-usuarios.md#us-22-ca-02) (TA-202), [US-22 · CA-03](../historias/US-22-gerir-usuarios.md#us-22-ca-03) (TA-203), [US-22 · CA-04](../historias/US-22-gerir-usuarios.md#us-22-ca-04) (TA-204), [US-22 · CA-05](../historias/US-22-gerir-usuarios.md#us-22-ca-05) (TA-205) |
| **Evidência (complementar)** | `PATCH /api/usuarios/{id}/` com `perfil` e/ou `ativo`, idempotente, no limite de 30 por minuto por conta (429 `LIMITE_DE_TENTATIVAS`); tela `/usuarios` com as ações "Promover a Gestor", "Rebaixar a Solicitante", "Desativar" e "Reativar" e diálogo de confirmação. `contas/tests/test_api_gestao_de_usuarios.py::test_gestor_promove_um_solicitante`, `::test_gestor_desativa_e_reativa_um_solicitante`, `::test_pedir_o_estado_atual_responde_200_sem_mudar_nada`, `::test_desativado_nao_entra_e_recebe_a_mesma_resposta_de_credenciais_invalidas`, `::test_access_de_quem_foi_desativado_deixa_de_funcionar`, `::test_refresh_de_quem_foi_desativado_nao_renova_e_nao_rotaciona`, `::test_desativar_nao_mexe_nas_reservas_da_pessoa`, `::test_alteracoes_tem_limite_de_tentativas_por_usuario`; `pages/PaginaUsuarios.test.tsx` ("promover: confirma, chama a API com o perfil, mostra a mensagem e recarrega a lista") |
| **Código (complementar)** | `contas/application/casos_de_uso.py::AlterarUsuario`, `contas/domain/gestao.py::situacao_pedida`, `contas/api/views.py::UsuarioDetalheView`, `contas/api/limites.py::LimiteDeGestaoDeUsuariosPorUsuario`, `components/usuarios/DialogoDeUsuario.tsx::DialogoDeUsuario` |
| **Regras de negócio** | [RN-18](regras-de-negocio.md#rn-18), [RN-19](regras-de-negocio.md#rn-19). Glossário e detalhes: [Usuário ativo](../glossario.md#usuario-ativo), [perfil](../glossario.md#perfil), [sessão](../glossario.md#sessao), [tentativas em excesso](../glossario.md#tentativas-em-excesso) |
| **Decisões** | [DEC-27](../decisoes/DEC-27.md) (o perfil e a situação são lidos do banco a cada pedido e valem na próxima ação, com a mesma credencial) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-43-1"></a>RF-43.1 · Recusar que o Gestor rebaixe ou desative a própria conta

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o Gestor rebaixe o próprio perfil ou desative a própria conta, sem alterar o usuário e sem encerrar a sessão, e informar que outro Gestor deve fazer a alteração. |
| **Pai** | [RF-43](#rf-43) |
| **Origem** | NS-11 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Normal — um clique errado tiraria do Gestor o acesso que ele usa para desfazê-lo. |
| **Vínculos** | UC: [UC-23 Gerir usuários](../casos-de-uso/README.md#uc-23) (exceção) — na ficha: [UC-23 E6.5](../casos-de-uso/fichas-resumidas.md#uc23-e6-5), [UC-23 E6.6](../casos-de-uso/fichas-resumidas.md#uc23-e6-6) · US/CA: [US-22 · CA-06](../historias/US-22-gerir-usuarios.md#us-22-ca-06) (TA-206) |
| **Evidência (complementar)** | 403 `NAO_PODE_REBAIXAR_A_SI_MESMO` e `NAO_PODE_DESATIVAR_A_SI_MESMO`, nunca 401; na tela, as duas ações desabilitadas na linha do próprio Gestor, com a explicação em texto. `contas/tests/test_api_gestao_de_usuarios.py::test_gestor_nao_rebaixa_a_si_mesmo`, `::test_gestor_nao_desativa_a_si_mesmo`, `::test_unico_gestor_nao_se_rebaixa_nem_se_desativa`; `contas/tests/test_gestao_de_usuarios_dominio.py::test_o_proprio_ator_nao_se_rebaixa`; `pages/PaginaUsuarios.test.tsx` ("as ações do próprio usuário ficam desabilitadas, com a explicação em texto") |
| **Código (complementar)** | `contas/domain/gestao.py::garantir_alteracao_permitida`, `contas/domain/excecoes.py::NaoPodeRebaixarASiMesmo`, `contas/domain/excecoes.py::NaoPodeDesativarASiMesmo` |
| **Regras de negócio** | [RN-18](regras-de-negocio.md#rn-18). Glossário e detalhes: [Usuário ativo](../glossario.md#usuario-ativo), [perfil](../glossario.md#perfil) |
| **Decisões** | [DEC-27](../decisoes/DEC-27.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-43-2"></a>RF-43.2 · Recusar que o sistema fique sem Gestor ativo

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o Gestor rebaixe ou desative o último Gestor ativo, inclusive quando dois Gestores pedem ao mesmo tempo, sem alterar o usuário, e informar que antes é preciso promover ou reativar outro Gestor. |
| **Pai** | [RF-43](#rf-43) |
| **Origem** | NS-11 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — sem nenhum Gestor ativo, nenhum espaço é cadastrado e nenhum pedido é decidido, e só a Equipe de TI resolveria. |
| **Vínculos** | UC: [UC-23 Gerir usuários](../casos-de-uso/README.md#uc-23) (exceção) — na ficha: [UC-23 E6.7](../casos-de-uso/fichas-resumidas.md#uc23-e6-7) · US/CA: [US-22 · CA-07](../historias/US-22-gerir-usuarios.md#us-22-ca-07) (TA-207) |
| **Evidência (complementar)** | 409 `ULTIMO_GESTOR_ATIVO`; a contagem dos Gestores ativos é feita com as linhas travadas, e dois pedidos simultâneos deixam sempre um Gestor ativo. `contas/tests/test_gestao_de_usuarios_dominio.py::test_rebaixar_o_ultimo_gestor_ativo_e_recusado_mesmo_sendo_outra_pessoa`, `::test_desativar_o_ultimo_gestor_ativo_e_recusado`; `contas/tests/test_api_gestao_de_usuarios.py::test_ultimo_gestor_ativo_nao_e_rebaixado_nem_desativado_por_quem_ja_perdeu_o_perfil [x]`; `contas/tests/test_repositorio_gestao_de_usuarios.py::test_alterar_trava_o_alvo_e_os_gestores_ativos_em_ordem_de_id`; `contas/tests/test_concorrencia_de_gestao.py::test_dois_gestores_se_tirando_do_cargo_ao_mesmo_tempo_deixam_um_ativo [x]` |
| **Código (complementar)** | `contas/domain/gestao.py::garantir_alteracao_permitida`, `contas/domain/excecoes.py::UltimoGestorAtivo`, `contas/infrastructure/repositorio_django.py::RepositorioGestaoDeUsuariosDjango` |
| **Regras de negócio** | [RN-19](regras-de-negocio.md#rn-19). Glossário e detalhes: [Gestor](../glossario.md#gestor), [usuário ativo](../glossario.md#usuario-ativo) |
| **Decisões** | [DEC-27](../decisoes/DEC-27.md) (a trava das linhas dos Gestores ativos contra a corrida) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |
