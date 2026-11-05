# DEC-03 — Arquivos do Docker na estrutura do ZIP

| Identificação | Responsabilidade |
|---|---|
| **DEC-03 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Decidida |
| **Pergunta** | O ZIP precisa ter exatamente `README.md`, `src/` e `docs/`. Os arquivos do Docker (`docker-compose.yml`, `.env.example`) podem ficar dentro de `src/`? |
| **Decisão** | "Não tem problema utilizar o Docker." (resposta registrada junto com a [DEC-02](DEC-02.md)). O grupo mantém `docker-compose.yml` e `.env.example` dentro de `src/`. |
| **Motivo** | Resposta do professor; a localização dos arquivos é a forma de respeitar a estrutura obrigatória do ZIP. |
| **Alternativas** | `docker-compose.yml` na raiz do ZIP, o que quebraria a estrutura exigida. |
| **Responsável** | Professor (resposta); grupo (localização dos arquivos). |
| **Prazo** | Não registrado. |
| **Artefatos afetados** | Estrutura de `src/`; README (os comandos rodam a partir de `src/`); `scripts/empacotar_entrega.py`. · **REQ-06:** nenhuma história; 0 critérios de aceite e 0 testes de aceite ([mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-03)). |
| **Origem** | Ponto a confirmar 3 do `CLAUDE.md` ("Estrutura do ZIP"). |
| **Observações** | **Ambiguidade:** a resposta do professor não menciona o ZIP nem a localização dos arquivos; ela libera o Docker. Manter os arquivos dentro de `src/` é decisão do grupo, derivada dessa liberação. A data e o texto exato da pergunta não foram registrados; a pergunta acima foi reconstruída a partir do título do ponto a confirmar. |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Migrada de `.claude/requisitos.md` para a fonte oficial, no modelo A4·s13 (REQ-01). |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as histórias e o número de critérios e testes de aceite, a partir do [mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-03) (REQ-06). Estado e opção sem mudança. |
