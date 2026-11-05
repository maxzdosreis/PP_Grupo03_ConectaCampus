# Decisões (DEC)

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **IND-02 • 0.1 • Rascunho** (índice das decisões) | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/decisoes/` |

Registro oficial das decisões do Conecta Campus: respostas do professor e escolhas do grupo que ainda dependem de confirmação. Uma dúvida não vira regra escondida no código ou no texto: vira uma DEC com pergunta, responsável, prazo e artefatos afetados (A4·s13).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Criação do índice (REQ-01; data do commit, o arquivo não tinha histórico). Sem aprovação. |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Cabeçalho completado (REQ-06). Índice com responsável, prazo, o que muda se a resposta for outra (com link para o [mapa de impacto](../rastreabilidade/impacto-por-dec.md)) e o tipo de mudança; seção dos pontos a confirmar ainda abertos; [pauta da Aula 7](pauta-aula-7.md). Nenhum estado nem opção mudou. Sem aprovação. |

## Estados

| Estado | Significado |
|---|---|
| **Pendente** | Pergunta registrada, sem opção adotada. |
| **Adotada provisoriamente** | O código já implementa uma opção, mas a resposta de quem decide ainda não veio. |
| **Decidida** | Quem tem autoridade respondeu; a opção vale até um CR. |
| **Substituída** | Outra DEC tomou o lugar desta, que fica preservada com o link para a nova. |

O estado da decisão é diferente da versão e do estado do arquivo (`0.1 • Rascunho`); ver o [README da fonte oficial](../README.md#versão-e-estado).

## Índice

"Tipo de mudança" segue a classificação do A4·s17: **editorial** corrige o texto e mantém a obrigação; **comportamental** traz uma regra nova e exige análise de impacto e decisão. Uma resposta diferente da opção adotada em qualquer DEC aberta é comportamental. O impacto completo (RF, UC, US, CA, TA, endpoints e código) é gerado em [`impacto-por-dec.md`](../rastreabilidade/impacto-por-dec.md).

| ID | Título | Estado | Data | Responsável | Prazo | Muda o quê se a resposta for outra | Tipo de mudança | Arquivo |
|---|---|---|---|---|---|---|---|---|
| DEC-01 | React no frontend | Decidida | não registrada | Professor (resposta); grupo | não registrado | Só a restrição REST-03 e o frontend inteiro; nenhum RF ([impacto](../rastreabilidade/impacto-por-dec.md#dec-01)). | — (decidida) | [DEC-01](DEC-01.md) |
| DEC-02 | Docker e PostgreSQL na correção | Decidida | não registrada | Professor (resposta); grupo | não registrado | Só a restrição REST-04 e a execução; nenhum RF ([impacto](../rastreabilidade/impacto-por-dec.md#dec-02)). | — (decidida) | [DEC-02](DEC-02.md) |
| DEC-03 | Arquivos do Docker na estrutura do ZIP | Decidida | não registrada | Professor (resposta); grupo | não registrado | Só a restrição REST-04 e o empacotamento; nenhum RF ([impacto](../rastreabilidade/impacto-por-dec.md#dec-03)). | — (decidida) | [DEC-03](DEC-03.md) |
| DEC-04 | Autenticação e perfis de acesso | Decidida | 16/10/2026 | Professor (resposta); grupo | decidida em 16/10/2026 | Perfis e identificação de quase todo o sistema: 11 RF, 5 RNF e 39 CAs ([impacto](../rastreabilidade/impacto-por-dec.md#dec-04)). | — (decidida) | [DEC-04](DEC-04.md) |
| DEC-05 | Histórico só com mudanças efetivas | Adotada provisoriamente | registrada em 03/11/2026 | Max Zimmermann dos Reis (grupo) | 06/11/2026 | Registrar também as tentativas recusadas: RF-22, RNF-R02 e os CAs de registro de 6 histórias ([impacto](../rastreabilidade/impacto-por-dec.md#dec-05)). | comportamental | [DEC-05](DEC-05.md) |
| DEC-06 | Reservas de um espaço desativado | Adotada provisoriamente | registrada em 03/11/2026 | Max Zimmermann dos Reis (grupo) | 06/11/2026 | Desativar passaria a cancelar ou bloquear as reservas futuras, cruzando os dois contextos: 5 RF ([impacto](../rastreabilidade/impacto-por-dec.md#dec-06)). | comportamental | [DEC-06](DEC-06.md) |
| DEC-07 | Valores das regras de agenda | Adotada provisoriamente | registrada em 03/11/2026 | Max Zimmermann dos Reis (grupo) | 06/11/2026 | Outros horários, durações ou antecedência: RF-11.5, RF-28, RF-30, RF-31 e os testes de borda ([impacto](../rastreabilidade/impacto-por-dec.md#dec-07)). | comportamental | [DEC-07](DEC-07.md) |
| DEC-08 | Cobertura-alvo dos testes | Adotada provisoriamente | registrada em 03/11/2026 | Max Zimmermann dos Reis (grupo) | 13/11/2026 | Só a meta do RNF-S03 e a configuração da cobertura; nenhum CA ([impacto](../rastreabilidade/impacto-por-dec.md#dec-08)). | comportamental (meta de RNF) | [DEC-08](DEC-08.md) |
| DEC-09 | Formato da matrícula | Adotada provisoriamente | registrada em 03/11/2026 | Max Zimmermann dos Reis (grupo) | 06/11/2026 | Um formato mais restrito muda o RF-32.1, a validação do cadastro e os dados de exemplo ([impacto](../rastreabilidade/impacto-por-dec.md#dec-09)). | comportamental | [DEC-09](DEC-09.md) |
| DEC-10 | Nome de espaço único | Adotada provisoriamente | registrada em 03/11/2026 | Max Zimmermann dos Reis (grupo) | 06/11/2026 | Aceitar nomes repetidos remove o RF-05.2 e a restrição do banco ([impacto](../rastreabilidade/impacto-por-dec.md#dec-10)). | comportamental | [DEC-10](DEC-10.md) |
| DEC-11 | Períodos ocupados por outras pessoas na agenda do dia | Adotada provisoriamente | registrada em 03/11/2026 | Max Zimmermann dos Reis (grupo) | 06/11/2026 | Esconder os períodos de outras pessoas muda o RF-29 e o RNF-F06 ([impacto](../rastreabilidade/impacto-por-dec.md#dec-11)). | comportamental | [DEC-11](DEC-11.md) |
| DEC-12 | Metas de desempenho | Adotada provisoriamente | registrada em 03/11/2026 | Max Zimmermann dos Reis (grupo) | 13/11/2026 | Só as metas do RNF-P01 e do RNF-P02; uma carga maior exigiria paginação (L-05) ([impacto](../rastreabilidade/impacto-por-dec.md#dec-12)). | comportamental (meta de RNF) | [DEC-12](DEC-12.md) |
| DEC-13 | Mudança de situação em relação ao horário da reserva | Adotada provisoriamente | registrada em 03/11/2026 | Max Zimmermann dos Reis (grupo) | 06/11/2026 | Concluir, confirmar, recusar e cancelar passariam a depender do horário: RF-16 a RF-21, as ações disponíveis e o UC-10 ([impacto](../rastreabilidade/impacto-por-dec.md#dec-13)). | comportamental | [DEC-13](DEC-13.md) |

A [pauta da Aula 7](pauta-aula-7.md) (06/11/2026) leva ao professor as DECs com prazo nessa data e os pontos abaixo.

## Pontos a confirmar ainda abertos

A lista completa não é copiada aqui: está em dois arquivos locais, fora do Git, citados como caminho (como no [README da fonte oficial](../README.md#pontos-a-confirmar-com-o-professor)). Os que seguem abertos e afetam esta fonte:

| Ponto | Arquivo | Pergunta (resumo) | O que afeta |
|---|---|---|---|
| 4 | `.claude/requisitos.md` | Outros diagramas (sequência, C4, DER, jornada em raias) serão exigidos? | `modelagem.pdf` (DOC-01) e [`casos-de-uso/`](../casos-de-uso/README.md#pendências): hoje só o diagrama de casos de uso e o fluxo de decisão de UC-04. |
| 5 | `.claude/requisitos.md` | Alternativas e exceções: `A` e `E`, ou tudo como `A`? | Os IDs das fichas de caso de uso (`A3.1`, `E9.1`), a coluna UC da [matriz](../rastreabilidade/matriz.md) e a Origem dos CAs; a troca seria editorial. |
| 6 | `.claude/requisitos.md` | Quais campos tem o "Index Card padrão"? O custo em semanas aceita fração? | O Index Card das 19 [histórias](../historias/README.md#decisao-d). |
| 10 | `.claude/requisitos.md` | A convenção de versão 0.1 → 0.2 → 1.0 vale ou o grupo define a sua? | O cabeçalho de todos os documentos e a [baseline candidata](../baselines/conecta-campus-1.0-candidata.md). |
| 13 | `.claude/requisitos.md` | A rastreabilidade deve ir até o código? | As colunas complementares "Endpoint ou tela" e "Código" da [matriz](../rastreabilidade/README.md#decisao-b) e o campo Evidência das fichas. |
| 4 | `CLAUDE.md` | A composição do grupo atende às duas disciplinas? | O registro do grupo e do recorte; nenhum artefato desta fonte. |
| 5 | `CLAUDE.md` | O formato Dado/Quando/Então dos critérios de aceite atende à disciplina? | Os 156 critérios de aceite das [histórias](../historias/README.md). |

## Como registrar uma nova DEC

1. Use o próximo número livre. Um ID nunca é reutilizado, nem de uma DEC substituída.
2. Copie a estrutura de uma DEC existente: pergunta, opção adotada (ou "nenhuma"), motivo, alternativas, responsável, prazo, artefatos afetados, origem e observações.
3. Acrescente a linha neste índice e cite a DEC nos documentos que ela afeta (no campo Decisões das fichas de RF e no "Depende de" dos CAs). Rode `python scripts/gerar_rastreabilidade.py` para o mapa de impacto incluí-la.
4. Quando a resposta chegar, mude o estado, registre a resposta e a data e abra um [CR](../mudancas/modelo-cr.md) se a decisão mudar o comportamento já implementado; o [mapa de impacto](../rastreabilidade/impacto-por-dec.md) da DEC é o ponto de partida do mapa de impacto do CR.
