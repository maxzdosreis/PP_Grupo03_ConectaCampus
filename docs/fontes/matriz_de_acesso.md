# Matriz de acesso da API (AUT-07)

> **Fonte da verdade:** `src/backend/config/tests/test_matriz_de_acesso.py`. Esta tabela repete a do teste, e as duas precisam mudar juntas. Toda rota ou método novo sob `/api/` precisa de uma linha no teste: a guarda de cobertura falha com "a rota X não tem regra de acesso declarada na matriz" (ou "o método X da rota Y ...").
>
> Evidência dos testes de aceite de segurança para a rastreabilidade de Requisitos (REQ-06; DEC-04, RNF de segurança).

## Como a matriz é testada

- **Personas:** anônimo (sem token); **dono** (solicitante dono da reserva do cenário); **outro** (outro solicitante); **gestor**. Exceto o anônimo, cada uma faz login de verdade em `POST /api/auth/login/` e usa `Authorization: Bearer <access>`, sem `force_authenticate`.
- **Cenário de cada caso:** um espaço ativo e um espaço inativo, os dois cadastrados pelo gestor (o inativo é desativado pela API e é o alvo de `espacos:ativar`), e uma reserva do dono no espaço ativo (amanhã, 10:00–11:00). Cada caso roda isolado, com o banco desfeito ao final.
- **Livre:** "não exige login". O anônimo (e qualquer persona) não recebe 401 nem 403.
- Além do status, o código do erro é conferido: 401 `NAO_AUTENTICADO`, 403 `ACAO_NAO_PERMITIDA`, 405 `METODO_NAO_PERMITIDO`.

## Matriz

| Rota (nome) | Caminho | Método | Corpo de exemplo | Anônimo | Dono | Outro | Gestor |
|---|---|---|---|---|---|---|---|
| `health` | `/api/health/` | GET | — | 200 | 200 | 200 | 200 |
| `contas:login` | `/api/auth/login/` | POST | e-mail e senha válidos | livre | livre | livre | livre |
| `contas:refresh` | `/api/auth/refresh/` | POST | refresh válido (trocado a cada uso, AUT-09) | livre | livre | livre | livre |
| `contas:logout` | `/api/auth/logout/` | POST | refresh válido (do dono) | livre | livre | livre | livre |
| `contas:logout` | `/api/auth/logout/` | GET | — | 405 | 405 | 405 | 405 |
| `contas:logout` | `/api/auth/logout/` | PUT | — | 405 | 405 | 405 | 405 |
| `contas:logout` | `/api/auth/logout/` | PATCH | — | 405 | 405 | 405 | 405 |
| `contas:logout` | `/api/auth/logout/` | DELETE | — | 405 | 405 | 405 | 405 |
| `contas:cadastro` | `/api/auth/cadastro/` | POST | novo usuário | livre | livre | livre | livre |
| `contas:me` | `/api/auth/me/` | GET | — | 401 | 200 | 200 | 200 |
| `contas:senha` | `/api/auth/senha/` | POST | senha atual e nova senha válidas (AUT-10) | 401 | 200 | 200 | 200 |
| `contas:senha` | `/api/auth/senha/` | GET | — | 401 | 405 | 405 | 405 |
| `contas:senha` | `/api/auth/senha/` | PUT | — | 401 | 405 | 405 | 405 |
| `contas:senha` | `/api/auth/senha/` | PATCH | — | 401 | 405 | 405 | 405 |
| `contas:senha` | `/api/auth/senha/` | DELETE | — | 401 | 405 | 405 | 405 |
| `espacos:lista` | `/api/espacos/` | GET | — | 401 | 200 | 200 | 200 |
| `espacos:lista` | `/api/espacos/` | POST | novo espaço | 401 | 403 | 403 | 201 |
| `espacos:tipos` | `/api/espacos/tipos/` | GET | — | 200 | 200 | 200 | 200 |
| `espacos:detalhe` | `/api/espacos/{id}/` | GET | — | 401 | 200 | 200 | 200 |
| `espacos:detalhe` | `/api/espacos/{id}/` | PATCH | `{"capacidade": 40}` | 401 | 403 | 403 | 200 |
| `espacos:detalhe` | `/api/espacos/{id}/` | DELETE | — | 401 | 405 | 405 | 405 |
| `espacos:desativar` | `/api/espacos/{id}/desativar/` | POST | — | 401 | 403 | 403 | 200 |
| `espacos:desativar` | `/api/espacos/{id}/desativar/` | GET | — | 401 | 405 | 405 | 405 |
| `espacos:ativar` | `/api/espacos/{id}/ativar/` | POST | — (espaço inativo do cenário) | 401 | 403 | 403 | 200 |
| `espacos:ativar` | `/api/espacos/{id}/ativar/` | GET | — | 401 | 405 | 405 | 405 |
| `reservas:lista` | `/api/reservas/` | GET | — | 401 | 200 | 200 | 200 |
| `reservas:lista` | `/api/reservas/` | POST | nova reserva (14:00–15:00) | 401 | 201 | 201 | 201 |
| `reservas:situacoes` | `/api/reservas/situacoes/` | GET | — | 200 | 200 | 200 | 200 |
| `reservas:regras_de_agenda` | `/api/reservas/regras-de-agenda/` | GET | — | 200 | 200 | 200 | 200 |
| `reservas:ocupacao` | `/api/reservas/ocupacao/?espaco={id}&data=<amanhã>` | GET | — | 401 | 200 | 200 | 200 |
| `reservas:pendentes` | `/api/reservas/pendentes/` | GET | — | 401 | 403 | 403 | 200 |
| `reservas:contagem_por_situacao` | `/api/reservas/contagem-por-situacao/` | GET | — | 401 | 403 | 403 | 200 |
| `reservas:detalhe` | `/api/reservas/{id}/` | GET | — | 401 | 200 | 404 | 200 |
| `reservas:detalhe` | `/api/reservas/{id}/` | DELETE | — | 401 | 405 | 405 | 405 |
| `reservas:situacao` | `/api/reservas/{id}/situacao/` | PATCH | `CONFIRMADA` | 401 | 403 | 404 | 200 |
| `reservas:situacao` | `/api/reservas/{id}/situacao/` | PATCH | `CANCELADA` com motivo | 401 | 200 | 404 | 200 |
| `reservas:historico` | `/api/reservas/{id}/historico/` | GET | — | 401 | 200 | 404 | 200 |
| `reservas:historico` | `/api/reservas/{id}/historico/` | DELETE | — | 401 | 405 | 405 | 405 |
| `usuarios:lista` | `/api/usuarios/` | GET | — | 401 | 403 | 403 | 200 |
| `usuarios:detalhe` | `/api/usuarios/{id}/` | PATCH | desativar o usuário do cenário (AUT-11) | 401 | 403 | 403 | 200 |

## Leitura

- **Login obrigatório por padrão:** tudo exige login, exceto `health`, os vocabulários (`espacos:tipos`, `reservas:situacoes`, `reservas:regras_de_agenda`) e login, refresh, logout e cadastro.
- **Limite de tentativas (AUT-08):** login (por e-mail e por IP) e cadastro (por IP) recusam com 429 `LIMITE_DE_TENTATIVAS` o que passa do limite. Não é regra de acesso por perfil: a linha continua "livre" (não exige login) e vale igual para todas as personas. Cada caso da matriz faz no máximo cinco logins, com o contador zerado antes de cada teste (fixture do `conftest.py`), então nenhum caso chega ao limite. Provas em `contas/tests/test_limites_de_tentativas.py`.
- **Sair (AUT-09):** `contas:logout` é livre para todos, porque a posse do refresh é a credencial e o access pode já ter vencido; um refresh de outra pessoa é revogado do mesmo jeito, sem nenhum dado dela na resposta. Não tem limite de tentativas. Os outros métodos respondem 405 até para o anônimo, porque a rota não autentica ninguém.
- **Trocar a própria senha (AUT-10):** `contas:senha` exige login e é aberta aos dois perfis, mas só troca a senha de quem está logado: o usuário vem sempre do token, e a rota não tem id na URL nem no corpo. Tem limite de tentativas por usuário (429 `LIMITE_DE_TENTATIVAS`, `LIMITE_TROCA_DE_SENHA_POR_USUARIO`). Senha atual errada é 400 `SENHA_ATUAL_INCORRETA`, nunca 401. Provas em `contas/tests/test_api_alterar_senha.py`.
- **403 x 404:** o solicitante recebe 403 quando a ação é proibida ao perfil numa reserva que ele vê (confirmar a própria), e 404 numa reserva de outra pessoa, para não revelar que ela existe.
- **Sem exclusão:** `DELETE` não existe em espaços, em reservas nem no histórico (405 para quem está logado; o anônimo recebe 401 antes, porque a autenticação vem primeiro). Espaço é desativado, reserva muda de situação e o histórico só recebe registros novos (RES-07); nada é excluído.
- **Gestão de espaços (ESP-04):** cadastrar, editar (`PATCH`), desativar e reativar são só do gestor; os dois solicitantes recebem 403. As rotas de ação só aceitam `POST`: um `GET` nelas responde 405 a quem está logado, porque a restrição ao gestor vale só para o método implementado.
- **Histórico:** segue a visibilidade do detalhe. O dono e o gestor leem; outro solicitante recebe 404, como no detalhe.
- **Agenda do dia (FE-07):** qualquer pessoa logada consulta, inclusive o outro solicitante, que vê o 10:00–11:00 do dono como ocupado. A resposta só traz intervalo e situação, sem nome, matrícula, id, finalidade nem motivo (`reservas/tests/test_api_ocupacao_do_dia.py::test_solicitante_ve_a_reserva_de_outra_pessoa_sem_nenhum_dado_pessoal`). A query string (`espaco` e `data` de amanhã) vem de `_CONSULTA_DO_CENARIO`.
- **Fila de pendentes e contagem por situação (RDS-08, CR-09):** só o gestor consulta. O dono e o outro solicitante recebem 403 `ACAO_NAO_PERMITIDA`, inclusive quando têm reservas pendentes; outros métodos respondem 405 a quem está logado. A recusa vem do caso de uso, antes de qualquer leitura.

## Outros testes de segurança (fora da matriz)

| Requisito | Teste |
|---|---|
| Refresh de usuário inativo ou excluído → 401 | `contas/tests/test_api_autenticacao.py::test_refresh_de_usuario_inativo_responde_401`, `::test_refresh_de_usuario_excluido_responde_401` |
| Access de usuário desativado ou excluído → 401 | `::test_access_de_usuario_desativado_depois_do_login_responde_401`, `::test_access_de_usuario_excluido_responde_401` |
| Token adulterado, outra chave, `alg: none`, refresh como access → 401 | `::test_token_adulterado_responde_401` |
| `Authorization` fora do padrão → 401 | `::test_cabecalho_authorization_fora_do_padrao_responde_401`; Basic em `reservas/tests/test_api_reservas.py::test_autenticacao_basic_nao_e_mais_aceita` |
| Refresh revogado ao sair ou já trocado numa renovação → 401; o access continua até expirar | `contas/tests/test_api_sair.py::test_sair_revoga_o_refresh_e_ele_deixa_de_renovar`, `::test_access_emitido_antes_de_sair_continua_valendo_ate_expirar`; `contas/tests/test_api_autenticacao.py::test_renovacao_troca_o_refresh_e_o_antigo_passa_a_ser_recusado`, `::test_duas_trocas_do_mesmo_refresh_so_a_primeira_vale` |
| Perfil lido do banco a cada requisição | `config/tests/test_perfil_lido_do_banco.py` |
| CORS só para a origem configurada | `config/tests/test_cors.py` |
| Campos extras no PATCH de situação ignorados | `reservas/tests/test_api_situacao_reserva.py::test_campos_extras_no_corpo_nao_alteram_a_reserva` |
- **Gestão de usuários (AUT-11):** `usuarios:lista` e `usuarios:detalhe` são só do Gestor: quem não é Gestor recebe 403 `ACAO_NAO_PERMITIDA` antes de qualquer outra coisa (o Gestor que pede um método que a rota não tem, como DELETE, recebe 405: `test_outros_metodos_do_detalhe_respondem_405`) e o anônimo, 401. O perfil é lido do banco a cada pedido, então um Gestor rebaixado perde o acesso com a mesma credencial. Não há exclusão de usuário. Alterar tem limite de tentativas por usuário (429 `LIMITE_DE_TENTATIVAS`, `LIMITE_GESTAO_DE_USUARIOS_POR_USUARIO`). As recusas de regra (próprio Gestor, último Gestor) são 403 e 409, nunca 401. Provas em `contas/tests/test_api_gestao_de_usuarios.py` e `contas/tests/test_concorrencia_de_gestao.py`.
