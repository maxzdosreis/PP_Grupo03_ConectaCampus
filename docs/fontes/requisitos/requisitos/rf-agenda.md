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

## Regras de agenda

### <a id="rf-28"></a>RF-28 · Consultar as regras de agenda

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao visitante consultar as regras de agenda e ver o horário de abertura e de fechamento, a duração mínima e máxima de uma reserva, a antecedência máxima em dias e a data limite para reservar a partir de hoje. |
| **Origem** | NS-06 |
| **Funcionalidade** | Extra (RES-09) |
| **Prioridade (QFD)** | Fascinante — o Visitante conhece as regras de uso antes de criar a conta, e o formulário mostra a dica sem números escritos no navegador. |
| **Vínculos** | UC: [UC-04 Solicitar reserva](../casos-de-uso/README.md#uc-04) (fluxo principal); também em [UC-06 Consultar agenda do dia](../casos-de-uso/README.md#uc-06) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | `GET /api/reservas/regras-de-agenda/` (sem login); dica antes do campo Data em `/reservas/nova`. `reservas/tests/test_api_regras_de_agenda.py::test_regras_de_agenda_sem_login_respondem_200_com_as_constantes_do_dominio`, `::test_regras_de_agenda_tem_os_valores_combinados`; `components/reservas/dicaDaAgenda.test.ts` |
| **Regras de negócio** | [Regras de agenda](../glossario.md#regras-de-agenda), [horário de funcionamento](../glossario.md#horario-de-funcionamento), [duração mínima](../glossario.md#duracao-minima), [duração máxima](../glossario.md#duracao-maxima), [antecedência máxima](../glossario.md#antecedencia-maxima), [data limite](../glossario.md#data-limite), [vocabulário público](../glossario.md#vocabulario-publico) |
| **Decisões** | [DEC-07](../decisoes/DEC-07.md) |
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
| **Vínculos** | UC: [UC-06 Consultar agenda do dia](../casos-de-uso/README.md#uc-06) (fluxo principal) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | `GET /api/reservas/ocupacao/?espaco=&data=`; seção "Agenda do dia" em `/reservas/nova`. `reservas/tests/test_api_ocupacao_do_dia.py::test_solicitante_ve_a_reserva_de_outra_pessoa_sem_nenhum_dado_pessoal`, `::test_um_horario_ocupado_usa_a_mensagem_no_singular`; `reservas/tests/test_consultar_ocupacao_do_dia.py::test_so_solicitadas_e_confirmadas_ocupam_e_o_resto_fica_livre`; `exemplos/tests/test_carregar_dados_exemplo.py::test_horario_de_conflito_documentado_aparece_ocupado_na_agenda_do_dia`; `components/reservas/AgendaDoDia.test.tsx` |
| **Regras de negócio** | [Agenda do dia](../glossario.md#agenda-do-dia), [horário ocupado](../glossario.md#horario-ocupado), [reserva que ocupa horário](../glossario.md#reserva-que-ocupa-horario) |
| **Decisões** | [DEC-11](../decisoes/DEC-11.md) |
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
| **Vínculos** | UC: [UC-06 Consultar agenda do dia](../casos-de-uso/README.md#uc-06) (exceção) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | 400 `DADOS_INVALIDOS` com `campos`. `reservas/tests/test_api_ocupacao_do_dia.py::test_sem_espaco_ou_sem_data_responde_400_com_o_campo [x]` |
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
| **Vínculos** | UC: [UC-06 Consultar agenda do dia](../casos-de-uso/README.md#uc-06) (exceção) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | 404 `ESPACO_NAO_ENCONTRADO` ou 409 `ESPACO_INATIVO`. `reservas/tests/test_api_ocupacao_do_dia.py::test_espaco_inexistente_responde_404`, `::test_espaco_inativo_responde_409`; `reservas/tests/test_consultar_ocupacao_do_dia.py::test_espaco_desconhecido_e_recurso_nao_encontrado`, `::test_espaco_inativo_e_conflito_de_estado` |
| **Regras de negócio** | [Espaço reservável](../glossario.md#espaco-reservavel) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-30"></a>RF-30 · Ver os horários livres de um espaço num dia

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao usuário autenticado ver, na agenda do dia de um espaço, os horários livres dentro do funcionamento, cada um com pelo menos 30 minutos e, para hoje, começando no próximo múltiplo de 5 minutos depois do momento da consulta, e usar um deles para preencher o início e o término do pedido. |
| **Origem** | NS-05 |
| **Funcionalidade** | Extra (FE-07) |
| **Prioridade (QFD)** | Fascinante — a pessoa escolhe um horário que o sistema já sabe que aceitaria. |
| **Vínculos** | UC: [UC-06 Consultar agenda do dia](../casos-de-uso/README.md#uc-06) (fluxo principal) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | Campo `livres` de `GET /api/reservas/ocupacao/`; "Usar este horário" em `/reservas/nova`. `reservas/tests/test_horarios_livres.py::test_livres_sao_o_funcionamento_menos_os_ocupados [x]`, `::test_janela_de_20_minutos_entre_dois_ocupados_nao_aparece`, `::test_hoje_a_primeira_janela_comeca_no_proximo_multiplo_de_5_minutos [x]`; `reservas/tests/test_propriedades_da_agenda.py::test_agenda_mostra_livre_exatamente_o_que_o_backend_aceitaria`; `reservas/tests/test_api_ocupacao_do_dia.py::test_livres_sao_coerentes_com_os_ocupados`; `components/reservas/AgendaDoDia.test.tsx` ("Usar este horário" entrega a janela escolhida); `components/reservas/agendaDoDia.test.ts` |
| **Regras de negócio** | [Horário livre](../glossario.md#horario-livre), [duração mínima](../glossario.md#duracao-minima), [horário de funcionamento](../glossario.md#horario-de-funcionamento). O término sugerido é o menor entre o fim do horário livre e o início mais a duração máxima. |
| **Decisões** | [DEC-07](../decisoes/DEC-07.md) |
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
| **Vínculos** | UC: [UC-06 Consultar agenda do dia](../casos-de-uso/README.md#uc-06) (alternativa) · US e CA a definir (REQ-04, REQ-05) |
| **Evidência (complementar)** | `reservavel: false` e `motivo_indisponivel` na resposta da agenda. `reservas/tests/test_api_ocupacao_do_dia.py::test_ontem_nao_e_reservavel_e_traz_a_mensagem_do_dominio`; `reservas/tests/test_consultar_ocupacao_do_dia.py::test_data_indisponivel_nao_tem_livres_e_traz_o_motivo`; `reservas/tests/test_horarios_livres.py::test_data_alem_da_antecedencia_traz_a_mensagem_com_a_data_limite`, `::test_data_cujo_funcionamento_ja_acabou_traz_o_motivo_de_data_retroativa [x]`; `components/reservas/AgendaDoDia.test.tsx` ("data em que não é possível reservar mostra o motivo da API") |
| **Regras de negócio** | [Data reservável](../glossario.md#data-reservavel), [data limite](../glossario.md#data-limite), [data retroativa](../glossario.md#data-retroativa) |
| **Decisões** | [DEC-07](../decisoes/DEC-07.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |
