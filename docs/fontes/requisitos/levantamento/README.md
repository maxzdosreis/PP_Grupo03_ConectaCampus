# Levantamento de requisitos

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **IND-05 • 0.1 • Rascunho** (índice do levantamento) | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/levantamento/` |

Instrumentos e registros das técnicas de levantamento do Conecta Campus (enunciado do Projeto Final de Requisitos, §5.3, §6 "Levantamento" e §7). Esta pasta guarda **o que foi perguntado e o que foi respondido**; as consequências dos achados nos requisitos (Visão, NS, RF, DECs) são de outra tarefa (REQ-11) e não são feitas aqui.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Criação: técnicas, plano e status das entrevistas, decisões a) a i), roteiros ROT-01 a ROT-03, modelo de registro, guia do entrevistador e o registro da ENT-01 (REQ-09). Sem aprovação. |
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Entrevistas ENT-02 a ENT-04 registradas como **simuladas** (perfis fictícios, com aviso em cada arquivo); tabela de status e contagem de representantes por papel (REQ-09). Sem aprovação. |

## Técnicas do grupo

| # | Técnica | Tarefa | Com quem | Situação |
|---|---|---|---|---|
| 1 | **Entrevista semiestruturada** (roteiro com perguntas abertas e aprofundamentos livres) | REQ-09 | Representante do cliente, Solicitantes e Atendente responsável | ENT-01 realizada; demais planejadas |
| 2 | **Questionário** | REQ-10 | A definir na REQ-10 | Não iniciado |

**Por que a entrevista.** Cada perfil sabe coisas diferentes: o cliente define as regras de uso, o Solicitante conhece o pedido do lado de quem usa, e o Atendente responsável conhece o pedido do lado de quem decide e opera os espaços. A entrevista também cumpre a exigência de interação com pelo menos dois representantes de stakeholders (§5.3). Os papéis Atendente responsável (servidor que opera os espaços: confirma, recusa e conclui) e Gestor do serviço (cadastra espaços e define as regras) são os da REQ-12.

**A ENT-01 e o "cliente sem tempo" (A1·s30).** Na leitura do grupo, a pauta da Aula 7 foi a estratégia para um cliente com pouco tempo: perguntas curtas, cada uma com a opção já adotada e o impacto se a resposta fosse outra, para o professor só confirmar ou corrigir.

## Plano e status das entrevistas

| ID | Perfil do entrevistado | Roteiro | Quando | Entrevistador | Status |
|---|---|---|---|---|---|
| [ENT-01](entrevistas/ENT-01-representante-do-cliente.md) | Professor da disciplina, no papel de representante do cliente (instituição), [premissa P-01](../visao.md#premissas) | [ROT-01](entrevistas/ROT-01-representante-do-cliente.md) | 06/11/2026 (Aula 7) | Max Zimmermann dos Reis | Realizada |
| [ENT-02](entrevistas/ENT-02-solicitante-estudante-simulada.md) | Solicitante (estudante), perfil **fictício** | [ROT-02](entrevistas/ROT-02-solicitante.md) | Sem data de campo | — (elaborada pelo grupo com apoio de IA) | **Simulada** |
| [ENT-03](entrevistas/ENT-03-solicitante-servidor-simulada.md) | Solicitante (servidor), perfil **fictício** | [ROT-02](entrevistas/ROT-02-solicitante.md) | Sem data de campo | — (idem) | **Simulada** |
| [ENT-04](entrevistas/ENT-04-atendente-responsavel-simulada.md) | Atendente responsável, perfil **fictício** | [ROT-03](entrevistas/ROT-03-atendente-responsavel.md) | Sem data de campo | — (idem) | **Simulada** |

**Por que simuladas.** O grupo não teve tempo de entrevistar pessoas reais antes do prazo (11/11/2026). O enunciado (§5.3) admite representantes "reais ou simulados"; por isso as ENT-02 a ENT-04 foram elaboradas pelo grupo, com apoio de IA, a partir de perfis fictícios, e cada arquivo traz o aviso de simulação. Elas **não são falas de pessoas reais**: não provam uma necessidade de campo e devem ser apresentadas assim no PDF de evidências. Os campos "data", "duração" e "consentimento" não se aplicam a elas.

### Representantes por papel

| Papel | Real | Simulado | Entrevistas |
|---|---|---|---|
| Cliente (instituição) | 1 | 0 | ENT-01 |
| Solicitante | 0 | 2 | ENT-02, ENT-03 |
| Atendente responsável | 0 | 1 | ENT-04 |
| **Total** | **1** | **3** | 4 representantes em 3 papéis |

**Mínimo do enunciado (§5.3): atingido** (pelo menos dois representantes de stakeholders na mesma técnica), mas **só com os simulados**: o único representante real é a ENT-01. Se o grupo conseguir entrevistar uma pessoa real até a entrega, ela entra como ENT-05 (o ID não é reaproveitado) e fortalece a evidência.

Cada entrevista realizada ganha um arquivo `entrevistas/ENT-xx-<perfil>.md`, no formato do [modelo de registro](entrevistas/modelo-registro-entrevista.md). Uma entrevista planejada que não acontecer fica nesta tabela como **Cancelada**, com o motivo; o ID não é reaproveitado.

## Arquivos

| Arquivo | O que contém |
|---|---|
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
