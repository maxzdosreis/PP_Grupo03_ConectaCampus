# Entrevista ENT-04 — Atendente responsável, simulada

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **ENT-04 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/levantamento/entrevistas/ENT-04-atendente-responsavel-simulada.md` |

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Criação como entrevista simulada (REQ-09). Sem aprovação. |

## 1. Identificação

| Campo | Conteúdo |
|---|---|
| **ID** | ENT-04 |
| **Data** | Não se aplica (simulada) |
| **Duração** | Não se aplica |
| **Forma** | Simulada, sem encontro com pessoa real |
| **Roteiro usado** | [ROT-03](ROT-03-atendente-responsavel.md) |
| **Entrevistador** | Max Zimmermann dos Reis |
| **Perfil do entrevistado** | servidor do setor que atende os pedidos de uso dos espaços há mais de um ano |
| **Consentimento para anotar** | Não se aplica |

## 2. Respostas

| P | Resposta (simulada) |
|---|---|
| P01 | Os pedidos chegam por telefone, mensagem e pessoalmente. Anota numa agenda de papel e responde em um a três dias. |
| P02 | Aceita quando o horário está livre e o uso é compatível com o espaço. Nega quando o horário já está comprometido ou há atividade da instituição. Quando nega, explica o motivo à pessoa. |
| P03 | Já chegaram dois pedidos para o mesmo horário. Ficou com quem pediu primeiro, e avisou a outra pessoa por telefone. |
| P04 | sem anotação |
| P05 | Marca na agenda, depois do uso, que ele ocorreu. Nem sempre faz isso no mesmo dia. |
| P06 | Quando alguém não aparece, o horário fica vazio e, em geral, não se faz nada. Às vezes anota na agenda. |
| P07 | Cada espaço tem horário próprio: a quadra externa fecha mais cedo por causa da iluminação, e o ginásio funciona até mais tarde. Nos fins de semana o funcionamento é reduzido, e em feriados é fechado. |
| P08 | Quem define é a coordenação do setor. Quando uma regra muda, os atendentes são avisados por mensagem. |
| P09 | sem anotação |
| P10 | sem anotação |
| P11 | O que mais consome tempo é responder repetidamente quais horários estão livres. |

## 3. Perguntas e assuntos novos

- Mencionou que atividades da instituição têm prioridade sobre pedidos de pessoas, o que pode derrubar um uso já aceito.

## 4. Observações do entrevistador

- Entrevista simulada: não houve conversa, tempo, consentimento nem encontro com pessoa real.

## 5. Achados preliminares (interpretação do entrevistador)

| # | Achado | De onde saiu | Liga-se a |
|---|---|---|---|
| A1 | Hoje o pedido é anotado em papel, sem histórico, com resposta em dias. | P01 | Confirma o problema da Visão, seção 1; NS-09, NS-12 |
| A2 | Aceitar ou negar depende do horário livre; a recusa vem com motivo. | P02 | Confirma NS-09; motivo de recusa (RF-18) |
| A3 | Em pedidos simultâneos, vale quem pediu primeiro. | P03 | Confirma NS-04; RF-11.4 |
| A4 | O registro de que o uso aconteceu é feito depois do uso. | P05 | Confirma [DEC-13](../../decisoes/DEC-13.md) (concluir só depois do término) |
| A5 | Não comparecimento não gera ação, só às vezes uma anotação. | P06 | Possível necessidade nova (registro de não comparecimento; controle de presença é fora do escopo) |
| A6 | Cada espaço tem horário próprio, e há restrições em fins de semana e feriados. | P07 | Confirma o horário por espaço da [DEC-07](../../decisoes/DEC-07.md); contesta a premissa P-04 em parte: fins de semana e feriados seguem fora do escopo |
| A7 | As regras são definidas pela coordenação do setor. | P08 | Confirma o papel do Gestor do serviço (REQ-12) e o cliente × usuário da Visão |
| A8 | Atividades da instituição podem derrubar um uso aceito. | Assunto novo | Toca a [DEC-06](../../decisoes/DEC-06.md); possível necessidade nova (bloqueio de períodos; fora do escopo) |
| A9 | A pergunta mais repetida é "quais horários estão livres". | P11 | Confirma NS-05 |
