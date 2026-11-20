# Pacote de revisão por pares — baseline 1.0

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **RPP-01 • 0.1 • Rascunho** (pacote de revisão por pares da baseline 1.0) | Autor: Max Zimmermann dos Reis • Revisor: Eduardo Almeida da Cunha • Aprovador: Kelvin Fraga da Silva | `docs/fontes/requisitos/baselines/revisao-por-pares-1.0.md` |

Este pacote **prepara** a revisão e **verifica** os critérios da [baseline candidata](conecta-campus-1.0-candidata.md). Ele não registra revisão nem aprovação: quem revisa e quem aprova são pessoas, e os campos da seção 8 só são preenchidos com os nomes e as datas que elas informarem. Nenhum documento mudou de versão nem de estado por causa dele (A4·s14: salvo não é aprovado, commit não é aprovação). Índice da fonte oficial: [README](../README.md).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 19/11/2026 | Max Zimmermann dos Reis | Criação (REQ-07, primeira parte): escopo, checklists copiados da Visão e da SRS, portões automáticos, critérios da baseline, achados da preparação e campos de registro em branco. Sem revisão e sem aprovação. |

## Estado verificado (commit)

| Campo | Conteúdo |
|---|---|
| **Estado verificado (commit)** | `8bb653b16f6925cf1007478ef2291380a9c822f4` (`Merge pull request #72 from maxzdosreis/docs/DOC-06-contribuicoes`), branch `docs/REQ-07-baseline-1-0`, árvore limpa antes deste pacote |
| **Rótulo** | Estado verificado pela preparação, **sem aprovação**. Não é a "Referência Git revisada": essa só entra na seção 8, preenchida por pessoas. |
| **Quando** | 19/11/2026 |

Os resultados abaixo valem para esse commit mais este pacote e a linha nova do [README da fonte](../README.md). Se a fonte mudar depois, rode os portões de novo.

## 1. Escopo da revisão

Fonte oficial `docs/fontes/requisitos/`, 114 artefatos do [manifesto](conecta-campus-1.0-candidata.md#2-manifesto) (todo `.md`, `.puml` e `.csv`, menos `baselines/`). O manifesto lista o SHA-256 de cada arquivo; aqui eles vão agrupados por tipo.

| Tipo | Onde | Artefatos | Versão • estado atuais |
|---|---|---|---|
| Visão e glossário | [`visao.md`](../visao.md) (VIS-01), [`glossario.md`](../glossario.md) (GLO-01), [índice](../README.md) (IND-01) | 3 | 0.1 • Rascunho |
| SRS, fichas de RF e RNF, regras de negócio | [`requisitos/`](../requisitos/README.md) (SRS-01, RNG-01) | 9 | 0.1 • Rascunho |
| Casos de uso | [`casos-de-uso/`](../casos-de-uso/README.md) (UCD-01, UCD-02, UC-02, UC-04, UC-10, UC-14, UCR-01) | 9 | 0.1 • Rascunho |
| Histórias, CAs e TAs | [`historias/`](../historias/README.md) (HIS-01, US-01 a US-22) | 23 | 0.1 • Rascunho |
| Decisões | [`decisoes/`](../decisoes/README.md) (DEC-01 a DEC-27, IND-02, PAU-01) | 29 | 0.1 • Rascunho |
| Pedidos de mudança | [`mudancas/`](../mudancas/README.md) (CR-01 a CR-07, IND-03, MCR-01) | 9 | 0.1 • Rascunho |
| Rastreabilidade (gerada) | [`rastreabilidade/`](../rastreabilidade/README.md) (RAS-01 e os arquivos gerados) | 8 | 0.1 • Rascunho |
| Levantamento | [`levantamento/`](../levantamento/README.md) (IND-05, ENT, ROT, QST, SIN) | 18 | 0.1 • Rascunho |
| Verificações | [`verificacoes/`](../verificacoes/FE-08-usabilidade.md) (VER-01) | 1 | 0.1 • Rascunho |
| Entrega de 13/11/2026 | [`entrega/`](../entrega/RS_Grupo03_Especificacao.md) (especificação, ensaio, perguntas, roteiro) | 4 | 0.1 • Rascunho |
| Entrega de 13/11/2026 | [`entrega/RS_Grupo03_Evidencias.md`](../entrega/RS_Grupo03_Evidencias.md) | 1 | sem cabeçalho (ver o achado P-02) |

Nenhum arquivo está em 0.2 ou 1.0. A tabela arquivo a arquivo, com o SHA-256, é o [manifesto](conecta-campus-1.0-candidata.md#2-manifesto).

## 2. Portões automáticos

Rodados na raiz do repositório, em 19/11/2026, no commit acima. Nada foi alterado por eles.

| Portão | Resultado | Saída resumida |
|---|---|---|
| `python scripts/verificar_requisitos.py` | PASSA | seções 1 a 4 OK; termos vagos: 0; 9.958 links relativos conferidos, 0 quebrados |
| `python scripts/verificar_casos_de_uso.py` | PASSA | seções 1 a 10 OK (13 exceções da ficha = 13 do fluxo de UC-04) |
| `python scripts/verificar_historias.py` | PASSA | seções 1 a 8 OK; 22 histórias; 208 linhas no índice dos TAs; 624 partes Dado/Quando/Então |
| `python scripts/verificar_visao_do_sistema.py` | PASSA | 29 setas conferidas, nenhum import sem seta |
| `python scripts/verificar_modelo_do_dominio.py` | PASSA | 105 elementos conferidos contra o código |
| `python scripts/verificar_fluxo_principal.py` | **FALHA** | 1 pendência: `solicitar-reserva.mmd:31`, a chamada `obter_espaco_reservavel` (passo 4) não acontece depois de `garantir_inicio_no_futuro` (passo 3) na ordem real do código |
| `python scripts/gerar_rastreabilidade.py --verificar` | **FALHA** | a, b, c, d, e, g e h OK; **f falhou (3 erros)**: `entrega/RS_Grupo03_Evidencias.md` sem `**ID • versão • estado**`, sem `Autor • Revisor • Aprovador` e sem `## Histórico` |
| `python scripts/verificar_producao.py` | PASSA | (INF-08, modo de produção) |
| `python scripts/verificar_entrega_evidencias.py` | PASSA | (REQ-14) |
| `python scripts/verificar_entrega_especificacao.py` | FALHA | contagens do texto entregue em 13/11 (RF 63, RN 17, US 20, UC 22) × fonte (70, 19, 22, 23); a entrega não foi alterada de propósito depois de 13/11/2026 (ver P-04) |
| `python scripts/verificar_apresentacao.py` | FALHA | roteiro cita DEC 25 e CR 5; a fonte tem 27 e 7 (ver P-04) |

Não rodados: `verificar_der.py` e `verificar_documento_modelagem.py` precisam do container ou dos PDFs e não fazem parte do README da fonte como verificação de requisitos (o `--verificar` da rastreabilidade e os três verificadores de requisitos são os que ele lista).

## 3. Critérios da baseline

Cada critério com **PASSA**, **FALHA** ou **PRECISA DE REVISOR**, e a evidência.

| # | Critério | Resultado | Evidência |
|---|---|---|---|
| a | CR-01 a CR-07 com o estado final coerente; nenhum CA com a marca de implementação pendente; nenhum TA para teste inexistente | PASSA | CR-01 a CR-04: **Implementado** (16 e 17/11/2026; RES-11, RES-12, ESP-07, AUT-12). CR-05: **Aplicado na especificação** (sem código: o sistema tem um perfil só, DEC-25). CR-06 e CR-07: **Implementado** (AUT-10, AUT-11). A marca "implementação pendente" só aparece em linhas de histórico que dizem que ela saiu e na regra "Pronta quando" das histórias; nenhum CA a leva. Cobertura: 0 TA pendentes de 208; `verificar_historias` seção 5 OK (testes citados existem). |
| b | Cada DEC decidida ou aceita como premissa (CS-07) | PASSA, com ressalva | As 27 DECs estão com estado **Decidida** (tabela da seção 4). Nenhuma "adotada provisoriamente". Ressalva: o ponto 4 do `CLAUDE.md` (composição do grupo nas duas disciplinas) segue sem resposta e não é uma DEC; ver "PRECISA DE DECISÃO DO GRUPO" na seção 4. |
| c | Cada NS com RF; cada RF com UC ou US; cada US com CA; cada CA com TA | PASSA, com exceções justificadas | `--verificar` a: 17 de 17 NS chegam a um TA (a tabela de cobertura dá 16 de 17 com RF: a NS-17 não tem RF por decisão, [DEC-24](../decisoes/DEC-24.md)); RF com cadeia completa: 69 de 70, com o elo faltante justificado; 208 de 208 CA com TA. Exceções: NS-17 (fora do 1.0, DEC-24); RF-38 (F6, "Ver o resultado de cada operação"), o único RF sem UC, US, CA, endpoint e tela, tratado como transversal ("qualidade de todos os casos de uso", conforme a [matriz](../rastreabilidade/matriz.md)). O revisor confere se essa justificativa basta. |
| d | Status de cada RNF | PRECISA DE DECISÃO DO GRUPO | 33 RNF: 26 automatizado, 2 automatizado (comando), 1 manual, 2 medição, 2 **manual (a verificar)**: **RNF-S01** (execução num ambiente novo com um comando; critério CS-03) e **RNF-S06** (configuração sem segredos no código; "a verificar antes da entrega"). RNF-U02 a RNF-U05 foram verificados na FE-08 ([VER-01](../verificacoes/FE-08-usabilidade.md)); RNF-U03 segue "verificado em parte" ([L-09](../requisitos/srs.md#l-09)). Nem o README da fonte nem a CS-07 dizem se RNF "a verificar" bloqueiam a baseline; a candidata os trata como lacuna aceita (L-09, seção 4 dela) e pede a execução no ensaio (item 3 do checklist da candidata). Decisão não tomada aqui. |
| e | Valores e contagens iguais entre a fonte e o README da raiz | PASSA, com ressalvas | Agenda (07:00 às 00:00 por espaço, 1 h sugerida, 30 min a 3 h, 30 dias), matrícula (dígitos, 20 como limite técnico) e limites de tentativas (5/min por e-mail, 20/min por IP, 10/h no cadastro) batem com a fonte. O README da raiz não repete as contagens de RF, RNF, RN, UC, US e DEC. Ressalvas na fonte: ver P-05 e P-06. |
| f | Nenhum marcador de pendência, nenhum link ou âncora quebrados | PASSA, com ressalva | 0 links quebrados em 112 arquivos. Marcadores: fora de `entrega/apresentacao/` e do próprio histórico da candidata, nenhum. `entrega/apresentacao/` traz campos de papel a decidir pelo grupo (ver P-07). |
| g | Versão e estado de cada arquivo | FALHA para a aprovação | Os 113 arquivos com cabeçalho estão em 0.1 • Rascunho; o `RS_Grupo03_Evidencias.md` não tem cabeçalho. Nenhum em 0.2 e nenhum em 1.0. Isso é o esperado antes da revisão, mas a baseline só pode ser aprovada com os documentos em 1.0 • Aprovado (item 5 do checklist da candidata). |

## 4. Decisões (DEC) × estado

Estado lido do campo "Estado da decisão" de cada ficha em [`decisoes/`](../decisoes/README.md). Decididas pelo professor na Aula 7 (06/11/2026): DEC-05 a DEC-23, exceto onde o campo diz o contrário.

| DEC | Estado | Onde está a decisão |
|---|---|---|
| DEC-01, DEC-02, DEC-03 | Decidida (respostas do professor, sem data registrada) | `decisoes/DEC-01.md` a `DEC-03.md` |
| DEC-04 | Decidida (professor; grupo em 16/10/2026) | `decisoes/DEC-04.md` |
| DEC-05, DEC-07, DEC-09, DEC-13 | Decidida (Aula 7), com mudança de comportamento: CR-02, CR-03, CR-04, CR-01, todos Implementados | `DEC-05.md`, `DEC-07.md`, `DEC-09.md`, `DEC-13.md` |
| DEC-06, DEC-08, DEC-10, DEC-11, DEC-12 | Decidida (Aula 7), confirma a opção implementada; sem CR | `DEC-06.md`, `DEC-08.md`, `DEC-10.md`, `DEC-11.md`, `DEC-12.md` |
| DEC-14 a DEC-18 | Decidida (Aula 7), confirma o que o grupo já usava; sem CR | `DEC-14.md` a `DEC-18.md` |
| DEC-19 | Decidida: o professor deixou a critério do grupo, que decidiu fazer o DER | `DEC-19.md` |
| DEC-20 a DEC-23 | Decidida (Aula 7); entrega e apresentação | `DEC-20.md` a `DEC-23.md` |
| DEC-24, DEC-25 | Decidida **pelo grupo** em 10/11/2026 (REQ-11, REQ-12) | `DEC-24.md`, `DEC-25.md` |
| DEC-26, DEC-27 | Decidida **pelo grupo** em 16/11/2026 (AUT-10, AUT-11), com CR-06 e CR-07 Implementados | `DEC-26.md`, `DEC-27.md` |

Sem resposta do professor: nenhuma DEC fica sem estado. A DEC-19 (a critério do grupo) e as DEC-24 a DEC-27 foram decididas só pelo grupo; o professor não as confirmou. A CS-07 admite "decidida", mas quem aprova precisa aceitar isso explicitamente.

**PRECISA DE DECISÃO DO GRUPO:** (1) os RNF-S01 e RNF-S06 "a verificar" bloqueiam ou não a 1.0; (2) o ponto 4 do `CLAUDE.md` (grupo nas duas disciplinas) fica de fora ou vira DEC.

## 5. Achados da preparação (não corrigidos)

Encontrados pelos portões e pela leitura, ordenados por gravidade. **Nada foi corrigido**: quem decide o que corrigir é o grupo, depois da revisão.

| ID | Gravidade | Onde | Achado |
|---|---|---|---|
| P-01 | Alta | `scripts/verificar_fluxo_principal.py` | O portão falha: o diagrama `solicitar-reserva.mmd` (linha 31) põe a consulta do espaço depois de "data não retroativa", e o código chama `garantir_inicio_no_futuro` duas vezes antes de a consulta acontecer. Pode ser o diagrama ou o verificador; precisa de decisão. |
| P-02 | Alta | `entrega/RS_Grupo03_Evidencias.md` | Sem cabeçalho `ID • versão • estado`, sem autor, revisor e aprovador e sem histórico. Faz o `--verificar` da rastreabilidade (seção f) falhar, e o arquivo está no manifesto com versão e estado "—". Foi pedido para não mexer nesse arquivo; a correção cabe ao grupo. |
| P-12 | Alta | manifesto da candidata | A linha nova no [README da fonte](../README.md), pedida por esta tarefa, mudou o hash do `README.md` (IND-01); por isso o `--verificar` g ("manifesto desatualizado: README.md") passou a falhar depois da edição, embora estivesse OK no commit verificado. O manifesto não foi regenerado de propósito; rode `python scripts/gerar_rastreabilidade.py --manifesto` na parte 2, depois de qualquer correção da revisão. |
| P-03 | Alta | todos | Nenhum documento passou por revisão: todos em 0.1 • Rascunho. Sem a revisão e a promoção a 0.2, o item 1 do checklist de aprovação da candidata não pode ser marcado. |
| P-04 | Média | `entrega/` | `verificar_entrega_especificacao.py` e `verificar_apresentacao.py` falham por contagens antigas (RF 63 × 70, RN 17 × 19, US 20 × 22, UC 22 × 23, DEC 25 × 27, CR 5 × 7). A entrega de 13/11/2026 não foi alterada de propósito, e a especificação entregue precede AUT-10 e AUT-11. É preciso decidir se esses arquivos entram na 1.0 como estão, com a data da entrega. |
| P-05 | Média | `README.md` da fonte, linhas de "Estrutura" | `decisoes/` diz "DEC-01 a DEC-25" e a pasta tem 27; `casos-de-uso/` diz UC-01 a UC-19 e UC-20 a UC-22, e a fonte tem UC-23; `mudancas/` diz "CR-01 a CR-04 aprovados ... e CR-05" e há CR-07; o `mudancas/` não menciona CR-06 e CR-07. |
| P-06 | Média | `baselines/conecta-campus-1.0-candidata.md` | Texto de seção 3 desatualizado ("CR-01 a CR-04 ... aguardando implementação"); item 2 do checklist diz "pendente na AUT-12", que já foi entregue; item 3 cita TA-04, TA-185 e TA-192, mas os manuais atuais são TA-04, TA-181 e TA-188. A candidata não foi alterada. |
| P-07 | Média | `visao.md` §5, `decisoes/README.md` e outros | A Visão, o índice de DECs e a cobertura já trazem um nome de revisor e de aprovador no cabeçalho ("Revisor: ..."). Isso não é registro de revisão: o pacote não os reaproveita, e o registro só vale com a data e a confirmação da própria pessoa. Também há campos "A DEFINIR" e "[PREENCHER PELO INTEGRANTE]" em `entrega/apresentacao/` (quem responde, quem controla os slides). |
| P-08 | Média | RNF-S01, RNF-S06 | Seguem "a verificar" (CS-03 num clone novo; busca de segredos no ZIP). Dependem de uma execução humana e do ZIP. |
| P-09 | Baixa | RNF-U03 | "Verificado em parte" ([L-09](../requisitos/srs.md#l-09)): o teclado em todas as telas ficou parcial. |
| P-10 | Baixa | NS-17 | Sem RF por decisão ([DEC-24](../decisoes/DEC-24.md)); a revisão deve confirmar que isso é aceito. |
| P-11 | Baixa | SRS, seção 9 | A auditoria do próprio autor lista 9 ✘ em 103 fichas, todos com ação, 7 deles em "Completo" (DEC-13 e L-14, e L-13 no RF-17). Cabe ao revisor confirmar ou discordar na tabela da seção 10 da SRS. |

## 6. Checklists de revisão por pares

Texto copiado de [`visao.md`, seção 5](../visao.md#5-checklist-de-revisão-por-pares) e de [`srs.md`, seção 10](../requisitos/srs.md#10-checklist-de-revisão-por-pares), sem reescrever. As colunas em branco da fonte viram o campo do revisor. Um comentário útil localiza o trecho, descreve o risco e propõe uma correção.

### 6.1 Visão (VIS-01)

Preparação para a versão 0.2 (revisão por pares, A4·s7). Em branco: preenchido por um revisor do grupo que não seja o autor.

| Pergunta | Evidência dos portões | Sim/Não | Trecho e comentário |
|---|---|---|---|
| A condição de entrada de cada necessidade está clara (quem precisa, em que momento)? | Exige leitura humana | [REVISOR: ok / problema / não se aplica] | [OBSERVAÇÃO] |
| Todo termo do domínio usado aqui está no glossário, com o mesmo sentido? | Exige leitura humana (o `verificar_requisitos.py` confere links e âncoras, não o sentido) | [REVISOR: ok / problema / não se aplica] | [OBSERVAÇÃO] |
| Toda dúvida aparece como DEC, e não como regra afirmada? | Exige leitura humana; a seção 4 deste pacote lista as 27 DECs e o estado de cada | [REVISOR: ok / problema / não se aplica] | [OBSERVAÇÃO] |
| Há contradição entre seções, com o glossário ou com uma DEC? | Exige leitura humana; ver P-05 e P-06 | [REVISOR: ok / problema / não se aplica] | [OBSERVAÇÃO] |
| As opções descritas (ex.: recusar × cancelar) têm resultados distintos e verificáveis? | Exige leitura humana | [REVISOR: ok / problema / não se aplica] | [OBSERVAÇÃO] |
| Escopo e fora do escopo são excludentes e não deixam lacuna relevante? | Exige leitura humana; NS-17 fora do 1.0 pela DEC-24 (P-10) | [REVISOR: ok / problema / não se aplica] | [OBSERVAÇÃO] |
| Os critérios de sucesso são mensuráveis? | Exige leitura humana | [REVISOR: ok / problema / não se aplica] | [OBSERVAÇÃO] |

**Auditoria das necessidades** (marque ✔ ou ✘ e comente). A coluna "Rastreável" da fonte tem aqui a evidência do script (a NS chega a RF, UC, US, CA e TA, conforme a [cobertura](../rastreabilidade/cobertura.md)); o julgamento do revisor continua em branco.

| NS | Clara | Necessária | Verificável | Rastreável (evidência do script) | Rastreável (revisor) | Comentário |
|---|---|---|---|---|---|---|
| NS-01 | [REVISOR] | [REVISOR] | [REVISOR] | 6 RF, 2 UC, 4 US, 17 CA, 17 TA | [REVISOR] | [OBSERVAÇÃO] |
| NS-02 | [REVISOR] | [REVISOR] | [REVISOR] | 10 RF, 5 UC, 6 US, 33 CA, 33 TA | [REVISOR] | [OBSERVAÇÃO] |
| NS-03 | [REVISOR] | [REVISOR] | [REVISOR] | 3 RF, 2 UC, 1 US, 15 CA, 15 TA | [REVISOR] | [OBSERVAÇÃO] |
| NS-04 | [REVISOR] | [REVISOR] | [REVISOR] | 1 RF, 1 UC, 1 US, 2 CA, 2 TA | [REVISOR] | [OBSERVAÇÃO] |
| NS-05 | [REVISOR] | [REVISOR] | [REVISOR] | 5 RF, 1 UC, 1 US, 10 CA, 10 TA | [REVISOR] | [OBSERVAÇÃO] |
| NS-06 | [REVISOR] | [REVISOR] | [REVISOR] | 3 RF, 3 UC, 2 US, 14 CA, 14 TA | [REVISOR] | [OBSERVAÇÃO] |
| NS-07 | [REVISOR] | [REVISOR] | [REVISOR] | 2 RF, 3 UC, 5 US, 21 CA, 21 TA | [REVISOR] | [OBSERVAÇÃO] |
| NS-08 | [REVISOR] | [REVISOR] | [REVISOR] | 4 RF, 2 UC, 3 US, 17 CA, 17 TA | [REVISOR] | [OBSERVAÇÃO] |
| NS-09 | [REVISOR] | [REVISOR] | [REVISOR] | 9 RF, 7 UC, 9 US, 41 CA, 41 TA | [REVISOR] | [OBSERVAÇÃO] |
| NS-10 | [REVISOR] | [REVISOR] | [REVISOR] | 1 RF, 3 UC, 7 US, 15 CA, 15 TA | [REVISOR] | [OBSERVAÇÃO] |
| NS-11 | [REVISOR] | [REVISOR] | [REVISOR] | 14 RF, 8 UC, 19 US, 66 CA, 66 TA (1 manual) | [REVISOR] | [OBSERVAÇÃO] |
| NS-12 | [REVISOR] | [REVISOR] | [REVISOR] | 1 RF, 1 UC, 7 US, 15 CA, 15 TA | [REVISOR] | [OBSERVAÇÃO] |
| NS-13 | [REVISOR] | [REVISOR] | [REVISOR] | 1 RF, 11 UC, 17 US, 47 CA, 47 TA | [REVISOR] | [OBSERVAÇÃO] |
| NS-14 | [REVISOR] | [REVISOR] | [REVISOR] | 1 RF, 5 UC, 8 US, 22 CA, 22 TA | [REVISOR] | [OBSERVAÇÃO] |
| NS-15 | [REVISOR] | [REVISOR] | [REVISOR] | 7 RF, 2 UC, 3 US, 18 CA, 18 TA (1 manual) | [REVISOR] | [OBSERVAÇÃO] |
| NS-16 | [REVISOR] | [REVISOR] | [REVISOR] | 2 RF, 2 UC, 2 US, 8 CA, 8 TA (1 manual) | [REVISOR] | [OBSERVAÇÃO] |

### 6.2 SRS (SRS-01)

Preparação para a versão 0.2 (revisão por pares, A4·s7). Em branco: preenchido por um revisor do grupo que não seja o autor.

| Pergunta | Evidência dos portões | Sim/Não | Trecho e comentário |
|---|---|---|---|
| A condição de entrada de cada RF está clara (quem age, sobre o quê, em que situação)? | Exige leitura humana | [REVISOR: ok / problema / não se aplica] | [OBSERVAÇÃO] |
| Cada RF tem uma só obrigação, e os filhos mantêm o vínculo com o pai? | Em parte: `verificar_requisitos.py` seção 2 (sintaxe dos enunciados) PASSA; a obrigação única exige leitura | [REVISOR: ok / problema / não se aplica] | [OBSERVAÇÃO] |
| As opções (ex.: recusar × cancelar, inexistente × inativo) têm resultados distintos e verificáveis? | Exige leitura humana | [REVISOR: ok / problema / não se aplica] | [OBSERVAÇÃO] |
| Há contradição entre RFs, com o glossário, com a Visão ou com uma DEC? | Em parte: `--verificar` e (impacto por DEC) PASSA; contradição de sentido exige leitura | [REVISOR: ok / problema / não se aplica] | [OBSERVAÇÃO] |
| Toda recusa (F5) diz o que fica preservado e o que é informado? | Em parte: `verificar_casos_de_uso.py` seção 6 confere as quatro partes das exceções das fichas de UC; os RF exigem leitura | [REVISOR: ok / problema / não se aplica] | [OBSERVAÇÃO] |
| Todo RNF tem métrica, valor-alvo e forma de verificar? | Forma de verificar existe nos 33 RNF ([rastreabilidade dos RNF](../rastreabilidade/rnf.md)); métrica e valor-alvo exigem leitura; RNF-S01 e RNF-S06 "a verificar" (P-08) | [REVISOR: ok / problema / não se aplica] | [OBSERVAÇÃO] |
| Toda dúvida aparece como DEC ou lacuna, e não como regra afirmada? | Exige leitura humana; lacunas aceitas na seção 4 da candidata | [REVISOR: ok / problema / não se aplica] | [OBSERVAÇÃO] |
| A evidência citada existe e prova o enunciado (conferir uma amostra)? | Existência: PASSA (`verificar_historias.py` seção 5 e `--verificar` d, símbolos de código); "prova o enunciado" exige uma amostra lida | [REVISOR: ok / problema / não se aplica] | [OBSERVAÇÃO] |
| Algum termo vago ou de solução (tela, botão, tecnologia) ficou num enunciado? | Termos vagos: 0 (`verificar_requisitos.py` seção 3); termos de interface nas fichas de UC: PASSA (seção 9 de `verificar_casos_de_uso.py`) | [REVISOR: ok / problema / não se aplica] | [OBSERVAÇÃO] |

**Auditoria do revisor** (marque ✔ ou ✘ onde discordar da [seção 9](../requisitos/srs.md#9-auditoria-de-qualidade) e comente):

| ID | Critério em que discorda | Comentário |
|---|---|---|
| [REVISOR] | [REVISOR] | [OBSERVAÇÃO] |

### 6.3 Resultados da seção 3 que ainda pedem leitura

| Critério | O que o revisor confere |
|---|---|
| b | Aceitar (ou não) que DEC-24 a DEC-27 e a parte da DEC-19 dependam só do grupo. |
| c | Ler as exceções de rastreabilidade (NS-17 e RF-38) e a justificativa de cada uma. |
| d | Resposta do grupo sobre RNF-S01 e RNF-S06 (bloqueiam ou não). |
| e | Ler P-05 e P-06 e dizer quais viram correção. |

[REVISOR: ok / problema / não se aplica] [OBSERVAÇÃO]

## 7. Achados da revisão

Preenchida pelos revisores. Um achado por linha. Gravidade: Alta (bloqueia a baseline), Média (corrigir antes de aprovar ou aceitar com justificativa), Baixa (editorial).

| ID | Artefato | Achado | Gravidade | Decisão |
|---|---|---|---|---|
| | | | | |

## 8. Registro de revisão e aprovação

**Regra:** "revisão por pares" só vale se o revisor for **diferente** do autor do artefato. Se o mesmo integrante escreveu e revisou, o registro deve dizer **"autorrevisão"**, e a revisão não conta como por pares. Nenhum campo abaixo foi preenchido pela preparação.

| Campo | Conteúdo |
|---|---|
| Autor(es) dos artefatos | [PREENCHER] |
| Revisor(es) | [PREENCHER] |
| Data da revisão | [PREENCHER] |
| Aprovado por | [PREENCHER] |
| Data da aprovação | [PREENCHER] |
| Referência Git revisada (commit) | [PREENCHER] |
| Decisão | [PREENCHER] |
