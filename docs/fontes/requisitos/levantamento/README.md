# Levantamento de requisitos

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **IND-05 • 0.1 • Rascunho** (índice do levantamento) | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/levantamento/` |

Instrumentos e registros das técnicas de levantamento do Conecta Campus (enunciado do Projeto Final de Requisitos, §5.3, §6 "Levantamento" e §7). Esta pasta guarda **o que foi perguntado e o que foi respondido**; as consequências dos achados nos requisitos (Visão, NS, DECs) estão na [síntese do levantamento](sintese-do-levantamento.md) (REQ-11). O que exige mudar RF, casos de uso ou histórias fica nas pendências da REQ-13.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Criação: técnicas, plano e status das entrevistas, decisões a) a i), roteiros ROT-01 a ROT-03, modelo de registro, guia do entrevistador e o registro da ENT-01 (REQ-09). Sem aprovação. |
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Entrevistas ENT-02 a ENT-04 registradas como (perfis fictícios, com aviso em cada arquivo); tabela de status e contagem de representantes por papel (REQ-09). Sem aprovação. |
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Questionário QST-01: instrumento, versão impressa, plano de aplicação e modelo da síntese; status "instrumento pronto, aguardando aplicação"; sem respostas (REQ-10). Sem aprovação. |
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Aplicação do QST-01 (N = 18, dados não reais): síntese, versão de evidência de 1 página, status das técnicas e conclusão sobre o enunciado (REQ-10). Sem aprovação. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Síntese concluída (SIN-01): 23 achados com destino, NS-17, DEC-24, versão de evidência de 1 página e pendências para a REQ-13 (REQ-11). Sem aprovação. |

## Técnicas do grupo

| # | Técnica | Tarefa | Com quem | Situação |
|---|---|---|---|---|
| 1 | **Entrevista semiestruturada** (roteiro com perguntas abertas e aprofundamentos livres) | REQ-09 | Representante do cliente, Solicitantes e Atendente responsável | ENT-01 realizada (real); ENT-02 a ENT-04 |
| 2 | **Questionário anônimo** ([QST-01](questionario/QST-01-questionario.md)) | REQ-10 | Solicitantes (estudantes e servidores que usam ou já quiseram usar espaços esportivos do campus) | **Aplicação**: instrumento pronto; N = 18 respostas, sem período de campo; resultados em [QST-01-resultados.md](questionario/QST-01-resultados.md) |

**Por que a entrevista.** Cada perfil sabe coisas diferentes: o cliente define as regras de uso, o Solicitante conhece o pedido do lado de quem usa, e o Atendente responsável conhece o pedido do lado de quem decide e opera os espaços. A entrevista também cumpre a exigência de interação com pelo menos dois representantes de stakeholders (§5.3). Os papéis Atendente responsável (servidor que opera os espaços: confirma, recusa e conclui) e Gestor do serviço (cadastra espaços e define as regras) são os da REQ-12.

**A ENT-01 e o "cliente sem tempo" (A1·s30).** Na leitura do grupo, a pauta da Aula 7 foi a estratégia para um cliente com pouco tempo: perguntas curtas, cada uma com a opção já adotada e o impacto se a resposta fosse outra, para o professor só confirmar ou corrigir.

## Plano e status das entrevistas

| ID | Perfil do entrevistado | Roteiro | Quando | Entrevistador | Status |
|---|---|---|---|---|---|
| [ENT-01](entrevistas/ENT-01-representante-do-cliente.md) | Professor da disciplina, no papel de representante do cliente (instituição), [premissa P-01](../visao.md#premissas) | [ROT-01](entrevistas/ROT-01-representante-do-cliente.md) | 06/11/2026 (Aula 7) | Max Zimmermann dos Reis | Realizada |
| [ENT-02](entrevistas/ENT-02-solicitante-estudante-simulada.md) | Solicitante (estudante), perfil **fictício** | [ROT-02](entrevistas/ROT-02-solicitante.md) | Sem data de campo |
| [ENT-03](entrevistas/ENT-03-solicitante-servidor-simulada.md) | Solicitante (servidor), perfil **fictício** | [ROT-02](entrevistas/ROT-02-solicitante.md) |
| [ENT-04](entrevistas/ENT-04-atendente-responsavel-simulada.md) | Atendente responsável, perfil **fictício** | [ROT-03](entrevistas/ROT-03-atendente-responsavel.md) |

### Representantes por papel

| Papel | Real | Simulado | Entrevistas |
|---|---|---|---|
| Cliente (instituição) | 1 | 0 | ENT-01 |
| Solicitante | 0 | 2 | ENT-02, ENT-03 |
| Atendente responsável | 0 | 1 | ENT-04 |
| **Total** | **1** | **3** | 4 representantes em 3 papéis |

**Mínimo do enunciado (§5.3): atingido** (pelo menos dois representantes de stakeholders na mesma técnica), mas **só com os simulados**: o único representante real é a ENT-01. Se o grupo conseguir entrevistar uma pessoa real até a entrega, ela entra como ENT-05 (o ID não é reaproveitado) e fortalece a evidência.

### Conclusão sobre o enunciado (§5.3, §6 e §7)

| Exigência | Situação |
|---|---|
| Duas técnicas de levantamento | **Aplicadas**: entrevista (REQ-09) e questionário (REQ-10). |
| Interação com pelo menos dois representantes de stakeholders | Entrevistas: 4 representantes em 3 papéis (ENT-01 a ENT-04), dos quais **1 real** (ENT-01, cliente) e 3 simulados. O mínimo é atingido só com os simulados. |
| Instrumentos, participantes sem dado pessoal sensível, síntese e decisões | Instrumentos: ROT-01 a ROT-03 e QST-01. Participantes: perfis genéricos. Síntese: [QST-01-resultados.md](questionario/QST-01-resultados.md) e [sintese-do-levantamento.md](sintese-do-levantamento.md) (**concluída em 10/11/2026**, REQ-11). Decisões resultantes: NS-17 e [DEC-24](../decisoes/DEC-24.md), com a [versão de evidência](sintese-evidencia-1pag.md). |
| PDF de evidências (até 8 páginas) | O questionário entra em duas peças de 1 página: [versão impressa](questionario/QST-01-versao-impressa.md) e [versão de evidência](questionario/QST-01-resultados-evidencia.md). Cada peça deve dizer o que é simulado. |

Cada entrevista realizada ganha um arquivo `entrevistas/ENT-xx-<perfil>.md`, no formato do [modelo de registro](entrevistas/modelo-registro-entrevista.md). Uma entrevista planejada que não acontecer fica nesta tabela como **Cancelada**, com o motivo; o ID não é reaproveitado.

## Questionário (REQ-10)

Segunda técnica do grupo. O instrumento, o plano e o modelo da síntese vieram primeiro.

| Item | Situação |
|---|---|
| Instrumento | [QST-01](questionario/QST-01-questionario.md): 11 perguntas (9 obrigatórias), anônimo, cerca de 3 minutos (estimativa, a confirmar no piloto) |
| Aplicação | [Plano](questionario/plano-de-aplicacao.md): meta de 15 respostas, de 10/11 a 12/11/2026 (encerra às 12:00), piloto com 2 colegas |
| Síntese | [Modelo](questionario/modelo-sintese-questionario.md) preenchido em [QST-01-resultados.md](questionario/QST-01-resultados.md); resumo de 1 página em [QST-01-resultados-evidencia.md](questionario/QST-01-resultados-evidencia.md) |
| Status | **Aplicação** (09/11/2026): 18 respostas geradas pelo grupo. O plano de campo (10/11 a 12/11) não foi executado. |

Decisões:

- **a) Identificador.** `QST-01`, estável e nunca reutilizado; um próximo questionário seria `QST-02`. Cabeçalho `ID • versão • estado` e histórico, como os demais.
- **b) Público.** Só Solicitantes. O Atendente responsável e o Gestor do serviço ficam com as entrevistas, porque o que eles sabem (decidir, operar, definir regras) cabe mal em perguntas fechadas.
- **c) Forma.** Anônimo: não se coleta e-mail, nome, matrícula, curso nem turma. De 9 a 11 perguntas, até 3 minutos. A abertura diz o objetivo, que é anônimo e que as respostas só servem ao trabalho da disciplina.
- **d) Perguntas ligadas aos requisitos.** Cada pergunta tem, na tabela interna do QST-01, a NS, a regra ou a DEC que ela pode confirmar ou contestar; o que não tem ligação é marcado "possível necessidade nova", sem criar NS (isso é da REQ-11). As perguntas de perfil (P01, P02) são contexto e não confirmam NS.
- **e) Regras de escrita.** Neutras e sobre a situação, nunca sobre solução, tela, aplicativo, site ou tecnologia. A opção "Peço por e-mail ou formulário" (P03) descreve a prática de hoje. Opções que se excluem e cobrem os casos, sem pergunta dupla e sem dado pessoal.
- **f) Não repete a entrevista; complementa.** As perguntas fechadas medem o que o [ROT-02](entrevistas/ROT-02-solicitante.md) perguntou em aberto (como consegue o espaço, duração, antecedência, horários, desistência, o que precisa saber), para a síntese comparar as duas técnicas. As faixas de duração e de antecedência separam os limites já adotados (DEC-07), sem citá-los ao respondente.
- **g) Dados brutos fora do Git.** O CSV do formulário nunca entra no repositório: `levantamento/questionario/brutos/` está no `.gitignore`. O repositório guarda o instrumento e a síntese.
- **h) Tamanho.** A [versão impressa](questionario/QST-01-versao-impressa.md) foi escrita para caber em uma página do PDF de evidências (§7); a conferência é feita ao gerar o PDF.

## Arquivos

| Arquivo | O que contém |
|---|---|
| [`questionario/QST-01-questionario.md`](questionario/QST-01-questionario.md) | **QST-01**: abertura, perguntas como entram no formulário e tabela interna "o que busca". |
| [`questionario/QST-01-versao-impressa.md`](questionario/QST-01-versao-impressa.md) | O instrumento em uma página, sem a tabela interna, para o PDF de evidências. |
| [`questionario/plano-de-aplicacao.md`](questionario/plano-de-aplicacao.md) | Público, meta, canais, período, piloto, configurações do formulário, dados brutos e limitações. |
| [`questionario/modelo-sintese-questionario.md`](questionario/modelo-sintese-questionario.md) | Modelo da síntese, sem resultados. |
| [`questionario/QST-01-resultados.md`](questionario/QST-01-resultados.md) | Síntese: perfil, contagens, conferência das somas, abertas, achados, comparação com as entrevistas e limitações. |
| [`questionario/QST-01-resultados-evidencia.md`](questionario/QST-01-resultados-evidencia.md) | Versão de 1 página da síntese, para o PDF de evidências. |
| [`sintese-do-levantamento.md`](sintese-do-levantamento.md) | **SIN-01**: achados (ACH-01…) com fonte e destino, convergências, decisões resultantes, ameaças à validade e pendências para a REQ-13. |
| [`sintese-evidencia-1pag.md`](sintese-evidencia-1pag.md) | Versão de 1 página da síntese, para o PDF de evidências. |
| [`guia-do-entrevistador.md`](guia-do-entrevistador.md) | **GUI-01**: como abordar, pedir o consentimento, anotar, o que não fazer e o prazo. |
| [`entrevistas/ROT-01-representante-do-cliente.md`](entrevistas/ROT-01-representante-do-cliente.md) | **ROT-01**: as perguntas levadas ao professor na Aula 7, como foram feitas. |
| [`entrevistas/ROT-02-solicitante.md`](entrevistas/ROT-02-solicitante.md) | **ROT-02**: roteiro para o Solicitante. |
| [`entrevistas/ROT-03-atendente-responsavel.md`](entrevistas/ROT-03-atendente-responsavel.md) | **ROT-03**: roteiro para o Atendente responsável. |
| [`entrevistas/modelo-registro-entrevista.md`](entrevistas/modelo-registro-entrevista.md) | **MRE-01**: modelo de registro de uma entrevista. |
| [`entrevistas/ENT-01-representante-do-cliente.md`](entrevistas/ENT-01-representante-do-cliente.md) | **ENT-01**: registro da entrevista com o representante do cliente. |

## Decisões de organização (REQ-09)

- **a) Pasta própria.** `levantamento/` fica ao lado das pastas do modelo do professor (A4·s10), porque o levantamento é a origem das necessidades e não cabe em nenhuma delas. Cada arquivo tem o cabeçalho A4·s11 (`ID • versão • estado`, autor, revisor, aprovador) e o histórico de revisões.
- **b) Identificadores.** `ENT-01`, `ENT-02`… para as entrevistas e `ROT-01`, `ROT-02`… para os roteiros, estáveis e nunca reutilizados, como os demais. As perguntas são numeradas dentro do roteiro (`ROT-02 P03`). `IND-05` é este índice, `GUI-01` o guia e `MRE-01` o modelo de registro.
- **c) Três roteiros, um por perfil**, porque cada perfil sabe coisas diferentes. O **ROT-01** é o instrumento que existiu na Aula 7 (as perguntas da [pauta](../decisoes/pauta-aula-7.md) e as quatro sobre a entrega), sem reescrita nem "melhoria" retroativa. O **ROT-02** é para o Solicitante e o **ROT-03**, para o Atendente responsável.
- **d) Forma dos roteiros novos.** Abertura lida em voz alta (quem somos, objetivo, duração de 10 a 15 minutos, nenhum dado pessoal e o pedido de consentimento verbal para anotar); de 8 a 12 perguntas abertas, agrupadas por tema (como funciona hoje; problemas e consequências; regras e exceções; informação de que a pessoa precisa; prioridades), cada uma marcada **ESSENCIAL** ou **SE HOUVER TEMPO**, com 1 ou 2 aprofundamentos; uma coluna interna, **não lida** ao entrevistado, com o que a pergunta busca (a NS, a regra ou a DEC que ela pode confirmar ou contestar), que liga os achados aos requisitos na REQ-11; encerramento com "tem algo que eu não perguntei e deveria?" e o agradecimento.
- **e) Regras de escrita das perguntas.** Abertas e neutras: nenhuma pergunta de sim ou não que induza a resposta, nenhuma solução, tela ou tecnologia ("requisito ≠ interface; requisito = necessidade", A1·s14). Sobre experiências reais ("conte a última vez"), não sobre hipóteses. Nenhum dado pessoal: o perfil é registrado de forma genérica. Para o Solicitante, entram sem induzir os temas que as decisões da Aula 7 mudaram (duração típica, antecedência, horários inclusive à noite, desistência e não comparecimento, horários ocupados por outras pessoas); para o Atendente, como recebe e decide os pedidos, dois pedidos para o mesmo horário, o registro de que o uso aconteceu, o não comparecimento, horários diferentes por espaço e quem define as regras.
- **f) Modelo de registro único** ([MRE-01](entrevistas/modelo-registro-entrevista.md)), com as respostas (resumo fiel e trechos literais marcados) separadas dos "Achados preliminares", que são a interpretação do entrevistador.
- **g) ENT-01 a partir do que já existe.** As respostas são os textos registrados como "Resposta do professor" nas DECs e na pauta, copiados sem alteração, com o link para cada DEC. O que foi complemento do grupo (o campo "Decisão do grupo" das DECs) não é resposta: aparece nas observações do entrevistador. A duração não foi registrada e não é estimada.
- **h) Guia do entrevistador** de uma página ([GUI-01](guia-do-entrevistador.md)), para os integrantes que conduzem as entrevistas.
- **i) Tamanho.** Cada roteiro cabe em até uma página impressa, porque entra no PDF de evidências (até 8 páginas, §7) junto com o questionário e os registros.
