# DEC-07 — Valores das regras de agenda

| Identificação | Responsabilidade |
|---|---|
| **DEC-07 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Decidida. Resposta do professor na Aula 7 (06/11/2026); a resposta muda o comportamento implementado e segue pelo [CR-03](../mudancas/CR-03-horario-por-espaco.md). |
| **Pergunta** | Em que período do dia os espaços podem ser usados, qual a duração mínima e máxima de uma reserva e com quantos dias de antecedência se pode pedir? Esses limites são os mesmos para todos os espaços e todos os dias? |
| **Opção implementada até o CR-03** | [Horário de funcionamento](../glossario.md#horario-de-funcionamento) das 07:00 às 22:00; [duração mínima](../glossario.md#duracao-minima) de 30 minutos e [máxima](../glossario.md#duracao-maxima) de 3 horas; [antecedência máxima](../glossario.md#antecedencia-maxima) de 30 dias. Limites globais, iguais para todos os espaços e dias, aplicados só a novos pedidos. |
| **Resposta do professor** | "O horário de funcionamento é das 07:00 às 00:00, as reservas padrões são de 1 hora, e precisa de horário por espaço, porque teremos vários espaços." |
| **Decisão do grupo** | 07:00–00:00 é o padrão de cada espaço, configurável por espaço. "Reservas padrões de 1 hora" é a duração sugerida ao pedir. A duração mínima de 30 minutos, a máxima de 3 horas e a antecedência de 30 dias continuam (o professor não as mudou). O término à meia-noite é o fim do dia da reserva. |
| **Decisão** | Cada espaço tem o próprio horário de funcionamento, com padrão das 07:00 às 00:00 (o término à meia-noite é o fim do dia da reserva); o pedido sugere 1 hora de duração; a duração mínima (30 minutos), a máxima (3 horas) e a antecedência máxima (30 dias) continuam iguais para todos. |
| **Implementação** | [CR-03](../mudancas/CR-03-horario-por-espaco.md), tarefa ESP-07. Até ela, o código continua com os limites globais acima. |
| **Motivo** | Valores escolhidos pelo grupo, sem cliente real (premissa P-01), para a regra existir e ser testada. Ficam em constantes únicas: trocar um valor não muda nenhuma outra parte do código. |
| **Alternativas** | Outros valores; limites por espaço (exigiria consultar o cadastro de espaços); limites por dia da semana ou feriados; sem limites. A decisão adota o horário por espaço; limites por dia da semana ou feriados não foram pedidos. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor como representante do cliente. |
| **Prazo** | Decidida em 06/11/2026. |
| **Artefatos afetados** | `HORARIO_DE_ABERTURA`, `HORARIO_DE_FECHAMENTO`, `DURACAO_MINIMA`, `DURACAO_MAXIMA`, `ANTECEDENCIA_MAXIMA_EM_DIAS` (`reservas/domain/regras_de_agenda.py`); mensagens de `ForaDoHorarioDeFuncionamento`, `DuracaoInvalida` e `AntecedenciaExcedida`; `GET /api/reservas/regras-de-agenda/`; dica do formulário e agenda do dia; horários dos dados de exemplo; README; [Glossário](../glossario.md); [Visão](../visao.md) (NS-06, P-04, R-10); testes de regras de agenda; ficha de [UC-04](../casos-de-uso/UC-04-solicitar-reserva.md#questões-em-aberto) (E6.1 a E6.3) (REQ-04). · **REQ-06:** histórias [US-08](../historias/US-08-solicitar-reserva.md), [US-09](../historias/US-09-ver-a-agenda-do-dia.md); 10 critérios de aceite e 10 testes de aceite ([mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-07)). |
| **Origem** | RES-09, decisão b ("proposta de DEC-07" no `CLAUDE.md`). |
| **Observações** | Mudança comportamental grande: o horário por espaço faz o cadastro de espaços guardar o horário e as reservas consultá-lo pela fachada `espacos.publico`. O [CR-03](../mudancas/CR-03-horario-por-espaco.md) traz o impacto (inclusive o do cadastro de espaços, a confirmar na ESP-07) e o aceite; a ESP-07 aplica o CR no mesmo PR do código. |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Registro da decisão proposta na RES-09 (REQ-01). |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as fichas de caso de uso que dependem desta decisão (REQ-04). |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as histórias e o número de critérios e testes de aceite, a partir do [mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-07) (REQ-06). Estado e opção sem mudança. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Decidida na Aula 7: resposta do professor e decisão do grupo registradas; os valores atuais passam a "implementados até o CR-03"; CR-03 aberto, implementação na ESP-07 (GES-02). |
