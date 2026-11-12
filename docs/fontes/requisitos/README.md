# Requisitos do Conecta Campus — fonte oficial

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **IND-01 • 0.1 • Rascunho** (índice da fonte oficial) | Autor: Max Zimmermann dos Reis • Revisor: a definir • Aprovador: a definir | `docs/fontes/requisitos/` |

Esta pasta é a **fonte oficial** dos requisitos do Conecta Campus (disciplina de Requisitos de Software), versionada no Git e organizada como no modelo do professor (A4·s10). O que vale é o que está aqui: outros arquivos (README do projeto, `modelagem.pdf`, mensagens no chat) apontam para esta pasta e não são cópias editáveis. Um PDF gerado daqui serve só para consulta e mostra a versão e a origem.

`docs/fontes/` não entra no ZIP de entrega de Projeto de Programação; os PDFs entregues são gerados a partir destes arquivos.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Criação (REQ-01; data do commit, o arquivo não tinha histórico). As REQ-02 a REQ-05 acrescentaram as próprias decisões de organização. Sem aprovação. |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Cabeçalho completado (REQ-06). Estrutura com [`rastreabilidade/`](rastreabilidade/README.md); identificadores de documento IND, RAS, PAU, MCR e BL; rastreabilidade descrita até o código, com link para a matriz gerada; decisões de organização da REQ-06. Sem aprovação. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Respostas da Aula 7 (GES-02): estrutura com DEC-01 a DEC-23 e CR-01 a CR-04; decisões c (REQ-01) e c (REQ-02), a rastreabilidade e os pontos a confirmar apontam para as DEC-14 a DEC-19. Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Contagens de RF (61), RNF (32), CAs (157) e TAs (TA-01 a TA-157) atualizadas; renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Contagem de CAs (158) e TAs (TA-01 a TA-158), com o CA-03 da US-19 (AUT-08). Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | Contagens de RNF (33), CAs (161) e TAs (TA-01 a TA-161), com o RNF-F13 e os CAs novos da US-03; renumeração dos TAs: TA-19 e TA-20 passam a TA-20 e TA-21, e TA-21 a TA-158 passam a TA-24 a TA-161 (AUT-09). Sem aprovação. |
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Contagens de RF (62 fichas, com o RF-12.2), CAs (168) e TAs (TA-01 a TA-168), com os CAs novos das US-10 e US-11; renumeração dos TAs: TA-96 a TA-107 passam a TA-97 a TA-114, conforme as histórias, e TA-108 a TA-161 passam a TA-115 a TA-168 (RES-10). Sem aprovação. |
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Estrutura com [`levantamento/`](levantamento/README.md): técnicas de levantamento, roteiros ROT-01 a ROT-03, guia do entrevistador, modelo de registro e a ENT-01; identificadores `ENT`, `ROT`, `IND-05`, `GUI-01` e `MRE-01` (REQ-09). Sem aprovação. |
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Questionário QST-01 em [`levantamento/questionario/`](levantamento/questionario/QST-01-questionario.md): instrumento, plano de aplicação e modelo de síntese; identificador `QST` (REQ-10). Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Síntese do levantamento em [`levantamento/`](levantamento/sintese-do-levantamento.md) e a versão de evidência de 1 página; NS-17 na Visão e DEC-24 em [`decisoes/`](decisoes/README.md); identificador `SIN` (REQ-11). Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Papéis Atendente responsável e Gestor do serviço, com o perfil único do sistema mínimo ([DEC-25](decisoes/DEC-25.md)); catálogo de regras de negócio RN-01 a RN-17 em [`requisitos/regras-de-negocio.md`](requisitos/regras-de-negocio.md) e a rastreabilidade gerada das RN; CR-05 proposto para os artefatos de ator misto (REQ-12). Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Aplicação na especificação dos CR-01 a CR-04 (REQ-13): RF-24.1 novo (63 fichas), 193 CAs e 193 TAs (25 pendentes, com o código nas tarefas RES-11, RES-12, ESP-07 e AUT-12). A especificação está adiante do código de propósito. Mudança comportamental da especificação. Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Pasta [`entrega/`](entrega/RS_Grupo03_Especificacao.md): texto do documento principal de Requisitos para a entrega de 13/11/2026 (REQ-08), em um só arquivo Markdown, com a figura do diagrama de casos de uso; o PDF é montado pelo grupo a partir dele. Conferido por `scripts/verificar_entrega_especificacao.py`. Fica fora do ZIP de código (DEC-20). Sem aprovação. |

## Estrutura

| Caminho | O que contém | Situação |
|---|---|---|
| [`visao.md`](visao.md) | **VIS-01**, Documento de Visão (RUP, 4 quadrantes): problema, stakeholders, necessidades NS-xx, escopo, premissas, critérios de sucesso e riscos. | 0.1 • Rascunho (REQ-01) |
| [`glossario.md`](glossario.md) | **GLO-01**, termos do domínio com definição única e o nome correspondente no código. | 0.1 • Rascunho (REQ-01) |
| [`requisitos/`](requisitos/README.md) | **SRS-01** ([`srs.md`](requisitos/srs.md)) e as fichas A4·s9: RF-01 a RF-40 (com o catálogo de [regras de negócio](requisitos/regras-de-negocio.md), RN-01 a RN-17) (63 fichas, por área) e RNF-F01 a RNF-S06 (33, por FURPS). | 0.1 • Rascunho (REQ-02) |
| [`casos-de-uso/`](casos-de-uso/README.md) | **UCD-01** (diagrama do negócio, UC-01 a UC-19) e **UCD-02** (diagrama de apoio "Administração", UC-20 a UC-22) em PlantUML, com as imagens geradas, o índice dos UCs e a rastreabilidade RF → UC (REQ-03); fichas Cockburn completas de UC-02, UC-04, UC-10 e UC-14, resumidas dos demais e o fluxo de decisão de UC-04 (REQ-04). | 0.1 • Rascunho (REQ-03, REQ-04) |
| [`historias/`](historias/README.md) | **HIS-01**: histórias US-01 a US-20 (Index Card e INVEST), 193 critérios de aceite CA-xx em Dado/Quando/Então e os testes de aceite TA-01 a TA-189, ligados aos testes que existem (25 deles pendentes, ligados à tarefa de código que implementa a regra nova), com a cobertura UC → US/CA e a rastreabilidade RF → US/CA. | 0.1 • Rascunho (REQ-05) |
| [`decisoes/`](decisoes/README.md) | DEC-xx, uma decisão por arquivo, com índice e a [pauta da Aula 7](decisoes/pauta-aula-7.md). | DEC-01 a DEC-25, todas decididas (DEC-01 a DEC-23 na Aula 7; DEC-24 e DEC-25 pelo grupo, REQ-11 e REQ-12) |
| [`mudancas/`](mudancas/README.md) | CR-xx, pedidos de mudança, e o [modelo de CR](mudancas/modelo-cr.md). | CR-01 a CR-04 aprovados e aplicados na especificação, com o código pendente nas tarefas RES-11, RES-12, ESP-07 e AUT-12 (REQ-13); CR-05 aplicado na especificação (REQ-13) |
| [`baselines/`](baselines/README.md) | Manifestos de baseline (conjunto aprovado de versões). | [candidata à 1.0](baselines/conecta-campus-1.0-candidata.md), aguardando aprovação (REQ-06) |
| [`levantamento/`](levantamento/README.md) | **IND-05**: técnicas de levantamento do grupo (entrevista semiestruturada na REQ-09; questionário na REQ-10), roteiros de entrevista ROT-01 a ROT-03, [guia do entrevistador](levantamento/guia-do-entrevistador.md), modelo de registro e os registros ENT-xx (ENT-01, com o representante do cliente na Aula 7; as demais planejadas), e o [questionário QST-01](levantamento/questionario/QST-01-questionario.md) com plano de aplicação e modelo de síntese (instrumento pronto, sem respostas) e a [síntese do levantamento](levantamento/sintese-do-levantamento.md) (SIN-01, com a [versão de evidência](levantamento/sintese-evidencia-1pag.md)): 23 achados com destino, a NS-17 e a DEC-24. | 0.1 • Rascunho (REQ-09, REQ-10, REQ-11) |
| [`rastreabilidade/`](rastreabilidade/README.md) | **RAS-01**: [matriz](rastreabilidade/matriz.md) NS → RF → UC → US → CA/TA → endpoint ou tela → código (e [`matriz.csv`](rastreabilidade/matriz.csv)), [cobertura](rastreabilidade/cobertura.md), [sentido inverso](rastreabilidade/sentido-inverso.md), [RNF](rastreabilidade/rnf.md) e [mapa de impacto por DEC](rastreabilidade/impacto-por-dec.md), gerados por `scripts/gerar_rastreabilidade.py`. | 0.1 • Rascunho (REQ-06) |
| [`entrega/`](entrega/RS_Grupo03_Especificacao.md) | **RS_Grupo03_Especificacao.md**: texto da especificação para a entrega de 13/11/2026 (capa, 11 seções na ordem do enunciado e anexos), gerado da fonte oficial com os identificadores RF01, RNF01 e RN01, mais `figuras/` com o diagrama de casos de uso. Não entra no ZIP de código. | 0.1 • Rascunho (REQ-08) |

## Decisões de organização (REQ-01)

- **a) Fonte única.** Esta pasta é a fonte oficial. Nenhum outro lugar mantém uma cópia editável dos requisitos; os demais apontam para cá.
- **b) Decisões aqui.** As DECs saíram de `.claude/requisitos.md` (diretrizes locais da disciplina, fora do Git) e moram em [`decisoes/`](decisoes/README.md). As diretrizes de como documentar continuam naquele arquivo.
- **c) Convenção de versão** (abaixo), a do slide A4·s15. O próprio slide avisa que ela não é regra universal; o professor a confirmou na Aula 7 ([DEC-17](decisoes/DEC-17.md)).
- **d) Nada inventado.** O que o grupo não sabe (quem é o cliente real, o horário real de funcionamento, o formato da matrícula) aparece como premissa declarada na [Visão](visao.md#premissas) ou como DEC, nunca como afirmação.

## Decisões de organização (REQ-02)

- **a) SRS e fichas por área.** [`requisitos/srs.md`](requisitos/srs.md) é o documento principal, com as seis seções do A3·s8, os índices e as tabelas de rastreabilidade. As fichas ficam agrupadas por área, uma ficha por requisito: `rf-espacos.md`, `rf-reservas.md`, `rf-agenda.md`, `rf-contas.md`, `rf-gerais.md` e `rnf.md` (o README da pasta permite um arquivo por requisito ou por grupo). Cada ficha tem uma âncora explícita (`<a id="rf-11-4">`) para os links não dependerem do título.
- **b) Comportamento real.** A SRS descreve o que o sistema faz hoje, conferido nos testes e no código. O que uma NS pede e o sistema não faz entra na seção [Lacunas](requisitos/srs.md#lacunas) (e, se fosse um RF inteiro, com estado "Não implementado"). Nenhum código muda por causa da SRS: divergência vira lacuna, DEC ou CR.
- **c) Vínculos e evidência.** UC, US e CA ficam "a definir (REQ-03, REQ-04, REQ-05)". O vínculo com a implementação (endpoint ou tela e `arquivo::teste`) fica numa coluna **Evidência (complementar)**, porque a cadeia do professor para em CA/TA; o professor confirmou depois que o elo até o código conta ([DEC-16](decisoes/DEC-16.md)).
- **d) Versão.** Todos os documentos da REQ-02 nascem em 0.1 • Rascunho. A Visão e o glossário ganham uma linha no histórico (vínculos NS → RF e termos novos), sem mudar de versão.
- **Recusas (F5).** A recusa específica de uma operação é um filho `RF-xx.n`; a que vale para várias operações do mesmo item é um RF próprio, com as operações protegidas na ficha. As recusas usam a sintaxe "O sistema deve impedir que…" (justificativa na [SRS, seção 3](requisitos/srs.md#como-ler)).
- **IDs de documento.** `SRS-01` identifica a SRS; `REST-xx` identifica as restrições (o "+" de FURPS+) em [`rnf.md`](requisitos/rnf.md#6-restrições); `L-xx`, as lacunas da SRS.

## Decisões de organização (REQ-03)

- **a) Diagramas como texto.** Os diagramas de casos de uso são fontes PlantUML (`.puml`) versionadas; os `.svg` e `.png` ao lado são gerados por Docker e nunca editados à mão (comando e justificativa no [README da pasta](casos-de-uso/README.md#como-gerar-as-imagens)).
- **b) Decisões de modelagem no README da pasta.** Granularidade, notação, generalização, autenticação como precondição, Equipe de TI à parte e ausência de sistema externo: [decisões a) a g)](casos-de-uso/README.md#decisões-de-modelagem).
- **c) Vínculo RF → UC em três lugares, uma fonte.** A tabela de [rastreabilidade RF → UC](casos-de-uso/README.md#rastreabilidade-rf--uc) é a fonte; a coluna UC da [SRS, seção 6.4](requisitos/srs.md#64-rf--evidência-uc-us-e-ca) e o campo "Vínculos" de cada ficha repetem o UC principal, e `scripts/verificar_casos_de_uso.py` confere que os três batem. Desde a REQ-06, a 6.4 não repete mais o UC: ele está na matriz gerada.
- **d) Versão.** O README de casos de uso nasce em 0.1 • Rascunho; a SRS, as fichas e o glossário ganham uma linha no histórico, sem mudar de versão.

## Decisões de organização (REQ-05)

- **a) Histórias por fatia de valor.** As US saem dos casos de uso de objetivo, uma ou mais por caso de uso; as subfunções aparecem como CAs, e F5 e F6 não têm história própria. Fatiamento, numeração (CA dentro da história, TA global), Index Card, INVEST, ordem dos CAs, linguagem e DECs: [decisões a) a h)](historias/README.md#decisões-de-organização-req-05).
- **b) Uma fonte, vários espelhos.** Cada história é a fonte dos seus CAs e TAs; o índice dos TAs do README de `historias/`, o campo Vínculos das fichas de RF, as colunas US e CA da SRS 6.4 e a coluna Histórias do índice de casos de uso repetem esses vínculos, e `scripts/verificar_historias.py` confere que batem. Desde a REQ-06, a 6.4 não repete mais US e CA: eles estão na matriz gerada.
- **c) Versão.** O README de `historias/` e cada história nascem em 0.1 • Rascunho; a SRS, as fichas de RF, as fichas de caso de uso e o glossário ganham uma linha no histórico, sem mudar de versão.

## Decisões de organização (REQ-06)

- **a) Matriz gerada, nunca escrita à mão.** [`rastreabilidade/`](rastreabilidade/README.md) é montada por `scripts/gerar_rastreabilidade.py` a partir das fichas, dos casos de uso, das histórias e da matriz de acesso; para mudar um vínculo, muda-se a ficha de origem. O `--verificar` falha se a matriz ficou para trás. Decisões a) a f) no [README da pasta](rastreabilidade/README.md#decisões-de-organização-req-06).
- **b) Código como vínculo complementar da ficha.** Cada ficha de RF ganhou o campo **Código (complementar)** (`arquivo::Símbolo`), ao lado da Evidência; a coluna Código da matriz sai dele.
- **c) Sem cópias.** A SRS 6.4 ficou só com o teste representativo de cada RF; UC, US, CA e TA estão na matriz. Os READMEs de `casos-de-uso/` e `historias/` só apontam para ela.
- **d) Cabeçalho e histórico em todo documento**, inclusive os índices das pastas (IND-01 a IND-04), conferidos pelo script. Datas e aprovações não foram inventadas: a criação dos índices tem a data do commit, e o revisor e o aprovador dos documentos novos ficam "a definir".
- **e) Baseline só candidata.** A [referência candidata à 1.0](baselines/conecta-campus-1.0-candidata.md) traz o manifesto com o SHA-256 de cada artefato; nada foi aprovado e nenhum estado mudou.

## Identificadores

| Prefixo | Artefato | Onde |
|---|---|---|
| `NS` | Necessidade | [`visao.md`](visao.md#necessidades) |
| `RF` / `RNF` | Requisito funcional / não funcional (FURPS) | `requisitos/` |
| `UC` | Caso de uso | `casos-de-uso/` |
| `US` | História de usuário | `historias/` |
| `CA` / `TA` | Critério de aceite / teste de aceite | `historias/` |
| `DEC` | Decisão | `decisoes/` |
| `CR` | Pedido de mudança | `mudancas/` |
| `A2.1`, `E5` | Alternativa / exceção ligada ao passo de um UC | dentro do UC |
| `ROT` / `ENT` | Roteiro de entrevista / registro de entrevista (perguntas numeradas no roteiro: `ROT-02 P03`) | `levantamento/entrevistas/` |
| `QST` | Questionário (perguntas numeradas: `QST-01-P03`) | `levantamento/questionario/` |
| `SIN` / `ACH` | Síntese do levantamento / achado dela (`ACH-01`…) | `levantamento/` |

Convenções do grupo, além das do professor: `VIS-01` e `GLO-01` identificam os documentos; `P-xx` (premissa), `CS-xx` (critério de sucesso) e `R-xx` (risco) valem dentro da Visão. Desde a REQ-06: `IND-01` a `IND-04` (este README e os índices de `decisoes/`, `mudancas/` e `baselines/`), `RAS-01` (rastreabilidade), `PAU-01` (pauta da Aula 7), `MCR-01` (modelo de CR) e `BL-01` (manifesto da baseline candidata); `L-xx` são as lacunas da SRS. Desde a REQ-09: `IND-05` (índice de `levantamento/`), `GUI-01` (guia do entrevistador) e `MRE-01` (modelo de registro de entrevista). Desde a REQ-10: `QST-01` (questionário; as perguntas são `QST-01-P01`…).

Regras (A4·s8):

- **Um ID, uma obrigação principal.** Um requisito com duas obrigações é decomposto mantendo o vínculo com o pai: `RF-04.1 • solicitação`, `RF-04.2 • confirmação`.
- **IDs estáveis.** Um ID não muda quando o texto muda e **nunca é reutilizado**, nem depois de removido ou substituído.
- Números com dois dígitos (`NS-01`, `DEC-05`).

## Versão e estado

**Versão ≠ estado ≠ baseline** (A4·s14). Versão diz qual conteúdo; estado diz em que situação ele está; baseline diz qual conjunto foi acordado. Salvo não é aprovado, commit não é aprovação e push não é publicação de baseline.

| Versão | Estado | Quando |
|---|---|---|
| 0.1 | Rascunho | Criação, ainda sem revisão. Todos os documentos da REQ-01 nascem aqui. |
| 0.2 | Em revisão | Depois da revisão por pares (checklist no fim da [Visão](visao.md#5-checklist-de-revisão-por-pares)). |
| 1.0 | Aprovado | Primeira baseline aprovada, com manifesto em `baselines/`. |
| 1.1, 1.2… | Aprovado | Próximas baselines, cada uma por um CR aprovado. |

Quando uma versão aprovada é trocada, a anterior fica marcada como **Substituída**, nunca apagada. A versão do documento não é a release do software.

Cada documento traz no topo `[ID] • [versão] • [estado]`, autor, revisor e aprovador, e um histórico de revisões (versão | data | autor | alteração e referência da aprovação), como no template A4·s11.

## Como propor uma mudança

Antes da primeira baseline, os documentos mudam por PR, com a linha nova no histórico de revisões. Depois dela, toda mudança passa por um **CR** em [`mudancas/`](mudancas/README.md), no fluxo do A4·s20:

1. **Registrar:** quem pede, o motivo e o escopo.
2. **Analisar:** artefatos afetados nos dois sentidos da rastreabilidade ("de onde veio a regra e onde seu efeito precisa aparecer?"), risco e esforço. Classificar como **editorial** (corrige o texto, mesma obrigação) ou **comportamental** (nova regra: impacto e decisão). O tamanho do diff não mede o risco.
3. **Decidir:** o aprovador do documento (Eduardo Almeida da Cunha) aceita, rejeita ou adia. Se a resposta depender do professor ou do cliente, abre-se uma DEC.
4. **Atualizar:** requisitos, casos de uso, histórias, critérios e testes vinculados, no mesmo PR. A baseline vigente continua valendo até a nova ser aprovada.
5. **Verificar:** o revisor confere a coerência e a regressão; publica-se a nova baseline.

Uma proposta vai numa branch própria (`docs/CR-xx-<assunto>`). Um CR rejeitado ou adiado fica registrado com a justificativa.

## Rastreabilidade

Cadeia do professor (A3·s8), bidirecional, com o elo do código acrescentado pelo grupo:

```
NS-xx → RF-xx → UC-xx (passo, alternativa ou exceção) → US-xx → CA-xx / TA-xx → endpoint ou tela → código
```

- **A matriz completa, nos dois sentidos, está em [`rastreabilidade/`](rastreabilidade/README.md)** (REQ-06): a [matriz](rastreabilidade/matriz.md) com uma linha por RF, a [cobertura](rastreabilidade/cobertura.md) por elo, por NS e por funcionalidade, o [sentido inverso](rastreabilidade/sentido-inverso.md) (cada rota, tela e comando → RF → NS), os [RNF](rastreabilidade/rnf.md) com a forma de verificação e o [mapa de impacto por DEC](rastreabilidade/impacto-por-dec.md). Ela é **gerada** a partir dos vínculos das fontes abaixo por `python scripts/gerar_rastreabilidade.py`, e o `--verificar` falha se uma ficha mudar e a matriz ficar para trás. Exemplo de cadeia inteira (NS-04): [README da pasta](rastreabilidade/README.md#exemplo-de-cadeia-completa-ns-04-nunca-dois-usos-no-mesmo-período).
- Os slides param em CA/TA. O elo até o endpoint, a tela e o código é uma extensão do grupo (colunas complementares da matriz, a partir dos campos Evidência e Código de cada ficha), confirmada pelo professor ([DEC-16](decisoes/DEC-16.md)).
- Hoje existem as NS ([Visão](visao.md#necessidades)), os RF e RNF derivados delas ([SRS, seção 6](requisitos/srs.md#6-rastreabilidade): NS → RF, RF → F1–F6, RF/RNF → DEC e RF → evidência), os casos de uso com a [rastreabilidade RF → UC](casos-de-uso/README.md#rastreabilidade-rf--uc) (REQ-03) e as fichas que ligam cada RF a um passo, alternativa ou exceção (REQ-04), e as evidências do lado do código: [catálogo de testes de espaços](../testes_de_espacos.md), [catálogo de testes de reservas](../testes_de_reservas.md) e [matriz de acesso](../matriz_de_acesso.md). Desde a REQ-05, as [histórias](historias/README.md) completam a cadeia até CA/TA: cada RF aponta para os CAs que o verificam, e cada TA, para os testes automatizados ou para um roteiro manual. Essas são as fontes que a matriz da REQ-06 lê.
- `python scripts/verificar_requisitos.py` (na raiz) confere que toda NS tem RF, que todo RF tem NS, a sintaxe dos enunciados, os termos vagos e os links e âncoras desta pasta.
- `python scripts/verificar_casos_de_uso.py` (na raiz) confere que os UCs dos diagramas e do índice são os mesmos, que todo RF tem UC (na tabela RF → UC, na SRS e na ficha), a notação dos diagramas, se as imagens estão atualizadas e, desde a REQ-04, as fichas de caso de uso (RF ligados a âncoras, passos citados, as quatro partes das exceções, termos de interface e o fluxo de decisão).
- `python scripts/verificar_historias.py` (na raiz), desde a REQ-05, confere o Index Card e o INVEST de cada história, os CAs (Dado/Quando/Então, origem, RF e TA), a cobertura de cada alternativa e exceção das fichas, o RF → US/CA nas fichas e na SRS, a existência de cada teste citado num TA, a sequência dos IDs e a linguagem dos CAs.
- `python scripts/gerar_rastreabilidade.py --verificar` (na raiz), desde a REQ-06, confere que a matriz gerada está atualizada, que toda NS chega a um TA, que todo RF tem UC, US e CA (ou uma lacuna que justifica), o sentido inverso, os símbolos de código, as DECs, o cabeçalho e o histórico de todo documento e o manifesto da [baseline candidata](baselines/conecta-campus-1.0-candidata.md).
- A matriz responde a três perguntas: **impacto** (que artefatos são afetados?), **cobertura** (todo requisito tem teste?) e **justificativa** (que necessidade o originou?).

## Pontos a confirmar com o professor

A lista não é copiada aqui. Ela está em dois arquivos locais, fora do Git (por isso citados como caminho, sem link):

- `CLAUDE.md`, seção "Pontos a Confirmar com o Professor": os pontos 1, 2, 3 e 6 já foram respondidos ([DEC-01](decisoes/DEC-01.md), [DEC-02](decisoes/DEC-02.md), [DEC-03](decisoes/DEC-03.md) e [DEC-04](decisoes/DEC-04.md)); o ponto 5 foi respondido na Aula 7 ([DEC-15](decisoes/DEC-15.md)); o ponto 4 segue aberto (não foi perguntado).
- `.claude/requisitos.md`, seção "Pontos de Atenção / A Confirmar com o Professor": os pontos 4, 5, 6, 10 e 13 foram respondidos na Aula 7 (06/11/2026) e viraram a [DEC-19](decisoes/DEC-19.md), a [DEC-14](decisoes/DEC-14.md), a [DEC-18](decisoes/DEC-18.md), a [DEC-17](decisoes/DEC-17.md) e a [DEC-16](decisoes/DEC-16.md); os demais não foram perguntados. O resultado de cada item está na [pauta da Aula 7](decisoes/pauta-aula-7.md#resultado).

Quando um ponto for respondido, a resposta vira uma DEC em [`decisoes/`](decisoes/README.md).
