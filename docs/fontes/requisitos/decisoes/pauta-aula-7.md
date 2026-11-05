# Pauta para o professor — Aula 7 (06/11/2026)

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **PAU-01 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: a definir • Aprovador: a definir | `docs/fontes/requisitos/decisoes/pauta-aula-7.md` |

Perguntas que o grupo leva à Aula 7: as DECs com prazo em 06/11/2026 e os pontos a confirmar ainda abertos. Cada item traz a opção que o código já implementa, o porquê e o que muda se a resposta for outra, com o número de critérios (CA) e testes de aceite (TA) a rever, tirado do [mapa de impacto](../rastreabilidade/impacto-por-dec.md) (o script confere esses números). Toda resposta diferente da opção adotada é **mudança comportamental**: vira um [CR](../mudancas/modelo-cr.md), e a baseline vigente continua valendo até a aprovação. As respostas são passadas para a DEC (estado, resposta e data) no mesmo dia.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Criação: DEC-05, 06, 07, 09, 10, 11 e 13; DEC-08 e DEC-12 "se houver tempo"; pontos a confirmar abertos (REQ-06). Sem aprovação. |

## Decisões com prazo em 06/11/2026

### <a id="dec-13"></a>DEC-13 — Mudança de situação × horário da reserva

- **Pergunta:** concluir, confirmar, recusar e cancelar devem depender do horário da reserva (e o que acontece com um pedido que ninguém decidiu até a data passar)?
- **Adotado:** não dependem; valem a tabela de transições, o perfil e o motivo. Um pedido não decidido continua ocupando o horário. Por quê: nada no enunciado fixa essas regras, e elas dependem do uso real da instituição.
- **Se a resposta for outra:** 21 CAs e 21 TAs em 9 histórias; RF-16 a RF-21, exceções novas no UC-10 e as ações disponíveis em cada reserva ([impacto](../rastreabilidade/impacto-por-dec.md#dec-13)).
- Resposta do professor: ___ • Data: ___

### <a id="dec-05"></a>DEC-05 — Histórico só com mudanças efetivas

- **Pergunta:** uma tentativa recusada de mudar a situação precisa ficar registrada? Onde e para quem?
- **Adotado:** não; o histórico guarda só a criação e as mudanças aceitas. Por quê: uma recusa não muda a reserva. Difere do modelo de aceite da aula ("tentativa registrada com data, ator e resultado").
- **Se a resposta for outra:** 10 CAs e 10 TAs em 6 histórias; RF-22, RNF-R02 e o registro das recusas no histórico ou num log ([impacto](../rastreabilidade/impacto-por-dec.md#dec-05)).
- Resposta do professor: ___ • Data: ___

### <a id="dec-07"></a>DEC-07 — Valores das regras de agenda

- **Pergunta:** quais são o horário de funcionamento, a duração mínima e máxima e a antecedência máxima? São iguais para todos os espaços e dias?
- **Adotado:** 07:00 às 22:00, de 30 min a 3 h, até 30 dias, iguais para todos. Por quê: sem cliente real (P-01), os valores são do grupo e ficam em constantes únicas.
- **Se a resposta for outra:** 10 CAs e 10 TAs em 2 histórias; RF-11.5, RF-28, RF-30, RF-31 e os testes de borda; por espaço ou por dia, o cadastro de espaços também muda ([impacto](../rastreabilidade/impacto-por-dec.md#dec-07)).
- Resposta do professor: ___ • Data: ___

### <a id="dec-06"></a>DEC-06 — Reservas de um espaço desativado

- **Pergunta:** quando o Gestor desativa um espaço, o que acontece com as reservas que ele já tem?
- **Adotado:** continuam valendo; só novos pedidos ficam bloqueados, e o Gestor cancela uma a uma, se precisar. Por quê: preserva decisões e histórico; cancelar em cascata faria o cadastro de espaços conhecer as reservas.
- **Se a resposta for outra:** 14 CAs e 14 TAs em 4 histórias; RF-06, RF-07, RF-08, RF-11.3, RF-20 e RNF-R05 ([impacto](../rastreabilidade/impacto-por-dec.md#dec-06)).
- Resposta do professor: ___ • Data: ___

### <a id="dec-09"></a>DEC-09 — Formato da matrícula

- **Pergunta:** qual é o formato real da matrícula, e ela precisa ser conferida com a instituição?
- **Adotado:** obrigatória, única, até 20 caracteres, sem espaços, sem conferência. Por quê: o formato não foi informado; a regra está isolada numa função.
- **Se a resposta for outra:** 5 CAs e 5 TAs em 2 histórias; RF-32 e RF-32.1 e os dados de exemplo ([impacto](../rastreabilidade/impacto-por-dec.md#dec-09)).
- Resposta do professor: ___ • Data: ___

### <a id="dec-10"></a>DEC-10 — Nome de espaço único

- **Pergunta:** dois espaços podem ter o mesmo nome? "Ginásio A" e "ginásio a" são o mesmo?
- **Adotado:** único, sem diferenciar maiúsculas de minúsculas. Por quê: nomes repetidos confundiriam quem pede e quem decide.
- **Se a resposta for outra:** 6 CAs e 6 TAs em 2 histórias; RF-05.2, RF-06.2 e a restrição do banco ([impacto](../rastreabilidade/impacto-por-dec.md#dec-10)).
- Resposta do professor: ___ • Data: ___

### <a id="dec-11"></a>DEC-11 — Períodos ocupados por outras pessoas na agenda do dia

- **Pergunta:** o Solicitante pode ver, antes de pedir, os períodos ocupados por reservas de outras pessoas? Com quais dados?
- **Adotado:** sim, só início, término e situação, nunca quem pediu nem para quê. Por quê: é o mesmo dado que a recusa por conflito já mostrava, só que antes do pedido.
- **Se a resposta for outra:** 5 CAs e 5 TAs em 1 história; RF-29 e RNF-F06 ([impacto](../rastreabilidade/impacto-por-dec.md#dec-11)).
- Resposta do professor: ___ • Data: ___

## Se houver tempo (prazo 13/11/2026)

### <a id="dec-08"></a>DEC-08 — Cobertura-alvo dos testes

- **Pergunta:** que meta de testes o grupo adota, já que a disciplina não exige testes?
- **Adotado:** 100% de linhas e ramos em `domain` e `application` de espaços e reservas; 99% no total. Por quê: as regras vivem nessas camadas.
- **Se a resposta for outra:** 0 CAs e 0 TAs; só a meta do RNF-S03 ([impacto](../rastreabilidade/impacto-por-dec.md#dec-08)).
- Resposta do professor: ___ • Data: ___

### <a id="dec-12"></a>DEC-12 — Metas de desempenho

- **Pergunta:** em quanto tempo a consulta de reservas e a agenda do dia precisam responder, e com quantas reservas?
- **Adotado:** com 1.000 reservas, p95 até 1 s na consulta e até 500 ms na agenda (medido: 378 ms e 7 ms). Por quê: nenhum documento fixa tempo, e um RNF precisa de valor mensurável.
- **Se a resposta for outra:** 0 CAs e 0 TAs; as metas do RNF-P01 e do RNF-P02 e, com carga maior, a paginação da [L-05](../requisitos/srs.md#l-05) ([impacto](../rastreabilidade/impacto-por-dec.md#dec-12)).
- Resposta do professor: ___ • Data: ___

## Pontos a confirmar ainda abertos

Dos arquivos locais `.claude/requisitos.md` e `CLAUDE.md` (fora do Git); o que cada um afeta está no [índice das decisões](README.md#pontos-a-confirmar-ainda-abertos). Uma resposta vira uma DEC nova.

| Ponto | Pergunta | Adotado hoje | Resposta do professor • Data |
|---|---|---|---|
| `.claude/requisitos.md` 4 | Outros diagramas (sequência, C4, DER, raias) serão exigidos? | Só casos de uso e o fluxo de decisão de UC-04. | ___ • ___ |
| `.claude/requisitos.md` 5 | Exceções numeradas com `E` ou tudo com `A`? | `A` para alternativas e `E` para exceções. | ___ • ___ |
| `.claude/requisitos.md` 6 | Campos do "Index Card padrão"; o custo em semanas aceita fração? | Nove campos e fração (ex.: 1,2). | ___ • ___ |
| `.claude/requisitos.md` 10 | A convenção de versão 0.1 → 0.2 → 1.0 vale? | Adotada. | ___ • ___ |
| `.claude/requisitos.md` 13 | A rastreabilidade deve ir até o código? | Sim, como colunas complementares da matriz. | ___ • ___ |
| `CLAUDE.md` 4 | O grupo atende às regras das duas disciplinas? | Mesmo grupo e recorte nas duas. | ___ • ___ |
| `CLAUDE.md` 5 | Dado/Quando/Então atende como formato de critério de aceite? | Adotado nos 156 CAs. | ___ • ___ |
