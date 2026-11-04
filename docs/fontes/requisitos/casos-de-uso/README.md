# Casos de uso

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **UCD-01 • 0.1 • Rascunho** (diagrama do negócio) e **UCD-02 • 0.1 • Rascunho** (diagrama de apoio "Administração") | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/casos-de-uso/` |

Diagrama UML de casos de uso do Conecta Campus, índice dos casos de uso (UC-xx) e rastreabilidade RF → UC. Os atores são os da [Visão](../visao.md#2-usuários-atores-e-stakeholders) e da [SRS, seção 2](../requisitos/srs.md#atores-e-perfis); os nomes de atores e casos de uso saem do [glossário](../glossario.md#7-casos-de-uso). As fichas Cockburn (ator primário, meta, precondições, fluxo principal numerado, alternativas e exceções ligadas ao passo, pós-condições) vêm na **REQ-04**. Índice da fonte oficial: [README](../README.md).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: diagrama do negócio (UC-01 a UC-19), diagrama de apoio "Administração" (UC-20 a UC-22), decisões de modelagem, índice dos UCs e rastreabilidade RF → UC dos 60 RF (REQ-03). Sem aprovação. |

## Sumário

1. [Diagrama do negócio (UCD-01)](#diagrama-do-negócio-ucd-01)
2. [Diagrama de apoio "Administração" (UCD-02)](#diagrama-de-apoio-administração-ucd-02)
3. [Legenda](#legenda)
4. [Decisões de modelagem](#decisões-de-modelagem)
5. [Como gerar as imagens](#como-gerar-as-imagens)
6. [Índice dos casos de uso](#índice-dos-casos-de-uso)
7. [Rastreabilidade RF → UC](#rastreabilidade-rf--uc)
8. [Pendências](#pendências)

## Diagrama do negócio (UCD-01)

![Diagrama de casos de uso do negócio do Conecta Campus](diagrama-casos-de-uso.png)

Fonte: [`diagrama-casos-de-uso.puml`](diagrama-casos-de-uso.puml) · imagem vetorial: [`diagrama-casos-de-uso.svg`](diagrama-casos-de-uso.svg).

## Diagrama de apoio "Administração" (UCD-02)

![Diagrama de casos de uso de administração do Conecta Campus](diagrama-administracao.png)

Fonte: [`diagrama-administracao.puml`](diagrama-administracao.puml) · imagem vetorial: [`diagrama-administracao.svg`](diagrama-administracao.svg).

## Legenda

A mesma do próprio diagrama (A2·s24–27):

| Notação | Significado |
|---|---|
| Retângulo "Conecta Campus" | Fronteira do sistema. Tudo dentro é comportamento do sistema; os atores ficam fora. |
| Boneco | Ator: um papel externo ao sistema (sentido da UML, não o `Ator` do código; ver o [glossário](../glossario.md#ator)). |
| Elipse com "UC-xx Verbo …" | Caso de uso, nomeado pela meta, no infinitivo, com o ID visível. |
| Linha contínua ator–elipse | Associação: o ator inicia o caso de uso. |
| Seta tracejada `«include»` (base → incluído) | Inclusão **obrigatória**: toda execução do caso base executa o incluído. |
| Seta tracejada `«extend»` (extensão → base), com o ponto entre parênteses | Extensão **opcional**: acontece só quando o ator escolhe, no **ponto de extensão** declarado na elipse da base. |
| Seta contínua com triângulo vazado | Generalização: o filho herda as associações e o comportamento do pai (Gestor → Solicitante; Confirmar, Recusar, Concluir e Cancelar → Alterar situação). |
| Nome em itálico com `{abstrato}` | Caso de uso abstrato: não acontece sozinho, só por um dos filhos. |
| Elipse cinza com `«subfunção»` | Caso de uso de subfunção (Cockburn): parte de outro caso de uso, sem ator próprio. As brancas são do nível do objetivo do usuário. |
| Nota (folha dobrada) | Restrição que vale para os atores ligados a ela (aqui, a precondição de autenticação). |

A cor só reforça o estereótipo `«subfunção»`, que já aparece escrito: o diagrama não depende de cor (como o [RNF-U05](../requisitos/rnf.md#rnf-u05) exige das telas).

## Decisões de modelagem

<a id="decisao-a"></a>**a) Granularidade no nível do objetivo do usuário** (o "nível do mar" de Cockburn). Um caso de uso é algo que o ator quer alcançar numa sessão, e começa pela meta, não pela tela (A3·s13): "Solicitar reserva", e não "preencher a data". Consequências:

- **Recusas viram exceções, não elipses.** Os 27 RF de recusa (F5: os filhos `RF-xx.n` e RF-09, RF-10, RF-23 a RF-27) entram como **exceções** do caso de uso que protegem, detalhadas na REQ-04 (coluna "Como entra" da [rastreabilidade](#rastreabilidade-rf--uc)). Um "Recusar pedido em conflito de horário" não é meta de ninguém.
- **Consultas de apoio viram passos, não elipses.** Consultar um espaço (RF-03), os tipos de espaço (RF-04), as situações de reserva (RF-15) e as regras de agenda (RF-28) são passos ou alternativas dos casos de uso que os usam. Por isso o [vocabulário público](../glossario.md#vocabulario-publico) não gera um caso de uso próprio do Visitante: ele é dado de apoio a outros casos de uso, não uma meta.
- **Sessão faz parte de Autenticar.** Continuar identificado (RF-34), sessão expirada (RF-34.1), consultar os próprios dados ao voltar (RF-35) e sair (RF-36) são alternativas e exceções de UC-02.
- **RF transversais não são casos de uso.** O [RF-38](../requisitos/rf-gerais.md#rf-38) (ver o resultado de cada operação) é uma qualidade de todos os casos de uso, como um RNF: não tem elipse, e a rastreabilidade o marca como "transversal".
- **Subfunções só quando dizem algo.** As três elipses cinza ("Verificar disponibilidade do horário", "Informar motivo", "Registrar no histórico") existem porque são comportamento observável e obrigatório que mais de um caso de uso compartilha, ou que concentra as recusas principais (UC-05 reúne as três recusas do pedido que dependem do estado: espaço não reservável, conflito e regras de agenda).
- **Contagem.** 19 elipses no diagrama do negócio, acima das ~16 previstas: as quatro especializações de UC-10 são metas distintas (confirmar, recusar, concluir e cancelar têm atores, motivos e efeitos diferentes) e o caso de uso abstrato é o alvo da ficha "Alterar situação" da REQ-04. Mesmo assim o diagrama cabe numa A4 deitada, sem cruzamento entre as relações dos casos de uso (só as linhas tracejadas da nota de precondição cruzam associações).

<a id="decisao-b"></a>**b) Notação UML padrão.** Só associações ator–caso de uso, `«include»`, `«extend»` com ponto de extensão nomeado e generalização. **Não** ligamos casos de uso em sequência, como no diagrama de referência do slide A2·s24 ("Passo 1 → Passo 4"): a UML não prevê essa seta, e a ordem dos passos é assunto da ficha (fluxo principal numerado) e da jornada, não do diagrama. É o ponto 3 dos pontos a confirmar, ainda em aberto; se o professor pedir o estilo do slide, muda só o `.puml`, sem mudar IDs.

<a id="decisao-c"></a>**c) Generalização de atores.** O Gestor faz tudo o que o Solicitante faz, e mais ([SRS, seção 2](../requisitos/srs.md#atores-e-perfis)): pede reservas em nome próprio, consulta, cancela. Por isso o Gestor **herda** do Solicitante, e o diagrama não repete as associações (UC-03, UC-04, UC-07, UC-08 e UC-11 valem para os dois). As diferenças de alcance (o Solicitante vê e cancela só as próprias; o Gestor, todas) são regra de negócio, ficam nas fichas e já estão nos RF ([RF-13](../requisitos/rf-reservas.md#rf-13), [RF-20](../requisitos/rf-reservas.md#rf-20), [RF-21](../requisitos/rf-reservas.md#rf-21), [RF-23](../requisitos/rf-reservas.md#rf-23)). Do mesmo modo, Confirmar, Recusar, Concluir e Cancelar **especializam** o caso de uso abstrato "Alterar situação da reserva": as recusas comuns (transição não permitida, situação desconhecida, perfil sem permissão, reserva de outra pessoa) e a inclusão de "Registrar no histórico" ficam uma vez só, no pai.

<a id="decisao-d"></a>**d) Autenticação como precondição, numa nota.** O login é o caso de uso UC-02 do Visitante. Os casos de uso do Solicitante e do Gestor exigem um [usuário autenticado](../glossario.md#usuario-autenticado), mas o diagrama **não** desenha `«include»` para Autenticar, e sim uma nota UML ligada aos dois atores: "Precondição de todos os casos de uso do Solicitante e do Gestor: ator autenticado (UC-02 Autenticar)". Motivos:

- `«include»` diz que **toda** execução do caso base executa o incluído. Quem já está identificado não se autentica de novo a cada pedido; identificar-se é uma condição de entrada, não um passo.
- Tirar o include de só alguns casos de uso "âncora" (a primeira proposta) deixaria os outros parecendo livres de login, o que contradiz o [RNF-F04](../requisitos/rnf.md#rnf-f04) (identificação obrigatória por padrão). Pôr o include em todos os 13 casos de uso dos dois atores tornaria o diagrama ilegível.
- A nota diz a regra inteira com um só elemento, e a precondição "usuário autenticado" entra em cada ficha na REQ-04. Isso atende ao que a [DEC-04](../decisoes/DEC-04.md) lista como artefato afetado ("ator Gestor e `<<include>>` Autenticar"): o Gestor está no diagrama, e a dependência de Autenticar está expressa como precondição.

<a id="decisao-e"></a>**e) Equipe de TI num diagrama de apoio.** A [Equipe de TI](../glossario.md#equipe-de-ti) não é ator dos casos de uso do negócio ([Visão, seção 2](../visao.md#2-usuários-atores-e-stakeholders)). Os RF dela (criar usuário Gestor, carregar dados de exemplo, verificar se o sistema está no ar) ficam no diagrama separado "Administração" (UCD-02, UC-20 a UC-22), para a rastreabilidade RF → UC ficar completa sem misturar instalação e operação com o negócio.

<a id="decisao-f"></a>**f) Sem sistema externo.** O professor pede os atores "incluindo sistemas externos" quando existirem. Aqui não existe nenhum: o Conecta Campus não se integra a sistemas da instituição, de pagamento nem de notificação ([Visão, fora do escopo](../visao.md#fora-do-escopo); [SRS, seção 4.2](../requisitos/srs.md#42-com-outros-sistemas)). A legenda do diagrama registra essa ausência para ela não parecer esquecimento. Pelo mesmo motivo, nenhum caso de uso tem ator secundário.

<a id="decisao-g"></a>**g) Ferramenta: PlantUML.** Tem suporte nativo a diagrama de casos de uso UML (fronteira, atores, `«include»`, `«extend»`, generalização, notas e legenda); o Mermaid não tem. A fonte `.puml` é texto versionado no Git, como o resto da pasta (A4·s12). Os `.svg` e `.png` também são versionados, porque o `.png` entra nos PDFs e o Markdown o exibe; eles são **gerados** a partir do `.puml` e nunca editados à mão. A ferramenta e a notação são o ponto 2 dos pontos a confirmar, ainda em aberto.

## Como gerar as imagens

Pelo Docker, com a imagem oficial do PlantUML numa versão fixa, sem instalar Java. Na raiz do repositório, rode os dois comandos (um para SVG, outro para PNG):

Git Bash:

```bash
MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd)/docs/fontes/requisitos/casos-de-uso:/data" -w /data plantuml/plantuml:1.2026.9 -charset UTF-8 -tsvg diagrama-casos-de-uso.puml diagrama-administracao.puml
MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd)/docs/fontes/requisitos/casos-de-uso:/data" -w /data plantuml/plantuml:1.2026.9 -charset UTF-8 -tpng diagrama-casos-de-uso.puml diagrama-administracao.puml
```

PowerShell:

```powershell
docker run --rm -v "${PWD}/docs/fontes/requisitos/casos-de-uso:/data" -w /data plantuml/plantuml:1.2026.9 -charset UTF-8 -tsvg diagrama-casos-de-uso.puml diagrama-administracao.puml
docker run --rm -v "${PWD}/docs/fontes/requisitos/casos-de-uso:/data" -w /data plantuml/plantuml:1.2026.9 -charset UTF-8 -tpng diagrama-casos-de-uso.puml diagrama-administracao.puml
```

Os quatro arquivos gerados (`diagrama-casos-de-uso.svg`, `diagrama-casos-de-uso.png`, `diagrama-administracao.svg`, `diagrama-administracao.png`) ficam nesta pasta, ao lado das fontes. Toda mudança no `.puml` regera os quatro no mesmo PR. Depois, na raiz:

```bash
python scripts/verificar_casos_de_uso.py
```

O script confere o diagrama contra este README, a SRS e as fichas (UCs, RF → UC, notação e imagens desatualizadas). As ligações invisíveis e as setas mais longas do `.puml` (comentadas lá) servem só ao layout e não são relações UML.

## Índice dos casos de uso

Nível: **objetivo** = objetivo do usuário (o "nível do mar"); **subfunção** = parte de outro caso de uso, alcançada por `«include»`; **abstrato** = generalização, só acontece por um dos filhos. Estado: "Ficha na REQ-04" = a ficha Cockburn é escrita na próxima tarefa; "Ficha a definir" = ainda sem tarefa. Nenhum caso de uso tem ator secundário ([decisão f](#decisao-f)).

| ID | Caso de uso | Meta | Ator primário | Atores secundários | Nível | RF | Estado |
|---|---|---|---|---|---|---|---|
| <a id="uc-01"></a>UC-01 | Cadastrar-se | Obter acesso ao sistema como Solicitante, sem depender de um Gestor. | Visitante | — | objetivo | [RF-32](../requisitos/rf-contas.md#rf-32), [RF-32.1](../requisitos/rf-contas.md#rf-32-1), [RF-32.2](../requisitos/rf-contas.md#rf-32-2), [RF-32.3](../requisitos/rf-contas.md#rf-32-3) | Ficha a definir |
| <a id="uc-02"></a>UC-02 | Autenticar | Ser identificado pelo sistema para agir com o próprio perfil, e deixar de sê-lo ao sair. | Visitante | — | objetivo | [RF-33](../requisitos/rf-contas.md#rf-33), [RF-33.1](../requisitos/rf-contas.md#rf-33-1), [RF-34](../requisitos/rf-contas.md#rf-34), [RF-34.1](../requisitos/rf-contas.md#rf-34-1), [RF-35](../requisitos/rf-contas.md#rf-35), [RF-36](../requisitos/rf-contas.md#rf-36) | Ficha na REQ-04 |
| <a id="uc-03"></a>UC-03 | Consultar espaços | Saber quais espaços esportivos existem, de que tipo são e quais aceitam pedidos. | Solicitante (e o Gestor, por herança) | — | objetivo | [RF-01](../requisitos/rf-espacos.md#rf-01), [RF-02](../requisitos/rf-espacos.md#rf-02), [RF-02.1](../requisitos/rf-espacos.md#rf-02-1), [RF-03](../requisitos/rf-espacos.md#rf-03), [RF-04](../requisitos/rf-espacos.md#rf-04), [RF-09](../requisitos/rf-espacos.md#rf-09) | Ficha a definir |
| <a id="uc-04"></a>UC-04 | Solicitar reserva | Garantir o uso de um espaço num intervalo de um dia, com o pedido registrado na situação Solicitada. | Solicitante (e o Gestor, por herança) | — | objetivo | [RF-11](../requisitos/rf-reservas.md#rf-11), [RF-11.1](../requisitos/rf-reservas.md#rf-11-1), [RF-11.2](../requisitos/rf-reservas.md#rf-11-2), [RF-28](../requisitos/rf-agenda.md#rf-28) | Ficha na REQ-04 |
| <a id="uc-05"></a>UC-05 | Verificar disponibilidade do horário | Garantir que só é aceito o pedido num espaço reservável, dentro das regras de agenda e sem conflito de horário. | — (incluído por UC-04) | — | subfunção | [RF-11.3](../requisitos/rf-reservas.md#rf-11-3), [RF-11.4](../requisitos/rf-reservas.md#rf-11-4), [RF-11.5](../requisitos/rf-reservas.md#rf-11-5) | Ficha a definir (parte da ficha de UC-04) |
| <a id="uc-06"></a>UC-06 | Consultar agenda do dia | Escolher um horário que será aceito, vendo antes do pedido o que está ocupado e livre no espaço e no dia. | Solicitante (e o Gestor, por herança), pela extensão de UC-04 | — | objetivo | [RF-28](../requisitos/rf-agenda.md#rf-28), [RF-29](../requisitos/rf-agenda.md#rf-29), [RF-29.1](../requisitos/rf-agenda.md#rf-29-1), [RF-29.2](../requisitos/rf-agenda.md#rf-29-2), [RF-30](../requisitos/rf-agenda.md#rf-30), [RF-31](../requisitos/rf-agenda.md#rf-31) | Ficha a definir (extensão na ficha de UC-04) |
| <a id="uc-07"></a>UC-07 | Consultar reservas | Localizar reservas por critérios combinados (o Solicitante, só as próprias) e ver as ações disponíveis em cada uma. | Solicitante (e o Gestor, por herança) | — | objetivo | [RF-12](../requisitos/rf-reservas.md#rf-12), [RF-12.1](../requisitos/rf-reservas.md#rf-12-1), [RF-13](../requisitos/rf-reservas.md#rf-13), [RF-15](../requisitos/rf-reservas.md#rf-15), [RF-16](../requisitos/rf-reservas.md#rf-16) | Ficha a definir |
| <a id="uc-08"></a>UC-08 | Consultar detalhe da reserva | Acompanhar uma reserva: os dados, a situação atual com o motivo e as ações disponíveis. | Solicitante (e o Gestor, por herança) | — | objetivo | [RF-14](../requisitos/rf-reservas.md#rf-14), [RF-16](../requisitos/rf-reservas.md#rf-16), [RF-23](../requisitos/rf-reservas.md#rf-23) | Ficha a definir |
| <a id="uc-09"></a>UC-09 | Consultar histórico da reserva | Saber quem mudou a situação da reserva, quando, de qual para qual e por quê. | Solicitante (e o Gestor, por herança), pela extensão de UC-08 | — | objetivo | [RF-22](../requisitos/rf-reservas.md#rf-22), [RF-23](../requisitos/rf-reservas.md#rf-23) | Ficha a definir |
| <a id="uc-10"></a>UC-10 | *Alterar situação da reserva* {abstrato} | Levar uma reserva a uma situação permitida pela tabela de transições e pelo perfil, com a mudança registrada no histórico. | — (abstrato: pelos filhos UC-11, UC-17, UC-18 e UC-19) | — | abstrato | [RF-23](../requisitos/rf-reservas.md#rf-23), [RF-24](../requisitos/rf-reservas.md#rf-24), [RF-25](../requisitos/rf-reservas.md#rf-25), [RF-27](../requisitos/rf-reservas.md#rf-27) | Ficha na REQ-04 |
| <a id="uc-11"></a>UC-11 | Cancelar reserva | Desistir do uso pedido (o Solicitante, só na própria; o Gestor, em qualquer uma), com motivo, liberando o horário. | Solicitante (e o Gestor, por herança) | — | objetivo | [RF-20](../requisitos/rf-reservas.md#rf-20), [RF-21](../requisitos/rf-reservas.md#rf-21) | Ficha a definir (variação na ficha de UC-10) |
| <a id="uc-12"></a>UC-12 | Informar motivo | Deixar justificada ao solicitante uma recusa ou um cancelamento. | — (incluído por UC-11 e UC-18) | — | subfunção | [RF-26](../requisitos/rf-reservas.md#rf-26) | Ficha a definir (parte da ficha de UC-10) |
| <a id="uc-13"></a>UC-13 | Registrar no histórico | Guardar, na mesma gravação, a criação e cada mudança de situação aceita, como fato que não muda mais. | — (incluído por UC-04 e UC-10) | — | subfunção | [RF-22](../requisitos/rf-reservas.md#rf-22) | Ficha a definir (parte das fichas de UC-04 e UC-10) |
| <a id="uc-14"></a>UC-14 | Cadastrar espaço | Incluir um espaço novo na lista, para que passe a aceitar pedidos. | Gestor | — | objetivo | [RF-04](../requisitos/rf-espacos.md#rf-04), [RF-05](../requisitos/rf-espacos.md#rf-05), [RF-05.1](../requisitos/rf-espacos.md#rf-05-1), [RF-05.2](../requisitos/rf-espacos.md#rf-05-2), [RF-10](../requisitos/rf-espacos.md#rf-10) | Ficha na REQ-04 |
| <a id="uc-15"></a>UC-15 | Editar espaço | Manter o nome, o tipo e a capacidade de um espaço iguais à realidade. | Gestor | — | objetivo | [RF-04](../requisitos/rf-espacos.md#rf-04), [RF-05.2](../requisitos/rf-espacos.md#rf-05-2), [RF-06](../requisitos/rf-espacos.md#rf-06), [RF-06.1](../requisitos/rf-espacos.md#rf-06-1), [RF-06.2](../requisitos/rf-espacos.md#rf-06-2), [RF-09](../requisitos/rf-espacos.md#rf-09), [RF-10](../requisitos/rf-espacos.md#rf-10) | Ficha a definir |
| <a id="uc-16"></a>UC-16 | Desativar ou reativar espaço | Impedir novos pedidos num espaço que deixou de poder ser usado, ou voltar a aceitá-los. | Gestor | — | objetivo | [RF-07](../requisitos/rf-espacos.md#rf-07), [RF-07.1](../requisitos/rf-espacos.md#rf-07-1), [RF-08](../requisitos/rf-espacos.md#rf-08), [RF-08.1](../requisitos/rf-espacos.md#rf-08-1), [RF-09](../requisitos/rf-espacos.md#rf-09), [RF-10](../requisitos/rf-espacos.md#rf-10) | Ficha a definir |
| <a id="uc-17"></a>UC-17 | Confirmar reserva | Aprovar o uso pedido, mantendo o horário ocupado. | Gestor | — | objetivo | [RF-17](../requisitos/rf-reservas.md#rf-17) | Ficha a definir (variação na ficha de UC-10) |
| <a id="uc-18"></a>UC-18 | Recusar reserva | Negar o pedido, com motivo, liberando o horário. | Gestor | — | objetivo | [RF-18](../requisitos/rf-reservas.md#rf-18) | Ficha a definir (variação na ficha de UC-10) |
| <a id="uc-19"></a>UC-19 | Concluir reserva | Registrar que o uso confirmado aconteceu. | Gestor | — | objetivo | [RF-19](../requisitos/rf-reservas.md#rf-19) | Ficha a definir (variação na ficha de UC-10) |
| <a id="uc-20"></a>UC-20 | Criar usuário Gestor | Dar a uma pessoa do setor dos espaços o perfil Gestor. | Equipe de TI (UCD-02) | — | objetivo (apoio) | [RF-37](../requisitos/rf-contas.md#rf-37) | Ficha a definir |
| <a id="uc-21"></a>UC-21 | Carregar dados de exemplo | Ter usuários, espaços e reservas coerentes para demonstrar o sistema, com um comando. | Equipe de TI (UCD-02) | — | objetivo (apoio) | [RF-39](../requisitos/rf-gerais.md#rf-39) | Ficha a definir |
| <a id="uc-22"></a>UC-22 | Verificar se o sistema está no ar | Saber se o sistema e o banco de dados respondem, antes de usar ou demonstrar. | Equipe de TI (UCD-02) | — | objetivo (apoio) | [RF-40](../requisitos/rf-gerais.md#rf-40) | Ficha a definir |

## Rastreabilidade RF → UC

Todos os 60 RF da [tabela-resumo da SRS](../requisitos/srs.md#tabela-resumo). "Como entra" diz o papel do RF no caso de uso: **fluxo principal**, **alternativa** (outro caminho que ainda alcança a meta), **exceção** (a meta não é alcançada; detalhada na REQ-04) ou **transversal** (qualidade de todos os casos de uso). A coluna UC também está em cada ficha (campo "Vínculos") e na [SRS, seção 6.4](../requisitos/srs.md#64-rf--evidência-uc-us-e-ca).

| RF | Título | UC | Como entra | Também em |
|---|---|---|---|---|
| [RF-01](../requisitos/rf-espacos.md#rf-01) | Listar espaços | [UC-03 Consultar espaços](#uc-03) | fluxo principal | — |
| [RF-02](../requisitos/rf-espacos.md#rf-02) | Filtrar espaços | [UC-03 Consultar espaços](#uc-03) | alternativa (filtrar a lista) | — |
| [RF-02.1](../requisitos/rf-espacos.md#rf-02-1) | Recusar filtro com tipo inexistente | [UC-03 Consultar espaços](#uc-03) | exceção | — |
| [RF-03](../requisitos/rf-espacos.md#rf-03) | Consultar um espaço | [UC-03 Consultar espaços](#uc-03) | alternativa (ver um espaço) | — |
| [RF-04](../requisitos/rf-espacos.md#rf-04) | Consultar os tipos de espaço | [UC-03 Consultar espaços](#uc-03) | fluxo principal (os tipos do filtro e do formulário) | [UC-14](#uc-14), [UC-15](#uc-15) |
| [RF-05](../requisitos/rf-espacos.md#rf-05) | Cadastrar espaço | [UC-14 Cadastrar espaço](#uc-14) | fluxo principal | — |
| [RF-05.1](../requisitos/rf-espacos.md#rf-05-1) | Recusar espaço com dados inválidos | [UC-14 Cadastrar espaço](#uc-14) | exceção | — |
| [RF-05.2](../requisitos/rf-espacos.md#rf-05-2) | Recusar nome de espaço repetido | [UC-14 Cadastrar espaço](#uc-14) | exceção | [UC-15](#uc-15) |
| [RF-06](../requisitos/rf-espacos.md#rf-06) | Editar espaço | [UC-15 Editar espaço](#uc-15) | fluxo principal | — |
| [RF-06.1](../requisitos/rf-espacos.md#rf-06-1) | Recusar edição sem alteração | [UC-15 Editar espaço](#uc-15) | exceção | — |
| [RF-06.2](../requisitos/rf-espacos.md#rf-06-2) | Recusar edição que viola as regras do cadastro | [UC-15 Editar espaço](#uc-15) | exceção | — |
| [RF-07](../requisitos/rf-espacos.md#rf-07) | Desativar espaço | [UC-16 Desativar ou reativar espaço](#uc-16) | fluxo principal (desativar) | — |
| [RF-07.1](../requisitos/rf-espacos.md#rf-07-1) | Recusar desativar espaço já inativo | [UC-16 Desativar ou reativar espaço](#uc-16) | exceção | — |
| [RF-08](../requisitos/rf-espacos.md#rf-08) | Reativar espaço | [UC-16 Desativar ou reativar espaço](#uc-16) | alternativa (reativar) | — |
| [RF-08.1](../requisitos/rf-espacos.md#rf-08-1) | Recusar reativar espaço já ativo | [UC-16 Desativar ou reativar espaço](#uc-16) | exceção | — |
| [RF-09](../requisitos/rf-espacos.md#rf-09) | Recusar operação sobre espaço inexistente | [UC-03 Consultar espaços](#uc-03) | exceção (recusa comum) | [UC-15](#uc-15), [UC-16](#uc-16) |
| [RF-10](../requisitos/rf-espacos.md#rf-10) | Recusar manutenção de espaço por quem não é Gestor | [UC-14 Cadastrar espaço](#uc-14) | exceção (recusa comum) | [UC-15](#uc-15), [UC-16](#uc-16) |
| [RF-11](../requisitos/rf-reservas.md#rf-11) | Solicitar reserva | [UC-04 Solicitar reserva](#uc-04) | fluxo principal | — |
| [RF-11.1](../requisitos/rf-reservas.md#rf-11-1) | Recusar pedido com dados inválidos | [UC-04 Solicitar reserva](#uc-04) | exceção | — |
| [RF-11.2](../requisitos/rf-reservas.md#rf-11-2) | Recusar pedido com data retroativa | [UC-04 Solicitar reserva](#uc-04) | exceção | — |
| [RF-11.3](../requisitos/rf-reservas.md#rf-11-3) | Recusar pedido para espaço que não é reservável | [UC-05 Verificar disponibilidade do horário](#uc-05) | exceção | — |
| [RF-11.4](../requisitos/rf-reservas.md#rf-11-4) | Recusar pedido em conflito de horário | [UC-05 Verificar disponibilidade do horário](#uc-05) | exceção | — |
| [RF-11.5](../requisitos/rf-reservas.md#rf-11-5) | Recusar pedido fora das regras de agenda | [UC-05 Verificar disponibilidade do horário](#uc-05) | exceção | — |
| [RF-12](../requisitos/rf-reservas.md#rf-12) | Consultar reservas por critérios combináveis | [UC-07 Consultar reservas](#uc-07) | fluxo principal | — |
| [RF-12.1](../requisitos/rf-reservas.md#rf-12-1) | Recusar critério de consulta em formato inválido | [UC-07 Consultar reservas](#uc-07) | exceção | — |
| [RF-13](../requisitos/rf-reservas.md#rf-13) | Consultar as próprias reservas | [UC-07 Consultar reservas](#uc-07) | fluxo principal (o Solicitante vê só as próprias; para o Gestor, alternativa "somente as minhas") | — |
| [RF-14](../requisitos/rf-reservas.md#rf-14) | Consultar o detalhe de uma reserva | [UC-08 Consultar detalhe da reserva](#uc-08) | fluxo principal | — |
| [RF-15](../requisitos/rf-reservas.md#rf-15) | Consultar as situações de reserva | [UC-07 Consultar reservas](#uc-07) | fluxo principal (as situações do critério) | — |
| [RF-16](../requisitos/rf-reservas.md#rf-16) | Ver as ações disponíveis em cada reserva | [UC-07 Consultar reservas](#uc-07) | fluxo principal | [UC-08](#uc-08) |
| [RF-17](../requisitos/rf-reservas.md#rf-17) | Confirmar reserva | [UC-17 Confirmar reserva](#uc-17) | fluxo principal | — |
| [RF-18](../requisitos/rf-reservas.md#rf-18) | Recusar reserva com motivo | [UC-18 Recusar reserva](#uc-18) | fluxo principal | — |
| [RF-19](../requisitos/rf-reservas.md#rf-19) | Concluir reserva | [UC-19 Concluir reserva](#uc-19) | fluxo principal | — |
| [RF-20](../requisitos/rf-reservas.md#rf-20) | Cancelar reserva (Gestor) | [UC-11 Cancelar reserva](#uc-11) | fluxo principal (pelo Gestor) | — |
| [RF-21](../requisitos/rf-reservas.md#rf-21) | Cancelar a própria reserva (Solicitante) | [UC-11 Cancelar reserva](#uc-11) | fluxo principal (pelo Solicitante, na própria) | — |
| [RF-22](../requisitos/rf-reservas.md#rf-22) | Consultar o histórico da reserva | [UC-09 Consultar histórico da reserva](#uc-09) | fluxo principal (UC-13 grava o que UC-09 mostra) | [UC-13](#uc-13) |
| [RF-23](../requisitos/rf-reservas.md#rf-23) | Recusar operação sobre reserva inexistente ou de outra pessoa | [UC-08 Consultar detalhe da reserva](#uc-08) | exceção (recusa comum) | [UC-09](#uc-09), [UC-10](#uc-10) |
| [RF-24](../requisitos/rf-reservas.md#rf-24) | Recusar transição de situação não permitida | [UC-10 Alterar situação da reserva](#uc-10) | exceção (herdada pelos filhos) | — |
| [RF-25](../requisitos/rf-reservas.md#rf-25) | Recusar situação ausente ou desconhecida | [UC-10 Alterar situação da reserva](#uc-10) | exceção (herdada pelos filhos) | — |
| [RF-26](../requisitos/rf-reservas.md#rf-26) | Recusar recusa ou cancelamento sem motivo válido | [UC-12 Informar motivo](#uc-12) | exceção | — |
| [RF-27](../requisitos/rf-reservas.md#rf-27) | Recusar mudança de situação que o perfil não pode fazer | [UC-10 Alterar situação da reserva](#uc-10) | exceção (herdada pelos filhos) | — |
| [RF-28](../requisitos/rf-agenda.md#rf-28) | Consultar as regras de agenda | [UC-04 Solicitar reserva](#uc-04) | fluxo principal (as regras aparecem no pedido) | [UC-06](#uc-06) |
| [RF-29](../requisitos/rf-agenda.md#rf-29) | Ver os horários ocupados de um espaço num dia | [UC-06 Consultar agenda do dia](#uc-06) | fluxo principal | — |
| [RF-29.1](../requisitos/rf-agenda.md#rf-29-1) | Recusar consulta da agenda sem espaço ou sem data | [UC-06 Consultar agenda do dia](#uc-06) | exceção | — |
| [RF-29.2](../requisitos/rf-agenda.md#rf-29-2) | Recusar agenda de espaço que não é reservável | [UC-06 Consultar agenda do dia](#uc-06) | exceção | — |
| [RF-30](../requisitos/rf-agenda.md#rf-30) | Ver os horários livres de um espaço num dia | [UC-06 Consultar agenda do dia](#uc-06) | fluxo principal | — |
| [RF-31](../requisitos/rf-agenda.md#rf-31) | Saber que uma data não é reservável | [UC-06 Consultar agenda do dia](#uc-06) | alternativa (data que não é reservável) | — |
| [RF-32](../requisitos/rf-contas.md#rf-32) | Cadastrar-se como Solicitante | [UC-01 Cadastrar-se](#uc-01) | fluxo principal | — |
| [RF-32.1](../requisitos/rf-contas.md#rf-32-1) | Recusar cadastro com dados inválidos | [UC-01 Cadastrar-se](#uc-01) | exceção | — |
| [RF-32.2](../requisitos/rf-contas.md#rf-32-2) | Recusar senha fraca | [UC-01 Cadastrar-se](#uc-01) | exceção | — |
| [RF-32.3](../requisitos/rf-contas.md#rf-32-3) | Recusar e-mail ou matrícula já cadastrados | [UC-01 Cadastrar-se](#uc-01) | exceção | — |
| [RF-33](../requisitos/rf-contas.md#rf-33) | Entrar com e-mail e senha | [UC-02 Autenticar](#uc-02) | fluxo principal | — |
| [RF-33.1](../requisitos/rf-contas.md#rf-33-1) | Recusar credenciais inválidas | [UC-02 Autenticar](#uc-02) | exceção | — |
| [RF-34](../requisitos/rf-contas.md#rf-34) | Continuar identificado sem informar a senha de novo | [UC-02 Autenticar](#uc-02) | alternativa (continuar identificado) | — |
| [RF-34.1](../requisitos/rf-contas.md#rf-34-1) | Encerrar a sessão expirada | [UC-02 Autenticar](#uc-02) | exceção (sessão expirada) | — |
| [RF-35](../requisitos/rf-contas.md#rf-35) | Consultar os próprios dados | [UC-02 Autenticar](#uc-02) | alternativa (confirmar a identificação ao voltar) | — |
| [RF-36](../requisitos/rf-contas.md#rf-36) | Sair | [UC-02 Autenticar](#uc-02) | alternativa (sair) | — |
| [RF-37](../requisitos/rf-contas.md#rf-37) | Criar usuário Gestor | [UC-20 Criar usuário Gestor](#uc-20) | fluxo principal | — |
| [RF-38](../requisitos/rf-gerais.md#rf-38) | Ver o resultado de cada operação | — (todos) | transversal (qualidade de todos os casos de uso) | — |
| [RF-39](../requisitos/rf-gerais.md#rf-39) | Carregar dados de exemplo | [UC-21 Carregar dados de exemplo](#uc-21) | fluxo principal | — |
| [RF-40](../requisitos/rf-gerais.md#rf-40) | Verificar se o sistema está no ar | [UC-22 Verificar se o sistema está no ar](#uc-22) | fluxo principal | — |

## Pendências

Pontos a confirmar com o professor que afetam esta pasta (de `.claude/requisitos.md`, seção "Pontos de Atenção / A Confirmar com o Professor", arquivo local fora do Git):

- **Ponto 2, ferramenta e notação:** "UML é exigida, mas não a ferramenta (draw.io, PlantUML, Mermaid, Astah) nem a versão (UML 2.5?). Diagrama feito à mão é aceito?" Adotado provisoriamente: PlantUML e UML 2.5 ([decisão g](#decisao-g)).
- **Ponto 3, estilo do diagrama de referência:** o exemplo de A2·s24 liga os casos de uso principais com setas em sequência, que a UML estrita não prevê. Adotado provisoriamente: notação UML padrão ([decisão b](#decisao-b)).
- **Ponto 4, outros diagramas:** se sequência, C4, DER ou a jornada em raias (A3·s18) serão exigidos, ou só o diagrama de casos de uso. Nada foi feito além do diagrama de casos de uso.

Quando um ponto for respondido, a resposta vira uma DEC em [`decisoes/`](../decisoes/README.md) e esta pasta muda no mesmo PR.

**Para a REQ-04:** as fichas Cockburn de UC-02 Autenticar, UC-04 Solicitar reserva (com UC-05 e a extensão UC-06), UC-10 Alterar situação da reserva (com as quatro especializações e UC-12) e UC-14 Cadastrar espaço, com as exceções vindas dos RF de recusa listados acima e a precondição de autenticação ([decisão d](#decisao-d)).
