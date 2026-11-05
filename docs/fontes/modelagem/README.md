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

Esta pasta é a fonte de todo o `docs/modelagem.pdf` (Projeto de Programação, seção 6 do enunciado: no máximo 6 páginas). Ela fica em `docs/fontes/` e por isso **não entra no ZIP**: só o PDF gerado entra.

## Arquivos

| Arquivo | O que é |
|---|---|
| [`01-visao-do-sistema.md`](01-visao-do-sistema.md) | Texto da seção 1 do PDF (DOC-01) |
| [`visao-geral.mmd`](visao-geral.mmd) | Fonte da Figura 1 (visão geral) |
| [`regras-de-dependencia.mmd`](regras-de-dependencia.mmd) | Fonte da Figura 2 (regras de dependência) |
| `*.svg`, `*.png` | **Gerados** a partir dos `.mmd`; nunca editados à mão |
| [`configuracao-mermaid.json`](configuracao-mermaid.json) | Tema, fonte e espaçamento comuns a todas as figuras do PDF |

## Plano do PDF

| Seção do enunciado | Tarefa | Arquivo | Orçamento |
|---|---|---|---|
| 1. Visão do sistema | DOC-01 | `01-visao-do-sistema.md` | ≤ 1,5 página (medida: ~1,6; ver Pendências) |
| 2. Modelo do domínio (classes; estados da reserva) | DOC-02 | `02-modelo-do-dominio.md` | ≤ 1,5 página |
| 3. Fluxo principal (da solicitação à mudança de situação, com uma rejeição) | DOC-03 | `03-fluxo-principal.md` | ≤ 1,5 página |
| 4. Decisões técnicas (Django/DRF, React, PostgreSQL, Docker, JWT, pastas) | DOC-04 | `04-decisoes-tecnicas.md` | ≤ 1 página |
| Folga (capa, quebras de página) | — | — | 0,5 página (0,4 depois da seção 1) |

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

PowerShell (os mesmos quatro comandos, com `${PWD}` e sem `MSYS_NO_PATHCONV`):

```powershell
docker run --rm -v "${PWD}/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i visao-geral.mmd -o visao-geral.svg -b white
docker run --rm -v "${PWD}/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i visao-geral.mmd -o visao-geral.png -s 3 -b white
docker run --rm -v "${PWD}/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i regras-de-dependencia.mmd -o regras-de-dependencia.svg -b white
docker run --rm -v "${PWD}/docs/fontes/modelagem:/data" minlag/mermaid-cli:12.0.0 -c configuracao-mermaid.json -i regras-de-dependencia.mmd -o regras-de-dependencia.png -s 3 -b white
```

O PNG sai em escala 3 (2352 px de largura), nítido a 16 cm no PDF. Na largura de 16 cm, a Figura 1 ocupa 13,1 cm de altura e a Figura 2, 10,1 cm, e os rótulos ficam com cerca de 10 px (conferido numa página de 605 px no navegador): legíveis, mas no limite. Se uma figura nova ficar mais larga, simplifique os rótulos; não reduza a fonte.

## Como verificar

Na raiz, sem dependências além do Python 3.11+:

```bash
python scripts/verificar_visao_do_sistema.py
```

O script falha quando: uma seta "depende de" não tem import real nem `sem-import` com trecho achado; uma seta "implementa" não tem classe que herde uma porta do destino; uma seta de rede não tem `sem-import`; um import entre módulos mapeados não tem seta (fora de `EXCECOES`); um módulo com imports não está em nenhum nó nem em `IGNORADOS`; um nó aponta para módulo, caminho ou serviço inexistente; a imagem do serviço difere do `docker-compose.yml`; um serviço do compose não aparece; um contrato citado (nas figuras ou como contrato \`Nome\` no texto) não existe no `pyproject.toml`, ou um contrato do `pyproject.toml` não aparece; um teste citado não existe; um import de `somente` está em outro arquivo. Avisa (sem falhar) quando um `.svg` ou `.png` é mais antigo que o `.mmd`. No fim, imprime a tabela "seta → import que a sustenta".

**O que ele ignora, e por quê:** as pastas `tests/` e `migrations/`; imports dentro de `if TYPE_CHECKING:` (hoje só `reservas/domain/excecoes.py:13`, dentro da mesma camada); `import type` do frontend (some no build); os arquivos de teste do frontend (`*.test.ts(x)`, `testes/`, `configuracaoDosTestes.ts`); e a cola do Django (`<contexto>/models.py`, que só reexporta os models da infraestrutura, e `contas/admin.py`, a administração do Django). O frontend entra na verificação no nível das duas caixas da Figura 1 (`api/` e o resto de `src/`).

**Regra 13 do CLAUDE.md:** mudou uma camada, um contexto, uma dependência entre módulos ou um serviço do Compose → atualize o `.mmd`, gere as imagens de novo e rode a verificação **no mesmo PR**. O script falha se um import novo não tiver seta, então uma figura desatualizada não passa despercebida.

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

## Para as próximas seções (DOC-02 a DOC-04)

- Use o plano do PDF acima e o orçamento de páginas; a seção 1 ocupa ~1,6 página e deixou 0,4 de folga. Meça cada seção impressa em A4 antes de fechar a tarefa, e não só pela contagem de palavras.
- Reaproveite `configuracao-mermaid.json`, as cores por camada (`classDef` dos `.mmd`) e o bloco "Legenda" dentro da figura. Para diagramas de classes ou de sequência, o Mermaid tem `classDiagram`, `stateDiagram-v2` e `sequenceDiagram`; os comandos de geração são os mesmos, trocando o nome do arquivo.
- O script pode ganhar uma verificação do modelo de domínio (classe e atributo do diagrama existem no código, com `ast`), no mesmo estilo dos comentários `%%`.
