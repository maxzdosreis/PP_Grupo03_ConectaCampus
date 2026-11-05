# UC-02 · Autenticar

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **UC-02 • 0.1 • Rascunho** (ficha completa, formato Cockburn) | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/casos-de-uso/UC-02-autenticar.md` |

Ficha do caso de uso UC-02 do [índice](README.md#uc-02). Autenticar é a precondição de todos os casos de uso do Solicitante e do Gestor ([decisão d](README.md#decisao-d)); a sessão (continuar identificado, confirmar a identificação ao voltar, sair) faz parte dele ([decisão a](README.md#decisao-a)). Como ler a numeração: [decisões h e i](README.md#decisao-h).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Criação: fluxo principal, alternativas da sessão, exceções, garantias, RF cobertos e evidência (REQ-04). Sem aprovação. |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Linha "Histórias derivadas" (REQ-05), sem mudar o fluxo. Sem aprovação. |

## Sumário

1. [Identificação do caso de uso](#identificação-do-caso-de-uso)
2. [Stakeholders e interesses](#stakeholders-e-interesses)
3. [Fluxo principal](#fluxo-principal)
4. [Alternativas](#alternativas)
5. [Exceções](#exceções)
6. [Pós-condições e garantias](#pós-condições-e-garantias)
7. [Regras de negócio](#regras-de-negócio)
8. [RFs cobertos](#rfs-cobertos)
9. [RNFs relacionados](#rnfs-relacionados)
10. [Questões em aberto](#questões-em-aberto)
11. [Anexo — Evidência (complementar)](#anexo--evidência-complementar)

## Identificação do caso de uso

| Campo | Conteúdo |
|---|---|
| **Escopo** | Conecta Campus (caixa-preta). |
| **Nível** | Objetivo do usuário. |
| **Ator primário** | [Visitante](../glossario.md#visitante) com conta: depois do passo 4, ele é um [usuário autenticado](../glossario.md#usuario-autenticado) com o perfil Solicitante ou Gestor. |
| **Atores secundários** | Nenhum ([decisão f](README.md#decisao-f)). |
| **Meta de contexto** | Ser identificado pelo sistema para agir com o próprio [perfil](../glossario.md#perfil) — pedir, acompanhar ou decidir sobre reservas —, continuar identificado enquanto a [sessão](../glossario.md#sessao) valer e deixar de sê-lo ao sair. |
| **Precondições** | O visitante tem uma conta ativa: cadastrou-se ([UC-01](fichas-resumidas.md#uc-01)) ou teve a conta criada pela Equipe de TI ([UC-20](fichas-resumidas.md#uc-20)). |
| **Disparador** | O visitante quer usar algo que exige identificação (pedir, acompanhar ou decidir sobre reservas, manter espaços), ou o sistema o leva a se identificar ao tentar algo assim. |

## Stakeholders e interesses

| Stakeholder | Interesse neste caso de uso |
|---|---|
| **Solicitante** | Entrar sem atrito, com o e-mail e a senha de sempre; não precisar informar a senha de novo durante o uso do dia; ser levado de volta ao que estava fazendo; sair num computador compartilhado sem que a próxima pessoa aja em nome dele. |
| **Gestor** | O mesmo, e ter o perfil Gestor reconhecido logo ao entrar, para ver as ações de decisão; perder o perfil na hora se a Equipe de TI o retirar. |
| **Cliente** (instituição) | Só quem tem autoridade decide sobre os pedidos; saber quem pediu e quem decidiu cada reserva; que uma tentativa de entrada não revele quais e-mails estão cadastrados; que uma conta desativada perca o acesso na hora. |

## Fluxo principal

1. <a id="p1"></a>O Visitante pede para entrar.
2. <a id="p2"></a>O Visitante informa o e-mail e a senha.
3. <a id="p3"></a>O sistema confere que os dois foram informados, que o e-mail está num formato válido (sem diferenciar maiúsculas de minúsculas e sem espaços nas pontas) e que o e-mail e a senha são de uma conta ativa.
4. <a id="p4"></a>O sistema inicia a sessão, informa "Login realizado com sucesso." e passa a mostrar quem está identificado, pelo nome e pelo perfil (por exemplo, "«nome» · Gestor"); o usuário segue para onde queria ir ou, sem destino, para as próprias reservas.

## Alternativas

A meta ainda é alcançada.

#### <a id="a1-1"></a>A1.1 · Entrar a partir de algo que exige identificação

No passo 1, o visitante tentou usar algo que exige identificação. O sistema o leva a entrar e, depois do passo 4, de volta ao ponto em que estava, com os mesmos critérios. O destino só é aceito se for do próprio sistema; senão, ele segue para as próprias reservas.

#### <a id="a1-2"></a>A1.2 · Ainda não tem conta

No passo 1, o visitante ainda não tem conta. Ele segue em [UC-01 Cadastrar-se](fichas-resumidas.md#uc-01), que termina com ele já identificado como Solicitante, sem repetir este caso de uso.

#### <a id="a4-1"></a>A4.1 · Continuar identificado

Depois do passo 4, o usuário continua usando o sistema, inclusive depois de recarregar ou de abrir o sistema de novo em outra janela do mesmo navegador. Enquanto a sessão valer (1 dia desde a entrada), o sistema o mantém identificado sem pedir a senha e renova a credencial de acesso, que vale 30 minutos, sem que ele perceba. Se várias operações precisarem da renovação ao mesmo tempo, ela acontece uma vez só.

#### <a id="a4-2"></a>A4.2 · Confirmar a identificação ao voltar

Quando o usuário volta ao sistema com uma sessão guardada, o sistema confere os dados atuais da conta (nome, e-mail, matrícula e perfil) e passa a mostrá-los. Se a Equipe de TI mudou o perfil, vale o novo, inclusive para as permissões, já na próxima operação. Se a conferência não puder ser feita por falta de conexão, a sessão guardada continua valendo.

#### <a id="a4-3"></a>A4.3 · Sair

Em qualquer momento depois do passo 4, o usuário pede para sair. O sistema encerra a identificação neste navegador, informa "Você saiu da sua conta." e mostra a página inicial sem nenhuma identificação. A credencial já emitida não é invalidada fora deste navegador ([lacuna L-04](../requisitos/srs.md#l-04)).

## Exceções

A meta é interrompida: **nenhuma sessão é iniciada ou mantida**.

#### <a id="e3-1"></a>E3.1 · E-mail ou senha não informados, ou e-mail mal formado

- **Condição:** no passo 3, falta o e-mail ou a senha, ou o e-mail não está num formato de e-mail.
- **Resultado para o ator:** "Verifique os dados informados.", com a indicação, junto a cada dado, do que falta ou está mal formado. As credenciais nem são conferidas.
- **Estado depois:** nenhuma sessão é iniciada; nada na conta muda.
- **Requisito:** nenhum RF descreve esta recusa ([lacuna L-14](../requisitos/srs.md#l-14)); é a forma de [RF-33](../requisitos/rf-contas.md#rf-33) recusar dados incompletos, com a mensagem de [RF-38](../requisitos/rf-gerais.md#rf-38).

#### <a id="e3-2"></a>E3.2 · Credenciais inválidas

- **Condição:** no passo 3, o e-mail não está cadastrado, a senha está errada ou a conta está desativada.
- **Resultado para o ator:** "E-mail ou senha incorretos." — a **mesma** resposta nos três casos, para não revelar quais e-mails existem. O visitante confere o e-mail e a senha e tenta de novo, ou se cadastra ([A1.2](#a1-2)).
- **Estado depois:** nenhuma sessão é iniciada; o último acesso da conta não muda.
- **Requisito:** [RF-33.1](../requisitos/rf-contas.md#rf-33-1) e [RNF-F05](../requisitos/rnf.md#rnf-f05).

#### <a id="e4-1"></a>E4.1 · Sessão expirada

- **Condição:** depois do passo 4, a sessão deixou de valer: passou 1 dia desde a entrada, ou a renovação da credencial foi recusada (credencial adulterada ou de outro sistema).
- **Resultado para o ator:** "Sua sessão expirou. Faça login novamente."; o sistema o leva a entrar de novo (volta ao passo 1) e, depois, ao ponto em que estava ([A1.1](#a1-1)). Falta de conexão durante a renovação não encerra a sessão: a próxima operação tenta renovar de novo.
- **Estado depois:** a sessão é encerrada neste navegador; nada do que a pessoa já tinha gravado muda, e a operação que estava em curso não é executada.
- **Requisito:** [RF-34.1](../requisitos/rf-contas.md#rf-34-1) e [RNF-F03](../requisitos/rnf.md#rnf-f03).

#### <a id="e4-2"></a>E4.2 · Conta desativada ou excluída durante a sessão

- **Condição:** depois do passo 4, a Equipe de TI desativa ou exclui a conta.
- **Resultado para o ator:** a próxima operação é recusada e a sessão termina como em [E4.1](#e4-1) ("Sua sessão expirou. Faça login novamente."); uma nova entrada cai em [E3.2](#e3-2).
- **Estado depois:** a conta perde o acesso na hora, mesmo com a credencial ainda dentro do prazo; nada é gravado em nome dela depois disso.
- **Requisito:** [RF-34.1](../requisitos/rf-contas.md#rf-34-1) e [RNF-F07](../requisitos/rnf.md#rnf-f07).

**Fora das exceções:** credenciais forjadas, adulteradas ou fora do padrão são tratadas como ausência de identificação ([RNF-F10](../requisitos/rnf.md#rnf-f10)); o perfil nunca vem do pedido, sempre da conta ([RNF-F09](../requisitos/rnf.md#rnf-f09)). Não há limite de tentativas de entrada ([lacuna L-03](../requisitos/srs.md#l-03)).

## Pós-condições e garantias

| Campo | Conteúdo |
|---|---|
| **Pós-condições (sucesso)** | Existe uma sessão para a conta neste navegador, válida por 1 dia; o último acesso da conta foi atualizado; todo caso de uso que o usuário iniciar a seguir o reconhece com o perfil atual da conta. Depois de [A4.3](#a4-3), não há sessão neste navegador. |
| **Garantia de sucesso** | O usuário age com o próprio nome, matrícula e perfil, que o sistema lê da conta (nunca do pedido) a cada operação. |
| **Garantia mínima** | Mesmo quando a meta falha: nenhuma sessão é iniciada; a resposta não revela se o e-mail existe; a senha não é mostrada e só é guardada como hash ([RNF-F01](../requisitos/rnf.md#rnf-f01)); uma conta desativada não age. |

## Regras de negócio

- [Usuário](../glossario.md#usuario), [usuário autenticado](../glossario.md#usuario-autenticado), [perfil](../glossario.md#perfil) (Solicitante | Gestor), [sessão](../glossario.md#sessao): credencial de acesso de 30 minutos e renovação de 1 dia ([DEC-04](../decisoes/DEC-04.md)).
- [Credenciais inválidas](../glossario.md#credenciais-invalidas): a mesma resposta para e-mail inexistente, senha errada e conta desativada.
- O e-mail é comparado sem diferenciar maiúsculas de minúsculas e sem espaços nas pontas.
- O perfil é relido da conta a cada operação; a interface só usa o perfil para mostrar o que a pessoa pode fazer, e quem garante é o sistema.

## RFs cobertos

Todos os RF que a [rastreabilidade RF → UC](README.md#rastreabilidade-rf--uc) atribui a UC-02.

| RF | Título | Onde entra nesta ficha |
|---|---|---|
| [RF-33](../requisitos/rf-contas.md#rf-33) | Entrar com e-mail e senha | fluxo principal, [passos 1 a 4](#p1) |
| [RF-33.1](../requisitos/rf-contas.md#rf-33-1) | Recusar credenciais inválidas | [E3.2](#e3-2) |
| [RF-34](../requisitos/rf-contas.md#rf-34) | Continuar identificado sem informar a senha de novo | [A4.1](#a4-1) |
| [RF-34.1](../requisitos/rf-contas.md#rf-34-1) | Encerrar a sessão expirada | [E4.1](#e4-1), [E4.2](#e4-2) |
| [RF-35](../requisitos/rf-contas.md#rf-35) | Consultar os próprios dados | [A4.2](#a4-2) |
| [RF-36](../requisitos/rf-contas.md#rf-36) | Sair | [A4.3](#a4-3) |

[RF-38](../requisitos/rf-gerais.md#rf-38) é transversal ([passo 4](#p4), [A4.3](#a4-3) e todas as exceções).

## RNFs relacionados

| RNF | Onde pesa nesta ficha |
|---|---|
| [RNF-F01](../requisitos/rnf.md#rnf-f01) · Senha guardada só como hash | garantia mínima |
| [RNF-F03](../requisitos/rnf.md#rnf-f03) · Validade da sessão | [A4.1](#a4-1), [E4.1](#e4-1) |
| [RNF-F04](../requisitos/rnf.md#rnf-f04) · Identificação obrigatória por padrão | disparador, [A1.1](#a1-1) |
| [RNF-F05](../requisitos/rnf.md#rnf-f05) · Credenciais inválidas não revelam contas | [E3.2](#e3-2) |
| [RNF-F07](../requisitos/rnf.md#rnf-f07) · Conta desativada perde o acesso na hora | [E4.2](#e4-2) |
| [RNF-F08](../requisitos/rnf.md#rnf-f08) · Perfil relido a cada operação | [A4.2](#a4-2) |
| [RNF-F09](../requisitos/rnf.md#rnf-f09) · Identidade e perfil nunca vêm do pedido | garantia de sucesso |
| [RNF-F10](../requisitos/rnf.md#rnf-f10) · Credenciais forjadas recusadas | [E4.1](#e4-1) |
| [RNF-U01](../requisitos/rnf.md#rnf-u01) · Mensagens em português que orientam a correção | todas as exceções |

## Questões em aberto

| DEC ou lacuna | Como afeta este caso de uso |
|---|---|
| [DEC-04](../decisoes/DEC-04.md) · Autenticação e perfis (decidida) | Fixa a validade da sessão e que o cadastro público nunca cria Gestor. |
| [DEC-09](../decisoes/DEC-09.md) · Formato da matrícula | A matrícula mostrada em [A4.2](#a4-2) não é conferida com a instituição. |
| [Lacuna L-03](../requisitos/srs.md#l-03) | Sem limite de tentativas em [E3.2](#e3-2). |
| [Lacuna L-04](../requisitos/srs.md#l-04) | Sair ([A4.3](#a4-3)) não invalida a credencial fora deste navegador. |
| [Lacuna L-14](../requisitos/srs.md#l-14) | A recusa de [E3.1](#e3-1) não tem RF próprio. |

## Anexo — Evidência (complementar)

Ponte para os critérios e testes de aceite (REQ-05 e REQ-06). Testes a partir de `src/backend/`, salvo os do frontend (`src/frontend/src/`); `[x]` = teste parametrizado. Fontes: [rf-contas](../requisitos/rf-contas.md), [rnf](../requisitos/rnf.md) e [`matriz_de_acesso.md`](../../matriz_de_acesso.md).

| Item | Testes que o comprovam |
|---|---|
| [Fluxo principal](#p1) | `contas/tests/test_api_autenticacao.py::test_login_valido_devolve_tokens_e_usuario_sem_senha`, `::test_login_aceita_email_com_caixa_diferente_e_espacos`, `::test_login_preenche_last_login`; `exemplos/tests/test_carregar_dados_exemplo.py::test_login_com_cada_usuario_de_exemplo [x]`; `pages/PaginaEntrar.test.tsx`; `components/layout/Layout.test.tsx` |
| [A1.1](#a1-1) | `components/sessao/SessaoProvider.test.tsx` (volta ao caminho atual); `navegacao.test.ts` (`proximoSeguro`) |
| [A1.2](#a1-2) | `contas/tests/test_api_cadastro.py::test_usuario_recem_cadastrado_consegue_fazer_login`; `pages/PaginaCadastro.test.tsx` |
| [A4.1](#a4-1) | `contas/tests/test_api_autenticacao.py::test_refresh_valido_devolve_access_novo_que_funciona_no_me`, `::test_access_dura_o_tempo_configurado`, `::test_refresh_dura_o_tempo_configurado`; `api/cliente.test.ts` (renovação no 401 e renovação compartilhada) |
| [A4.2](#a4-2) | `contas/tests/test_api_autenticacao.py::test_me_com_bearer_valido_devolve_usuario_com_perfil`; `config/tests/test_perfil_lido_do_banco.py::test_gestor_rebaixado_perde_as_permissoes_com_o_mesmo_token`, `::test_solicitante_promovido_ganha_as_permissoes_com_o_mesmo_token`; `components/sessao/SessaoProvider.test.tsx` (restaura e confirma a sessão) |
| [A4.3](#a4-3) | `components/sessao/SessaoProvider.test.tsx` (sair limpa a sessão e vai para o início); `api/sessao.test.ts` |
| [E3.1](#e3-1) | `contas/tests/test_api_autenticacao.py::test_login_sem_campos_responde_400_com_cada_campo` |
| [E3.2](#e3-2) | `contas/tests/test_api_autenticacao.py::test_senha_errada_email_inexistente_e_inativo_respondem_igual`; `pages/PaginaEntrar.test.tsx` (credenciais inválidas no aviso do topo) |
| [E4.1](#e4-1) | `contas/tests/test_api_autenticacao.py::test_refresh_invalido_responde_401_no_formato_padrao`, `::test_me_com_access_expirado_responde_401`, `::test_token_adulterado_responde_401 [x]`, `::test_access_usado_como_refresh_responde_401`; `api/cliente.test.ts` (renovação recusada lança a sessão expirada); `components/sessao/SessaoProvider.test.tsx` (expiração leva ao login com o caminho atual) |
| [E4.2](#e4-2) | `contas/tests/test_api_autenticacao.py::test_access_de_usuario_desativado_depois_do_login_responde_401`, `::test_access_de_usuario_excluido_responde_401`, `::test_refresh_de_usuario_inativo_responde_401`, `::test_refresh_de_usuario_excluido_responde_401` |

**Histórias derivadas:** [US-02 Entrar no sistema](../historias/US-02-entrar-no-sistema.md), [US-03 Manter e encerrar a sessão](../historias/US-03-manter-e-encerrar-a-sessao.md). Cobertura de cada alternativa e exceção: [historias/README.md](../historias/README.md#cobertura-uc--usca).
