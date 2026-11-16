# CR-07 — Gestão de usuários pelo Gestor

| Identificação | Responsabilidade |
|---|---|
| **CR-07 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

Pedido de mudança aberto na tarefa AUT-11, no [modelo de CR](modelo-cr.md), porque a [Visão](../visao.md#fora-do-escopo) lista "trocar o perfil pela tela" como fora do escopo, a premissa P-06 diz que o Gestor só é criado pela Equipe de TI e a lacuna [L-10](../requisitos/srs.md#l-10) (b) aceita a administração como único caminho. A decisão do grupo é a [DEC-27](../decisoes/DEC-27.md). A especificação entregue em 13/11/2026 não foi alterada.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 16/11/2026 | Max Zimmermann dos Reis | Abertura, aplicação na fonte oficial e implementação na tarefa AUT-11, no mesmo PR. Sem aprovação. |

## 1. Solicitação

| Campo | Conteúdo |
|---|---|
| **Motivo** | Promover um Gestor ou bloquear uma conta depende hoje da Equipe de TI e da administração do Django, que não é ator do negócio. |
| **Solicitante** | Max Zimmermann dos Reis (grupo). |
| **Responsável** | Max Zimmermann dos Reis. |
| **Estado** | **Implementado** (16/11/2026, AUT-11: especificação e código no mesmo PR) |
| **Origem** | [DEC-27](../decisoes/DEC-27.md); tarefa AUT-11. |
| **Baseline vigente** | [Conecta Campus — Requisitos 1.0 (candidata)](../baselines/conecta-campus-1.0-candidata.md), até a nova ser aprovada. |

## 2. Classificação (A4·s17)

- [ ] **Editorial:** corrige o texto e mantém a obrigação; registra-se a correção.
- [x] **Comportamental:** o sistema ganha operações novas (listar usuários; promover, rebaixar, desativar e reativar), com recusas, limite de tentativas e proteção contra ficar sem Gestor.

## 3. Mapa de impacto

| Elo | Afetados | Muda o quê |
|---|---|---|
| NS | [NS-11](../visao.md#ns-11) | Passa a cobrir também a gestão de usuários pelo Gestor; nenhuma necessidade nova. |
| RF / RNF | [RF-42](../requisitos/rf-contas.md#rf-42), [RF-43](../requisitos/rf-contas.md#rf-43), [RF-43.1](../requisitos/rf-contas.md#rf-43-1), [RF-43.2](../requisitos/rf-contas.md#rf-43-2) (novos); [RNF-F07](../requisitos/rnf.md#rnf-f07) | A conta desativada perde o acesso também por esta via. |
| UC (passo, alternativa ou exceção) | [UC-23](../casos-de-uso/README.md#uc-23) (novo); [UC-20 A1.1](../casos-de-uso/fichas-resumidas.md#uc20-a1-1) | A alternativa "promover pela administração" continua; a tela é um segundo caminho. |
| US / CA | [US-22](../historias/US-22-gerir-usuarios.md) (nova, CA-01 a CA-08) | História nova. |
| TA | TA-201 a TA-208 | Novos, ao fim da numeração; nenhum TA existente é renumerado. |
| Endpoint ou tela (complementar) | `GET /api/usuarios/`; `PATCH /api/usuarios/{id}/`; tela `/usuarios` | Novos. |
| Código (complementar) | `ListarUsuarios`, `AlterarUsuario`, `garantir_alteracao_permitida`, `RepositorioGestaoDeUsuariosDjango`, `UsuariosView`, `UsuarioDetalheView`, `PaginaUsuarios` | Novos. |
| DEC | [DEC-27](../decisoes/DEC-27.md) (nova) | A [DEC-04](../decisoes/DEC-04.md) e a [DEC-26](../decisoes/DEC-26.md) não mudam. |

## 4. Diferença

| Artefato | Antes | Depois |
|---|---|---|
| Visão, fora do escopo | "Recuperar senha por e-mail; trocar o perfil pela tela" | "Recuperar senha por e-mail; criar usuário e redefinir a senha de outra pessoa pela tela" (o perfil e a situação da conta entram) |
| Visão, P-06 | Gestor só é criado pela Equipe de TI | Gestor é criado pela Equipe de TI ou promovido por outro Gestor; nunca pelo cadastro público |
| SRS, L-10 (b) | A administração é o único caminho; aceitar | Fechada: o Gestor tem a tela, e a administração continua para a Equipe de TI |
| Sistema | Só a administração muda perfil e situação | O Gestor lista, promove, rebaixa, desativa e reativa, sem ficar sem Gestor ativo |

## 5. Critérios de aceite

- **Dado** um Gestor identificado **Quando** ele promove um Solicitante e confirma **Então** a pessoa passa a ter os poderes de Gestor na próxima ação dela (US-22 · CA-02; TA-202).
- **Dado** um Gestor identificado **Quando** ele tenta rebaixar ou desativar a própria conta, ou o último Gestor ativo **Então** o pedido é recusado com o motivo e nada muda (US-22 · CA-06 e CA-07; TA-206 e TA-207).

## 6. Regressão

- Rever US-02 e US-03 (entrada e sessão): a conta desativada continua recebendo a mesma resposta de credenciais inválidas.
- Cenário que não deve mudar: o cadastro público cria só Solicitantes ([RF-32](../requisitos/rf-contas.md#rf-32)).

## 7. Decisão

| Campo | Conteúdo |
|---|---|
| **Decisão** | Aceita pelo grupo e aplicada na especificação e no código, na tarefa AUT-11. |
| **Quem decidiu e quando** | Grupo, em 16/11/2026 ([DEC-27](../decisoes/DEC-27.md)). |
| **Justificativa** | O perfil já é lido do banco a cada pedido e a conta inativa já é recusada em todo lugar; o custo é pequeno e não afeta as seis funcionalidades mínimas. |
| **Referência candidata** | Manifesto da [baseline candidata](../baselines/conecta-campus-1.0-candidata.md), regerado no mesmo PR. |
