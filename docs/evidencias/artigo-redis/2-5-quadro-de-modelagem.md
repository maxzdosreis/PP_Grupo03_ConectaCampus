# 2.5: Quadro de modelagem observado no Redis (DOC-02)

Quadro **consolidado à mão** a partir das saídas brutas `2-2-comandos-por-estrutura.txt` e `2-2-scan-e-contagem-por-familia.txt` (commit `de351d0`, Redis 8.10.3, modo padrão, dados de exemplo, em 26/11/2026) e do código. As colunas "observado" vêm dessas saídas; a coluna "fonte" foi conferida por `grep`. Nomes físicos têm o prefixo `conecta-campus:1:` (`KEY_PREFIX` das `CACHES` + versão 1 do cache do Django); a tabela usa o nome lógico. Conferido contra `docs/fontes/modelagem/06-redis.md` (DOC-01) e a DEC-28.

| Família (nome lógico) | Tipo | TYPE / ENCODING observados | TTL observado | Fonte no código |
|---|---|---|---|---|
| `agenda:espaco:{id}:{data}` | Sorted Set | zset / listpack (129 B com 3 membros) | 604.988 s ≈ 7 dias (dia 01/12 visto em 26/11: fim do dia + 1 dia) | `reservas/infrastructure/agenda_redis.py:189` (chave), `:19-20` (`FOLGA_DO_TTL`, `TTL_MINIMO`), `:60` (`_SUBSTITUIR`) |
| `agenda:versao:espaco:{id}:{data}` | String (inteiro) | string; **só existe depois de uma escrita** (valor `3` no dia 03/12 após registrar e remover; ausente no dia 01/12, só repovoado) | o da chave do dia | `reservas/infrastructure/agenda_redis.py:202`, scripts `:28` (`_AVANCAR_VERSAO`) |
| `reservas:pendentes` | Sorted Set | zset / listpack (110 B) | -1 (sem TTL) | `reservas/infrastructure/indice_redis.py:196` |
| `reservas:situacao:{S}` (5 chaves) | Set | set / intset (88 B) | -1 | `reservas/infrastructure/indice_redis.py:200` |
| `reservas:indice:montado` | String | string / int (61 B) | -1 | `reservas/infrastructure/indice_redis.py:204` |
| `reservas:indice:versao` | String (inteiro) | string / int (60 B) | -1 | `reservas/infrastructure/indice_redis.py:208` |
| `ranking:espacos` | Sorted Set | zset / listpack (80 B) | -1 | `reservas/infrastructure/ranking_redis.py:206` |
| `ranking:contadas` (livro) | Hash | hash / listpack (85 B, 4 campos) | -1 | `reservas/infrastructure/ranking_redis.py:210` |
| `ranking:montado`, `ranking:versao` | String | string / int (53 B no `montado`) | -1 | `reservas/infrastructure/ranking_redis.py:214`, `:218` |
| `espaco:{id}` | Hash | hash / listpack (196 B, 6 campos) | 300 s no máximo (vistos 264, 223, 142, 85) | `espacos/infrastructure/cache_de_espacos_redis.py:94`, `:14` |
| `espaco:versao:{id}` | String (inteiro) | string / int (61 B) | 86.400 s no máximo (visto 81.434) | `espacos/infrastructure/cache_de_espacos_redis.py:98`, `:15` |
| `throttle_login_ip_<ip>`, `throttle_login_email_<e-mail>` | Sorted Set | zset / listpack (157 e 172 B, 1 membro) | ≈ 60 s (vistos 58 e 55 depois de uma tentativa; janela de 1 min) | `contas/api/limites.py:107` (chave), script `:16` (`_REGISTRAR_TENTATIVA`) |
| `reservas:tmp:{uuid}:*`, `ranking:tmp:{uuid}:*` | os mesmos das definitivas | **não observadas**: existem só durante a reconstrução (600 s) e são renomeadas ou apagadas | 600 s (`TTL_DAS_TEMPORARIAS`) | `indice_redis.py:22` e `:192`; `ranking_redis.py:22` e `:202` |

Contagem de chaves por família no instante da coleta (via `SCAN`, banco 0): agenda 1, espaço 3, reservas 8, ranking 4, limite de tentativas 2, total 18 (`2-2-scan-e-contagem-por-familia.txt`).

## Conferência com a DOC-01 (`06-redis.md`) e a DEC-28

Os tipos, TTLs e padrões observados **batem** com a seção 6.2 da DOC-01. Três observações, sem divergência de fato:

1. `agenda:versao:...` aparece **só depois de uma escrita** (`registrar` ou `remover`); um dia apenas repovoado pela leitura ou pela reconstrução não a tem (`TYPE` = none). A DOC-01 diz "contador de escritas do dia", o que é coerente, mas um leitor pode esperar a chave sempre presente.
2. O padrão `agenda:*` do `SCAN` também devolve `agenda:versao:...`; para listar só as projeções de dia, o padrão é `agenda:espaco:*`.
3. A DOC-01 informa o TTL das chaves `*:montado` como `-1`, e o `TTL` observado foi `-1` (sem expiração), como dito.

Os encodings (`listpack` para zset e hash pequenos, `intset` para o set de ids, `int` para strings numéricas) **não estão** na DOC-01; vêm só desta coleta e dependem do tamanho dos dados (acima de limites internos do Redis, o encoding muda para `skiplist`/`hashtable`).
