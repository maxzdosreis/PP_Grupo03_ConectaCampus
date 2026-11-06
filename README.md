# Conecta Campus — Reserva de Quadras e Espaços Esportivos

Sistema para a comunidade acadêmica cadastrar quadras e espaços esportivos, solicitar reservas e acompanhar a situação de cada reserva.

## Identificação

- **Grupo 03** — Unilasalle RS, semestre 2026/2.
- **Disciplinas:** Requisitos de Software e Projeto de Programação. **Professor:** Luis Antonio Leite Francisco da Costa.
- **Integrantes:** [nome]; [nome]; [nome]. Quem fez cada parte está em [`docs/contribuicoes.pdf`](docs/contribuicoes.pdf).

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
| Backend | Python 3.12 (imagem `python:3.12-slim`), Django 5.2.18 LTS, Django REST Framework 3.18.3, Simple JWT 5.5.1 (login com token), django-cors-headers 4.9.0, psycopg 3.3.6 |
| Banco | PostgreSQL 16 (imagem `postgres:16-alpine`) |
| Frontend | Node 24 (imagem `node:24-alpine`), React 19.3.1, React Router 8.4.0, TypeScript 6.0.3, Vite 8.3.4; ESLint 10.13.0, Vitest 5.0.5, Testing Library 16.3.3 e jsdom 30.1.3 só no desenvolvimento |
| Execução | Docker e Docker Compose |

As versões das bibliotecas são fixas em `src/backend/requirements.txt` e `src/frontend/package-lock.json`. As imagens fixam só a versão principal; o grupo testou com Python 3.12.16, PostgreSQL 16.15 e Node 24.22.0.

## Como executar

### Pré-requisitos

- **Docker Desktop** instalado e **aberto** (no Windows, com o WSL 2, a opção padrão da instalação). Ele já traz o Docker Compose. Nada mais precisa ser instalado: Python, Node e PostgreSQL rodam dentro dos containers.
- **Conferir que o Docker está pronto**, em qualquer terminal:

  ```bash
  docker compose version
  ```

  ```bash
  docker version
  ```

  O primeiro mostra a versão do Compose; o segundo precisa mostrar também a parte **Server**. Se ele terminar com `failed to connect to the docker API`, o Docker Desktop está fechado: abra-o e espere ficar "running".
- **Portas livres no seu computador:** 5173 (tela), 8000 (API) e 5432 (banco). Se alguma estiver ocupada, troque-a no passo 1 (veja [Problemas comuns](#problemas-comuns)).
- Testado pelo grupo com Docker Desktop 4.91.0 (Docker Engine 29.8.0, Docker Compose 5.5.1) no Windows 10 Pro com WSL 2.

### Passo a passo

Os comandos valem para Git Bash, Linux e macOS; onde o Windows muda, há a versão para o PowerShell e o Prompt de Comando.

0. **Obtenha o projeto:** extraia o ZIP **ou** clone o repositório. Abra um terminal na pasta do projeto, a que tem `README.md`, `src/` e `docs/`.

1. **Crie o arquivo de configuração** a partir do exemplo (só na primeira vez; se `src/.env` já existir, mantenha o seu):

   ```bash
   cp src/.env.example src/.env
   ```

   No PowerShell ou no Prompt de Comando do Windows:

   ```bat
   copy src\.env.example src\.env
   ```

   Os valores do exemplo já funcionam como estão. Só mude uma porta se ela estiver ocupada, no `src/.env`:

   | Porta ocupada | O que mudar (ex.) |
   |---|---|
   | 5432 (banco) | `DB_PORT_HOST=5433` (`DB_PORT` continua `5432`) |
   | 8000 (API) | `BACKEND_PORT_HOST=8001` **e** `VITE_API_URL=http://localhost:8001/api` |
   | 5173 (tela) | `FRONTEND_PORT_HOST=5174` **e** `CORS_ALLOWED_ORIGINS=http://localhost:5174,http://127.0.0.1:5174`; a tela passa a ser http://localhost:5174 |

   O que faz cada variável: [README de `src`](src/README.md#variáveis-de-ambiente-env).

2. **Entre em `src` e suba os três serviços** (banco, API e tela):

   ```bash
   cd src
   docker compose up --build
   ```

   A primeira vez leva alguns minutos: o grupo mediu cerca de 4 minutos com as imagens base já baixadas (3 min de build e menos de 1 min até a API responder), mais o tempo de baixar as imagens. As tabelas do banco são criadas sozinhas. A API está pronta quando aparecer `Starting development server at http://0.0.0.0:8000/`; a tela (`Local: http://localhost:5173/`) costuma ficar pronta antes. Deixe este terminal aberto: ele mostra os registros dos serviços.

3. **Carregue os dados de exemplo.** Em **outro terminal**, também dentro de `src`:

   ```bash
   docker compose exec backend python manage.py carregar_dados_exemplo
   ```

   Ele termina mostrando os usuários e o horário de conflito com a data (veja [Dados de exemplo](#dados-de-exemplo)).

4. **Entre no sistema:** abra http://localhost:5173/entrar e entre como Bruno (`bruno.lima@exemplo.com`, senha `Rede-Alta-73`). A tela "Minhas reservas" mostra três reservas.

Outros endereços: a API em http://localhost:8000 (endpoints e exemplos com `curl` no [README do backend](src/backend/README.md)); o admin do Django em http://localhost:8000/admin/, com a gestora de exemplo ou um [superusuário](src/backend/README.md#criar-um-superusuário-acesso-ao-admin). O que cada tela faz: [README do frontend](src/frontend/README.md#rotas-e-telas).

### Verificar se a API está no ar

Abra http://localhost:8000/api/health/, que testa a conexão com o banco:

- **200** — `{"mensagem": "API no ar.", "dados": {"banco": "ok"}}`
- **503** — `{"erro": {"codigo": "BANCO_INDISPONIVEL", "mensagem": "Não foi possível conectar ao banco de dados."}}`

## Dados de exemplo

```bash
docker compose exec backend python manage.py carregar_dados_exemplo
```

O comando cria usuários, espaços e reservas passando pelas mesmas regras do sistema: se um dado de exemplo violasse uma regra, o comando falharia sem gravar nada. Pode ser executado mais de uma vez: o que já existe (usuário pelo e-mail, espaço pelo nome) não é criado de novo, e as reservas só são criadas se os solicitantes de exemplo ainda não tiverem nenhuma (a saída diz "0 criados, 3 já existiam"). Ele só roda com `DJANGO_DEBUG=True` (o valor do `.env.example`), porque cria usuários com senhas conhecidas. Como ele funciona por dentro: [README de exemplos](src/backend/exemplos/README.md).

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

Dentro de `src`, para parar os serviços **mantendo os dados** (no terminal do passo 2, `Ctrl+C` também para):

```bash
docker compose down
```

Para subir de novo, `docker compose up` (sem `--build`, que só é preciso na primeira vez ou depois de mudar dependências).

### Recomeçar do zero

Para **apagar todos os dados** (inclusive o que foi cadastrado à mão) e carregar os de exemplo de novo, dentro de `src`:

```bash
docker compose down -v
```

```bash
docker compose up -d
```

```bash
docker compose exec backend python manage.py carregar_dados_exemplo
```

O `-d` sobe os serviços em segundo plano; espere a [verificação da API](#verificar-se-a-api-está-no-ar) responder 200 antes do último comando.

## Persistência

Os dados ficam no PostgreSQL 16, no serviço `db` (imagem `postgres:16-alpine`), guardados no volume Docker **`conecta-campus_postgres_data`** (o Compose acrescenta o nome do projeto, `conecta-campus`, ao volume `postgres_data`). Eles se mantêm quando os serviços param (`Ctrl+C`, `docker compose stop` ou `docker compose down`) e quando o computador reinicia. Só são apagados com `docker compose down -v` ou removendo o volume. Rodar o comando de dados de exemplo de novo não duplica nada.

Como o nome do projeto é fixo, outra cópia do projeto no mesmo computador (outro clone ou outro ZIP extraído) usa **os mesmos containers e o mesmo banco**: rode uma cópia de cada vez, e lembre que um `docker compose down -v` em qualquer uma delas apaga os dados das duas.

## Problemas comuns

- **`failed to connect to the docker API` ao rodar qualquer comando:** o Docker Desktop está fechado ou ainda iniciando. Abra-o, espere ficar "running" e repita.
- **`ports are not available: exposing port TCP 0.0.0.0:8000 ... bind: Normalmente é permitida apenas uma utilização de cada endereço de soquete`** (em inglês, `Only one usage of each socket address` ou `port is already allocated`): outro programa usa a porta citada. Feche-o ou troque a porta no `src/.env` como na tabela do passo 1, e rode `docker compose up -d` de novo.
- **`required variable DB_PASSWORD is missing a value: defina DB_PASSWORD no .env`** (ou outra variável): falta o `src/.env` ou ele está incompleto. Refaça o passo 1, dentro da pasta do projeto, e rode o comando a partir de `src`. Depois de mudar o `.env`, rode `docker compose up -d` (um `restart` não relê o arquivo).
- **`CommandError: Os dados de exemplo só podem ser carregados com DJANGO_DEBUG=True...`:** o `src/.env` tem `DJANGO_DEBUG=False`. Volte para `True`, rode `docker compose up -d` e repita o comando.
- **"E-mail ou senha incorretos." com os usuários de exemplo:** os dados de exemplo não foram carregados neste banco (ou foram apagados com `down -v`). Rode o passo 3.
- **A tela mostra "Não foi possível conectar ao servidor. Verifique se a API está em execução.":** a API ainda está subindo (espere a mensagem do passo 2), ou uma porta foi trocada só pela metade: `VITE_API_URL` precisa usar a porta de `BACKEND_PORT_HOST`, e `CORS_ALLOWED_ORIGINS`, a de `FRONTEND_PORT_HOST`. Corrija o `src/.env` e rode `docker compose up -d`.
- **Finais de linha no Windows:** não é preciso converter nada. O grupo testou uma cópia com os arquivos em formato Windows (CRLF), inclusive o `.env`, o `docker-compose.yml` e os `Dockerfile`, e ela sobe igual.

## Limitações conhecidas

- **Configuração de desenvolvimento, não de produção:** a API roda no servidor de desenvolvimento do Django e a tela no do Vite, com o modo de depuração ligado, e o `.env.example` traz uma senha de banco e uma chave de exemplo. Serve para avaliar e demonstrar localmente, não para publicar.
- **Troca de porta em duas variáveis:** trocar a porta da API ou da tela exige ajustar também `VITE_API_URL` ou `CORS_ALLOWED_ORIGINS` (passo 1); o sistema não deduz uma da outra.
- **Fuso horário fixo:** datas e horários são sempre os de Brasília (America/Sao_Paulo), independentemente do fuso do computador.
- **Regras de agenda iguais para todos os espaços:** funcionamento das 07:00 às 22:00, duração de 30 minutos a 3 horas e até 30 dias de antecedência valem para todos; não há horário próprio por espaço.
- **Situação e horário da reserva independentes:** o Gestor pode concluir uma reserva antes do horário terminar e confirmar ou recusar depois de ele começar, qualquer um pode cancelar depois do uso, e uma reserva Solicitada que ninguém decidiu continua ocupando o horário mesmo depois da data.
- **Lista de reservas sem paginação:** a consulta devolve todas as reservas de uma vez. O grupo mediu 378 ms (p95) com 1.000 reservas e 1.743 ms com 5.000, então a lista fica lenta a partir de alguns milhares.
- **Matrícula não conferida com a instituição:** qualquer texto de até 20 caracteres, sem espaços, é aceito no cadastro.
- **Sem recuperação de senha nem troca de perfil pela tela:** quem esquecer a senha, ou precisar virar Gestor, depende da administração (admin do Django).
- **Desativar um espaço não cancela as reservas dele:** novas reservas ficam bloqueadas, mas as existentes continuam valendo, e o Gestor decide se cancela alguma.
- **Sem revogação de tokens:** sair é descartar os tokens no navegador; um token de acesso roubado continua valendo até expirar (30 minutos) e o de renovação, até 1 dia. A exceção é desativar ou excluir o usuário: a partir daí, nenhum token dele é aceito.
- **Sem limite de tentativas de login:** não há proteção contra quem tenta adivinhar senhas repetindo o login.
- **Sessão no `localStorage`:** a tela guarda os tokens no `localStorage` do navegador, para o login sobreviver ao recarregar. Um script malicioso injetado na página poderia lê-los. Na navegação privada que bloqueia o `localStorage`, o login vale só até recarregar.
- **Perfil na interface:** esconder o formulário e os botões de espaços de quem não é Gestor é só conveniência; quem garante as permissões é a API (403 `ACAO_NAO_PERMITIDA`).
- **Alterações simultâneas:** se duas pessoas mudarem ao mesmo tempo a situação da mesma reserva, ou o mesmo espaço, só a primeira é gravada; a segunda recebe 409 e precisa atualizar a lista e decidir de novo.
- **Histórico só das mudanças aceitas:** a linha do tempo registra a criação e cada mudança de situação efetiva; tentativas recusadas (sem permissão, transição inválida, motivo ausente) não ficam registradas.

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
| Modelagem | [`docs/modelagem.pdf`](docs/modelagem.pdf) | Visão do sistema, modelo do domínio, fluxo principal e decisões técnicas. |
| Contribuições | [`docs/contribuicoes.pdf`](docs/contribuicoes.pdf) | Quem fez cada parte do trabalho. |
