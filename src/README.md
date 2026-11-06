# `src/` — serviços e configuração

Tudo o que executa o Conecta Campus fica nesta pasta: o [backend](backend/README.md) (Django + DRF), o [frontend](frontend/README.md) (React + Vite) e o `docker-compose.yml` que sobe os dois com o PostgreSQL. Os comandos `docker compose ...` de todos os READMEs rodam **a partir desta pasta**. O passo a passo para rodar do zero está no [README da raiz](../README.md#como-executar).

## Serviços do Docker Compose

O projeto se chama `conecta-campus` no Compose (`name:` do `docker-compose.yml`). Por isso os containers e o volume levam esse prefixo (`conecta-campus-backend-1`, `conecta-campus_postgres_data`), e outra cópia do projeto no mesmo computador usa os mesmos. As três portas publicadas no seu computador vêm do `.env` (`DB_PORT_HOST`, `BACKEND_PORT_HOST`, `FRONTEND_PORT_HOST`, com 5432, 8000 e 5173 como padrão); dentro dos containers elas não mudam.

| Serviço | Imagem / build | Porta no seu computador | O que faz |
|---|---|---|---|
| `db` | `postgres:16-alpine` | `DB_PORT_HOST` → 5432 (padrão 5432) | Banco PostgreSQL. Tem `healthcheck` com `pg_isready`, a cada 5 s, até 10 tentativas. |
| `backend` | `backend/Dockerfile` (`python:3.12-slim`, instala `requirements.txt` e `requirements-dev.txt`) | `BACKEND_PORT_HOST` → 8000 (padrão 8000) | Ao subir, roda `python manage.py migrate --noinput` e depois `python manage.py runserver 0.0.0.0:8000`. Só sobe quando o `db` está saudável (`condition: service_healthy`). Lê as variáveis do `.env` (`env_file`). |
| `frontend` | `frontend/Dockerfile` (`node:24-alpine`, `npm ci`) | `FRONTEND_PORT_HOST` → 5173 (padrão 5173) | Servidor de desenvolvimento do Vite (`npm run dev -- --host 0.0.0.0`). Recebe só `VITE_API_URL` e `CHOKIDAR_USEPOLLING=true`. Sobe depois do `backend`. |

## Volumes

| Volume | Serviço | Para quê |
|---|---|---|
| `postgres_data` (volume nomeado; no Docker, `conecta-campus_postgres_data`) | `db` | Os dados do banco. Sobrevive a `docker compose down` e só é apagado com `docker compose down -v`. |
| `./backend:/app` (bind mount) | `backend` | O código do backend montado no container: editar um arquivo recarrega o `runserver`. |
| `./frontend:/app` (bind mount) | `frontend` | O código do frontend montado no container, com recarga do Vite. A observação de arquivos usa polling (`CHOKIDAR_USEPOLLING` e `watch.usePolling` no `vite.config.ts`), porque o bind mount do Windows não avisa mudanças. |
| `/app/node_modules` (volume anônimo) | `frontend` | Mantém as dependências instaladas na imagem, para o bind mount não escondê-las. Depois de mudar o `package.json`, recrie-o (veja os [comandos do frontend](frontend/README.md#comandos)). |

## Variáveis de ambiente (`.env`)

O `.env` é criado a partir do `.env.example` (passo 1 do [README da raiz](../README.md#passo-a-passo)) e **nunca** é versionado. O Compose recusa subir se `DB_DATABASE`, `DB_USER`, `DB_PASSWORD` ou `VITE_API_URL` estiverem ausentes ou vazias (`required variable DB_PASSWORD is missing a value: defina DB_PASSWORD no .env`), e o backend não sobe sem `DJANGO_SECRET_KEY` (`ImproperlyConfigured`). `DJANGO_DEBUG` ausente vale `False`. O `.env` é lido quando o container é criado: depois de mudá-lo, rode `docker compose up -d` (um `restart` não relê o arquivo).

| Variável | Valor no `.env.example` | Para que serve |
|---|---|---|
| `DB_DATABASE` | `conecta_campus` | Nome do banco criado pelo `db` e usado pelo Django. |
| `DB_USER` | `conecta` | Usuário do banco. |
| `DB_PASSWORD` | valor de exemplo (troque) | Senha do banco. |
| `DB_HOST` | `db` | Nome do serviço do banco na rede do Docker. |
| `DB_PORT` | `5432` | Porta que o Django usa dentro da rede do Docker: deixe 5432. |
| `DB_PORT_HOST` | `5432` | Porta publicada no seu computador. Se já houver um PostgreSQL local na 5432, mude só esta (ex.: `5433`). |
| `BACKEND_PORT_HOST` | `8000` | Porta da API no seu computador. Ao trocar (ex.: `8001`), troque a porta de `VITE_API_URL` junto. |
| `FRONTEND_PORT_HOST` | `5173` | Porta da tela no seu computador. Ao trocar (ex.: `5174`), troque as portas de `CORS_ALLOWED_ORIGINS` junto e abra a tela na porta nova. |
| `DJANGO_SECRET_KEY` | valor de exemplo (troque) | Chave do Django, que também assina os tokens JWT: use pelo menos 32 caracteres aleatórios. Para gerar uma: `python -c "import secrets; print(secrets.token_urlsafe(50))"`. |
| `DJANGO_DEBUG` | `True` | Modo de desenvolvimento. O comando de dados de exemplo só roda com `True`. |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1,backend` | Hosts aceitos pelo Django, separados por vírgula. |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | Origens que podem chamar a API pelo navegador (a tela aberta por `localhost` ou por `127.0.0.1`, na `FRONTEND_PORT_HOST`). Qualquer outra é recusada. |
| `JWT_ACCESS_MINUTES` | `30` | Validade do token de acesso, em minutos. |
| `JWT_REFRESH_DAYS` | `1` | Validade do token de renovação, em dias. |
| `VITE_API_URL` | `http://localhost:8000/api` | Endereço da API usado pelo frontend no navegador; a porta é a `BACKEND_PORT_HOST`. |

## Onde continuar

- [Backend](backend/README.md): organização em contextos e camadas, formato das respostas, autenticação, comandos e o roteiro com `curl`.
- [Frontend](frontend/README.md): pastas, telas, sessão e comandos.
