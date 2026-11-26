# Trechos curtos para os quadros do artigo (DOC-02)

Cada trecho é um recorte literal (com `...` onde cortado) da evidência indicada, com sugestão de legenda. A ART-01 decide o que usar; nada aqui afirma mais do que a evidência prova (ver "o que NÃO prova" no [índice](README.md)).

## 2.1 — O Redis que o container executa
Fonte: `2-1-redis-no-container.txt`
```
redis_version:8.10.3     redis_mode:standalone     tcp_port:6379
["redis-server","--save","","--appendonly","no"]
appendonly no     save ""     maxmemory-policy noeviction
```
Legenda sugerida: "Quadro: versão e configuração do Redis no modo padrão do projeto (sem persistência)."

## 2.2 — Um exemplo por estrutura
Fonte: `2-2-comandos-por-estrutura.txt`
```
> ZRANGE conecta-campus:1:agenda:espaco:5:2026-12-01 0 -1 WITHSCORES
_  -1 | 17:600:CONFIRMADA  540 | 18:780:SOLICITADA  720
> SCARD (CONFIRMADA)  3      > HGETALL espaco:1  nome, tipo, capacidade, ativo...
> ZREVRANGE ranking:espacos 0 -1 WITHSCORES   (ids 5,2,1 com 2,1,1)
```
Legenda sugerida: "Quadro: Sorted Set da agenda (score = início em minutos), Set por situação, Hash do espaço e Sorted Set do ranking."

## 2.2 — Tipos, encodings e tamanhos
Fonte: `2-2-comandos-por-estrutura.txt`
```
agenda:espaco:5:2026-12-01   zset   listpack  129 bytes  ttl=604988
reservas:situacao:CONFIRMADA set    intset     88 bytes  ttl=-1
espaco:1                     hash   listpack  196 bytes  ttl=85
```
Legenda sugerida: "Quadro: tipo, codificação interna, memória e TTL de uma chave de cada família, com os dados de exemplo."

## 2.2 / 2.5 — Varredura com SCAN
Fonte: `2-2-scan-e-contagem-por-familia.txt`
```
> SCAN 0 MATCH conecta-campus:1:espaco:* COUNT 4   -> 12
> SCAN 12 ... -> 26      > SCAN 26 ... -> 27      > SCAN 27 ... -> 0
agenda: 1   espaco: 3   reservas: 8   ranking: 4   throttle_: 2   TOTAL 18
```
Legenda sugerida: "Quadro: SCAN com COUNT pequeno exige várias voltas até o cursor 0; contagem de chaves por família."

## 2.3 — Persistência: padrão × AOF
Fonte: `2-3-persistencia-padrao-e-aof.txt`
```
padrão  restart: DBSIZE=0   -> reconstruir: DBSIZE=11
AOF     reconstruir: DBSIZE=11 -> restart: 11 -> kill -9 + start: 11
        aof_enabled:1  aof_last_write_status:ok
```
Legenda sugerida: "Quadro: reinício do Redis sem persistência (perde as projeções) e com AOF everysec (mantém)."

## 2.3 — Persistência: janela de perda do RDB (experimento isolado)
Fonte: `2-3-rdb-experimento-isolado.txt`
```
--save 60 1   BGSAVE -> rdb_changes_since_last_save:0 ; dump.rdb 221 bytes
docker restart (limpo)       -> DBSIZE=3  (chaves voltam)
SET depois do snapshot + kill -9 -> DBSIZE=3 ; chave:depois_do_snapshot vazia (perdida)
```
Legenda sugerida: "Quadro: com RDB, a gravação feita depois do último snapshot se perde numa parada brusca (experimento fora do compose)."

## 2.6 — Reconstrução idempotente
Fonte: `2-6-reconstrucao-antes-e-depois.txt`
```
Agenda reconstruída: 1 dia, 2 reservas, 0 dias esvaziados.
Filas e contagens reconstruídas: 10 reservas, 1 pendente.
Ranking de espaços reconstruído: 3 espaços, 4 reservas contadas.
(2ª execução: as mesmas 3 linhas; DBSIZE 12 antes e depois)
```
Legenda sugerida: "Quadro: saída do comando de reconstrução, repetido sem alterar o resultado."

## 2.6 — O Redis não decide conflito
Fonte: `2-6-redis-nunca-decide.txt`
```
ZREM ...:2026-12-03 20:960:SOLICITADA   -> 1   (projeção sem a reserva)
GET ocupacao  -> "Nenhum horário ocupado neste dia."
POST reserva no mesmo horário -> HTTP 409 CONFLITO_DE_HORARIO
reconstruir_agenda_redis -> projeção volta; ocupação mostra 15:00-16:00
```
Legenda sugerida: "Quadro: com a projeção adulterada, a criação concorrente ainda é recusada pelo PostgreSQL; a reconstrução corrige a leitura."

## 2.7 — Resposta idêntica com e sem a projeção
Fonte: `2-7-api-*.json` (campo `comparacao`)
```
ocupacao-do-dia   http 200/200  corpos_identicos: true
fila-de-pendentes http 200/200  corpos_identicos: true
contagem-por-situacao ... true   ranking-de-espacos ... true   espaco-cache ... true
```
Legenda sugerida: "Quadro: as cinco leituras devolvem o mesmo corpo com a projeção presente e com a chave apagada."

## 2.7 — Redis parado, por caminho
Fonte: `2-7-falha-do-redis-por-caminho.txt`
```
leituras (5)  -> HTTP 200, mesmo md5 do corpo, 3,3 a 11,4 s (com Redis: 0,03 a 0,06 s)
POST reserva  -> HTTP 201, salva (GET 200)
POST login    -> HTTP 503 SERVICO_INDISPONIVEL      GET /health/ -> 503 CACHE_INDISPONIVEL
```
Legenda sugerida: "Quadro: consultas e criação seguem funcionando sem o Redis (mais lentas); login e health falham fechados."

## 2.7 — Testes do Redis (subconjunto)
Fonte: `2-7-testes-do-redis-subconjunto.txt`
```
462 passed in 154.17s   (21 arquivos; subconjunto, não a suíte inteira)
test_criacoes_simultaneas_no_mesmo_horario_deixam_so_uma_reserva[com_projecao|sem_projecao] PASSED
test_projecao_que_diz_livre_nao_impede_o_conflito_e_a_reconstrucao_a_corrige PASSED
```
Legenda sugerida: "Quadro: testes das projeções do Redis, incluindo a concorrência de criação e a projeção que não decide."

## 2.7 — Medição da RDS-10
Fonte: `2-7-rds-10-tabela-para-o-artigo.md` (cópia do relatório original)
```
| 1.000 | a | +3,96 ms [+2,74; +5,25] | +2,56 ms [+2,06; +3,13] | 207 → 310 req/s |
| 20.000 | a | +4,40 ms [+4,08; +4,70] | +3,70 ms [+3,50; +3,84] | 293 → 624 req/s |
(diferença das medianas, PG − acerto do Redis; IC 95%; máquina única, em processo, sem rede)
```
Legenda sugerida: "Quadro: diferença das medianas da ocupação do dia sem e com acerto no Redis (medição da RDS-10; ver limites)."

## 2.4 / 2.6 — Arquitetura em números
Fonte: `2-4-arquitetura-em-numeros-reais.txt`
```
10 chamadas register_script (10 scripts Lua) em 5 arquivos; 11 contratos do import-linter mantidos
"Domínio e aplicação não conhecem o Redis" KEPT
```
Legenda sugerida: "Quadro: contagem de scripts Lua e resultado do contrato que mantém o Redis fora do domínio e da aplicação."
