# RDS-10 — Ocupação do dia com e sem Redis (medição)

Medido em 25/11/2026 com `scripts/medir_desempenho.py` (comando em `CLAUDE.md`). Este é um registro de medição, não uma afirmação geral: leia "Interpretação e limites".

**Ambiente:** Windows 10 Pro (host), Docker Engine 29.8.0 com Docker Desktop/WSL 2, 4 CPUs e 8 GiB para o Docker; container do backend Linux 6.18 x86_64 com Python 3.12.16, Django 5.2.18, PostgreSQL 16.15 e Redis 8.10.3 (modo padrão, sem persistência) em containers próprios. Redis: banco 2 dedicado. Durante as rodadas finais o container do frontend ficou parado (consumia ~42% de CPU) e rodavam apenas db, redis, backend e um container alheio ocioso (`otto-local`, 0% de CPU). Medição em processo, sem rede.

**Método:** 300 chamadas por cenário e nível (5 rodadas de 60, intercaladas e com a ordem girada), 5 de aquecimento; PG = agenda que sempre falha (equivale ao comportamento anterior à RDS-05); REDIS_ACERTO = projeção montada por `reconstruir_agenda` e `reconstruir_indice`; REDIS_ERRO = chave do dia apagada fora do trecho cronometrado antes de cada chamada. Respostas dos três cenários conferidas idênticas antes de medir. IC 95% por bootstrap (2.000 reamostragens, semente fixa) da diferença de medianas; o bootstrap trata as amostras como independentes e ignora o pareamento por rodada. Com 20.000 reservas a carga é em lote (`bulk_create`, sem histórico, o que não afeta a leitura da ocupação); o dia medido tem 6 reservas ativas.

## Resumo (diferença das medianas, PG − acerto do Redis; IC 95%)

| Reservas | Rodada | API | Caso de uso | Vazão com 8 threads (PG → acerto) |
|---|---|---|---|---|
| 1.000 | a | +3,96 ms [+2,74; +5,25] | +2,56 ms [+2,06; +3,13] | 207 → 310 req/s |
| 1.000 | b | +1,50 ms [+1,24; +1,73] | +1,74 ms [+1,63; +1,88] | 267 → 345 req/s |
| 20.000 | a | +4,40 ms [+4,08; +4,70] | +3,70 ms [+3,50; +3,84] | 293 → 624 req/s |
| 20.000 | b | +3,53 ms [+3,30; +3,83] | +3,49 ms [+3,38; +3,62] | 277 → 469 req/s |

O miss (chave apagada) foi de 1,4 a 2,8 ms **mais lento** que o PostgreSQL em todas as rodadas (ICs sem zero). Reconstrução com 20.000 reservas: `reconstruir_agenda` 24,5 s e 29,8 s (2.000 dias, 12.000 reservas), `reconstruir_indice` 0,6 a 0,75 s. Todos os cenários ficaram com p95 ≤ ~30 ms, muito abaixo da meta de 500 ms da DEC-12. O `EXPLAIN` com 20.000 reservas usa o índice `reservas_espaco_inicio_idx` só pelo `espaco_id` (4.000 linhas lidas, 6 mantidas) e leva 2,3 ms.

## Interpretação e limites

Nos dois tamanhos, o acerto do Redis foi mais rápido que o PostgreSQL, com IC que não inclui zero, mas o ganho é de poucos milissegundos (1,5 a 4,4 ms na mediana) sobre uma consulta que já levava de 6 a 10 ms; ele variou entre rodadas do mesmo tamanho (1.000: 1,5 a 4,0 ms), então os ICs de uma rodada subestimam a incerteza real, e só cabe falar em "da ordem de 2 a 4 ms". O ganho em vazão com 8 threads (cerca de 1,3 a 2,1 vezes) também variou muito entre rodadas e vem de um único processo com GIL, na mesma máquina. A meta da DEC-12 já é atendida sem Redis, então nada aqui mostra que ele seja necessário para cumpri-la. O miss é mais lento que o PostgreSQL puro (leitura, versão e gravação extras), e a reconstrução completa leva cerca de meio minuto com 20.000 reservas. Limites: máquina única com Docker Desktop/WSL 2, em processo e sem rede (o custo de ida e volta ao Redis e ao PostgreSQL por rede não está medido); a consulta do espaço continua no PostgreSQL em todos os cenários (por isso o caso de uso do acerto ainda faz 1 consulta SQL); o ganho do caso de uso diminui no total da API; só 6 reservas ativas no dia; sem carga concorrente real além das 8 threads; dados sintéticos e uniformes; planos com a tabela recém-analisada (`ANALYZE`) e totalmente em memória.

## Bancos do Redis

`DBSIZE` dos bancos 0 (desenvolvimento) e 1 (testes): 0 antes e depois em todas as rodadas; `INFO keyspace` vazio no fim; banco 2 esvaziado ao final. Como os bancos 0 e 1 já estavam vazios, isso prova que a medição não criou chaves neles, não que dados existentes foram preservados.

Amostras brutas: `rds-10-amostras-<reservas>_<rodada>.json`.

## Saída completa: 1000_a

- Sistema: Linux-6.18.58.1-microsoft-standard-WSL2-x86_64-with-glibc2.41 (4 CPUs visíveis no container)
- Python 3.12.16, Django 5.2.18, PostgreSQL 16.15
- Redis 8.10.3 (Linux 6.18.58.1-microsoft-standard-WSL2 x86_64), banco 2 dedicado à medição
- Carga: 1000 reservas (repositório, com histórico), 5 espaços, 20 solicitantes (gravadas em 7.1 s); tabela: 384 kB
- Medição: 5 chamadas de aquecimento e 300 medidas por cenário (5 rodadas intercaladas nos cenários de ocupação), pela API em processo (APIClient com token de acesso), sem rede nem navegador

| Cenário | Itens | Resposta | Consultas SQL | Mín | Mediana | p95 | Máx | Meta (p95) | Atende |
|---|---|---|---|---|---|---|---|---|---|
| Consulta: Gestor, sem critério | 20 de 1000 | 9 KiB | 3 | 8.5 ms | 16.3 ms | 33.2 ms | 157.1 ms | ≤ 1000 ms | ✔ |
| Consulta: Gestor, sem critério, última página (50) | 20 de 1000 | 8 KiB | 3 | 8.8 ms | 16.4 ms | 32.0 ms | 117.2 ms | ≤ 1000 ms | ✔ |
| Consulta: Gestor, espaço + data | 10 de 10 | 4 KiB | 3 | 6.9 ms | 15.3 ms | 29.9 ms | 42.9 ms | ≤ 1000 ms | ✔ |
| Consulta: Solicitante, só as próprias | 20 de 50 | 8 KiB | 3 | 8.4 ms | 16.7 ms | 32.1 ms | 150.8 ms | ≤ 1000 ms | ✔ |
| Ocupação do dia: PG, API | 6 ocupados, 3 livres | 1 KiB | 3 | 5.1 ms | 12.3 ms | 26.3 ms | 50.3 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: PG, Caso de uso | 6 ocupados, 3 livres | 1 KiB | 2 | 2.6 ms | 5.4 ms | 17.0 ms | 49.3 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: REDIS_ACERTO, API | 6 ocupados, 3 livres | 1 KiB | 2 | 3.8 ms | 8.3 ms | 17.1 ms | 39.2 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: REDIS_ACERTO, Caso de uso | 6 ocupados, 3 livres | 1 KiB | 1 | 1.3 ms | 2.8 ms | 7.5 ms | 16.3 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: REDIS_ERRO, API | 6 ocupados, 3 livres | 1 KiB | 3 | 6.6 ms | 14.1 ms | 29.1 ms | 48.8 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: REDIS_ERRO, Caso de uso | 6 ocupados, 3 livres | 1 KiB | 2 | 3.8 ms | 8.0 ms | 19.6 ms | 36.6 ms | ≤ 500 ms | ✔ |

Diferença das medianas e IC 95% (bootstrap, 2000 reamostragens, semente 20261125):

| Nível | Comparação | Diferença | IC 95% | O IC inclui zero? |
|---|---|---|---|---|
| API | PG − REDIS_ACERTO (ganho do acerto) | +3.96 ms | [+2.74; +5.25] ms | não |
| API | REDIS_ERRO − PG (custo extra do miss) | +1.84 ms | [+0.45; +3.29] ms | não |
| Caso de uso | PG − REDIS_ACERTO (ganho do acerto) | +2.56 ms | [+2.06; +3.13] ms | não |
| Caso de uso | REDIS_ERRO − PG (custo extra do miss) | +2.58 ms | [+1.74; +3.41] ms | não |

Reconstrução das projeções (Redis vazio → montado):

| Comando | Tempo | Resultado |
|---|---|---|
| reconstruir_agenda | 1.28 s | {'dias_refeitos': 100, 'reservas_gravadas': 600, 'dias_esvaziados': 0, 'dias_descartados': 0} |
| reconstruir_indice | 0.07 s | {'reservas_indexadas': 1000, 'pendentes': 200, 'descartado': False} |

Concorrência (caso de uso direto, uma conexão por thread):

| Cenário | Threads | Chamadas | Vazão | p95 |
|---|---|---|---|---|
| PG | 8 | 2400 | 207 req/s | 74.4 ms |
| REDIS_ACERTO | 8 | 2400 | 310 req/s | 56.6 ms |

Tabela: 1000 linhas; índices: reservas_espaco_inicio_idx, reservas_reserva_pkey, reservas_reserva_sem_sobreposicao_no_espaco, reservas_reserva_solicitante_usuario_id_1f613a30.

EXPLAIN (ANALYZE, BUFFERS) de `listar_que_ocupam_horario`:

```
Sort  (cost=34.29..34.29 rows=1 width=122) (actual time=0.163..0.164 rows=6 loops=1)
  Sort Key: inicio, id
  Sort Method: quicksort  Memory: 25kB
  Buffers: shared hit=22
  ->  Bitmap Heap Scan on reservas_reserva  (cost=9.78..34.28 rows=1 width=122) (actual time=0.047..0.154 rows=6 loops=1)
        Recheck Cond: (espaco_id = 1)
        Filter: (((situacao)::text = ANY ('{CONFIRMADA,SOLICITADA}'::text[])) AND (((inicio AT TIME ZONE 'America/Sao_Paulo'::text))::date = '2026-11-26'::date))
        Rows Removed by Filter: 194
        Heap Blocks: exact=20
        Buffers: shared hit=22
        ->  Bitmap Index Scan on reservas_espaco_inicio_idx  (cost=0.00..9.78 rows=200 width=0) (actual time=0.030..0.030 rows=200 loops=1)
              Index Cond: (espaco_id = 1)
              Buffers: shared hit=2
Planning Time: 0.163 ms
Execution Time: 0.237 ms
```

Bancos do Redis que a medição não pode tocar (DBSIZE antes → depois): banco 0: 0 → 0; banco 1: 0 → 0

## Saída completa: 1000_b

- Sistema: Linux-6.18.58.1-microsoft-standard-WSL2-x86_64-with-glibc2.41 (4 CPUs visíveis no container)
- Python 3.12.16, Django 5.2.18, PostgreSQL 16.15
- Redis 8.10.3 (Linux 6.18.58.1-microsoft-standard-WSL2 x86_64), banco 2 dedicado à medição
- Carga: 1000 reservas (repositório, com histórico), 5 espaços, 20 solicitantes (gravadas em 3.9 s); tabela: 384 kB
- Medição: 5 chamadas de aquecimento e 300 medidas por cenário (5 rodadas intercaladas nos cenários de ocupação), pela API em processo (APIClient com token de acesso), sem rede nem navegador

| Cenário | Itens | Resposta | Consultas SQL | Mín | Mediana | p95 | Máx | Meta (p95) | Atende |
|---|---|---|---|---|---|---|---|---|---|
| Consulta: Gestor, sem critério | 20 de 1000 | 9 KiB | 3 | 9.0 ms | 13.9 ms | 32.8 ms | 86.1 ms | ≤ 1000 ms | ✔ |
| Consulta: Gestor, sem critério, última página (50) | 20 de 1000 | 8 KiB | 3 | 8.7 ms | 11.8 ms | 28.8 ms | 148.6 ms | ≤ 1000 ms | ✔ |
| Consulta: Gestor, espaço + data | 10 de 10 | 4 KiB | 3 | 7.9 ms | 10.5 ms | 28.0 ms | 45.9 ms | ≤ 1000 ms | ✔ |
| Consulta: Solicitante, só as próprias | 20 de 50 | 8 KiB | 3 | 8.5 ms | 12.7 ms | 31.7 ms | 162.8 ms | ≤ 1000 ms | ✔ |
| Ocupação do dia: PG, API | 6 ocupados, 3 livres | 1 KiB | 3 | 5.7 ms | 7.7 ms | 15.1 ms | 26.0 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: PG, Caso de uso | 6 ocupados, 3 livres | 1 KiB | 2 | 2.6 ms | 3.7 ms | 7.1 ms | 14.2 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: REDIS_ACERTO, API | 6 ocupados, 3 livres | 1 KiB | 2 | 4.4 ms | 6.2 ms | 15.4 ms | 28.0 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: REDIS_ACERTO, Caso de uso | 6 ocupados, 3 livres | 1 KiB | 1 | 1.4 ms | 2.0 ms | 3.0 ms | 9.9 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: REDIS_ERRO, API | 6 ocupados, 3 livres | 1 KiB | 3 | 6.9 ms | 9.4 ms | 27.0 ms | 36.7 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: REDIS_ERRO, Caso de uso | 6 ocupados, 3 livres | 1 KiB | 2 | 3.8 ms | 5.7 ms | 9.1 ms | 20.7 ms | ≤ 500 ms | ✔ |

Diferença das medianas e IC 95% (bootstrap, 2000 reamostragens, semente 20261125):

| Nível | Comparação | Diferença | IC 95% | O IC inclui zero? |
|---|---|---|---|---|
| API | PG − REDIS_ACERTO (ganho do acerto) | +1.50 ms | [+1.24; +1.73] ms | não |
| API | REDIS_ERRO − PG (custo extra do miss) | +1.74 ms | [+1.56; +2.11] ms | não |
| Caso de uso | PG − REDIS_ACERTO (ganho do acerto) | +1.74 ms | [+1.63; +1.88] ms | não |
| Caso de uso | REDIS_ERRO − PG (custo extra do miss) | +2.02 ms | [+1.81; +2.18] ms | não |

Reconstrução das projeções (Redis vazio → montado):

| Comando | Tempo | Resultado |
|---|---|---|
| reconstruir_agenda | 0.92 s | {'dias_refeitos': 100, 'reservas_gravadas': 600, 'dias_esvaziados': 0, 'dias_descartados': 0} |
| reconstruir_indice | 0.09 s | {'reservas_indexadas': 1000, 'pendentes': 200, 'descartado': False} |

Concorrência (caso de uso direto, uma conexão por thread):

| Cenário | Threads | Chamadas | Vazão | p95 |
|---|---|---|---|---|
| PG | 8 | 2400 | 267 req/s | 56.8 ms |
| REDIS_ACERTO | 8 | 2400 | 345 req/s | 45.8 ms |

Tabela: 1000 linhas; índices: reservas_espaco_inicio_idx, reservas_reserva_pkey, reservas_reserva_sem_sobreposicao_no_espaco, reservas_reserva_solicitante_usuario_id_1f613a30.

EXPLAIN (ANALYZE, BUFFERS) de `listar_que_ocupam_horario`:

```
Sort  (cost=34.29..34.29 rows=1 width=122) (actual time=0.166..0.167 rows=6 loops=1)
  Sort Key: inicio, id
  Sort Method: quicksort  Memory: 25kB
  Buffers: shared hit=22
  ->  Bitmap Heap Scan on reservas_reserva  (cost=9.78..34.28 rows=1 width=122) (actual time=0.035..0.162 rows=6 loops=1)
        Recheck Cond: (espaco_id = 1)
        Filter: (((situacao)::text = ANY ('{SOLICITADA,CONFIRMADA}'::text[])) AND (((inicio AT TIME ZONE 'America/Sao_Paulo'::text))::date = '2026-11-26'::date))
        Rows Removed by Filter: 194
        Heap Blocks: exact=20
        Buffers: shared hit=22
        ->  Bitmap Index Scan on reservas_espaco_inicio_idx  (cost=0.00..9.78 rows=200 width=0) (actual time=0.021..0.022 rows=200 loops=1)
              Index Cond: (espaco_id = 1)
              Buffers: shared hit=2
Planning Time: 0.090 ms
Execution Time: 0.208 ms
```

Bancos do Redis que a medição não pode tocar (DBSIZE antes → depois): banco 0: 0 → 0; banco 1: 0 → 0

## Saída completa: 20000_a

- Sistema: Linux-6.18.58.1-microsoft-standard-WSL2-x86_64-with-glibc2.41 (4 CPUs visíveis no container)
- Python 3.12.16, Django 5.2.18, PostgreSQL 16.15
- Redis 8.10.3 (Linux 6.18.58.1-microsoft-standard-WSL2 x86_64), banco 2 dedicado à medição
- Carga: 20000 reservas (bulk_create em lotes, sem histórico), 5 espaços, 20 solicitantes (gravadas em 2.9 s); tabela: 5680 kB
- Medição: 5 chamadas de aquecimento e 300 medidas por cenário (5 rodadas intercaladas nos cenários de ocupação), pela API em processo (APIClient com token de acesso), sem rede nem navegador

| Cenário | Itens | Resposta | Consultas SQL | Mín | Mediana | p95 | Máx | Meta (p95) | Atende |
|---|---|---|---|---|---|---|---|---|---|
| Consulta: Gestor, sem critério | 20 de 20000 | 9 KiB | 3 | 12.7 ms | 15.5 ms | 27.3 ms | 86.3 ms | ≤ 1000 ms | ✔ |
| Consulta: Gestor, sem critério, última página (1000) | 20 de 20000 | 8 KiB | 3 | 23.4 ms | 34.4 ms | 63.7 ms | 273.6 ms | ≤ 1000 ms | ✔ |
| Consulta: Gestor, espaço + data | 10 de 10 | 4 KiB | 3 | 12.4 ms | 15.8 ms | 27.9 ms | 85.9 ms | ≤ 1000 ms | ✔ |
| Consulta: Solicitante, só as próprias | 20 de 1000 | 8 KiB | 3 | 9.5 ms | 13.7 ms | 27.3 ms | 101.8 ms | ≤ 1000 ms | ✔ |
| Ocupação do dia: PG, API | 6 ocupados, 3 livres | 1 KiB | 3 | 7.1 ms | 9.7 ms | 15.7 ms | 25.5 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: PG, Caso de uso | 6 ocupados, 3 livres | 1 KiB | 2 | 4.6 ms | 5.9 ms | 9.6 ms | 17.6 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: REDIS_ACERTO, API | 6 ocupados, 3 livres | 1 KiB | 2 | 3.5 ms | 5.3 ms | 15.5 ms | 37.9 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: REDIS_ACERTO, Caso de uso | 6 ocupados, 3 livres | 1 KiB | 1 | 1.3 ms | 2.2 ms | 6.7 ms | 18.7 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: REDIS_ERRO, API | 6 ocupados, 3 livres | 1 KiB | 3 | 8.6 ms | 11.1 ms | 16.7 ms | 80.8 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: REDIS_ERRO, Caso de uso | 6 ocupados, 3 livres | 1 KiB | 2 | 6.0 ms | 7.8 ms | 14.0 ms | 28.2 ms | ≤ 500 ms | ✔ |

Diferença das medianas e IC 95% (bootstrap, 2000 reamostragens, semente 20261125):

| Nível | Comparação | Diferença | IC 95% | O IC inclui zero? |
|---|---|---|---|---|
| API | PG − REDIS_ACERTO (ganho do acerto) | +4.40 ms | [+4.08; +4.70] ms | não |
| API | REDIS_ERRO − PG (custo extra do miss) | +1.43 ms | [+1.04; +1.76] ms | não |
| Caso de uso | PG − REDIS_ACERTO (ganho do acerto) | +3.70 ms | [+3.50; +3.84] ms | não |
| Caso de uso | REDIS_ERRO − PG (custo extra do miss) | +1.93 ms | [+1.69; +2.15] ms | não |

Reconstrução das projeções (Redis vazio → montado):

| Comando | Tempo | Resultado |
|---|---|---|
| reconstruir_agenda | 24.48 s | {'dias_refeitos': 2000, 'reservas_gravadas': 12000, 'dias_esvaziados': 0, 'dias_descartados': 0} |
| reconstruir_indice | 0.75 s | {'reservas_indexadas': 20000, 'pendentes': 4000, 'descartado': False} |

Concorrência (caso de uso direto, uma conexão por thread):

| Cenário | Threads | Chamadas | Vazão | p95 |
|---|---|---|---|---|
| PG | 8 | 2400 | 293 req/s | 52.3 ms |
| REDIS_ACERTO | 8 | 2400 | 624 req/s | 20.9 ms |

Tabela: 20000 linhas; índices: reservas_espaco_inicio_idx, reservas_reserva_pkey, reservas_reserva_sem_sobreposicao_no_espaco, reservas_reserva_solicitante_usuario_id_1f613a30.

EXPLAIN (ANALYZE, BUFFERS) de `listar_que_ocupam_horario`:

```
Sort  (cost=581.51..581.54 rows=12 width=122) (actual time=2.237..2.239 rows=6 loops=1)
  Sort Key: inicio, id
  Sort Method: quicksort  Memory: 25kB
  Buffers: shared hit=410
  ->  Bitmap Heap Scan on reservas_reserva  (cost=98.29..581.29 rows=12 width=122) (actual time=0.257..2.224 rows=6 loops=1)
        Recheck Cond: (espaco_id = 1)
        Filter: (((situacao)::text = ANY ('{SOLICITADA,CONFIRMADA}'::text[])) AND (((inicio AT TIME ZONE 'America/Sao_Paulo'::text))::date = '2026-11-26'::date))
        Rows Removed by Filter: 3994
        Heap Blocks: exact=393
        Buffers: shared hit=410
        ->  Bitmap Index Scan on reservas_espaco_inicio_idx  (cost=0.00..98.29 rows=4000 width=0) (actual time=0.201..0.201 rows=4000 loops=1)
              Index Cond: (espaco_id = 1)
              Buffers: shared hit=17
Planning Time: 0.151 ms
Execution Time: 2.300 ms
```

Bancos do Redis que a medição não pode tocar (DBSIZE antes → depois): banco 0: 0 → 0; banco 1: 0 → 0

## Saída completa: 20000_b

- Sistema: Linux-6.18.58.1-microsoft-standard-WSL2-x86_64-with-glibc2.41 (4 CPUs visíveis no container)
- Python 3.12.16, Django 5.2.18, PostgreSQL 16.15
- Redis 8.10.3 (Linux 6.18.58.1-microsoft-standard-WSL2 x86_64), banco 2 dedicado à medição
- Carga: 20000 reservas (bulk_create em lotes, sem histórico), 5 espaços, 20 solicitantes (gravadas em 3.0 s); tabela: 5680 kB
- Medição: 5 chamadas de aquecimento e 300 medidas por cenário (5 rodadas intercaladas nos cenários de ocupação), pela API em processo (APIClient com token de acesso), sem rede nem navegador

| Cenário | Itens | Resposta | Consultas SQL | Mín | Mediana | p95 | Máx | Meta (p95) | Atende |
|---|---|---|---|---|---|---|---|---|---|
| Consulta: Gestor, sem critério | 20 de 20000 | 9 KiB | 3 | 11.5 ms | 13.6 ms | 25.1 ms | 69.1 ms | ≤ 1000 ms | ✔ |
| Consulta: Gestor, sem critério, última página (1000) | 20 de 20000 | 8 KiB | 3 | 22.2 ms | 26.9 ms | 52.9 ms | 98.7 ms | ≤ 1000 ms | ✔ |
| Consulta: Gestor, espaço + data | 10 de 10 | 4 KiB | 3 | 11.7 ms | 18.3 ms | 32.8 ms | 86.3 ms | ≤ 1000 ms | ✔ |
| Consulta: Solicitante, só as próprias | 20 de 1000 | 8 KiB | 3 | 9.6 ms | 13.9 ms | 27.0 ms | 102.7 ms | ≤ 1000 ms | ✔ |
| Ocupação do dia: PG, API | 6 ocupados, 3 livres | 1 KiB | 3 | 7.1 ms | 9.2 ms | 15.9 ms | 24.1 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: PG, Caso de uso | 6 ocupados, 3 livres | 1 KiB | 2 | 4.4 ms | 5.8 ms | 8.0 ms | 12.7 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: REDIS_ACERTO, API | 6 ocupados, 3 livres | 1 KiB | 2 | 3.6 ms | 5.7 ms | 13.5 ms | 30.5 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: REDIS_ACERTO, Caso de uso | 6 ocupados, 3 livres | 1 KiB | 1 | 1.3 ms | 2.3 ms | 10.7 ms | 27.1 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: REDIS_ERRO, API | 6 ocupados, 3 livres | 1 KiB | 3 | 8.7 ms | 12.0 ms | 27.9 ms | 72.8 ms | ≤ 500 ms | ✔ |
| Ocupação do dia: REDIS_ERRO, Caso de uso | 6 ocupados, 3 livres | 1 KiB | 2 | 6.1 ms | 8.1 ms | 17.6 ms | 43.6 ms | ≤ 500 ms | ✔ |

Diferença das medianas e IC 95% (bootstrap, 2000 reamostragens, semente 20261125):

| Nível | Comparação | Diferença | IC 95% | O IC inclui zero? |
|---|---|---|---|---|
| API | PG − REDIS_ACERTO (ganho do acerto) | +3.53 ms | [+3.30; +3.83] ms | não |
| API | REDIS_ERRO − PG (custo extra do miss) | +2.81 ms | [+2.35; +3.22] ms | não |
| Caso de uso | PG − REDIS_ACERTO (ganho do acerto) | +3.49 ms | [+3.38; +3.62] ms | não |
| Caso de uso | REDIS_ERRO − PG (custo extra do miss) | +2.28 ms | [+2.14; +2.53] ms | não |

Reconstrução das projeções (Redis vazio → montado):

| Comando | Tempo | Resultado |
|---|---|---|
| reconstruir_agenda | 29.77 s | {'dias_refeitos': 2000, 'reservas_gravadas': 12000, 'dias_esvaziados': 0, 'dias_descartados': 0} |
| reconstruir_indice | 0.57 s | {'reservas_indexadas': 20000, 'pendentes': 4000, 'descartado': False} |

Concorrência (caso de uso direto, uma conexão por thread):

| Cenário | Threads | Chamadas | Vazão | p95 |
|---|---|---|---|---|
| PG | 8 | 2400 | 277 req/s | 57.2 ms |
| REDIS_ACERTO | 8 | 2400 | 469 req/s | 33.3 ms |

Tabela: 20000 linhas; índices: reservas_espaco_inicio_idx, reservas_reserva_pkey, reservas_reserva_sem_sobreposicao_no_espaco, reservas_reserva_solicitante_usuario_id_1f613a30.

EXPLAIN (ANALYZE, BUFFERS) de `listar_que_ocupam_horario`:

```
Sort  (cost=581.51..581.54 rows=12 width=122) (actual time=2.292..2.294 rows=6 loops=1)
  Sort Key: inicio, id
  Sort Method: quicksort  Memory: 25kB
  Buffers: shared hit=410
  ->  Bitmap Heap Scan on reservas_reserva  (cost=98.29..581.29 rows=12 width=122) (actual time=0.262..2.282 rows=6 loops=1)
        Recheck Cond: (espaco_id = 1)
        Filter: (((situacao)::text = ANY ('{SOLICITADA,CONFIRMADA}'::text[])) AND (((inicio AT TIME ZONE 'America/Sao_Paulo'::text))::date = '2026-11-26'::date))
        Rows Removed by Filter: 3994
        Heap Blocks: exact=393
        Buffers: shared hit=410
        ->  Bitmap Index Scan on reservas_espaco_inicio_idx  (cost=0.00..98.29 rows=4000 width=0) (actual time=0.215..0.216 rows=4000 loops=1)
              Index Cond: (espaco_id = 1)
              Buffers: shared hit=17
Planning Time: 0.112 ms
Execution Time: 2.365 ms
```

Bancos do Redis que a medição não pode tocar (DBSIZE antes → depois): banco 0: 0 → 0; banco 1: 0 → 0

