# CR-01 — Mudança de situação em relação ao horário da reserva

| Identificação | Responsabilidade |
|---|---|
| **CR-01 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha (aprovador da fonte oficial) |

Pedido de mudança aberto a partir da resposta do professor à [DEC-13](../decisoes/DEC-13.md) na Aula 7 (06/11/2026), no [modelo de CR](modelo-cr.md). Este CR **não** muda nenhum RF, UC, CA nem código: quem o aplica é a tarefa **RES-11**, no mesmo PR do código, e é ela que atualiza os artefatos da seção 4 e roda `python scripts/gerar_rastreabilidade.py --manifesto`.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Abertura a partir da DEC-13 decidida na Aula 7 (GES-02). Aprovado pelo professor, aguardando implementação na RES-11. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-19 e TA-20 passam a TA-20 e TA-21, e TA-21 a TA-158 passam a TA-24 a TA-161, para os TA-19, TA-22 e TA-23 novos da US-03 (revogação e troca da credencial de renovação) seguirem a ordem das histórias (AUT-09). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-96 a TA-107 passam a TA-97, TA-98, TA-99, TA-102, TA-103, TA-105, TA-106, TA-107, TA-109, TA-110, TA-113 e TA-114, e TA-108 a TA-161 passam a TA-115 a TA-168, para os TAs novos das US-10 e US-11 (consulta em páginas) seguirem a ordem das histórias (RES-10). Mudança editorial, sem nova obrigação. Sem aprovação. |

## 1. Solicitação

| Campo | Conteúdo |
|---|---|
| **Motivo** | Resposta do professor à [DEC-13](../decisoes/DEC-13.md) na Aula 7 (06/11/2026): "Temos que alterar, deve poder concluir somente depois do término, e recusar e cancelar somente antes do início (isso para Gestor)." Decisão do grupo, nos pontos que a resposta não cobriu: confirmar continua sem restrição de horário; o cancelamento pelo Solicitante continua sem restrição de horário; a Solicitada não decidida continua ocupando o horário depois da data. Bordas: concluir vale a partir do instante do término; recusar e cancelar (Gestor) valem só enquanto o início ainda não chegou. |
| **Solicitante** | O professor, como representante do cliente. |
| **Responsável** | O grupo. |
| **Estado** | Aprovado, aguardando implementação. |
| **Origem** | [DEC-13](../decisoes/DEC-13.md) e lacuna [L-01](../requisitos/srs.md#l-01). |
| **Baseline vigente** | Nenhuma aprovada: a [candidata à 1.0](../baselines/conecta-campus-1.0-candidata.md) continua candidata (aprovação na REQ-07). |
| **Tarefa que implementa** | RES-11 |

## 2. Classificação (A4·s17)

- [ ] **Editorial:** corrige o texto e mantém a obrigação; registra-se a correção.
- [x] **Comportamental:** o Gestor passa a ter recusadas mudanças hoje aceitas (concluir antes do término; recusar ou cancelar a partir do início), e as ações disponíveis passam a depender do momento da consulta.

## 3. Mapa de impacto

Nos dois sentidos (A4·s19). O resumo por elo vem primeiro; depois, a seção da DEC no [mapa de impacto gerado](../rastreabilidade/impacto-por-dec.md#dec-13), copiada sem mudança em 06/11/2026, e o que a regra nova acrescenta.

| Elo | Afetados | Muda o quê |
|---|---|---|
| NS | [NS-09](../visao.md#ns-09) | Passa a ser atendida por inteiro: concluir registra que o uso aconteceu (só a partir do término). |
| RF / RNF | [RF-16](../requisitos/rf-reservas.md#rf-16), [RF-18](../requisitos/rf-reservas.md#rf-18), [RF-19](../requisitos/rf-reservas.md#rf-19), [RF-20](../requisitos/rf-reservas.md#rf-20) mudam; [RF-17](../requisitos/rf-reservas.md#rf-17) e [RF-21](../requisitos/rf-reservas.md#rf-21) ficam (regressão); nenhum RNF | Ações conforme o horário (RF-16); recusar e cancelar pelo Gestor só antes do início (RF-18, RF-20); concluir só a partir do término (RF-19); uma recusa nova (F5), com o ID definido na RES-11. |
| UC (passo, alternativa ou exceção) | [UC-10 passo 2](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p2), [passo 6](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p6), [variações](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#variações) UC-11 (Gestor), UC-18 e UC-19, [Questões em aberto](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#questões-em-aberto) | Passo 2 e passo 6 consideram o momento; uma exceção nova no passo 6, depois de [E6.5](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-5); a nota das variações deixa de dizer que nenhuma transição depende do horário. |
| US / CA | 21 CAs em 9 histórias (lista abaixo); CAs novos em [US-13](../historias/US-13-cancelar-uma-reserva.md), [US-15](../historias/US-15-recusar-uma-reserva.md) e [US-16](../historias/US-16-concluir-uma-reserva.md) | Os de sucesso de concluir, recusar e cancelar pelo Gestor ganham a condição de horário; as recusas novas viram CAs de exceção. |
| TA | 21 TAs (lista abaixo), nenhum manual; TAs novos para os CAs novos | Revisar os 21 e criar os dos CAs da seção 5. |
| Endpoint ou tela (complementar) | `PATCH /api/reservas/{id}/situacao/`, `GET /api/reservas/`, `GET /api/reservas/{id}/`, `/reservas`, `/reservas/:reservaId` | A recusa nova na alteração; `acoes_disponiveis` conforme o momento na lista e no detalhe. |
| Código (complementar) | `Reserva.alterar_situacao`, `Reserva.acoes_permitidas_para`, `situacao.py`, `AlterarSituacaoReserva`, `ReservaSaidaSerializer.get_acoes_disponiveis` | Regra de horário no domínio, uma única vez, usada pelas ações e pela alteração; o momento chega pelo relógio já injetado. |
| DEC | [DEC-13](../decisoes/DEC-13.md); [DEC-05](../decisoes/DEC-05.md) ([CR-02](CR-02-tentativas-recusadas-no-historico.md)) | Se o CR-02 já estiver aplicado, a recusa nova por horário também entra no histórico como tentativa recusada. |

### Da DEC-13 (copiado de `impacto-por-dec.md`)

- **RF:** [RF-16](../rastreabilidade/matriz.md#rf-16), [RF-17](../rastreabilidade/matriz.md#rf-17), [RF-18](../rastreabilidade/matriz.md#rf-18), [RF-19](../rastreabilidade/matriz.md#rf-19), [RF-20](../rastreabilidade/matriz.md#rf-20), [RF-21](../rastreabilidade/matriz.md#rf-21)
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
- **TA:** [TA-56](../historias/US-07-desativar-e-reativar-espaco.md#ta-56), [TA-79](../historias/US-08-solicitar-reserva.md#ta-79), [TA-94](../historias/US-10-acompanhar-minhas-reservas.md#ta-94), [TA-107](../historias/US-11-acompanhar-todas-as-reservas.md#ta-107), [TA-115](../historias/US-12-ver-detalhe-e-historico.md#ta-115), [TA-117](../historias/US-12-ver-detalhe-e-historico.md#ta-117), [TA-125](../historias/US-13-cancelar-uma-reserva.md#ta-125), [TA-126](../historias/US-13-cancelar-uma-reserva.md#ta-126), [TA-127](../historias/US-13-cancelar-uma-reserva.md#ta-127), [TA-128](../historias/US-13-cancelar-uma-reserva.md#ta-128), [TA-131](../historias/US-13-cancelar-uma-reserva.md#ta-131), [TA-134](../historias/US-14-confirmar-uma-reserva.md#ta-134), [TA-135](../historias/US-14-confirmar-uma-reserva.md#ta-135), [TA-136](../historias/US-14-confirmar-uma-reserva.md#ta-136), [TA-140](../historias/US-14-confirmar-uma-reserva.md#ta-140), [TA-141](../historias/US-14-confirmar-uma-reserva.md#ta-141), [TA-145](../historias/US-15-recusar-uma-reserva.md#ta-145), [TA-146](../historias/US-15-recusar-uma-reserva.md#ta-146), [TA-152](../historias/US-16-concluir-uma-reserva.md#ta-152), [TA-153](../historias/US-16-concluir-uma-reserva.md#ta-153), [TA-154](../historias/US-16-concluir-uma-reserva.md#ta-154)
- **Endpoint ou tela:** `GET /api/reservas/`; `GET /api/reservas/{id}/`; `/reservas`; `/reservas/:reservaId`; `PATCH /api/reservas/{id}/situacao/`
- **Código:** `reservas/domain/reserva.py::Reserva.acoes_permitidas_para`, `reservas/domain/situacao.py::transicoes_a_partir_de`, `reservas/api/serializers.py::ReservaSaidaSerializer.get_acoes_disponiveis`, `reservas/application/casos_de_uso.py::AlterarSituacaoReserva.executar`, `reservas/domain/reserva.py::Reserva.alterar_situacao`, `reservas/domain/situacao.py::SITUACOES_QUE_EXIGEM_MOTIVO`, `reservas/domain/situacao.py::DESTINOS_POR_PAPEL`

### Acrescentado pela regra nova

- Exceção nova no [UC-10](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p6), passo 6, depois de E6.5: o Gestor tenta concluir antes do término, ou recusar ou cancelar a partir do início; a reserva fica como estava.
- Ações disponíveis ([RF-16](../requisitos/rf-reservas.md#rf-16), passo 2): "Concluir" só a partir do término; "Recusar" e o "Cancelar" do Gestor só antes do início; "Confirmar" e o "Cancelar" do Solicitante sem mudança. As ações passam a depender do momento da consulta, então a lista, o detalhe e a resposta da alteração precisam do relógio.
- Mensagem da recusa nova: informa a partir de quando se pode concluir (data e hora do término) ou que recusar e cancelar só valem antes do início.
- Uma exceção de domínio nova, numa das 4 categorias, e a linha dela na tabela de erros do README de reservas.
- Testes: a máquina de estados `TestMaquinaDaReserva` (a invariante "ação oferecida ⇔ alteração aceita" passa a depender do momento), os testes de domínio, de caso de uso e de API das transições e `docs/fontes/testes_de_reservas.md`.
- Dados de exemplo: a Concluída já é concluída depois do término, e as recusas e cancelamentos de exemplo são de reservas futuras; continuam válidos, a conferir.
- Documentos: glossário (ação disponível, Concluída), [Visão](../visao.md) (NS-09), SRS (auditoria do RF-16 ao RF-21) e a Figura 4 da modelagem (`estados-da-reserva.mmd`), se as condições de horário forem desenhadas.

## 4. Diferença

Trechos atuais e propostos. O texto proposto é a referência para a RES-11; a redação final sai no PR dela.

| Artefato | Antes | Depois |
|---|---|---|
| [RF-16](../requisitos/rf-reservas.md#rf-16), enunciado | O sistema deve permitir ao usuário autenticado ver, em cada reserva que ele pode ver, as mudanças de situação que o perfil dele pode executar a partir da situação atual, com a indicação das que exigem motivo, e nenhuma numa situação final. | O sistema deve permitir ao usuário autenticado ver, em cada reserva que ele pode ver, as mudanças de situação que o perfil dele pode executar a partir da situação atual **e do momento da consulta (concluir só a partir do término; recusar e cancelar, pelo Gestor, só antes do início)**, com a indicação das que exigem motivo, e nenhuma numa situação final. |
| [RF-18](../requisitos/rf-reservas.md#rf-18), enunciado | O sistema deve permitir ao Gestor recusar uma reserva Solicitada informando um motivo de até 300 caracteres e ver a reserva na situação Recusada, com o motivo, sem ocupar mais o horário. | O sistema deve permitir ao Gestor recusar uma reserva Solicitada **cujo início ainda não chegou**, informando um motivo de até 300 caracteres, e ver a reserva na situação Recusada, com o motivo, sem ocupar mais o horário. |
| [RF-19](../requisitos/rf-reservas.md#rf-19), enunciado | O sistema deve permitir ao Gestor concluir uma reserva Confirmada, com motivo opcional, e ver a reserva na situação Concluída, sem nenhuma ação disponível depois disso. | O sistema deve permitir ao Gestor concluir uma reserva Confirmada **cujo término já chegou**, com motivo opcional, e ver a reserva na situação Concluída, sem nenhuma ação disponível depois disso. |
| [RF-20](../requisitos/rf-reservas.md#rf-20), enunciado | O sistema deve permitir ao Gestor cancelar uma reserva Solicitada ou Confirmada informando um motivo de até 300 caracteres e ver a reserva na situação Cancelada, com o motivo, sem ocupar mais o horário. | O sistema deve permitir ao Gestor cancelar uma reserva Solicitada ou Confirmada **cujo início ainda não chegou**, informando um motivo de até 300 caracteres, e ver a reserva na situação Cancelada, com o motivo, sem ocupar mais o horário. |
| [RF-17](../requisitos/rf-reservas.md#rf-17) e [RF-21](../requisitos/rf-reservas.md#rf-21) | Sem condição de horário. | Sem mudança (decisão do grupo). |
| Recusa nova (F5), ID definido na RES-11 | — | O sistema deve impedir que o Gestor conclua uma reserva antes do término dela ou a recuse ou cancele a partir do início dela, sem mudar a reserva, e informar a partir de quando é possível concluir ou que recusar e cancelar só valem antes do início. |
| [UC-10 passo 2](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p2) | O sistema mostra a reserva com a situação atual, o motivo (se houver) e as ações disponíveis para o ator: as transições que a tabela permite a partir da situação atual e que o perfil dele pode executar, com a indicação das que exigem motivo. | … as transições que a tabela permite a partir da situação atual, que o perfil dele pode executar **e que o momento atual permite (concluir a partir do término; recusar e cancelar, pelo Gestor, antes do início)**, com a indicação das que exigem motivo. |
| [UC-10 passo 6](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p6) | … o perfil do ator pode levar a reserva a ela; a tabela permite a transição a partir da situação atual; o motivo respeita o limite e, para recusar ou cancelar, foi informado. | … a tabela permite a transição a partir da situação atual; **o momento atual permite a mudança;** o motivo respeita o limite e, para recusar ou cancelar, foi informado (posição exata na ordem real, definida na RES-11). |
| [UC-10, variações](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#variações) | Nenhuma transição depende do horário da reserva: confirmar ou recusar depois do início, concluir antes do término e cancelar depois do uso são aceitos (opção a da DEC-13; lacuna L-01). | Concluir depende do término, e recusar e cancelar pelo Gestor dependem do início; confirmar e o cancelamento pelo Solicitante não dependem do horário (DEC-13 decidida). |
| UC-10, exceção nova (depois de E6.5) | — | Condição: o Gestor tenta concluir antes do término, ou recusar ou cancelar a partir do início. Resultado para o ator: a regra e o momento a partir do qual concluir é possível, ou que recusar e cancelar só valiam antes do início. Estado depois: a reserva fica como estava. Requisito: a recusa nova. |

## 5. Critérios de aceite

Novos ou alterados, em Dado/Quando/Então ([DEC-15](../decisoes/DEC-15.md)). Entram nas histórias na RES-11, com o TA de cada um.

#### CR-01 · CA-01 · Concluir antes do término (exceção)

- **Dado** uma reserva Confirmada cujo término ainda não chegou
- **Quando** o Gestor tenta concluí-la
- **Então** o sistema recusa, informa a partir de quando pode concluir (a data e a hora do término) e a reserva continua Confirmada
- **TA:** a criar na RES-11, junto com o CA na história.

#### CR-01 · CA-02 · Concluir a partir do término (sucesso)

- **Dado** uma reserva Confirmada cujo término acabou de chegar
- **Quando** o Gestor a conclui
- **Então** a reserva passa a Concluída, sem nenhuma ação oferecida depois disso
- **TA:** a criar na RES-11, junto com o CA na história.

#### CR-01 · CA-03 · Recusar depois do início (exceção)

- **Dado** uma reserva Solicitada cujo início já chegou
- **Quando** o Gestor tenta recusá-la, com motivo
- **Então** o sistema recusa, informa que só é possível recusar antes do início e a reserva continua Solicitada
- **TA:** a criar na RES-11, junto com o CA na história.

#### CR-01 · CA-04 · Cancelar pelo Gestor depois do início (exceção)

- **Dado** uma reserva Confirmada cujo início já chegou
- **Quando** o Gestor tenta cancelá-la, com motivo
- **Então** o sistema recusa, informa que só é possível cancelar antes do início e a reserva continua Confirmada
- **TA:** a criar na RES-11, junto com o CA na história.

#### CR-01 · CA-05 · Ações oferecidas conforme o horário (alternativa)

- **Dado** uma reserva Confirmada cujo início já chegou e cujo término ainda não chegou
- **Quando** o Gestor a consulta
- **Então** nem concluir nem cancelar são oferecidos a ele; depois do término, concluir passa a ser oferecido
- **TA:** a criar na RES-11, junto com o CA na história.

#### CR-01 · CA-06 · Solicitante cancela depois do início (sucesso)

- **Dado** uma reserva própria Confirmada cujo início já chegou
- **Quando** o Solicitante a cancela, com motivo
- **Então** a reserva passa a Cancelada, com o motivo (sem mudança, decisão do grupo)
- **TA:** a criar na RES-11, junto com o CA na história.

#### CR-01 · CA-07 · Confirmar depois do início (sucesso)

- **Dado** uma reserva Solicitada cujo início já chegou
- **Quando** o Gestor a confirma
- **Então** a reserva passa a Confirmada (sem mudança, decisão do grupo)
- **TA:** a criar na RES-11, junto com o CA na história.

## 6. Regressão

- Rever os 21 TAs listados no mapa de impacto (seção 3), todos automatizados.
- Mudam: [US-15 · CA-01](../historias/US-15-recusar-uma-reserva.md#us-15-ca-01), [US-16 · CA-01](../historias/US-16-concluir-uma-reserva.md#us-16-ca-01) e [US-13 · CA-02](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-02) (ganham a condição de horário) e [US-14 · CA-01](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-01) (as ações oferecidas ao Gestor depois de confirmar passam a depender do horário).
- Não devem mudar: [US-13 · CA-01](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-01) (o Solicitante cancela a própria) e [US-08 · CA-18](../historias/US-08-solicitar-reserva.md#us-08-ca-18) (a Solicitada não decidida continua ocupando o horário), além dos CA-06 e CA-07 da seção 5.
- A garantia mínima do UC-10 continua: em qualquer recusa, a reserva fica como estava.

## 7. Decisão

| Campo | Conteúdo |
|---|---|
| **Decisão** | Aceita. |
| **Quem decidiu e quando** | O professor, como representante do cliente, na Aula 7 (06/11/2026), na resposta à [DEC-13](../decisoes/DEC-13.md); registrado pelo grupo na GES-02. |
| **Justificativa** | Regra de uso dada pelo cliente na resposta à DEC-13; com ela, concluir passa a registrar que o uso aconteceu, como pede a NS-09. Os pontos que o professor não abordou ficam como estão, por decisão do grupo. |
| **Referência candidata** | Ainda nenhuma: a RES-11 aplica o CR e gera o manifesto (`python scripts/gerar_rastreabilidade.py --manifesto`). A [baseline candidata à 1.0](../baselines/conecta-campus-1.0-candidata.md) continua candidata; a aprovação é da REQ-07. |
