# Evidências do Redis para o artigo e o vídeo (DOC-02)

Saídas **reais** de comandos rodados contra o compose do projeto, reunidas por seção do artigo. Nada foi escrito à mão nem "limpo": cada `.txt` abre com um cabeçalho `#` (comando, data e hora, commit, versão do Redis, modo) e traz a saída crua. Os `.json` levam o cabeçalho no objeto `_origem`. Os `.md` desta pasta são consolidações e dizem de onde vêm. Os números de desempenho **não foram remedidos**: vêm de [`../rds-10-ocupacao-redis-vs-postgres.md`](../rds-10-ocupacao-redis-vs-postgres.md).

**Convenção:** a pasta `docs/evidencias/` já existia (só com a RDS-10); esta fica numa subpasta `artigo-redis/`. A numeração `2-x-` segue o esboço do artigo e pode ser renumerada pela ART-01; este índice é o mapa.

## Ambiente e versão

| Item | Valor |
|---|---|
| Data da coleta | 26/11/2026 (cada cabeçalho traz a hora do seu comando) |
| Commit do código | `de351d0` (branch `docs/DOC-02-evidencias-do-artigo`), sem alterações locais em `src/`, `scripts/` e `docs/fontes/` |
| Sistema | Windows 10 Pro 10.0.19045; Docker 29.8.0 (Docker Desktop/WSL 2); Git Bash e PowerShell 5.1 |
| Redis | 8.10.3 (imagem `redis:8-alpine`), Linux 6.18.58 x86_64, standalone |
| PostgreSQL | 16.15 |
| Python / Django | 3.12.16 / 5.2.18 (container do backend) |
| Dados | `carregar_dados_exemplo` (3 usuários de exemplo) mais um usuário e um espaço de teste que já estavam no banco de desenvolvimento (ver "Dados pessoais") |

**Dados pessoais:** o banco de desenvolvimento tem um usuário que não é de exemplo e um espaço de teste. Nenhuma coleta o expõe: as respostas de API usam o perfil de exemplo e só contêm reservas dos usuários de exemplo; nenhum arquivo traz o e-mail ou a matrícula dele. Nenhuma troca por `<NOME>`/`<MATRICULA>` foi necessária. **Tokens:** nenhum token foi gravado; onde um comando os usa, o cabeçalho mostra `<TOKEN-REMOVIDO>` ou a variável (`$TS`, `$TG`) sem valor.

## Índice

Modo: **padrão** = Redis sem persistência (`--save "" --appendonly no`).

| Arquivo | Seção | O que prova | O que NÃO prova | Modo |
|---|---|---|---|---|
| `2-1-redis-no-container.txt` | 2.1 | A versão do Redis e a configuração com que o container roda (`save ""`, `appendonly no`, `noeviction`, porta sem publicação no host) | Desempenho ou limites do Redis em geral; só mostra este container | padrão |
| `2-2-comandos-por-estrutura.txt` | 2.2 | Um exemplo real por estrutura (Sorted Set, Set, Hash, String), com `TYPE`, `OBJECT ENCODING`, `MEMORY USAGE` e `TTL`, no modelo do app | Que são as melhores estruturas possíveis; os encodings valem para este tamanho de dados | padrão |
| `2-2-scan-e-contagem-por-familia.txt` | 2.2 / 2.5 | `SCAN` com cursor até 0, `--scan --pattern`, contagem por família sem `KEYS`; as chaves do limite de tentativas aparecem no mesmo banco 0 | Comportamento do `SCAN` com milhões de chaves | padrão |
| `2-3-persistencia-padrao-e-aof.txt` | 2.3 / 2.7 | No padrão, o `restart` zera o `DBSIZE` e a reconstrução o recupera; com AOF everysec, o `DBSIZE` e as chaves sobrevivem a `restart` e a `kill -9`; depois, volta ao padrão e remove o volume do AOF | Durabilidade sob falha de disco ou de energia; o `kill -9` foi dado 3 s depois da gravação (acima do `everysec`) | padrão → AOF → padrão |
| `2-3-rdb-experimento-isolado.txt` | 2.3 | Num Redis descartável com `--save 60 1`: o RDB restaura no reinício limpo, e uma gravação **depois** do último snapshot se perde com `kill -9` | Que o app usa RDB (não usa); o tamanho exato da janela de perda (o experimento mostra um caso, não um tempo) | experimento isolado, fora do compose |
| `2-4-arquitetura-em-numeros-reais.txt` | 2.4 / 2.6 | Onde ficam as chaves e os 10 `register_script` (Lua), as camadas de uma criação de reserva com `arquivo:linha`, e os 11 contratos do import-linter mantidos | Que o código é correto, só que as dependências respeitam os contratos | padrão |
| `2-5-quadro-de-modelagem.md` | 2.5 | Quadro família × tipo × encoding × TTL × fonte, conferido com a DOC-01 | Nada além das saídas 2-2 que o alimentam (é consolidado à mão a partir delas) | padrão |
| `2-6-reconstrucao-antes-e-depois.txt` | 2.6 | As 3 linhas do `reconstruir_agenda_redis`, rodado 2 vezes, e o estado antes e depois (as projeções apagadas por padrão voltam; `espaco:*` e limites ficam) | Tempo da reconstrução em escala (6 s aqui incluem a partida do Python; ver RDS-10 para 20.000 reservas) | padrão |
| `2-6-redis-nunca-decide.txt` | 2.6 | Com a reserva removida da agenda por `ZREM`, a ocupação mostra o horário livre, a nova reserva no mesmo horário recebe 409 do PostgreSQL, e a reconstrução corrige a leitura | Concorrência real (isso é `2-7-testes-do-redis-subconjunto.txt`); só um caso manual | padrão |
| `2-6-dia-nao-projetado-a-leitura-repovoa.txt` | 2.6 (apoio) | **Tentativa anterior**, mantida de propósito: com o dia ainda não projetado, o `ZREM` devolve 0 e a leitura repovoa o dia a partir do PostgreSQL | Que o teste do "nunca decide" falhou; só mostra que o dia precisa estar projetado antes do `ZREM` (`2-6-redis-nunca-decide.txt` corrige isso no passo 0) | padrão |
| `2-7-api-ocupacao-do-dia.json`, `2-7-api-fila-de-pendentes.json`, `2-7-api-contagem-por-situacao.json`, `2-7-api-ranking-de-espacos.json`, `2-7-api-espaco-cache.json` | 2.7 | Cada resposta completa com a projeção presente e com a chave da projeção apagada (só ela): HTTP e corpo **idênticos** (`comparacao`) | Que o tempo é igual (os tempos gravados são informativos, de uma chamada) nem que vale com projeção parcial | padrão |
| `2-7-falha-do-redis-por-caminho.txt` | 2.7 | Com o Redis parado: 5 leituras 200 com o mesmo MD5 do corpo, criação 201 e salva, login 503 `SERVICO_INDISPONIVEL`, health 503 `CACHE_INDISPONIVEL`, avisos no log, e a reconstrução ao religar; tempos com e sem Redis | Que o fallback é rápido: leva de 3 a 11 s por leitura (nome `redis` não resolve, tentativas e *timeouts*) | padrão (Redis parado e religado) |
| `2-7-testes-do-redis-subconjunto.txt` | 2.7 | 462 testes de 21 arquivos do Redis passam (154 s), incluindo concorrência de criação (uma só reserva) e "projeção não decide"; cobertura dos adaptadores Redis em 100% | A cobertura nem o resultado da suíte inteira (91% é do subconjunto em `infrastructure`) | padrão |
| `2-7-qualidade-ruff.txt` | 2.7 | `ruff check` e `ruff format --check` limpos **na árvore de trabalho, depois de `# noqa: F401` nos 3 imports da fixture `redis_limpo_depois`** (sem a correção, `ruff check` acusava 3 F401 no commit `de351d0`) | Que o commit `de351d0` sozinho passa; a correção está só na árvore de trabalho, sem commit | padrão |
| `2-7-rds-10-tabela-para-o-artigo.md` | 2.7 | Cópia, linha a linha, dos números da RDS-10 e das ressalvas do original (conferida por programa) | Desempenho em produção; é máquina única, em processo, sem rede, e o ganho é de milissegundos | padrão (medido em 25/11) |
| `demonstracao-comandos.md` | vídeo | Sequência copiável (PowerShell e bash) com tempos reais de um ensaio de 80,5 s | O `docker compose up` a frio, a fala e o tempo de edição | padrão e AOF |
| `trechos-para-o-artigo.md` | todas | Recortes curtos prontos para quadros, com legenda | Nada além dos arquivos citados | — |

## O que a coleta mostrou de inesperado

1. **Fallback lento:** com o Redis parado, as leituras que deveriam "só ler do PostgreSQL" levam de 3,3 a 11,4 s (contra 0,03 a 0,06 s com ele), e o login com 503 leva ~8 s. O conteúdo é igual, mas o tempo muda muito; a DOC-01 (6.4) diz "200, o mesmo conteúdo" sem citar o tempo. **Causa medida:** não são os *timeouts* do cache (já são de 1 s em `config/settings.py:177`): com o container parado o nome `redis` deixa de resolver, e `socket.getaddrinfo('redis', 6379)` falha em 3,3 s (8,1 s na primeira chamada) em cada tentativa; uma leitura toca o Redis de 1 a 3 vezes. Reduzir isso exigiria evitar novas tentativas na mesma requisição depois da primeira falha (mudança de projeto, não feita).
2. **`ruff check` com 3 erros F401** em `test_falhas_do_redis.py`, `test_projecao_nao_decide_conflito.py` e `test_reconstrucao_com_escritas_no_meio.py` (importação de `redis_limpo_depois`). **Corrigido a pedido** com `# noqa: F401`, a convenção que `test_concorrencia_de_criacao.py` já usava; os 14 testes dos 3 arquivos passam. A correção é uma alteração de código **fora da pasta de evidências**, a entrar em commit à parte.
3. **Senha do Gestor:** o login de `carla.mendes@exemplo.com` com a senha do README foi recusado no banco de desenvolvimento. O token do Gestor foi emitido pelo Simple JWT no container (sem alterar a senha). O README da raiz e o banco de desenvolvimento divergem nesse ponto.
4. **`agenda:versao:...` só existe depois de uma escrita** (ver `2-5-quadro-de-modelagem.md`); e o padrão `agenda:*` a inclui.
5. **A DOC-01 e a DEC-28 batem** com o que o Redis mostrou (tipos, TTLs, `montado`, versões); nenhum nome, tipo ou TTL divergente foi encontrado.
6. **Não há medição do cache de espaço (RDS-11):** o `scripts/medir_desempenho.py` ganhou o cenário `REDIS_ACERTO_SEM_CACHE_DE_ESPACO` no merge `c772d9f`, mas nenhum relatório com o resultado foi versionado.

## Como regerar

Depois do congelamento do código (29/11), se algo mudar. Confira antes o hash: `git rev-parse --short HEAD` deve ser o do código entregue; se for outro, os cabeçalhos desta pasta estão defasados.

1. Subir o ambiente no modo padrão a partir de `src/`: `docker compose up -d`; conferir `docker compose exec redis redis-cli INFO server`.
2. `docker compose exec backend python manage.py carregar_dados_exemplo` e `docker compose exec backend python manage.py reconstruir_agenda_redis`.
3. Obter um token por perfil (um login por perfil; o limite de tentativas é 5/min por e-mail) e guardá-lo só em variável de shell.
4. Refazer, nesta ordem, os comandos que cada cabeçalho `# Comando:` lista: `2-1`, `2-2`, `2-2-scan`, `2-6-reconstrucao`, `2-6-redis-nunca-decide`, as cinco respostas `2-7-api-*` (chamada normal e com `UNLINK` da chave da projeção), `2-7-falha-do-redis-por-caminho` (reservas de teste canceladas ao fim), `2-3-persistencia-padrao-e-aof` (termina removendo `conecta-campus_redis_data`, **só se foi criado pela coleta**), `2-3-rdb-experimento-isolado`, `2-4-arquitetura`.
5. Testes: `docker compose exec backend pytest <os 21 arquivos listados no cabeçalho de 2-7-testes-do-redis-subconjunto.txt> --no-cov -q`; `lint-imports`; `ruff check .` e `ruff format --check .`.
6. Reensaiar `demonstracao-comandos.md` e atualizar os tempos.
7. A `2-7-rds-10-tabela-para-o-artigo.md` só muda se o relatório da RDS-10 mudar (reexecutar a conferência por programa do fim do arquivo).
8. Terminar com o Redis no modo padrão (`aof_enabled:0`), sem volume `conecta-campus_redis_data`, projeções reconstruídas e as reservas de teste canceladas (nunca apagadas).
9. Rodar `grep` por `eyJ`, `Bearer `, `senha`, e-mails e matrículas antes de commitar.

**Segredos e limites:** nenhum token, senha de usuário ou `.env` foi gravado; o `senha` que aparece em alguns cabeçalhos é a chave do JSON de um login com e-mail fictício e senha `x`. A coleta não rodou a suíte completa (14 min 40 s, 2276 testes e 99,77% de cobertura são a **linha de base conhecida, histórica**, não resultado desta tarefa).
