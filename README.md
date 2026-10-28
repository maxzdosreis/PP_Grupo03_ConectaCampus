# Conecta Campus — Reserva de Quadras e Espaços Esportivos

Sistema para a comunidade acadêmica cadastrar quadras e espaços esportivos, solicitar reservas e acompanhar a situação de cada reserva.

## Tecnologias

- Python 3.12, Django 5.2 LTS, Django REST Framework 3.18, Simple JWT 5.5 (login com token)
- PostgreSQL 16 (driver psycopg 3)
- Node 24, React 19.3, TypeScript 6.0, Vite 8.3, React Router 8.4, ESLint 10; testes com Vitest 5, Testing Library 16 e jsdom 30 (só desenvolvimento)
- Docker e Docker Compose

## Como executar

### Pré-requisito

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (inclui o Docker Compose).

### Passo a passo

1. Na raiz do repositório, crie o arquivo de variáveis de ambiente a partir do exemplo:

   ```bash
   cp src/.env.example src/.env
   ```

   No Prompt de Comando do Windows:

   ```bat
   copy src\.env.example src\.env
   ```

   Se já existir um PostgreSQL rodando na porta 5432 do seu computador, mude só `DB_PORT_HOST` (ex.: `5433`). `DB_PORT` é a porta usada pelo Django dentro da rede do Docker e deve continuar `5432`.

2. Entre na pasta `src` e suba os três serviços (banco, backend e frontend):

   ```bash
   cd src
   docker compose up --build
   ```

   As migrations do banco são aplicadas automaticamente quando o backend sobe.

3. Com os serviços no ar, em outro terminal dentro de `src`, carregue os dados de exemplo (usuários, espaços e reservas; veja [Dados de exemplo](#dados-de-exemplo)):

   ```bash
   docker compose exec backend python manage.py carregar_dados_exemplo
   ```

4. Acesse:
   - Aplicação (frontend): http://localhost:5173 — a página inicial mostra a situação da API ("API no ar.") e os atalhos "Entrar" e "Criar conta" (ou "Ir para minhas reservas", com login).
   - Entrar: http://localhost:5173/entrar (ou "Entrar" no cabeçalho) — com o e-mail e a senha de um dos [usuários de exemplo](#dados-de-exemplo). Espaços e reservas exigem login: quem abre uma dessas telas sem login vai para a tela de entrar e volta para ela depois. O login continua valendo ao recarregar a página e em abas novas, e o token é renovado sozinho enquanto o refresh for válido (1 dia). O cabeçalho mostra quem está logado ("Nome · Perfil") e o botão "Sair".
   - Criar conta: http://localhost:5173/cadastro (ou "Cadastre-se" no cabeçalho) — cadastrar um solicitante com nome, matrícula, e-mail e senha; a conta já entra sozinha e abre a tela de nova reserva.
   - Tela de espaços: http://localhost:5173/espacos (ou o item "Espaços" do menu) — listar os espaços, com filtro por tipo e "Somente ativos"; o formulário de cadastro aparece só para o Gestor. Os filtros ficam no endereço da página, então recarregar mantém o filtro.
   - Tela de nova reserva: http://localhost:5173/reservas/nova (ou o item "Nova reserva" do menu, ou o link "Reservar" de um espaço ativo na tela de espaços, que já traz o espaço selecionado) — mostra quem está solicitando (nome e matrícula), solicitar uma reserva e ver o resumo com a situação "Solicitada".
   - Tela de consulta de reservas: http://localhost:5173/reservas (ou o item "Reservas" do menu, ou o link "Ver minhas reservas" do resumo de uma reserva solicitada) — listar as reservas com filtros por espaço, situação, data, solicitante (nome ou matrícula) e "Somente minhas reservas", que se combinam. O Solicitante vê só as próprias; o Gestor vê todas. Os filtros ficam no endereço da página; por exemplo, dois critérios combinados: http://localhost:5173/reservas?espaco=1&situacao=SOLICITADA.
   - Alterar a situação de uma reserva, na mesma tela: cada linha tem um botão para cada mudança permitida a partir da situação atual e ao perfil de quem está logado (para o Gestor, uma solicitada mostra "Confirmar", "Recusar" e "Cancelar" e uma confirmada, "Cancelar" e "Concluir"; o Solicitante só vê "Cancelar" nas próprias; as concluídas, recusadas e canceladas não têm ações). O botão abre um diálogo com o resumo da reserva; para recusar ou cancelar, ele pede o motivo, que o solicitante verá. Confirme no botão do diálogo (ex.: "Recusar reserva") ou feche com "Voltar" ou Esc sem alterar nada. Depois da mudança, a mensagem aparece no canto da tela e a lista é recarregada. Se outra pessoa já tiver mudado a reserva, o diálogo explica o motivo e oferece "Atualizar lista". As ações disponíveis vêm da API (`acoes_disponiveis` em cada reserva).
   - API: http://localhost:8000
   - Saúde da API: http://localhost:8000/api/health/
   - Admin do Django: http://localhost:8000/admin/

### Dados de exemplo

```bash
docker compose exec backend python manage.py carregar_dados_exemplo
```

O comando cria usuários, espaços e reservas passando pelas mesmas regras do sistema (casos de uso e entidades do domínio): se um dado de exemplo violasse uma regra, o comando falharia sem gravar nada. Pode ser executado mais de uma vez: o que já existe (usuário pelo e-mail, espaço pelo nome) não é criado de novo, e as reservas só são criadas se os solicitantes de exemplo ainda não tiverem nenhuma. Ele só roda com `DJANGO_DEBUG=True` (o valor do `.env.example`), porque cria usuários com senhas conhecidas.

**Usuários de exemplo.** As senhas são fictícias e servem **só para teste local**:

| Nome | E-mail | Matrícula | Perfil | Senha |
|---|---|---|---|---|
| Carla Mendes | `carla.mendes@exemplo.com` | 2026900 | Gestor (também entra no `/admin/`) | `Apito-Dourado-48` |
| Bruno Lima | `bruno.lima@exemplo.com` | 2026101 | Solicitante | `Rede-Alta-73` |
| Daniela Rocha | `daniela.rocha@exemplo.com` | 2026102 | Solicitante | `Cesta-Tripla-59` |

**Espaços:** Quadra Poliesportiva Central (30 pessoas), Campo de Futebol Principal (22), Ginásio Coberto (200), Quadra de Areia Norte (12), Quadra de Tênis 1 (4) — um de cada tipo — e a Quadra de Tênis 2 (4), **inativa**.

**Reservas**, com datas relativas ao dia em que o comando roda:

| Situação | Quando | Espaço | Solicitante |
|---|---|---|---|
| Solicitada | amanhã, 10:00–11:00 | Quadra Poliesportiva Central | Bruno Lima |
| Confirmada | amanhã, 14:00–16:00 | Campo de Futebol Principal | Daniela Rocha |
| Recusada (com motivo) | daqui a 2 dias, 19:00–21:00 | Ginásio Coberto | Bruno Lima |
| Cancelada (com motivo) | daqui a 3 dias, 08:00–09:00 | Quadra de Areia Norte | Daniela Rocha |
| Concluída | ontem, 18:00–19:30 | Quadra de Tênis 1 | Bruno Lima |

**Horário para demonstrar o conflito:** Quadra Poliesportiva Central, **amanhã, 10:30–11:30** — sobrepõe a reserva Solicitada e responde **409** `CONFLITO_DE_HORARIO`. O próprio comando imprime esse horário com a data no fim da saída.

#### Roteiro da demonstração

Pela tela, em http://localhost:5173, com os usuários de exemplo:

1. **Entrar como solicitante.** Abrir http://localhost:5173/reservas sem login: a aplicação leva para a tela de entrar. Entrar como Bruno (`bruno.lima@exemplo.com`, `Rede-Alta-73`); depois do login, ela volta para as reservas. O cabeçalho mostra "Bruno Lima · Solicitante".
2. **Consultar.** Bruno vê só as próprias reservas (Solicitada, Recusada e Concluída). Filtrar por espaço "Quadra Poliesportiva Central" e situação "Solicitada" (dois critérios combinados). Só a Solicitada tem ação, e só "Cancelar".
3. **Entrada inválida.** Em "Nova reserva", que mostra "Solicitante: Bruno Lima (2026101)", pedir a Quadra Poliesportiva Central **amanhã, 10:30–11:30**, com qualquer finalidade: o aviso no topo do formulário explica o conflito de horário (**409** `CONFLITO_DE_HORARIO`) e os valores continuam preenchidos. Outras entradas inválidas prontas: uma data de ontem, explicada embaixo do campo Data, e um término antes do início.
4. **Solicitar.** Trocar o horário para **16:00–17:00** e enviar: a mensagem de sucesso aparece e o resumo mostra a situação "Solicitada". "Ver minhas reservas" leva à lista com a nova reserva.
5. **Cancelar.** Na lista, cancelar a reserva Solicitada de amanhã às 10:00 (a dos dados de exemplo): o diálogo pede o motivo, e sem motivo o erro aparece embaixo do campo. Com o motivo, a reserva passa a "Cancelada".
6. **Sem permissão.** Em "Espaços", Bruno vê a lista e o aviso "Somente o gestor cadastra espaços.", sem o formulário. Sair (botão "Sair" no cabeçalho).
7. **Entrar como gestora** Carla (`carla.mendes@exemplo.com`, `Apito-Dourado-48`). Em "Espaços", cadastrar um espaço (ex.: "Quadra Coberta Sul", Quadra poliesportiva, 20 pessoas); um nome repetido ou uma capacidade 0 mostra o erro embaixo do campo.
8. **Confirmar e concluir.** Em "Reservas", Carla vê as reservas de todos. Confirmar a reserva das 16:00 do Bruno e depois concluí-la: cada mudança mostra a mensagem da API ("Reserva confirmada com sucesso.", "Reserva concluída com sucesso."), e a reserva concluída fica sem ações.

O mesmo roteiro com `curl`, na seção a seguir, mostra também o **403** de um solicitante tentando confirmar, que a tela não oferece.

#### Roteiro alternativo com `curl`

Troque `AAAA-MM-DD` pela data de amanhã e use os ids que aparecem em `GET /api/espacos/` (num banco recém-criado, a Quadra Poliesportiva Central é o espaço `1`). Os comandos de Windows seguem o padrão dos [exemplos de uso da API](#exemplos-de-uso-da-api).

1. Entrar como o solicitante Bruno e guardar o `access` em `ACCESS`, como em [Entrar (login) e usar o token](#entrar-login-e-usar-o-token):

   ```bash
   curl -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" -d '{"email": "bruno.lima@exemplo.com", "senha": "Rede-Alta-73"}'
   ```

2. Consultar as reservas e filtrar por dois critérios. Como Solicitante, o Bruno só vê as próprias (Solicitada, Recusada e Concluída), e `acoes_disponiveis` só traz "Cancelar" na Solicitada:

   ```bash
   curl "http://localhost:8000/api/reservas/?espaco=1&situacao=SOLICITADA" -H "Authorization: Bearer $ACCESS"
   ```

3. Entrada inválida: pedir o horário de conflito → **409** `CONFLITO_DE_HORARIO`:

   ```bash
   curl -X POST http://localhost:8000/api/reservas/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"espaco_id": 1, "data": "AAAA-MM-DD", "hora_inicio": "10:30", "hora_fim": "11:30", "finalidade": "Treino de futsal"}'
   ```

   Outras entradas inválidas prontas: a Quadra de Tênis 2 (inativa) → **409** `ESPACO_INATIVO`; uma data de ontem → **400** `DATA_RETROATIVA`.

4. Solicitar um horário livre (amanhã, 16:00–17:00) → **201**, situação `SOLICITADA`; anote o `id` da resposta:

   ```bash
   curl -X POST http://localhost:8000/api/reservas/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"espaco_id": 1, "data": "AAAA-MM-DD", "hora_inicio": "16:00", "hora_fim": "17:00", "finalidade": "Treino de futsal"}'
   ```

5. Ação sem permissão: ainda como Bruno, tentar confirmar a reserva do passo 4 (troque `ID`) → **403** `ACAO_NAO_PERMITIDA`, `"Somente o gestor pode confirmar reservas."`, e a reserva continua Solicitada:

   ```bash
   curl -X PATCH http://localhost:8000/api/reservas/ID/situacao/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"situacao": "CONFIRMADA"}'
   ```

6. Entrar como a gestora Carla (`carla.mendes@exemplo.com`, `Apito-Dourado-48`), guardar o novo `access` em `ACCESS` e repetir o mesmo comando → **200** `"Reserva confirmada com sucesso."`. A gestora vê as reservas de todos.

7. Concluir a mesma reserva → **200** `"Reserva concluída com sucesso."`, com `acoes_disponiveis` vazia:

   ```bash
   curl -X PATCH http://localhost:8000/api/reservas/ID/situacao/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"situacao": "CONCLUIDA"}'
   ```

   Tentar voltá-la para `SOLICITADA` responde **409** `TRANSICAO_DE_SITUACAO_INVALIDA`.

#### Recomeçar do zero

Para apagar tudo (inclusive o que foi cadastrado à mão) e carregar os dados de novo, dentro de `src`:

```bash
docker compose down -v
```

```bash
docker compose up -d
```

```bash
docker compose exec backend python manage.py carregar_dados_exemplo
```

### Verificar se a API está no ar

`GET /api/health/` testa a conexão com o banco:

- **200** — `{"mensagem": "API no ar.", "dados": {"banco": "ok"}}`
- **503** — `{"erro": {"codigo": "BANCO_INDISPONIVEL", "mensagem": "Não foi possível conectar ao banco de dados."}}`

### Exemplos de uso da API

Todo endpoint exige login com token JWT, exceto `GET /api/health/`, cadastro, login, refresh e os vocabulários `GET /api/espacos/tipos/` e `GET /api/reservas/situacoes/`. Sem token, a resposta é **401** `NAO_AUTENTICADO`. Para os exemplos de espaços, entre como a gestora de exemplo Carla (`carla.mendes@exemplo.com`, `Apito-Dourado-48`), porque só o Gestor cadastra espaços, e guarde o `access` em `ACCESS` como em [Entrar (login) e usar o token](#entrar-login-e-usar-o-token). Toda resposta segue o mesmo formato: `{"mensagem", "dados"}` no sucesso e `{"erro": {"codigo", "mensagem", "campos"?}}` no erro.

Tipos aceitos em `tipo`: `QUADRA_POLIESPORTIVA`, `CAMPO_DE_FUTEBOL`, `GINASIO`, `QUADRA_DE_AREIA`, `QUADRA_DE_TENIS`. A mesma lista, com os rótulos, sai de `GET /api/espacos/tipos/` (é dela que o frontend monta os seletores):

```bash
curl http://localhost:8000/api/espacos/tipos/
```

```json
{"mensagem": "Tipos de espaço disponíveis.", "dados": [{"valor": "QUADRA_POLIESPORTIVA", "rotulo": "Quadra poliesportiva"}, {"valor": "CAMPO_DE_FUTEBOL", "rotulo": "Campo de futebol"}, {"valor": "GINASIO", "rotulo": "Ginásio"}, {"valor": "QUADRA_DE_AREIA", "rotulo": "Quadra de areia"}, {"valor": "QUADRA_DE_TENIS", "rotulo": "Quadra de tênis"}]}
```

Cadastrar um espaço (`POST /api/espacos/`, só Gestor):

```bash
curl -X POST http://localhost:8000/api/espacos/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"nome": "Quadra Central", "tipo": "QUADRA_POLIESPORTIVA", "capacidade": 20}'
```

No Prompt de Comando do Windows, as aspas internas são escapadas:

```bat
curl -X POST http://localhost:8000/api/espacos/ -H "Authorization: Bearer %ACCESS%" -H "Content-Type: application/json" -d "{\"nome\": \"Quadra Central\", \"tipo\": \"QUADRA_POLIESPORTIVA\", \"capacidade\": 20}"
```

Resposta **201**:

```json
{"mensagem": "Espaço cadastrado com sucesso.", "dados": {"id": 1, "nome": "Quadra Central", "tipo": "QUADRA_POLIESPORTIVA", "tipo_rotulo": "Quadra poliesportiva", "capacidade": 20, "ativo": true}}
```

Repetir o mesmo cadastro responde **409**:

```json
{"erro": {"codigo": "NOME_DE_ESPACO_JA_CADASTRADO", "mensagem": "Já existe um espaço com este nome.", "campos": {"nome": ["Já existe um espaço com este nome."]}}}
```

Outros erros de cadastro: capacidade `0` → **400** `CAPACIDADE_INVALIDA`; tipo fora da lista → **400** `TIPO_DE_ESPACO_INVALIDO`; nome vazio → **400** `CAMPO_OBRIGATORIO_AUSENTE`; token de um Solicitante → **403**:

```json
{"erro": {"codigo": "ACAO_NAO_PERMITIDA", "mensagem": "Você não tem permissão para realizar esta ação."}}
```

> No Windows, nomes com acento passados direto no `-d` podem chegar fora de UTF-8 e a API responde `JSON_INVALIDO`. Nesse caso, salve o corpo num arquivo UTF-8 e envie com `--data-binary @espaco.json`.

Listar os espaços (`GET /api/espacos/`, qualquer usuário logado), ordenados por nome. Filtros opcionais: `apenas_ativos=true` e `tipo=<TIPO>`, combináveis:

```bash
curl "http://localhost:8000/api/espacos/?tipo=QUADRA_POLIESPORTIVA&apenas_ativos=true" -H "Authorization: Bearer $ACCESS"
```

```json
{"mensagem": "1 espaço encontrado.", "dados": [{"id": 1, "nome": "Quadra Central", "tipo": "QUADRA_POLIESPORTIVA", "tipo_rotulo": "Quadra poliesportiva", "capacidade": 20, "ativo": true}]}
```

Obter um espaço (`GET /api/espacos/{id}/`):

```bash
curl http://localhost:8000/api/espacos/1/ -H "Authorization: Bearer $ACCESS"
```

Um id inexistente responde **404**:

```json
{"erro": {"codigo": "ESPACO_NAO_ENCONTRADO", "mensagem": "Espaço de código 9999 não encontrado."}}
```

#### Entrar (login) e usar o token

As reservas exigem login com token JWT. O login devolve dois tokens: o `access`, enviado em cada pedido no cabeçalho `Authorization: Bearer <access>` e válido por 30 minutos, e o `refresh`, que gera um `access` novo e vale 1 dia (os dois prazos mudam em `JWT_ACCESS_MINUTES` e `JWT_REFRESH_DAYS` no `.env`).

Primeiro cadastre um usuário (`POST /api/auth/cadastro/`, público). O cadastro cria sempre um **Solicitante**: `perfil`, `is_staff` ou `is_superuser` enviados no corpo são ignorados. Um Gestor só nasce pelo `createsuperuser` (veja a seção abaixo) ou pelo admin. A senha precisa ter pelo menos 8 caracteres, não pode ser comum, só números nem parecida com o e-mail, o nome ou a matrícula. A matrícula tem até 20 caracteres, sem espaços.

```bash
curl -X POST http://localhost:8000/api/auth/cadastro/ -H "Content-Type: application/json" -d '{"nome": "Ana Souza", "matricula": "2026001", "email": "ana@exemplo.com", "senha": "senha-de-teste-123"}'
```

No Prompt de Comando do Windows:

```bat
curl -X POST http://localhost:8000/api/auth/cadastro/ -H "Content-Type: application/json" -d "{\"nome\": \"Ana Souza\", \"matricula\": \"2026001\", \"email\": \"ana@exemplo.com\", \"senha\": \"senha-de-teste-123\"}"
```

Resposta **201** (o cadastro não faz login nem devolve tokens):

```json
{"mensagem": "Cadastro realizado com sucesso. Faça login para continuar.", "dados": {"id": 1, "nome": "Ana Souza", "email": "ana@exemplo.com", "matricula": "2026001", "perfil": "SOLICITANTE", "perfil_rotulo": "Solicitante", "eh_gestor": false}}
```

Cadastrar de novo o mesmo e-mail (mesmo em outra caixa, como `ANA@exemplo.com`) responde **409**:

```json
{"erro": {"codigo": "EMAIL_JA_CADASTRADO", "mensagem": "Já existe um usuário com este e-mail.", "campos": {"email": ["Já existe um usuário com este e-mail."]}}}
```

Outros erros de cadastro: matrícula repetida → **409** `MATRICULA_JA_CADASTRADA`; senha `12345678` → **400** `SENHA_FRACA` ("Esta senha é muito comum. Esta senha é inteiramente numérica."); matrícula com espaço ou com mais de 20 caracteres → **400** `MATRICULA_INVALIDA`; e-mail malformado → **400** `DADOS_INVALIDOS`; nome em branco → **400** `CAMPO_OBRIGATORIO_AUSENTE`.

Entrar (`POST /api/auth/login/`) com `email` e `senha`:

```bash
curl -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" -d '{"email": "ana@exemplo.com", "senha": "senha-de-teste-123"}'
```

No Prompt de Comando do Windows:

```bat
curl -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" -d "{\"email\": \"ana@exemplo.com\", \"senha\": \"senha-de-teste-123\"}"
```

Resposta **200** (tokens encurtados aqui):

```json
{"mensagem": "Login realizado com sucesso.", "dados": {"access": "eyJhbGciOi...", "refresh": "eyJhbGciOi...", "usuario": {"id": 1, "nome": "Ana Souza", "email": "ana@exemplo.com", "matricula": "2026001", "perfil": "SOLICITANTE", "perfil_rotulo": "Solicitante", "eh_gestor": false}}}
```

E-mail ou senha errados (ou usuário desativado) respondem sempre igual, **401**:

```json
{"erro": {"codigo": "CREDENCIAIS_INVALIDAS", "mensagem": "E-mail ou senha incorretos."}}
```

Copie o valor de `access` para uma variável e use-o nos exemplos seguintes:

```bash
ACCESS="cole-aqui-o-access"
```

No Prompt de Comando do Windows (sem aspas):

```bat
set ACCESS=cole-aqui-o-access
```

Ver o usuário logado (`GET /api/auth/me/`):

```bash
curl http://localhost:8000/api/auth/me/ -H "Authorization: Bearer $ACCESS"
```

```json
{"mensagem": "Usuário autenticado.", "dados": {"id": 1, "nome": "Ana Souza", "email": "ana@exemplo.com", "matricula": "2026001", "perfil": "SOLICITANTE", "perfil_rotulo": "Solicitante", "eh_gestor": false}}
```

Quando o `access` expira, os pedidos respondem **401** `NAO_AUTENTICADO`. Gere outro com o `refresh` (`POST /api/auth/refresh/`):

```bash
curl -X POST http://localhost:8000/api/auth/refresh/ -H "Content-Type: application/json" -d '{"refresh": "cole-aqui-o-refresh"}'
```

```json
{"mensagem": "Token renovado.", "dados": {"access": "eyJhbGciOi..."}}
```

Um `refresh` inválido ou expirado responde **401** `NAO_AUTENTICADO`; aí é preciso entrar de novo. Para sair, basta descartar os dois tokens.

#### Solicitar uma reserva

Solicitar uma reserva exige o token do login. O solicitante é sempre o usuário logado; um `solicitante` enviado no corpo é ignorado.

Solicitar a reserva (`POST /api/reservas/`), com data no formato `AAAA-MM-DD` e horas em `HH:MM`, usando o id de um espaço cadastrado:

```bash
curl -X POST http://localhost:8000/api/reservas/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"espaco_id": 1, "data": "2026-11-10", "hora_inicio": "10:00", "hora_fim": "11:00", "finalidade": "Treino de volei"}'
```

No Prompt de Comando do Windows:

```bat
curl -X POST http://localhost:8000/api/reservas/ -H "Authorization: Bearer %ACCESS%" -H "Content-Type: application/json" -d "{\"espaco_id\": 1, \"data\": \"2026-11-10\", \"hora_inicio\": \"10:00\", \"hora_fim\": \"11:00\", \"finalidade\": \"Treino de volei\"}"
```

Resposta **201**, com a reserva na situação inicial `SOLICITADA` (a resposta traz `espaco_id`; o nome do espaço vem da listagem de espaços):

```json
{"mensagem": "Reserva solicitada com sucesso. Aguarde a confirmação do gestor.", "dados": {"id": 1, "espaco_id": 1, "solicitante": {"usuario_id": 1, "nome": "Ana Souza", "matricula": "2026001"}, "data": "2026-11-10", "hora_inicio": "10:00", "hora_fim": "11:00", "finalidade": "Treino de volei", "situacao": "SOLICITADA", "situacao_rotulo": "Solicitada", "motivo_da_situacao": null, "criada_em": "2026-10-22T15:57:00.442650-03:00", "acoes_disponiveis": [{"situacao": "CANCELADA", "rotulo": "Cancelar", "exige_motivo": true}]}}
```

`acoes_disponiveis` depende de quem pergunta: a Ana é Solicitante e, na própria reserva Solicitada, só pode cancelar. A mesma reserva vista por um Gestor traz Confirmar, Recusar e Cancelar.

Repetir o pedido no mesmo horário responde **409**:

```json
{"erro": {"codigo": "CONFLITO_DE_HORARIO", "mensagem": "Este espaço já tem uma reserva Solicitada em 10/11/2026 10:00–11:00. Escolha outro horário."}}
```

Outros erros: sem token → **401** `NAO_AUTENTICADO`; espaço inexistente → **404** `ESPACO_NAO_ENCONTRADO`; espaço inativo → **409** `ESPACO_INATIVO`; término igual ou antes do início → **400** `HORARIO_INVALIDO`; horário que já passou → **400** `DATA_RETROATIVA`; campo ausente ou data inválida → **400** `DADOS_INVALIDOS` com o campo em `campos`.

#### Consultar reservas

Listar as reservas (`GET /api/reservas/`) exige login e devolve as reservas ordenadas pelo início. Filtros opcionais, que funcionam sozinhos ou combinados:

| Parâmetro | Exemplo | Efeito |
|---|---|---|
| `espaco` | `espaco=1` | reservas do espaço com esse id (um id inexistente devolve lista vazia) |
| `situacao` | `situacao=SOLICITADA` | `SOLICITADA`, `CONFIRMADA`, `RECUSADA`, `CANCELADA` ou `CONCLUIDA` |
| `data` | `data=2026-11-10` | reservas desse dia (`AAAA-MM-DD`) |
| `solicitante` | `solicitante=souza` | trecho do nome ou da matrícula, sem diferenciar maiúsculas |
| `minhas` | `minhas=true` | só as reservas do usuário logado |

> O Solicitante só vê as próprias reservas, qualquer que seja o filtro (inclusive `minhas=false` ou `solicitante=` com o nome de outra pessoa). O Gestor vê todas e pode filtrar por solicitante.

Por um critério:

```bash
curl "http://localhost:8000/api/reservas/?situacao=SOLICITADA" -H "Authorization: Bearer $ACCESS"
```

Por dois critérios combinados:

```bash
curl "http://localhost:8000/api/reservas/?espaco=1&situacao=SOLICITADA" -H "Authorization: Bearer $ACCESS"
```

Só as reservas do usuário logado:

```bash
curl "http://localhost:8000/api/reservas/?minhas=true" -H "Authorization: Bearer $ACCESS"
```

Resposta **200** (a mensagem informa a quantidade: "Nenhuma reserva encontrada.", "1 reserva encontrada." ou "N reservas encontradas."):

```json
{"mensagem": "1 reserva encontrada.", "dados": [{"id": 1, "espaco_id": 1, "solicitante": {"usuario_id": 1, "nome": "Ana Souza", "matricula": "2026001"}, "data": "2026-11-10", "hora_inicio": "10:00", "hora_fim": "11:00", "finalidade": "Treino de volei", "situacao": "SOLICITADA", "situacao_rotulo": "Solicitada", "motivo_da_situacao": null, "criada_em": "2026-10-22T15:57:00.442650-03:00", "acoes_disponiveis": [{"situacao": "CANCELADA", "rotulo": "Cancelar", "exige_motivo": true}]}]}
```

Um filtro em formato inválido (por exemplo, `situacao=XYZ`, `data=2026-13-40` ou `espaco=abc`) responde **400** `DADOS_INVALIDOS`, com o parâmetro em `campos`.

As situações aceitas no filtro, com o rótulo exibido (`GET /api/reservas/situacoes/`, não exige login):

```bash
curl http://localhost:8000/api/reservas/situacoes/
```

```json
{"mensagem": "Situações de reserva disponíveis.", "dados": [{"valor": "SOLICITADA", "rotulo": "Solicitada"}, {"valor": "CONFIRMADA", "rotulo": "Confirmada"}, {"valor": "RECUSADA", "rotulo": "Recusada"}, {"valor": "CANCELADA", "rotulo": "Cancelada"}, {"valor": "CONCLUIDA", "rotulo": "Concluída"}]}
```

Obter uma reserva (`GET /api/reservas/{id}/`), no mesmo formato da criação:

```bash
curl http://localhost:8000/api/reservas/1/ -H "Authorization: Bearer $ACCESS"
```

Um id inexistente responde **404**:

```json
{"erro": {"codigo": "RESERVA_NAO_ENCONTRADA", "mensagem": "Reserva de código 9999 não encontrada."}}
```

Para um Solicitante, a reserva de outra pessoa também responde **404**, e não 403, para não revelar que ela existe. Com os dados de exemplo, logado como Bruno, pedir a reserva Confirmada da Daniela (troque `ID_DA_DANIELA` pelo id que a gestora vê em `GET /api/reservas/`):

```bash
curl http://localhost:8000/api/reservas/ID_DA_DANIELA/ -H "Authorization: Bearer $ACCESS"
```

```json
{"erro": {"codigo": "RESERVA_NAO_ENCONTRADA", "mensagem": "Reserva de código 2 não encontrada."}}
```

#### Alterar a situação de uma reserva

Alterar a situação (`PATCH /api/reservas/{id}/situacao/`) exige login. Cada reserva devolvida pela API traz `acoes_disponiveis`, com as mudanças aceitas a partir da situação atual, o texto do botão e se exigem motivo. O corpo leva `situacao` e, para recusar ou cancelar, um `motivo`. Só estas mudanças são aceitas:

| Situação atual | Pode ir para |
|---|---|
| `SOLICITADA` | `CONFIRMADA`, `RECUSADA` (com motivo), `CANCELADA` (com motivo) |
| `CONFIRMADA` | `CONCLUIDA`, `CANCELADA` (com motivo) |
| `CONCLUIDA`, `RECUSADA`, `CANCELADA` | nenhuma (situações finais) |

Quem pode fazer cada mudança:

| Perfil | Pode levar para |
|---|---|
| Gestor | `CONFIRMADA`, `RECUSADA`, `CONCLUIDA`, `CANCELADA`, em qualquer reserva |
| Solicitante | só `CANCELADA`, e só nas próprias reservas |

Um Solicitante que tenta confirmar, recusar ou concluir recebe **403**, mesmo que a mudança fosse inválida pela tabela de situações, e a reserva fica como estava. Com o token do Bruno, confirmar a própria reserva:

```json
{"erro": {"codigo": "ACAO_NAO_PERMITIDA", "mensagem": "Somente o gestor pode confirmar reservas."}}
```

Mudar a situação da reserva de outra pessoa responde **404** `RESERVA_NAO_ENCONTRADA`, como no detalhe.

Confirmar a reserva (com o token de um Gestor):

```bash
curl -X PATCH http://localhost:8000/api/reservas/1/situacao/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"situacao": "CONFIRMADA"}'
```

No Prompt de Comando do Windows:

```bat
curl -X PATCH http://localhost:8000/api/reservas/1/situacao/ -H "Authorization: Bearer %ACCESS%" -H "Content-Type: application/json" -d "{\"situacao\": \"CONFIRMADA\"}"
```

Resposta **200**, com a reserva atualizada (a mensagem acompanha a nova situação: confirmada, recusada, cancelada ou concluída):

```json
{"mensagem": "Reserva confirmada com sucesso.", "dados": {"id": 1, "espaco_id": 1, "solicitante": {"usuario_id": 1, "nome": "Ana Souza", "matricula": "2026001"}, "data": "2026-11-10", "hora_inicio": "10:00", "hora_fim": "11:00", "finalidade": "Treino de volei", "situacao": "CONFIRMADA", "situacao_rotulo": "Confirmada", "motivo_da_situacao": null, "criada_em": "2026-10-22T15:57:00.442650-03:00", "acoes_disponiveis": [{"situacao": "CANCELADA", "rotulo": "Cancelar", "exige_motivo": true}, {"situacao": "CONCLUIDA", "rotulo": "Concluir", "exige_motivo": false}]}}
```

Uma mudança fora da tabela (por exemplo, voltar a confirmada para `SOLICITADA`) responde **409** e a reserva fica como estava:

```json
{"erro": {"codigo": "TRANSICAO_DE_SITUACAO_INVALIDA", "mensagem": "Não é possível alterar uma reserva Confirmada para Solicitada."}}
```

Cancelar com motivo (o horário fica livre para outra reserva):

```bash
curl -X PATCH http://localhost:8000/api/reservas/1/situacao/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"situacao": "CANCELADA", "motivo": "Chuva forte"}'
```

```json
{"mensagem": "Reserva cancelada com sucesso.", "dados": {"id": 1, "espaco_id": 1, "solicitante": {"usuario_id": 1, "nome": "Ana Souza", "matricula": "2026001"}, "data": "2026-11-10", "hora_inicio": "10:00", "hora_fim": "11:00", "finalidade": "Treino de volei", "situacao": "CANCELADA", "situacao_rotulo": "Cancelada", "motivo_da_situacao": "Chuva forte", "criada_em": "2026-10-22T15:57:00.442650-03:00", "acoes_disponiveis": []}}
```

Outros erros: recusar ou cancelar sem motivo → **400** `MOTIVO_OBRIGATORIO`; situação fora da lista → **400** `SITUACAO_INVALIDA`; corpo sem `situacao` → **400** `DADOS_INVALIDOS`; reserva inexistente → **404** `RESERVA_NAO_ENCONTRADA`; sem token → **401** `NAO_AUTENTICADO`; outro método além de `PATCH` → **405** `METODO_NAO_PERMITIDO`.

### Criar um superusuário (acesso ao admin)

Com os serviços no ar, em outro terminal dentro de `src`:

```bash
docker compose exec backend python manage.py createsuperuser
```

O comando pede **e-mail, nome, matrícula e senha**. O login no admin é feito com o e-mail, e o superusuário é criado com o perfil **Gestor**.

> **Quem subiu o banco antes da AUT-02:** a migration `contas.0002` remove o `username` e torna nome e matrícula obrigatórios, partindo de uma tabela de usuários vazia. Apague o banco local uma vez antes de subir de novo:
>
> ```bash
> docker compose down -v
> ```

### Frontend: lint, testes e build

Com os serviços no ar, dentro de `src`:

```bash
docker compose exec frontend npm run lint
```

Testes (Vitest e Testing Library, em jsdom):

```bash
docker compose exec frontend npm test -- --run
```

```bash
docker compose exec frontend npm run build
```

As dependências do frontend ficam num volume próprio do container (`/app/node_modules`). Ao mudar o `package.json` (instalar, remover ou atualizar pacotes), recrie esse volume:

```bash
docker compose up --build -V frontend
```

### Qualidade do código (backend)

Com os serviços no ar, dentro de `src`. As configurações ficam em `src/backend/pyproject.toml`.

Testes (pytest):

```bash
docker compose exec backend pytest
```

Cobertura de testes dos contextos `espacos`, `reservas` e `contas`, do pacote `compartilhado` e do app `exemplos`:

```bash
docker compose exec backend pytest --cov
```

Linter e formatação (ruff):

```bash
docker compose exec backend sh -c "ruff check . && ruff format --check ."
```

Regra de dependência entre camadas e contextos (import-linter):

```bash
docker compose exec backend lint-imports
```

Verificação completa, antes de cada PR:

```bash
docker compose exec backend sh -c "ruff check . && ruff format --check . && lint-imports && pytest"
```

Ao mudar o `requirements.txt` ou o `requirements-dev.txt`, reconstrua a imagem do backend:

```bash
docker compose up --build -d backend
```

### Parar a aplicação

```bash
docker compose down
```

Para parar **e apagar os dados do banco**:

```bash
docker compose down -v
```

## Persistência

PostgreSQL 16, executado no container `db`. Os dados ficam no volume Docker `postgres_data` e se mantêm entre execuções até um `docker compose down -v`.

## Limitações conhecidas

- **Sem revogação de tokens:** não há lista de tokens revogados. Sair é descartar os tokens no cliente; um `access` roubado continua valendo até expirar (30 minutos) e um `refresh`, até 1 dia.
- **Sessão no `localStorage`:** o frontend guarda os tokens e os dados do usuário no `localStorage` do navegador (chave `conecta-campus:sessao`), para o login sobreviver ao recarregar e a abas novas. Um script malicioso injetado na página (XSS) poderia ler esses tokens; cookies `HttpOnly` evitariam isso, mas exigiriam mudar a autenticação da API. Se o navegador recusar o `localStorage` (navegação privada), o login vale só até recarregar.
- **Perfil na interface:** esconder o formulário de espaços de quem não é Gestor é só conveniência; quem garante as permissões é a API (403 `ACAO_NAO_PERMITIDA`).
- **Alterações simultâneas na mesma reserva:** se duas pessoas mudarem a situação da mesma reserva ao mesmo tempo, vale a última gravada (não há bloqueio otimista). Para o porte do projeto, isso é aceitável.
