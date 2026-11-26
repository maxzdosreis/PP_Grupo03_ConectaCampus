# Demonstração do Redis para o vídeo: sequência exata, com tempos reais (DOC-02)

Ensaiada de ponta a ponta em 26/11/2026 (commit `de351d0`, Redis 8.10.3, Windows 10 + Docker Desktop/WSL 2), a partir de `src/`, com o ambiente já no ar e os dados de exemplo carregados. Os tempos são do **ensaio em bash** (cronometrados por script, sem a fala): "Passo" é a duração do comando, "Acum." é a soma desde o primeiro. As variantes PowerShell foram conferidas à parte (login, ocupação, `SCAN`, `ZRANGE` e o login com 401), mas não cronometradas.

**Total do ensaio: 80,5 s de tela, 24 passos.** Cabe com folga nos 10 minutos; a folga é para a fala, pausas, digitação e o `docker compose up` a frio, que **não foi medido** (o ambiente já estava no ar; o passo 1 mediu um `up -d` sem nada a criar). Os comandos que esperam o *healthcheck* incluem a espera (até ~5 s cada).

## Antes de gravar
- **Redis não publica porta no host**: tudo que fala com ele usa `docker compose exec redis redis-cli ...` (dentro de `src/`).
- **Limite de tentativas** (RNF-F12): login 5/min por e-mail e 20/min por IP. Faça **um** login por perfil e reaproveite o token. Parar o Redis zera os contadores.
- **O login só funciona com o Redis no ar** (falha fechada, 503). Por isso o token é obtido **antes** de pará-lo.
- **Senha do Gestor:** no banco de desenvolvimento usado no ensaio, o login de `carla.mendes@exemplo.com` com a senha do README foi recusado (credenciais inválidas). O ensaio usou só o Solicitante (`bruno.lima@exemplo.com`). Antes de gravar, confira o login do Gestor ou recrie os dados de exemplo; o passo 7 mostra a fila direto no Redis para não depender dele.
- O `SCAN ... agenda:*` também lista `agenda:versao:...` (a chave do contador casa com o padrão); não é erro.
- Reserva de teste: use um horário livre (aqui, Quadra de Tênis 1, 05/12/2026 11:00–12:00) e **cancele ao fim** (passo 24). Ajuste a data se já passou.
- **Não rodar a suíte inteira no vídeo** (≈15 min). Os passos 22 e 23 só mostram resultados já gravados e o contrato do import-linter.
- O fallback com o Redis parado é **lento** (3 a 11 s por leitura, e ~8 s para o 503 do login): o nome `redis` deixa de resolver e há tentativas e *timeouts*. Corte ou acelere essa espera na edição; o conteúdo da resposta é o mesmo.

## Tempos

| # | O que mostrar | Passo | Acum. |
|---|---|---|---|
| 1 | Subir o compose | 1,6 s | 1,7 s |
| 2 | Login do Solicitante | 1,2 s | 3,0 s |
| 3 | Criar uma reserva (201) | 0,2 s | 3,4 s |
| 4 | `SCAN` filtrado | 0,7 s | 4,3 s |
| 5 | `ZRANGE` da agenda | 0,6 s | 5,1 s |
| 6 | Ocupação do dia pela API | 0,2 s | 5,4 s |
| 7 | Fila de pendentes e contagem | 1,7 s | 7,1 s |
| 8 | `stop redis` | 1,0 s | 8,3 s |
| 9 | Ocupação com Redis parado (200) | 6,8 s | 15,2 s |
| 10 | Login com Redis parado (503) | 8,2 s | 23,5 s |
| 11 | `start redis` e healthcheck | 7,4 s | 31,0 s |
| 12 | Reconstruir | 4,9 s | 35,9 s |
| 13 | Redis com AOF (override) | 2,3 s | 38,3 s |
| 14 | Healthcheck do Redis com AOF | 6,2 s | 44,6 s |
| 15 | Reconstruir (grava no AOF) | 5,1 s | 49,8 s |
| 16 | `DBSIZE` antes (12) | 0,7 s | 50,6 s |
| 17 | `restart` com AOF e healthcheck | 7,4 s | 58,0 s |
| 18 | `DBSIZE` depois (12, igual) | 0,8 s | 58,9 s |
| 19 | Voltar ao modo padrão | 8,5 s | 67,5 s |
| 20 | Remover o volume do AOF | 0,4 s | 68,0 s |
| 21 | Reconstruir (Redis padrão, vazio) | 7,6 s | 75,6 s |
| 22 | Mostrar testes já gravados | 0,2 s | 76,0 s |
| 23 | `lint-imports` (11 contratos mantidos) | 4,1 s | 80,1 s |
| 24 | Cancelar a reserva de teste | 0,2 s | 80,5 s |

Senhas: não ficam nestes arquivos; troque `<SENHA-DO-BRUNO-NO-README-DA-RAIZ>` pela senha da tabela de usuários de exemplo do README da raiz. Variáveis: bash `API=http://localhost:8000/api`; PowerShell `$API = "http://localhost:8000/api"`. Todos os comandos rodam dentro de `src/`.

## Comandos

### Passo 1: subir
```powershell
docker compose up -d
```

### Passo 2: login (uma vez; não mostre o token)
bash:
```bash
TOK=$(curl -s -X POST $API/auth/login/ -H 'Content-Type: application/json' -d '{"email":"bruno.lima@exemplo.com","senha":"<SENHA-DO-BRUNO-NO-README-DA-RAIZ>"}' | python -c "import sys,json;print(json.load(sys.stdin)['dados']['access'])")
```
PowerShell:
```powershell
$tok = (Invoke-RestMethod -Method Post -Uri "$API/auth/login/" -ContentType 'application/json' -Body '{"email":"bruno.lima@exemplo.com","senha":"<SENHA-DO-BRUNO-NO-README-DA-RAIZ>"}').dados.access
```

### Passo 3: criar a reserva (201)
bash:
```bash
curl -s -w '\nHTTP %{http_code}\n' -X POST $API/reservas/ -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"espaco_id":5,"data":"2026-12-05","hora_inicio":"11:00","hora_fim":"12:00","finalidade":"Demonstracao Redis"}'
```
PowerShell (anote o `id` devolvido):
```powershell
curl.exe -s -w "`nHTTP %{http_code}`n" -X POST "$API/reservas/" -H "Authorization: Bearer $tok" -H "Content-Type: application/json" -d '{\"espaco_id\":5,\"data\":\"2026-12-05\",\"hora_inicio\":\"11:00\",\"hora_fim\":\"12:00\",\"finalidade\":\"Demonstracao Redis\"}'
```

### Passos 4 e 5: chaves no Redis
```powershell
docker compose exec redis redis-cli --scan --pattern "conecta-campus:1:agenda:*"
docker compose exec redis redis-cli ZRANGE conecta-campus:1:agenda:espaco:5:2026-12-05 0 -1 WITHSCORES
```
Esperado no `ZRANGE`: `_` com -1 e `<id>:720:SOLICITADA` com 660 (11:00 = 660 min; fim 12:00 = 720).

### Passo 6: ocupação pela API
bash: `curl -s "$API/reservas/ocupacao/?espaco=5&data=2026-12-05" -H "Authorization: Bearer $TOK"`

PowerShell: `curl.exe -s "$API/reservas/ocupacao/?espaco=5&data=2026-12-05" -H "Authorization: Bearer $tok"`

### Passo 7: fila e contagem (direto no Redis, sem depender do Gestor)
```powershell
docker compose exec redis redis-cli ZRANGE conecta-campus:1:reservas:pendentes 0 -1 WITHSCORES
docker compose exec redis redis-cli SCARD conecta-campus:1:reservas:situacao:SOLICITADA
```
Com o Gestor logado, as rotas são `GET /api/reservas/pendentes/` e `/contagem-por-situacao/`.

### Passos 8 a 10: Redis parado
```powershell
docker compose stop redis
curl.exe -s -w "`nHTTP %{http_code}`n" "$API/reservas/ocupacao/?espaco=5&data=2026-12-05" -H "Authorization: Bearer $tok"
curl.exe -s -w "`nHTTP %{http_code}`n" -X POST "$API/auth/login/" -H "Content-Type: application/json" -d '{\"email\":\"nao.existe@exemplo.com\",\"senha\":\"x\"}'
```
Esperado: 200 com a mesma ocupação (lenta) e depois 503 `SERVICO_INDISPONIVEL`. **Uma** tentativa de login só.

### Passos 11 e 12: religar e reconstruir
```powershell
docker compose start redis
docker compose exec backend python manage.py reconstruir_agenda_redis
```
Espere o `healthy` (`docker compose ps redis`, ~5 s) antes do segundo comando. Esperado: as três linhas "Agenda reconstruída…", "Filas e contagens reconstruídas…" e "Ranking de espaços reconstruído…".

### Passos 13 a 18: o AOF sobrevive
```powershell
docker compose -f docker-compose.yml -f docker-compose.redis-persistente.yml up -d redis
docker compose exec backend python manage.py reconstruir_agenda_redis
docker compose exec redis redis-cli DBSIZE
docker compose -f docker-compose.yml -f docker-compose.redis-persistente.yml restart redis
docker compose exec redis redis-cli DBSIZE
```
Esperado: o mesmo `DBSIZE` antes e depois (12 no ensaio). Sem o override, o `restart` zera (ver `2-3-persistencia-padrao-e-aof.txt`).

### Passos 19 e 20: voltar ao padrão (deixa o ambiente como estava)
```powershell
docker compose up -d redis
docker volume rm conecta-campus_redis_data
```
O `docker volume rm` só é seguro se o volume foi criado pelo próprio ensaio.

### Passo 21: reconstruir o Redis padrão, vazio
```powershell
docker compose exec backend python manage.py reconstruir_agenda_redis
```

### Passos 22 e 23: testes e contrato (nada de suíte inteira)
```powershell
Select-String -Path ..\docs\evidencias\artigo-redis\2-7-testes-do-redis-subconjunto.txt -Pattern "passed"
docker compose exec backend lint-imports
```
Esperado: `462 passed` (arquivo gravado) e `Contracts: 11 kept, 0 broken.`

### Passo 24: limpeza
```powershell
curl.exe -s -o NUL -w "HTTP %{http_code}`n" -X PATCH "$API/reservas/<ID>/situacao/" -H "Authorization: Bearer $tok" -H "Content-Type: application/json" -d '{\"situacao\":\"CANCELADA\",\"motivo\":\"Reserva de teste da demonstracao, cancelada.\"}'
```

## Observações do ensaio
- O primeiro ensaio teve o cronômetro quebrado (faltava `bc` no Git Bash); a sequência foi repetida com o cronômetro corrigido e **só o segundo ensaio tem tempos**. Ambos criaram e cancelaram a própria reserva de teste.
- Nenhum passo falhou no segundo ensaio. Os passos que esperam o *healthcheck* (11, 14, 17 e 19) levam de 6 a 9 s cada.
