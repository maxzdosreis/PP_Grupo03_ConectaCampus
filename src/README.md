# `src/` — serviços e configuração

Tudo o que executa o Conecta Campus fica nesta pasta: o [backend](backend/README.md) (Django + DRF), o [frontend](frontend/README.md) (React + Vite) e o `docker-compose.yml` que sobe os dois com o PostgreSQL. Os comandos `docker compose ...` de todos os READMEs rodam **a partir desta pasta**. O passo a passo para rodar do zero está no [README da raiz](../README.md#como-executar).

## Serviços do Docker Compose

O projeto se chama `conecta-campus` no Compose (`name:` do `docker-compose.yml`). Por isso os containers e o volume levam esse prefixo (`conecta-campus-backend-1`, `conecta-campus_postgres_data`), e outra cópia do projeto no mesmo computador usa os mesmos. As três portas publicadas no seu computador vêm do `.env` (`DB_PORT_HOST`, `BACKEND_PORT_HOST`, `FRONTEND_PORT_HOST`, com 5432, 8000 e 5173 como padrão); dentro dos containers elas não mudam.

| Serviço | Imagem / build | Porta no seu computador | O que faz |
|---|---|---|---|
| `db` | `postgres:16-alpine` | `DB_PORT_HOST` → 5432 (padrão 5432) | Banco PostgreSQL. Tem `healthcheck` com `pg_isready`, a cada 5 s, até 10 tentativas. |
| `backend` | `backend/Dockerfile` (`python:3.12-slim`, instala `requirements.txt` e `requirements-dev.txt`) | `BACKEND_PORT_HOST` → 8000 (padrão 8000) | Ao subir, roda `python manage.py migrate --noinput` e depois `python manage.py runserver 0.0.0.0:8000`. Só sobe quando o `db` e o `redis` estão saudáveis (`condition: service_healthy`). Lê as variáveis do `.env` (`env_file`) e recebe do Compose `CORS_ALLOWED_ORIGINS`, [derivada da porta da tela](#derivadas-pelo-compose-a-partir-das-portas), e `REDIS_URL`. |
| `redis` | `redis:8-alpine` | nenhuma (só a rede interna do Compose) | Cache do backend: guarda a contagem do limite de tentativas de login e de cadastro. Roda com `redis-server --save "" --appendonly no`, só em memória (sem volume): a contagem zera quando ele reinicia. Tem `healthcheck` com `redis-cli ping`, a cada 5 s, até 10 tentativas. |
| `frontend` | `frontend/Dockerfile` (`node:24-alpine`, `npm ci`) | `FRONTEND_PORT_HOST` → 5173 (padrão 5173) | Servidor de desenvolvimento do Vite (`npm run dev -- --host 0.0.0.0`). Recebe só `VITE_API_URL`, [derivada da porta da API](#derivadas-pelo-compose-a-partir-das-portas), e `CHOKIDAR_USEPOLLING=true`. Sobe depois do `backend`. |

## Volumes

| Volume | Serviço | Para quê |
|---|---|---|
| `postgres_data` (volume nomeado; no Docker, `conecta-campus_postgres_data`) | `db` | Os dados do banco. Sobrevive a `docker compose down` e só é apagado com `docker compose down -v`. |
| `./backend:/app` (bind mount) | `backend` | O código do backend montado no container: editar um arquivo recarrega o `runserver`. |
| `./frontend:/app` (bind mount) | `frontend` | O código do frontend montado no container, com recarga do Vite. A observação de arquivos usa polling (`CHOKIDAR_USEPOLLING` e `watch.usePolling` no `vite.config.ts`), porque o bind mount do Windows não avisa mudanças. |
| `/app/node_modules` (volume anônimo) | `frontend` | Mantém as dependências instaladas na imagem, para o bind mount não escondê-las. Depois de mudar o `package.json`, recrie-o (veja os [comandos do frontend](frontend/README.md#comandos)). |

## Variáveis de ambiente (`.env`)

O `.env` é criado a partir do `.env.example` (passo 1 do [README da raiz](../README.md#passo-a-passo)) e **nunca** é versionado. O Compose recusa subir se `DB_DATABASE`, `DB_USER` ou `DB_PASSWORD` estiverem ausentes ou vazias (`required variable DB_PASSWORD is missing a value: defina DB_PASSWORD no .env`), e o backend não sobe sem `DJANGO_SECRET_KEY` (`ImproperlyConfigured`). `DJANGO_DEBUG` ausente vale `False`. O `.env` é lido quando o container é criado: depois de mudá-lo, rode `docker compose up -d` (um `restart` não relê o arquivo).

| Variável | Valor no `.env.example` | Para que serve |
|---|---|---|
| `DB_DATABASE` | `conecta_campus` | Nome do banco criado pelo `db` e usado pelo Django. |
| `DB_USER` | `conecta` | Usuário do banco. |
| `DB_PASSWORD` | valor de exemplo (troque) | Senha do banco. |
| `DB_HOST` | `db` | Nome do serviço do banco na rede do Docker. |
| `DB_PORT` | `5432` | Porta que o Django usa dentro da rede do Docker: deixe 5432. |
| `DB_PORT_HOST` | `5432` | Porta publicada no seu computador. Se já houver um PostgreSQL local na 5432, mude só esta (ex.: `5433`). |
| `BACKEND_PORT_HOST` | `8000` | Porta da API no seu computador. Se estiver ocupada, mude só esta (ex.: `8001`): o endereço da API usado pela tela acompanha. |
| `FRONTEND_PORT_HOST` | `5173` | Porta da tela no seu computador. Se estiver ocupada, mude só esta (ex.: `5174`) e abra a tela na porta nova: as origens aceitas pela API acompanham. |
| `DJANGO_SECRET_KEY` | valor de exemplo (troque) | Chave do Django, que também assina os tokens JWT: use pelo menos 32 caracteres aleatórios. Para gerar uma: `python -c "import secrets; print(secrets.token_urlsafe(50))"`. |
| `DJANGO_DEBUG` | `True` | Modo de desenvolvimento. O comando de dados de exemplo só roda com `True`. |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1,backend` | Hosts aceitos pelo Django, separados por vírgula. |
| `JWT_ACCESS_MINUTES` | `30` | Validade do token de acesso, em minutos. |
| `JWT_REFRESH_DAYS` | `1` | Validade do token de renovação, em dias. |
| `LIMITE_LOGIN_POR_EMAIL` | `5/min` | Tentativas de login com o mesmo e-mail, no formato `N/s`, `N/min`, `N/hour` ou `N/day`. Um valor fora do formato impede o backend de subir (`ImproperlyConfigured`, com o nome da variável). Ausente, vale o do exemplo. |
| `LIMITE_LOGIN_POR_IP` | `20/min` | Tentativas de login do mesmo computador (endereço da conexão), com qualquer e-mail. Mesmo formato. |
| `LIMITE_CADASTRO_POR_IP` | `10/hour` | Pedidos de cadastro do mesmo computador. Mesmo formato. A renovação do token não tem limite. |

### Derivadas pelo Compose a partir das portas

Estas duas **não ficam no `.env`**: o `docker-compose.yml` as monta a partir das portas, para a troca de uma porta valer numa variável só. O `backend` recebe do Compose também `REDIS_URL: redis://redis:6379/0` (o serviço `redis` pela rede interna, banco 0); sem ela, o backend não sobe (`ImproperlyConfigured`). Os testes usam o banco 1 do mesmo Redis, limpo antes de cada teste, e nunca mexem no banco 0.

| Variável | Serviço | Fórmula no `docker-compose.yml` | Com as portas padrão |
|---|---|---|---|
| `CORS_ALLOWED_ORIGINS` | `backend` | `http://localhost:${FRONTEND_PORT_HOST:-5173},http://127.0.0.1:${FRONTEND_PORT_HOST:-5173}` | `http://localhost:5173,http://127.0.0.1:5173`: a tela aberta por `localhost` ou por `127.0.0.1` pode chamar a API pelo navegador; qualquer outra origem é recusada. |
| `VITE_API_URL` | `frontend` | `http://localhost:${BACKEND_PORT_HOST:-8000}/api` | `http://localhost:8000/api`: o endereço da API usado pela tela no navegador. |

As duas ficam em `environment:`, que tem precedência sobre o `env_file: .env`. Por isso um `.env` antigo, que ainda traga essas variáveis com as portas de antes, não muda nada e pode ficar como está. Não há como sobrescrevê-las pelo `.env`, de propósito: o defeito corrigido era justamente o valor escrito à mão que ficava fora de sincronia com a porta. Abrir a tela por outro host ou outra origem exigiria mudar o `docker-compose.yml`.

## Onde continuar

- [Backend](backend/README.md): organização em contextos e camadas, formato das respostas, autenticação, comandos e o roteiro com `curl`.
- [Frontend](frontend/README.md): pastas, telas, sessão e comandos.
