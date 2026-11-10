# Requisitos funcionais — Regras de agenda e agenda do dia

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **Parte da [SRS-01](srs.md) • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/requisitos/rf-agenda.md` |

Fichas dos RF que ajudam a escolher o horário antes de pedir: as [regras de agenda](../glossario.md#regras-de-agenda) consultáveis (NS-06) e a [agenda do dia](../glossario.md#agenda-do-dia) de um espaço (NS-05). A recusa de um pedido fora das regras de agenda é o [RF-11.5](rf-reservas.md#rf-11-5), filho do pedido de reserva. A agenda é ajuda: o pedido continua verificado por inteiro ao ser enviado ([RF-11](rf-reservas.md#rf-11)). Como ler as fichas: [SRS, seção 3](srs.md#3-requisitos-funcionais).

Caminhos de teste a partir de `src/backend/`, salvo os do frontend (`src/frontend/src/`); `[x]` = teste parametrizado.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Criação: RF-28 a RF-31 (REQ-02). Sem aprovação. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Vínculos: o UC de cada ficha preenchido, com link para o [índice de casos de uso](../casos-de-uso/README.md#índice-dos-casos-de-uso) (REQ-03). Sem aprovação. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Vínculos: o passo, a alternativa ou a exceção exata de cada RF nas [fichas de caso de uso](../casos-de-uso/README.md#fichas-dos-casos-de-uso); US e CA ficam para a REQ-05 (REQ-04). Sem aprovação. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Vínculos: as US e os CAs de cada RF, com o TA, no lugar de "a definir" ([histórias](../historias/README.md)) (REQ-05). Sem aprovação. |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Campo **Código (complementar)** em cada ficha (caso de uso da aplicação e regra do domínio, como `arquivo::Símbolo`), lido pela [matriz de rastreabilidade](../rastreabilidade/matriz.md) (REQ-06). Evidência do RF-31 passa a citar a rota e a tela da agenda do dia (correção editorial achada pela matriz). Sem aprovação. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Campo Decisões: a DEC-11 marcada como decidida (Aula 7, 06/11/2026; GES-02). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-19 e TA-20 passam a TA-20 e TA-21, e TA-21 a TA-158 passam a TA-24 a TA-161, para os TA-19, TA-22 e TA-23 novos da US-03 (revogação e troca da credencial de renovação) seguirem a ordem das histórias (AUT-09). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Aplicação na especificação do CR-03 (DEC-07), com a implementação pendente na tarefa ESP-07 (REQ-13): RF-28 com o horário de cada espaço e a duração sugerida de 1 hora; RF-30 com o funcionamento do espaço; renumeração dos CAs e TAs dos Vínculos. A especificação está adiante do código de propósito. Sem aprovação. |

## Regras de agenda

### <a id="rf-28"></a>RF-28 · Consultar as regras de agenda

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao visitante consultar as regras de agenda e ver o horário de abertura e de fechamento de cada espaço, a duração sugerida (1 hora), a duração mínima e máxima de uma reserva, a antecedência máxima em dias e a data limite para reservar a partir de hoje. |
| **Origem** | NS-06 |
| **Funcionalidade** | Extra (RES-09) |
| **Prioridade (QFD)** | Fascinante — o Visitante conhece as regras de uso antes de criar a conta, e o formulário mostra a dica sem números escritos no navegador. |
| **Vínculos** | UC: [UC-04 Solicitar reserva](../casos-de-uso/README.md#uc-04) (fluxo principal); também em [UC-06 Consultar agenda do dia](../casos-de-uso/README.md#uc-06) — na ficha: [UC-04 passo 2](../casos-de-uso/UC-04-solicitar-reserva.md#p2), [A2.1](../casos-de-uso/UC-04-solicitar-reserva.md#a2-1), [UC-06 passo 5](../casos-de-uso/fichas-resumidas.md#uc06-p5) · US/CA: [US-08 · CA-02](../historias/US-08-solicitar-reserva.md#us-08-ca-02) (TA-68), [US-08 · CA-06](../historias/US-08-solicitar-reserva.md#us-08-ca-06) (TA-72), [US-08 · CA-08](../historias/US-08-solicitar-reserva.md#us-08-ca-08) (TA-74), [US-09 · CA-03](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-03) (TA-95) |
| **Evidência (complementar)** | `GET /api/reservas/regras-de-agenda/` (sem login); dica antes do campo Data em `/reservas/nova`. `reservas/tests/test_api_regras_de_agenda.py::test_regras_de_agenda_sem_login_respondem_200_com_as_constantes_do_dominio`, `::test_regras_de_agenda_tem_os_valores_combinados`; `components/reservas/dicaDaAgenda.test.ts` **Regra nova ([CR-03](../mudancas/CR-03-horario-por-espaco.md), aplicada na especificação em 10/11/2026):** o horário de cada espaço e a duração sugerida — implementação pendente (tarefa ESP-07); os testes citados acima verificam a regra anterior. |
| **Código (complementar)** | `reservas/domain/regras_de_agenda.py::data_limite_para_reservar`, `reservas/domain/regras_de_agenda.py::HORARIO_DE_ABERTURA`, `reservas/api/serializers.py::RegrasDeAgendaSaidaSerializer.vigentes` |
| **Regras de negócio** | [RN-03](regras-de-negocio.md#rn-03), [RN-04](regras-de-negocio.md#rn-04), [RN-05](regras-de-negocio.md#rn-05). Glossário e detalhes: [Regras de agenda](../glossario.md#regras-de-agenda), [horário de funcionamento](../glossario.md#horario-de-funcionamento), [duração mínima](../glossario.md#duracao-minima), [duração máxima](../glossario.md#duracao-maxima), [antecedência máxima](../glossario.md#antecedencia-maxima), [data limite](../glossario.md#data-limite), [vocabulário público](../glossario.md#vocabulario-publico) |
| **Decisões** | [DEC-07](../decisoes/DEC-07.md) (decidida na Aula 7; [CR-03](../mudancas/CR-03-horario-por-espaco.md), tarefa ESP-07; como a consulta recebe o espaço, a definir na ESP-07) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

## Agenda do dia

### <a id="rf-29"></a>RF-29 · Ver os horários ocupados de um espaço num dia

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao usuário autenticado escolher um espaço e uma data e ver os horários ocupados por reservas Solicitadas ou Confirmadas desse espaço nesse dia, em ordem de início, cada um só com início, término e situação, com a quantidade de horários ocupados. |
| **Origem** | NS-05 (principal); NS-14 |
| **Funcionalidade** | Extra (FE-07) |
| **Prioridade (QFD)** | Fascinante — o Solicitante vê o conflito antes de enviar, em vez de descobrir pela recusa. |
| **Vínculos** | UC: [UC-06 Consultar agenda do dia](../casos-de-uso/README.md#uc-06) (fluxo principal) — na ficha: [UC-06 passo 3](../casos-de-uso/fichas-resumidas.md#uc06-p3), [UC-04 A3.1](../casos-de-uso/UC-04-solicitar-reserva.md#a3-1) · US/CA: [US-09 · CA-01](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-01) (TA-93), [US-09 · CA-04](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-04) (TA-96), [US-09 · CA-06](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-06) (TA-98), [US-09 · CA-09](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-09) (TA-101), [US-09 · CA-10](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-10) (TA-102) |
| **Evidência (complementar)** | `GET /api/reservas/ocupacao/?espaco=&data=`; seção "Agenda do dia" em `/reservas/nova`. `reservas/tests/test_api_ocupacao_do_dia.py::test_solicitante_ve_a_reserva_de_outra_pessoa_sem_nenhum_dado_pessoal`, `::test_um_horario_ocupado_usa_a_mensagem_no_singular`; `reservas/tests/test_consultar_ocupacao_do_dia.py::test_so_solicitadas_e_confirmadas_ocupam_e_o_resto_fica_livre`; `exemplos/tests/test_carregar_dados_exemplo.py::test_horario_de_conflito_documentado_aparece_ocupado_na_agenda_do_dia`; `components/reservas/AgendaDoDia.test.tsx` |
| **Código (complementar)** | `reservas/application/casos_de_uso.py::ConsultarOcupacaoDoDia.executar`, `reservas/application/ocupacao_do_dia.py::OcupacaoDoDia` |
| **Regras de negócio** | [RN-01](regras-de-negocio.md#rn-01), [RN-02](regras-de-negocio.md#rn-02), [RN-16](regras-de-negocio.md#rn-16). Glossário e detalhes: [Agenda do dia](../glossario.md#agenda-do-dia), [horário ocupado](../glossario.md#horario-ocupado), [reserva que ocupa horário](../glossario.md#reserva-que-ocupa-horario) |
| **Decisões** | [DEC-11](../decisoes/DEC-11.md) (decidida) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-29-1"></a>RF-29.1 · Recusar consulta da agenda sem espaço ou sem data

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o usuário autenticado consulte a agenda do dia sem informar o espaço ou sem informar a data e informar o critério que falta. |
| **Pai** | [RF-29](#rf-29) |
| **Origem** | NS-05 (principal); NS-13 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — sem espaço e data a agenda não tem o que mostrar. |
| **Vínculos** | UC: [UC-06 Consultar agenda do dia](../casos-de-uso/README.md#uc-06) (exceção) — na ficha: [UC-06 E2.1](../casos-de-uso/fichas-resumidas.md#uc06-e2-1) · US/CA: [US-09 · CA-07](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-07) (TA-99) |
| **Evidência (complementar)** | 400 `DADOS_INVALIDOS` com `campos`. `reservas/tests/test_api_ocupacao_do_dia.py::test_sem_espaco_ou_sem_data_responde_400_com_o_campo [x]` |
| **Código (complementar)** | `reservas/api/serializers.py::FiltrosDeOcupacaoSerializer` |
| **Regras de negócio** | [Agenda do dia](../glossario.md#agenda-do-dia) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-29-2"></a>RF-29.2 · Recusar agenda de espaço que não é reservável

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o usuário autenticado consulte a agenda do dia de um espaço que não existe ou está inativo e informar qual dos dois casos impediu a consulta, com as mesmas mensagens do pedido de reserva. |
| **Pai** | [RF-29](#rf-29) |
| **Origem** | NS-05 (principal); NS-02 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — mostrar horários livres num espaço inativo induziria um pedido que será recusado. |
| **Vínculos** | UC: [UC-06 Consultar agenda do dia](../casos-de-uso/README.md#uc-06) (exceção) — na ficha: [UC-06 E2.2](../casos-de-uso/fichas-resumidas.md#uc06-e2-2) · US/CA: [US-09 · CA-08](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-08) (TA-100) |
| **Evidência (complementar)** | 404 `ESPACO_NAO_ENCONTRADO` ou 409 `ESPACO_INATIVO`. `reservas/tests/test_api_ocupacao_do_dia.py::test_espaco_inexistente_responde_404`, `::test_espaco_inativo_responde_409`; `reservas/tests/test_consultar_ocupacao_do_dia.py::test_espaco_desconhecido_e_recurso_nao_encontrado`, `::test_espaco_inativo_e_conflito_de_estado` |
| **Código (complementar)** | `reservas/application/casos_de_uso.py::ConsultarOcupacaoDoDia.executar`, `reservas/application/portas.py::ConsultaDeEspacos.obter_espaco_reservavel` |
| **Regras de negócio** | [RN-07](regras-de-negocio.md#rn-07). Glossário e detalhes: [Espaço reservável](../glossario.md#espaco-reservavel) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-30"></a>RF-30 · Ver os horários livres de um espaço num dia

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao usuário autenticado ver, na agenda do dia de um espaço, os horários livres dentro do funcionamento do espaço, cada um com pelo menos 30 minutos e, para hoje, começando no próximo múltiplo de 5 minutos depois do momento da consulta, e usar um deles para preencher o início e o término do pedido. |
| **Origem** | NS-05 |
| **Funcionalidade** | Extra (FE-07) |
| **Prioridade (QFD)** | Fascinante — a pessoa escolhe um horário que o sistema já sabe que aceitaria. |
| **Vínculos** | UC: [UC-06 Consultar agenda do dia](../casos-de-uso/README.md#uc-06) (fluxo principal) — na ficha: [UC-06 passos 4 e 5](../casos-de-uso/fichas-resumidas.md#uc06-p4), [UC-04 A3.1](../casos-de-uso/UC-04-solicitar-reserva.md#a3-1) · US/CA: [US-09 · CA-01](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-01) (TA-93), [US-09 · CA-02](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-02) (TA-94), [US-09 · CA-03](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-03) (TA-95) |
| **Evidência (complementar)** | Campo `livres` de `GET /api/reservas/ocupacao/`; "Usar este horário" em `/reservas/nova`. `reservas/tests/test_horarios_livres.py::test_livres_sao_o_funcionamento_menos_os_ocupados [x]`, `::test_janela_de_20_minutos_entre_dois_ocupados_nao_aparece`, `::test_hoje_a_primeira_janela_comeca_no_proximo_multiplo_de_5_minutos [x]`; `reservas/tests/test_propriedades_da_agenda.py::test_agenda_mostra_livre_exatamente_o_que_o_backend_aceitaria`; `reservas/tests/test_api_ocupacao_do_dia.py::test_livres_sao_coerentes_com_os_ocupados`; `components/reservas/AgendaDoDia.test.tsx` ("Usar este horário" entrega a janela escolhida); `components/reservas/agendaDoDia.test.ts` **Regra nova ([CR-03](../mudancas/CR-03-horario-por-espaco.md), aplicada na especificação em 10/11/2026):** o funcionamento do espaço — implementação pendente (tarefa ESP-07); os testes citados acima verificam a regra anterior. |
| **Código (complementar)** | `reservas/domain/regras_de_agenda.py::horarios_livres`, `reservas/application/casos_de_uso.py::ConsultarOcupacaoDoDia.executar` |
| **Regras de negócio** | [RN-01](regras-de-negocio.md#rn-01), [RN-03](regras-de-negocio.md#rn-03), [RN-04](regras-de-negocio.md#rn-04), [RN-16](regras-de-negocio.md#rn-16). Glossário e detalhes: [Horário livre](../glossario.md#horario-livre), [duração mínima](../glossario.md#duracao-minima), [horário de funcionamento](../glossario.md#horario-de-funcionamento). O término sugerido é o menor entre o fim do horário livre e o início mais a duração máxima. |
| **Decisões** | [DEC-07](../decisoes/DEC-07.md) (decidida na Aula 7; [CR-03](../mudancas/CR-03-horario-por-espaco.md), tarefa ESP-07; onde a duração sugerida vale no preenchimento, a definir na ESP-07) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-31"></a>RF-31 · Saber que uma data não é reservável

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao usuário autenticado consultar a agenda do dia de uma data que não é reservável (o fechamento daquele dia já passou ou a data passa da data limite) e ver o motivo, sem nenhum horário livre, com os horários ocupados mantidos. |
| **Origem** | NS-05 (principal); NS-06 |
| **Funcionalidade** | Extra (FE-07) |
| **Prioridade (QFD)** | Esperado — uma agenda vazia sem explicação seria lida como "tudo livre". |
| **Vínculos** | UC: [UC-06 Consultar agenda do dia](../casos-de-uso/README.md#uc-06) (alternativa) — na ficha: [UC-06 A4.1](../casos-de-uso/fichas-resumidas.md#uc06-a4-1), [UC-04 A3.1](../casos-de-uso/UC-04-solicitar-reserva.md#a3-1) · US/CA: [US-09 · CA-05](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-05) (TA-97) |
| **Evidência (complementar)** | `reservavel: false` e `motivo_indisponivel` na resposta da agenda (`GET /api/reservas/ocupacao/`); aviso na seção "Agenda do dia" em `/reservas/nova`. `reservas/tests/test_api_ocupacao_do_dia.py::test_ontem_nao_e_reservavel_e_traz_a_mensagem_do_dominio`; `reservas/tests/test_consultar_ocupacao_do_dia.py::test_data_indisponivel_nao_tem_livres_e_traz_o_motivo`; `reservas/tests/test_horarios_livres.py::test_data_alem_da_antecedencia_traz_a_mensagem_com_a_data_limite`, `::test_data_cujo_funcionamento_ja_acabou_traz_o_motivo_de_data_retroativa [x]`; `components/reservas/AgendaDoDia.test.tsx` ("data em que não é possível reservar mostra o motivo da API") |
| **Código (complementar)** | `reservas/domain/regras_de_agenda.py::garantir_data_reservavel`, `reservas/domain/regras_de_agenda.py::motivo_de_indisponibilidade` |
| **Regras de negócio** | [RN-03](regras-de-negocio.md#rn-03), [RN-05](regras-de-negocio.md#rn-05). Glossário e detalhes: [Data reservável](../glossario.md#data-reservavel), [data limite](../glossario.md#data-limite), [data retroativa](../glossario.md#data-retroativa) |
| **Decisões** | [DEC-07](../decisoes/DEC-07.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |
