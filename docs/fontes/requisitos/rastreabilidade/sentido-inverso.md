# Rastreabilidade no sentido inverso (rota ou tela → RF → NS)

> Gerado por `scripts/gerar_rastreabilidade.py`, não edite à mão; para mudar um vínculo, mude a ficha de origem.

| Identificação | Responsabilidade |
|---|---|
| **Parte da [RAS-01](README.md) • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

Prova de que nenhum comportamento existe sem necessidade: cada rota da [matriz de acesso](../../matriz_de_acesso.md), cada página do frontend e cada comando citado nas fichas aparece com os RF cuja evidência a cita (os filhos que só herdam a rota do pai não entram) e as NS de origem deles. Rota sem RF aparece marcada, com o RNF ou a lacuna que a explica.

## Rotas da API

| Rota | Nome | RF | NS | Observação |
|---|---|---|---|---|
| `GET /api/health/` | `health` | [RF-40](matriz.md#rf-40) | [NS-16](../visao.md#ns-16) | — |
| `POST /api/auth/login/` | `contas:login` (corpo: e-mail e senha válidos) | [RF-33](matriz.md#rf-33) | [NS-11](../visao.md#ns-11) | — |
| `POST /api/auth/refresh/` | `contas:refresh` (corpo: refresh válido (trocado a cada uso, AUT-09)) | [RF-34](matriz.md#rf-34) | [NS-11](../visao.md#ns-11) | — |
| `POST /api/auth/logout/` | `contas:logout` (corpo: refresh válido (do dono)) | [RF-36](matriz.md#rf-36) | [NS-11](../visao.md#ns-11), [NS-14](../visao.md#ns-14) | — |
| `GET /api/auth/logout/` | `contas:logout` | **sem RF** | — | método não implementado, provado pela matriz: [RNF-F04](../requisitos/rnf.md#rnf-f04) (toda rota e método com regra) |
| `PUT /api/auth/logout/` | `contas:logout` | **sem RF** | — | método não implementado, provado pela matriz: [RNF-F04](../requisitos/rnf.md#rnf-f04) (toda rota e método com regra) |
| `PATCH /api/auth/logout/` | `contas:logout` | **sem RF** | — | método não implementado, provado pela matriz: [RNF-F04](../requisitos/rnf.md#rnf-f04) (toda rota e método com regra) |
| `DELETE /api/auth/logout/` | `contas:logout` | **sem RF** | — | operação inexistente, provada pela matriz: [RNF-R05](../requisitos/rnf.md#rnf-r05) (nada é excluído) |
| `POST /api/auth/cadastro/` | `contas:cadastro` (corpo: novo usuário) | [RF-32](matriz.md#rf-32) | [NS-15](../visao.md#ns-15) | — |
| `GET /api/auth/me/` | `contas:me` | [RF-35](matriz.md#rf-35) | [NS-11](../visao.md#ns-11) | — |
| `GET /api/espacos/` | `espacos:lista` | [RF-01](matriz.md#rf-01), [RF-02](matriz.md#rf-02) | [NS-01](../visao.md#ns-01) | — |
| `POST /api/espacos/` | `espacos:lista` (corpo: novo espaço) | [RF-05](matriz.md#rf-05) | [NS-02](../visao.md#ns-02) | — |
| `GET /api/espacos/tipos/` | `espacos:tipos` | [RF-04](matriz.md#rf-04) | [NS-01](../visao.md#ns-01) | — |
| `GET /api/espacos/{id}/` | `espacos:detalhe` | [RF-03](matriz.md#rf-03) | [NS-01](../visao.md#ns-01) | — |
| `PATCH /api/espacos/{id}/` | `espacos:detalhe` (corpo: `{"capacidade": 40}`) | [RF-06](matriz.md#rf-06) | [NS-02](../visao.md#ns-02) | — |
| `DELETE /api/espacos/{id}/` | `espacos:detalhe` | **sem RF** | — | operação inexistente, provada pela matriz: [RNF-R05](../requisitos/rnf.md#rnf-r05) (nada é excluído) |
| `POST /api/espacos/{id}/desativar/` | `espacos:desativar` | [RF-07](matriz.md#rf-07) | [NS-02](../visao.md#ns-02) | — |
| `GET /api/espacos/{id}/desativar/` | `espacos:desativar` | **sem RF** | — | método não implementado, provado pela matriz: [RNF-F04](../requisitos/rnf.md#rnf-f04) (toda rota e método com regra) |
| `POST /api/espacos/{id}/ativar/` | `espacos:ativar` (corpo: — (espaço inativo do cenário)) | [RF-08](matriz.md#rf-08) | [NS-02](../visao.md#ns-02) | — |
| `GET /api/espacos/{id}/ativar/` | `espacos:ativar` | **sem RF** | — | método não implementado, provado pela matriz: [RNF-F04](../requisitos/rnf.md#rnf-f04) (toda rota e método com regra) |
| `GET /api/reservas/` | `reservas:lista` | [RF-12](matriz.md#rf-12), [RF-12.2](matriz.md#rf-12-2), [RF-13](matriz.md#rf-13), [RF-16](matriz.md#rf-16) | [NS-07](../visao.md#ns-07), [NS-08](../visao.md#ns-08), [NS-09](../visao.md#ns-09), [NS-10](../visao.md#ns-10), [NS-11](../visao.md#ns-11), [NS-14](../visao.md#ns-14) | — |
| `POST /api/reservas/` | `reservas:lista` (corpo: nova reserva (14:00–15:00)) | [RF-11](matriz.md#rf-11) | [NS-03](../visao.md#ns-03) | — |
| `GET /api/reservas/situacoes/` | `reservas:situacoes` | [RF-15](matriz.md#rf-15) | [NS-07](../visao.md#ns-07), [NS-08](../visao.md#ns-08) | — |
| `GET /api/reservas/regras-de-agenda/` | `reservas:regras_de_agenda` | [RF-28](matriz.md#rf-28) | [NS-06](../visao.md#ns-06) | — |
| `GET /api/reservas/ocupacao/` | `reservas:ocupacao` | [RF-29](matriz.md#rf-29), [RF-30](matriz.md#rf-30), [RF-31](matriz.md#rf-31) | [NS-05](../visao.md#ns-05), [NS-06](../visao.md#ns-06), [NS-14](../visao.md#ns-14) | — |
| `GET /api/reservas/{id}/` | `reservas:detalhe` | [RF-14](matriz.md#rf-14), [RF-16](matriz.md#rf-16) | [NS-07](../visao.md#ns-07), [NS-08](../visao.md#ns-08), [NS-09](../visao.md#ns-09), [NS-10](../visao.md#ns-10), [NS-11](../visao.md#ns-11) | — |
| `DELETE /api/reservas/{id}/` | `reservas:detalhe` | **sem RF** | — | operação inexistente, provada pela matriz: [RNF-R05](../requisitos/rnf.md#rnf-r05) (nada é excluído) |
| `PATCH /api/reservas/{id}/situacao/` | `reservas:situacao` (corpo: `CONFIRMADA`) | [RF-17](matriz.md#rf-17), [RF-18](matriz.md#rf-18), [RF-19](matriz.md#rf-19), [RF-20](matriz.md#rf-20), [RF-21](matriz.md#rf-21) | [NS-09](../visao.md#ns-09), [NS-10](../visao.md#ns-10) | — |
| `PATCH /api/reservas/{id}/situacao/` | `reservas:situacao` (corpo: `CANCELADA` com motivo) | [RF-17](matriz.md#rf-17), [RF-18](matriz.md#rf-18), [RF-19](matriz.md#rf-19), [RF-20](matriz.md#rf-20), [RF-21](matriz.md#rf-21) | [NS-09](../visao.md#ns-09), [NS-10](../visao.md#ns-10) | — |
| `GET /api/reservas/{id}/historico/` | `reservas:historico` | [RF-22](matriz.md#rf-22) | [NS-11](../visao.md#ns-11), [NS-12](../visao.md#ns-12) | — |
| `DELETE /api/reservas/{id}/historico/` | `reservas:historico` | **sem RF** | — | operação inexistente, provada pela matriz: [RNF-R05](../requisitos/rnf.md#rnf-r05) (nada é excluído) |

## Telas

| Rota | Nome | RF | NS | Observação |
|---|---|---|---|---|
| `/` | PaginaInicial | [RF-36](matriz.md#rf-36), [RF-40](matriz.md#rf-40) | [NS-11](../visao.md#ns-11), [NS-14](../visao.md#ns-14), [NS-16](../visao.md#ns-16) | — |
| `/entrar` | PaginaEntrar | [RF-33](matriz.md#rf-33) | [NS-11](../visao.md#ns-11) | — |
| `/cadastro` | PaginaCadastro | [RF-32](matriz.md#rf-32) | [NS-15](../visao.md#ns-15) | — |
| `/espacos` | PaginaEspacos | [RF-01](matriz.md#rf-01), [RF-02](matriz.md#rf-02), [RF-04](matriz.md#rf-04), [RF-05](matriz.md#rf-05), [RF-06](matriz.md#rf-06), [RF-07](matriz.md#rf-07), [RF-08](matriz.md#rf-08) | [NS-01](../visao.md#ns-01), [NS-02](../visao.md#ns-02) | — |
| `/reservas` | PaginaReservas | [RF-12](matriz.md#rf-12), [RF-12.2](matriz.md#rf-12-2), [RF-13](matriz.md#rf-13), [RF-15](matriz.md#rf-15), [RF-16](matriz.md#rf-16) | [NS-07](../visao.md#ns-07), [NS-08](../visao.md#ns-08), [NS-09](../visao.md#ns-09), [NS-10](../visao.md#ns-10), [NS-11](../visao.md#ns-11), [NS-14](../visao.md#ns-14) | — |
| `/reservas/nova` | PaginaNovaReserva | [RF-11](matriz.md#rf-11), [RF-28](matriz.md#rf-28), [RF-29](matriz.md#rf-29), [RF-30](matriz.md#rf-30), [RF-31](matriz.md#rf-31), [RF-35](matriz.md#rf-35) | [NS-03](../visao.md#ns-03), [NS-05](../visao.md#ns-05), [NS-06](../visao.md#ns-06), [NS-11](../visao.md#ns-11), [NS-14](../visao.md#ns-14) | — |
| `/reservas/:reservaId` | PaginaReserva | [RF-03](matriz.md#rf-03), [RF-14](matriz.md#rf-14), [RF-16](matriz.md#rf-16), [RF-22](matriz.md#rf-22) | [NS-01](../visao.md#ns-01), [NS-07](../visao.md#ns-07), [NS-08](../visao.md#ns-08), [NS-09](../visao.md#ns-09), [NS-10](../visao.md#ns-10), [NS-11](../visao.md#ns-11), [NS-12](../visao.md#ns-12) | — |
| `*` | PaginaNaoEncontrada | **sem RF** | — | sem RF: [L-17](../requisitos/srs.md#l-17) |
| `/admin/` | Django admin (config/urls.py) | [RF-37](matriz.md#rf-37) | [NS-11](../visao.md#ns-11) | ver [L-10](../requisitos/srs.md#l-10) |

## Comandos

| Rota | Nome | RF | NS | Observação |
|---|---|---|---|---|
| `comando carregar_dados_exemplo` | carregar_dados_exemplo | [RF-39](matriz.md#rf-39) | [NS-16](../visao.md#ns-16) | — |
| `comando createsuperuser` | createsuperuser | [RF-37](matriz.md#rf-37) | [NS-11](../visao.md#ns-11) | — |
