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

## Endpoints

Conferidos com `config/tests/test_matriz_de_acesso.py`.

| Método e caminho | Quem pode | Sucesso | Erros principais |
|---|---|---|---|
| `POST /api/auth/cadastro/` | público | 201 | 400 `CAMPO_OBRIGATORIO_AUSENTE`, `TEXTO_MUITO_LONGO`, `MATRICULA_INVALIDA`, `SENHA_FRACA`, `DADOS_INVALIDOS`; 409 `EMAIL_JA_CADASTRADO`, `MATRICULA_JA_CADASTRADA` |
| `POST /api/auth/login/` | público | 200 | 401 `CREDENCIAIS_INVALIDAS`; 400 `DADOS_INVALIDOS` |
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
| Admin do Django | `admin.py` |

Testes em `contas/tests/`: domínio sem banco, `CadastrarSolicitante` com os fakes de `fakes.py`, o contrato do repositório (contra o Django e o fake) e a API (`test_api_cadastro.py`, `test_api_autenticacao.py`, com os casos de token adulterado, expirado e de usuário desativado).
