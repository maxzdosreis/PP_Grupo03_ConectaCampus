# Modelagem — fonte do `docs/modelagem.pdf`

**MOD-00 • 0.1 • Rascunho**

| Papel | Nome |
|---|---|
| Autor | Max Zimmermann dos Reis |
| Revisor | Matheus Cezar Santos |
| Aprovador | Eduardo Almeida da Cunha |

| Versão | Data | Autor | Mudança |
|---|---|---|---|
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Criação da pasta, plano do PDF e seção 1 (Visão do sistema, DOC-01) |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Seção 2 (Modelo do domínio e estados da reserva, DOC-02): figuras 3 e 4, verificação e correspondência com o banco |

Esta pasta é a fonte de todo o `docs/modelagem.pdf` (Projeto de Programação, seção 6 do enunciado: no máximo 6 páginas). Ela fica em `docs/fontes/` e por isso **não entra no ZIP**: só o PDF gerado entra.

## Arquivos

| Arquivo | O que é |
|---|---|
| [`01-visao-do-sistema.md`](01-visao-do-sistema.md) | Texto da seção 1 do PDF (DOC-01) |
| [`visao-geral.mmd`](visao-geral.mmd) | Fonte da Figura 1 (visão geral) |
| [`regras-de-dependencia.mmd`](regras-de-dependencia.mmd) | Fonte da Figura 2 (regras de dependência) |
| [`02-modelo-do-dominio.md`](02-modelo-do-dominio.md) | Texto da seção 2 do PDF (DOC-02) |
| [`modelo-do-dominio.mmd`](modelo-do-dominio.mmd) | Fonte da Figura 3 (modelo do domínio, `classDiagram`) |
| [`estados-da-reserva.mmd`](estados-da-reserva.mmd) | Fonte da Figura 4 (estados da reserva, `stateDiagram-v2`) |
| `*.svg`, `*.png` | **Gerados** a partir dos `.mmd`; nunca editados à mão |
| [`configuracao-mermaid.json`](configuracao-mermaid.json) | Tema, fonte e espaçamento comuns a todas as figuras do PDF |

## Plano do PDF

| Seção do enunciado | Tarefa | Arquivo | Orçamento |
|---|---|---|---|
| 1. Visão do sistema | DOC-01 | `01-visao-do-sistema.md` | ≤ 1,5 página (medida: ~1,6; ver Pendências) |
| 2. Modelo do domínio (classes; estados da reserva) | DOC-02 | `02-modelo-do-dominio.md` | ≤ 1,5 página (medida: ~1,49; ver Pendências) |
| 3. Fluxo principal (da solicitação à mudança de situação, com uma rejeição) | DOC-03 | `03-fluxo-principal.md` | ≤ 1,5 página |
| 4. Decisões técnicas (Django/DRF, React, PostgreSQL, Docker, JWT, pastas) | DOC-04 | `04-decisoes-tecnicas.md` | ≤ 1 página |
| Folga (capa, quebras de página) | — | — | 0,5 página (0,4 depois da seção 1; 0,4 também depois da seção 2, que ficou dentro do orçamento; 0,3 se valer a nova medida da seção 1, ver Pendências) |

A montagem do `docs/modelagem.pdf` a partir desses arquivos é da DOC-04. As figuras entram no PDF pelo `.png`, na largura da área útil (16 cm numa A4 com margens de 2,5 cm).

## Decisões

- <a id="decisao-a"></a>**a) Notação: Mermaid flowchart.** É estável, versionável como texto e atende à "notação livre, legível e explicada" do enunciado. O C4 do Mermaid ficou de fora por ser experimental. Uma fonte `.mmd` por figura; o `.svg` e o `.png` são gerados, nunca editados à mão.
- <a id="decisao-b"></a>**b) Duas figuras**, para cada uma continuar legível na largura de uma A4: a Figura 1 (visão geral: os três serviços do Compose, o frontend no navegador, `config`, os três contextos com as quatro camadas, `compartilhado`, `exemplos` e o PostgreSQL) e a Figura 2 (regras de dependência de um contexto genérico e a única ligação entre contextos, com o contrato do import-linter de cada regra). As setas entre camadas, as de cada contexto para `compartilhado` e a de `reservas.infrastructure` para `espacos.publico` ficam só na Figura 2: na Figura 1 elas cruzariam a figura toda e dobrariam a altura (as tentativas estão no histórico do `.mmd`).
- <a id="decisao-c"></a>**c) Nomes reais.** Os nós usam o nome exato do módulo ou pacote (`reservas.domain`, `espacos.publico`, `compartilhado.api`); a explicação em português vai entre parênteses ou na segunda linha. Na Figura 2, `‹contexto›` vale para `espacos`, `reservas` e `contas`.
- <a id="decisao-d"></a>**d) Um estilo de linha por tipo de relação**, para não depender só da cor: contínua = depende de (importa); tracejada = implementa (a classe herda a porta `Protocol`); grossa = comunicação em rede, com o protocolo no rótulo. As cores por camada são reforço: o nome da camada está escrito em toda caixa.
- <a id="decisao-e"></a>**e) Legenda dentro de cada figura** (bloco "Legenda" no `.mmd`, para a figura se sustentar sozinha na apresentação) **e** uma tabela de legenda no texto.
- <a id="decisao-f"></a>**f) Correspondência com o código por verificação automática**, e não por revisão a olho: cada nó é mapeado a um módulo Python, a um caminho do frontend ou a um serviço do Compose em comentários `%%`, e [`scripts/verificar_visao_do_sistema.py`](../../../scripts/verificar_visao_do_sistema.py) compara as setas com o grafo real de imports. Relações sem import (rede, rotas por texto, `AUTH_USER_MODEL`) são marcadas com `%% sem-import`, com o arquivo e o trecho que as provam.
- <a id="decisao-g"></a>**g) Renderização reprodutível em Docker**, como o PlantUML da REQ-03: a imagem oficial `minlag/mermaid-cli` na tag exata **12.0.0** (publicada em 24/09/2026; a 12.0.1, de 02/11/2026, ainda não tinha duas semanas). Sem instalar Node nem Chromium.

## Convenções dos `.mmd`

```text
flowchart TB                                   (primeira linha; um %%{init}%% opcional antes)
%% modulo: NO = pacote.modulo                  nó → módulo Python de src/backend
%% modulo: NO = {ctx}.camada                   nó genérico, com %% contextos: espacos, reservas, contas
%% caminho: NO = a, b - c                      nó → arquivos do frontend (incluídos menos excluídos)
%% servico: NO = nome                          nó ou moldura → serviço do docker-compose.yml
%% imagem: servico = imagem:tag                imagem do serviço no compose
%% sem-import: A -> B | arquivo | trecho       relação sem import e o trecho que a prova
%% somente: A -> B | sufixo                    os imports A → B só podem estar nesse arquivo
%% contrato: C1 = nome exato                   contrato do import-linter citado na nota da figura
A --> B   A -.-> B   A ==> B   A ~~~ B          depende, implementa, rede, só layout (invisível)
```

Uma seta ou um nó por linha, com o rótulo entre aspas. Nós `LEG_*` (legenda) e `NOTA_*` (notas) não representam código. Uma seta para uma moldura (`subgraph`) vale para tudo o que está dentro dela.

Na seção 2 (`classDiagram` e `stateDiagram-v2`, conferidos por `scripts/verificar_modelo_do_dominio.py`):

```text
%% classe: Reserva = reservas.domain.reserva.Reserva     classe da figura → classe do código (mesmo nome)
%% referencia-por-id: A.x_id -> B | ctx.infrastructure.models.XModel.coluna
                                                         a linha "A .. B : x_id" e a coluna do banco
%% nota: Classe | src/backend/arquivo.py | trecho        nota presa à classe e o trecho que prova o que ela diz
%% papel: GESTOR = Gestor                                texto de cada PapelDoAtor nos rótulos das transições
%% motivo: motivo obrigatório                            texto que marca SITUACOES_QUE_EXIGEM_MOTIVO
namespace espacos { ... }                                um namespace por contexto (o do módulo da classe)
A *-- B : atributo   A --> B : atributo   A .. B : x_id  composição, associação, referência por id
nome: tipo   metodo(param) retorno   metodo(…)$ retorno   VALOR
                                                         atributo ou property · método público · de classe · valor de enum
```

Tipos em notação Python, exatamente como anotados no código (`int | None`, `list[SituacaoReserva]`); `…` no lugar dos parâmetros os omite. No `stateDiagram-v2`, cada rótulo é `ação · papéis [· motivo]`, e o estado composto cujo rótulo contém "ocupa o horário" agrupa as situações que ocupam horário; `NOTA_*` é legenda. As notas do Mermaid (`note`) não representam código.

## Como gerar as imagens

Na raiz do repositório. Git Bash:

```bash
MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd)/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i visao-geral.mmd -o visao-geral.svg -b white
```

```bash
MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd)/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i visao-geral.mmd -o visao-geral.png -s 3 -b white
```

```bash
MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd)/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i regras-de-dependencia.mmd -o regras-de-dependencia.svg -b white
```

```bash
MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd)/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i regras-de-dependencia.mmd -o regras-de-dependencia.png -s 3 -b white
```

Seção 2 (figuras 3 e 4):

```bash
MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd)/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i modelo-do-dominio.mmd -o modelo-do-dominio.svg -b white
```

```bash
MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd)/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i modelo-do-dominio.mmd -o modelo-do-dominio.png -s 3 -b white
```

```bash
MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd)/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i estados-da-reserva.mmd -o estados-da-reserva.svg -b white
```

```bash
MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd)/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i estados-da-reserva.mmd -o estados-da-reserva.png -s 3 -b white
```

PowerShell (os mesmos oito comandos, com `${PWD}` e sem `MSYS_NO_PATHCONV`):

```powershell
docker run --rm -v "${PWD}/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i visao-geral.mmd -o visao-geral.svg -b white
docker run --rm -v "${PWD}/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i visao-geral.mmd -o visao-geral.png -s 3 -b white
docker run --rm -v "${PWD}/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i regras-de-dependencia.mmd -o regras-de-dependencia.svg -b white
docker run --rm -v "${PWD}/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i regras-de-dependencia.mmd -o regras-de-dependencia.png -s 3 -b white
docker run --rm -v "${PWD}/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i modelo-do-dominio.mmd -o modelo-do-dominio.svg -b white
docker run --rm -v "${PWD}/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i modelo-do-dominio.mmd -o modelo-do-dominio.png -s 3 -b white
docker run --rm -v "${PWD}/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i estados-da-reserva.mmd -o estados-da-reserva.svg -b white
docker run --rm -v "${PWD}/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i estados-da-reserva.mmd -o estados-da-reserva.png -s 3 -b white
```

O PNG sai em escala 3 (2352 px de largura), nítido a 16 cm no PDF. Na largura de 16 cm, a Figura 1 ocupa 13,1 cm de altura e a Figura 2, 10,1 cm, e os rótulos ficam com cerca de 10 px (conferido numa página de 605 px no navegador): legíveis, mas no limite. Se uma figura nova ficar mais larga, simplifique os rótulos; não reduza a fonte. Na seção 2, a Figura 3 tem 1693 × 1620 px naturais (16 × 15,3 cm) e a Figura 4, 1771 × 369 (16 × 3,3 cm); ver a legibilidade nas Pendências.

## Como verificar

Na raiz, sem dependências além do Python 3.11+:

```bash
python scripts/verificar_visao_do_sistema.py
```

```bash
python scripts/verificar_modelo_do_dominio.py
```

O script falha quando: uma seta "depende de" não tem import real nem `sem-import` com trecho achado; uma seta "implementa" não tem classe que herde uma porta do destino; uma seta de rede não tem `sem-import`; um import entre módulos mapeados não tem seta (fora de `EXCECOES`); um módulo com imports não está em nenhum nó nem em `IGNORADOS`; um nó aponta para módulo, caminho ou serviço inexistente; a imagem do serviço difere do `docker-compose.yml`; um serviço do compose não aparece; um contrato citado (nas figuras ou como contrato \`Nome\` no texto) não existe no `pyproject.toml`, ou um contrato do `pyproject.toml` não aparece; um teste citado não existe; um import de `somente` está em outro arquivo. Avisa (sem falhar) quando um `.svg` ou `.png` é mais antigo que o `.mmd`. No fim, imprime a tabela "seta → import que a sustenta".

**O que ele ignora, e por quê:** as pastas `tests/` e `migrations/`; imports dentro de `if TYPE_CHECKING:` (hoje só `reservas/domain/excecoes.py:13`, dentro da mesma camada); `import type` do frontend (some no build); os arquivos de teste do frontend (`*.test.ts(x)`, `testes/`, `configuracaoDosTestes.ts`); e a cola do Django (`<contexto>/models.py`, que só reexporta os models da infraestrutura, e `contas/admin.py`, a administração do Django). O frontend entra na verificação no nível das duas caixas da Figura 1 (`api/` e o resto de `src/`).

O primeiro lê só os `.mmd` que começam com `flowchart` (seção 1). O segundo lê os `classDiagram` e `stateDiagram-v2` (seção 2) e falha quando: uma classe não existe no módulo mapeado ou tem outro nome na figura; o «estereótipo» não bate com o código («enumeration» = `StrEnum`, «objeto de valor» = `@dataclass(frozen=True)`, «Django model» = model do Django, «entidade» e «raiz do agregado» = classe comum); o namespace não é o contexto do módulo; um atributo não existe (campo de dataclass, property, `self.x` do `__init__` ou campo do model) ou tem outro tipo; um método não existe, é privado, tem outros parâmetros, outro retorno ou outro `$`; os valores de um enum não são os do código, na mesma ordem; uma composição ou associação não corresponde a um atributo do tipo da classe destino; uma referência por id não é um `*_id: int`, liga classes do mesmo contexto ou aponta para uma coluna que não é `BigIntegerField`; há `ForeignKey` entre contextos nos models; o trecho de uma nota não está no arquivo; o `stateDiagram` não é exatamente `TRANSICOES_PERMITIDAS`, a ação não é `rotulo_da_acao`, os papéis não são os de `DESTINOS_POR_PAPEL`, "motivo obrigatório" não bate com `SITUACOES_QUE_EXIGEM_MOTIVO`, o grupo "ocupa o horário" não é `SITUACOES_QUE_OCUPAM_HORARIO`, os finais não são os de `eh_final` ou o inicial não é o de `Reserva.solicitar`. Avisa (sem falhar) quando uma classe não está na coluna "Nome no código" do glossário e quando as imagens estão mais antigas que os `.mmd`. A estrutura é lida com `ast`; as tabelas de situação são importadas de `reservas.domain.situacao` e `reservas.domain.ator` (domínio puro, sem Django).

**Regra 13 do CLAUDE.md:** mudou uma camada, um contexto, uma dependência entre módulos ou um serviço do Compose → atualize o `.mmd`, gere as imagens de novo e rode a verificação **no mesmo PR**. O mesmo vale para a seção 2 ao mudar uma entidade, um atributo, um método público, um enum, uma transição ou uma referência entre contextos. O script falha se um import novo não tiver seta, então uma figura desatualizada não passa despercebida.

## Decisões da seção 2

- <a id="decisao-2a"></a>**a) Nomes reais.** O backlog cita "HistoricoSituacao", mas a classe é `RegistroDeSituacao` (`reservas/domain/registro_de_situacao.py`); o "histórico" é a sequência de registros de uma reserva (`RepositorioReservas.listar_historico`). A figura usa os nomes do código, sem tradução nem acento. O verificador recusa uma classe com outro nome (prova abaixo).
- <a id="decisao-2b"></a>**b) Onze caixas:** `EspacoEsportivo` e `TipoEspaco` (espacos); `Reserva`, `SituacaoReserva`, `RegistroDeSituacao`, `Solicitante`, `IntervaloDeHorario`, `Ator` e `PapelDoAtor` (reservas); `Usuario` («Django model», porque é ali que ele existe) e `PerfilUsuario` (contas). As regras que são funções de módulo (`regras_de_agenda`, `conflito_de_horario.garantir_horario_livre`) ficaram numa frase do texto: uma caixa «módulo» a mais não cabia em 16 cm. `EstadoDoEspaco` (estado lido, para recusar gravação desatualizada) e `DadosDeCadastro` (entrada do cadastro) são detalhes de gravação e de entrada; exceções vão para a seção 3; repositórios e `*Model` são persistência (seção 1).
- <a id="decisao-2c"></a>**c) Atributos e responsabilidades.** Atributos com nome e tipo do código, em notação Python. Um atributo mostrado como linha (composição ou associação) não se repete dentro da caixa, para a figura caber; o rótulo da linha é o nome do atributo. Como responsabilidades, só os métodos públicos que carregam regra. **Ajuste:** `eh_final`, `ocupa_horario` e `eh_gestor` são `@property` no código, não métodos; entram entre os atributos, com tipo (`eh_final: bool`), como as propriedades só de leitura de `EspacoEsportivo` (`nome`, `tipo`, `capacidade`, `ativo`). Nada de `__eq__`, `__repr__` ou funções privadas.
- <a id="decisao-2d"></a>**d) Relacionamentos como estão no código:** composição `Reserva` → `Solicitante` (1), `IntervaloDeHorario` (1) e `RegistroDeSituacao` (0..*, `registros_pendentes`: a entidade guarda só os registros ainda não gravados; o histórico gravado é lido pelo repositório); associação a `SituacaoReserva` e `Ator` → `PapelDoAtor`; **referência por id**, tracejada e sem seta, com o atributo no rótulo: `Reserva.espaco_id` → `EspacoEsportivo`, `Solicitante.usuario_id` e `RegistroDeSituacao.autor_usuario_id` → `Usuario`. No banco são `BigIntegerField`, sem chave estrangeira; a única `ForeignKey` dos models é `RegistroDeSituacaoModel.reserva`, dentro de `reservas`. **Ator × Usuario:** uma nota presa ao `Ator` diz que a API o monta a partir de `request.user` por duck typing (`reservas/api/autenticacao.py`), e que `PapelDoAtor` e `PerfilUsuario` são enums separados de propósito (contrato `reservas não importa contas`). **`Solicitante` é cópia:** nome e matrícula do momento do pedido, imutáveis (`@dataclass(frozen=True)`) e gravados em colunas próprias de `ReservaModel` (`solicitante_nome`, `solicitante_matricula`); a lista e o histórico mostram quem pediu mesmo se o cadastro mudar. **Ajuste:** `Usuario.perfil` é `CharField` (`str`), não `PerfilUsuario`; `Usuario.eh_gestor` delega a `PerfilUsuario(self.perfil).eh_gestor`. A dependência `Usuario ⇢ PerfilUsuario` ficou no texto: a seta empurrava `PerfilUsuario` para baixo e a figura passava de 16,6 cm de altura.
- <a id="decisao-2e"></a>**e) Máquina de estados** gerada da tabela: as cinco transições de `TRANSICOES_PERMITIDAS`, `[*] → SOLICITADA` (`Reserva.solicitar`, o caminho de toda reserva nova por convenção da aplicação; ver Pendências) e os três finais (`eh_final`) → `[*]`. Rótulo = `rotulo_da_acao · papéis [· motivo obrigatório]`, com os papéis de `DESTINOS_POR_PAPEL` ("Solicitante (só o dono)", porque `visivel_para` limita o solicitante às próprias reservas) e o motivo de `SITUACOES_QUE_EXIGEM_MOTIVO`. SOLICITADA e CONFIRMADA ficam no estado composto "Ocupa o horário" (`SITUACOES_QUE_OCUPAM_HORARIO`). A legenda diz que as transições não dependem do horário (DEC-13) e que qualquer outra é recusada sem mudar nada; a ordem das verificações fica para a seção 3.
- <a id="decisao-2f"></a>**f) Mesma notação da seção 1:** `configuracao-mermaid.json`, PNG em escala 3, legenda dentro da figura (nota "Legenda") e uma linha de legenda no texto. Nada depende de cor: o tipo de cada linha e o «estereótipo» estão desenhados. Duas configurações próprias: `look: classic` na Figura 3 (o visual "neo" do Mermaid 11 desenha como contínua uma linha tracejada que cruza outra, e a referência `autor_usuario_id` parecia uma ligação forte) e `state.wrappingWidth: 400` na Figura 4 (senão a legenda quebrava a cada duas palavras).
- <a id="decisao-2g"></a>**g) Verificação automática** por um script novo, [`scripts/verificar_modelo_do_dominio.py`](../../../scripts/verificar_modelo_do_dominio.py), e não por uma extensão do da DOC-01: são outras gramáticas e outra pergunta (estrutura das classes, e não grafo de imports). Ele reaproveita do primeiro os caminhos, o `Resultado` e o aviso de imagens. O da DOC-01 passou a ler só os `flowchart`, porque os `.mmd` novos davam "linha não reconhecida". A estrutura é lida com `ast`; as tabelas de situação, por import de `reservas.domain.situacao` e `reservas.domain.ator` (são valores calculados, e o domínio não importa Django: contrato `Domínio é Python puro`).

### Prova de que a verificação pega erro

Em cópias dos `.mmd` fora do repositório (`--pasta`), sem tocar nos originais:

| Alteração | Saída do script |
|---|---|
| `RegistroDeSituacao` → `HistoricoSituacao` só na figura (o `%% classe:` continua no módulo real) | `a figura chama de HistoricoSituacao a classe RegistroDeSituacao de reservas.domain.registro_de_situacao: use o nome do código`; `Reserva.registros_pendentes é 'tuple[RegistroDeSituacao, ...]' no código, não um HistoricoSituacao` |
| O mesmo, também no `%% classe:` | `a classe HistoricoSituacao não existe em reservas.domain.registro_de_situacao`, mais a linha da composição |
| Transição `CONCLUIDA --> CANCELADA` a mais | `a transição CONCLUIDA → CANCELADA não está em TRANSICOES_PERMITIDAS (reservas/domain/situacao.py:45)` |
| "motivo obrigatório" tirado de RECUSADA | `'motivo obrigatório' falta no rótulo: RECUSADA exige motivo (SITUACOES_QUE_EXIGEM_MOTIVO)` |

Nos três casos o script sai com código 1.

## Correspondência domínio → banco (fora do PDF)

A regra vive no domínio (ou no caso de uso, quando depende de outros registros); o banco a repete como última defesa, contra corridas e gravações que contornem a entidade. Os tamanhos máximos das colunas saem das constantes do domínio (`NOME_MAXIMO_CARACTERES`, `FINALIDADE_MAXIMO_CARACTERES`, `MOTIVO_MAXIMO_CARACTERES` etc.).

| Classe do domínio | Model (`infrastructure/models.py`) | Regra no domínio | Restrição no banco |
|---|---|---|---|
| `EspacoEsportivo` | `EspacoEsportivoModel` (`espacos_espaco_esportivo`) | nome único sem diferenciar caixa: `existe_com_nome` no caso de uso, `NomeDeEspacoJaCadastrado` (DEC-10) | `UniqueConstraint(Lower("nome"))` `espacos_espaco_esportivo_nome_unico_sem_caixa` |
| | | capacidade ≥ `CAPACIDADE_MINIMA` (`_validar_capacidade`) | `CheckConstraint` `espacos_espaco_esportivo_capacidade_minima` |
| | | tipo em `TipoEspaco` (`_converter_tipo`) | `CheckConstraint` `espacos_espaco_esportivo_tipo_valido` |
| `Reserva` | `ReservaModel` (`reservas_reserva`) | sem sobreposição com reserva que ocupa horário: `garantir_horario_livre` | `ExclusionConstraint` `reservas_reserva_sem_sobreposicao_no_espaco` (`TsTzRange(inicio, fim, '[)')` `&&` e `espaco_id` `=`, só SOLICITADA e CONFIRMADA) |
| | | situação em `SituacaoReserva` (`_converter_situacao`) | `CheckConstraint` `reservas_reserva_situacao_valida` |
| | | motivo obrigatório para RECUSADA e CANCELADA (`_exigir_motivo_se_necessario`) | `CheckConstraint` `reservas_reserva_motivo_obrigatorio` |
| `IntervaloDeHorario` (colunas `inicio` e `fim` de `ReservaModel`) | — | término depois do início (`HorarioInvalido`) | `CheckConstraint` `reservas_reserva_fim_apos_inicio` |
| `Solicitante` (colunas `solicitante_*` de `ReservaModel`) | — | cópia imutável do usuário | `solicitante_usuario_id` é `BigIntegerField`, sem chave estrangeira para `contas` |
| `RegistroDeSituacao` | `RegistroDeSituacaoModel` (`reservas_registro_de_situacao`) | situações válidas e anterior ≠ nova (`_validar_situacoes`) | `CheckConstraint` `reservas_registro_de_situacao_situacoes_validas` e `..._anterior_diferente_da_nova`; `ForeignKey` para `ReservaModel` com `PROTECT` (mesmo contexto) |
| `Usuario` | o próprio model (`contas.Usuario`) | e-mail e matrícula únicos: `existe_email` e `existe_matricula` em `CadastrarSolicitante` | `UniqueConstraint(Lower("email"))` `contas_usuario_email_unico_sem_caixa`; `unique=True` em `email` e `matricula` |

Sem restrição no banco, de propósito: as regras de agenda (horário de funcionamento, duração e antecedência; decisão e da RES-09), que podem mudar e não podem invalidar reservas antigas, e a tabela de transições, que só vale para mudanças novas.

## Componentes e relações da seção 1 (fora do PDF)

Estas tabelas saíram do `01-visao-do-sistema.md` para a seção 1 caber no orçamento de páginas (decisão do grupo em 05/11/2026). O PDF traz as duas figuras, a legenda e um parágrafo com a razão de cada camada; aqui ficam o detalhe e o que garante cada relação. A verificação confere os contratos e os testes citados aqui também.

### Componentes

| Componente | Responsabilidade · o que **não** faz | Por que existe |
|---|---|---|
| Frontend (navegador) | Telas, sessão e `api/cliente.ts` (Bearer JWT, renova no 401) · não valida regra nem decide permissão | Funcionalidade 6 e as telas das demais |
| `frontend` (Vite) | Entrega o app · não fala com o backend | Servidor do React no Compose |
| `config` | Settings, rotas, `JWTAuthentication`, health · sem regra | Composição do Django |
| `<contexto>.api` | Valida formato, chama o caso de uso, responde · nunca usa o ORM; só `dependencias.py` vê a infraestrutura | Separa HTTP das regras |
| `<contexto>.application` | Casos de uso e portas (`Protocol`) · não conhece Django | Orquestra o domínio; testada com fakes |
| `<contexto>.domain` | Entidades, transições, exceções · não importa Django nem DRF | Regra de negócio num lugar só |
| `<contexto>.infrastructure` | Models, migrations, repositórios (model ↔ entidade) · só traduz erros do banco | Isola o ORM e o PostgreSQL |
| `espacos.publico` | Fachada `verificar_espaco_disponivel` · não expõe entidades | Única porta de `espacos` para outro contexto |
| `compartilhado` | `domain`: `ErroDeDominio` e 4 categorias; `api`: respostas, tratador de erros, `ApenasGestor` · não conhece contextos | Um formato de erro e de resposta |
| `exemplos` | Dados de exemplo pelos casos de uso · ninguém o importa | Demonstração com as regras reais |
| `db` | Dados e restrições finais (nome único, sem sobreposição) | Defesa contra corridas |

`contas` tem as quatro camadas porque tem regra própria: `DadosDeCadastro` (domínio) e `CadastrarSolicitante`, que depende das portas `RepositorioUsuarios` e `PoliticaDeSenha` e é testado com fakes; o `Usuario` do Django fica na infraestrutura.

### Relações

| Origem → destino | Tipo e motivo | Garantido por |
|---|---|---|
| Navegador → `config` | rede: HTTP/JSON com Bearer | `config/tests/test_matriz_de_acesso.py` |
| `config` → `<contexto>.api`, `contas.infrastructure` | sem import: `include()` e `AUTH_USER_MODEL` por texto; perfil por duck typing (`request.user.eh_gestor`) | `config/tests/test_perfil_lido_do_banco.py` |
| `api` → `application`, `domain`, `infrastructure` | depende; infraestrutura só em `dependencias.py` | contrato `Camadas de cada contexto` |
| `infrastructure` ⇢ `application` | implementa: repositórios herdam as portas | contrato `Camadas de cada contexto`; `reservas/tests/test_repositorio_reservas.py` |
| `domain` → `compartilhado.domain`; `api` → `compartilhado.api` | depende: erros e respostas | contratos `Domínio é Python puro` e `Só a camada api usa compartilhado.api` |
| `reservas.infrastructure` → `espacos.publico` | depende: `ConsultaDeEspacosViaFachada` | contrato `reservas só conversa com espacos pela fachada pública`; `espacos/tests/test_api_desativacao_e_reservas.py` |
| Qualquer outra entre contextos | proibida | contratos `espacos não depende de outros contextos`, `contas não depende de outros contextos`, `reservas não importa contas` |
| `exemplos` → contextos | depende: `api/dependencias.py` e o `Usuario` | contrato `Nenhum contexto depende dos dados de exemplo` |
| `infrastructure` → `db` | rede: SQL pelo ORM | `DATABASES` no `settings.py` |

## Relações sem import

| Seta | Prova (arquivo e trecho) | Por que não há import |
|---|---|---|
| Navegador → `frontend` (Vite) | `src/docker-compose.yml`: `npm run dev` | Rede: o navegador baixa o app por HTTP |
| `api/` (frontend) → `config` | `src/frontend/src/api/cliente.ts`: `` Bearer ${access} `` | Rede: HTTP/JSON com o token |
| `config` → `espacos.api`, `reservas.api`, `contas.api` | `src/backend/config/urls.py`: `include("<contexto>.api.urls")` | O Django importa as rotas a partir do texto |
| `config` → `compartilhado.api` | `src/backend/config/settings.py`: `"EXCEPTION_HANDLER": "compartilhado.api.tratador_de_erros.tratar_excecao"` | O DRF carrega o tratador pelo texto (há também um import real em `config/views.py`) |
| `config` → `contas.infrastructure` | `src/backend/config/settings.py`: `AUTH_USER_MODEL = "contas.Usuario"` | O Django resolve o model do usuário pelo texto; a API lê `request.user.eh_gestor` por duck typing (`compartilhado/api/permissoes.py`, `reservas/api/autenticacao.py`), sem importar `contas` |
| `<contexto>.infrastructure` → `db` | `src/backend/config/settings.py`: `"ENGINE": "django.db.backends.postgresql"` | Rede: SQL pelo ORM |

## Exceções da verificação

Nenhuma. A lista `EXCECOES` do script está vazia: todo import entre módulos mapeados tem uma seta numa das duas figuras.

## Pendências

- **Seção 1 um pouco acima do orçamento.** Medida em A4 (margens de 2,5 cm, texto 11 pt, tabelas 9 pt, figuras a 16 cm; Chromium do próprio `mermaid-cli`): com as tabelas de componentes e de relações no PDF, 64,7 cm (~2,6 páginas). Por decisão do grupo (05/11/2026), as duas tabelas vieram para este README ([Componentes e relações](#componentes-e-relações-da-seção-1-fora-do-pdf)), e o PDF ficou com as figuras, a legenda, um parágrafo com a razão de cada camada (regra 3 do CLAUDE.md), o caminho de uma requisição e o que ficou de fora: **39,6 cm, ~1,6 página**. As figuras somam 23,2 cm e não encolhem sem ficar ilegíveis. Os 0,1 página a mais saem da folga; se a DOC-04 precisar dela, o próximo corte é a tabela de legenda do texto, que repete a legenda das figuras.

- **Seção 2 dentro do orçamento.** Medida em A4 pelo mesmo método (margens de 2,5 cm, texto 11 pt, tabelas 9 pt, figuras a 16 cm; Chromium do `mermaid-cli`): **36,8 cm, ~1,49 página**. As figuras somam 18,6 cm (Figura 3: 15,3 cm; Figura 4: 3,3 cm). Para caber, a legenda do texto virou uma linha só, e os parágrafos de responsabilidades e de decisões ficaram curtos; o detalhe está nas decisões da seção 2 e na correspondência com o banco, acima. Na mesma medição, a seção 1 dá 42,3 cm (~1,7 página), e não os 39,6 cm registrados na DOC-01: a diferença é do CSS da medição, que não ficou registrado. Se valer a medida nova, a folga cai de 0,4 para 0,3 página.
- **Legibilidade das figuras no limite.** Numa página de 605 px (16 cm), o texto das figuras 3 e 4 fica com cerca de 5,7 e 5,5 px (fonte de 16 px × 605 / largura natural de 1693 e 1771 px), cerca de 4 pt impresso; o da seção 1 fica com ~4,6 px pela mesma conta. Estreitar a Figura 3 (tirar `situacao_anterior`, por exemplo) só aumenta a altura dela a 16 cm (num teste, 1551 px de largura deram 16,7 cm de altura) e estoura o orçamento. Se a DOC-04 achar pequeno no PDF, as saídas são uma página em paisagem para as figuras 1 e 3, ou menos atributos.
- **Divergências encontradas (o diagrama segue o código):** (1) backlog "HistoricoSituacao" × código `RegistroDeSituacao`; (2) `eh_final`, `ocupa_horario` e `eh_gestor` pedidos como métodos são `@property`; (3) `Usuario.perfil` é `str` no model, com os valores de `PerfilUsuario`; (4) a `Reserva` guarda só os registros pendentes (`registros_pendentes`), e o histórico gravado é lido pelo repositório. Glossário × código: nenhuma divergência nova; as 11 classes estão na coluna "Nome no código" (o verificador não avisou nada). As divergências que o glossário já registra continuam valendo (dois nomes para o perfil, `PapelDoAtor` × `PerfilUsuario`; "permitidas" × "disponíveis").
- **"Reserva nova só por `Reserva.solicitar`" é convenção, não invariante da classe** (achado da revisão). O construtor de `Reserva` é público e valida só o que vale em qualquer situação (`espaco_id`, finalidade, situação, motivo em Recusada e Cancelada, `criada_em` com fuso); início no futuro, regras de agenda e o registro inicial `None → SOLICITADA` só existem em `Reserva.solicitar`. Fora dos testes, quem chama o construtor é só o repositório, para reconstituir (`reservas/infrastructure/repositorio_django.py`), e quem cria reserva nova é só `CriarReserva` (`reservas/application/casos_de_uso.py`). O texto da seção 2 diz isso. Tornar a regra da classe exigiria mudar o código (por exemplo, um construtor de reconstituição separado ou um id obrigatório na reconstituição), fora do escopo desta tarefa.
- **Sem teste da cópia do solicitante.** Nenhum teste prova que mudar o nome ou a matrícula de um usuário deixa as reservas antigas como estavam; a garantia é estrutural (`Solicitante` imutável, colunas `solicitante_nome` e `solicitante_matricula` sem chave estrangeira). Fica sugerido um teste de repositório ou de API para a próxima tarefa de testes (esta tarefa não muda testes).

A verificação da DOC-01 não achou import que viole a arquitetura. Duas dependências que parecem exceção são as documentadas no CLAUDE.md e estão desenhadas: `exemplos` importa `contas.infrastructure` (o gestor de exemplo é criado com `Usuario.objects.create_superuser`, porque não há caso de uso para gestor) e `espacos.publico` importa `espacos.infrastructure` (a fachada monta `VerificarEspacoDisponivel` com o repositório Django).

## Evidência: seta → import

Saída de `python scripts/verificar_visao_do_sistema.py` em 05/11/2026 (as três primeiras ocorrências de cada seta; `(+N)` = quantas mais):

| Figura | Seta | Tipo | Sustentada por (arquivo:linha) |
|---|---|---|---|
| regras-de-dependencia.mmd | ‹contexto›.api → ‹contexto›.application | depende | contas/api/dependencias.py:1; espacos/api/dependencias.py:1; reservas/api/dependencias.py:6 (+1) |
| regras-de-dependencia.mmd | ‹contexto›.api → ‹contexto›.domain | depende | contas/api/serializers.py:3; espacos/api/serializers.py:3; espacos/api/views.py:15 (+5) |
| regras-de-dependencia.mmd | ‹contexto›.api → ‹contexto›.infrastructure | depende | contas/api/dependencias.py:2; contas/api/dependencias.py:3; espacos/api/dependencias.py:9 (+2) |
| regras-de-dependencia.mmd | ‹contexto›.application → ‹contexto›.domain | depende | contas/application/casos_de_uso.py:7; contas/application/casos_de_uso.py:8; contas/application/portas.py:4 (+18) |
| regras-de-dependencia.mmd | ‹contexto›.infrastructure → ‹contexto›.application | implementa | espacos/infrastructure/repositorio_django.py:14 RepositorioEspacosDjango(RepositorioEspacos); reservas/infrastructure/consulta_de_espacos.py:5 ConsultaDeEspacosViaFachada(ConsultaDeEspacos); reservas/infrastructure/repositorio_django.py:21 RepositorioReservasDjango(RepositorioReservas) (+7) |
| regras-de-dependencia.mmd | ‹contexto›.infrastructure → ‹contexto›.domain | depende | contas/infrastructure/models.py:5; contas/infrastructure/models.py:11; contas/infrastructure/models.py:12 (+19) |
| regras-de-dependencia.mmd | ‹contexto›.api → compartilhado.api | depende | contas/api/views.py:11; espacos/api/views.py:5; espacos/api/views.py:6 (+1) |
| regras-de-dependencia.mmd | ‹contexto›.application → compartilhado.domain | depende | contas/application/casos_de_uso.py:1 |
| regras-de-dependencia.mmd | ‹contexto›.domain → compartilhado.domain | depende | contas/domain/cadastro.py:3; contas/domain/excecoes.py:3; espacos/domain/espaco_esportivo.py:3 (+6) |
| regras-de-dependencia.mmd | compartilhado.api → compartilhado.domain | depende | compartilhado/api/tratador_de_erros.py:10 |
| regras-de-dependencia.mmd | reservas.infrastructure → reservas.application | implementa | reservas/infrastructure/consulta_de_espacos.py:5 ConsultaDeEspacosViaFachada(ConsultaDeEspacos); reservas/infrastructure/repositorio_django.py:21 RepositorioReservasDjango(RepositorioReservas); reservas/infrastructure/consulta_de_espacos.py:2 (+1) |
| regras-de-dependencia.mmd | reservas.infrastructure → espacos.publico | depende | reservas/infrastructure/consulta_de_espacos.py:1 |
| regras-de-dependencia.mmd | espacos.publico → espacos.application | depende | espacos/publico.py:3 |
| regras-de-dependencia.mmd | espacos.publico → espacos.infrastructure | depende | espacos/publico.py:4 |
| visao-geral.mmd | páginas, componentes e hooks → api/ | depende | src/frontend/src/components/espacos/DialogoDeAtivacao.tsx:2; src/frontend/src/components/espacos/DialogoDeEdicaoDeEspaco.tsx:2; src/frontend/src/components/espacos/FormularioDeEspaco.tsx:2 (+20) |
| visao-geral.mmd | páginas, componentes e hooks → Vite :5173 | rede | sem import: src/docker-compose.yml:33 `npm run dev` |
| visao-geral.mmd | api/ → config | rede | sem import: src/frontend/src/api/cliente.ts:56 `Bearer ${access}` |
| visao-geral.mmd | config → espacos.api | depende | sem import: src/backend/config/urls.py:10 `include("espacos.api.urls")` |
| visao-geral.mmd | config → reservas.api | depende | sem import: src/backend/config/urls.py:11 `include("reservas.api.urls")` |
| visao-geral.mmd | config → contas.api | depende | sem import: src/backend/config/urls.py:9 `include("contas.api.urls")` |
| visao-geral.mmd | config → contas.infrastructure | depende | sem import: src/backend/config/settings.py:108 `AUTH_USER_MODEL = "contas.Usuario"` |
| visao-geral.mmd | config → compartilhado.api | depende | sem import: src/backend/config/settings.py:143 `"EXCEPTION_HANDLER": "compartilhado.api.tratador_de_erros.tratar_excecao"`; config/views.py:10 |
| visao-geral.mmd | exemplos → [contextos] | depende | exemplos/carga.py:5; exemplos/carga.py:6; exemplos/carga.py:7 (+11) |
| visao-geral.mmd | exemplos → compartilhado.domain | depende | exemplos/management/commands/carregar_dados_exemplo.py:8 |
| visao-geral.mmd | espacos.infrastructure → db | rede | sem import: src/backend/config/settings.py:98 `"ENGINE": "django.db.backends.postgresql"` |
| visao-geral.mmd | reservas.infrastructure → db | rede | sem import: src/backend/config/settings.py:98 `"ENGINE": "django.db.backends.postgresql"` |
| visao-geral.mmd | contas.infrastructure → db | rede | sem import: src/backend/config/settings.py:98 `"ENGINE": "django.db.backends.postgresql"` |

## Evidência: elemento do diagrama → código (seção 2)

Saída de `python scripts/verificar_modelo_do_dominio.py` em 05/11/2026 (caminhos a partir de `src/backend/`):

| Figura | Elemento do diagrama | Onde está no código (src/backend/, arquivo:linha) |
|---|---|---|
| modelo-do-dominio.mmd | classe EspacoEsportivo | espacos/domain/espaco_esportivo.py:27 |
| modelo-do-dominio.mmd | EspacoEsportivo.id: int \| None | espacos/domain/espaco_esportivo.py:37 |
| modelo-do-dominio.mmd | EspacoEsportivo.nome: str | espacos/domain/espaco_esportivo.py:45 |
| modelo-do-dominio.mmd | EspacoEsportivo.tipo: TipoEspaco | espacos/domain/espaco_esportivo.py:49 |
| modelo-do-dominio.mmd | EspacoEsportivo.capacidade: int | espacos/domain/espaco_esportivo.py:53 |
| modelo-do-dominio.mmd | EspacoEsportivo.ativo: bool | espacos/domain/espaco_esportivo.py:57 |
| modelo-do-dominio.mmd | EspacoEsportivo.alterar_dados() | espacos/domain/espaco_esportivo.py:71 |
| modelo-do-dominio.mmd | EspacoEsportivo.desativar() | espacos/domain/espaco_esportivo.py:87 |
| modelo-do-dominio.mmd | EspacoEsportivo.ativar() | espacos/domain/espaco_esportivo.py:92 |
| modelo-do-dominio.mmd | EspacoEsportivo.garantir_que_esta_ativo() | espacos/domain/espaco_esportivo.py:97 |
| modelo-do-dominio.mmd | classe TipoEspaco | espacos/domain/tipo_espaco.py:4 |
| modelo-do-dominio.mmd | TipoEspaco.QUADRA_POLIESPORTIVA | espacos/domain/tipo_espaco.py:5 |
| modelo-do-dominio.mmd | TipoEspaco.CAMPO_DE_FUTEBOL | espacos/domain/tipo_espaco.py:6 |
| modelo-do-dominio.mmd | TipoEspaco.GINASIO | espacos/domain/tipo_espaco.py:7 |
| modelo-do-dominio.mmd | TipoEspaco.QUADRA_DE_AREIA | espacos/domain/tipo_espaco.py:8 |
| modelo-do-dominio.mmd | TipoEspaco.QUADRA_DE_TENIS | espacos/domain/tipo_espaco.py:9 |
| modelo-do-dominio.mmd | classe Reserva | reservas/domain/reserva.py:33 |
| modelo-do-dominio.mmd | Reserva.id: int \| None | reservas/domain/reserva.py:46 |
| modelo-do-dominio.mmd | Reserva.espaco_id: int | reservas/domain/reserva.py:47 |
| modelo-do-dominio.mmd | Reserva.finalidade: str | reservas/domain/reserva.py:50 |
| modelo-do-dominio.mmd | Reserva.motivo_da_situacao: str \| None | reservas/domain/reserva.py:52 |
| modelo-do-dominio.mmd | Reserva.criada_em: datetime | reservas/domain/reserva.py:55 |
| modelo-do-dominio.mmd | Reserva.solicitar() | reservas/domain/reserva.py:59 |
| modelo-do-dominio.mmd | Reserva.alterar_situacao() | reservas/domain/reserva.py:124 |
| modelo-do-dominio.mmd | Reserva.visivel_para() | reservas/domain/reserva.py:110 |
| modelo-do-dominio.mmd | Reserva.acoes_permitidas_para() | reservas/domain/reserva.py:115 |
| modelo-do-dominio.mmd | classe SituacaoReserva | reservas/domain/situacao.py:6 |
| modelo-do-dominio.mmd | SituacaoReserva.eh_final: bool | reservas/domain/situacao.py:22 |
| modelo-do-dominio.mmd | SituacaoReserva.ocupa_horario: bool | reservas/domain/situacao.py:26 |
| modelo-do-dominio.mmd | SituacaoReserva.SOLICITADA | reservas/domain/situacao.py:7 |
| modelo-do-dominio.mmd | SituacaoReserva.CONFIRMADA | reservas/domain/situacao.py:8 |
| modelo-do-dominio.mmd | SituacaoReserva.RECUSADA | reservas/domain/situacao.py:9 |
| modelo-do-dominio.mmd | SituacaoReserva.CANCELADA | reservas/domain/situacao.py:10 |
| modelo-do-dominio.mmd | SituacaoReserva.CONCLUIDA | reservas/domain/situacao.py:11 |
| modelo-do-dominio.mmd | classe Solicitante | reservas/domain/solicitante.py:8 |
| modelo-do-dominio.mmd | Solicitante.usuario_id: int | reservas/domain/solicitante.py:9 |
| modelo-do-dominio.mmd | Solicitante.nome: str | reservas/domain/solicitante.py:10 |
| modelo-do-dominio.mmd | Solicitante.matricula: str | reservas/domain/solicitante.py:11 |
| modelo-do-dominio.mmd | classe IntervaloDeHorario | reservas/domain/intervalo_de_horario.py:12 |
| modelo-do-dominio.mmd | IntervaloDeHorario.data: date | reservas/domain/intervalo_de_horario.py:13 |
| modelo-do-dominio.mmd | IntervaloDeHorario.hora_inicio: time | reservas/domain/intervalo_de_horario.py:14 |
| modelo-do-dominio.mmd | IntervaloDeHorario.hora_fim: time | reservas/domain/intervalo_de_horario.py:15 |
| modelo-do-dominio.mmd | IntervaloDeHorario.sobrepoe() | reservas/domain/intervalo_de_horario.py:30 |
| modelo-do-dominio.mmd | classe RegistroDeSituacao | reservas/domain/registro_de_situacao.py:9 |
| modelo-do-dominio.mmd | RegistroDeSituacao.situacao_anterior: SituacaoReserva \| None | reservas/domain/registro_de_situacao.py:10 |
| modelo-do-dominio.mmd | RegistroDeSituacao.motivo: str \| None | reservas/domain/registro_de_situacao.py:12 |
| modelo-do-dominio.mmd | RegistroDeSituacao.autor_usuario_id: int | reservas/domain/registro_de_situacao.py:13 |
| modelo-do-dominio.mmd | RegistroDeSituacao.autor_nome: str | reservas/domain/registro_de_situacao.py:14 |
| modelo-do-dominio.mmd | RegistroDeSituacao.registrado_em: datetime | reservas/domain/registro_de_situacao.py:15 |
| modelo-do-dominio.mmd | classe Ator | reservas/domain/ator.py:11 |
| modelo-do-dominio.mmd | Ator.usuario_id: int | reservas/domain/ator.py:12 |
| modelo-do-dominio.mmd | Ator.nome: str | reservas/domain/ator.py:13 |
| modelo-do-dominio.mmd | classe PapelDoAtor | reservas/domain/ator.py:5 |
| modelo-do-dominio.mmd | PapelDoAtor.GESTOR | reservas/domain/ator.py:6 |
| modelo-do-dominio.mmd | PapelDoAtor.SOLICITANTE | reservas/domain/ator.py:7 |
| modelo-do-dominio.mmd | classe Usuario | contas/infrastructure/models.py:57 |
| modelo-do-dominio.mmd | Usuario.id: int | config/settings.py:131 (django.db.models.BigAutoField) |
| modelo-do-dominio.mmd | Usuario.nome: str | contas/infrastructure/models.py:62 |
| modelo-do-dominio.mmd | Usuario.matricula: str | contas/infrastructure/models.py:63 |
| modelo-do-dominio.mmd | Usuario.email: str | contas/infrastructure/models.py:69 |
| modelo-do-dominio.mmd | Usuario.perfil: str | contas/infrastructure/models.py:74 |
| modelo-do-dominio.mmd | Usuario.eh_gestor: bool | contas/infrastructure/models.py:106 |
| modelo-do-dominio.mmd | classe PerfilUsuario | contas/domain/perfil.py:4 |
| modelo-do-dominio.mmd | PerfilUsuario.eh_gestor: bool | contas/domain/perfil.py:13 |
| modelo-do-dominio.mmd | PerfilUsuario.SOLICITANTE | contas/domain/perfil.py:5 |
| modelo-do-dominio.mmd | PerfilUsuario.GESTOR | contas/domain/perfil.py:6 |
| modelo-do-dominio.mmd | Reserva → Solicitante (composição, solicitante) | reservas/domain/reserva.py:48 `Solicitante` |
| modelo-do-dominio.mmd | Reserva → IntervaloDeHorario (composição, intervalo) | reservas/domain/reserva.py:49 `IntervaloDeHorario` |
| modelo-do-dominio.mmd | Reserva → RegistroDeSituacao (composição, registros_pendentes) | reservas/domain/reserva.py:98 `tuple[RegistroDeSituacao, ...]` |
| modelo-do-dominio.mmd | Reserva → SituacaoReserva (associação, situacao) | reservas/domain/reserva.py:51 `SituacaoReserva` |
| modelo-do-dominio.mmd | Ator → PapelDoAtor (associação, papel) | reservas/domain/ator.py:14 `PapelDoAtor` |
| modelo-do-dominio.mmd | Reserva.espaco_id ‥ EspacoEsportivo (por id) | reservas/domain/reserva.py:47; reservas/infrastructure/models.py:42 BigIntegerField |
| modelo-do-dominio.mmd | Solicitante.usuario_id ‥ Usuario (por id) | reservas/domain/solicitante.py:9; reservas/infrastructure/models.py:43 BigIntegerField |
| modelo-do-dominio.mmd | RegistroDeSituacao.autor_usuario_id ‥ Usuario (por id) | reservas/domain/registro_de_situacao.py:13; reservas/infrastructure/models.py:135 BigIntegerField |
| modelo-do-dominio.mmd | nota de Ator | reservas/api/autenticacao.py:15 `Ator(usuario_id=usuario.pk, nome=usuario.nome, papel=papel)` |
| (banco) | FK dentro de reservas: ReservaModel | reservas/infrastructure/models.py:113 |
| estados-da-reserva.mmd | CONFIRMADA → CANCELADA: Cancelar · Gestor ou Solicitante (só o dono) · motivo obrigatório | reservas/domain/situacao.py:53; rótulo reservas/domain/situacao.py:41; papéis reservas/domain/situacao.py:63 |
| estados-da-reserva.mmd | CONFIRMADA → CONCLUIDA: Concluir · Gestor | reservas/domain/situacao.py:53; rótulo reservas/domain/situacao.py:42; papéis reservas/domain/situacao.py:63 |
| estados-da-reserva.mmd | SOLICITADA → CANCELADA: Cancelar · Gestor ou Solicitante (só o dono) · motivo obrigatório | reservas/domain/situacao.py:46; rótulo reservas/domain/situacao.py:41; papéis reservas/domain/situacao.py:63 |
| estados-da-reserva.mmd | SOLICITADA → CONFIRMADA: Confirmar · Gestor | reservas/domain/situacao.py:46; rótulo reservas/domain/situacao.py:39; papéis reservas/domain/situacao.py:63 |
| estados-da-reserva.mmd | SOLICITADA → RECUSADA: Recusar · Gestor · motivo obrigatório | reservas/domain/situacao.py:46; rótulo reservas/domain/situacao.py:40; papéis reservas/domain/situacao.py:63 |
| estados-da-reserva.mmd | [*] → SOLICITADA | reservas/domain/reserva.py:82 Reserva.solicitar |
| estados-da-reserva.mmd | CANCELADA, CONCLUIDA, RECUSADA → [*] | reservas/domain/situacao.py:45 (eh_final: sem destinos) |
| estados-da-reserva.mmd | grupo 'ocupa o horário': CONFIRMADA, SOLICITADA | reservas/domain/situacao.py:79 |

## Para as próximas seções (DOC-03 e DOC-04)

- Use o plano do PDF acima e o orçamento de páginas; a seção 1 ocupa ~1,6 página e deixou 0,4 de folga. Meça cada seção impressa em A4 antes de fechar a tarefa, e não só pela contagem de palavras.
- Reaproveite `configuracao-mermaid.json`, as cores por camada (`classDef` dos `.mmd`) e o bloco "Legenda" dentro da figura. Para diagramas de classes ou de sequência, o Mermaid tem `classDiagram`, `stateDiagram-v2` e `sequenceDiagram`; os comandos de geração são os mesmos, trocando o nome do arquivo.
- A DOC-02 usou ~1,49 página, e a folga continua em 0,4 (0,3 pela nova medida da seção 1). A seção 3 tem 1,5 página, e a DOC-04, 1 página.
- **DOC-03 (fluxo principal):** reaproveite os nomes da Figura 4 e a ordem real das verificações, que a seção 2 deixou de fora. Em `Reserva.alterar_situacao`: `agora` com fuso (`TypeError`) → reserva não visível ao ator (`ReservaNaoEncontrada`, 404) → `SituacaoInvalida` (400) → `AlteracaoDeSituacaoNaoPermitida` (403) → `TransicaoDeSituacaoInvalida` (409) → motivo longo demais (`TextoMuitoLongo`, 400) → `MotivoObrigatorio` (400); no `salvar`, `ReservaDesatualizada` (409). Em `CriarReserva`: `Reserva.solicitar` (data e horas obrigatórias e `HorarioInvalido` em `IntervaloDeHorario` → `DataRetroativa` → `ForaDoHorarioDeFuncionamento` → `DuracaoInvalida` → `AntecedenciaExcedida` → só então o construtor: `IdentificadorDeEspacoInvalido` e finalidade obrigatória ou longa demais; todas 400) → `obter_espaco_reservavel` (`EspacoNaoEncontrado` 404, `EspacoInativo` 409) → `listar_que_ocupam_horario` → `garantir_horario_livre` (`ConflitoDeHorario`, 409) → `salvar` (a `ExclusionConstraint` ainda pode lançar `ConflitoDeHorario` numa corrida). As fichas UC-04 e UC-10 de `docs/fontes/requisitos/casos-de-uso/` têm essa ordem em linguagem de negócio.
- Um `sequenceDiagram` cabe na mesma verificação: mapeie cada participante a um módulo com `%% classe:` ou `%% modulo:` e confira as chamadas com `ast`, como aqui.
