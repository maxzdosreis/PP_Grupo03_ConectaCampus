# Contexto `contas` — usuários, perfis e autenticação

Guarda quem usa o sistema e com qual perfil, cadastra novos solicitantes e faz o login com token JWT. É um extra do projeto (DEC-04): as seis funcionalidades mínimas não dependem dele, mas todas as rotas de espaços e reservas exigem um usuário logado. Organização em camadas e regra de dependência: [README do backend](../README.md#organização).

## Perfis

| Perfil (`PerfilUsuario`) | Como nasce | O que pode a mais |
|---|---|---|
| `SOLICITANTE` (padrão) | `POST /api/auth/cadastro/` | Solicita reservas e cancela as próprias. |
| `GESTOR` | `createsuperuser`, o admin, os dados de exemplo ou a [promoção por outro Gestor](#gestão-de-usuários) (a criação do primeiro Gestor continua por `createsuperuser` ([como](../README.md#criar-um-superusuário-acesso-ao-admin)) ou pelos [dados de exemplo](../exemplos/README.md)) | Cadastra e gerencia espaços, vê todas as reservas e muda a situação de qualquer uma. |

`PerfilUsuario.eh_gestor` (`contas/domain/perfil.py`) é a única definição de "é gestor". Os outros contextos não importam `contas`: leem do usuário autenticado só `pk`, `nome`, `matricula` e `eh_gestor`. O perfil é lido do banco a cada requisição, então rebaixar ou promover alguém vale na hora, com o mesmo token.

## Regras

- **Usuário** (`contas.Usuario`, o `AUTH_USER_MODEL`): `nome`, `matricula` (única), `email` (único sem diferenciar maiúsculas de minúsculas), `perfil` e a senha guardada só com o hash do Django. O login é pelo e-mail, gravado em minúsculas e sem espaços.
- **Dados do cadastro** (`DadosDeCadastro`, `contas/domain/cadastro.py`), validados nesta ordem: nome obrigatório e com até `NOME_MAXIMO_CARACTERES` (150), sem espaços nas pontas nem repetidos (`normalizar_nome`); matrícula obrigatória, com até `MATRICULA_MAXIMO_CARACTERES` (20) e sem espaços; e-mail obrigatório (`normalizar_email`). O formato do e-mail é validado pelo serializer.
- **Formato da matrícula:** por enquanto só "até 20 caracteres, sem espaços"; o padrão real da Unilasalle está pendente (DEC-09). Muda só `_validar_matricula` e `MatriculaInvalida`.
- **Senha** (`PoliticaDeSenha`, implementada por `PoliticaDeSenhaDjango` com os validadores do Django): pelo menos 8 caracteres, não pode ser comum, só números nem parecida com o e-mail, o nome ou a matrícula. Uma senha só com espaços conta como vazia.
- **Caso de uso** `CadastrarSolicitante`: valida os dados, a senha, depois confere e-mail e matrícula repetidos e só então cria. Dados inválidos são recusados antes de qualquer consulta ao banco. O banco também garante a unicidade, e o repositório traduz a violação para as mesmas exceções.
- O cadastro público cria sempre um `SOLICITANTE`: `perfil`, `is_staff` ou `is_superuser` enviados no corpo são ignorados. O cadastro não faz login; o frontend chama o login logo depois.
- **Login:** senha errada, e-mail inexistente e usuário desativado dão a mesma resposta (`CREDENCIAIS_INVALIDAS`), para não revelar quais e-mails existem. Usuário desativado ou excluído também perde o `access` e o `refresh` que já tinha (401).
- **Sessão (AUT-09):** o `refresh` é de uso único. A renovação devolve um `access` e um `refresh` novos e revoga o usado, na mesma transação (`_trocar_refresh`); o novo mantém o vencimento do primeiro, 1 dia depois do login. Reusar um `refresh` já trocado dá 401, e duas renovações simultâneas com o mesmo `refresh` dão uma 200 e uma 401. Sair (`SairView`) revoga o `refresh`. O `access` não é revogado e vale até expirar (30 minutos), porque não há lista negra de `access` e conferi-la custaria uma consulta em cada pedido.
- **Limite de tentativas** (AUT-08, `api/limites.py`): ver [Limite de tentativas](#limite-de-tentativas).

## Endpoints

Conferidos com `config/tests/test_matriz_de_acesso.py`.

| Método e caminho | Quem pode | Sucesso | Erros principais |
|---|---|---|---|
| `POST /api/auth/cadastro/` | público | 201 | 400 `CAMPO_OBRIGATORIO_AUSENTE`, `TEXTO_MUITO_LONGO`, `MATRICULA_INVALIDA`, `SENHA_FRACA`, `DADOS_INVALIDOS`; 409 `EMAIL_JA_CADASTRADO`, `MATRICULA_JA_CADASTRADA`; 429 `LIMITE_DE_TENTATIVAS`; 503 `SERVICO_INDISPONIVEL` (Redis fora do ar) |
| `POST /api/auth/login/` | público | 200 | 401 `CREDENCIAIS_INVALIDAS`; 400 `DADOS_INVALIDOS`; 429 `LIMITE_DE_TENTATIVAS`; 503 `SERVICO_INDISPONIVEL` (Redis fora do ar) |
| `POST /api/auth/refresh/` | público, com o `refresh` | 200 com `access` e `refresh` novos | 401 `NAO_AUTENTICADO` (inválido, expirado, revogado, já usado, de usuário inativo ou excluído); 400 `DADOS_INVALIDOS` sem `refresh` |
| `POST /api/auth/logout/` | público, com o `refresh` | 200 (também com o `refresh` já revogado ou vencido) | 400 `DADOS_INVALIDOS` sem `refresh` ou com um texto que não é `refresh` (com `campos.refresh`) |
| `GET /api/auth/me/` | logado | 200 | 401 `NAO_AUTENTICADO` |
| `GET /api/usuarios/` | só Gestor | 200, em páginas | 400 `DADOS_INVALIDOS` (`pagina`, `tamanho`, `perfil`, `ativo`); 401 `NAO_AUTENTICADO`; 403 `ACAO_NAO_PERMITIDA` |
| `PATCH /api/usuarios/{id}/` | só Gestor | 200 `Usuário atualizado.` ou `Nenhuma mudança: o usuário já estava assim.` | 400 `PERFIL_INVALIDO`, `NENHUMA_ALTERACAO_INFORMADA`, `DADOS_INVALIDOS`; 401; 403 `ACAO_NAO_PERMITIDA`, `NAO_PODE_REBAIXAR_A_SI_MESMO`, `NAO_PODE_DESATIVAR_A_SI_MESMO`; 404 `USUARIO_NAO_ENCONTRADO`; 409 `ULTIMO_GESTOR_ATIVO`; 429 `LIMITE_DE_TENTATIVAS` |
| `POST /api/auth/senha/` | logado, qualquer perfil (só a própria senha) | 200 `Senha alterada com sucesso.` | 400 `SENHA_ATUAL_INCORRETA` (campo `senha_atual`, **nunca 401**), `NOVA_SENHA_IGUAL_A_ATUAL`, `SENHA_FRACA` (campo `nova_senha`), `CAMPO_OBRIGATORIO_AUSENTE`, `DADOS_INVALIDOS`; 401 `NAO_AUTENTICADO` (sem login); 429 `LIMITE_DE_TENTATIVAS`; 503 `SERVICO_INDISPONIVEL` (Redis fora do ar) |

Os exemplos de login, de guardar o `access` e de renovar o token estão em [Autenticação JWT](../README.md#autenticação-jwt), porque todos os contextos usam o mesmo token.

## Renovar o token

`POST /api/auth/refresh/` troca o `refresh`: guarde o novo, porque o enviado deixa de valer.

```bash
curl -X POST http://localhost:8000/api/auth/refresh/ -H "Content-Type: application/json" -d '{"refresh": "cole-aqui-o-refresh"}'
```

```json
{"mensagem": "Token renovado.", "dados": {"access": "eyJhbGciOi...", "refresh": "eyJhbGciOi..."}}
```

Repetir o mesmo comando com o `refresh` antigo responde **401**:

```json
{"erro": {"codigo": "NAO_AUTENTICADO", "mensagem": "Faça login para continuar."}}
```

## Sair (logout)

`POST /api/auth/logout/` revoga o `refresh` no servidor. É público, porque a posse do `refresh` é a credencial e o `access` pode já ter vencido quando a pessoa sai; um `refresh` de outra pessoa é revogado do mesmo jeito, e a resposta não traz nada dela. Não tem limite de tentativas.

```bash
curl -X POST http://localhost:8000/api/auth/logout/ -H "Content-Type: application/json" -d '{"refresh": "cole-aqui-o-refresh"}'
```

```json
{"mensagem": "Você saiu da sua conta.", "dados": null}
```

- Sair é idempotente: o mesmo `refresh` de novo, ou um já vencido, também responde **200**.
- Sem `refresh`, ou com um texto que não é um `refresh` (formato ou assinatura inválidos, ou um `access`), responde **400** `DADOS_INVALIDOS` com `campos.refresh` ("Informe um token de renovação válido.").
- O `access` emitido antes continua valendo até expirar (30 minutos).

## Cadastrar um solicitante

Primeiro cadastre um usuário (`POST /api/auth/cadastro/`, público). O cadastro cria sempre um **Solicitante**: `perfil`, `is_staff` ou `is_superuser` enviados no corpo são ignorados. Um Gestor só nasce pelo `createsuperuser` (veja a [seção do backend](../README.md#criar-um-superusuário-acesso-ao-admin)) ou pelo admin. A senha precisa ter pelo menos 8 caracteres, não pode ser comum, só números nem parecida com o e-mail, o nome ou a matrícula. A matrícula tem até 20 caracteres, sem espaços.

```bash
curl -X POST http://localhost:8000/api/auth/cadastro/ -H "Content-Type: application/json" -d '{"nome": "Ana Souza", "matricula": "2026001", "email": "ana@exemplo.com", "senha": "senha-de-teste-123"}'
```

No Prompt de Comando do Windows:

```bat
curl -X POST http://localhost:8000/api/auth/cadastro/ -H "Content-Type: application/json" -d "{\"nome\": \"Ana Souza\", \"matricula\": \"2026001\", \"email\": \"ana@exemplo.com\", \"senha\": \"senha-de-teste-123\"}"
```

Resposta **201** (o cadastro não faz login nem devolve tokens):

```json
{"mensagem": "Cadastro realizado com sucesso. Faça login para continuar.", "dados": {"id": 1, "nome": "Ana Souza", "email": "ana@exemplo.com", "matricula": "2026001", "perfil": "SOLICITANTE", "perfil_rotulo": "Solicitante", "eh_gestor": false}}
```

Cadastrar de novo o mesmo e-mail (mesmo em outra caixa, como `ANA@exemplo.com`) responde **409**:

```json
{"erro": {"codigo": "EMAIL_JA_CADASTRADO", "mensagem": "Já existe um usuário com este e-mail.", "campos": {"email": ["Já existe um usuário com este e-mail."]}}}
```

Outros erros de cadastro: matrícula repetida → **409** `MATRICULA_JA_CADASTRADA`; senha `12345678` → **400** `SENHA_FRACA` ("Esta senha é muito comum. Esta senha é inteiramente numérica."); matrícula com espaço ou com mais de 20 caracteres → **400** `MATRICULA_INVALIDA`; e-mail malformado → **400** `DADOS_INVALIDOS`; nome em branco → **400** `CAMPO_OBRIGATORIO_AUSENTE`.

Com a conta criada, [entre e guarde o token](../README.md#entrar-login-e-usar-o-token).

### Erros do login

E-mail ou senha errados (ou usuário desativado) respondem sempre igual, **401**:

```json
{"erro": {"codigo": "CREDENCIAIS_INVALIDAS", "mensagem": "E-mail ou senha incorretos."}}
```

## Trocar a própria senha

`POST /api/auth/senha/` (AUT-10, [DEC-26](../../../README.md#limitações-conhecidas)). Exige login, vale para os dois perfis e troca **só a senha de quem está logado**: a conta vem do token, e um `id` ou e-mail no corpo é ignorado. Corpo: `senha_atual`, `nova_senha` e, opcional, `refresh_atual` (o `refresh` da sessão que fez a troca).

```bash
curl -X POST http://localhost:8000/api/auth/senha/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"senha_atual": "...", "nova_senha": "...", "refresh_atual": "'$REFRESH'"}'
```

- **Ordem das conferências:** limite de tentativas → campos informados → senha atual (`SENHA_ATUAL_INCORRETA`) → nova diferente da atual (`NOVA_SENHA_IGUAL_A_ATUAL`) → mesma política de senha do cadastro (`SENHA_FRACA`, com `PoliticaDeSenhaDjango`). A senha atual vem antes da política: quem não prova a atual não aprende nada sobre a política.
- **Senha atual errada é 400, nunca 401:** um 401 faria o navegador tentar renovar o token ou encerrar a sessão, e a pessoa seria deslogada por errar a senha.
- **Limite de tentativas:** 5 por minuto **por conta** (`LIMITE_TROCA_DE_SENHA_POR_USUARIO`), contado no Redis como o login; por conta e não por IP, porque no Docker todos chegam do mesmo IP. Estourado: 429 `LIMITE_DE_TENTATIVAS`.
- **Sessões:** a API revoga o refresh token das **outras** sessões da conta (lista negra do Simple JWT, AUT-09) e mantém o do `refresh_atual`; sem `refresh_atual`, revoga todos. Um `refresh_atual` inválido, ou de outra pessoa, é 400 `DADOS_INVALIDOS` (`campos.refresh_atual`) e nada é trocado. Os **tokens de acesso (JWT) não são revogáveis**: o já emitido em outro aparelho vale até expirar (30 minutos).
- **Nada de senha em resposta, exceção ou log.** A senha só é guardada como hash.
- **Onde fica:** caso de uso `AlterarSenha` (`application/casos_de_uso.py`), exceções `SenhaAtualIncorreta` e `NovaSenhaIgualAAtual` (`domain/excecoes.py`), `AlterarSenhaView` (`api/views.py`) e `LimiteDeTrocaDeSenhaPorUsuario` (`api/limites.py`).

## Gestão de usuários

AUT-11 ([DEC-27](../../../docs/fontes/requisitos/decisoes/DEC-27.md)). Só o Gestor lista os usuários e altera o **perfil** e a **situação da conta** (`is_active`) de outra pessoa. Não há exclusão nem criação de usuário por aqui, e a resposta nunca traz senha, hash nem token.

**Listar:** `GET /api/usuarios/?busca=&perfil=&ativo=&pagina=&tamanho=`, no mesmo padrão da consulta de reservas: `busca` (trecho do nome, do e-mail ou da matrícula, sem diferenciar caixa), `perfil` (`SOLICITANTE` ou `GESTOR`), `ativo` (`true` ou `false`), `pagina` (a partir de 1) e `tamanho` (padrão 20, até 100). Responde 200 com `dados` (a lista, em ordem de nome e depois de id) e `paginacao` (`pagina`, `tamanho`, `total`, `total_de_paginas`) ao lado; uma página depois da última é 200 com `dados` vazio. Cada usuário traz `id`, `nome`, `email`, `matricula`, `perfil`, `perfil_rotulo`, `eh_gestor`, `ativo`, `cadastrado_em` e `ultimo_acesso`.

```bash
curl "http://localhost:8000/api/usuarios/?perfil=SOLICITANTE&ativo=true" -H "Authorization: Bearer $ACCESS"
```

**Alterar:** `PATCH /api/usuarios/{id}/` com `perfil` e/ou `ativo` (ao menos um). É **idempotente**: pedir o estado em que a pessoa já está responde 200 sem gravar.

```bash
curl -X PATCH http://localhost:8000/api/usuarios/2/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"ativo": false}'
```

- **Ordem das conferências:** limite de tentativas (429) → login e perfil Gestor (401 e 403) → formato do pedido (`PERFIL_INVALIDO`, `DADOS_INVALIDOS`; depois `NENHUMA_ALTERACAO_INFORMADA`) → usuário existe (404) → mudança efetiva (senão, 200 sem gravar) → o próprio Gestor não rebaixa (`NAO_PODE_REBAIXAR_A_SI_MESMO`) nem desativa (`NAO_PODE_DESATIVAR_A_SI_MESMO`) a si, ambas 403 → o último Gestor ativo não é rebaixado nem desativado (`ULTIMO_GESTOR_ATIVO`, 409). Promover e reativar são sempre permitidos. Nenhuma recusa de regra é 401: o frontend renovaria ou encerraria a sessão.
- **Corrida:** `RepositorioGestaoDeUsuariosDjango.alterar_sob_trava` roda numa transação que trava, em ordem de id, o usuário e todos os Gestores ativos antes de contá-los (`select_for_update`); o domínio (`garantir_alteracao_permitida`) recebe a contagem já travada. Dois Gestores que se rebaixam ao mesmo tempo: só o primeiro vale. Prova: `test_concorrencia_de_gestao.py` (duas conexões de verdade, mais uma contraprova sem a trava).
- **Sessão e perfil:** o perfil e `is_active` são lidos do banco a cada pedido. Quem é rebaixado perde os poderes na próxima ação, com a mesma credencial; quem é desativado não entra (a mesma resposta de credenciais inválidas), e o access e o refresh que tinha deixam de valer. Reativar devolve o acesso, sem restaurar nada.
- **Reservas:** nada acontece com as reservas de quem é desativado ou rebaixado; o Gestor cancela ou recusa pelas regras de sempre.
- **Limite:** 30 alterações por minuto por conta (`LIMITE_GESTAO_DE_USUARIOS_POR_USUARIO`), como a troca de senha.
- **Onde fica:** regras em `domain/gestao.py` e `domain/excecoes.py`; casos de uso `ListarUsuarios` e `AlterarUsuario`; a porta `RepositorioGestaoDeUsuarios` e o DTO `UsuarioGerenciado` em `application/portas.py`; `RepositorioGestaoDeUsuariosDjango`; `UsuariosView` e `UsuarioDetalheView` em `api/views.py`; as rotas em `api/urls_usuarios.py`, montadas em `/api/usuarios/`. A paginação é a de `compartilhado/domain/paginacao.py` e `compartilhado/api/paginacao.py`.

## Limite de tentativas

Para ninguém adivinhar uma senha repetindo o login, o login e o cadastro têm limite de tentativas (throttles do DRF em `api/limites.py`, AUT-08):

| Onde | Chave | Padrão | Variável |
|---|---|---|---|
| Login | e-mail do corpo, normalizado como no login (minúsculas, sem espaços nas pontas) | 5 por minuto | `LIMITE_LOGIN_POR_EMAIL` |
| Login | IP da conexão | 20 por minuto | `LIMITE_LOGIN_POR_IP` |
| Cadastro | IP da conexão | 10 por hora | `LIMITE_CADASTRO_POR_IP` |

- **Toda tentativa conta**, com acerto ou erro, numa janela deslizante, inclusive as simultâneas. A contagem é um script Lua no Redis (`_REGISTRAR_TENTATIVA`), que limpa as tentativas que saíram da janela, conta, decide e registra numa só operação, sobre um sorted set por chave. O get/set do `SimpleRateThrottle` do DRF não é usado: em operações separadas, tentativas ao mesmo tempo liam o mesmo total e passavam juntas (achado da revisão do PR; `test_tentativas_simultaneas_nao_passam_do_limite` dispara 30 de uma vez e só 5 passam). Acima do limite, a resposta é **429** `LIMITE_DE_TENTATIVAS` com o tempo de espera na mensagem e no cabeçalho `Retry-After`, sem dizer qual limite foi atingido nem se o e-mail existe (a mesma regra das credenciais inválidas). A tentativa recusada não conta.
- **O limite vem antes de tudo:** o DRF confere os throttles antes da validação do corpo e da senha. Depois de excedido, até a senha certa é recusada até o tempo passar.
- **Por e-mail e por IP:** o por e-mail protege uma conta; o por IP pega quem testa muitos e-mails e é mais folgado, porque no Docker todos os acessos do computador chegam com o mesmo IP. Sem um e-mail válido no corpo, vale só o por IP (um corpo que não é JSON continua 400 `JSON_INVALIDO` e conta no por IP).
- **IP confiável:** `REST_FRAMEWORK["NUM_PROXIES"] = 0` faz o DRF usar o `REMOTE_ADDR` e ignorar o `X-Forwarded-For`, que o próprio cliente escreve. Atrás de um proxy, esse valor teria de mudar.
- **A renovação do token não tem limite:** o `refresh` é assinado, não há o que adivinhar.
- **As taxas são lidas das settings a cada requisição** (`LimiteDeTentativas.get_rate`), e não da constante de classe do DRF, lida uma vez só na importação; assim `override_settings` funciona nos testes. Um valor fora do formato `N/s|min|hour|day` impede o backend de subir.
- **Contador no Redis** (`CACHES` com o `RedisCache` do Django, serviço `redis` do Compose): vale para todos os processos do backend e não zera ao reiniciar o backend. O Redis roda sem persistência, então a contagem zera quando ele reinicia (limitação no [README da raiz](../../../README.md#limitações-conhecidas)).
- **Redis fora do ar → 503:** `LimiteDeTentativas.allow_request` transforma o `RedisError` em `ServicoIndisponivel`, e login e cadastro respondem **503** `SERVICO_INDISPONIVEL` ("Serviço temporariamente indisponível. Tente de novo em alguns instantes.") antes de conferir qualquer dado: nenhuma tentativa passa sem contagem. Os timeouts do Redis são de 1 s, para a recusa ser rápida.

Seis tentativas seguidas com senha errada:

```bash
for i in 1 2 3 4 5 6; do
  curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8000/api/auth/login/ \
    -H "Content-Type: application/json" -d '{"email": "ana@exemplo.com", "senha": "errada"}'
done
```

As cinco primeiras respondem `401` e a sexta, `429`. A próxima, mesmo com a senha certa, também:

```bash
curl -i -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" -d '{"email": "ana@exemplo.com", "senha": "senha-de-teste-123"}'
```

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 57
```

```json
{"erro": {"codigo": "LIMITE_DE_TENTATIVAS", "mensagem": "Muitas tentativas. Tente de novo em 57 segundos."}}
```

## Ver o usuário logado

Ver o usuário logado (`GET /api/auth/me/`):

```bash
curl http://localhost:8000/api/auth/me/ -H "Authorization: Bearer $ACCESS"
```

```json
{"mensagem": "Usuário autenticado.", "dados": {"id": 1, "nome": "Ana Souza", "email": "ana@exemplo.com", "matricula": "2026001", "perfil": "SOLICITANTE", "perfil_rotulo": "Solicitante", "eh_gestor": false}}
```

Sem token, com token malformado ou expirado → **401** `NAO_AUTENTICADO`.

## Onde mexer

| Para mudar… | Arquivo |
|---|---|
| Perfis | `domain/perfil.py` |
| Regras de nome, matrícula e e-mail, e os limites | `domain/cadastro.py` (e `domain/excecoes.py` para as mensagens) |
| Ordem do cadastro | `application/casos_de_uso.py` (`CadastrarSolicitante`) |
| Política de senha | `infrastructure/politica_de_senha.py` e `AUTH_PASSWORD_VALIDATORS` no `config/settings.py` |
| Model, manager e unicidade | `infrastructure/models.py` e `infrastructure/repositorio_django.py` |
| Rotas, login, refresh (com a troca do `refresh`), logout e `me` | `api/views.py`, `api/serializers.py`, `api/urls.py` |
| Gestão de usuários (regras, ordem e trava) | `domain/gestao.py`, `application/casos_de_uso.py` (`AlterarUsuario`), `infrastructure/repositorio_django.py` (`alterar_sob_trava`), `api/urls_usuarios.py` |
| Limites de tentativas | `api/limites.py` e `LIMITE_*`, `NUM_PROXIES` e `CACHES` no `config/settings.py` |
| Admin do Django | `admin.py` |

Testes em `contas/tests/`: domínio sem banco, `CadastrarSolicitante` com os fakes de `fakes.py`, o contrato do repositório (contra o Django e o fake) e a API (`test_api_cadastro.py`, `test_api_autenticacao.py`, com os casos de token adulterado, expirado e de usuário desativado).
