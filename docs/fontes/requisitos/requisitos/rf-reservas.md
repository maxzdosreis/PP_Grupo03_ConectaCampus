# Requisitos funcionais — Reservas

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **Parte da [SRS-01](srs.md) • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/requisitos/rf-reservas.md` |

Fichas dos RF de [reservas](../glossario.md#reserva): pedido, consulta, mudança de [situação](../glossario.md#situacao) e [histórico](../glossario.md#historico), derivados das NS-03, NS-04, NS-07 a NS-10, NS-12 e NS-14 da [Visão](../visao.md#necessidades). As regras de agenda e a agenda do dia estão em [`rf-agenda.md`](rf-agenda.md). Como ler as fichas: [SRS, seção 3](srs.md#3-requisitos-funcionais).

Caminhos de teste a partir de `src/backend/`, salvo os do frontend (`src/frontend/src/`); `[x]` = teste parametrizado.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Criação: RF-11 a RF-27 (REQ-02). Sem aprovação. |

## Pedido de reserva

### <a id="rf-11"></a>RF-11 · Solicitar reserva

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao usuário autenticado solicitar, em nome próprio, a reserva de um espaço para uma data, uma hora de início, uma hora de término e uma finalidade e ver a reserva criada na situação Solicitada, com o próprio nome e matrícula como solicitante. |
| **Origem** | NS-03 |
| **Funcionalidade** | F2 |
| **Prioridade (QFD)** | Normal — "cadastrar solicitação com solicitante, item, data e situação inicial" é a segunda funcionalidade do enunciado. |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | `POST /api/reservas/` → 201; tela `/reservas/nova` (resumo com a situação). `reservas/tests/test_api_reservas.py::test_solicitacao_valida_responde_201_com_a_reserva`, `::test_solicitante_enviado_no_corpo_e_ignorado`; `reservas/tests/test_api_permissoes.py::test_gestor_tambem_solicita_reserva`; `reservas/tests/test_criar_reserva.py::test_solicitacao_valida_e_salva_como_solicitada`; `pages/PaginaNovaReserva.test.tsx` |
| **Regras de negócio** | [Reserva](../glossario.md#reserva), [solicitante da reserva](../glossario.md#solicitante-da-reserva), [finalidade](../glossario.md#finalidade), [Solicitada](../glossario.md#solicitada). Ordem das verificações: dados ([RF-11.1](#rf-11-1)) → data retroativa ([RF-11.2](#rf-11-2)) → regras de agenda ([RF-11.5](#rf-11-5)) → espaço ([RF-11.3](#rf-11-3)) → conflito ([RF-11.4](#rf-11-4)). |
| **Decisões** | [DEC-04](../decisoes/DEC-04.md) (o solicitante é sempre quem está conectado; o Gestor também pede em nome próprio) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-11-1"></a>RF-11.1 · Recusar pedido com dados inválidos

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o usuário autenticado solicite uma reserva sem espaço, data, hora de início, hora de término ou finalidade, com finalidade de mais de 200 caracteres ou com o término igual ou anterior ao início, sem gravar nada, e informar a regra violada no campo correspondente. |
| **Pai** | [RF-11](#rf-11) |
| **Origem** | NS-03 (principal); NS-13 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Normal — "campos obrigatórios vazios" é uma das operações inválidas do enunciado. |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | 400 com `campos`. `reservas/tests/test_api_reservas.py::test_campos_ausentes_respondem_400_com_cada_campo`, `::test_dado_invalido_responde_400_sem_salvar [data-inexistente, fim-antes-do-inicio, sem-finalidade]`; `reservas/tests/test_reserva.py::test_finalidade_vazia_e_recusada [x]`, `::test_finalidade_acima_do_limite_e_recusada`; `reservas/tests/test_intervalo_de_horario.py::test_fim_igual_ou_antes_do_inicio_e_recusado [x]` |
| **Regras de negócio** | [Finalidade](../glossario.md#finalidade), [intervalo de horário](../glossario.md#intervalo-de-horario) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-11-2"></a>RF-11.2 · Recusar pedido com data retroativa

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o usuário autenticado solicite uma reserva cujo início seja igual ou anterior ao momento do pedido, sem gravar nada, e informar no campo data que não é possível reservar um horário que já passou. |
| **Pai** | [RF-11](#rf-11) |
| **Origem** | NS-06 (principal); NS-03 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — o cliente não pede, mas um pedido para o passado não teria uso. |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | 400 `DATA_RETROATIVA` em `campos.data`. `reservas/tests/test_reserva.py::test_solicitar_com_inicio_igual_a_agora_e_recusado`, `::test_solicitar_um_minuto_depois_de_agora_e_aceito`, `::test_solicitar_para_ontem_e_recusado`; `reservas/tests/test_api_reservas.py::test_dado_invalido_responde_400_sem_salvar [data-retroativa]` |
| **Regras de negócio** | [Data retroativa](../glossario.md#data-retroativa), [fuso horário](../glossario.md#fuso-horario) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-11-3"></a>RF-11.3 · Recusar pedido para espaço que não é reservável

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o usuário autenticado solicite uma reserva num espaço que não existe ou que está inativo, sem gravar nada, e informar qual dos dois casos impediu o pedido. |
| **Pai** | [RF-11](#rf-11) |
| **Origem** | NS-03 (principal); NS-02 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Normal — "item inexistente" é uma das operações inválidas do enunciado; o inativo vem da desativação ([RF-07](rf-espacos.md#rf-07)). |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | 404 `ESPACO_NAO_ENCONTRADO` ou 409 `ESPACO_INATIVO`. `reservas/tests/test_api_reservas.py::test_espaco_inexistente_responde_404`; `espacos/tests/test_api_desativacao_e_reservas.py::test_espaco_desativado_recusa_nova_reserva_com_409`; `reservas/tests/test_criar_reserva.py::test_espaco_indisponivel_propaga_o_erro_sem_salvar [x]` |
| **Regras de negócio** | [Espaço reservável](../glossario.md#espaco-reservavel), [espaço inativo](../glossario.md#espaco-inativo) |
| **Decisões** | [DEC-06](../decisoes/DEC-06.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-11-4"></a>RF-11.4 · Recusar pedido em conflito de horário

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o usuário autenticado solicite uma reserva que tenha algum momento em comum com uma reserva Solicitada ou Confirmada do mesmo espaço, sem gravar nada, e informar a data, o horário e a situação da reserva que ocupa o período, sem dizer quem a pediu. |
| **Pai** | [RF-11](#rf-11) |
| **Origem** | NS-04 (principal); NS-14 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Normal — impedir que um espaço seja comprometido duas vezes é a declaração da solução na Visão. |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | 409 `CONFLITO_DE_HORARIO`, sem `campos`. `reservas/tests/test_api_reservas.py::test_horario_ocupado_responde_409_e_preserva_as_reservas`; `reservas/tests/test_conflito_de_horario.py::test_sobreposicao_com_reserva_que_ocupa_horario_e_conflito [x]`, `::test_horario_encostado_e_aceito [x]`, `::test_mesmo_horario_em_outro_espaco_e_aceito`, `::test_mensagem_mostra_horario_e_situacao_sem_dados_do_outro_solicitante`; `exemplos/tests/test_carregar_dados_exemplo.py::test_horario_de_conflito_documentado_responde_409` |
| **Regras de negócio** | [Conflito de horário](../glossario.md#conflito-de-horario), [reserva que ocupa horário](../glossario.md#reserva-que-ocupa-horario), [intervalo de horário](../glossario.md#intervalo-de-horario) (semiaberto: encostar não é conflito) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-11-5"></a>RF-11.5 · Recusar pedido fora das regras de agenda

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o usuário autenticado solicite uma reserva que comece antes das 07:00 ou termine depois das 22:00, que dure menos de 30 minutos ou mais de 3 horas, ou cuja data passe da data limite (hoje mais 30 dias), sem gravar nada, e informar no campo correspondente a primeira regra violada, nesta ordem: funcionamento, duração, antecedência. |
| **Pai** | [RF-11](#rf-11) |
| **Origem** | NS-06 |
| **Funcionalidade** | F5 (regra do extra de agenda, [DEC-07](../decisoes/DEC-07.md)) |
| **Prioridade (QFD)** | Esperado — o cliente define as regras de uso e espera que pedidos fora delas não cheguem ao Gestor. |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | 400 `FORA_DO_HORARIO_DE_FUNCIONAMENTO`, `DURACAO_INVALIDA` ou `ANTECEDENCIA_EXCEDIDA`. `reservas/tests/test_api_reservas.py::test_dado_invalido_responde_400_sem_salvar [antes-da-abertura, duracao-acima-da-maxima, alem-da-antecedencia]`; `reservas/tests/test_regras_de_agenda.py::test_horario_nas_bordas_do_funcionamento_e_aceito [x]`, `::test_horario_fora_do_funcionamento_e_recusado_no_campo_certo [x]`, `::test_duracao_fora_dos_limites_e_recusada_no_termino [x]`, `::test_data_alem_da_antecedencia_e_recusada_com_a_data_limite`; `reservas/tests/test_reserva.py::test_horario_de_funcionamento_e_checado_antes_da_duracao`, `::test_duracao_e_checada_antes_da_antecedencia`; `reservas/tests/test_propriedades_da_agenda.py::test_solicitar_aceita_so_o_que_respeita_as_regras_e_recusa_pela_primeira_violada` |
| **Regras de negócio** | [Regras de agenda](../glossario.md#regras-de-agenda), [horário de funcionamento](../glossario.md#horario-de-funcionamento), [duração mínima](../glossario.md#duracao-minima), [duração máxima](../glossario.md#duracao-maxima), [antecedência máxima](../glossario.md#antecedencia-maxima), [data limite](../glossario.md#data-limite) |
| **Decisões** | [DEC-07](../decisoes/DEC-07.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

## Consulta de reservas

### <a id="rf-12"></a>RF-12 · Consultar reservas por critérios combináveis

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao Gestor consultar as reservas por espaço, situação, data, solicitante (trecho do nome ou da matrícula) e "somente as minhas", sozinhos ou combinados, e ver só as reservas que atendem a todos os critérios informados, ordenadas pelo início, com a quantidade encontrada. |
| **Origem** | NS-08 |
| **Funcionalidade** | F3 |
| **Prioridade (QFD)** | Normal — "consultar por pelo menos dois critérios" é a terceira funcionalidade do enunciado. |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | `GET /api/reservas/?espaco=&situacao=&data=&solicitante=&minhas=`; tela `/reservas` (filtros no endereço). `reservas/tests/test_api_consulta_reservas.py::test_consulta_sem_filtros_devolve_todas_ordenadas_por_inicio`, `::test_cada_criterio_sozinho_devolve_so_as_correspondentes [x]`, `::test_criterios_combinados_se_somam [x]`, `::test_mensagem_informa_a_quantidade_encontrada [x]`, `::test_consulta_nao_altera_as_reservas`; `reservas/tests/test_api_permissoes.py::test_gestor_lista_todas_e_filtra_por_solicitante`; `pages/PaginaReservas.test.tsx` |
| **Regras de negócio** | [Reserva](../glossario.md#reserva), [situação da reserva](../glossario.md#situacao), [solicitante da reserva](../glossario.md#solicitante-da-reserva). Um espaço inexistente no critério dá lista vazia, não erro. |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-12-1"></a>RF-12.1 · Recusar critério de consulta em formato inválido

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o usuário autenticado consulte reservas com uma situação fora da lista, uma data que não existe ou um espaço que não seja um número, e informar o critério com problema. |
| **Pai** | [RF-12](#rf-12) |
| **Origem** | NS-08 (principal); NS-13 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — um critério ignorado em silêncio mostraria reservas que a pessoa não pediu. |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | 400 `DADOS_INVALIDOS` com `campos`. `reservas/tests/test_api_consulta_reservas.py::test_filtro_invalido_responde_400_com_o_campo [x]`, `::test_filtro_em_branco_e_ignorado [x]` |
| **Regras de negócio** | [Situação da reserva](../glossario.md#situacao) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-13"></a>RF-13 · Consultar as próprias reservas

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao Solicitante consultar as próprias reservas por espaço, situação e data, sozinhos ou combinados, e ver só as reservas que ele pediu e que atendem aos critérios, com a situação e o motivo de cada uma. |
| **Origem** | NS-07 (principal); NS-14 |
| **Funcionalidade** | F3 |
| **Prioridade (QFD)** | Normal — acompanhar o próprio pedido é o motivo de o Solicitante usar o sistema (Visão, seção 2). |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | `GET /api/reservas/` como Solicitante; tela "Minhas reservas" (`/reservas`). `reservas/tests/test_api_permissoes.py::test_solicitante_so_lista_as_proprias [x]`, `::test_solicitante_sem_filtros_ve_a_propria`; `reservas/tests/test_consultar_reservas.py::test_solicitante_so_ve_as_proprias_mesmo_filtrando_por_outro [x]`; `components/layout/Layout.test.tsx` ("logado como solicitante, o item das reservas se chama Minhas reservas") |
| **Regras de negócio** | [Solicitante](../glossario.md#solicitante), [motivo](../glossario.md#motivo) |
| **Decisões** | [DEC-04](../decisoes/DEC-04.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-14"></a>RF-14 · Consultar o detalhe de uma reserva

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao usuário autenticado consultar uma reserva que ele pode ver e ver o espaço, a data e o horário, o solicitante com a matrícula, o momento do pedido, a finalidade, a situação com o motivo e as ações disponíveis para ele. |
| **Origem** | NS-07 (principal); NS-08 |
| **Funcionalidade** | F3 |
| **Prioridade (QFD)** | Normal — é onde o Solicitante lê o motivo de uma recusa ou de um cancelamento. |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | `GET /api/reservas/{id}/`; tela `/reservas/:reservaId`. `reservas/tests/test_api_consulta_reservas.py::test_detalhe_devolve_a_reserva_no_mesmo_formato_da_criacao`; `reservas/tests/test_api_permissoes.py::test_gestor_ve_o_detalhe_de_qualquer_reserva`; `pages/PaginaReserva.test.tsx` |
| **Regras de negócio** | [Reserva](../glossario.md#reserva), [ação disponível](../glossario.md#acao-disponivel). "Pode ver": o Gestor vê todas; o Solicitante, só as próprias. |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-15"></a>RF-15 · Consultar as situações de reserva

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao visitante consultar as situações de reserva e ver o nome de cada uma, na ordem do ciclo de vida (Solicitada, Confirmada, Recusada, Cancelada, Concluída). |
| **Origem** | NS-08 (principal); NS-07 |
| **Funcionalidade** | F3 |
| **Prioridade (QFD)** | Esperado — o critério situação da consulta se escolhe numa lista com os nomes do negócio. |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | `GET /api/reservas/situacoes/` (sem login); seletor de situação em `/reservas`. `reservas/tests/test_api_consulta_reservas.py::test_situacoes_de_reserva_listam_todas_na_ordem_do_enum_sem_login` |
| **Regras de negócio** | [Situação da reserva](../glossario.md#situacao), [vocabulário público](../glossario.md#vocabulario-publico) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

## Mudança de situação

### <a id="rf-16"></a>RF-16 · Ver as ações disponíveis em cada reserva

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao usuário autenticado ver, em cada reserva que ele pode ver, as mudanças de situação que o perfil dele pode executar a partir da situação atual, com a indicação das que exigem motivo, e nenhuma numa situação final. |
| **Origem** | NS-09 (principal); NS-10, NS-11 |
| **Funcionalidade** | F4 |
| **Prioridade (QFD)** | Esperado — sem a lista, a pessoa só descobriria que uma ação é proibida depois de tentar. |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | Campo `acoes_disponiveis` de toda reserva; botões na lista e no detalhe. `reservas/tests/test_api_situacao_reserva.py::test_reserva_solicitada_traz_confirmar_recusar_e_cancelar`, `::test_reserva_confirmada_traz_cancelar_e_concluir`, `::test_reserva_concluida_nao_traz_acoes`; `reservas/tests/test_api_permissoes.py::test_acoes_do_solicitante_na_propria_solicitada_sao_so_cancelar`; `reservas/tests/test_propriedades_da_reserva.py::TestMaquinaDaReserva` (as ações são exatamente as mudanças aceitas); `components/reservas/TabelaDeReservas.test.tsx` |
| **Regras de negócio** | [Ação disponível](../glossario.md#acao-disponivel), [transição de situação](../glossario.md#transicao-de-situacao), [situação final](../glossario.md#situacao-final) |
| **Decisões** | [DEC-13](../decisoes/DEC-13.md) (as ações não dependem do horário) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-17"></a>RF-17 · Confirmar reserva

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao Gestor confirmar uma reserva Solicitada, com motivo opcional, e ver a reserva na situação Confirmada, ainda ocupando o horário. |
| **Origem** | NS-09 |
| **Funcionalidade** | F4 |
| **Prioridade (QFD)** | Normal — aprovar o pedido é a decisão central do Gestor. |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | `PATCH /api/reservas/{id}/situacao/` com `CONFIRMADA`; diálogo "Confirmar reserva". `reservas/tests/test_api_situacao_reserva.py::test_confirmar_responde_200_com_a_reserva_atualizada`; `reservas/tests/test_api_permissoes.py::test_gestor_confirma`; `reservas/tests/test_reserva.py::test_motivo_opcional_ao_confirmar_e_guardado_normalizado` |
| **Regras de negócio** | [Confirmada](../glossario.md#confirmada), [transição de situação](../glossario.md#transicao-de-situacao) |
| **Decisões** | [DEC-13](../decisoes/DEC-13.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-18"></a>RF-18 · Recusar reserva com motivo

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao Gestor recusar uma reserva Solicitada informando um motivo de até 300 caracteres e ver a reserva na situação Recusada, com o motivo, sem ocupar mais o horário. |
| **Origem** | NS-09 |
| **Funcionalidade** | F4 |
| **Prioridade (QFD)** | Normal — negar com justificativa faz parte da decisão do Gestor (NS-09). |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | `PATCH /api/reservas/{id}/situacao/` com `RECUSADA` e `motivo`; diálogo "Recusar reserva". `reservas/tests/test_api_situacao_reserva.py::test_mensagem_de_sucesso_usa_o_rotulo_da_nova_situacao [recusada]`; `reservas/tests/test_alterar_situacao.py::test_transicao_permitida_e_persistida [x]`; `reservas/tests/test_conflito_de_horario.py::test_sobreposicao_com_reserva_que_nao_ocupa_horario_e_aceita [x]` |
| **Regras de negócio** | [Recusada](../glossario.md#recusada), [motivo](../glossario.md#motivo), [reserva que ocupa horário](../glossario.md#reserva-que-ocupa-horario) |
| **Decisões** | [DEC-13](../decisoes/DEC-13.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-19"></a>RF-19 · Concluir reserva

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao Gestor concluir uma reserva Confirmada, com motivo opcional, e ver a reserva na situação Concluída, sem nenhuma ação disponível depois disso. |
| **Origem** | NS-09 |
| **Funcionalidade** | F4 |
| **Prioridade (QFD)** | Normal — com Solicitada → Confirmada → Concluída a reserva atende aos "pelo menos três estados" do enunciado. |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | `PATCH /api/reservas/{id}/situacao/` com `CONCLUIDA`. `reservas/tests/test_api_situacao_reserva.py::test_fluxo_da_demonstracao_ate_concluida` (conclui uma reserva de amanhã: hoje não há verificação de horário), `::test_reserva_concluida_nao_traz_acoes` |
| **Regras de negócio** | [Concluída](../glossario.md#concluida), [situação final](../glossario.md#situacao-final) |
| **Decisões** | [DEC-13](../decisoes/DEC-13.md): a NS-09 fala em "registrar que o uso aconteceu", mas o sistema aceita concluir antes do término (lacuna [L-01](srs.md#lacunas)). |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-20"></a>RF-20 · Cancelar reserva (Gestor)

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao Gestor cancelar uma reserva Solicitada ou Confirmada informando um motivo de até 300 caracteres e ver a reserva na situação Cancelada, com o motivo, sem ocupar mais o horário. |
| **Origem** | NS-09 |
| **Funcionalidade** | F4 |
| **Prioridade (QFD)** | Normal — "registrar que o uso aprovado foi desfeito" está na NS-09. |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | `PATCH /api/reservas/{id}/situacao/` com `CANCELADA` e `motivo`. `reservas/tests/test_api_situacao_reserva.py::test_mensagem_de_sucesso_usa_o_rotulo_da_nova_situacao [cancelada]`, `::test_cancelar_libera_o_horario_para_nova_reserva`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]` (gestor, `CANCELADA` com motivo) |
| **Regras de negócio** | [Cancelada](../glossario.md#cancelada), [motivo](../glossario.md#motivo) |
| **Decisões** | [DEC-06](../decisoes/DEC-06.md) (é assim que o Gestor desfaz as reservas de um espaço desativado), [DEC-13](../decisoes/DEC-13.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-21"></a>RF-21 · Cancelar a própria reserva (Solicitante)

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao Solicitante cancelar uma reserva própria Solicitada ou Confirmada informando um motivo de até 300 caracteres e ver a reserva na situação Cancelada, com o motivo, sem ocupar mais o horário. |
| **Origem** | NS-10 |
| **Funcionalidade** | F4 |
| **Prioridade (QFD)** | Esperado — quem desiste precisa liberar o horário sem procurar o Gestor. |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | `PATCH /api/reservas/{id}/situacao/` com `CANCELADA` e `motivo`, como Solicitante. `reservas/tests/test_api_permissoes.py::test_solicitante_cancela_a_propria`; `reservas/tests/test_alterar_situacao.py::test_solicitante_cancela_a_propria_reserva`; `reservas/tests/test_api_historico.py::test_cancelamento_aparece_com_o_motivo` |
| **Regras de negócio** | [Cancelada](../glossario.md#cancelada), [Solicitante](../glossario.md#solicitante) |
| **Decisões** | [DEC-13](../decisoes/DEC-13.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-22"></a>RF-22 · Consultar o histórico da reserva

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao usuário autenticado consultar o histórico de uma reserva que ele pode ver e ver, em ordem cronológica, a criação e cada mudança de situação aceita, com data e hora, nome do autor, situação anterior e nova e motivo. |
| **Origem** | NS-12 (principal); NS-11 |
| **Funcionalidade** | Extra (RES-07) |
| **Prioridade (QFD)** | Normal — a declaração da solução na Visão promete registrar cada decisão com autor, momento e motivo. |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | `GET /api/reservas/{id}/historico/`; linha do tempo em `/reservas/:reservaId`. `reservas/tests/test_api_historico.py::test_fluxo_completo_aparece_no_historico_em_ordem`, `::test_registrado_em_sai_em_iso_8601_no_fuso_de_sao_paulo`, `::test_registro_nao_expoe_o_id_do_autor`, `::test_tentativa_recusada_nao_aparece_no_historico`; `pages/PaginaReserva.test.tsx` |
| **Regras de negócio** | [Histórico da reserva](../glossario.md#historico), [registro de situação](../glossario.md#registro-de-situacao) |
| **Decisões** | [DEC-05](../decisoes/DEC-05.md) (tentativas recusadas não entram) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

## Recusas comuns às operações de reserva

### <a id="rf-23"></a>RF-23 · Recusar operação sobre reserva inexistente ou de outra pessoa

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o usuário autenticado consulte, consulte o histórico ou mude a situação de uma reserva que não existe ou, no caso do Solicitante, que é de outra pessoa, sem alterar nada, e informar que a reserva não foi encontrada, com a mesma resposta nos dois casos. |
| **Operações protegidas** | [RF-14](#rf-14), [RF-22](#rf-22), [RF-17](#rf-17) a [RF-21](#rf-21) |
| **Origem** | NS-14 (principal); NS-13 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Normal — "item inexistente" é uma das operações inválidas do enunciado; responder igual à reserva alheia não revela que ela existe. |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | 404 `RESERVA_NAO_ENCONTRADA`. `reservas/tests/test_api_consulta_reservas.py::test_detalhe_inexistente_responde_404`; `reservas/tests/test_api_situacao_reserva.py::test_reserva_inexistente_responde_404`; `reservas/tests/test_api_historico.py::test_historico_de_reserva_inexistente_responde_404`, `::test_solicitante_pedindo_historico_de_outra_pessoa_recebe_404`; `reservas/tests/test_api_permissoes.py::test_detalhe_de_outra_pessoa_para_o_solicitante_responde_404`, `::test_solicitante_cancelando_a_de_outra_pessoa_responde_404_sem_mudar_nada` |
| **Regras de negócio** | [Solicitante](../glossario.md#solicitante), [Gestor](../glossario.md#gestor) |
| **Decisões** | [DEC-04](../decisoes/DEC-04.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-24"></a>RF-24 · Recusar transição de situação não permitida

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o usuário autenticado leve uma reserva a uma situação que a tabela de transições não permite a partir da situação atual, sem alterar a reserva nem o histórico, e informar a situação atual e a pedida. |
| **Operações protegidas** | [RF-17](#rf-17) a [RF-21](#rf-21) |
| **Origem** | NS-09 (principal); NS-13 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Normal — "mudança de situação não permitida" é uma das operações inválidas do enunciado. |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | 409 `TRANSICAO_DE_SITUACAO_INVALIDA`. `reservas/tests/test_api_situacao_reserva.py::test_transicao_proibida_responde_409_e_preserva_a_reserva`, `::test_reserva_concluida_nao_pode_ser_cancelada`; `reservas/tests/test_reserva.py::test_transicao_proibida_e_recusada_e_preserva_a_situacao [x]`, `::test_transicao_proibida_tem_mensagem_com_os_rotulos`; `reservas/tests/test_situacao.py::test_transicao_permitida_segue_a_tabela [x]` |
| **Regras de negócio** | [Transição de situação](../glossario.md#transicao-de-situacao), [situação final](../glossario.md#situacao-final) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-25"></a>RF-25 · Recusar situação ausente ou desconhecida

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o usuário autenticado peça a mudança de situação de uma reserva sem informar a situação nova ou com uma situação fora da lista, sem alterar a reserva, e informar no campo situação que ela é obrigatória ou, para um valor desconhecido, quais situações são aceitas. |
| **Operações protegidas** | [RF-17](#rf-17) a [RF-21](#rf-21) |
| **Origem** | NS-09 (principal); NS-13 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Normal — "campos obrigatórios vazios" é uma das operações inválidas do enunciado. |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | 400 `DADOS_INVALIDOS` (ausente ou vazia) ou `SITUACAO_INVALIDA` (desconhecida), com `campos.situacao`. `reservas/tests/test_api_situacao_reserva.py::test_situacao_ausente_ou_invalida_responde_400 [x]` |
| **Regras de negócio** | [Situação da reserva](../glossario.md#situacao) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-26"></a>RF-26 · Recusar recusa ou cancelamento sem motivo válido

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o usuário autenticado recuse ou cancele uma reserva sem motivo, com motivo só de espaços ou com motivo de mais de 300 caracteres, sem alterar a reserva nem o histórico, e informar a regra violada no campo motivo. |
| **Operações protegidas** | [RF-18](#rf-18), [RF-20](#rf-20), [RF-21](#rf-21) |
| **Origem** | NS-09 (principal); NS-07, NS-10 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — sem motivo, o Solicitante não saberia por que o pedido foi negado ou desfeito (NS-07). |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | 400 `MOTIVO_OBRIGATORIO` ou `TEXTO_MUITO_LONGO` em `campos.motivo`. `reservas/tests/test_api_situacao_reserva.py::test_recusar_sem_motivo_responde_400_no_campo_motivo`; `reservas/tests/test_reserva.py::test_recusar_ou_cancelar_sem_motivo_e_recusado_e_nada_muda [x]`, `::test_motivo_acima_do_limite_e_recusado_e_nada_muda`; `reservas/tests/test_alterar_situacao.py::test_recusar_ou_cancelar_sem_motivo_lanca_erro_e_preserva_a_reserva [x]` |
| **Regras de negócio** | [Motivo](../glossario.md#motivo) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-27"></a>RF-27 · Recusar mudança de situação que o perfil não pode fazer

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o Solicitante confirme, recuse ou conclua uma reserva própria, sem alterar a reserva nem o histórico, e informar que só o Gestor pode fazer essa ação, sem revelar se a transição seria permitida. |
| **Operações protegidas** | [RF-17](#rf-17), [RF-18](#rf-18), [RF-19](#rf-19) |
| **Origem** | NS-11 (principal); NS-09 |
| **Funcionalidade** | F5 (regra do extra de perfis, [DEC-04](../decisoes/DEC-04.md)) |
| **Prioridade (QFD)** | Esperado — o cliente espera que só quem tem autoridade decida sobre os pedidos (NS-11). |
| **Vínculos** | UC, US e CA a definir (REQ-03, REQ-04, REQ-05) |
| **Evidência (complementar)** | 403 `ACAO_NAO_PERMITIDA` ("Somente o gestor pode confirmar reservas."). `reservas/tests/test_api_permissoes.py::test_solicitante_confirmando_a_propria_responde_403_sem_mudar_nada`; `reservas/tests/test_permissoes_reserva.py::test_alterar_situacao_segue_a_matriz_e_preserva_a_reserva_nos_erros [x]`, `::test_solicitante_concluindo_uma_solicitada_recebe_403_e_nao_409`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]` (`reservas:situacao`) |
| **Regras de negócio** | [Transição de situação](../glossario.md#transicao-de-situacao) (`DESTINOS_POR_PAPEL`), [perfil](../glossario.md#perfil) |
| **Decisões** | [DEC-04](../decisoes/DEC-04.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |
