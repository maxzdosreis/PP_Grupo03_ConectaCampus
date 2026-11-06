# DEC-08 — Cobertura-alvo dos testes

| Identificação | Responsabilidade |
|---|---|
| **DEC-08 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Decidida. Resposta do professor na Aula 7 (06/11/2026), que confirma a opção já implementada; nenhum CR. |
| **Pergunta** | Que meta de qualidade dos testes o grupo adota, já que a disciplina de Projeto de Programação não exige testes automatizados nem cobertura? |
| **Resposta do professor** | "Isso faz sentido, e precisamos fazer isso." (resposta dada à DEC-08 e à [DEC-12](DEC-12.md) juntas) |
| **Decisão** | 100% de linhas e ramos nas camadas `domain` e `application` de `espacos` e `reservas`; no mínimo 99% no total (`fail_under`). Antes da entrega: testes por propriedade no perfil `exaustivo` e testes de mutação sem mutante sobrevivente sem justificativa. |
| **Motivo** | As regras de negócio vivem nessas camadas; a meta prova que cada regra tem teste e alimenta a rastreabilidade (catálogos de testes). |
| **Alternativas** | Só a meta global; nenhuma meta numérica; estender a meta de 100% ao contexto `contas`. |
| **Responsável** | Max Zimmermann dos Reis (grupo). Decisão interna; não depende do professor. |
| **Prazo** | Decidida em 06/11/2026. |
| **Artefatos afetados** | `src/backend/pyproject.toml` (`fail_under`, mutmut); [testes de espaços](../../testes_de_espacos.md) e [testes de reservas](../../testes_de_reservas.md); checklist pré-entrega; [README do backend](../../../../src/backend/README.md#comandos) (comandos de teste e qualidade); [Visão](../visao.md) (R-11). · **REQ-06:** nenhuma história; 0 critérios de aceite e 0 testes de aceite ([mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-08)). |
| **Origem** | ESP-06 e RES-08 ("proposta de DEC-08" no `CLAUDE.md`). |
| **Observações** | Medido na RES-08: 99,71% no total. |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Registro da decisão proposta na ESP-06 e complementada na RES-08 (REQ-01). |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as histórias e o número de critérios e testes de aceite, a partir do [mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-08) (REQ-06). Estado e opção sem mudança. |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: os comandos de qualidade do código passam a estar no README do backend, com a divisão do README (DOC-09). Mudança editorial; estado e opção sem mudança. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Decidida na Aula 7: resposta do professor registrada, confirmando a opção adotada (que passa ao campo Decisão); nenhum CR (GES-02). |
