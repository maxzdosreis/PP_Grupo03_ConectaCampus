# DEC-07 — Valores das regras de agenda

| Identificação | Responsabilidade |
|---|---|
| **DEC-07 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Adotada provisoriamente (o código já implementa os valores abaixo; falta a confirmação). |
| **Pergunta** | Em que período do dia os espaços podem ser usados, qual a duração mínima e máxima de uma reserva e com quantos dias de antecedência se pode pedir? Esses limites são os mesmos para todos os espaços e todos os dias? |
| **Opção adotada hoje** | [Horário de funcionamento](../glossario.md#horario-de-funcionamento) das 07:00 às 22:00; [duração mínima](../glossario.md#duracao-minima) de 30 minutos e [máxima](../glossario.md#duracao-maxima) de 3 horas; [antecedência máxima](../glossario.md#antecedencia-maxima) de 30 dias. Limites globais, iguais para todos os espaços e dias, aplicados só a novos pedidos. |
| **Motivo** | Valores escolhidos pelo grupo, sem cliente real (premissa P-01), para a regra existir e ser testada. Ficam em constantes únicas: trocar um valor não muda nenhuma outra parte do código. |
| **Alternativas** | Outros valores; limites por espaço (exigiria consultar o cadastro de espaços); limites por dia da semana ou feriados; sem limites. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor como representante do cliente. |
| **Prazo sugerido** | 06/11/2026 (Aula 7). |
| **Artefatos afetados** | `HORARIO_DE_ABERTURA`, `HORARIO_DE_FECHAMENTO`, `DURACAO_MINIMA`, `DURACAO_MAXIMA`, `ANTECEDENCIA_MAXIMA_EM_DIAS` (`reservas/domain/regras_de_agenda.py`); mensagens de `ForaDoHorarioDeFuncionamento`, `DuracaoInvalida` e `AntecedenciaExcedida`; `GET /api/reservas/regras-de-agenda/`; dica do formulário e agenda do dia; horários dos dados de exemplo; README; [Glossário](../glossario.md); [Visão](../visao.md) (NS-06, P-04, R-10); testes de regras de agenda. |
| **Origem** | RES-09, decisão b ("proposta de DEC-07" no `CLAUDE.md`). |
| **Observações** | Mudar só os valores é mudança comportamental pequena (CR com regressão dos testes de borda). Limites por espaço ou por dia são mudança comportamental grande e estão fora do escopo até um CR. |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Registro da decisão proposta na RES-09 (REQ-01). |
