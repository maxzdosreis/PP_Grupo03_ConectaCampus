# Requisitos do Conecta Campus — fonte oficial

Esta pasta é a **fonte oficial** dos requisitos do Conecta Campus (disciplina de Requisitos de Software), versionada no Git e organizada como no modelo do professor (A4·s10). O que vale é o que está aqui: outros arquivos (README do projeto, `modelagem.pdf`, mensagens no chat) apontam para esta pasta e não são cópias editáveis. Um PDF gerado daqui serve só para consulta e mostra a versão e a origem.

`docs/fontes/` não entra no ZIP de entrega de Projeto de Programação; os PDFs entregues são gerados a partir destes arquivos.

## Estrutura

| Caminho | O que contém | Situação |
|---|---|---|
| [`visao.md`](visao.md) | **VIS-01**, Documento de Visão (RUP, 4 quadrantes): problema, stakeholders, necessidades NS-xx, escopo, premissas, critérios de sucesso e riscos. | 0.1 • Rascunho (REQ-01) |
| [`glossario.md`](glossario.md) | **GLO-01**, termos do domínio com definição única e o nome correspondente no código. | 0.1 • Rascunho (REQ-01) |
| [`requisitos/`](requisitos/README.md) | RF-xx e RNF-xx (SRS), com ficha A4·s9. | vazia; REQ-02 |
| [`casos-de-uso/`](casos-de-uso/README.md) | UC-xx (ficha Cockburn) e o diagrama de casos de uso. | vazia; REQ-03 |
| [`historias/`](historias/README.md) | US-xx com CA-xx (Dado/Quando/Então) e TA-xx. | vazia; REQ-04 em diante |
| [`decisoes/`](decisoes/README.md) | DEC-xx, uma decisão por arquivo, com índice. | DEC-01 a DEC-11 |
| [`mudancas/`](mudancas/README.md) | CR-xx, pedidos de mudança depois de uma baseline. | vazia |
| [`baselines/`](baselines/README.md) | Manifestos de baseline (conjunto aprovado de versões). | vazia |

## Decisões de organização (REQ-01)

- **a) Fonte única.** Esta pasta é a fonte oficial. Nenhum outro lugar mantém uma cópia editável dos requisitos; os demais apontam para cá.
- **b) Decisões aqui.** As DECs saíram de `.claude/requisitos.md` (diretrizes locais da disciplina, fora do Git) e moram em [`decisoes/`](decisoes/README.md). As diretrizes de como documentar continuam naquele arquivo.
- **c) Convenção de versão** (abaixo), a do slide A4·s15. O próprio slide avisa que ela não é regra universal, e a pergunta ao professor sobre a convenção segue aberta.
- **d) Nada inventado.** O que o grupo não sabe (quem é o cliente real, o horário real de funcionamento, o formato da matrícula) aparece como premissa declarada na [Visão](visao.md#premissas) ou como DEC, nunca como afirmação.

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

Convenções do grupo, além das do professor: `VIS-01` e `GLO-01` identificam os documentos; `P-xx` (premissa), `CS-xx` (critério de sucesso) e `R-xx` (risco) valem dentro da Visão.

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
NS-xx → RF-xx → UC-xx → US-xx → CA-xx / TA-xx → código e testes
```

- Os slides param em CA/TA. O elo até o código e os testes é uma extensão do grupo, e a pergunta se ele é esperado segue aberta.
- Hoje existem as NS ([Visão](visao.md#necessidades)), cada uma ligada à funcionalidade que a atende, e as evidências do lado do código: [catálogo de testes de espaços](../testes_de_espacos.md), [catálogo de testes de reservas](../testes_de_reservas.md) e [matriz de acesso](../matriz_de_acesso.md). RF, UC, US e CA preenchem o meio da cadeia nas próximas tarefas (REQ-02 a REQ-06).
- A matriz responde a três perguntas: **impacto** (que artefatos são afetados?), **cobertura** (todo requisito tem teste?) e **justificativa** (que necessidade o originou?).

## Pontos a confirmar com o professor

A lista não é copiada aqui. Ela está em dois arquivos locais, fora do Git (por isso citados como caminho, sem link):

- `CLAUDE.md`, seção "Pontos a Confirmar com o Professor": os pontos 1, 2, 3 e 6 já foram respondidos ([DEC-01](decisoes/DEC-01.md), [DEC-02](decisoes/DEC-02.md), [DEC-03](decisoes/DEC-03.md) e [DEC-04](decisoes/DEC-04.md)); os pontos 4 e 5 seguem abertos.
- `.claude/requisitos.md`, seção "Pontos de Atenção / A Confirmar com o Professor": nenhum foi respondido por uma DEC. O ponto 10 (convenção de versão) e o ponto 13 (rastreabilidade até o código) foram **adotados provisoriamente** nesta pasta e seguem abertos.

Quando um ponto for respondido, a resposta vira uma DEC em [`decisoes/`](decisoes/README.md).
