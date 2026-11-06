# Conecta Campus — Reserva de Quadras e Espaços Esportivos

Sistema para a comunidade acadêmica cadastrar quadras e espaços esportivos, solicitar reservas e acompanhar a situação de cada reserva.

## O que o sistema faz

1. **Espaços:** o Gestor cadastra, lista, edita, desativa e reativa quadras e espaços (espaço nunca é excluído).
2. **Solicitar reserva:** quem está logado pede um espaço numa data e horário, com finalidade; a reserva nasce **Solicitada**.
3. **Consultar:** reservas filtradas por espaço, situação, data, solicitante e "somente minhas", combináveis; detalhe com o histórico.
4. **Alterar a situação:** Solicitada → Confirmada, Recusada ou Cancelada; Confirmada → Concluída ou Cancelada (recusar e cancelar pedem motivo).
5. **Bloquear operações inválidas:** campos vazios, espaço inexistente ou inativo, horário que já passou, conflito de horário, fora do horário de funcionamento e transição proibida.
6. **Mensagens claras** de sucesso e de erro, vindas da API e mostradas na tela.

**Login e perfis (extra):** entrar com e-mail e senha (token JWT). O **Solicitante** pede reservas e cancela as próprias; o **Gestor** cuida dos espaços e confirma, recusa, conclui ou cancela qualquer reserva.

## Tecnologias

| Parte | Tecnologia e versão |
|---|---|
| Backend | Python 3.12, Django 5.2 LTS (5.2.18), Django REST Framework 3.18, Simple JWT 5.5 (login com token), django-cors-headers 4.9 |
| Banco | PostgreSQL 16 (driver psycopg 3) |
| Frontend | Node 24, React 19.3, TypeScript 6.0, Vite 8.3, React Router 8.4, ESLint 10; testes com Vitest 5, Testing Library 16 e jsdom 30 (só desenvolvimento) |
| Execução | Docker e Docker Compose |

As versões exatas estão em `src/backend/requirements.txt`, `src/backend/requirements-dev.txt` e `src/frontend/package-lock.json`.

## Como executar

### Pré-requisito

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (inclui o Docker Compose).

### Passo a passo

1. Na raiz do repositório, crie o arquivo de variáveis de ambiente a partir do exemplo (se `src/.env` já existir, mantenha o seu):

   ```bash
   cp src/.env.example src/.env
   ```

   No Prompt de Comando do Windows:

   ```bat
   copy src\.env.example src\.env
   ```

   Se já existir um PostgreSQL rodando na porta 5432 do seu computador, mude só `DB_PORT_HOST` (ex.: `5433`). `DB_PORT` é a porta usada pelo Django dentro da rede do Docker e deve continuar `5432`. O que faz cada variável: [README de `src`](src/README.md#variáveis-de-ambiente-env).

2. Entre na pasta `src` e suba os três serviços (banco, backend e frontend):

   ```bash
   cd src
   docker compose up --build
   ```

   As migrations do banco são aplicadas automaticamente quando o backend sobe.

3. Com os serviços no ar, em outro terminal dentro de `src`, carregue os dados de exemplo (usuários, espaços e reservas; veja [Dados de exemplo](#dados-de-exemplo)):

   ```bash
   docker compose exec backend python manage.py carregar_dados_exemplo
   ```

4. Acesse:
   - Aplicação (frontend): http://localhost:5173 — entre com um dos [usuários de exemplo](#dados-de-exemplo) em http://localhost:5173/entrar ou crie uma conta em http://localhost:5173/cadastro. O que cada tela faz e quem acessa: [README do frontend](src/frontend/README.md#rotas-e-telas).
   - API: http://localhost:8000 — endpoints e exemplos com `curl` no [README do backend](src/backend/README.md).
   - Saúde da API: http://localhost:8000/api/health/
   - Admin do Django: http://localhost:8000/admin/ — com a gestora de exemplo ou um [superusuário](src/backend/README.md#criar-um-superusuário-acesso-ao-admin).

### Verificar se a API está no ar

`GET /api/health/` testa a conexão com o banco:

- **200** — `{"mensagem": "API no ar.", "dados": {"banco": "ok"}}`
- **503** — `{"erro": {"codigo": "BANCO_INDISPONIVEL", "mensagem": "Não foi possível conectar ao banco de dados."}}`

## Dados de exemplo

```bash
docker compose exec backend python manage.py carregar_dados_exemplo
```

O comando cria usuários, espaços e reservas passando pelas mesmas regras do sistema (casos de uso e entidades do domínio): se um dado de exemplo violasse uma regra, o comando falharia sem gravar nada. Pode ser executado mais de uma vez: o que já existe (usuário pelo e-mail, espaço pelo nome) não é criado de novo, e as reservas só são criadas se os solicitantes de exemplo ainda não tiverem nenhuma. Ele só roda com `DJANGO_DEBUG=True` (o valor do `.env.example`), porque cria usuários com senhas conhecidas. Como ele funciona por dentro: [README de exemplos](src/backend/exemplos/README.md).

**Usuários de exemplo.** As senhas são fictícias e servem **só para teste local**:

| Nome | E-mail | Matrícula | Perfil | Senha |
|---|---|---|---|---|
| Carla Mendes | `carla.mendes@exemplo.com` | 2026900 | Gestor (também entra no `/admin/`) | `Apito-Dourado-48` |
| Bruno Lima | `bruno.lima@exemplo.com` | 2026101 | Solicitante | `Rede-Alta-73` |
| Daniela Rocha | `daniela.rocha@exemplo.com` | 2026102 | Solicitante | `Cesta-Tripla-59` |

**Espaços:** Quadra Poliesportiva Central (30 pessoas), Campo de Futebol Principal (22), Ginásio Coberto (200), Quadra de Areia Norte (12), Quadra de Tênis 1 (4) — um de cada tipo — e a Quadra de Tênis 2 (4), **inativa**.

**Reservas**, com datas relativas ao dia em que o comando roda:

| Situação | Quando | Espaço | Solicitante |
|---|---|---|---|
| Solicitada | amanhã, 10:00–11:00 | Quadra Poliesportiva Central | Bruno Lima |
| Confirmada | amanhã, 14:00–16:00 | Campo de Futebol Principal | Daniela Rocha |
| Recusada (com motivo) | daqui a 2 dias, 19:00–21:00 | Ginásio Coberto | Bruno Lima |
| Cancelada (com motivo) | daqui a 3 dias, 08:00–09:00 | Quadra de Areia Norte | Daniela Rocha |
| Concluída | ontem, 18:00–19:30 | Quadra de Tênis 1 | Bruno Lima |

**Horário para demonstrar o conflito:** Quadra Poliesportiva Central, **amanhã, 10:30–11:30** — sobrepõe a reserva Solicitada e responde **409** `CONFLITO_DE_HORARIO`. O próprio comando imprime esse horário com a data no fim da saída.

## Roteiro da demonstração

Pela tela, em http://localhost:5173, com os usuários de exemplo:

1. **Entrar como solicitante.** Abrir http://localhost:5173/reservas sem login: a aplicação leva para a tela de entrar. Entrar como Bruno (`bruno.lima@exemplo.com`, `Rede-Alta-73`); depois do login, ela volta para as reservas. O cabeçalho mostra "Bruno Lima · Solicitante".
2. **Consultar.** O menu mostra "Minhas reservas", e Bruno vê só as próprias reservas (Solicitada, Recusada e Concluída), sem os filtros de solicitante. Filtrar por espaço "Quadra Poliesportiva Central" e situação "Solicitada" (dois critérios combinados). Só a Solicitada tem ação, e só "Cancelar". Limpar os filtros e clicar na data da reserva Concluída (ontem, Quadra de Tênis 1): a linha do tempo mostra as três etapas — "Solicitada por Bruno Lima", "Confirmada por Carla Mendes" e "Concluída por Carla Mendes", cada uma com data e hora.
3. **Agenda do dia e entrada inválida.** Em "Nova reserva", que mostra "Solicitante: Bruno Lima (2026101)", escolher a Quadra Poliesportiva Central e a data de **amanhã**: a [agenda do dia](src/backend/reservas/README.md#agenda-do-dia) mostra **10:00–11:00** em "Ocupados" (Solicitada) e as janelas livres 07:00–10:00 e 11:00–22:00, sem dizer de quem é a reserva. Mesmo assim, insistir em **10:30–11:30**, com qualquer finalidade: o aviso no topo do formulário explica o conflito de horário (**409** `CONFLITO_DE_HORARIO`), os valores continuam preenchidos e a agenda é recarregada. Outras entradas inválidas prontas: uma data de ontem, explicada embaixo do campo Data (a agenda avisa "Não é possível reservar um horário que já passou."); uma data daqui a 40 dias (a agenda mostra a data limite); um término antes do início; e **22:00–23:00**, fora do horário de funcionamento, com a mensagem "Os espaços funcionam das 07:00 às 22:00. Escolha um horário dentro desse período." embaixo do campo Término. Acima de Data, a dica mostra as [regras de agenda](src/backend/reservas/README.md#regras-de-agenda) que vêm da API.
4. **Solicitar.** Voltar a data para amanhã e, em "Livres", clicar em "Usar este horário" na janela **11:00–22:00**: Início vira 11:00 e Término 14:00 (a duração máxima de 3 h vem da API), e o foco vai para Término. Enviar: a mensagem de sucesso aparece e o resumo mostra a situação "Solicitada". "Ver minhas reservas" leva à lista com a nova reserva.
5. **Cancelar.** Em "Minhas reservas", abrir a reserva Solicitada de amanhã às 10:00 (a dos dados de exemplo) e cancelá-la pelo detalhe: o diálogo pede o motivo, e sem motivo o erro aparece embaixo do campo. Com o motivo, a reserva passa a "Cancelada" e a linha do tempo ganha o item "Cancelada por Bruno Lima" com o motivo.
6. **Sem permissão.** Em "Espaços", Bruno vê a lista e o aviso "Somente o gestor cadastra espaços.", sem o formulário. Sair (botão "Sair" no cabeçalho).
7. **Entrar como gestora** Carla (`carla.mendes@exemplo.com`, `Apito-Dourado-48`). Em "Espaços", cadastrar um espaço (ex.: "Quadra Coberta Sul", Quadra poliesportiva, 20 pessoas); um nome repetido ou uma capacidade 0 mostra o erro embaixo do campo. Na tabela, "Editar" na Quadra de Areia Norte abre o diálogo já preenchido: trocar a capacidade para 16 e salvar mostra "Espaço atualizado com sucesso."; trocar o nome para "Ginásio Coberto" (já usado) ou a capacidade para 0 mostra o erro embaixo do campo, e salvar sem mudar nada mostra "Informe ao menos um campo para alterar.".
8. **Confirmar e concluir.** Em "Reservas", Carla vê as reservas de todos. Filtrar por situação "Solicitada", abrir a reserva das 11:00 do Bruno pela data, confirmá-la e depois concluí-la no próprio detalhe: cada mudança mostra a mensagem da API ("Reserva confirmada com sucesso.", "Reserva concluída com sucesso."), a linha do tempo ganha um item para cada uma, e a reserva concluída fica sem ações. "Voltar para as reservas" volta à lista ainda filtrada por "Solicitada".
9. **Desativar um espaço (operação inválida bloqueada).** Numa janela anônima ou em outro navegador (a sessão fica no navegador, então cada janela precisa da sua), entrar como Bruno, abrir "Nova reserva" e preencher o Campo de Futebol Principal, amanhã, 10:00–11:00. Na janela da Carla, em "Espaços", clicar em "Desativar" no Campo de Futebol Principal: o diálogo avisa que novas reservas ficarão bloqueadas e que as existentes continuam valendo. Confirmar. De volta à janela do Bruno, enviar o pedido: o aviso no topo do formulário mostra **409** "Este espaço está inativo e não aceita reservas.". Ao recarregar a página, o espaço nem aparece mais entre as opções. Em "Reservas", a Carla ainda vê a reserva Confirmada da Daniela nesse espaço, com "Concluir" e "Cancelar". Por fim, "Reativar" o espaço em "Espaços": o pedido do Bruno volta a ser aceito.

O mesmo roteiro com `curl`, no [README do backend](src/backend/README.md#roteiro-alternativo-com-curl), mostra também o **403** de um solicitante tentando confirmar, que a tela não oferece.

## Parar e recomeçar do zero

Dentro de `src`:

```bash
docker compose down
```

Para parar **e apagar os dados do banco**:

```bash
docker compose down -v
```

### Recomeçar do zero

Para apagar tudo (inclusive o que foi cadastrado à mão) e carregar os dados de novo, dentro de `src`. Faça isso também se o seu banco foi criado antes do histórico de situação (RES-07): as reservas antigas não têm histórico, porque a migration não reconstrói o passado.

```bash
docker compose down -v
```

```bash
docker compose up -d
```

```bash
docker compose exec backend python manage.py carregar_dados_exemplo
```

## Persistência

PostgreSQL 16, executado no container `db`. Os dados ficam no volume Docker `postgres_data` e se mantêm entre execuções até um `docker compose down -v`.

## Limitações conhecidas

- **Sem revogação de tokens:** não há lista de tokens revogados. Sair é descartar os tokens no cliente; um `access` roubado continua valendo até expirar (30 minutos) e um `refresh`, até 1 dia. A exceção é desativar ou excluir o usuário: a partir daí, nem o `access` nem o `refresh` dele são aceitos (401).
- **Sem limite de tentativas de login:** `POST /api/auth/login/` não limita tentativas, então não há proteção contra força bruta de senhas. A evolução natural é o throttling do DRF (`ScopedRateThrottle` com um escopo próprio para o login, ou `AnonRateThrottle`), que responde 429 depois de N tentativas por minuto.
- **Sessão no `localStorage`:** o frontend guarda os tokens e os dados do usuário no `localStorage` do navegador (chave `conecta-campus:sessao`), para o login sobreviver ao recarregar e a abas novas. Um script malicioso injetado na página (XSS) poderia ler esses tokens; cookies `HttpOnly` evitariam isso, mas exigiriam mudar a autenticação da API. Se o navegador recusar o `localStorage` (navegação privada), o login vale só até recarregar.
- **Perfil na interface:** esconder o formulário de espaços e os botões de editar, desativar e reativar de quem não é Gestor é só conveniência; quem garante as permissões é a API (403 `ACAO_NAO_PERMITIDA`).
- **Alterações simultâneas na mesma reserva:** se duas pessoas mudarem a situação da mesma reserva ao mesmo tempo, só a primeira é gravada; a segunda recebe 409 `RESERVA_DESATUALIZADA` e precisa atualizar a lista e decidir de novo. Não há nova tentativa automática.
- **Alterações simultâneas no mesmo espaço:** se dois gestores editarem, desativarem ou reativarem o mesmo espaço ao mesmo tempo, só a primeira alteração é gravada; a segunda recebe 409 `ESPACO_DESATUALIZADO` e precisa atualizar a lista e decidir de novo. Não há nova tentativa automática.
- **Histórico só das mudanças aceitas:** o histórico da reserva registra a criação e cada mudança de situação efetiva. Tentativas recusadas (sem permissão, transição inválida, motivo ausente) não ficam registradas em nenhum lugar, nem na linha do tempo do detalhe da reserva.

## Mapa da documentação

| Módulo | README | O que está lá |
|---|---|---|
| Execução | [`src/README.md`](src/README.md) | Serviços do Docker Compose, portas, volumes e cada variável do `.env.example`. |
| Backend | [`src/backend/README.md`](src/backend/README.md) | Organização em contextos e camadas, regra de dependência, formato das respostas, autenticação JWT, superusuário, comandos de teste e qualidade, roteiro com `curl`. |
| Contas | [`src/backend/contas/README.md`](src/backend/contas/README.md) | Perfis, regras de cadastro e senha, endpoints de cadastro, login e usuário logado. |
| Espaços | [`src/backend/espacos/README.md`](src/backend/espacos/README.md) | Regras dos espaços e endpoints de cadastrar, listar, editar, desativar e reativar. |
| Reservas | [`src/backend/reservas/README.md`](src/backend/reservas/README.md) | Regras de reserva, agenda, conflito, situações, permissões e histórico, com os endpoints. |
| Compartilhado | [`src/backend/compartilhado/README.md`](src/backend/compartilhado/README.md) | Erros de domínio, formato das respostas, tratador de erros e permissão de gestor. |
| Exemplos | [`src/backend/exemplos/README.md`](src/backend/exemplos/README.md) | Como o comando de dados de exemplo funciona. |
| Frontend | [`src/frontend/README.md`](src/frontend/README.md) | Pastas, rotas e telas, cliente da API e sessão, convenções e comandos. |
| Modelagem | [`docs/modelagem.pdf`](docs/modelagem.pdf) (gerado na entrega) | Visão do sistema, modelo do domínio, fluxo principal e decisões técnicas. |
| Contribuições | [`docs/contribuicoes.pdf`](docs/contribuicoes.pdf) (gerado na entrega) | Quem fez cada parte do trabalho. |
