## 6. Redis: projeções e contadores (DOC-01)

**MOD-06 • 0.1 • Rascunho** • Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha

Material complementar da seção 1 do PDF, fora do PDF (a seção 1 de `modelagem.md` traz um resumo de 0,3 página; ver o plano em [`README.md`](README.md)). Cada fato abaixo foi conferido no código (caminhos a partir de `src/backend/`) e no Redis em execução em 25/11/2026 (`SCAN`, `TYPE`, `TTL`, `HGETALL`, `ZRANGE ... WITHSCORES` depois de `carregar_dados_exemplo` e `reconstruir_agenda_redis`). Decisão de origem: [DEC-28](../requisitos/decisoes/DEC-28.md), adotada provisoriamente.

| Versão | Data | Autor | Mudança |
|---|---|---|---|
| 0.1 | 25/11/2026 | Max Zimmermann dos Reis | Criação (DOC-01): famílias de chaves, padrões, falhas, reconstrução, persistência e a medição da RDS-10. Sem aprovação. |

### 6.1 Papel do Redis e a regra central

O Redis tem dois usos, em dois conjuntos de chaves que não se misturam:

1. **Contadores do limite de tentativas** (AUT-08, AUT-10, AUT-11): estado próprio, que só existe no Redis. Falha fechada: Redis fora do ar → 503 `SERVICO_INDISPONIVEL` (RNF-F12).
2. **Projeções** do PostgreSQL (DEC-28): cópias de leitura da agenda do dia, da fila e das contagens de reservas, do ranking de espaços e do cadastro de espaço. Todas se refazem a partir do banco. Falha aberta: o caso de uso lê do PostgreSQL e a API não devolve 503 por causa delas.

**Regra central:** o PostgreSQL decide; o Redis nunca decide conflito de horário, transição de situação nem permissão. A restrição de exclusão `reservas_reserva_sem_sobreposicao_no_espaco` continua sendo a guarda final contra conflito, e não há pré-checagem em Lua sobre a projeção (DEC-28, itens a e j). Quem cria uma reserva lê o espaço do PostgreSQL, com trava de linha (`verificar_espaco_disponivel_para_reserva`, `espacos/publico.py`), nunca do cache.

### 6.2 Chaves

Toda chave física é `conecta-campus:1:<nome lógico>`: `conecta-campus` é o `KEY_PREFIX` das `CACHES` e `1` é a versão padrão do cache do Django (`cache.make_key`, `config/settings.py`). A tabela usa só o nome lógico. `{id}` é o id do espaço, `{data}` é `AAAA-MM-DD` e `{S}` é a situação (`SOLICITADA`, `CONFIRMADA`, `CONCLUIDA`, `RECUSADA`, `CANCELADA`).

| Chave (nome lógico) | Tipo | Conteúdo | TTL | Escreve | Lê | Na falha |
|---|---|---|---|---|---|---|
| `throttle_login_email_<e-mail>`, `throttle_login_ip_<ip>` e as dos outros limites | Sorted Set (um por chave de limite; script Lua `_REGISTRAR_TENTATIVA`) | membro `agora:uuid4`, score = momento da tentativa | a janela do limite (`EXPIRE`) | throttles de `contas/api/limites.py`, a cada requisição | os mesmos | **falha fechada**: 503 `SERVICO_INDISPONIVEL` |
| `agenda:espaco:{id}:{data}` | Sorted Set | membro `"{reserva_id}:{fim_em_minutos}:{S}"`, score = início em minutos desde a meia-noite local; fim 1440 = meia-noite do fim do dia; sentinela `_` com score -1 marca "dia projetado, sem reservas" | fim do dia + 1 dia, no mínimo 1 h (`FOLGA_DO_TTL`, `TTL_MINIMO`; `_ttl_em_segundos`) | `RepositorioReservasComAgenda` depois do commit; `ConsultarOcupacaoDoDia` ao repovoar; `reconstruir_agenda_redis` | `ConsultarOcupacaoDoDia` | lê do PostgreSQL (`AgendaIndisponivel`) |
| `agenda:versao:espaco:{id}:{data}` | String (inteiro) | contador de escritas do dia | o mesmo da chave do dia | os scripts `_REGISTRAR` e `_REMOVER` (`INCR` + `EXPIRE`) | `versao()`, antes de reconstruir ou repovoar | idem |
| `reservas:pendentes` | Sorted Set | membro = id da reserva com 19 dígitos (`0000000000000000018`), score = `criada_em` em segundos (timestamp) | sem TTL | índice (`aplicar`, `substituir`) | `ConsultarFilaDePendentes` | lê do PostgreSQL (`IndiceIndisponivel`) |
| `reservas:situacao:{S}` | Set | ids das reservas naquela situação (cinco chaves) | sem TTL | índice | `ContarReservasPorSituacao` e o total da fila | idem |
| `reservas:indice:montado` | String | `"1"`: o índice foi montado | sem TTL | `substituir` (script `_TROCAR`) | `pendentes` e `contagem_por_situacao`, no mesmo pipeline da leitura | ausente = miss, lê do PostgreSQL |
| `reservas:indice:versao` | String (inteiro) | contador de escritas do índice | sem TTL | `aplicar` (`INCR`) | `versao()` | idem |
| `ranking:espacos` | Sorted Set | membro = id do espaço, score = total de reservas Confirmadas ou Concluídas | sem TTL | ranking (`aplicar`, `substituir`) | `ConsultarRankingDeEspacos` | lê do PostgreSQL (`RankingIndisponivel`) |
| `ranking:contadas` | Hash | campo = id da reserva, valor = id do espaço em que foi contada (o livro de idempotência) | sem TTL | ranking | o próprio script `_APLICAR` | idem |
| `ranking:montado`, `ranking:versao` | String | como as do índice | sem TTL | como as do índice | como as do índice | idem |
| `espaco:{id}` | Hash | campos `nome`, `tipo`, `capacidade`, `ativo` (0 ou 1), `abertura_em_minutos`, `fechamento_em_minutos` | 300 s (`TTL_DO_ESPACO_EM_SEGUNDOS`) | `LeitorDeEspacosComCache`, ao ler com miss (script `_GUARDAR`) | `LeitorDeEspacosComCache` | lê do PostgreSQL (`CacheDeEspacosIndisponivel`); entrada quebrada é descartada |
| `espaco:versao:{id}` | String (inteiro) | contador de invalidações | 86.400 s (`TTL_DA_VERSAO_EM_SEGUNDOS`) | `invalidar` (script `_INVALIDAR`: `DEL` do Hash e `INCR`) | `versao()`, antes de gravar | idem |
| `reservas:tmp:{uuid}:pendentes`, `reservas:tmp:{uuid}:situacao:{S}`, `ranking:tmp:{uuid}:espacos`, `ranking:tmp:{uuid}:contadas` | os mesmos tipos das definitivas | cópia em montagem, só durante a reconstrução | 600 s (`TTL_DAS_TEMPORARIAS`) | `substituir` do índice e do ranking | só o script `_TROCAR`, que as renomeia | apagadas no `finally`; se o `DEL` falhar, o TTL as remove |

Confirmado no Redis em execução: `agenda:espaco:5:2026-12-01` (zset, TTL 609.922 s, membros `_` -1, `17:600:CONFIRMADA` 540, `18:780:SOLICITADA` 720), `reservas:pendentes` (zset com um membro), cinco `reservas:situacao:*` (set), `ranking:espacos` (zset), `ranking:contadas` (hash `reserva → espaço`), `espaco:1` (hash, TTL 287 s) e `espaco:versao:1` (string, TTL 86.386 s); as chaves `*:montado` são strings `"1"` sem TTL (`TTL` = -1).

**O que cada família faz**

- **Agenda.** Responde "o que está ocupado no espaço X na data D" com `ZRANGE`, ordenado por início. A API de ocupação do dia não mudou de formato; só o caminho de leitura.
- **Fila e contagens.** `reservas:pendentes` ordena as Solicitadas por `criada_em`, e o membro de 19 dígitos faz o desempate de mesmo instante coincidir com a ordem do id. As cinco chaves `reservas:situacao:{S}` dão a contagem por situação (`SCARD`) sem `COUNT` no banco.
- **Ranking.** O score do `ranking:espacos` é o número de reservas Confirmadas ou Concluídas (`SITUACOES_QUE_CONTAM_NO_RANKING`, `reservas/domain/situacao.py`); a consulta do Gestor aceita de 1 a 20 posições, padrão 5 (`LIMITE_MINIMO_DO_RANKING`, `LIMITE_MAXIMO_DO_RANKING`, `LIMITE_PADRAO_DO_RANKING`).
- **Cache de espaço.** Uma cópia do espaço por 300 s para as leituras informativas.

### 6.3 Padrões que se repetem

**Leitura com miss e fallback.** Cada projeção é lida pelo caso de uso por uma porta (`Protocol`): `AgendaDoDia`, `IndiceDeReservas`, `RankingDeEspacos` (`reservas/application/portas.py`) e `CacheDeEspacos` (`espacos/application/portas.py`). Redis fora do ar levanta uma exceção própria (`AgendaIndisponivel`, `IndiceIndisponivel`, `RankingIndisponivel`, `CacheDeEspacosIndisponivel`, que **não** são erros de domínio e nunca chegam ao tratador de erros da API); `None` significa miss. Nos dois casos o caso de uso lê do PostgreSQL. Na agenda e no cache de espaço, o miss repovoa a projeção com o resultado lido do banco, e a falha de gravação é só registrada em log. Fila, contagens e ranking não se repovoam sozinhos: só o comando de reconstrução os remonta.

**Gravação depois do commit, com convergência por releitura.** `RepositorioReservasComAgenda.salvar` grava no PostgreSQL e agenda `transaction.on_commit(..., robust=True)` (`reservas/infrastructure/repositorio_com_agenda.py`). Depois do commit, cada projeção (agenda, índice e ranking) é atualizada em separado: o repositório relê a reserva do banco e aplica o estado lido, no máximo 3 vezes (`TENTATIVAS_DE_CONVERGENCIA`), parando quando a situação lida é a que já aplicou. Se a reserva continuar mudando, ou o Redis falhar, só há um aviso no log. A falha de uma projeção não impede as outras, e o commit já aconteceu: a reserva fica salva. `RepositorioEspacosQueInvalida` faz o mesmo para o espaço: depois do commit de `salvar` (editar, desativar e reativar), apaga a cópia e avança a versão.

**Aplicação por estado.** O que se grava no Redis é o **estado atual** da reserva (situação, espaço, horário), nunca o evento "mudou". Por isso aplicar duas vezes dá o mesmo resultado, e a releitura por convergência não duplica nada. Na fila e nas contagens, o script `_APLICAR` adiciona o id ao conjunto da situação atual e o remove dos outros quatro. Na agenda, o `_REGISTRAR` tira os membros antigos da reserva (prefixo `"{reserva_id}:"`) antes de gravar o novo. No ranking, o `ZINCRBY` ingênuo **não** seria idempotente (aplicar duas vezes contaria duas vezes), e por isso existe o livro `ranking:contadas`: `HSETNX` no livro e só então `ZINCRBY +1`; ao deixar de contar, `HGET` do espaço contado, `HDEL` e `ZINCRBY -1`, removendo o membro quando o total chega a zero. O livro também guarda o espaço em que a reserva foi contada, então um estado repetido não conta de novo.

**Sinal `montado`.** O Redis apaga uma estrutura vazia (um Sorted Set sem membros deixa de existir) e, no modo padrão, não persiste. Sem um sinal, "fila de pendentes vazia" e "índice perdido" seriam a mesma chave ausente, e uma leitura devolveria "0 pendentes" quando o Redis acabou de reiniciar. As chaves `reservas:indice:montado` e `ranking:montado` distinguem os dois: com o sinal, ausente é vazio verdadeiro; sem ele, é miss, e o caso de uso lê do PostgreSQL. O sinal e a leitura vão no mesmo pipeline (`EXISTS` + `ZRANGE` ou `SCARD`), e o script `_APLICAR` **não escreve** enquanto o sinal não existe (retorna 0 depois de avançar a versão), para uma escrita isolada não passar por montagem. Na agenda, o papel do sinal é da sentinela `_` com score -1: um dia sem reservas é gravado com só a sentinela, e `listar` devolve `None` (miss) apenas quando o Sorted Set não existe; `_REGISTRAR` e `_REMOVER` também só mexem num dia que já foi projetado (`ZSCORE` da sentinela).

**Contador de versão e troca atômica.** A reconstrução lê o banco devagar (em lotes de 500) e, nesse intervalo, uma escrita concorrente pode mudar o estado. Cada projeção tem um contador de versão (`INCR` em toda escrita aplicada). A reconstrução anota a versão antes de ler o banco e entrega o resultado ao script `_TROCAR` ou `_SUBSTITUIR`, que compara a versão atual com a anotada e só troca se forem iguais; senão devolve 0 e a reconstrução tenta de novo (até 3 vezes por dia na agenda e 3 vezes no índice e no ranking, `TENTATIVAS_POR_DIA` e `TENTATIVAS_DE_RECONSTRUCAO`) ou, se nada der certo, descarta e avisa. No índice e no ranking, a montagem acontece em chaves temporárias (`*:tmp:{uuid}:*`, TTL de 600 s, em lotes de 1.000 gravações, `LOTE_DE_GRAVACAO`) e o `_TROCAR` as renomeia sobre as definitivas (`RENAME` + `PERSIST`) e só então liga o sinal `montado`, tudo numa execução atômica: quem lê vê a projeção antiga inteira ou a nova inteira, nunca metade. Se a projeção nova ficou vazia (sem temporária), o `_TROCAR` apaga a definitiva. No cache de espaço, a versão serve ao mesmo fim: o leitor anota a versão **antes** de ler o PostgreSQL e o `_GUARDAR` só grava se ela não mudou, então uma invalidação no meio impede que o dado velho volte ao cache.

**Desempate do ranking.** O score é o total; membros com o mesmo score vêm do Redis em ordem lexicográfica (reversa no `ZREVRANGE`), que não é a ordem numérica do id (`"10"` antes de `"2"`). Por isso `top` (`ranking_redis.py`) não confia nessa ordem: lê o `ZREVRANGE`, completa os empatados no corte com `ZRANGEBYSCORE` (para o corte não esconder um espaço empatado) e ordena em Python por total decrescente e id do espaço crescente. A consulta ao banco, usada no fallback, ordena igual (`order_by("-total", "espaco_id")`).

### 6.4 Política de falhas por caminho

| Caminho | Redis fora do ar ou projeção perdida | Resposta |
|---|---|---|
| Ocupação do dia (agenda) | lê do PostgreSQL | 200, o mesmo conteúdo |
| Fila de pendentes e contagens por situação (Gestor) | lê do PostgreSQL; também quando o índice não bate com o banco (id da fila que não está mais Solicitada) | 200 |
| Ranking de espaços (Gestor) | lê do PostgreSQL (`contar_por_espaco_que_contam_no_ranking`) | 200 |
| Leitura de espaço (cache) | lê do PostgreSQL | 200 |
| Escrita das projeções (depois do commit) | aviso no log; a reserva ou o espaço já está salvo; a leitura seguinte ou o comando de reconstrução corrige | sem efeito na resposta |
| Login e cadastro (e troca de senha, e alteração de usuários pelo Gestor) | recusa | **503** `SERVICO_INDISPONIVEL` (falha fechada, RNF-F12 intacto) |
| `GET /api/health/` | confere banco e depois cache | 503 `CACHE_INDISPONIVEL` |

As consultas nunca respondem 503 por causa das projeções (DEC-28, item c); só o contador de tentativas, que decide acesso, falha fechado.

### 6.5 Os dois caminhos do cache de espaço

| Caminho | Fonte do espaço | Usa o cache? |
|---|---|---|
| `GET /api/espacos/{id}/` (`obter_espaco`) | `LeitorDeEspacosComCache` | **sim** |
| Ocupação do dia (`ConsultarOcupacaoDoDia` → `ConsultaDeEspacosViaFachada.obter_espaco_reservavel` → `verificar_espaco_disponivel`) | `LeitorDeEspacosComCache` | **sim** |
| Criar reserva (`CriarReserva`, `obter_espaco_reservavel_travado` → `verificar_espaco_disponivel_para_reserva`) | PostgreSQL, com trava de linha | **nunca** |
| Editar, desativar e reativar espaço (decisão e trava da ESP-08) | PostgreSQL | **nunca** |

A decisão (o espaço existe, está ativo, o horário cabe) e a trava de linha leem sempre o PostgreSQL. O cache só serve a telas que mostram o espaço. **Limite de velhice:** a invalidação depois do commit apaga a cópia e avança a versão; se ela falhar (Redis fora do ar no momento), a cópia antiga pode ser mostrada por até 300 s (o TTL), e o log registra o aviso. Reativar um espaço também invalida (`AtivarEspaco` usa o repositório que invalida, como `EditarEspaco` e `DesativarEspaco`; `espacos/api/dependencias.py`).

### 6.6 Reconstrução

`docker compose exec backend python manage.py reconstruir_agenda_redis` (a partir de `src/`) refaz, nesta ordem e a partir do PostgreSQL: (1) a agenda dos dias de hoje em diante, de todos os dias que têm reserva que ocupa horário **ou** já estão projetados (um dia projetado que perdeu as reservas vira só a sentinela); (2) o índice de filas e contagens; (3) o ranking. Imprime uma linha por etapa:

```
Agenda reconstruída: 1 dia, 2 reservas, 0 dias esvaziados.
Filas e contagens reconstruídas: 10 reservas, 1 pendente.
Ranking de espaços reconstruído: 3 espaços, 4 reservas contadas.
```

(saída real em 25/11/2026 com os dados de exemplo). É idempotente e seguro de rodar várias vezes. Se uma reserva mudou durante a reconstrução e as 3 tentativas não bastaram, a etapa imprime um aviso ("rode o comando de novo") em vez do resumo; Redis fora do ar no meio levanta um erro de comando com a mensagem da etapa. Não refaz os contadores de tentativas (que zeram quando o Redis reinicia) nem o cache de espaço (que vence pelo TTL).

### 6.7 Persistência

O padrão é sem persistência: `redis-server --save "" --appendonly no` (`src/docker-compose.yml`). Perder o Redis perde só projeções e contadores; as projeções voltam pelo comando de reconstrução ou pela leitura com miss. O override opcional `src/docker-compose.redis-persistente.yml` troca o comando por `--appendonly yes --appendfsync everysec` e monta o volume `redis_data`: com ele, o Redis recarrega o AOF ao reiniciar (uma queda brusca pode perder cerca de 1 s de escrita). Existe só para a demonstração de "reinicia e perde" × "reinicia e continua" e não é para produção; o modo de produção não o usa. Passo a passo no [README de `src/`](../../../src/README.md).

### 6.8 Contrato do import-linter

O contrato `Domínio e aplicação não conhecem o Redis` (`src/backend/pyproject.toml`) proíbe `redis` em `compartilhado.domain`, `*.domain` e `*.application` dos três contextos. O pacote `redis` aparece só fora delas: nas `infrastructure` de `reservas` e `espacos` (adaptadores), em `contas/api/limites.py` e em `config/views.py` (para a exceção `RedisError`). `compartilhado/infrastructure/redis_comum.py` guarda o acesso comum ao cliente do cache do Django (`cliente`, `texto`); `reservas/infrastructure/redis_comum.py` só o reexporta. Com isso, as portas (`AgendaDoDia` etc.) são testadas com fakes e os adaptadores são os únicos que falam Redis.

### 6.9 Medição da RDS-10

Resumo de [`docs/evidencias/rds-10-ocupacao-redis-vs-postgres.md`](../../evidencias/rds-10-ocupacao-redis-vs-postgres.md), medido em 25/11/2026, em máquina única, em processo e sem rede, com 300 chamadas por cenário. Diferença das medianas, PostgreSQL menos acerto do Redis, na ocupação do dia pela API: de +1,50 ms a +4,40 ms entre quatro rodadas (1.000 e 20.000 reservas), com intervalo de confiança de 95% sem zero em todas; o resultado variou entre rodadas do mesmo tamanho. O miss (chave apagada) ficou de 1,4 a 2,8 ms mais lento que o PostgreSQL. A meta de 500 ms da DEC-12 é atendida sem o Redis (p95 máximo de cerca de 30 ms). A reconstrução com 20.000 reservas levou 24,5 s e 29,8 s (agenda). O arquivo conclui que nada na medição mostra que o Redis seja necessário para cumprir a meta; o ganho observado é de milissegundos. Limites: sem rede entre os serviços, só 6 reservas ativas no dia e dados sintéticos.
