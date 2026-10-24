# Conecta Campus — Reserva de Quadras e Espaços Esportivos

Sistema para a comunidade acadêmica cadastrar quadras e espaços esportivos, solicitar reservas e acompanhar a situação de cada reserva.

## Tecnologias

- Python 3.12, Django 5.2 LTS, Django REST Framework 3.18, Simple JWT 5.5 (login com token)
- PostgreSQL 16 (driver psycopg 3)
- Node 24, React 19.3, TypeScript 6.0, Vite 8.3, React Router 8.4, ESLint 10
- Docker e Docker Compose

## Como executar

### Pré-requisito

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (inclui o Docker Compose).

### Passo a passo

1. Na raiz do repositório, crie o arquivo de variáveis de ambiente a partir do exemplo:

   ```bash
   cp src/.env.example src/.env
   ```

   No Prompt de Comando do Windows:

   ```bat
   copy src\.env.example src\.env
   ```

   Se já existir um PostgreSQL rodando na porta 5432 do seu computador, mude só `DB_PORT_HOST` (ex.: `5433`). `DB_PORT` é a porta usada pelo Django dentro da rede do Docker e deve continuar `5432`.

2. Entre na pasta `src` e suba os três serviços (banco, backend e frontend):

   ```bash
   cd src
   docker compose up --build
   ```

   As migrations do banco são aplicadas automaticamente quando o backend sobe.

3. Acesse:
   - Aplicação (frontend): http://localhost:5173 — a página inicial mostra a situação da API ("API no ar.")
   - API: http://localhost:8000
   - Saúde da API: http://localhost:8000/api/health/
   - Admin do Django: http://localhost:8000/admin/

### Verificar se a API está no ar

`GET /api/health/` testa a conexão com o banco:

- **200** — `{"mensagem": "API no ar.", "dados": {"banco": "ok"}}`
- **503** — `{"erro": {"codigo": "BANCO_INDISPONIVEL", "mensagem": "Não foi possível conectar ao banco de dados."}}`

### Exemplos de uso da API

Por enquanto os endpoints de espaços não exigem login; a restrição do cadastro ao perfil Gestor entra na AUT-05. Toda resposta segue o mesmo formato: `{"mensagem", "dados"}` no sucesso e `{"erro": {"codigo", "mensagem", "campos"?}}` no erro.

Tipos aceitos em `tipo`: `QUADRA_POLIESPORTIVA`, `CAMPO_DE_FUTEBOL`, `GINASIO`, `QUADRA_DE_AREIA`, `QUADRA_DE_TENIS`.

Cadastrar um espaço (`POST /api/espacos/`):

```bash
curl -X POST http://localhost:8000/api/espacos/ -H "Content-Type: application/json" -d '{"nome": "Quadra Central", "tipo": "QUADRA_POLIESPORTIVA", "capacidade": 20}'
```

No Prompt de Comando do Windows, as aspas internas são escapadas:

```bat
curl -X POST http://localhost:8000/api/espacos/ -H "Content-Type: application/json" -d "{\"nome\": \"Quadra Central\", \"tipo\": \"QUADRA_POLIESPORTIVA\", \"capacidade\": 20}"
```

Resposta **201**:

```json
{"mensagem": "Espaço cadastrado com sucesso.", "dados": {"id": 1, "nome": "Quadra Central", "tipo": "QUADRA_POLIESPORTIVA", "tipo_rotulo": "Quadra poliesportiva", "capacidade": 20, "ativo": true}}
```

Repetir o mesmo cadastro responde **409**:

```json
{"erro": {"codigo": "NOME_DE_ESPACO_JA_CADASTRADO", "mensagem": "Já existe um espaço com este nome.", "campos": {"nome": ["Já existe um espaço com este nome."]}}}
```

Outros erros de cadastro: capacidade `0` → **400** `CAPACIDADE_INVALIDA`; tipo fora da lista → **400** `TIPO_DE_ESPACO_INVALIDO`; nome vazio → **400** `CAMPO_OBRIGATORIO_AUSENTE`.

> No Windows, nomes com acento passados direto no `-d` podem chegar fora de UTF-8 e a API responde `JSON_INVALIDO`. Nesse caso, salve o corpo num arquivo UTF-8 e envie com `--data-binary @espaco.json`.

Listar os espaços (`GET /api/espacos/`), ordenados por nome. Filtros opcionais: `apenas_ativos=true` e `tipo=<TIPO>`, combináveis:

```bash
curl "http://localhost:8000/api/espacos/?tipo=QUADRA_POLIESPORTIVA&apenas_ativos=true"
```

```json
{"mensagem": "1 espaço encontrado.", "dados": [{"id": 1, "nome": "Quadra Central", "tipo": "QUADRA_POLIESPORTIVA", "tipo_rotulo": "Quadra poliesportiva", "capacidade": 20, "ativo": true}]}
```

Obter um espaço (`GET /api/espacos/{id}/`):

```bash
curl http://localhost:8000/api/espacos/1/
```

Um id inexistente responde **404**:

```json
{"erro": {"codigo": "ESPACO_NAO_ENCONTRADO", "mensagem": "Espaço de código 9999 não encontrado."}}
```

#### Entrar (login) e usar o token

As reservas exigem login com token JWT. O login devolve dois tokens: o `access`, enviado em cada pedido no cabeçalho `Authorization: Bearer <access>` e válido por 30 minutos, e o `refresh`, que gera um `access` novo e vale 1 dia (os dois prazos mudam em `JWT_ACCESS_MINUTES` e `JWT_REFRESH_DAYS` no `.env`).

Primeiro cadastre um usuário (`POST /api/auth/cadastro/`, público). O cadastro cria sempre um **Solicitante**: `perfil`, `is_staff` ou `is_superuser` enviados no corpo são ignorados. Um Gestor só nasce pelo `createsuperuser` (veja a seção abaixo) ou pelo admin. A senha precisa ter pelo menos 8 caracteres, não pode ser comum, só números nem parecida com o e-mail, o nome ou a matrícula. A matrícula tem até 20 caracteres, sem espaços.

```bash
curl -X POST http://localhost:8000/api/auth/cadastro/ -H "Content-Type: application/json" -d '{"nome": "Ana Souza", "matricula": "2026001", "email": "ana@exemplo.com", "senha": "senha-de-teste-123"}'
```

No Prompt de Comando do Windows:

```bat
curl -X POST http://localhost:8000/api/auth/cadastro/ -H "Content-Type: application/json" -d "{\"nome\": \"Ana Souza\", \"matricula\": \"2026001\", \"email\": \"ana@exemplo.com\", \"senha\": \"senha-de-teste-123\"}"
```

Resposta **201** (o cadastro não faz login nem devolve tokens):

```json
{"mensagem": "Cadastro realizado com sucesso. Faça login para continuar.", "dados": {"id": 1, "nome": "Ana Souza", "email": "ana@exemplo.com", "matricula": "2026001", "perfil": "SOLICITANTE", "perfil_rotulo": "Solicitante"}}
```

Cadastrar de novo o mesmo e-mail (mesmo em outra caixa, como `ANA@exemplo.com`) responde **409**:

```json
{"erro": {"codigo": "EMAIL_JA_CADASTRADO", "mensagem": "Já existe um usuário com este e-mail.", "campos": {"email": ["Já existe um usuário com este e-mail."]}}}
```

Outros erros de cadastro: matrícula repetida → **409** `MATRICULA_JA_CADASTRADA`; senha `12345678` → **400** `SENHA_FRACA` ("Esta senha é muito comum. Esta senha é inteiramente numérica."); matrícula com espaço ou com mais de 20 caracteres → **400** `MATRICULA_INVALIDA`; e-mail malformado → **400** `DADOS_INVALIDOS`; nome em branco → **400** `CAMPO_OBRIGATORIO_AUSENTE`.

Entrar (`POST /api/auth/login/`) com `email` e `senha`:

```bash
curl -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" -d '{"email": "ana@exemplo.com", "senha": "senha-de-teste-123"}'
```

No Prompt de Comando do Windows:

```bat
curl -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" -d "{\"email\": \"ana@exemplo.com\", \"senha\": \"senha-de-teste-123\"}"
```

Resposta **200** (tokens encurtados aqui):

```json
{"mensagem": "Login realizado com sucesso.", "dados": {"access": "eyJhbGciOi...", "refresh": "eyJhbGciOi...", "usuario": {"id": 1, "nome": "Ana Souza", "email": "ana@exemplo.com", "matricula": "2026001", "perfil": "SOLICITANTE", "perfil_rotulo": "Solicitante"}}}
```

E-mail ou senha errados (ou usuário desativado) respondem sempre igual, **401**:

```json
{"erro": {"codigo": "CREDENCIAIS_INVALIDAS", "mensagem": "E-mail ou senha incorretos."}}
```

Copie o valor de `access` para uma variável e use-o nos exemplos seguintes:

```bash
ACCESS="cole-aqui-o-access"
```

No Prompt de Comando do Windows (sem aspas):

```bat
set ACCESS=cole-aqui-o-access
```

Ver o usuário logado (`GET /api/auth/me/`):

```bash
curl http://localhost:8000/api/auth/me/ -H "Authorization: Bearer $ACCESS"
```

```json
{"mensagem": "Usuário autenticado.", "dados": {"id": 1, "nome": "Ana Souza", "email": "ana@exemplo.com", "matricula": "2026001", "perfil": "SOLICITANTE", "perfil_rotulo": "Solicitante"}}
```

Quando o `access` expira, os pedidos respondem **401** `NAO_AUTENTICADO`. Gere outro com o `refresh` (`POST /api/auth/refresh/`):

```bash
curl -X POST http://localhost:8000/api/auth/refresh/ -H "Content-Type: application/json" -d '{"refresh": "cole-aqui-o-refresh"}'
```

```json
{"mensagem": "Token renovado.", "dados": {"access": "eyJhbGciOi..."}}
```

Um `refresh` inválido ou expirado responde **401** `NAO_AUTENTICADO`; aí é preciso entrar de novo. Para sair, basta descartar os dois tokens.

#### Solicitar uma reserva

Solicitar uma reserva exige o token do login. O solicitante é sempre o usuário logado; um `solicitante` enviado no corpo é ignorado.

Solicitar a reserva (`POST /api/reservas/`), com data no formato `AAAA-MM-DD` e horas em `HH:MM`, usando o id de um espaço cadastrado:

```bash
curl -X POST http://localhost:8000/api/reservas/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"espaco_id": 1, "data": "2026-11-10", "hora_inicio": "10:00", "hora_fim": "11:00", "finalidade": "Treino de volei"}'
```

No Prompt de Comando do Windows:

```bat
curl -X POST http://localhost:8000/api/reservas/ -H "Authorization: Bearer %ACCESS%" -H "Content-Type: application/json" -d "{\"espaco_id\": 1, \"data\": \"2026-11-10\", \"hora_inicio\": \"10:00\", \"hora_fim\": \"11:00\", \"finalidade\": \"Treino de volei\"}"
```

Resposta **201**, com a reserva na situação inicial `SOLICITADA` (a resposta traz `espaco_id`; o nome do espaço vem da listagem de espaços):

```json
{"mensagem": "Reserva solicitada com sucesso. Aguarde a confirmação do gestor.", "dados": {"id": 1, "espaco_id": 1, "solicitante": {"usuario_id": 1, "nome": "Ana Souza", "matricula": "2026001"}, "data": "2026-11-10", "hora_inicio": "10:00", "hora_fim": "11:00", "finalidade": "Treino de volei", "situacao": "SOLICITADA", "situacao_rotulo": "Solicitada", "motivo_da_situacao": null, "criada_em": "2026-10-22T15:57:00.442650-03:00"}}
```

Repetir o pedido no mesmo horário responde **409**:

```json
{"erro": {"codigo": "CONFLITO_DE_HORARIO", "mensagem": "Este espaço já tem uma reserva Solicitada em 10/11/2026 10:00–11:00. Escolha outro horário."}}
```

Outros erros: sem token → **401** `NAO_AUTENTICADO`; espaço inexistente → **404** `ESPACO_NAO_ENCONTRADO`; espaço inativo → **409** `ESPACO_INATIVO`; término igual ou antes do início → **400** `HORARIO_INVALIDO`; horário que já passou → **400** `DATA_RETROATIVA`; campo ausente ou data inválida → **400** `DADOS_INVALIDOS` com o campo em `campos`.

#### Consultar reservas

Listar as reservas (`GET /api/reservas/`) exige login e devolve as reservas ordenadas pelo início. Filtros opcionais, que funcionam sozinhos ou combinados:

| Parâmetro | Exemplo | Efeito |
|---|---|---|
| `espaco` | `espaco=1` | reservas do espaço com esse id (um id inexistente devolve lista vazia) |
| `situacao` | `situacao=SOLICITADA` | `SOLICITADA`, `CONFIRMADA`, `RECUSADA`, `CANCELADA` ou `CONCLUIDA` |
| `data` | `data=2026-11-10` | reservas desse dia (`AAAA-MM-DD`) |
| `solicitante` | `solicitante=souza` | trecho do nome ou da matrícula, sem diferenciar maiúsculas |
| `minhas` | `minhas=true` | só as reservas do usuário logado |

> Por enquanto, qualquer usuário logado vê todas as reservas. A restrição do perfil Solicitante às próprias reservas entra na AUT-05.

Por um critério:

```bash
curl "http://localhost:8000/api/reservas/?situacao=SOLICITADA" -H "Authorization: Bearer $ACCESS"
```

Por dois critérios combinados:

```bash
curl "http://localhost:8000/api/reservas/?espaco=1&situacao=SOLICITADA" -H "Authorization: Bearer $ACCESS"
```

Só as reservas do usuário logado:

```bash
curl "http://localhost:8000/api/reservas/?minhas=true" -H "Authorization: Bearer $ACCESS"
```

Resposta **200** (a mensagem informa a quantidade: "Nenhuma reserva encontrada.", "1 reserva encontrada." ou "N reservas encontradas."):

```json
{"mensagem": "1 reserva encontrada.", "dados": [{"id": 1, "espaco_id": 1, "solicitante": {"usuario_id": 1, "nome": "Ana Souza", "matricula": "2026001"}, "data": "2026-11-10", "hora_inicio": "10:00", "hora_fim": "11:00", "finalidade": "Treino de volei", "situacao": "SOLICITADA", "situacao_rotulo": "Solicitada", "motivo_da_situacao": null, "criada_em": "2026-10-22T15:57:00.442650-03:00"}]}
```

Um filtro em formato inválido (por exemplo, `situacao=XYZ`, `data=2026-13-40` ou `espaco=abc`) responde **400** `DADOS_INVALIDOS`, com o parâmetro em `campos`.

Obter uma reserva (`GET /api/reservas/{id}/`), no mesmo formato da criação:

```bash
curl http://localhost:8000/api/reservas/1/ -H "Authorization: Bearer $ACCESS"
```

Um id inexistente responde **404**:

```json
{"erro": {"codigo": "RESERVA_NAO_ENCONTRADA", "mensagem": "Reserva de código 9999 não encontrada."}}
```

#### Alterar a situação de uma reserva

Alterar a situação (`PATCH /api/reservas/{id}/situacao/`) exige login. O corpo leva `situacao` e, para recusar ou cancelar, um `motivo`. Só estas mudanças são aceitas:

| Situação atual | Pode ir para |
|---|---|
| `SOLICITADA` | `CONFIRMADA`, `RECUSADA` (com motivo), `CANCELADA` (com motivo) |
| `CONFIRMADA` | `CONCLUIDA`, `CANCELADA` (com motivo) |
| `CONCLUIDA`, `RECUSADA`, `CANCELADA` | nenhuma (situações finais) |

> Por enquanto, qualquer usuário logado executa qualquer mudança permitida. A restrição por perfil (Gestor confirma, recusa, conclui e cancela; Solicitante só cancela as próprias) entra na AUT-05.

Confirmar a reserva:

```bash
curl -X PATCH http://localhost:8000/api/reservas/1/situacao/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"situacao": "CONFIRMADA"}'
```

No Prompt de Comando do Windows:

```bat
curl -X PATCH http://localhost:8000/api/reservas/1/situacao/ -H "Authorization: Bearer %ACCESS%" -H "Content-Type: application/json" -d "{\"situacao\": \"CONFIRMADA\"}"
```

Resposta **200**, com a reserva atualizada (a mensagem acompanha a nova situação: confirmada, recusada, cancelada ou concluída):

```json
{"mensagem": "Reserva confirmada com sucesso.", "dados": {"id": 1, "espaco_id": 1, "solicitante": {"usuario_id": 1, "nome": "Ana Souza", "matricula": "2026001"}, "data": "2026-11-10", "hora_inicio": "10:00", "hora_fim": "11:00", "finalidade": "Treino de volei", "situacao": "CONFIRMADA", "situacao_rotulo": "Confirmada", "motivo_da_situacao": null, "criada_em": "2026-10-22T15:57:00.442650-03:00"}}
```

Uma mudança fora da tabela (por exemplo, voltar a confirmada para `SOLICITADA`) responde **409** e a reserva fica como estava:

```json
{"erro": {"codigo": "TRANSICAO_DE_SITUACAO_INVALIDA", "mensagem": "Não é possível alterar uma reserva Confirmada para Solicitada."}}
```

Cancelar com motivo (o horário fica livre para outra reserva):

```bash
curl -X PATCH http://localhost:8000/api/reservas/1/situacao/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"situacao": "CANCELADA", "motivo": "Chuva forte"}'
```

```json
{"mensagem": "Reserva cancelada com sucesso.", "dados": {"id": 1, "espaco_id": 1, "solicitante": {"usuario_id": 1, "nome": "Ana Souza", "matricula": "2026001"}, "data": "2026-11-10", "hora_inicio": "10:00", "hora_fim": "11:00", "finalidade": "Treino de volei", "situacao": "CANCELADA", "situacao_rotulo": "Cancelada", "motivo_da_situacao": "Chuva forte", "criada_em": "2026-10-22T15:57:00.442650-03:00"}}
```

Outros erros: recusar ou cancelar sem motivo → **400** `MOTIVO_OBRIGATORIO`; situação fora da lista → **400** `SITUACAO_INVALIDA`; corpo sem `situacao` → **400** `DADOS_INVALIDOS`; reserva inexistente → **404** `RESERVA_NAO_ENCONTRADA`; sem token → **401** `NAO_AUTENTICADO`; outro método além de `PATCH` → **405** `METODO_NAO_PERMITIDO`.

### Criar um superusuário (acesso ao admin)

Com os serviços no ar, em outro terminal dentro de `src`:

```bash
docker compose exec backend python manage.py createsuperuser
```

O comando pede **e-mail, nome, matrícula e senha**. O login no admin é feito com o e-mail, e o superusuário é criado com o perfil **Gestor**.

> **Quem subiu o banco antes da AUT-02:** a migration `contas.0002` remove o `username` e torna nome e matrícula obrigatórios, partindo de uma tabela de usuários vazia. Apague o banco local uma vez antes de subir de novo:
>
> ```bash
> docker compose down -v
> ```

### Frontend: lint e build

Com os serviços no ar, dentro de `src`:

```bash
docker compose exec frontend npm run lint
```

```bash
docker compose exec frontend npm run build
```

As dependências do frontend ficam num volume próprio do container (`/app/node_modules`). Ao mudar o `package.json` (instalar, remover ou atualizar pacotes), recrie esse volume:

```bash
docker compose up --build -V frontend
```

### Qualidade do código (backend)

Com os serviços no ar, dentro de `src`. As configurações ficam em `src/backend/pyproject.toml`.

Testes (pytest):

```bash
docker compose exec backend pytest
```

Cobertura de testes dos contextos `espacos`, `reservas` e `contas` e do pacote `compartilhado`:

```bash
docker compose exec backend pytest --cov
```

Linter e formatação (ruff):

```bash
docker compose exec backend sh -c "ruff check . && ruff format --check ."
```

Regra de dependência entre camadas e contextos (import-linter):

```bash
docker compose exec backend lint-imports
```

Verificação completa, antes de cada PR:

```bash
docker compose exec backend sh -c "ruff check . && ruff format --check . && lint-imports && pytest"
```

Ao mudar o `requirements.txt` ou o `requirements-dev.txt`, reconstrua a imagem do backend:

```bash
docker compose up --build -d backend
```

### Parar a aplicação

```bash
docker compose down
```

Para parar **e apagar os dados do banco**:

```bash
docker compose down -v
```

## Persistência

PostgreSQL 16, executado no container `db`. Os dados ficam no volume Docker `postgres_data` e se mantêm entre execuções até um `docker compose down -v`.

## Limitações conhecidas

- **Sem revogação de tokens:** não há lista de tokens revogados. Sair é descartar os tokens no cliente; um `access` roubado continua valendo até expirar (30 minutos) e um `refresh`, até 1 dia.
- **Perfis ainda sem efeito:** até a AUT-05, qualquer usuário logado vê todas as reservas e executa qualquer mudança de situação permitida, seja Gestor ou Solicitante.
- **Alterações simultâneas na mesma reserva:** se duas pessoas mudarem a situação da mesma reserva ao mesmo tempo, vale a última gravada (não há bloqueio otimista). Para o porte do projeto, isso é aceitável.
