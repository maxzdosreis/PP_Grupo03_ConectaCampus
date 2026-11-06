# Contexto `espacos` — quadras e espaços esportivos

Cadastra, lista, edita, desativa e reativa os espaços que podem ser reservados (Funcionalidade 1). Não conhece reservas: `reservas` consulta um espaço só pela fachada `espacos/publico.py` (`verificar_espaco_disponivel`, que devolve o DTO `EspacoDisponivel`). Organização em camadas e regra de dependência: [README do backend](../README.md#organização).

## Regras

- **Entidade** `EspacoEsportivo` (`domain/espaco_esportivo.py`): `id`, `nome`, `tipo`, `capacidade` e `ativo` (padrão `True`). As propriedades são só de leitura; o estado muda só por `alterar_dados`, `desativar` e `ativar`.
- **Tipos** (`TipoEspaco`): `QUADRA_POLIESPORTIVA` (Quadra poliesportiva), `CAMPO_DE_FUTEBOL` (Campo de futebol), `GINASIO` (Ginásio), `QUADRA_DE_AREIA` (Quadra de areia) e `QUADRA_DE_TENIS` (Quadra de tênis).
- **Nome:** obrigatório, gravado sem espaços nas pontas nem repetidos, com até `NOME_MAXIMO_CARACTERES` (100). **Único** sem diferenciar maiúsculas de minúsculas (DEC-10): o caso de uso confere antes de gravar, e uma constraint do banco garante contra pedidos simultâneos.
- **Capacidade:** número inteiro, no mínimo `CAPACIDADE_MINIMA` (1).
- **Edição parcial** (`alterar_dados`): qualquer combinação de nome, tipo e capacidade, mas pelo menos um (senão `NenhumaAlteracaoInformada`). Cada valor passa pelas mesmas validações do cadastro, e em qualquer erro nada muda. Manter o próprio nome, ou só mudar a caixa dele, não conflita.
- **Espaço nunca é excluído, só desativado** (DEC-06). Desativar bloqueia **novas** reservas (`EspacoInativo` ao solicitar); as já existentes continuam valendo, e o gestor cancela alguma pela tela de reservas, se precisar. Desativar um inativo ou ativar um ativo é erro explícito (409).
- **Alterações simultâneas:** a entidade guarda o estado lido (`estado_de_origem`). Ao gravar, o repositório bloqueia a linha e compara com o que está no banco; se outra pessoa mudou o espaço nesse meio-tempo, responde 409 `ESPACO_DESATUALIZADO` sem gravar nada.
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

### Listar e obter

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

### Editar um espaço

Editar um espaço (`PATCH /api/espacos/{id}/`, só Gestor). Aceita qualquer combinação de `nome`, `tipo` e `capacidade`, mas pelo menos um; `ativo` no corpo é ignorado, porque ativar e desativar têm rotas próprias:

```bash
curl -X PATCH http://localhost:8000/api/espacos/1/ -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d '{"capacidade": 25}'
```

```bat
curl -X PATCH http://localhost:8000/api/espacos/1/ -H "Authorization: Bearer %ACCESS%" -H "Content-Type: application/json" -d "{\"capacidade\": 25}"
```

```json
{"mensagem": "Espaço atualizado com sucesso.", "dados": {"id": 1, "nome": "Quadra Central", "tipo": "QUADRA_POLIESPORTIVA", "tipo_rotulo": "Quadra poliesportiva", "capacidade": 25, "ativo": true}}
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
{"mensagem": "Espaço desativado. Novas reservas ficam bloqueadas; as existentes continuam valendo.", "dados": {"id": 1, "nome": "Quadra Central", "tipo": "QUADRA_POLIESPORTIVA", "tipo_rotulo": "Quadra poliesportiva", "capacidade": 25, "ativo": false}}
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
| Casos de uso (`CadastrarEspaco`, `ListarEspacos`, `ObterEspaco`, `EditarEspaco`, `DesativarEspaco`, `AtivarEspaco`, `VerificarEspacoDisponivel`) | `application/casos_de_uso.py` |
| O que `reservas` enxerga de um espaço | `publico.py` |
| Model, constraints e gravação | `infrastructure/models.py`, `infrastructure/repositorio_django.py` |
| Rotas e permissões | `api/views.py`, `api/serializers.py`, `api/urls.py` |

Testes em `espacos/tests/`: domínio sem banco, casos de uso com o fake de `fakes.py`, o contrato do repositório (contra o Django e o fake), a API, a concorrência com duas threads (`test_concorrencia_de_espaco.py`), o efeito da desativação nas reservas só por URL (`test_api_desativacao_e_reservas.py`) e as propriedades com Hypothesis (`test_propriedades_do_espaco.py`).
