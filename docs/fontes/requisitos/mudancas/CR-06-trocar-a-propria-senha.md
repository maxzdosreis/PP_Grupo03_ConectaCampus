# CR-06 — Trocar a própria senha

| Identificação | Responsabilidade |
|---|---|
| **CR-06 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

Pedido de mudança aberto na tarefa AUT-10, no [modelo de CR](modelo-cr.md), porque a [Visão](../visao.md#fora-do-escopo) lista "trocar senha" como fora do escopo e diz que o que está fora só entra por um CR. A decisão do grupo é a [DEC-26](../decisoes/DEC-26.md). A especificação entregue em 13/11/2026 não foi alterada.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 16/11/2026 | Max Zimmermann dos Reis | Abertura, aplicação na fonte oficial e implementação na tarefa AUT-10, no mesmo PR. Sem aprovação. |

## 1. Solicitação

| Campo | Conteúdo |
|---|---|
| **Motivo** | Quem suspeita que a senha vazou, ou quer uma melhor, hoje depende da Equipe de TI. A [NS-15](../visao.md#ns-15) pede acesso sem depender de um gestor. |
| **Solicitante** | Max Zimmermann dos Reis (grupo). |
| **Responsável** | Max Zimmermann dos Reis. |
| **Estado** | **Implementado** (16/11/2026, AUT-10: especificação e código no mesmo PR) |
| **Origem** | [DEC-26](../decisoes/DEC-26.md); tarefa AUT-10. |
| **Baseline vigente** | [Conecta Campus — Requisitos 1.0 (candidata)](../baselines/conecta-campus-1.0-candidata.md), até a nova ser aprovada. |

## 2. Classificação (A4·s17)

- [ ] **Editorial:** corrige o texto e mantém a obrigação; registra-se a correção.
- [x] **Comportamental:** o sistema ganha uma operação nova (trocar a própria senha), com recusas, limite de tentativas e revogação das outras sessões.

## 3. Mapa de impacto

| Elo | Afetados | Muda o quê |
|---|---|---|
| NS | [NS-15](../visao.md#ns-15) | Passa a cobrir também a troca da própria senha; nenhuma necessidade nova. |
| RF / RNF | [RF-41](../requisitos/rf-contas.md#rf-41), [RF-41.1](../requisitos/rf-contas.md#rf-41-1), [RF-41.2](../requisitos/rf-contas.md#rf-41-2) (novos); [RNF-F12](../requisitos/rnf.md#rnf-f12) e [RNF-F13](../requisitos/rnf.md#rnf-f13) | O limite de tentativas e a revogação da credencial de renovação passam a valer também para a troca de senha. |
| UC (passo, alternativa ou exceção) | [UC-02 A4.4](../casos-de-uso/UC-02-autenticar.md#a4-4), [UC-02 E4.3](../casos-de-uso/UC-02-autenticar.md#e4-3) a [E4.6](../casos-de-uso/UC-02-autenticar.md#e4-6) | Alternativa e quatro exceções novas; nenhum caso de uso novo e nenhum diagrama muda. |
| US / CA | [US-21](../historias/US-21-trocar-a-propria-senha.md) (nova, CA-01 a CA-07) | História nova. |
| TA | TA-194 a TA-200 | Novos, ao fim da numeração; nenhum TA existente é renumerado. |
| Endpoint ou tela (complementar) | `POST /api/auth/senha/`; tela `/conta` | Novos. |
| Código (complementar) | `AlterarSenha`, `AlterarSenhaView`, `LimiteDeTrocaDeSenhaPorUsuario`, `FormularioDeTrocaDeSenha` | Novos. |
| DEC | [DEC-26](../decisoes/DEC-26.md) (nova) | A [DEC-04](../decisoes/DEC-04.md) não muda. |

## 4. Diferença

| Artefato | Antes | Depois |
|---|---|---|
| Visão, fora do escopo | "Recuperar ou trocar senha; trocar o perfil pela tela" | "Recuperar senha por e-mail; trocar o perfil pela tela" (a troca da própria senha entra) |
| UC-02 | Sem troca de senha | A4.4 e E4.3 a E4.6 |
| Sistema | Só a administração muda a senha | O usuário troca a própria senha, com limite de tentativas e revogação das outras sessões |

## 5. Critérios de aceite

- **Dado** um usuário identificado **Quando** ele informa a senha atual certa e uma senha nova válida **Então** a senha muda, ele continua identificado e as outras sessões deixam de renovar (US-21 · CA-01 e CA-02; TA-194 e TA-195).
- **Dado** um usuário identificado **Quando** ele erra a senha atual **Então** vê o erro junto ao campo e continua identificado (US-21 · CA-03; TA-196).

## 6. Regressão

- Rever US-02 e US-03 (entrada e sessão) e o cadastro (US-01): a política de senha é a mesma.
- Cenário que não deve mudar: o cadastro recusa senha fraca com o mesmo código `SENHA_FRACA` e o mesmo campo `senha`.

## 7. Decisão

| Campo | Conteúdo |
|---|---|
| **Decisão** | Aceita pelo grupo e aplicada na especificação e no código, na tarefa AUT-10. |
| **Quem decidiu e quando** | Grupo, em 16/11/2026 ([DEC-26](../decisoes/DEC-26.md)). |
| **Justificativa** | A infraestrutura (política de senha, limite de tentativas, revogação das credenciais de renovação) já existia; o custo é pequeno e não afeta as seis funcionalidades mínimas. |
| **Referência candidata** | Manifesto da [baseline candidata](../baselines/conecta-campus-1.0-candidata.md), regerado no mesmo PR. |
