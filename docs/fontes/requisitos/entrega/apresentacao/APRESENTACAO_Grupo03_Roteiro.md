# Roteiro da apresentação de Requisitos (Aula 8)

| Identificação | Responsabilidade |
|---|---|
| **APR-01 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

Texto-base para o grupo montar os slides (REQ-15). Não é a apresentação em si e não contém demonstração do software. Fonte do conteúdo: [especificação](../RS_Grupo03_Especificacao.md) e fonte oficial em `docs/fontes/requisitos/`. Conferido por `scripts/verificar_apresentacao.py`.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 12/11/2026 | Max Zimmermann dos Reis | Criação (REQ-15). Sem aprovação. |

## Regras seguidas e avisos

- Apresentação de 10 minutos, com todos os integrantes falando e sem demonstração do software (pedido da REQ-15). O PDF do enunciado não está no repositório; valem as regras do pedido. [PENDENTE: o grupo confere o §9 do enunciado]
- A DEC-23 registra "mostrando o sistema funcionando"; este roteiro segue o pedido da REQ-15 e não demonstra. [CONFIRMAR COM O GRUPO: qual vale na Aula 8]
- Cálculo: 130 palavras por minuto. Meta de fala: de 9 min a 9 min 15 s, deixando de 45 s a 1 min de folga.
- O slide opcional "Roteiro da apresentação" foi cortado, porque o tempo não comporta; a capa já diz os seis assuntos.
- Falantes: [INTEGRANTE 1] a [INTEGRANTE 4] são uma proposta de distribuição para os 4 integrantes. Os documentos da fonte trazem só três nomes (Max Zimmermann dos Reis, Matheus Cezar Santos e Eduardo Almeida da Cunha) [PENDENTE: nome do quarto integrante, que não consta nos documentos] [CONFIRMAR COM O GRUPO: quem fala cada bloco].

## Tabela de abertura

| Slide | Título | Tempo | Falante |
|---|---|---|---|
| 1 | Capa | 0:26 | Max Zimmermann dos Reis |
| 2 | O problema | 0:54 | Max Zimmermann dos Reis |
| 3 | Quem usa e quem decide | 1:00 | Eduardo Almeida da Cunha |
| 4 | Como levantamos | 1:31 | Eduardo Almeida da Cunha |
| 5 | Os requisitos | 1:16 | Kelvin Fraga da Silva |
| 6 | UC-04: o fluxo principal | 1:18 | Kelvin Fraga da Silva |
| 7 | UC-04: uma alternativa e uma exceção | 1:06 | Matheus Cezar Santos |
| 8 | Como documentamos | 1:03 | Matheus Cezar Santos |
| 9 | Encerramento | 0:36 | Max Zimmermann dos Reis |

Os tempos desta tabela são os estimados pelo verificador (palavras ÷ 130). Total proposto por falante: Max Zimmermann dos Reis ≈ 1:55, Eduardo Almeida da Cunha ≈ 2:31, Kelvin Fraga da Silva ≈ 2:33, Matheus Cezar Santos ≈ 2:09; fala total ≈ 9:08. Cada slide cabe em uma mensagem.

---

### Slide 1 — Capa

- **Falante:** Max Zimmermann dos Reis

**Conteúdo do slide**

- Conecta Campus: Especificação de Requisitos
- Grupo 03 · Requisitos de Software 2026/2 · 13/11/2026
- Max Zimmermann dos Reis · Matheus Cezar Santos · Eduardo Almeida da Cunha · [PENDENTE: 4º integrante]

**Fala**

> Bom dia, professor, bom dia, colegas. Somos o Grupo 03 e vamos apresentar a especificação de requisitos do Conecta Campus, um sistema para reservar quadras e espaços esportivos da comunidade acadêmica. Em dez minutos, falaremos do problema, das pessoas envolvidas, do levantamento, dos requisitos, de um caso de uso e das decisões de documentação. Começo pelo problema.

Palavras: 57 · Tempo: 26 s

**Passagem:** "Começo pelo problema."

**Se o professor interromper aqui:** O recorte é a reserva de quadras e espaços esportivos; a especificação completa está no documento entregue (RS-GRUPO03).

---

### Slide 2 — O problema

- **Falante:** Max Zimmermann dos Reis

**Conteúdo do slide**

- Hoje: conversa, mensagem e anotação em papel
- Ninguém vê o que já está ocupado antes de pedir
- Sem registro de quem pediu, quem decidiu e por quê
- 14 de 18 já chegaram a um espaço ocupado ou fechado

**Fala**

> Hoje, quem quer usar uma quadra combina por conversa, por mensagem ou por anotação de papel. Antes de pedir, ninguém sabe quais horários já estão comprometidos. Dois grupos podem combinar o mesmo espaço no mesmo horário e só descobrir o choque na hora do uso. E depois não fica registrado quem pediu, quem aprovou, quando, nem por que um pedido foi negado. No nosso levantamento, 14 de 18 respondentes já chegaram a um espaço ocupado ou fechado em três meses. O Conecta Campus propõe um registro único. Cada pedido fica guardado, o mesmo espaço não é comprometido duas vezes no mesmo período, e cada decisão tem autor, momento e motivo. Agora, quem são as pessoas envolvidas.

Palavras: 116 · Tempo: 54 s

**Passagem:** "Agora, quem são as pessoas envolvidas."

**Se o professor interromper aqui:** Os 14 de 18 vêm do questionário, cujas respostas foram simuladas (seção 4 da especificação); explicamos isso no slide do levantamento.

---

### Slide 3 — Quem usa e quem decide

- **Falante:** Eduardo Almeida da Cunha

**Conteúdo do slide**

| Papel | O que faz |
|---|---|
| Solicitante | Pede e acompanha reservas |
| Atendente responsável | Confirma, recusa, conclui e cancela |
| Gestor do serviço | Mantém o cadastro dos espaços |

Cliente: a instituição (P-01). No sistema mínimo, um perfil cobre os dois últimos papéis (DEC-25).

**Fala**

> Pensamos em três papéis. O Solicitante é o aluno ou servidor que pede espaços em nome próprio e acompanha o pedido, inclusive o motivo de uma recusa. O Atendente responsável é o servidor do setor que decide cada pedido: confirma, recusa, conclui ou cancela. O Gestor do serviço mantém o cadastro dos espaços. A instituição é o cliente: define as regras, mas não opera o sistema. Há ainda o Visitante, que só se cadastra e entra. No sistema mínimo, um único perfil, o Gestor, cobre o Atendente e o Gestor do serviço. É a decisão DEC-25. Outro ponto: não temos cliente real nomeado. O grupo representa a instituição, e o professor é a referência para dúvidas de regra. É a premissa P-01. Meu colega conta como levantamos tudo isso.

Palavras: 129 · Tempo: 60 s

**Passagem:** "Meu colega conta como levantamos tudo isso."

**Se o professor interromper aqui:** Um perfil só porque o sistema mínimo não distingue as duas funções; os requisitos falam em Gestor (o perfil) e os casos de uso falam no papel (DEC-25, seção 3 da especificação).

---

### Slide 4 — Como levantamos

- **Falante:** Eduardo Almeida da Cunha

**Conteúdo do slide**

| Técnica | Participantes |
|---|---|
| Entrevista | 4: cliente, 2 Solicitantes, Atendente |
| Questionário | 18 Solicitantes |

Real: ENT-01 (Aula 7). Simuladas: ENT-02 a ENT-04 e o questionário.

**Fala**

> Usamos duas técnicas: entrevista e questionário. Foram quatro entrevistados em três papéis: um representante do cliente, dois Solicitantes e um Atendente responsável. O questionário teve 18 respostas de Solicitantes. Uma coisa precisa ficar clara: só a entrevista com o representante do cliente foi real, com o professor, na Aula 7. As outras três entrevistas e as 18 respostas foram simuladas, sem pessoas reais, e dizemos isso no documento de evidências. O que descobrimos: 14 de 18 já chegaram a um espaço ocupado ou fechado; 12 de 18 querem, acima de tudo, saber se o pedido foi aceito; e o uso típico dura de 30 minutos a 1 hora. Na Aula 7, o professor mudou quatro regras. Concluir só depois do término da reserva, DEC-13. Registrar no histórico até as tentativas recusadas, DEC-05. Funcionar das sete à meia-noite, por espaço, DEC-07. E matrícula só com dígitos, DEC-09. A necessidade de ser avisado de mudanças ficou fora desta versão, DEC-24. Aulas e eventos da instituição que ocupam o espaço, o não comparecimento e o material esportivo também ficaram fora do escopo. E não há base para concluir sobre usos acima de 3 horas. Com isso em mãos, passamos aos requisitos.

Palavras: 198 · Tempo: 91 s

**Passagem:** "Com isso em mãos, passamos aos requisitos."

**Se o professor interromper aqui:** Amostra por conveniência e dados simulados; os números descrevem os dados simulados, não pessoas reais. Quem decide o escopo e as regras é o grupo, com o professor como referência (P-01).

---

### Slide 5 — Os requisitos

- **Falante:** Kelvin Fraga da Silva

**Conteúdo do slide**

| Tipo | Quantidade |
|---|---|
| Funcionais (RF) | 63 identificadores em 6 temas |
| Não funcionais (RNF), FURPS+ | 33 |
| Regras de negócio (RN) | 17 |

Exemplo de RN: reserva de 30 min a 3 h, até 30 dias à frente.

**Fala**

> Os requisitos funcionais dizem o que o sistema faz. São 63 identificadores, contando as recusas específicas de cada um, em seis temas: espaços, com 17; pedir e consultar reservas, 13; mudar a situação e o histórico, 12; agenda do dia, 6; contas e acesso, 12; e três transversais. Os não funcionais dizem com que qualidade. São 33, organizados em FURPS+: 13 de funcionalidade, 6 de usabilidade, 6 de confiabilidade, 2 de desempenho e 6 de suportabilidade. Um exemplo: nunca existem duas reservas ocupando o mesmo espaço com algum momento em comum. As 17 regras de negócio dizem o que a instituição exige. Por exemplo: uma reserva dura de 30 minutos a 3 horas, e só se reserva com até 30 dias de antecedência. Cada requisito funcional indica o caso de uso e as histórias de usuário a que se liga, e cada regra de negócio indica os requisitos que a cobram. A prioridade é Normal, Esperado ou Fascinante. Agora, um caso de uso completo.

Palavras: 164 · Tempo: 76 s

**Passagem:** "Agora, um caso de uso completo."

**Se o professor interromper aqui:** RF é o que o sistema faz (RF11, pedir reserva); RNF é uma qualidade verificável (RNF20, sem sobreposição); RN é a regra da instituição (RN04, duração de 30 min a 3 h). FURPS+ cobre todas as classes de qualidade com uma lista curta.

---

### Slide 6 — UC-04: o fluxo principal

- **Falante:** Kelvin Fraga da Silva

**Conteúdo do slide**

Figura: diagrama geral dos casos de uso, `../figuras/diagrama-casos-de-uso.png` (destacar UC-04).

- UC-04 Solicitar reserva · Ator: Solicitante
- Meta: garantir o uso de um espaço num intervalo de um dia
- Fluxo: escolhe, informa, envia, sistema confere, grava

**Fala**

> O caso de uso UC-04 é Solicitar reserva. O ator é o Solicitante, e o Gestor também pode pedir, sempre em nome próprio. A meta é garantir o uso de um espaço num intervalo de um dia. Quem pede já está identificado. Primeiro, o Solicitante pede para reservar. O sistema apresenta os espaços que aceitam pedidos, as regras de agenda e quem constará como solicitante. Depois, o Solicitante escolhe o espaço e informa data, hora de início, hora de término e a finalidade, e envia. O sistema, então, confere o pedido em ordem: se está completo e se o início ainda não passou; se respeita o horário de funcionamento, a duração e a antecedência; se o espaço existe e está ativo; e se não há conflito com outra reserva. Estando tudo certo, o sistema grava a reserva como Solicitada, com o registro de criação no histórico, e informa que o pedido aguarda a decisão do Atendente responsável. Meu colega mostra o que acontece quando algo foge desse fluxo.

Palavras: 168 · Tempo: 78 s

**Passagem:** "Meu colega mostra o que acontece quando algo foge desse fluxo."

**Se o professor interromper aqui:** O UC começa pela meta, não por tela; a pré-condição é estar autenticado (UC-02). Por que o UC-04: é o coração do sistema, tem a regra mais importante (sem conflito de horário) e liga RF11, US-08 e RN01.

---

### Slide 7 — UC-04: uma alternativa e uma exceção

- **Falante:** Matheus Cezar Santos

**Conteúdo do slide**

- A3.1 Consultar a agenda do dia antes de enviar (UC-06)
- E9.1 Conflito com reserva que ocupa o horário
- Em toda exceção, nada é gravado (RF11.4)

**Fala**

> Um fluxo alternativo é uma variação que ainda chega à meta. A A3.1 é consultar a agenda do dia antes de enviar. O sistema mostra os horários ocupados, só com início, término e situação, nunca quem reservou nem para quê. E mostra os horários livres, de pelo menos 30 minutos, para a pessoa escolher um. Uma exceção é um caminho em que a meta não é alcançada. A E9.1 é o conflito de horário. Se outra reserva Solicitada ou Confirmada do mesmo espaço tem algum momento em comum com o pedido, o sistema informa a data, o horário e a situação dessa reserva e pede outro horário. Encostar não é conflito: 10 às 11 e 11 às 12 convivem. Em toda exceção, nada é gravado, e a pessoa fica sabendo qual regra impediu e o que corrigir. Passo agora às decisões de documentação.

Palavras: 143 · Tempo: 66 s

**Passagem:** "Passo agora às decisões de documentação."

**Se o professor interromper aqui:** A é alternativa (a meta continua possível); E é exceção (a meta é interrompida). Os IDs ligam ao passo: A3.1 sai do passo 3, E9.1 falha no passo 9 (DEC-14). A regra de RN01 vale também para pedidos simultâneos (E10.1, RNF20).

---

### Slide 8 — Como documentamos

- **Falante:** Matheus Cezar Santos

**Conteúdo do slide**

- IDs: RF01 no documento, RF-01 na fonte (Anexo A)
- Versão 0.1 → 0.2 → 1.0 (DEC-17); cabeçalho em todo documento
- 25 decisões (DEC-01 a DEC-25)
- 5 pedidos de mudança (CR-01 a CR-05), aplicados

**Fala**

> Sobre os identificadores: no documento, os requisitos são RF01, RNF01 e RN01. Na fonte oficial são RF-01 e assim por diante, e uma tabela no anexo A faz a correspondência. A versão segue a DEC-17: 0.1 para o rascunho, 0.2 depois da revisão e 1.0 para a primeira baseline aprovada. Todo documento leva no topo identificador, versão, estado, autor, revisor, aprovador e histórico. Hoje estamos na 0.1; a baseline 1.0 existe como candidata, aguardando aprovação. São 25 decisões registradas. As principais: dois perfis de acesso, na DEC-04; espaço nunca é excluído, só desativado, na DEC-06; e a agenda do dia sem dados pessoais, na DEC-11. E há 5 pedidos de mudança, os CRs. O CR-01 a CR-04 aplicam as quatro mudanças da Aula 7, e o CR-05 ajustou os papéis. Todos já estão aplicados na especificação.

Palavras: 136 · Tempo: 63 s

**Passagem:** "Todos já estão aplicados na especificação." (o encerramento é do [INTEGRANTE 1])

**Se o professor interromper aqui:** CR é um pedido de mudança de requisito, registrado antes de alterar a especificação. A regra de conversão de IDs está no Anexo A; o RNF perde a letra da classe e vira RNF01 a RNF33 em sequência.

---

### Slide 9 — Encerramento

- **Falante:** Max Zimmermann dos Reis

**Conteúdo do slide**

- Pronto: especificação 0.1, 20 histórias, levantamento
- Para o código: regras da Aula 7 (CR-01 a CR-04)
- Limites: dados simulados, cliente sem nome, sem aprovação
- Obrigado

**Fala**

> Para fechar. Está pronta a especificação na versão 0.1, com 20 histórias de usuário e o levantamento documentado. Ficam para o código as regras da Aula 7, que já estão especificadas e entram em tarefas posteriores. Assumimos três limites: boa parte dos dados do levantamento é simulada, o cliente não tem nome e a versão 0.1 ainda não foi aprovada. Obrigado pela atenção. Todos os números que citamos vêm da especificação entregue. Estamos à disposição para perguntas.

Palavras: 77 · Tempo: 36 s

**Passagem:** "Estamos à disposição para perguntas." (abre a rodada de perguntas; ver o material de perguntas)

**Se o professor interromper aqui:** As regras da Aula 7 já estão na especificação e entram no código em tarefas posteriores (seção 11.1 da especificação). [CONFIRMAR COM O GRUPO: estado atual do código, se o professor perguntar]
