# CR-08 — Login como tela inicial (sem a tela de Início)

| Identificação | Responsabilidade |
|---|---|
| **CR-08 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

Pedido de mudança aberto na tarefa FE-09, no [modelo de CR](modelo-cr.md), a partir de um ajuste achado em teste manual em 20/11/2026, depois da baseline 1.0 candidata. A baseline não foi alterada; o manifesto candidato é regerado no mesmo conjunto de mudanças.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 20/11/2026 | Max Zimmermann dos Reis | Abertura, aplicação na fonte oficial e implementação na tarefa FE-09, no mesmo conjunto de mudanças. Sem aprovação. |

## 1. Solicitação

| Campo | Conteúdo |
|---|---|
| **Motivo** | No teste manual de 20/11/2026, a tela de Início (texto de apresentação, atalhos e a situação da API) e o item "Início" do menu se mostraram desnecessários: a pessoa deve cair direto no login. |
| **Solicitante** | Max Zimmermann dos Reis (grupo). |
| **Responsável** | Max Zimmermann dos Reis. |
| **Estado** | **Implementado** (20/11/2026, FE-09: especificação e código no mesmo conjunto de mudanças; aprovação do grupo pendente) |
| **Origem** | Ajuste de teste manual em 20/11/2026; tarefa FE-09. Sem DEC. |
| **Baseline vigente** | [Conecta Campus — Requisitos 1.0 (candidata)](../baselines/conecta-campus-1.0-candidata.md), até a nova ser aprovada. |

## 2. Classificação (A4·s17)

- [ ] **Editorial:** corrige o texto e mantém a obrigação; registra-se a correção.
- [x] **Comportamental:** some uma tela e muda para onde a raiz, os endereços desconhecidos e o "Sair" levam. O resultado observável de [RF-40](../requisitos/rf-gerais.md#rf-40) deixa de existir na interface.

## 3. Mapa de impacto

| Elo | Afetados | Muda o quê |
|---|---|---|
| NS | [NS-16](../visao.md#ns-16) | A necessidade de saber se o sistema está no ar passa a ser atendida só pela rota de verificação, sem tela. |
| RF / RNF | [RF-36](../requisitos/rf-contas.md#rf-36), [RF-40](../requisitos/rf-gerais.md#rf-40), [RNF-U02](../requisitos/rnf.md#rnf-u02) | RF-36: depois de sair, a pessoa volta à entrada do sistema. RF-40: a obrigação e as mensagens continuam em `GET /api/health/`; só a exibição na tela de Início sai. RNF-U02: 8 de 8 telas. |
| UC (passo, alternativa ou exceção) | [UC-02 A4.3](../casos-de-uso/UC-02-autenticar.md#a4-3), [UC-22](../casos-de-uso/fichas-resumidas.md#uc-22) | A4.3: "volta à entrada do sistema". UC-22 não muda de texto: a Equipe de TI já verifica pela rota. |
| US / CA | [US-03 · CA-02](../historias/US-03-manter-e-encerrar-a-sessao.md#us-03-ca-02); [US-19](../historias/US-19-verificar-se-o-sistema-esta-no-ar.md) | CA-02: "volta à entrada do sistema". US-19 não muda nos critérios. |
| TA | TA-19 (US-03 · CA-02) | Nenhum TA novo ou renumerado; o TA-19 continua cobrindo o sair. |
| Endpoint ou tela (complementar) | tela `/` removida; `/` e rotas desconhecidas passam a redirecionar | Sem endpoint novo; `GET /api/health/` não muda. |
| Código (complementar) | `RotasDaAplicacao`, `ITENS_DE_NAVEGACAO`, `Navegacao`; removidos `PaginaInicial`, `PaginaNaoEncontrada` e `api/saude.ts` | Ver a diferença. |
| DEC | — | Nenhuma DEC muda. |

## 4. Diferença

| Artefato | Antes | Depois |
|---|---|---|
| SRS 4.1 | Tela "Início (`/`)" | Sem a tela; a descrição da tela Entrar diz que ela é a inicial |
| Menu | Primeiro item "Início" | Sem o item; sem sessão, sem menu |
| `/` | Tela de Início | Sem sessão, tela de entrar; com sessão, `/reservas` (Gestor e Solicitante) |
| Endereço desconhecido | Tela "Página não encontrada" | O mesmo redirecionamento de `/` |
| Sair | Leva à tela de Início | Leva a `/`, e daí à tela de entrar |
| RF-40 | Mostrado também na tela de Início | Só `GET /api/health/` (e o `healthcheck` do Compose) |

## 5. Critérios de aceite

- **Dado** uma pessoa sem sessão **Quando** abre `/` ou um endereço que não existe **Então** vê a tela de entrar (`RotasDaAplicacao.test.tsx`).
- **Dado** um Gestor ou um Solicitante com sessão **Quando** abre `/` ou um endereço que não existe **Então** vai para as reservas, sem passar pelo login nem entrar em laço (`RotasDaAplicacao.test.tsx`).
- **Dado** qualquer perfil, ou sem sessão **Quando** olha o cabeçalho **Então** não há "Início" (`Layout.test.tsx`, `navegacao.test.ts`).
- **Dado** o sistema no ar **Quando** se pede `GET /api/health/` **Então** o resultado é o mesmo de antes (`config/tests/test_health.py`, sem alteração).

## 6. Regressão

- Rever US-02 e US-03 (entrar, sessão e sair): o destino pós-login (`/reservas`, ou o `?proximo` seguro) não muda.
- Rever o `healthcheck` do `backend` e do `nginx` (usam `/api/health/` e `/`): `/` continua servindo a aplicação.
- Cenário que não deve mudar: a sessão só cai num refresh recusado; os redirecionamentos não mudam o tratamento de 401.

## 7. Decisão

| Campo | Conteúdo |
|---|---|
| **Decisão** | Aplicada na especificação e no código na tarefa FE-09; aguardando a aprovação do grupo. |
| **Quem decidiu e quando** | Pedido do grupo no teste manual de 20/11/2026; sem DEC. |
| **Justificativa** | O login como porta de entrada é o uso real; a verificação do sistema continua existindo na rota e no `healthcheck`, que são o que a Equipe de TI usa. |
| **Referência candidata** | Manifesto da [baseline candidata](../baselines/conecta-campus-1.0-candidata.md), regerado no mesmo conjunto de mudanças. |
