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
