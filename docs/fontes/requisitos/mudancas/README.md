# Pedidos de mudança

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **IND-03 • 0.1 • Rascunho** (índice dos pedidos de mudança) | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/mudancas/` |

CR-xx, um arquivo por pedido, com solicitação (motivo, solicitante, responsável, estado), classificação (editorial ou comportamental), mapa de impacto (artefatos afetados e regressão), trecho antes e depois, critérios de aceite e decisão.

Usada depois da primeira baseline; o fluxo está no [README da fonte oficial](../README.md#como-propor-uma-mudança).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Criação (REQ-01; data do commit, o arquivo não tinha histórico). Sem aprovação. |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Cabeçalho completado (REQ-06). Índice com o [modelo de CR](modelo-cr.md), cujo mapa de impacto sai da [matriz de rastreabilidade](../rastreabilidade/README.md). Sem aprovação. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | CR-01 a CR-04 abertos a partir das respostas da Aula 7 que mudam o comportamento (DEC-13, DEC-05, DEC-07 e DEC-09), aprovados pelo professor e aguardando implementação (GES-02). Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | CR-05 aberto na REQ-12 (artefatos de ator misto da DEC-25), no estado proposto, aguardando decisão na REQ-13. Os CR-01 a CR-04 não mudaram. Sem aprovação. |

## Índice

| ID | Assunto | Origem | Estado | Tarefa que implementa | Arquivo |
|---|---|---|---|---|---|
| — | Modelo de CR (não é um pedido) | — | — | — | [modelo-cr.md](modelo-cr.md) |
| CR-01 | Mudança de situação em relação ao horário da reserva | [DEC-13](../decisoes/DEC-13.md) | Aprovado, aguardando implementação | RES-11 | [CR-01](CR-01-situacao-e-horario-da-reserva.md) |
| CR-02 | Tentativas recusadas no histórico da reserva | [DEC-05](../decisoes/DEC-05.md) | Aprovado, aguardando implementação | RES-12 | [CR-02](CR-02-tentativas-recusadas-no-historico.md) |
| CR-03 | Horário de funcionamento por espaço e duração sugerida | [DEC-07](../decisoes/DEC-07.md) | Aprovado, aguardando implementação | ESP-07 | [CR-03](CR-03-horario-por-espaco.md) |
| CR-04 | Matrícula só com dígitos | [DEC-09](../decisoes/DEC-09.md) | Aprovado, aguardando implementação | AUT-12 | [CR-04](CR-04-matricula-so-digitos.md) |
| CR-05 | Atendente responsável e Gestor do serviço nos artefatos de ator misto (US-13, US-12, US-03) | [DEC-25](../decisoes/DEC-25.md) | Proposto | REQ-13 | [CR-05](CR-05-atendente-e-gestor-nos-artefatos-mistos.md) |

Os quatro primeiros nascem das respostas da [Aula 7](../decisoes/pauta-aula-7.md#resultado) que mudam o comportamento implementado. O CR-05 nasce da [DEC-25](../decisoes/DEC-25.md) (REQ-12) e está proposto. Nenhum CR muda RF, UC, CA nem código: quem o aplica é a tarefa de implementação, no mesmo PR do código, e até lá o sistema e os requisitos continuam descrevendo o comportamento anterior.
