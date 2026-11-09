# Especificação de Requisitos de Software (SRS) — Conecta Campus

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **SRS-01 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/requisitos/srs.md` |

Modelo: estrutura de SRS do A3·s8 (introdução, descrição geral, requisitos funcionais, interfaces, qualidade e restrições, rastreabilidade) com o cabeçalho do template de documento de projeto (A4·s11). As fichas de cada requisito (A4·s9) ficam nos arquivos de área listados na [seção 3](#3-requisitos-funcionais) e na [seção 5](#5-qualidade-e-restrições); este documento é o índice e a rastreabilidade deles.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Criação: RF-01 a RF-40 (60 fichas), RNF-F01 a RNF-S06 (31 fichas), restrições, priorização QFD, lacunas, auditoria e rastreabilidade (REQ-02). Sem aprovação. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Coluna UC da seção 6.4 preenchida e vínculos UC das fichas, a partir do [diagrama e do índice de casos de uso](../casos-de-uso/README.md) (REQ-03). Sem aprovação. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Lacunas L-12 a L-14, achadas ao escrever as [fichas de caso de uso](../casos-de-uso/README.md#fichas-dos-casos-de-uso); auditoria do RF-11, RF-17, RF-26 e RF-33.1 e resumo recontado; textos sobre US e CA apontam para a REQ-05 (REQ-04). Coluna UC da 6.4 sem mudança. Sem aprovação. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Colunas US e CA da 6.4 preenchidas a partir das [histórias](../historias/README.md); lacunas L-15 e L-16 (CA sem TA automatizado); L-08 ligada à US-19; a introdução, o "Como ler", a 6.4 e a auditoria do RF-01 apontam para as histórias (REQ-05). Sem aprovação. |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Seção 6 aponta para a [matriz de rastreabilidade gerada](../rastreabilidade/README.md); a 6.4 fica só com o teste representativo (UC, US, CA e TA saem da matriz); "Como ler" cita o campo Código (complementar) das fichas; lacuna L-17 (tela de endereço desconhecido sem RF), achada no sentido inverso da matriz (REQ-06). Sem aprovação. |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | L-12 com a ordem real entre o espaço e a finalidade (o espaço primeiro), corrigida também na ficha de UC-04 (DOC-03). Sem aprovação. |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | L-03 e L-04 apontam para as limitações conhecidas do README da raiz, com a divisão do README (DOC-09). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Respostas da Aula 7 (GES-02): 6.3 com as DECs decididas e as DEC-14 a DEC-23; L-01, L-02 e L-06 passam a CR-01, CR-02 e CR-04, e a L-05 fica aceita com a DEC-12 decidida; referências, premissas, "Como ler" (DEC-16) e a coluna de ações da auditoria apontam para as decisões e os CRs. Mudança editorial: nenhum enunciado, regra ou critério de aceite muda (os CRs mudam na RES-11, RES-12, ESP-07 e AUT-12). Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | AUT-08: RF-33.2 e RNF-F12 nas tabelas (resumo, 5, 6.1, 6.2, 6.4, QFD e auditoria; 61 RF e 32 RNF); a lacuna L-03 passa a resolvida; a L-14 aponta para UC-02 E3.2, renumerada; TAs citados renumerados (TA-12 a TA-156 passam a TA-13 a TA-157). Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | AUT-08: auditoria do RNF-F12 e L-03 com o contador no Redis; RF-40 passa a conferir também o cache. Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | AUT-09: RNF-F13 nas tabelas (5, 6.3 e auditoria; 33 RNF); RNF-F04 com 8 operações públicas; a L-04 passa a cobrir só a credencial de acesso, porque sair revoga a de renovação; auditoria e evidência (6.4) do RF-36; TAs citados renumerados (TA-19 e TA-20 passam a TA-20 e TA-21; TA-21 a TA-158 passam a TA-24 a TA-161). Sem aprovação. |

## Sumário

1. [Introdução](#1-introdução)
2. [Descrição geral](#2-descrição-geral)
3. [Requisitos funcionais](#3-requisitos-funcionais)
4. [Interfaces](#4-interfaces)
5. [Qualidade e restrições](#5-qualidade-e-restrições)
6. [Rastreabilidade](#6-rastreabilidade)
7. [Análise QFD](#7-análise-qfd)
8. [Lacunas](#lacunas)
9. [Auditoria de qualidade](#9-auditoria-de-qualidade)
10. [Checklist de revisão por pares](#10-checklist-de-revisão-por-pares)

No sumário do template A4·s11, este documento cobre a parte 3 (RF e RNF), a parte das interfaces da 4 e a rastreabilidade da 5. O diagrama e o índice dos casos de uso estão em [`casos-de-uso/`](../casos-de-uso/README.md) (REQ-03); as fichas dos casos de uso estão na mesma pasta (REQ-04); as histórias, os critérios e os testes de aceite estão em [`historias/`](../historias/README.md) (REQ-05).

---

## 1. Introdução

### Propósito

Esta SRS diz **o que** o Conecta Campus faz (requisitos funcionais) e **como** ele se comporta (requisitos não funcionais), com um identificador estável por obrigação, para que quem implementa, testa, avalia ou muda o sistema consiga agir sem adivinhar. Ela descreve o **comportamento real** do sistema nesta versão, conferido nos testes automatizados; o que uma necessidade pede e o sistema não faz aparece como [lacuna](#lacunas), não como requisito cumprido.

Leitores: a equipe do projeto (Grupo 03), o professor das duas disciplinas e quem fizer a revisão por pares da versão 0.2.

### Escopo

O escopo é o da [Visão (VIS-01)](../visao.md#3-escopo-inicial-do-sistema): o cadastro de espaços esportivos, o pedido de reserva de um espaço num intervalo de um dia, a consulta dos pedidos, a decisão do Gestor sobre cada pedido e o histórico de cada decisão, com identificação por perfil. A lista "fora do escopo" da Visão vale aqui sem mudança: nada desta SRS a amplia.

### Definições

Os termos do domínio (espaço reservável, reserva que ocupa horário, ação disponível, agenda do dia…) têm **definição única** no [Glossário (GLO-01)](../glossario.md), com o nome correspondente no código. Um termo usado aqui num sentido diferente do glossário é erro desta SRS.

Siglas: **NS** necessidade; **RF** requisito funcional; **RNF** requisito não funcional; **FURPS** Funcionalidade, Usabilidade, Confiabilidade (*Reliability*), Desempenho (*Performance*), Suportabilidade; **QFD** *Quality Function Deployment* (normal, esperado, fascinante); **F1** a **F6** as seis funcionalidades mínimas do enunciado de Projeto de Programação; **DEC** decisão; **CR** pedido de mudança; **UC**, **US**, **CA** caso de uso, história, critério de aceite.

### Referências

- [Documento de Visão (VIS-01)](../visao.md) — necessidades NS-01 a NS-16, atores, escopo, premissas, critérios de sucesso e riscos.
- [Glossário (GLO-01)](../glossario.md).
- [Decisões DEC-01 a DEC-23](../decisoes/README.md) e [pedidos de mudança](../mudancas/README.md) [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md) a [CR-04](../mudancas/CR-04-matricula-so-digitos.md).
- [README da fonte oficial](../README.md) — convenções de ID, versão, estado e rastreabilidade.
- Evidências do lado do código: [catálogo de testes de espaços](../../testes_de_espacos.md), [catálogo de testes de reservas](../../testes_de_reservas.md) e [matriz de acesso](../../matriz_de_acesso.md).
- Diretrizes da disciplina (A1 a A4) em `.claude/requisitos.md` (arquivo local, fora do Git) e enunciado de Projeto de Programação (Seção 5, funcionalidades mínimas).

## 2. Descrição geral

### Atores e perfis

Os mesmos da [Visão](../visao.md#2-usuários-atores-e-stakeholders). Um "usuário autenticado" é qualquer um dos dois perfis.

| Ator | Quem é | O que faz no sistema |
|---|---|---|
| [Visitante](../glossario.md#visitante) | Pessoa ainda não identificada. | Cadastra-se como Solicitante, entra e consulta o [vocabulário público](../glossario.md#vocabulario-publico) (tipos de espaço, situações e regras de agenda). |
| [Solicitante](../glossario.md#solicitante) | Aluno ou servidor com matrícula. | Consulta espaços, pede reservas em nome próprio, consulta e cancela as próprias, vê a agenda do dia. |
| [Gestor](../glossario.md#gestor) | Pessoa do setor dos espaços. | Tudo o que o Solicitante faz (pedindo em nome próprio), mais manter os espaços, consultar todas as reservas e confirmar, recusar, concluir ou cancelar qualquer uma. |
| [Equipe de TI](../glossario.md#equipe-de-ti) | Quem instala e administra. | Cria usuários Gestor e carrega os dados de exemplo. Não é ator dos casos de uso do negócio (Visão, seção 2). |

O cliente (a instituição) não opera o sistema e não é ator.

### Componentes, em linguagem de negócio

| Componente | Responsabilidade | RF |
|---|---|---|
| **Cadastro de espaços** | Manter a lista de espaços esportivos igual à realidade e dizer quais aceitam pedidos. | [RF-01 a RF-10](rf-espacos.md) |
| **Reservas** | Receber pedidos, impedir dois usos no mesmo período, registrar cada decisão e mostrar o histórico. | [RF-11 a RF-27](rf-reservas.md) |
| **Agenda** | Mostrar as regras de uso e o que está ocupado e livre num espaço e dia, antes do pedido. | [RF-28 a RF-31](rf-agenda.md) |
| **Contas e acesso** | Identificar quem age, com o perfil que define o que cada um pode fazer. | [RF-32 a RF-37](rf-contas.md) |
| **Mensagens e operação** | Dizer o resultado de toda operação; permitir instalar, verificar e demonstrar o sistema. | [RF-38 a RF-40](rf-gerais.md) |

Reservas consulta o cadastro de espaços para saber se um espaço é [reservável](../glossario.md#espaco-reservavel); o cadastro de espaços não conhece as reservas (por isso desativar um espaço não mexe nas reservas dele, [DEC-06](../decisoes/DEC-06.md)).

### Premissas e dependências

- As premissas P-01 a P-07 da [Visão](../visao.md#premissas) valem para toda a SRS. As que mais afetam os requisitos: P-01 (sem cliente real: os valores de regra são do grupo, com o professor como referência), P-03 (horário de Brasília), P-04 (regras de agenda iguais para todos os espaços, até o [CR-03](../mudancas/CR-03-horario-por-espaco.md) trazer o horário por espaço), P-05 (um pedido é de um espaço, num dia, num intervalo contínuo) e P-06 (Gestor criado só pela Equipe de TI).
- Dependências de decisão: as DEC-05 a DEC-13 foram decididas na Aula 7 (06/11/2026). As que mudam o comportamento seguem pelo fluxo de [CR](../README.md#como-propor-uma-mudança) e só mudam os requisitos quando a tarefa que implementa o CR for feita: DEC-13 ([CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md), RES-11), DEC-05 ([CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md), RES-12), DEC-07 ([CR-03](../mudancas/CR-03-horario-por-espaco.md), ESP-07) e DEC-09 ([CR-04](../mudancas/CR-04-matricula-so-digitos.md), AUT-12). Até lá, esta SRS descreve o comportamento atual. Índice: [`decisoes/`](../decisoes/README.md).
- Nenhuma dependência de sistema externo (seção 4).

## 3. Requisitos funcionais

### Como ler

- **Sintaxe (A3·s9):** "O sistema deve permitir ao [ator qualificado] [ação] e [resultado observável]." O resultado é algo que se vê (a reserva na situação Solicitada, o espaço inativo na lista), nunca "com sucesso".
- **Recusas (F5):** a recusa de uma operação inválida é uma obrigação do sistema diante de um pedido, não uma capacidade do ator. Por isso usa a sintaxe "O sistema deve impedir que o [ator] [ação inválida], sem alterar [o quê], e informar [o motivo e o campo]." São as únicas fichas que não começam com "O sistema deve permitir ao". RF-37 e RF-39 começam com "O sistema deve permitir à" só pela concordância com o ator ("à Equipe de TI"): é a mesma sintaxe.
- **Decomposição (A4·s8):** uma obrigação por ID. A recusa específica de uma operação é um filho `RF-xx.n` do RF da operação (ex.: [RF-11.4](rf-reservas.md#rf-11-4), conflito de horário no pedido). A recusa que vale para várias operações do mesmo item é um RF próprio, com as operações protegidas listadas na ficha (ex.: [RF-23](rf-reservas.md#rf-23), reserva inexistente ou de outra pessoa, que protege o detalhe, o histórico e a mudança de situação). Assim cada recusa tem um ID e uma evidência, sem repetir a mesma obrigação em várias fichas, e a F5 fica coberta por IDs próprios.
- **Ficha (A4·s9):** ID e título, enunciado, pai (filhos) ou operações protegidas (recusas comuns), origem (NS principal primeiro), funcionalidade do enunciado, prioridade QFD com justificativa, vínculos, evidência, regras de negócio (com link para o glossário), decisões, revisão, estado e responsável.
- **Vínculos:** o caso de uso em que o RF entra, com o papel dele (fluxo principal, alternativa, exceção ou transversal), definido na REQ-03 ([rastreabilidade RF → UC](../casos-de-uso/README.md#rastreabilidade-rf--uc)), e o passo, a alternativa ou a exceção exata na ficha do caso de uso (REQ-04); e as US e os CAs que o verificam, cada um com o seu TA ([histórias](../historias/README.md), REQ-05).
- **Evidência (complementar):** o endpoint ou a tela e o `arquivo::teste` que prova o comportamento. **Código (complementar)** (REQ-06): o caso de uso da aplicação e a regra do domínio que implementam o RF, como `arquivo::Símbolo`, conferidos por `scripts/gerar_rastreabilidade.py`. É uma extensão do grupo: a cadeia do professor para em CA/TA, e o professor confirmou que o elo até o código conta ([DEC-16](../decisoes/DEC-16.md)).
- **Estado:** todos em **Rascunho** (versão 0.1). Nenhum RF ficou "Não implementado": todas as NS têm comportamento implementado (ver [lacunas](#lacunas)).

### Tabela-resumo

F = funcionalidade do enunciado (F1 a F6) ou Extra. QFD: N normal, E esperado, Fa fascinante.

| ID | Título | NS | F | QFD | Estado |
|---|---|---|---|---|---|
| [RF-01](rf-espacos.md#rf-01) | Listar espaços | NS-01 | F1 | N | Rascunho |
| [RF-02](rf-espacos.md#rf-02) | Filtrar espaços | NS-01 | F1 | E | Rascunho |
| [RF-02.1](rf-espacos.md#rf-02-1) | Recusar filtro com tipo inexistente | NS-01 | F5 | E | Rascunho |
| [RF-03](rf-espacos.md#rf-03) | Consultar um espaço | NS-01 | F1 | N | Rascunho |
| [RF-04](rf-espacos.md#rf-04) | Consultar os tipos de espaço | NS-01 | F1 | E | Rascunho |
| [RF-05](rf-espacos.md#rf-05) | Cadastrar espaço | NS-02 | F1 | N | Rascunho |
| [RF-05.1](rf-espacos.md#rf-05-1) | Recusar espaço com dados inválidos | NS-02 | F5 | N | Rascunho |
| [RF-05.2](rf-espacos.md#rf-05-2) | Recusar nome de espaço repetido | NS-02 | F5 | E | Rascunho |
| [RF-06](rf-espacos.md#rf-06) | Editar espaço | NS-02 | Extra | E | Rascunho |
| [RF-06.1](rf-espacos.md#rf-06-1) | Recusar edição sem alteração | NS-02 | F5 | E | Rascunho |
| [RF-06.2](rf-espacos.md#rf-06-2) | Recusar edição que viola as regras do cadastro | NS-02 | F5 | E | Rascunho |
| [RF-07](rf-espacos.md#rf-07) | Desativar espaço | NS-02 | Extra | E | Rascunho |
| [RF-07.1](rf-espacos.md#rf-07-1) | Recusar desativar espaço já inativo | NS-02 | F5 | E | Rascunho |
| [RF-08](rf-espacos.md#rf-08) | Reativar espaço | NS-02 | Extra | E | Rascunho |
| [RF-08.1](rf-espacos.md#rf-08-1) | Recusar reativar espaço já ativo | NS-02 | F5 | E | Rascunho |
| [RF-09](rf-espacos.md#rf-09) | Recusar operação sobre espaço inexistente | NS-01 | F5 | N | Rascunho |
| [RF-10](rf-espacos.md#rf-10) | Recusar manutenção de espaço por quem não é Gestor | NS-11 | F5 | E | Rascunho |
| [RF-11](rf-reservas.md#rf-11) | Solicitar reserva | NS-03 | F2 | N | Rascunho |
| [RF-11.1](rf-reservas.md#rf-11-1) | Recusar pedido com dados inválidos | NS-03 | F5 | N | Rascunho |
| [RF-11.2](rf-reservas.md#rf-11-2) | Recusar pedido com data retroativa | NS-06 | F5 | E | Rascunho |
| [RF-11.3](rf-reservas.md#rf-11-3) | Recusar pedido para espaço que não é reservável | NS-03 | F5 | N | Rascunho |
| [RF-11.4](rf-reservas.md#rf-11-4) | Recusar pedido em conflito de horário | NS-04 | F5 | N | Rascunho |
| [RF-11.5](rf-reservas.md#rf-11-5) | Recusar pedido fora das regras de agenda | NS-06 | F5 | E | Rascunho |
| [RF-12](rf-reservas.md#rf-12) | Consultar reservas por critérios combináveis | NS-08 | F3 | N | Rascunho |
| [RF-12.1](rf-reservas.md#rf-12-1) | Recusar critério de consulta em formato inválido | NS-08 | F5 | E | Rascunho |
| [RF-13](rf-reservas.md#rf-13) | Consultar as próprias reservas | NS-07 | F3 | N | Rascunho |
| [RF-14](rf-reservas.md#rf-14) | Consultar o detalhe de uma reserva | NS-07 | F3 | N | Rascunho |
| [RF-15](rf-reservas.md#rf-15) | Consultar as situações de reserva | NS-08 | F3 | E | Rascunho |
| [RF-16](rf-reservas.md#rf-16) | Ver as ações disponíveis em cada reserva | NS-09 | F4 | E | Rascunho |
| [RF-17](rf-reservas.md#rf-17) | Confirmar reserva | NS-09 | F4 | N | Rascunho |
| [RF-18](rf-reservas.md#rf-18) | Recusar reserva com motivo | NS-09 | F4 | N | Rascunho |
| [RF-19](rf-reservas.md#rf-19) | Concluir reserva | NS-09 | F4 | N | Rascunho |
| [RF-20](rf-reservas.md#rf-20) | Cancelar reserva (Gestor) | NS-09 | F4 | N | Rascunho |
| [RF-21](rf-reservas.md#rf-21) | Cancelar a própria reserva (Solicitante) | NS-10 | F4 | E | Rascunho |
| [RF-22](rf-reservas.md#rf-22) | Consultar o histórico da reserva | NS-12 | Extra | N | Rascunho |
| [RF-23](rf-reservas.md#rf-23) | Recusar operação sobre reserva inexistente ou de outra pessoa | NS-14 | F5 | N | Rascunho |
| [RF-24](rf-reservas.md#rf-24) | Recusar transição de situação não permitida | NS-09 | F5 | N | Rascunho |
| [RF-25](rf-reservas.md#rf-25) | Recusar situação ausente ou desconhecida | NS-09 | F5 | N | Rascunho |
| [RF-26](rf-reservas.md#rf-26) | Recusar recusa ou cancelamento sem motivo válido | NS-09 | F5 | E | Rascunho |
| [RF-27](rf-reservas.md#rf-27) | Recusar mudança de situação que o perfil não pode fazer | NS-11 | F5 | E | Rascunho |
| [RF-28](rf-agenda.md#rf-28) | Consultar as regras de agenda | NS-06 | Extra | Fa | Rascunho |
| [RF-29](rf-agenda.md#rf-29) | Ver os horários ocupados de um espaço num dia | NS-05 | Extra | Fa | Rascunho |
| [RF-29.1](rf-agenda.md#rf-29-1) | Recusar consulta da agenda sem espaço ou sem data | NS-05 | F5 | E | Rascunho |
| [RF-29.2](rf-agenda.md#rf-29-2) | Recusar agenda de espaço que não é reservável | NS-05 | F5 | E | Rascunho |
| [RF-30](rf-agenda.md#rf-30) | Ver os horários livres de um espaço num dia | NS-05 | Extra | Fa | Rascunho |
| [RF-31](rf-agenda.md#rf-31) | Saber que uma data não é reservável | NS-05 | Extra | E | Rascunho |
| [RF-32](rf-contas.md#rf-32) | Cadastrar-se como Solicitante | NS-15 | Extra | E | Rascunho |
| [RF-32.1](rf-contas.md#rf-32-1) | Recusar cadastro com dados inválidos | NS-15 | F5 | E | Rascunho |
| [RF-32.2](rf-contas.md#rf-32-2) | Recusar senha fraca | NS-15 | F5 | E | Rascunho |
| [RF-32.3](rf-contas.md#rf-32-3) | Recusar e-mail ou matrícula já cadastrados | NS-15 | F5 | E | Rascunho |
| [RF-33](rf-contas.md#rf-33) | Entrar com e-mail e senha | NS-11 | Extra | E | Rascunho |
| [RF-33.1](rf-contas.md#rf-33-1) | Recusar credenciais inválidas | NS-11 | F5 | E | Rascunho |
| [RF-33.2](rf-contas.md#rf-33-2) | Recusar tentativas de entrada em excesso | NS-11 | F5 | E | Rascunho |
| [RF-34](rf-contas.md#rf-34) | Continuar identificado sem informar a senha de novo | NS-11 | Extra | E | Rascunho |
| [RF-34.1](rf-contas.md#rf-34-1) | Encerrar a sessão expirada | NS-11 | F5 | E | Rascunho |
| [RF-35](rf-contas.md#rf-35) | Consultar os próprios dados | NS-11 | Extra | E | Rascunho |
| [RF-36](rf-contas.md#rf-36) | Sair | NS-11 | Extra | E | Rascunho |
| [RF-37](rf-contas.md#rf-37) | Criar usuário Gestor | NS-11 | Extra | N | Rascunho |
| [RF-38](rf-gerais.md#rf-38) | Ver o resultado de cada operação | NS-13 | F6 | N | Rascunho |
| [RF-39](rf-gerais.md#rf-39) | Carregar dados de exemplo | NS-16 | Extra | E | Rascunho |
| [RF-40](rf-gerais.md#rf-40) | Verificar se o sistema está no ar | NS-16 | Extra | E | Rascunho |

**Contagem:** 61 fichas (40 RF principais e 21 filhos). Por área: espaços 17, reservas 23, agenda 6, contas 12, mensagens e operação 3.

## 4. Interfaces

### 4.1 Com o usuário

Telas no navegador, em português (premissa P-07). Descrição do que cada tela permite, sem desenho; os detalhes de interação ficam para os casos de uso (REQ-04).

| Tela | Quem usa | O que permite | RF |
|---|---|---|---|
| Início (`/`) | Todos | Ver se o sistema está no ar; ir para entrar, criar conta ou, identificado, para as próprias reservas. | RF-40, RF-33, RF-32 |
| Entrar (`/entrar`) | Visitante | Entrar com e-mail e senha e voltar à tela de onde veio. | RF-33, RF-33.1 |
| Cadastro (`/cadastro`) | Visitante | Criar a conta de Solicitante e já entrar. | RF-32 e filhos |
| Espaços (`/espacos`) | Usuário autenticado | Listar e filtrar espaços; ir para o pedido num espaço ativo. Só o Gestor: cadastrar, editar, desativar e reativar. | RF-01 a RF-10 |
| Nova reserva (`/reservas/nova`) | Usuário autenticado | Pedir uma reserva, ver as regras de agenda e a agenda do dia do espaço escolhido, usar um horário livre e ver o resumo do pedido criado. | RF-11 e filhos, RF-28 a RF-31 |
| Reservas (`/reservas`; "Minhas reservas" para o Solicitante) | Usuário autenticado | Consultar reservas pelos critérios do perfil e mudar a situação pelas ações disponíveis de cada uma. | RF-12, RF-13, RF-16 a RF-21 |
| Detalhe da reserva (`/reservas/:reservaId`) | Usuário autenticado | Ver os dados da reserva, as ações disponíveis e o histórico. | RF-14, RF-16 a RF-22 |
| Administração (`/admin/`) | Equipe de TI | Criar usuários Gestor e manter usuários. | RF-37 |

Em todas as telas, o resultado de cada operação aparece como mensagem ([RF-38](rf-gerais.md#rf-38)); usabilidade em [RNF-U01 a RNF-U06](rnf.md#2-usabilidade-u).

### 4.2 Com outros sistemas

- **Nenhuma integração externa.** O Conecta Campus não troca dados com sistemas da instituição (cadastro acadêmico, login institucional), de pagamento nem de notificação: tudo isso está [fora do escopo](../visao.md#fora-do-escopo). A matrícula não é conferida com a instituição ([DEC-09](../decisoes/DEC-09.md)).
- **Interface própria (API REST em JSON)**, usada pelas telas e chamada diretamente pelos testes de API:
  - Sucesso: `{"mensagem": "...", "dados": {...}}`.
  - Erro: `{"erro": {"codigo": "...", "mensagem": "...", "campos": {"<campo>": ["..."]}}}`, com `campos` só quando a recusa vem de um campo.
  - Status por categoria: 400 dados inválidos, 401 sem identificação, 403 perfil sem permissão, 404 não encontrado, 405 operação inexistente, 409 conflito com o estado atual, 500 erro interno sem detalhes, 503 banco fora do ar (só na verificação do sistema).

| Método e caminho | RF |
|---|---|
| `GET /api/health/` | RF-40 |
| `POST /api/auth/cadastro/` · `POST /api/auth/login/` · `POST /api/auth/refresh/` · `GET /api/auth/me/` | RF-32 · RF-33 · RF-34 · RF-35 |
| `GET /api/espacos/` · `POST /api/espacos/` | RF-01, RF-02 · RF-05 |
| `GET /api/espacos/tipos/` | RF-04 |
| `GET /api/espacos/{id}/` · `PATCH /api/espacos/{id}/` | RF-03 · RF-06 |
| `POST /api/espacos/{id}/desativar/` · `POST /api/espacos/{id}/ativar/` | RF-07 · RF-08 |
| `GET /api/reservas/` · `POST /api/reservas/` | RF-12, RF-13 · RF-11 |
| `GET /api/reservas/situacoes/` · `GET /api/reservas/regras-de-agenda/` | RF-15 · RF-28 |
| `GET /api/reservas/ocupacao/?espaco=&data=` | RF-29 a RF-31 |
| `GET /api/reservas/{id}/` · `GET /api/reservas/{id}/historico/` | RF-14 · RF-22 |
| `PATCH /api/reservas/{id}/situacao/` | RF-17 a RF-21 |

Quem pode chamar cada rota: [matriz de acesso](../../matriz_de_acesso.md) ([RNF-F04](rnf.md#rnf-f04)).

### 4.3 De comunicação

HTTP na própria máquina: telas em `http://localhost:5173` e API em `http://localhost:8000`, com o banco de dados na rede interna do ambiente de execução. A identificação vai no cabeçalho de cada chamada ([RNF-F03](rnf.md#rnf-f03), [RNF-F10](rnf.md#rnf-f10)); só a origem das telas é autorizada pelo navegador ([RNF-F11](rnf.md#rnf-f11)). Não há HTTPS porque a execução é local ([restrição REST-05](rnf.md#6-restrições)).

## 5. Qualidade e restrições

Fichas completas em [`rnf.md`](rnf.md). "Cliente" = ✔ quando é um RNF que o cliente não pediria (A3·s27).

| ID | FURPS | Título | Métrica e valor-alvo | Cliente | Estado |
|---|---|---|---|---|---|
| [RNF-F01](rnf.md#rnf-f01) | F | Senha guardada só como hash | 0 senhas em texto no banco ou nas respostas | ✔ | Rascunho |
| [RNF-F02](rnf.md#rnf-f02) | F | Política de senha | 100% das senhas < 8, numéricas, comuns ou parecidas com os dados recusadas | ✔ | Rascunho |
| [RNF-F03](rnf.md#rnf-f03) | F | Validade da sessão | acesso 30 min; renovação 1 dia | ✔ | Rascunho |
| [RNF-F04](rnf.md#rnf-f04) | F | Identificação obrigatória por padrão | 8 operações públicas; 100% das rotas na matriz | — | Rascunho |
| [RNF-F05](rnf.md#rnf-f05) | F | Credenciais inválidas não revelam contas | resposta idêntica nos 3 casos | ✔ | Rascunho |
| [RNF-F06](rnf.md#rnf-f06) | F | Privacidade das reservas de outras pessoas | 0 campos pessoais alheios; 100% de 404 na reserva alheia | — | Rascunho |
| [RNF-F07](rnf.md#rnf-f07) | F | Conta desativada perde o acesso na hora | 100% recusadas com 401 | ✔ | Rascunho |
| [RNF-F08](rnf.md#rnf-f08) | F | Perfil relido a cada operação | 0 operações com o perfil antigo | ✔ | Rascunho |
| [RNF-F09](rnf.md#rnf-f09) | F | Identidade e perfil nunca vêm do pedido | 0 reservas com outro solicitante; 0 Gestores pelo cadastro | ✔ | Rascunho |
| [RNF-F10](rnf.md#rnf-f10) | F | Credenciais forjadas recusadas | 100% recusadas com 401 | ✔ | Rascunho |
| [RNF-F11](rnf.md#rnf-f11) | F | Só a origem configurada acessa a API pelo navegador | 0 autorizações a outra origem | ✔ | Rascunho |
| [RNF-F12](rnf.md#rnf-f12) | F | Limite de tentativas de entrada e de cadastro | entrada 5/min por e-mail e 20/min por origem; cadastro 10/h por origem | ✔ | Rascunho |
| [RNF-F13](rnf.md#rnf-f13) | F | Revogação e troca da credencial de renovação | 100% das renovações com credencial revogada ou trocada recusadas; acesso vale até 30 min | ✔ | Rascunho |
| [RNF-U01](rnf.md#rnf-u01) | U | Mensagens em português que orientam a correção | 100% das recusas com código, mensagem e campo | — | Rascunho |
| [RNF-U02](rnf.md#rnf-u02) | U | Telas utilizáveis em telas estreitas | 7 de 7 telas sem rolagem horizontal a 360 px | ✔ | A verificar |
| [RNF-U03](rnf.md#rnf-u03) | U | Operação completa pelo teclado | 100% das operações sem mouse | ✔ | A verificar |
| [RNF-U04](rnf.md#rnf-u04) | U | Contraste de cores (WCAG AA) | texto ≥ 4,5:1; bordas ≥ 3:1 (menor medido: 4,79:1 e 3,66:1) | ✔ | Rascunho (telas a verificar) |
| [RNF-U05](rnf.md#rnf-u05) | U | Situação nunca indicada só por cor | 100% das etiquetas e avisos com texto | ✔ | A verificar |
| [RNF-U06](rnf.md#rnf-u06) | U | Datas e horas no formato brasileiro | dd/mm/aaaa e HH:MM; 0 datas deslocadas | ✔ | Rascunho |
| [RNF-R01](rnf.md#rnf-r01) | R | Nenhum espaço comprometido duas vezes | 0 pares sobrepostos, inclusive simultâneos | — | Rascunho |
| [RNF-R02](rnf.md#rnf-r02) | R | Histórico completo e na mesma gravação | 100% das mudanças aceitas com registro; 0 a mais | ✔ | Rascunho |
| [RNF-R03](rnf.md#rnf-r03) | R | Operação recusada não muda nada | 0 mudanças depois de uma recusa | ✔ | Rascunho |
| [RNF-R04](rnf.md#rnf-r04) | R | Alteração sobre leitura desatualizada é recusada | 2 simultâneas → 1 gravada, 1 recusada | ✔ | Rascunho |
| [RNF-R05](rnf.md#rnf-r05) | R | Nada é excluído | 0 operações de exclusão | ✔ | Rascunho |
| [RNF-R06](rnf.md#rnf-r06) | R | Nenhuma regra violada vira erro interno | 0 regras em 500; 500 sem detalhes | ✔ | Rascunho |
| [RNF-P01](rnf.md#rnf-p01) | P | Tempo da consulta de reservas | p95 ≤ 1 s com 1.000 reservas (medido: 378 ms no pior cenário) | ✔ | Rascunho (atendido) |
| [RNF-P02](rnf.md#rnf-p02) | P | Tempo da agenda do dia | p95 ≤ 500 ms com 1.000 reservas (medido: 7 ms) | ✔ | Rascunho (atendido) |
| [RNF-S01](rnf.md#rnf-s01) | S | Execução num ambiente novo com um comando | 1 comando; 0 intervenções | — | A verificar |
| [RNF-S02](rnf.md#rnf-s02) | S | Dados de exemplo em um comando, repetível | 1 comando; 0 duplicados; 0 restos de falha | ✔ | Rascunho |
| [RNF-S03](rnf.md#rnf-s03) | S | Cobertura de testes | 100% em domain/application; ≥ 99% total | ✔ | Rascunho |
| [RNF-S04](rnf.md#rnf-s04) | S | Regra de dependência entre camadas e contextos | 0 contratos quebrados | ✔ | Rascunho |
| [RNF-S05](rnf.md#rnf-s05) | S | Horário de Brasília em todo o sistema | 0 horários deslocados, 2000 a 2100 | ✔ | Rascunho |
| [RNF-S06](rnf.md#rnf-s06) | S | Configuração sem segredos no código | 0 credenciais no repositório e no ZIP | ✔ | A verificar |

**Contagem:** 33 RNF — F 13, U 6, R 6, P 2, S 6. Marcados como "o cliente não pediria": 28.

**Restrições** (FURPS+, não são RNF): Python no backend; entrega em 20/11/2026 com o ZIP de três itens; React ([DEC-01](../decisoes/DEC-01.md)); Docker e PostgreSQL ([DEC-02](../decisoes/DEC-02.md), [DEC-03](../decisoes/DEC-03.md)); execução local; limites de páginas; demonstração em 10 minutos; extras sem atrasar as seis funcionalidades. Tabela: [REST-01 a REST-08](rnf.md#6-restrições).

## 6. Rastreabilidade

Cadeia do professor (A3·s8), nos dois sentidos: NS → RF → UC → US → CA/TA. A coluna de evidência leva até o código e os testes (extensão do grupo).

**Matriz consolidada (REQ-06):** a cadeia inteira, de NS a TA e até o endpoint, a tela e o código, nos dois sentidos, está em [`rastreabilidade/`](../rastreabilidade/README.md): [matriz](../rastreabilidade/matriz.md) (uma linha por RF), [cobertura](../rastreabilidade/cobertura.md), [sentido inverso](../rastreabilidade/sentido-inverso.md), [RNF](../rastreabilidade/rnf.md) e [mapa de impacto por DEC](../rastreabilidade/impacto-por-dec.md). Ela é gerada a partir das fichas por `scripts/gerar_rastreabilidade.py`; as tabelas abaixo continuam como índice por necessidade, por funcionalidade e por decisão, e o script confere que a 6.3 bate com o campo Decisões das fichas.

### 6.1 NS → RF

Toda NS tem pelo menos um RF; todo RF tem uma NS principal (a coluna "NS" da [tabela-resumo](#tabela-resumo)). A volta (NS → RF) também está na [Visão](../visao.md#necessidades). Conferido por `scripts/verificar_requisitos.py`.

| NS | Necessidade (resumo) | RF com esta NS como origem principal | Também citada em |
|---|---|---|---|
| NS-01 | Saber quais espaços existem | RF-01, RF-02, RF-02.1, RF-03, RF-04, RF-09 | RF-05.2 |
| NS-02 | Manter o cadastro de espaços | RF-05, RF-05.1, RF-05.2, RF-06, RF-06.1, RF-06.2, RF-07, RF-07.1, RF-08, RF-08.1 | RF-10, RF-11.3, RF-29.2 |
| NS-03 | Pedir o uso de um espaço | RF-11, RF-11.1, RF-11.3 | RF-11.2 |
| NS-04 | Nunca dois usos no mesmo período | RF-11.4 | — |
| NS-05 | Ver o que está ocupado e livre antes de pedir | RF-29, RF-29.1, RF-29.2, RF-30, RF-31 | — |
| NS-06 | Conhecer as regras de uso e ter os pedidos fora delas impedidos | RF-11.2, RF-11.5, RF-28 | RF-31 |
| NS-07 | Acompanhar os próprios pedidos | RF-13, RF-14 | RF-15, RF-26 |
| NS-08 | Localizar pedidos por critérios combinados | RF-12, RF-12.1, RF-15 | RF-14 |
| NS-09 | Decidir sobre cada pedido | RF-16, RF-17, RF-18, RF-19, RF-20, RF-24, RF-25, RF-26 | RF-27 |
| NS-10 | Desistir do próprio pedido | RF-21 | RF-16, RF-26 |
| NS-11 | Saber quem pediu e só quem tem autoridade decide | RF-10, RF-27, RF-33, RF-33.1, RF-33.2, RF-34, RF-34.1, RF-35, RF-36, RF-37 | RF-16, RF-22, RF-32.2, RF-32.3 |
| NS-12 | Histórico de cada reserva | RF-22 | — |
| NS-13 | Saber o resultado de cada operação | RF-38 | todas as recusas (F5) |
| NS-14 | Pedidos protegidos de outros solicitantes | RF-23 | RF-11.4, RF-13, RF-29, RF-36 |
| NS-15 | Acesso sem depender de um gestor | RF-32, RF-32.1, RF-32.2, RF-32.3 | — |
| NS-16 | Instalar, executar e demonstrar | RF-39, RF-40 | — |

### 6.2 RF → funcionalidades do enunciado (F1 a F6)

| F | Funcionalidade mínima | RF | Coberta |
|---|---|---|---|
| F1 | Cadastrar e listar os itens | RF-01 a RF-05 | ✔ |
| F2 | Cadastrar solicitação com solicitante, item, data e situação inicial | RF-11 | ✔ |
| F3 | Consultar por pelo menos dois critérios | RF-12 (espaço, situação, data, solicitante, "somente as minhas"), RF-13, RF-14, RF-15 | ✔ |
| F4 | Alterar a situação com pelo menos três estados | RF-16 a RF-21 (cinco situações) | ✔ |
| F5 | Impedir operações inválidas: campo obrigatório vazio, item inexistente, mudança de situação não permitida | 28 recusas: RF-02.1, RF-05.1, RF-05.2, RF-06.1, RF-06.2, RF-07.1, RF-08.1, RF-09, RF-10, RF-11.1 a RF-11.5, RF-12.1, RF-23 a RF-27, RF-29.1, RF-29.2, RF-32.1 a RF-32.3, RF-33.1, RF-33.2, RF-34.1. Os três casos do enunciado: campo vazio (RF-05.1, RF-11.1, RF-25), item inexistente (RF-09, RF-11.3, RF-23), mudança não permitida (RF-24). | ✔ |
| F6 | Mensagens claras de sucesso e erro | RF-38 (e RNF-U01) | ✔ |
| Extra | Além das seis | RF-06, RF-07, RF-08, RF-22, RF-28 a RF-31, RF-32 a RF-37, RF-39, RF-40 (16 fichas, sem contar as recusas, que são F5) | — |

### 6.3 RF e RNF → DEC

| DEC | Estado | RF | RNF |
|---|---|---|---|
| [DEC-01](../decisoes/DEC-01.md) | Decidida | — | REST-03 |
| [DEC-02](../decisoes/DEC-02.md) | Decidida | — | REST-04 |
| [DEC-03](../decisoes/DEC-03.md) | Decidida | — | REST-04 |
| [DEC-04](../decisoes/DEC-04.md) | Decidida | RF-05, RF-10, RF-11, RF-13, RF-23, RF-27, RF-32, RF-33, RF-34, RF-36, RF-37 | RNF-F01 a RNF-F04, RNF-F09, RNF-F13; REST-08 |
| [DEC-05](../decisoes/DEC-05.md) | Decidida (CR-02) | RF-22 | RNF-R02 |
| [DEC-06](../decisoes/DEC-06.md) | Decidida | RF-06, RF-07, RF-08, RF-11.3, RF-20 | RNF-R05 |
| [DEC-07](../decisoes/DEC-07.md) | Decidida (CR-03) | RF-11.5, RF-28, RF-30, RF-31 | — |
| [DEC-08](../decisoes/DEC-08.md) | Decidida | — | RNF-S03 |
| [DEC-09](../decisoes/DEC-09.md) | Decidida (CR-04) | RF-32, RF-32.1 | — |
| [DEC-10](../decisoes/DEC-10.md) | Decidida | RF-05.2, RF-06.2 | — |
| [DEC-11](../decisoes/DEC-11.md) | Decidida | RF-29 | RNF-F06 |
| [DEC-12](../decisoes/DEC-12.md) | Decidida | — | RNF-P01, RNF-P02 |
| [DEC-13](../decisoes/DEC-13.md) | Decidida (CR-01) | RF-16, RF-17, RF-18, RF-19, RF-20, RF-21 | — |
| [DEC-14](../decisoes/DEC-14.md) | Decidida | — | — |
| [DEC-15](../decisoes/DEC-15.md) | Decidida | — | — |
| [DEC-16](../decisoes/DEC-16.md) | Decidida | — | — |
| [DEC-17](../decisoes/DEC-17.md) | Decidida | — | — |
| [DEC-18](../decisoes/DEC-18.md) | Decidida | — | — |
| [DEC-19](../decisoes/DEC-19.md) | Decidida | — | — |
| [DEC-20](../decisoes/DEC-20.md) | Decidida | — | — |
| [DEC-21](../decisoes/DEC-21.md) | Decidida | — | — |
| [DEC-22](../decisoes/DEC-22.md) | Decidida | — | — |
| [DEC-23](../decisoes/DEC-23.md) | Decidida | — | — |

### 6.4 RF → evidência, UC, US e CA

UC, US, CA e TA de cada RF estão na [matriz gerada](../rastreabilidade/matriz.md) (REQ-06), e o endpoint, a tela e o código, nas colunas complementares dela. Aqui fica só **um teste representativo por RF**, a amostra de verificação do item "A evidência citada existe e prova o enunciado?" do [checklist de revisão](#10-checklist-de-revisão-por-pares): ele não está na matriz, que liga cada CA ao seu TA, e repetir UC, US e CA aqui criaria uma segunda cópia para esquecer de atualizar. A evidência completa está no campo Evidência de cada ficha. O RF-38 é transversal e não tem CA próprio.

| RF | Teste representativo (a partir de `src/backend/`, ou `src/frontend/src/` quando indicado) |
|---|---|
| RF-01 | `espacos/tests/test_api_espacos.py::test_listar_ordena_por_nome` |
| RF-02 | `espacos/tests/test_api_espacos.py::test_listar_aplica_os_filtros_da_query_string` |
| RF-02.1 | `espacos/tests/test_api_espacos.py::test_listar_com_tipo_desconhecido_no_filtro_responde_400` |
| RF-03 | `espacos/tests/test_api_espacos.py::test_obter_espaco_existente_responde_200_com_o_espaco` |
| RF-04 | `espacos/tests/test_api_espacos.py::test_tipos_de_espaco_lista_todos_os_tipos_na_ordem_do_enum` |
| RF-05 | `espacos/tests/test_api_espacos.py::test_cadastrar_espaco_valido_responde_201_com_o_espaco` |
| RF-05.1 | `espacos/tests/test_api_espacos.py::test_cadastro_invalido_responde_erro_e_preserva_a_listagem` |
| RF-05.2 | `espacos/tests/test_casos_de_uso.py::test_cadastrar_nome_repetido_com_caixa_e_espacos_diferentes_lanca_conflito` |
| RF-06 | `espacos/tests/test_api_edicao_de_espaco.py::test_editar_responde_200_e_a_listagem_mostra_os_dados_novos` |
| RF-06.1 | `espacos/tests/test_api_edicao_de_espaco.py::test_editar_sem_nenhum_campo_responde_400` |
| RF-06.2 | `espacos/tests/test_api_edicao_de_espaco.py::test_editar_com_dado_invalido_responde_erro_no_campo_e_nao_grava` |
| RF-07 | `espacos/tests/test_api_desativacao_e_reservas.py::test_reserva_existente_continua_listada_com_as_acoes_depois_de_desativar` |
| RF-07.1 | `espacos/tests/test_api_edicao_de_espaco.py::test_desativar_espaco_ja_inativo_responde_409_e_ele_continua_inativo` |
| RF-08 | `espacos/tests/test_api_desativacao_e_reservas.py::test_reativar_volta_a_aceitar_reservas` |
| RF-08.1 | `espacos/tests/test_api_edicao_de_espaco.py::test_ativar_espaco_ja_ativo_responde_409` |
| RF-09 | `espacos/tests/test_api_edicao_de_espaco.py::test_acoes_em_espaco_inexistente_respondem_404` |
| RF-10 | `espacos/tests/test_api_edicao_de_espaco.py::test_solicitante_nao_edita_desativa_nem_ativa_e_nada_muda` |
| RF-11 | `reservas/tests/test_api_reservas.py::test_solicitacao_valida_responde_201_com_a_reserva` |
| RF-11.1 | `reservas/tests/test_api_reservas.py::test_campos_ausentes_respondem_400_com_cada_campo` |
| RF-11.2 | `reservas/tests/test_reserva.py::test_solicitar_com_inicio_igual_a_agora_e_recusado` |
| RF-11.3 | `reservas/tests/test_api_reservas.py::test_espaco_inexistente_responde_404` |
| RF-11.4 | `reservas/tests/test_api_reservas.py::test_horario_ocupado_responde_409_e_preserva_as_reservas` |
| RF-11.5 | `reservas/tests/test_regras_de_agenda.py::test_horario_fora_do_funcionamento_e_recusado_no_campo_certo` |
| RF-12 | `reservas/tests/test_api_consulta_reservas.py::test_criterios_combinados_se_somam` |
| RF-12.1 | `reservas/tests/test_api_consulta_reservas.py::test_filtro_invalido_responde_400_com_o_campo` |
| RF-13 | `reservas/tests/test_api_permissoes.py::test_solicitante_so_lista_as_proprias` |
| RF-14 | `reservas/tests/test_api_consulta_reservas.py::test_detalhe_devolve_a_reserva_no_mesmo_formato_da_criacao` |
| RF-15 | `reservas/tests/test_api_consulta_reservas.py::test_situacoes_de_reserva_listam_todas_na_ordem_do_enum_sem_login` |
| RF-16 | `reservas/tests/test_api_situacao_reserva.py::test_reserva_solicitada_traz_confirmar_recusar_e_cancelar` |
| RF-17 | `reservas/tests/test_api_situacao_reserva.py::test_confirmar_responde_200_com_a_reserva_atualizada` |
| RF-18 | `reservas/tests/test_api_situacao_reserva.py::test_mensagem_de_sucesso_usa_o_rotulo_da_nova_situacao` |
| RF-19 | `reservas/tests/test_api_situacao_reserva.py::test_fluxo_da_demonstracao_ate_concluida` |
| RF-20 | `reservas/tests/test_api_situacao_reserva.py::test_cancelar_libera_o_horario_para_nova_reserva` |
| RF-21 | `reservas/tests/test_api_permissoes.py::test_solicitante_cancela_a_propria` |
| RF-22 | `reservas/tests/test_api_historico.py::test_fluxo_completo_aparece_no_historico_em_ordem` |
| RF-23 | `reservas/tests/test_api_permissoes.py::test_detalhe_de_outra_pessoa_para_o_solicitante_responde_404` |
| RF-24 | `reservas/tests/test_api_situacao_reserva.py::test_transicao_proibida_responde_409_e_preserva_a_reserva` |
| RF-25 | `reservas/tests/test_api_situacao_reserva.py::test_situacao_ausente_ou_invalida_responde_400` |
| RF-26 | `reservas/tests/test_api_situacao_reserva.py::test_recusar_sem_motivo_responde_400_no_campo_motivo` |
| RF-27 | `reservas/tests/test_api_permissoes.py::test_solicitante_confirmando_a_propria_responde_403_sem_mudar_nada` |
| RF-28 | `reservas/tests/test_api_regras_de_agenda.py::test_regras_de_agenda_sem_login_respondem_200_com_as_constantes_do_dominio` |
| RF-29 | `reservas/tests/test_api_ocupacao_do_dia.py::test_solicitante_ve_a_reserva_de_outra_pessoa_sem_nenhum_dado_pessoal` |
| RF-29.1 | `reservas/tests/test_api_ocupacao_do_dia.py::test_sem_espaco_ou_sem_data_responde_400_com_o_campo` |
| RF-29.2 | `reservas/tests/test_api_ocupacao_do_dia.py::test_espaco_inativo_responde_409` |
| RF-30 | `reservas/tests/test_propriedades_da_agenda.py::test_agenda_mostra_livre_exatamente_o_que_o_backend_aceitaria` |
| RF-31 | `reservas/tests/test_api_ocupacao_do_dia.py::test_ontem_nao_e_reservavel_e_traz_a_mensagem_do_dominio` |
| RF-32 | `contas/tests/test_api_cadastro.py::test_cadastro_valido_responde_201_com_solicitante_sem_senha` |
| RF-32.1 | `contas/tests/test_api_cadastro.py::test_campos_ausentes_respondem_400_com_cada_campo` |
| RF-32.2 | `contas/tests/test_api_cadastro.py::test_senha_fraca_responde_400_com_motivos_em_senha` |
| RF-32.3 | `contas/tests/test_api_cadastro.py::test_email_repetido_com_caixa_diferente_responde_409` |
| RF-33 | `contas/tests/test_api_autenticacao.py::test_login_valido_devolve_tokens_e_usuario_sem_senha` |
| RF-33.1 | `contas/tests/test_api_autenticacao.py::test_senha_errada_email_inexistente_e_inativo_respondem_igual` |
| RF-33.2 | `contas/tests/test_limites_de_tentativas.py::test_sexta_tentativa_com_o_mesmo_email_responde_429_com_a_espera` |
| RF-34 | `contas/tests/test_api_autenticacao.py::test_refresh_valido_devolve_access_novo_que_funciona_no_me` |
| RF-34.1 | `api/cliente.test.ts` (frontend) |
| RF-35 | `contas/tests/test_api_autenticacao.py::test_me_com_bearer_valido_devolve_usuario_com_perfil` |
| RF-36 | `contas/tests/test_api_sair.py::test_sair_revoga_o_refresh_e_ele_deixa_de_renovar` |
| RF-37 | `contas/tests/test_usuario_manager.py::test_create_superuser_cria_gestor_com_staff_e_superuser` |
| RF-38 | `compartilhado/tests/test_tratador_de_erros.py::test_campo_obrigatorio_ausente_indica_o_campo_que_falhou` |
| RF-39 | `exemplos/tests/test_carregar_dados_exemplo.py::test_rodar_duas_vezes_nao_duplica_e_informa_que_ja_existiam` |
| RF-40 | `reservas/tests/test_api_permissoes.py::test_vocabularios_e_health_nao_exigem_login` (sem teste do 503: [L-08](#lacunas)) |

## 7. Análise QFD

Classificação do ponto de vista do **cliente** (a instituição), não do enunciado (A2·s12–13):

- **Normal:** o que foi pedido na negociação: as seis funcionalidades do enunciado e o que a declaração da solução na Visão promete (impedir dois usos no mesmo período, registrar cada decisão com autor, momento e motivo).
- **Esperado:** o que o cliente não diz, mas cuja falta o frustraria: perfis e identificação, privacidade, filtros, manutenção completa do cadastro, motivos, ações disponíveis, regras de uso aplicadas.
- **Fascinante:** o que ele não espera e encanta: ver, antes de pedir, o que está ocupado e livre num dia e escolher um horário livre; conhecer as regras de uso antes de criar a conta.

| Classe | Fichas | RF |
|---|---|---|
| Normal | 22 | RF-01, RF-03, RF-05, RF-05.1, RF-09, RF-11, RF-11.1, RF-11.3, RF-11.4, RF-12, RF-13, RF-14, RF-17, RF-18, RF-19, RF-20, RF-22, RF-23, RF-24, RF-25, RF-37, RF-38 |
| Esperado | 36 | as demais, salvo as três abaixo |
| Fascinante | 3 | RF-28, RF-29, RF-30 |

**Risco de *scope creep* (A2·s14).** Dezesseis fichas são extras ao enunciado (seção 6.2), e três delas são fascinantes. Elas não comprometeram as seis funcionalidades mínimas porque:

1. **Vieram depois.** As seis funcionalidades estavam integradas e testadas antes de cada extra; a regra 2 do projeto ("escopo mínimo primeiro") e a contingência da [DEC-04](../decisoes/DEC-04.md) mandam cortar o extra que ameaçar o prazo (risco R-03 da Visão).
2. **Não mudam as regras das seis.** A agenda do dia ([RF-29](rf-agenda.md#rf-29), [RF-30](rf-agenda.md#rf-30)) só lê reservas e reaproveita as mesmas regras de conflito e de agenda do pedido; o pedido continua sendo verificado por inteiro no envio. As regras de agenda consultáveis ([RF-28](rf-agenda.md#rf-28)) leem as mesmas constantes da recusa ([RF-11.5](rf-reservas.md#rf-11-5)). Uma propriedade testada prova que a agenda mostra livre exatamente o que o pedido aceitaria.
3. **Nenhum fascinante é exigido por um normal.** Se os três fossem retirados, nenhuma das seis funcionalidades deixaria de funcionar.

O risco que fica é de **prazo** (R-01): daqui até a entrega não entra nenhum RF novo além do [RF-33.2](rf-contas.md#rf-33-2) (AUT-08), uma recusa que fecha a lacuna [L-03](#l-03) sem tocar nas seis funcionalidades; o tempo vai para documentação e ensaio.

## Lacunas

Comportamento que uma necessidade pede e o sistema não tem, comportamento sem teste e comportamento sem necessidade de origem. Cada lacuna tem uma proposta: **DEC** (pergunta a quem decide), **CR** (mudança depois da baseline) ou **aceitar** (registrar e conviver). Nenhuma muda o código nesta tarefa.

| ID | Tipo | Lacuna | Afeta | Proposta |
|---|---|---|---|---|
| <a id="l-01"></a>L-01 | NS × comportamento | A NS-09 fala em registrar que o uso **aconteceu**, mas o Gestor conclui uma reserva antes do término; também confirma ou recusa depois do início, qualquer um cancela depois do uso, e uma Solicitada não decidida continua ocupando horário depois da data. | RF-16 a RF-21; NS-09 | **CR** — [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md) (a [DEC-13](../decisoes/DEC-13.md), decidida em 06/11/2026: concluir só a partir do término; recusar e cancelar, pelo Gestor, só antes do início); fecha com a RES-11. |
| <a id="l-02"></a>L-02 | NS × comportamento | O modelo de aceite do professor inclui "tentativa registrada com data, ator e resultado"; o histórico só registra as mudanças aceitas. | RF-22; RNF-R02 | **CR** — [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md) (a [DEC-05](../decisoes/DEC-05.md), decidida em 06/11/2026: as tentativas recusadas entram no histórico); fecha com a RES-12. |
| <a id="l-03"></a>L-03 | RNF ausente | Não havia limite de tentativas de entrada: nada impedia adivinhar senhas por tentativa e erro. | RF-33; NS-11 | **Resolvida pela AUT-08:** [RF-33.2](rf-contas.md#rf-33-2) (a recusa e o tempo de espera) e [RNF-F12](rnf.md#rnf-f12) (limites por e-mail e por origem no login e por origem no cadastro). Fica a limitação do contador no Redis sem persistência, nas [limitações conhecidas do README da raiz](../../../../README.md#limitações-conhecidas). |
| <a id="l-04"></a>L-04 | RNF ausente | Sair não invalida a credencial de acesso: uma cópia dela continua valendo até expirar (até 30 min). A parte da credencial de renovação foi resolvida pela AUT-09: sair a revoga, e cada renovação a troca ([RNF-F13](rnf.md#rnf-f13)). | RF-36; RNF-F03; RNF-F13 | **Aceitar** ([limitação conhecida do README da raiz](../../../../README.md#limitações-conhecidas); [DEC-04](../decisoes/DEC-04.md), decisão c da AUT-03). |
| <a id="l-05"></a>L-05 | Comportamento | A consulta de reservas não é paginada: a lista do Gestor sem critério devolve todas as reservas, e o tempo e o tamanho da resposta crescem com elas. Medido: p95 de 378 ms com 1.000 reservas (meta atendida) e de 1.743 ms com 5.000 (meta estourada). | RF-12; RNF-P01 | **Aceitar** para a entrega (aceita: [DEC-12](../decisoes/DEC-12.md) decidida em 06/11/2026): a meta vale para 1.000 reservas e foi atingida ([medição](rnf.md#medição)). Se a carga esperada passar de alguns milhares de reservas, **CR** com paginação da consulta. |
| <a id="l-06"></a>L-06 | NS × comportamento | A matrícula não é conferida com a instituição: qualquer texto de até 20 caracteres sem espaço é aceito. | RF-32, RF-32.1; NS-11 | **CR** — [CR-04](../mudancas/CR-04-matricula-so-digitos.md) (a [DEC-09](../decisoes/DEC-09.md), decidida em 06/11/2026: só dígitos); fecha com a AUT-12. A conferência com a instituição continua fora do escopo. |
| <a id="l-07"></a>L-07 | RF/RNF sem teste | Não há teste com dois pedidos simultâneos de verdade (duas threads) para o mesmo período; a garantia é a restrição do banco, provada por um teste que simula a corrida. Para a mudança de situação o teste de duas threads existe. | RNF-R01; RF-11.4 | **Aceitar** nesta tarefa (não muda testes); sugerir o teste numa tarefa de testes antes da baseline. |
| <a id="l-08"></a>L-08 | RF sem teste | A resposta "Não foi possível conectar ao banco de dados." (503) da verificação do sistema não tem teste. | RF-40; [US-19 · CA-02](../historias/US-19-verificar-se-o-sistema-esta-no-ar.md#us-19-ca-02) (TA-160, roteiro manual, REQ-05) | **Aceitar** nesta tarefa; sugerir o teste numa tarefa de testes. |
| <a id="l-09"></a>L-09 | RNF sem verificação automática | 360 px, teclado, contraste nas telas, situação sem depender da cor, execução num ambiente novo e ausência de segredos no ZIP dependem de verificação manual. | RNF-U02 a RNF-U05, RNF-S01, RNF-S06 | **Aceitar**, com a verificação feita no ensaio antes da entrega e o resultado registrado na versão 0.2. |
| <a id="l-10"></a>L-10 | Comportamento sem NS | (a) Só a origem das telas é autorizada a chamar a API pelo navegador (RNF-F11): proteção técnica sem NS própria, ligada à NS-14. (b) A administração (`/admin/`) permite à Equipe de TI mudar o perfil e desativar usuários, sem RF próprio além do [RF-37](rf-contas.md#rf-37). (c) O Gestor também pede reservas em nome próprio ([RF-11](rf-reservas.md#rf-11)) e filtra "somente as minhas" ([RF-12](rf-reservas.md#rf-12)), mas a NS-03 e a NS-07 têm só o Solicitante como origem. | RNF-F11; RF-37; RF-11, RF-12; Visão | (a) e (b) **aceitar**: são operação da Equipe de TI, que não é ator do negócio. (c) Ajuste editorial na Visão na 0.2 (acrescentar o Gestor à origem da NS-03 e da NS-07), sem mudança de comportamento. |
| <a id="l-11"></a>L-11 | NS sem RF implementado | Nenhuma. As 16 NS têm pelo menos um RF implementado e com teste. | — | — |
| <a id="l-12"></a>L-12 | RF × comportamento | Ao solicitar, o espaço informado por um número que não é positivo e, depois dele, a finalidade (em branco ou acima de 200 caracteres) são conferidos **depois** da data retroativa e das regras de agenda, e não junto com os outros dados do RF-11.1, como diz a ordem do campo Regras de negócio do [RF-11](rf-reservas.md#rf-11). Um pedido com finalidade vazia e data passada recebe primeiro "data retroativa"; com finalidade vazia e espaço zero, recebe primeiro "espaço não identificado" (a ficha dizia o contrário até a DOC-03). O que é aceito não muda, só qual mensagem aparece primeiro; nenhum teste fixa essa posição. Achada ao escrever a ficha de [UC-04](../casos-de-uso/UC-04-solicitar-reserva.md#p7) (REQ-04). | RF-11, RF-11.1; UC-04 | **Aceitar** o comportamento; ajuste editorial do campo Regras de negócio do RF-11 na 0.2 (a ficha de UC-04 já mostra a ordem real) e um teste da ordem numa tarefa de testes. |
| <a id="l-13"></a>L-13 | RF incompleto | O motivo de mais de 300 caracteres é recusado em **qualquer** mudança de situação, inclusive ao confirmar e ao concluir, em que é opcional; o [RF-26](rf-reservas.md#rf-26) só cobre recusar e cancelar, e o [RF-17](rf-reservas.md#rf-17) e o [RF-19](rf-reservas.md#rf-19) dizem só "motivo opcional". Provado pela máquina de estados da reserva. Achada na ficha de [UC-10](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-6) (REQ-04). | RF-17, RF-19, RF-26; UC-10 | **Aceitar**; ajuste editorial na 0.2 ("motivo opcional de até 300 caracteres" no RF-17 e no RF-19). |
| <a id="l-14"></a>L-14 | Comportamento sem RF | A entrada sem e-mail ou sem senha, ou com e-mail mal formado, é recusada com a indicação de cada dado, antes de conferir as credenciais; nenhum RF descreve essa recusa (o [RF-33.1](rf-contas.md#rf-33-1) trata só as credenciais inválidas). Coberta por teste. Achada na ficha de [UC-02](../casos-de-uso/UC-02-autenticar.md#e3-2) (REQ-04). | RF-33, RF-33.1; UC-02 | **Aceitar**; na 0.2, um RF filho novo (o próximo ID livre do RF-33), sem mudança de comportamento. |
| <a id="l-15"></a>L-15 | CA sem TA automatizado | [US-01 · CA-02](../historias/US-01-criar-minha-conta.md#us-01-ca-02): depois de criar a conta vindo de algo que exige identificação, a pessoa volta ao ponto em que estava. Os testes cobrem só a preservação do destino até o cadastro e a regra do destino seguro, não o retorno depois dele; o TA-02 é roteiro manual. Achada ao escrever as histórias (REQ-05). | RF-32; UC-01 A1.1; US-01 | **Aceitar**, com o TA-02 executado no ensaio; sugerir um teste do cadastro com destino numa tarefa de testes. |
| <a id="l-16"></a>L-16 | CA sem TA automatizado | [US-17 · CA-03](../historias/US-17-criar-o-primeiro-gestor.md#us-17-ca-03): criar um administrador com um e-mail já cadastrado é recusado pelo comando de administração. Só a unicidade do e-mail tem teste, não a resposta do comando; o TA-153 é roteiro manual. Achada ao escrever as histórias (REQ-05). | RF-37; UC-20 E2.1; US-17 | **Aceitar**, com o TA-153 executado no ensaio. |
| <a id="l-17"></a>L-17 | Comportamento sem RF | Um endereço de tela que não existe (`*`) mostra a página "não encontrada" com o caminho de volta ao início; nenhum RF descreve esse comportamento, que não tem regra de negócio nem teste próprio. Achada no [sentido inverso da matriz](../rastreabilidade/sentido-inverso.md#telas) (REQ-06). | Telas; NS-13 | **Aceitar**: é navegação, sem dado nem regra. Se o professor pedir rastreabilidade de toda tela, ajuste editorial na 0.2 (citar a tela na evidência do [RF-38](rf-gerais.md#rf-38)). |

## 9. Auditoria de qualidade

Critérios do A3·s9: **Cl**aro · **Ne**cessário · **Vi**ável · **Co**mpleto · **Ve**rificável · **Ra**streável. ✔ atende; ✘ não atende, com a ação ao lado. "Verificável" quer dizer que existe um jeito objetivo de verificar (teste ou método descrito); um RNF "a verificar" pode ser verificável e ainda não verificado.

### Requisitos funcionais

| ID | Cl | Ne | Vi | Co | Ve | Ra | Observação e ação |
|---|---|---|---|---|---|---|---|
| RF-01 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | "Ordenados pelo nome" segue a ordem do banco (maiúsculas antes de minúsculas, acentos no fim); registrado em [US-04 · CA-01](../historias/US-04-consultar-os-espacos.md#us-04-ca-01) (REQ-05). |
| RF-02 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-02.1 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-03 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-04 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-05 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-05.1 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-05.2 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Conforme a [DEC-10](../decisoes/DEC-10.md) (decidida). |
| RF-06 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-06.1 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-06.2 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-07 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Efeito sobre as reservas existentes conforme a [DEC-06](../decisoes/DEC-06.md) (decidida). |
| RF-07.1 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-08 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-08.1 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-09 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-10 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-11 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | O Gestor também pede: ajuste editorial na Visão ([L-10](#l-10)). A ordem das verificações no campo Regras de negócio difere da real para a finalidade ([L-12](#l-12)). |
| RF-11.1 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-11.2 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | "Data retroativa" compara data e hora (divergência registrada no glossário). |
| RF-11.3 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-11.4 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-11.5 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Valores da [DEC-07](../decisoes/DEC-07.md), decidida; mudam pelo [CR-03](../mudancas/CR-03-horario-por-espaco.md). |
| RF-12 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Sem paginação ([L-05](#l-05)). |
| RF-12.1 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-13 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-14 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-15 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-16 | ✔ | ✔ | ✔ | ✘ | ✔ | ✔ | Co: as ações não consideram o horário da reserva. Ação: [DEC-13](../decisoes/DEC-13.md) decidida; [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md). |
| RF-17 | ✔ | ✔ | ✔ | ✘ | ✔ | ✔ | Co: confirmar depois do início é aceito. Ação: [DEC-13](../decisoes/DEC-13.md) decidida; confirmar continua sem restrição de horário. Co: o limite de 300 caracteres do motivo opcional não está no enunciado ([L-13](#l-13)). |
| RF-18 | ✔ | ✔ | ✔ | ✘ | ✔ | ✔ | Co: recusar depois do início é aceito. Ação: [DEC-13](../decisoes/DEC-13.md) decidida; [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md). |
| RF-19 | ✔ | ✔ | ✔ | ✘ | ✔ | ✔ | Co: concluir antes do término é aceito, contra a NS-09. Ação: [DEC-13](../decisoes/DEC-13.md) decidida; [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md), lacuna [L-01](#l-01). |
| RF-20 | ✔ | ✔ | ✔ | ✘ | ✔ | ✔ | Co: cancelar depois do uso é aceito. Ação: [DEC-13](../decisoes/DEC-13.md) decidida; [CR-01](../mudancas/CR-01-situacao-e-horario-da-reserva.md) (só para o Gestor). |
| RF-21 | ✔ | ✔ | ✔ | ✘ | ✔ | ✔ | Co: idem. Ação: [DEC-13](../decisoes/DEC-13.md) decidida; o cancelamento pelo Solicitante continua sem restrição de horário. |
| RF-22 | ✔ | ✔ | ✔ | ✘ | ✔ | ✔ | Co: tentativas recusadas não são registradas. Ação: [DEC-05](../decisoes/DEC-05.md) decidida; [CR-02](../mudancas/CR-02-tentativas-recusadas-no-historico.md), lacuna [L-02](#l-02). |
| RF-23 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-24 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-25 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-26 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | O limite do motivo também vale ao confirmar e concluir, fora deste RF ([L-13](#l-13)). |
| RF-27 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-28 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-29 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Privacidade conforme a [DEC-11](../decisoes/DEC-11.md) (decidida). |
| RF-29.1 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-29.2 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-30 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-31 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-32 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-32.1 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Formato da matrícula pela [DEC-09](../decisoes/DEC-09.md), decidida; muda pelo [CR-04](../mudancas/CR-04-matricula-so-digitos.md). |
| RF-32.2 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-32.3 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-33 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Limite de tentativas no [RF-33.2](rf-contas.md#rf-33-2) ([L-03](#l-03), resolvida). |
| RF-33.1 | ✔ | ✔ | ✔ | ✘ | ✔ | ✔ | Co: a entrada sem e-mail ou senha, ou com e-mail mal formado, é recusada antes das credenciais e não está descrita. Ação: [L-14](#l-14). |
| RF-33.2 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-34 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-34.1 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Evidência só no frontend; o lado do servidor é o 401 da renovação recusada. |
| RF-35 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-36 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Sair revoga a credencial de renovação no servidor; a de acesso vale até expirar ([L-04](#l-04)). O resultado observável (página inicial sem identificação; a sessão não é renovada depois) é atendido. |
| RF-37 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-38 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-39 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RF-40 | ✔ | ✔ | ✔ | ✔ | ✘ | ✔ | Ve: o caso do banco fora do ar não tem teste. Ação: lacuna [L-08](#l-08). |

### Requisitos não funcionais

| ID | Cl | Ne | Vi | Co | Ve | Ra | Observação e ação |
|---|---|---|---|---|---|---|---|
| RNF-F01 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RNF-F02 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RNF-F03 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RNF-F04 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RNF-F05 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RNF-F06 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RNF-F07 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RNF-F08 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RNF-F09 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RNF-F10 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RNF-F11 | ✔ | ✔ | ✔ | ✔ | ✔ | ✘ | Ra: sem NS direta. Ação: lacuna [L-10](#l-10) (aceitar, ligado à NS-14). |
| RNF-F12 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Contador no Redis, sem persistência: zera ao reiniciar o Redis (limitação conhecida do README da raiz). |
| RNF-F13 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | A credencial de acesso não é revogada ([L-04](#l-04), aceita). |
| RNF-U01 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Os testes cobrem as recusas existentes; uma recusa nova precisa do seu teste de mensagem. |
| RNF-U02 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | A verificar ([L-09](#l-09)). |
| RNF-U03 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | A verificar ([L-09](#l-09)). |
| RNF-U04 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Cores-base medidas; telas a verificar ([L-09](#l-09)). |
| RNF-U05 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | A verificar ([L-09](#l-09)). |
| RNF-U06 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RNF-R01 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Sem teste de duas threads na criação ([L-07](#l-07)). |
| RNF-R02 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RNF-R03 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RNF-R04 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RNF-R05 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RNF-R06 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RNF-P01 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Meta da [DEC-12](../decisoes/DEC-12.md) (decidida) atendida com 1.000 reservas; não escala sem paginação ([L-05](#l-05)). |
| RNF-P02 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Meta atendida (p95 de 7 ms). |
| RNF-S01 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | A verificar (CS-03). |
| RNF-S02 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RNF-S03 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Meta interna ([DEC-08](../decisoes/DEC-08.md), decidida). |
| RNF-S04 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RNF-S05 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | |
| RNF-S06 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | A verificar antes da entrega ([L-09](#l-09)). |

**Resumo:** 10 ✘ em 93 fichas, todos com ação: 8 em Completo (DEC-13, DEC-05 e, desde a REQ-04, L-14; o RF-17 ganhou também a L-13), 1 em Verificável (L-08) e 1 em Rastreável (L-10).

## 10. Checklist de revisão por pares

Preparação para a versão 0.2 (revisão por pares, A4·s7). **Em branco: preenchido por um revisor do grupo que não seja o autor.** Um comentário útil localiza o trecho, descreve o risco e propõe uma correção.

Revisor: [nome] • Data: [dd/mm/aaaa]

| Pergunta | Sim/Não | Trecho e comentário |
|---|---|---|
| A condição de entrada de cada RF está clara (quem age, sobre o quê, em que situação)? | | |
| Cada RF tem uma só obrigação, e os filhos mantêm o vínculo com o pai? | | |
| As opções (ex.: recusar × cancelar, inexistente × inativo) têm resultados distintos e verificáveis? | | |
| Há contradição entre RFs, com o glossário, com a Visão ou com uma DEC? | | |
| Toda recusa (F5) diz o que fica preservado e o que é informado? | | |
| Todo RNF tem métrica, valor-alvo e forma de verificar? | | |
| Toda dúvida aparece como DEC ou lacuna, e não como regra afirmada? | | |
| A evidência citada existe e prova o enunciado (conferir uma amostra)? | | |
| Algum termo vago ou de solução (tela, botão, tecnologia) ficou num enunciado? | | |

**Auditoria do revisor** (marque ✔ ou ✘ onde discordar da [seção 9](#9-auditoria-de-qualidade) e comente):

| ID | Critério em que discorda | Comentário |
|---|---|---|
| | | |
