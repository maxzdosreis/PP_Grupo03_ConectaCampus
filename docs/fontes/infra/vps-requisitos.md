# Requisitos de uma VPS para o modo de produção do Conecta Campus

INF-09 (parte 1) • 0.1 • Rascunho. Autor: Max Zimmermann dos Reis. Revisor: Matheus Cezar Santos. Aprovador: Eduardo Almeida da Cunha.
Medido em 22/11/2026. Base do runbook da parte 2. Este documento não faz deploy e não altera código.

## Resumo executivo

1. Todo o stack de produção (db, redis, backend com 3 workers, nginx) usou **cerca de 257 MiB de RAM ocioso e cerca de 310 MiB sob carga de 20 a 40 usuários**, medido (Docker Desktop, WSL2, 4 vCPU). O banco com 10 mil reservas ocupa **cerca de 18 MB**.
2. **Mínimo viável:** 1 vCPU, 1 GB de RAM + 2 GB de swap, 25 GB de SSD, **com o build feito fora do servidor**. **Recomendado:** 2 vCPU, 2 GB de RAM, 40 GB de SSD, build no próprio servidor.
3. Todas as imagens base têm amd64 e arm64: uma VPS ARM serve (verificado com `docker buildx imagetools inspect`; o build em ARM não foi testado).
4. **Bloqueio real para publicar atrás de proxy HTTPS:** o nginx do compose reescreve `X-Forwarded-For` com `$remote_addr`, que atrás de um proxy é o IP do proxy; o limite por IP (AUT-08) passaria a contar todos os usuários juntos. Além disso, a porta 8080 é publicada em todas as interfaces e o Docker **ignora o `ufw`** nesse caso.
5. Faltam backup, limites de recursos nos contêineres e a decisão de provedor, domínio e orçamento (perguntas ao final). A VPS é opcional: a avaliação roda local com `docker compose up`.

## 1. O que o repositório declara (lido)

| Item | Valor | Fonte |
|---|---|---|
| Projeto Compose / volume / rede | `conecta-campus-prod` / `conecta-campus-prod_postgres_data` / `conecta-campus-prod_rede` | `src/docker-compose.prod.yml` |
| Serviços | `db` (postgres:16-alpine), `redis` (redis:8-alpine, `--save "" --appendonly no`, sem volume), `migrar` (uso único), `backend` (python:3.12-slim, gunicorn, usuário 10001, `expose 8000`), `frontend` (build node:24-alpine, runtime nginx:1.29-alpine) | idem e Dockerfiles `*.prod` |
| Porta publicada | só `frontend`: `${FRONTEND_PORT_HOST:-8080}:80`, **sem endereço, ou seja, em 0.0.0.0**. `db` e `redis` não publicam porta | compose |
| Workers do gunicorn | `GUNICORN_WORKERS` (padrão 3), `GUNICORN_TIMEOUT` (padrão 30), definidos no `CMD` por variável | `Dockerfile.prod`, compose |
| `restart` / healthcheck | `unless-stopped` em todos menos `migrar`; healthcheck em db, redis, backend (`/api/health/`) e frontend | compose |
| Logs | `json-file`, `max-size 10m`, `max-file 3` em todos os serviços (teto de 30 MB por serviço) | compose (`x-log`) |
| Limites de memória ou CPU | **nenhum declarado** | compose |
| Build x start | `collectstatic` no build do backend; `migrate` no serviço `migrar` a cada `up`; `npm ci` e `vite build` no build do frontend | Dockerfiles, compose |
| Variáveis obrigatórias | `DJANGO_SECRET_KEY` (≥ 50 caracteres), `DJANGO_ALLOWED_HOSTS` (sem `*`), `DB_DATABASE`, `DB_USER`, `DB_PASSWORD` | `.env.prod.example`, `settings.py` |
| HTTPS | `DJANGO_HTTPS=1` liga redirect, HSTS de 1 ano (com preload), cookies seguros e `SECURE_PROXY_SSL_HEADER`; `/api/health/` fica isento do redirect | `settings.py` |
| IP e proxies | `DJANGO_NUM_PROXIES` (padrão 1); nginx faz `X-Forwarded-For $remote_addr` (sobrescreve) e repassa `X-Forwarded-Proto` do cliente se existir | `settings.py`, `frontend/nginx.conf` |
| Fuso | `TIME_ZONE=America/Sao_Paulo`, `USE_TZ=True`. O contêiner do PostgreSQL e o do backend rodam em UTC (verificado), o que é correto: o Django grava `timestamptz` e converte | `settings.py`, medição |
| Arquitetura | `python:3.12-slim`, `node:24-alpine`, `nginx:1.29-alpine`, `postgres:16-alpine` e `redis:8-alpine` têm `linux/amd64` e `linux/arm64/v8` | `docker buildx imagetools inspect` |

## 2. Medições

**Ambiente (viés a considerar):** Docker Desktop 29.8 no Windows 10, VM WSL2 com 4 vCPU e 8 GB, amd64. O gerador de carga (script Python com threads) rodou na mesma máquina, falando com o nginx pela porta publicada no Windows. Não é uma VPS: latências e CPU absolutas podem diferir. Projeto isolado `cc-medicao` (cópia do compose com nomes trocados, porta 18080), segredos aleatórios, limites de login e cadastro elevados **só no arquivo de variáveis temporário** (nenhum código alterado). Dados 100% fictícios.

| Medida | Valor | Como foi medido |
|---|---|---|
| Imagem do backend | 300 MB | `docker images` |
| Imagem do frontend (nginx + estáticos) | 93,1 MB | `docker images` |
| Imagens base de runtime | postgres:16-alpine 420 MB, redis:8-alpine 162 MB | `docker images` |
| Contexto de build enviado | backend 13,3 kB, frontend 102,4 kB | saída do BuildKit |
| Build sem cache (backend, `migrar` e frontend, 1 build) | **102 s**, com a rede de pacotes disponível | cronometrado |
| Queda máxima da memória disponível da VM durante o build | **cerca de 650 MiB** (7,34 para 6,68 GB), amostrada a cada 1 s; inclui cache de página e outros processos da VM, então é uma ordem de grandeza e não o pico exato do `npm ci` e do `vite build` | `MemAvailable` de `/proc/meminfo` numa amostragem em contêiner |
| RAM ociosa, aquecido por ~4 min | frontend 7,2 MiB, backend 180,4 MiB, redis 8,1 MiB, db 61,2 MiB. **Soma 257 MiB**. CPU de 0 a 5% | `docker stats --no-stream`, 3 leituras |
| Carga A: 20 usuários, 60 s, ~62 req/s | picos de RAM: backend 205,5 / db 82,1 / redis 8,6 / frontend 8,5 MiB (**soma 305 MiB**). Picos de CPU: backend 291%, db 138% (porcentagem de um núcleo) | `docker stats` em laço, 2 s |
| Latência da carga A (sem saturação) | listar espaços: mediana 64 ms, p95 181 ms; agenda do dia: 78 / 204 ms; listar reservas: 74 / 179 ms; criar reserva: 95 / 188 ms. Sem erros 5xx. Os 282 `409` em 538 criações são conflitos de horário esperados (os usuários repetem horários). Login: mediana 2,4 s, p95 4,2 s com 20 logins simultâneos no começo (PBKDF2 do Django) | script `carga.py` |
| Carga B: 40 usuários, 90 s, ~44 req/s | picos de RAM: backend 209,8 / db 82,7 (soma **310 MiB**). Com 3 workers síncronos, a CPU saturou: mediana de ~540 ms por requisição, p95 de ~870 ms, login p95 11,4 s. **0 erros** em 4.143 requisições (todas 200/201) | idem |
| Tamanho do banco | só schema e 201 usuários: 9,22 MB. Com 10 mil reservas e 30 mil registros de histórico (3 por reserva): **18,14 MB** | `pg_database_size` |
| Crescimento do banco por reserva | **cerca de 890 B por reserva** com 3 registros de histórico (reserva e índices 308 B, cada registro 186 B) | `pg_total_relation_size` |
| Disco do volume do PostgreSQL (visão do Docker) | 49,7 MB (vazio) e 75,4 MB (10 mil reservas); o volume inclui WAL | `docker system df -v` |
| Backup do PostgreSQL com 10 mil reservas | `pg_dump` SQL 4,36 MB, SQL com gzip 336 kB, formato custom (`-Fc`) 377 kB | `pg_dump` |
| Redis | 0 chaves 1 min depois da carga; 1,63 MB usados. Guarda só contadores de limite (janela de 1 min a 1 hora) | `redis-cli dbsize` e `info memory` |
| Logs na carga A+B (db e Redis incluídos) | nginx 448 kB e backend 431 kB para ~4.100 requisições (**cerca de 210 B por requisição somando os dois**); db 182 kB; redis 5 kB. O healthcheck de 10 s do backend e do frontend entra nesses números | `docker logs` |

### Estimativas (não medidas)

| Estimativa | Valor | Base |
|---|---|---|
| Disco do banco em 1 ano, dezenas de usuários | **menos de 50 MB** (10 mil reservas ≈ 9 MB acima do schema; com a margem de 5x) | 890 B por reserva medido, mais crescimento de `OutstandingToken` e `BlacklistedToken` (um registro por login e por renovação), cujo tamanho por linha **não foi medido** |
| RAM por worker do gunicorn | cerca de 40 a 50 MiB | 180 MiB com master e 3 workers, divididos por 4 (`ps` não existe na imagem, então não foi medido por processo) |
| Logs sem rotação em um ano | seriam centenas de MB para 20 mil req/dia | 210 B por requisição medido; com a rotação do compose, o teto é de 30 MB por serviço |
| Banda mensal | abaixo de 10 GB para dezenas de usuários | o tamanho dos estáticos da tela **não foi medido**; é um palpite para esse perfil de uso |
| Desempenho em ARM e em VPS real | desconhecido | não foi testado |
| RAM do SO, do Docker Engine e do proxy | SO 300 a 400 MB, Docker 100 a 150 MB, Caddy 20 a 40 MB | conhecimento geral, não medido aqui |

## 3. Dimensionamento recomendado

| | Mínimo viável | Recomendado |
|---|---|---|
| vCPU | 1 | 2 |
| RAM | 1 GB + 2 GB de swap (o stack usa ~310 MiB; o resto é SO, Docker e proxy) | 2 GB (cabe o build no servidor, que pede cerca de 650 MiB extras) |
| Swap | 2 GB | 2 GB |
| SSD | 25 GB: SO e Docker ~8 GB, imagens ~1 GB, cache de build ~3 GB (estimativa), volume do banco < 0,1 GB, logs ≤ 0,15 GB, backups locais ~1 GB | 40 GB: mesma conta com folga para vários backups e atualizações de imagem |
| Banda | pouca (estimativa acima de 10 GB/mês é improvável) | idem |
| Arquitetura | amd64 | amd64 ou arm64 (imagens multi-arch; build em ARM a validar) |
| Workers do gunicorn | 2 | 3 (padrão atual); regra geral 2 x vCPU + 1 |
| Onde construir as imagens | fora do servidor (máquina do Max ou CI), publicando num registro ou transferindo com `docker save`/`docker load` | no servidor, se houver 2 GB |

Observação de carga: na medição, 3 workers síncronos com 4 vCPU saturaram com 40 usuários em atividade contínua (um pedido a cada 0,3 a 1,2 s por usuário). Uma turma real usa o sistema muito mais devagar do que esse script, então 20 usuários a esse ritmo é um cenário pessimista. Com 1 vCPU, o login (PBKDF2) é o ponto mais caro: espere logins lentos se vários entrarem juntos.

**Banco gerenciado ou contêiner?** O banco tem cerca de 18 MB e 60 a 80 MiB de RAM: o contêiner basta, e o gerenciado só se justifica se o Max quiser backups e atualizações prontos, ao custo de uma cobrança mensal e de mais um serviço para configurar. Se o contêiner for mantido, o backup é obrigação nossa (ver lacunas).

## 4. Software e configuração do servidor

**Obrigatório**

- **Sistema operacional:** Ubuntu Server 24.04 LTS (ou Debian estável). Suporte de longo prazo e pacote do Docker mantido pela Docker Inc. para os dois.
- **Docker Engine e plugin do Compose**, do repositório oficial da Docker. O compose usa `name:` no topo, `depends_on` com `condition: service_healthy` e `service_completed_successfully` e `healthcheck`. A versão mínima exata **não foi testada**; o repositório foi validado com Docker 29.8 e Compose 5.5.1. Use as versões atuais do repositório oficial.
- **Proxy reverso com HTTPS e certificado automático** (o compose não termina TLS). Comparação: **Caddy** emite e renova o certificado sozinho, com um `Caddyfile` de poucas linhas, e já envia `X-Forwarded-For` e `X-Forwarded-Proto`; **Traefik** faz o mesmo, mas pede mais configuração (rótulos ou arquivo dinâmico); **nginx + certbot** é conhecido, mas o renovar e o recarregar são peças separadas. **Recomendado: Caddy** instalado no host, escutando 80 e 443 e repassando para `127.0.0.1:8080`. O que isso exige:
  - publicar o nginx do compose só em `127.0.0.1` (`"127.0.0.1:8080:80"`);
  - no nginx do compose, `set_real_ip_from` com a rede do Docker, `real_ip_header X-Forwarded-For` e `real_ip_recursive off`, para que `$remote_addr` seja o IP do cliente. Sem isso, o limite por IP vira um balde único;
  - manter `DJANGO_NUM_PROXIES=1` (o nginx é o único proxy que o Django enxerga, porque o nginx sobrescreve o cabeçalho com um IP só); `DJANGO_HTTPS=1` e `DJANGO_CSRF_TRUSTED_ORIGINS=https://<domínio>`;
  - `DJANGO_ALLOWED_HOSTS` com o domínio.
- **Firewall** liberando só 22, 80 e 443. Atenção: portas publicadas pelo Docker **contornam o `ufw`**, por isso o item acima de publicar o compose em `127.0.0.1` é obrigatório, e não só uma boa prática.
- **Usuário sem root com `sudo`, SSH somente por chave** (login de root e senha desligados).
- **Sincronização de horário (chrony ou `systemd-timesyncd`)**: a expiração dos JWT (access de 30 min, refresh de 1 dia), os horários de reserva (07:00 a 00:00, fechamento 00:00 = 24:00) e a janela de 1 min do limite de tentativas dependem do relógio. Sem NTP, o relógio deriva e os tokens podem expirar cedo ou tarde.
- **Backup agendado** (cron ou timer do systemd) do PostgreSQL com `pg_dump -Fc` (377 kB no exemplo), retenção definida e **cópia para fora da VPS**. Backup só na mesma máquina não protege contra a perda dela.
- **DNS**: domínio ou subdomínio com registro A (e AAAA se houver IPv6) apontando para a VPS, com 80 e 443 abertas para o desafio do certificado.
- **Forma de enviar o código**: `git` com chave de leitura (deploy key), ou `rsync`/ZIP.

**Recomendado**

- `fail2ban` para o SSH; `unattended-upgrades` com atualizações de segurança.
- `curl` e `jq` (verificar `/api/health/` e ler as respostas da API); `make` só se o runbook for escrito com ele.
- Monitoramento externo gratuito de `GET /api/health/` (200 com banco e cache no ar; 503 `BANCO_INDISPONIVEL` ou `CACHE_INDISPONIVEL`) e alerta de disco.
- Rotação de logs: a do compose (10 MB x 3) já limita os contêineres; falta apenas a do host para o `journald` e o Caddy.
- Limites `mem_limit` nos serviços, quando a VPS for pequena.

**O projeto não precisa de:** servidor de e-mail (notificações estão fora do 1.0 por DEC-24), fila de tarefas, CDN, balanceador, segundo servidor, nem Redis persistente. Quando o Redis reinicia, os contadores de limite recomeçam do zero: o efeito é só reabrir a janela de tentativas; ele **não precisa entrar no backup**, basta documentar isso. Se o Redis estiver fora do ar, login e cadastro respondem 503 em vez de liberar (comportamento da AUT-08).

## 5. Lacunas e riscos do repositório

| # | Lacuna | Efeito | Onde se encaixa |
|---|---|---|---|
| 1 | O nginx do compose usa `X-Forwarded-For $remote_addr`, sem `real_ip` | atrás do Caddy, todos os clientes têm o mesmo IP para o limite por IP (AUT-08); 20 logins/min no total, e 10 cadastros/h no total | **INF-09** (configuração do nginx) |
| 2 | Porta publicada em todas as interfaces (`"8080:80"`) | o site fica acessível por HTTP direto, sem TLS, e o `ufw` não bloqueia (Docker usa iptables próprios); além disso, o `X-Forwarded-Proto` do cliente é aceito pelo `map` do nginx, permitindo forjar o esquema | **INF-09** (bind em `127.0.0.1`, em um override ou no compose) |
| 3 | Sem backup, sem rotina de restauração e sem teste de restauração | perda total se a VPS ou o volume forem perdidos | **INF-09** (script e cron) e documentação |
| 4 | Sem `mem_limit` nem `cpus` nos serviços | um serviço descontrolado pode derrubar uma VPS de 1 GB | INF-09, opcional |
| 5 | O build depende de rede (Docker Hub, npm, PyPI) | build no servidor falha sem acesso; o fallback é construir fora e transferir | INF-09 (decisão de onde construir) |
| 6 | `.env.prod.example` não menciona o par `DJANGO_HTTPS=1` com `DJANGO_CSRF_TRUSTED_ORIGINS` como obrigatório junto para o `/admin/`, nem a relação com o `real_ip` do nginx | configuração incompleta atrás do proxy | só documentação (README do módulo e runbook) |
| 7 | O primeiro Gestor é criado com `createsuperuser` interativo em `docker compose exec`, e a migração roda pelo serviço `migrar` a cada `up` | procedimento existe no README; falta amarrar ao runbook da VPS | só documentação |
| 8 | HSTS com `preload` e 1 ano ligados por `DJANGO_HTTPS=1` | difícil de desfazer se o domínio ou o certificado forem trocados; ligar só quando o domínio for definitivo | documentação (aviso no runbook) |
| 9 | Contadores de `OutstandingToken` crescem sem limpeza automática | crescimento lento do banco; há o comando `flushexpiredtokens` | documentação ou um cron na INF-09 |
| 10 | O healthcheck e os logs de acesso do gunicorn registram os healthchecks a cada 10 s | ruído nos logs | irrelevante, só observação |

## 6. O que só o Max sabe

1. Já existe uma VPS ou será contratada? Qual provedor e plano você prefere?
2. Qual o orçamento mensal máximo?
3. Qual região? (para o Rio Grande do Sul, a latência favorece São Paulo.)
4. Existe um domínio ou subdomínio disponível? Quem controla o DNS?
5. Onde guardar os backups fora do servidor (outro provedor, armazenamento de objetos, seu computador)? Por quanto tempo reter?
6. Que disponibilidade se espera? O professor roda só localmente com `docker compose up`; a VPS precisa estar no ar o tempo todo, ou só para a demonstração?
7. O build será feito no servidor ou na sua máquina (o que muda a RAM mínima)?
