# Verificação de responsividade e acessibilidade (RNF-U02 a RNF-U05)

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **VER-01 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: a definir • Aprovador: a definir | `docs/fontes/requisitos/verificacoes/FE-08-usabilidade.md` |

Resultado da verificação dos [RNF-U02](../requisitos/rnf.md#rnf-u02), [RNF-U03](../requisitos/rnf.md#rnf-u03), [RNF-U04](../requisitos/rnf.md#rnf-u04) e [RNF-U05](../requisitos/rnf.md#rnf-u05) (tarefa FE-08), feita em 19/11/2026, antes da baseline 1.0. Cada RNF fica com a evidência que o repositório reproduz (testes do Vitest) ou com o roteiro e o resultado registrados aqui. O que não foi verificado está dito na [seção 7](#7-o-que-não-foi-verificado) e na lacuna [L-09](../requisitos/srs.md#l-09).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 19/11/2026 | Max Zimmermann dos Reis | Criação: verificação automática (axe no jsdom e contraste calculado), roteiro no navegador (larguras, teclado e foco, cinza), correções feitas e o que ficou sem verificar (FE-08). Sem aprovação. |

## 1. Ambiente e ferramentas

| Item | Valor |
|---|---|
| Aplicação | `docker compose up` (fluxo do README da raiz), frontend em `http://localhost:5173` e API em `http://localhost:8000`, com os dados de exemplo (`carregar_dados_exemplo`) |
| Computador | Windows 10, Docker Desktop com 4 CPUs para os containers |
| Testes automáticos | Vitest 5 + Testing Library 16 + jsdom 30 (container `frontend`, `node:24-alpine`); `axe-core` 4.14.1 (dependência de desenvolvimento, versão fixa) |
| Navegador | Chromium 156.0.8078.100 (navegador embutido do aplicativo de desenvolvimento do grupo), com emulação de tamanho de tela; abaixo de 768 px a emulação é de celular (toque e viewport móvel) |
| Larguras | 320 × 640, 360 × 640 (a do RNF-U02), 768 × 1024, 1280 × 800 e 640 × 400 (equivale a 1280 px com zoom de 200%) |
| Contas | as de exemplo do README da raiz: Carla Mendes (Gestor) e Bruno Lima (Solicitante) |

O roteiro do navegador foi rodado por um script descartável (não versionado) que mede pelo próprio navegador: `document.documentElement.scrollWidth` × largura útil, elementos fora da tela que não estão dentro de uma área com rolagem própria, textos cortados, alvos menores que 24 × 24 px e alvos sobrepostos; para o teclado, um ouvinte de `focusin` registra cada parada do Tab, se o contorno de foco está desenhado e os controles que nenhum Tab alcançou. Para repetir à mão: [seção 8](#8-como-repetir).

## 2. Verificação automática no jsdom (axe)

`src/acessibilidade.test.tsx` renderiza as telas pelas rotas de verdade (`RotasDaAplicacao`, com o `Layout`), com a API simulada como nos outros testes, e roda o axe em cada estado. A regra `color-contrast` fica desligada **só nesse teste**, porque o jsdom não calcula estilo nem layout; o contraste está na [seção 4](#4-contraste-calculado-rnf-u04). Nenhuma outra regra foi desligada.

| Tela | Estados verificados | Violações |
|---|---|---|
| `/` | carregada (visitante), carregando, API fora do ar | 0 |
| `/entrar` | vazia, erro de campo, erro geral da API (401) | 0 |
| `/cadastro` | vazia, erros de campo (senha e matrícula) | 0 |
| `/conta` | vazia, erro de campo da API | 0 |
| `/espacos` (Gestor) | carregada com formulário, filtros e ações; carregando; vazia; falha ao carregar; erro de campo no cadastro; diálogos de edição e de desativação abertos | 0 |
| `/espacos` (Solicitante) | carregada | 0 |
| `/reservas/nova` | com a dica e a agenda do dia; erro da API (409 de conflito); erro de campo; sem espaços ativos | 0 |
| `/reservas` (Gestor) | com filtros e ações; carregando; vazia com filtro; falha ao carregar; diálogo de recusa com o campo de motivo | 0 |
| `/reservas` (Solicitante, "Minhas reservas") | carregada | 0 |
| `/reservas/:reservaId` | linha do tempo com mudança aceita e tentativa recusada; diálogo de confirmação; não encontrada | 0 |
| `/usuarios` | com filtros e ações; vazia; diálogo de desativação | 0 |
| página não encontrada | carregada | 0 |

**O teste detecta violações reais:** um teste descartável com um `<input>` sem rótulo e um `<button>` vazio falhou com `label (critical): Form elements must have labels` e `button-name (critical): Buttons must have discernible text`; depois foi apagado. O mesmo arquivo confere o `index.html` (`lang="pt-BR"`, `viewport` sem bloqueio de zoom e `<title>`) e, para o RNF-U05, que situação, estado do espaço, tipo de aviso e tentativa recusada aparecem como texto.

## 3. Navegador real: larguras (RNF-U02)

Resultado depois das correções da [seção 5](#5-correções-feitas). "Ok" = sem rolagem horizontal da página (`scrollWidth` igual à largura útil), nada fora da tela fora de uma área com rolagem própria, nenhum texto cortado e nenhum alvo sobreposto.

| Tela | 320 | 360 | 768 | 1280 | 640 (zoom 200%) |
|---|---|---|---|---|---|
| `/` (visitante e logado) | ok | ok | ok | ok | — |
| `/entrar` | ok | — | — | — | — |
| `/cadastro` | ok | — | — | — | — |
| `/conta` | ok | ok | ok | ok | — |
| `/espacos` (Gestor e Solicitante) | ok | ok | ok | ok | ok |
| `/reservas` (Gestor e Solicitante) | ok (antes da correção: **rolagem**, 1003 px) | ok | ok | ok | ok |
| `/reservas/nova` | ok | ok | ok | ok | ok |
| `/reservas/:reservaId` (Gestor e Solicitante) | ok | ok | ok | ok | — |
| `/usuarios` | ok | ok | ok | ok | ok |

- As três tabelas (espaços, reservas, usuários) rolam dentro da própria região (`role="region"`, `tabindex="0"`, alcançada pelo Tab), com a contagem da API como legenda.
- **Alvos de toque (WCAG 2.5.8, 24 × 24 px):** depois da correção, os únicos alvos menores são links de texto com 21 px de altura ("Ver detalhes" da data na tabela, "Voltar para as reservas", "Cadastre-se" e "Entrar" dentro de frases). Todos atendem pela exceção de espaçamento: o vizinho mais próximo fica a 56 a 77 px do centro (o mínimo é 12). Os links dentro de frases também atendem pela exceção de texto.
- A meta `viewport` é `width=device-width, initial-scale=1.0`, sem `user-scalable=no` nem `maximum-scale` (o zoom não é bloqueado).
- 200% foi verificado pela largura equivalente (640 px de área útil); o zoom do navegador em si não foi acionado.

## 4. Contraste calculado (RNF-U04)

`src/contraste.test.ts` lê as cores do `index.css` (os tokens `--cor-*`) e o foco branco do cabeçalho em `Layout.module.css`, compõe as cores translúcidas sobre o fundo em que aparecem e calcula a razão pela fórmula da WCAG 2.1 (conferida com os valores de referência 21:1, 1:1 e 4,54:1). Duas guardas fazem o teste falhar se um módulo CSS passar a usar como texto ou como fundo um token que nenhum par confere.

**Texto (mínimo 4,5:1)**

| Frente × fundo | Onde | Razão |
|---|---|---|
| texto × fundo | corpo da página | 13,75 |
| texto × superfície | cartões, formulários, tabelas, diálogos, campos | 14,76 |
| texto × fundo de sucesso / de erro / informativo | avisos e toasts | 14,10 / 13,49 / 13,56 |
| texto-suave × fundo | cabeçalho das tabelas, etiqueta neutra, agenda | 6,02 |
| texto-suave × superfície | dicas, legendas, rodapé, carregando, vazio | 6,46 |
| texto-suave × fundos de sucesso / erro / informativo | "×" dos avisos | 6,17 / 5,90 / 5,93 |
| texto × fundos dos avisos com 8% de tinta | "×" sob o mouse | 11,99 / 11,48 / 11,54 |
| primária × fundo / superfície | links, botões secundários | 6,24 / 6,70 |
| sobre-primária × primária | botões primários, "Pular para o conteúdo" | 6,70 |
| sobre-primária × primária-escura | cabeçalho, botões sob o mouse | 10,36 |
| sobre-primária × primária-escura com 15% de branco | "Sair" sob o mouse | 6,83 |
| sucesso × fundo de sucesso | etiqueta (Confirmada, Ativo, Concluída) — **menor par** | 4,79 |
| aviso × fundo de aviso | etiqueta (Solicitada) | 6,84 |
| erro × fundo de erro | etiqueta (Recusada, Cancelada, Inativo) | 5,91 |
| erro × superfície / fundo | mensagem de erro do campo | 6,47 / 6,03 |
| sobre-primária × erro / sucesso | marcadores "!" e "✓" | 6,47 / 5,02 |

**Bordas, foco e indicadores de controles (mínimo 3:1)**

| Frente × fundo | Onde | Razão |
|---|---|---|
| borda forte × superfície / fundo | borda dos campos | 3,66 / 3,41 |
| erro × superfície | borda do campo com erro | 6,47 |
| primária × superfície / fundo | botões, caixas de marcar | 6,70 / 6,24 |
| foco × superfície / fundo | contorno de foco | 6,70 / 6,24 |
| branco × primária-escura / primária | contorno de foco no cabeçalho e em "Pular para o conteúdo"; borda de "Sair" e traço do item ativo | 10,36 / 6,70 |

Isentos, com o motivo: `--cor-borda` (separadores e contornos de cartões, tabelas e avisos, que são decoração, e o fundo da faixa da agenda e do traço da linha do tempo, decorativos); botões desabilitados (opacidade 0,6; a WCAG 1.4.3 exclui componentes inativos). No navegador, o contorno de foco aparece na cor de foco nas capturas de tela; o `getComputedStyle` desse Chromium informa a cor do texto para o contorno, então a cor foi conferida pela imagem e o contraste pelo cálculo acima.

## 5. Correções feitas

| Problema encontrado | Tela | Antes | Depois |
|---|---|---|---|
| Rolagem horizontal da página inteira em telas estreitas | `/reservas` do Gestor (linhas sem ação, com o texto "Nenhuma ação disponível" só para leitor de tela) | a 320 px, a página media 1003 px de largura: o texto escondido (`position: absolute`) escapava da área de rolagem da tabela, que não era posicionada | `.rolagem { position: relative }` nas três tabelas (`TabelaDeReservas`, `TabelaDeEspacos`, `TabelaDeUsuarios`): 320 px |
| Caixas de marcar menores que 24 × 24 px | filtros de `/espacos`, `/reservas` e `/usuarios` ("Somente ativos", "Somente minhas reservas" e o de usuários) | 18 × 18 px | 24 × 24 px (`1.5rem` nos três módulos de filtros) |
| Foco perdido ao trocar de tela quando o elemento com o foco some | depois de entrar (ida para `/reservas`), de sair (ida para `/`) e ao seguir um link de dentro do conteúdo | o foco caía no `<body>`, e o próximo Tab recomeçava do topo sem nada anunciado | o `Layout` põe o foco no `<main id="conteudo">` quando a tela muda e o foco está no `<body>`; não age na primeira carga nem tira o foco que a própria tela pôs (testes em `Layout.test.tsx`) |

Nenhum texto, rótulo ou mensagem mudou; nenhum CA ou TA cita o que foi alterado.

## 6. Navegador real: teclado e foco (RNF-U03)

Só Tab, Shift+Tab, Enter, Espaço, setas e Esc. Em todas as telas, num ciclo completo de Tab, **nenhum controle ficou sem ser alcançado, o contorno de foco esteve desenhado em todas as paradas e o ciclo sai da página e volta ao começo (sem armadilha)**.

| Tela | Ordem do foco | Operação feita só com o teclado |
|---|---|---|
| `/entrar` | pular → cabeçalho → e-mail → senha → Entrar → Cadastre-se | entrar como Gestor e como Solicitante (Enter no formulário); o erro 503 de um Redis lento apareceu no aviso do topo, que recebeu o foco |
| `/espacos` (Gestor) | pular → cabeçalho → cadastro → filtros → região da tabela → ações de cada linha | cadastrar vazio (erro no campo, que recebe o foco); abrir edição (Enter) e desativação (Espaço); enviar a edição sem mudança (aviso no topo do diálogo, com o foco) |
| `/espacos` (Solicitante) | igual, sem cadastro e só "Reservar" | — |
| `/reservas` (Gestor) | filtros → região → data (link) e ações de cada linha | trocar a situação do filtro com a seta (a URL e a lista mudam, o foco fica no filtro); "Pular para o conteúdo" leva o foco ao `<main>` |
| `/reservas` (Solicitante) | igual, sem os filtros de solicitante | — |
| `/reservas/nova` | espaço → data → agenda → início → término → finalidade → Solicitar | espaço pela seta, data pelos dígitos, "Usar este horário" (preenche início e término e foca o término), enviar sem finalidade (erro no campo, com o foco) |
| `/reservas/:reservaId` | voltar → ações | abrir "Confirmar" (foco em "Voltar"); como Solicitante, "Cancelar" com o motivo vazio (foco no Motivo; o erro do domínio aparece nele) |
| `/usuarios` | busca → filtros → região → ações | abrir "Desativar" (foco em "Voltar"); as duas ações da própria conta do Gestor ficam desabilitadas, com o motivo em texto na linha |
| `/conta` | senha atual → nova → confirmação → Alterar senha | enviar vazio (erro no primeiro campo, com o foco) |
| Cabeçalho | — | trocar de tela pelo menu com Enter (o título da aba muda e o item fica `aria-current="page"`); sair com Enter (foco no `<main>`, aviso anunciado na região `polite`) |

**Diálogos** (edição e desativação de espaço, confirmação e cancelamento de reserva, desativação de usuário): todos abrem como modais (`:modal`, o resto da página inerte); o foco inicial vai para o primeiro campo, para o Motivo ou para "Voltar"; Tab e Shift+Tab circulam só dentro do diálogo; Esc fecha sem chamar a API e devolve o foco ao botão que abriu, em 5 de 5.

**Título por tela:** `document.title` muda em toda troca ("Espaços · Conecta Campus", "Minhas reservas · Conecta Campus", "Reserva de 31/10/2026 · Conecta Campus" etc.).

**Mensagens anunciadas:** avisos de erro com `role="alert"`, de estado com `role="status"`; toasts em duas regiões (`aria-live="polite"` para sucesso e `assertive` para erro); a agenda do dia anuncia a mensagem da API numa região `polite`.

**Cinza (RNF-U05):** a tela de reservas foi vista com `filter: grayscale(1)`: cada situação continua legível como texto (Concluída, Solicitada, Recusada, Cancelada), com o motivo embaixo; a linha do tempo marca a tentativa recusada com o texto "Tentativa recusada:" (o ícone ⚠ é decorativo).

## 7. O que não foi verificado

- **Leitor de tela real** (NVDA, JAWS, VoiceOver, TalkBack): não foi usado. Os nomes acessíveis foram conferidos pelo axe no jsdom e pelos nomes registrados em cada parada do Tab; a árvore de acessibilidade do navegador não foi lida.
- **Operações que gravam, até o fim, pelo teclado:** para não alterar os dados de exemplo, cadastrar, editar, desativar e reativar espaço, solicitar, confirmar, recusar, cancelar e concluir reserva, trocar a senha e alterar usuário foram levadas pelo teclado até o envio e a resposta de recusa da API (ou até o diálogo de confirmação), mas não até o sucesso. O envio usa o mesmo botão e o mesmo Enter nos dois casos. Fica para o ensaio da demonstração (L-09).
- **Outros navegadores e aparelhos:** só o Chromium, com emulação de celular; nenhum celular de verdade, Firefox nem Safari.
- **Zoom do navegador:** 200% foi simulado pela largura de 640 px; o zoom de texto (só fonte) não foi testado.

## 8. Como repetir

- **Automático:** `docker compose exec frontend npx vitest --run src/acessibilidade.test.tsx src/contraste.test.ts` (a partir de `src/`).
- **Larguras:** com a aplicação no ar e os dados de exemplo, abrir cada tela nas ferramentas do navegador (modo de dispositivo) a 320, 360, 768 e 1280 px e conferir no console que `document.documentElement.scrollWidth <= document.documentElement.clientWidth`.
- **Teclado:** percorrer cada tela só com Tab e Shift+Tab, abrir cada diálogo com Enter, circular dentro dele e fechar com Esc, conferindo que o foco volta ao botão; para registrar as paradas, rodar no console `document.addEventListener('focusin', e => console.log(e.target))` antes do primeiro Tab.
- **Cinza:** no console, `document.documentElement.style.filter = 'grayscale(1)'`.
