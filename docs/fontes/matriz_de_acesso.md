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
| `contas:refresh` | `/api/auth/refresh/` | POST | refresh válido | livre | livre | livre | livre |
| `contas:cadastro` | `/api/auth/cadastro/` | POST | novo usuário | livre | livre | livre | livre |
| `contas:me` | `/api/auth/me/` | GET | — | 401 | 200 | 200 | 200 |
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
| `reservas:detalhe` | `/api/reservas/{id}/` | GET | — | 401 | 200 | 404 | 200 |
| `reservas:detalhe` | `/api/reservas/{id}/` | DELETE | — | 401 | 405 | 405 | 405 |
| `reservas:situacao` | `/api/reservas/{id}/situacao/` | PATCH | `CONFIRMADA` | 401 | 403 | 404 | 200 |
| `reservas:situacao` | `/api/reservas/{id}/situacao/` | PATCH | `CANCELADA` com motivo | 401 | 200 | 404 | 200 |
| `reservas:historico` | `/api/reservas/{id}/historico/` | GET | — | 401 | 200 | 404 | 200 |
| `reservas:historico` | `/api/reservas/{id}/historico/` | DELETE | — | 401 | 405 | 405 | 405 |

## Leitura

- **Login obrigatório por padrão:** tudo exige login, exceto `health`, os vocabulários (`espacos:tipos`, `reservas:situacoes`, `reservas:regras_de_agenda`) e login, refresh e cadastro.
- **403 x 404:** o solicitante recebe 403 quando a ação é proibida ao perfil numa reserva que ele vê (confirmar a própria), e 404 numa reserva de outra pessoa, para não revelar que ela existe.
- **Sem exclusão:** `DELETE` não existe em espaços, em reservas nem no histórico (405 para quem está logado; o anônimo recebe 401 antes, porque a autenticação vem primeiro). Espaço é desativado, reserva muda de situação e o histórico só recebe registros novos (RES-07); nada é excluído.
- **Gestão de espaços (ESP-04):** cadastrar, editar (`PATCH`), desativar e reativar são só do gestor; os dois solicitantes recebem 403. As rotas de ação só aceitam `POST`: um `GET` nelas responde 405 a quem está logado, porque a restrição ao gestor vale só para o método implementado.
- **Histórico:** segue a visibilidade do detalhe. O dono e o gestor leem; outro solicitante recebe 404, como no detalhe.

## Outros testes de segurança (fora da matriz)

| Requisito | Teste |
|---|---|
| Refresh de usuário inativo ou excluído → 401 | `contas/tests/test_api_autenticacao.py::test_refresh_de_usuario_inativo_responde_401`, `::test_refresh_de_usuario_excluido_responde_401` |
| Access de usuário desativado ou excluído → 401 | `::test_access_de_usuario_desativado_depois_do_login_responde_401`, `::test_access_de_usuario_excluido_responde_401` |
| Token adulterado, outra chave, `alg: none`, refresh como access → 401 | `::test_token_adulterado_responde_401` |
| `Authorization` fora do padrão → 401 | `::test_cabecalho_authorization_fora_do_padrao_responde_401`; Basic em `reservas/tests/test_api_reservas.py::test_autenticacao_basic_nao_e_mais_aceita` |
| Perfil lido do banco a cada requisição | `config/tests/test_perfil_lido_do_banco.py` |
| CORS só para a origem configurada | `config/tests/test_cors.py` |
| Campos extras no PATCH de situação ignorados | `reservas/tests/test_api_situacao_reserva.py::test_campos_extras_no_corpo_nao_alteram_a_reserva` |
