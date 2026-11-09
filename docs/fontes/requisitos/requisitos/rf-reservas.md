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
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Vínculos: o UC de cada ficha preenchido, com link para o [índice de casos de uso](../casos-de-uso/README.md#índice-dos-casos-de-uso) (REQ-03). Sem aprovação. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Vínculos: o passo, a alternativa ou a exceção exata de cada RF nas [fichas de caso de uso](../casos-de-uso/README.md#fichas-dos-casos-de-uso); US e CA ficam para a REQ-05 (REQ-04). Sem aprovação. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Vínculos: as US e os CAs de cada RF, com o TA, no lugar de "a definir" ([histórias](../historias/README.md)) (REQ-05). Sem aprovação. |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Campo **Código (complementar)** em cada ficha (caso de uso da aplicação e regra do domínio, como `arquivo::Símbolo`), lido pela [matriz de rastreabilidade](../rastreabilidade/matriz.md) (REQ-06). Evidência do RF-16 passa a citar as rotas e as telas onde as ações aparecem (correção editorial achada pela matriz). Sem aprovação. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Campo Decisões: a DEC-06 marcada como decidida (Aula 7, 06/11/2026; GES-02). As fichas ligadas às DEC-13 e DEC-05 ficam como estão até a RES-11 e a RES-12 aplicarem os CR-01 e CR-02. Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-19 e TA-20 passam a TA-20 e TA-21, e TA-21 a TA-158 passam a TA-24 a TA-161, para os TA-19, TA-22 e TA-23 novos da US-03 (revogação e troca da credencial de renovação) seguirem a ordem das histórias (AUT-09). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | RF-12.2 novo (consulta em páginas, com o total; fecha a [L-05](srs.md#l-05)); RF-12.1 passa a recusar também uma página ou um tamanho de página inválidos; RF-12 com a ordem e o total na consulta paginada; Vínculos do RF-12, RF-12.1 e RF-13 com os CAs novos e renumerados das US-10 e US-11. Renumeração dos TAs: TA-96 a TA-107 passam a TA-97, TA-98, TA-99, TA-102, TA-103, TA-105, TA-106, TA-107, TA-109, TA-110, TA-113 e TA-114, e TA-108 a TA-161 passam a TA-115 a TA-168, para os TAs novos das US-10 e US-11 seguirem a ordem das histórias (RES-10). Sem aprovação. |

## Pedido de reserva

### <a id="rf-11"></a>RF-11 · Solicitar reserva

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao usuário autenticado solicitar, em nome próprio, a reserva de um espaço para uma data, uma hora de início, uma hora de término e uma finalidade e ver a reserva criada na situação Solicitada, com o próprio nome e matrícula como solicitante. |
| **Origem** | NS-03 |
| **Funcionalidade** | F2 |
| **Prioridade (QFD)** | Normal — "cadastrar solicitação com solicitante, item, data e situação inicial" é a segunda funcionalidade do enunciado. |
| **Vínculos** | UC: [UC-04 Solicitar reserva](../casos-de-uso/README.md#uc-04) (fluxo principal) — na ficha: [UC-04 passos 1 a 11](../casos-de-uso/UC-04-solicitar-reserva.md#p1) · US/CA: [US-08 · CA-01](../historias/US-08-solicitar-reserva.md#us-08-ca-01) (TA-62), [US-08 · CA-02](../historias/US-08-solicitar-reserva.md#us-08-ca-02) (TA-63), [US-08 · CA-03](../historias/US-08-solicitar-reserva.md#us-08-ca-03) (TA-64), [US-08 · CA-05](../historias/US-08-solicitar-reserva.md#us-08-ca-05) (TA-66), [US-08 · CA-21](../historias/US-08-solicitar-reserva.md#us-08-ca-21) (TA-82) |
| **Evidência (complementar)** | `POST /api/reservas/` → 201; tela `/reservas/nova` (resumo com a situação). `reservas/tests/test_api_reservas.py::test_solicitacao_valida_responde_201_com_a_reserva`, `::test_solicitante_enviado_no_corpo_e_ignorado`; `reservas/tests/test_api_permissoes.py::test_gestor_tambem_solicita_reserva`; `reservas/tests/test_criar_reserva.py::test_solicitacao_valida_e_salva_como_solicitada`; `pages/PaginaNovaReserva.test.tsx` |
| **Código (complementar)** | `reservas/application/casos_de_uso.py::CriarReserva.executar`, `reservas/domain/reserva.py::Reserva.solicitar` |
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
| **Vínculos** | UC: [UC-04 Solicitar reserva](../casos-de-uso/README.md#uc-04) (exceção) — na ficha: [UC-04 E5.1](../casos-de-uso/UC-04-solicitar-reserva.md#e5-1), [E5.2](../casos-de-uso/UC-04-solicitar-reserva.md#e5-2), [E7.1](../casos-de-uso/UC-04-solicitar-reserva.md#e7-1), [E7.2](../casos-de-uso/UC-04-solicitar-reserva.md#e7-2) · US/CA: [US-08 · CA-07](../historias/US-08-solicitar-reserva.md#us-08-ca-07) (TA-68), [US-08 · CA-08](../historias/US-08-solicitar-reserva.md#us-08-ca-08) (TA-69), [US-08 · CA-14](../historias/US-08-solicitar-reserva.md#us-08-ca-14) (TA-75), [US-08 · CA-15](../historias/US-08-solicitar-reserva.md#us-08-ca-15) (TA-76) |
| **Evidência (complementar)** | 400 com `campos`. `reservas/tests/test_api_reservas.py::test_campos_ausentes_respondem_400_com_cada_campo`, `::test_dado_invalido_responde_400_sem_salvar [data-inexistente, fim-antes-do-inicio, sem-finalidade]`; `reservas/tests/test_reserva.py::test_finalidade_vazia_e_recusada [x]`, `::test_finalidade_acima_do_limite_e_recusada`; `reservas/tests/test_intervalo_de_horario.py::test_fim_igual_ou_antes_do_inicio_e_recusado [x]` |
| **Código (complementar)** | `reservas/domain/reserva.py::Reserva`, `reservas/domain/intervalo_de_horario.py::IntervaloDeHorario`, `reservas/domain/texto.py::exigir_tamanho_maximo` |
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
| **Vínculos** | UC: [UC-04 Solicitar reserva](../casos-de-uso/README.md#uc-04) (exceção) — na ficha: [UC-04 E5.3](../casos-de-uso/UC-04-solicitar-reserva.md#e5-3) · US/CA: [US-08 · CA-09](../historias/US-08-solicitar-reserva.md#us-08-ca-09) (TA-70), [US-08 · CA-13](../historias/US-08-solicitar-reserva.md#us-08-ca-13) (TA-74) |
| **Evidência (complementar)** | 400 `DATA_RETROATIVA` em `campos.data`. `reservas/tests/test_reserva.py::test_solicitar_com_inicio_igual_a_agora_e_recusado`, `::test_solicitar_um_minuto_depois_de_agora_e_aceito`, `::test_solicitar_para_ontem_e_recusado`; `reservas/tests/test_api_reservas.py::test_dado_invalido_responde_400_sem_salvar [data-retroativa]` |
| **Código (complementar)** | `reservas/domain/reserva.py::Reserva.solicitar`, `reservas/domain/excecoes.py::DataRetroativa` |
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
| **Vínculos** | UC: [UC-05 Verificar disponibilidade do horário](../casos-de-uso/README.md#uc-05) (exceção) — na ficha: [UC-04 E8.1](../casos-de-uso/UC-04-solicitar-reserva.md#e8-1), [E8.2](../casos-de-uso/UC-04-solicitar-reserva.md#e8-2) · US/CA: [US-08 · CA-06](../historias/US-08-solicitar-reserva.md#us-08-ca-06) (TA-67), [US-08 · CA-16](../historias/US-08-solicitar-reserva.md#us-08-ca-16) (TA-77), [US-08 · CA-17](../historias/US-08-solicitar-reserva.md#us-08-ca-17) (TA-78) |
| **Evidência (complementar)** | 404 `ESPACO_NAO_ENCONTRADO` ou 409 `ESPACO_INATIVO`. `reservas/tests/test_api_reservas.py::test_espaco_inexistente_responde_404`; `espacos/tests/test_api_desativacao_e_reservas.py::test_espaco_desativado_recusa_nova_reserva_com_409`; `reservas/tests/test_criar_reserva.py::test_espaco_indisponivel_propaga_o_erro_sem_salvar [x]` |
| **Código (complementar)** | `reservas/application/casos_de_uso.py::CriarReserva.executar`, `reservas/application/portas.py::ConsultaDeEspacos.obter_espaco_reservavel`, `espacos/publico.py::verificar_espaco_disponivel`, `espacos/domain/espaco_esportivo.py::EspacoEsportivo.garantir_que_esta_ativo` |
| **Regras de negócio** | [Espaço reservável](../glossario.md#espaco-reservavel), [espaço inativo](../glossario.md#espaco-inativo) |
| **Decisões** | [DEC-06](../decisoes/DEC-06.md) (decidida) |
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
| **Vínculos** | UC: [UC-05 Verificar disponibilidade do horário](../casos-de-uso/README.md#uc-05) (exceção) — na ficha: [UC-04 E9.1](../casos-de-uso/UC-04-solicitar-reserva.md#e9-1), [E10.1](../casos-de-uso/UC-04-solicitar-reserva.md#e10-1) · US/CA: [US-08 · CA-18](../historias/US-08-solicitar-reserva.md#us-08-ca-18) (TA-79), [US-08 · CA-19](../historias/US-08-solicitar-reserva.md#us-08-ca-19) (TA-80) |
| **Evidência (complementar)** | 409 `CONFLITO_DE_HORARIO`, sem `campos`. `reservas/tests/test_api_reservas.py::test_horario_ocupado_responde_409_e_preserva_as_reservas`; `reservas/tests/test_conflito_de_horario.py::test_sobreposicao_com_reserva_que_ocupa_horario_e_conflito [x]`, `::test_horario_encostado_e_aceito [x]`, `::test_mesmo_horario_em_outro_espaco_e_aceito`, `::test_mensagem_mostra_horario_e_situacao_sem_dados_do_outro_solicitante`; `exemplos/tests/test_carregar_dados_exemplo.py::test_horario_de_conflito_documentado_responde_409` |
| **Código (complementar)** | `reservas/domain/conflito_de_horario.py::garantir_horario_livre`, `reservas/domain/intervalo_de_horario.py::IntervaloDeHorario.sobrepoe`, `reservas/application/casos_de_uso.py::CriarReserva.executar`, `reservas/infrastructure/models.py::ReservaModel`, `reservas/infrastructure/repositorio_django.py::RepositorioReservasDjango.salvar` |
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
| **Vínculos** | UC: [UC-05 Verificar disponibilidade do horário](../casos-de-uso/README.md#uc-05) (exceção) — na ficha: [UC-04 E6.1](../casos-de-uso/UC-04-solicitar-reserva.md#e6-1), [E6.2](../casos-de-uso/UC-04-solicitar-reserva.md#e6-2), [E6.3](../casos-de-uso/UC-04-solicitar-reserva.md#e6-3) · US/CA: [US-08 · CA-04](../historias/US-08-solicitar-reserva.md#us-08-ca-04) (TA-65), [US-08 · CA-10](../historias/US-08-solicitar-reserva.md#us-08-ca-10) (TA-71), [US-08 · CA-11](../historias/US-08-solicitar-reserva.md#us-08-ca-11) (TA-72), [US-08 · CA-12](../historias/US-08-solicitar-reserva.md#us-08-ca-12) (TA-73), [US-08 · CA-13](../historias/US-08-solicitar-reserva.md#us-08-ca-13) (TA-74) |
| **Evidência (complementar)** | 400 `FORA_DO_HORARIO_DE_FUNCIONAMENTO`, `DURACAO_INVALIDA` ou `ANTECEDENCIA_EXCEDIDA`. `reservas/tests/test_api_reservas.py::test_dado_invalido_responde_400_sem_salvar [antes-da-abertura, duracao-acima-da-maxima, alem-da-antecedencia]`; `reservas/tests/test_regras_de_agenda.py::test_horario_nas_bordas_do_funcionamento_e_aceito [x]`, `::test_horario_fora_do_funcionamento_e_recusado_no_campo_certo [x]`, `::test_duracao_fora_dos_limites_e_recusada_no_termino [x]`, `::test_data_alem_da_antecedencia_e_recusada_com_a_data_limite`; `reservas/tests/test_reserva.py::test_horario_de_funcionamento_e_checado_antes_da_duracao`, `::test_duracao_e_checada_antes_da_antecedencia`; `reservas/tests/test_propriedades_da_agenda.py::test_solicitar_aceita_so_o_que_respeita_as_regras_e_recusa_pela_primeira_violada` |
| **Código (complementar)** | `reservas/domain/regras_de_agenda.py::garantir_regras_de_agenda`, `reservas/domain/reserva.py::Reserva.solicitar` |
| **Regras de negócio** | [Regras de agenda](../glossario.md#regras-de-agenda), [horário de funcionamento](../glossario.md#horario-de-funcionamento), [duração mínima](../glossario.md#duracao-minima), [duração máxima](../glossario.md#duracao-maxima), [antecedência máxima](../glossario.md#antecedencia-maxima), [data limite](../glossario.md#data-limite) |
| **Decisões** | [DEC-07](../decisoes/DEC-07.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

## Consulta de reservas

### <a id="rf-12"></a>RF-12 · Consultar reservas por critérios combináveis

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao Gestor consultar as reservas por espaço, situação, data, solicitante (trecho do nome ou da matrícula) e "somente as minhas", sozinhos ou combinados, e ver só as reservas que atendem a todos os critérios informados, ordenadas pelo início, com a quantidade encontrada (em páginas: [RF-12.2](#rf-12-2)). |
| **Origem** | NS-08 |
| **Funcionalidade** | F3 |
| **Prioridade (QFD)** | Normal — "consultar por pelo menos dois critérios" é a terceira funcionalidade do enunciado. |
| **Vínculos** | UC: [UC-07 Consultar reservas](../casos-de-uso/README.md#uc-07) (fluxo principal) — na ficha: [UC-07 passos 3 e 4](../casos-de-uso/fichas-resumidas.md#uc07-p3) · US/CA: [US-10 · CA-03](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-03) (TA-95), [US-10 · CA-06](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-06) (TA-98), [US-11 · CA-01](../historias/US-11-acompanhar-todas-as-reservas.md#us-11-ca-01) (TA-105), [US-11 · CA-02](../historias/US-11-acompanhar-todas-as-reservas.md#us-11-ca-02) (TA-106), [US-11 · CA-06](../historias/US-11-acompanhar-todas-as-reservas.md#us-11-ca-06) (TA-110) |
| **Evidência (complementar)** | `GET /api/reservas/?espaco=&situacao=&data=&solicitante=&minhas=` (com `pagina` e `tamanho`, [RF-12.2](#rf-12-2)); tela `/reservas` (filtros e página no endereço). `reservas/tests/test_api_consulta_reservas.py::test_consulta_sem_filtros_devolve_todas_ordenadas_por_inicio`, `::test_cada_criterio_sozinho_devolve_so_as_correspondentes [x]`, `::test_criterios_combinados_se_somam [x]`, `::test_mensagem_informa_a_quantidade_encontrada [x]`, `::test_consulta_nao_altera_as_reservas`; `reservas/tests/test_api_permissoes.py::test_gestor_lista_todas_e_filtra_por_solicitante`; `pages/PaginaReservas.test.tsx` |
| **Código (complementar)** | `reservas/application/casos_de_uso.py::ConsultarReservas.executar`, `reservas/application/repositorio.py::FiltrosDeReservas`, `reservas/infrastructure/repositorio_django.py::RepositorioReservasDjango.listar` |
| **Regras de negócio** | [Reserva](../glossario.md#reserva), [situação da reserva](../glossario.md#situacao), [solicitante da reserva](../glossario.md#solicitante-da-reserva). Um espaço inexistente no critério dá lista vazia, não erro. |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-12-1"></a>RF-12.1 · Recusar critério de consulta em formato inválido

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve impedir que o usuário autenticado consulte reservas com uma situação fora da lista, uma data que não existe, um espaço que não seja um número, uma página que não seja um número inteiro a partir de 1 ou um tamanho de página fora de 1 a 100, e informar o critério com problema. |
| **Pai** | [RF-12](#rf-12) |
| **Origem** | NS-08 (principal); NS-13 |
| **Funcionalidade** | F5 |
| **Prioridade (QFD)** | Esperado — um critério ignorado em silêncio mostraria reservas que a pessoa não pediu. |
| **Vínculos** | UC: [UC-07 Consultar reservas](../casos-de-uso/README.md#uc-07) (exceção) — na ficha: [UC-07 E3.1](../casos-de-uso/fichas-resumidas.md#uc07-e3-1) · US/CA: [US-10 · CA-10](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-10) (TA-102), [US-11 · CA-09](../historias/US-11-acompanhar-todas-as-reservas.md#us-11-ca-09) (TA-113) |
| **Evidência (complementar)** | 400 `DADOS_INVALIDOS` com `campos`. `reservas/tests/test_api_consulta_reservas.py::test_filtro_invalido_responde_400_com_o_campo [x]`, `::test_filtro_em_branco_e_ignorado [x]`; `reservas/tests/test_api_paginacao_de_reservas.py::test_pagina_ou_tamanho_invalidos_respondem_400_com_o_campo [x]`, `::test_pagina_ou_tamanho_em_branco_valem_o_padrao [x]` |
| **Código (complementar)** | `reservas/api/serializers.py::FiltrosReservasSerializer`, `reservas/application/repositorio.py::TAMANHO_MAXIMO_DA_PAGINA` |
| **Regras de negócio** | [Situação da reserva](../glossario.md#situacao) |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

#### <a id="rf-12-2"></a>RF-12.2 · Apresentar o resultado da consulta em páginas

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao usuário autenticado ver o resultado da consulta de reservas em páginas de até 20 reservas, mantendo a ordem pelo início, e informar o total encontrado, a página atual e o número de páginas; as páginas juntas trazem cada reserva uma vez só, e uma página além da última vem sem reservas, com o total. |
| **Pai** | [RF-12](#rf-12) |
| **Origem** | NS-08 (principal); NS-07 |
| **Funcionalidade** | F3 |
| **Prioridade (QFD)** | Esperado — o cliente não pede páginas, mas com alguns milhares de reservas a lista inteira passava da meta de tempo ([RNF-P01](rnf.md#rnf-p01)). |
| **Vínculos** | UC: [UC-07 Consultar reservas](../casos-de-uso/README.md#uc-07) (fluxo principal) — na ficha: [UC-07 passo 2](../casos-de-uso/fichas-resumidas.md#uc07-p2), [A2.3](../casos-de-uso/fichas-resumidas.md#uc07-a2-3), [A2.4](../casos-de-uso/fichas-resumidas.md#uc07-a2-4), [A3.2](../casos-de-uso/fichas-resumidas.md#uc07-a3-2) · US/CA: [US-10 · CA-04](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-04) (TA-96), [US-10 · CA-08](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-08) (TA-100), [US-10 · CA-09](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-09) (TA-101), [US-10 · CA-12](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-12) (TA-104), [US-11 · CA-04](../historias/US-11-acompanhar-todas-as-reservas.md#us-11-ca-04) (TA-108), [US-11 · CA-07](../historias/US-11-acompanhar-todas-as-reservas.md#us-11-ca-07) (TA-111), [US-11 · CA-08](../historias/US-11-acompanhar-todas-as-reservas.md#us-11-ca-08) (TA-112) |
| **Evidência (complementar)** | `GET /api/reservas/?pagina=&tamanho=` (padrão: página 1, tamanho 20; máximo 100), com `paginacao` `{pagina, tamanho, total, total_de_paginas}` na resposta; tela `/reservas` ("Anterior", "Página X de Y", "Próxima"; página no endereço). `reservas/tests/test_api_paginacao_de_reservas.py::test_sem_parametros_devolve_a_primeira_pagina_de_20_com_o_total`, `::test_as_paginas_juntas_dao_a_lista_completa_sem_repeticao`, `::test_pagina_depois_da_ultima_responde_200_sem_reservas [x]`, `::test_solicitante_conta_e_pagina_so_as_proprias`; `reservas/tests/test_repositorio_reservas.py::test_listar_devolve_a_pagina_pedida_com_o_total [x]`, `::test_listar_pagina_no_banco_com_count_e_limit`; `reservas/tests/test_propriedades_da_paginacao.py::test_as_paginas_em_ordem_formam_a_lista_completa_sem_repeticao`; `pages/PaginaReservas.test.tsx`; `components/reservas/PaginacaoDeReservas.test.tsx` |
| **Código (complementar)** | `reservas/application/repositorio.py::Paginacao`, `reservas/application/repositorio.py::PaginaDeReservas`, `reservas/application/casos_de_uso.py::ConsultarReservas.executar`, `reservas/infrastructure/repositorio_django.py::RepositorioReservasDjango.listar` |
| **Regras de negócio** | [Reserva](../glossario.md#reserva). A paginação é da consulta, não da regra: a ordem (início e, no empate, código da reserva) e a visibilidade ([RF-13](#rf-13)) são as mesmas. Mudar um critério recomeça da primeira página. |
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
| **Vínculos** | UC: [UC-07 Consultar reservas](../casos-de-uso/README.md#uc-07) (fluxo principal) — na ficha: [UC-07 passo 2](../casos-de-uso/fichas-resumidas.md#uc07-p2), [A3.1](../casos-de-uso/fichas-resumidas.md#uc07-a3-1) · US/CA: [US-10 · CA-01](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-01) (TA-93), [US-10 · CA-05](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-05) (TA-97), [US-10 · CA-07](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-07) (TA-99), [US-10 · CA-11](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-11) (TA-103), [US-10 · CA-12](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-12) (TA-104), [US-11 · CA-05](../historias/US-11-acompanhar-todas-as-reservas.md#us-11-ca-05) (TA-109), [US-11 · CA-10](../historias/US-11-acompanhar-todas-as-reservas.md#us-11-ca-10) (TA-114) |
| **Evidência (complementar)** | `GET /api/reservas/` como Solicitante; tela "Minhas reservas" (`/reservas`). `reservas/tests/test_api_permissoes.py::test_solicitante_so_lista_as_proprias [x]`, `::test_solicitante_sem_filtros_ve_a_propria`; `reservas/tests/test_consultar_reservas.py::test_solicitante_so_ve_as_proprias_mesmo_filtrando_por_outro [x]`, `::test_solicitante_conta_e_pagina_so_as_proprias_ate_a_ultima_pagina`; `components/layout/Layout.test.tsx` ("logado como solicitante, o item das reservas se chama Minhas reservas") |
| **Código (complementar)** | `reservas/application/casos_de_uso.py::ConsultarReservas.executar`, `reservas/domain/reserva.py::Reserva.visivel_para` |
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
| **Vínculos** | UC: [UC-08 Consultar detalhe da reserva](../casos-de-uso/README.md#uc-08) (fluxo principal) — na ficha: [UC-08 passo 3](../casos-de-uso/fichas-resumidas.md#uc08-p3) · US/CA: [US-12 · CA-01](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-01) (TA-115), [US-12 · CA-04](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-04) (TA-118), [US-12 · CA-10](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-10) (TA-124) |
| **Evidência (complementar)** | `GET /api/reservas/{id}/`; tela `/reservas/:reservaId`. `reservas/tests/test_api_consulta_reservas.py::test_detalhe_devolve_a_reserva_no_mesmo_formato_da_criacao`; `reservas/tests/test_api_permissoes.py::test_gestor_ve_o_detalhe_de_qualquer_reserva`; `pages/PaginaReserva.test.tsx` |
| **Código (complementar)** | `reservas/application/casos_de_uso.py::ObterReserva.executar` |
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
| **Vínculos** | UC: [UC-07 Consultar reservas](../casos-de-uso/README.md#uc-07) (fluxo principal) — na ficha: [UC-07 passo 3](../casos-de-uso/fichas-resumidas.md#uc07-p3) · US/CA: [US-10 · CA-03](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-03) (TA-95), [US-11 · CA-02](../historias/US-11-acompanhar-todas-as-reservas.md#us-11-ca-02) (TA-106) |
| **Evidência (complementar)** | `GET /api/reservas/situacoes/` (sem login); seletor de situação em `/reservas`. `reservas/tests/test_api_consulta_reservas.py::test_situacoes_de_reserva_listam_todas_na_ordem_do_enum_sem_login` |
| **Código (complementar)** | `reservas/domain/situacao.py::SituacaoReserva`, `reservas/api/views.py::SituacoesDeReservaView.get` |
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
| **Vínculos** | UC: [UC-07 Consultar reservas](../casos-de-uso/README.md#uc-07) (fluxo principal); também em [UC-08 Consultar detalhe da reserva](../casos-de-uso/README.md#uc-08) — na ficha: [UC-07 passo 2](../casos-de-uso/fichas-resumidas.md#uc07-p2), [UC-08 passo 3](../casos-de-uso/fichas-resumidas.md#uc08-p3), [UC-10 passo 2](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p2) · US/CA: [US-10 · CA-02](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-02) (TA-94), [US-11 · CA-03](../historias/US-11-acompanhar-todas-as-reservas.md#us-11-ca-03) (TA-107), [US-12 · CA-01](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-01) (TA-115), [US-12 · CA-03](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-03) (TA-117), [US-13 · CA-04](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-04) (TA-128), [US-16 · CA-03](../historias/US-16-concluir-uma-reserva.md#us-16-ca-03) (TA-154) |
| **Evidência (complementar)** | Campo `acoes_disponiveis` de toda reserva (`GET /api/reservas/`, `GET /api/reservas/{id}/`); botões na lista `/reservas` e no detalhe `/reservas/:reservaId`. `reservas/tests/test_api_situacao_reserva.py::test_reserva_solicitada_traz_confirmar_recusar_e_cancelar`, `::test_reserva_confirmada_traz_cancelar_e_concluir`, `::test_reserva_concluida_nao_traz_acoes`; `reservas/tests/test_api_permissoes.py::test_acoes_do_solicitante_na_propria_solicitada_sao_so_cancelar`; `reservas/tests/test_propriedades_da_reserva.py::TestMaquinaDaReserva` (as ações são exatamente as mudanças aceitas); `components/reservas/TabelaDeReservas.test.tsx` |
| **Código (complementar)** | `reservas/domain/reserva.py::Reserva.acoes_permitidas_para`, `reservas/domain/situacao.py::transicoes_a_partir_de`, `reservas/api/serializers.py::ReservaSaidaSerializer.get_acoes_disponiveis` |
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
| **Vínculos** | UC: [UC-17 Confirmar reserva](../casos-de-uso/README.md#uc-17) (fluxo principal) — na ficha: [UC-10 passos 1 a 8, variação UC-17](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-17) · US/CA: [US-14 · CA-01](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-01) (TA-134), [US-14 · CA-02](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-02) (TA-135), [US-14 · CA-03](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-03) (TA-136), [US-14 · CA-07](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-07) (TA-140), [US-14 · CA-08](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-08) (TA-141) |
| **Evidência (complementar)** | `PATCH /api/reservas/{id}/situacao/` com `CONFIRMADA`; diálogo "Confirmar reserva". `reservas/tests/test_api_situacao_reserva.py::test_confirmar_responde_200_com_a_reserva_atualizada`; `reservas/tests/test_api_permissoes.py::test_gestor_confirma`; `reservas/tests/test_reserva.py::test_motivo_opcional_ao_confirmar_e_guardado_normalizado` |
| **Código (complementar)** | `reservas/application/casos_de_uso.py::AlterarSituacaoReserva.executar`, `reservas/domain/reserva.py::Reserva.alterar_situacao` |
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
| **Vínculos** | UC: [UC-18 Recusar reserva](../casos-de-uso/README.md#uc-18) (fluxo principal) — na ficha: [UC-10 passos 1 a 8, variação UC-18](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-18) · US/CA: [US-15 · CA-01](../historias/US-15-recusar-uma-reserva.md#us-15-ca-01) (TA-145), [US-15 · CA-02](../historias/US-15-recusar-uma-reserva.md#us-15-ca-02) (TA-146) |
| **Evidência (complementar)** | `PATCH /api/reservas/{id}/situacao/` com `RECUSADA` e `motivo`; diálogo "Recusar reserva". `reservas/tests/test_api_situacao_reserva.py::test_mensagem_de_sucesso_usa_o_rotulo_da_nova_situacao [recusada]`; `reservas/tests/test_alterar_situacao.py::test_transicao_permitida_e_persistida [x]`; `reservas/tests/test_conflito_de_horario.py::test_sobreposicao_com_reserva_que_nao_ocupa_horario_e_aceita [x]` |
| **Código (complementar)** | `reservas/application/casos_de_uso.py::AlterarSituacaoReserva.executar`, `reservas/domain/reserva.py::Reserva.alterar_situacao`, `reservas/domain/situacao.py::SITUACOES_QUE_EXIGEM_MOTIVO` |
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
| **Vínculos** | UC: [UC-19 Concluir reserva](../casos-de-uso/README.md#uc-19) (fluxo principal) — na ficha: [UC-10 passos 1 a 8, variação UC-19](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-19) · US/CA: [US-16 · CA-01](../historias/US-16-concluir-uma-reserva.md#us-16-ca-01) (TA-152), [US-16 · CA-02](../historias/US-16-concluir-uma-reserva.md#us-16-ca-02) (TA-153) |
| **Evidência (complementar)** | `PATCH /api/reservas/{id}/situacao/` com `CONCLUIDA`. `reservas/tests/test_api_situacao_reserva.py::test_fluxo_da_demonstracao_ate_concluida` (conclui uma reserva de amanhã: hoje não há verificação de horário), `::test_reserva_concluida_nao_traz_acoes` |
| **Código (complementar)** | `reservas/application/casos_de_uso.py::AlterarSituacaoReserva.executar`, `reservas/domain/reserva.py::Reserva.alterar_situacao` |
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
| **Vínculos** | UC: [UC-11 Cancelar reserva](../casos-de-uso/README.md#uc-11) (fluxo principal) — na ficha: [UC-10 passos 1 a 8, variação UC-11](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-11) · US/CA: [US-07 · CA-04](../historias/US-07-desativar-e-reativar-espaco.md#us-07-ca-04) (TA-56), [US-13 · CA-02](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-02) (TA-126), [US-13 · CA-03](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-03) (TA-127) |
| **Evidência (complementar)** | `PATCH /api/reservas/{id}/situacao/` com `CANCELADA` e `motivo`. `reservas/tests/test_api_situacao_reserva.py::test_mensagem_de_sucesso_usa_o_rotulo_da_nova_situacao [cancelada]`, `::test_cancelar_libera_o_horario_para_nova_reserva`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]` (gestor, `CANCELADA` com motivo) |
| **Código (complementar)** | `reservas/application/casos_de_uso.py::AlterarSituacaoReserva.executar`, `reservas/domain/reserva.py::Reserva.alterar_situacao`, `reservas/domain/situacao.py::SITUACOES_QUE_EXIGEM_MOTIVO` |
| **Regras de negócio** | [Cancelada](../glossario.md#cancelada), [motivo](../glossario.md#motivo) |
| **Decisões** | [DEC-06](../decisoes/DEC-06.md) (decidida; é assim que o Gestor desfaz as reservas de um espaço desativado), [DEC-13](../decisoes/DEC-13.md) |
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
| **Vínculos** | UC: [UC-11 Cancelar reserva](../casos-de-uso/README.md#uc-11) (fluxo principal) — na ficha: [UC-10 passos 1 a 8, variação UC-11](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-11) · US/CA: [US-13 · CA-01](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-01) (TA-125), [US-13 · CA-03](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-03) (TA-127), [US-13 · CA-07](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-07) (TA-131) |
| **Evidência (complementar)** | `PATCH /api/reservas/{id}/situacao/` com `CANCELADA` e `motivo`, como Solicitante. `reservas/tests/test_api_permissoes.py::test_solicitante_cancela_a_propria`; `reservas/tests/test_alterar_situacao.py::test_solicitante_cancela_a_propria_reserva`; `reservas/tests/test_api_historico.py::test_cancelamento_aparece_com_o_motivo` |
| **Código (complementar)** | `reservas/application/casos_de_uso.py::AlterarSituacaoReserva.executar`, `reservas/domain/reserva.py::Reserva.alterar_situacao`, `reservas/domain/situacao.py::DESTINOS_POR_PAPEL` |
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
| **Vínculos** | UC: [UC-09 Consultar histórico da reserva](../casos-de-uso/README.md#uc-09) (fluxo principal); também em [UC-13 Registrar no histórico](../casos-de-uso/README.md#uc-13) — na ficha: [UC-09 passo 3](../casos-de-uso/fichas-resumidas.md#uc09-p3), [UC-04 passo 10](../casos-de-uso/UC-04-solicitar-reserva.md#p10), [UC-10 passo 7](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p7) · US/CA: [US-08 · CA-20](../historias/US-08-solicitar-reserva.md#us-08-ca-20) (TA-81), [US-12 · CA-02](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-02) (TA-116), [US-12 · CA-03](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-03) (TA-117), [US-12 · CA-05](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-05) (TA-119), [US-12 · CA-08](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-08) (TA-122), [US-12 · CA-09](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-09) (TA-123), [US-13 · CA-08](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-08) (TA-132), [US-14 · CA-09](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-09) (TA-142), [US-15 · CA-06](../historias/US-15-recusar-uma-reserva.md#us-15-ca-06) (TA-150), [US-16 · CA-05](../historias/US-16-concluir-uma-reserva.md#us-16-ca-05) (TA-156) |
| **Evidência (complementar)** | `GET /api/reservas/{id}/historico/`; linha do tempo em `/reservas/:reservaId`. `reservas/tests/test_api_historico.py::test_fluxo_completo_aparece_no_historico_em_ordem`, `::test_registrado_em_sai_em_iso_8601_no_fuso_de_sao_paulo`, `::test_registro_nao_expoe_o_id_do_autor`, `::test_tentativa_recusada_nao_aparece_no_historico`; `pages/PaginaReserva.test.tsx` |
| **Código (complementar)** | `reservas/application/casos_de_uso.py::ConsultarHistoricoDaReserva.executar`, `reservas/domain/registro_de_situacao.py::RegistroDeSituacao`, `reservas/infrastructure/repositorio_django.py::RepositorioReservasDjango.salvar` |
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
| **Vínculos** | UC: [UC-08 Consultar detalhe da reserva](../casos-de-uso/README.md#uc-08) (exceção); também em [UC-09 Consultar histórico da reserva](../casos-de-uso/README.md#uc-09), [UC-10 Alterar situação da reserva](../casos-de-uso/README.md#uc-10) — na ficha: [UC-08 E2.1](../casos-de-uso/fichas-resumidas.md#uc08-e2-1), [UC-09 E2.1](../casos-de-uso/fichas-resumidas.md#uc09-e2-1), [UC-10 E6.2](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-2) · US/CA: [US-10 · CA-11](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-11) (TA-103), [US-11 · CA-10](../historias/US-11-acompanhar-todas-as-reservas.md#us-11-ca-10) (TA-114), [US-12 · CA-06](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-06) (TA-120), [US-12 · CA-07](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-07) (TA-121), [US-12 · CA-10](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-10) (TA-124), [US-13 · CA-09](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-09) (TA-133), [US-14 · CA-11](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-11) (TA-144) |
| **Evidência (complementar)** | 404 `RESERVA_NAO_ENCONTRADA`. `reservas/tests/test_api_consulta_reservas.py::test_detalhe_inexistente_responde_404`; `reservas/tests/test_api_situacao_reserva.py::test_reserva_inexistente_responde_404`; `reservas/tests/test_api_historico.py::test_historico_de_reserva_inexistente_responde_404`, `::test_solicitante_pedindo_historico_de_outra_pessoa_recebe_404`; `reservas/tests/test_api_permissoes.py::test_detalhe_de_outra_pessoa_para_o_solicitante_responde_404`, `::test_solicitante_cancelando_a_de_outra_pessoa_responde_404_sem_mudar_nada` |
| **Código (complementar)** | `reservas/application/casos_de_uso.py::_obter_ou_falhar`, `reservas/domain/reserva.py::Reserva.visivel_para`, `reservas/domain/excecoes.py::ReservaNaoEncontrada` |
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
| **Vínculos** | UC: [UC-10 Alterar situação da reserva](../casos-de-uso/README.md#uc-10) (exceção) — na ficha: [UC-10 E6.5](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-5), [E2.1](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e2-1) · US/CA: [US-13 · CA-04](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-04) (TA-128), [US-13 · CA-05](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-05) (TA-129), [US-14 · CA-06](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-06) (TA-139), [US-15 · CA-03](../historias/US-15-recusar-uma-reserva.md#us-15-ca-03) (TA-147), [US-16 · CA-03](../historias/US-16-concluir-uma-reserva.md#us-16-ca-03) (TA-154), [US-16 · CA-04](../historias/US-16-concluir-uma-reserva.md#us-16-ca-04) (TA-155) |
| **Evidência (complementar)** | 409 `TRANSICAO_DE_SITUACAO_INVALIDA`. `reservas/tests/test_api_situacao_reserva.py::test_transicao_proibida_responde_409_e_preserva_a_reserva`, `::test_reserva_concluida_nao_pode_ser_cancelada`; `reservas/tests/test_reserva.py::test_transicao_proibida_e_recusada_e_preserva_a_situacao [x]`, `::test_transicao_proibida_tem_mensagem_com_os_rotulos`; `reservas/tests/test_situacao.py::test_transicao_permitida_segue_a_tabela [x]` |
| **Código (complementar)** | `reservas/domain/reserva.py::Reserva.alterar_situacao`, `reservas/domain/situacao.py::TRANSICOES_PERMITIDAS`, `reservas/domain/situacao.py::transicao_permitida` |
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
| **Vínculos** | UC: [UC-10 Alterar situação da reserva](../casos-de-uso/README.md#uc-10) (exceção) — na ficha: [UC-10 E6.1](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-1), [E6.3](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-3) · US/CA: [US-14 · CA-04](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-04) (TA-137), [US-14 · CA-05](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-05) (TA-138) |
| **Evidência (complementar)** | 400 `DADOS_INVALIDOS` (ausente ou vazia) ou `SITUACAO_INVALIDA` (desconhecida), com `campos.situacao`. `reservas/tests/test_api_situacao_reserva.py::test_situacao_ausente_ou_invalida_responde_400 [x]` |
| **Código (complementar)** | `reservas/domain/reserva.py::Reserva.alterar_situacao`, `reservas/domain/excecoes.py::SituacaoInvalida` |
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
| **Vínculos** | UC: [UC-12 Informar motivo](../casos-de-uso/README.md#uc-12) (exceção) — na ficha: [UC-10 E6.6](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-6), [E6.7](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-7) · US/CA: [US-13 · CA-06](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-06) (TA-130), [US-15 · CA-04](../historias/US-15-recusar-uma-reserva.md#us-15-ca-04) (TA-148), [US-15 · CA-05](../historias/US-15-recusar-uma-reserva.md#us-15-ca-05) (TA-149) |
| **Evidência (complementar)** | 400 `MOTIVO_OBRIGATORIO` ou `TEXTO_MUITO_LONGO` em `campos.motivo`. `reservas/tests/test_api_situacao_reserva.py::test_recusar_sem_motivo_responde_400_no_campo_motivo`; `reservas/tests/test_reserva.py::test_recusar_ou_cancelar_sem_motivo_e_recusado_e_nada_muda [x]`, `::test_motivo_acima_do_limite_e_recusado_e_nada_muda`; `reservas/tests/test_alterar_situacao.py::test_recusar_ou_cancelar_sem_motivo_lanca_erro_e_preserva_a_reserva [x]` |
| **Código (complementar)** | `reservas/domain/reserva.py::_exigir_motivo_se_necessario`, `reservas/domain/situacao.py::SITUACOES_QUE_EXIGEM_MOTIVO` |
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
| **Vínculos** | UC: [UC-10 Alterar situação da reserva](../casos-de-uso/README.md#uc-10) (exceção) — na ficha: [UC-10 E6.4](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-4) · US/CA: [US-14 · CA-10](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-10) (TA-143), [US-15 · CA-07](../historias/US-15-recusar-uma-reserva.md#us-15-ca-07) (TA-151), [US-16 · CA-06](../historias/US-16-concluir-uma-reserva.md#us-16-ca-06) (TA-157) |
| **Evidência (complementar)** | 403 `ACAO_NAO_PERMITIDA` ("Somente o gestor pode confirmar reservas."). `reservas/tests/test_api_permissoes.py::test_solicitante_confirmando_a_propria_responde_403_sem_mudar_nada`; `reservas/tests/test_permissoes_reserva.py::test_alterar_situacao_segue_a_matriz_e_preserva_a_reserva_nos_erros [x]`, `::test_solicitante_concluindo_uma_solicitada_recebe_403_e_nao_409`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]` (`reservas:situacao`) |
| **Código (complementar)** | `reservas/domain/reserva.py::Reserva.alterar_situacao`, `reservas/domain/situacao.py::papel_pode_levar_a`, `reservas/domain/excecoes.py::AlteracaoDeSituacaoNaoPermitida` |
| **Regras de negócio** | [Transição de situação](../glossario.md#transicao-de-situacao) (`DESTINOS_POR_PAPEL`), [perfil](../glossario.md#perfil) |
| **Decisões** | [DEC-04](../decisoes/DEC-04.md) |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |
