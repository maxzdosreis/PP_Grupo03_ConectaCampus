# Contexto `contas` — usuários, perfis e autenticação

Guarda quem usa o sistema e com qual perfil, cadastra novos solicitantes e faz o login com token JWT. É um extra do projeto (DEC-04): as seis funcionalidades mínimas não dependem dele, mas todas as rotas de espaços e reservas exigem um usuário logado. Organização em camadas e regra de dependência: [README do backend](../README.md#organização).

## Perfis

| Perfil (`PerfilUsuario`) | Como nasce | O que pode a mais |
|---|---|---|
| `SOLICITANTE` (padrão) | `POST /api/auth/cadastro/` | Solicita reservas e cancela as próprias. |
| `GESTOR` | só por `createsuperuser` ([como](../README.md#criar-um-superusuário-acesso-ao-admin)), pelo admin ou pelos [dados de exemplo](../exemplos/README.md) | Cadastra e gerencia espaços, vê todas as reservas e muda a situação de qualquer uma. |

`PerfilUsuario.eh_gestor` (`contas/domain/perfil.py`) é a única definição de "é gestor". Os outros contextos não importam `contas`: leem do usuário autenticado só `pk`, `nome`, `matricula` e `eh_gestor`. O perfil é lido do banco a cada requisição, então rebaixar ou promover alguém vale na hora, com o mesmo token.

## Regras

- **Usuário** (`contas.Usuario`, o `AUTH_USER_MODEL`): `nome`, `matricula` (única), `email` (único sem diferenciar maiúsculas de minúsculas), `perfil` e a senha guardada só com o hash do Django. O login é pelo e-mail, gravado em minúsculas e sem espaços.
- **Dados do cadastro** (`DadosDeCadastro`, `contas/domain/cadastro.py`), validados nesta ordem: nome obrigatório e com até `NOME_MAXIMO_CARACTERES` (150), sem espaços nas pontas nem repetidos (`normalizar_nome`); matrícula obrigatória, com até `MATRICULA_MAXIMO_CARACTERES` (20) e sem espaços; e-mail obrigatório (`normalizar_email`). O formato do e-mail é validado pelo serializer.
- **Formato da matrícula:** por enquanto só "até 20 caracteres, sem espaços"; o padrão real da Unilasalle está pendente (DEC-09). Muda só `_validar_matricula` e `MatriculaInvalida`.
- **Senha** (`PoliticaDeSenha`, implementada por `PoliticaDeSenhaDjango` com os validadores do Django): pelo menos 8 caracteres, não pode ser comum, só números nem parecida com o e-mail, o nome ou a matrícula. Uma senha só com espaços conta como vazia.
- **Caso de uso** `CadastrarSolicitante`: valida os dados, a senha, depois confere e-mail e matrícula repetidos e só então cria. Dados inválidos são recusados antes de qualquer consulta ao banco. O banco também garante a unicidade, e o repositório traduz a violação para as mesmas exceções.
- O cadastro público cria sempre um `SOLICITANTE`: `perfil`, `is_staff` ou `is_superuser` enviados no corpo são ignorados. O cadastro não faz login; o frontend chama o login logo depois.
- **Login:** senha errada, e-mail inexistente e usuário desativado dão a mesma resposta (`CREDENCIAIS_INVALIDAS`), para não revelar quais e-mails existem. Usuário desativado ou excluído também perde o `access` e o `refresh` que já tinha (401).
- **Limite de tentativas** (AUT-08, `api/limites.py`): ver [Limite de tentativas](#limite-de-tentativas).

## Endpoints

Conferidos com `config/tests/test_matriz_de_acesso.py`.

| Método e caminho | Quem pode | Sucesso | Erros principais |
|---|---|---|---|
| `POST /api/auth/cadastro/` | público | 201 | 400 `CAMPO_OBRIGATORIO_AUSENTE`, `TEXTO_MUITO_LONGO`, `MATRICULA_INVALIDA`, `SENHA_FRACA`, `DADOS_INVALIDOS`; 409 `EMAIL_JA_CADASTRADO`, `MATRICULA_JA_CADASTRADA`; 429 `LIMITE_DE_TENTATIVAS`; 503 `SERVICO_INDISPONIVEL` (Redis fora do ar) |
| `POST /api/auth/login/` | público | 200 | 401 `CREDENCIAIS_INVALIDAS`; 400 `DADOS_INVALIDOS`; 429 `LIMITE_DE_TENTATIVAS`; 503 `SERVICO_INDISPONIVEL` (Redis fora do ar) |
| `POST /api/auth/refresh/` | público, com o `refresh` | 200 | 401 `NAO_AUTENTICADO` (inválido, expirado, de usuário inativo ou excluído); 400 `DADOS_INVALIDOS` sem `refresh` |
| `GET /api/auth/me/` | logado | 200 | 401 `NAO_AUTENTICADO` |

Os exemplos de login, de guardar o `access` e de renovar o token estão em [Autenticação JWT](../README.md#autenticação-jwt), porque todos os contextos usam o mesmo token.

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
| Rotas, login, refresh e `me` | `api/views.py`, `api/serializers.py`, `api/urls.py` |
| Limites de tentativas | `api/limites.py` e `LIMITE_*`, `NUM_PROXIES` e `CACHES` no `config/settings.py` |
| Admin do Django | `admin.py` |

Testes em `contas/tests/`: domínio sem banco, `CadastrarSolicitante` com os fakes de `fakes.py`, o contrato do repositório (contra o Django e o fake) e a API (`test_api_cadastro.py`, `test_api_autenticacao.py`, com os casos de token adulterado, expirado e de usuário desativado).
