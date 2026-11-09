# US-18 · Carregar os dados de exemplo

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-18 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-18-carregar-os-dados-de-exemplo.md` |

História de apoio do [índice](README.md#índice-das-histórias) (diagrama UCD-02, Equipe de TI). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-12 a TA-156 passam a TA-13 a TA-157, para o TA-12 novo da US-02 (tentativas em excesso) seguir a ordem das histórias (AUT-08). Mudança editorial, sem nova obrigação. Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-19 e TA-20 passam a TA-20 e TA-21, e TA-21 a TA-158 passam a TA-24 a TA-161, para os TA-19, TA-22 e TA-23 novos da US-03 (revogação e troca da credencial de renovação) seguirem a ordem das histórias (AUT-09). Mudança editorial, sem nova obrigação. Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-18 |
| **Título** | Carregar os dados de exemplo |
| **História** | Como integrante da Equipe de TI (ou do grupo, na demonstração), quero carregar com um comando usuários, espaços e reservas coerentes para mostrar o sistema funcionando sem montar tudo à mão. |
| **Valor** | A demonstração de 10 minutos e a correção num ambiente limpo partem do mesmo conjunto conhecido, com logins e um conflito de horário documentados ([NS-16](../visao.md#necessidades)). |
| **Origem** | [UC-21 Carregar dados de exemplo, passos 1 a 4](../casos-de-uso/fichas-resumidas.md#uc21-p1), alternativa [A3.1](../casos-de-uso/fichas-resumidas.md#uc21-a3-1) e exceções [E2.1](../casos-de-uso/fichas-resumidas.md#uc21-e2-1) e [E3.1](../casos-de-uso/fichas-resumidas.md#uc21-e3-1). |
| **Prioridade** | Esperado — [RF-39](../requisitos/rf-gerais.md#rf-39) é esperado. |
| **Estimativa (Custo em Semanas)** | 0,3 (retrospectiva: a INF-06 e o ajuste de datas e histórico da RES-07). |
| **Conversa** | "Os dados de exemplo podem ir para produção?" → não: o comando recusa fora do modo de desenvolvimento, porque cria senhas conhecidas. "Rodar duas vezes duplica?" → não. "As reservas de exemplo passam pelas regras?" → sim, pelos mesmos casos de uso. |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Usa os casos de uso de [US-01](US-01-criar-minha-conta.md), [US-05](US-05-cadastrar-espaco.md), [US-07](US-07-desativar-e-reativar-espaco.md), [US-08](US-08-solicitar-reserva.md) e [US-13](US-13-cancelar-uma-reserva.md) a [US-16](US-16-concluir-uma-reserva.md): só pode ser feita depois delas. |
| **N** · Negociável | ✓ | O conteúdo (quantos usuários, quais espaços e reservas) é escolha do grupo. |
| **V** · Valiosa | ✓ | Torna a demonstração e a correção reprodutíveis. |
| **E** · Estimável | ✓ | Só monta dados com operações que já existem. |
| **S** · Small | ✓ | Um comando, que só reaproveita operações existentes. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado. |

**Diagnóstico:** negociável, valiosa, pequena e testável, mas é a história menos independente: vem por último.

## Critérios de aceite

#### <a id="us-18-ca-01"></a>US-18 · CA-01 · Carga completa (sucesso)

- **Dado** o sistema instalado em modo de desenvolvimento, sem dados de exemplo
- **Quando** a Equipe de TI pede a carga dos dados de exemplo
- **Então** o sistema cria 1 Gestor e 2 Solicitantes, um espaço de cada tipo mais um inativo e uma reserva de cada situação, todas com o histórico coerente, sem sobreposição entre as que ocupam horário e com as reservas em aberto no futuro, e mostra o resumo do que foi criado
- **Origem:** [UC-21 passos 1 a 4](../casos-de-uso/fichas-resumidas.md#uc21-p1)
- **RF:** [RF-39](../requisitos/rf-gerais.md#rf-39)
- **TA:** [TA-154](#ta-154)

#### <a id="us-18-ca-02"></a>US-18 · CA-02 · Pronta para a demonstração (sucesso)

- **Dado** os dados de exemplo carregados
- **Quando** o grupo segue o roteiro do README
- **Então** cada usuário de exemplo entra com a senha documentada, e o horário de conflito documentado é recusado por conflito no pedido e aparece ocupado na agenda do dia
- **Origem:** [UC-21 passo 3](../casos-de-uso/fichas-resumidas.md#uc21-p3)
- **RF:** [RF-39](../requisitos/rf-gerais.md#rf-39)
- **TA:** [TA-155](#ta-155)

#### <a id="us-18-ca-03"></a>US-18 · CA-03 · Carga repetida (alternativa)

- **Dado** os dados de exemplo já carregados
- **Quando** a carga é pedida de novo
- **Então** nada é duplicado (usuário pelo e-mail, espaço pelo nome, reservas dos usuários de exemplo), e o resumo informa que os dados já existiam
- **Origem:** [UC-21 A3.1](../casos-de-uso/fichas-resumidas.md#uc21-a3-1)
- **RF:** [RF-39](../requisitos/rf-gerais.md#rf-39)
- **TA:** [TA-156](#ta-156)

#### <a id="us-18-ca-04"></a>US-18 · CA-04 · Fora do modo de desenvolvimento (exceção)

- **Dado** o sistema em modo de produção
- **Quando** a carga dos dados de exemplo é pedida
- **Então** a carga é recusada, porque criaria usuários com senhas conhecidas, e nada é criado
- **Origem:** [UC-21 E2.1](../casos-de-uso/fichas-resumidas.md#uc21-e2-1)
- **RF:** [RF-39](../requisitos/rf-gerais.md#rf-39)
- **TA:** [TA-157](#ta-157)

#### <a id="us-18-ca-05"></a>US-18 · CA-05 · Dado de exemplo que viola uma regra (exceção)

- **Dado** um dado de exemplo que não passa por uma regra do sistema, ou uma falha no meio da carga
- **Quando** a carga é pedida
- **Então** o sistema informa "Dado de exemplo inválido: «mensagem da regra»" (no caso da regra) e a carga inteira é desfeita: nada fica pela metade
- **Origem:** [UC-21 E3.1](../casos-de-uso/fichas-resumidas.md#uc21-e3-1)
- **RF:** [RF-39](../requisitos/rf-gerais.md#rf-39)
- **TA:** [TA-158](#ta-158)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-154"></a>TA-154 | [CA-01](#us-18-ca-01) | automatizado | `exemplos/tests/test_carregar_dados_exemplo.py::test_cria_um_gestor_e_dois_solicitantes`; `exemplos/tests/test_carregar_dados_exemplo.py::test_cria_um_espaco_de_cada_tipo_e_um_inativo`; `exemplos/tests/test_carregar_dados_exemplo.py::test_cria_uma_reserva_de_cada_situacao`; `exemplos/tests/test_carregar_dados_exemplo.py::test_todas_as_reservas_de_exemplo_tem_historico_coerente`; `exemplos/tests/test_carregar_dados_exemplo.py::test_reservas_que_ocupam_horario_nao_se_sobrepoem`; `exemplos/tests/test_carregar_dados_exemplo.py::test_reservas_em_aberto_sao_futuras_e_a_concluida_e_passada`; `exemplos/tests/test_carregar_dados_exemplo.py::test_primeira_execucao_informa_o_que_foi_criado` |
| <a id="ta-155"></a>TA-155 | [CA-02](#us-18-ca-02) | automatizado | `exemplos/tests/test_carregar_dados_exemplo.py::test_login_com_cada_usuario_de_exemplo [x]`; `exemplos/tests/test_carregar_dados_exemplo.py::test_horario_de_conflito_documentado_responde_409`; `exemplos/tests/test_carregar_dados_exemplo.py::test_horario_de_conflito_documentado_aparece_ocupado_na_agenda_do_dia`; `exemplos/tests/test_carregar_dados_exemplo.py::test_nenhum_dado_de_exemplo_usa_o_usuario_do_readme` |
| <a id="ta-156"></a>TA-156 | [CA-03](#us-18-ca-03) | automatizado | `exemplos/tests/test_carregar_dados_exemplo.py::test_rodar_duas_vezes_nao_duplica_e_informa_que_ja_existiam` |
| <a id="ta-157"></a>TA-157 | [CA-04](#us-18-ca-04) | automatizado | `exemplos/tests/test_carregar_dados_exemplo.py::test_com_debug_desligado_recusa_sem_criar_nada` |
| <a id="ta-158"></a>TA-158 | [CA-05](#us-18-ca-05) | automatizado | `exemplos/tests/test_carregar_dados_exemplo.py::test_dado_de_exemplo_que_viola_regra_faz_o_comando_falhar`; `exemplos/tests/test_carregar_dados_exemplo.py::test_falha_no_meio_da_carga_nao_deixa_nada_gravado` |
