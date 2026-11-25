# CR-09 — Gestor consulta a fila de pendentes e as contagens por situação

| Identificação | Responsabilidade |
|---|---|
| **CR-09 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

Pedido de mudança aberto na tarefa RDS-08, no [modelo de CR](modelo-cr.md), porque a [DEC-28](../decisoes/DEC-28.md) (item f) diz que a consulta do Gestor à fila de pendentes e às contagens é funcionalidade nova, fora do que a decisão decide, e exige um CR e um RF próprios. A especificação entregue em 13/11/2026 não foi alterada.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 25/11/2026 | Max Zimmermann dos Reis | Abertura, aplicação na fonte oficial e implementação na tarefa RDS-08, no mesmo PR. Sem aprovação. |

## 1. Solicitação

| Campo | Conteúdo |
|---|---|
| **Motivo** | Hoje o Gestor só acha o que espera a decisão dele filtrando a lista de reservas por situação, ordenada pelo horário de uso, e não vê de relance quantas reservas há em cada situação. |
| **Solicitante** | Max Zimmermann dos Reis (grupo). |
| **Responsável** | Max Zimmermann dos Reis. |
| **Estado** | **Implementado** (25/11/2026, RDS-08: especificação e código no mesmo PR) |
| **Origem** | [DEC-28](../decisoes/DEC-28.md), item f; tarefa RDS-08. |
| **Baseline vigente** | [Conecta Campus — Requisitos 1.0 (candidata)](../baselines/conecta-campus-1.0-candidata.md), até a nova ser aprovada. |

## 2. Classificação (A4·s17)

- [ ] **Editorial:** corrige o texto e mantém a obrigação; registra-se a correção.
- [x] **Comportamental:** o sistema ganha duas consultas novas e restritas ao Gestor (a fila de reservas pendentes, em ordem de solicitação, e a contagem de reservas por situação), com recusa de quem não é Gestor e de página inválida.

## 3. Mapa de impacto

| Elo | Afetados | Muda o quê |
|---|---|---|
| NS | [NS-08](../visao.md#ns-08) | Passa a cobrir também a fila de pendentes e a contagem por situação; nenhuma necessidade nova. A [NS-09](../visao.md#ns-09) (decidir) é o uso da fila. |
| RF / RNF | [RF-44](../requisitos/rf-reservas.md#rf-44), [RF-44.1](../requisitos/rf-reservas.md#rf-44-1), [RF-44.2](../requisitos/rf-reservas.md#rf-44-2) (novos) | Nenhum RF existente muda; nenhum RNF muda. |
| UC (passo, alternativa ou exceção) | [UC-24](../casos-de-uso/README.md#uc-24) (novo) | O [UC-07](../casos-de-uso/README.md#uc-07) (consultar reservas) continua como está. |
| US / CA | [US-23](../historias/US-23-consultar-a-fila-de-pendentes.md) (nova, CA-01 a CA-08) | História nova. |
| TA | TA-209 a TA-216 | Novos, ao fim da numeração; nenhum TA existente é renumerado. |
| Endpoint ou tela (complementar) | `GET /api/reservas/pendentes/`; `GET /api/reservas/contagem-por-situacao/` | Novos. Sem tela nesta mudança. |
| Código (complementar) | `ConsultarFilaDePendentes`, `ContarReservasPorSituacao`, `RepositorioReservasDjango.listar_pendentes`, `RepositorioReservasDjango.contar_por_situacao`, `FilaDePendentesView`, `ContagemPorSituacaoView` | Novos. |
| Matriz de acesso | `reservas:pendentes`, `reservas:contagem_por_situacao` | Duas linhas novas: anônimo 401, Solicitante 403, Gestor 200. |
| DEC | [DEC-28](../decisoes/DEC-28.md) (só o histórico e a lista de artefatos) | A decisão técnica não muda. |

## 4. Diferença

| Artefato | Antes | Depois |
|---|---|---|
| Consulta do Gestor | Só a lista de reservas com filtros ([RF-12](../requisitos/rf-reservas.md#rf-12)), ordenada pelo início do horário | Também a fila das Solicitadas em ordem de solicitação e a contagem por situação |
| Glossário | — | Fila de pendentes; Contagem por situação |
| Matriz de acesso | Nenhuma rota de leitura de reservas só do Gestor | `reservas:pendentes` e `reservas:contagem_por_situacao`, só do Gestor |

## 5. Critérios de aceite

- **Dado** um Gestor identificado e reservas Solicitadas pedidas em momentos diferentes **Quando** ele pede a fila de pendentes **Então** vê só as Solicitadas, da mais antiga para a mais nova, com o total (US-23 · CA-01; TA-209).
- **Dado** um Solicitante, ou alguém sem identificação **Quando** pede a fila ou a contagem **Então** a consulta é recusada, sem mostrar reserva nem número (US-23 · CA-08; TA-216).
- **Dado** um Gestor identificado **Quando** uma reserva pendente é confirmada, recusada ou cancelada e ele consulta de novo **Então** ela sai da fila e a contagem muda, sem nada a refazer, e o resultado é o mesmo em qualquer condição de funcionamento do sistema (US-23 · CA-03 e CA-06; TA-211 e TA-214).

## 6. Regressão

- Rever US-10, US-11 e US-12 (consulta, detalhe e histórico): a lista `GET /api/reservas/`, o detalhe, o histórico e o formato das respostas não mudam.
- Rever US-06 (agenda do dia): a agenda continua igual e não depende da fila.
- Rever US-14 a US-16 e US-20 (decidir): as regras de situação, permissão e histórico não mudam; a fila só lê.
- Cenário que não deve mudar: o Solicitante vê só as próprias reservas na lista, e a fila e a contagem, que mostram as de todos, não lhe são abertas ([RF-23](../requisitos/rf-reservas.md#rf-23), [RF-13](../requisitos/rf-reservas.md#rf-13)).

## 7. Decisão

| Campo | Conteúdo |
|---|---|
| **Decisão** | Aceita pelo grupo e aplicada na especificação e no código, na tarefa RDS-08. |
| **Quem decidiu e quando** | Grupo, em 25/11/2026 (previsto no item f da [DEC-28](../decisoes/DEC-28.md)). |
| **Justificativa** | É uma leitura nova, sem escrita nem regra de negócio nova: usa as situações e a ordem já existentes e não afeta as seis funcionalidades mínimas. |
| **Referência candidata** | Manifesto da [baseline candidata](../baselines/conecta-campus-1.0-candidata.md), regerado no mesmo PR. |
