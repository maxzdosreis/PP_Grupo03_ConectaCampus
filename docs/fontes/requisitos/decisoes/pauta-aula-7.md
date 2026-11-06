# Pauta para o professor — Aula 7 (06/11/2026)

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **PAU-01 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: a definir • Aprovador: a definir | `docs/fontes/requisitos/decisoes/pauta-aula-7.md` |

Perguntas que o grupo leva à Aula 7: as DECs com prazo em 06/11/2026 e os pontos a confirmar ainda abertos. Cada item traz a opção que o código já implementa, o porquê e o que muda se a resposta for outra, com o número de critérios (CA) e testes de aceite (TA) a rever, tirado do [mapa de impacto](../rastreabilidade/impacto-por-dec.md) (o script confere esses números). Toda resposta diferente da opção adotada é **mudança comportamental**: vira um [CR](../mudancas/modelo-cr.md), e a baseline vigente continua valendo até a aprovação. As respostas são passadas para a DEC (estado, resposta e data) no mesmo dia.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Criação: DEC-05, 06, 07, 09, 10, 11 e 13; DEC-08 e DEC-12 "se houver tempo"; pontos a confirmar abertos (REQ-06). Sem aprovação. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Respostas da Aula 7 registradas: resposta do professor e data em cada DEC, decisão do grupo separada onde a resposta não cobriu tudo, conclusão com o CR e a tarefa, tabela de pontos preenchida, entrega e apresentação e a seção Resultado (GES-02). Sem aprovação. |

## Decisões com prazo em 06/11/2026

### <a id="dec-13"></a>DEC-13 — Mudança de situação × horário da reserva

- **Pergunta:** concluir, confirmar, recusar e cancelar devem depender do horário da reserva (e o que acontece com um pedido que ninguém decidiu até a data passar)?
- **Adotado:** não dependem; valem a tabela de transições, o perfil e o motivo. Um pedido não decidido continua ocupando o horário. Por quê: nada no enunciado fixa essas regras, e elas dependem do uso real da instituição.
- **Se a resposta for outra:** 21 CAs e 21 TAs em 9 histórias; RF-16 a RF-21, exceções novas no UC-10 e as ações disponíveis em cada reserva ([impacto](../rastreabilidade/impacto-por-dec.md#dec-13)).
- **Resposta do professor:** "Temos que alterar, deve poder concluir somente depois do término, e recusar e cancelar somente antes do início (isso para Gestor)." • **Data:** 06/11/2026
- **Decisão do grupo:** confirmar continua sem restrição de horário; o cancelamento pelo Solicitante continua sem restrição de horário; a Solicitada não decidida continua ocupando o horário depois da data (pontos que o professor não abordou; mantida a opção atual).
- **Conclusão:** **muda** → [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md), tarefa RES-11.

### <a id="dec-05"></a>DEC-05 — Histórico só com mudanças efetivas

- **Pergunta:** uma tentativa recusada de mudar a situação precisa ficar registrada? Onde e para quem?
- **Adotado:** não; o histórico guarda só a criação e as mudanças aceitas. Por quê: uma recusa não muda a reserva. Difere do modelo de aceite da aula ("tentativa registrada com data, ator e resultado").
- **Se a resposta for outra:** 10 CAs e 10 TAs em 6 histórias; RF-22, RNF-R02 e o registro das recusas no histórico ou num log ([impacto](../rastreabilidade/impacto-por-dec.md#dec-05)).
- **Resposta do professor:** "Deve ficar registrado sim, para ter o histórico completo da reserva." • **Data:** 06/11/2026
- **Decisão do grupo:** as tentativas recusadas entram no próprio histórico da reserva (não num log separado), com ator, momento, situação pedida, resultado e código do erro; só se registram tentativas sobre uma reserva visível ao ator (a de outro Solicitante continua "não encontrada" e não é registrada, para não revelar a reserva).
- **Conclusão:** **muda** → [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md), tarefa RES-12.

### <a id="dec-07"></a>DEC-07 — Valores das regras de agenda

- **Pergunta:** quais são o horário de funcionamento, a duração mínima e máxima e a antecedência máxima? São iguais para todos os espaços e dias?
- **Adotado:** 07:00 às 22:00, de 30 min a 3 h, até 30 dias, iguais para todos. Por quê: sem cliente real (P-01), os valores são do grupo e ficam em constantes únicas.
- **Se a resposta for outra:** 10 CAs e 10 TAs em 2 histórias; RF-11.5, RF-28, RF-30, RF-31 e os testes de borda; por espaço ou por dia, o cadastro de espaços também muda ([impacto](../rastreabilidade/impacto-por-dec.md#dec-07)).
- **Resposta do professor:** "O horário de funcionamento é das 07:00 às 00:00, as reservas padrões são de 1 hora, e precisa de horário por espaço, porque teremos vários espaços." • **Data:** 06/11/2026
- **Decisão do grupo:** 07:00–00:00 é o padrão de cada espaço, configurável por espaço; "reservas padrões de 1 hora" = duração sugerida ao pedir; mínimo de 30 min, máximo de 3 h e antecedência de 30 dias continuam (o professor não os mudou); o término à meia-noite é o fim do dia da reserva.
- **Conclusão:** **muda** → [CR-03](../mudancas/CR-03-horario-por-espaco.md), tarefa ESP-07.

### <a id="dec-06"></a>DEC-06 — Reservas de um espaço desativado

- **Pergunta:** quando o Gestor desativa um espaço, o que acontece com as reservas que ele já tem?
- **Adotado:** continuam valendo; só novos pedidos ficam bloqueados, e o Gestor cancela uma a uma, se precisar. Por quê: preserva decisões e histórico; cancelar em cascata faria o cadastro de espaços conhecer as reservas.
- **Se a resposta for outra:** 14 CAs e 14 TAs em 4 histórias; RF-06, RF-07, RF-08, RF-11.3, RF-20 e RNF-R05 ([impacto](../rastreabilidade/impacto-por-dec.md#dec-06)).
- **Resposta do professor:** "Isso mesmo, deve continuar assim." • **Data:** 06/11/2026
- **Conclusão:** **confirma** a opção adotada; nenhum CR.

### <a id="dec-09"></a>DEC-09 — Formato da matrícula

- **Pergunta:** qual é o formato real da matrícula, e ela precisa ser conferida com a instituição?
- **Adotado:** obrigatória, única, até 20 caracteres, sem espaços, sem conferência. Por quê: o formato não foi informado; a regra está isolada numa função.
- **Se a resposta for outra:** 5 CAs e 5 TAs em 2 histórias; RF-32 e RF-32.1 e os dados de exemplo ([impacto](../rastreabilidade/impacto-por-dec.md#dec-09)).
- **Resposta do professor:** "São números sempre, mas não tem uma quantidade máxima e uma quantidade mínima." • **Data:** 06/11/2026
- **Decisão do grupo:** só dígitos; o limite de 20 caracteres fica como limite técnico (coluna do banco), não como regra da instituição.
- **Conclusão:** **muda** → [CR-04](../mudancas/CR-04-matricula-so-digitos.md), tarefa AUT-12.

### <a id="dec-10"></a>DEC-10 — Nome de espaço único

- **Pergunta:** dois espaços podem ter o mesmo nome? "Ginásio A" e "ginásio a" são o mesmo?
- **Adotado:** único, sem diferenciar maiúsculas de minúsculas. Por quê: nomes repetidos confundiriam quem pede e quem decide.
- **Se a resposta for outra:** 6 CAs e 6 TAs em 2 histórias; RF-05.2, RF-06.2 e a restrição do banco ([impacto](../rastreabilidade/impacto-por-dec.md#dec-10)).
- **Resposta do professor:** "É isso aí mesmo, está bom assim." • **Data:** 06/11/2026
- **Conclusão:** **confirma** a opção adotada; nenhum CR.

### <a id="dec-11"></a>DEC-11 — Períodos ocupados por outras pessoas na agenda do dia

- **Pergunta:** o Solicitante pode ver, antes de pedir, os períodos ocupados por reservas de outras pessoas? Com quais dados?
- **Adotado:** sim, só início, término e situação, nunca quem pediu nem para quê. Por quê: é o mesmo dado que a recusa por conflito já mostrava, só que antes do pedido.
- **Se a resposta for outra:** 5 CAs e 5 TAs em 1 história; RF-29 e RNF-F06 ([impacto](../rastreabilidade/impacto-por-dec.md#dec-11)).
- **Resposta do professor:** "É isso aí mesmo, está bom assim." • **Data:** 06/11/2026
- **Conclusão:** **confirma** a opção adotada; nenhum CR.

## Se houver tempo (prazo 13/11/2026)

### <a id="dec-08"></a>DEC-08 — Cobertura-alvo dos testes

- **Pergunta:** que meta de testes o grupo adota, já que a disciplina não exige testes?
- **Adotado:** 100% de linhas e ramos em `domain` e `application` de espaços e reservas; 99% no total. Por quê: as regras vivem nessas camadas.
- **Se a resposta for outra:** 0 CAs e 0 TAs; só a meta do RNF-S03 ([impacto](../rastreabilidade/impacto-por-dec.md#dec-08)).
- **Resposta do professor:** "Isso faz sentido, e precisamos fazer isso." (resposta dada à DEC-08 e à DEC-12 juntas) • **Data:** 06/11/2026
- **Conclusão:** **confirma** a opção adotada; nenhum CR.

### <a id="dec-12"></a>DEC-12 — Metas de desempenho

- **Pergunta:** em quanto tempo a consulta de reservas e a agenda do dia precisam responder, e com quantas reservas?
- **Adotado:** com 1.000 reservas, p95 até 1 s na consulta e até 500 ms na agenda (medido: 378 ms e 7 ms). Por quê: nenhum documento fixa tempo, e um RNF precisa de valor mensurável.
- **Se a resposta for outra:** 0 CAs e 0 TAs; as metas do RNF-P01 e do RNF-P02 e, com carga maior, a paginação da [L-05](../requisitos/srs.md#l-05) ([impacto](../rastreabilidade/impacto-por-dec.md#dec-12)).
- **Resposta do professor:** "Isso faz sentido, e precisamos fazer isso." (resposta dada à DEC-08 e à DEC-12 juntas) • **Data:** 06/11/2026
- **Conclusão:** **confirma** a opção adotada; nenhum CR.

## Pontos a confirmar

Dos arquivos locais `.claude/requisitos.md` e `CLAUDE.md` (fora do Git). Cada resposta virou uma DEC nova, já decidida; o único ponto que segue aberto está no [índice das decisões](README.md#pontos-a-confirmar-ainda-abertos).

| Ponto | Pergunta | Adotado hoje | Resposta do professor • Data |
|---|---|---|---|
| `.claude/requisitos.md` 4 | Outros diagramas (sequência, C4, DER, raias) serão exigidos? | Só casos de uso e o fluxo de decisão de UC-04. | A critério do grupo: o professor não exigiu outros diagramas; o grupo decidiu fazer o DER ([DEC-19](DEC-19.md), DOC-10) • 06/11/2026 |
| `.claude/requisitos.md` 5 | Exceções numeradas com `E` ou tudo com `A`? | `A` para alternativas e `E` para exceções. | "Pode ser assim sim." ([DEC-14](DEC-14.md)) • 06/11/2026 |
| `.claude/requisitos.md` 6 | Campos do "Index Card padrão"; o custo em semanas aceita fração? | Nove campos e fração (ex.: 1,2). | "Sim, pode." ([DEC-18](DEC-18.md)) • 06/11/2026 |
| `.claude/requisitos.md` 10 | A convenção de versão 0.1 → 0.2 → 1.0 vale? | Adotada. | "Serve sim, e deve ser assim mesmo." ([DEC-17](DEC-17.md)) • 06/11/2026 |
| `.claude/requisitos.md` 13 | A rastreabilidade deve ir até o código? | Sim, como colunas complementares da matriz. | "Conta sim." ([DEC-16](DEC-16.md)) • 06/11/2026 |
| `CLAUDE.md` 4 | O grupo atende às regras das duas disciplinas? | Mesmo grupo e recorte nas duas. | Sem resposta (não perguntado; o registro do grupo já foi feito até 16/10/2026) • — |
| `CLAUDE.md` 5 | Dado/Quando/Então atende como formato de critério de aceite? | Adotado nos 156 CAs. | "Atende sim, e é dessa forma." ([DEC-15](DEC-15.md)) • 06/11/2026 |

## Também respondido na aula: entrega e apresentação

Fora da pauta; cada resposta virou uma DEC nova, já decidida.

| Assunto | Resposta do professor | DEC |
|---|---|---|
| Entrega dos documentos de Requisitos | "Os documentos de Requisitos vão ser uma entrega separada"; pediu outros documentos, a detalhar depois. | [DEC-20](DEC-20.md) |
| Capa do `modelagem.pdf` | (sem as palavras exatas) a capa não entra nas 6 páginas e não precisa ser formal: só o título e os nomes. | [DEC-21](DEC-21.md) |
| Modelo do `contribuicoes.pdf` | (sem as palavras exatas) não há modelo. | [DEC-22](DEC-22.md) |
| Apresentação | (sem as palavras exatas) em aula, com o notebook do grupo, mostrando o sistema funcionando, em até 10 minutos. | [DEC-23](DEC-23.md) |

## Resultado

| DEC ou ponto | Conclusão | Estado | CR | Tarefa |
|---|---|---|---|---|
| [DEC-13](DEC-13.md) · Mudança de situação × horário | Muda | Decidida | [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md) | RES-11 |
| [DEC-05](DEC-05.md) · Histórico só com mudanças efetivas | Muda | Decidida | [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md) | RES-12 |
| [DEC-07](DEC-07.md) · Valores das regras de agenda | Muda | Decidida | [CR-03](../mudancas/CR-03-horario-por-espaco.md) | ESP-07 |
| [DEC-06](DEC-06.md) · Reservas de um espaço desativado | Confirma | Decidida | — | — |
| [DEC-09](DEC-09.md) · Formato da matrícula | Muda | Decidida | [CR-04](../mudancas/CR-04-matricula-so-digitos.md) | AUT-12 |
| [DEC-10](DEC-10.md) · Nome de espaço único | Confirma | Decidida | — | — |
| [DEC-11](DEC-11.md) · Períodos ocupados na agenda do dia | Confirma | Decidida | — | — |
| [DEC-08](DEC-08.md) · Cobertura-alvo dos testes | Confirma | Decidida | — | — |
| [DEC-12](DEC-12.md) · Metas de desempenho | Confirma | Decidida | — | — |
| Ponto 5 de `.claude/requisitos.md` · `A` e `E` | Confirma | Decidida ([DEC-14](DEC-14.md)) | — | — |
| Ponto 5 do `CLAUDE.md` · Dado/Quando/Então | Confirma | Decidida ([DEC-15](DEC-15.md)) | — | — |
| Ponto 13 de `.claude/requisitos.md` · rastreabilidade até o código | Confirma | Decidida ([DEC-16](DEC-16.md)) | — | — |
| Ponto 10 de `.claude/requisitos.md` · convenção de versão | Confirma | Decidida ([DEC-17](DEC-17.md)) | — | — |
| Ponto 6 de `.claude/requisitos.md` · Index Card e fração | Confirma | Decidida ([DEC-18](DEC-18.md)) | — | — |
| Ponto 4 de `.claude/requisitos.md` · outros diagramas | A critério do grupo (DER) | Decidida ([DEC-19](DEC-19.md)) | — | DOC-10 |
| Ponto 4 do `CLAUDE.md` · grupo nas duas disciplinas | Sem resposta (não perguntado) | Aberto | — | — |
| Entrega dos documentos de Requisitos | Entrega separada | Decidida ([DEC-20](DEC-20.md)) | — | REQ-08 |
| Capa do `modelagem.pdf` | Fora das 6 páginas; só título e nomes | Decidida ([DEC-21](DEC-21.md)) | — | DOC-04 |
| Modelo do `contribuicoes.pdf` | Sem modelo | Decidida ([DEC-22](DEC-22.md)) | — | DOC-06 |
| Apresentação | Em aula, notebook do grupo, até 10 minutos | Decidida ([DEC-23](DEC-23.md)) | — | — |
