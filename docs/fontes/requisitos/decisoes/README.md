# Decisões (DEC)

Registro oficial das decisões do Conecta Campus: respostas do professor e escolhas do grupo que ainda dependem de confirmação. Uma dúvida não vira regra escondida no código ou no texto: vira uma DEC com pergunta, responsável, prazo e artefatos afetados (A4·s13).

## Estados

| Estado | Significado |
|---|---|
| **Pendente** | Pergunta registrada, sem opção adotada. |
| **Adotada provisoriamente** | O código já implementa uma opção, mas a resposta de quem decide ainda não veio. |
| **Decidida** | Quem tem autoridade respondeu; a opção vale até um CR. |
| **Substituída** | Outra DEC tomou o lugar desta, que fica preservada com o link para a nova. |

O estado da decisão é diferente da versão e do estado do arquivo (`0.1 • Rascunho`); ver o [README da fonte oficial](../README.md#versão-e-estado).

## Índice

| ID | Título | Estado | Data | Arquivo |
|---|---|---|---|---|
| DEC-01 | React no frontend | Decidida | não registrada | [DEC-01](DEC-01.md) |
| DEC-02 | Docker e PostgreSQL na correção | Decidida | não registrada | [DEC-02](DEC-02.md) |
| DEC-03 | Arquivos do Docker na estrutura do ZIP | Decidida | não registrada | [DEC-03](DEC-03.md) |
| DEC-04 | Autenticação e perfis de acesso | Decidida | 16/10/2026 | [DEC-04](DEC-04.md) |
| DEC-05 | Histórico só com mudanças efetivas | Adotada provisoriamente | registrada em 03/11/2026; prazo 06/11/2026 | [DEC-05](DEC-05.md) |
| DEC-06 | Reservas de um espaço desativado | Adotada provisoriamente | registrada em 03/11/2026; prazo 06/11/2026 | [DEC-06](DEC-06.md) |
| DEC-07 | Valores das regras de agenda | Adotada provisoriamente | registrada em 03/11/2026; prazo 06/11/2026 | [DEC-07](DEC-07.md) |
| DEC-08 | Cobertura-alvo dos testes | Adotada provisoriamente | registrada em 03/11/2026; prazo 13/11/2026 | [DEC-08](DEC-08.md) |
| DEC-09 | Formato da matrícula | Adotada provisoriamente | registrada em 03/11/2026; prazo 06/11/2026 | [DEC-09](DEC-09.md) |
| DEC-10 | Nome de espaço único | Adotada provisoriamente | registrada em 03/11/2026; prazo 06/11/2026 | [DEC-10](DEC-10.md) |
| DEC-11 | Períodos ocupados por outras pessoas na agenda do dia | Adotada provisoriamente | registrada em 03/11/2026; prazo 06/11/2026 | [DEC-11](DEC-11.md) |

## Como registrar uma nova DEC

1. Use o próximo número livre. Um ID nunca é reutilizado, nem de uma DEC substituída.
2. Copie a estrutura de uma DEC existente: pergunta, opção adotada (ou "nenhuma"), motivo, alternativas, responsável, prazo, artefatos afetados, origem e observações.
3. Acrescente a linha neste índice e cite a DEC nos documentos que ela afeta.
4. Quando a resposta chegar, mude o estado, registre a resposta e a data e abra um CR se a decisão mudar o comportamento já implementado.
