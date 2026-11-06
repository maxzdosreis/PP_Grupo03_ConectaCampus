# Checklist de reprodutibilidade do README — Conecta Campus

| Identificação | Responsabilidade | Fonte |
|---|---|---|
| **REP-01 • 0.1 • Rascunho** | Autor: [nome] • Revisor: [nome] • Aprovador: [nome] | `docs/fontes/checklist-reprodutibilidade.md` (fora do ZIP) |

Roteiro do critério de sucesso CS-03 da [Visão](requisitos/visao.md): **um integrante que não escreveu o README** executa o sistema num clone novo (ou no ZIP da entrega), seguindo **só** o `README.md` da raiz, sem ajuda, até entrar com os usuários de teste. Cada linha é um passo do README, na ordem dele. Marque **ok?** com ✔ ou ✘ e anote em **observação** tudo o que precisou adivinhar, perguntar ou corrigir: cada ✘ vira uma correção no README (DOC-05) ou uma pendência abaixo.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Criação do roteiro e rodada 1, executada pelo assistente de IA num projeto Compose separado (DOC-05). A rodada do CS-03 por um integrante fica para a DOC-07. Sem aprovação. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | P-1 e P-4 resolvidas (portas da API e da tela configuráveis; `127.0.0.1` no CORS do exemplo); passos 4 e 19 ajustados. A rodada 1 ficou como foi feita, antes da correção. Sem aprovação. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | P-5 resolvida (INF-07): `VITE_API_URL` e `CORS_ALLOWED_ORIGINS` derivadas das portas no `docker-compose.yml`, fora do `.env`; passos 1, 4 e 19 ajustados; notas em P-1 e P-4. Sem aprovação. |

## Como executar a rodada

- Use uma pasta nova: um clone novo (`git clone`) ou o ZIP gerado para a entrega, extraído. Não use a pasta em que você trabalha.
- **Proteja o seu banco:** o `docker-compose.yml` fixa o nome do projeto (`conecta-campus`), então outra cópia usa os mesmos containers e o mesmo volume. Se você já tem o projeto rodando, pare-o antes com `docker compose stop` (sem `-v`) e **não** rode `docker compose down -v` na cópia de teste: isso apaga os seus dados. Para testar sem tocar neles, acrescente `-p conecta-campus-limpo` a todos os comandos `docker compose` (é o único desvio permitido do README) e, no fim, apague só esse projeto com `docker compose -p conecta-campus-limpo down -v --rmi local`.
- Cronometre do passo 0 ao passo 4 (o tempo total pedido abaixo).

## Rodada

| Campo | Valor |
|---|---|
| Data | |
| Nome de quem executou (não escreveu o README) | |
| Sistema operacional e versão | |
| Terminal usado (Git Bash, PowerShell, Prompt de Comando, outro) | |
| Docker Desktop / Engine / Compose (`docker version`, `docker compose version`) | |
| Origem da cópia (clone novo ou ZIP; commit ou nome do arquivo) | |
| Tempo total, do passo 0 até entrar como Bruno | |
| Precisou de ajuda? Onde? | |

| # | Passo do README | Resultado esperado | ok? | Observação |
|---|---|---|---|---|
| 1 | Pré-requisitos: Docker Desktop aberto | Ícone do Docker "running" (se uma porta do passo 4 estiver ocupada, a tabela do passo 1 do README pede uma variável só) | | |
| 2 | `docker compose version` | `Docker Compose version v…` | | |
| 3 | `docker version` | Seções Client **e Server**, sem `failed to connect to the docker API` | | |
| 4 | Portas 5173, 8000 e 5432 livres | Nada mais rodando nelas; se alguma estiver ocupada, a tabela do passo 1 do README diz qual variável trocar (uma só por porta: `DB_PORT_HOST`, `BACKEND_PORT_HOST` ou `FRONTEND_PORT_HOST`) | | |
| 5 | Passo 0: extrair o ZIP ou clonar; abrir o terminal na pasta com `README.md`, `src/` e `docs/` | As três entradas aparecem na pasta | | |
| 6 | Passo 1: `cp src/.env.example src/.env` (ou `copy src\.env.example src\.env`) | `src/.env` criado, sem editar nada | | |
| 7 | Passo 2: `cd src` e `docker compose up --build` | Termina com `Starting development server at http://0.0.0.0:8000/` e `Local: http://localhost:5173/`; anote o tempo | | |
| 8 | Passo 3: em outro terminal, em `src`, `docker compose exec backend python manage.py carregar_dados_exemplo` | "Usuários: 3 criados", "Espaços: 6 criados", "Reservas: 5 criadas" e o horário de conflito com a data de amanhã | | |
| 9 | Verificar a API: http://localhost:8000/api/health/ | 200 `{"mensagem": "API no ar.", "dados": {"banco": "ok"}}` | | |
| 10 | Passo 4: http://localhost:5173/entrar como Bruno (`bruno.lima@exemplo.com`, `Rede-Alta-73`) | "Minhas reservas" com 3 reservas; cabeçalho "Bruno Lima · Solicitante" | | |
| 11 | Sair e entrar como Carla (`carla.mendes@exemplo.com`, `Apito-Dourado-48`) | Cabeçalho "Carla Mendes · Gestor"; "Reservas" com 5 reservas | | |
| 12 | Roteiro, passo 3: Quadra Poliesportiva Central, amanhã, 10:30–11:30 | Aviso de conflito de horário (409 `CONFLITO_DE_HORARIO`) e os valores continuam no formulário | | |
| 13 | Roteiro, passo 6: Bruno em "Espaços" | "Somente o gestor cadastra espaços.", sem formulário | | |
| 14 | Roteiro com `curl` (README do backend): Bruno tenta confirmar | 403 `ACAO_NAO_PERMITIDA` | | |
| 15 | Roteiro completo (passos 1 a 9) em até 10 minutos | Cada passo com a mensagem descrita | | |
| 16 | Parar: `docker compose down`; subir: `docker compose up` | Ao entrar de novo, os mesmos dados (5 reservas para a Carla, mais as criadas no roteiro) | | |
| 17 | Rodar de novo o comando de dados de exemplo | "0 criados, 3 já existiam" (nada duplicado) | | |
| 18 | Recomeçar do zero: `down -v`, `up -d`, comando de dados de exemplo (só no projeto de teste) | Dados recriados: 3 usuários, 6 espaços, 5 reservas | | |
| 19 | Abrir http://127.0.0.1:5173 (ou a porta da `FRONTEND_PORT_HOST`, se foi trocada) | A página inicial mostra "API no ar." e o login funciona, como por `localhost`, sem editar outra variável | | |
| 20 | Os links do README abrem (ZIP ou GitHub) | Nenhum link quebrado | | |

## Pendências que só se resolvem no código ou na infraestrutura

| # | Pendência | Contorno no README | Proposta (tarefa separada) |
|---|---|---|---|
| P-1 | **Resolvida em 06/11/2026.** As portas 8000 e 5173 eram fixas no `docker-compose.yml`. | Tabela de portas no passo 1 do README. | Feito: `"${BACKEND_PORT_HOST:-8000}:8000"` e `"${FRONTEND_PORT_HOST:-5173}:5173"` no compose, as duas no `.env.example` com o aviso de que `VITE_API_URL` e `CORS_ALLOWED_ORIGINS` acompanham a troca (desde a INF-07 elas acompanham sozinhas: ver P-5). Prova: uma cópia com 8001, 5174 e 5433 subiu ao lado do ambiente do integrante (nas portas padrão), com login pela tela; sem as variáveis novas no `.env`, o `docker compose config` publica 8000, 5432 e 5173. |
| P-2 | O nome fixo do projeto (`name: conecta-campus`) faz duas cópias no mesmo computador dividirem containers e volume: um `down -v` numa apaga os dados da outra, e a rodada de teste precisa do `-p`. | Persistência: rodar uma cópia de cada vez. | Avaliar tirar o `name:` (o Compose usaria o nome da pasta, e o volume mudaria para `src_postgres_data`) ou documentar o `-p` como o jeito de testar; mudar o nome muda o volume dos integrantes, então exige aviso e migração dos dados. |
| P-3 | `docker compose version` funciona com o Docker Desktop fechado, então sozinho não prova que o Docker está pronto. | O README pede também `docker version` (parte Server). | Nenhuma mudança de código; registrar no roteiro da DOC-07. |
| P-4 | **Resolvida em 06/11/2026.** A tela só falava com a API quando aberta por `localhost` (CORS). | — | Feito: `CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173` no `.env.example`. Prova: a pré-verificação de CORS do login devolve `Access-Control-Allow-Origin` para as duas origens e nenhum para `http://localhost:9999`; pela tela, `127.0.0.1` mostra "API no ar." e o login do Bruno funciona. Quem já tinha um `src/.env` precisava acrescentar a origem à mão; desde a INF-07 (P-5) não precisa mais, porque o Compose monta as duas origens. |
| P-5 | **Resolvida em 06/11/2026 (INF-07).** Trocar a porta da API ou da tela exigia mudar também `VITE_API_URL` ou `CORS_ALLOWED_ORIGINS` no `.env`; um valor esquecido deixava a tela sem conexão. | — | Feito: o `docker-compose.yml` deriva as duas das portas (`VITE_API_URL: http://localhost:${BACKEND_PORT_HOST:-8000}/api` no `frontend`; `CORS_ALLOWED_ORIGINS: http://localhost:${FRONTEND_PORT_HOST:-5173},http://127.0.0.1:${FRONTEND_PORT_HOST:-5173}` no `environment:` do `backend`, que vence o `env_file`), e elas saíram do `.env.example`. Prova: `docker compose config` com o `.env.example`, com 8001/5174 e com 8001/5174 mais um `.env` antigo (`VITE_API_URL=http://localhost:8000/api`, `CORS_ALLOWED_ORIGINS=http://localhost:5173`) dá sempre os valores derivados; num projeto separado (`-p conecta-campus-portas`, 8001, 5174 e 5433, com esse `.env` antigo), health 200 em 8001, a pré-verificação de CORS do login devolve `Access-Control-Allow-Origin` para `http://localhost:5174` e `http://127.0.0.1:5174` e nenhum para `http://localhost:5173`, o container do backend tem `CORS_ALLOWED_ORIGINS=http://localhost:5174,http://127.0.0.1:5174` e o do frontend `VITE_API_URL=http://localhost:8001/api`; pela tela em http://localhost:5174, o login do Bruno mostra "Minhas reservas" com 3 reservas e o console diz `[vite] connected.` (o HMR não precisou de `hmr.clientPort`). Um `.env` antigo pode ficar como está. |

## Rodada 1 — 06/11/2026 (assistente de IA, durante a DOC-05)

Não vale como CS-03, porque foi feita por quem reescreveu o README. Serve para provar que o README novo funciona do começo ao fim numa cópia igual à do professor.

| Campo | Valor |
|---|---|
| Data | 06/11/2026 |
| Quem executou | Claude Code (assistente de IA), a pedido do grupo |
| Sistema operacional | Windows 10 Pro 10.0.19045 |
| Terminais | Git Bash (passos 1 a 3 da primeira passada) e PowerShell (`copy` da segunda passada); `copy` também conferido no Prompt de Comando |
| Docker | Docker Desktop 4.91.0, Engine 29.8.0, Compose v5.5.1 (WSL 2) |
| Origem da cópia | `git archive HEAD README.md src docs ':!docs/fontes'`, extraído numa pasta nova; na segunda passada, com o README novo copiado por cima. Escolhido em vez de um clone porque é o conteúdo versionado, sem `.env` nem `node_modules`, e com os finais de linha que este checkout (Windows, `core.autocrlf=true`) poria num ZIP: `README.md`, `.env.example` e os `.py` em CRLF; `docker-compose.yml` e `Dockerfile` em LF. |
| Desvio | `-p conecta-campus-limpo` em todos os comandos `docker compose`; o ambiente do integrante foi parado com `docker compose stop` e religado com `docker compose start` |
| Tempo total | Build sem cache: 193 s (imagens base já baixadas); até a API responder: mais 51 s; dados de exemplo: 9 s. Cerca de 4 min do passo 1 ao passo 4. Na segunda passada, com o build em cache: 32 s até a API. |
| Precisou de ajuda? | Não. Duas correções no README vieram da primeira passada (abaixo). |

| # | ok? | Observação |
|---|---|---|
| 1–3 | ✔ | `docker compose version` → v5.5.1; `docker version` → Server 29.8.0. Com o Docker fora do ar (simulado apontando `DOCKER_HOST` para um pipe inexistente), `docker compose version` **continua respondendo**, e só o `docker version` e o `up` falham com `failed to connect to the docker API`: por isso o README pede os dois. |
| 4 | ✔ | Livres depois de parar o ambiente do integrante. Achado: esta máquina tem um PostgreSQL nativo na 5432 (`postgres.exe`), e mesmo assim o Docker publicou a 5432 sem erro; o app não usa a porta do computador, então não houve efeito. |
| 5 | ✔ | Pasta com `README.md`, `docs/` (só `information.md`) e `src/`. |
| 6 | ✔ | `cp` no Git Bash e no PowerShell, `copy` no PowerShell e no Prompt de Comando: os quatro criam o `src/.env`. O `.env` saiu em CRLF e foi lido certo (`DJANGO_DEBUG` = `'True'`). |
| 7 | ✔ | As linhas de pronto do README aparecem; a do Vite vem antes da do Django. |
| 8 | ✔ | 3 usuários, 6 espaços, 5 reservas; "Horário para demonstrar o conflito (409): Quadra Poliesportiva Central, 07/11/2026, 10:30–11:30." |
| 9 | ✔ | 200 `{"mensagem":"API no ar.","dados":{"banco":"ok"}}`. |
| 10 | ✔ | Pela tela (navegador embutido): "Minhas reservas", 3 reservas, "Bruno Lima · Solicitante". Pela API: login do Bruno e da Carla → 200 "Login realizado com sucesso." com `access` e `refresh`. |
| 11 | ✔ | Pela API: Carla (Gestor) vê 5 reservas. |
| 12 | ✔ | Pela API: 409 `CONFLITO_DE_HORARIO` "Este espaço já tem uma reserva Solicitada em 07/11/2026 10:00–11:00. Escolha outro horário.". Transição inválida (concluir a Recusada) → 409 `TRANSICAO_DE_SITUACAO_INVALIDA` "Não é possível alterar uma reserva Recusada para Concluída.". |
| 13 | — | Não executado pela tela nesta rodada (texto conferido no código, `PaginaEspacos.tsx`). |
| 14 | ✔ | Pela API: 403 `ACAO_NAO_PERMITIDA` "Somente o gestor pode confirmar reservas.". |
| 15 | — | Fica para o ensaio da apresentação. |
| 16 | ✔ | `down` + `up -d`: as mesmas 5 reservas. `Ctrl+C` não foi testado (execução sem terminal interativo). |
| 17 | ✔ | "Usuários: 0 criados, 3 já existiam.", o mesmo para espaços e reservas. |
| 18 | ✔ | `down -v` apagou só `conecta-campus-limpo_postgres_data`; depois, 3/6/5 criados de novo. |
| 19 | ✔ | Antes da P-4: em http://127.0.0.1:5173 a página inicial mostrava "Não foi possível conectar ao servidor. Verifique se a API está em execução.". Depois dela, `127.0.0.1` funciona como `localhost` (ver P-4). |
| 20 | ✔ | Verificador de links e âncoras (padrão do GitHub) sobre todos os READMEs da cópia sem `docs/fontes`: sem erro, exceto `docs/modelagem.pdf` e `docs/contribuicoes.pdf`, que só existem depois de gerados na entrega. |

**Problemas comuns reproduzidos** (no projeto de teste):

| Caso | O que apareceu | Bate com o README? |
|---|---|---|
| Porta 8000 ocupada (um `python -m http.server 8000` no Windows) | `Error response from daemon: ports are not available: exposing port TCP 0.0.0.0:8000 -> 127.0.0.1:0: listen tcp 0.0.0.0:8000: bind: Normalmente é permitida apenas uma utilização de cada endereço de soquete (protocolo/endereço de rede/porta).`; o `db` sobe e o `backend` não | ✔ |
| `src/.env` ausente | `error while interpolating services.db.environment.POSTGRES_PASSWORD: required variable DB_PASSWORD is missing a value: defina DB_PASSWORD no .env` (a variável citada varia) | ✔ |
| `.env` sem `DB_PASSWORD` | A mesma mensagem, só para `DB_PASSWORD` | ✔ |
| `DJANGO_DEBUG=False` | `CommandError: Os dados de exemplo só podem ser carregados com DJANGO_DEBUG=True, porque criam usuários com senhas conhecidas.`; a API continua respondendo 200 | ✔ |
| `DB_PORT_HOST=5433` | `db` publicado em `0.0.0.0:5433->5432`, API 200 | ✔ |
| Docker fora do ar (simulado) | `failed to connect to the docker API at npipe:...; check if the path is correct and if the daemon is running` | ✔ |
| Login com e-mail sem cadastro (o mesmo caso de banco sem os dados de exemplo) | 401 `CREDENCIAIS_INVALIDAS` "E-mail ou senha incorretos." | ✔ |
| Cópia com `docker-compose.yml`, os dois `Dockerfile` e o `.env` convertidos para CRLF | `docker compose config` e `build` sem erro; `DJANGO_DEBUG` lido como `'True'` | ✔ (não é problema) |

**Correções no README que saíram desta rodada:** a checagem do Docker passou a ser `docker compose version` **e** `docker version` (só o primeiro passa com o Docker fechado); e o nome do volume passou a ser o real, `conecta-campus_postgres_data` (o README dizia `postgres_data`).

**Volumes:** antes, `conecta-campus_postgres_data`; durante, também `conecta-campus-limpo_postgres_data` e `conecta-campus-crlf_postgres_data`; depois, só `conecta-campus_postgres_data`, intacto (o ambiente do integrante voltou com a API em 200). As imagens de teste foram removidas.
