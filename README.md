# Conecta Campus — Reserva de Quadras e Espaços Esportivos

Sistema para a comunidade acadêmica cadastrar quadras e espaços esportivos, solicitar reservas e acompanhar a situação de cada reserva.

## Tecnologias

- Python 3.12, Django 5.2 LTS, Django REST Framework 3.18
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

#### Solicitar uma reserva

Solicitar uma reserva exige login. **Por enquanto a autenticação é Basic (e-mail e senha em cada pedido, com `-u`) e é provisória:** a AUT-03 troca por login com token (JWT). O solicitante é sempre o usuário logado; um `solicitante` enviado no corpo é ignorado.

Primeiro crie um usuário de teste. Pode ser um superusuário (`createsuperuser`, veja a seção abaixo) ou um usuário comum pelo shell do Django:

```bash
docker compose exec backend python manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_user('ana@exemplo.com', 'senha-de-teste-123', nome='Ana Souza', matricula='2026001')"
```

Solicitar a reserva (`POST /api/reservas/`), com data no formato `AAAA-MM-DD` e horas em `HH:MM`, usando o id de um espaço cadastrado:

```bash
curl -X POST http://localhost:8000/api/reservas/ -u ana@exemplo.com:senha-de-teste-123 -H "Content-Type: application/json" -d '{"espaco_id": 1, "data": "2026-11-10", "hora_inicio": "10:00", "hora_fim": "11:00", "finalidade": "Treino de volei"}'
```

No Prompt de Comando do Windows:

```bat
curl -X POST http://localhost:8000/api/reservas/ -u ana@exemplo.com:senha-de-teste-123 -H "Content-Type: application/json" -d "{\"espaco_id\": 1, \"data\": \"2026-11-10\", \"hora_inicio\": \"10:00\", \"hora_fim\": \"11:00\", \"finalidade\": \"Treino de volei\"}"
```

Resposta **201**, com a reserva na situação inicial `SOLICITADA` (a resposta traz `espaco_id`; o nome do espaço vem da listagem de espaços):

```json
{"mensagem": "Reserva solicitada com sucesso. Aguarde a confirmação do gestor.", "dados": {"id": 1, "espaco_id": 1, "solicitante": {"usuario_id": 1, "nome": "Ana Souza", "matricula": "2026001"}, "data": "2026-11-10", "hora_inicio": "10:00", "hora_fim": "11:00", "finalidade": "Treino de volei", "situacao": "SOLICITADA", "situacao_rotulo": "Solicitada", "motivo_da_situacao": null, "criada_em": "2026-10-22T15:57:00.442650-03:00"}}
```

Repetir o pedido no mesmo horário responde **409**:

```json
{"erro": {"codigo": "CONFLITO_DE_HORARIO", "mensagem": "Este espaço já tem uma reserva Solicitada em 10/11/2026 10:00–11:00. Escolha outro horário."}}
```

Outros erros: sem `-u` → **401** `NAO_AUTENTICADO`; espaço inexistente → **404** `ESPACO_NAO_ENCONTRADO`; espaço inativo → **409** `ESPACO_INATIVO`; término igual ou antes do início → **400** `HORARIO_INVALIDO`; horário que já passou → **400** `DATA_RETROATIVA`; campo ausente ou data inválida → **400** `DADOS_INVALIDOS` com o campo em `campos`.

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
