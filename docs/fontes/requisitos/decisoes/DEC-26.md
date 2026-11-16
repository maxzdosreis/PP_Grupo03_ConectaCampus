# DEC-26 — O usuário autenticado pode trocar a própria senha

| Identificação | Responsabilidade |
|---|---|
| **DEC-26 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Decidida pelo grupo em 16/11/2026, na tarefa AUT-10, depois da entrega da especificação de 13/11/2026. Não depende de resposta do professor: é um extra de autenticação, como a [DEC-04](DEC-04.md), e não toca nas seis funcionalidades mínimas. Muda a Visão ([CR-06](../mudancas/CR-06-trocar-a-propria-senha.md)). |
| **Pergunta** | A troca da própria senha, hoje listada como fora do escopo na [Visão](../visao.md#fora-do-escopo), entra no 1.0? Se entrar, como tratar a senha atual errada, as sessões abertas em outros aparelhos e o limite de tentativas? |
| **Resposta do professor** | Não perguntada. |
| **Decisão** | **a)** O usuário autenticado, de qualquer perfil, troca **só a própria** senha informando a senha atual e a nova ([RF-41](../requisitos/rf-contas.md#rf-41)). A conta vem sempre da identificação, nunca de um dado do pedido. **b)** A senha nova segue a **mesma** política de senha do cadastro e precisa ser diferente da atual; as conferências vêm nesta ordem: limite de tentativas, campos informados, senha atual, igual à atual, política ([RF-41.1](../requisitos/rf-contas.md#rf-41-1)). **c)** Errar a senha atual é um erro de validação com código próprio (`SENHA_ATUAL_INCORRETA`, 400), **nunca** um 401: um 401 faria o navegador renovar ou encerrar a sessão, e a pessoa seria deslogada por errar a senha. **d)** A troca tem limite de 5 tentativas por minuto **por conta**, e não por origem do pedido (`LIMITE_TROCA_DE_SENHA_POR_USUARIO`), porque no Docker todos os acessos chegam da mesma origem ([RF-41.2](../requisitos/rf-contas.md#rf-41-2)). **e)** Depois da troca, a credencial de renovação das **outras** sessões da conta é revogada e a da sessão atual continua; o aparelho informa a própria credencial de renovação para a API saber qual manter, e sem ela todas são revogadas. **f)** A credencial de **acesso** já emitida não é revogável e vale até expirar (30 minutos): isso fica documentado como limitação conhecida ([L-04](../requisitos/srs.md#l-04)). **g)** **Fora do escopo:** recuperar a senha esquecida por e-mail, que exigiria um servidor de e-mail ([Notificações](../visao.md#fora-do-escopo)); quem esquece a senha continua dependendo da administração (Equipe de TI). |
| **Motivo** | Sem a troca, quem suspeita que a senha vazou, ou quer uma melhor, depende de outra pessoa, o contrário da [NS-15](../visao.md#ns-15) (acesso sem depender de um gestor). A infraestrutura já existia: a política de senha do cadastro, o limite de tentativas e a revogação das credenciais de renovação da AUT-09. Por isso o custo é pequeno e não ameaça as seis funcionalidades mínimas ([R-01](../visao.md#riscos)). |
| **Achados** | Nenhum. Surgiu da lista de tarefas de autenticação (AUT-10), não do levantamento. |
| **Alternativas** | **h)** Manter fora do escopo: a senha só mudaria pela administração. **i)** Responder 401 à senha atual errada, como no login: descartada, porque o 401 desloga a pessoa no navegador. **j)** Revogar também as credenciais de acesso: exigiria consultar o banco a cada operação, em todas as chamadas, e o Simple JWT não traz isso pronto. **k)** Não revogar nenhuma sessão: descartada, porque quem trocou a senha por suspeita de vazamento continuaria exposto nos outros aparelhos. **l)** Limite por origem do pedido: descartada, porque no Docker todos os acessos têm a mesma origem. |
| **Responsável** | Max Zimmermann dos Reis (grupo). |
| **Prazo** | Decidida em 16/11/2026. |
| **Artefatos afetados** | [Visão](../visao.md) (fora do escopo e NS-15); [glossário](../glossario.md#troca-de-senha); SRS; UC-02 (A4.4 e E4.3 a E4.6); US-21; matriz de acesso; README (limitações conhecidas). · **REQ-06:** histórias [US-21](../historias/US-21-trocar-a-propria-senha.md); 7 critérios de aceite e 7 testes de aceite ([mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-26)). |
| **Origem** | Tarefa AUT-10 (backlog de autenticação). |
| **Observações** | Esta DEC não altera a [DEC-04](DEC-04.md): a troca de senha é mais um extra de autenticação. A especificação entregue em 13/11/2026 (`RS_Grupo03_Especificacao.md` e os PDFs) não foi alterada; o histórico dos arquivos da fonte oficial registra a mudança. |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 16/11/2026 | Max Zimmermann dos Reis | Criação e decisão do grupo, na tarefa AUT-10, com o [CR-06](../mudancas/CR-06-trocar-a-propria-senha.md). |
