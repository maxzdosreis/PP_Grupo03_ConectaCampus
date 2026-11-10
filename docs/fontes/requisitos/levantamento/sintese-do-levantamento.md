# Síntese do levantamento

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **SIN-01 • 0.1 • Rascunho** (síntese do levantamento) | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/levantamento/sintese-do-levantamento.md` |

Elo entre o que ouvimos (entrevistas e questionário) e a especificação: cada achado vai para uma necessidade (NS), um requisito, uma decisão (DEC) ou para o fora do escopo da [Visão](../visao.md#3-escopo-inicial-do-sistema), ou fica sem base para concluir. Esta síntese **não altera** RF, casos de uso, histórias, critérios de aceite, testes de aceite nem a rastreabilidade: o que isso exige está em [Pendências para a REQ-13](#6-pendências-para-a-req-13). Versão de uma página para o PDF de evidências: [sintese-evidencia-1pag.md](sintese-evidencia-1pag.md).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Criação: 23 achados com destino, convergências, decisões resultantes (NS-17 e DEC-24) e pendências para a REQ-13 (REQ-11). Sem aprovação. |

## 1. Técnicas, instrumentos e participantes

| Técnica | Instrumento | Participantes (perfis genéricos, sem dado pessoal) | Registro |
|---|---|---|---|
| Entrevista semiestruturada | [ROT-01](entrevistas/ROT-01-representante-do-cliente.md), [ROT-02](entrevistas/ROT-02-solicitante.md), [ROT-03](entrevistas/ROT-03-atendente-responsavel.md) | 4 entrevistados em 3 papéis: 1 representante do cliente (instituição), 2 Solicitantes (1 estudante de graduação que usa as quadras toda semana e 1 servidor que usa o ginásio de vez em quando) e 1 Atendente responsável (servidor do setor, há mais de um ano) | [ENT-01](entrevistas/ENT-01-representante-do-cliente.md), [ENT-02](entrevistas/ENT-02-solicitante-estudante-simulada.md), [ENT-03](entrevistas/ENT-03-solicitante-servidor-simulada.md), [ENT-04](entrevistas/ENT-04-atendente-responsavel-simulada.md) |
| Questionário anônimo | [QST-01](questionario/QST-01-questionario.md) (11 perguntas, 9 obrigatórias) | N = 18 Solicitantes: 13 estudantes de graduação, 3 de pós-graduação, 1 servidor técnico-administrativo e 1 docente (P01); 9 usam toda semana, 5 algumas vezes por mês, 2 raramente e 2 nunca usaram (P02) | [QST-01-resultados](questionario/QST-01-resultados.md) |

**O que cada técnica mostrou.**

- **Entrevistas.** O representante do cliente definiu as regras que mudaram na Aula 7 ([DEC-13](../decisoes/DEC-13.md), [DEC-05](../decisoes/DEC-05.md), [DEC-07](../decisoes/DEC-07.md), [DEC-09](../decisoes/DEC-09.md)) e confirmou as demais opções adotadas. Os Solicitantes descrevem um pedido informal (mensagem, telefone, ir até lá), com resposta em dias e sem saber o que está livre. O Atendente descreve anotação em papel, resposta em um a três dias, horário próprio por espaço e a pergunta que mais se repete: "quais horários estão livres?".
- **Questionário.** A prática mais comum é ir até lá e ver (12 de 18) ou combinar por mensagem ou telefone (9 de 18); pedir por e-mail ou formulário é raro (2 de 18). Chegar a um espaço ocupado ou fechado sem saber aconteceu ao menos uma vez em 3 meses com 14 de 18 (3 vezes ou mais: 4 de 18). Saber se o pedido foi aceito é a informação mais marcada (12 de 18). O uso típico dura de 30 minutos a 1 hora (10 de 18) e ninguém marcou mais de 2 horas (0 de 18). O uso à noite é comum (11 de 18 no início da noite; 7 de 18 depois das 22 h). Das 18 pessoas, 9 não comunicam a desistência (7 não sabem a quem avisar e 2 não avisam).

## 2. Achados e destinos

Cada linha reúne os achados preliminares dos registros que tratam do mesmo assunto (coluna "Origem"). Destinos possíveis: **CONFIRMA** um item existente, **CONTESTA** um item existente, **NOVA NS**, **FORA DO ESCOPO** ou **SEM BASE PARA CONCLUIR**. Todas as decisões abaixo foram aprovadas pelo grupo em 10/11/2026. Não existem requisitos de regra com ID "RN" no repositório: as regras são as DECs, os RF e as premissas.

| ID | Achado | Fonte | Origem | Destino | Item afetado | Decisão |
|---|---|---|---|---|---|---|
| ACH-01 | O Gestor só conclui depois do término e só recusa ou cancela antes do início. | ENT-01 P01; ENT-04 P05 | ENT-01 A1; ENT-04 A4 | CONFIRMA DEC-13 | NS-09; [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md) | Aprovada: segue o CR-01 |
| ACH-02 | As tentativas recusadas de mudar a situação ficam no histórico. | ENT-01 P02 | ENT-01 A2 | CONFIRMA DEC-05 | NS-12; [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md) | Aprovada: segue o CR-02 |
| ACH-03 | Funcionamento das 07:00 às 00:00, reserva padrão de 1 h e horário por espaço; o uso à noite é comum (11 de 18 no início da noite, 7 de 18 depois das 22 h). | ENT-01 P03; ENT-04 P07; ENT-02 P07; QST-01-P07 | ENT-01 A3; ENT-04 A6 (1ª parte); ENT-02 A4; QST A8 | CONFIRMA DEC-07 | NS-06; P-04; [CR-03](../mudancas/CR-03-horario-por-espaco.md) | Aprovada: segue o CR-03 |
| ACH-04 | A matrícula tem só números, sem mínimo nem máximo. | ENT-01 P05 | ENT-01 A4 | CONFIRMA DEC-09 | P-02; [CR-04](../mudancas/CR-04-matricula-so-digitos.md) | Aprovada: segue o CR-04 |
| ACH-05 | Opções já adotadas, confirmadas: reservas de espaço desativado, nome único, horários ocupados na agenda, cobertura, desempenho e convenções de documentação. | ENT-01 P04; ENT-01 P06; ENT-01 P07; ENT-01 P08; ENT-01 P09; ENT-01 P10; ENT-01 P11; ENT-01 P12; ENT-01 P13; ENT-01 P14; ENT-01 P16 | ENT-01 A5 | CONFIRMA DEC-06, DEC-10, DEC-11, DEC-08, DEC-12 e DEC-14 a DEC-19 | NS-02, NS-05, NS-14 | Aprovada: nenhuma mudança |
| ACH-06 | Os documentos de Requisitos são entrega separada, com outros a detalhar. | ENT-01 P17 | ENT-01 A6 | FORA DO ESCOPO (é entrega do projeto, não necessidade do produto) | DEC-20 | Aprovada: tratada na DEC-20 |
| ACH-07 | Hoje o pedido é feito indo até lá, por mensagem ou por telefone; e-mail ou formulário é raro (2 de 18). | QST-01-P03; ENT-02 P01; ENT-03 P01; ENT-04 P01 | QST A1; ENT-02 A1; ENT-03 A1; ENT-04 A1 | CONFIRMA Visão §1 (o problema) | NS-03, NS-05 | Aprovada: nenhuma mudança |
| ACH-08 | A resposta ao pedido leva de um dia a uma semana, sem registro claro (no questionário, 2 de 9 respostas abertas citam a demora). | ENT-03 P01; ENT-03 P11; ENT-04 P01; QST-01-P10 | ENT-03 A1; ENT-04 A1; QST A10 | CONFIRMA NS-07 | NS-09, NS-12 | Aprovada. Sem base para priorizar pelo questionário (2 de 9) |
| ACH-09 | Dois grupos no mesmo horário e chegar a espaço ocupado ou fechado são frequentes (14 de 18; 4 de 9 respostas abertas citam combinados informais). | QST-01-P04; QST-01-P10; ENT-02 P04; ENT-04 P03 | QST A2, A9; ENT-02 A2; ENT-04 A3 | CONFIRMA NS-04 | NS-05, RF-11.4 (vale quem pediu primeiro) | Aprovada: nenhuma mudança |
| ACH-10 | Quem pede quer ver quais horários estão livres ou tomados, sem saber quem ocupou nem por quê (8 de 18); o Atendente responde isso repetidamente. | QST-01-P09; ENT-02 P09; ENT-02 P11; ENT-03 P02; ENT-03 P09; ENT-04 P11 | ENT-02 A3; ENT-03 A2; ENT-04 A9 | CONFIRMA NS-05 | NS-14, DEC-11 | Aprovada: nenhuma mudança |
| ACH-11 | Quem pede quer ver se o pedido foi aceito (12 de 18) e, se negado, o motivo. | QST-01-P09; ENT-03 P10; ENT-04 P02 | QST A3 (1ª parte); ENT-03 A3; ENT-04 A2 | CONFIRMA NS-07 | NS-09, RF-18 | Aprovada: nenhuma mudança |
| ACH-12 | "Saber quem decidiu e por quê" foi a opção menos marcada (5 de 18), sem diferença clara das outras. | QST-01-P09 | QST A3 (2ª parte) | SEM BASE PARA CONCLUIR | NS-11, NS-12 | Aprovada: nenhuma mudança |
| ACH-13 | O uso típico dura de 30 min a 1 h (10 de 18; 0 de 18 acima de 2 h); a ENT-03 descreve 2 a 3 h. | QST-01-P06; ENT-02 P05; ENT-03 P05 | QST A6; ENT-02 A5; ENT-03 A5 | CONFIRMA DEC-07 (padrão de 1 h, máximo de 3 h) | NS-06 | Aprovada: divergência anotada |
| ACH-14 | A antecedência é curta (mesmo dia 5 de 18; de 1 a 7 dias 6 de 18; acima de 30 dias 0 de 18), com semanas em torneios. | QST-01-P05; ENT-02 P06; ENT-03 P06 | QST A7; ENT-02 A6 | CONFIRMA DEC-07 (30 dias) | NS-06 | Aprovada: compatível; sem base sobre o limite |
| ACH-15 | Há usos maiores que 3 h e pedidos com mais de 30 dias de antecedência (atividades grandes). | ENT-03 P06 | ENT-03 A6 | SEM BASE PARA CONCLUIR | DEC-07 | Aprovada: uma fonte; o questionário tem 0 de 18 acima de 2 h e acima de 30 dias |
| ACH-16 | Quem pede quer ficar sabendo quando a situação do pedido muda, em especial quando um uso confirmado é cancelado na véspera (8 de 18). | QST-01-P09; ENT-03 P04 | QST A4; ENT-03 A4 | NOVA NS-17 | [NS-17](../visao.md#ns-17); [DEC-24](../decisoes/DEC-24.md) | Aprovada: NS-17 fora do 1.0 |
| ACH-17 | Quem desiste muitas vezes não avisa ou não sabe a quem avisar (9 de 18; 4 de 18 pedem um jeito de avisar). | QST-01-P08; QST-01-P11; ENT-03 P08; ENT-02 P08 | QST A5; ENT-03 A7 | CONFIRMA NS-10 | NS-04 (cancelar libera o horário) | Aprovada: não vira NS nova |
| ACH-18 | Grupo que não aparece deixa o horário vazio, e nada é feito. | ENT-02 P08; ENT-04 P06 | ENT-02 A7; ENT-04 A5 | FORA DO ESCOPO (controle de presença, Visão §3) | Visão §3 | Aprovada |
| ACH-19 | Aulas e atividades da instituição ocupam o espaço ou derrubam um uso aceito, sem aviso. | ENT-02 (assunto novo); ENT-04 (assunto novo); ENT-03 P04 | ENT-02 A8; ENT-04 A8 | FORA DO ESCOPO (bloqueio de períodos, Visão §3) | [DEC-24](../decisoes/DEC-24.md) (d) | Aprovada: sem NS própria; reavaliar com cliente real |
| ACH-20 | Pediram saber se há material esportivo disponível (2 de 18). | QST-01-P11 | QST A11 | FORA DO ESCOPO (empréstimo de material, Visão §3) | Visão §3 | Aprovada. Sem base para priorizar |
| ACH-21 | Há funcionamento reduzido em fins de semana e fechamento em feriados. | ENT-04 P07 | ENT-04 A6 (2ª parte) | FORA DO ESCOPO (por dia da semana e feriados, Visão §3) | DEC-07; P-04 | Aprovada: uma fonte; a ENT-01 pediu só horário por espaço |
| ACH-22 | As regras de uso são definidas pela coordenação do setor, e os atendentes só são avisados. | ENT-04 P08 | ENT-04 A7 | CONFIRMA Visão, "Cliente × usuário" | Visão §2 | Aprovada. A separação Atendente e Gestor do serviço é da REQ-12 |
| ACH-23 | Quase só estudantes de graduação responderam (13 de 18). | QST-01-P01 | QST A12 | SEM BASE PARA CONCLUIR sobre servidores e docentes | P-02 | Aprovada: nenhuma mudança |

**Texto da NS-17.** "Ficar sabendo que a situação de um pedido próprio mudou, em especial quando um uso já confirmado é cancelado antes de acontecer." Descreve a necessidade, não o canal: o aviso ativo (e-mail, SMS, aplicativo) segue no fora do escopo.

**Descartados ou rebaixados**, porque as respostas não os sustentam:

- **ENT-03 A5, "contesta a duração padrão de 1 h":** descartado. O padrão é só uma sugestão editável; uma fonte contra 10 de 18 no questionário e a ENT-02.
- **ENT-03 A6, "contesta o máximo de 3 h e os 30 dias":** rebaixado a SEM BASE (ACH-15).
- **QST A4, "contesta o fora do escopo":** reduzido. "Ser avisado se algo mudar" foi marcado por 8 de 18 numa lista de até 3 opções e não indica canal; a NS-17 trata da necessidade, não de notificação por e-mail ou SMS.
- **QST A5 e ENT-03 A7, "necessidade nova: aviso ao Gestor":** descartado como NS. O cancelamento já libera o horário e o Gestor vê todas as reservas (ACH-17).
- **Temas de P10 e P11 sem achado preliminar:** regras pouco claras (1 de 18) e capacidade do espaço (1 de 18). Não promovidos; a capacidade já está na NS-01.
- **ENT-01 P15** (grupo nas duas disciplinas): não foi perguntada.

## 3. Convergências e divergências

**Entre técnicas.**

| Tema | Relação | Achados |
|---|---|---|
| Como se consegue o espaço hoje | Convergem | ACH-07 |
| Choque de horário e espaço ocupado | Convergem | ACH-09 |
| Ver o que está livre sem saber quem ocupou | Convergem (e o Atendente confirma do outro lado) | ACH-10 |
| Funcionamento à noite | Convergem (QST P07, ENT-02, ENT-01) | ACH-03 |
| Aviso de mudança | Convergem: a necessidade aparece nas duas técnicas | ACH-16 |
| Duração e antecedência | Divergem: a ENT-03 descreve 2 a 3 h e cerca de 2 semanas; no questionário, 0 de 18 passam de 2 h e 1 de 18 marcou de 7 a 30 dias | ACH-13, ACH-14, ACH-15 |
| Desistência | Divergem em parte: as entrevistas avisam de modo informal; o questionário mostra 9 de 18 que não comunicam | ACH-17 |
| Material esportivo | Só o questionário | ACH-20 |
| Aulas e eventos da instituição | Só as entrevistas | ACH-19 |

**Entre perfis.**

- **Solicitantes (ENT-02, ENT-03, questionário):** querem ver o que está livre sem saber quem ocupou; o servidor quer também o motivo da recusa e o aviso de cancelamento.
- **Atendente (ENT-04):** a pergunta que mais se repete é "quais horários estão livres?" (reforça a NS-05); só ele traz horário por espaço e por dia da semana (ACH-03, ACH-21). O questionário não o cobre.
- **Cliente (ENT-01):** é quem decide regra. Não citou notificação, bloqueio de períodos, presença nem material (ACH-16, ACH-18 a ACH-20).

## 4. Decisões resultantes

| DEC | Situação nesta síntese | Origem | CR |
|---|---|---|---|
| [DEC-13](../decisoes/DEC-13.md) | **Mudou** (concluir só depois do término; recusar e cancelar pelo Gestor só antes do início) | ACH-01 | [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md) |
| [DEC-05](../decisoes/DEC-05.md) | **Mudou** (tentativas recusadas no histórico) | ACH-02 | [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md) |
| [DEC-07](../decisoes/DEC-07.md) | **Mudou** (07:00 às 00:00, 1 h sugerida, horário por espaço) e foi reforçada pelo questionário | ACH-03, ACH-13, ACH-14 | [CR-03](../mudancas/CR-03-horario-por-espaco.md) |
| [DEC-09](../decisoes/DEC-09.md) | **Mudou** (matrícula só com dígitos) | ACH-04 | [CR-04](../mudancas/CR-04-matricula-so-digitos.md) |
| [DEC-06](../decisoes/DEC-06.md), [DEC-08](../decisoes/DEC-08.md), [DEC-10](../decisoes/DEC-10.md), [DEC-11](../decisoes/DEC-11.md), [DEC-12](../decisoes/DEC-12.md), [DEC-14](../decisoes/DEC-14.md) a [DEC-19](../decisoes/DEC-19.md) | Confirmadas (a DEC-11 também pelos Solicitantes e pelo Atendente) | ACH-05, ACH-10 | — |
| [DEC-20](../decisoes/DEC-20.md) a [DEC-23](../decisoes/DEC-23.md) | Decididas na Aula 7: entrega, capa, contribuições e apresentação (processo do projeto, não do produto) | ACH-06 | — |
| [DEC-24](../decisoes/DEC-24.md) | **Nova**: NS-17 fica fora do 1.0; bloqueio de períodos continua fora do escopo | ACH-16, ACH-19 | — |

Nova necessidade: **[NS-17](../visao.md#ns-17)**. Nenhuma NS existente foi alterada.

## 5. Ameaças à validade e limitações

- **Amostra por conveniência, não estatística.** N = 18 no questionário e 4 entrevistados; os números indicam tendências, não probabilidades.
- **N obtido × meta.** 18 respostas contra a meta de 15 (+3). As entrevistas cumprem o mínimo de dois representantes de stakeholders do enunciado (§5.3).
- **Perfis ausentes ou raros.** Servidor e docente somam 2 de 18; nenhum "Outro"; só 2 de 18 nunca usaram os espaços; sem comparação entre perfis. O questionário não cobre Atendente nem Gestor, que ficam com as entrevistas (1 Atendente, 1 representante do cliente).
- **Cliente sem nome (P-01).** O representante do cliente é o professor da disciplina; as regras de uso não têm validação de um cliente real. Daí o item "Bloqueio de períodos" ficar para reavaliação (ACH-19).
- **Viés de resposta.** Quem tem problema tende a responder mais, o que pode inflar ACH-09.
- **Uma fonte só** em ACH-15 e ACH-21; por isso ficam sem base ou fora do escopo, e não viram requisito.
- **Registros.** Os registros ENT-02 a ENT-04 e QST-01 trazem, cada um, a própria nota sobre como foram obtidos; esta síntese usa o conteúdo deles como está, sem acrescentar dado.
- **O que o questionário não mostra:** os motivos por trás das respostas, regras por espaço, usos acima de 3 horas ou muito antecipados.

## 6. Pendências para a REQ-13

Nada abaixo foi aplicado aqui. A REQ-13 aplica na especificação, antes do código.

| # | Item afetado | Tipo de mudança | Origem |
|---|---|---|---|
| 1 | [NS-17](../visao.md#ns-17) sem RF: o `verificar_requisitos.py` (NS ↔ RF) acusa a NS-17 como "não é origem principal de nenhum RF" | Decidir: criar um RF ou fazer a verificação reconhecer necessidade fora do 1.0 | ACH-16, DEC-24 |
| 2 | SRS: lacuna L-11 ("as 16 NS têm pelo menos um RF"), tabela NS → RF (6.1) e contagens de NS | Editorial: passam a 17 NS, uma fora do 1.0 | ACH-16 |
| 3 | RF-16 a RF-21, ações disponíveis, UC-10 e histórias de decisão | Comportamental: aplicar o [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md) | ACH-01 |
| 4 | RF-22, RNF-R02 e os CAs de registro de 6 histórias | Comportamental: aplicar o [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md) | ACH-02 |
| 5 | RF-11.5, RF-28, RF-30, RF-31, cadastro de espaços e P-04 | Comportamental: aplicar o [CR-03](../mudancas/CR-03-horario-por-espaco.md) | ACH-03 |
| 6 | RF-32.1 e validação do cadastro | Comportamental: aplicar o [CR-04](../mudancas/CR-04-matricula-so-digitos.md) | ACH-04 |
| 7 | Visão (stakeholders) e papéis Atendente responsável e Gestor do serviço | Tarefa REQ-12, não CR desta síntese | ACH-22 |
| 8 | Visão §3, "Bloqueio de períodos" | Reavaliar com cliente real; sem CR agora | ACH-19, DEC-24 |
| 9 | Se o grupo trouxer a NS-17 para o 1.0 | Abrir um CR novo (o próximo número livre) pelo [modelo de CR](../mudancas/modelo-cr.md) e substituir a DEC-24 | ACH-16 |

Os CR-01 a CR-04 já existem, aprovados, e aguardam a implementação (RES-11, RES-12, ESP-07 e AUT-12). Nenhum CR novo foi aberto, porque a NS-17 fica fora do 1.0 e não muda nenhum artefato existente.
