# US-17 · Criar o primeiro Gestor

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-17 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-17-criar-o-primeiro-gestor.md` |

História de apoio do [índice](README.md#índice-das-histórias) (diagrama UCD-02, Equipe de TI). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | TA-149 aponta para o README do backend, onde ficou o comando de criar superusuário com a divisão do README (DOC-09). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-17 |
| **Título** | Criar o primeiro Gestor |
| **História** | Como integrante da Equipe de TI, quero criar um usuário com o perfil Gestor, ou promover um Solicitante, para que o setor dos espaços possa cadastrar espaços e decidir sobre os pedidos. |
| **Valor** | Sem um Gestor, nenhum espaço é cadastrado e nenhum pedido é decidido; e só a Equipe de TI concede esse poder ([NS-11](../visao.md#necessidades)). |
| **Origem** | [UC-20 Criar usuário Gestor, passos 1 a 4](../casos-de-uso/fichas-resumidas.md#uc20-p1), alternativa [A1.1](../casos-de-uso/fichas-resumidas.md#uc20-a1-1) e exceção [E2.1](../casos-de-uso/fichas-resumidas.md#uc20-e2-1). |
| **Prioridade** | Normal — [RF-37](../requisitos/rf-contas.md#rf-37) é normal. |
| **Estimativa (Custo em Semanas)** | 0,1 (retrospectiva: o `UsuarioManager` e o administrador da AUT-02). |
| **Conversa** | "A promoção de um Solicitante tem requisito próprio?" → não; é operação da Equipe de TI pela administração ([L-10](../requisitos/srs.md#l-10), aceita). "Quem pode ser Gestor?" → quem a Equipe de TI cadastrar; o cadastro público nunca cria Gestor ([DEC-04](../decisoes/DEC-04.md)). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando (os automatizados na verificação do PR; o manual executado e registrado no ensaio), esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✓ | É instalação: não depende de nenhuma outra história. |
| **N** · Negociável | ✓ | A forma de criar e promover (comando, administração) pode mudar sem mudar a meta. |
| **V** · Valiosa | ✓ | Habilita todas as histórias do Gestor. |
| **E** · Estimável | ✓ | Usa o mecanismo de administração já existente. |
| **S** · Small | ✓ | Uma operação de administração, sem regra própria. |
| **T** · Testável | ✗ | A recusa do e-mail repetido pelo comando de administração não tem teste automatizado: só a unicidade é provada ([L-16](../requisitos/srs.md#l-16)). |

**Diagnóstico:** independente, pequena e valiosa, mas ainda precisa ser testável por inteiro (CA-03 é manual).

## Critérios de aceite

#### <a id="us-17-ca-01"></a>US-17 · CA-01 · Gestor criado (sucesso)

- **Dado** o sistema instalado e a Equipe de TI com acesso à administração
- **Quando** a Equipe de TI cria um usuário administrador informando e-mail, nome, matrícula e senha
- **Então** o usuário é criado com o perfil Gestor e acesso à administração, e, ao entrar com o e-mail e a senha, a pessoa é reconhecida como Gestor; um usuário criado pelo cadastro comum continua Solicitante
- **Origem:** [UC-20 passos 1 a 4](../casos-de-uso/fichas-resumidas.md#uc20-p1)
- **RF:** [RF-37](../requisitos/rf-contas.md#rf-37)
- **TA:** [TA-148](#ta-148)

#### <a id="us-17-ca-02"></a>US-17 · CA-02 · Promover um Solicitante (alternativa)

- **Dado** um Solicitante identificado
- **Quando** a Equipe de TI muda o perfil dele para Gestor pela administração
- **Então** ele passa a ter as permissões de Gestor já na próxima operação, sem precisar entrar de novo
- **Origem:** [UC-20 A1.1](../casos-de-uso/fichas-resumidas.md#uc20-a1-1)
- **RF:** [RF-37](../requisitos/rf-contas.md#rf-37)
- **TA:** [TA-149](#ta-149)

#### <a id="us-17-ca-03"></a>US-17 · CA-03 · E-mail já cadastrado (exceção)

- **Dado** um usuário com o e-mail "gestor@exemplo.com"
- **Quando** a Equipe de TI tenta criar outro administrador com "Gestor@Exemplo.com"
- **Então** o sistema informa que o e-mail já está em uso e pede outro; nenhum usuário é criado e o existente não muda
- **Origem:** [UC-20 E2.1](../casos-de-uso/fichas-resumidas.md#uc20-e2-1)
- **RF:** [RF-37](../requisitos/rf-contas.md#rf-37)
- **TA:** [TA-150](#ta-150)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-148"></a>TA-148 | [CA-01](#us-17-ca-01) | automatizado | `contas/tests/test_usuario_manager.py::test_create_superuser_cria_gestor_com_staff_e_superuser`; `contas/tests/test_usuario_manager.py::test_superusuario_e_gestor_e_usuario_comum_nao`; `exemplos/tests/test_carregar_dados_exemplo.py::test_login_com_cada_usuario_de_exemplo [x]` |
| <a id="ta-149"></a>TA-149 | [CA-02](#us-17-ca-02) | automatizado | `config/tests/test_perfil_lido_do_banco.py::test_solicitante_promovido_ganha_as_permissoes_com_o_mesmo_token` |
| <a id="ta-150"></a>TA-150 | [CA-03](#us-17-ca-03) | manual | **Precondição:** sistema no ar, com um usuário de e-mail conhecido. **Passos:** pela administração (o comando de criar superusuário do [README do backend](../../../../src/backend/README.md#criar-um-superusuário-acesso-ao-admin)), criar um administrador com o mesmo e-mail, em outra caixa. **Resultado esperado:** o e-mail é recusado como já usado, e nenhum usuário novo aparece na administração. Apoio automatizado (só a unicidade, sem a mensagem): `contas/tests/test_usuario_manager.py::test_email_repetido_com_caixa_diferente_viola_unicidade`. Lacuna [L-16](../requisitos/srs.md#l-16). |
