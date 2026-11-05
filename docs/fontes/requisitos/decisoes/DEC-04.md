# DEC-04 — Autenticação e perfis de acesso

| Identificação | Responsabilidade |
|---|---|
| **DEC-04 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Decidida. Resposta do professor recebida; decisão do grupo registrada em 16/10/2026. |
| **Pergunta** | O sistema precisa identificar quem solicita uma reserva e quem pode aprová-la? O enunciado de Projeto de Programação não exige autenticação real. |
| **Resposta do professor** | "Conta como extra, mas não é obrigatório." |
| **Decisão** | O sistema terá cadastro e login de usuários (JWT) e dois perfis. `SOLICITANTE` solicita reservas, consulta as próprias e cancela as próprias. `GESTOR` cadastra e edita espaços, consulta todas as reservas e pode confirmá-las, recusá-las, concluí-las ou cancelá-las. O solicitante de uma reserva passa a ser sempre o usuário autenticado, e não um nome digitado no formulário. |
| **Motivo** | Sem identificação, qualquer pessoa poderia confirmar ou cancelar a reserva de outra, e o campo "solicitante" seria texto livre sem garantia de autoria. Na priorização QFD é um requisito **esperado**: o usuário não pede, mas se frustra se faltar. |
| **Alternativas** | Sem autenticação, com o solicitante informado na reserva (nome e matrícula): é a contingência abaixo. |
| **Requisitos derivados** | IDs a definir no SRS (REQ-02): RF de cadastro de usuário solicitante; RF de autenticação; RF de controle de ações por perfil; RNF de segurança (FURPS, Funcionalidade): senhas armazenadas apenas com hash, no mínimo 8 caracteres, token de acesso que expira em 30 minutos e toda operação, exceto cadastro e login, exigindo autenticação. |
| **Responsável** | Professor (resposta); grupo (decisão). |
| **Prazo** | Decidida em 16/10/2026. |
| **Artefatos afetados** | `CLAUDE.md` (estrutura, modelo de domínio, rastreabilidade e regras); Documento de Visão (stakeholders Solicitante e Gestor); SRS; diagrama de casos de uso (ator Gestor e `<<include>>` Autenticar); casos de uso Solicitar reserva e Alterar situação (precondição "usuário autenticado" e exceção "perfil sem permissão"); user stories e critérios de aceite; matriz de rastreabilidade; `modelagem.pdf`; README (usuários de teste). · **REQ-06:** histórias [US-01](../historias/US-01-criar-minha-conta.md), [US-02](../historias/US-02-entrar-no-sistema.md), [US-03](../historias/US-03-manter-e-encerrar-a-sessao.md), [US-04](../historias/US-04-consultar-os-espacos.md), [US-05](../historias/US-05-cadastrar-espaco.md), [US-06](../historias/US-06-editar-espaco.md), [US-07](../historias/US-07-desativar-e-reativar-espaco.md), [US-08](../historias/US-08-solicitar-reserva.md), [US-10](../historias/US-10-acompanhar-minhas-reservas.md), [US-11](../historias/US-11-acompanhar-todas-as-reservas.md), [US-12](../historias/US-12-ver-detalhe-e-historico.md), [US-13](../historias/US-13-cancelar-uma-reserva.md), [US-14](../historias/US-14-confirmar-uma-reserva.md), [US-15](../historias/US-15-recusar-uma-reserva.md), [US-16](../historias/US-16-concluir-uma-reserva.md), [US-17](../historias/US-17-criar-o-primeiro-gestor.md); 39 critérios de aceite e 39 testes de aceite ([mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-04)). |
| **Restrição de escopo** | Por ser extra, não pode atrasar as seis funcionalidades mínimas. Só o modelo de usuário (`contas.Usuario`) entra na fundação do projeto, porque não pode ser trocado depois da primeira migration. |
| **Contingência** | Se a autenticação ameaçar a entrega, ela é retirada e o solicitante volta a ser informado na reserva (nome e matrícula). Essa reversão é uma mudança comportamental e exige um novo registro, sem reutilizar este ID. |
| **Origem** | Ponto a confirmar 6 do `CLAUDE.md` ("Autenticação"). |
| **Observações** | Conteúdo migrado sem alteração de sentido da seção "DECs" de `.claude/requisitos.md`. A contingência não foi acionada: a autenticação foi implantada (AUT-03 a AUT-07). |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Migrada de `.claude/requisitos.md` para a fonte oficial, no modelo A4·s13 (REQ-01). |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as histórias e o número de critérios e testes de aceite, a partir do [mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-04) (REQ-06). Estado e opção sem mudança. |
