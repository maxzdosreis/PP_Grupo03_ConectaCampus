# Evidências do Levantamento de Requisitos

Projeto Conecta Campus (reserva de quadras e espaços esportivos) • Grupo 03 • Requisitos de Software, semestre 2026/2 • Professor Luis Antonio Leite Francisco da Costa, Unilasalle RS

Turma: [PENDENTE: preencher a turma]

Integrantes: Max Zimmermann dos Reis; Matheus Cezar Santos; Eduardo Almeida da Cunha [PENDENTE: confirmar os nomes completos de todos os integrantes; os três nomes vêm do cabeçalho dos documentos da fonte]

Data: 13/11/2026

## 1. Visão geral do levantamento

O grupo usou duas técnicas: a entrevista semiestruturada, com um roteiro por perfil, e o questionário anônimo, dirigido a quem pede os espaços. A entrevista cobre o cliente (regras de uso e decisões do projeto), o Solicitante (como o pedido acontece hoje) e o Atendente responsável (como o pedido é decidido e operado); o questionário cobre só o Solicitante, em escala maior. Das quatro entrevistas, uma foi real: a da Aula 7, em que o professor fez o papel de representante do cliente. As outras três e as 18 respostas do questionário são simuladas pelo grupo, para ensaiar o método e a rastreabilidade; nenhuma pessoa real as respondeu. Nenhum dado pessoal foi coletado nem aparece neste documento.

| Técnica | Instrumento | Participantes (n) | Período | Registro |
|---|---|---|---|---|
| Entrevista semiestruturada | ROT-01, ROT-02, ROT-03 | 4 em 3 perfis: 1 representante do cliente (real), 2 Solicitantes e 1 Atendente responsável (simulados) | Aula 7, em 06/11/2026 (ENT-01); simuladas, sem data (ENT-02 a ENT-04) | ENT-01 a ENT-04 |
| Questionário anônimo | QST-01 | 18 respostas de Solicitantes, todas simuladas | Simulação em 09/11/2026, sem período de campo | QST-01, resultados |

## 2. Instrumentos

Quatro instrumentos, com o texto das perguntas sem alteração; ficam de fora só as anotações internas do entrevistador. "[se houver tempo]" marca as perguntas feitas só se sobrar tempo.

### ROT-01 — Roteiro com o representante do cliente

Usado na Aula 7 (06/11/2026), com o professor no papel de representante do cliente. P01 a P16 são as perguntas da pauta da aula; P17 a P20 foram feitas fora da pauta escrita. A pauta não tinha abertura nem encerramento escritos.

- **P01** — Mudança de situação × horário da reserva: concluir, confirmar, recusar e cancelar devem depender do horário da reserva (e o que acontece com um pedido que ninguém decidiu até a data passar)?
- **P02** — Histórico só com mudanças efetivas: uma tentativa recusada de mudar a situação precisa ficar registrada? Onde e para quem?
- **P03** — Valores das regras de agenda: quais são o horário de funcionamento, a duração mínima e máxima e a antecedência máxima? São iguais para todos os espaços e dias?
- **P04** — Reservas de um espaço desativado: quando o Gestor desativa um espaço, o que acontece com as reservas que ele já tem?
- **P05** — Formato da matrícula: qual é o formato real da matrícula, e ela precisa ser conferida com a instituição?
- **P06** — Nome de espaço único: dois espaços podem ter o mesmo nome? "Ginásio A" e "ginásio a" são o mesmo?
- **P07** — Períodos ocupados por outras pessoas na agenda do dia: o Solicitante pode ver, antes de pedir, os períodos ocupados por reservas de outras pessoas? Com quais dados?
- **P08** — Cobertura-alvo dos testes (se houver tempo): que meta de testes o grupo adota, já que a disciplina não exige testes?
- **P09** — Metas de desempenho (se houver tempo): em quanto tempo a consulta de reservas e a agenda do dia precisam responder, e com quantas reservas?
- **P10** — Outros diagramas: Outros diagramas (sequência, C4, DER, raias) serão exigidos?
- **P11** — Numeração de exceções: Exceções numeradas com `E` ou tudo com `A`?
- **P12** — Index Card: Campos do "Index Card padrão"; o custo em semanas aceita fração?
- **P13** — Convenção de versão: A convenção de versão 0.1 → 0.2 → 1.0 vale?
- **P14** — Rastreabilidade até o código: A rastreabilidade deve ir até o código?
- **P15** — Grupo nas duas disciplinas: O grupo atende às regras das duas disciplinas?
- **P16** — Formato dos critérios de aceite: Dado/Quando/Então atende como formato de critério de aceite?
- **P17** — Entrega dos documentos de Requisitos: Como os documentos de Requisitos são entregues?
- **P18** — Capa do `modelagem.pdf`: A capa conta nas 6 páginas do `modelagem.pdf`, e precisa ser uma capa formal?
- **P19** — Modelo do `contribuicoes.pdf`: Há um modelo para o `contribuicoes.pdf`?
- **P20** — Apresentação: Como e onde é a apresentação do sistema?

### ROT-02 — Roteiro com o Solicitante

Abertura (lida em voz alta): Olá! Somos do Grupo 03 da disciplina de Requisitos de Software. Queremos entender como funciona hoje o uso dos espaços esportivos do campus e o que falta para quem os usa. Não estamos vendendo nem apresentando nada: o que importa é a sua experiência. A conversa leva de 10 a 15 minutos. Não anotamos o seu nome, matrícula, contato nem curso, só um perfil geral, como "estudante que usa as quadras toda semana". Você pode pular qualquer pergunta ou parar quando quiser. Posso anotar as suas respostas?

Sem consentimento: agradecer e encerrar, sem anotar.

- **P01.** Conte como foi a última vez que você usou, ou tentou usar, um espaço esportivo do campus, do começo ao fim. *Aprofundamento:* Com quem você falou? Quanto tempo levou até ter certeza de que podia usar?
- **P02.** Como você descobre se um espaço está livre no horário que quer? *Aprofundamento:* Conte a última vez que o horário que você queria já estava tomado: o que fez?
- **P03** [se houver tempo]. Para que você costuma usar os espaços, e com quantas pessoas? *Aprofundamento:* Que tipo de espaço vocês procuram? O que acontece quando o grupo é maior que o esperado?
- **P04.** Conte uma vez em que o uso de um espaço não saiu como estava combinado. O que aconteceu? *Aprofundamento:* O que você fez depois? Que consequência isso teve para você ou para o grupo?
- **P05.** Pensando nas últimas vezes, quanto tempo durou cada uso do espaço? *Aprofundamento:* Do que depende ser mais curto ou mais longo?
- **P06.** Com quanta antecedência você costuma combinar o uso? *Aprofundamento:* Conte a vez em que combinou com mais antecedência. Por que precisou?
- **P07** [se houver tempo]. Em que dias e horários você costuma usar os espaços? *Aprofundamento:* E mais tarde, à noite, como costuma ser? Até que horas vocês ficam?
- **P08.** O que acontece quando você desiste de um uso combinado ou não consegue ir? *Aprofundamento:* Como você avisa, e com quanto tempo antes? E quando outro grupo não aparece no horário dele, o que acontece?
- **P09.** Antes de pedir um horário, o que você precisa saber sobre os horários que outras pessoas já ocuparam? *Aprofundamento:* E o que você prefere que outras pessoas não saibam sobre o seu uso? Por quê?
- **P10** [se houver tempo]. Depois de pedir, o que você precisa saber até o dia do uso? *Aprofundamento:* Da última vez, como ficou sabendo da resposta? Se já recebeu uma resposta negativa, o que lhe disseram?
- **P11.** De tudo o que conversamos, o que mais atrapalha hoje? *Aprofundamento:* Por que isso pesa mais que o resto? Pode me dar um exemplo recente?

Encerramento: Tem algo que eu não perguntei e deveria ter perguntado? … Muito obrigado pelo seu tempo, isso ajuda bastante o nosso trabalho.

### ROT-03 — Roteiro com o Atendente responsável

Abertura (lida em voz alta): Olá! Somos do Grupo 03 da disciplina de Requisitos de Software. Queremos entender como funcionam hoje os pedidos de uso dos espaços esportivos do campus e o que falta para quem os atende. Não estamos vendendo nem apresentando nada: o que importa é a sua experiência. A conversa leva de 10 a 15 minutos. Não anotamos o seu nome, cargo, setor exato nem contato, só um perfil geral, como "servidor que atende os pedidos há mais de um ano". Você pode pular qualquer pergunta ou parar quando quiser. Posso anotar as suas respostas?

Sem consentimento: agradecer e encerrar, sem anotar.

- **P01.** Conte como chegou até você o último pedido de uso de um espaço e o que você fez com ele, do começo ao fim. *Aprofundamento:* Quanto tempo levou para dar a resposta? Onde ficou anotado?
- **P02.** Como você decide se aceita ou nega um pedido? *Aprofundamento:* Conte um pedido que você negou: o que disse à pessoa?
- **P03.** Conte a última vez em que chegaram dois pedidos para o mesmo espaço no mesmo horário. Como resolveu? *Aprofundamento:* Quem ficou com o horário, e por quê? Como a outra pessoa soube?
- **P04** [se houver tempo]. Que problemas aparecem com mais frequência no uso dos espaços? *Aprofundamento:* Qual foi o último? Que consequência teve?
- **P05.** Quando e como você registra que um uso aconteceu? *Aprofundamento:* O que é feito com esse registro depois? Quem o consulta?
- **P06.** O que você faz quando alguém não aparece no horário combinado? *Aprofundamento:* Que consequência isso tem para a pessoa? E para o horário que ficou vazio?
- **P07.** Como funcionam os horários de cada espaço? Conte como é num espaço que você conhece bem. *Aprofundamento:* O que muda de um espaço para outro? E nos fins de semana e feriados?
- **P08.** Quem define as regras de uso dos espaços, como horários, duração e antecedência? *Aprofundamento:* Conte a última vez que uma regra mudou: quem decidiu e como vocês souberam?
- **P09** [se houver tempo]. Quando um espaço precisa sair de uso, por manutenção ou evento, o que acontece com os usos já combinados? *Aprofundamento:* Como as pessoas ficam sabendo?
- **P10** [se houver tempo]. Que informações você precisa ter em mãos para decidir sobre um pedido? *Aprofundamento:* Conte uma vez em que faltou informação para decidir. O que fez?
- **P11.** Do seu trabalho com os pedidos, o que mais consome tempo hoje? *Aprofundamento:* Por que isso pesa mais que o resto?

Encerramento: Tem algo que eu não perguntei e deveria ter perguntado? … Muito obrigado pelo seu tempo, isso ajuda bastante o nosso trabalho.

### QST-01 — Questionário

*Somos do Grupo 03 da disciplina de Requisitos de Software. Queremos entender como você consegue um espaço esportivo hoje. Não é avaliação de ninguém. O formulário é anônimo (não pedimos nome, e-mail, matrícula, curso nem turma) e as respostas servem só ao trabalho da disciplina. Leva cerca de 3 minutos.*

**P01. Qual é o seu vínculo com o campus?** ( ) Estudante de graduação ( ) Estudante de pós-graduação ( ) Servidor técnico-administrativo ( ) Docente ( ) Outro

**P02. Com que frequência você usa quadras ou outros espaços esportivos do campus?** ( ) Toda semana ( ) Algumas vezes por mês ( ) Raramente ( ) Nunca usei

**P03. Como você costuma conseguir um espaço esportivo hoje?** (várias) [ ] Vou até lá e vejo se está livre [ ] Peço pessoalmente a um servidor [ ] Combino por mensagem ou telefone [ ] Peço por e-mail ou formulário [ ] Outro [ ] Nunca precisei

**P04. Nos últimos 3 meses, quantas vezes você chegou a um espaço esportivo do campus e ele estava ocupado ou fechado sem que você soubesse antes?** ( ) Nunca ( ) 1 ou 2 vezes ( ) 3 vezes ou mais ( ) Não se aplica

**P05. Com quanta antecedência você costuma precisar saber se terá o espaço?** ( ) No mesmo dia ( ) Com 1 ou 2 dias ( ) De 3 a 7 dias ( ) Mais de 7 dias, até 30 dias ( ) Mais de 30 dias ( ) Varia muito ( ) Não se aplica

**P06. Quanto dura, em geral, o seu uso de um espaço?** ( ) Até 30 min ( ) Mais de 30 min, até 1 h ( ) Mais de 1 h, até 2 h ( ) Mais de 2 h, até 3 h ( ) Mais de 3 h ( ) Varia muito ( ) Não se aplica

**P07. Em que períodos você mais usa os espaços?** (várias) [ ] Manhã (até 12 h) [ ] Tarde (12 h às 18 h) [ ] Início da noite (18 h às 22 h) [ ] Noite tardia (depois das 22 h) [ ] Não se aplica

**P08. Quando você precisa desistir de um uso combinado ou não pode comparecer, o que costuma acontecer?** ( ) Aviso alguém ( ) Não aviso ( ) Não sei a quem avisar ( ) Nunca aconteceu

**P09. Antes de ir ao espaço, quais destas informações são mais importantes para você? Escolha até 3.** [ ] Saber se o horário está livre [ ] Saber se meu pedido foi aceito [ ] Saber quem decidiu e por quê [ ] Ser avisado se algo mudar [ ] Conhecer as regras do espaço [ ] Outra: ________

**P10. (opcional) Qual é o maior problema que você enfrenta hoje para usar um espaço esportivo do campus?** *Sem citar nomes de pessoas.* ______________________________

**P11. (opcional) Há algo que não perguntamos e que você acha importante?** *Sem citar nomes de pessoas.* ______________________________

*P01 a P09 são obrigatórias. Obrigado por responder!*

## 3. Registros sintéticos das entrevistas

Entrevistador de todas: Max Zimmermann dos Reis. Nas simuladas (ENT-02 a ENT-04), forma: simulada, sem encontro com pessoa real; data, duração e consentimento não se aplicam. A citação da ENT-01 é literal.

**ENT-01 — Representante do cliente (real).** Data: 06/11/2026. Duração: não registrada. Forma: presencial, na Aula 7. Roteiro: ROT-01. Entrevistado: o professor da disciplina, no papel de representante do cliente (premissa P-01: não há cliente real nomeado). Consentimento: não registrado.
Respostas por tema. *Situação e horário:* concluir só depois do término; recusar e cancelar só antes do início, para o Gestor. *Histórico:* "Deve ficar registrado sim, para ter o histórico completo da reserva." *Agenda:* funcionamento das 07:00 às 00:00, reservas padrão de 1 hora e horário por espaço. *Matrícula:* só números, sem quantidade mínima nem máxima. *Confirmou as opções adotadas* para espaço desativado, nome único, agenda do dia, testes, desempenho e convenções de documentação; P15 não foi feita. *Entrega:* documentos de Requisitos em entrega separada; apresentação em aula, em até 10 minutos.
Achados: mudam DEC-13, DEC-05, DEC-07 e DEC-09 (NS-06, NS-09, NS-12); as demais respostas confirmam as opções adotadas (NS-02, NS-05, NS-14); a entrega gerou DEC-20 a DEC-23. P10, P18, P19 e P20 são resumo do grupo, sem as palavras exatas.

**ENT-02 — Solicitante, estudante (simulada).** Roteiro: ROT-02. Perfil: estudante de graduação que usa as quadras toda semana.
Respostas por tema. *Hoje:* combina por mensagem com um colega e procura um funcionário para confirmar; leva de um a dois dias até ter certeza. *Problema:* encontrou outro grupo no mesmo horário. *Regras:* usa cerca de uma hora (às vezes uma e meia), combina com poucos dias de antecedência (semanas em torneios), usa até cerca de 23h. *Desistência:* avisa o colega; já houve grupo que não apareceu. *Informação:* quer saber quais horários estão tomados, sem saber quem ocupou. Assunto novo: aulas ou eventos ocupam o espaço sem aviso.
Achados: confirma NS-03, NS-04, NS-05, NS-07, NS-14, DEC-11 e DEC-07; possível necessidade nova (não comparecimento).

**ENT-03 — Solicitante, servidor (simulada).** Roteiro: ROT-02. Perfil: servidor que usa o ginásio de vez em quando, para atividades com a equipe.
Respostas por tema. *Hoje:* liga para o setor; a resposta vem no mesmo dia ou só depois de uma semana; não sabe sozinho se há horário livre. *Problema:* um uso foi cancelado na véspera, porque o espaço foi cedido a outra atividade. *Regras:* usa duas a três horas, pede com cerca de duas semanas de antecedência. *Informação:* não se incomoda que vejam o horário ocupado, mas não quer que saibam o motivo; precisa saber se o pedido foi aceito e, se não, por quê. Assunto novo: perguntou se três horas seriam permitidas para atividade maior.
Achados: confirma NS-05, NS-07, NS-10 e DEC-11; contesta a duração padrão de 1 h e, em casos grandes, o máximo de 3 h e os 30 dias da DEC-07; possível necessidade nova (aviso de cancelamento).

**ENT-04 — Atendente responsável (simulada).** Roteiro: ROT-03. Perfil: servidor do setor que atende os pedidos de uso dos espaços há mais de um ano.
Respostas por tema. *Hoje:* pedidos chegam por telefone, mensagem e pessoalmente; anota numa agenda de papel e responde em um a três dias. *Decisão:* aceita se o horário está livre e o uso é compatível; nega com motivo; em pedidos simultâneos, vale quem pediu primeiro. *Registro:* marca o uso na agenda depois; quem não aparece, em geral, não gera ação. *Regras:* cada espaço tem horário próprio, fins de semana reduzidos e feriados fechados; a coordenação do setor define as regras. *Maior consumo de tempo:* responder quais horários estão livres. Assunto novo: atividades da instituição têm prioridade e podem derrubar um uso aceito.
Achados: confirma NS-04, NS-05, NS-09, DEC-13 e o horário por espaço da DEC-07; contesta em parte a premissa P-04 (fins de semana e feriados seguem fora do escopo); toca a DEC-06.

## 4. Resultados agregados do questionário (QST-01)

N = 18 respostas, todas válidas e todas simuladas (sem período de campo, 09/11/2026). Perfil, P01: Estudante de graduação 13 de 18, Estudante de pós-graduação 3 de 18, Servidor técnico-administrativo 1 de 18, Docente 1 de 18, Outro 0 de 18; P02: Toda semana 9 de 18, Algumas vezes por mês 5 de 18, Raramente 2 de 18, Nunca usei 2 de 18. P03, P07 e P09 admitem várias opções (a soma passa de 18); em todas as linhas o denominador é N = 18 pessoas.

| Pergunta | Opção: n de N |
|---|---|
| P03 Como consegue hoje | Vou até lá e vejo se está livre: 12 de 18; Combino por mensagem ou telefone: 9 de 18; Peço pessoalmente a um servidor: 7 de 18; Outro: 4 de 18; Peço por e-mail ou formulário: 2 de 18; Nunca precisei: 2 de 18 |
| P04 Ocupado ou fechado sem saber (3 meses) | Nunca: 2 de 18; 1 ou 2 vezes: 10 de 18; 3 vezes ou mais: 4 de 18; Não se aplica: 2 de 18 |
| P05 Antecedência | No mesmo dia: 5 de 18; Com 1 ou 2 dias: 1 de 18; De 3 a 7 dias: 5 de 18; Mais de 7 dias, até 30 dias: 1 de 18; Mais de 30 dias: 0 de 18; Varia muito: 4 de 18; Não se aplica: 2 de 18 |
| P06 Duração | Até 30 minutos: 3 de 18; Mais de 30 minutos, até 1 hora: 10 de 18; Mais de 1 hora, até 2 horas: 2 de 18; Mais de 2 horas, até 3 horas: 0 de 18; Mais de 3 horas: 0 de 18; Varia muito: 1 de 18; Não se aplica: 2 de 18 |
| P07 Períodos | Manhã (até 12 h): 11 de 18; Tarde (12 h às 18 h): 10 de 18; Início da noite (18 h às 22 h): 11 de 18; Noite tardia (depois das 22 h): 7 de 18; Não se aplica: 2 de 18 |
| P08 Desistência | Aviso alguém: 5 de 18; Não aviso: 2 de 18; Não sei a quem avisar: 7 de 18; Nunca aconteceu: 4 de 18 |
| P09 Mais importante (até 3) | Saber se o horário está livre: 8 de 18; Saber se meu pedido foi aceito: 12 de 18; Saber quem decidiu e por quê: 5 de 18; Ser avisado se algo mudar: 8 de 18; Conhecer as regras do espaço: 5 de 18; Outra (descreva): 0 de 18 |

Conferência: a soma das contagens é 18 em P01, P02, P04, P05, P06 e P08, e é 36 em P03, 41 em P07 e 38 em P09 (várias opções, no máximo 3 por pessoa em P09).

Respostas abertas, por tema, sem citação literal e sem dado pessoal. *P10, maior problema (9 de 18 responderam):* combinados informais e conflito de horário, 4 de 18; demora e falta de resposta, 2 de 18; não saber se o espaço está livre ou aberto, 2 de 18; regras pouco claras, 1 de 18. *P11, algo que não perguntamos (7 de 18 responderam):* avisar que não vai usar o horário, 4 de 18; material esportivo, 2 de 18; capacidade do espaço, 1 de 18.


## 5. Síntese dos achados e decisões resultantes

| Achado | Fonte | Destino |
|---|---|---|
| Choque de horário e espaço ocupado ou fechado são frequentes: 14 de 18 passaram por isso em 3 meses. | QST P04; ENT-02, ENT-04 | Confirma NS-04 e NS-05 |
| Quem pede quer ver o que está livre sem saber quem ocupou (8 de 18); o Atendente responde isso o tempo todo. | QST P09; ENT-02, ENT-03, ENT-04 | Confirma NS-05, NS-14 e DEC-11 |
| Saber se o pedido foi aceito é o que mais importa (12 de 18), com o motivo da recusa. | QST P09; ENT-03, ENT-04 | Confirma NS-07 |
| O uso típico dura de 30 min a 1 h (10 de 18) e o uso à noite é comum (7 de 18 depois das 22 h). | QST P06, P07; ENT-01, ENT-02 | Confirma DEC-07 (1 h, até 00:00, por espaço) |
| Querer ser avisado quando o pedido muda ou um uso confirmado é cancelado (8 de 18). | QST P09; ENT-03 | Nova NS-17, fora do 1.0 (DEC-24) |
| Aulas e eventos da instituição ocupam o espaço sem aviso. | ENT-02, ENT-03, ENT-04 | Fora do escopo (DEC-24) |

Também fora do escopo: não comparecimento e material esportivo. Sem base para concluir: usos acima de 3 h, "quem decidiu e por quê" (5 de 18) e servidores e docentes (2 de 18).

Decisões resultantes. Mudaram na Aula 7: DEC-13 (concluir só depois do término), DEC-05 (tentativas recusadas no histórico), DEC-07 (07:00 às 00:00 por espaço) e DEC-09 (matrícula só com dígitos); as demais foram confirmadas. Nova: DEC-24, NS-17 fica fora do 1.0.

## 6. Limitações e ameaças à validade

A amostra é por conveniência, não estatística: os números indicam tendências, não probabilidades. Os dados de três das quatro entrevistas e todas as 18 respostas do questionário são simulados pelo grupo; servem para ensaiar o método e a rastreabilidade, não para decidir requisitos, e o único registro com pessoa real é a entrevista da Aula 7. O representante do cliente é o professor da disciplina, sem cliente real nomeado (premissa P-01), e as regras de uso não têm validação de um cliente real. As 18 respostas superam a meta de 15 só em número. Quase só estudantes de graduação responderam (13 de 18); servidor e docente somam 2 de 18, não há resposta "Outro" e nenhum subgrupo permite comparar perfis; o questionário não mostra os motivos nem a visão do Atendente e do Gestor, que só aparecem nas entrevistas (uma delas simulada). Quem tem problema tende a responder mais, o que, com respostas reais, inflaria os achados de conflito.
