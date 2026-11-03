# DEC-02 — Docker e PostgreSQL na correção

| Identificação | Responsabilidade |
|---|---|
| **DEC-02 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Decidida |
| **Pergunta** | O projeto pode ser executado com Docker (e o PostgreSQL dentro dele) na correção, já que o enunciado não exige banco de dados e recomenda memória ou arquivo JSON? |
| **Decisão** | "Não tem problema utilizar o Docker." (resposta registrada junto com a [DEC-03](DEC-03.md)) |
| **Motivo** | Resposta do professor. |
| **Alternativas** | Persistência em memória ou JSON e execução com `venv` + `pip`, sem Docker. |
| **Responsável** | Professor (resposta); grupo (adoção). |
| **Prazo** | Não registrado. |
| **Artefatos afetados** | `src/docker-compose.yml`, Dockerfiles, `src/.env.example`; README (pré-requisito, execução e persistência); `modelagem.pdf` (decisões técnicas); [Visão](../visao.md#restrições) (restrições) e risco R-02. |
| **Origem** | Ponto a confirmar 2 do `CLAUDE.md` ("Docker e PostgreSQL na correção"). |
| **Observações** | **Ambiguidade:** a resposta fala só de Docker. O uso do PostgreSQL é inferência do grupo: ele roda dentro do Docker Compose, então foi tratado como liberado junto. A mesma frase responde à DEC-02 e à DEC-03, e a data não foi registrada. A pergunta acima foi reconstruída a partir do título do ponto a confirmar. Se o professor discordar do PostgreSQL, registrar uma nova DEC, sem reutilizar este ID. |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Migrada de `.claude/requisitos.md` para a fonte oficial, no modelo A4·s13 (REQ-01). |
