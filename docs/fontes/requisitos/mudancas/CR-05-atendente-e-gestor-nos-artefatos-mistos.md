# CR-05 — Atendente responsável e Gestor do serviço nos artefatos de ator misto

| Identificação | Responsabilidade |
|---|---|
| **CR-05 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha (aprovador da fonte oficial) |

Pedido de mudança aberto na REQ-12, no [modelo de CR](modelo-cr.md), para os artefatos que a separação entre Atendente responsável e Gestor do serviço ([DEC-25](../decisoes/DEC-25.md)) deixou **sem rótulo único**: eles falam de mais de um papel ao mesmo tempo, então trocar o nome do ator mudaria a história ou os critérios, e não só o texto. Os artefatos de um papel só foram ajustados na própria REQ-12 (mudança editorial). Este CR **não** muda RF, UC, CA, TA nem código; fica **proposto**, para decisão do grupo na REQ-13.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Abertura a partir da DEC-25 (REQ-12). Estado: proposto, aguardando decisão na REQ-13. Sem aprovação. |

## 1. Solicitação

| Campo | Conteúdo |
|---|---|
| **Motivo** | A [DEC-25](../decisoes/DEC-25.md) separa o Atendente responsável (opera as reservas) do Gestor do serviço (mantém os espaços e as regras). Três histórias e um caso de uso reúnem os dois papéis, ou um papel e o perfil, numa só frase de ator. |
| **Solicitante** | Max Zimmermann dos Reis (grupo). |
| **Responsável** | Max Zimmermann dos Reis (análise); a atualização é da REQ-13. |
| **Estado** | **Proposto** |
| **Origem** | [DEC-25](../decisoes/DEC-25.md); enunciado §2; [síntese do levantamento](../levantamento/sintese-do-levantamento.md) (ACH-22). |
| **Baseline vigente** | [Conecta Campus — Requisitos 1.0 (candidata)](../baselines/conecta-campus-1.0-candidata.md), até a nova ser aprovada. |

## 2. Classificação (A4·s17)

- [ ] **Editorial:** corrige o texto e mantém a obrigação; registra-se a correção.
- [x] **Comportamental (da especificação):** divide uma história em duas e muda o ator de critérios de aceite. O comportamento do sistema **não** muda (um perfil só, a [DEC-25](../decisoes/DEC-25.md)), mas o escopo das histórias e dos testes de aceite muda, por isso não é editorial.

## 3. Mapa de impacto

| Elo | Afetados | Muda o quê |
|---|---|---|
| NS | [NS-09](../visao.md#ns-09), [NS-12](../visao.md#ns-12) | Nada no texto; só a coluna de ator, se o grupo quiser distinguir. |
| RF / RNF | [RF-12](../requisitos/rf-reservas.md#rf-12), [RF-17](../requisitos/rf-reservas.md#rf-17) a [RF-20](../requisitos/rf-reservas.md#rf-20) | Opcional: enunciados passam a dizer "Atendente responsável" em vez do perfil Gestor. RF-04 a RF-09 diriam "Gestor do serviço". Nenhum comportamento muda. |
| UC (passo, alternativa ou exceção) | [UC-10](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md) (ator primário "depende do filho"), [UC-11](../casos-de-uso/README.md#uc-11), [UC-08](../casos-de-uso/README.md#uc-08), [UC-09](../casos-de-uso/README.md#uc-09) | O ator primário de UC-11 reúne o Solicitante e o Atendente responsável; UC-08 e UC-09 são do Solicitante "e do Gestor, por herança". Decidir se o Gestor do serviço também os herda como papel. |
| US / CA | [US-13](../historias/US-13-cancelar-uma-reserva.md), [US-12](../historias/US-12-ver-detalhe-e-historico.md), [US-03](../historias/US-03-manter-e-encerrar-a-sessao.md) | US-13: duas metas (o Solicitante cancela a própria; o Atendente cancela qualquer) numa só história, a dividir. US-12 e US-03: "Solicitante (ou Gestor)" e "Solicitante ou Gestor", a reescrever com os três papéis. Os CAs de acesso citam "o Gestor" nos Dado/Quando. |
| TA | Os TAs dos CAs de [US-13](../historias/US-13-cancelar-uma-reserva.md), [US-12](../historias/US-12-ver-detalhe-e-historico.md) e [US-03](../historias/US-03-manter-e-encerrar-a-sessao.md) | Renumeração se US-13 for dividida; os testes citados no código não mudam. |
| Endpoint ou tela (complementar) | Nenhum | O sistema tem um perfil só. |
| Código (complementar) | Nenhum | `PerfilUsuario.GESTOR` e `PapelDoAtor.GESTOR` continuam. |
| DEC | [DEC-25](../decisoes/DEC-25.md), [DEC-04](../decisoes/DEC-04.md) | Nenhuma muda; a DEC-04 segue válida para o perfil. |

## 4. Diferença

| Artefato | Antes | Depois |
|---|---|---|
| US-13 | Uma história: "Como Solicitante, quero cancelar uma reserva minha… e, como Gestor, quero cancelar qualquer reserva…". | Duas histórias: o Solicitante cancela a própria; o Atendente responsável cancela qualquer reserva (UC-11 nos dois). |
| US-12 | "Como Solicitante (ou Gestor), quero ver uma reserva… e a linha do tempo…". | "Como Solicitante ou Atendente responsável…", com o Gestor do serviço herdando, se o grupo decidir. |
| US-03 | "Como pessoa identificada (Solicitante ou Gestor)…". | "Como pessoa identificada (qualquer um dos três papéis)…". |
| UC-10 (ator primário) | "Depende do filho: o Atendente responsável em UC-17, UC-18 e UC-19; o Atendente responsável ou o Solicitante em UC-11". | Igual (já ajustado na REQ-12); sem mudança se o CR for rejeitado. |
| Enunciados de RF | "permitir ao Gestor…" (perfil). | "permitir ao Atendente responsável…" (RF-12, RF-17 a RF-20) ou "ao Gestor do serviço…" (RF-04 a RF-09), se o grupo preferir o papel ao perfil. |

## 5. Critérios de aceite

- **Dado** a US-13 dividida **Quando** o grupo confere a rastreabilidade **Então** cada uma das duas histórias tem UC-11, RF-20 ou RF-21 e pelo menos um CA com TA, e `python scripts/verificar_historias.py` não aponta pendência. (TA a criar na REQ-13.)
- **Dado** o CR aceito **Quando** se roda `python scripts/gerar_rastreabilidade.py --verificar` **Então** nenhum RF, UC, CA ou TA fica sem ligação, e a contagem de CAs e TAs do README da fonte oficial confere com a matriz. (TA a criar na REQ-13.)

## 6. Regressão

- Rever os TAs de [US-13](../historias/US-13-cancelar-uma-reserva.md), [US-12](../historias/US-12-ver-detalhe-e-historico.md) e [US-03](../historias/US-03-manter-e-encerrar-a-sessao.md).
- Cenário que não deve mudar: o Solicitante só cancela a própria reserva e recebe 404 na de outra pessoa ([RN-15](../requisitos/regras-de-negocio.md#rn-15)); o Atendente responsável cancela qualquer uma, antes do início ([RN-09](../requisitos/regras-de-negocio.md#rn-09), [RN-10](../requisitos/regras-de-negocio.md#rn-10)).

## 7. Decisão

| Campo | Conteúdo |
|---|---|
| **Decisão** | Adiada: proposto, sem decisão. |
| **Quem decidiu e quando** | — |
| **Justificativa** | A REQ-12 ajustou só o rótulo dos artefatos de um papel; os de ator misto mudam história e testes e ficam para a REQ-13, que gera os IDs do PDF e aplica os CRs. |
| **Referência candidata** | Manifesto da [baseline candidata](../baselines/conecta-campus-1.0-candidata.md); falta a decisão do grupo na REQ-13. |
