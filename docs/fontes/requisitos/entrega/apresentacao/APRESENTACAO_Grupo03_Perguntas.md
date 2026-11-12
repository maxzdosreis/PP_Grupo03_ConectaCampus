# Perguntas prováveis da apresentação de Requisitos

| Identificação | Responsabilidade |
|---|---|
| **APR-02 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

Material de apoio à [apresentação](APRESENTACAO_Grupo03_Roteiro.md) (REQ-15). As respostas são fatos da [especificação](../RS_Grupo03_Especificacao.md) e da fonte oficial; onde a resposta depende de opinião ou de experiência do grupo, está marcado. Ninguém aqui responde pelo que outra pessoa fez.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 12/11/2026 | Max Zimmermann dos Reis | Criação (REQ-15). Sem aprovação. |

## Escopo e decisões

### P01. Por que a Aula 7 mudou a DEC-13, a DEC-05, a DEC-07 e a DEC-09, e o que não mudou?

**Resposta:** A entrevista com o professor, na Aula 7, definiu quatro regras: concluir só a partir do término e recusar ou cancelar só antes do início (DEC-13); registrar no histórico também as tentativas recusadas (DEC-05); funcionamento das 07:00 às 00:00 por espaço, com duração sugerida de 1 hora (DEC-07); e matrícula só com dígitos (DEC-09). As demais decisões adotadas até então foram confirmadas. As quatro viraram os CR-01 a CR-04, já aplicados na especificação.
**Origem:** DEC-13, DEC-05, DEC-07, DEC-09, CR-01 a CR-04; seção 4 da especificação.
**Quem responde:** [A DEFINIR]

### P02. O que ficou fora do escopo, e por que desativar um espaço não cancela as reservas dele?

**Resposta:** Ficaram fora, entre outros, pagamento, notificações, reservas recorrentes, lista de espera e exclusão de reservas ou espaços (seção 2). A necessidade de ser avisado de mudanças (NS-17) ficou fora do 1.0 pela DEC-24. Desativar um espaço só bloqueia novos pedidos; as reservas existentes continuam valendo (DEC-06, RN07), e quem decide cancelar alguma é o Gestor.
**Origem:** seção 2 da especificação; DEC-24; DEC-06; RN07.
**Quem responde:** [A DEFINIR]

## Papéis

### P03. Por que um perfil cobre o Atendente responsável e o Gestor do serviço?

**Resposta:** Porque o sistema mínimo (1.0) tem dois perfis, Solicitante e Gestor. Atendente responsável e Gestor do serviço são papéis da especificação, e o perfil Gestor exerce os dois. Os requisitos falam em Gestor (o perfil); os casos de uso falam no papel.
**Origem:** DEC-25; seção 3 da especificação; glossário.
**Quem responde:** [A DEFINIR]

### P04. Como o Atendente responsável entra na especificação?

**Resposta:** Como papel e ator dos casos de uso que decidem sobre reservas (por exemplo UC-17 e UC-18), nas regras RN09 e RN10 e nas histórias US-11 e US-14 a US-16. O CR-05 ajustou os artefatos de ator misto e dividiu a US-13 em US-13 e US-20.
**Origem:** DEC-25; CR-05; RN09, RN10; seção 9 da especificação.
**Quem responde:** [A DEFINIR]

## Levantamento

### P05. Qual foi o tamanho da amostra?

**Resposta:** Quatro entrevistados em três papéis (um representante do cliente, dois Solicitantes e um Atendente responsável) e 18 respostas de Solicitantes no questionário, 13 de graduação, 3 de pós, 1 servidor e 1 docente. É amostra por conveniência; as 18 respostas superam a meta de 15. Servidores e docentes somam 2 de 18, pouco para concluir sobre eles.
**Origem:** seção 4 da especificação; síntese do levantamento; ENT-01 a ENT-04.
**Quem responde:** [A DEFINIR]

### P06. O professor como cliente: isso vale como entrevista com o cliente?

**Resposta:** O grupo não tem cliente real nomeado: representa a instituição, e o professor é a referência para as dúvidas de regra (P-01). A ENT-01 foi presencial, na Aula 7, com o professor no papel de representante da instituição, e foi o que definiu as quatro mudanças de regra. As regras e as necessidades precisam ser validadas com um cliente real, o que a P-01 registra como risco.
**Origem:** P-01 (visão); ENT-01; seção 4 da especificação.
**Quem responde:** [A DEFINIR]

### P07. As entrevistas e o questionário foram simulados. Isso não invalida o levantamento?

**Resposta:** Só a ENT-01 foi com pessoa real. As ENT-02 a ENT-04 foram simuladas, e as 18 respostas do questionário foram simuladas em 09/11/2026, sem período de campo; a especificação diz que os números descrevem esses dados simulados e não medem pessoas reais. O enunciado admite a interação com ao menos dois representantes de stakeholders, e o grupo deixou os registros sintéticos no arquivo de evidências. [CONFIRMAR COM O GRUPO: como o grupo construiu os dados simulados e o que diria ao professor sobre a validade]
**Origem:** seção 4 da especificação; documento de evidências; ENT-02 a ENT-04.
**Quem responde:** [A DEFINIR]

## Requisitos

### P08. Qual a diferença entre RF, RNF e RN, com um exemplo do projeto?

**Resposta:** RF é o que o sistema faz: RF11, solicitar a reserva de um espaço. RNF é uma qualidade com condição observável: RNF20, nunca existem duas reservas que ocupam horário no mesmo espaço com algum momento em comum. RN é a regra que a instituição exige: RN04, uma reserva dura de 30 minutos a 3 horas. Cada RN aponta os RF que a cobram.
**Origem:** RF11; RNF20; RN04; seções 5 a 7 da especificação.
**Quem responde:** [A DEFINIR]

### P09. Por que FURPS+?

**Resposta:** A especificação classifica cada requisito não funcional numa das classes do modelo FURPS+ (funcionalidade, usabilidade, confiabilidade, desempenho e suportabilidade), o que dá uma lista de verificação de qualidades e uma condição observável por requisito. Dos 33, 13 são de funcionalidade, 6 de usabilidade, 6 de confiabilidade, 2 de desempenho e 6 de suportabilidade. [CONFIRMAR COM O GRUPO: o motivo da escolha do FURPS+ em vez de outro modelo]
**Origem:** seção 6 da especificação.
**Quem responde:** [A DEFINIR]

### P10. Dê um exemplo de requisito verificável.

**Resposta:** RNF26: com 1.000 e com 5.000 reservas, a consulta de reservas responde em até 1 s no percentil 95, em quatro usos descritos. Outro: RF11.5 recusa o pedido que comece antes da abertura, dure menos de 30 minutos ou mais de 3 horas, ou passe de 30 dias de antecedência, e informa a primeira regra violada, nesta ordem: funcionamento, duração e antecedência.
**Origem:** RNF26 (DEC-12); RF11.5.
**Quem responde:** [A DEFINIR]

## Caso de uso

### P11. O que é fluxo alternativo (A) e o que é exceção (E)?

**Resposta:** A alternativa é uma variação em que a meta continua possível, como a A3.1 do UC-04, consultar a agenda do dia antes de enviar. A exceção é um caminho em que a meta não é alcançada, como a E9.1, conflito de horário. Os IDs ligam ao passo: A3.1 sai do passo 3 e E9.1 falha no passo 9. Cada exceção traz condição, resultado, estado depois e requisito.
**Origem:** DEC-14; UC-04 (seção 8.1 da especificação).
**Quem responde:** [A DEFINIR]

### P12. Por que o UC-04 e não outro?

**Resposta:** O UC-04 realiza o pedido de reserva, a meta central do sistema, e concentra a regra mais importante, sem conflito de horário (RN01). Tem a US-08, com 26 critérios de aceitação, o maior número entre as histórias. [CONFIRMAR COM O GRUPO: se o grupo escolheu o UC-04 por esse motivo]
**Origem:** UC-04; US-08; RN01.
**Quem responde:** [A DEFINIR]

### P13. O que acontece quando uma regra é violada?

**Resposta:** O sistema recusa a operação, informa qual regra impediu e em qual campo corrigir, e não grava nada. Os dados informados continuam com a pessoa para ela corrigir só o apontado. No UC-04, a reserva e o registro de criação não são gravados, e as reservas existentes não mudam. Só a tentativa recusada de mudar a situação de uma reserva visível ao ator entra no histórico (DEC-05, RNF21).
**Origem:** UC-04 (alternativas e exceções); RNF22; RNF21; DEC-05.
**Quem responde:** [A DEFINIR]

## Documentação e rastreabilidade

### P14. Por que RF01 no documento e RF-01 na fonte?

**Resposta:** O documento usa a forma RF01, RNF01 e RN01 e a fonte oficial mantém a forma RF-01. A regra de conversão é única e está no Anexo A, com a tabela de correspondência. O RNF da fonte leva a letra da classe (RNF-F01) e vira RNF01 a RNF33 em sequência. UC, US, NS e DEC não mudam.
**Origem:** Anexo A da especificação.
**Quem responde:** [A DEFINIR]

### P15. Qual a regra de versão, de 0.1 a 1.0?

**Resposta:** 0.1 é o rascunho, 0.2 vem depois da revisão por pares e 1.0 é a primeira baseline aprovada. Todo documento traz identificador, versão, estado, autor, revisor, aprovador e histórico de revisões. A especificação está na 0.1, Rascunho; a baseline 1.0 existe como candidata, aguardando aprovação.
**Origem:** DEC-17; seção 11.1 da especificação.
**Quem responde:** [A DEFINIR]

### P16. O que é um CR e o que o grupo mudou?

**Resposta:** CR é um pedido de mudança, registrado antes de alterar a especificação. Foram cinco, todos aplicados: CR-01 a CR-04 aplicam as quatro mudanças da Aula 7 e o CR-05 ajustou os papéis, dividindo a US-13.
**Origem:** CR-01 a CR-05; seção 11.1 da especificação.
**Quem responde:** [A DEFINIR]

### P17. Como uma necessidade vira requisito, caso de uso e história?

**Resposta:** As necessidades (NS) da Visão originam os requisitos. Na especificação, cada RF traz o caso de uso e as histórias a que se liga; cada RNF, a necessidade e a decisão de origem; cada RN, os RF que a cobram. A fonte oficial tem uma matriz de rastreabilidade gerada por script. Exemplo: NS-04 leva ao RNF20 e ao RF11.4, ao UC-05 e à US-08.
**Origem:** seções 5 a 7 da especificação; RNF20; RF11.4.
**Quem responde:** [A DEFINIR]

## Entrega

### P18. O que está implementado e o que ainda não, sem esconder?

**Resposta:** Está pronta a especificação, na versão 0.1, com 20 histórias e o levantamento documentado. As regras decididas na Aula 7 já estão especificadas e, segundo a especificação, entram no código em tarefas posteriores; o código descrito no repositório ainda usa o fechamento do horário anterior à DEC-07. [CONFIRMAR COM O GRUPO: o estado real do código no dia da apresentação, regra por regra]
**Origem:** seção 11.1 da especificação; DEC-13, DEC-05, DEC-07, DEC-09.
**Quem responde:** [A DEFINIR]

## O que não sabemos

- **Dados do levantamento:** três das quatro entrevistas e todas as 18 respostas do questionário são simuladas. Não podemos afirmar o que pessoas reais pensam; os números descrevem os dados simulados.
- **Cliente:** não há cliente real nomeado (P-01). Os valores de regra, como o horário e a duração, estão decididos com o professor como referência e precisam de validação com um cliente real.
- **Amostra:** por conveniência, com poucos servidores e docentes (2 de 18). Usos acima de 3 horas e a pergunta "quem decidiu e por quê" não têm base para conclusão.
- **Código:** as regras da Aula 7 estão só na especificação e entram no código depois. [CONFIRMAR COM O GRUPO: lista do que já está no código]
- **Aprovação:** os documentos estão em 0.1, sem aprovação; a turma e os nomes completos dos integrantes seguem pendentes. [PENDENTE: preencher a turma e confirmar os nomes completos]
- **Quadro de contribuições:** parte do quadro da especificação (seção 11.2) ainda está por preencher pelo grupo.

## Perguntas sobre contribuição individual

Cada integrante deve responder com as próprias palavras. Este material não escreve a resposta por ninguém.

### [INTEGRANTE 1]

1. Minha parte no projeto foi: [PREENCHER PELO INTEGRANTE]
2. Um requisito, caso de uso ou decisão em que trabalhei e o que aprendi: [PREENCHER PELO INTEGRANTE]
3. O que eu faria diferente: [PREENCHER PELO INTEGRANTE]

### [INTEGRANTE 2]

1. Minha parte no projeto foi: [PREENCHER PELO INTEGRANTE]
2. Um requisito, caso de uso ou decisão em que trabalhei e o que aprendi: [PREENCHER PELO INTEGRANTE]
3. O que eu faria diferente: [PREENCHER PELO INTEGRANTE]

### [INTEGRANTE 3]

1. Minha parte no projeto foi: [PREENCHER PELO INTEGRANTE]
2. Um requisito, caso de uso ou decisão em que trabalhei e o que aprendi: [PREENCHER PELO INTEGRANTE]
3. O que eu faria diferente: [PREENCHER PELO INTEGRANTE]

### [INTEGRANTE 4]

1. Minha parte no projeto foi: [PREENCHER PELO INTEGRANTE]
2. Um requisito, caso de uso ou decisão em que trabalhei e o que aprendi: [PREENCHER PELO INTEGRANTE]
3. O que eu faria diferente: [PREENCHER PELO INTEGRANTE]
