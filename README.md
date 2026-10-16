# Conecta Campus — Reserva de Quadras e Espaços Esportivos

Sistema para a comunidade acadêmica cadastrar quadras e espaços esportivos, solicitar reservas e acompanhar a situação de cada reserva.

## Como executar

> **Situação atual:** por enquanto só o banco de dados (`db`) sobe. O backend e o frontend dependem da criação do projeto Django (INF-02) e do projeto Vite/React (INF-05); até lá, o build desses dois serviços falha.

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

2. Entre na pasta `src` e suba os serviços:

   ```bash
   cd src
   docker compose up --build
   ```

   As migrations do banco são aplicadas automaticamente quando o backend sobe.

3. Acesse:
   - API: http://localhost:8000
   - Frontend: http://localhost:5173

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
