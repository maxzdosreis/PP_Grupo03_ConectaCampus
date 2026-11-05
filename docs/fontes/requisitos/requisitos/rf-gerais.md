# Requisitos funcionais — Mensagens e operação

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **Parte da [SRS-01](srs.md) • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/requisitos/rf-gerais.md` |

Fichas dos RF que valem para o sistema inteiro: a [mensagem de resultado](../glossario.md#mensagem-de-resultado) de toda operação (NS-13, F6) e o que a [Equipe de TI](../glossario.md#equipe-de-ti) precisa para instalar e demonstrar o sistema (NS-16). Como ler as fichas: [SRS, seção 3](srs.md#3-requisitos-funcionais).

Caminhos de teste a partir de `src/backend/`, salvo os do frontend (`src/frontend/src/`); `[x]` = teste parametrizado.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Criação: RF-38 a RF-40 (REQ-02). Sem aprovação. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Vínculos: o UC de cada ficha preenchido, com link para o [índice de casos de uso](../casos-de-uso/README.md#índice-dos-casos-de-uso) (REQ-03). Sem aprovação. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Vínculos: o passo, a alternativa ou a exceção exata de cada RF nas [fichas de caso de uso](../casos-de-uso/README.md#fichas-dos-casos-de-uso); US e CA ficam para a REQ-05 (REQ-04). Sem aprovação. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Vínculos: as US e os CAs de cada RF, com o TA, no lugar de "a definir" ([histórias](../historias/README.md)) (REQ-05). Sem aprovação. |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Campo **Código (complementar)** em cada ficha (caso de uso da aplicação e regra do domínio, como `arquivo::Símbolo`), lido pela [matriz de rastreabilidade](../rastreabilidade/matriz.md) (REQ-06). Sem aprovação. |

## Mensagens

### <a id="rf-38"></a>RF-38 · Ver o resultado de cada operação

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao usuário que executou uma operação ver, ao final dela, uma mensagem em português com o resultado: o que foi feito, quando a operação é aceita; o motivo, quando é recusada; e, quando a recusa vem de um campo, a mensagem ao lado desse campo. |
| **Origem** | NS-13 |
| **Funcionalidade** | F6 |
| **Prioridade (QFD)** | Normal — "exibir mensagens claras de sucesso e erro" é a sexta funcionalidade do enunciado. |
| **Vínculos** | UC: transversal, qualidade de todos os casos de uso, sem caso de uso próprio ([decisão a](../casos-de-uso/README.md#decisao-a)) · US e CA: transversal, sem história própria; aparece no Então de todos os CAs ([decisão a](../historias/README.md#decisao-a)) |
| **Evidência (complementar)** | Formato `{"mensagem", "dados"}` e `{"erro": {"codigo", "mensagem", "campos"}}`; notificação no canto da tela, aviso no topo do formulário e erro embaixo do campo. `compartilhado/tests/test_respostas.py::test_resposta_sucesso_devolve_mensagem_dados_e_status_pedidos`, `::test_corpo_de_erro_com_campos_inclui_os_campos`; `compartilhado/tests/test_tratador_de_erros.py::test_campo_obrigatorio_ausente_indica_o_campo_que_falhou`, `::test_excecao_do_framework_vira_codigo_e_mensagem_em_portugues [x]`; `reservas/tests/test_api_situacao_reserva.py::test_mensagem_de_sucesso_usa_o_rotulo_da_nova_situacao [x]`; `components/mensagens/MensagensProvider.test.tsx`; `components/formulario/Campo.test.tsx` ("com erro, descreve o controle pela dica e pelo erro e o marca como inválido"); `hooks/useEnvio.test.ts` |
| **Código (complementar)** | `compartilhado/api/tratador_de_erros.py::tratar_excecao`, `compartilhado/api/respostas.py::resposta_sucesso`, `compartilhado/domain/erros.py::ErroDeDominio` |
| **Regras de negócio** | [Mensagem de resultado](../glossario.md#mensagem-de-resultado). A forma e a língua das mensagens são o [RNF-U01](rnf.md#rnf-u01). |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

## Operação

### <a id="rf-39"></a>RF-39 · Carregar dados de exemplo

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir à Equipe de TI carregar, com um único comando, um Gestor, dois Solicitantes, um espaço de cada tipo mais um inativo e uma reserva de cada situação, e ver o resumo do que foi criado e do que já existia. |
| **Origem** | NS-16 |
| **Funcionalidade** | Extra (INF-06) |
| **Prioridade (QFD)** | Esperado — o professor avalia executando o sistema; sem dados, a demonstração começaria do zero. |
| **Vínculos** | UC: [UC-21 Carregar dados de exemplo](../casos-de-uso/README.md#uc-21) (fluxo principal) — na ficha: [UC-21 passos 1 a 4](../casos-de-uso/fichas-resumidas.md#uc21-p1) · US/CA: [US-18 · CA-01](../historias/US-18-carregar-os-dados-de-exemplo.md#us-18-ca-01) (TA-150), [US-18 · CA-02](../historias/US-18-carregar-os-dados-de-exemplo.md#us-18-ca-02) (TA-151), [US-18 · CA-03](../historias/US-18-carregar-os-dados-de-exemplo.md#us-18-ca-03) (TA-152), [US-18 · CA-04](../historias/US-18-carregar-os-dados-de-exemplo.md#us-18-ca-04) (TA-153), [US-18 · CA-05](../historias/US-18-carregar-os-dados-de-exemplo.md#us-18-ca-05) (TA-154) |
| **Evidência (complementar)** | `python manage.py carregar_dados_exemplo`. `exemplos/tests/test_carregar_dados_exemplo.py::test_cria_um_gestor_e_dois_solicitantes`, `::test_cria_um_espaco_de_cada_tipo_e_um_inativo`, `::test_cria_uma_reserva_de_cada_situacao`, `::test_primeira_execucao_informa_o_que_foi_criado`, `::test_rodar_duas_vezes_nao_duplica_e_informa_que_ja_existiam`, `::test_com_debug_desligado_recusa_sem_criar_nada` |
| **Código (complementar)** | `exemplos/management/commands/carregar_dados_exemplo.py::Command`, `exemplos/carga.py::garantir_reservas` |
| **Regras de negócio** | [Dados de exemplo](../glossario.md#dados-de-exemplo); os dados passam pelas mesmas regras de todas as fichas acima. |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |

### <a id="rf-40"></a>RF-40 · Verificar se o sistema está no ar

| Campo | Conteúdo |
|---|---|
| **Enunciado** | O sistema deve permitir ao visitante verificar se o sistema está em funcionamento e ver "API no ar." quando o banco de dados responde, ou "Não foi possível conectar ao banco de dados." quando não responde. |
| **Origem** | NS-16 |
| **Funcionalidade** | Extra |
| **Prioridade (QFD)** | Esperado — quem instala precisa saber se terminou antes de abrir as telas. |
| **Vínculos** | UC: [UC-22 Verificar se o sistema está no ar](../casos-de-uso/README.md#uc-22) (fluxo principal) — na ficha: [UC-22 passos 1 a 3](../casos-de-uso/fichas-resumidas.md#uc22-p1) · US/CA: [US-19 · CA-01](../historias/US-19-verificar-se-o-sistema-esta-no-ar.md#us-19-ca-01) (TA-155), [US-19 · CA-02](../historias/US-19-verificar-se-o-sistema-esta-no-ar.md#us-19-ca-02) (TA-156) |
| **Evidência (complementar)** | `GET /api/health/` (sem login): 200 ou 503 `BANCO_INDISPONIVEL`; situação da API na página inicial `/`. `reservas/tests/test_api_permissoes.py::test_vocabularios_e_health_nao_exigem_login [x]`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]` (`health`). **Sem teste do 503** (lacuna [L-08](srs.md#lacunas)). |
| **Código (complementar)** | `config/views.py::health` |
| **Regras de negócio** | — |
| **Decisões** | — |
| **Revisão** | 0.1 |
| **Estado** | Rascunho |
| **Responsável** | Max Zimmermann dos Reis |
