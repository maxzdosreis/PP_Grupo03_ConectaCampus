# Fichas resumidas dos casos de uso

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **UCR-01 • 0.1 • Rascunho** (fichas resumidas, formato Cockburn "casual") | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/casos-de-uso/fichas-resumidas.md` |

Fichas resumidas dos casos de uso de objetivo que não têm ficha completa e, num bloco separado, dos casos de uso de apoio da Equipe de TI ([decisão h](README.md#decisao-h)). Cada uma tem ator, meta, precondição, fluxo principal curto, as alternativas e exceções principais (com condição, resultado para o ator, estado depois e requisito, como nas completas) e os RF cobertos. As âncoras levam o prefixo do caso de uso (`uc07-e3-1` = E3.1 de UC-07), porque todas ficam neste arquivo ([decisão i](README.md#decisao-i)). As fichas completas são [UC-02](UC-02-autenticar.md), [UC-04](UC-04-solicitar-reserva.md), [UC-10](UC-10-alterar-situacao-da-reserva.md) e [UC-14](UC-14-cadastrar-espaco.md).

Todas as exceções deixam o sistema como estava: nada é gravado, e a pessoa fica sabendo o que impediu a operação ([RNF-R03](../requisitos/rnf.md#rnf-r03), [RF-38](../requisitos/rf-gerais.md#rf-38)).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: UC-01, UC-03, UC-06 a UC-09, UC-15 e UC-16 e o bloco de apoio UC-20 a UC-22 (REQ-04). Sem aprovação. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Linha "Histórias derivadas" em cada caso de uso (REQ-05), sem mudar o fluxo. Sem aprovação. |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Bloco de apoio aponta para o README da raiz e o do backend, com a divisão do README (DOC-09). Mudança editorial, sem mudar o fluxo. Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | UC-01: nota do limite de pedidos de cadastro por origem (RNF-F12, AUT-08), sem exceção nem RF novos. Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | UC-22: confere também o cache, com a exceção E2.2 · Cache fora do ar; UC-01: a recusa com o serviço de contagem fora do ar (Redis, AUT-08). Sem aprovação. |
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | UC-07: a consulta em páginas, com o total, nos passos 2 e 4; alternativas novas A2.3 (ver outra página), A2.4 (página além da última) e A3.2 (mudar um critério recomeça da primeira página); a exceção E3.1 inclui a página e o tamanho inválidos; RF-12.2 nos RFs cobertos (RES-10). Sem aprovação. |

## Sumário

**Negócio:** [UC-01 Cadastrar-se](#uc-01) · [UC-03 Consultar espaços](#uc-03) · [UC-06 Consultar agenda do dia](#uc-06) · [UC-07 Consultar reservas](#uc-07) · [UC-08 Consultar detalhe da reserva](#uc-08) · [UC-09 Consultar histórico da reserva](#uc-09) · [UC-15 Editar espaço](#uc-15) · [UC-16 Desativar ou reativar espaço](#uc-16)

**Apoio:** [UC-20 Criar usuário Gestor](#uc-20) · [UC-21 Carregar dados de exemplo](#uc-21) · [UC-22 Verificar se o sistema está no ar](#uc-22)

---

## <a id="uc-01"></a>UC-01 · Cadastrar-se

| Campo | Conteúdo |
|---|---|
| **Ator primário** | [Visitante](../glossario.md#visitante) |
| **Meta** | Obter acesso ao sistema como Solicitante, sem depender de um Gestor. |
| **Precondição** | O visitante não está identificado. |
| **Ficha completa relacionada** | [UC-02 Autenticar](UC-02-autenticar.md): o cadastro termina com a pessoa já identificada ([A1.2](UC-02-autenticar.md#a1-2)). |

**Fluxo principal**

1. <a id="uc01-p1"></a>O Visitante pede para criar uma conta.
2. <a id="uc01-p2"></a>O Visitante informa nome, [matrícula](../glossario.md#matricula), e-mail e senha.
3. <a id="uc01-p3"></a>O sistema confere, nesta ordem: dados presentes e e-mail bem formado; nome, matrícula e e-mail; senha pela [política de senha](../glossario.md#politica-de-senha); e-mail e matrícula ainda não usados.
4. <a id="uc01-p4"></a>O sistema cria a conta com o perfil Solicitante (nunca Gestor, mesmo que o pedido diga outra coisa), informa "Cadastro realizado com sucesso." e já identifica a pessoa, como no [passo 4 de UC-02](UC-02-autenticar.md#p4), seguindo para pedir uma reserva.

**Alternativas**

- <a id="uc01-a1-1"></a>**A1.1** · Vindo de algo que exige identificação: depois do passo 4, a pessoa volta ao ponto em que estava ([UC-02 A1.1](UC-02-autenticar.md#a1-1)).

**Exceções**

| Exceção | Condição | Resultado para o ator | Estado depois | Requisito |
|---|---|---|---|---|
| <a id="uc01-e3-1"></a>E3.1 · Dados ausentes ou inválidos | Falta um dado; o nome só tem espaços ou passa de 150 caracteres; a matrícula passa de 20 caracteres ou tem espaço; o e-mail está mal formado. | A regra violada junto a cada dado (por exemplo, 'O campo "Nome" é obrigatório.'). | Nenhuma conta é criada. | [RF-32.1](../requisitos/rf-contas.md#rf-32-1) ([DEC-09](../decisoes/DEC-09.md)) |
| <a id="uc01-e3-2"></a>E3.2 · Senha fraca | A senha é curta (menos de 8 caracteres), comum, só de números ou parecida com o nome, o e-mail ou a matrícula. | Junto à senha, cada motivo da recusa. | Nenhuma conta é criada. | [RF-32.2](../requisitos/rf-contas.md#rf-32-2) |
| <a id="uc01-e3-3"></a>E3.3 · E-mail ou matrícula já usados | O e-mail (sem diferenciar maiúsculas) ou a matrícula já pertencem a outra conta. | Junto ao dado, que ele já está cadastrado; a pessoa pode entrar ([UC-02](UC-02-autenticar.md)) se a conta for dela. | Nenhuma conta é criada; a outra conta não muda. | [RF-32.3](../requisitos/rf-contas.md#rf-32-3) |

**Fora das exceções:** antes do passo 3, o sistema também limita os pedidos de cadastro a partir da mesma origem; acima do limite, informa "Muitas tentativas. Tente de novo em N segundos." e não cria a conta ([RNF-F12](../requisitos/rnf.md#rnf-f12)); se o serviço que conta os pedidos estiver fora do ar, informa "Serviço temporariamente indisponível. Tente de novo em alguns instantes." e também não cria. É uma garantia de segurança, sem RF de recusa próprio.

**RFs cobertos:** [RF-32](../requisitos/rf-contas.md#rf-32) → [passos 1 a 4](#uc01-p1) · [RF-32.1](../requisitos/rf-contas.md#rf-32-1) → [E3.1](#uc01-e3-1) · [RF-32.2](../requisitos/rf-contas.md#rf-32-2) → [E3.2](#uc01-e3-2) · [RF-32.3](../requisitos/rf-contas.md#rf-32-3) → [E3.3](#uc01-e3-3)

**Histórias derivadas:** [US-01 Criar minha conta](../historias/US-01-criar-minha-conta.md)

---

## <a id="uc-03"></a>UC-03 · Consultar espaços

| Campo | Conteúdo |
|---|---|
| **Ator primário** | [Solicitante](../glossario.md#solicitante) (e o Gestor, por herança) |
| **Meta** | Saber quais espaços esportivos existem, de que tipo são e quais aceitam pedidos. |
| **Precondição** | Ator autenticado ([UC-02](UC-02-autenticar.md); [decisão d](README.md#decisao-d)). |
| **Ficha completa relacionada** | [UC-04 Solicitar reserva](UC-04-solicitar-reserva.md) ([A1.1](UC-04-solicitar-reserva.md#a1-1)) e [UC-14 Cadastrar espaço](UC-14-cadastrar-espaco.md). |

**Fluxo principal**

1. <a id="uc03-p1"></a>O ator pede para ver os espaços.
2. <a id="uc03-p2"></a>O sistema mostra todos os espaços, ordenados pelo nome, com nome, tipo, capacidade e se está ativo, e a quantidade encontrada.
3. <a id="uc03-p3"></a>O ator escolhe um espaço ativo para pedir uma reserva e segue em [UC-04 A1.1](UC-04-solicitar-reserva.md#a1-1).

**Alternativas**

- <a id="uc03-a2-1"></a>**A2.1** · Filtrar: o ator restringe a lista por um dos [tipos de espaço](../glossario.md#tipo-de-espaco) (que o sistema apresenta), por "somente ativos" ou pelos dois; o sistema mostra só os que atendem a todos os critérios. Sem resultado, informa "Nenhum espaço encontrado." e oferece limpar os critérios.
- <a id="uc03-a2-2"></a>**A2.2** · Ver um espaço: o ator escolhe um espaço e o sistema mostra nome, tipo, capacidade e se está ativo.
- <a id="uc03-a2-3"></a>**A2.3** · Manter espaços (só o Gestor): segue em [UC-14](UC-14-cadastrar-espaco.md), [UC-15](#uc-15) ou [UC-16](#uc-16).

**Exceções**

| Exceção | Condição | Resultado para o ator | Estado depois | Requisito |
|---|---|---|---|---|
| <a id="uc03-e2-1"></a>E2.1 · Tipo desconhecido no filtro | Em A2.1, o tipo informado não é um dos tipos de espaço. | No critério tipo, que o valor não é aceito. | Nenhum espaço muda; a lista não é filtrada. | [RF-02.1](../requisitos/rf-espacos.md#rf-02-1) |
| <a id="uc03-e2-2"></a>E2.2 · Espaço inexistente | Em A2.2, não existe espaço com a identificação escolhida. | "Espaço de código «n» não encontrado." | Nenhum espaço muda. | [RF-09](../requisitos/rf-espacos.md#rf-09) |

**RFs cobertos:** [RF-01](../requisitos/rf-espacos.md#rf-01) → [passo 2](#uc03-p2) · [RF-02](../requisitos/rf-espacos.md#rf-02) → [A2.1](#uc03-a2-1) · [RF-02.1](../requisitos/rf-espacos.md#rf-02-1) → [E2.1](#uc03-e2-1) · [RF-03](../requisitos/rf-espacos.md#rf-03) → [A2.2](#uc03-a2-2) · [RF-04](../requisitos/rf-espacos.md#rf-04) → [A2.1](#uc03-a2-1) (os tipos do filtro) · [RF-09](../requisitos/rf-espacos.md#rf-09) → [E2.2](#uc03-e2-2)

**Histórias derivadas:** [US-04 Consultar os espaços](../historias/US-04-consultar-os-espacos.md)

---

## <a id="uc-06"></a>UC-06 · Consultar agenda do dia

| Campo | Conteúdo |
|---|---|
| **Ator primário** | Solicitante (e o Gestor, por herança), pela extensão de UC-04 no ponto "antes de enviar o pedido". |
| **Meta** | Escolher um horário que será aceito, vendo antes do pedido o que está ocupado e livre no espaço e no dia. |
| **Precondição** | Ator autenticado; espaço e data escolhidos no [passo 3 de UC-04](UC-04-solicitar-reserva.md#p3). |
| **Ficha completa relacionada** | [UC-04 A3.1](UC-04-solicitar-reserva.md#a3-1). |

**Fluxo principal**

1. <a id="uc06-p1"></a>O ator, com espaço e data escolhidos, pede a [agenda do dia](../glossario.md#agenda-do-dia).
2. <a id="uc06-p2"></a>O sistema confere que o espaço e a data foram informados e que o espaço aceita pedidos.
3. <a id="uc06-p3"></a>O sistema mostra os [horários ocupados](../glossario.md#horario-ocupado) por reservas Solicitadas ou Confirmadas daquele espaço no dia, em ordem de início, cada um só com início, término e situação (nunca quem reservou nem para quê), e a quantidade ("1 horário ocupado neste dia.").
4. <a id="uc06-p4"></a>O sistema mostra o horário de funcionamento e os [horários livres](../glossario.md#horario-livre): dentro do funcionamento, com pelo menos 30 minutos e, para hoje, a partir do próximo múltiplo de 5 minutos.
5. <a id="uc06-p5"></a>O ator usa um horário livre: o sistema preenche o início do pedido com o começo dele e o término com o [término sugerido](../glossario.md#termino-sugerido). Segue no [passo 3 de UC-04](UC-04-solicitar-reserva.md#p3).

**Alternativas**

- <a id="uc06-a1-1"></a>**A1.1** · Sem espaço ou sem data escolhidos: o sistema só orienta a escolher os dois e não consulta nada.
- <a id="uc06-a4-1"></a>**A4.1** · Data que não é [reservável](../glossario.md#data-reservavel) (o fechamento daquele dia já passou ou ela passa da data limite): o sistema informa o motivo, com a mensagem da regra correspondente, não mostra horário livre e mantém os ocupados.
- <a id="uc06-a4-2"></a>**A4.2** · Depois de um pedido recusado por conflito ([UC-04 E9.1](UC-04-solicitar-reserva.md#e9-1)), a agenda é atualizada e passa a mostrar o período ocupado.

**Exceções**

| Exceção | Condição | Resultado para o ator | Estado depois | Requisito |
|---|---|---|---|---|
| <a id="uc06-e2-1"></a>E2.1 · Sem espaço ou sem data | A agenda é pedida sem o espaço ou sem a data. | O critério que falta. | Nada muda. | [RF-29.1](../requisitos/rf-agenda.md#rf-29-1) |
| <a id="uc06-e2-2"></a>E2.2 · Espaço inexistente ou inativo | O espaço não existe ou está inativo. | As mesmas mensagens do pedido de reserva ([UC-04 E8.1 e E8.2](UC-04-solicitar-reserva.md#e8-1)). | Nada muda. | [RF-29.2](../requisitos/rf-agenda.md#rf-29-2) |
| <a id="uc06-e3-1"></a>E3.1 · Agenda não pôde ser obtida | Falha de comunicação ao consultar. | Que não foi possível carregar a agenda e que o ator ainda pode solicitar normalmente, com a opção de tentar de novo. | Nada muda; o pedido de UC-04 continua possível e é conferido por inteiro. | [RF-29](../requisitos/rf-agenda.md#rf-29) (a agenda é ajuda, não regra) |

**RFs cobertos:** [RF-28](../requisitos/rf-agenda.md#rf-28) → [passo 5](#uc06-p5) (a duração máxima do término sugerido) · [RF-29](../requisitos/rf-agenda.md#rf-29) → [passo 3](#uc06-p3) · [RF-29.1](../requisitos/rf-agenda.md#rf-29-1) → [E2.1](#uc06-e2-1) · [RF-29.2](../requisitos/rf-agenda.md#rf-29-2) → [E2.2](#uc06-e2-2) · [RF-30](../requisitos/rf-agenda.md#rf-30) → [passos 4 e 5](#uc06-p4) · [RF-31](../requisitos/rf-agenda.md#rf-31) → [A4.1](#uc06-a4-1)

**Histórias derivadas:** [US-09 Ver a agenda do dia antes de pedir](../historias/US-09-ver-a-agenda-do-dia.md)

---

## <a id="uc-07"></a>UC-07 · Consultar reservas

| Campo | Conteúdo |
|---|---|
| **Ator primário** | Solicitante (e o Gestor, por herança) |
| **Meta** | Localizar reservas por critérios combinados (o Solicitante, só as próprias) e ver as ações disponíveis em cada uma. |
| **Precondição** | Ator autenticado. |
| **Ficha completa relacionada** | [UC-10 Alterar situação da reserva](UC-10-alterar-situacao-da-reserva.md) (a ação parte daqui, [passo 1](UC-10-alterar-situacao-da-reserva.md#p1)). |

**Fluxo principal**

1. <a id="uc07-p1"></a>O ator pede para ver as reservas.
2. <a id="uc07-p2"></a>O sistema mostra as reservas que o ator pode ver — o Gestor, todas; o Solicitante, só as próprias, como "Minhas reservas" —, ordenadas pelo início, em páginas de até 20, com data e horário, espaço, solicitante, finalidade, situação com o motivo, as [ações disponíveis](../glossario.md#acao-disponivel) de cada uma, o total encontrado, a página atual e o número de páginas.
3. <a id="uc07-p3"></a>O ator informa um ou mais critérios: espaço, situação (entre as situações de reserva, na ordem do ciclo de vida), data e, só para o Gestor, solicitante (trecho do nome ou da matrícula) e "somente as minhas".
4. <a id="uc07-p4"></a>O sistema mostra só as reservas que atendem a todos os critérios, a partir da primeira página, com a quantidade.

**Alternativas**

- <a id="uc07-a2-1"></a>**A2.1** · Escolher uma reserva para acompanhar: segue em [UC-08](#uc-08), e a volta mantém os critérios.
- <a id="uc07-a2-2"></a>**A2.2** · Escolher uma ação de uma reserva: segue em [UC-10](UC-10-alterar-situacao-da-reserva.md); depois, a lista é consultada de novo com os mesmos critérios.
- <a id="uc07-a2-3"></a>**A2.3** · Ver outra página: o ator pede a página seguinte ou a anterior, e o sistema mostra aquela página do mesmo resultado, com os mesmos critérios e o mesmo total; a volta de uma reserva acompanhada ([A2.1](#uc07-a2-1)) também mantém a página.
- <a id="uc07-a2-4"></a>**A2.4** · Página além da última (o resultado encolheu entre duas consultas, por uma mudança de situação ou de critério): o sistema não recusa; informa que não há reservas naquela página, com o total e o número de páginas atuais, e o ator passa a ver a última página que existe.
- <a id="uc07-a4-1"></a>**A4.1** · Nenhuma reserva atende: "Nenhuma reserva encontrada.", com a opção de limpar os critérios. Um espaço inexistente no critério também dá lista vazia, não erro.
- <a id="uc07-a3-1"></a>**A3.1** · O Solicitante informa um solicitante ou "somente as minhas = não": o critério é ignorado, e ele continua vendo só as próprias.
- <a id="uc07-a3-2"></a>**A3.2** · O ator muda um critério ou limpa os critérios quando está numa página que não é a primeira: o resultado novo começa da primeira página.

**Exceções**

| Exceção | Condição | Resultado para o ator | Estado depois | Requisito |
|---|---|---|---|---|
| <a id="uc07-e3-1"></a>E3.1 · Critério em formato inválido | Situação fora da lista, data que não existe, espaço que não é um número, página que não é um número inteiro a partir de 1 ou tamanho de página fora de 1 a 100. | "Verifique os dados informados.", com o critério com problema. | Nenhuma reserva muda. | [RF-12.1](../requisitos/rf-reservas.md#rf-12-1) |

**RFs cobertos:** [RF-12](../requisitos/rf-reservas.md#rf-12) → [passos 3 e 4](#uc07-p3) · [RF-12.1](../requisitos/rf-reservas.md#rf-12-1) → [E3.1](#uc07-e3-1) · [RF-12.2](../requisitos/rf-reservas.md#rf-12-2) → [passo 2](#uc07-p2), [A2.3](#uc07-a2-3), [A2.4](#uc07-a2-4), [A3.2](#uc07-a3-2) · [RF-13](../requisitos/rf-reservas.md#rf-13) → [passo 2](#uc07-p2), [A3.1](#uc07-a3-1) · [RF-15](../requisitos/rf-reservas.md#rf-15) → [passo 3](#uc07-p3) · [RF-16](../requisitos/rf-reservas.md#rf-16) → [passo 2](#uc07-p2)

**Histórias derivadas:** [US-10 Acompanhar minhas reservas](../historias/US-10-acompanhar-minhas-reservas.md), [US-11 Acompanhar todas as reservas](../historias/US-11-acompanhar-todas-as-reservas.md)

---

## <a id="uc-08"></a>UC-08 · Consultar detalhe da reserva

| Campo | Conteúdo |
|---|---|
| **Ator primário** | Solicitante (e o Gestor, por herança) |
| **Meta** | Acompanhar uma reserva: os dados, a situação atual com o motivo e as ações disponíveis. |
| **Precondição** | Ator autenticado. |
| **Ficha completa relacionada** | [UC-10](UC-10-alterar-situacao-da-reserva.md) (as ações) e [UC-04](UC-04-solicitar-reserva.md) ([A11.2](UC-04-solicitar-reserva.md#a11-2)). |

**Fluxo principal**

1. <a id="uc08-p1"></a>O ator escolhe uma reserva (pela consulta, [UC-07](#uc-07), ou logo depois de pedi-la).
2. <a id="uc08-p2"></a>O sistema confere que a reserva existe e é visível ao ator.
3. <a id="uc08-p3"></a>O sistema mostra o espaço, a data e o horário, o solicitante com a matrícula, o momento do pedido, a finalidade, a situação com o motivo e as ações disponíveis para o ator.

**Alternativas**

- <a id="uc08-a3-1"></a>**A3.1** · Ver o histórico (ponto de extensão "ver o histórico"): segue em [UC-09](#uc-09).
- <a id="uc08-a3-2"></a>**A3.2** · Escolher uma ação: segue em [UC-10](UC-10-alterar-situacao-da-reserva.md); depois, a reserva e o histórico são mostrados de novo, já com a mudança.
- <a id="uc08-a3-3"></a>**A3.3** · Voltar às reservas: o sistema volta à consulta com os critérios que o ator usava.

**Exceções**

| Exceção | Condição | Resultado para o ator | Estado depois | Requisito |
|---|---|---|---|---|
| <a id="uc08-e2-1"></a>E2.1 · Reserva inexistente ou de outra pessoa | A reserva não existe, a identificação é inválida ou, para o Solicitante, ela é de outra pessoa. | Que a reserva não foi encontrada, com a mesma resposta nos dois casos, e o caminho de volta às reservas. | Nada muda; a existência da reserva de outra pessoa não é revelada. | [RF-23](../requisitos/rf-reservas.md#rf-23) |

**RFs cobertos:** [RF-14](../requisitos/rf-reservas.md#rf-14) → [passo 3](#uc08-p3) · [RF-16](../requisitos/rf-reservas.md#rf-16) → [passo 3](#uc08-p3) · [RF-23](../requisitos/rf-reservas.md#rf-23) → [E2.1](#uc08-e2-1)

**Histórias derivadas:** [US-12 Ver o detalhe e o histórico de uma reserva](../historias/US-12-ver-detalhe-e-historico.md)

---

## <a id="uc-09"></a>UC-09 · Consultar histórico da reserva

| Campo | Conteúdo |
|---|---|
| **Ator primário** | Solicitante (e o Gestor, por herança), pela extensão de UC-08. |
| **Meta** | Saber quem mudou a situação da reserva, quando, de qual para qual e por quê. |
| **Precondição** | Ator autenticado, no detalhe de uma reserva ([UC-08](#uc-08)). |
| **Ficha completa relacionada** | O que este caso de uso mostra é gravado por UC-13, no [passo 10 de UC-04](UC-04-solicitar-reserva.md#p10) e no [passo 7 de UC-10](UC-10-alterar-situacao-da-reserva.md#p7). |

**Fluxo principal**

1. <a id="uc09-p1"></a>O ator pede o [histórico](../glossario.md#historico) da reserva.
2. <a id="uc09-p2"></a>O sistema confere que a reserva existe e é visível ao ator (a mesma regra do detalhe).
3. <a id="uc09-p3"></a>O sistema mostra, em ordem cronológica, a criação e cada mudança de situação aceita: data e hora, nome do autor, situação anterior e nova e motivo.

**Alternativas**

- <a id="uc09-a3-1"></a>**A3.1** · Reserva sem registros (gravada antes de existir o histórico): "Nenhuma mudança registrada."
- <a id="uc09-a3-2"></a>**A3.2** · Tentativas recusadas não aparecem: só as mudanças aceitas ([DEC-05](../decisoes/DEC-05.md)).

**Exceções**

| Exceção | Condição | Resultado para o ator | Estado depois | Requisito |
|---|---|---|---|---|
| <a id="uc09-e2-1"></a>E2.1 · Reserva inexistente ou de outra pessoa | Como em [UC-08 E2.1](#uc08-e2-1). | Que a reserva não foi encontrada, com a mesma resposta nos dois casos. | Nada muda. | [RF-23](../requisitos/rf-reservas.md#rf-23) |
| <a id="uc09-e3-1"></a>E3.1 · Histórico não pôde ser obtido | Falha de comunicação só ao consultar o histórico. | Que não foi possível carregar o histórico, com a opção de tentar de novo; o detalhe da reserva continua visível. | Nada muda. | [RF-22](../requisitos/rf-reservas.md#rf-22) |

**RFs cobertos:** [RF-22](../requisitos/rf-reservas.md#rf-22) → [passo 3](#uc09-p3) · [RF-23](../requisitos/rf-reservas.md#rf-23) → [E2.1](#uc09-e2-1)

**Histórias derivadas:** [US-12 Ver o detalhe e o histórico de uma reserva](../historias/US-12-ver-detalhe-e-historico.md)

---

## <a id="uc-15"></a>UC-15 · Editar espaço

| Campo | Conteúdo |
|---|---|
| **Ator primário** | [Gestor](../glossario.md#gestor) |
| **Meta** | Manter o nome, o tipo e a capacidade de um espaço iguais à realidade. |
| **Precondição** | Ator autenticado com o perfil Gestor. |
| **Ficha completa relacionada** | [UC-14 Cadastrar espaço](UC-14-cadastrar-espaco.md): as mesmas regras de nome, tipo e capacidade ([E5.2 a E5.5](UC-14-cadastrar-espaco.md#e5-2)) e de nome único ([E6.1](UC-14-cadastrar-espaco.md#e6-1)). |

**Fluxo principal**

1. <a id="uc15-p1"></a>O Gestor escolhe um espaço e pede para editá-lo.
2. <a id="uc15-p2"></a>O sistema mostra o nome, o tipo e a capacidade atuais e os tipos de espaço existentes.
3. <a id="uc15-p3"></a>O Gestor altera um ou mais dados e envia; só os dados alterados entram no pedido.
4. <a id="uc15-p4"></a>O sistema confere, nesta ordem: formato dos dados; o espaço existe; algum dado foi alterado; nome, tipo e capacidade pelas regras do cadastro; o nome novo não é de outro espaço.
5. <a id="uc15-p5"></a>O sistema grava os dados novos, mantém os não alterados, informa "Espaço atualizado com sucesso." e mostra o espaço atualizado.

**Alternativas**

- <a id="uc15-a3-1"></a>**A3.1** · Manter o próprio nome, ou só trocar maiúsculas por minúsculas: não conta como nome repetido.
- <a id="uc15-a3-2"></a>**A3.2** · Ativo ou inativo no pedido: é ignorado; ativar e desativar são [UC-16](#uc-16).

**Exceções**

| Exceção | Condição | Resultado para o ator | Estado depois | Requisito |
|---|---|---|---|---|
| <a id="uc15-e1-1"></a>E1.1 · Ator sem o perfil Gestor | Quem pede não é Gestor. | "Você não tem permissão para realizar esta ação." | O espaço não muda. | [RF-10](../requisitos/rf-espacos.md#rf-10) |
| <a id="uc15-e4-1"></a>E4.1 · Dado em formato inválido | A capacidade não é um número inteiro. | "Verifique os dados informados.", com o problema junto ao dado. | O espaço não muda. | [RF-06.2](../requisitos/rf-espacos.md#rf-06-2) |
| <a id="uc15-e4-2"></a>E4.2 · Espaço inexistente | Não existe espaço com a identificação escolhida. | "Espaço de código «n» não encontrado." | Nenhum espaço muda. | [RF-09](../requisitos/rf-espacos.md#rf-09) |
| <a id="uc15-e4-3"></a>E4.3 · Nenhum dado alterado | O pedido não altera nome, tipo nem capacidade. | "Informe ao menos um campo para alterar." | O espaço não muda. | [RF-06.1](../requisitos/rf-espacos.md#rf-06-1) |
| <a id="uc15-e4-4"></a>E4.4 · Dado fora das regras do cadastro | Nome em branco ou longo, tipo desconhecido ou capacidade menor que 1, como em [UC-14 E5.2 a E5.5](UC-14-cadastrar-espaco.md#e5-2). | A mensagem da regra junto ao dado. | Nenhum dado do espaço muda, nem os válidos do mesmo pedido. | [RF-06.2](../requisitos/rf-espacos.md#rf-06-2) |
| <a id="uc15-e4-5"></a>E4.5 · Nome de outro espaço | O nome novo já é de outro espaço, sem diferenciar maiúsculas. | Junto ao nome, "Já existe um espaço com este nome." | O espaço não muda. | [RF-05.2](../requisitos/rf-espacos.md#rf-05-2), [RF-06.2](../requisitos/rf-espacos.md#rf-06-2) |
| <a id="uc15-e5-1"></a>E5.1 · Espaço alterado por outra pessoa | Outra edição, desativação ou reativação do espaço foi gravada depois que o Gestor o leu. | "Este espaço foi alterado por outra pessoa enquanto você decidia. Atualize a lista e tente de novo." | Vale só a primeira alteração. | [RNF-R04](../requisitos/rnf.md#rnf-r04) |

**RFs cobertos:** [RF-04](../requisitos/rf-espacos.md#rf-04) → [passo 2](#uc15-p2) · [RF-05.2](../requisitos/rf-espacos.md#rf-05-2) → [E4.5](#uc15-e4-5) · [RF-06](../requisitos/rf-espacos.md#rf-06) → [passos 1 a 5](#uc15-p1) · [RF-06.1](../requisitos/rf-espacos.md#rf-06-1) → [E4.3](#uc15-e4-3) · [RF-06.2](../requisitos/rf-espacos.md#rf-06-2) → [E4.1](#uc15-e4-1), [E4.4](#uc15-e4-4) · [RF-09](../requisitos/rf-espacos.md#rf-09) → [E4.2](#uc15-e4-2) · [RF-10](../requisitos/rf-espacos.md#rf-10) → [E1.1](#uc15-e1-1)

**Histórias derivadas:** [US-06 Editar espaço](../historias/US-06-editar-espaco.md)

---

## <a id="uc-16"></a>UC-16 · Desativar ou reativar espaço

| Campo | Conteúdo |
|---|---|
| **Ator primário** | [Gestor](../glossario.md#gestor) |
| **Meta** | Impedir novos pedidos num espaço que deixou de poder ser usado, ou voltar a aceitá-los. |
| **Precondição** | Ator autenticado com o perfil Gestor. |
| **Ficha completa relacionada** | [UC-04 E8.2](UC-04-solicitar-reserva.md#e8-2) (o pedido recusado num espaço inativo) e [UC-10](UC-10-alterar-situacao-da-reserva.md), variação [Cancelar](UC-10-alterar-situacao-da-reserva.md#v-uc-11) (para desfazer as reservas existentes). |

**Fluxo principal**

1. <a id="uc16-p1"></a>O Gestor escolhe um espaço ativo e pede para desativá-lo.
2. <a id="uc16-p2"></a>O sistema pede a confirmação, mostrando o nome e o tipo e avisando que novos pedidos ficarão bloqueados e que as reservas já existentes continuam valendo.
3. <a id="uc16-p3"></a>O Gestor confirma.
4. <a id="uc16-p4"></a>O sistema confere que o espaço existe, ainda está ativo e não foi alterado por outra pessoa desde a leitura.
5. <a id="uc16-p5"></a>O sistema grava o espaço como inativo e informa "Espaço desativado. Novas reservas ficam bloqueadas; as existentes continuam valendo."

**Alternativas**

- <a id="uc16-a1-1"></a>**A1.1** · Reativar: o Gestor escolhe um espaço inativo e pede para reativá-lo; seguem os passos 2 a 5, e o sistema grava o espaço como ativo e informa "Espaço reativado." Ele volta a aceitar pedidos.
- <a id="uc16-a3-1"></a>**A3.1** · O Gestor desiste no passo 3: nada muda.
- <a id="uc16-a5-1"></a>**A5.1** · Desfazer as reservas do espaço desativado: o Gestor cancela, com motivo, as que quiser ([UC-11](UC-10-alterar-situacao-da-reserva.md#v-uc-11); [DEC-06](../decisoes/DEC-06.md)).

**Exceções**

| Exceção | Condição | Resultado para o ator | Estado depois | Requisito |
|---|---|---|---|---|
| <a id="uc16-e1-1"></a>E1.1 · Ator sem o perfil Gestor | Quem pede não é Gestor. | "Você não tem permissão para realizar esta ação." | O espaço não muda. | [RF-10](../requisitos/rf-espacos.md#rf-10) |
| <a id="uc16-e4-1"></a>E4.1 · Espaço inexistente | Não existe espaço com a identificação escolhida. | "Espaço de código «n» não encontrado." | Nenhum espaço muda. | [RF-09](../requisitos/rf-espacos.md#rf-09) |
| <a id="uc16-e4-2"></a>E4.2 · Espaço já inativo | Ao desativar, o espaço já está inativo. | "Este espaço já está inativo." | O espaço continua inativo. | [RF-07.1](../requisitos/rf-espacos.md#rf-07-1) |
| <a id="uc16-e4-3"></a>E4.3 · Espaço já ativo | Ao reativar ([A1.1](#uc16-a1-1)), o espaço já está ativo. | "Este espaço já está ativo." | O espaço continua ativo. | [RF-08.1](../requisitos/rf-espacos.md#rf-08-1) |
| <a id="uc16-e4-4"></a>E4.4 · Espaço alterado por outra pessoa | Outra alteração do espaço foi gravada depois da leitura (por exemplo, duas desativações ao mesmo tempo). | "Este espaço foi alterado por outra pessoa enquanto você decidia. Atualize a lista e tente de novo." | Vale só a primeira. | [RNF-R04](../requisitos/rnf.md#rnf-r04) |

**RFs cobertos:** [RF-07](../requisitos/rf-espacos.md#rf-07) → [passos 1 a 5](#uc16-p1) · [RF-07.1](../requisitos/rf-espacos.md#rf-07-1) → [E4.2](#uc16-e4-2) · [RF-08](../requisitos/rf-espacos.md#rf-08) → [A1.1](#uc16-a1-1) · [RF-08.1](../requisitos/rf-espacos.md#rf-08-1) → [E4.3](#uc16-e4-3) · [RF-09](../requisitos/rf-espacos.md#rf-09) → [E4.1](#uc16-e4-1) · [RF-10](../requisitos/rf-espacos.md#rf-10) → [E1.1](#uc16-e1-1)

**Histórias derivadas:** [US-07 Desativar e reativar espaço](../historias/US-07-desativar-e-reativar-espaco.md)

---

# Apoio (diagrama UCD-02, Equipe de TI)

Casos de uso de instalação e operação, fora do negócio ([decisão e](README.md#decisao-e)). O ator é a [Equipe de TI](../glossario.md#equipe-de-ti), que age pelos comandos de administração descritos no README da raiz e no [README do backend](../../../../src/backend/README.md#comandos).

## <a id="uc-20"></a>UC-20 · Criar usuário Gestor

| Campo | Conteúdo |
|---|---|
| **Ator primário** | Equipe de TI |
| **Meta** | Dar a uma pessoa do setor dos espaços o perfil Gestor. |
| **Precondição** | O sistema está instalado e a Equipe de TI tem acesso à administração. |
| **Ficha completa relacionada** | [UC-02 Autenticar](UC-02-autenticar.md) (o Gestor criado entra como qualquer usuário). |

**Fluxo principal**

1. <a id="uc20-p1"></a>A Equipe de TI pede para criar um usuário administrador.
2. <a id="uc20-p2"></a>A Equipe de TI informa e-mail, nome, matrícula e senha.
3. <a id="uc20-p3"></a>O sistema cria o usuário com o perfil Gestor e acesso à administração.
4. <a id="uc20-p4"></a>A pessoa entra com o e-mail e a senha ([UC-02](UC-02-autenticar.md)) e é reconhecida como Gestor.

**Alternativas**

- <a id="uc20-a1-1"></a>**A1.1** · Promover um usuário existente: pela administração, a Equipe de TI muda o perfil de um Solicitante para Gestor; vale já na próxima operação dele ([UC-02 A4.2](UC-02-autenticar.md#a4-2); [lacuna L-10](../requisitos/srs.md#l-10)).

**Exceções**

| Exceção | Condição | Resultado para o ator | Estado depois | Requisito |
|---|---|---|---|---|
| <a id="uc20-e2-1"></a>E2.1 · E-mail já cadastrado | O e-mail informado já é de outro usuário. | O sistema informa que o e-mail já está em uso e pede outro. | Nenhum usuário é criado. | [RF-37](../requisitos/rf-contas.md#rf-37) |

**RFs cobertos:** [RF-37](../requisitos/rf-contas.md#rf-37) → [passos 1 a 4](#uc20-p1), [E2.1](#uc20-e2-1)

**Histórias derivadas:** [US-17 Criar o primeiro Gestor](../historias/US-17-criar-o-primeiro-gestor.md)

## <a id="uc-21"></a>UC-21 · Carregar dados de exemplo

| Campo | Conteúdo |
|---|---|
| **Ator primário** | Equipe de TI |
| **Meta** | Ter usuários, espaços e reservas coerentes para demonstrar o sistema, com um comando. |
| **Precondição** | O sistema está instalado, em modo de desenvolvimento. |
| **Ficha completa relacionada** | As reservas de exemplo passam por [UC-04](UC-04-solicitar-reserva.md) e [UC-10](UC-10-alterar-situacao-da-reserva.md), com as mesmas regras. |

**Fluxo principal**

1. <a id="uc21-p1"></a>A Equipe de TI pede a carga dos [dados de exemplo](../glossario.md#dados-de-exemplo).
2. <a id="uc21-p2"></a>O sistema confere que está em modo de desenvolvimento.
3. <a id="uc21-p3"></a>O sistema cria, pelas mesmas regras de qualquer usuário, 1 Gestor e 2 Solicitantes, um espaço de cada tipo mais um inativo e uma reserva de cada situação, com o histórico coerente e as reservas em aberto sempre no futuro.
4. <a id="uc21-p4"></a>O sistema mostra o resumo: o que foi criado e o que já existia.

**Alternativas**

- <a id="uc21-a3-1"></a>**A3.1** · Carga repetida: o que já existe (usuário pelo e-mail, espaço pelo nome, reservas dos usuários de exemplo) não é duplicado, e o resumo diz que já existia.

**Exceções**

| Exceção | Condição | Resultado para o ator | Estado depois | Requisito |
|---|---|---|---|---|
| <a id="uc21-e2-1"></a>E2.1 · Fora do modo de desenvolvimento | O sistema está em modo de produção. | A carga é recusada, porque cria usuários com senhas conhecidas. | Nada é criado. | [RF-39](../requisitos/rf-gerais.md#rf-39) |
| <a id="uc21-e3-1"></a>E3.1 · Dado de exemplo viola uma regra | Um dado de exemplo não passa por uma regra do sistema. | "Dado de exemplo inválido: «mensagem da regra»". | Nada fica pela metade: a carga inteira é desfeita. | [RF-39](../requisitos/rf-gerais.md#rf-39), [RNF-S02](../requisitos/rnf.md#rnf-s02) |

**RFs cobertos:** [RF-39](../requisitos/rf-gerais.md#rf-39) → [passos 1 a 4](#uc21-p1), [A3.1](#uc21-a3-1), [E2.1](#uc21-e2-1)

**Histórias derivadas:** [US-18 Carregar os dados de exemplo](../historias/US-18-carregar-os-dados-de-exemplo.md)

## <a id="uc-22"></a>UC-22 · Verificar se o sistema está no ar

| Campo | Conteúdo |
|---|---|
| **Ator primário** | Equipe de TI (qualquer visitante pode fazer a mesma verificação) |
| **Meta** | Saber se o sistema, o banco de dados e o cache respondem, antes de usar ou demonstrar. |
| **Precondição** | Nenhuma (não exige identificação). |
| **Ficha completa relacionada** | — |

**Fluxo principal**

1. <a id="uc22-p1"></a>A Equipe de TI pede a verificação do sistema.
2. <a id="uc22-p2"></a>O sistema confere, nesta ordem, se o banco de dados e o cache respondem.
3. <a id="uc22-p3"></a>O sistema informa "API no ar."

**Exceções**

| Exceção | Condição | Resultado para o ator | Estado depois | Requisito |
|---|---|---|---|---|
| <a id="uc22-e2-1"></a>E2.1 · Banco de dados fora do ar | O banco de dados não responde. | "Não foi possível conectar ao banco de dados." | Nada muda. | [RF-40](../requisitos/rf-gerais.md#rf-40) (sem teste: [lacuna L-08](../requisitos/srs.md#l-08)) |
| <a id="uc22-e2-2"></a>E2.2 · Cache fora do ar | O banco responde, mas o cache não. | "Não foi possível conectar ao cache." Enquanto ele estiver fora do ar, entrar e cadastrar-se são recusados ([RNF-F12](../requisitos/rnf.md#rnf-f12)). | Nada muda. | [RF-40](../requisitos/rf-gerais.md#rf-40) |

**RFs cobertos:** [RF-40](../requisitos/rf-gerais.md#rf-40) → [passos 1 a 3](#uc22-p1), [E2.1](#uc22-e2-1), [E2.2](#uc22-e2-2)

**Histórias derivadas:** [US-19 Verificar se o sistema está no ar](../historias/US-19-verificar-se-o-sistema-esta-no-ar.md)
