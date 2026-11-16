# US-22 · Gerir usuários

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-22 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-22-gerir-usuarios.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 16/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, oito critérios e testes de aceite (TA-201 a TA-208), a partir da [DEC-27](../decisoes/DEC-27.md) e do [CR-07](../mudancas/CR-07-gestao-de-usuarios.md) (AUT-11). Mudança posterior à entrega de 13/11/2026. Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-22 |
| **Título** | Gerir usuários |
| **História** | Como Gestor do serviço, quero ver os usuários e promover, rebaixar, desativar e reativar contas, para dar e tirar acessos sem depender da Equipe de TI e sem deixar o sistema sem Gestor. |
| **Valor** | Quem cuida do serviço dá o perfil de Gestor a uma pessoa de confiança e bloqueia uma conta que não deve mais entrar, na hora, sem pedir à administração ([NS-11](../visao.md#ns-11)). |
| **Origem** | [UC-23 Gerir usuários](../casos-de-uso/README.md#uc-23) ([ficha resumida](../casos-de-uso/fichas-resumidas.md#uc-23)). A alternativa [UC-20 A1.1](../casos-de-uso/fichas-resumidas.md#uc20-a1-1) é o caminho da Equipe de TI para o mesmo fim. |
| **Prioridade** | Normal — a classe QFD de [RF-42](../requisitos/rf-contas.md#rf-42), [RF-43](../requisitos/rf-contas.md#rf-43), [RF-43.1](../requisitos/rf-contas.md#rf-43-1) e [RF-43.2](../requisitos/rf-contas.md#rf-43-2). |
| **Estimativa (Custo em Semanas)** | 0,5 (retrospectiva: casos de uso, domínio das regras, trava das linhas, rotas, limite de tentativas e a tela Usuários da AUT-11). |
| **Conversa** | "E se o Gestor quiser sair do cargo?" → outro Gestor faz a alteração; ninguém rebaixa nem desativa a si. "E o último Gestor?" → nunca é rebaixado nem desativado, mesmo que dois Gestores peçam ao mesmo tempo. "E as reservas de quem foi desativado?" → continuam como estão, e o Gestor pode cancelá-las ou recusá-las ([DEC-13](../decisoes/DEC-13.md)). "Criar usuário?" → continua fora da tela ([DEC-27](../decisoes/DEC-27.md)). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Só existe depois de [US-02](US-02-entrar-no-sistema.md): é preciso estar identificado como Gestor. |
| **N** · Negociável | ✓ | O limite de tentativas vem de configuração, e quais campos a lista mostra pode ser combinado. |
| **V** · Valiosa | ✓ | Sem ela, dar ou tirar um acesso dependeria da Equipe de TI. |
| **E** · Estimável | ✓ | Comportamento conhecido e já medido no custo retrospectivo. |
| **S** · Small | ✓ | Uma capacidade (gerir a conta de outra pessoa), com as recusas dela; criar usuário e redefinir senha de terceiros ficam de fora. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado, no frontend e no backend. |

**Diagnóstico:** média, valiosa e testável; só depende de US-02.

## Critérios de aceite

#### <a id="us-22-ca-01"></a>US-22 · CA-01 · Ver, buscar e filtrar usuários (sucesso)

- **Dado** um Gestor identificado e usuários cadastrados
- **Quando** ele abre a lista, busca por nome, e-mail ou matrícula, filtra por perfil ou por situação e passa de página
- **Então** o sistema mostra os usuários em páginas, em ordem de nome, com nome, e-mail, matrícula, perfil, situação da conta e data do último acesso, informa quantos encontrou e, depois da última página, mostra a lista vazia; nunca aparece senha nem credencial de ninguém
- **Origem:** [UC-23 passos 1 a 3](../casos-de-uso/fichas-resumidas.md#uc23-p1), [A3.1](../casos-de-uso/fichas-resumidas.md#uc23-a3-1)
- **RF:** [RF-42](../requisitos/rf-contas.md#rf-42)
- **TA:** [TA-201](#ta-201)

#### <a id="us-22-ca-02"></a>US-22 · CA-02 · Promover e rebaixar (sucesso)

- **Dado** um Gestor identificado que escolhe promover um Solicitante ou rebaixar outro Gestor
- **Quando** ele confirma a alteração
- **Então** o sistema informa que o usuário foi atualizado e mostra o novo perfil; com a mesma credencial de acesso, a pessoa promovida passa a ter os poderes de Gestor e a rebaixada os perde, na próxima ação dela; antes da confirmação nada é alterado
- **Origem:** [UC-23 passos 4 a 6](../casos-de-uso/fichas-resumidas.md#uc23-p4), [A5.1](../casos-de-uso/fichas-resumidas.md#uc23-a5-1)
- **RF:** [RF-43](../requisitos/rf-contas.md#rf-43)
- **TA:** [TA-202](#ta-202)

#### <a id="us-22-ca-03"></a>US-22 · CA-03 · Desativar e reativar (sucesso)

- **Dado** um Gestor identificado que escolhe desativar ou reativar a conta de outra pessoa
- **Quando** ele confirma a alteração
- **Então** a conta desativada deixa de entrar (com a mesma resposta de credenciais incorretas, sem revelar o estado da conta), a credencial de acesso dela deixa de valer e a de renovação não renova; as reservas da pessoa continuam como estão, com as mesmas ações disponíveis ao Gestor; ao reativar, a pessoa volta a entrar, sem que nada seja restaurado
- **Origem:** [UC-23 passos 4 a 6](../casos-de-uso/fichas-resumidas.md#uc23-p4)
- **RF:** [RF-43](../requisitos/rf-contas.md#rf-43)
- **TA:** [TA-203](#ta-203)

#### <a id="us-22-ca-04"></a>US-22 · CA-04 · Pedir o estado em que a pessoa já está (alternativa)

- **Dado** um Gestor identificado e uma pessoa que já tem o perfil e a situação pedidos
- **Quando** ele envia o pedido
- **Então** o sistema informa que nada mudou e responde como se a alteração tivesse acontecido, sem gravar nada
- **Origem:** [UC-23 A6.1](../casos-de-uso/fichas-resumidas.md#uc23-a6-1)
- **RF:** [RF-43](../requisitos/rf-contas.md#rf-43)
- **TA:** [TA-204](#ta-204)

#### <a id="us-22-ca-05"></a>US-22 · CA-05 · Pedido inválido (exceção)

- **Dado** um Gestor identificado que pede um perfil que não existe ou nenhuma mudança
- **Quando** ele envia o pedido
- **Então** o sistema recusa o pedido, informa o campo e o motivo e não altera o usuário
- **Origem:** [UC-23 E6.2](../casos-de-uso/fichas-resumidas.md#uc23-e6-2), [E6.3](../casos-de-uso/fichas-resumidas.md#uc23-e6-3)
- **RF:** [RF-43](../requisitos/rf-contas.md#rf-43)
- **TA:** [TA-205](#ta-205)

#### <a id="us-22-ca-06"></a>US-22 · CA-06 · O Gestor não rebaixa nem desativa a si mesmo (exceção)

- **Dado** um Gestor identificado
- **Quando** ele tenta rebaixar o próprio perfil ou desativar a própria conta
- **Então** o sistema informa que ele não pode fazer isso na própria conta e que outro Gestor deve fazê-lo, sem alterar nada e sem encerrar a sessão; a lista mostra essas duas ações desabilitadas na linha dele, com a explicação em texto
- **Origem:** [UC-23 E6.5](../casos-de-uso/fichas-resumidas.md#uc23-e6-5), [E6.6](../casos-de-uso/fichas-resumidas.md#uc23-e6-6)
- **RF:** [RF-43.1](../requisitos/rf-contas.md#rf-43-1)
- **TA:** [TA-206](#ta-206)

#### <a id="us-22-ca-07"></a>US-22 · CA-07 · Nunca sem Gestor ativo (exceção)

- **Dado** que só resta um Gestor ativo, ou dois Gestores que pedem ao mesmo tempo para tirar um ao outro do cargo
- **Quando** alguém pede para rebaixar ou desativar o último Gestor ativo
- **Então** o sistema recusa o pedido e informa que é preciso antes promover ou reativar outro Gestor; nos pedidos simultâneos, só o primeiro vale, e sempre sobra pelo menos um Gestor ativo
- **Origem:** [UC-23 E6.7](../casos-de-uso/fichas-resumidas.md#uc23-e6-7)
- **RF:** [RF-43.2](../requisitos/rf-contas.md#rf-43-2)
- **TA:** [TA-207](#ta-207)

#### <a id="us-22-ca-08"></a>US-22 · CA-08 · Só o Gestor, só identificado, só usuário existente, com limite (acesso)

- **Dado** uma pessoa sem identificação, um Solicitante, um Gestor que indica um usuário que não existe ou um Gestor que já fez 30 alterações no último minuto
- **Quando** a pessoa pede a lista ou uma alteração
- **Então** quem não está identificado é levado a entrar; o Solicitante é informado de que não tem permissão e nada é mostrado nem alterado; o usuário inexistente é informado como não encontrado; e o excesso de alterações é recusado com o tempo de espera; em todos os casos, a sessão continua como estava
- **Origem:** [UC-23 E1.1](../casos-de-uso/fichas-resumidas.md#uc23-e1-1), [E6.1](../casos-de-uso/fichas-resumidas.md#uc23-e6-1), [E6.4](../casos-de-uso/fichas-resumidas.md#uc23-e6-4)
- **RF:** [RF-42](../requisitos/rf-contas.md#rf-42)
- **TA:** [TA-208](#ta-208)


## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-201"></a>TA-201 | [CA-01](#us-22-ca-01) | automatizado | `contas/tests/test_api_gestao_de_usuarios.py::test_gestor_lista_os_usuarios_no_formato_padrao`; `contas/tests/test_api_gestao_de_usuarios.py::test_listagem_pagina_e_depois_da_ultima_devolve_vazio_com_200`; `contas/tests/test_api_gestao_de_usuarios.py::test_busca_por_nome_email_e_matricula`; `contas/tests/test_api_gestao_de_usuarios.py::test_filtros_por_perfil_e_por_ativo`; `contas/tests/test_api_gestao_de_usuarios.py::test_ordem_e_estavel_por_nome_e_depois_por_id`; `contas/tests/test_api_gestao_de_usuarios.py::test_resposta_nunca_traz_hash_de_senha_nem_token`; `contas/tests/test_api_gestao_de_usuarios.py::test_parametros_invalidos_respondem_400_com_o_campo [x]`; `contas/tests/test_repositorio_gestao_de_usuarios.py::test_listar_pagina_com_total_certo [x]`; `pages/PaginaUsuarios.test.tsx`: `mostra a tabela com a contagem da API como legenda e o perfil e a situação em texto`; `pages/PaginaUsuarios.test.tsx`: `a busca só vai para a API depois de a pessoa parar de digitar`; `pages/PaginaUsuarios.test.tsx`: `filtrar por perfil e por situação chama a API e guarda o filtro na URL`; `pages/PaginaUsuarios.test.tsx`: `a paginação aparece com mais de uma página e "Próxima" pede a página seguinte`; `pages/PaginaUsuarios.test.tsx`: `lista vazia sem filtros mostra "Nenhum usuário cadastrado"` |
| <a id="ta-202"></a>TA-202 | [CA-02](#us-22-ca-02) | automatizado | `contas/tests/test_api_gestao_de_usuarios.py::test_gestor_promove_um_solicitante`; `contas/tests/test_api_gestao_de_usuarios.py::test_gestor_rebaixa_outro_gestor_havendo_dois_ativos`; `contas/tests/test_api_gestao_de_usuarios.py::test_gestor_rebaixado_perde_os_poderes_na_proxima_requisicao_com_o_mesmo_token`; `contas/tests/test_api_gestao_de_usuarios.py::test_promovido_ganha_os_poderes_na_proxima_requisicao_com_o_mesmo_token`; `contas/tests/test_alterar_usuario.py::test_promover_solicitante_grava_e_devolve_o_usuario_alterado`; `pages/PaginaUsuarios.test.tsx`: `pede confirmação e não chama a API antes dela; "Voltar" fecha sem alterar`; `pages/PaginaUsuarios.test.tsx`: `promover: confirma, chama a API com o perfil, mostra a mensagem e recarrega a lista`; `pages/PaginaUsuarios.test.tsx`: `rebaixar outro Gestor chama a API com o perfil Solicitante` |
| <a id="ta-203"></a>TA-203 | [CA-03](#us-22-ca-03) | automatizado | `contas/tests/test_api_gestao_de_usuarios.py::test_gestor_desativa_e_reativa_um_solicitante`; `contas/tests/test_api_gestao_de_usuarios.py::test_desativado_nao_entra_e_recebe_a_mesma_resposta_de_credenciais_invalidas`; `contas/tests/test_api_gestao_de_usuarios.py::test_access_de_quem_foi_desativado_deixa_de_funcionar`; `contas/tests/test_api_gestao_de_usuarios.py::test_refresh_de_quem_foi_desativado_nao_renova_e_nao_rotaciona`; `contas/tests/test_api_gestao_de_usuarios.py::test_reativado_volta_a_entrar_sem_restaurar_nada`; `pages/PaginaUsuarios.test.tsx`: `desativar chama a API com ativo falso e reativar, com ativo verdadeiro`; `contas/tests/test_api_gestao_de_usuarios.py::test_desativar_nao_mexe_nas_reservas_da_pessoa` |
| <a id="ta-204"></a>TA-204 | [CA-04](#us-22-ca-04) | automatizado | `contas/tests/test_api_gestao_de_usuarios.py::test_pedir_o_estado_atual_responde_200_sem_mudar_nada`; `contas/tests/test_alterar_usuario.py::test_pedir_o_estado_atual_e_idempotente_e_nao_grava` |
| <a id="ta-205"></a>TA-205 | [CA-05](#us-22-ca-05) | automatizado | `contas/tests/test_api_gestao_de_usuarios.py::test_corpo_vazio_responde_400`; `contas/tests/test_api_gestao_de_usuarios.py::test_perfil_invalido_responde_400_no_campo`; `contas/tests/test_api_gestao_de_usuarios.py::test_ativo_que_nao_e_booleano_responde_400`; `contas/tests/test_alterar_usuario.py::test_sem_perfil_nem_ativo_lanca_nenhuma_alteracao_informada_sem_consultar`; `contas/tests/test_gestao_de_usuarios_dominio.py::test_converter_perfil_recusa_valor_fora_do_enum [x]` |
| <a id="ta-206"></a>TA-206 | [CA-06](#us-22-ca-06) | automatizado | `contas/tests/test_api_gestao_de_usuarios.py::test_gestor_nao_rebaixa_a_si_mesmo`; `contas/tests/test_api_gestao_de_usuarios.py::test_gestor_nao_desativa_a_si_mesmo`; `contas/tests/test_api_gestao_de_usuarios.py::test_unico_gestor_nao_se_rebaixa_nem_se_desativa`; `contas/tests/test_api_gestao_de_usuarios.py::test_pedir_o_proprio_estado_nao_e_recusado`; `contas/tests/test_gestao_de_usuarios_dominio.py::test_o_proprio_ator_nao_se_rebaixa`; `contas/tests/test_gestao_de_usuarios_dominio.py::test_o_proprio_ator_nao_se_desativa`; `pages/PaginaUsuarios.test.tsx`: `as ações do próprio usuário ficam desabilitadas, com a explicação em texto`; `api/cliente.test.ts`: `erro de regra %i %s numa requisição autenticada não renova o token nem encerra a sessão` |
| <a id="ta-207"></a>TA-207 | [CA-07](#us-22-ca-07) | automatizado | `contas/tests/test_gestao_de_usuarios_dominio.py::test_rebaixar_o_ultimo_gestor_ativo_e_recusado_mesmo_sendo_outra_pessoa`; `contas/tests/test_gestao_de_usuarios_dominio.py::test_desativar_o_ultimo_gestor_ativo_e_recusado`; `contas/tests/test_alterar_usuario.py::test_rebaixar_o_ultimo_gestor_ativo_e_recusado_e_nada_muda`; `contas/tests/test_api_gestao_de_usuarios.py::test_ultimo_gestor_ativo_nao_e_rebaixado_nem_desativado_por_quem_ja_perdeu_o_perfil [x]`; `contas/tests/test_repositorio_gestao_de_usuarios.py::test_alterar_trava_o_alvo_e_os_gestores_ativos_em_ordem_de_id`; `contas/tests/test_concorrencia_de_gestao.py::test_dois_gestores_se_tirando_do_cargo_ao_mesmo_tempo_deixam_um_ativo [x]`; `contas/tests/test_concorrencia_de_gestao.py::test_sem_a_trava_os_dois_pedidos_passariam_e_nao_sobraria_gestor` |
| <a id="ta-208"></a>TA-208 | [CA-08](#us-22-ca-08) | automatizado | `contas/tests/test_api_gestao_de_usuarios.py::test_solicitante_nao_lista_usuarios`; `contas/tests/test_api_gestao_de_usuarios.py::test_anonimo_nao_lista_usuarios`; `contas/tests/test_api_gestao_de_usuarios.py::test_solicitante_nao_altera_usuarios`; `contas/tests/test_api_gestao_de_usuarios.py::test_solicitante_nao_se_promove`; `contas/tests/test_api_gestao_de_usuarios.py::test_anonimo_nao_altera_usuarios`; `contas/tests/test_api_gestao_de_usuarios.py::test_usuario_inexistente_responde_404`; `contas/tests/test_api_gestao_de_usuarios.py::test_alteracoes_tem_limite_de_tentativas_por_usuario`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]`; `components/sessao/RotaDeGestor.test.tsx`: `quem não é gestor é levado para as reservas, sem ver a tela`; `navegacao.test.ts`: `o item Usuários aparece só para o gestor` |
