# Contexto `reservas` — reservas, situação, agenda e histórico

Recebe as solicitações de reserva, impede conflito de horário e pedidos fora das regras de agenda, controla a situação de cada reserva (quem pode fazer cada mudança) e guarda o histórico. Cobre as Funcionalidades 2 a 5. Não importa `contas` (o usuário logado chega por `request.user`) e só fala com `espacos` pela fachada `espacos.publico`, através da porta `ConsultaDeEspacos`. Organização em camadas e regra de dependência: [README do backend](../README.md#organização).

## Regras

- **Reserva** (`domain/reserva.py`): espaço (`espaco_id`), solicitante (`Solicitante`: id, nome e matrícula copiados do usuário logado no momento), horário (`IntervaloDeHorario`: data, início e fim), finalidade (até `FINALIDADE_MAXIMO_CARACTERES`, 200), situação, motivo da situação (até `MOTIVO_MAXIMO_CARACTERES`, 300) e `criada_em`.
- **Nova solicitação** (`Reserva.solicitar`) nasce `SOLICITADA` e é recusada, nesta ordem: campos ausentes ou término igual ou antes do início (`HorarioInvalido`); horário que já passou (`DataRetroativa`); fora do horário de funcionamento; duração fora dos limites; antecedência maior que a máxima ([regras de agenda](#regras-de-agenda)). Depois, o caso de uso `CriarReserva` confere o espaço (inexistente → 404, inativo → 409) e o conflito de horário.
- **Conflito de horário** (`garantir_horario_livre`, `domain/conflito_de_horario.py`): outra reserva do mesmo espaço, `SOLICITADA` ou `CONFIRMADA` (`SITUACOES_QUE_OCUPAM_HORARIO`), com horário sobreposto. Os intervalos são semiabertos: 10:00–11:00 e 11:00–12:00 não conflitam. A mensagem mostra o horário e a situação da reserva que ocupa, nunca quem reservou. Uma constraint do banco garante o mesmo contra pedidos simultâneos.
- **Situações e transições** (`domain/situacao.py`, tabela única `TRANSICOES_PERMITIDAS`): veja [Alterar a situação](#alterar-a-situação-de-uma-reserva). Recusar e cancelar exigem motivo (`SITUACOES_QUE_EXIGEM_MOTIVO`). Recusar, cancelar ou concluir libera o horário.
- **Quem pode** (`DESTINOS_POR_PAPEL`): o Gestor confirma, recusa, conclui e cancela; o Solicitante só cancela, e só as próprias. A permissão é checada antes da transição, então um Solicitante que tenta confirmar recebe sempre 403. `acoes_disponiveis` (cada reserva da API) sai da mesma regra (`acoes_permitidas_para`), por isso os botões da tela e o que a API aceita nunca divergem.
- **Visibilidade:** o Gestor vê todas; o Solicitante vê só as próprias. Reserva de outra pessoa responde 404, e não 403, para não revelar que existe. A única exceção é a [agenda do dia](#agenda-do-dia), que mostra que um horário está ocupado, sem dizer de quem.
- **Histórico** (`RegistroDeSituacao`): a criação e cada mudança aceita viram um registro, gravado na mesma transação da reserva. Tentativas recusadas não entram (DEC-05).
- **Alterações simultâneas:** se duas pessoas mudarem a mesma reserva ao mesmo tempo, só a primeira grava; a segunda recebe 409 `RESERVA_DESATUALIZADA`.

## Endpoints

Conferidos com `config/tests/test_matriz_de_acesso.py`. "Logado" = qualquer perfil.

| Método e caminho | Quem pode | Sucesso | Erros principais |
|---|---|---|---|
| `GET /api/reservas/situacoes/` | público | 200 | — |
| `GET /api/reservas/regras-de-agenda/` | público | 200 | — |
| `POST /api/reservas/` | logado (em nome próprio) | 201 | 400 `DADOS_INVALIDOS`, `HORARIO_INVALIDO`, `DATA_RETROATIVA`, `FORA_DO_HORARIO_DE_FUNCIONAMENTO`, `DURACAO_INVALIDA`, `ANTECEDENCIA_EXCEDIDA`; 404 `ESPACO_NAO_ENCONTRADO`; 409 `ESPACO_INATIVO`, `CONFLITO_DE_HORARIO` |
| `GET /api/reservas/?espaco=&situacao=&data=&solicitante=&minhas=` | logado (Solicitante: só as próprias) | 200 | 400 `DADOS_INVALIDOS` (filtro em formato inválido) |
| `GET /api/reservas/ocupacao/?espaco=&data=` | logado | 200 | 400 `DADOS_INVALIDOS`; 404 `ESPACO_NAO_ENCONTRADO`; 409 `ESPACO_INATIVO` |
| `GET /api/reservas/{id}/` | Gestor; Solicitante só a própria | 200 | 404 `RESERVA_NAO_ENCONTRADA` |
| `PATCH /api/reservas/{id}/situacao/` | Gestor; Solicitante só cancela a própria | 200 | 400 `MOTIVO_OBRIGATORIO`, `SITUACAO_INVALIDA`, `DADOS_INVALIDOS`; 403 `ACAO_NAO_PERMITIDA`; 404; 409 `TRANSICAO_DE_SITUACAO_INVALIDA`, `RESERVA_DESATUALIZADA` |
| `GET /api/reservas/{id}/historico/` | Gestor; Solicitante só a própria | 200 | 404 `RESERVA_NAO_ENCONTRADA` |

Sem token, todas as rotas (menos `situacoes/` e `regras-de-agenda/`) respondem **401** `NAO_AUTENTICADO`. Não há exclusão: `DELETE` na reserva e no histórico responde **405** `METODO_NAO_PERMITIDO`.

Os exemplos usam o `access` guardado em `ACCESS`, como em [Entrar (login) e usar o token](../README.md#entrar-login-e-usar-o-token).

## Solicitar uma reserva

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

Outros erros: sem token → **401** `NAO_AUTENTICADO`; espaço inexistente → **404** `ESPACO_NAO_ENCONTRADO`; espaço inativo → **409** `ESPACO_INATIVO`; término igual ou antes do início → **400** `HORARIO_INVALIDO`; horário que já passou → **400** `DATA_RETROATIVA`; fora das [regras de agenda](#regras-de-agenda) → **400** `FORA_DO_HORARIO_DE_FUNCIONAMENTO`, `DURACAO_INVALIDA` ou `ANTECEDENCIA_EXCEDIDA`; campo ausente ou data inválida → **400** `DADOS_INVALIDOS` com o campo em `campos`.

## Regras de agenda

Toda nova solicitação precisa respeitar estes limites, iguais para todos os espaços (constantes de `domain/regras_de_agenda.py`, DEC-07):

| Regra | Valor | Erro (400) e campo |
|---|---|---|
| Horário de funcionamento | início a partir das **07:00** e término até as **22:00** | `FORA_DO_HORARIO_DE_FUNCIONAMENTO` em `hora_inicio` (antes da abertura) ou `hora_fim` (depois do fechamento) |
| Duração | de **30 minutos** a **3 horas**, com as bordas incluídas | `DURACAO_INVALIDA` em `hora_fim` |
| Antecedência máxima | até **30 dias** a partir de hoje (fuso de São Paulo) | `ANTECEDENCIA_EXCEDIDA` em `data`, com a data limite na mensagem |

As regras valem só ao solicitar. Reservas já gravadas continuam válidas se os limites mudarem. Por exemplo, pedir 06:00–07:00 responde:

```json
{"erro": {"codigo": "FORA_DO_HORARIO_DE_FUNCIONAMENTO", "mensagem": "Os espaços funcionam das 07:00 às 22:00. Escolha um horário dentro desse período.", "campos": {"hora_inicio": ["Os espaços funcionam das 07:00 às 22:00. Escolha um horário dentro desse período."]}}}
```

Os valores vigentes saem de `GET /api/reservas/regras-de-agenda/`, que não exige login. É deles que a tela de nova reserva monta a dica acima dos campos de data e horário:

```bash
curl http://localhost:8000/api/reservas/regras-de-agenda/
```

```json
{"mensagem": "Regras de agenda.", "dados": {"horario_de_abertura": "07:00", "horario_de_fechamento": "22:00", "duracao_minima_em_minutos": 30, "duracao_maxima_em_minutos": 180, "antecedencia_maxima_em_dias": 30, "data_limite": "2026-11-29"}}
```

`data_limite` é hoje + 30 dias e muda a cada dia.

## Agenda do dia

`GET /api/reservas/ocupacao/?espaco=<id>&data=<AAAA-MM-DD>` (login obrigatório, qualquer perfil) mostra os horários ocupados de um espaço num dia e as janelas livres. É a única forma de um Solicitante ver horários de reservas que não são dele, por isso a resposta traz **só** o intervalo e a situação: nunca nome, matrícula, id, finalidade nem motivo de quem reservou. Os livres são calculados no backend com as [regras de agenda](#regras-de-agenda): janelas menores que a duração mínima não aparecem e, para hoje, elas começam no próximo múltiplo de 5 minutos. É ajuda, não regra: a solicitação continua sendo validada só ao enviar.

```bash
curl "http://localhost:8000/api/reservas/ocupacao/?espaco=1&data=AAAA-MM-DD" -H "Authorization: Bearer $ACCESS"
```

```json
{"mensagem": "1 horário ocupado neste dia.", "dados": {"data": "2026-10-31", "horario_de_abertura": "07:00", "horario_de_fechamento": "22:00", "reservavel": true, "motivo_indisponivel": null, "ocupados": [{"hora_inicio": "10:00", "hora_fim": "11:00", "situacao": "SOLICITADA", "situacao_rotulo": "Solicitada"}], "livres": [{"hora_inicio": "07:00", "hora_fim": "10:00"}, {"hora_inicio": "11:00", "hora_fim": "22:00"}]}}
```

Para uma data em que não é possível reservar (ontem, hoje depois das 22:00 ou além da antecedência máxima), `reservavel` é `false`, `livres` vem vazio e `motivo_indisponivel` traz a mesma mensagem que a solicitação receberia (ex.: "Não é possível reservar um horário que já passou."). Espaço inexistente → **404** `ESPACO_NAO_ENCONTRADO`; inativo → **409** `ESPACO_INATIVO`; sem `espaco` ou `data` → **400** `DADOS_INVALIDOS` com o campo em `campos`.

## Consultar reservas

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

## Alterar a situação de uma reserva

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

Outros erros: recusar ou cancelar sem motivo → **400** `MOTIVO_OBRIGATORIO`; situação fora da lista → **400** `SITUACAO_INVALIDA`; corpo sem `situacao` → **400** `DADOS_INVALIDOS`; reserva inexistente → **404** `RESERVA_NAO_ENCONTRADA`; reserva alterada por outra pessoa enquanto você decidia → **409** `RESERVA_DESATUALIZADA` (nada é gravado; atualize a lista e decida de novo); sem token → **401** `NAO_AUTENTICADO`; outro método além de `PATCH` → **405** `METODO_NAO_PERMITIDO`.

## Histórico de uma reserva

`GET /api/reservas/{id}/historico/` exige login e lista a criação e cada mudança de situação aceita, da mais antiga para a mais recente: data e hora, quem fez, situação anterior (`null` na criação), situação nova e motivo. Tentativas recusadas (403, 409, 400) não entram, porque não mudaram nada. O histórico só recebe registros novos: não há como alterá-lo nem excluí-lo.

Com os dados de exemplo e o token da Carla (gestora), o histórico da reserva Concluída, que é a de id 5 num banco recém-criado (confira em `GET /api/reservas/`):

```bash
curl http://localhost:8000/api/reservas/5/historico/ -H "Authorization: Bearer $ACCESS"
```

No Prompt de Comando do Windows:

```bat
curl http://localhost:8000/api/reservas/5/historico/ -H "Authorization: Bearer %ACCESS%"
```

Resposta **200**:

```json
{"mensagem": "Histórico da reserva.", "dados": [{"situacao_anterior": null, "situacao_anterior_rotulo": null, "situacao_nova": "SOLICITADA", "situacao_nova_rotulo": "Solicitada", "motivo": null, "autor": {"nome": "Bruno Lima"}, "registrado_em": "2026-10-25T17:28:21.892426-03:00"}, {"situacao_anterior": "SOLICITADA", "situacao_anterior_rotulo": "Solicitada", "situacao_nova": "CONFIRMADA", "situacao_nova_rotulo": "Confirmada", "motivo": null, "autor": {"nome": "Carla Mendes"}, "registrado_em": "2026-10-26T17:28:21.892426-03:00"}, {"situacao_anterior": "CONFIRMADA", "situacao_anterior_rotulo": "Confirmada", "situacao_nova": "CONCLUIDA", "situacao_nova_rotulo": "Concluída", "motivo": null, "autor": {"nome": "Carla Mendes"}, "registrado_em": "2026-10-28T17:28:21.892426-03:00"}]}
```

Num cancelamento ou numa recusa, o registro traz o motivo (`"motivo": "Previsão de chuva forte."`). Para um Solicitante, o histórico da reserva de outra pessoa responde **404** `RESERVA_NAO_ENCONTRADA`, como no detalhe; sem token, **401** `NAO_AUTENTICADO`; outro método além de `GET` → **405** `METODO_NAO_PERMITIDO`.

Se o banco foi criado antes desta versão, as reservas antigas aparecem com o histórico vazio. Recrie o banco como em [Recomeçar do zero](../../../README.md#recomeçar-do-zero).

## Onde mexer

| Para mudar… | Arquivo |
|---|---|
| Situações, transições, quem pode cada uma, motivo obrigatório | `domain/situacao.py` |
| Regras da reserva, visibilidade e ações permitidas | `domain/reserva.py` (mensagens em `domain/excecoes.py`) |
| Horário de funcionamento, duração, antecedência, horários livres | `domain/regras_de_agenda.py` |
| Conflito de horário | `domain/conflito_de_horario.py` |
| Casos de uso (`CriarReserva`, `ConsultarReservas`, `ObterReserva`, `AlterarSituacaoReserva`, `ConsultarHistoricoDaReserva`, `ConsultarOcupacaoDoDia`) | `application/casos_de_uso.py` |
| Como um espaço é consultado | `application/portas.py` e `infrastructure/consulta_de_espacos.py` |
| Models, constraints (inclusive a de sobreposição) e gravação do histórico | `infrastructure/models.py`, `infrastructure/repositorio_django.py` |
| Rotas, filtros e formato da saída | `api/views.py`, `api/serializers.py`, `api/urls.py`; o usuário logado é lido só em `api/autenticacao.py` |

Testes em `reservas/tests/`: domínio sem banco, casos de uso com os fakes de `fakes.py`, o contrato do repositório (contra o Django e o fake), a API (`test_api_*.py`), a concorrência com duas threads (`test_concorrencia_de_situacao.py`) e as propriedades com Hypothesis (`test_propriedades_da_reserva.py`, `test_propriedades_do_horario.py`, `test_propriedades_da_agenda.py`). Comandos no [README do backend](../README.md#comandos).
