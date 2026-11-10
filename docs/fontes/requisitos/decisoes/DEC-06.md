# DEC-06 — Reservas de um espaço desativado

| Identificação | Responsabilidade |
|---|---|
| **DEC-06 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Decidida. Resposta do professor na Aula 7 (06/11/2026), que confirma a opção já implementada; nenhum CR. |
| **Pergunta** | Um espaço pode ser excluído? Quando o gestor desativa um espaço, o que acontece com as reservas que ele já tem? |
| **Resposta do professor** | "Isso mesmo, deve continuar assim." |
| **Decisão** | **a)** Espaço nunca é excluído, só desativado. Desativar impede **novos** pedidos ([espaço inativo](../glossario.md#espaco-inativo)). As reservas existentes continuam valendo, com as mesmas ações; o gestor cancela, uma a uma, as que precisar. Reativar volta a aceitar pedidos. |
| **Motivo** | Preserva as decisões já tomadas e o histórico. Bloquear a desativação ou cancelar em cascata exigiria que o cadastro de espaços conhecesse as reservas, o que a arquitetura atual proíbe (contratos do import-linter). |
| **Alternativas** | **b)** Impedir a desativação enquanto houver reservas futuras que ocupam horário. **c)** Cancelar automaticamente as reservas futuras, com um motivo padrão. **d)** Mostrar ao gestor as reservas afetadas antes de confirmar a desativação. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor como representante do cliente (premissa P-01). |
| **Prazo** | Decidida em 06/11/2026. |
| **Artefatos afetados** | `EspacoEsportivo.desativar` e `ativar`; `DesativarEspaco` e `AtivarEspaco`; `POST /api/espacos/{id}/desativar/` e `.../ativar/`; texto do `DialogoDeAtivacao`; `espacos/tests/test_api_desativacao_e_reservas.py`; [Visão](../visao.md) (NS-02, fora do escopo, R-09); casos de uso de espaços (REQ-03); fichas de [UC-04](../casos-de-uso/UC-04-solicitar-reserva.md#e8-2) (E8.2), [UC-10](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#questões-em-aberto) e [UC-16](../casos-de-uso/fichas-resumidas.md#uc-16) (REQ-04). · **REQ-06:** histórias [US-06](../historias/US-06-editar-espaco.md), [US-07](../historias/US-07-desativar-e-reativar-espaco.md), [US-08](../historias/US-08-solicitar-reserva.md), [US-13](../historias/US-13-cancelar-uma-reserva.md), [US-20](../historias/US-20-cancelar-qualquer-reserva.md); 15 critérios de aceite e 15 testes de aceite ([mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-06)). |
| **Origem** | ESP-04, decisão a ("Proposta de DEC-06" no `CLAUDE.md`). |
| **Observações** | As opções b e c fazem um contexto depender do outro e são mudança comportamental (CR). |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Registro da decisão proposta na ESP-04 (REQ-01). |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as fichas de caso de uso que dependem desta decisão (REQ-04). |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as histórias e o número de critérios e testes de aceite, a partir do [mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-06) (REQ-06). Estado e opção sem mudança. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Decidida na Aula 7: resposta do professor registrada, confirmando a opção adotada (que passa ao campo Decisão); nenhum CR (GES-02). |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Artefatos afetados com 15 critérios e 15 testes de aceite, pelos CAs novos de outras decisões aplicadas na especificação (REQ-13). Estado e opção sem mudança. Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | US-20 nova (divisão da US-13 pelo CR-05, REQ-13) entre as histórias afetadas. Estado e opção sem mudança. Sem aprovação. |
