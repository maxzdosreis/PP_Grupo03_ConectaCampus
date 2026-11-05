# DEC-05 — Histórico só com mudanças efetivas

| Identificação | Responsabilidade |
|---|---|
| **DEC-05 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Adotada provisoriamente (o código já implementa a opção a; falta a confirmação). |
| **Pergunta** | Uma tentativa recusada de mudar a situação de uma reserva (perfil sem permissão, transição não permitida, motivo ausente) precisa ficar registrada? Se sim, onde e quem a consulta? |
| **Opção adotada hoje** | **a)** Não registrar. O [histórico](../glossario.md#historico) guarda só a criação e as mudanças aceitas. Uma recusa não altera a reserva e não gera [registro de situação](../glossario.md#registro-de-situacao). |
| **Motivo** | O histórico é o registro de negócio da reserva; uma recusa não muda nada nela. O modelo de critério de aceite do professor (CA-04: "tentativa registrada com data, ator e resultado", A3·s23–24) fica atendido só em parte. |
| **Alternativas** | **b)** Registrar só em log técnico, sem tela, consultado pela Equipe de TI. **c)** Registrar no histórico de negócio também as recusas, com o resultado, visíveis na linha do tempo. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor. |
| **Prazo sugerido** | 06/11/2026 (Aula 7). |
| **Artefatos afetados** | `RegistroDeSituacao` e `Reserva.alterar_situacao` (`reservas/domain/`); `RepositorioReservas` e a tabela do histórico; `GET /api/reservas/{id}/historico/`; linha do tempo do detalhe da reserva; README ("Limitações conhecidas"); caso de uso e critérios de aceite de "Alterar situação" (REQ-03/REQ-04); [Visão](../visao.md) (NS-12, R-08); `docs/fontes/testes_de_reservas.md`; fichas de [UC-10](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#questões-em-aberto) (garantia mínima) e de [UC-09](../casos-de-uso/fichas-resumidas.md#uc-09) (REQ-04). · **REQ-06:** histórias [US-08](../historias/US-08-solicitar-reserva.md), [US-12](../historias/US-12-ver-detalhe-e-historico.md), [US-13](../historias/US-13-cancelar-uma-reserva.md), [US-14](../historias/US-14-confirmar-uma-reserva.md), [US-15](../historias/US-15-recusar-uma-reserva.md), [US-16](../historias/US-16-concluir-uma-reserva.md); 10 critérios de aceite e 10 testes de aceite ([mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-05)). |
| **Origem** | RES-07, decisão c ("proposta DEC-05" no `CLAUDE.md`). |
| **Observações** | A opção c é mudança comportamental: muda o significado do histórico e exige um CR. |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Registro da decisão proposta na RES-07 (REQ-01). |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as fichas de caso de uso que dependem desta decisão (REQ-04). |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as histórias e o número de critérios e testes de aceite, a partir do [mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-05) (REQ-06). Estado e opção sem mudança. |
