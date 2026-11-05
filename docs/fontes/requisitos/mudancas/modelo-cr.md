# Modelo de pedido de mudança (CR)

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **MCR-01 • 0.1 • Rascunho** (modelo; nenhum CR foi aberto) | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/mudancas/modelo-cr.md` |

Modelo de CR no fluxo do A4·s20 (registrar → analisar → decidir → atualizar → verificar) e na estrutura do pacote de mudança da Aula 4 (solicitação, mapa de impacto, diferença e aceite, referência candidata). Para abrir um CR, copie este arquivo como `CR-xx-<assunto>.md` (próximo número livre, nunca reutilizado), numa branch `docs/CR-xx-<assunto>`, e preencha cada seção. Commit não é aprovação; push não é publicação de baseline.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Criação do modelo, com o mapa de impacto tirado da [matriz de rastreabilidade](../rastreabilidade/README.md) (REQ-06). Sem aprovação. |

---

# CR-xx — [assunto]

| Identificação | Responsabilidade |
|---|---|
| **CR-xx • 0.1 • Rascunho** | Autor: [nome] • Revisor: [nome] • Aprovador: Eduardo Almeida da Cunha (aprovador da fonte oficial) |

## 1. Solicitação

| Campo | Conteúdo |
|---|---|
| **Motivo** | Por que mudar (a resposta de uma DEC, um defeito, um pedido do cliente). |
| **Solicitante** | Quem pede. |
| **Responsável** | Quem analisa e atualiza os artefatos. |
| **Estado** | Pendente · Em análise · Aprovado · Rejeitado · Adiado |
| **Origem** | DEC-xx, lacuna L-xx ou outro pedido. |
| **Baseline vigente** | A que continua valendo até a nova ser aprovada (ex.: Conecta Campus — Requisitos 1.0). |

## 2. Classificação (A4·s17)

- [ ] **Editorial:** corrige o texto e mantém a obrigação; registra-se a correção.
- [ ] **Comportamental:** traz uma regra nova; exige o mapa de impacto, a regressão e a decisão.

O tamanho do diff não mede o risco: trocar um número numa constante pode ser comportamental.

## 3. Mapa de impacto

Nos dois sentidos ("de onde veio a regra e onde seu efeito precisa aparecer?", A4·s19). Se o CR nasce de uma DEC, copie a seção dela em [`impacto-por-dec.md`](../rastreabilidade/impacto-por-dec.md); senão, parta das linhas dos RF afetados na [matriz](../rastreabilidade/matriz.md) e do [sentido inverso](../rastreabilidade/sentido-inverso.md). Pelo menos três artefatos afetados.

| Elo | Afetados | Muda o quê |
|---|---|---|
| NS | | |
| RF / RNF | | |
| UC (passo, alternativa ou exceção) | | |
| US / CA | | |
| TA | | |
| Endpoint ou tela (complementar) | | |
| Código (complementar) | | |
| DEC | | |

## 4. Diferença

| Artefato | Antes | Depois |
|---|---|---|
| | | |

## 5. Critérios de aceite

Pelo menos dois critérios observáveis, em Dado/Quando/Então, novos ou alterados, com o TA de cada um.

## 6. Regressão

Os TAs a rever (do mapa de impacto) e pelo menos um cenário de regressão dos critérios que não deveriam mudar.

## 7. Decisão

| Campo | Conteúdo |
|---|---|
| **Decisão** | Aceita · Rejeitada · Adiada |
| **Quem decidiu e quando** | |
| **Justificativa** | Preservada mesmo se rejeitada ou adiada. |
| **Referência candidata** | Manifesto curto da nova baseline, a partir de `python scripts/gerar_rastreabilidade.py --manifesto`, e a decisão que ainda falta. |
