# Backend — API do Conecta Campus

API REST em Python 3.12, Django 5.2 LTS, Django REST Framework 3.18 e Simple JWT 5.5, com PostgreSQL 16 (psycopg 3). Roda no serviço `backend` do Docker Compose ([serviços e variáveis](../README.md)). Todos os comandos abaixo rodam dentro de `src`, com os serviços no ar.

Ferramentas de desenvolvimento (`requirements-dev.txt`, instaladas na mesma imagem): pytest 9.1, pytest-django 4.14, pytest-cov 7.1, ruff 0.17, import-linter 2.15, Hypothesis 6.170 e mutmut 3.8. As configurações delas ficam em `pyproject.toml`.

## Organização

| Pasta | O que é | README |
|---|---|---|
| `config/` | Composição do projeto: `settings.py`, `urls.py` (monta as rotas de cada contexto sob `api/`), `GET /api/health/` (`views.py`) e os testes de segurança (`config/tests/`: matriz de acesso, perfil lido do banco, CORS). Não tem regra de negócio. | este |
| `contas/` | Contexto de usuários, perfis e autenticação. | [contas](contas/README.md) |
| `espacos/` | Contexto de quadras e espaços esportivos. | [espacos](espacos/README.md) |
| `reservas/` | Contexto de reservas, situação, agenda e histórico. | [reservas](reservas/README.md) |
| `compartilhado/` | Base comum aos contextos (erros, respostas, tratador de erros, permissão de gestor). Não é contexto nem app Django. | [compartilhado](compartilhado/README.md) |
| `exemplos/` | Comando `carregar_dados_exemplo`. É composição, como o `config`: o único que conhece os três contextos. | [exemplos](exemplos/README.md) |

### Camadas de cada contexto

| Camada | Conteúdo | Pode importar |
|---|---|---|
| `domain/` | Entidades, objetos de valor, enums, regras e exceções. Python puro. | só `compartilhado.domain` |
| `application/` | Casos de uso (uma classe com `executar(...)`) e as portas (`typing.Protocol`) dos repositórios. | `domain` |
| `infrastructure/` | Models do Django ORM (sufixo `Model`), migrations e repositórios Django (model ↔ entidade). | `application`, `domain` |
| `api/` | Serializers (só formato), views do DRF, `urls.py` e `dependencias.py`, o único módulo da `api/` que monta os casos de uso com a infraestrutura. | as três de baixo e `compartilhado.api` |

Um contexto consultado por outro expõe `<contexto>/publico.py` (funções e DTOs imutáveis). Exemplo: `reservas` consulta um espaço pela porta `ConsultaDeEspacos` (`reservas/application/portas.py`), implementada por `ConsultaDeEspacosViaFachada`, que chama `espacos.publico`. Reserva guarda só o `espaco_id`, sem chave estrangeira entre contextos.

### Regra de dependência (import-linter)

Os contratos de `pyproject.toml` são conferidos por `lint-imports` ([comando](#comandos)):

| Contrato | O que garante |
|---|---|
| Domínio é Python puro | `domain` de `compartilhado`, `espacos`, `reservas` e `contas` não importa `django` nem `rest_framework`. |
| compartilhado não depende dos contextos | `compartilhado` não importa `espacos`, `reservas`, `contas` nem `config`. |
| Só a camada api usa compartilhado.api | `domain`, `application` e `infrastructure` dos contextos não importam `compartilhado.api`. |
| Camadas de cada contexto | Em `espacos`, `reservas` e `contas`: `api` → `infrastructure` → `application` → `domain`, nunca ao contrário. |
| espacos não depende de outros contextos | `espacos` não importa `reservas` nem `contas`. |
| contas não depende de outros contextos | `contas` não importa `espacos` nem `reservas`. |
| reservas não importa contas | O usuário logado chega a `reservas` por `request.user`, lido por duck typing. |
| reservas só conversa com espacos pela fachada pública | `reservas` não importa as camadas de `espacos`, só `espacos.publico`. |
| Domínio e aplicação de reservas não conhecem espacos | Só a `infrastructure` de `reservas` chama a fachada. |
| Nenhum contexto depende dos dados de exemplo | Nenhum contexto nem `compartilhado` importa `exemplos`. |

## Formato das respostas e dos erros

Toda resposta segue o mesmo formato: `{"mensagem", "dados", "paginacao"?}` no sucesso e `{"erro": {"codigo", "mensagem", "campos"?}}` no erro. `paginacao` (`{"pagina", "tamanho", "total", "total_de_paginas"}`) só aparece na consulta de reservas, que é paginada ([reservas](reservas/README.md#consultar-reservas)); nela, `dados` é a lista da página e a mensagem conta o total. `campos` aparece quando o erro é de um campo, com a lista de mensagens de cada um. Os detalhes (exceções de domínio, categorias e o tratador) estão no [README do compartilhado](compartilhado/README.md).

| Status | Quando | Exemplos de `codigo` |
|---|---|---|
| 400 | Dados que violam uma regra, formato inválido ou JSON malformado | `CAMPO_OBRIGATORIO_AUSENTE`, `DADOS_INVALIDOS`, `JSON_INVALIDO` |
| 401 | Sem token, token inválido ou expirado | `NAO_AUTENTICADO`, `CREDENCIAIS_INVALIDAS` |
| 403 | O perfil não pode fazer a ação | `ACAO_NAO_PERMITIDA` |
| 404 | O que foi referenciado não existe (ou não é visível para quem pede) | `ESPACO_NAO_ENCONTRADO`, `RESERVA_NAO_ENCONTRADA`, `NAO_ENCONTRADO` |
| 405 | Método que a rota não aceita | `METODO_NAO_PERMITIDO` |
| 409 | A operação contradiz o estado atual | `CONFLITO_DE_HORARIO`, `TRANSICAO_DE_SITUACAO_INVALIDA`, `ESPACO_INATIVO` |
| 429 | Tentativas de login ou de cadastro acima do limite (com o cabeçalho `Retry-After`, em segundos) | `LIMITE_DE_TENTATIVAS` |
| 500 | Erro inesperado (vai para o log, sem detalhes na resposta) | `ERRO_INTERNO` |
| 503 | Banco fora do ar (só em `GET /api/health/`); Redis fora do ar (`CACHE_INDISPONIVEL` no health, `SERVICO_INDISPONIVEL` no login e no cadastro) | `BANCO_INDISPONIVEL`, `CACHE_INDISPONIVEL`, `SERVICO_INDISPONIVEL` |

Todo endpoint exige login com token JWT, exceto `GET /api/health/`, cadastro, login, refresh, logout e os vocabulários `GET /api/espacos/tipos/`, `GET /api/reservas/situacoes/` e `GET /api/reservas/regras-de-agenda/`. Sem token, a resposta é **401** `NAO_AUTENTICADO`. Quem pode chamar cada rota está em cada contexto e é provado por `config/tests/test_matriz_de_acesso.py`.

## Autenticação JWT

O login devolve dois tokens: o `access`, enviado em cada pedido no cabeçalho `Authorization: Bearer <access>` e válido por 30 minutos, e o `refresh`, que gera um `access` novo e vale 1 dia desde o login (os dois prazos mudam em `JWT_ACCESS_MINUTES` e `JWT_REFRESH_DAYS` no `.env`). O `refresh` é de uso único: cada renovação devolve outro e revoga o usado, e sair o revoga (AUT-09). O cadastro de usuários e o `GET /api/auth/me/` estão no [README de contas](contas/README.md).

### Entrar (login) e usar o token

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

E-mail ou senha errados (ou usuário desativado) respondem sempre igual, **401** `CREDENCIAIS_INVALIDAS` ([exemplo](contas/README.md#erros-do-login)).

Copie o valor de `access` para uma variável e use-o nos exemplos seguintes:

```bash
ACCESS="cole-aqui-o-access"
```

No Prompt de Comando do Windows (sem aspas):

```bat
set ACCESS=cole-aqui-o-access
```

### Renovar e sair

Quando o `access` expira, os pedidos respondem **401** `NAO_AUTENTICADO`. Gere outro com o `refresh` (`POST /api/auth/refresh/`). A resposta traz um `access` **e um `refresh` novos**; guarde os dois, porque o `refresh` enviado deixa de valer:

```bash
curl -X POST http://localhost:8000/api/auth/refresh/ -H "Content-Type: application/json" -d '{"refresh": "cole-aqui-o-refresh"}'
```

```json
{"mensagem": "Token renovado.", "dados": {"access": "eyJhbGciOi...", "refresh": "eyJhbGciOi..."}}
```

O `refresh` novo vence no mesmo momento que o do login (1 dia depois de entrar): renovar não estende a sessão. Um `refresh` inválido, expirado, revogado ou já usado numa renovação responde **401** `NAO_AUTENTICADO`; aí é preciso entrar de novo.

Para sair, revogue o `refresh` (`POST /api/auth/logout/`, sem precisar do `access`):

```bash
curl -X POST http://localhost:8000/api/auth/logout/ -H "Content-Type: application/json" -d '{"refresh": "cole-aqui-o-refresh"}'
```

```json
{"mensagem": "Você saiu da sua conta.", "dados": null}
```

Depois disso, o `refresh` não renova mais. O `access` não é revogado e vale até expirar (veja as [limitações conhecidas](../../README.md#limitações-conhecidas)). Os detalhes do logout estão no [README de contas](contas/README.md#sair-logout).

### Tokens guardados no banco

A lista negra do Simple JWT (`rest_framework_simplejwt.token_blacklist`, em `INSTALLED_APPS`) guarda cada `refresh` emitido (`OutstandingToken`) e cada um revogado (`BlacklistedToken`); as duas tabelas aparecem no admin. Elas crescem a cada login e renovação. Para apagar os tokens já vencidos:

```bash
docker compose exec backend python manage.py flushexpiredtokens
```

Na avaliação local não é preciso rodá-lo. As tabelas são criadas pelo `migrate` que roda ao subir o backend; um `refresh` emitido antes delas existirem também pode ser renovado e revogado.

## Criar um superusuário (acesso ao admin)

Com os serviços no ar, em outro terminal dentro de `src`:

```bash
docker compose exec backend python manage.py createsuperuser
```

O comando pede **e-mail, nome, matrícula e senha**. O login no admin (http://localhost:8000/admin/) é feito com o e-mail, e o superusuário é criado com o perfil **Gestor**. É a única forma, além do admin e dos [dados de exemplo](exemplos/README.md), de criar um Gestor: o cadastro público cria sempre um Solicitante.

> **Quem subiu o banco antes da AUT-02:** a migration `contas.0002` remove o `username` e torna nome e matrícula obrigatórios, partindo de uma tabela de usuários vazia. Apague o banco local uma vez antes de subir de novo:
>
> ```bash
> docker compose down -v
> ```

## Comandos

As migrations rodam sozinhas quando o backend sobe. Manualmente, se necessário:

```bash
docker compose exec backend python manage.py migrate
```

Migrations novas são sempre geradas pelo Django, nunca escritas à mão (`docker compose exec backend python manage.py makemigrations <app>`).

Testes (pytest):

```bash
docker compose exec backend pytest
```

Cobertura de testes (linhas e ramos) dos contextos `espacos`, `reservas` e `contas`, do pacote `compartilhado` e do app `exemplos`. Falha abaixo de 99% no total (`fail_under` em `pyproject.toml`; cobertura-alvo da DEC-08, adotada provisoriamente pelo grupo):

```bash
docker compose exec backend pytest --cov
```

Cobertura por camada: exige 100% de linhas e ramos no domínio e na aplicação de `espacos` e de `reservas` (troque o `--include` para ver outra camada, por exemplo `reservas/infrastructure/*`):

```bash
docker compose exec backend sh -c "pytest --cov && coverage report --include='espacos/domain/*,espacos/application/*,reservas/domain/*,reservas/application/*' --fail-under=100"
```

Testes por propriedade (Hypothesis): `espacos/tests/test_propriedades_do_espaco.py` e, em reservas, `test_propriedades_da_reserva.py` (a máquina de estados da reserva: gestor, dona e outra pessoa tentam mudar a situação em sequências geradas, e depois de cada passo o teste confere as invariantes, entre elas que os botões de ação da tela são exatamente as mudanças que o backend aceita), `test_propriedades_do_horario.py` e `test_propriedades_da_agenda.py`. No dia a dia rodam com o perfil `rapido` (50 exemplos por propriedade, sempre os mesmos). Antes da entrega, rode o perfil `exaustivo` (2.000 exemplos aleatórios por propriedade):

```bash
docker compose exec -e HYPOTHESIS_PROFILE=exaustivo backend sh -c "pytest espacos/tests/test_propriedades_do_espaco.py reservas/tests/test_propriedades_*.py --durations=0"
```

Para ver um passo a passo gerado pela máquina de estados da reserva:

```bash
docker compose exec backend pytest reservas/tests/test_propriedades_da_reserva.py -s --hypothesis-verbosity=debug
```

Testes de mutação (mutmut), em `domain` e `application` de `espacos` e de `reservas`. O mutmut altera o código de propósito (troca `<` por `<=`, apaga argumentos, muda textos) e confere se algum teste falha. Leva vários minutos (cerca de meia hora para `reservas` no Docker do Windows), por isso fica fora da verificação de cada PR; rode antes da entrega, um contexto de cada vez. Os mutantes que sobrevivem e são equivalentes estão justificados nos catálogos de testes de espaços e de reservas do grupo, mantidos no repositório (fora do ZIP de entrega):

```bash
docker compose exec backend sh -c "rm -rf mutants && mutmut run 'reservas.*'"
```

```bash
docker compose exec backend sh -c "rm -rf mutants && mutmut run 'espacos.*'"
```

```bash
docker compose exec backend mutmut results
```

Para ver a mudança de um mutante (o nome sai do `mutmut results`):

```bash
docker compose exec backend mutmut show "reservas.domain.regras_de_agenda.x__janelas_entre__mutmut_2"
```

Só a matriz de acesso (quem pode chamar cada rota da API, com login JWT de verdade, em `src/backend/config/tests/test_matriz_de_acesso.py`) e os outros testes de segurança de `config/`. Todo endpoint novo ganha uma linha na matriz, senão o teste de cobertura de rotas falha:

```bash
docker compose exec backend pytest config/tests -v
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
docker compose exec backend sh -c "ruff check . && ruff format --check . && lint-imports && pytest --cov"
```

Ao mudar o `requirements.txt` ou o `requirements-dev.txt`, reconstrua a imagem do backend:

```bash
docker compose up --build -d backend
```

## Roteiro alternativo com `curl`

O mesmo roteiro da [demonstração pela tela](../../README.md#roteiro-da-demonstração), pela API, com os [dados de exemplo](../../README.md#dados-de-exemplo). Ele mostra também o **403** de um solicitante tentando confirmar, que a tela não oferece. Fica inteiro aqui, e não dividido entre os contextos, porque é uma sequência só, com o mesmo `$ACCESS` passando por contas, reservas e espaços.

Troque `AAAA-MM-DD` pela data de amanhã e use os ids que aparecem em `GET /api/espacos/` (num banco recém-criado, a Quadra Poliesportiva Central é o espaço `1`). Os comandos de Windows seguem o padrão dos exemplos de cada contexto (por exemplo, [cadastrar um espaço](espacos/README.md#cadastrar-um-espaço)).

1. Entrar como o solicitante Bruno e guardar o `access` em `ACCESS`, como em [Entrar (login) e usar o token](#entrar-login-e-usar-o-token):

   ```bash
   curl -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" -d '{"email": "bruno.lima@exemplo.com", "senha": "Rede-Alta-73"}'
   ```

2. Consultar as reservas e filtrar por dois critérios ([consultar reservas](reservas/README.md#consultar-reservas)). Como Solicitante, o Bruno só vê as próprias (Solicitada, Recusada e Concluída), e `acoes_disponiveis` só traz "Cancelar" na Solicitada:

   ```bash
   curl "http://localhost:8000/api/reservas/?espaco=1&situacao=SOLICITADA" -H "Authorization: Bearer $ACCESS"
   ```

3. Entrada inválida: pedir o horário de conflito → **409** `CONFLITO_DE_HORARIO` ([solicitar uma reserva](reservas/README.md#solicitar-uma-reserva)):

   ```bash
   curl -X POST http://localhost:8000/api/reservas/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"espaco_id": 1, "data": "AAAA-MM-DD", "hora_inicio": "10:30", "hora_fim": "11:30", "finalidade": "Treino de futsal"}'
   ```

   Outras entradas inválidas prontas: a Quadra de Tênis 2 (inativa) → **409** `ESPACO_INATIVO`; uma data de ontem → **400** `DATA_RETROATIVA`; 22:00–23:00 → **400** `FORA_DO_HORARIO_DE_FUNCIONAMENTO` em `hora_fim`; 10:00–14:00 → **400** `DURACAO_INVALIDA`; uma data daqui a 40 dias → **400** `ANTECEDENCIA_EXCEDIDA` (ver [Regras de agenda](reservas/README.md#regras-de-agenda)).

4. Solicitar um horário livre (amanhã, 16:00–17:00) → **201**, situação `SOLICITADA`; anote o `id` da resposta:

   ```bash
   curl -X POST http://localhost:8000/api/reservas/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"espaco_id": 1, "data": "AAAA-MM-DD", "hora_inicio": "16:00", "hora_fim": "17:00", "finalidade": "Treino de futsal"}'
   ```

5. Ação sem permissão: ainda como Bruno, tentar confirmar a reserva do passo 4 (troque `ID`) → **403** `ACAO_NAO_PERMITIDA`, `"Somente o gestor pode confirmar reservas."`, e a reserva continua Solicitada ([alterar a situação](reservas/README.md#alterar-a-situação-de-uma-reserva)):

   ```bash
   curl -X PATCH http://localhost:8000/api/reservas/ID/situacao/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"situacao": "CONFIRMADA"}'
   ```

6. Entrar como a gestora Carla (`carla.mendes@exemplo.com`, `Apito-Dourado-48`), guardar o novo `access` em `ACCESS` e repetir o mesmo comando → **200** `"Reserva confirmada com sucesso."`. A gestora vê as reservas de todos.

7. Concluir a mesma reserva → **200** `"Reserva concluída com sucesso."`, com `acoes_disponiveis` vazia:

   ```bash
   curl -X PATCH http://localhost:8000/api/reservas/ID/situacao/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"situacao": "CONCLUIDA"}'
   ```

   Tentar voltá-la para `SOLICITADA` responde **409** `TRANSICAO_DE_SITUACAO_INVALIDA`.

8. Ainda como Carla, desativar o Campo de Futebol Principal (espaço `2` num banco recém-criado) → **200**; repetir o comando responde **409** `ESPACO_JA_INATIVO` ([desativar e reativar](espacos/README.md#desativar-e-reativar)):

   ```bash
   curl -X POST http://localhost:8000/api/espacos/2/desativar/ -H "Authorization: Bearer $ACCESS"
   ```

9. Entrar de novo como Bruno e pedir esse espaço → **409** `ESPACO_INATIVO`, "Este espaço está inativo e não aceita reservas.". A reserva Confirmada da Daniela nesse espaço continua valendo:

   ```bash
   curl -X POST http://localhost:8000/api/reservas/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"espaco_id": 2, "data": "AAAA-MM-DD", "hora_inicio": "10:00", "hora_fim": "11:00", "finalidade": "Treino de futebol"}'
   ```

10. Como Carla, reativar o espaço (`POST /api/espacos/2/ativar/`) → **200** `"Espaço reativado."`; o pedido do passo 9 passa a ser aceito (**201**).

## Sobre esta documentação

A documentação do projeto foi dividida (DOC-09) num README da raiz, para rodar e demonstrar, e num README por módulo. As decisões:

- **a) Uma informação, um lugar.** Cada fato fica num README só, e os outros apontam para ele com link relativo: assim uma mudança não deixa cópias desatualizadas. A única repetição permitida é o caminho mínimo para rodar, que fica na raiz mesmo que este README detalhe os comandos, porque o professor precisa iniciar o projeto lendo um arquivo só.
- **b) Onde fica cada coisa.** Raiz: o que o sistema faz, tecnologias, como executar, dados de exemplo, roteiro da demonstração, persistência, limitações e o mapa da documentação. `src/`: serviços do Compose e variáveis. Este README: organização, camadas, formato das respostas, autenticação, comandos e o roteiro com `curl`. Cada contexto: regras, endpoints e exemplos de `curl`. `config` fica aqui, porque é composição, não módulo de negócio.
- **c) Mais a fundo, mas sem copiar requisitos.** Cada README de módulo explica o que o módulo faz, como usar e onde mexer. A documentação de requisitos e de modelagem não é repetida: ela vai em `docs/modelagem.pdf` e na fonte dos requisitos, que não entra no ZIP. Por isso nenhum README do ZIP linka para fora dele.
- **d) Links relativos** que funcionam no GitHub e no ZIP descompactado, com âncoras no padrão do GitHub.
- **e) Nada se perdeu na divisão.** Todo comando, tabela e aviso do README antigo foi movido para um README novo; o que estava desatualizado foi corrigido.
- **Convenção:** ao mudar um endpoint, uma regra ou um comando, atualize o README do módulo no mesmo PR; o README da raiz só muda se mudar o jeito de rodar.
