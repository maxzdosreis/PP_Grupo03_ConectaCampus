# US-09 · Ver a agenda do dia antes de pedir

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-09 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-09-ver-a-agenda-do-dia.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Marca "Depende de" das DECs confirmadas na Aula 7 (DEC-06, DEC-10, DEC-11) com "(decidida)" (GES-02). Nenhum Dado/Quando/Então muda. Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-19 e TA-20 passam a TA-20 e TA-21, e TA-21 a TA-158 passam a TA-24 a TA-161, para os TA-19, TA-22 e TA-23 novos da US-03 (revogação e troca da credencial de renovação) seguirem a ordem das histórias (AUT-09). Mudança editorial, sem nova obrigação. Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-09 |
| **Título** | Ver a agenda do dia antes de pedir |
| **História** | Como Solicitante, quero ver o que já está ocupado e o que está livre num espaço e num dia antes de pedir para escolher um horário que será aceito, sem tentar às cegas. |
| **Valor** | Menos pedidos recusados por conflito ou fora das regras; a pessoa escolhe e preenche o horário de uma vez ([NS-05](../visao.md#necessidades)). |
| **Origem** | [UC-06 Consultar agenda do dia, passos 1 a 5](../casos-de-uso/fichas-resumidas.md#uc06-p1), alternativas [A1.1](../casos-de-uso/fichas-resumidas.md#uc06-a1-1), [A4.1](../casos-de-uso/fichas-resumidas.md#uc06-a4-1) e [A4.2](../casos-de-uso/fichas-resumidas.md#uc06-a4-2) e exceções [E2.1](../casos-de-uso/fichas-resumidas.md#uc06-e2-1) a [E3.1](../casos-de-uso/fichas-resumidas.md#uc06-e3-1); é a extensão [A3.1 de UC-04](../casos-de-uso/UC-04-solicitar-reserva.md#a3-1). |
| **Prioridade** | Esperado — a classe QFD mais alta entre os RF da história é a de [RF-29.1](../requisitos/rf-agenda.md#rf-29-1), [RF-29.2](../requisitos/rf-agenda.md#rf-29-2) e [RF-31](../requisitos/rf-agenda.md#rf-31) (esperados); o núcleo ([RF-28](../requisitos/rf-agenda.md#rf-28), [RF-29](../requisitos/rf-agenda.md#rf-29), [RF-30](../requisitos/rf-agenda.md#rf-30)) é fascinante e extra ao enunciado. Pela regra de herança (decisão d), as recusas puxam a prioridade para cima; na prática, é a última história a entrar e a primeira a sair se o prazo apertar ([SRS, seção 7](../requisitos/srs.md#7-análise-qfd)). |
| **Estimativa (Custo em Semanas)** | 0,5 (retrospectiva: a FE-07 inteira, com o cálculo dos horários livres no domínio e a propriedade que o liga ao pedido). |
| **Conversa** | "Pode um Solicitante ver que outra pessoa ocupou um horário?" → sim, só o intervalo e a situação, nunca quem nem para quê ([DEC-11](../decisoes/DEC-11.md), adotada provisoriamente). "A agenda impede o pedido?" → não, é ajuda: o pedido continua conferido por inteiro ([US-08](US-08-solicitar-reserva.md)). "Quanto tempo pode demorar?" → a meta de desempenho da agenda ([DEC-12](../decisoes/DEC-12.md), [RNF-P02](../requisitos/rnf.md#rnf-p02)). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | É uma extensão do pedido: depende de [US-08](US-08-solicitar-reserva.md) (onde é usada e cujas regras repete) e de espaços ([US-05](US-05-cadastrar-espaco.md)). |
| **N** · Negociável | ✓ | Mostrar ou não os ocupados de outras pessoas ([DEC-11](../decisoes/DEC-11.md)), a granularidade dos livres e o término sugerido podem mudar sem mudar a meta. |
| **V** · Valiosa | ✓ | Evita a tentativa e erro do conflito; é o requisito fascinante da análise QFD. |
| **E** · Estimável | ✓ | Reaproveita as regras de agenda e de conflito já conhecidas. |
| **S** · Small | ✓ | Uma consulta e uma ação ("usar este horário"). |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado, inclusive uma propriedade que prova que o livre mostrado é exatamente o que o pedido aceitaria. |

**Diagnóstico:** negociável, pequena e testável, mas não é independente: só faz sentido junto do pedido (US-08).

## Critérios de aceite

#### <a id="us-09-ca-01"></a>US-09 · CA-01 · Ocupados e livres do dia (sucesso)

- **Dado** um espaço ativo com uma reserva Confirmada de outra pessoa das 10:00 às 11:00 numa data futura, e uma Cancelada das 14:00 às 15:00 no mesmo dia
- **Quando** o Solicitante, ao pedir, escolhe esse espaço e essa data
- **Então** o sistema mostra o período das 10:00 às 11:00 como ocupado, com a situação Confirmada e sem quem reservou nem para quê, informa "1 horário ocupado neste dia.", mostra o horário de funcionamento e, como livres, das 07:00 às 10:00 e das 11:00 às 22:00 (a Cancelada não ocupa)
- **Origem:** [UC-06 passos 3 e 4](../casos-de-uso/fichas-resumidas.md#uc06-p3), [UC-04 A3.1](../casos-de-uso/UC-04-solicitar-reserva.md#a3-1)
- **RF:** [RF-29](../requisitos/rf-agenda.md#rf-29), [RF-30](../requisitos/rf-agenda.md#rf-30)
- **TA:** [TA-83](#ta-83)
- **Depende de:** [DEC-11](../decisoes/DEC-11.md) (decidida)

#### <a id="us-09-ca-02"></a>US-09 · CA-02 · O livre mostrado é o que o pedido aceita (sucesso)

- **Dado** qualquer combinação de reservas num espaço e num dia
- **Quando** a agenda desse dia é consultada
- **Então** cada horário livre mostrado tem pelo menos 30 minutos, fica dentro do funcionamento e, para hoje, começa no próximo múltiplo de 5 minutos depois de agora; e todo pedido dentro de um horário livre seria aceito, e nenhum fora deles
- **Origem:** [UC-06 passo 4](../casos-de-uso/fichas-resumidas.md#uc06-p4)
- **RF:** [RF-30](../requisitos/rf-agenda.md#rf-30)
- **TA:** [TA-84](#ta-84)

#### <a id="us-09-ca-03"></a>US-09 · CA-03 · Usar um horário livre (sucesso)

- **Dado** a agenda do dia com o livre das 11:00 às 22:00
- **Quando** o Solicitante escolhe usar esse horário
- **Então** o pedido passa a ter início às 11:00 e término às 14:00 (o menor entre o fim do livre e a duração máxima), e ele pode ajustar os dois antes de enviar
- **Origem:** [UC-06 passo 5](../casos-de-uso/fichas-resumidas.md#uc06-p5)
- **RF:** [RF-30](../requisitos/rf-agenda.md#rf-30), [RF-28](../requisitos/rf-agenda.md#rf-28)
- **TA:** [TA-85](#ta-85)

#### <a id="us-09-ca-04"></a>US-09 · CA-04 · Sem espaço ou sem data escolhidos (alternativa)

- **Dado** um pedido em que ainda falta escolher o espaço ou a data
- **Quando** o Solicitante olha a agenda do dia
- **Então** o sistema só orienta a escolher o espaço e a data para ver os horários ocupados, e não consulta nada
- **Origem:** [UC-06 A1.1](../casos-de-uso/fichas-resumidas.md#uc06-a1-1)
- **RF:** [RF-29](../requisitos/rf-agenda.md#rf-29)
- **TA:** [TA-86](#ta-86)

#### <a id="us-09-ca-05"></a>US-09 · CA-05 · Data que não é reservável (alternativa)

- **Dado** a data de ontem, hoje depois das 22:00 ou uma data além da data limite
- **Quando** a agenda dessa data é consultada
- **Então** o sistema informa o motivo com a mensagem da regra correspondente (por exemplo, "Não é possível reservar um horário que já passou."), não mostra nenhum horário livre e continua mostrando os ocupados
- **Origem:** [UC-06 A4.1](../casos-de-uso/fichas-resumidas.md#uc06-a4-1)
- **RF:** [RF-31](../requisitos/rf-agenda.md#rf-31)
- **TA:** [TA-87](#ta-87)
- **Depende de:** [DEC-07](../decisoes/DEC-07.md)

#### <a id="us-09-ca-06"></a>US-09 · CA-06 · Agenda atualizada depois de um conflito (alternativa)

- **Dado** um pedido recusado por conflito de horário ([US-08 · CA-18](US-08-solicitar-reserva.md#us-08-ca-18)), com a agenda do dia aberta
- **Quando** a recusa aparece
- **Então** a agenda é consultada de novo e passa a mostrar o período que ficou ocupado; uma recusa por outro motivo não a consulta de novo
- **Origem:** [UC-06 A4.2](../casos-de-uso/fichas-resumidas.md#uc06-a4-2)
- **RF:** [RF-29](../requisitos/rf-agenda.md#rf-29)
- **TA:** [TA-88](#ta-88)

#### <a id="us-09-ca-07"></a>US-09 · CA-07 · Agenda pedida sem espaço ou sem data (exceção)

- **Dado** um pedido de agenda que chega sem o espaço ou sem a data
- **Quando** o sistema o recebe
- **Então** o sistema aponta o critério que falta e não mostra horário nenhum; nada muda
- **Origem:** [UC-06 E2.1](../casos-de-uso/fichas-resumidas.md#uc06-e2-1)
- **RF:** [RF-29.1](../requisitos/rf-agenda.md#rf-29-1)
- **TA:** [TA-89](#ta-89)

#### <a id="us-09-ca-08"></a>US-09 · CA-08 · Espaço inexistente ou inativo (exceção)

- **Dado** um espaço que não existe, ou que está inativo
- **Quando** a agenda dele é pedida
- **Então** o sistema responde com as mesmas mensagens do pedido de reserva ("Espaço de código «n» não encontrado." ou "Este espaço está inativo e não aceita reservas.") e não mostra horário nenhum
- **Origem:** [UC-06 E2.2](../casos-de-uso/fichas-resumidas.md#uc06-e2-2)
- **RF:** [RF-29.2](../requisitos/rf-agenda.md#rf-29-2)
- **TA:** [TA-90](#ta-90)

#### <a id="us-09-ca-09"></a>US-09 · CA-09 · Agenda não pôde ser obtida (exceção)

- **Dado** uma falha de comunicação ao consultar a agenda
- **Quando** o Solicitante escolhe o espaço e a data
- **Então** o sistema informa "Não foi possível carregar a agenda. Você ainda pode solicitar normalmente.", oferece tentar de novo, e o pedido continua podendo ser enviado e conferido por inteiro
- **Origem:** [UC-06 E3.1](../casos-de-uso/fichas-resumidas.md#uc06-e3-1)
- **RF:** [RF-29](../requisitos/rf-agenda.md#rf-29)
- **TA:** [TA-91](#ta-91)

#### <a id="us-09-ca-10"></a>US-09 · CA-10 · Só quem está identificado vê; nunca dados de quem reservou (acesso)

- **Dado** uma reserva de outra pessoa no espaço e no dia, e, à parte, uma pessoa que não entrou
- **Quando** cada um pede a agenda desse dia
- **Então** o Solicitante vê o período ocupado só com início, término e situação, sem nome, matrícula, finalidade nem motivo de ninguém; quem não entrou não vê nada e é levado a se identificar
- **Origem:** [UC-06 passo 3](../casos-de-uso/fichas-resumidas.md#uc06-p3)
- **RF:** [RF-29](../requisitos/rf-agenda.md#rf-29)
- **TA:** [TA-92](#ta-92)
- **Depende de:** [DEC-11](../decisoes/DEC-11.md) (decidida)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-83"></a>TA-83 | [CA-01](#us-09-ca-01) | automatizado | `reservas/tests/test_api_ocupacao_do_dia.py::test_livres_sao_coerentes_com_os_ocupados`; `reservas/tests/test_api_ocupacao_do_dia.py::test_um_horario_ocupado_usa_a_mensagem_no_singular`; `reservas/tests/test_api_ocupacao_do_dia.py::test_dia_livre_responde_com_o_funcionamento_inteiro`; `reservas/tests/test_consultar_ocupacao_do_dia.py::test_so_solicitadas_e_confirmadas_ocupam_e_o_resto_fica_livre`; `pages/PaginaNovaReserva.test.tsx`: `escolher espaço e data consulta a agenda uma vez e mostra ocupados e livres`; `components/reservas/AgendaDoDia.test.tsx`: `mostra os ocupados com a situação e os livres com o horário recebido` |
| <a id="ta-84"></a>TA-84 | [CA-02](#us-09-ca-02) | automatizado | `reservas/tests/test_propriedades_da_agenda.py::test_agenda_mostra_livre_exatamente_o_que_o_backend_aceitaria`; `reservas/tests/test_consultar_ocupacao_do_dia.py::test_dia_sem_reservas_tem_o_funcionamento_inteiro_livre` |
| <a id="ta-85"></a>TA-85 | [CA-03](#us-09-ca-03) | automatizado | `pages/PaginaNovaReserva.test.tsx`: `"Usar este horário" preenche Início e Término, limitado pela duração máxima, e foca Término`; `components/reservas/agendaDoDia.test.ts`: `limita o término pela duração máxima recebida`; `components/reservas/agendaDoDia.test.ts`: `não passa do fim da janela`; `components/reservas/AgendaDoDia.test.tsx`: `"Usar este horário" entrega a janela escolhida` |
| <a id="ta-86"></a>TA-86 | [CA-04](#us-09-ca-04) | automatizado | `components/reservas/AgendaDoDia.test.tsx`: `sem espaço ou sem data (%o, %o), mostra a instrução e não consulta`; `pages/PaginaNovaReserva.test.tsx`: `sem espaço e data, a agenda só orienta e não consulta` |
| <a id="ta-87"></a>TA-87 | [CA-05](#us-09-ca-05) | automatizado | `reservas/tests/test_api_ocupacao_do_dia.py::test_ontem_nao_e_reservavel_e_traz_a_mensagem_do_dominio`; `reservas/tests/test_consultar_ocupacao_do_dia.py::test_data_indisponivel_nao_tem_livres_e_traz_o_motivo`; `components/reservas/AgendaDoDia.test.tsx`: `data em que não é possível reservar mostra o motivo da API` |
| <a id="ta-88"></a>TA-88 | [CA-06](#us-09-ca-06) | automatizado | `pages/PaginaNovaReserva.test.tsx`: `depois de um 409 de conflito, a agenda é recarregada`; `pages/PaginaNovaReserva.test.tsx`: `outros erros de envio não recarregam a agenda`; `exemplos/tests/test_carregar_dados_exemplo.py::test_horario_de_conflito_documentado_aparece_ocupado_na_agenda_do_dia` |
| <a id="ta-89"></a>TA-89 | [CA-07](#us-09-ca-07) | automatizado | `reservas/tests/test_api_ocupacao_do_dia.py::test_sem_espaco_ou_sem_data_responde_400_com_o_campo [x]` |
| <a id="ta-90"></a>TA-90 | [CA-08](#us-09-ca-08) | automatizado | `reservas/tests/test_api_ocupacao_do_dia.py::test_espaco_inexistente_responde_404`; `reservas/tests/test_api_ocupacao_do_dia.py::test_espaco_inativo_responde_409`; `reservas/tests/test_consultar_ocupacao_do_dia.py::test_espaco_desconhecido_e_recurso_nao_encontrado`; `reservas/tests/test_consultar_ocupacao_do_dia.py::test_espaco_inativo_e_conflito_de_estado` |
| <a id="ta-91"></a>TA-91 | [CA-09](#us-09-ca-09) | automatizado | `components/reservas/AgendaDoDia.test.tsx`: `falha ao carregar mostra um aviso informativo e "Tentar novamente" consulta de novo`; `pages/PaginaNovaReserva.test.tsx`: `com a agenda falhando, o formulário continua enviando` |
| <a id="ta-92"></a>TA-92 | [CA-10](#us-09-ca-10) | automatizado | `reservas/tests/test_api_ocupacao_do_dia.py::test_solicitante_ve_a_reserva_de_outra_pessoa_sem_nenhum_dado_pessoal`; `reservas/tests/test_api_ocupacao_do_dia.py::test_sem_login_responde_401`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]` |
