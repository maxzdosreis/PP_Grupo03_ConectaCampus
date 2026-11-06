# `compartilhado` — erros, respostas e permissão comuns

Base que os três contextos (`espacos`, `reservas`, `contas`) usam igual e não podem importar uns dos outros. Não é contexto nem app Django: não tem models e não entra em `INSTALLED_APPS`. Não importa nenhum contexto nem `config`; o `domain` de cada contexto importa `compartilhado.domain`, e só a camada `api/` importa `compartilhado.api` (contratos do import-linter no [README do backend](../README.md#regra-de-dependência-import-linter)).

## Erros de domínio (`domain/erros.py`)

Python puro. Toda exceção de um contexto herda de uma das quatro categorias, nunca direto de `ErroDeDominio` nem de `Exception`; uma que herde direto de `ErroDeDominio` é tratada como bug (500). Cada exceção define `codigo` (MAIÚSCULAS_COM_UNDERLINE), `mensagem_padrao` e, se o erro é de um campo, `campo`.

| Categoria | Quando usar | Status |
|---|---|---|
| `DadosInvalidos` | o pedido tem dados que violam uma regra | 400 |
| `RecursoNaoEncontrado` | o que foi referenciado não existe | 404 |
| `ConflitoDeEstado` | a operação contradiz o estado atual (conflito de horário, transição proibida) | 409 |
| `AcaoNaoPermitida` | o perfil não pode fazer isso (`ACAO_NAO_PERMITIDA`) | 403 |

Duas exceções concretas são comuns: `CampoObrigatorioAusente(campo, rotulo)` (`CAMPO_OBRIGATORIO_AUSENTE`, 'O campo "<rótulo>" é obrigatório.') e `TextoMuitoLongo(campo, rotulo, limite)` (`TEXTO_MUITO_LONGO`), usadas por `reservas` e `contas`.

O domínio não conhece HTTP: quem converte a categoria em status é o tratador abaixo.

## Respostas (`api/respostas.py`)

O único lugar que monta o corpo das respostas:

- `resposta_sucesso(mensagem, dados=None, status=200)` → `{"mensagem": ..., "dados": ...}`.
- `resposta_erro(codigo, mensagem, status, campos=None)` e `corpo_de_erro(codigo, mensagem, campos=None)` → `{"erro": {"codigo", "mensagem", "campos"?}}` (`campos` só aparece quando há).
- `mensagem_de_contagem(total, *, nenhum, um, varios)` escolhe a mensagem de uma lista ("Nenhuma reserva encontrada.", "1 reserva encontrada.", "{total} reservas encontradas."); o texto, com o gênero certo, fica com quem chama.

## Tratador de erros (`api/tratador_de_erros.py`)

`tratar_excecao` é o `EXCEPTION_HANDLER` do DRF (ligado por texto no `config/settings.py`). Ele responde:

- **Exceções de domínio:** o status da categoria, com `codigo`, `mensagem` e, se houver, o `campo` em `campos`.
- **Exceções do DRF e do Django**, no mesmo formato: `ValidationError` → 400 `DADOS_INVALIDOS` (com cada campo em `campos`); `ParseError` → 400 `JSON_INVALIDO`; `NotAuthenticated` e `AuthenticationFailed` → 401 `NAO_AUTENTICADO` ("Faça login para continuar."); `PermissionDenied` → 403 `ACAO_NAO_PERMITIDA`; `NotFound` e `Http404` → 404 `NAO_ENCONTRADO`; `MethodNotAllowed` → 405 `METODO_NAO_PERMITIDO`.
- **Qualquer outra exceção:** vai para o log e sai como 500 `ERRO_INTERNO` ("Ocorreu um erro inesperado. Tente novamente."), sem detalhes internos.

## Permissão (`api/permissoes.py`)

`ApenasGestor` (`BasePermission` do DRF) lê `request.user.eh_gestor` por duck typing, sem importar `contas`. É usada nas escritas de espaços; sem permissão, o DRF responde 403 `ACAO_NAO_PERMITIDA` pelo tratador. Quem pode mudar a situação de uma reserva não é permissão de endpoint, é regra do domínio de `reservas` ([README de reservas](../reservas/README.md#regras)).

## Onde mexer

Uma categoria nova de erro ou um status novo muda `domain/erros.py` e `_STATUS_POR_CATEGORIA` no tratador. Uma tradução nova de exceção do DRF muda `_TRADUTORES`. Testes em `compartilhado/tests/` (`test_erros.py`, `test_respostas.py`, `test_tratador_de_erros.py`, `test_permissoes.py`).
