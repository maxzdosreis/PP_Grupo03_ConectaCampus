# Frontend — interface do Conecta Campus

Aplicação React 19.3 + TypeScript 6.0, com Vite 8.3 e React Router 8.4, rodando no serviço `frontend` do Docker Compose (Node 24) em http://localhost:5173. Testes com Vitest 5, Testing Library 16 e jsdom 30 (só desenvolvimento); lint com ESLint 10. Fala com a API pelo endereço de `VITE_API_URL`, que o Compose monta a partir de `BACKEND_PORT_HOST` ([variáveis derivadas](../README.md#derivadas-pelo-compose-a-partir-das-portas)). Não tem regra de negócio: mostra o que a API devolve e envia o que a pessoa digitou.

## Pastas de `src/`

| Pasta ou arquivo | Papel |
|---|---|
| `main.tsx`, `App.tsx` | Entrada e rotas (`MensagensProvider` > `BrowserRouter` > `SessaoProvider` > rotas). |
| `navegacao.ts` | Itens do menu (com `exigeLogin`) e os caminhos das telas, montados num lugar só (`caminhoParaReservar`, `caminhoDaReserva`, `proximoSeguro` etc.). |
| `formatacao.ts` | Datas e horários para exibição, por texto, sem `new Date("AAAA-MM-DD")` (que leria a data em UTC e poderia mostrar o dia anterior no Brasil). |
| `api/` | Cliente HTTP (`cliente.ts`), sessão (`sessao.ts`) e uma função por endpoint (`autenticacao.ts`, `espacos.ts`, `reservas.ts`, `saude.ts`), com os tipos das respostas; `erros.ts` extrai a mensagem e os erros de cada campo. |
| `pages/` | Uma página por rota (`PaginaInicial`, `PaginaEntrar`, `PaginaCadastro`, `PaginaEspacos`, `PaginaReservas`, `PaginaNovaReserva`, `PaginaReserva`, `PaginaNaoEncontrada`). |
| `components/` | Componentes por assunto: `layout/` (cabeçalho, menu, área do usuário), `sessao/` (provider, rota protegida, formulários de entrar e de cadastro), `mensagens/` (toasts e `Aviso`), `estados/` (carregando, vazio, falha), `formulario/` (`Campo`), `dialogo/`, `etiqueta/`, `espacos/` e `reservas/`. Estilos em `<Componente>.module.css`; testes em `*.test.ts(x)` ao lado. |
| `hooks/` | `useConsulta` (carregar com carregando, sucesso e erro), `useEnvio` (enviar formulário e separar erros de campo e gerais), foco depois de erro ou recarga, `useSessao`, `useMensagens`, `useTituloDaPagina`, `useValorAtrasado`. |
| `testes/`, `configuracaoDosTestes.ts` | Só para os testes: renderizar com sessão controlada, usuários de teste, limpeza e o polyfill do `<dialog>` no jsdom. |
| `index.css` | Tokens de cor (contraste AA), espaçamentos, fontes, foco visível e movimento reduzido. |

## Rotas e telas

| Rota | Tela | Quem acessa |
|---|---|---|
| `/` | Página inicial | qualquer pessoa |
| `/entrar` | Entrar | qualquer pessoa (com sessão, vai direto para o destino) |
| `/cadastro` | Criar conta | qualquer pessoa |
| `/espacos` | Espaços | logado; formulário e ações de gestão só para o Gestor |
| `/reservas` | Reservas ("Minhas reservas" para o Solicitante) | logado |
| `/reservas/nova` | Nova reserva | logado |
| `/reservas/:reservaId` | Detalhe da reserva | logado (Solicitante: só as próprias) |
| qualquer outra | Página não encontrada | qualquer pessoa |

As rotas que exigem login ficam dentro de `RotaProtegida`: sem sessão, a pessoa vai para `/entrar?proximo=<tela pedida>` e volta para ela depois do login. O `proximo` só é aceito se for um caminho do próprio site.

- Aplicação (frontend): http://localhost:5173 — a página inicial mostra a situação da API ("API no ar.") e os atalhos "Entrar" e "Criar conta" (ou "Ir para minhas reservas", com login).
- Entrar: http://localhost:5173/entrar (ou "Entrar" no cabeçalho) — com o e-mail e a senha de um dos [usuários de exemplo](../../README.md#dados-de-exemplo). Espaços e reservas exigem login: quem abre uma dessas telas sem login vai para a tela de entrar e volta para ela depois. O login continua valendo ao recarregar a página e em abas novas, e o token é renovado sozinho enquanto o refresh for válido (1 dia desde o login). O cabeçalho mostra quem está logado ("Nome · Perfil") e o botão "Sair", que encerra a sessão também na API: depois de sair, aquele login não renova mais.
- Criar conta: http://localhost:5173/cadastro (ou "Cadastre-se" no cabeçalho) — cadastrar um solicitante com nome, matrícula, e-mail e senha; a conta já entra sozinha e abre a tela de nova reserva.
- Tela de espaços: http://localhost:5173/espacos (ou o item "Espaços" do menu) — listar os espaços, com filtro por tipo e "Somente ativos"; o formulário de cadastro aparece só para o Gestor. Os filtros ficam no endereço da página, então recarregar mantém o filtro. Para o Gestor, cada linha também tem "Editar" (diálogo com os campos preenchidos, que envia só o que mudou) e "Desativar" ou "Reativar" (diálogo de confirmação; desativar avisa que novas reservas ficam bloqueadas e as existentes continuam valendo). O Solicitante vê o aviso "Somente o gestor cadastra espaços." e só o link "Reservar".
- Tela de nova reserva: http://localhost:5173/reservas/nova (ou o item "Nova reserva" do menu, ou o link "Reservar" de um espaço ativo na tela de espaços, que já traz o espaço selecionado) — mostra quem está solicitando (nome e matrícula), solicitar uma reserva e ver o resumo com a situação "Solicitada". Acima da data, uma dica com as regras de agenda vindas da API; depois de escolher espaço e data, a **agenda do dia** mostra os horários ocupados (só horário e situação, sem dizer de quem) e as janelas livres, cada uma com "Usar este horário", que preenche início e término. A agenda é só ajuda: quem decide é a API ao enviar, e depois de um conflito ela é recarregada.
- Tela de consulta de reservas: http://localhost:5173/reservas (ou o item "Reservas" do menu, ou o link "Ver minhas reservas" do resumo de uma reserva solicitada) — listar as reservas com filtros por espaço, situação, data, solicitante (nome ou matrícula) e "Somente minhas reservas", que se combinam. O Gestor vê todas. O Solicitante vê só as próprias, e para ele a tela (e o item do menu) se chama "Minhas reservas", sem os filtros de solicitante e "Somente minhas reservas", que não mudariam nada. Os filtros ficam no endereço da página; por exemplo, dois critérios combinados: http://localhost:5173/reservas?espaco=1&situacao=SOLICITADA.
- Detalhe de uma reserva: clicar na data e horário de uma linha da lista (ou em "Ver reserva", no resumo de uma reserva recém-solicitada) abre http://localhost:5173/reservas/ID — os dados da reserva, os mesmos botões de ação da lista e a **linha do tempo do histórico**: a criação e cada mudança de situação, com data e hora, quem fez e o motivo. Depois de uma ação, a reserva e a linha do tempo são recarregadas. "Voltar para as reservas" devolve à lista com os mesmos filtros de antes. Uma reserva que não existe, ou de outra pessoa para um Solicitante, aparece como "Reserva não encontrada".
- Alterar a situação de uma reserva, na mesma tela: cada linha tem um botão para cada mudança permitida a partir da situação atual e ao perfil de quem está logado (para o Gestor, uma solicitada mostra "Confirmar", "Recusar" e "Cancelar" e uma confirmada, "Cancelar" e "Concluir"; o Solicitante só vê "Cancelar" nas próprias; as concluídas, recusadas e canceladas não têm ações). O botão abre um diálogo com o resumo da reserva; para recusar ou cancelar, ele pede o motivo, que o solicitante verá. Confirme no botão do diálogo (ex.: "Recusar reserva") ou feche com "Voltar" ou Esc sem alterar nada. Depois da mudança, a mensagem aparece no canto da tela e a lista é recarregada. Se outra pessoa já tiver mudado a reserva, o diálogo explica o motivo e oferece "Atualizar lista". As ações disponíveis vêm da API (`acoes_disponiveis` em cada reserva).

## Cliente da API e sessão

- **`api/cliente.ts`** — `requisitar(caminho, { autenticar = true, ... })` monta a URL a partir de `VITE_API_URL`, envia `Authorization: Bearer <access>` quando há sessão e transforma toda resposta de erro em `ErroDaApi` (status, código, mensagem e `campos`).
- **Renovação automática:** um 401 `NAO_AUTENTICADO` numa requisição que levou token chama `POST /api/auth/refresh/` uma vez e repete a requisição uma vez. Requisições que recebem 401 ao mesmo tempo esperam a mesma renovação. A renovação devolve um `access` e um `refresh` novos, e os dois vão para a sessão (`atualizarTokens`, motivo `atualizacao`): o `refresh` é de uso único e o enviado deixa de valer. Se o refresh for recusado (ou a repetição voltar 401), a sessão é encerrada com "Sua sessão expirou. Faça login novamente." e a pessoa vai para a tela de entrar.
- **Duas abas:** as abas dividem a sessão no `localStorage`, então a renovação de uma troca o `refresh` da outra. Quando o refresh é recusado, o cliente relê a sessão: se o `refresh` guardado já é outro, outra aba renovou, e a requisição é repetida uma vez com o `access` dela, sem deslogar. Se ainda é o mesmo, espera até `ESPERA_PELA_OUTRA_ABA_MS` (1 s) pelo evento `storage` da outra aba (`aguardarSessaoDeOutraAba`), porque as duas podem ter renovado ao mesmo tempo e a resposta da outra ainda não ter sido gravada; só sem nenhuma sessão nova a sessão termina, com o motivo `expiracao`. Dentro de uma aba, a renovação continua sendo uma só. Sem conexão ou erro do servidor no refresh não encerram a sessão. Login, cadastro, refresh e logout usam `autenticar: false`.
- **`api/sessao.ts`** — único módulo que toca o armazenamento. A sessão (`access`, `refresh` e `usuario`) fica no `localStorage`, na chave `conecta-campus:sessao`, para sobreviver ao recarregar e a abas novas. Um valor corrompido é lido como "sem sessão"; se o navegador recusar o `localStorage` (navegação privada), a sessão fica em memória até recarregar. O risco disso está nas [limitações conhecidas](../../README.md#limitações-conhecidas).
- **`SessaoProvider`** (`components/sessao/`) — expõe `usuario`, `verificando`, `autenticado`, `ehGestor`, `entrar`, `cadastrarEEntrar` e `sair` (por `useSessao`). Ao abrir com sessão salva, confere o usuário em `GET /api/auth/me/`. Depois do cadastro, faz o login com as mesmas credenciais. `sair` dispara `POST /api/auth/logout/` com o `refresh` da sessão **sem esperar a resposta** e limpa a sessão na hora, com o aviso "Você saiu da sua conta."; se a API estiver fora do ar, a saída funciona igual, só com um `console.warn`. O `access` não é revogado e vale até expirar (30 minutos).
- **Perfil é só conveniência:** a tela usa `usuario.eh_gestor`, vindo da API, para esconder o que o Solicitante não pode fazer. Quem garante as permissões é a API (403).

## Convenções

- **Sem regra de negócio no navegador.** Formulários com `noValidate`, sem `required`, `maxLength`, `min`, `max`, `pattern` nem `step`; os valores vão como foram digitados, e as mensagens exibidas são sempre as da API: erro de um campo embaixo do campo (`Campo`, com `aria-describedby` e `aria-invalid`), erro geral num `Aviso` no topo do formulário, que recebe o foco.
- **Vocabulário vem da API:** tipos de espaço (`GET /api/espacos/tipos/`), situações (`GET /api/reservas/situacoes/`), regras de agenda e as ações de cada reserva (`acoes_disponiveis`). Nenhuma lista nem tabela de transições é copiada no frontend.
- **Filtros na URL** (`useSearchParams` com `replace`), nas telas de espaços e de reservas: recarregar ou voltar mantém o filtro. O texto do solicitante só vai para a URL depois que a pessoa para de digitar (400 ms).
- **Mensagens:** resultado de uma ação (cadastrou, alterou, falhou) vira toast com a mensagem da API (`useMensagens`; o sucesso some sozinho, o erro fica até fechar, no máximo 3 na tela). Estado da página e erros de carregamento usam `Aviso`, `Carregando`, `EstadoVazio` e `FalhaAoCarregar` ("Tentar novamente").
- **Ações irreversíveis pedem confirmação** num `<dialog>` (`Dialogo`), com o foco inicial em "Voltar" (ou no campo Motivo, quando a ação pede motivo, ou no Nome, na edição de espaço) e Esc para fechar.
- **Acessibilidade:** etiquetas com texto (nunca só cor), tabelas com `caption` e rolagem horizontal focável, nomes acessíveis com contexto nos botões de cada linha, foco devolvido depois de fechar diálogos e de recarregar listas.

## Comandos

Com os serviços no ar, dentro de `src`. O servidor de desenvolvimento (`npm run dev`, com recarga automática) já sobe com o `docker compose up`.

```bash
docker compose exec frontend npm run lint
```

Testes (Vitest e Testing Library, em jsdom):

```bash
docker compose exec frontend npm test -- --run
```

```bash
docker compose exec frontend npm run build
```

As dependências do frontend ficam num volume próprio do container (`/app/node_modules`). Ao mudar o `package.json` (instalar, remover ou atualizar pacotes), recrie esse volume:

```bash
docker compose up --build -V frontend
```

Instale pacotes dentro do container (`docker compose run --rm --no-deps frontend npm install -D <pacote>`), para o `package-lock.json` sair do Linux: o Dockerfile roda `npm ci`, que exige o lock.

## Onde mexer

| Para mudar… | Arquivo |
|---|---|
| Uma rota ou item do menu | `App.tsx` e `navegacao.ts` (cada tela nova acrescenta o seu item) |
| Uma chamada à API | `api/<assunto>.ts` |
| Login, renovação e sessão | `api/cliente.ts`, `api/sessao.ts`, `components/sessao/SessaoProvider.tsx` |
| Uma tela | `pages/Pagina<Nome>.tsx` e os componentes de `components/<assunto>/` |
