# CR-10 — Gestor consulta o ranking de espaços mais reservados

| Identificação | Responsabilidade |
|---|---|
| **CR-10 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

Pedido de mudança aberto na tarefa RDS-12, no [modelo de CR](modelo-cr.md), porque a [DEC-28](../decisoes/DEC-28.md) (itens e e f) diz que o ranking de espaços é opcional e, sendo funcionalidade nova, fora do que a decisão decide, exige um CR e um RF próprios. A especificação entregue em 13/11/2026 não foi alterada.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 25/11/2026 | Max Zimmermann dos Reis | Abertura, aplicação na fonte oficial e implementação na tarefa RDS-12, no mesmo PR. Sem aprovação. |

## 1. Solicitação

| Campo | Conteúdo |
|---|---|
| **Motivo** | Hoje o Gestor só descobre quais espaços são mais usados contando, à mão, as reservas da lista; não há uma visão de relance de onde está a procura e de onde sobra horário. |
| **Solicitante** | Max Zimmermann dos Reis (grupo). |
| **Responsável** | Max Zimmermann dos Reis. |
| **Estado** | **Implementado** (25/11/2026, RDS-12: especificação e código no mesmo PR) |
| **Origem** | [DEC-28](../decisoes/DEC-28.md), itens e e f; tarefa RDS-12. |
| **Baseline vigente** | [Conecta Campus — Requisitos 1.0 (candidata)](../baselines/conecta-campus-1.0-candidata.md), até a nova ser aprovada. |

## 2. Classificação (A4·s17)

- [ ] **Editorial:** corrige o texto e mantém a obrigação; registra-se a correção.
- [x] **Comportamental:** o sistema ganha uma consulta nova e restrita ao Gestor (o ranking dos espaços com mais reservas que contam), com recusa de quem não é Gestor e de limite inválido.

## 3. Mapa de impacto

| Elo | Afetados | Muda o quê |
|---|---|---|
| NS | [NS-08](../visao.md#ns-08) | Passa a cobrir também o ranking de espaços; nenhuma necessidade nova. |
| RF / RNF | [RF-45](../requisitos/rf-reservas.md#rf-45), [RF-45.1](../requisitos/rf-reservas.md#rf-45-1) (novos) | Nenhum RF existente muda; nenhum RNF muda. |
| UC (passo, alternativa ou exceção) | [UC-25](../casos-de-uso/README.md#uc-25) (novo) | O [UC-07](../casos-de-uso/README.md#uc-07) (consultar reservas) e o [UC-24](../casos-de-uso/README.md#uc-24) (fila e contagens) continuam como estão. |
| US / CA | [US-24](../historias/US-24-consultar-o-ranking-de-espacos.md) (nova, CA-01 a CA-10) | História nova. |
| TA | TA-217 a TA-226 | Novos, ao fim da numeração; nenhum TA existente é renumerado. |
| Endpoint ou tela (complementar) | `GET /api/reservas/ranking-de-espacos/?limite=` | Novo. Sem tela nesta mudança. |
| Código (complementar) | `ConsultarRankingDeEspacos`, `SITUACOES_QUE_CONTAM_NO_RANKING`, `RepositorioReservasDjango.contar_por_espaco_que_contam_no_ranking`, `RankingDeEspacosView` | Novos. |
| Matriz de acesso | `reservas:ranking_de_espacos` | Uma linha nova: anônimo 401, Solicitante 403, Gestor 200. |
| DEC | [DEC-28](../decisoes/DEC-28.md) (só o histórico) | A decisão técnica não muda. |

## 4. Diferença

| Artefato | Antes | Depois |
|---|---|---|
| Consulta do Gestor | A lista de reservas ([RF-12](../requisitos/rf-reservas.md#rf-12)), a fila de pendentes e a contagem por situação ([RF-44](../requisitos/rf-reservas.md#rf-44)) | Também o ranking dos espaços com mais reservas que contam |
| Glossário | — | Ranking de espaços; Reserva que conta no ranking |
| Matriz de acesso | Duas rotas de leitura só do Gestor (fila e contagem) | Mais `reservas:ranking_de_espacos`, só do Gestor |

## 5. Critérios de aceite

- **Dado** um Gestor identificado e espaços com quantidades diferentes de reservas Confirmadas ou Concluídas **Quando** ele pede o ranking **Então** vê os espaços do que tem mais para o que tem menos, no empate pelo menor código do espaço, com posição, código, nome e total, até o limite pedido (1 a 20; cinco se não informado) (US-24 · CA-01, CA-02 e CA-06; TA-217, TA-218 e TA-222).
- **Dado** uma reserva Confirmada que conta no total do espaço **Quando** ela é concluída ou cancelada **Então** continua contando uma só vez ao ser concluída e deixa de contar ao ser cancelada, sem nada a refazer; reservas Solicitadas, Recusadas e Canceladas nunca contam (US-24 · CA-03, CA-04 e CA-05; TA-219, TA-220 e TA-221).
- **Dado** um Solicitante, ou alguém sem identificação **Quando** pede o ranking **Então** a consulta é recusada, sem mostrar espaço nem número (US-24 · CA-10; TA-226); e o resultado é o mesmo em qualquer condição de funcionamento do sistema (US-24 · CA-08; TA-224).

## 6. Limites e regressão

- **Limites desta mudança:** o ranking é do tempo todo, sem filtro de período; é só informação de apoio e nunca decide nada (nem a reserva, nem a agenda, nem a permissão); o total pode estar um instante atrás do cadastro quando uma mudança de situação ainda está sendo registrada, e o nome do espaço vem sempre do cadastro; não há tela.
- Rever US-10, US-11 e US-12 (consulta, detalhe e histórico): a lista `GET /api/reservas/`, o detalhe, o histórico e o formato das respostas não mudam.
- Rever US-23 (fila e contagens): a fila de pendentes e a contagem por situação continuam iguais e não dependem do ranking.
- Rever US-06 (agenda do dia) e US-14 a US-16 e US-20 (decidir): a agenda, as regras de situação, a permissão e o histórico não mudam; o ranking só lê.
- Cenário que não deve mudar: o Solicitante vê só as próprias reservas na lista, e o ranking, que reúne as de todos, não lhe é aberto ([RF-23](../requisitos/rf-reservas.md#rf-23), [RF-13](../requisitos/rf-reservas.md#rf-13)).

## 7. Decisão

| Campo | Conteúdo |
|---|---|
| **Decisão** | Aceita pelo grupo e aplicada na especificação e no código, na tarefa RDS-12. |
| **Quem decidiu e quando** | Grupo, em 25/11/2026 (previsto nos itens e e f da [DEC-28](../decisoes/DEC-28.md)). |
| **Justificativa** | É uma leitura nova, sem escrita nem regra de negócio nova além de dizer quais situações contam; não afeta as seis funcionalidades mínimas e é fácil de reverter (uma rota, um caso de uso e uma projeção isolados). |
| **Referência candidata** | Manifesto da [baseline candidata](../baselines/conecta-campus-1.0-candidata.md), regerado no mesmo PR. |
