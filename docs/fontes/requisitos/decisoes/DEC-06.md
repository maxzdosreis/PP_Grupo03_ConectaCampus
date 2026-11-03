# DEC-06 — Reservas de um espaço desativado

| Identificação | Responsabilidade |
|---|---|
| **DEC-06 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Adotada provisoriamente (o código já implementa a opção a; falta a confirmação). |
| **Pergunta** | Um espaço pode ser excluído? Quando o gestor desativa um espaço, o que acontece com as reservas que ele já tem? |
| **Opção adotada hoje** | **a)** Espaço nunca é excluído, só desativado. Desativar impede **novos** pedidos ([espaço inativo](../glossario.md#espaco-inativo)). As reservas existentes continuam valendo, com as mesmas ações; o gestor cancela, uma a uma, as que precisar. Reativar volta a aceitar pedidos. |
| **Motivo** | Preserva as decisões já tomadas e o histórico. Bloquear a desativação ou cancelar em cascata exigiria que o cadastro de espaços conhecesse as reservas, o que a arquitetura atual proíbe (contratos do import-linter). |
| **Alternativas** | **b)** Impedir a desativação enquanto houver reservas futuras que ocupam horário. **c)** Cancelar automaticamente as reservas futuras, com um motivo padrão. **d)** Mostrar ao gestor as reservas afetadas antes de confirmar a desativação. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor como representante do cliente (premissa P-01). |
| **Prazo sugerido** | 06/11/2026 (Aula 7). |
| **Artefatos afetados** | `EspacoEsportivo.desativar` e `ativar`; `DesativarEspaco` e `AtivarEspaco`; `POST /api/espacos/{id}/desativar/` e `.../ativar/`; texto do `DialogoDeAtivacao`; `espacos/tests/test_api_desativacao_e_reservas.py`; [Visão](../visao.md) (NS-02, fora do escopo, R-09); casos de uso de espaços (REQ-03). |
| **Origem** | ESP-04, decisão a ("Proposta de DEC-06" no `CLAUDE.md`). |
| **Observações** | As opções b e c fazem um contexto depender do outro e são mudança comportamental (CR). |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Registro da decisão proposta na ESP-04 (REQ-01). |
