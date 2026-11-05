# UC-10 · Alterar situação da reserva {abstrato}

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **UC-10 • 0.1 • Rascunho** (ficha completa, formato Cockburn) | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/casos-de-uso/UC-10-alterar-situacao-da-reserva.md` |

Ficha do caso de uso abstrato UC-10 do [índice](README.md#uc-10). Ela descreve uma vez o fluxo comum aos quatro filhos — UC-11 [Cancelar reserva](README.md#uc-11), UC-17 [Confirmar reserva](README.md#uc-17), UC-18 [Recusar reserva](README.md#uc-18) e UC-19 [Concluir reserva](README.md#uc-19) — e as diferenças entre eles na tabela [Variações](#variações). As subfunções incluídas UC-12 [Informar motivo](README.md#uc-12) e UC-13 [Registrar no histórico](README.md#uc-13) aparecem como passos. Como ler a numeração: [decisões h e i](README.md#decisao-h).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: fluxo comum, variações UC-11/17/18/19, exceções na ordem real das verificações, garantias, RF cobertos e evidência (REQ-04). Sem aprovação. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Linha "Histórias derivadas" (REQ-05), sem mudar o fluxo. Sem aprovação. |

## Sumário

1. [Identificação do caso de uso](#identificação-do-caso-de-uso)
2. [Stakeholders e interesses](#stakeholders-e-interesses)
3. [Fluxo principal (comum aos filhos)](#fluxo-principal-comum-aos-filhos)
4. [Variações](#variações)
5. [Alternativas](#alternativas)
6. [Exceções](#exceções)
7. [Pós-condições e garantias](#pós-condições-e-garantias)
8. [Regras de negócio](#regras-de-negócio)
9. [RFs cobertos](#rfs-cobertos)
10. [RNFs relacionados](#rnfs-relacionados)
11. [Questões em aberto](#questões-em-aberto)
12. [Anexo — Evidência (complementar)](#anexo--evidência-complementar)

## Identificação do caso de uso

| Campo | Conteúdo |
|---|---|
| **Escopo** | Conecta Campus (caixa-preta). |
| **Nível** | Objetivo do usuário, **abstrato**: só acontece por um dos filhos ([decisão c](README.md#decisao-c)). Inclui UC-12 (nos filhos que exigem motivo) e UC-13. |
| **Ator primário** | Depende do filho: o [Gestor](../glossario.md#gestor) em UC-17, UC-18 e UC-19; o Gestor ou o [Solicitante](../glossario.md#solicitante) (só na própria reserva) em UC-11. Ver [Variações](#variações). |
| **Atores secundários** | Nenhum ([decisão f](README.md#decisao-f)). |
| **Meta de contexto** | Levar uma reserva a uma situação que a [tabela de transições](../glossario.md#transicao-de-situacao) e o [perfil](../glossario.md#perfil) de quem age permitem, com o motivo quando exigido, e deixar a mudança registrada no [histórico](../glossario.md#historico). |
| **Precondições** | O ator é um [usuário autenticado](../glossario.md#usuario-autenticado) com o perfil exigido pelo filho ([UC-02 Autenticar](UC-02-autenticar.md); [decisão d](README.md#decisao-d)). A reserva existir e ser visível ao ator **não** é precondição: é conferido no [passo 6](#p6). |
| **Disparador** | O Gestor decide sobre um pedido (confirmar, recusar), registra que o uso aconteceu (concluir) ou desfaz um uso combinado (cancelar); ou o Solicitante desiste do próprio pedido (cancelar). |

## Stakeholders e interesses

| Stakeholder | Interesse neste caso de uso |
|---|---|
| **Solicitante** | Desistir sem procurar o Gestor, liberando o horário; saber, pela situação e pelo motivo, por que o pedido foi recusado ou cancelado; ter certeza de que ninguém além do Gestor decide sobre o pedido dele, e que outro solicitante não o vê nem o altera. |
| **Gestor** | Decidir com uma ação só, vendo apenas as ações que fazem sentido na situação atual; justificar recusas e cancelamentos; não perder uma decisão tomada ao mesmo tempo por outra pessoa sem ficar sabendo. |
| **Cliente** (instituição) | Só quem tem autoridade decide sobre os pedidos; toda decisão fica registrada com autor, momento e motivo; nenhuma reserva sai de um estado final nem pula etapas. |

## Fluxo principal (comum aos filhos)

1. <a id="p1"></a>O ator localiza a reserva, pela consulta ([UC-07](fichas-resumidas.md#uc-07)) ou pelo detalhe ([UC-08](fichas-resumidas.md#uc-08)).
2. <a id="p2"></a>O sistema mostra a reserva com a situação atual, o motivo (se houver) e as [ações disponíveis](../glossario.md#acao-disponivel) para o ator: as transições que a tabela permite a partir da situação atual e que o perfil dele pode executar, com a indicação das que exigem motivo.
3. <a id="p3"></a>O ator escolhe uma das ações disponíveis.
4. <a id="p4"></a>O sistema pede que o ator confirme a decisão, mostrando o espaço, a data e o horário e o solicitante da reserva e, se a ação exige motivo, pedindo o motivo. *(UC-12, nos filhos que exigem motivo.)*
5. <a id="p5"></a>O ator confirma a decisão, com o [motivo](../glossario.md#motivo) quando exigido (opcional nas outras ações).
6. <a id="p6"></a>O sistema confere o pedido de mudança, nesta ordem: a situação nova foi informada; a reserva existe e é visível ao ator; a situação nova é conhecida; o perfil do ator pode levar a reserva a ela; a tabela permite a transição a partir da situação atual; o motivo respeita o limite e, para recusar ou cancelar, foi informado.
7. <a id="p7"></a>O sistema grava a nova situação e o motivo e, na mesma gravação, o [registro de situação](../glossario.md#registro-de-situacao) da mudança: situação anterior e nova, motivo, autor (o ator) e momento. *(UC-13.)*
8. <a id="p8"></a>O sistema mostra a reserva na nova situação, com o motivo e as novas ações disponíveis, e informa o resultado ("Reserva «situação» com sucesso."). O horário fica ocupado ou é liberado conforme a [variação](#variações).

**Subfunções incluídas.** UC-12 *Informar motivo* = o pedido do motivo no [passo 4](#p4), o motivo no [passo 5](#p5) e as exceções [E6.6](#e6-6) e [E6.7](#e6-7). UC-13 *Registrar no histórico* = a segunda metade do [passo 7](#p7). Só as mudanças aceitas são registradas: nenhuma exceção grava registro ([DEC-05](../decisoes/DEC-05.md)).

## Variações

O que muda de um filho para outro. Tudo o mais (passos, alternativas e exceções) é comum.

| Filho | Ator permitido | Situações de origem | Exige motivo? | Efeito sobre o horário | Ações depois | RF |
|---|---|---|---|---|---|---|
| <a id="v-uc-17"></a>**UC-17 Confirmar reserva** | Gestor | Solicitada | Não (opcional, até 300 caracteres) | Continua ocupado (Confirmada ocupa horário) | Gestor: Cancelar, Concluir · Solicitante dono: Cancelar | [RF-17](../requisitos/rf-reservas.md#rf-17) |
| <a id="v-uc-18"></a>**UC-18 Recusar reserva** | Gestor | Solicitada | **Sim** (UC-12), até 300 caracteres | Liberado (Recusada não ocupa) | Nenhuma: situação final | [RF-18](../requisitos/rf-reservas.md#rf-18) |
| <a id="v-uc-19"></a>**UC-19 Concluir reserva** | Gestor | Confirmada | Não (opcional, até 300 caracteres) | Liberado (Concluída não ocupa; só tem efeito se concluída antes do término, [DEC-13](../decisoes/DEC-13.md)) | Nenhuma: situação final | [RF-19](../requisitos/rf-reservas.md#rf-19) |
| <a id="v-uc-11"></a>**UC-11 Cancelar reserva** | Gestor (qualquer reserva) ou Solicitante (só a própria) | Solicitada ou Confirmada | **Sim** (UC-12), até 300 caracteres | Liberado (Cancelada não ocupa) | Nenhuma: situação final | [RF-20](../requisitos/rf-reservas.md#rf-20) (Gestor), [RF-21](../requisitos/rf-reservas.md#rf-21) (Solicitante) |

Nenhuma transição depende do horário da reserva: confirmar ou recusar depois do início, concluir antes do término e cancelar depois do uso são aceitos (opção a da [DEC-13](../decisoes/DEC-13.md); [lacuna L-01](../requisitos/srs.md#l-01)). Solicitada não é destino de nenhuma ação.

## Alternativas

A meta ainda é alcançada.

#### <a id="a1-1"></a>A1.1 · Localizar pela consulta ou pelo detalhe

No passo 1, o ator parte da lista de reservas ([UC-07](fichas-resumidas.md#uc-07)) ou do detalhe de uma delas ([UC-08](fichas-resumidas.md#uc-08)). As ações oferecidas no passo 2 são as mesmas nos dois casos; o que muda é só o que o sistema mostra depois do passo 8 (a lista atualizada, ou a reserva com o histórico atualizado, em que o novo registro já aparece).

#### <a id="a5-1"></a>A5.1 · O ator desiste da decisão

No passo 5, o ator desiste de confirmar a decisão. O sistema não altera nada, não registra nada e volta ao passo 2; o ator pode escolher outra ação ou nenhuma.

#### <a id="a8-1"></a>A8.1 · Motivo opcional informado ao confirmar ou concluir

No passo 5 de UC-17 ou UC-19, o ator informa um motivo, mesmo sem ser exigido. O sistema o guarda sem espaços nas pontas nem repetidos, como motivo da nova situação e do registro; o motivo da situação anterior é descartado da reserva (continua no histórico). Segue no passo 8.

## Exceções

A meta é interrompida: **a reserva fica exatamente como estava** (situação, motivo e histórico) e **nenhum registro é gravado**. A ordem é a ordem real das verificações, que decide qual mensagem a pessoa vê primeiro ([evidência da ordem](#evidencia-da-ordem)). Em particular, o perfil é conferido **antes** da transição: um Solicitante que tenta confirmar recebe sempre a mesma resposta, sem descobrir a situação atual.

#### <a id="e2-1"></a>E2.1 · Nenhuma ação disponível

- **Condição:** no passo 2, a reserva está numa [situação final](../glossario.md#situacao-final) (Concluída, Recusada ou Cancelada), ou o perfil do ator não tem nenhuma transição a partir da situação atual.
- **Resultado para o ator:** o sistema mostra a reserva sem nenhuma ação e indica que não há ação disponível; não há o que decidir.
- **Estado depois:** a reserva não muda.
- **Requisito:** [RF-24](../requisitos/rf-reservas.md#rf-24) (prevenção) e [RF-16](../requisitos/rf-reservas.md#rf-16) (nenhuma ação numa situação final).

#### <a id="e6-1"></a>E6.1 · Situação nova não informada

- **Condição:** no passo 6, o pedido de mudança chega sem a situação nova, ou com ela em branco. É conferido antes de procurar a reserva.
- **Resultado para o ator:** "Verifique os dados informados.", com a indicação, junto à situação, de que ela é obrigatória.
- **Estado depois:** a reserva não muda; nem é procurada.
- **Requisito:** [RF-25](../requisitos/rf-reservas.md#rf-25).

#### <a id="e6-2"></a>E6.2 · Reserva inexistente ou de outra pessoa

- **Condição:** no passo 6, a reserva não existe ou, para o Solicitante, é de outra pessoa.
- **Resultado para o ator:** "Reserva de código «n» não encontrada." — a **mesma** resposta nos dois casos, para não revelar que a reserva de outra pessoa existe. O ator atualiza a lista.
- **Estado depois:** nenhuma reserva muda.
- **Requisito:** [RF-23](../requisitos/rf-reservas.md#rf-23).

#### <a id="e6-3"></a>E6.3 · Situação desconhecida

- **Condição:** no passo 6, a situação nova não é uma das situações de reserva.
- **Resultado para o ator:** junto à situação, "Situação inválida. Escolha uma destas: Solicitada, Confirmada, Recusada, Cancelada, Concluída."
- **Estado depois:** a reserva não muda.
- **Requisito:** [RF-25](../requisitos/rf-reservas.md#rf-25).

#### <a id="e6-4"></a>E6.4 · Perfil sem permissão para a ação

- **Condição:** no passo 6, o Solicitante pede para confirmar, recusar ou concluir uma reserva própria (só o Gestor leva a essas situações; [`DESTINOS_POR_PAPEL`](../glossario.md#transicao-de-situacao)).
- **Resultado para o ator:** "Somente o gestor pode «confirmar | recusar | concluir» reservas." A resposta é a mesma qualquer que seja a situação atual.
- **Estado depois:** a reserva não muda.
- **Requisito:** [RF-27](../requisitos/rf-reservas.md#rf-27).

#### <a id="e6-5"></a>E6.5 · Transição não permitida

- **Condição:** no passo 6, a tabela não permite ir da situação atual para a pedida: por exemplo, concluir uma Solicitada, confirmar uma Confirmada, voltar a Solicitada, ou qualquer mudança a partir de uma situação final.
- **Resultado para o ator:** "Não é possível alterar uma reserva «situação atual» para «situação pedida»."
- **Estado depois:** a reserva continua na situação atual, com o mesmo motivo e o mesmo histórico.
- **Requisito:** [RF-24](../requisitos/rf-reservas.md#rf-24).

#### <a id="e6-6"></a>E6.6 · Motivo longo demais

- **Condição:** no passo 6, o motivo informado passa de 300 caracteres depois de tirar os espaços das pontas e os repetidos, em **qualquer** ação (inclusive confirmar e concluir, em que o motivo é opcional).
- **Resultado para o ator:** junto ao motivo, 'O campo "Motivo" deve ter no máximo 300 caracteres.'
- **Estado depois:** a reserva não muda.
- **Requisito:** [RF-26](../requisitos/rf-reservas.md#rf-26) (recusar e cancelar); ao confirmar e concluir, o limite não está em RF nenhum: [lacuna L-13](../requisitos/srs.md#l-13).

#### <a id="e6-7"></a>E6.7 · Motivo ausente ao recusar ou cancelar

- **Condição:** no passo 6 de UC-18 ou UC-11, o motivo não foi informado ou só tem espaços.
- **Resultado para o ator:** junto ao motivo, "Informe o motivo para recusar ou cancelar a reserva."
- **Estado depois:** a reserva não muda.
- **Requisito:** [RF-26](../requisitos/rf-reservas.md#rf-26).

#### <a id="e7-1"></a>E7.1 · Leitura desatualizada: outra pessoa alterou antes

- **Condição:** no passo 7, outra mudança da mesma reserva foi gravada depois que o ator a leu (dois decidindo ao mesmo tempo, ou uma lista antiga). Só a primeira grava.
- **Resultado para o ator:** "Esta reserva já está «situação atual»: ela foi alterada enquanto você decidia. Atualize a lista e tente de novo." O ator atualiza a reserva e decide de novo sobre o estado real.
- **Estado depois:** vale só a mudança que chegou primeiro; a segunda não grava situação, motivo nem registro, e o histórico continua um caminho coerente da tabela.
- **Requisito:** [RNF-R04](../requisitos/rnf.md#rnf-r04) (não há RF "Recusar…" para este caso; a garantia é de confiabilidade).

**Fora das exceções:** sem identificação, o pedido não chega ao passo 1 (precondição; [UC-02 E4.1](UC-02-autenticar.md#e4-1)). Dados extras no pedido (outro solicitante, outra data) são ignorados: só a situação e o motivo são lidos ([RNF-F09](../requisitos/rnf.md#rnf-f09)). A [DEC-13](../decisoes/DEC-13.md) hoje não gera exceção; se a opção b, c ou d for adotada, nasce uma exceção nova no passo 6, depois de [E6.5](#e6-5) (por exemplo, "concluir antes do término").

## Pós-condições e garantias

| Campo | Conteúdo |
|---|---|
| **Pós-condições (sucesso)** | A reserva está na situação nova, com o motivo informado (ou sem motivo, se não foi informado e não era exigido). O histórico ganhou exatamente um registro, da situação anterior para a nova, com autor, momento e motivo. Se a nova situação é final (Recusada, Cancelada, Concluída), a reserva deixa de ocupar o horário, que volta a aceitar pedidos, e não tem mais nenhuma ação disponível. |
| **Garantia de sucesso** | A mudança é uma das permitidas pela tabela e pelo perfil, foi feita sobre o estado real da reserva e está registrada com quem decidiu, quando e por quê. |
| **Garantia mínima** | Mesmo quando a meta falha: a reserva fica exatamente como estava (situação, motivo e histórico); nenhuma tentativa recusada vira registro; uma reserva de outra pessoa não é revelada ao Solicitante; de duas decisões simultâneas, nenhuma é perdida em silêncio (a segunda é recusada e informada). |

## Regras de negócio

- [Situação da reserva](../glossario.md#situacao), [transição de situação](../glossario.md#transicao-de-situacao) (`TRANSICOES_PERMITIDAS`, tabela única), [situação final](../glossario.md#situacao-final), [ação disponível](../glossario.md#acao-disponivel).
- Quem pode levar a cada situação (`DESTINOS_POR_PAPEL`): Gestor → Confirmada, Recusada, Concluída, Cancelada; Solicitante → Cancelada, só na própria. [Perfil](../glossario.md#perfil), [DEC-04](../decisoes/DEC-04.md).
- [Motivo](../glossario.md#motivo): obrigatório para recusar e cancelar, até 300 caracteres em qualquer ação, normalizado.
- [Reserva que ocupa horário](../glossario.md#reserva-que-ocupa-horario): só Solicitada e Confirmada.
- [Reserva desatualizada](../glossario.md#reserva-desatualizada): a situação gravada precisa ser a lida.
- [Histórico](../glossario.md#historico) e [registro de situação](../glossario.md#registro-de-situacao): só mudanças aceitas, na mesma gravação, imutáveis ([DEC-05](../decisoes/DEC-05.md)).
- Visibilidade: o Gestor vê todas; o Solicitante, só as próprias; a de outra pessoa é tratada como inexistente.

## RFs cobertos

Todos os RF que a [rastreabilidade RF → UC](README.md#rastreabilidade-rf--uc) atribui a UC-10, aos filhos UC-11, UC-17, UC-18 e UC-19 e às subfunções UC-12 e UC-13.

| RF | Título | Onde entra nesta ficha |
|---|---|---|
| [RF-17](../requisitos/rf-reservas.md#rf-17) | Confirmar reserva | fluxo principal, [passos 1 a 8](#p1), variação [UC-17](#v-uc-17) |
| [RF-18](../requisitos/rf-reservas.md#rf-18) | Recusar reserva com motivo | fluxo principal, [passos 1 a 8](#p1), variação [UC-18](#v-uc-18) |
| [RF-19](../requisitos/rf-reservas.md#rf-19) | Concluir reserva | fluxo principal, [passos 1 a 8](#p1), variação [UC-19](#v-uc-19) |
| [RF-20](../requisitos/rf-reservas.md#rf-20) | Cancelar reserva (Gestor) | fluxo principal, [passos 1 a 8](#p1), variação [UC-11](#v-uc-11) |
| [RF-21](../requisitos/rf-reservas.md#rf-21) | Cancelar a própria reserva (Solicitante) | fluxo principal, [passos 1 a 8](#p1), variação [UC-11](#v-uc-11) |
| [RF-22](../requisitos/rf-reservas.md#rf-22) | Consultar o histórico da reserva | [passo 7](#p7) (UC-13 grava a mudança que UC-09 mostra) |
| [RF-23](../requisitos/rf-reservas.md#rf-23) | Recusar operação sobre reserva inexistente ou de outra pessoa | [E6.2](#e6-2) |
| [RF-24](../requisitos/rf-reservas.md#rf-24) | Recusar transição de situação não permitida | [E6.5](#e6-5); prevenção em [E2.1](#e2-1) |
| [RF-25](../requisitos/rf-reservas.md#rf-25) | Recusar situação ausente ou desconhecida | [E6.1](#e6-1), [E6.3](#e6-3) |
| [RF-26](../requisitos/rf-reservas.md#rf-26) | Recusar recusa ou cancelamento sem motivo válido | [E6.6](#e6-6), [E6.7](#e6-7) (UC-12) |
| [RF-27](../requisitos/rf-reservas.md#rf-27) | Recusar mudança de situação que o perfil não pode fazer | [E6.4](#e6-4) |

Também aparece aqui, sem ser atribuído a UC-10: [RF-16](../requisitos/rf-reservas.md#rf-16) (ações disponíveis, de [UC-07](fichas-resumidas.md#uc-07)) no [passo 2](#p2) e em [E2.1](#e2-1). [RF-38](../requisitos/rf-gerais.md#rf-38) é transversal ([passo 8](#p8) e todas as exceções).

## RNFs relacionados

| RNF | Onde pesa nesta ficha |
|---|---|
| [RNF-F04](../requisitos/rnf.md#rnf-f04) · Identificação obrigatória por padrão | precondição |
| [RNF-F06](../requisitos/rnf.md#rnf-f06) · Privacidade das reservas de outras pessoas | [E6.2](#e6-2) |
| [RNF-F08](../requisitos/rnf.md#rnf-f08) · Perfil relido a cada operação | [passo 2](#p2), [E6.4](#e6-4): vale o perfil atual, não o da entrada |
| [RNF-F09](../requisitos/rnf.md#rnf-f09) · Identidade e perfil nunca vêm do pedido | [passo 7](#p7) (autor = ator) |
| [RNF-U01](../requisitos/rnf.md#rnf-u01) · Mensagens em português que orientam a correção | todas as exceções |
| [RNF-U05](../requisitos/rnf.md#rnf-u05) · Situação nunca indicada só por cor | [passo 2](#p2), [passo 8](#p8) |
| [RNF-R02](../requisitos/rnf.md#rnf-r02) · Histórico completo e na mesma gravação | [passo 7](#p7) |
| [RNF-R03](../requisitos/rnf.md#rnf-r03) · Operação recusada não muda nada | garantia mínima |
| [RNF-R04](../requisitos/rnf.md#rnf-r04) · Alteração sobre leitura desatualizada é recusada | [E7.1](#e7-1) |
| [RNF-R05](../requisitos/rnf.md#rnf-r05) · Nada é excluído | não há ação de excluir reserva nem registro |
| [RNF-R06](../requisitos/rnf.md#rnf-r06) · Nenhuma regra violada vira erro interno | todas as exceções |

## Questões em aberto

| DEC | Como afeta este caso de uso |
|---|---|
| [DEC-13](../decisoes/DEC-13.md) · Mudança de situação × horário | Hoje nenhuma mudança depende do horário. As opções b, c e d criariam exceções novas no passo 6 (concluir antes do término; confirmar, recusar ou cancelar depois do início) e mudariam as [ações disponíveis](#p2) conforme o horário. |
| [DEC-05](../decisoes/DEC-05.md) · Histórico só com mudanças efetivas | Se as tentativas recusadas passarem a ser registradas, a garantia mínima muda: as exceções do passo 6 passariam a gravar um registro (ou um log técnico). |
| [DEC-06](../decisoes/DEC-06.md) · Reservas de um espaço desativado | É por UC-11 (cancelar, pelo Gestor) que as reservas de um espaço desativado são desfeitas; a desativação não as muda. |
| [DEC-04](../decisoes/DEC-04.md) · Autenticação e perfis (decidida) | Define os atores de cada variação. |

O limite do motivo ao confirmar e concluir ([E6.6](#e6-6)) não está escrito em nenhum RF: [lacuna L-13](../requisitos/srs.md#l-13).

## Anexo — Evidência (complementar)

Ponte para os critérios e testes de aceite (REQ-05 e REQ-06). Testes a partir de `src/backend/`, salvo os do frontend (`src/frontend/src/`); `[x]` = teste parametrizado. Fontes: [`testes_de_reservas.md`](../../testes_de_reservas.md), [`matriz_de_acesso.md`](../../matriz_de_acesso.md) e [rf-reservas](../requisitos/rf-reservas.md).

| Item | Testes que o comprovam |
|---|---|
| [Fluxo principal](#p1) | `reservas/tests/test_api_situacao_reserva.py::test_confirmar_responde_200_com_a_reserva_atualizada`, `::test_fluxo_da_demonstracao_ate_concluida`, `::test_mensagem_de_sucesso_usa_o_rotulo_da_nova_situacao [x]`; `reservas/tests/test_alterar_situacao.py::test_transicao_permitida_e_persistida [x]`, `::test_ciclo_solicitada_confirmada_concluida`; `reservas/tests/test_propriedades_da_reserva.py::TestMaquinaDaReserva` |
| [Passo 2](#p2) (ações disponíveis) | `reservas/tests/test_api_situacao_reserva.py::test_reserva_solicitada_traz_confirmar_recusar_e_cancelar`, `::test_reserva_confirmada_traz_cancelar_e_concluir`; `reservas/tests/test_api_permissoes.py::test_acoes_do_solicitante_na_propria_solicitada_sao_so_cancelar`, `::test_acoes_do_gestor_na_solicitada_sao_confirmar_recusar_e_cancelar`; `reservas/tests/test_permissoes_reserva.py::test_acoes_permitidas_contem_o_destino_so_quando_a_alteracao_e_aceita [x]`; `components/reservas/TabelaDeReservas.test.tsx` |
| [Passo 7](#p7) (UC-13) | `reservas/tests/test_reserva.py::test_transicao_permitida_gera_o_registro_da_mudanca [x]`; `reservas/tests/test_alterar_situacao.py::test_registro_da_mudanca_usa_o_relogio_injetado_e_o_ator`; `reservas/tests/test_api_historico.py::test_fluxo_completo_aparece_no_historico_em_ordem`, `::test_cancelamento_aparece_com_o_motivo` |
| Variação [UC-17](#v-uc-17) | `reservas/tests/test_api_permissoes.py::test_gestor_confirma`; `reservas/tests/test_reserva.py::test_motivo_opcional_ao_confirmar_e_guardado_normalizado` |
| Variação [UC-18](#v-uc-18) | `reservas/tests/test_api_situacao_reserva.py::test_mensagem_de_sucesso_usa_o_rotulo_da_nova_situacao [recusada]`; `reservas/tests/test_conflito_de_horario.py::test_sobreposicao_com_reserva_que_nao_ocupa_horario_e_aceita [x]` |
| Variação [UC-19](#v-uc-19) | `reservas/tests/test_api_situacao_reserva.py::test_fluxo_da_demonstracao_ate_concluida`, `::test_reserva_concluida_nao_traz_acoes` |
| Variação [UC-11](#v-uc-11) | `reservas/tests/test_api_permissoes.py::test_solicitante_cancela_a_propria`; `reservas/tests/test_alterar_situacao.py::test_solicitante_cancela_a_propria_reserva`, `::test_cancelar_guarda_o_motivo_normalizado`; `reservas/tests/test_api_situacao_reserva.py::test_cancelar_libera_o_horario_para_nova_reserva` |
| [A8.1](#a8-1) | `reservas/tests/test_reserva.py::test_motivo_opcional_ao_confirmar_e_guardado_normalizado`, `::test_nova_situacao_limpa_o_motivo_da_anterior` |
| [E2.1](#e2-1) | `reservas/tests/test_api_situacao_reserva.py::test_reserva_concluida_nao_traz_acoes`; `reservas/tests/test_api_permissoes.py::test_solicitante_numa_concluida_nao_tem_acoes` |
| [E6.1](#e6-1), [E6.3](#e6-3) | `reservas/tests/test_api_situacao_reserva.py::test_situacao_ausente_ou_invalida_responde_400 [x]`; `reservas/tests/test_alterar_situacao.py::test_situacao_desconhecida_lanca_erro_e_preserva_a_reserva`; `reservas/tests/test_reserva.py::test_situacao_desconhecida_e_recusada_e_nada_muda` |
| [E6.2](#e6-2) | `reservas/tests/test_api_situacao_reserva.py::test_reserva_inexistente_responde_404`; `reservas/tests/test_api_permissoes.py::test_solicitante_cancelando_a_de_outra_pessoa_responde_404_sem_mudar_nada`; `reservas/tests/test_alterar_situacao.py::test_reserva_de_outra_pessoa_para_o_solicitante_lanca_nao_encontrada`; `reservas/tests/test_permissoes_reserva.py::test_quem_nao_ve_a_reserva_recebe_nao_encontrada_com_o_codigo_dela` |
| [E6.4](#e6-4) | `reservas/tests/test_api_permissoes.py::test_solicitante_confirmando_a_propria_responde_403_sem_mudar_nada`; `reservas/tests/test_permissoes_reserva.py::test_alterar_situacao_segue_a_matriz_e_preserva_a_reserva_nos_erros [x]`, `::test_solicitante_concluindo_uma_solicitada_recebe_403_e_nao_409`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]` |
| [E6.5](#e6-5) | `reservas/tests/test_api_situacao_reserva.py::test_transicao_proibida_responde_409_e_preserva_a_reserva`, `::test_reserva_concluida_nao_pode_ser_cancelada`; `reservas/tests/test_reserva.py::test_transicao_proibida_e_recusada_e_preserva_a_situacao [x]`, `::test_transicao_proibida_tem_mensagem_com_os_rotulos`; `reservas/tests/test_situacao.py::test_transicao_permitida_segue_a_tabela [x]`; `reservas/tests/test_permissoes_reserva.py::test_solicitada_como_destino_e_transicao_invalida_para_os_dois_papeis [x]` |
| [E6.6](#e6-6) | `reservas/tests/test_reserva.py::test_motivo_acima_do_limite_e_recusado_e_nada_muda`; `reservas/tests/test_propriedades_da_reserva.py::TestMaquinaDaReserva` (motivo acima do limite em qualquer destino) |
| [E6.7](#e6-7) | `reservas/tests/test_api_situacao_reserva.py::test_recusar_sem_motivo_responde_400_no_campo_motivo`; `reservas/tests/test_reserva.py::test_recusar_ou_cancelar_sem_motivo_e_recusado_e_nada_muda [x]`; `reservas/tests/test_alterar_situacao.py::test_recusar_ou_cancelar_sem_motivo_lanca_erro_e_preserva_a_reserva [x]` |
| [E7.1](#e7-1) | `reservas/tests/test_repositorio_reservas.py::test_alteracao_sobre_leitura_desatualizada_e_recusada_sem_gravar`, `::test_salvar_entidade_que_ficou_para_tras_nao_regride_a_situacao`, `::test_salvar_reserva_existente_bloqueia_a_linha`; `reservas/tests/test_concorrencia_de_situacao.py::test_alteracoes_simultaneas_gravam_so_uma_e_o_historico_fica_coerente`; `reservas/tests/test_reserva.py::test_reserva_desatualizada_vira_409_com_a_situacao_atual` |
| Nenhuma exceção registra | `reservas/tests/test_reserva.py::test_alteracao_recusada_nao_muda_nada_nem_registra [x]`; `reservas/tests/test_alterar_situacao.py::test_alteracao_recusada_nao_registra_no_historico`; `reservas/tests/test_api_historico.py::test_tentativa_recusada_nao_aparece_no_historico` |

<a id="evidencia-da-ordem"></a>**Ordem das exceções.** E6.1 vem antes de procurar a reserva porque o formato do pedido é conferido primeiro (`ReservaSituacaoView.patch` valida a entrada e só então chama `AlterarSituacaoReserva`). E6.2 → E6.3 → E6.4 → E6.5 → E6.6 → E6.7 é a ordem de `Reserva.alterar_situacao` (visibilidade, conversão da situação, `_exigir_permissao`, `transicao_permitida`, `_normalizar_motivo`, `_exigir_motivo_se_necessario`), fixada por `reservas/tests/test_permissoes_reserva.py::test_alterar_situacao_segue_a_matriz_e_preserva_a_reserva_nos_erros [x]` e `::test_solicitante_concluindo_uma_solicitada_recebe_403_e_nao_409` (perfil antes da transição). E7.1 só pode acontecer na gravação (`RepositorioReservasDjango.salvar`, com a linha bloqueada).

**Histórias derivadas:** [US-13 Cancelar uma reserva](../historias/US-13-cancelar-uma-reserva.md), [US-14 Confirmar uma reserva](../historias/US-14-confirmar-uma-reserva.md), [US-15 Recusar uma reserva com motivo](../historias/US-15-recusar-uma-reserva.md), [US-16 Concluir uma reserva](../historias/US-16-concluir-uma-reserva.md) (uma por variação; [A1.1](#a1-1) também em US-11 e US-12). Cobertura de cada alternativa e exceção: [historias/README.md](../historias/README.md#cobertura-uc--usca).
