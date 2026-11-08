# Requisitos não funcionais (FURPS) e restrições

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **Parte da [SRS-01](srs.md) • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/requisitos/rnf.md` |

RNF descrevem **como** o sistema se comporta, e não o que ele faz (A2·s9). Cada um é classificado por FURPS (Funcionalidade, Usabilidade, Confiabilidade, Desempenho, Suportabilidade) e tem métrica e valor-alvo mensuráveis (A2·s11). O "+" de FURPS+ (o que limita a solução sem ser qualidade) está em [Restrições](#6-restrições).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Criação: RNF-F01 a RNF-S06 e restrições (REQ-02). Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | RNF-F12 · Limite de tentativas de entrada e de cadastro, que fecha a lacuna L-03 (AUT-08). Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | RNF-F12: o contador fica no Redis, sem persistência, e o Redis fora do ar recusa a tentativa com 503 (AUT-08). Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | RNF-F12: o limite vale também para tentativas simultâneas (contagem atômica no Redis), com o teste de concorrência na verificação (AUT-08, achado da revisão do PR). Sem aprovação. |

## Como ler

- **ID:** `RNF-<letra FURPS><número>`, estável e nunca reutilizado.
- **O cliente não pediria (A3):** ✔ marca o RNF que a instituição dificilmente diria sozinha, mas que a frustraria se faltasse (A3·s27 pede para identificá-los).
- **Como verificar:** o teste ou comando que já existe (caminhos a partir de `src/backend/`, salvo os do frontend, em `src/frontend/src/`), ou "a verificar" com o método proposto.
- **Estado:** Rascunho (verificado pelos testes citados), Rascunho — a verificar (sem verificação automática ainda) ou Não atendido (medido e fora do alvo; vira lacuna).
- Os termos têm definição única no [glossário](../glossario.md).

## 1. Funcionalidade (F)

Segurança e acesso. Base: [DEC-04](../decisoes/DEC-04.md) e a [matriz de acesso](../../matriz_de_acesso.md).

### <a id="rnf-f01"></a>RNF-F01 · Senha guardada só como hash

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Nenhuma senha é guardada nem devolvida em texto: o banco guarda só o resultado de uma função de hash com sal, e nenhuma resposta traz a senha ou o hash. |
| **Métrica e valor-alvo** | 0 senhas em texto no banco; 0 respostas com o campo senha ou o hash. |
| **Como verificar** | `contas/tests/test_api_cadastro.py::test_senha_e_gravada_com_hash`, `::test_cadastro_valido_responde_201_com_solicitante_sem_senha`; `contas/tests/test_usuario_manager.py::test_senha_nao_e_gravada_em_texto_puro`; `contas/tests/test_api_autenticacao.py::test_login_valido_devolve_tokens_e_usuario_sem_senha` |
| **Origem** | NS-11, NS-15; [DEC-04](../decisoes/DEC-04.md) |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-f02"></a>RNF-F02 · Política de senha

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Uma senha nova tem pelo menos 8 caracteres e não pode ser só de números, estar numa lista de senhas comuns nem ser parecida com o e-mail, o nome ou a matrícula da pessoa. |
| **Métrica e valor-alvo** | 100% das senhas com 7 caracteres ou menos, numéricas, comuns ou parecidas com os dados recusadas no cadastro ([RF-32.2](rf-contas.md#rf-32-2)). |
| **Como verificar** | `contas/tests/test_politica_de_senha.py::test_senha_com_sete_caracteres_e_recusada`, `::test_senha_comum_e_numerica_e_recusada_com_mensagens_em_portugues`, `::test_senha_parecida_com_os_dados_do_usuario_e_recusada [x]`, `::test_senha_forte_e_aceita` |
| **Origem** | NS-15, NS-11; [DEC-04](../decisoes/DEC-04.md) |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-f03"></a>RNF-F03 · Validade da sessão

| Campo | Conteúdo |
|---|---|
| **Enunciado** | A credencial de acesso de uma sessão vale 30 minutos e pode ser renovada sem senha por até 1 dia depois da entrada; depois disso, a pessoa precisa entrar de novo. Os dois prazos são configuráveis sem mudar o código. |
| **Métrica e valor-alvo** | Acesso: 30 min. Renovação: 1 dia (`JWT_ACCESS_MINUTES` = 30, `JWT_REFRESH_DAYS` = 1 no `.env.example`). |
| **Como verificar** | `contas/tests/test_api_autenticacao.py::test_access_dura_o_tempo_configurado`, `::test_refresh_dura_o_tempo_configurado`, `::test_me_com_access_expirado_responde_401` |
| **Origem** | NS-11; [DEC-04](../decisoes/DEC-04.md) |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-f04"></a>RNF-F04 · Identificação obrigatória por padrão

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Toda operação exige um [usuário autenticado](../glossario.md#usuario-autenticado), exceto as sete operações públicas: verificar se o sistema está no ar, entrar, renovar a sessão, cadastrar-se e consultar os tipos de espaço, as situações de reserva e as regras de agenda. Toda operação tem a regra de acesso declarada e testada por perfil. |
| **Métrica e valor-alvo** | 7 operações públicas, nenhuma outra; 100% das rotas e métodos da API com linha na matriz de acesso (a guarda de cobertura falha se faltar uma). |
| **Como verificar** | `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]`, `::test_toda_rota_da_api_tem_regra_de_acesso_na_matriz`, `::test_todo_metodo_implementado_tem_regra_de_acesso_na_matriz`; `reservas/tests/test_api_permissoes.py::test_vocabularios_e_health_nao_exigem_login [x]`. Comando: `docker compose exec backend pytest config/tests -v` |
| **Origem** | NS-11, NS-14; [DEC-04](../decisoes/DEC-04.md) |
| **O cliente não pediria** | — (o cliente pede "só quem tem autoridade"; a matriz é a forma de medir) |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-f05"></a>RNF-F05 · Credenciais inválidas não revelam contas

| Campo | Conteúdo |
|---|---|
| **Enunciado** | A resposta a uma tentativa de entrada com e-mail inexistente, senha errada ou conta desativada é idêntica nos três casos. |
| **Métrica e valor-alvo** | Mesmo status (401), mesmo código (`CREDENCIAIS_INVALIDAS`) e mesma mensagem nos 3 casos. |
| **Como verificar** | `contas/tests/test_api_autenticacao.py::test_senha_errada_email_inexistente_e_inativo_respondem_igual` |
| **Origem** | NS-14, NS-11 |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-f06"></a>RNF-F06 · Privacidade das reservas de outras pessoas

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Um Solicitante nunca recebe o nome, a matrícula, a finalidade nem o motivo de uma reserva de outra pessoa. Fora da agenda do dia e da mensagem de conflito, que mostram só o período e a situação, essa reserva é tratada como inexistente. |
| **Métrica e valor-alvo** | 0 campos pessoais de outra pessoa nas respostas da agenda do dia e do conflito; 100% das consultas, históricos e mudanças de situação sobre reserva alheia respondidas como "não encontrada" (404). |
| **Como verificar** | `reservas/tests/test_api_ocupacao_do_dia.py::test_solicitante_ve_a_reserva_de_outra_pessoa_sem_nenhum_dado_pessoal` (procura os dados no JSON inteiro); `reservas/tests/test_propriedades_do_horario.py::test_mensagem_do_conflito_nao_depende_de_quem_reservou`; `reservas/tests/test_api_permissoes.py::test_detalhe_de_outra_pessoa_para_o_solicitante_responde_404`, `::test_solicitante_so_lista_as_proprias [x]`; `reservas/tests/test_api_historico.py::test_solicitante_pedindo_historico_de_outra_pessoa_recebe_404` |
| **Origem** | NS-14; [DEC-11](../decisoes/DEC-11.md) |
| **O cliente não pediria** | — (é a NS-14) |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-f07"></a>RNF-F07 · Conta desativada perde o acesso na hora

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Quando a Equipe de TI desativa ou exclui um usuário, a sessão dele deixa de valer na próxima operação, sem esperar o fim do prazo da credencial. |
| **Métrica e valor-alvo** | 100% das operações e renovações de usuário desativado ou excluído recusadas com 401. |
| **Como verificar** | `contas/tests/test_api_autenticacao.py::test_access_de_usuario_desativado_depois_do_login_responde_401`, `::test_access_de_usuario_excluido_responde_401`, `::test_refresh_de_usuario_inativo_responde_401`, `::test_refresh_de_usuario_excluido_responde_401` |
| **Origem** | NS-11 |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-f08"></a>RNF-F08 · Perfil relido a cada operação

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Uma mudança de perfil feita pela Equipe de TI vale na próxima operação da pessoa, com a mesma sessão. |
| **Métrica e valor-alvo** | Gestor rebaixado perde as permissões e Solicitante promovido as ganha na operação seguinte (0 operações com o perfil antigo). |
| **Como verificar** | `config/tests/test_perfil_lido_do_banco.py::test_gestor_rebaixado_perde_as_permissoes_com_o_mesmo_token`, `::test_solicitante_promovido_ganha_as_permissoes_com_o_mesmo_token`, `::test_gestor_rebaixado_deixa_de_ver_reserva_de_outra_pessoa` |
| **Origem** | NS-11 |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-f09"></a>RNF-F09 · Identidade e perfil nunca vêm do pedido

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O solicitante de uma reserva é sempre o usuário autenticado, e o perfil de uma conta nova é sempre Solicitante: valores de solicitante, perfil ou privilégio enviados junto com o pedido são ignorados. |
| **Métrica e valor-alvo** | 0 reservas com solicitante diferente de quem pediu; 0 contas criadas pelo cadastro com perfil Gestor ou privilégio de administração. |
| **Como verificar** | `reservas/tests/test_api_reservas.py::test_solicitante_enviado_no_corpo_e_ignorado`; `contas/tests/test_api_cadastro.py::test_campos_de_privilegio_no_corpo_sao_ignorados`; `reservas/tests/test_api_situacao_reserva.py::test_campos_extras_no_corpo_nao_alteram_a_reserva` |
| **Origem** | NS-11; [DEC-04](../decisoes/DEC-04.md) |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-f10"></a>RNF-F10 · Credenciais forjadas recusadas

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Uma credencial de sessão alterada, assinada com outra chave, sem assinatura, de outro tipo (a de renovação no lugar da de acesso) ou enviada fora do formato esperado é recusada. |
| **Métrica e valor-alvo** | 100% dos casos testados recusados com 401 `NAO_AUTENTICADO`. |
| **Como verificar** | `contas/tests/test_api_autenticacao.py::test_token_adulterado_responde_401 [x]`, `::test_cabecalho_authorization_fora_do_padrao_responde_401 [x]`, `::test_access_usado_como_refresh_responde_401`; `reservas/tests/test_api_reservas.py::test_autenticacao_basic_nao_e_mais_aceita` |
| **Origem** | NS-11 |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-f11"></a>RNF-F11 · Só a origem configurada acessa a API pelo navegador

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O navegador só autoriza chamadas à API vindas da origem configurada para as telas do sistema. |
| **Métrica e valor-alvo** | Origem configurada (`CORS_ALLOWED_ORIGINS`) recebe a autorização; qualquer outra, 0 autorizações. |
| **Como verificar** | `config/tests/test_cors.py::test_origem_configurada_recebe_access_control_allow_origin`, `::test_origem_desconhecida_nao_recebe_access_control_allow_origin` |
| **Origem** | NS-14 (sem NS direta; ver lacuna [L-10](srs.md#lacunas)) |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-f12"></a>RNF-F12 · Limite de tentativas de entrada e de cadastro

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema limita as tentativas de entrada por e-mail e por origem, e os pedidos de cadastro por origem, numa janela de tempo. A tentativa acima do limite é recusada antes de qualquer outra conferência, com o tempo de espera, e a origem é o endereço da conexão, nunca um dado que o próprio pedido informa. |
| **Métrica e valor-alvo** | Entrada: 5 tentativas por minuto por e-mail (sem diferenciar maiúsculas de minúsculas nem espaços nas pontas) e 20 por minuto por origem; cadastro: 10 por hora por origem; janela deslizante, contando acertos e erros. 100% das tentativas acima do limite recusadas, inclusive com a senha certa e com tentativas simultâneas, com o tempo de espera em segundos; 0 tentativas escapam trocando o cabeçalho de origem do pedido; a renovação da sessão não tem limite. Valores configuráveis por variável de ambiente, conferidos na subida. Contador no Redis, sem persistência: vale para todos os processos do backend e zera quando o Redis reinicia. Com o Redis fora do ar, 100% das tentativas são recusadas (503), nunca liberadas sem contagem. |
| **Como verificar** | `contas/tests/test_limites_de_tentativas.py::test_sexta_tentativa_com_o_mesmo_email_responde_429_com_a_espera`, `::test_senha_certa_tambem_e_recusada_depois_do_limite`, `::test_email_com_caixa_e_espacos_diferentes_conta_como_o_mesmo`, `::test_limite_por_ip_vale_para_varios_emails`, `::test_x_forwarded_for_diferente_nao_escapa_do_limite_por_ip`, `::test_cadastro_acima_do_limite_por_ip_responde_429`, `::test_depois_da_janela_o_login_volta_a_ser_aceito`, `::test_renovar_o_token_nao_tem_limite_de_tentativas`, `::test_redis_fora_do_ar_recusa_o_login_com_503_sem_conferir_a_senha`, `::test_redis_fora_do_ar_recusa_o_cadastro_com_503`, `::test_tentativas_simultaneas_nao_passam_do_limite [x]`; `config/tests/test_configuracao_de_limites.py::test_taxa_invalida_impede_a_subida_com_mensagem_clara [x]` |
| **Origem** | NS-11, NS-14 |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho |

## 2. Usabilidade (U)

### <a id="rnf-u01"></a>RNF-U01 · Mensagens em português que orientam a correção

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Toda mensagem de resultado está em português; toda recusa traz um código próprio, diz o que impediu a operação e, quando a causa é um campo, indica o campo e o que corrigir nele. |
| **Métrica e valor-alvo** | 100% das recusas previstas nas regras com código e mensagem em português; 100% das recusas ligadas a um campo com `campos`; 0 mensagens técnicas em inglês nas respostas. |
| **Como verificar** | `compartilhado/tests/test_tratador_de_erros.py::test_excecao_do_framework_vira_codigo_e_mensagem_em_portugues [x]`, `::test_campo_obrigatorio_ausente_indica_o_campo_que_falhou`, `::test_validation_error_por_campo_lista_as_mensagens_de_cada_campo`; testes de API que conferem `campos` (ex.: `reservas/tests/test_api_reservas.py::test_dado_invalido_responde_400_sem_salvar [x]`); `contas/tests/test_politica_de_senha.py::test_senha_comum_e_numerica_e_recusada_com_mensagens_em_portugues`. Os testes cobrem as recusas existentes, não provam "100%" de recusas futuras. |
| **Origem** | NS-13; critério CS-05 da [Visão](../visao.md#critérios-de-sucesso) |
| **O cliente não pediria** | — (é a F6 do enunciado) |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-u02"></a>RNF-U02 · Telas utilizáveis em telas estreitas

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Todas as telas podem ser usadas, sem rolagem horizontal da página inteira, numa largura de 360 px; tabelas largas rolam dentro da própria área. |
| **Métrica e valor-alvo** | 7 de 7 telas (`/`, `/entrar`, `/cadastro`, `/espacos`, `/reservas`, `/reservas/nova`, `/reservas/:reservaId`) sem rolagem horizontal da página a 360 × 640 px. |
| **Como verificar** | A verificar: abrir cada tela com a largura de 360 px (ferramentas do navegador, modo de dispositivo) e conferir `document.documentElement.scrollWidth <= 360`. Hoje há só o apoio do CSS (quebras abaixo de 30rem e tabelas em região com rolagem própria), sem teste. |
| **Origem** | NS-03, NS-07; premissa P-07 da [Visão](../visao.md#premissas) |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho — a verificar |

### <a id="rnf-u03"></a>RNF-U03 · Operação completa pelo teclado

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Todas as operações das telas podem ser feitas só com o teclado, com o foco sempre visível, e um diálogo devolve o foco a quem o abriu. |
| **Métrica e valor-alvo** | 100% das operações dos RF com tela feitas sem mouse no roteiro da demonstração; 0 elementos de ação inalcançáveis por Tab. |
| **Como verificar** | Parcial (testes): `components/dialogo/Dialogo.test.tsx` ("Esc chama aoFechar", "ao fechar, o foco volta para quem abriu"); `pages/PaginaEntrar.test.tsx` ("erros de campo aparecem embaixo do campo, que recebe o foco"); `components/formulario/Campo.test.tsx`. A verificar: roteiro manual só com Tab, Shift+Tab, Enter, espaço e Esc pelo fluxo da demonstração. |
| **Origem** | NS-13; premissa P-07 |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho — a verificar |

### <a id="rnf-u04"></a>RNF-U04 · Contraste de cores (WCAG AA)

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O texto tem contraste de pelo menos 4,5:1 com o fundo, e as bordas de controles, de pelo menos 3:1 (nível AA das WCAG 2.1). |
| **Métrica e valor-alvo** | Texto ≥ 4,5:1; bordas de controle ≥ 3:1. |
| **Como verificar** | **Medido** nas cores definidas em `index.css` (cálculo da razão de luminância relativa das WCAG): menor par de texto, sucesso sobre o fundo de sucesso, 4,79:1; texto suave sobre o fundo, 6,02:1; texto do botão sobre a cor primária, 6,70:1; erro sobre o fundo de erro, 5,91:1; aviso sobre o fundo de aviso, 6,84:1; borda forte sobre a superfície, 3,66:1. A verificar: as combinações montadas pelos módulos CSS de cada componente, com uma ferramenta de auditoria de acessibilidade do navegador em cada tela. |
| **Origem** | NS-13; premissa P-07 |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho (cores-base medidas; telas a verificar) |

### <a id="rnf-u05"></a>RNF-U05 · Situação nunca indicada só por cor

| Campo | Conteúdo |
|---|---|
| **Enunciado** | A situação de uma reserva, o estado de um espaço e o tipo de cada aviso aparecem sempre como texto, além da cor. |
| **Métrica e valor-alvo** | 100% das etiquetas e avisos com texto legível sem cor. |
| **Como verificar** | Sem teste específico: as etiquetas recebem o rótulo da situação como texto (`components/reservas/EtiquetaDeSituacao.tsx`, `components/etiqueta/`), e `components/mensagens/Aviso.test.tsx` confere o papel de cada aviso. A verificar: no roteiro do [RNF-U03](#rnf-u03), ver cada tela em tons de cinza (filtro de cor do navegador) e conferir que toda situação e todo aviso continuam identificáveis. |
| **Origem** | NS-07, NS-13 |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho — a verificar |

### <a id="rnf-u06"></a>RNF-U06 · Datas e horas no formato brasileiro

| Campo | Conteúdo |
|---|---|
| **Enunciado** | As telas mostram datas como dd/mm/aaaa e horas como HH:MM, no horário de Brasília, sem mudar o dia por causa do fuso do computador. |
| **Métrica e valor-alvo** | 100% das datas e horas exibidas nesses formatos; 0 datas deslocadas em um dia. |
| **Como verificar** | `formatacao.test.ts` (formatação por texto, sem conversão de fuso no navegador); [RNF-S05](#rnf-s05) para o lado do servidor. |
| **Origem** | NS-07; premissa P-03 |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho |

## 3. Confiabilidade (R)

### <a id="rnf-r01"></a>RNF-R01 · Nenhum espaço comprometido duas vezes

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Nunca existem duas [reservas que ocupam horário](../glossario.md#reserva-que-ocupa-horario) no mesmo espaço com algum momento em comum, inclusive quando dois pedidos para o mesmo período chegam ao mesmo tempo. |
| **Métrica e valor-alvo** | 0 pares sobrepostos no banco; a segunda gravação simultânea é recusada com o mesmo conflito da regra ([RF-11.4](rf-reservas.md#rf-11-4)). |
| **Como verificar** | `reservas/tests/test_repositorio_reservas.py::test_banco_barra_sobreposicao_que_escapou_da_checagem_em_codigo` (simula o pedido que passou pela checagem enquanto o outro gravava); `reservas/tests/test_propriedades_do_horario.py::test_so_conta_reserva_do_mesmo_espaco_que_ocupa_horario_e_se_sobrepoe`; `exemplos/tests/test_carregar_dados_exemplo.py::test_reservas_que_ocupam_horario_nao_se_sobrepoem`. Não há teste com duas threads para a criação, só para a mudança de situação (lacuna [L-07](srs.md#lacunas)). |
| **Origem** | NS-04; critério CS-01 |
| **O cliente não pediria** | — (é a NS-04; a simultaneidade é o que ele não diria) |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-r02"></a>RNF-R02 · Histórico completo e na mesma gravação

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Toda criação e toda mudança de situação aceita gera exatamente um registro no histórico, gravado junto com a reserva: ou os dois ficam gravados, ou nenhum. Registros nunca são alterados nem excluídos. |
| **Métrica e valor-alvo** | 100% das mudanças aceitas com registro; 0 registros de operações recusadas ou que falharam ao gravar; histórico coerente (cada situação anterior é a nova do registro anterior; a última é a situação atual). |
| **Como verificar** | `reservas/tests/test_repositorio_reservas.py::test_conflito_ao_salvar_nao_grava_registro_e_mantem_os_pendentes`, `::test_conflito_barrado_pelo_banco_nao_grava_registro`, `::test_salvar_de_novo_sem_mudanca_nao_duplica_registros`; `reservas/tests/test_propriedades_da_reserva.py::TestMaquinaDaReserva`; `reservas/tests/test_api_historico.py::test_historico_nao_aceita_alteracao_nem_exclusao [x]`; `exemplos/tests/test_carregar_dados_exemplo.py::test_todas_as_reservas_de_exemplo_tem_historico_coerente` |
| **Origem** | NS-12; critério CS-02; [DEC-05](../decisoes/DEC-05.md) |
| **O cliente não pediria** | ✔ (ele pede o histórico; a atomicidade, não) |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-r03"></a>RNF-R03 · Operação recusada não muda nada

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Uma operação recusada deixa espaços, reservas e histórico exatamente como estavam. |
| **Métrica e valor-alvo** | 0 mudanças de estado depois de uma recusa, em sequências geradas de tentativas. |
| **Como verificar** | `reservas/tests/test_propriedades_da_reserva.py::TestMaquinaDaReserva` e `espacos/tests/test_propriedades_do_espaco.py::TestMaquinaDoEspaco` (toda recusa compara o estado antes e depois); `reservas/tests/test_api_situacao_reserva.py::test_transicao_proibida_responde_409_e_preserva_a_reserva`; `espacos/tests/test_api_espacos.py::test_cadastro_invalido_responde_erro_e_preserva_a_listagem [x]`; `reservas/tests/test_api_reservas.py::test_horario_ocupado_responde_409_e_preserva_as_reservas` |
| **Origem** | NS-13, NS-09; enunciado (F5) |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-r04"></a>RNF-R04 · Alteração sobre leitura desatualizada é recusada

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Quando duas pessoas alteram o mesmo espaço ou mudam a situação da mesma reserva ao mesmo tempo, só a primeira alteração é gravada; a outra é recusada, sem gravar nada, e a pessoa é orientada a atualizar e decidir de novo. |
| **Métrica e valor-alvo** | Em 2 alterações simultâneas, exatamente 1 gravada e 1 recusada (`ESPACO_DESATUALIZADO` ou `RESERVA_DESATUALIZADA`, 409); 0 alterações perdidas em silêncio. |
| **Como verificar** | `espacos/tests/test_concorrencia_de_espaco.py::test_edicao_e_desativacao_simultaneas_gravam_so_uma`, `::test_duas_desativacoes_simultaneas_aceitam_so_uma`; `reservas/tests/test_concorrencia_de_situacao.py::test_alteracoes_simultaneas_gravam_so_uma_e_o_historico_fica_coerente` (duas threads de verdade); `reservas/tests/test_repositorio_reservas.py::test_alteracao_sobre_leitura_desatualizada_e_recusada_sem_gravar` |
| **Origem** | NS-02, NS-09, NS-12 |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-r05"></a>RNF-R05 · Nada é excluído

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Espaços, reservas e registros do histórico não podem ser excluídos por nenhuma operação: espaços são desativados e reservas mudam de situação. |
| **Métrica e valor-alvo** | 0 operações de exclusão aceitas (405 para quem está autenticado); o banco recusa excluir uma reserva com histórico. |
| **Como verificar** | `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]` (linhas `DELETE`); `reservas/tests/test_repositorio_reservas.py::test_banco_nao_deixa_excluir_reserva_com_historico` |
| **Origem** | NS-02, NS-12; [DEC-06](../decisoes/DEC-06.md) |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-r06"></a>RNF-R06 · Nenhuma regra violada vira erro interno

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Toda regra violada responde com a categoria certa (400, 403, 404 ou 409); só uma falha não prevista vira erro interno, e ele não mostra detalhes do sistema, mas fica registrado para a Equipe de TI. |
| **Métrica e valor-alvo** | 0 regras de negócio terminando em 500; 100% dos erros internos sem detalhe técnico na resposta e com registro no log. |
| **Como verificar** | `compartilhado/tests/test_tratador_de_erros.py::test_erro_de_dominio_usa_o_status_da_categoria [x]`, `::test_excecao_inesperada_vira_500_sem_detalhes_e_fica_no_log`, `::test_erro_de_dominio_sem_categoria_e_tratado_como_erro_interno` |
| **Origem** | NS-13; critério CS-05 |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho |

## 4. Desempenho (P)

Metas da [DEC-12](../decisoes/DEC-12.md). Medição: `scripts/medir_desempenho.py` (fora do ZIP), que cria um banco de teste separado, grava as reservas, mede e apaga o banco. Resultado e ambiente em [Medição](#medição).

### <a id="rnf-p01"></a>RNF-P01 · Tempo da consulta de reservas

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Com 1.000 reservas cadastradas, a consulta de reservas responde em até 1 s no percentil 95, nos três usos: Gestor sem critério (todas as reservas na resposta), Gestor com espaço e data, e Solicitante (só as próprias). |
| **Métrica e valor-alvo** | p95 ≤ 1.000 ms em cada cenário, com 1.000 reservas, 50 repetições depois de 5 de aquecimento, medido dentro do container do backend (sem rede nem navegador). |
| **Como verificar** | `docker compose exec -T backend python - --reservas 1000 < ../scripts/medir_desempenho.py` (a partir de `src/`; o script sai com código 1 se alguma meta falhar). Resultado em 04/11/2026: p95 de 378 ms (Gestor sem critério), 10 ms (Gestor com espaço e data) e 20 ms (Solicitante). [Medição](#medição). |
| **Origem** | NS-08, NS-07; [DEC-12](../decisoes/DEC-12.md) |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho (atendido com 1.000 reservas; com 5.000, a lista sem critério passa de 1 s: lacuna [L-05](srs.md#l-05)) |

### <a id="rnf-p02"></a>RNF-P02 · Tempo da agenda do dia

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Com 1.000 reservas cadastradas, a agenda do dia de um espaço num dia com horários ocupados responde em até 500 ms no percentil 95. |
| **Métrica e valor-alvo** | p95 ≤ 500 ms, nas mesmas condições do [RNF-P01](#rnf-p01). |
| **Como verificar** | O mesmo comando do RNF-P01. Resultado em 04/11/2026: p95 de 7 ms com 1.000 reservas (9 ms com 5.000). [Medição](#medição). |
| **Origem** | NS-05; [DEC-12](../decisoes/DEC-12.md) |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho (atendido) |

### Medição

Feita em 04/11/2026 com `scripts/medir_desempenho.py`, na carga de referência da [DEC-12](../decisoes/DEC-12.md) (1.000 reservas) e, para ver a tendência, com 5.000.

**Ambiente:** Windows 10 Pro com Docker Desktop (WSL 2); container do backend Linux 6.18 x86_64 com 4 CPUs visíveis; Python 3.12.16, Django 5.2.18, PostgreSQL 16.15 em outro container. Carga: 5 espaços, 20 solicitantes, reservas de 1 h das 08:00 às 18:00 a partir de amanhã, em cinco situações misturadas (Solicitada, Confirmada ×2, Cancelada, Recusada). 5 chamadas de aquecimento e 50 medidas por cenário, pela API em processo com token de acesso (sem rede nem navegador).

**1.000 reservas (meta da DEC-12):**

| Cenário | Itens | Resposta | Consultas SQL | Mín | Mediana | p95 | Máx | Meta (p95) | Atende |
|---|---|---|---|---|---|---|---|---|---|
| Consulta: Gestor, sem critério | 1000 | 448 KiB | 2 | 185 ms | 285 ms | 378 ms | 447 ms | ≤ 1000 ms | ✔ |
| Consulta: Gestor, espaço + data | 10 | 5 KiB | 2 | 5 ms | 6 ms | 10 ms | 153 ms | ≤ 1000 ms | ✔ |
| Consulta: Solicitante, só as próprias | 50 | 20 KiB | 2 | 12 ms | 14 ms | 20 ms | 81 ms | ≤ 1000 ms | ✔ |
| Agenda do dia (espaço + data) | 6 | 1 KiB | 3 | 5 ms | 5 ms | 7 ms | 8 ms | ≤ 500 ms | ✔ |

**5.000 reservas (tendência, fora da meta):**

| Cenário | Itens | Resposta | Consultas SQL | Mín | Mediana | p95 | Máx | Meta (p95) | Atende |
|---|---|---|---|---|---|---|---|---|---|
| Consulta: Gestor, sem critério | 5000 | 2246 KiB | 2 | 1271 ms | 1487 ms | 1743 ms | 2565 ms | ≤ 1000 ms | ✘ |
| Consulta: Gestor, espaço + data | 10 | 5 KiB | 2 | 6 ms | 8 ms | 15 ms | 21 ms | ≤ 1000 ms | ✔ |
| Consulta: Solicitante, só as próprias | 250 | 99 KiB | 2 | 48 ms | 58 ms | 145 ms | 208 ms | ≤ 1000 ms | ✔ |
| Agenda do dia (espaço + data) | 6 | 1 KiB | 3 | 5 ms | 7 ms | 9 ms | 11 ms | ≤ 500 ms | ✔ |

**Leitura:** com 1.000 reservas, as duas metas são atingidas com folga (p95 de 378 ms na pior consulta e de 7 ms na agenda). O número de consultas SQL não cresce com as reservas (2 na lista, 3 na agenda): não há consulta por item. O tempo da lista do Gestor **sem critério** cresce com a quantidade de reservas, porque ela devolve todas (sem paginação): com 5.000, passa de 1 s. As consultas com critério e a agenda do dia quase não mudam. Isso confirma a lacuna [L-05](srs.md#l-05).

## 5. Suportabilidade (S)

### <a id="rnf-s01"></a>RNF-S01 · Execução num ambiente novo com um comando

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Num computador só com Docker, o sistema sobe com um único comando seguindo o README, sem passo fora dele. |
| **Métrica e valor-alvo** | 1 comando para subir (`docker compose up --build`, depois de copiar o `.env.example`); 0 intervenções de quem escreveu o roteiro. |
| **Como verificar** | A verificar: critério CS-03 da [Visão](../visao.md#critérios-de-sucesso) (um integrante que não escreveu o roteiro executa num clone novo, com data e nome registrados no checklist pré-entrega). |
| **Origem** | NS-16; critério CS-03 |
| **O cliente não pediria** | — (é a NS-16) |
| **Revisão / estado** | 0.1 • Rascunho — a verificar |

### <a id="rnf-s02"></a>RNF-S02 · Dados de exemplo em um comando, repetível

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Os dados de exemplo são carregados por um comando, que pode ser repetido sem duplicar nada e que, se falhar no meio, não deixa nada gravado. |
| **Métrica e valor-alvo** | 1 comando; 2.ª execução cria 0 registros; 0 registros depois de uma falha no meio. |
| **Como verificar** | `exemplos/tests/test_carregar_dados_exemplo.py::test_rodar_duas_vezes_nao_duplica_e_informa_que_ja_existiam`, `::test_falha_no_meio_da_carga_nao_deixa_nada_gravado` |
| **Origem** | NS-16 |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-s03"></a>RNF-S03 · Cobertura de testes

| Campo | Conteúdo |
|---|---|
| **Enunciado** | As regras de negócio de espaços e de reservas são exercitadas por inteiro pelos testes automatizados. |
| **Métrica e valor-alvo** | 100% de linhas e ramos em `domain` e `application` de `espacos` e `reservas`; ≥ 99% no total (medido na RES-08: 99,71%). |
| **Como verificar** | `docker compose exec backend sh -c "pytest --cov && coverage report --include='espacos/domain/*,espacos/application/*,reservas/domain/*,reservas/application/*' --fail-under=100"` |
| **Origem** | NS-16; [DEC-08](../decisoes/DEC-08.md) |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-s04"></a>RNF-S04 · Regra de dependência entre camadas e contextos

| Campo | Conteúdo |
|---|---|
| **Enunciado** | As regras de negócio não dependem do framework, e cada contexto (espaços, reservas, contas) só conversa com outro pela fachada pública dele. |
| **Métrica e valor-alvo** | 0 contratos quebrados no `lint-imports` (todos "KEPT"). |
| **Como verificar** | `docker compose exec backend lint-imports` |
| **Origem** | NS-16 (manutenção pela equipe) |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-s05"></a>RNF-S05 · Horário de Brasília em todo o sistema

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Todos os horários são do fuso America/Sao_Paulo: um horário gravado volta com a mesma data e as mesmas horas, inclusive perto da meia-noite e em anos com horário de verão. |
| **Métrica e valor-alvo** | 0 horários deslocados na ida e volta pelo banco, de 2000 a 2100. |
| **Como verificar** | `reservas/tests/test_intervalo_de_horario.py::test_fuso_horario_e_o_de_sao_paulo`; `reservas/tests/test_propriedades_do_horario.py::test_gravar_em_utc_e_ler_no_fuso_de_sao_paulo_devolve_o_mesmo_intervalo`; `reservas/tests/test_repositorio_reservas.py::test_reserva_no_fim_do_dia_volta_na_mesma_data` |
| **Origem** | NS-03, NS-04; premissa P-03 |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho |

### <a id="rnf-s06"></a>RNF-S06 · Configuração sem segredos no código

| Campo | Conteúdo |
|---|---|
| **Enunciado** | Senhas, chaves e endereços do ambiente ficam fora do código, em variáveis de ambiente documentadas num arquivo de exemplo, e o arquivo real nunca vai para o repositório nem para a entrega. |
| **Métrica e valor-alvo** | 0 credenciais reais no repositório e no ZIP; 100% das variáveis usadas pelo `docker-compose.yml` presentes no `.env.example`. |
| **Como verificar** | A verificar antes da entrega: `git ls-files` sem `.env`; busca por senhas e chaves no ZIP; conferir as variáveis do `docker-compose.yml` contra o `.env.example`. |
| **Origem** | NS-16 (interesse da Equipe de TI na Visão) |
| **O cliente não pediria** | ✔ |
| **Revisão / estado** | 0.1 • Rascunho — a verificar |

## 6. Restrições

O "+" de FURPS+: limitam a solução, mas não são qualidade do comportamento. Por isso não têm métrica nem entram na auditoria dos RNF.

| ID | Restrição | Origem |
|---|---|---|
| REST-01 | O backend é escrito em Python. | Enunciado de Projeto de Programação, Seção 7 |
| REST-02 | Entrega até 20/11/2026, num ZIP com exatamente `README.md`, `src/` e `docs/`. | Enunciado |
| REST-03 | Telas em React. | [DEC-01](../decisoes/DEC-01.md) |
| REST-04 | Execução com Docker e PostgreSQL, com `docker-compose.yml` e `.env.example` dentro de `src/`. | [DEC-02](../decisoes/DEC-02.md), [DEC-03](../decisoes/DEC-03.md) |
| REST-05 | Execução local, por quem corrige, seguindo o README; sem publicação na internet. | Enunciado; [Visão](../visao.md#fora-do-escopo) |
| REST-06 | `modelagem.pdf` com até 6 páginas e `contribuicoes.pdf` com até 2. | Enunciado |
| REST-07 | Demonstração ao vivo em até 10 minutos, com todos os integrantes. | Enunciado |
| REST-08 | Extras não podem atrasar as seis funcionalidades mínimas. | Enunciado; [DEC-04](../decisoes/DEC-04.md) |
