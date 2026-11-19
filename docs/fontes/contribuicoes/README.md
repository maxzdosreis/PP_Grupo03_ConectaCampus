# Contribuições

**IND-06 • 0.1 • Rascunho** (índice da pasta) • Autor: [nome] • Revisor: [nome] • Aprovador: [nome]

| Versão | Data | Autor | Mudança |
|---|---|---|---|
| 0.1 | 19/11/2026 | [nome] | Criação (DOC-06). Sem aprovação. |

Fonte do `docs/contribuicoes.pdf` (no máximo 2 páginas; formato livre, sem modelo do professor, Aula 7).

- [`contribuicoes.md`](contribuicoes.md): o texto (CON-01). O PDF é montado à mão a partir do trecho entre `corpo:inicio` e `corpo:fim`, A4, margens de 2,5 cm, corpo de 11 pt, e salvo em `docs/contribuicoes.pdf`.

## Regra: só evidência

Cada linha do quadro tem uma fonte verificável (backlog, Git, levantamento, cabeçalho de documento, roteiro). Nada é atribuído por estimativa ou equilíbrio. Sem registro, a célula diz "sem registro" e o integrante preenche o marcador `[PREENCHER PELO INTEGRANTE: ...]` com o que fez e a evidência. A autoria de commit não prova contribuição por si só.

## Repetir o levantamento

Na raiz, com o CSV do backlog (que fica fora do repositório):

```powershell
python -I scripts/levantar_contribuicoes.py --csv CAMINHO\backlog-tarefas.csv
```

O script só lê: não grava no repositório, usa apenas `git log` e imprime nomes, nunca e-mails.
