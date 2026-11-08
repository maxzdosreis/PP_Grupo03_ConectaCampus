# Mapa de impacto por decisão (DEC)

> Gerado por `scripts/gerar_rastreabilidade.py`, não edite à mão; para mudar um vínculo, mude a ficha de origem.

| Identificação | Responsabilidade |
|---|---|
| **Parte da [RAS-01](README.md) • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

Para cada DEC, tudo o que muda se a resposta for diferente da opção adotada: RF (campo Decisões das fichas), RNF (Origem), UC e passos (dos RF), US e CA (os que dependem da DEC e os que verificam os RF afetados), TA, endpoints, telas e código. A regressão estimada é o número de TAs a rever. Pronto para virar a seção "Mapa de impacto" de um [CR](../mudancas/modelo-cr.md). Ordem: DEC-13, DEC-05 e DEC-07 primeiro (maior impacto), depois as demais adotadas provisoriamente e, no fim, as decididas.

| DEC | Estado | RF | RNF | US | CA | TA (manuais) | Tipo de mudança |
|---|---|---|---|---|---|---|---|
| [DEC-13](#dec-13) | Decidida | 6 | 0 | 9 | 21 | 21 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-05](#dec-05) | Decidida | 1 | 1 | 6 | 10 | 10 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-07](#dec-07) | Decidida | 4 | 0 | 2 | 10 | 10 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-01](#dec-01) | Decidida | 0 | 0 | 0 | 0 | 0 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-02](#dec-02) | Decidida | 0 | 0 | 0 | 0 | 0 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-03](#dec-03) | Decidida | 0 | 0 | 0 | 0 | 0 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-04](#dec-04) | Decidida | 11 | 5 | 16 | 39 | 39 (2) | decidida: outra resposta só por CR (comportamental) |
| [DEC-05](#dec-05) | Decidida | 1 | 1 | 6 | 10 | 10 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-06](#dec-06) | Decidida | 5 | 1 | 4 | 14 | 14 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-07](#dec-07) | Decidida | 4 | 0 | 2 | 10 | 10 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-08](#dec-08) | Decidida | 0 | 1 | 0 | 0 | 0 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-09](#dec-09) | Decidida | 2 | 0 | 2 | 5 | 5 (1) | decidida: outra resposta só por CR (comportamental) |
| [DEC-10](#dec-10) | Decidida | 2 | 0 | 2 | 6 | 6 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-11](#dec-11) | Decidida | 1 | 1 | 1 | 5 | 5 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-12](#dec-12) | Decidida | 0 | 2 | 0 | 0 | 0 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-13](#dec-13) | Decidida | 6 | 0 | 9 | 21 | 21 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-14](#dec-14) | Decidida | 0 | 0 | 0 | 0 | 0 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-15](#dec-15) | Decidida | 0 | 0 | 0 | 0 | 0 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-16](#dec-16) | Decidida | 0 | 0 | 0 | 0 | 0 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-17](#dec-17) | Decidida | 0 | 0 | 0 | 0 | 0 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-18](#dec-18) | Decidida | 0 | 0 | 0 | 0 | 0 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-19](#dec-19) | Decidida | 0 | 0 | 0 | 0 | 0 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-20](#dec-20) | Decidida | 0 | 0 | 0 | 0 | 0 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-21](#dec-21) | Decidida | 0 | 0 | 0 | 0 | 0 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-22](#dec-22) | Decidida | 0 | 0 | 0 | 0 | 0 (0) | decidida: outra resposta só por CR (comportamental) |
| [DEC-23](#dec-23) | Decidida | 0 | 0 | 0 | 0 | 0 (0) | decidida: outra resposta só por CR (comportamental) |

## <a id="dec-13"></a>DEC-13 · Mudança de situação em relação ao horário da reserva

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-13.md)) |
| **Pergunta** | A mudança de situação deve depender do horário da reserva? Em especial: (1) o Gestor pode [concluir](../glossario.md#concluida) uma reserva cujo término ainda não chegou? (2) pode [confirmar](../glossario.md#confirmada) ou [recusar](../glossario.md#recusada) uma reserva cujo início já passou? (3) o Solicitante ou o Gestor podem [cancelar](../glossario.md#cancelada) depois do início? (4) o que acontece com uma reserva [Solicitada](../glossario.md#solicitada) que ninguém decidiu até a data dela passar? |
| **Opção adotada** | O Gestor só conclui uma reserva a partir do término dela e só recusa ou cancela uma reserva antes do início dela; confirmar, o cancelamento pelo Solicitante e a ocupação do horário pela Solicitada não decidida não dependem do horário. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor como representante do cliente. |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 21 TAs a rever (0 manuais), de 21 CAs em 9 histórias: 5 CAs dependem diretamente da DEC e 16 verificam os RF afetados |

- **RF:** [RF-16](matriz.md#rf-16), [RF-17](matriz.md#rf-17), [RF-18](matriz.md#rf-18), [RF-19](matriz.md#rf-19), [RF-20](matriz.md#rf-20), [RF-21](matriz.md#rf-21)
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):**
  - RF-16: [UC-07](../casos-de-uso/README.md#uc-07) · fluxo principal — [UC-07 passo 2](../casos-de-uso/fichas-resumidas.md#uc07-p2), [UC-08 passo 3](../casos-de-uso/fichas-resumidas.md#uc08-p3), [UC-10 passo 2](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p2)
  - RF-17: [UC-17](../casos-de-uso/README.md#uc-17) · fluxo principal — [UC-10 passos 1 a 8, variação UC-17](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-17)
  - RF-18: [UC-18](../casos-de-uso/README.md#uc-18) · fluxo principal — [UC-10 passos 1 a 8, variação UC-18](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-18)
  - RF-19: [UC-19](../casos-de-uso/README.md#uc-19) · fluxo principal — [UC-10 passos 1 a 8, variação UC-19](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-19)
  - RF-20: [UC-11](../casos-de-uso/README.md#uc-11) · fluxo principal (pelo Gestor) — [UC-10 passos 1 a 8, variação UC-11](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-11)
  - RF-21: [UC-11](../casos-de-uso/README.md#uc-11) · fluxo principal (pelo Solicitante, na própria) — [UC-10 passos 1 a 8, variação UC-11](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-11)
- **US:** [US-07](../historias/US-07-desativar-e-reativar-espaco.md), [US-08](../historias/US-08-solicitar-reserva.md), [US-10](../historias/US-10-acompanhar-minhas-reservas.md), [US-11](../historias/US-11-acompanhar-todas-as-reservas.md), [US-12](../historias/US-12-ver-detalhe-e-historico.md), [US-13](../historias/US-13-cancelar-uma-reserva.md), [US-14](../historias/US-14-confirmar-uma-reserva.md), [US-15](../historias/US-15-recusar-uma-reserva.md), [US-16](../historias/US-16-concluir-uma-reserva.md)
- **CA que dependem da DEC:** US-08: [CA-18](../historias/US-08-solicitar-reserva.md#us-08-ca-18); US-13: [CA-01](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-01); US-14: [CA-01](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-01); US-15: [CA-01](../historias/US-15-recusar-uma-reserva.md#us-15-ca-01); US-16: [CA-01](../historias/US-16-concluir-uma-reserva.md#us-16-ca-01)
- **CA dos RF afetados (regressão):** US-07: [CA-04](../historias/US-07-desativar-e-reativar-espaco.md#us-07-ca-04); US-10: [CA-02](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-02); US-11: [CA-03](../historias/US-11-acompanhar-todas-as-reservas.md#us-11-ca-03); US-12: [CA-01](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-01), [CA-03](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-03); US-13: [CA-02](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-02), [CA-03](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-03), [CA-04](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-04), [CA-07](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-07); US-14: [CA-02](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-02), [CA-03](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-03), [CA-07](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-07), [CA-08](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-08); US-15: [CA-02](../historias/US-15-recusar-uma-reserva.md#us-15-ca-02); US-16: [CA-02](../historias/US-16-concluir-uma-reserva.md#us-16-ca-02), [CA-03](../historias/US-16-concluir-uma-reserva.md#us-16-ca-03)
- **TA:** [TA-53](../historias/US-07-desativar-e-reativar-espaco.md#ta-53), [TA-76](../historias/US-08-solicitar-reserva.md#ta-76), [TA-91](../historias/US-10-acompanhar-minhas-reservas.md#ta-91), [TA-100](../historias/US-11-acompanhar-todas-as-reservas.md#ta-100), [TA-105](../historias/US-12-ver-detalhe-e-historico.md#ta-105), [TA-107](../historias/US-12-ver-detalhe-e-historico.md#ta-107), [TA-115](../historias/US-13-cancelar-uma-reserva.md#ta-115), [TA-116](../historias/US-13-cancelar-uma-reserva.md#ta-116), [TA-117](../historias/US-13-cancelar-uma-reserva.md#ta-117), [TA-118](../historias/US-13-cancelar-uma-reserva.md#ta-118), [TA-121](../historias/US-13-cancelar-uma-reserva.md#ta-121), [TA-124](../historias/US-14-confirmar-uma-reserva.md#ta-124), [TA-125](../historias/US-14-confirmar-uma-reserva.md#ta-125), [TA-126](../historias/US-14-confirmar-uma-reserva.md#ta-126), [TA-130](../historias/US-14-confirmar-uma-reserva.md#ta-130), [TA-131](../historias/US-14-confirmar-uma-reserva.md#ta-131), [TA-135](../historias/US-15-recusar-uma-reserva.md#ta-135), [TA-136](../historias/US-15-recusar-uma-reserva.md#ta-136), [TA-142](../historias/US-16-concluir-uma-reserva.md#ta-142), [TA-143](../historias/US-16-concluir-uma-reserva.md#ta-143), [TA-144](../historias/US-16-concluir-uma-reserva.md#ta-144)
- **Endpoint ou tela:** `GET /api/reservas/`; `GET /api/reservas/{id}/`; `/reservas`; `/reservas/:reservaId`; `PATCH /api/reservas/{id}/situacao/`
- **Código:** `reservas/domain/reserva.py::Reserva.acoes_permitidas_para`, `reservas/domain/situacao.py::transicoes_a_partir_de`, `reservas/api/serializers.py::ReservaSaidaSerializer.get_acoes_disponiveis`, `reservas/application/casos_de_uso.py::AlterarSituacaoReserva.executar`, `reservas/domain/reserva.py::Reserva.alterar_situacao`, `reservas/domain/situacao.py::SITUACOES_QUE_EXIGEM_MOTIVO`, `reservas/domain/situacao.py::DESTINOS_POR_PAPEL`

## <a id="dec-05"></a>DEC-05 · Histórico só com mudanças efetivas

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-05.md)) |
| **Pergunta** | Uma tentativa recusada de mudar a situação de uma reserva (perfil sem permissão, transição não permitida, motivo ausente) precisa ficar registrada? Se sim, onde e quem a consulta? |
| **Opção adotada** | Toda tentativa recusada de mudar a situação de uma reserva visível ao ator fica no histórico dessa reserva, com ator, momento, situação pedida, resultado e código do erro, sem mudar a situação. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor. |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 10 TAs a rever (0 manuais), de 10 CAs em 6 histórias: 6 CAs dependem diretamente da DEC e 4 verificam os RF afetados |

- **RF:** [RF-22](matriz.md#rf-22)
- **RNF:** [RNF-R02](../requisitos/rnf.md#rnf-r02)
- **UC (passo, alternativa ou exceção):**
  - RF-22: [UC-09](../casos-de-uso/README.md#uc-09) · fluxo principal (UC-13 grava o que UC-09 mostra) — [UC-09 passo 3](../casos-de-uso/fichas-resumidas.md#uc09-p3), [UC-04 passo 10](../casos-de-uso/UC-04-solicitar-reserva.md#p10), [UC-10 passo 7](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p7)
- **US:** [US-08](../historias/US-08-solicitar-reserva.md), [US-12](../historias/US-12-ver-detalhe-e-historico.md), [US-13](../historias/US-13-cancelar-uma-reserva.md), [US-14](../historias/US-14-confirmar-uma-reserva.md), [US-15](../historias/US-15-recusar-uma-reserva.md), [US-16](../historias/US-16-concluir-uma-reserva.md)
- **CA que dependem da DEC:** US-08: [CA-20](../historias/US-08-solicitar-reserva.md#us-08-ca-20); US-12: [CA-09](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-09); US-13: [CA-08](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-08); US-14: [CA-09](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-09); US-15: [CA-06](../historias/US-15-recusar-uma-reserva.md#us-15-ca-06); US-16: [CA-05](../historias/US-16-concluir-uma-reserva.md#us-16-ca-05)
- **CA dos RF afetados (regressão):** US-12: [CA-02](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-02), [CA-03](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-03), [CA-05](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-05), [CA-08](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-08)
- **TA:** [TA-78](../historias/US-08-solicitar-reserva.md#ta-78), [TA-106](../historias/US-12-ver-detalhe-e-historico.md#ta-106), [TA-107](../historias/US-12-ver-detalhe-e-historico.md#ta-107), [TA-109](../historias/US-12-ver-detalhe-e-historico.md#ta-109), [TA-112](../historias/US-12-ver-detalhe-e-historico.md#ta-112), [TA-113](../historias/US-12-ver-detalhe-e-historico.md#ta-113), [TA-122](../historias/US-13-cancelar-uma-reserva.md#ta-122), [TA-132](../historias/US-14-confirmar-uma-reserva.md#ta-132), [TA-140](../historias/US-15-recusar-uma-reserva.md#ta-140), [TA-146](../historias/US-16-concluir-uma-reserva.md#ta-146)
- **Endpoint ou tela:** `GET /api/reservas/{id}/historico/`; `/reservas/:reservaId`
- **Código:** `reservas/application/casos_de_uso.py::ConsultarHistoricoDaReserva.executar`, `reservas/domain/registro_de_situacao.py::RegistroDeSituacao`, `reservas/infrastructure/repositorio_django.py::RepositorioReservasDjango.salvar`

## <a id="dec-07"></a>DEC-07 · Valores das regras de agenda

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-07.md)) |
| **Pergunta** | Em que período do dia os espaços podem ser usados, qual a duração mínima e máxima de uma reserva e com quantos dias de antecedência se pode pedir? Esses limites são os mesmos para todos os espaços e todos os dias? |
| **Opção adotada** | Cada espaço tem o próprio horário de funcionamento, com padrão das 07:00 às 00:00 (o término à meia-noite é o fim do dia da reserva); o pedido sugere 1 hora de duração; a duração mínima (30 minutos), a máxima (3 horas) e a antecedência máxima (30 dias) continuam iguais para todos. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor como representante do cliente. |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 10 TAs a rever (0 manuais), de 10 CAs em 2 histórias: 5 CAs dependem diretamente da DEC e 5 verificam os RF afetados |

- **RF:** [RF-11.5](matriz.md#rf-11-5), [RF-28](matriz.md#rf-28), [RF-30](matriz.md#rf-30), [RF-31](matriz.md#rf-31)
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):**
  - RF-11.5: [UC-05](../casos-de-uso/README.md#uc-05) · exceção — [UC-04 E6.1](../casos-de-uso/UC-04-solicitar-reserva.md#e6-1), [E6.2](../casos-de-uso/UC-04-solicitar-reserva.md#e6-2), [E6.3](../casos-de-uso/UC-04-solicitar-reserva.md#e6-3)
  - RF-28: [UC-04](../casos-de-uso/README.md#uc-04) · fluxo principal (as regras aparecem no pedido) — [UC-04 passo 2](../casos-de-uso/UC-04-solicitar-reserva.md#p2), [A2.1](../casos-de-uso/UC-04-solicitar-reserva.md#a2-1), [UC-06 passo 5](../casos-de-uso/fichas-resumidas.md#uc06-p5)
  - RF-30: [UC-06](../casos-de-uso/README.md#uc-06) · fluxo principal — [UC-06 passos 4 e 5](../casos-de-uso/fichas-resumidas.md#uc06-p4), [UC-04 A3.1](../casos-de-uso/UC-04-solicitar-reserva.md#a3-1)
  - RF-31: [UC-06](../casos-de-uso/README.md#uc-06) · alternativa (data que não é reservável) — [UC-06 A4.1](../casos-de-uso/fichas-resumidas.md#uc06-a4-1), [UC-04 A3.1](../casos-de-uso/UC-04-solicitar-reserva.md#a3-1)
- **US:** [US-08](../historias/US-08-solicitar-reserva.md), [US-09](../historias/US-09-ver-a-agenda-do-dia.md)
- **CA que dependem da DEC:** US-08: [CA-02](../historias/US-08-solicitar-reserva.md#us-08-ca-02), [CA-10](../historias/US-08-solicitar-reserva.md#us-08-ca-10), [CA-11](../historias/US-08-solicitar-reserva.md#us-08-ca-11), [CA-12](../historias/US-08-solicitar-reserva.md#us-08-ca-12); US-09: [CA-05](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-05)
- **CA dos RF afetados (regressão):** US-08: [CA-04](../historias/US-08-solicitar-reserva.md#us-08-ca-04), [CA-13](../historias/US-08-solicitar-reserva.md#us-08-ca-13); US-09: [CA-01](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-01), [CA-02](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-02), [CA-03](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-03)
- **TA:** [TA-60](../historias/US-08-solicitar-reserva.md#ta-60), [TA-62](../historias/US-08-solicitar-reserva.md#ta-62), [TA-68](../historias/US-08-solicitar-reserva.md#ta-68), [TA-69](../historias/US-08-solicitar-reserva.md#ta-69), [TA-70](../historias/US-08-solicitar-reserva.md#ta-70), [TA-71](../historias/US-08-solicitar-reserva.md#ta-71), [TA-80](../historias/US-09-ver-a-agenda-do-dia.md#ta-80), [TA-81](../historias/US-09-ver-a-agenda-do-dia.md#ta-81), [TA-82](../historias/US-09-ver-a-agenda-do-dia.md#ta-82), [TA-84](../historias/US-09-ver-a-agenda-do-dia.md#ta-84)
- **Endpoint ou tela:** `POST /api/reservas/`; `/reservas/nova`; `GET /api/reservas/regras-de-agenda/`; `GET /api/reservas/ocupacao/`
- **Código:** `reservas/domain/regras_de_agenda.py::garantir_regras_de_agenda`, `reservas/domain/reserva.py::Reserva.solicitar`, `reservas/domain/regras_de_agenda.py::data_limite_para_reservar`, `reservas/domain/regras_de_agenda.py::HORARIO_DE_ABERTURA`, `reservas/api/serializers.py::RegrasDeAgendaSaidaSerializer.vigentes`, `reservas/domain/regras_de_agenda.py::horarios_livres`, `reservas/application/casos_de_uso.py::ConsultarOcupacaoDoDia.executar`, `reservas/domain/regras_de_agenda.py::garantir_data_reservavel`, `reservas/domain/regras_de_agenda.py::motivo_de_indisponibilidade`

## <a id="dec-01"></a>DEC-01 · React no frontend

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-01.md)) |
| **Pergunta** | O frontend pode ser feito em React, ou deve ser uma interface simples (terminal, desktop ou templates do Django)? |
| **Opção adotada** | "É liberado utilizar React no front-end, com isso confirmamos a utilização no projeto." |
| **Responsável** | Professor (resposta); grupo (confirmação). |
| **Prazo** | Não registrado. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 0 TAs a rever (0 manuais), de 0 CAs em 0 histórias: 0 CAs dependem diretamente da DEC e 0 verificam os RF afetados |

- **RF:** nenhum
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):** nenhum
- **US:** —
- **CA que dependem da DEC:** —
- **CA dos RF afetados (regressão):** —
- **TA:** —
- **Endpoint ou tela:** nenhum
- **Código:** nenhum

## <a id="dec-02"></a>DEC-02 · Docker e PostgreSQL na correção

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-02.md)) |
| **Pergunta** | O projeto pode ser executado com Docker (e o PostgreSQL dentro dele) na correção, já que o enunciado não exige banco de dados e recomenda memória ou arquivo JSON? |
| **Opção adotada** | "Não tem problema utilizar o Docker." (resposta registrada junto com a [DEC-03](../decisoes/DEC-03.md)) |
| **Responsável** | Professor (resposta); grupo (adoção). |
| **Prazo** | Não registrado. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 0 TAs a rever (0 manuais), de 0 CAs em 0 histórias: 0 CAs dependem diretamente da DEC e 0 verificam os RF afetados |

- **RF:** nenhum
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):** nenhum
- **US:** —
- **CA que dependem da DEC:** —
- **CA dos RF afetados (regressão):** —
- **TA:** —
- **Endpoint ou tela:** nenhum
- **Código:** nenhum

## <a id="dec-03"></a>DEC-03 · Arquivos do Docker na estrutura do ZIP

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-03.md)) |
| **Pergunta** | O ZIP precisa ter exatamente `README.md`, `src/` e `docs/`. Os arquivos do Docker (`docker-compose.yml`, `.env.example`) podem ficar dentro de `src/`? |
| **Opção adotada** | "Não tem problema utilizar o Docker." (resposta registrada junto com a [DEC-02](../decisoes/DEC-02.md)). O grupo mantém `docker-compose.yml` e `.env.example` dentro de `src/`. |
| **Responsável** | Professor (resposta); grupo (localização dos arquivos). |
| **Prazo** | Não registrado. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 0 TAs a rever (0 manuais), de 0 CAs em 0 histórias: 0 CAs dependem diretamente da DEC e 0 verificam os RF afetados |

- **RF:** nenhum
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):** nenhum
- **US:** —
- **CA que dependem da DEC:** —
- **CA dos RF afetados (regressão):** —
- **TA:** —
- **Endpoint ou tela:** nenhum
- **Código:** nenhum

## <a id="dec-04"></a>DEC-04 · Autenticação e perfis de acesso

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-04.md)) |
| **Pergunta** | O sistema precisa identificar quem solicita uma reserva e quem pode aprová-la? O enunciado de Projeto de Programação não exige autenticação real. |
| **Opção adotada** | O sistema terá cadastro e login de usuários (JWT) e dois perfis. `SOLICITANTE` solicita reservas, consulta as próprias e cancela as próprias. `GESTOR` cadastra e edita espaços, consulta todas as reservas e pode confirmá-las, recusá-las, concluí-las ou cancelá-las. O solicitante de uma reserva passa a ser sempre o usuário autenticado, e não um nome digitado no formulário. |
| **Responsável** | Professor (resposta); grupo (decisão). |
| **Prazo** | Decidida em 16/10/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 39 TAs a rever (2 manuais), de 39 CAs em 16 histórias: 2 CAs dependem diretamente da DEC e 37 verificam os RF afetados |

- **RF:** [RF-05](matriz.md#rf-05), [RF-10](matriz.md#rf-10), [RF-11](matriz.md#rf-11), [RF-13](matriz.md#rf-13), [RF-23](matriz.md#rf-23), [RF-27](matriz.md#rf-27), [RF-32](matriz.md#rf-32), [RF-33](matriz.md#rf-33), [RF-34](matriz.md#rf-34), [RF-36](matriz.md#rf-36), [RF-37](matriz.md#rf-37)
- **RNF:** [RNF-F01](../requisitos/rnf.md#rnf-f01), [RNF-F02](../requisitos/rnf.md#rnf-f02), [RNF-F03](../requisitos/rnf.md#rnf-f03), [RNF-F04](../requisitos/rnf.md#rnf-f04), [RNF-F09](../requisitos/rnf.md#rnf-f09)
- **UC (passo, alternativa ou exceção):**
  - RF-05: [UC-14](../casos-de-uso/README.md#uc-14) · fluxo principal — [UC-14 passos 1 a 8](../casos-de-uso/UC-14-cadastrar-espaco.md#p1)
  - RF-10: [UC-14](../casos-de-uso/README.md#uc-14) · exceção (recusa comum) — [UC-14 E1.1](../casos-de-uso/UC-14-cadastrar-espaco.md#e1-1), [UC-15 E1.1](../casos-de-uso/fichas-resumidas.md#uc15-e1-1), [UC-16 E1.1](../casos-de-uso/fichas-resumidas.md#uc16-e1-1)
  - RF-11: [UC-04](../casos-de-uso/README.md#uc-04) · fluxo principal — [UC-04 passos 1 a 11](../casos-de-uso/UC-04-solicitar-reserva.md#p1)
  - RF-13: [UC-07](../casos-de-uso/README.md#uc-07) · fluxo principal (o Solicitante vê só as próprias; para o Gestor, alternativa "somente as minhas") — [UC-07 passo 2](../casos-de-uso/fichas-resumidas.md#uc07-p2), [A3.1](../casos-de-uso/fichas-resumidas.md#uc07-a3-1)
  - RF-23: [UC-08](../casos-de-uso/README.md#uc-08) · exceção (recusa comum) — [UC-08 E2.1](../casos-de-uso/fichas-resumidas.md#uc08-e2-1), [UC-09 E2.1](../casos-de-uso/fichas-resumidas.md#uc09-e2-1), [UC-10 E6.2](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-2)
  - RF-27: [UC-10](../casos-de-uso/README.md#uc-10) · exceção (herdada pelos filhos) — [UC-10 E6.4](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-4)
  - RF-32: [UC-01](../casos-de-uso/README.md#uc-01) · fluxo principal — [UC-01 passos 1 a 4](../casos-de-uso/fichas-resumidas.md#uc01-p1)
  - RF-33: [UC-02](../casos-de-uso/README.md#uc-02) · fluxo principal — [UC-02 passos 1 a 4](../casos-de-uso/UC-02-autenticar.md#p1)
  - RF-34: [UC-02](../casos-de-uso/README.md#uc-02) · alternativa (continuar identificado) — [UC-02 A4.1](../casos-de-uso/UC-02-autenticar.md#a4-1)
  - RF-36: [UC-02](../casos-de-uso/README.md#uc-02) · alternativa (sair) — [UC-02 A4.3](../casos-de-uso/UC-02-autenticar.md#a4-3)
  - RF-37: [UC-20](../casos-de-uso/README.md#uc-20) · fluxo principal — [UC-20 passos 1 a 4](../casos-de-uso/fichas-resumidas.md#uc20-p1)
- **US:** [US-01](../historias/US-01-criar-minha-conta.md), [US-02](../historias/US-02-entrar-no-sistema.md), [US-03](../historias/US-03-manter-e-encerrar-a-sessao.md), [US-04](../historias/US-04-consultar-os-espacos.md), [US-05](../historias/US-05-cadastrar-espaco.md), [US-06](../historias/US-06-editar-espaco.md), [US-07](../historias/US-07-desativar-e-reativar-espaco.md), [US-08](../historias/US-08-solicitar-reserva.md), [US-10](../historias/US-10-acompanhar-minhas-reservas.md), [US-11](../historias/US-11-acompanhar-todas-as-reservas.md), [US-12](../historias/US-12-ver-detalhe-e-historico.md), [US-13](../historias/US-13-cancelar-uma-reserva.md), [US-14](../historias/US-14-confirmar-uma-reserva.md), [US-15](../historias/US-15-recusar-uma-reserva.md), [US-16](../historias/US-16-concluir-uma-reserva.md), [US-17](../historias/US-17-criar-o-primeiro-gestor.md)
- **CA que dependem da DEC:** US-01: [CA-06](../historias/US-01-criar-minha-conta.md#us-01-ca-06); US-08: [CA-21](../historias/US-08-solicitar-reserva.md#us-08-ca-21)
- **CA dos RF afetados (regressão):** US-01: [CA-01](../historias/US-01-criar-minha-conta.md#us-01-ca-01), [CA-02](../historias/US-01-criar-minha-conta.md#us-01-ca-02); US-02: [CA-01](../historias/US-02-entrar-no-sistema.md#us-02-ca-01), [CA-02](../historias/US-02-entrar-no-sistema.md#us-02-ca-02), [CA-03](../historias/US-02-entrar-no-sistema.md#us-02-ca-03), [CA-04](../historias/US-02-entrar-no-sistema.md#us-02-ca-04), [CA-07](../historias/US-02-entrar-no-sistema.md#us-02-ca-07); US-03: [CA-01](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-01), [CA-02](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-02), [CA-05](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-05); US-04: [CA-08](../historias/US-04-consultar-os-espacos.md#us-04-ca-08); US-05: [CA-01](../historias/US-05-cadastrar-espaco.md#us-05-ca-01), [CA-03](../historias/US-05-cadastrar-espaco.md#us-05-ca-03), [CA-11](../historias/US-05-cadastrar-espaco.md#us-05-ca-11); US-06: [CA-10](../historias/US-06-editar-espaco.md#us-06-ca-10); US-07: [CA-09](../historias/US-07-desativar-e-reativar-espaco.md#us-07-ca-09); US-08: [CA-01](../historias/US-08-solicitar-reserva.md#us-08-ca-01), [CA-02](../historias/US-08-solicitar-reserva.md#us-08-ca-02), [CA-03](../historias/US-08-solicitar-reserva.md#us-08-ca-03), [CA-05](../historias/US-08-solicitar-reserva.md#us-08-ca-05); US-10: [CA-01](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-01), [CA-04](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-04), [CA-06](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-06), [CA-08](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-08); US-11: [CA-04](../historias/US-11-acompanhar-todas-as-reservas.md#us-11-ca-04), [CA-07](../historias/US-11-acompanhar-todas-as-reservas.md#us-11-ca-07); US-12: [CA-06](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-06), [CA-07](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-07), [CA-10](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-10); US-13: [CA-09](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-09); US-14: [CA-10](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-10), [CA-11](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-11); US-15: [CA-07](../historias/US-15-recusar-uma-reserva.md#us-15-ca-07); US-16: [CA-06](../historias/US-16-concluir-uma-reserva.md#us-16-ca-06); US-17: [CA-01](../historias/US-17-criar-o-primeiro-gestor.md#us-17-ca-01), [CA-02](../historias/US-17-criar-o-primeiro-gestor.md#us-17-ca-02), [CA-03](../historias/US-17-criar-o-primeiro-gestor.md#us-17-ca-03)
- **TA:** [TA-01](../historias/US-01-criar-minha-conta.md#ta-01), [TA-02 (manual)](../historias/US-01-criar-minha-conta.md#ta-02), [TA-06](../historias/US-01-criar-minha-conta.md#ta-06), [TA-07](../historias/US-02-entrar-no-sistema.md#ta-07), [TA-08](../historias/US-02-entrar-no-sistema.md#ta-08), [TA-09](../historias/US-02-entrar-no-sistema.md#ta-09), [TA-10](../historias/US-02-entrar-no-sistema.md#ta-10), [TA-13](../historias/US-02-entrar-no-sistema.md#ta-13), [TA-14](../historias/US-03-manter-e-encerrar-a-sessao.md#ta-14), [TA-15](../historias/US-03-manter-e-encerrar-a-sessao.md#ta-15), [TA-18](../historias/US-03-manter-e-encerrar-a-sessao.md#ta-18), [TA-28](../historias/US-04-consultar-os-espacos.md#ta-28), [TA-29](../historias/US-05-cadastrar-espaco.md#ta-29), [TA-31](../historias/US-05-cadastrar-espaco.md#ta-31), [TA-39](../historias/US-05-cadastrar-espaco.md#ta-39), [TA-49](../historias/US-06-editar-espaco.md#ta-49), [TA-58](../historias/US-07-desativar-e-reativar-espaco.md#ta-58), [TA-59](../historias/US-08-solicitar-reserva.md#ta-59), [TA-60](../historias/US-08-solicitar-reserva.md#ta-60), [TA-61](../historias/US-08-solicitar-reserva.md#ta-61), [TA-63](../historias/US-08-solicitar-reserva.md#ta-63), [TA-79](../historias/US-08-solicitar-reserva.md#ta-79), [TA-90](../historias/US-10-acompanhar-minhas-reservas.md#ta-90), [TA-93](../historias/US-10-acompanhar-minhas-reservas.md#ta-93), [TA-95](../historias/US-10-acompanhar-minhas-reservas.md#ta-95), [TA-97](../historias/US-10-acompanhar-minhas-reservas.md#ta-97), [TA-101](../historias/US-11-acompanhar-todas-as-reservas.md#ta-101), [TA-104](../historias/US-11-acompanhar-todas-as-reservas.md#ta-104), [TA-110](../historias/US-12-ver-detalhe-e-historico.md#ta-110), [TA-111](../historias/US-12-ver-detalhe-e-historico.md#ta-111), [TA-114](../historias/US-12-ver-detalhe-e-historico.md#ta-114), [TA-123](../historias/US-13-cancelar-uma-reserva.md#ta-123), [TA-133](../historias/US-14-confirmar-uma-reserva.md#ta-133), [TA-134](../historias/US-14-confirmar-uma-reserva.md#ta-134), [TA-141](../historias/US-15-recusar-uma-reserva.md#ta-141), [TA-147](../historias/US-16-concluir-uma-reserva.md#ta-147), [TA-148](../historias/US-17-criar-o-primeiro-gestor.md#ta-148), [TA-149](../historias/US-17-criar-o-primeiro-gestor.md#ta-149), [TA-150 (manual)](../historias/US-17-criar-o-primeiro-gestor.md#ta-150)
- **Endpoint ou tela:** `POST /api/espacos/`; `/espacos`; `PATCH /api/espacos/{id}/`; `POST /api/espacos/{id}/desativar/`; `POST /api/espacos/{id}/ativar/`; `POST /api/reservas/`; `/reservas/nova`; `GET /api/reservas/`; `/reservas`; `GET /api/reservas/{id}/`; `/reservas/:reservaId`; `PATCH /api/reservas/{id}/situacao/`; `GET /api/reservas/{id}/historico/`; `POST /api/auth/cadastro/`; `/cadastro`; `POST /api/auth/login/`; `/entrar`; `POST /api/auth/refresh/`; `/`; `/admin/`; `comando createsuperuser`
- **Código:** `espacos/application/casos_de_uso.py::CadastrarEspaco.executar`, `espacos/domain/espaco_esportivo.py::EspacoEsportivo`, `compartilhado/api/permissoes.py::ApenasGestor`, `espacos/api/views.py::_ViewComMetodosDoGestor.get_permissions`, `reservas/application/casos_de_uso.py::CriarReserva.executar`, `reservas/domain/reserva.py::Reserva.solicitar`, `reservas/application/casos_de_uso.py::ConsultarReservas.executar`, `reservas/domain/reserva.py::Reserva.visivel_para`, `reservas/application/casos_de_uso.py::_obter_ou_falhar`, `reservas/domain/excecoes.py::ReservaNaoEncontrada`, `reservas/domain/reserva.py::Reserva.alterar_situacao`, `reservas/domain/situacao.py::papel_pode_levar_a`, `reservas/domain/excecoes.py::AlteracaoDeSituacaoNaoPermitida`, `contas/application/casos_de_uso.py::CadastrarSolicitante.executar`, `contas/domain/cadastro.py::DadosDeCadastro`, `contas/api/views.py::LoginView.post`, `contas/api/views.py::RenovarTokenView.post`, `contas/api/views.py::_refresh_de_usuario_ativo`, `components/sessao/SessaoProvider.tsx::SessaoProvider`, `api/sessao.ts::limparSessao`, `contas/infrastructure/models.py::UsuarioManager.create_superuser`

## <a id="dec-05"></a>DEC-05 · Histórico só com mudanças efetivas

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-05.md)) |
| **Pergunta** | Uma tentativa recusada de mudar a situação de uma reserva (perfil sem permissão, transição não permitida, motivo ausente) precisa ficar registrada? Se sim, onde e quem a consulta? |
| **Opção adotada** | Toda tentativa recusada de mudar a situação de uma reserva visível ao ator fica no histórico dessa reserva, com ator, momento, situação pedida, resultado e código do erro, sem mudar a situação. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor. |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 10 TAs a rever (0 manuais), de 10 CAs em 6 histórias: 6 CAs dependem diretamente da DEC e 4 verificam os RF afetados |

- **RF:** [RF-22](matriz.md#rf-22)
- **RNF:** [RNF-R02](../requisitos/rnf.md#rnf-r02)
- **UC (passo, alternativa ou exceção):**
  - RF-22: [UC-09](../casos-de-uso/README.md#uc-09) · fluxo principal (UC-13 grava o que UC-09 mostra) — [UC-09 passo 3](../casos-de-uso/fichas-resumidas.md#uc09-p3), [UC-04 passo 10](../casos-de-uso/UC-04-solicitar-reserva.md#p10), [UC-10 passo 7](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p7)
- **US:** [US-08](../historias/US-08-solicitar-reserva.md), [US-12](../historias/US-12-ver-detalhe-e-historico.md), [US-13](../historias/US-13-cancelar-uma-reserva.md), [US-14](../historias/US-14-confirmar-uma-reserva.md), [US-15](../historias/US-15-recusar-uma-reserva.md), [US-16](../historias/US-16-concluir-uma-reserva.md)
- **CA que dependem da DEC:** US-08: [CA-20](../historias/US-08-solicitar-reserva.md#us-08-ca-20); US-12: [CA-09](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-09); US-13: [CA-08](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-08); US-14: [CA-09](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-09); US-15: [CA-06](../historias/US-15-recusar-uma-reserva.md#us-15-ca-06); US-16: [CA-05](../historias/US-16-concluir-uma-reserva.md#us-16-ca-05)
- **CA dos RF afetados (regressão):** US-12: [CA-02](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-02), [CA-03](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-03), [CA-05](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-05), [CA-08](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-08)
- **TA:** [TA-78](../historias/US-08-solicitar-reserva.md#ta-78), [TA-106](../historias/US-12-ver-detalhe-e-historico.md#ta-106), [TA-107](../historias/US-12-ver-detalhe-e-historico.md#ta-107), [TA-109](../historias/US-12-ver-detalhe-e-historico.md#ta-109), [TA-112](../historias/US-12-ver-detalhe-e-historico.md#ta-112), [TA-113](../historias/US-12-ver-detalhe-e-historico.md#ta-113), [TA-122](../historias/US-13-cancelar-uma-reserva.md#ta-122), [TA-132](../historias/US-14-confirmar-uma-reserva.md#ta-132), [TA-140](../historias/US-15-recusar-uma-reserva.md#ta-140), [TA-146](../historias/US-16-concluir-uma-reserva.md#ta-146)
- **Endpoint ou tela:** `GET /api/reservas/{id}/historico/`; `/reservas/:reservaId`
- **Código:** `reservas/application/casos_de_uso.py::ConsultarHistoricoDaReserva.executar`, `reservas/domain/registro_de_situacao.py::RegistroDeSituacao`, `reservas/infrastructure/repositorio_django.py::RepositorioReservasDjango.salvar`

## <a id="dec-06"></a>DEC-06 · Reservas de um espaço desativado

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-06.md)) |
| **Pergunta** | Um espaço pode ser excluído? Quando o gestor desativa um espaço, o que acontece com as reservas que ele já tem? |
| **Opção adotada** | **a)** Espaço nunca é excluído, só desativado. Desativar impede **novos** pedidos ([espaço inativo](../glossario.md#espaco-inativo)). As reservas existentes continuam valendo, com as mesmas ações; o gestor cancela, uma a uma, as que precisar. Reativar volta a aceitar pedidos. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor como representante do cliente (premissa P-01). |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 14 TAs a rever (0 manuais), de 14 CAs em 4 histórias: 4 CAs dependem diretamente da DEC e 10 verificam os RF afetados |

- **RF:** [RF-06](matriz.md#rf-06), [RF-07](matriz.md#rf-07), [RF-08](matriz.md#rf-08), [RF-11.3](matriz.md#rf-11-3), [RF-20](matriz.md#rf-20)
- **RNF:** [RNF-R05](../requisitos/rnf.md#rnf-r05)
- **UC (passo, alternativa ou exceção):**
  - RF-06: [UC-15](../casos-de-uso/README.md#uc-15) · fluxo principal — [UC-15 passos 1 a 5](../casos-de-uso/fichas-resumidas.md#uc15-p1)
  - RF-07: [UC-16](../casos-de-uso/README.md#uc-16) · fluxo principal (desativar) — [UC-16 passos 1 a 5](../casos-de-uso/fichas-resumidas.md#uc16-p1)
  - RF-08: [UC-16](../casos-de-uso/README.md#uc-16) · alternativa (reativar) — [UC-16 A1.1](../casos-de-uso/fichas-resumidas.md#uc16-a1-1)
  - RF-11.3: [UC-05](../casos-de-uso/README.md#uc-05) · exceção — [UC-04 E8.1](../casos-de-uso/UC-04-solicitar-reserva.md#e8-1), [E8.2](../casos-de-uso/UC-04-solicitar-reserva.md#e8-2)
  - RF-20: [UC-11](../casos-de-uso/README.md#uc-11) · fluxo principal (pelo Gestor) — [UC-10 passos 1 a 8, variação UC-11](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-11)
- **US:** [US-06](../historias/US-06-editar-espaco.md), [US-07](../historias/US-07-desativar-e-reativar-espaco.md), [US-08](../historias/US-08-solicitar-reserva.md), [US-13](../historias/US-13-cancelar-uma-reserva.md)
- **CA que dependem da DEC:** US-07: [CA-01](../historias/US-07-desativar-e-reativar-espaco.md#us-07-ca-01), [CA-04](../historias/US-07-desativar-e-reativar-espaco.md#us-07-ca-04); US-08: [CA-17](../historias/US-08-solicitar-reserva.md#us-08-ca-17); US-13: [CA-02](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-02)
- **CA dos RF afetados (regressão):** US-06: [CA-01](../historias/US-06-editar-espaco.md#us-06-ca-01), [CA-02](../historias/US-06-editar-espaco.md#us-06-ca-02), [CA-03](../historias/US-06-editar-espaco.md#us-06-ca-03), [CA-09](../historias/US-06-editar-espaco.md#us-06-ca-09); US-07: [CA-02](../historias/US-07-desativar-e-reativar-espaco.md#us-07-ca-02), [CA-03](../historias/US-07-desativar-e-reativar-espaco.md#us-07-ca-03), [CA-08](../historias/US-07-desativar-e-reativar-espaco.md#us-07-ca-08); US-08: [CA-06](../historias/US-08-solicitar-reserva.md#us-08-ca-06), [CA-16](../historias/US-08-solicitar-reserva.md#us-08-ca-16); US-13: [CA-03](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-03)
- **TA:** [TA-40](../historias/US-06-editar-espaco.md#ta-40), [TA-41](../historias/US-06-editar-espaco.md#ta-41), [TA-42](../historias/US-06-editar-espaco.md#ta-42), [TA-48](../historias/US-06-editar-espaco.md#ta-48), [TA-50](../historias/US-07-desativar-e-reativar-espaco.md#ta-50), [TA-51](../historias/US-07-desativar-e-reativar-espaco.md#ta-51), [TA-52](../historias/US-07-desativar-e-reativar-espaco.md#ta-52), [TA-53](../historias/US-07-desativar-e-reativar-espaco.md#ta-53), [TA-57](../historias/US-07-desativar-e-reativar-espaco.md#ta-57), [TA-64](../historias/US-08-solicitar-reserva.md#ta-64), [TA-74](../historias/US-08-solicitar-reserva.md#ta-74), [TA-75](../historias/US-08-solicitar-reserva.md#ta-75), [TA-116](../historias/US-13-cancelar-uma-reserva.md#ta-116), [TA-117](../historias/US-13-cancelar-uma-reserva.md#ta-117)
- **Endpoint ou tela:** `PATCH /api/espacos/{id}/`; `/espacos`; `POST /api/espacos/{id}/desativar/`; `POST /api/espacos/{id}/ativar/`; `POST /api/reservas/`; `/reservas/nova`; `PATCH /api/reservas/{id}/situacao/`
- **Código:** `espacos/application/casos_de_uso.py::EditarEspaco.executar`, `espacos/domain/espaco_esportivo.py::EspacoEsportivo.alterar_dados`, `espacos/infrastructure/repositorio_django.py::RepositorioEspacosDjango.salvar`, `espacos/application/casos_de_uso.py::DesativarEspaco.executar`, `espacos/domain/espaco_esportivo.py::EspacoEsportivo.desativar`, `espacos/application/casos_de_uso.py::AtivarEspaco.executar`, `espacos/domain/espaco_esportivo.py::EspacoEsportivo.ativar`, `reservas/application/casos_de_uso.py::CriarReserva.executar`, `reservas/application/portas.py::ConsultaDeEspacos.obter_espaco_reservavel`, `espacos/publico.py::verificar_espaco_disponivel`, `espacos/domain/espaco_esportivo.py::EspacoEsportivo.garantir_que_esta_ativo`, `reservas/application/casos_de_uso.py::AlterarSituacaoReserva.executar`, `reservas/domain/reserva.py::Reserva.alterar_situacao`, `reservas/domain/situacao.py::SITUACOES_QUE_EXIGEM_MOTIVO`

## <a id="dec-07"></a>DEC-07 · Valores das regras de agenda

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-07.md)) |
| **Pergunta** | Em que período do dia os espaços podem ser usados, qual a duração mínima e máxima de uma reserva e com quantos dias de antecedência se pode pedir? Esses limites são os mesmos para todos os espaços e todos os dias? |
| **Opção adotada** | Cada espaço tem o próprio horário de funcionamento, com padrão das 07:00 às 00:00 (o término à meia-noite é o fim do dia da reserva); o pedido sugere 1 hora de duração; a duração mínima (30 minutos), a máxima (3 horas) e a antecedência máxima (30 dias) continuam iguais para todos. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor como representante do cliente. |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 10 TAs a rever (0 manuais), de 10 CAs em 2 histórias: 5 CAs dependem diretamente da DEC e 5 verificam os RF afetados |

- **RF:** [RF-11.5](matriz.md#rf-11-5), [RF-28](matriz.md#rf-28), [RF-30](matriz.md#rf-30), [RF-31](matriz.md#rf-31)
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):**
  - RF-11.5: [UC-05](../casos-de-uso/README.md#uc-05) · exceção — [UC-04 E6.1](../casos-de-uso/UC-04-solicitar-reserva.md#e6-1), [E6.2](../casos-de-uso/UC-04-solicitar-reserva.md#e6-2), [E6.3](../casos-de-uso/UC-04-solicitar-reserva.md#e6-3)
  - RF-28: [UC-04](../casos-de-uso/README.md#uc-04) · fluxo principal (as regras aparecem no pedido) — [UC-04 passo 2](../casos-de-uso/UC-04-solicitar-reserva.md#p2), [A2.1](../casos-de-uso/UC-04-solicitar-reserva.md#a2-1), [UC-06 passo 5](../casos-de-uso/fichas-resumidas.md#uc06-p5)
  - RF-30: [UC-06](../casos-de-uso/README.md#uc-06) · fluxo principal — [UC-06 passos 4 e 5](../casos-de-uso/fichas-resumidas.md#uc06-p4), [UC-04 A3.1](../casos-de-uso/UC-04-solicitar-reserva.md#a3-1)
  - RF-31: [UC-06](../casos-de-uso/README.md#uc-06) · alternativa (data que não é reservável) — [UC-06 A4.1](../casos-de-uso/fichas-resumidas.md#uc06-a4-1), [UC-04 A3.1](../casos-de-uso/UC-04-solicitar-reserva.md#a3-1)
- **US:** [US-08](../historias/US-08-solicitar-reserva.md), [US-09](../historias/US-09-ver-a-agenda-do-dia.md)
- **CA que dependem da DEC:** US-08: [CA-02](../historias/US-08-solicitar-reserva.md#us-08-ca-02), [CA-10](../historias/US-08-solicitar-reserva.md#us-08-ca-10), [CA-11](../historias/US-08-solicitar-reserva.md#us-08-ca-11), [CA-12](../historias/US-08-solicitar-reserva.md#us-08-ca-12); US-09: [CA-05](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-05)
- **CA dos RF afetados (regressão):** US-08: [CA-04](../historias/US-08-solicitar-reserva.md#us-08-ca-04), [CA-13](../historias/US-08-solicitar-reserva.md#us-08-ca-13); US-09: [CA-01](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-01), [CA-02](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-02), [CA-03](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-03)
- **TA:** [TA-60](../historias/US-08-solicitar-reserva.md#ta-60), [TA-62](../historias/US-08-solicitar-reserva.md#ta-62), [TA-68](../historias/US-08-solicitar-reserva.md#ta-68), [TA-69](../historias/US-08-solicitar-reserva.md#ta-69), [TA-70](../historias/US-08-solicitar-reserva.md#ta-70), [TA-71](../historias/US-08-solicitar-reserva.md#ta-71), [TA-80](../historias/US-09-ver-a-agenda-do-dia.md#ta-80), [TA-81](../historias/US-09-ver-a-agenda-do-dia.md#ta-81), [TA-82](../historias/US-09-ver-a-agenda-do-dia.md#ta-82), [TA-84](../historias/US-09-ver-a-agenda-do-dia.md#ta-84)
- **Endpoint ou tela:** `POST /api/reservas/`; `/reservas/nova`; `GET /api/reservas/regras-de-agenda/`; `GET /api/reservas/ocupacao/`
- **Código:** `reservas/domain/regras_de_agenda.py::garantir_regras_de_agenda`, `reservas/domain/reserva.py::Reserva.solicitar`, `reservas/domain/regras_de_agenda.py::data_limite_para_reservar`, `reservas/domain/regras_de_agenda.py::HORARIO_DE_ABERTURA`, `reservas/api/serializers.py::RegrasDeAgendaSaidaSerializer.vigentes`, `reservas/domain/regras_de_agenda.py::horarios_livres`, `reservas/application/casos_de_uso.py::ConsultarOcupacaoDoDia.executar`, `reservas/domain/regras_de_agenda.py::garantir_data_reservavel`, `reservas/domain/regras_de_agenda.py::motivo_de_indisponibilidade`

## <a id="dec-08"></a>DEC-08 · Cobertura-alvo dos testes

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-08.md)) |
| **Pergunta** | Que meta de qualidade dos testes o grupo adota, já que a disciplina de Projeto de Programação não exige testes automatizados nem cobertura? |
| **Opção adotada** | 100% de linhas e ramos nas camadas `domain` e `application` de `espacos` e `reservas`; no mínimo 99% no total (`fail_under`). Antes da entrega: testes por propriedade no perfil `exaustivo` e testes de mutação sem mutante sobrevivente sem justificativa. |
| **Responsável** | Max Zimmermann dos Reis (grupo). Decisão interna; não depende do professor. |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 0 TAs a rever (0 manuais), de 0 CAs em 0 histórias: 0 CAs dependem diretamente da DEC e 0 verificam os RF afetados |

- **RF:** nenhum
- **RNF:** [RNF-S03](../requisitos/rnf.md#rnf-s03)
- **UC (passo, alternativa ou exceção):** nenhum
- **US:** —
- **CA que dependem da DEC:** —
- **CA dos RF afetados (regressão):** —
- **TA:** —
- **Endpoint ou tela:** nenhum
- **Código:** nenhum

## <a id="dec-09"></a>DEC-09 · Formato da matrícula

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-09.md)) |
| **Pergunta** | Qual é o formato da matrícula na instituição (quantidade de caracteres, só dígitos, prefixo)? Ela precisa ser conferida com o cadastro acadêmico? |
| **Opção adotada** | A matrícula é obrigatória, única e formada só por dígitos, sem quantidade mínima ou máxima definida pela instituição; o limite de 20 caracteres continua apenas como limite técnico do armazenamento. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor. |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 5 TAs a rever (1 manuais), de 5 CAs em 2 histórias: 1 CAs dependem diretamente da DEC e 4 verificam os RF afetados |

- **RF:** [RF-32](matriz.md#rf-32), [RF-32.1](matriz.md#rf-32-1)
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):**
  - RF-32: [UC-01](../casos-de-uso/README.md#uc-01) · fluxo principal — [UC-01 passos 1 a 4](../casos-de-uso/fichas-resumidas.md#uc01-p1)
  - RF-32.1: [UC-01](../casos-de-uso/README.md#uc-01) · exceção — [UC-01 E3.1](../casos-de-uso/fichas-resumidas.md#uc01-e3-1)
- **US:** [US-01](../historias/US-01-criar-minha-conta.md), [US-02](../historias/US-02-entrar-no-sistema.md)
- **CA que dependem da DEC:** US-01: [CA-03](../historias/US-01-criar-minha-conta.md#us-01-ca-03)
- **CA dos RF afetados (regressão):** US-01: [CA-01](../historias/US-01-criar-minha-conta.md#us-01-ca-01), [CA-02](../historias/US-01-criar-minha-conta.md#us-01-ca-02), [CA-06](../historias/US-01-criar-minha-conta.md#us-01-ca-06); US-02: [CA-03](../historias/US-02-entrar-no-sistema.md#us-02-ca-03)
- **TA:** [TA-01](../historias/US-01-criar-minha-conta.md#ta-01), [TA-02 (manual)](../historias/US-01-criar-minha-conta.md#ta-02), [TA-03](../historias/US-01-criar-minha-conta.md#ta-03), [TA-06](../historias/US-01-criar-minha-conta.md#ta-06), [TA-09](../historias/US-02-entrar-no-sistema.md#ta-09)
- **Endpoint ou tela:** `POST /api/auth/cadastro/`; `/cadastro`
- **Código:** `contas/application/casos_de_uso.py::CadastrarSolicitante.executar`, `contas/domain/cadastro.py::DadosDeCadastro`, `contas/domain/excecoes.py::MatriculaInvalida`

## <a id="dec-10"></a>DEC-10 · Nome de espaço único

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-10.md)) |
| **Pergunta** | Dois espaços esportivos podem ter o mesmo nome? Se não, "Ginásio A" e "ginásio a" contam como o mesmo nome? |
| **Opção adotada** | O nome é único sem diferenciar maiúsculas de minúsculas, comparado depois de removidos os espaços das pontas e os repetidos. Cadastrar ou renomear para um nome já usado é recusado. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor como representante do cliente. |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 6 TAs a rever (0 manuais), de 6 CAs em 2 histórias: 3 CAs dependem diretamente da DEC e 3 verificam os RF afetados |

- **RF:** [RF-05.2](matriz.md#rf-05-2), [RF-06.2](matriz.md#rf-06-2)
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):**
  - RF-05.2: [UC-14](../casos-de-uso/README.md#uc-14) · exceção — [UC-14 E6.1](../casos-de-uso/UC-14-cadastrar-espaco.md#e6-1), [UC-14 E7.1](../casos-de-uso/UC-14-cadastrar-espaco.md#e7-1), [UC-15 E4.5](../casos-de-uso/fichas-resumidas.md#uc15-e4-5)
  - RF-06.2: [UC-15](../casos-de-uso/README.md#uc-15) · exceção — [UC-15 E4.1](../casos-de-uso/fichas-resumidas.md#uc15-e4-1), [UC-15 E4.4](../casos-de-uso/fichas-resumidas.md#uc15-e4-4)
- **US:** [US-05](../historias/US-05-cadastrar-espaco.md), [US-06](../historias/US-06-editar-espaco.md)
- **CA que dependem da DEC:** US-05: [CA-09](../historias/US-05-cadastrar-espaco.md#us-05-ca-09), [CA-10](../historias/US-05-cadastrar-espaco.md#us-05-ca-10); US-06: [CA-08](../historias/US-06-editar-espaco.md#us-06-ca-08)
- **CA dos RF afetados (regressão):** US-06: [CA-02](../historias/US-06-editar-espaco.md#us-06-ca-02), [CA-04](../historias/US-06-editar-espaco.md#us-06-ca-04), [CA-07](../historias/US-06-editar-espaco.md#us-06-ca-07)
- **TA:** [TA-37](../historias/US-05-cadastrar-espaco.md#ta-37), [TA-38](../historias/US-05-cadastrar-espaco.md#ta-38), [TA-41](../historias/US-06-editar-espaco.md#ta-41), [TA-43](../historias/US-06-editar-espaco.md#ta-43), [TA-46](../historias/US-06-editar-espaco.md#ta-46), [TA-47](../historias/US-06-editar-espaco.md#ta-47)
- **Endpoint ou tela:** `POST /api/espacos/`; `/espacos`; `PATCH /api/espacos/{id}/`
- **Código:** `espacos/application/casos_de_uso.py::CadastrarEspaco.executar`, `espacos/application/repositorio.py::RepositorioEspacos.existe_com_nome`, `espacos/infrastructure/models.py::EspacoEsportivoModel`, `espacos/infrastructure/repositorio_django.py::RepositorioEspacosDjango.salvar`, `espacos/domain/espaco_esportivo.py::EspacoEsportivo.alterar_dados`, `espacos/application/casos_de_uso.py::EditarEspaco.executar`

## <a id="dec-11"></a>DEC-11 · Períodos ocupados por outras pessoas na agenda do dia

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-11.md)) |
| **Pergunta** | Um Solicitante pode ver, antes de pedir, os períodos de um espaço já ocupados por reservas de outras pessoas? Com quais dados? |
| **Opção adotada** | **a)** Sim. A [agenda do dia](../glossario.md#agenda-do-dia) mostra a qualquer usuário identificado o início, o término e a situação de cada [horário ocupado](../glossario.md#horario-ocupado), nunca quem pediu, a finalidade nem o motivo. Fora da agenda, a reserva de outra pessoa continua inexistente para o Solicitante. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor como representante do cliente. |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 5 TAs a rever (0 manuais), de 5 CAs em 1 histórias: 2 CAs dependem diretamente da DEC e 3 verificam os RF afetados |

- **RF:** [RF-29](matriz.md#rf-29)
- **RNF:** [RNF-F06](../requisitos/rnf.md#rnf-f06)
- **UC (passo, alternativa ou exceção):**
  - RF-29: [UC-06](../casos-de-uso/README.md#uc-06) · fluxo principal — [UC-06 passo 3](../casos-de-uso/fichas-resumidas.md#uc06-p3), [UC-04 A3.1](../casos-de-uso/UC-04-solicitar-reserva.md#a3-1)
- **US:** [US-09](../historias/US-09-ver-a-agenda-do-dia.md)
- **CA que dependem da DEC:** US-09: [CA-01](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-01), [CA-10](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-10)
- **CA dos RF afetados (regressão):** US-09: [CA-04](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-04), [CA-06](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-06), [CA-09](../historias/US-09-ver-a-agenda-do-dia.md#us-09-ca-09)
- **TA:** [TA-80](../historias/US-09-ver-a-agenda-do-dia.md#ta-80), [TA-83](../historias/US-09-ver-a-agenda-do-dia.md#ta-83), [TA-85](../historias/US-09-ver-a-agenda-do-dia.md#ta-85), [TA-88](../historias/US-09-ver-a-agenda-do-dia.md#ta-88), [TA-89](../historias/US-09-ver-a-agenda-do-dia.md#ta-89)
- **Endpoint ou tela:** `GET /api/reservas/ocupacao/`; `/reservas/nova`
- **Código:** `reservas/application/casos_de_uso.py::ConsultarOcupacaoDoDia.executar`, `reservas/application/ocupacao_do_dia.py::OcupacaoDoDia`

## <a id="dec-12"></a>DEC-12 · Metas de desempenho

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-12.md)) |
| **Pergunta** | Em quanto tempo a consulta de reservas e a agenda do dia precisam responder, e com quantas reservas cadastradas essa meta vale? |
| **Opção adotada** | Com **1.000 reservas** cadastradas: a consulta de reservas responde em até **1 s** no percentil 95 (inclusive a lista do Gestor sem critério, com todas as reservas na resposta); a agenda do dia responde em até **500 ms** no percentil 95. Medido dentro do ambiente de execução local (container do backend, com o banco no container ao lado), sem contar a rede nem o navegador. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor como representante do cliente. |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 0 TAs a rever (0 manuais), de 0 CAs em 0 histórias: 0 CAs dependem diretamente da DEC e 0 verificam os RF afetados |

- **RF:** nenhum
- **RNF:** [RNF-P01](../requisitos/rnf.md#rnf-p01), [RNF-P02](../requisitos/rnf.md#rnf-p02)
- **UC (passo, alternativa ou exceção):** nenhum
- **US:** —
- **CA que dependem da DEC:** —
- **CA dos RF afetados (regressão):** —
- **TA:** —
- **Endpoint ou tela:** nenhum
- **Código:** nenhum

## <a id="dec-13"></a>DEC-13 · Mudança de situação em relação ao horário da reserva

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-13.md)) |
| **Pergunta** | A mudança de situação deve depender do horário da reserva? Em especial: (1) o Gestor pode [concluir](../glossario.md#concluida) uma reserva cujo término ainda não chegou? (2) pode [confirmar](../glossario.md#confirmada) ou [recusar](../glossario.md#recusada) uma reserva cujo início já passou? (3) o Solicitante ou o Gestor podem [cancelar](../glossario.md#cancelada) depois do início? (4) o que acontece com uma reserva [Solicitada](../glossario.md#solicitada) que ninguém decidiu até a data dela passar? |
| **Opção adotada** | O Gestor só conclui uma reserva a partir do término dela e só recusa ou cancela uma reserva antes do início dela; confirmar, o cancelamento pelo Solicitante e a ocupação do horário pela Solicitada não decidida não dependem do horário. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor como representante do cliente. |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 21 TAs a rever (0 manuais), de 21 CAs em 9 histórias: 5 CAs dependem diretamente da DEC e 16 verificam os RF afetados |

- **RF:** [RF-16](matriz.md#rf-16), [RF-17](matriz.md#rf-17), [RF-18](matriz.md#rf-18), [RF-19](matriz.md#rf-19), [RF-20](matriz.md#rf-20), [RF-21](matriz.md#rf-21)
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):**
  - RF-16: [UC-07](../casos-de-uso/README.md#uc-07) · fluxo principal — [UC-07 passo 2](../casos-de-uso/fichas-resumidas.md#uc07-p2), [UC-08 passo 3](../casos-de-uso/fichas-resumidas.md#uc08-p3), [UC-10 passo 2](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p2)
  - RF-17: [UC-17](../casos-de-uso/README.md#uc-17) · fluxo principal — [UC-10 passos 1 a 8, variação UC-17](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-17)
  - RF-18: [UC-18](../casos-de-uso/README.md#uc-18) · fluxo principal — [UC-10 passos 1 a 8, variação UC-18](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-18)
  - RF-19: [UC-19](../casos-de-uso/README.md#uc-19) · fluxo principal — [UC-10 passos 1 a 8, variação UC-19](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-19)
  - RF-20: [UC-11](../casos-de-uso/README.md#uc-11) · fluxo principal (pelo Gestor) — [UC-10 passos 1 a 8, variação UC-11](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-11)
  - RF-21: [UC-11](../casos-de-uso/README.md#uc-11) · fluxo principal (pelo Solicitante, na própria) — [UC-10 passos 1 a 8, variação UC-11](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#v-uc-11)
- **US:** [US-07](../historias/US-07-desativar-e-reativar-espaco.md), [US-08](../historias/US-08-solicitar-reserva.md), [US-10](../historias/US-10-acompanhar-minhas-reservas.md), [US-11](../historias/US-11-acompanhar-todas-as-reservas.md), [US-12](../historias/US-12-ver-detalhe-e-historico.md), [US-13](../historias/US-13-cancelar-uma-reserva.md), [US-14](../historias/US-14-confirmar-uma-reserva.md), [US-15](../historias/US-15-recusar-uma-reserva.md), [US-16](../historias/US-16-concluir-uma-reserva.md)
- **CA que dependem da DEC:** US-08: [CA-18](../historias/US-08-solicitar-reserva.md#us-08-ca-18); US-13: [CA-01](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-01); US-14: [CA-01](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-01); US-15: [CA-01](../historias/US-15-recusar-uma-reserva.md#us-15-ca-01); US-16: [CA-01](../historias/US-16-concluir-uma-reserva.md#us-16-ca-01)
- **CA dos RF afetados (regressão):** US-07: [CA-04](../historias/US-07-desativar-e-reativar-espaco.md#us-07-ca-04); US-10: [CA-02](../historias/US-10-acompanhar-minhas-reservas.md#us-10-ca-02); US-11: [CA-03](../historias/US-11-acompanhar-todas-as-reservas.md#us-11-ca-03); US-12: [CA-01](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-01), [CA-03](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-03); US-13: [CA-02](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-02), [CA-03](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-03), [CA-04](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-04), [CA-07](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-07); US-14: [CA-02](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-02), [CA-03](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-03), [CA-07](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-07), [CA-08](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-08); US-15: [CA-02](../historias/US-15-recusar-uma-reserva.md#us-15-ca-02); US-16: [CA-02](../historias/US-16-concluir-uma-reserva.md#us-16-ca-02), [CA-03](../historias/US-16-concluir-uma-reserva.md#us-16-ca-03)
- **TA:** [TA-53](../historias/US-07-desativar-e-reativar-espaco.md#ta-53), [TA-76](../historias/US-08-solicitar-reserva.md#ta-76), [TA-91](../historias/US-10-acompanhar-minhas-reservas.md#ta-91), [TA-100](../historias/US-11-acompanhar-todas-as-reservas.md#ta-100), [TA-105](../historias/US-12-ver-detalhe-e-historico.md#ta-105), [TA-107](../historias/US-12-ver-detalhe-e-historico.md#ta-107), [TA-115](../historias/US-13-cancelar-uma-reserva.md#ta-115), [TA-116](../historias/US-13-cancelar-uma-reserva.md#ta-116), [TA-117](../historias/US-13-cancelar-uma-reserva.md#ta-117), [TA-118](../historias/US-13-cancelar-uma-reserva.md#ta-118), [TA-121](../historias/US-13-cancelar-uma-reserva.md#ta-121), [TA-124](../historias/US-14-confirmar-uma-reserva.md#ta-124), [TA-125](../historias/US-14-confirmar-uma-reserva.md#ta-125), [TA-126](../historias/US-14-confirmar-uma-reserva.md#ta-126), [TA-130](../historias/US-14-confirmar-uma-reserva.md#ta-130), [TA-131](../historias/US-14-confirmar-uma-reserva.md#ta-131), [TA-135](../historias/US-15-recusar-uma-reserva.md#ta-135), [TA-136](../historias/US-15-recusar-uma-reserva.md#ta-136), [TA-142](../historias/US-16-concluir-uma-reserva.md#ta-142), [TA-143](../historias/US-16-concluir-uma-reserva.md#ta-143), [TA-144](../historias/US-16-concluir-uma-reserva.md#ta-144)
- **Endpoint ou tela:** `GET /api/reservas/`; `GET /api/reservas/{id}/`; `/reservas`; `/reservas/:reservaId`; `PATCH /api/reservas/{id}/situacao/`
- **Código:** `reservas/domain/reserva.py::Reserva.acoes_permitidas_para`, `reservas/domain/situacao.py::transicoes_a_partir_de`, `reservas/api/serializers.py::ReservaSaidaSerializer.get_acoes_disponiveis`, `reservas/application/casos_de_uso.py::AlterarSituacaoReserva.executar`, `reservas/domain/reserva.py::Reserva.alterar_situacao`, `reservas/domain/situacao.py::SITUACOES_QUE_EXIGEM_MOTIVO`, `reservas/domain/situacao.py::DESTINOS_POR_PAPEL`

## <a id="dec-14"></a>DEC-14 · Alternativas e exceções nos casos de uso

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-14.md)) |
| **Pergunta** | Nas fichas de caso de uso, as exceções são numeradas com `E` (como sugere A3·s12: `A3` / `E5`) ou tudo fica como `A` (como A3·s15 numera uma exceção, `A2.2`)? |
| **Opção adotada** | Alternativas numeradas com `A` e exceções com `E`, ligadas ao passo (`A3.1`, `E9.1`), como nas fichas de caso de uso desde a REQ-04 ([decisão i](../casos-de-uso/README.md#decisao-i)). Nada muda. |
| **Responsável** | Professor (resposta); grupo (decisão). |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 0 TAs a rever (0 manuais), de 0 CAs em 0 histórias: 0 CAs dependem diretamente da DEC e 0 verificam os RF afetados |

- **RF:** nenhum
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):** nenhum
- **US:** —
- **CA que dependem da DEC:** —
- **CA dos RF afetados (regressão):** —
- **TA:** —
- **Endpoint ou tela:** nenhum
- **Código:** nenhum

## <a id="dec-15"></a>DEC-15 · Critérios de aceite em Dado/Quando/Então

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-15.md)) |
| **Pergunta** | O formato Dado/Quando/Então dos critérios de aceite atende à disciplina de Requisitos? |
| **Opção adotada** | Os critérios de aceite são escritos em Dado/Quando/Então, como os 156 CAs das [histórias](../historias/README.md). Nada muda. |
| **Responsável** | Professor (resposta); grupo (decisão). |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 0 TAs a rever (0 manuais), de 0 CAs em 0 histórias: 0 CAs dependem diretamente da DEC e 0 verificam os RF afetados |

- **RF:** nenhum
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):** nenhum
- **US:** —
- **CA que dependem da DEC:** —
- **CA dos RF afetados (regressão):** —
- **TA:** —
- **Endpoint ou tela:** nenhum
- **Código:** nenhum

## <a id="dec-16"></a>DEC-16 · Rastreabilidade até o código

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-16.md)) |
| **Pergunta** | Os slides param em CA/TA. A rastreabilidade deve ir também até a implementação (endpoint ou tela e código)? |
| **Opção adotada** | A rastreabilidade vai até o endpoint ou a tela e o código, como colunas complementares da [matriz](README.md#decisao-b), geradas dos campos Evidência (complementar) e Código (complementar) das fichas de RF. Nada muda. |
| **Responsável** | Professor (resposta); grupo (decisão). |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 0 TAs a rever (0 manuais), de 0 CAs em 0 histórias: 0 CAs dependem diretamente da DEC e 0 verificam os RF afetados |

- **RF:** nenhum
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):** nenhum
- **US:** —
- **CA que dependem da DEC:** —
- **CA dos RF afetados (regressão):** —
- **TA:** —
- **Endpoint ou tela:** nenhum
- **Código:** nenhum

## <a id="dec-17"></a>DEC-17 · Convenção de versão dos documentos

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-17.md)) |
| **Pergunta** | O professor diz que 0.1 → 0.2 → 1.0 → 1.1 "não é regra universal" (A4·s15). O grupo adota essa convenção ou define a sua? |
| **Opção adotada** | 0.1 Rascunho → 0.2 Em revisão → 1.0 Aprovado (primeira baseline) → 1.1, 1.2… (baselines seguintes, cada uma por um CR aprovado), como no [README da fonte oficial](../README.md#versão-e-estado). Nada muda. |
| **Responsável** | Professor (resposta); grupo (decisão). |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 0 TAs a rever (0 manuais), de 0 CAs em 0 histórias: 0 CAs dependem diretamente da DEC e 0 verificam os RF afetados |

- **RF:** nenhum
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):** nenhum
- **US:** —
- **CA que dependem da DEC:** —
- **CA dos RF afetados (regressão):** —
- **TA:** —
- **Endpoint ou tela:** nenhum
- **Código:** nenhum

## <a id="dec-18"></a>DEC-18 · Index Card das histórias

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-18.md)) |
| **Pergunta** | Quais campos compõem o "Index Card padrão"? O "Custo em Semanas" aceita fração? |
| **Opção adotada** | O Index Card tem nove campos (ID, título, história, valor, origem, prioridade, estimativa em custo em semanas, conversa e pronta quando), e o custo em semanas aceita fração (ex.: 1,2), como nas 19 [histórias](../historias/README.md#decisao-d). Nada muda. |
| **Responsável** | Professor (resposta); grupo (decisão). |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 0 TAs a rever (0 manuais), de 0 CAs em 0 histórias: 0 CAs dependem diretamente da DEC e 0 verificam os RF afetados |

- **RF:** nenhum
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):** nenhum
- **US:** —
- **CA que dependem da DEC:** —
- **CA dos RF afetados (regressão):** —
- **TA:** —
- **Endpoint ou tela:** nenhum
- **Código:** nenhum

## <a id="dec-19"></a>DEC-19 · Outros diagramas além dos casos de uso

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-19.md)) |
| **Pergunta** | Outros diagramas (sequência, C4, DER ou a jornada em raias) serão exigidos, ou só o diagrama de casos de uso? |
| **Opção adotada** | Além dos diagramas existentes, sem mudança, o grupo faz o DER. |
| **Responsável** | Professor (resposta); grupo (decisão). |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 0 TAs a rever (0 manuais), de 0 CAs em 0 histórias: 0 CAs dependem diretamente da DEC e 0 verificam os RF afetados |

- **RF:** nenhum
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):** nenhum
- **US:** —
- **CA que dependem da DEC:** —
- **CA dos RF afetados (regressão):** —
- **TA:** —
- **Endpoint ou tela:** nenhum
- **Código:** nenhum

## <a id="dec-20"></a>DEC-20 · Entrega separada dos documentos de Requisitos

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-20.md)) |
| **Pergunta** | Como os documentos de Requisitos são entregues? |
| **Opção adotada** | Os documentos de Requisitos são entregues à parte; o ZIP de Projeto de Programação continua com `README.md`, `src/` e `docs/`, sem `docs/fontes/`. |
| **Responsável** | Professor (resposta); grupo (decisão). |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 0 TAs a rever (0 manuais), de 0 CAs em 0 histórias: 0 CAs dependem diretamente da DEC e 0 verificam os RF afetados |

- **RF:** nenhum
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):** nenhum
- **US:** —
- **CA que dependem da DEC:** —
- **CA dos RF afetados (regressão):** —
- **TA:** —
- **Endpoint ou tela:** nenhum
- **Código:** nenhum

## <a id="dec-21"></a>DEC-21 · Capa do modelagem.pdf

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-21.md)) |
| **Pergunta** | A capa conta nas 6 páginas do `modelagem.pdf`, e precisa ser uma capa formal? |
| **Opção adotada** | A capa do `modelagem.pdf` fica fora do limite de 6 páginas e tem só o título e os nomes; a folga do plano do PDF fica para as quebras de página. |
| **Responsável** | Professor (resposta); grupo (decisão). |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 0 TAs a rever (0 manuais), de 0 CAs em 0 histórias: 0 CAs dependem diretamente da DEC e 0 verificam os RF afetados |

- **RF:** nenhum
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):** nenhum
- **US:** —
- **CA que dependem da DEC:** —
- **CA dos RF afetados (regressão):** —
- **TA:** —
- **Endpoint ou tela:** nenhum
- **Código:** nenhum

## <a id="dec-22"></a>DEC-22 · Modelo do contribuicoes.pdf

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-22.md)) |
| **Pergunta** | Há um modelo para o `contribuicoes.pdf`? |
| **Opção adotada** | Não há modelo do professor; o formato do `contribuicoes.pdf` fica a critério do grupo. |
| **Responsável** | Professor (resposta); grupo (decisão). |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 0 TAs a rever (0 manuais), de 0 CAs em 0 histórias: 0 CAs dependem diretamente da DEC e 0 verificam os RF afetados |

- **RF:** nenhum
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):** nenhum
- **US:** —
- **CA que dependem da DEC:** —
- **CA dos RF afetados (regressão):** —
- **TA:** —
- **Endpoint ou tela:** nenhum
- **Código:** nenhum

## <a id="dec-23"></a>DEC-23 · Apresentação

| Campo | Conteúdo |
|---|---|
| **Estado** | Decidida ([ficha](../decisoes/DEC-23.md)) |
| **Pergunta** | Como e onde é a apresentação do sistema? |
| **Opção adotada** | A apresentação é feita em aula, no notebook do grupo, com o sistema funcionando, em até 10 minutos. |
| **Responsável** | Professor (resposta); grupo (decisão). |
| **Prazo** | Decidida em 06/11/2026. |
| **Tipo de mudança se a resposta for outra** | decidida: outra resposta só por CR (comportamental) |
| **Regressão estimada** | 0 TAs a rever (0 manuais), de 0 CAs em 0 histórias: 0 CAs dependem diretamente da DEC e 0 verificam os RF afetados |

- **RF:** nenhum
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):** nenhum
- **US:** —
- **CA que dependem da DEC:** —
- **CA dos RF afetados (regressão):** —
- **TA:** —
- **Endpoint ou tela:** nenhum
- **Código:** nenhum
