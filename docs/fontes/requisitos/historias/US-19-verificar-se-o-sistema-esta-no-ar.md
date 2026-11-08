# US-19 · Verificar se o sistema está no ar

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-19 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-19-verificar-se-o-sistema-esta-no-ar.md` |

História de apoio do [índice](README.md#índice-das-histórias) (diagrama UCD-02, Equipe de TI). Entra porque tem RF próprio ([RF-40](../requisitos/rf-gerais.md#rf-40)), com origem na [NS-16](../visao.md#necessidades) ([decisão a](README.md#decisao-a)). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | CA-03 · Cache fora do ar, com o TA-158 (automatizado); TA-156 cita o teste do health com banco e cache (Redis, AUT-08). Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-19 |
| **Título** | Verificar se o sistema está no ar |
| **História** | Como integrante da Equipe de TI, quero saber se o sistema, o banco de dados e o cache respondem para não começar uma demonstração ou um uso com o sistema fora do ar. |
| **Valor** | Um problema de instalação aparece antes da demonstração, com uma mensagem que diz o que falhou ([NS-16](../visao.md#necessidades)). |
| **Origem** | [UC-22 Verificar se o sistema está no ar, passos 1 a 3](../casos-de-uso/fichas-resumidas.md#uc22-p1) e exceções [E2.1](../casos-de-uso/fichas-resumidas.md#uc22-e2-1) e [E2.2](../casos-de-uso/fichas-resumidas.md#uc22-e2-2). |
| **Prioridade** | Esperado — [RF-40](../requisitos/rf-gerais.md#rf-40) é esperado. |
| **Estimativa (Custo em Semanas)** | 0,1 (retrospectiva: a verificação da INF-02 e a mensagem da página inicial da FE-01). |
| **Conversa** | "Precisa estar identificado?" → não; qualquer visitante pode verificar ([RNF-F04](../requisitos/rnf.md#rnf-f04), exceção declarada). "Por que a resposta com o banco fora do ar não tem teste?" → derrubar o banco no meio dos testes não foi feito ([L-08](../requisitos/srs.md#l-08)). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando (o automatizado na verificação do PR; o manual executado e registrado no ensaio), esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✓ | Não depende de nenhuma outra história. |
| **N** · Negociável | ✓ | O que é verificado e a mensagem podem mudar. |
| **V** · Valiosa | ✗ | O valor é só operacional, para a Equipe de TI e o ensaio; nenhum Solicitante ou Gestor o percebe. Entra porque há RF, não por pedido do cliente. |
| **E** · Estimável | ✓ | Uma verificação, com três respostas conhecidas. |
| **S** · Small | ✓ | A menor história do conjunto. |
| **T** · Testável | ✗ | A exceção do banco fora do ar só tem roteiro manual ([L-08](../requisitos/srs.md#l-08)); a do cache tem teste automatizado. |

**Diagnóstico:** independente e pequena, mas pouco valiosa para o negócio e ainda não testável por inteiro.

## Critérios de aceite

#### <a id="us-19-ca-01"></a>US-19 · CA-01 · Sistema no ar (sucesso)

- **Dado** o sistema e o banco de dados funcionando
- **Quando** qualquer pessoa, mesmo sem entrar, pede a verificação do sistema
- **Então** o sistema informa "API no ar."
- **Origem:** [UC-22 passos 1 a 3](../casos-de-uso/fichas-resumidas.md#uc22-p1)
- **RF:** [RF-40](../requisitos/rf-gerais.md#rf-40)
- **TA:** [TA-156](#ta-156)

#### <a id="us-19-ca-02"></a>US-19 · CA-02 · Banco de dados fora do ar (exceção)

- **Dado** o sistema no ar e o banco de dados parado
- **Quando** a Equipe de TI pede a verificação do sistema
- **Então** o sistema informa "Não foi possível conectar ao banco de dados." e nada muda
- **Origem:** [UC-22 E2.1](../casos-de-uso/fichas-resumidas.md#uc22-e2-1)
- **RF:** [RF-40](../requisitos/rf-gerais.md#rf-40)
- **TA:** [TA-157](#ta-157)

#### <a id="us-19-ca-03"></a>US-19 · CA-03 · Cache fora do ar (exceção)

- **Dado** o sistema e o banco de dados no ar e o cache parado
- **Quando** a Equipe de TI pede a verificação do sistema
- **Então** o sistema informa "Não foi possível conectar ao cache." e nada muda
- **Origem:** [UC-22 E2.2](../casos-de-uso/fichas-resumidas.md#uc22-e2-2)
- **RF:** [RF-40](../requisitos/rf-gerais.md#rf-40)
- **TA:** [TA-158](#ta-158)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-156"></a>TA-156 | [CA-01](#us-19-ca-01) | automatizado | `reservas/tests/test_api_permissoes.py::test_vocabularios_e_health_nao_exigem_login [x]`; `config/tests/test_health.py::test_health_confere_o_banco_e_o_cache`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]` |
| <a id="ta-157"></a>TA-157 | [CA-02](#us-19-ca-02) | manual | **Precondição:** sistema no ar pelo Docker Compose. **Passos:** parar só o serviço do banco de dados; pedir a verificação do sistema; religar o banco e pedir de novo. **Resultado esperado:** com o banco parado, "Não foi possível conectar ao banco de dados."; religado, "API no ar.". Sem teste automatizado: lacuna [L-08](../requisitos/srs.md#l-08). |
| <a id="ta-158"></a>TA-158 | [CA-03](#us-19-ca-03) | automatizado | `config/tests/test_health.py::test_health_com_o_redis_fora_do_ar_responde_503` |
