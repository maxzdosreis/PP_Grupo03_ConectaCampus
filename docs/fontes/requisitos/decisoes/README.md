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
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Respostas da Aula 7 (GES-02): DEC-05 a DEC-13 decididas, com a data e o CR de cada resposta que muda o comportamento (coluna CR); DEC-14 a DEC-23 criadas a partir dos pontos a confirmar respondidos e das respostas sobre entrega e apresentação; só o ponto 4 do `CLAUDE.md` segue aberto. Sem aprovação. |

## Estados

| Estado | Significado |
|---|---|
| **Pendente** | Pergunta registrada, sem opção adotada. |
| **Adotada provisoriamente** | O código já implementa uma opção, mas a resposta de quem decide ainda não veio. |
| **Decidida** | Quem tem autoridade respondeu; a opção vale até um CR. |
| **Substituída** | Outra DEC tomou o lugar desta, que fica preservada com o link para a nova. |

Uma DEC decidida com uma resposta diferente do que o código fazia continua **Decidida**: a diferença vira um [CR](../mudancas/README.md), e o código segue a opção anterior até a tarefa que implementa o CR (linha "Implementação" da DEC).

O estado da decisão é diferente da versão e do estado do arquivo (`0.1 • Rascunho`); ver o [README da fonte oficial](../README.md#versão-e-estado).

## Índice

"Tipo de mudança" segue a classificação do A4·s17: **editorial** corrige o texto e mantém a obrigação; **comportamental** traz uma regra nova e exige análise de impacto e decisão. Uma resposta diferente da opção adotada é comportamental e abre um CR. O impacto completo (RF, UC, US, CA, TA, endpoints e código) é gerado em [`impacto-por-dec.md`](../rastreabilidade/impacto-por-dec.md).

| ID | Título | Estado | Data | Responsável | Prazo | Muda o quê se a resposta for outra | Tipo de mudança | CR | Arquivo |
|---|---|---|---|---|---|---|---|---|---|
| DEC-01 | React no frontend | Decidida | não registrada | Professor (resposta); grupo | não registrado | Só a restrição REST-03 e o frontend inteiro; nenhum RF ([impacto](../rastreabilidade/impacto-por-dec.md#dec-01)). | — (decidida) | — | [DEC-01](DEC-01.md) |
| DEC-02 | Docker e PostgreSQL na correção | Decidida | não registrada | Professor (resposta); grupo | não registrado | Só a restrição REST-04 e a execução; nenhum RF ([impacto](../rastreabilidade/impacto-por-dec.md#dec-02)). | — (decidida) | — | [DEC-02](DEC-02.md) |
| DEC-03 | Arquivos do Docker na estrutura do ZIP | Decidida | não registrada | Professor (resposta); grupo | não registrado | Só a restrição REST-04 e o empacotamento; nenhum RF ([impacto](../rastreabilidade/impacto-por-dec.md#dec-03)). | — (decidida) | — | [DEC-03](DEC-03.md) |
| DEC-04 | Autenticação e perfis de acesso | Decidida | 16/10/2026 | Professor (resposta); grupo | decidida em 16/10/2026 | Perfis e identificação de quase todo o sistema: 11 RF, 5 RNF e 39 CAs ([impacto](../rastreabilidade/impacto-por-dec.md#dec-04)). | — (decidida) | — | [DEC-04](DEC-04.md) |
| DEC-05 | Histórico só com mudanças efetivas | Decidida | 06/11/2026 | Professor (resposta); Max Zimmermann dos Reis (grupo) | decidida em 06/11/2026 | Registrar também as tentativas recusadas: RF-22, RNF-R02 e os CAs de registro de 6 histórias ([impacto](../rastreabilidade/impacto-por-dec.md#dec-05)). | comportamental (a resposta muda; implementação na RES-12) | [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md) | [DEC-05](DEC-05.md) |
| DEC-06 | Reservas de um espaço desativado | Decidida | 06/11/2026 | Professor (resposta); Max Zimmermann dos Reis (grupo) | decidida em 06/11/2026 | Desativar passaria a cancelar ou bloquear as reservas futuras, cruzando os dois contextos: 5 RF ([impacto](../rastreabilidade/impacto-por-dec.md#dec-06)). | — (confirmada) | — | [DEC-06](DEC-06.md) |
| DEC-07 | Valores das regras de agenda | Decidida | 06/11/2026 | Professor (resposta); Max Zimmermann dos Reis (grupo) | decidida em 06/11/2026 | Outros horários, durações ou antecedência: RF-11.5, RF-28, RF-30, RF-31 e os testes de borda; por espaço, o cadastro de espaços também muda ([impacto](../rastreabilidade/impacto-por-dec.md#dec-07)). | comportamental (a resposta muda; implementação na ESP-07) | [CR-03](../mudancas/CR-03-horario-por-espaco.md) | [DEC-07](DEC-07.md) |
| DEC-08 | Cobertura-alvo dos testes | Decidida | 06/11/2026 | Professor (resposta); Max Zimmermann dos Reis (grupo) | decidida em 06/11/2026 | Só a meta do RNF-S03 e a configuração da cobertura; nenhum CA ([impacto](../rastreabilidade/impacto-por-dec.md#dec-08)). | — (confirmada) | — | [DEC-08](DEC-08.md) |
| DEC-09 | Formato da matrícula | Decidida | 06/11/2026 | Professor (resposta); Max Zimmermann dos Reis (grupo) | decidida em 06/11/2026 | Um formato mais restrito muda o RF-32.1, a validação do cadastro e os dados de exemplo ([impacto](../rastreabilidade/impacto-por-dec.md#dec-09)). | comportamental (a resposta muda; implementação na AUT-12) | [CR-04](../mudancas/CR-04-matricula-so-digitos.md) | [DEC-09](DEC-09.md) |
| DEC-10 | Nome de espaço único | Decidida | 06/11/2026 | Professor (resposta); Max Zimmermann dos Reis (grupo) | decidida em 06/11/2026 | Aceitar nomes repetidos remove o RF-05.2 e a restrição do banco ([impacto](../rastreabilidade/impacto-por-dec.md#dec-10)). | — (confirmada) | — | [DEC-10](DEC-10.md) |
| DEC-11 | Períodos ocupados por outras pessoas na agenda do dia | Decidida | 06/11/2026 | Professor (resposta); Max Zimmermann dos Reis (grupo) | decidida em 06/11/2026 | Esconder os períodos de outras pessoas muda o RF-29 e o RNF-F06 ([impacto](../rastreabilidade/impacto-por-dec.md#dec-11)). | — (confirmada) | — | [DEC-11](DEC-11.md) |
| DEC-12 | Metas de desempenho | Decidida | 06/11/2026 | Professor (resposta); Max Zimmermann dos Reis (grupo) | decidida em 06/11/2026 | Só as metas do RNF-P01 e do RNF-P02; uma carga maior exigiria paginação (L-05) ([impacto](../rastreabilidade/impacto-por-dec.md#dec-12)). | — (confirmada) | — | [DEC-12](DEC-12.md) |
| DEC-13 | Mudança de situação em relação ao horário da reserva | Decidida | 06/11/2026 | Professor (resposta); Max Zimmermann dos Reis (grupo) | decidida em 06/11/2026 | Concluir, recusar e cancelar pelo Gestor passam a depender do horário: RF-16 a RF-21, as ações disponíveis e o UC-10 ([impacto](../rastreabilidade/impacto-por-dec.md#dec-13)). | comportamental (a resposta muda; implementação na RES-11) | [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md) | [DEC-13](DEC-13.md) |
| DEC-14 | Alternativas e exceções nos casos de uso | Decidida | 06/11/2026 | Professor (resposta); grupo | decidida em 06/11/2026 | Só os rótulos `A`/`E` das fichas de caso de uso; troca editorial ([impacto](../rastreabilidade/impacto-por-dec.md#dec-14)). | — (confirmada) | — | [DEC-14](DEC-14.md) |
| DEC-15 | Critérios de aceite em Dado/Quando/Então | Decidida | 06/11/2026 | Professor (resposta); grupo | decidida em 06/11/2026 | O formato dos 156 CAs das histórias ([impacto](../rastreabilidade/impacto-por-dec.md#dec-15)). | — (confirmada) | — | [DEC-15](DEC-15.md) |
| DEC-16 | Rastreabilidade até o código | Decidida | 06/11/2026 | Professor (resposta); grupo | decidida em 06/11/2026 | As colunas complementares "Endpoint ou tela" e "Código" da matriz ([impacto](../rastreabilidade/impacto-por-dec.md#dec-16)). | — (confirmada) | — | [DEC-16](DEC-16.md) |
| DEC-17 | Convenção de versão dos documentos | Decidida | 06/11/2026 | Professor (resposta); grupo | decidida em 06/11/2026 | O cabeçalho de todos os documentos e a baseline ([impacto](../rastreabilidade/impacto-por-dec.md#dec-17)). | — (confirmada) | — | [DEC-17](DEC-17.md) |
| DEC-18 | Index Card das histórias | Decidida | 06/11/2026 | Professor (resposta); grupo | decidida em 06/11/2026 | O Index Card das 19 histórias ([impacto](../rastreabilidade/impacto-por-dec.md#dec-18)). | — (confirmada) | — | [DEC-18](DEC-18.md) |
| DEC-19 | Outros diagramas além dos casos de uso | Decidida | 06/11/2026 | Professor (resposta); grupo (decisão: DER) | decidida em 06/11/2026 | Só a modelagem; o DER é a DOC-10 ([impacto](../rastreabilidade/impacto-por-dec.md#dec-19)). | — (a critério do grupo) | — | [DEC-19](DEC-19.md) |
| DEC-20 | Entrega separada dos documentos de Requisitos | Decidida | 06/11/2026 | Professor (resposta); grupo | decidida em 06/11/2026 | Só a entrega (REQ-08); o ZIP não muda ([impacto](../rastreabilidade/impacto-por-dec.md#dec-20)). | — (decidida) | — | [DEC-20](DEC-20.md) |
| DEC-21 | Capa do modelagem.pdf | Decidida | 06/11/2026 | Professor (resposta); grupo | decidida em 06/11/2026 | Só o plano de páginas do `modelagem.pdf` (DOC-04) ([impacto](../rastreabilidade/impacto-por-dec.md#dec-21)). | — (decidida) | — | [DEC-21](DEC-21.md) |
| DEC-22 | Modelo do contribuicoes.pdf | Decidida | 06/11/2026 | Professor (resposta); grupo | decidida em 06/11/2026 | Só o formato do `contribuicoes.pdf` (DOC-06) ([impacto](../rastreabilidade/impacto-por-dec.md#dec-22)). | — (decidida) | — | [DEC-22](DEC-22.md) |
| DEC-23 | Apresentação | Decidida | 06/11/2026 | Professor (resposta); grupo | decidida em 06/11/2026 | Só o roteiro e o ensaio da demonstração ([impacto](../rastreabilidade/impacto-por-dec.md#dec-23)). | — (decidida) | — | [DEC-23](DEC-23.md) |

A [pauta da Aula 7](pauta-aula-7.md) (06/11/2026) levou ao professor as DECs com prazo nessa data e os pontos a confirmar; as respostas e o resultado de cada item estão na [seção Resultado](pauta-aula-7.md#resultado).

## Pontos a confirmar ainda abertos

A lista completa não é copiada aqui: está em dois arquivos locais, fora do Git, citados como caminho (como no [README da fonte oficial](../README.md#pontos-a-confirmar-com-o-professor)). Os pontos 4, 5, 6, 10 e 13 de `.claude/requisitos.md` e o ponto 5 do `CLAUDE.md` foram respondidos na Aula 7 e viraram as DEC-14 a DEC-19. Segue aberto:

| Ponto | Arquivo | Pergunta (resumo) | O que afeta |
|---|---|---|---|
| 4 | `CLAUDE.md` | A composição do grupo atende às duas disciplinas? | O registro do grupo e do recorte (já feito até 16/10/2026); nenhum artefato desta fonte. Não foi perguntado na Aula 7. |

## Como registrar uma nova DEC

1. Use o próximo número livre. Um ID nunca é reutilizado, nem de uma DEC substituída.
2. Copie a estrutura de uma DEC existente: pergunta, opção adotada (ou "nenhuma"), motivo, alternativas, responsável, prazo, artefatos afetados, origem e observações.
3. Acrescente a linha neste índice e cite a DEC nos documentos que ela afeta (no campo Decisões das fichas de RF e no "Depende de" dos CAs). Rode `python scripts/gerar_rastreabilidade.py` para o mapa de impacto incluí-la.
4. Quando a resposta chegar, mude o estado, registre a resposta (literal, entre aspas) e a data, separe a decisão do grupo do que o professor disse e, se a decisão mudar o comportamento já implementado, abra um [CR](../mudancas/modelo-cr.md) e acrescente a linha "Implementação" com o CR e a tarefa; o [mapa de impacto](../rastreabilidade/impacto-por-dec.md) da DEC é o ponto de partida do mapa de impacto do CR. Nos CAs, a marca de uma DEC confirmada fica `Depende de: DEC-xx (decidida)`, a única forma que os scripts leem.
