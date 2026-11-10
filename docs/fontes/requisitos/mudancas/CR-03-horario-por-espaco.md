# CR-03 — Horário de funcionamento por espaço e duração sugerida

| Identificação | Responsabilidade |
|---|---|
| **CR-03 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha (aprovador da fonte oficial) |

Pedido de mudança aberto a partir da resposta do professor à [DEC-07](../decisoes/DEC-07.md) na Aula 7 (06/11/2026), no [modelo de CR](modelo-cr.md). Este CR foi **aplicado na especificação em 10/11/2026 (REQ-13)** (seção 8): os RF, UC, CA e TA já trazem a regra nova, com a marca \"implementação pendente (tarefa ESP-07)\". O **código não mudou**: quem o muda é a tarefa **ESP-07**, que também cria os testes de aceite e marca o CR como implementado.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Abertura a partir da DEC-07 decidida na Aula 7 (GES-02). Aprovado pelo professor, aguardando implementação na ESP-07. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-19 e TA-20 passam a TA-20 e TA-21, e TA-21 a TA-158 passam a TA-24 a TA-161, para os TA-19, TA-22 e TA-23 novos da US-03 (revogação e troca da credencial de renovação) seguirem a ordem das histórias (AUT-09). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Aplicado na especificação (REQ-13): RF, RN, UC, histórias, CAs e TAs com a regra nova, listados na [seção 8](#8-aplicação-na-especificação-req-13). Estado: aplicado na especificação; código pendente (tarefa ESP-07). A especificação está adiante do código de propósito, e cada CA novo leva a marca "implementação pendente (tarefa ESP-07)". Sem aprovação. |

## 1. Solicitação

| Campo | Conteúdo |
|---|---|
| **Motivo** | Resposta do professor à [DEC-07](../decisoes/DEC-07.md) na Aula 7 (06/11/2026): "O horário de funcionamento é das 07:00 às 00:00, as reservas padrões são de 1 hora, e precisa de horário por espaço, porque teremos vários espaços." Decisão do grupo, nos pontos que a resposta não cobriu: 07:00–00:00 é o padrão de cada espaço, configurável por espaço; "reservas padrões de 1 hora" é a duração sugerida ao pedir; mínimo de 30 minutos, máximo de 3 horas e antecedência de 30 dias continuam; o término à meia-noite é o fim do dia da reserva. |
| **Solicitante** | O professor, como representante do cliente. |
| **Responsável** | O grupo. |
| **Estado** | **Aplicado na especificação; código pendente (tarefa ESP-07)** (10/11/2026, REQ-13). |
| **Origem** | [DEC-07](../decisoes/DEC-07.md). |
| **Baseline vigente** | Nenhuma aprovada: a [candidata à 1.0](../baselines/conecta-campus-1.0-candidata.md) continua candidata (aprovação na REQ-07). |
| **Tarefa que implementa** | ESP-07 |

## 2. Classificação (A4·s17)

- [ ] **Editorial:** corrige o texto e mantém a obrigação; registra-se a correção.
- [x] **Comportamental:** muda o fechamento (22:00 → 00:00), passa o horário de funcionamento de global a por espaço (o cadastro de espaços passa a guardá-lo) e acrescenta a duração sugerida de 1 hora.

## 3. Mapa de impacto

Nos dois sentidos (A4·s19). O resumo por elo vem primeiro; depois, a seção da DEC no [mapa de impacto gerado](../rastreabilidade/impacto-por-dec.md#dec-07), copiada sem mudança em 06/11/2026, e o que a regra nova acrescenta.

| Elo | Afetados | Muda o quê |
|---|---|---|
| NS | [NS-06](../visao.md#ns-06); a confirmar na ESP-07: [NS-01](../visao.md#ns-01) e [NS-02](../visao.md#ns-02) | As regras de uso passam a ser por espaço; o cadastro e a consulta de espaços passam a mostrar o horário. |
| RF / RNF | Da DEC: [RF-11.5](../requisitos/rf-reservas.md#rf-11-5), [RF-28](../requisitos/rf-agenda.md#rf-28), [RF-30](../requisitos/rf-agenda.md#rf-30), [RF-31](../requisitos/rf-agenda.md#rf-31). A confirmar na ESP-07: [RF-01](../requisitos/rf-espacos.md#rf-01), [RF-02](../requisitos/rf-espacos.md#rf-02), [RF-05](../requisitos/rf-espacos.md#rf-05), [RF-06](../requisitos/rf-espacos.md#rf-06), [RF-29](../requisitos/rf-agenda.md#rf-29); nenhum RNF | Funcionamento do espaço pedido; regras de agenda com o horário de cada espaço e a duração sugerida; agenda do dia dentro do horário do espaço; cadastro, edição e consulta de espaços com o horário. |
| UC (passo, alternativa ou exceção) | Da DEC: [UC-04 E6.1](../casos-de-uso/UC-04-solicitar-reserva.md#e6-1), [passo 2](../casos-de-uso/UC-04-solicitar-reserva.md#p2), [A2.1](../casos-de-uso/UC-04-solicitar-reserva.md#a2-1), [A3.1](../casos-de-uso/UC-04-solicitar-reserva.md#a3-1); [UC-06 passos 4 e 5](../casos-de-uso/fichas-resumidas.md#uc06-p4), [A4.1](../casos-de-uso/fichas-resumidas.md#uc06-a4-1). A confirmar: [UC-14](../casos-de-uso/UC-14-cadastrar-espaco.md), [UC-15](../casos-de-uso/fichas-resumidas.md#uc-15), [UC-03](../casos-de-uso/fichas-resumidas.md#uc-03) | E6.1 confere o horário do espaço pedido; E6.2 e E6.3 sem mudança; o cadastro e a edição ganham o horário. |
| US / CA | Da DEC: 10 CAs em 2 histórias (lista abaixo). A confirmar: [US-04](../historias/US-04-consultar-os-espacos.md), [US-05](../historias/US-05-cadastrar-espaco.md), [US-06](../historias/US-06-editar-espaco.md) | Os CAs de funcionamento passam a usar o horário do espaço (e o padrão 07:00–00:00); CAs novos de cadastro, edição e consulta do horário. |
| TA | 10 TAs (lista abaixo), nenhum manual; TAs novos para os CAs novos | Revisar os 10 (inclusive os testes de borda) e criar os da seção 5. |
| Endpoint ou tela (complementar) | Da DEC: `POST /api/reservas/`, `/reservas/nova`, `GET /api/reservas/regras-de-agenda/`, `GET /api/reservas/ocupacao/`. A confirmar: `POST /api/espacos/`, `PATCH /api/espacos/{id}/`, `GET /api/espacos/`, `GET /api/espacos/{id}/`, `/espacos` | As regras de agenda deixam de ser só globais; o espaço passa a ter o horário na entrada e na saída. |
| Código (complementar) | Da DEC: `regras_de_agenda.py` (constantes e funções), `Reserva.solicitar`, `RegrasDeAgendaSaidaSerializer.vigentes`, `ConsultarOcupacaoDoDia.executar`. Acrescentado: abaixo | O horário sai das constantes globais e passa a vir do espaço, pela fachada. |
| DEC | [DEC-07](../decisoes/DEC-07.md); [DEC-06](../decisoes/DEC-06.md) e [DEC-11](../decisoes/DEC-11.md) sem mudança | Espaço inativo continua recusando pedidos; a agenda do dia continua sem dados pessoais. |

### Da DEC-07 (copiado de `impacto-por-dec.md`)

- **RF:** [RF-11.5](../rastreabilidade/matriz.md#rf-11-5), [RF-28](../rastreabilidade/matriz.md#rf-28), [RF-30](../rastreabilidade/matriz.md#rf-30), [RF-31](../rastreabilidade/matriz.md#rf-31)
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):**
  - RF-11.5: [UC-05](../casos-de-uso/README.md#uc-05) · exceção — [UC-04 E6.1](../casos-de-uso/UC-04-solicitar-reserva.md#e6-1), [E6.2](../casos-de-uso/UC-04-solicitar-reserva.md#e6-2), [E6.3](../casos-de-uso/UC-04-solicitar-reserva.md#e6-3)
  - RF-28: [UC-04](../casos-de-uso/README.md#uc-04) · fluxo principal (as regras aparecem no pedido) — [UC-04 passo 2](../casos-de-uso/UC-04-solicitar-reserva.md#p2), [A2.1](../casos-de-uso/UC-04-solicitar-reserva.md#a2-1), [UC-06 passo 5](../casos-de-uso/fichas-resumidas.md#uc06-p5)
  - RF-30: [UC-06](../casos-de-uso/README.md#uc-06) · fluxo principal — [UC-06 passos 4 e 5](../casos-de-uso/fichas-resumidas.md#uc06-p4), [UC-04 A3.1](../casos-de-uso/UC-04-solicitar-reserva.md#a3-1)
  - RF-31: [UC-06](../casos-de-uso/README.md#uc-06) · alternativa (data que não é reservável) — [UC-06 A4.1](../casos-de-uso/fichas-resumidas.md#uc06-a4-1), [UC-04 A3.1](../casos-de-uso/UC-04-solicitar-reserva.md#a3-1)
- **US:** [US-08](../historias/US-08-solicitar-reserva.md), [US-09](../historias/US-09-ver-a-agenda-do-dia.md)
- **CA que dependem da DEC:** US-08: [CA-02](../historias/US-08-solicitar-reserva.md#us-08-ca-02), [CA-13](../historias/US-08-solicitar-reserva.md#us-08-ca-13), [CA-15](../historias/US-08-solicitar-reserva.md#us-08-ca-15), [CA-17](../historias/US-08-solicitar-reserva.md#us-08-ca-17); US-09: [CA-05](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-05)
- **CA dos RF afetados (regressão):** US-08: [CA-06](../historias/US-08-solicitar-reserva.md#us-08-ca-06), [CA-18](../historias/US-08-solicitar-reserva.md#us-08-ca-18); US-09: [CA-01](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-01), [CA-02](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-02), [CA-03](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-03)
- **TA:** [TA-68](../historias/US-08-solicitar-reserva.md#ta-68), [TA-72](../historias/US-08-solicitar-reserva.md#ta-72), [TA-79](../historias/US-08-solicitar-reserva.md#ta-79), [TA-81](../historias/US-08-solicitar-reserva.md#ta-81), [TA-83](../historias/US-08-solicitar-reserva.md#ta-83), [TA-84](../historias/US-08-solicitar-reserva.md#ta-84), [TA-93](../historias/US-09-ver-a-agenda-do-dia.md#ta-93), [TA-94](../historias/US-09-ver-a-agenda-do-dia.md#ta-94), [TA-95](../historias/US-09-ver-a-agenda-do-dia.md#ta-95), [TA-97](../historias/US-09-ver-a-agenda-do-dia.md#ta-97)
- **Endpoint ou tela:** `POST /api/reservas/`; `/reservas/nova`; `GET /api/reservas/regras-de-agenda/`; `GET /api/reservas/ocupacao/`
- **Código:** `reservas/domain/regras_de_agenda.py::garantir_regras_de_agenda`, `reservas/domain/reserva.py::Reserva.solicitar`, `reservas/domain/regras_de_agenda.py::data_limite_para_reservar`, `reservas/domain/regras_de_agenda.py::HORARIO_DE_ABERTURA`, `reservas/api/serializers.py::RegrasDeAgendaSaidaSerializer.vigentes`, `reservas/domain/regras_de_agenda.py::horarios_livres`, `reservas/application/casos_de_uso.py::ConsultarOcupacaoDoDia.executar`, `reservas/domain/regras_de_agenda.py::garantir_data_reservavel`, `reservas/domain/regras_de_agenda.py::motivo_de_indisponibilidade`

### Acrescentado pela regra nova

- Cadastro de espaços: `EspacoEsportivo` ganha o horário de funcionamento (padrão 07:00–00:00), validado no domínio; `CadastrarEspaco` e `EditarEspaco`; os serializers de entrada e saída de `espacos/api/`; `CamposDoEspaco`, `FormularioDeEspaco` e `DialogoDeEdicaoDeEspaco` (frontend).
- Persistência: `EspacoEsportivoModel` com as colunas novas e a migration de `espacos` (gerada pelo `makemigrations`), com o padrão para os espaços já cadastrados.
- Fachada `espacos.publico`: `EspacoDisponivel` e `verificar_espaco_disponivel` passam a levar o horário do espaço; do lado de reservas, a porta `ConsultaDeEspacos`/`EspacoReservavel` e o adaptador `ConsultaDeEspacosViaFachada`.
- Regras de agenda: `garantir_regras_de_agenda`, `horarios_livres` e `garantir_data_reservavel` recebem o horário do espaço em vez de `HORARIO_DE_ABERTURA`/`HORARIO_DE_FECHAMENTO`; a ordem das validações de `Reserva.solicitar` muda se o horário só for conhecido depois da consulta do espaço (hoje as regras vêm antes dela).
- Término à meia-noite: hoje `IntervaloDeHorario` exige término depois do início no mesmo dia (00:00 seria anterior a qualquer início); "00:00 = fim do dia da reserva" precisa ser tratado no objeto de valor, na mensagem e na faixa da agenda do dia.
- Duração sugerida de 1 hora: uma constante nomeada no domínio, exposta pelas regras de agenda e usada no pedido (dica do formulário, `horarioSugerido` da agenda do dia); onde ela aparece fica para a ESP-07.
- `GET /api/reservas/regras-de-agenda/` é público e global hoje; com horário por espaço, ele passa a depender do espaço (parâmetro ou rota nova), e a [matriz de acesso](../../matriz_de_acesso.md) muda se houver rota nova.
- Dados de exemplo (`exemplos/dados.py`): espaços com o horário padrão e, se útil para a demonstração, um com horário próprio; o horário de conflito do README continua válido.
- Documentos: glossário (horário de funcionamento, duração sugerida), [Visão](../visao.md) (NS-06, P-04, R-10, fora do escopo "regras diferentes por espaço"), README de espaços e de reservas, a Figura 3 da modelagem (atributos de `EspacoEsportivo`) e `docs/fontes/testes_de_reservas.md`.

## 4. Diferença

Trechos atuais e propostos. O texto proposto é a referência para a ESP-07; a redação final sai no PR dela.

| Artefato | Antes | Depois |
|---|---|---|
| [RF-11.5](../requisitos/rf-reservas.md#rf-11-5), enunciado | O sistema deve impedir que o usuário autenticado solicite uma reserva que comece antes das 07:00 ou termine depois das 22:00, que dure menos de 30 minutos ou mais de 3 horas, ou cuja data passe da data limite (hoje mais 30 dias), sem gravar nada, e informar no campo correspondente a primeira regra violada, nesta ordem: funcionamento, duração, antecedência. | O sistema deve impedir que o usuário autenticado solicite uma reserva que comece antes da abertura ou termine depois do fechamento **do espaço pedido (padrão: 07:00 às 00:00, com o término à meia-noite como fim do dia da reserva)**, que dure menos de 30 minutos ou mais de 3 horas, ou cuja data passe da data limite (hoje mais 30 dias), sem gravar nada, e informar no campo correspondente a primeira regra violada, nesta ordem: funcionamento, duração, antecedência. |
| [RF-28](../requisitos/rf-agenda.md#rf-28), enunciado | O sistema deve permitir ao visitante consultar as regras de agenda e ver o horário de abertura e de fechamento, a duração mínima e máxima de uma reserva, a antecedência máxima em dias e a data limite para reservar a partir de hoje. | O sistema deve permitir ao visitante consultar as regras de agenda e ver o horário de abertura e de fechamento **de cada espaço**, a **duração sugerida (1 hora)**, a duração mínima e máxima de uma reserva, a antecedência máxima em dias e a data limite para reservar a partir de hoje. |
| [RF-30](../requisitos/rf-agenda.md#rf-30), enunciado | O sistema deve permitir ao usuário autenticado ver, na agenda do dia de um espaço, os horários livres dentro do funcionamento, cada um com pelo menos 30 minutos e, para hoje, começando no próximo múltiplo de 5 minutos depois do momento da consulta, e usar um deles para preencher o início e o término do pedido. | … os horários livres dentro do funcionamento **do espaço**, cada um com pelo menos 30 minutos e, para hoje, começando no próximo múltiplo de 5 minutos depois do momento da consulta, e usar um deles para preencher o início e o término do pedido, **com a duração sugerida (onde, a confirmar na ESP-07)**. |
| [RF-05](../requisitos/rf-espacos.md#rf-05) e [RF-06](../requisitos/rf-espacos.md#rf-06), enunciado (a confirmar na ESP-07) | … cadastrar um espaço esportivo com nome, tipo e capacidade … / … alterar o nome, o tipo ou a capacidade de um espaço … | … com nome, tipo, capacidade **e horário de funcionamento (padrão 07:00 às 00:00)** … / … alterar o nome, o tipo, a capacidade **ou o horário de funcionamento** … |
| [UC-04 E6.1](../casos-de-uso/UC-04-solicitar-reserva.md#e6-1) | Condição: no passo 6, o pedido começa antes da abertura (07:00) ou termina depois do fechamento (22:00). As bordas valem: começar às 07:00 e terminar às 22:00 é aceito. Resultado: "Os espaços funcionam das 07:00 às 22:00. Escolha um horário dentro desse período." | Condição: o pedido começa antes da abertura ou termina depois do fechamento **do espaço pedido** (padrão 07:00 e 00:00); as bordas valem. Resultado: a mensagem com o horário **desse espaço**. |
| [UC-04 E6.2](../casos-de-uso/UC-04-solicitar-reserva.md#e6-2) e [E6.3](../casos-de-uso/UC-04-solicitar-reserva.md#e6-3) | 30 minutos a 3 horas; até 30 dias. | Sem mudança (decisão do grupo). |

**A definir na ESP-07, sem mudar a decisão:**

- Os RF, UC, US e CAs de espaços marcados "a confirmar" na seção 3.
- Onde a duração sugerida aparece (dica do pedido, término preenchido pela agenda do dia ou os dois).
- Se a consulta das regras de agenda passa a receber o espaço ou se o horário vai junto com o espaço na consulta de espaços.

## 5. Critérios de aceite

Novos ou alterados, em Dado/Quando/Então ([DEC-15](../decisoes/DEC-15.md)). Entram nas histórias na ESP-07, com o TA de cada um.

#### CR-03 · CA-01 · Pedido até a meia-noite no horário padrão (sucesso)

- **Dado** um espaço com o horário padrão (07:00 às 00:00)
- **Quando** o Solicitante pede das 23:00 às 00:00 de uma data reservável
- **Então** o pedido é aceito e fica Solicitado, com o término à meia-noite do mesmo dia
- **TA:** a criar na ESP-07, junto com o CA na história.

#### CR-03 · CA-02 · Pedido depois das 22:00 aceito (sucesso)

- **Dado** um espaço com o horário padrão
- **Quando** o Solicitante pede das 22:00 às 23:00
- **Então** o pedido é aceito e fica Solicitado
- **TA:** a criar na ESP-07, junto com o CA na história.

#### CR-03 · CA-03 · Fora do horário de um espaço com horário próprio (exceção)

- **Dado** um espaço cujo horário o Gestor definiu das 08:00 às 18:00
- **Quando** o Solicitante pede das 17:30 às 18:30
- **Então** o sistema informa, junto ao término, o horário de funcionamento desse espaço, e nada é gravado
- **TA:** a criar na ESP-07, junto com o CA na história.

#### CR-03 · CA-04 · Espaço cadastrado sem horário (sucesso)

- **Dado** o Gestor cadastrando um espaço sem informar o horário de funcionamento
- **Quando** ele conclui o cadastro
- **Então** o espaço fica com o horário padrão das 07:00 às 00:00
- **TA:** a criar na ESP-07, junto com o CA na história.

#### CR-03 · CA-05 · Duração sugerida (alternativa)

- **Dado** um pedido com o início às 10:00
- **Quando** o término é sugerido ao Solicitante
- **Então** a sugestão é 11:00 (1 hora), e ele pode trocá-la por outro término entre 30 minutos e 3 horas depois do início
- **TA:** a criar na ESP-07, junto com o CA na história.

#### CR-03 · CA-06 · Limites de duração sem mudança (exceção)

- **Dado** um espaço com o horário padrão
- **Quando** o Solicitante pede das 10:00 às 10:20
- **Então** o sistema informa "A reserva deve durar entre 30 minutos e 3 horas." e nada é gravado
- **TA:** a criar na ESP-07, junto com o CA na história.

## 6. Regressão

- Rever os 10 TAs listados no mapa de impacto (seção 3), todos automatizados, com os testes de borda de `reservas/tests/test_regras_de_agenda.py` e as propriedades de `test_propriedades_da_agenda.py`.
- Não devem mudar: a duração mínima e a máxima ([US-08 · CA-15](../historias/US-08-solicitar-reserva.md#us-08-ca-15)), a antecedência ([US-08 · CA-17](../historias/US-08-solicitar-reserva.md#us-08-ca-17)), a ordem funcionamento → duração → antecedência, a recusa de espaço inativo ([DEC-06](../decisoes/DEC-06.md)) e a agenda do dia sem dados pessoais ([DEC-11](../decisoes/DEC-11.md)).
- Os espaços já cadastrados continuam reserváveis com o horário padrão depois da migration.

## 7. Decisão

| Campo | Conteúdo |
|---|---|
| **Decisão** | Aceita. |
| **Quem decidiu e quando** | O professor, como representante do cliente, na Aula 7 (06/11/2026), na resposta à [DEC-07](../decisoes/DEC-07.md); registrado pelo grupo na GES-02. |
| **Justificativa** | Regra de uso dada pelo cliente na resposta à DEC-07: funcionamento das 07:00 às 00:00, reservas padrões de 1 hora e horário por espaço "porque teremos vários espaços". Mínimo, máximo e antecedência ficam como estão, por decisão do grupo. |
| **Referência candidata** | O manifesto da [baseline candidata](../baselines/conecta-campus-1.0-candidata.md) foi gerado de novo com a aplicação na especificação (REQ-13); a ESP-07 só marca o CR como implementado. A [baseline candidata à 1.0](../baselines/conecta-campus-1.0-candidata.md) continua candidata; a aprovação é da REQ-07. |

## 8. Aplicação na especificação (REQ-13)

Aplicado na especificação em 10/11/2026. **O código ainda não mudou**: a especificação está adiante do código de propósito, e cada critério abaixo leva a marca "implementação pendente (tarefa ESP-07)" até a tarefa ESP-07 implementar a regra e criar o teste de aceite dele. Os testes que existem hoje verificam a regra anterior, e nenhum TA novo cita um deles.

**O que mudou:**

- RF: [RF-11.5](../requisitos/rf-reservas.md#rf-11-5), [RF-28](../requisitos/rf-agenda.md#rf-28), [RF-30](../requisitos/rf-agenda.md#rf-30), [RF-05](../requisitos/rf-espacos.md#rf-05) e [RF-06](../requisitos/rf-espacos.md#rf-06) (enunciado e decisão).
- RN: [RN-03](../requisitos/regras-de-negocio.md#rn-03) e [RN-04](../requisitos/regras-de-negocio.md#rn-04) (vigência).
- UC: [UC-04 E6.1](../casos-de-uso/UC-04-solicitar-reserva.md#e6-1) (horário do espaço pedido) e as questões em aberto de [UC-04](../casos-de-uso/UC-04-solicitar-reserva.md); [UC-06 passo 4](../casos-de-uso/fichas-resumidas.md#uc06-p4); nota nas questões em aberto do [UC-14](../casos-de-uso/UC-14-cadastrar-espaco.md). O fluxo `fluxo-solicitar-reserva.puml` não cita horário: nada foi regerado.
- US/CA/TA: [US-05](../historias/US-05-cadastrar-espaco.md) e [US-08](../historias/US-08-solicitar-reserva.md) (CAs novos); [US-09](../historias/US-09-ver-a-agenda-do-dia.md) (CAs de agenda reescritos sem o valor fixo de 22:00, mesma obrigação, mesmos TAs).
- Documentos: [glossário](../glossario.md) (horário de funcionamento, termo novo duração sugerida), [Visão](../visao.md) (NS-06, P-04, R-10), [SRS](../requisitos/srs.md) (auditoria).

**CAs novos (6, todos com a marca "implementação pendente (tarefa ESP-07)")**

| CA | Título | Tipo | TA | Pedido do CR | Implementação |
|---|---|---|---|---|---|
| [US-08 · CA-03](../historias/US-08-solicitar-reserva.md#us-08-ca-03) | Pedido até a meia-noite no horário padrão | sucesso | [TA-69](../historias/US-08-solicitar-reserva.md#ta-69) | CR-03 · CA-01 | implementação pendente (tarefa ESP-07) |
| [US-08 · CA-04](../historias/US-08-solicitar-reserva.md#us-08-ca-04) | Pedido depois das 22:00 aceito | sucesso | [TA-70](../historias/US-08-solicitar-reserva.md#ta-70) | CR-03 · CA-02 | implementação pendente (tarefa ESP-07) |
| [US-08 · CA-08](../historias/US-08-solicitar-reserva.md#us-08-ca-08) | Duração sugerida | alternativa | [TA-74](../historias/US-08-solicitar-reserva.md#ta-74) | CR-03 · CA-05 | implementação pendente (tarefa ESP-07) |
| [US-08 · CA-14](../historias/US-08-solicitar-reserva.md#us-08-ca-14) | Fora do horário de um espaço com horário próprio | exceção | [TA-80](../historias/US-08-solicitar-reserva.md#ta-80) | CR-03 · CA-03 | implementação pendente (tarefa ESP-07) |
| [US-08 · CA-16](../historias/US-08-solicitar-reserva.md#us-08-ca-16) | Limites de duração sem mudança | exceção | [TA-82](../historias/US-08-solicitar-reserva.md#ta-82) | CR-03 · CA-06 | implementação pendente (tarefa ESP-07) |
| [US-05 · CA-03](../historias/US-05-cadastrar-espaco.md#us-05-ca-03) | Espaço cadastrado sem horário | sucesso | [TA-38](../historias/US-05-cadastrar-espaco.md#ta-38) | CR-03 · CA-04 | implementação pendente (tarefa ESP-07) |

**CAs antigos marcados:** [US-08 · CA-02](../historias/US-08-solicitar-reserva.md#us-08-ca-02) (substituído em parte), [US-08 · CA-13](../historias/US-08-solicitar-reserva.md#us-08-ca-13) (substituído). O texto e o TA deles ficam como estavam, com a linha Situação apontando para o CA novo: descrevem a regra anterior, que o código cumpre até a tarefa ESP-07.

**Pontos que ficam abertos para a tarefa ESP-07 (nada foi decidido aqui):**

- Os artefatos marcados "a confirmar" na seção 3: [RF-01](../requisitos/rf-espacos.md#rf-01), [RF-02](../requisitos/rf-espacos.md#rf-02), [RF-29](../requisitos/rf-agenda.md#rf-29), [UC-03](../casos-de-uso/fichas-resumidas.md#uc-03), [UC-14](../casos-de-uso/UC-14-cadastrar-espaco.md) (fluxo), [UC-15](../casos-de-uso/fichas-resumidas.md#uc-15), [US-04](../historias/US-04-consultar-os-espacos.md), [US-06](../historias/US-06-editar-espaco.md), [NS-01](../visao.md#ns-01) e [NS-02](../visao.md#ns-02). Não há CA da edição do horário nem da consulta dele.
- Onde a duração sugerida aparece (dica do pedido, término preenchido pela agenda do dia ou os dois): por isso [US-09 · CA do preenchimento do horário livre](../historias/US-09-ver-a-agenda-do-dia.md) segue como está.
- Se a consulta das regras de agenda passa a receber o espaço ou se o horário vai junto com o espaço na consulta de espaços.
- O texto da mensagem de fora do horário e a validação do horário do espaço (por exemplo, abertura antes do fechamento).
- A Figura 3 da modelagem (atributos de `EspacoEsportivo`) não foi alterada nesta tarefa.
