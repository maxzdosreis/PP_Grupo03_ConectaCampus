# US-07 · Desativar e reativar espaço

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **US-07 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/historias/US-07-desativar-e-reativar-espaco.md` |

História do [índice](README.md#índice-das-histórias). Como ler: [decisões de organização](README.md#decisões-de-organização-req-05).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: Index Card, INVEST, critérios e testes de aceite (REQ-05). Sem aprovação. |

## Index Card

| Campo | Conteúdo |
|---|---|
| **ID** | US-07 |
| **Título** | Desativar e reativar espaço |
| **História** | Como Gestor, quero desativar um espaço que não pode mais ser usado, e reativá-lo depois, para que ninguém peça um espaço interditado sem eu perder o histórico dele. |
| **Valor** | Uma interdição (obra, manutenção) bloqueia novos pedidos na hora, sem apagar o espaço nem as reservas dele ([NS-02](../visao.md#necessidades)). |
| **Origem** | [UC-16 Desativar ou reativar espaço, passos 1 a 5](../casos-de-uso/fichas-resumidas.md#uc16-p1), alternativas [A1.1](../casos-de-uso/fichas-resumidas.md#uc16-a1-1), [A3.1](../casos-de-uso/fichas-resumidas.md#uc16-a3-1) e [A5.1](../casos-de-uso/fichas-resumidas.md#uc16-a5-1) e exceções [E1.1](../casos-de-uso/fichas-resumidas.md#uc16-e1-1) a [E4.4](../casos-de-uso/fichas-resumidas.md#uc16-e4-4). |
| **Prioridade** | Normal — por [RF-09](../requisitos/rf-espacos.md#rf-09) (espaço inexistente); os RF próprios ([RF-07](../requisitos/rf-espacos.md#rf-07), [RF-08](../requisitos/rf-espacos.md#rf-08) e as recusas) são esperados e extras ao enunciado. |
| **Estimativa (Custo em Semanas)** | 0,2 (retrospectiva: desativar e ativar da ESP-04, com o diálogo de confirmação). |
| **Conversa** | "O que acontece com as reservas já feitas no espaço desativado?" → continuam valendo; o Gestor cancela as que quiser ([DEC-06](../decisoes/DEC-06.md), adotada provisoriamente). "Desativar um espaço já inativo é erro?" → sim, informado (decisão c da ESP-04). |
| **Pronta quando** | Todos os CAs abaixo têm o TA passando na verificação do PR, esta ficha e os vínculos (RF, UC e SRS 6.4) estão atualizados e a revisão por pares está registrada no histórico (versão 0.2). |

## INVEST

| Letra | Atende | Justificativa |
|---|---|---|
| **I** · Independente | ✗ | Precisa de espaços ([US-05](US-05-cadastrar-espaco.md)); o efeito só é visível com pedidos ([US-08](US-08-solicitar-reserva.md)). |
| **N** · Negociável | ✗ | O destino das reservas existentes está preso à [DEC-06](../decisoes/DEC-06.md): bloquear a desativação ou cancelar junto exigiria outra organização do sistema, não só outro texto. |
| **V** · Valiosa | ✓ | Sem ela, um espaço interditado continuaria recebendo pedidos. |
| **E** · Estimável | ✓ | Duas operações simétricas. |
| **S** · Small | ✓ | Duas operações simétricas sobre um mesmo dado: cabe numa iteração. |
| **T** · Testável | ✓ | Todos os CAs têm TA automatizado, inclusive duas desativações simultâneas. |

**Diagnóstico:** valiosa, pequena e testável, mas depende de US-05 e não é negociável enquanto a DEC-06 estiver aberta.

## Critérios de aceite

#### <a id="us-07-ca-01"></a>US-07 · CA-01 · Espaço desativado (sucesso)

- **Dado** um espaço ativo com uma reserva Solicitada e um Gestor identificado
- **Quando** o Gestor pede para desativá-lo e, avisado de que novos pedidos ficarão bloqueados e as reservas existentes continuam valendo, confirma
- **Então** o sistema informa "Espaço desativado. Novas reservas ficam bloqueadas; as existentes continuam valendo.", o espaço aparece como inativo, um novo pedido nele é recusado com "Este espaço está inativo e não aceita reservas." e a reserva Solicitada continua na lista, com as mesmas ações
- **Origem:** [UC-16 passos 1 a 5](../casos-de-uso/fichas-resumidas.md#uc16-p1)
- **RF:** [RF-07](../requisitos/rf-espacos.md#rf-07)
- **TA:** [TA-49](#ta-49)
- **Depende de:** [DEC-06](../decisoes/DEC-06.md)

#### <a id="us-07-ca-02"></a>US-07 · CA-02 · Espaço reativado (alternativa)

- **Dado** um espaço inativo
- **Quando** o Gestor pede para reativá-lo e confirma
- **Então** o sistema informa "Espaço reativado.", o espaço aparece como ativo e volta a aceitar pedidos
- **Origem:** [UC-16 A1.1](../casos-de-uso/fichas-resumidas.md#uc16-a1-1)
- **RF:** [RF-08](../requisitos/rf-espacos.md#rf-08)
- **TA:** [TA-50](#ta-50)

#### <a id="us-07-ca-03"></a>US-07 · CA-03 · O Gestor desiste (alternativa)

- **Dado** o aviso de confirmação da desativação
- **Quando** o Gestor desiste em vez de confirmar
- **Então** nada muda: o espaço continua ativo e aceitando pedidos
- **Origem:** [UC-16 A3.1](../casos-de-uso/fichas-resumidas.md#uc16-a3-1)
- **RF:** [RF-07](../requisitos/rf-espacos.md#rf-07)
- **TA:** [TA-51](#ta-51)

#### <a id="us-07-ca-04"></a>US-07 · CA-04 · Decidir sobre as reservas do espaço desativado (alternativa)

- **Dado** um espaço desativado com uma reserva Solicitada
- **Quando** o Gestor consulta essa reserva
- **Então** ela continua oferecendo as mesmas ações de antes (confirmar, recusar ou cancelar, com motivo), e a decisão é aceita normalmente
- **Origem:** [UC-16 A5.1](../casos-de-uso/fichas-resumidas.md#uc16-a5-1)
- **RF:** [RF-07](../requisitos/rf-espacos.md#rf-07), [RF-20](../requisitos/rf-reservas.md#rf-20)
- **TA:** [TA-52](#ta-52)
- **Depende de:** [DEC-06](../decisoes/DEC-06.md)

#### <a id="us-07-ca-05"></a>US-07 · CA-05 · Espaço inexistente (exceção)

- **Dado** uma identificação de espaço que não existe
- **Quando** o Gestor pede para desativá-lo ou reativá-lo
- **Então** o sistema informa "Espaço de código «n» não encontrado." e nenhum espaço muda
- **Origem:** [UC-16 E4.1](../casos-de-uso/fichas-resumidas.md#uc16-e4-1)
- **RF:** [RF-09](../requisitos/rf-espacos.md#rf-09)
- **TA:** [TA-53](#ta-53)

#### <a id="us-07-ca-06"></a>US-07 · CA-06 · Desativar um espaço já inativo (exceção)

- **Dado** um espaço inativo
- **Quando** o Gestor pede para desativá-lo de novo
- **Então** o sistema informa "Este espaço já está inativo." e o espaço continua inativo
- **Origem:** [UC-16 E4.2](../casos-de-uso/fichas-resumidas.md#uc16-e4-2)
- **RF:** [RF-07.1](../requisitos/rf-espacos.md#rf-07-1)
- **TA:** [TA-54](#ta-54)

#### <a id="us-07-ca-07"></a>US-07 · CA-07 · Reativar um espaço já ativo (exceção)

- **Dado** um espaço ativo
- **Quando** o Gestor pede para reativá-lo
- **Então** o sistema informa "Este espaço já está ativo." e o espaço continua ativo
- **Origem:** [UC-16 E4.3](../casos-de-uso/fichas-resumidas.md#uc16-e4-3)
- **RF:** [RF-08.1](../requisitos/rf-espacos.md#rf-08-1)
- **TA:** [TA-55](#ta-55)

#### <a id="us-07-ca-08"></a>US-07 · CA-08 · Espaço alterado por outra pessoa (exceção)

- **Dado** dois Gestores que leram o mesmo espaço ativo
- **Quando** os dois pedem para desativá-lo quase ao mesmo tempo
- **Então** só a primeira desativação vale; o segundo recebe "Este espaço foi alterado por outra pessoa enquanto você decidia. Atualize a lista e tente de novo." e a opção de atualizar a lista
- **Origem:** [UC-16 E4.4](../casos-de-uso/fichas-resumidas.md#uc16-e4-4)
- **RF:** [RF-07](../requisitos/rf-espacos.md#rf-07) (a garantia é o [RNF-R04](../requisitos/rnf.md#rnf-r04))
- **TA:** [TA-56](#ta-56)

#### <a id="us-07-ca-09"></a>US-07 · CA-09 · Só o Gestor desativa e reativa (acesso)

- **Dado** um Solicitante identificado
- **Quando** ele tenta desativar ou reativar um espaço
- **Então** o sistema informa "Você não tem permissão para realizar esta ação." e o espaço não muda
- **Origem:** [UC-16 E1.1](../casos-de-uso/fichas-resumidas.md#uc16-e1-1)
- **RF:** [RF-10](../requisitos/rf-espacos.md#rf-10)
- **TA:** [TA-57](#ta-57)

## Testes de aceite

Testes a partir de `src/backend/` (pytest, `arquivo::teste`) ou de `src/frontend/src/` (Vitest, `arquivo`: `descrição`); `[x]` = teste parametrizado.

| TA | CA | Tipo | Testes ou roteiro |
|---|---|---|---|
| <a id="ta-49"></a>TA-49 | [CA-01](#us-07-ca-01) | automatizado | `espacos/tests/test_api_edicao_de_espaco.py::test_desativar_espaco_ativo_responde_200_e_a_listagem_mostra_inativo`; `espacos/tests/test_api_desativacao_e_reservas.py::test_espaco_desativado_recusa_nova_reserva_com_409`; `espacos/tests/test_api_desativacao_e_reservas.py::test_reserva_existente_continua_listada_com_as_acoes_depois_de_desativar`; `pages/PaginaEspacos.test.tsx`: `o diálogo explica que as reservas existentes continuam valendo`; `pages/PaginaEspacos.test.tsx`: `desativar com sucesso mostra o toast, fecha e recarrega a lista` |
| <a id="ta-50"></a>TA-50 | [CA-02](#us-07-ca-02) | automatizado | `espacos/tests/test_api_edicao_de_espaco.py::test_ativar_espaco_inativo_responde_200_com_o_espaco_ativo`; `espacos/tests/test_api_desativacao_e_reservas.py::test_reativar_volta_a_aceitar_reservas`; `pages/PaginaEspacos.test.tsx`: `reativar chama a API de ativar para o espaço inativo` |
| <a id="ta-51"></a>TA-51 | [CA-03](#us-07-ca-03) | automatizado | `pages/PaginaEspacos.test.tsx`: `"Voltar" fecha sem chamar a API e devolve o foco ao botão da linha` |
| <a id="ta-52"></a>TA-52 | [CA-04](#us-07-ca-04) | automatizado | `espacos/tests/test_api_desativacao_e_reservas.py::test_reserva_existente_continua_listada_com_as_acoes_depois_de_desativar`; `espacos/tests/test_api_desativacao_e_reservas.py::test_reserva_existente_pode_ser_confirmada_depois_de_desativar` |
| <a id="ta-53"></a>TA-53 | [CA-05](#us-07-ca-05) | automatizado | `espacos/tests/test_api_edicao_de_espaco.py::test_acoes_em_espaco_inexistente_respondem_404 [x]` |
| <a id="ta-54"></a>TA-54 | [CA-06](#us-07-ca-06) | automatizado | `espacos/tests/test_api_edicao_de_espaco.py::test_desativar_espaco_ja_inativo_responde_409_e_ele_continua_inativo`; `espacos/tests/test_espaco_esportivo.py::test_desativar_espaco_ja_inativo_e_recusado` |
| <a id="ta-55"></a>TA-55 | [CA-07](#us-07-ca-07) | automatizado | `espacos/tests/test_api_edicao_de_espaco.py::test_ativar_espaco_ja_ativo_responde_409`; `espacos/tests/test_espaco_esportivo.py::test_ativar_espaco_ja_ativo_e_recusado` |
| <a id="ta-56"></a>TA-56 | [CA-08](#us-07-ca-08) | automatizado | `espacos/tests/test_concorrencia_de_espaco.py::test_duas_desativacoes_simultaneas_aceitam_so_uma`; `pages/PaginaEspacos.test.tsx`: `com 409 %s, mostra o aviso e "Atualizar lista", que fecha e recarrega` |
| <a id="ta-57"></a>TA-57 | [CA-09](#us-07-ca-09) | automatizado | `espacos/tests/test_api_edicao_de_espaco.py::test_solicitante_nao_edita_desativa_nem_ativa_e_nada_muda [x]`; `config/tests/test_matriz_de_acesso.py::test_matriz_de_acesso [x]` |
