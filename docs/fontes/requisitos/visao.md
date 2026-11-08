# Documento de Visão — Conecta Campus

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **VIS-01 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/visao.md` |

Modelo: Documento de Visão do RUP em quatro quadrantes (A3·s7), com o cabeçalho do template de documento de projeto (A4·s11). Os termos do domínio têm definição única no [Glossário (GLO-01)](glossario.md); as decisões citadas estão em [`decisoes/`](decisoes/README.md).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Criação: problema, stakeholders, necessidades NS-01 a NS-16, escopo, premissas, critérios de sucesso e riscos (REQ-01). Sem aprovação. |
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Coluna "RF derivados" na tabela de necessidades, com o vínculo NS → RF da [SRS-01](requisitos/srs.md#61-ns--rf) (REQ-02). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Âncoras estáveis `#ns-01` a `#ns-16` na tabela de necessidades, para a [matriz de rastreabilidade](rastreabilidade/README.md) apontar para cada NS (REQ-06). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Respostas da Aula 7 (GES-02): P-02, P-04, o item de regras por espaço do fora do escopo e a resposta dos riscos R-05 e R-08 a R-14 apontam para as DECs decididas e os CR-02 a CR-04. Nenhuma necessidade, premissa ou risco novo; a P-04 deixa de valer só com a ESP-07. Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | NS-11 cita também o RF-33.2, novo na AUT-08. Nenhuma necessidade nova. Sem aprovação. |

## Sumário

1. [Problema e declaração](#1-problema-e-declaração)
2. [Usuários, atores e stakeholders](#2-usuários-atores-e-stakeholders)
   - [Cliente × usuário](#cliente--usuário)
   - [Necessidades](#necessidades)
3. [Escopo inicial do sistema](#3-escopo-inicial-do-sistema)
   - [Restrições](#restrições)
   - [Premissas](#premissas)
4. [Sucesso e risco](#4-sucesso-e-risco)
5. [Checklist de revisão por pares](#5-checklist-de-revisão-por-pares)

No sumário do template A4·s11, este documento cobre as partes 1 (visão, objetivos e escopo), 2 (stakeholders; o glossário é o GLO-01) e 6 (premissas, riscos e decisões pendentes). As demais partes vêm nas próximas tarefas (REQ-02 em diante).

---

## 1. Problema e declaração

**O problema.** Na comunidade acadêmica, o uso das quadras e dos demais [espaços esportivos](glossario.md#espaco-esportivo) é combinado de forma informal: por conversa, mensagem ou anotação de quem cuida do espaço. Quem quer usar um espaço não sabe, antes de pedir, quais períodos já estão comprometidos. Dois grupos podem combinar o mesmo espaço no mesmo horário e só descobrir o choque na hora do uso. Depois que o uso é combinado, não fica registrado quem pediu, quem aprovou, quando e por qual motivo um pedido foi negado ou desfeito.

**Quem é afetado.**

- Alunos e servidores que pedem espaços: perdem tempo procurando quem decide, não sabem se o pedido foi aceito e podem chegar a um espaço já ocupado.
- Quem administra os espaços: decide sem ver o conjunto dos pedidos, resolve conflitos depois que eles acontecem e não tem como mostrar o que decidiu.
- A instituição: não sabe como os espaços são usados e não consegue explicar uma decisão contestada.

**Impacto.** Choques de uso no mesmo espaço e horário, pedidos sem resposta, decisões que dependem da memória de uma pessoa e nenhuma evidência para resolver uma reclamação.

**Declaração da solução.** Para a comunidade acadêmica que usa os espaços esportivos da instituição, o Conecta Campus registra cada pedido de uso de um espaço num período, impede que um espaço seja comprometido duas vezes no mesmo período e registra cada decisão sobre o pedido, com autor, momento e motivo.

## 2. Usuários, atores e stakeholders

| Papel | Descrição | Interesses | Cliente, usuário ou ator? |
|---|---|---|---|
| **Cliente** (instituição: [nome do setor que administra os espaços esportivos]) | Patrocina o sistema, define as regras de uso dos espaços e aprova o escopo. **Premissa P-01:** não há cliente real nomeado; o grupo representa a instituição. | Uso organizado dos espaços; menos conflitos de horário; rastreabilidade de quem pediu e de quem decidiu; custo de operação baixo (execução local, sem serviços pagos). | **Cliente.** Não opera o sistema e não é ator. |
| **Solicitante** ([perfil](glossario.md#solicitante)) | Aluno ou servidor com [matrícula](glossario.md#matricula), cadastrado no sistema, que pede o uso de espaços em nome próprio. | Pedir sem procurar ninguém; saber antes de pedir o que já está ocupado; acompanhar a [situação](glossario.md#situacao) do próprio pedido; desistir quando precisar; não ter os próprios pedidos expostos a outros solicitantes. | **Usuário** e **ator** do sistema. |
| **Gestor** ([perfil](glossario.md#gestor)) | Pessoa do setor responsável pelos espaços. Mantém o cadastro de espaços e decide sobre os pedidos: confirma, recusa, conclui ou cancela. | Ver todos os pedidos e filtrá-los; decidir sem conflito de horário; justificar recusas e cancelamentos; retirar um espaço de uso sem perder o que já foi combinado. | **Usuário** e **ator** do sistema. |
| **Visitante** ([definição](glossario.md#visitante)) | Pessoa ainda não identificada no sistema. | Criar a própria conta; conhecer as regras de uso antes de se cadastrar. | **Ator** do sistema (antes de se identificar). |
| **Equipe de TI** | Quem instala e opera o sistema e cria os usuários Gestor pela administração. | Instalar e executar seguindo um roteiro escrito; dados de exemplo para demonstração; configuração sem senhas no código. | **Stakeholder.** Não é ator dos casos de uso do negócio: atua na instalação e na administração. |
| **Professor / avaliador** | Avalia o produto e a documentação nas duas disciplinas. | Executar o sistema pelo README num ambiente limpo; requisitos rastreáveis até o código e os testes. | **Stakeholder** do projeto acadêmico. Não é usuário. |
| **Equipe do projeto** (Grupo 03) | Integrantes que especificam, implementam e documentam. | Escopo estável até 20/11/2026; decisões registradas para não dependerem da memória. | **Stakeholder.** Também representa o cliente enquanto a P-01 valer. |

### Cliente × usuário

O **cliente** e o **usuário** não são a mesma pessoa e não querem as mesmas coisas (A2·s5):

| | Cliente (instituição) | Usuários (Solicitante e Gestor) |
|---|---|---|
| Papel | Aprova o escopo e as regras de uso | Opera o sistema no dia a dia |
| Foco | Metas da instituição: espaços sem conflito, decisões rastreáveis, custo | Tarefa do momento: pedir, acompanhar, decidir sem atrito |
| Exemplo de necessidade | NS-11 (saber quem pediu e quem decidiu) e NS-12 (histórico) | NS-03 (pedir o uso) e NS-05 (ver o que está ocupado antes de pedir) |
| Quem responde às dúvidas | As DECs de regra de uso (ex.: [DEC-07](decisoes/DEC-07.md)) | As dúvidas de uso surgem nas histórias e nos critérios de aceite (REQ-04 em diante) |

O Gestor é usuário, não cliente: ele aplica as regras de uso, mas quem as define é a instituição.

### Necessidades

Cada necessidade descreve **o que** um stakeholder precisa, sem tela nem tecnologia (A1·s14). Os IDs são estáveis e nunca reutilizados. Cada NS aponta para a funcionalidade que a atende hoje e para os RF derivados dela na [SRS-01](requisitos/srs.md) (REQ-02): na coluna "RF derivados" estão os RF que têm a NS como origem principal; a volta (RF → NS) está na ficha de cada RF e na [rastreabilidade da SRS](requisitos/srs.md#61-ns--rf). "F1" a "F6" são as seis funcionalidades mínimas do enunciado de Projeto de Programação; "extra" é o que foi feito além delas.

| ID | Necessidade | Origem | Atendida hoje por | RF derivados |
|---|---|---|---|---|
| <a id="ns-01"></a>NS-01 | Saber quais espaços esportivos existem, de que tipo são, quantas pessoas comportam e quais aceitam pedidos. | Solicitante, Gestor | F1: listar e consultar espaços, com filtro por [tipo](glossario.md#tipo-de-espaco) e por [espaço ativo](glossario.md#espaco-ativo). | [RF-01](requisitos/rf-espacos.md#rf-01), [RF-02](requisitos/rf-espacos.md#rf-02), [RF-02.1](requisitos/rf-espacos.md#rf-02-1), [RF-03](requisitos/rf-espacos.md#rf-03), [RF-04](requisitos/rf-espacos.md#rf-04), [RF-09](requisitos/rf-espacos.md#rf-09) |
| <a id="ns-02"></a>NS-02 | Manter o cadastro de espaços igual à realidade: incluir um espaço, corrigir seus dados, retirá-lo de uso e devolvê-lo ao uso sem perder os pedidos já feitos. | Cliente, Gestor | F1: cadastrar espaço. Extra (ESP-04): editar, desativar e reativar ([DEC-06](decisoes/DEC-06.md)). | [RF-05](requisitos/rf-espacos.md#rf-05), [RF-05.1](requisitos/rf-espacos.md#rf-05-1), [RF-05.2](requisitos/rf-espacos.md#rf-05-2), [RF-06](requisitos/rf-espacos.md#rf-06), [RF-06.1](requisitos/rf-espacos.md#rf-06-1), [RF-06.2](requisitos/rf-espacos.md#rf-06-2), [RF-07](requisitos/rf-espacos.md#rf-07), [RF-07.1](requisitos/rf-espacos.md#rf-07-1), [RF-08](requisitos/rf-espacos.md#rf-08), [RF-08.1](requisitos/rf-espacos.md#rf-08-1) |
| <a id="ns-03"></a>NS-03 | Pedir o uso de um espaço para uma data, um horário de início e de término e uma finalidade. | Solicitante | F2: solicitar [reserva](glossario.md#reserva), que nasce [Solicitada](glossario.md#solicitada). | [RF-11](requisitos/rf-reservas.md#rf-11), [RF-11.1](requisitos/rf-reservas.md#rf-11-1), [RF-11.3](requisitos/rf-reservas.md#rf-11-3) |
| <a id="ns-04"></a>NS-04 | Garantir que um espaço nunca fique comprometido com dois usos que tenham algum momento em comum. | Cliente, Gestor, Solicitante | F5: recusa por [conflito de horário](glossario.md#conflito-de-horario) entre [reservas que ocupam horário](glossario.md#reserva-que-ocupa-horario). | [RF-11.4](requisitos/rf-reservas.md#rf-11-4) |
| <a id="ns-05"></a>NS-05 | Saber, antes de pedir, quais períodos de um espaço num dia já estão comprometidos e quais estão livres. | Solicitante | Extra (FE-07): [agenda do dia](glossario.md#agenda-do-dia). | [RF-29](requisitos/rf-agenda.md#rf-29), [RF-29.1](requisitos/rf-agenda.md#rf-29-1), [RF-29.2](requisitos/rf-agenda.md#rf-29-2), [RF-30](requisitos/rf-agenda.md#rf-30), [RF-31](requisitos/rf-agenda.md#rf-31) |
| <a id="ns-06"></a>NS-06 | Conhecer as regras de uso dos espaços (período de funcionamento, duração e antecedência) e ter os pedidos fora delas impedidos. | Cliente, Solicitante | Extra (RES-09): [regras de agenda](glossario.md#regras-de-agenda) consultáveis e aplicadas ao pedido. F5: recusa de [data retroativa](glossario.md#data-retroativa) e de término antes do início. | [RF-11.2](requisitos/rf-reservas.md#rf-11-2), [RF-11.5](requisitos/rf-reservas.md#rf-11-5), [RF-28](requisitos/rf-agenda.md#rf-28) |
| <a id="ns-07"></a>NS-07 | Acompanhar a situação dos próprios pedidos, inclusive o motivo de uma recusa ou de um cancelamento. | Solicitante | F3: consultar as próprias reservas e o detalhe de cada uma. | [RF-13](requisitos/rf-reservas.md#rf-13), [RF-14](requisitos/rf-reservas.md#rf-14) |
| <a id="ns-08"></a>NS-08 | Localizar pedidos por espaço, situação, data e solicitante, combinando os critérios. | Gestor | F3: consultar reservas com filtros combináveis. | [RF-12](requisitos/rf-reservas.md#rf-12), [RF-12.1](requisitos/rf-reservas.md#rf-12-1), [RF-15](requisitos/rf-reservas.md#rf-15) |
| <a id="ns-09"></a>NS-09 | Decidir sobre cada pedido (aprovar ou negar com justificativa) e registrar que o uso aprovado aconteceu ou foi desfeito. | Gestor | F4: [transições de situação](glossario.md#transicao-de-situacao) para Confirmada, Recusada, Concluída e Cancelada, com [motivo](glossario.md#motivo) obrigatório para recusar e cancelar. | [RF-16](requisitos/rf-reservas.md#rf-16), [RF-17](requisitos/rf-reservas.md#rf-17), [RF-18](requisitos/rf-reservas.md#rf-18), [RF-19](requisitos/rf-reservas.md#rf-19), [RF-20](requisitos/rf-reservas.md#rf-20), [RF-24](requisitos/rf-reservas.md#rf-24), [RF-25](requisitos/rf-reservas.md#rf-25), [RF-26](requisitos/rf-reservas.md#rf-26) ([DEC-13](decisoes/DEC-13.md)) |
| <a id="ns-10"></a>NS-10 | Desistir de um pedido próprio, justificando. | Solicitante | F4: cancelar a própria reserva, com motivo. | [RF-21](requisitos/rf-reservas.md#rf-21) |
| <a id="ns-11"></a>NS-11 | Saber quem pediu cada reserva e garantir que só quem tem autoridade decida sobre os pedidos e altere os espaços. | Cliente | Extra ([DEC-04](decisoes/DEC-04.md)): identificação por e-mail e senha, [perfis](glossario.md#perfil) Solicitante e Gestor e [ações disponíveis](glossario.md#acao-disponivel) por perfil. | [RF-10](requisitos/rf-espacos.md#rf-10), [RF-27](requisitos/rf-reservas.md#rf-27), [RF-33](requisitos/rf-contas.md#rf-33), [RF-33.1](requisitos/rf-contas.md#rf-33-1), [RF-33.2](requisitos/rf-contas.md#rf-33-2), [RF-34](requisitos/rf-contas.md#rf-34), [RF-34.1](requisitos/rf-contas.md#rf-34-1), [RF-35](requisitos/rf-contas.md#rf-35), [RF-36](requisitos/rf-contas.md#rf-36), [RF-37](requisitos/rf-contas.md#rf-37) |
| <a id="ns-12"></a>NS-12 | Consultar o histórico de cada reserva: cada mudança, quem fez, quando, de qual situação para qual e com que motivo. | Cliente, Gestor, Solicitante | Extra (RES-07): [histórico da reserva](glossario.md#historico) ([DEC-05](decisoes/DEC-05.md)). | [RF-22](requisitos/rf-reservas.md#rf-22) |
| <a id="ns-13"></a>NS-13 | Saber o resultado de cada operação e, quando ela for impedida, o que a impediu e o que mudar para conseguir. | Solicitante, Gestor | F5 e F6: mensagens de sucesso e de erro, com o campo a corrigir quando houver. | [RF-38](requisitos/rf-gerais.md#rf-38) (e, como origem secundária, todas as recusas) |
| <a id="ns-14"></a>NS-14 | Ter os próprios pedidos protegidos: um solicitante não conhece quem pediu outros espaços nem para quê. | Solicitante, Cliente | Extra (AUT-05): o Solicitante só lê as próprias reservas. A agenda do dia mostra período e situação, sem dados pessoais ([DEC-11](decisoes/DEC-11.md)). | [RF-23](requisitos/rf-reservas.md#rf-23) |
| <a id="ns-15"></a>NS-15 | Obter acesso ao sistema sem depender de um gestor. | Visitante | Extra (AUT-04): cadastro de solicitante. | [RF-32](requisitos/rf-contas.md#rf-32), [RF-32.1](requisitos/rf-contas.md#rf-32-1), [RF-32.2](requisitos/rf-contas.md#rf-32-2), [RF-32.3](requisitos/rf-contas.md#rf-32-3) |
| <a id="ns-16"></a>NS-16 | Instalar, executar e demonstrar o sistema num ambiente novo seguindo instruções escritas, com dados de exemplo. | Equipe de TI, Professor | README com o passo a passo e o comando de dados de exemplo (INF-06). | [RF-39](requisitos/rf-gerais.md#rf-39), [RF-40](requisitos/rf-gerais.md#rf-40) |

## 3. Escopo inicial do sistema

### Dentro do escopo

As seis funcionalidades mínimas, em linguagem de negócio:

1. **Espaços (F1):** o Gestor cadastra espaços esportivos; qualquer usuário identificado os lista e consulta.
2. **Pedido (F2):** o usuário identificado pede o uso de um espaço numa data e horário, com finalidade; o pedido nasce Solicitado.
3. **Consulta (F3):** pedidos consultados por espaço, situação, data e solicitante, sozinhos ou combinados.
4. **Decisão (F4):** a situação do pedido muda entre cinco estados (Solicitada, Confirmada, Recusada, Cancelada, Concluída), só pelas transições permitidas.
5. **Bloqueio de operações inválidas (F5):** campos obrigatórios vazios, espaço inexistente ou inativo, horário inválido, data retroativa, conflito de horário e transição não permitida são recusados sem alterar nada.
6. **Mensagens (F6):** toda operação termina com uma mensagem de sucesso ou de erro.

Extras já implementados, depois das seis:

- Identificação por e-mail e senha, cadastro de solicitante, perfis Solicitante e Gestor e restrição das ações por perfil ([DEC-04](decisoes/DEC-04.md)).
- Edição, desativação e reativação de espaços ([DEC-06](decisoes/DEC-06.md)).
- Histórico de cada reserva ([DEC-05](decisoes/DEC-05.md)).
- Regras de agenda: período de funcionamento, duração mínima e máxima e antecedência máxima ([DEC-07](decisoes/DEC-07.md)).
- Agenda do dia de um espaço, sem dados pessoais ([DEC-11](decisoes/DEC-11.md)).
- Dados de exemplo para demonstração.

### Fora do escopo

Lista fechada. O que não está em "dentro do escopo" nem aqui só entra por um CR ([`mudancas/`](mudancas/README.md)).

| Fora do escopo | Observação |
|---|---|
| Pagamento ou cobrança pelo uso | O uso dos espaços é tratado como gratuito. |
| Integração com sistemas da instituição (cadastro acadêmico, login institucional) | Cada pessoa se cadastra; a matrícula não é conferida com a instituição ([DEC-09](decisoes/DEC-09.md)). |
| Notificações por e-mail, SMS ou aplicativo de mensagens | A situação é acompanhada consultando o sistema. |
| Reservas recorrentes (ex.: toda terça às 18:00) | Cada pedido é de um dia (premissa P-05). |
| Empréstimo de material esportivo | — |
| Lista de espera para um horário ocupado | — |
| Limite de quantidade de pedidos por pessoa | — |
| Bloqueio de períodos para manutenção ou eventos da instituição | Hoje, retirar um espaço de uso é desativá-lo por inteiro. |
| Regras de uso diferentes por espaço, por dia da semana ou em feriados | [DEC-07](decisoes/DEC-07.md). O horário por espaço entra com o [CR-03](mudancas/CR-03-horario-por-espaco.md) (ESP-07); por dia da semana ou em feriados continua fora. |
| Alterar data, horário ou espaço de um pedido já feito | Pede-se outro e cancela-se o anterior. |
| Excluir reservas ou espaços | Reservas só mudam de situação; espaços são desativados ([DEC-06](decisoes/DEC-06.md)). |
| Recuperar ou trocar senha; trocar o perfil pela tela | O perfil só é alterado pela administração (Equipe de TI). |
| Controle de presença no uso do espaço | — |
| Relatórios e estatísticas de uso | — |
| Aplicativo de celular instalável | — |
| Publicação em servidor na internet | Execução local (restrição). |

### Restrições

| Restrição | Origem |
|---|---|
| Entrega em 20/11/2026 (ZIP com `README.md`, `src/` e `docs/`). | Enunciado de Projeto de Programação |
| Python é obrigatório. | Enunciado, Seção 7 |
| React no frontend. | [DEC-01](decisoes/DEC-01.md) |
| Docker e PostgreSQL na execução. | [DEC-02](decisoes/DEC-02.md), [DEC-03](decisoes/DEC-03.md) |
| Execução local, por quem corrige, seguindo o README. | Enunciado |
| `modelagem.pdf` com até 6 páginas e `contribuicoes.pdf` com até 2. | Enunciado |
| Demonstração ao vivo em até 10 minutos, com todos os integrantes. | Enunciado |
| Extras não podem atrasar as seis funcionalidades mínimas. | Enunciado; [DEC-04](decisoes/DEC-04.md) |

### Premissas

Premissa é o que o grupo assume como verdadeiro sem ter confirmado. Se uma premissa cair, ela vira CR.

| ID | Premissa | Se não valer |
|---|---|---|
| P-01 | Não há cliente real nomeado. O grupo representa a instituição, e o professor é a referência para as dúvidas de regra. | Necessidades e valores de regra precisam ser validados com o cliente real. |
| P-02 | Solicitantes e gestores têm e-mail e matrícula e se identificam por e-mail e senha. | [DEC-09](decisoes/DEC-09.md) e o cadastro mudam. A DEC-09, decidida em 06/11/2026, fixa a matrícula só com dígitos ([CR-04](mudancas/CR-04-matricula-so-digitos.md), AUT-12); a premissa continua valendo. |
| P-03 | Todos os horários são de Brasília ([fuso horário](glossario.md#fuso-horario)). | Regras de agenda e conflito precisam de fuso por espaço. |
| P-04 | As regras de agenda são as mesmas para todos os espaços e todos os dias. | [DEC-07](decisoes/DEC-07.md). Deixa de valer quando o [CR-03](mudancas/CR-03-horario-por-espaco.md) for aplicado (ESP-07): a DEC-07, decidida em 06/11/2026, traz o horário de funcionamento por espaço; duração e antecedência continuam iguais para todos. |
| P-05 | Um pedido é de um espaço, num único dia, num [intervalo](glossario.md#intervalo-de-horario) contínuo. | Recorrência e vários espaços por pedido exigem novos requisitos. |
| P-06 | Os usuários Gestor são criados pela Equipe de TI, nunca pelo cadastro público. | [DEC-04](decisoes/DEC-04.md). |
| P-07 | O acesso é por navegador, em português. | — |

## 4. Sucesso e risco

### Critérios de sucesso

| ID | Critério | Como verificar |
|---|---|---|
| CS-01 | Nenhum par de reservas que ocupam horário no mesmo espaço tem um momento em comum. | Testes de conflito e de concorrência ([testes de reservas](../testes_de_reservas.md)); na demonstração, o pedido no horário de conflito dos dados de exemplo é recusado. |
| CS-02 | 100% das mudanças de situação aceitas aparecem no histórico com data e hora, autor, situação anterior e nova; 100% das recusas e dos cancelamentos têm motivo. | Testes de histórico; consulta ao histórico na demonstração. |
| CS-03 | Um integrante que não escreveu o roteiro executa o sistema num clone novo seguindo só o README, sem ajuda, até entrar com os usuários de teste. | Checklist pré-entrega do grupo, com data e nome de quem executou. |
| CS-04 | As seis funcionalidades, uma entrada inválida e uma ação sem permissão são demonstradas em até 10 minutos. | Ensaio cronometrado. |
| CS-05 | Toda recusa prevista numa regra de negócio responde com um código próprio e uma mensagem em português; nenhuma regra violada termina em erro interno. | Testes de API e catálogos de testes. |
| CS-06 | Nenhum Solicitante lê uma reserva de outra pessoa, e toda rota da API tem regra de acesso declarada e testada. | [Matriz de acesso](../matriz_de_acesso.md). |
| CS-07 | Os documentos de requisitos chegam à versão 1.0 (primeira baseline) antes de 20/11/2026, com cada DEC decidida ou aceita como premissa. | Manifesto em [`baselines/`](baselines/README.md). |

### Riscos

Probabilidade e impacto em Baixa, Média ou Alta. Resposta: **mitigar** (reduzir), **aceitar** (conviver, com plano) ou **evitar** (tirar a causa).

| ID | Risco | Prob. | Impacto | Resposta |
|---|---|---|---|---|
| R-01 | Prazo: 17 dias até 20/11/2026, com requisitos (REQ-02 em diante), `modelagem.pdf`, `contribuicoes.pdf` e ensaio ainda por fazer. | Alta | Alto | Mitigar: nenhuma funcionalidade nova; documentação e ensaio priorizados. |
| R-02 | O ambiente de correção não executa o sistema (sem Docker, ou Docker no Windows com finais de linha e arquivos montados diferentes). | Média | Alto | Mitigar: CS-03 num clone novo, `.gitattributes` com LF, pré-requisitos no README. |
| R-03 | Extras atrasarem as seis funcionalidades mínimas. | Baixa | Alto | Evitar: as seis já estão integradas; contingência da [DEC-04](decisoes/DEC-04.md). |
| R-04 | Documentos de requisitos e modelagem divergirem do código entregue. | Média | Alto | Mitigar: glossário com o nome no código; requisitos e código mudam no mesmo PR. |
| R-05 | A rubrica de Requisitos, o formato de entrega e a ferramenta dos diagramas não estão definidos (pontos de atenção da disciplina). | Alta | Médio | Mitigar: perguntar ao professor na Aula 7 (06/11/2026). Perguntado: numeração `A`/`E` ([DEC-14](decisoes/DEC-14.md)), Dado/Quando/Então ([DEC-15](decisoes/DEC-15.md)), rastreabilidade até o código ([DEC-16](decisoes/DEC-16.md)), versão ([DEC-17](decisoes/DEC-17.md)), Index Card ([DEC-18](decisoes/DEC-18.md)), diagramas ([DEC-19](decisoes/DEC-19.md)) e entrega separada dos documentos de Requisitos ([DEC-20](decisoes/DEC-20.md)); a rubrica não foi respondida, e os outros documentos pedidos serão detalhados depois. |
| R-06 | Conhecimento concentrado em poucos integrantes; a apresentação exige domínio de todos. | Média | Alto | Mitigar: revisão por pares destes documentos e ensaio com todos. |
| R-07 | Cliente fictício (P-01): necessidades e valores de regra sem validação externa. | Alta | Médio | Aceitar: premissa declarada e DECs com o professor como referência. |
| R-08 | [DEC-05](decisoes/DEC-05.md): o professor esperar que tentativas recusadas também fiquem registradas (o modelo de aceite dele inclui "tentativa registrada"). | Média | Médio | Mitigar: confirmar; se mudar, CR sobre o histórico. Ocorreu: a DEC-05, decidida em 06/11/2026, pede o registro das tentativas recusadas ([CR-02](mudancas/CR-02-tentativas-recusadas-no-historico.md), RES-12). |
| R-09 | [DEC-06](decisoes/DEC-06.md): o cliente querer que desativar um espaço cancele ou bloqueie as reservas futuras dele. | Média | Médio | Mitigar: confirmar; a mudança cruza dois contextos do código. Não ocorreu: a DEC-06 foi confirmada em 06/11/2026. |
| R-10 | [DEC-07](decisoes/DEC-07.md): o funcionamento real ter outros horários, ou horários por espaço ou por dia. | Média | Médio | Mitigar: valores são constantes únicas; horários por espaço ficam fora do escopo até um CR. Ocorreu: a DEC-07, decidida em 06/11/2026, traz 07:00 às 00:00 e o horário por espaço ([CR-03](mudancas/CR-03-horario-por-espaco.md), ESP-07). |
| R-11 | [DEC-08](decisoes/DEC-08.md): manter a cobertura-alvo consumir tempo das tarefas restantes. | Baixa | Baixo | Aceitar: meta interna do grupo, não exigida. A DEC-08 foi confirmada em 06/11/2026. |
| R-12 | [DEC-09](decisoes/DEC-09.md): o formato real da matrícula ser mais restrito e invalidar dados de exemplo. | Média | Baixo | Mitigar: regra isolada numa função; ajustar exemplos junto. Ocorreu em parte: a DEC-09, decidida em 06/11/2026, exige só dígitos ([CR-04](mudancas/CR-04-matricula-so-digitos.md), AUT-12); os dados de exemplo já são só dígitos. |
| R-13 | [DEC-10](decisoes/DEC-10.md): existirem espaços reais com o mesmo nome (ex.: em unidades diferentes). | Baixa | Baixo | Aceitar: nomes distintos por convenção até a confirmação. A DEC-10 foi confirmada em 06/11/2026. |
| R-14 | [DEC-11](decisoes/DEC-11.md): o cliente considerar que mostrar períodos ocupados por outras pessoas expõe o uso. | Baixa | Médio | Mitigar: confirmar; a agenda pode ser restrita sem afetar o pedido. Não ocorreu: a DEC-11 foi confirmada em 06/11/2026. |

## 5. Checklist de revisão por pares

Preparação para a versão 0.2 (revisão por pares, A4·s7). **Em branco: preenchido por um revisor do grupo que não seja o autor.** Um comentário útil localiza o trecho, descreve o risco e propõe uma correção.

Revisor: Matheus Cezar Santos • Data: [dd/mm/aaaa]

| Pergunta | Sim/Não | Trecho e comentário |
|---|---|---|
| A condição de entrada de cada necessidade está clara (quem precisa, em que momento)? | | |
| Todo termo do domínio usado aqui está no glossário, com o mesmo sentido? | | |
| Toda dúvida aparece como DEC, e não como regra afirmada? | | |
| Há contradição entre seções, com o glossário ou com uma DEC? | | |
| As opções descritas (ex.: recusar × cancelar) têm resultados distintos e verificáveis? | | |
| Escopo e fora do escopo são excludentes e não deixam lacuna relevante? | | |
| Os critérios de sucesso são mensuráveis? | | |

**Auditoria das necessidades** (marque ✔ ou ✘ e comente):

| NS | Clara | Necessária | Verificável | Rastreável | Comentário |
|---|---|---|---|---|---|
| NS-01 | | | | | |
| NS-02 | | | | | |
| NS-03 | | | | | |
| NS-04 | | | | | |
| NS-05 | | | | | |
| NS-06 | | | | | |
| NS-07 | | | | | |
| NS-08 | | | | | |
| NS-09 | | | | | |
| NS-10 | | | | | |
| NS-11 | | | | | |
| NS-12 | | | | | |
| NS-13 | | | | | |
| NS-14 | | | | | |
| NS-15 | | | | | |
| NS-16 | | | | | |
