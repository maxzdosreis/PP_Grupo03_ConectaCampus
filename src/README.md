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
| `redis_data` (só no [override do Redis persistente](#redis-com-persistência-opcional-para-a-demonstração); no Docker, `conecta-campus_redis_data`) | `redis` | O AOF do Redis, em `/data`. Não existe no modo padrão. `docker compose down` o mantém, e `down -v` o apaga junto com o do banco. |
| `/app/node_modules` (volume anônimo) | `frontend` | Mantém as dependências instaladas na imagem, para o bind mount não escondê-las. Depois de mudar o `package.json`, recrie-o (veja os [comandos do frontend](frontend/README.md#comandos)). |

## Redis com persistência (opcional, para a demonstração)

O Redis padrão não persiste nada: a agenda e o índice de reservas são projeções que o PostgreSQL reconstrói, e a contagem do limite de tentativas zera ao reiniciar. O arquivo `docker-compose.redis-persistente.yml` é um override que só serve para a demonstração, para comparar "reinicia e perde tudo" com "reinicia e continua". **Não é para produção.**

```powershell
docker compose -f docker-compose.yml -f docker-compose.redis-persistente.yml up -d redis
```

- **O que muda:** o `command` do `redis` é substituído por `redis-server --save "" --appendonly yes --appendfsync everysec` (AOF gravado a cada segundo; snapshots RDB seguem desligados, então o AOF é o único mecanismo) e o volume `redis_data` é montado em `/data`. Imagem e `healthcheck` são os do arquivo base. Uma queda brusca pode perder até cerca de 1 s de escrita.
- **Trocar de modo exige recriar o container:** use `up -d redis` com a lista de arquivos desejada. `docker compose restart redis` mantém o comando antigo.
- **Voltar ao padrão:** `docker compose up -d redis` (só o arquivo base). O volume continua existindo, mas é ignorado.
- **Zerar o AOF guardado:** com o Redis parado (`docker compose stop redis`), `docker volume rm conecta-campus_redis_data`. `docker compose down` mantém o volume; `docker compose down -v` apaga o do banco **e** o do Redis.
- **Cuidado com dado velho:** com o override ligado, os contadores do limite de tentativas também sobrevivem ao reinício (aceitável só na demonstração). Se o PostgreSQL mudar ou for recriado (`down -v`) e o override for ligado de novo, o Redis carrega o AOF antigo. Corrija com `docker compose exec backend python manage.py reconstruir_agenda_redis` ou zere o volume.

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
| `LIMITE_LOGIN_POR_IP` | `20/min` | Tentativas de login do mesmo endereço IP (o da conexão), com qualquer e-mail. Mesmo formato. |
| `LIMITE_CADASTRO_POR_IP` | `10/hour` | Pedidos de cadastro do mesmo endereço IP. Mesmo formato. A renovação do token não tem limite. |
| `LIMITE_TROCA_DE_SENHA_POR_USUARIO` | `5/min` | Pedidos de troca de senha da mesma pessoa logada (contados por usuário, não por endereço IP). Mesmo formato. |
| `LIMITE_GESTAO_DE_USUARIOS_POR_USUARIO` | `30/min` | Alterações de perfil ou situação de contas feitas pelo mesmo Gestor (contadas por usuário). Mesmo formato. |

### Derivadas pelo Compose a partir das portas

Estas duas **não ficam no `.env`**: o `docker-compose.yml` as monta a partir das portas, para a troca de uma porta valer numa variável só. O `backend` recebe do Compose também `REDIS_URL: redis://redis:6379/0` (o serviço `redis` pela rede interna, banco 0); sem ela, o backend não sobe (`ImproperlyConfigured`). Os testes usam o banco 1 do mesmo Redis, limpo antes de cada teste, e nunca mexem no banco 0.

| Variável | Serviço | Fórmula no `docker-compose.yml` | Com as portas padrão |
|---|---|---|---|
| `CORS_ALLOWED_ORIGINS` | `backend` | `http://localhost:${FRONTEND_PORT_HOST:-5173},http://127.0.0.1:${FRONTEND_PORT_HOST:-5173}` | `http://localhost:5173,http://127.0.0.1:5173`: a tela aberta por `localhost` ou por `127.0.0.1` pode chamar a API pelo navegador; qualquer outra origem é recusada. |
| `VITE_API_URL` | `frontend` | `http://localhost:${BACKEND_PORT_HOST:-8000}/api` | `http://localhost:8000/api`: o endereço da API usado pela tela no navegador. |

As duas ficam em `environment:`, que tem precedência sobre o `env_file: .env`. Por isso um `.env` antigo, que ainda traga essas variáveis com as portas de antes, não muda nada e pode ficar como está. Não há como sobrescrevê-las pelo `.env`, de propósito: o defeito corrigido era justamente o valor escrito à mão que ficava fora de sincronia com a porta. Abrir a tela por outro host ou outra origem exigiria mudar o `docker-compose.yml`.

## Modo de produção (opcional, INF-08)

O `docker-compose.prod.yml` sobe o sistema sem as facilidades do desenvolvimento. **Nada do modo padrão muda**: o `docker-compose.yml`, os `Dockerfile` e o `.env.example` são os mesmos, e tudo do modo de produção vive em arquivos próprios (`docker-compose.prod.yml`, `backend/Dockerfile.prod`, `frontend/Dockerfile.prod`, `frontend/nginx.conf` e `.env.prod.example`). O passo a passo curto está no [README da raiz](../README.md#modo-de-produção-opcional); aqui ficam os detalhes. Todo comando abaixo roda dentro de `src` e leva `-f docker-compose.prod.yml --env-file .env.prod` (sem o `--env-file`, o Compose leria o `.env` de desenvolvimento).

| Serviço | Imagem / build | Porta no seu computador | O que faz |
|---|---|---|---|
| `db` | `postgres:16-alpine` | nenhuma | Banco PostgreSQL só na rede interna, com volume próprio. |
| `redis` | `redis:8-alpine` | nenhuma | Contador do limite de tentativas, sem persistência, como no modo padrão. |
| `migrar` | `backend/Dockerfile.prod` | nenhuma | Tarefa de uso único: `python manage.py migrate --noinput` e sai. |
| `backend` | `backend/Dockerfile.prod` (`python:3.12-slim`, só `requirements.txt`) | nenhuma (`expose` 8000, rede interna) | gunicorn (`config.wsgi:application`) como usuário `aplicacao`, sem root. Sobe depois de `db` e `redis` saudáveis e de `migrar` concluído. Healthcheck em `/api/health/` (banco e cache). |
| `frontend` | `frontend/Dockerfile.prod` (build com `node:24-alpine`, servido por `nginx:1.29-alpine`) | `FRONTEND_PORT_HOST` → 80 (padrão **8080**) | nginx: serve a tela compilada e repassa `/api/`, `/admin/` e `/static/` ao `backend`. Sobe depois do `backend` saudável. |

### Decisões

- **a) Projeto, volume e rede com nome próprio.** O `name:` é `conecta-campus-prod` (o do modo padrão é `conecta-campus`), e o volume (`conecta-campus-prod_postgres_data`) e a rede (`conecta-campus-prod_rede`) têm `name:` explícito. Com o mesmo nome, o modo de produção reutilizaria o banco do desenvolvimento, e um `down -v` aqui o apagaria. Nenhum serviço monta o código-fonte (sem bind mount).
- **b) Uma origem só.** O navegador fala só com o nginx, então a tela é construída com `VITE_API_URL=/api` (relativa) e **não é preciso CORS**. O Vite grava esse valor no JavaScript **em tempo de build** (build arg do `frontend`): para mudá-lo, reconstrua com `up -d --build`.
- **c) Migração separada.** O servidor web não roda `migrate` a cada start: o serviço `migrar` roda uma vez, e o `backend` espera `service_completed_successfully`. Não há carga de dados de exemplo (o comando exige `DJANGO_DEBUG=True`); o primeiro Gestor sai de `createsuperuser`.
- **d) Estáticos do admin com whitenoise**, coletados no build (`collectstatic`); `STATIC_ROOT` é `backend/staticfiles`. O `gunicorn` e o `whitenoise` entram em `requirements.txt` (também chegam à imagem de desenvolvimento, que não os usa).
- **e) Só o nginx publica porta.** Banco, Redis e backend não têm `ports`.
- **f) Segredos sem padrão.** `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DB_DATABASE`, `DB_USER` e `DB_PASSWORD` usam `${VAR:?...}`: faltando uma (ou vazia), o `up` falha dizendo qual. Além disso, o Django só aplica as regras de produção quando `DJANGO_MODO_PRODUCAO=1` (o compose de produção define): chave com 50 caracteres ou mais, com pelo menos 5 diferentes e que não comece com `troque-` nem `django-insecure-`; `DJANGO_DEBUG` falso; `DJANGO_ALLOWED_HOSTS` preenchida e sem `*`; `DB_HOST` definido. A variável própria existe porque `DJANGO_DEBUG=False` sozinho já é o padrão do modo de avaliação e dos testes, que usam a chave de exemplo.
- **g) Limite de tentativas atrás do nginx.** O nginx **sobrescreve** `X-Forwarded-For` com o IP de quem o chama (`$remote_addr`), e o compose define `DJANGO_NUM_PROXIES=1` para o limite por IP (AUT-08) usar esse valor, e não o IP do nginx. Por isso o backend só enxerga o IP de quem chama o nginx: com mais um proxy (por exemplo, o de TLS) na frente, o limite por IP passaria a valer para todos juntos, porque o nginx ainda não repassa o IP real que esse proxy informa. Isso é uma limitação conhecida, a tratar na INF-09.
- **h) Healthchecks e logs.** O do `backend` chama `/api/health/` com o primeiro host de `DJANGO_ALLOWED_HOSTS` no cabeçalho `Host` (por isso essa variável deve listar hosts simples, sem porta nem curinga); o do nginx pede `/`. Os serviços de longa duração têm `restart: unless-stopped`, e os logs rodam em `json-file` com 3 arquivos de 10 MB.
- **i) gunicorn:** `GUNICORN_WORKERS` (padrão 3) e `GUNICORN_TIMEOUT` (padrão 30 s), lidos no start.

### Variáveis (`.env.prod`)

O `.env.prod` nunca é versionado; o `.env.prod.example` lista só os nomes. **Obrigatórias:** `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DB_DATABASE`, `DB_USER`, `DB_PASSWORD`. **Opcionais (padrão entre parênteses):** `FRONTEND_PORT_HOST` (8080), `GUNICORN_WORKERS` (3), `GUNICORN_TIMEOUT` (30), `DJANGO_HTTPS` (0), `DJANGO_CSRF_TRUSTED_ORIGINS` (vazio), `DJANGO_NUM_PROXIES` (1), os cinco `LIMITE_*` e `JWT_ACCESS_MINUTES` e `JWT_REFRESH_DAYS` (iguais aos do `.env.example`).

### HTTPS e `manage.py check --deploy`

O compose **não tem TLS**: o nginx escuta HTTP na porta 80. Para uso real, ponha um proxy com certificado na frente e ligue `DJANGO_HTTPS=1`, que ativa o redirecionamento para HTTPS (menos no `/api/health/`), o HSTS de 1 ano (com subdomínios e `preload`; só declara a elegibilidade, e quem decide é o envio do domínio à lista), os cookies de sessão e CSRF `Secure` e a leitura de `X-Forwarded-Proto` (`SECURE_PROXY_SSL_HEADER`). O admin atrás do proxy precisa de `DJANGO_CSRF_TRUSTED_ORIGINS` com as origens `https://...` do sistema.

O `python manage.py check --deploy` (rodado dentro do `backend` de produção) dá:

- **Com `DJANGO_HTTPS=0` (padrão, sem TLS): 4 avisos, todos que dependem de TLS** (nenhum erro): `security.W004` (sem `SECURE_HSTS_SECONDS`), `security.W008` (`SECURE_SSL_REDIRECT` desligado), `security.W012` (`SESSION_COOKIE_SECURE`) e `security.W016` (`CSRF_COOKIE_SECURE`). Um cookie `Secure` e o HSTS sobre HTTP puro travariam o login e o navegador, por isso ficam desligados sem HTTPS.
- **Com `DJANGO_HTTPS=1`: nenhum aviso** (`System check identified no issues`). Para conferir sem proxy: `docker compose -f docker-compose.prod.yml --env-file .env.prod exec -e DJANGO_HTTPS=1 backend python manage.py check --deploy`.

Por "sem avisos críticos" entende-se: nenhum erro e nenhum aviso de segurança que não dependa de TLS.

### Comandos úteis

```bash
docker compose -f docker-compose.prod.yml --env-file .env.prod ps
docker compose -f docker-compose.prod.yml --env-file .env.prod logs -f backend
docker compose -f docker-compose.prod.yml --env-file .env.prod exec backend python manage.py check --deploy
```

## Onde continuar

- [Backend](backend/README.md): organização em contextos e camadas, formato das respostas, autenticação, comandos e o roteiro com `curl`.
- [Frontend](frontend/README.md): pastas, telas, sessão e comandos.
