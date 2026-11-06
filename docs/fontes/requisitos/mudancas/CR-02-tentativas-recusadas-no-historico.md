# CR-02 — Tentativas recusadas no histórico da reserva

| Identificação | Responsabilidade |
|---|---|
| **CR-02 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha (aprovador da fonte oficial) |

Pedido de mudança aberto a partir da resposta do professor à [DEC-05](../decisoes/DEC-05.md) na Aula 7 (06/11/2026), no [modelo de CR](modelo-cr.md). Este CR **não** muda nenhum RF, UC, CA nem código: quem o aplica é a tarefa **RES-12**, no mesmo PR do código, e é ela que atualiza os artefatos da seção 4 e roda `python scripts/gerar_rastreabilidade.py --manifesto`.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Abertura a partir da DEC-05 decidida na Aula 7 (GES-02). Aprovado pelo professor, aguardando implementação na RES-12. |

## 1. Solicitação

| Campo | Conteúdo |
|---|---|
| **Motivo** | Resposta do professor à [DEC-05](../decisoes/DEC-05.md) na Aula 7 (06/11/2026): "Deve ficar registrado sim, para ter o histórico completo da reserva." Decisão do grupo, nos pontos que a resposta não cobriu: as tentativas recusadas entram no próprio histórico da reserva (não num log separado), com ator, momento, situação pedida, resultado e código do erro; só se registram tentativas sobre uma reserva visível ao ator (a de outro Solicitante continua "não encontrada" e não é registrada, para não revelar a reserva). |
| **Solicitante** | O professor, como representante do cliente. |
| **Responsável** | O grupo. |
| **Estado** | Aprovado, aguardando implementação. |
| **Origem** | [DEC-05](../decisoes/DEC-05.md) e lacuna [L-02](../requisitos/srs.md#l-02). |
| **Baseline vigente** | Nenhuma aprovada: a [candidata à 1.0](../baselines/conecta-campus-1.0-candidata.md) continua candidata (aprovação na REQ-07). |
| **Tarefa que implementa** | RES-12 |

## 2. Classificação (A4·s17)

- [ ] **Editorial:** corrige o texto e mantém a obrigação; registra-se a correção.
- [x] **Comportamental:** o histórico deixa de ser só das mudanças aceitas: uma recusa passa a gravar um registro, o que muda o RF-22, o RNF-R02 e a garantia mínima do UC-10.

## 3. Mapa de impacto

Nos dois sentidos (A4·s19). O resumo por elo vem primeiro; depois, a seção da DEC no [mapa de impacto gerado](../rastreabilidade/impacto-por-dec.md#dec-05), copiada sem mudança em 06/11/2026, e o que a regra nova acrescenta.

| Elo | Afetados | Muda o quê |
|---|---|---|
| NS | [NS-12](../visao.md#ns-12) | O histórico de cada reserva passa a ser completo: mudanças aceitas e tentativas recusadas. |
| RF / RNF | [RF-22](../requisitos/rf-reservas.md#rf-22); [RNF-R02](../requisitos/rnf.md#rnf-r02) | RF-22 mostra também as tentativas recusadas; RNF-R02 passa a cobrir a gravação da tentativa. |
| UC (passo, alternativa ou exceção) | [UC-10 passo 7](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p7), subfunções incluídas, exceções do passo 6 e [garantia mínima](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#pós-condições-e-garantias); [UC-09 passo 3](../casos-de-uso/fichas-resumidas.md#uc09-p3); [UC-04 passo 10](../casos-de-uso/UC-04-solicitar-reserva.md#p10) sem mudança | As exceções sobre uma reserva visível gravam a tentativa; a consulta do histórico mostra as tentativas. |
| US / CA | 10 CAs em 6 histórias (lista abaixo); CAs novos em [US-12](../historias/US-12-ver-detalhe-e-historico.md) e nas histórias de mudar a situação (US-13 a US-16) | Os CAs de registro que dizem "nada entra no histórico" passam a dizer que a tentativa entra. |
| TA | 10 TAs (lista abaixo), nenhum manual; TAs novos para os CAs novos | Revisar os 10 e criar os da seção 5. |
| Endpoint ou tela (complementar) | `GET /api/reservas/{id}/historico/`, `/reservas/:reservaId`; `PATCH /api/reservas/{id}/situacao/` | A alteração recusada grava a tentativa; o histórico e a linha do tempo mostram o resultado e o código do erro. |
| Código (complementar) | `RegistroDeSituacao`, `RepositorioReservasDjango.salvar`, `ConsultarHistoricoDaReserva.executar`, `AlterarSituacaoReserva.executar` | O modelo do registro ganha resultado e código do erro (ou um registro irmão de tentativa); a gravação da tentativa acontece mesmo quando a alteração é recusada. |
| DEC | [DEC-05](../decisoes/DEC-05.md); [DEC-13](../decisoes/DEC-13.md) ([CR-01](CR-01-situacao-e-horario-da-reserva.md)) | A recusa nova por horário do CR-01 também é uma tentativa recusada. |

### Da DEC-05 (copiado de `impacto-por-dec.md`)

- **RF:** [RF-22](../rastreabilidade/matriz.md#rf-22)
- **RNF:** [RNF-R02](../requisitos/rnf.md#rnf-r02)
- **UC (passo, alternativa ou exceção):**
  - RF-22: [UC-09](../casos-de-uso/README.md#uc-09) · fluxo principal (UC-13 grava o que UC-09 mostra) — [UC-09 passo 3](../casos-de-uso/fichas-resumidas.md#uc09-p3), [UC-04 passo 10](../casos-de-uso/UC-04-solicitar-reserva.md#p10), [UC-10 passo 7](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#p7)
- **US:** [US-08](../historias/US-08-solicitar-reserva.md), [US-12](../historias/US-12-ver-detalhe-e-historico.md), [US-13](../historias/US-13-cancelar-uma-reserva.md), [US-14](../historias/US-14-confirmar-uma-reserva.md), [US-15](../historias/US-15-recusar-uma-reserva.md), [US-16](../historias/US-16-concluir-uma-reserva.md)
- **CA que dependem da DEC:** US-08: [CA-20](../historias/US-08-solicitar-reserva.md#us-08-ca-20); US-12: [CA-09](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-09); US-13: [CA-08](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-08); US-14: [CA-09](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-09); US-15: [CA-06](../historias/US-15-recusar-uma-reserva.md#us-15-ca-06); US-16: [CA-05](../historias/US-16-concluir-uma-reserva.md#us-16-ca-05)
- **CA dos RF afetados (regressão):** US-12: [CA-02](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-02), [CA-03](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-03), [CA-05](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-05), [CA-08](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-08)
- **TA:** [TA-77](../historias/US-08-solicitar-reserva.md#ta-77), [TA-105](../historias/US-12-ver-detalhe-e-historico.md#ta-105), [TA-106](../historias/US-12-ver-detalhe-e-historico.md#ta-106), [TA-108](../historias/US-12-ver-detalhe-e-historico.md#ta-108), [TA-111](../historias/US-12-ver-detalhe-e-historico.md#ta-111), [TA-112](../historias/US-12-ver-detalhe-e-historico.md#ta-112), [TA-121](../historias/US-13-cancelar-uma-reserva.md#ta-121), [TA-131](../historias/US-14-confirmar-uma-reserva.md#ta-131), [TA-139](../historias/US-15-recusar-uma-reserva.md#ta-139), [TA-145](../historias/US-16-concluir-uma-reserva.md#ta-145)
- **Endpoint ou tela:** `GET /api/reservas/{id}/historico/`; `/reservas/:reservaId`
- **Código:** `reservas/application/casos_de_uso.py::ConsultarHistoricoDaReserva.executar`, `reservas/domain/registro_de_situacao.py::RegistroDeSituacao`, `reservas/infrastructure/repositorio_django.py::RepositorioReservasDjango.salvar`

### Acrescentado pela regra nova

- Modelo do histórico: `RegistroDeSituacao` (`reservas/domain/registro_de_situacao.py`) e `RegistroDeSituacaoModel` com a migration nova; as constraints `reservas_registro_de_situacao_situacoes_validas` e `reservas_registro_de_situacao_anterior_diferente_da_nova` precisam aceitar uma tentativa (a situação pedida pode ser igual à atual ou desconhecida).
- Gravação: hoje `alterar_situacao` não muda nada e não registra nada quando recusa; a tentativa precisa ser gravada sem mudar a situação, mesmo com a exceção de domínio lançada, e sem quebrar a trava de concorrência (`ReservaDesatualizada`).
- Visibilidade: só reserva visível ao ator; a reserva de outro Solicitante continua 404 e não grava nada (garantia de não revelar a reserva).
- Saída: `RegistroDeSituacaoSaidaSerializer` com o resultado e o código do erro; linha do tempo `LinhaDoTempo` (frontend) distinguindo tentativa de mudança.
- Invariante do histórico: `reservas/tests/historico.py::verificar_historico_coerente` (o encadeamento passa a valer só para as mudanças aceitas) e a máquina de estados `TestMaquinaDaReserva` ("uma recusa não muda nada" passa a acrescentar uma tentativa).
- Documentos: README de reservas e "Limitações conhecidas" do README da raiz, glossário (histórico, registro de situação), [Visão](../visao.md) (NS-12, R-08), `docs/fontes/testes_de_reservas.md` e a Figura 3 da modelagem, se o registro mudar de forma.

## 4. Diferença

Trechos atuais e propostos. O texto proposto é a referência para a RES-12; a redação final sai no PR dela.

| Artefato | Antes | Depois |
|---|---|---|
| [RF-22](../requisitos/rf-reservas.md#rf-22), enunciado | O sistema deve permitir ao usuário autenticado consultar o histórico de uma reserva que ele pode ver e ver, em ordem cronológica, a criação e cada mudança de situação aceita, com data e hora, nome do autor, situação anterior e nova e motivo. | O sistema deve permitir ao usuário autenticado consultar o histórico de uma reserva que ele pode ver e ver, em ordem cronológica, a criação, cada mudança de situação aceita **e cada tentativa recusada de mudar a situação**, com data e hora, nome do autor, situação anterior e nova (**ou a pedida, na tentativa**), motivo **e, na tentativa, o resultado e o código do erro**. |
| [UC-10, subfunções incluídas](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#fluxo-principal-comum-aos-filhos) | Só as mudanças aceitas são registradas: nenhuma exceção grava registro (DEC-05). | As mudanças aceitas e as tentativas recusadas sobre uma reserva visível ao ator são registradas; a reserva inexistente ou de outra pessoa (E6.2) não grava nada (DEC-05 decidida). |
| [UC-10, garantia mínima](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#pós-condições-e-garantias) | Mesmo quando a meta falha: a reserva fica exatamente como estava (situação, motivo e histórico); nenhuma tentativa recusada vira registro; … | Mesmo quando a meta falha: a reserva fica com a mesma situação e o mesmo motivo; a tentativa recusada sobre uma reserva visível ao ator fica no histórico com o resultado e o código do erro; … |
| [UC-09 passo 3](../casos-de-uso/fichas-resumidas.md#uc09-p3) | O sistema mostra, em ordem cronológica, a criação e cada mudança de situação aceita: data e hora, nome do autor, situação anterior e nova e motivo. | O sistema mostra, em ordem cronológica, a criação, cada mudança de situação aceita **e cada tentativa recusada**: data e hora, nome do autor, situação anterior e nova (ou a pedida), motivo e, na tentativa, o resultado e o código do erro. |

**A definir na RES-12, sem mudar a decisão:**

- Se a recusa por situação não informada ([E6.1](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e6-1)), conferida antes da visibilidade, entra como tentativa quando a reserva é visível ao ator.
- Se a leitura desatualizada ([E7.1](../casos-de-uso/UC-10-alterar-situacao-da-reserva.md#e7-1), `RESERVA_DESATUALIZADA`) entra como tentativa recusada.
- Como gravar a situação pedida quando ela é desconhecida (`SITUACAO_INVALIDA`).

## 5. Critérios de aceite

Novos ou alterados, em Dado/Quando/Então ([DEC-15](../decisoes/DEC-15.md)). Entram nas histórias na RES-12, com o TA de cada um.

#### CR-02 · CA-01 · Tentativa sem permissão registrada (registro)

- **Dado** uma reserva Solicitada do próprio Solicitante
- **Quando** ele tenta confirmá-la
- **Então** o sistema recusa, a reserva continua Solicitada e o histórico dela ganha a tentativa, com o ator, o momento, a situação pedida (Confirmada), o resultado (recusada) e o código do erro
- **TA:** a criar na RES-12, junto com o CA na história.

#### CR-02 · CA-02 · Transição não permitida registrada (registro)

- **Dado** uma reserva Concluída
- **Quando** o Gestor tenta cancelá-la, com motivo
- **Então** o sistema recusa, a reserva continua Concluída e o histórico mostra a tentativa com o código do erro da transição não permitida
- **TA:** a criar na RES-12, junto com o CA na história.

#### CR-02 · CA-03 · Reserva de outra pessoa não registrada (acesso)

- **Dado** uma reserva de outro Solicitante
- **Quando** um Solicitante tenta cancelá-la
- **Então** o sistema informa que a reserva não foi encontrada e o histórico dela não ganha nenhum registro
- **TA:** a criar na RES-12, junto com o CA na história.

#### CR-02 · CA-04 · Tentativa na consulta do histórico (sucesso)

- **Dado** uma reserva Confirmada com uma tentativa recusada registrada depois da confirmação
- **Quando** o Gestor consulta o histórico
- **Então** a tentativa aparece na ordem cronológica, distinta das mudanças aceitas, e a situação atual continua Confirmada
- **TA:** a criar na RES-12, junto com o CA na história.

## 6. Regressão

- Rever os 10 TAs listados no mapa de impacto (seção 3), todos automatizados.
- Mudam: os CAs de registro que dependem da DEC-05 ([US-08 · CA-20](../historias/US-08-solicitar-reserva.md#us-08-ca-20), [US-12 · CA-09](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-09), [US-13 · CA-08](../historias/US-13-cancelar-uma-reserva.md#us-13-ca-08), [US-14 · CA-09](../historias/US-14-confirmar-uma-reserva.md#us-14-ca-09), [US-15 · CA-06](../historias/US-15-recusar-uma-reserva.md#us-15-ca-06), [US-16 · CA-05](../historias/US-16-concluir-uma-reserva.md#us-16-ca-05)), conforme o que cada um diz sobre recusas.
- Não devem mudar: a criação continua sendo o primeiro registro ("Solicitada por …"); uma mudança aceita continua com a situação anterior e a nova; a reserva de outra pessoa continua "não encontrada" ([US-12 · CA-06](../historias/US-12-ver-detalhe-e-historico.md#us-12-ca-06) e o CA-03 da seção 5).
- Uma recusa continua sem mudar a situação nem o motivo da reserva.

## 7. Decisão

| Campo | Conteúdo |
|---|---|
| **Decisão** | Aceita. |
| **Quem decidiu e quando** | O professor, como representante do cliente, na Aula 7 (06/11/2026), na resposta à [DEC-05](../decisoes/DEC-05.md); registrado pelo grupo na GES-02. |
| **Justificativa** | O cliente quer o histórico completo da reserva, como no modelo de critério de aceite da aula ("tentativa registrada com data, ator e resultado"). A restrição à reserva visível é do grupo, para não revelar reservas de outras pessoas. |
| **Referência candidata** | Ainda nenhuma: a RES-12 aplica o CR e gera o manifesto (`python scripts/gerar_rastreabilidade.py --manifesto`). A [baseline candidata à 1.0](../baselines/conecta-campus-1.0-candidata.md) continua candidata; a aprovação é da REQ-07. |
