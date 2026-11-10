# US-08 · Solicitar reserva

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-08 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-08-solicitar-reserva.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Origem do CA-14 e do CA-15 acompanha a nova numeração de UC-04 (E7.1 = espaço, E7.2 = finalidade, na ordem do código); o CA-14 diz qual recusa aparece com o espaço também inválido (DOC-03). Sem aprovação. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Marca "Depende de" das DECs confirmadas na Aula 7 (DEC-06, DEC-10, DEC-11) com "(decidida)" (GES-02). Nenhum Dado/Quando/Então muda. Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-19 e TA-20 passam a TA-20 e TA-21, e TA-21 a TA-158 passam a TA-24 a TA-161, para os TA-19, TA-22 e TA-23 novos da US-03 (revogação e troca da credencial de renovação) seguirem a ordem das histórias (AUT-09). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Critérios novos: CA-03, CA-04, CA-08, CA-14, CA-16 novos, com a implementação pendente na tarefa ESP-07 ([CR-03](../mudancas/CR-03-horario-por-espaco.md)). CAs antigos que a regra nova substitui ficam marcados com Situação, sem apagar o texto nem o TA. Renumeração dos TAs: TA-62 a TA-82 passam a TA-67 a TA-92 (e os CAs seguintes na mesma história, quando há CA novo antes deles), para os 25 TAs pendentes novos seguirem a ordem das histórias (REQ-13). A especificação está adiante do código de propósito. Mudança comportamental da especificação nos CAs novos; a renumeração é editorial, sem nova obrigação. Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-08 |
| **Título** | Solicitar reserva |
| **História** | Como Solicitante, quero pedir um espaço para uma data, um horário e uma finalidade para garantir o uso dele sem procurar ninguém e sem chocar com outro pedido. |
| **Valor** | O pedido fica registrado na hora, ocupa o horário até o Gestor decidir e só é aceito se respeita as regras de uso; nenhum espaço é comprometido duas vezes ([NS-03](../visao.md#necessidades), [NS-04](../visao.md#necessidades), [NS-06](../visao.md#necessidades)). |
| **Origem** | [UC-04 Solicitar reserva, passos 1 a 11](../casos-de-uso/UC-04-solicitar-reserva.md#p1), com as subfunções UC-05 (passos [6](../casos-de-uso/UC-04-solicitar-reserva.md#p6), [8](../casos-de-uso/UC-04-solicitar-reserva.md#p8) e [9](../casos-de-uso/UC-04-solicitar-reserva.md#p9)) e UC-13 ([passo 10](../casos-de-uso/UC-04-solicitar-reserva.md#p10)), as alternativas A1.1, A2.1 e A11.1 e todas as exceções da ficha. A extensão [A3.1](../casos-de-uso/UC-04-solicitar-reserva.md#a3-1) (agenda do dia) é a [US-09](US-09-ver-a-agenda-do-dia.md). |
| **Prioridade** | Normal — [RF-11](../requisitos/rf-reservas.md#rf-11), [RF-11.1](../requisitos/rf-reservas.md#rf-11-1), [RF-11.3](../requisitos/rf-reservas.md#rf-11-3), [RF-11.4](../requisitos/rf-reservas.md#rf-11-4) e [RF-22](../requisitos/rf-reservas.md#rf-22) são normais (F2 e F5 do enunciado). |
| **Estimativa (Custo em Semanas)** | 1,2 (retrospectiva: domínio, conflito, persistência e caso de uso das RES-01 a RES-04, as regras de agenda da RES-09 e a tela da FE-03). |
| **Conversa** | "Quais são o horário de funcionamento, a duração e a antecedência reais?" → [DEC-07](../decisoes/DEC-07.md), decidida na Aula 7: funcionamento das 07:00 às 00:00 por padrão e configurável por espaço, duração sugerida de 1 h, mínimo de 30 min, máximo de 3 h e 30 dias ([CR-03](../mudancas/CR-03-horario-por-espaco.md), tarefa ESP-07). "Um pedido Solicitado que ninguém decidiu continua ocupando o horário depois da data?" → sim, por decisão do grupo ([DEC-13](../decisoes/DEC-13.md), decidida na Aula 7). "Pode pedir num espaço desativado?" → não, e as reservas que ele já tinha continuam valendo ([DEC-06](../decisoes/DEC-06.md)). "A mensagem de conflito pode dizer quem reservou?" → não ([RNF-F06](../requisitos/rnf.md#rnf-f06)). "Em que ordem as regras são conferidas?" → a real, da ficha; a da finalidade diverge do RF-11 ([L-12](../requisitos/srs.md#l-12)). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). Os CAs marcados com implementação pendente só contam quando a tarefa citada os implementar e criar o TA deles. |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Depende de espaços ativos ([US-05](US-05-cadastrar-espaco.md)) e de uma pessoa identificada ([US-02](US-02-entrar-no-sistema.md)). |
| **N** · Negociável | ✗ | Os valores das regras de agenda foram decididos na [DEC-07](../decisoes/DEC-07.md) e o efeito de um pedido não decidido, na [DEC-13](../decisoes/DEC-13.md); o texto dos CAs de regras de agenda e do conflito segue essas decisões e não é renegociado só entre o grupo. |
| **V** · Valiosa | ✓ | É a meta central do sistema (F2): sem ela não há reserva. |
| **E** · Estimável | ✓ | As regras são todas conhecidas e o custo retrospectivo está medido. |
| **S** · Small | ✗ | São 21 critérios e cinco grupos de regra (dados, data, agenda, espaço, conflito). O corte natural seria "pedido básico" (dados, data, espaço e conflito: F2 e F5) × "regras de agenda" (funcionamento, duração e antecedência). Não foi cortada, porque a meta do UC-04 é uma só e as regras de agenda são conferidas no mesmo envio, antes do espaço. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado; o conflito por pedido simultâneo é provado por um teste que simula a corrida ([L-07](../requisitos/srs.md#l-07)). |

**Diagnóstico:** valiosa e testável, mas ainda precisa ser menor e negociável — o mesmo diagnóstico da US-07 do professor.

## Critérios de aceite

#### <a id="us-08-ca-01"></a>US-08 · CA-01 · Pedido aceito (sucesso)

- **Dado** um Solicitante identificado e um espaço ativo sem nenhuma reserva Solicitada ou Confirmada no período
- **Quando** ele pede o espaço para uma data futura, das 10:00 às 11:00, dentro do funcionamento e da antecedência, com uma finalidade
- **Então** o sistema mostra a reserva criada, com o espaço, a data e o horário, a finalidade, a situação Solicitada e o próprio Solicitante (nome e matrícula), informa que o pedido aguarda a decisão do Gestor, e o período passa a impedir outro pedido no mesmo espaço
- **Origem:** [UC-04 passos 1 a 11](../casos-de-uso/UC-04-solicitar-reserva.md#p1)
- **RF:** [RF-11](../requisitos/rf-reservas.md#rf-11)
- **TA:** [TA-67](#ta-67)

#### <a id="us-08-ca-02"></a>US-08 · CA-02 · O que o pedido apresenta antes do envio (sucesso)

- **Dado** um Solicitante que vai pedir uma reserva
- **Quando** ele começa o pedido
- **Então** o sistema apresenta só os espaços que aceitam pedidos, como "Nome (Tipo)", as regras de agenda vigentes ("Funcionamento das 07:00 às 22:00 · duração de 30 min a 3 h · até «data limite».") e quem constará como solicitante, com o nome e a matrícula dele
- **Origem:** [UC-04 passo 2](../casos-de-uso/UC-04-solicitar-reserva.md#p2)
- **RF:** [RF-11](../requisitos/rf-reservas.md#rf-11), [RF-28](../requisitos/rf-agenda.md#rf-28)
- **TA:** [TA-68](#ta-68)
- **Depende de:** [DEC-07](../decisoes/DEC-07.md)
- **Situação:** em parte substituído (a regra do horário de funcionamento apresentado, agora o do espaço, e da duração sugerida) por [CA-08](#us-08-ca-08), pelo [CR-03](../mudancas/CR-03-horario-por-espaco.md) (REQ-13). Este CA e o TA dele descrevem a regra anterior, que o código ainda cumpre até a tarefa ESP-07; não valem como prova da regra nova.

#### <a id="us-08-ca-03"></a>US-08 · CA-03 · Pedido até a meia-noite no horário padrão (sucesso)

- **Dado** um espaço com o horário padrão (07:00 às 00:00)
- **Quando** o Solicitante pede das 23:00 às 00:00 de uma data reservável
- **Então** o pedido é aceito e fica Solicitado, com o término à meia-noite do mesmo dia
- **Origem:** [UC-04 passo 6](../casos-de-uso/UC-04-solicitar-reserva.md#p6)
- **RF:** [RF-11](../requisitos/rf-reservas.md#rf-11), [RF-11.5](../requisitos/rf-reservas.md#rf-11-5)
- **TA:** [TA-69](#ta-69)
- **Depende de:** [DEC-07](../decisoes/DEC-07.md) (decidida na Aula 7; regra aplicada na especificação pelo [CR-03](../mudancas/CR-03-horario-por-espaco.md), REQ-13)
- **Implementação:** implementação pendente (tarefa ESP-07)

#### <a id="us-08-ca-04"></a>US-08 · CA-04 · Pedido depois das 22:00 aceito (sucesso)

- **Dado** um espaço com o horário padrão
- **Quando** o Solicitante pede das 22:00 às 23:00
- **Então** o pedido é aceito e fica Solicitado
- **Origem:** [UC-04 passo 6](../casos-de-uso/UC-04-solicitar-reserva.md#p6)
- **RF:** [RF-11.5](../requisitos/rf-reservas.md#rf-11-5)
- **TA:** [TA-70](#ta-70)
- **Depende de:** [DEC-07](../decisoes/DEC-07.md) (decidida na Aula 7; regra aplicada na especificação pelo [CR-03](../mudancas/CR-03-horario-por-espaco.md), REQ-13)
- **Implementação:** implementação pendente (tarefa ESP-07)

#### <a id="us-08-ca-05"></a>US-08 · CA-05 · Pedir a partir de um espaço já consultado (alternativa)

- **Dado** um Solicitante que escolheu reservar um espaço na lista de espaços
- **Quando** o pedido começa
- **Então** esse espaço já vem escolhido, se ele aceitar pedidos; se ele não existir ou estiver inativo, a escolha é ignorada e o Solicitante escolhe outro
- **Origem:** [UC-04 A1.1](../casos-de-uso/UC-04-solicitar-reserva.md#a1-1)
- **RF:** [RF-11](../requisitos/rf-reservas.md#rf-11)
- **TA:** [TA-71](#ta-71)

#### <a id="us-08-ca-06"></a>US-08 · CA-06 · Regras de agenda não puderam ser obtidas (alternativa)

- **Dado** que as regras de agenda não puderam ser obtidas ao começar o pedido
- **Quando** o Solicitante preenche e envia o pedido
- **Então** o pedido segue sem a dica das regras e continua conferido por inteiro: um pedido dentro das regras é aceito, e um fora delas recebe a recusa da regra correspondente (CA-13 a CA-17)
- **Origem:** [UC-04 A2.1](../casos-de-uso/UC-04-solicitar-reserva.md#a2-1)
- **RF:** [RF-28](../requisitos/rf-agenda.md#rf-28), [RF-11.5](../requisitos/rf-reservas.md#rf-11-5)
- **TA:** [TA-72](#ta-72)

#### <a id="us-08-ca-07"></a>US-08 · CA-07 · Solicitar outra reserva (alternativa)

- **Dado** uma reserva que acabou de ser criada
- **Quando** o Solicitante pede outra reserva
- **Então** o pedido recomeça com o mesmo espaço escolhido e a data, os horários e a finalidade em branco
- **Origem:** [UC-04 A11.1](../casos-de-uso/UC-04-solicitar-reserva.md#a11-1)
- **RF:** [RF-11](../requisitos/rf-reservas.md#rf-11)
- **TA:** [TA-73](#ta-73)

#### <a id="us-08-ca-08"></a>US-08 · CA-08 · Duração sugerida (alternativa)

- **Dado** um pedido com o início às 10:00
- **Quando** o término é sugerido ao Solicitante
- **Então** a sugestão é 11:00 (1 hora), e ele pode trocá-la por outro término entre 30 minutos e 3 horas depois do início
- **Origem:** [UC-04 passo 2](../casos-de-uso/UC-04-solicitar-reserva.md#p2)
- **RF:** [RF-28](../requisitos/rf-agenda.md#rf-28)
- **TA:** [TA-74](#ta-74)
- **Depende de:** [DEC-07](../decisoes/DEC-07.md) (decidida na Aula 7; regra aplicada na especificação pelo [CR-03](../mudancas/CR-03-horario-por-espaco.md), REQ-13)
- **Implementação:** implementação pendente (tarefa ESP-07)

#### <a id="us-08-ca-09"></a>US-08 · CA-09 · Nenhum espaço aceita pedidos (exceção)

- **Dado** que nenhum espaço está ativo
- **Quando** o Solicitante começa um pedido
- **Então** o sistema informa que nenhum espaço está aceitando reservas e indica a consulta de espaços; não há o que escolher e nada é gravado
- **Origem:** [UC-04 E2.1](../casos-de-uso/UC-04-solicitar-reserva.md#e2-1)
- **RF:** [RF-11.3](../requisitos/rf-reservas.md#rf-11-3)
- **TA:** [TA-75](#ta-75)

#### <a id="us-08-ca-10"></a>US-08 · CA-10 · Dados ausentes ou em formato inválido (exceção)

- **Dado** um Solicitante enviando um pedido
- **Quando** falta o espaço, a data, a hora de início, a hora de término ou a finalidade, ou um deles está mal escrito (por exemplo, uma data que não existe)
- **Então** o sistema informa "Verifique os dados informados." e aponta, junto a cada dado com problema, o que está errado, todos de uma vez; nenhuma reserva é criada, nenhum horário fica ocupado e nada entra no histórico
- **Origem:** [UC-04 E5.1](../casos-de-uso/UC-04-solicitar-reserva.md#e5-1)
- **RF:** [RF-11.1](../requisitos/rf-reservas.md#rf-11-1)
- **TA:** [TA-76](#ta-76)

#### <a id="us-08-ca-11"></a>US-08 · CA-11 · Término igual ou anterior ao início (exceção)

- **Dado** um Solicitante enviando um pedido
- **Quando** a hora de término é igual ou anterior à de início (por exemplo, das 11:00 às 10:00)
- **Então** o sistema informa, junto ao término, "O horário de término deve ser posterior ao de início."; nenhuma reserva é criada
- **Origem:** [UC-04 E5.2](../casos-de-uso/UC-04-solicitar-reserva.md#e5-2)
- **RF:** [RF-11.1](../requisitos/rf-reservas.md#rf-11-1)
- **TA:** [TA-77](#ta-77)

#### <a id="us-08-ca-12"></a>US-08 · CA-12 · Data retroativa (exceção)

- **Dado** um Solicitante enviando um pedido
- **Quando** o início pedido é igual ou anterior ao momento do pedido, no horário de Brasília (um minuto depois de agora já é aceito)
- **Então** o sistema informa, junto à data, "Não é possível reservar um horário que já passou."; nenhuma reserva é criada e o espaço nem é consultado
- **Origem:** [UC-04 E5.3](../casos-de-uso/UC-04-solicitar-reserva.md#e5-3)
- **RF:** [RF-11.2](../requisitos/rf-reservas.md#rf-11-2)
- **TA:** [TA-78](#ta-78)

#### <a id="us-08-ca-13"></a>US-08 · CA-13 · Fora do horário de funcionamento (exceção)

- **Dado** um Solicitante enviando um pedido para uma data futura
- **Quando** o pedido começa antes das 07:00 ou termina depois das 22:00 (começar às 07:00 e terminar às 22:00 é aceito)
- **Então** o sistema informa, junto ao início (se começa cedo demais) ou ao término (se termina tarde demais), "Os espaços funcionam das 07:00 às 22:00. Escolha um horário dentro desse período."; nenhuma reserva é criada
- **Origem:** [UC-04 E6.1](../casos-de-uso/UC-04-solicitar-reserva.md#e6-1)
- **RF:** [RF-11.5](../requisitos/rf-reservas.md#rf-11-5)
- **TA:** [TA-79](#ta-79)
- **Depende de:** [DEC-07](../decisoes/DEC-07.md)
- **Situação:** substituído por [CA-14](#us-08-ca-14), [CA-03](#us-08-ca-03), [CA-04](#us-08-ca-04), pelo [CR-03](../mudancas/CR-03-horario-por-espaco.md) (REQ-13). Este CA e o TA dele descrevem a regra anterior, que o código ainda cumpre até a tarefa ESP-07; não valem como prova da regra nova.

#### <a id="us-08-ca-14"></a>US-08 · CA-14 · Fora do horário de um espaço com horário próprio (exceção)

- **Dado** um espaço cujo horário o Gestor definiu das 08:00 às 18:00
- **Quando** o Solicitante pede das 17:30 às 18:30
- **Então** o sistema informa, junto ao término, o horário de funcionamento desse espaço, e nada é gravado
- **Origem:** [UC-04 E6.1](../casos-de-uso/UC-04-solicitar-reserva.md#e6-1)
- **RF:** [RF-11.5](../requisitos/rf-reservas.md#rf-11-5)
- **TA:** [TA-80](#ta-80)
- **Depende de:** [DEC-07](../decisoes/DEC-07.md) (decidida na Aula 7; regra aplicada na especificação pelo [CR-03](../mudancas/CR-03-horario-por-espaco.md), REQ-13)
- **Implementação:** implementação pendente (tarefa ESP-07)

#### <a id="us-08-ca-15"></a>US-08 · CA-15 · Duração fora dos limites (exceção)

- **Dado** um Solicitante enviando um pedido dentro do funcionamento
- **Quando** o pedido dura menos de 30 minutos ou mais de 3 horas (exatamente 30 minutos ou 3 horas é aceito)
- **Então** o sistema informa, junto ao término, "A reserva deve durar entre 30 minutos e 3 horas."; nenhuma reserva é criada
- **Origem:** [UC-04 E6.2](../casos-de-uso/UC-04-solicitar-reserva.md#e6-2)
- **RF:** [RF-11.5](../requisitos/rf-reservas.md#rf-11-5)
- **TA:** [TA-81](#ta-81)
- **Depende de:** [DEC-07](../decisoes/DEC-07.md)

#### <a id="us-08-ca-16"></a>US-08 · CA-16 · Limites de duração sem mudança (exceção)

- **Dado** um espaço com o horário padrão
- **Quando** o Solicitante pede das 10:00 às 10:20
- **Então** o sistema informa "A reserva deve durar entre 30 minutos e 3 horas." e nada é gravado
- **Origem:** [UC-04 E6.2](../casos-de-uso/UC-04-solicitar-reserva.md#e6-2)
- **RF:** [RF-11.5](../requisitos/rf-reservas.md#rf-11-5)
- **TA:** [TA-82](#ta-82)
- **Depende de:** [DEC-07](../decisoes/DEC-07.md) (decidida na Aula 7; regra aplicada na especificação pelo [CR-03](../mudancas/CR-03-horario-por-espaco.md), REQ-13)
- **Implementação:** implementação pendente (tarefa ESP-07)

#### <a id="us-08-ca-17"></a>US-08 · CA-17 · Além da antecedência máxima (exceção)

- **Dado** um Solicitante enviando um pedido dentro do funcionamento e da duração
- **Quando** a data passa da data limite (hoje, em São Paulo, mais 30 dias; a própria data limite é aceita)
- **Então** o sistema informa, junto à data, "Só é possível reservar com até 30 dias de antecedência (até «data limite»).", com a data limite no formato brasileiro; nenhuma reserva é criada
- **Origem:** [UC-04 E6.3](../casos-de-uso/UC-04-solicitar-reserva.md#e6-3)
- **RF:** [RF-11.5](../requisitos/rf-reservas.md#rf-11-5)
- **TA:** [TA-83](#ta-83)
- **Depende de:** [DEC-07](../decisoes/DEC-07.md)

#### <a id="us-08-ca-18"></a>US-08 · CA-18 · Uma regra por vez, na ordem (exceção)

- **Dado** um pedido que viola mais de uma regra: por exemplo, para ontem e fora do funcionamento, ou fora do funcionamento e longo demais
- **Quando** o Solicitante o envia
- **Então** o sistema informa só a primeira regra violada, nesta ordem: data retroativa, horário de funcionamento, duração e antecedência; o Solicitante corrige e, se houver outra, ela aparece no envio seguinte
- **Origem:** [UC-04 passo 6](../casos-de-uso/UC-04-solicitar-reserva.md#p6) ("uma regra por vez")
- **RF:** [RF-11.5](../requisitos/rf-reservas.md#rf-11-5), [RF-11.2](../requisitos/rf-reservas.md#rf-11-2)
- **TA:** [TA-84](#ta-84)

#### <a id="us-08-ca-19"></a>US-08 · CA-19 · Finalidade em branco ou longa demais (exceção)

- **Dado** um pedido dentro das regras de agenda
- **Quando** a finalidade só tem espaços, ou passa do limite de caracteres depois de tirar os espaços das pontas e os repetidos
- **Então** o sistema informa, junto à finalidade, que ela é obrigatória ou o limite de caracteres; nenhuma reserva é criada. Com finalidade vazia e data passada, a data é a recusa que aparece primeiro; com finalidade vazia e espaço zero ou negativo, o espaço ([CA-20](#us-08-ca-20))
- **Origem:** [UC-04 E7.2](../casos-de-uso/UC-04-solicitar-reserva.md#e7-2)
- **RF:** [RF-11.1](../requisitos/rf-reservas.md#rf-11-1) (ordem divergente do RF-11: [L-12](../requisitos/srs.md#l-12))
- **TA:** [TA-85](#ta-85)

#### <a id="us-08-ca-20"></a>US-08 · CA-20 · Espaço não identificado (exceção)

- **Dado** um pedido dentro das regras de agenda
- **Quando** o espaço é informado por um número zero ou negativo
- **Então** o sistema informa, junto ao espaço, "O espaço deve ser informado por um número inteiro positivo."; nenhuma reserva é criada
- **Origem:** [UC-04 E7.1](../casos-de-uso/UC-04-solicitar-reserva.md#e7-1)
- **RF:** [RF-11.1](../requisitos/rf-reservas.md#rf-11-1)
- **TA:** [TA-86](#ta-86)

#### <a id="us-08-ca-21"></a>US-08 · CA-21 · Espaço inexistente (exceção)

- **Dado** um pedido dentro de todas as regras
- **Quando** o espaço informado não existe
- **Então** o sistema informa "Espaço de código «n» não encontrado." e o Solicitante escolhe outro espaço; nenhuma reserva é criada
- **Origem:** [UC-04 E8.1](../casos-de-uso/UC-04-solicitar-reserva.md#e8-1)
- **RF:** [RF-11.3](../requisitos/rf-reservas.md#rf-11-3)
- **TA:** [TA-87](#ta-87)

#### <a id="us-08-ca-22"></a>US-08 · CA-22 · Espaço inativo (exceção)

- **Dado** um espaço que o Gestor desativou e que já tinha reservas
- **Quando** o Solicitante pede esse espaço
- **Então** o sistema informa "Este espaço está inativo e não aceita reservas."; nenhuma reserva é criada, e as reservas que o espaço já tinha continuam valendo
- **Origem:** [UC-04 E8.2](../casos-de-uso/UC-04-solicitar-reserva.md#e8-2)
- **RF:** [RF-11.3](../requisitos/rf-reservas.md#rf-11-3)
- **TA:** [TA-88](#ta-88)
- **Depende de:** [DEC-06](../decisoes/DEC-06.md) (decidida)

#### <a id="us-08-ca-23"></a>US-08 · CA-23 · Conflito com uma reserva que ocupa o horário (exceção)

- **Dado** uma reserva Confirmada de outra pessoa no mesmo espaço, de 10:00 às 11:00
- **Quando** o Solicitante pede o mesmo espaço das 10:30 às 11:30
- **Então** o sistema informa "Este espaço já tem uma reserva Confirmada em «data» 10:00–11:00. Escolha outro horário.", sem dizer quem a pediu nem para quê, mantém os dados do pedido para ele ajustar, e nada muda: nenhuma reserva é criada, a Confirmada continua exatamente como estava e nada entra no histórico. Pedir das 11:00 às 12:00 (encostado), pedir outro espaço no mesmo horário ou pedir sobre uma reserva Recusada, Cancelada ou Concluída é aceito; havendo várias em conflito, a mensagem cita a de início mais cedo
- **Origem:** [UC-04 E9.1](../casos-de-uso/UC-04-solicitar-reserva.md#e9-1)
- **RF:** [RF-11.4](../requisitos/rf-reservas.md#rf-11-4)
- **TA:** [TA-89](#ta-89)
- **Depende de:** [DEC-13](../decisoes/DEC-13.md) (decidida na Aula 7; por decisão do grupo, uma Solicitada não decidida continua ocupando o horário depois da data)

#### <a id="us-08-ca-24"></a>US-08 · CA-24 · Conflito descoberto por um pedido simultâneo (exceção)

- **Dado** dois pedidos para o mesmo espaço, com algum momento em comum, enviados quase ao mesmo tempo
- **Quando** os dois passam pela conferência de conflito antes de algum ser gravado
- **Então** só o primeiro pedido vira reserva; o segundo recebe a mesma mensagem do CA-23, com o horário e a situação do primeiro, e dele nem a reserva nem o registro de criação ficam gravados
- **Origem:** [UC-04 E10.1](../casos-de-uso/UC-04-solicitar-reserva.md#e10-1)
- **RF:** [RF-11.4](../requisitos/rf-reservas.md#rf-11-4)
- **TA:** [TA-90](#ta-90)

#### <a id="us-08-ca-25"></a>US-08 · CA-25 · Criação registrada no histórico (registro)

- **Dado** uma reserva que acabou de ser criada (CA-01)
- **Quando** alguém que pode vê-la consulta o histórico dela
- **Então** o histórico tem exatamente um registro: sem situação anterior, nova Solicitada, com o nome do Solicitante como autor e o momento do pedido. Um pedido recusado (CA-09 a CA-24) não cria reserva e, por isso, não há histórico em que registrá-lo; a tentativa recusada de mudar a situação de uma reserva que já existe fica no histórico dela ([CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md), tarefa RES-12)
- **Origem:** [UC-04 passo 10](../casos-de-uso/UC-04-solicitar-reserva.md#p10)
- **RF:** [RF-22](../requisitos/rf-reservas.md#rf-22)
- **TA:** [TA-91](#ta-91)
- **Depende de:** [DEC-05](../decisoes/DEC-05.md)

#### <a id="us-08-ca-26"></a>US-08 · CA-26 · O solicitante é sempre quem está identificado (acesso)

- **Dado** um Gestor identificado e, à parte, um pedido que informa outra pessoa como solicitante
- **Quando** cada um é enviado
- **Então** a reserva é sempre criada em nome de quem está identificado (o Gestor também pede em nome próprio), o solicitante informado no pedido é ignorado, e as ações disponíveis na reserva criada são as do perfil de quem pediu (o Solicitante pode cancelar; o Gestor, confirmar, recusar ou cancelar). Sem identificação, o pedido não é aceito e a pessoa é orientada a entrar
- **Origem:** [UC-04 passo 10](../casos-de-uso/UC-04-solicitar-reserva.md#p10)
- **RF:** [RF-11](../requisitos/rf-reservas.md#rf-11)
- **TA:** [TA-92](#ta-92)
- **Depende de:** [DEC-04](../decisoes/DEC-04.md) (decidida)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-67"></a>TA-67 | [CA-01](#us-08-ca-01) | automatizado | `reservas/tests/test_api_reservas.py::test_solicitacao_valida_responde_201_com_a_reserva`; `reservas/tests/test_criar_reserva.py::test_solicitacao_valida_e_salva_como_solicitada`; `reservas/tests/test_reserva.py::test_solicitar_cria_reserva_solicitada_com_criada_em_igual_a_agora`; `pages/PaginaNovaReserva.test.tsx`: `com sucesso, mostra o toast e o resumo; "Solicitar outra reserva" volta ao formulário com o espaço mantido` |
| <a id="ta-68"></a>TA-68 | [CA-02](#us-08-ca-02) | automatizado | `pages/PaginaNovaReserva.test.tsx`: `pede só os espaços ativos e mostra "Nome (Tipo)" no seletor`; `pages/PaginaNovaReserva.test.tsx`: `mostra quem está solicitando, com o nome e a matrícula do usuário logado`; `pages/PaginaNovaReserva.test.tsx`: `mostra a dica da agenda com os valores vindos da API, sem limites nos campos`; `components/reservas/dicaDaAgenda.test.ts`: `monta a dica só com os valores recebidos da API`; `reservas/tests/test_api_regras_de_agenda.py::test_regras_de_agenda_sem_login_respondem_200_com_as_constantes_do_dominio` |
| <a id="ta-69"></a>TA-69 | [CA-03](#us-08-ca-03) | pendente | implementação pendente (tarefa ESP-07) — TA a criar junto com o código ([CR-03 · CA-01](../mudancas/CR-03-horario-por-espaco.md#5-critérios-de-aceite)). |
| <a id="ta-70"></a>TA-70 | [CA-04](#us-08-ca-04) | pendente | implementação pendente (tarefa ESP-07) — TA a criar junto com o código ([CR-03 · CA-02](../mudancas/CR-03-horario-por-espaco.md#5-critérios-de-aceite)). |
| <a id="ta-71"></a>TA-71 | [CA-05](#us-08-ca-05) | automatizado | `pages/PaginaNovaReserva.test.tsx`: `pré-seleciona o espaço ativo informado em ?espaco=`; `pages/PaginaNovaReserva.test.tsx`: `ignora ?espaco= de um espaço inexistente ou inativo` |
| <a id="ta-72"></a>TA-72 | [CA-06](#us-08-ca-06) | automatizado | `pages/PaginaNovaReserva.test.tsx`: `sem as regras de agenda, o formulário funciona sem a dica`; `pages/PaginaNovaReserva.test.tsx`: `o erro %s da agenda aparece embaixo do campo do domínio` |
| <a id="ta-73"></a>TA-73 | [CA-07](#us-08-ca-07) | automatizado | `pages/PaginaNovaReserva.test.tsx`: `com sucesso, mostra o toast e o resumo; "Solicitar outra reserva" volta ao formulário com o espaço mantido` |
| <a id="ta-74"></a>TA-74 | [CA-08](#us-08-ca-08) | pendente | implementação pendente (tarefa ESP-07) — TA a criar junto com o código ([CR-03 · CA-05](../mudancas/CR-03-horario-por-espaco.md#5-critérios-de-aceite)). |
| <a id="ta-75"></a>TA-75 | [CA-09](#us-08-ca-09) | automatizado | `pages/PaginaNovaReserva.test.tsx`: `sem espaços ativos, mostra o estado vazio com um link para os espaços` |
| <a id="ta-76"></a>TA-76 | [CA-10](#us-08-ca-10) | automatizado | `reservas/tests/test_api_reservas.py::test_campos_ausentes_respondem_400_com_cada_campo`; `reservas/tests/test_api_reservas.py::test_dado_invalido_responde_400_sem_salvar [data-inexistente]` |
| <a id="ta-77"></a>TA-77 | [CA-11](#us-08-ca-11) | automatizado | `reservas/tests/test_intervalo_de_horario.py::test_fim_igual_ou_antes_do_inicio_e_recusado [x]`; `reservas/tests/test_criar_reserva.py::test_fim_igual_ou_antes_do_inicio_lanca_horario_invalido [x]`; `reservas/tests/test_api_reservas.py::test_dado_invalido_responde_400_sem_salvar [fim-antes-do-inicio]`; `pages/PaginaNovaReserva.test.tsx`: `término antes do início aparece embaixo de Término` |
| <a id="ta-78"></a>TA-78 | [CA-12](#us-08-ca-12) | automatizado | `reservas/tests/test_reserva.py::test_solicitar_com_inicio_igual_a_agora_e_recusado`; `reservas/tests/test_reserva.py::test_solicitar_um_minuto_depois_de_agora_e_aceito`; `reservas/tests/test_reserva.py::test_solicitar_para_ontem_e_recusado`; `reservas/tests/test_criar_reserva.py::test_horario_no_passado_lanca_data_retroativa_antes_de_consultar_o_espaco`; `reservas/tests/test_api_reservas.py::test_dado_invalido_responde_400_sem_salvar [data-retroativa]`; `pages/PaginaNovaReserva.test.tsx`: `data retroativa aparece embaixo de Data, que recebe o foco, e some ao editar` |
| <a id="ta-79"></a>TA-79 | [CA-13](#us-08-ca-13) | automatizado | `reservas/tests/test_regras_de_agenda.py::test_horario_nas_bordas_do_funcionamento_e_aceito [x]`; `reservas/tests/test_regras_de_agenda.py::test_horario_fora_do_funcionamento_e_recusado_no_campo_certo [x]`; `reservas/tests/test_api_reservas.py::test_dado_invalido_responde_400_sem_salvar [antes-da-abertura]`; `pages/PaginaNovaReserva.test.tsx`: `o erro %s da agenda aparece embaixo do campo do domínio` |
| <a id="ta-80"></a>TA-80 | [CA-14](#us-08-ca-14) | pendente | implementação pendente (tarefa ESP-07) — TA a criar junto com o código ([CR-03 · CA-03](../mudancas/CR-03-horario-por-espaco.md#5-critérios-de-aceite)). |
| <a id="ta-81"></a>TA-81 | [CA-15](#us-08-ca-15) | automatizado | `reservas/tests/test_regras_de_agenda.py::test_duracao_nas_bordas_e_aceita [x]`; `reservas/tests/test_regras_de_agenda.py::test_duracao_fora_dos_limites_e_recusada_no_termino [x]`; `reservas/tests/test_api_reservas.py::test_dado_invalido_responde_400_sem_salvar [duracao-acima-da-maxima]` |
| <a id="ta-82"></a>TA-82 | [CA-16](#us-08-ca-16) | pendente | implementação pendente (tarefa ESP-07) — regra já cumprida pelo código; o teste que a fixa com o horário padrão novo nasce na tarefa ([CR-03 · CA-06](../mudancas/CR-03-horario-por-espaco.md#5-critérios-de-aceite)). |
| <a id="ta-83"></a>TA-83 | [CA-17](#us-08-ca-17) | automatizado | `reservas/tests/test_regras_de_agenda.py::test_data_no_limite_da_antecedencia_e_aceita`; `reservas/tests/test_regras_de_agenda.py::test_data_alem_da_antecedencia_e_recusada_com_a_data_limite`; `reservas/tests/test_regras_de_agenda.py::test_data_limite_conta_hoje_no_fuso_de_sao_paulo`; `reservas/tests/test_api_reservas.py::test_dado_invalido_responde_400_sem_salvar [alem-da-antecedencia]` |
| <a id="ta-84"></a>TA-84 | [CA-18](#us-08-ca-18) | automatizado | `reservas/tests/test_reserva.py::test_data_retroativa_e_checada_antes_do_horario_de_funcionamento`; `reservas/tests/test_reserva.py::test_horario_de_funcionamento_e_checado_antes_da_duracao`; `reservas/tests/test_reserva.py::test_duracao_e_checada_antes_da_antecedencia`; `reservas/tests/test_propriedades_da_agenda.py::test_solicitar_aceita_so_o_que_respeita_as_regras_e_recusa_pela_primeira_violada` |
| <a id="ta-85"></a>TA-85 | [CA-19](#us-08-ca-19) | automatizado | `reservas/tests/test_reserva.py::test_finalidade_vazia_e_recusada [x]`; `reservas/tests/test_reserva.py::test_finalidade_no_limite_e_aceita`; `reservas/tests/test_reserva.py::test_finalidade_acima_do_limite_e_recusada`; `reservas/tests/test_api_reservas.py::test_dado_invalido_responde_400_sem_salvar [sem-finalidade]` (a posição da finalidade depois da data não tem teste que a fixe: [L-12](../requisitos/srs.md#l-12)) |
| <a id="ta-86"></a>TA-86 | [CA-20](#us-08-ca-20) | automatizado | `reservas/tests/test_reserva.py::test_espaco_id_vazio_e_recusado_como_obrigatorio`; `reservas/tests/test_reserva.py::test_espaco_id_que_nao_e_inteiro_positivo_e_recusado [x]` |
| <a id="ta-87"></a>TA-87 | [CA-21](#us-08-ca-21) | automatizado | `reservas/tests/test_api_reservas.py::test_espaco_inexistente_responde_404`; `reservas/tests/test_criar_reserva.py::test_espaco_indisponivel_propaga_o_erro_sem_salvar [x]` |
| <a id="ta-88"></a>TA-88 | [CA-22](#us-08-ca-22) | automatizado | `espacos/tests/test_api_desativacao_e_reservas.py::test_espaco_desativado_recusa_nova_reserva_com_409`; `espacos/tests/test_api_desativacao_e_reservas.py::test_reserva_existente_continua_listada_com_as_acoes_depois_de_desativar`; `reservas/tests/test_criar_reserva.py::test_espaco_indisponivel_propaga_o_erro_sem_salvar [x]` |
| <a id="ta-89"></a>TA-89 | [CA-23](#us-08-ca-23) | automatizado | `reservas/tests/test_api_reservas.py::test_horario_ocupado_responde_409_e_preserva_as_reservas`; `reservas/tests/test_conflito_de_horario.py::test_sobreposicao_com_reserva_que_ocupa_horario_e_conflito [x]`; `reservas/tests/test_conflito_de_horario.py::test_sobreposicao_com_reserva_que_nao_ocupa_horario_e_aceita [x]`; `reservas/tests/test_conflito_de_horario.py::test_horario_encostado_e_aceito [x]`; `reservas/tests/test_conflito_de_horario.py::test_mesmo_horario_em_outro_espaco_e_aceito`; `reservas/tests/test_conflito_de_horario.py::test_varias_em_conflito_a_mensagem_cita_a_de_inicio_mais_cedo`; `reservas/tests/test_conflito_de_horario.py::test_mensagem_mostra_horario_e_situacao_sem_dados_do_outro_solicitante`; `reservas/tests/test_criar_reserva.py::test_horario_ocupado_lanca_conflito_sem_salvar [x]`; `exemplos/tests/test_carregar_dados_exemplo.py::test_horario_de_conflito_documentado_responde_409`; `pages/PaginaNovaReserva.test.tsx`: `conflito de horário aparece num aviso no topo, que recebe o foco, e mantém os valores` |
| <a id="ta-90"></a>TA-90 | [CA-24](#us-08-ca-24) | automatizado | `reservas/tests/test_repositorio_reservas.py::test_banco_barra_sobreposicao_que_escapou_da_checagem_em_codigo`; `reservas/tests/test_repositorio_reservas.py::test_conflito_barrado_pelo_banco_nao_grava_registro` (simulam a corrida; sem teste de duas threads na criação: [L-07](../requisitos/srs.md#l-07)) |
| <a id="ta-91"></a>TA-91 | [CA-25](#us-08-ca-25) | automatizado | `reservas/tests/test_reserva.py::test_solicitar_gera_o_registro_de_criacao_pendente`; `reservas/tests/test_repositorio_reservas.py::test_conflito_ao_salvar_nao_grava_registro_e_mantem_os_pendentes`; `reservas/tests/test_api_historico.py::test_fluxo_completo_aparece_no_historico_em_ordem` |
| <a id="ta-92"></a>TA-92 | [CA-26](#us-08-ca-26) | automatizado | `reservas/tests/test_api_permissoes.py::test_gestor_tambem_solicita_reserva`; `reservas/tests/test_api_reservas.py::test_solicitante_enviado_no_corpo_e_ignorado`; `reservas/tests/test_api_permissoes.py::test_resposta_da_solicitacao_traz_as_acoes_de_quem_solicitou`; `reservas/tests/test_api_reservas.py::test_token_jwt_do_login_autoriza_solicitacao`; `pages/PaginaNovaReserva.test.tsx`: `sem login, mostra a mensagem da API no aviso do topo` |
