# Contexto `espacos` — quadras e espaços esportivos

Cadastra, lista, edita, desativa e reativa os espaços que podem ser reservados (Funcionalidade 1). Não conhece reservas: `reservas` consulta um espaço só pela fachada `espacos/publico.py` (`verificar_espaco_disponivel`, que devolve o DTO `EspacoDisponivel`). Organização em camadas e regra de dependência: [README do backend](../README.md#organização).

## Regras

- **Entidade** `EspacoEsportivo` (`domain/espaco_esportivo.py`): `id`, `nome`, `tipo`, `capacidade`, `ativo` (padrão `True`) e `horario` (`HorarioDeFuncionamento`, padrão 07:00 às 00:00). As propriedades são só de leitura; o estado muda só por `alterar_dados`, `desativar` e `ativar`.
- **Tipos** (`TipoEspaco`): `QUADRA_POLIESPORTIVA` (Quadra poliesportiva), `CAMPO_DE_FUTEBOL` (Campo de futebol), `GINASIO` (Ginásio), `QUADRA_DE_AREIA` (Quadra de areia) e `QUADRA_DE_TENIS` (Quadra de tênis).
- **Nome:** obrigatório, gravado sem espaços nas pontas nem repetidos, com até `NOME_MAXIMO_CARACTERES` (100). **Único** sem diferenciar maiúsculas de minúsculas (DEC-10): o caso de uso confere antes de gravar, e uma constraint do banco garante contra pedidos simultâneos.
- **Capacidade:** número inteiro, no mínimo `CAPACIDADE_MINIMA` (1).
- **Edição parcial** (`alterar_dados`): qualquer combinação de nome, tipo, capacidade e horário (`abertura` e `fechamento`), mas pelo menos um (senão `NenhumaAlteracaoInformada`). Cada valor passa pelas mesmas validações do cadastro, e em qualquer erro nada muda. Manter o próprio nome, ou só mudar a caixa dele, não conflita.
- **Espaço nunca é excluído, só desativado** (DEC-06). Desativar bloqueia **novas** reservas (`EspacoInativo` ao solicitar); as já existentes continuam valendo, e o gestor cancela alguma pela tela de reservas, se precisar. Desativar um inativo ou ativar um ativo é erro explícito (409).
- **Alterações simultâneas:** a entidade guarda o estado lido (`estado_de_origem`). Ao gravar, o repositório bloqueia a linha e compara com o que está no banco; se outra pessoa mudou o espaço nesse meio-tempo, responde 409 `ESPACO_DESATUALIZADO` sem gravar nada.
- **Horário do espaço × reserva criada ao mesmo tempo** (ESP-08): editar o horário e criar uma reserva no mesmo espaço se serializam pela trava da linha do espaço (`select_for_update`). Cada um abre uma transação e trava o espaço antes de olhar as reservas: a edição, antes de contar as que ficariam fora da nova janela (`RepositorioEspacos.travar`); a criação, antes de ler o horário (`espacos.publico.verificar_espaco_disponivel_para_reserva`) e até gravar. Quem chega depois espera o commit da outra. Se a criação vem primeiro, a edição conta a reserva nova e responde 409 `HORARIO_INCOMPATIVEL_COM_RESERVAS`; se a edição vem primeiro, a criação lê o horário novo e é recusada por estar fora dele (`FORA_DO_HORARIO_DE_FUNCIONAMENTO`). Sem a trava, nas duas ordens a reserva ficava fora da janela. O custo: criações no mesmo espaço passam uma de cada vez (cerca de 2 ms a mais por criação, medido); espaços diferentes não se bloqueiam. Só a edição que muda o horário trava; desativar e reativar seguem como acima. Provas: `config/tests/test_concorrencia_de_horario_e_reserva.py`.
- A listagem sai ordenada por nome. O banco ordena por código de caractere, então maiúsculas vêm antes de minúsculas e letras acentuadas vão para o fim.

## Endpoints

Conferidos com `config/tests/test_matriz_de_acesso.py`. "Logado" = qualquer perfil.

| Método e caminho | Quem pode | Sucesso | Erros principais |
|---|---|---|---|
| `GET /api/espacos/tipos/` | público | 200 | — |
| `GET /api/espacos/?apenas_ativos=&tipo=` | logado | 200 | 400 `DADOS_INVALIDOS` (filtro inválido) |
| `POST /api/espacos/` | só Gestor | 201 | 400 `CAMPO_OBRIGATORIO_AUSENTE`, `NOME_DE_ESPACO_MUITO_LONGO`, `TIPO_DE_ESPACO_INVALIDO`, `CAPACIDADE_INVALIDA`; 409 `NOME_DE_ESPACO_JA_CADASTRADO`; 403 para o Solicitante |
| `GET /api/espacos/{id}/` | logado | 200 | 404 `ESPACO_NAO_ENCONTRADO` |
| `PATCH /api/espacos/{id}/` | só Gestor | 200 | 400 `NENHUMA_ALTERACAO_INFORMADA` e os do cadastro; 404; 409 `NOME_DE_ESPACO_JA_CADASTRADO`, `ESPACO_DESATUALIZADO`; 403 |
| `POST /api/espacos/{id}/desativar/` | só Gestor | 200 | 404; 409 `ESPACO_JA_INATIVO`, `ESPACO_DESATUALIZADO`; 403 |
| `POST /api/espacos/{id}/ativar/` | só Gestor | 200 | 404; 409 `ESPACO_JA_ATIVO`, `ESPACO_DESATUALIZADO`; 403 |

Sem token, todas as rotas (menos `tipos/`) respondem **401** `NAO_AUTENTICADO`. Não há exclusão: `DELETE` em `/api/espacos/{id}/` responde **405**, assim como `GET` nas rotas de desativar e ativar. A permissão de Gestor é a `ApenasGestor` do [compartilhado](../compartilhado/README.md), aplicada só aos métodos de escrita (`metodos_do_gestor` em `api/views.py`).

## Exemplos de uso

Para estes exemplos, entre como a gestora de exemplo Carla (`carla.mendes@exemplo.com`, `Apito-Dourado-48`), porque só o Gestor cadastra espaços, e guarde o `access` em `ACCESS` como em [Entrar (login) e usar o token](../README.md#entrar-login-e-usar-o-token).

### Tipos de espaço

Tipos aceitos em `tipo`: `QUADRA_POLIESPORTIVA`, `CAMPO_DE_FUTEBOL`, `GINASIO`, `QUADRA_DE_AREIA`, `QUADRA_DE_TENIS`. A mesma lista, com os rótulos, sai de `GET /api/espacos/tipos/` (é dela que o frontend monta os seletores):

```bash
curl http://localhost:8000/api/espacos/tipos/
```

```json
{"mensagem": "Tipos de espaço disponíveis.", "dados": [{"valor": "QUADRA_POLIESPORTIVA", "rotulo": "Quadra poliesportiva"}, {"valor": "CAMPO_DE_FUTEBOL", "rotulo": "Campo de futebol"}, {"valor": "GINASIO", "rotulo": "Ginásio"}, {"valor": "QUADRA_DE_AREIA", "rotulo": "Quadra de areia"}, {"valor": "QUADRA_DE_TENIS", "rotulo": "Quadra de tênis"}]}
```

### Cadastrar um espaço

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
{"mensagem": "Espaço cadastrado com sucesso.", "dados": {"id": 1, "nome": "Quadra Central", "tipo": "QUADRA_POLIESPORTIVA", "tipo_rotulo": "Quadra poliesportiva", "capacidade": 20, "ativo": true, "abertura": "07:00", "fechamento": "00:00"}}
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

### Listar e obter

Listar os espaços (`GET /api/espacos/`, qualquer usuário logado), ordenados por nome. Filtros opcionais: `apenas_ativos=true` e `tipo=<TIPO>`, combináveis:

```bash
curl "http://localhost:8000/api/espacos/?tipo=QUADRA_POLIESPORTIVA&apenas_ativos=true" -H "Authorization: Bearer $ACCESS"
```

```json
{"mensagem": "1 espaço encontrado.", "dados": [{"id": 1, "nome": "Quadra Central", "tipo": "QUADRA_POLIESPORTIVA", "tipo_rotulo": "Quadra poliesportiva", "capacidade": 20, "ativo": true, "abertura": "07:00", "fechamento": "00:00"}]}
```

Obter um espaço (`GET /api/espacos/{id}/`):

```bash
curl http://localhost:8000/api/espacos/1/ -H "Authorization: Bearer $ACCESS"
```

Um id inexistente responde **404**:

```json
{"erro": {"codigo": "ESPACO_NAO_ENCONTRADO", "mensagem": "Espaço de código 9999 não encontrado."}}
```

### Editar um espaço

Editar um espaço (`PATCH /api/espacos/{id}/`, só Gestor). Aceita qualquer combinação de `nome`, `tipo` e `capacidade`, mas pelo menos um; `ativo` no corpo é ignorado, porque ativar e desativar têm rotas próprias:

```bash
curl -X PATCH http://localhost:8000/api/espacos/1/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"capacidade": 25}'
```

```bat
curl -X PATCH http://localhost:8000/api/espacos/1/ -H "Authorization: Bearer %ACCESS%" -H "Content-Type: application/json" -d "{\"capacidade\": 25}"
```

```json
{"mensagem": "Espaço atualizado com sucesso.", "dados": {"id": 1, "nome": "Quadra Central", "tipo": "QUADRA_POLIESPORTIVA", "tipo_rotulo": "Quadra poliesportiva", "capacidade": 25, "ativo": true, "abertura": "07:00", "fechamento": "00:00"}}
```

Corpo vazio (`{}`) → **400** `NENHUMA_ALTERACAO_INFORMADA` ("Informe ao menos um campo para alterar."). Os outros erros são os do cadastro: capacidade `0` → **400** `CAPACIDADE_INVALIDA`; nome de outro espaço → **409** `NOME_DE_ESPACO_JA_CADASTRADO`, sempre com o campo em `campos`. Espaço alterado por outra pessoa depois que você o leu → **409** `ESPACO_DESATUALIZADO` (nada é gravado; atualize a lista e tente de novo).

### Desativar e reativar

Desativar e reativar (`POST /api/espacos/{id}/desativar/` e `POST /api/espacos/{id}/ativar/`, só Gestor, sem corpo). Espaço nunca é excluído: desativar só bloqueia **novas** reservas, e as já existentes continuam valendo (o gestor cancela alguma pela tela de reservas, se precisar):

```bash
curl -X POST http://localhost:8000/api/espacos/1/desativar/ -H "Authorization: Bearer $ACCESS"
```

```bat
curl -X POST http://localhost:8000/api/espacos/1/desativar/ -H "Authorization: Bearer %ACCESS%"
```

```json
{"mensagem": "Espaço desativado. Novas reservas ficam bloqueadas; as existentes continuam valendo.", "dados": {"id": 1, "nome": "Quadra Central", "tipo": "QUADRA_POLIESPORTIVA", "tipo_rotulo": "Quadra poliesportiva", "capacidade": 25, "ativo": false, "abertura": "07:00", "fechamento": "00:00"}}
```

Desativar de novo responde **409** `ESPACO_JA_INATIVO` (ou `ESPACO_DESATUALIZADO`, se outra pessoa o alterou ao mesmo tempo), e pedir uma reserva nesse espaço responde **409** `ESPACO_INATIVO`. Para reativar:

```bash
curl -X POST http://localhost:8000/api/espacos/1/ativar/ -H "Authorization: Bearer $ACCESS"
```

A resposta é **200** `"Espaço reativado."`; ativar um espaço já ativo responde **409** `ESPACO_JA_ATIVO`. Com o token de um Solicitante, editar, desativar e ativar respondem **403** `ACAO_NAO_PERMITIDA`, e nada muda.

## Onde mexer

| Para mudar… | Arquivo |
|---|---|
| Tipos de espaço | `domain/tipo_espaco.py` |
| Regras de nome e capacidade, edição, ativação | `domain/espaco_esportivo.py` (mensagens em `domain/excecoes.py`) |
| Horário de funcionamento (minutos desde a meia-noite, 0 a 1440; o fechamento 1440 é a meia-noite do fim do dia) | `domain/horario_de_funcionamento.py` |
| Casos de uso (`CadastrarEspaco`, `ListarEspacos`, `ObterEspaco`, `EditarEspaco`, `DesativarEspaco`, `AtivarEspaco`, `VerificarEspacoDisponivel`) | `application/casos_de_uso.py` |
| O que `reservas` enxerga de um espaço | `publico.py` |
| Model, constraints e gravação | `infrastructure/models.py`, `infrastructure/repositorio_django.py` |
| Rotas e permissões | `api/views.py`, `api/serializers.py`, `api/urls.py` |

Testes em `espacos/tests/`: domínio sem banco, casos de uso com o fake de `fakes.py`, o contrato do repositório (contra o Django e o fake), a API, a concorrência com duas threads (`test_concorrencia_de_espaco.py`), o efeito da desativação nas reservas só por URL (`test_api_desativacao_e_reservas.py`) e as propriedades com Hypothesis (`test_propriedades_do_espaco.py`).

## Horário de funcionamento

Cada espaço tem o seu horário de funcionamento, que as reservas usam (pela fachada `espacos.publico`) para recusar pedidos fora dele e para montar a agenda do dia. **Um espaço novo abre às 07:00 e fecha às 00:00**, e `00:00` como fechamento é a **meia-noite do fim do dia**, nunca o começo: o objeto de valor `HorarioDeFuncionamento` guarda minutos desde a meia-noite local (de 0 a 1440), e o fechamento 1440 é escrito `00:00` na API e na tela.

- **Entrada e saída:** `abertura` e `fechamento`, como `"HH:MM"`, opcionais no cadastro (sem eles, vale o padrão) e na edição (só o que for enviado muda; o outro lado do horário fica como estava). A listagem, o detalhe, o cadastro e a edição devolvem os dois campos.
- **Validação (no domínio):** o fechamento precisa ser depois da abertura (`HORARIO_DE_FUNCIONAMENTO_INVALIDO`, junto ao fechamento) e a janela precisa ter pelo menos 30 minutos, a duração mínima de uma reserva (`JANELA_DE_FUNCIONAMENTO_CURTA`). Qualquer minuto é aceito.
- **Reduzir o horário com reservas ativas:** é recusado (**409** `HORARIO_INCOMPATIVEL_COM_RESERVAS`, com a quantidade) se alguma reserva Solicitada ou Confirmada, ainda não terminada, ficar fora da nova janela; cancelar ou concluir essas reservas libera a edição. `espacos` não importa `reservas`: o contexto de reservas se registra em `espacos.publico` ao iniciar, e o cadastro recebe só a porta `ReservasDoEspaco`.
- **Espaços que já existiam** ganham o padrão 07:00–00:00 pela migration `0002_horario_de_funcionamento` (o funcionamento antigo ia das 07:00 às 22:00, então nenhuma reserva antiga fica fora do horário novo).

```bash
curl -X POST http://localhost:8000/api/espacos/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"nome": "Quadra de Dia", "tipo": "QUADRA_DE_AREIA", "capacidade": 12, "abertura": "08:00", "fechamento": "22:00"}'
```

## Cache de espaço no Redis

Uma cópia de **leitura** do espaço fica no Redis (cache-aside), só para tirar consultas à tabela de espaços das leituras informativas. Nenhuma resposta da API muda.

- **O que é guardado:** um Hash `espaco:{id}` (nome, tipo, capacidade, ativo, abertura e fechamento em minutos), gravado junto com o `EXPIRE` por um script Lua, então nunca existe Hash sem TTL nem pela metade. Espaço inexistente não é guardado. Hash vazio, incompleto ou com valor que a entidade recusa conta como *miss* (a chave quebrada é apagada e vai para o log).
- **Quem lê o cache:** `GET /api/espacos/{id}/` (`ObterEspaco`) e a ocupação do dia, por `publico.verificar_espaco_disponivel`.
- **Quem nunca lê:** a trava e a validação para reservar (`verificar_espaco_disponivel_para_reserva`, `CriarReserva`), o cadastro, a edição, a ativação, a desativação e a lista de espaços. Quem decide ou grava lê só o PostgreSQL.
- **TTL de 300 s** (`TTL_DO_ESPACO_EM_SEGUNDOS`): é o teto de velhice quando uma invalidação falha.
- **Invalidação:** editar, desativar e reativar apagam o Hash e avançam uma versão **depois do commit** (`transaction.on_commit`); rollback não invalida. O leitor lê a versão antes do PostgreSQL e só grava no cache se ela não avançou, o que impede um valor lido antes do commit de ressuscitar depois da invalidação. O cadastro não invalida (não há cache de ausência).
- **Falhas:** Redis fora do ar, travado ou com a chave de outro tipo → a leitura vai ao PostgreSQL e responde igual, sem 503 e sem erro novo; falha na invalidação só vira aviso no log e a escrita vale.
- **Limite conhecido:** com a invalidação falhando, a leitura informativa pode mostrar o espaço antigo por até o TTL. A decisão nunca é afetada.

Código: `application/leitor_de_espacos_em_cache.py`, a porta `CacheDeEspacos` em `application/portas.py`, `infrastructure/cache_de_espacos_redis.py` e `infrastructure/repositorio_que_invalida.py`.

