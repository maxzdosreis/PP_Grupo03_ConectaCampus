# DEC-25 — Atendente responsável como papel da especificação; um perfil cobre Atendente e Gestor no sistema mínimo

| Identificação | Responsabilidade |
|---|---|
| **DEC-25 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Decidida pelo grupo em 10/11/2026 (REQ-12). Não depende de resposta do professor. Nenhum CR: a decisão mantém o comportamento implementado. |
| **Pergunta** | O enunciado do Projeto Final (§2) pede os papéis "solicitante, atendente responsável e gestor do serviço". O sistema só tem os perfis Solicitante e [Gestor](../glossario.md#gestor). Como a especificação trata os três papéis? |
| **Resposta do professor** | Não perguntada. |
| **Contexto** | O enunciado §2 lista os três papéis mínimos. A [Visão](../visao.md#2-usuários-atores-e-stakeholders) e o [glossário](../glossario.md) descreviam um só papel, o Gestor, que cadastrava espaços e decidia sobre os pedidos. O levantamento (entrevista [ENT-04](../levantamento/entrevistas/ENT-04-atendente-responsavel-simulada.md), simulada, e síntese [ACH-22](../levantamento/sintese-do-levantamento.md#2-achados-e-destinos)) separou quem opera os espaços de quem define as regras, e remeteu a separação à REQ-12. |
| **Decisão** | **a)** O **Atendente responsável** é um papel da especificação: o servidor que opera os espaços no dia a dia e confirma, recusa, conclui e cancela reservas. **b)** O **Gestor do serviço** é o papel que cadastra e mantém os espaços e define as regras de uso. **c)** No sistema mínimo (1.0), **um único perfil cobre os dois papéis**: o perfil Gestor (`PerfilUsuario.GESTOR`, `PapelDoAtor.GESTOR`). Os dois papéis são distintos na especificação e coincidem no produto. **d)** O Solicitante segue como o outro papel; o Gestor também solicita em nome próprio ([DEC-04](DEC-04.md)). |
| **Consequências na especificação** | A Visão e o glossário passam a definir os três papéis, e "Gestor" fica como o nome do perfil técnico que cobre dois deles. O diagrama de casos de uso tem três atores (Solicitante, Atendente responsável e Gestor do serviço), os dois últimos generalizando o Solicitante, com a nota do perfil único. Os casos de uso e as histórias de decisão (confirmar, recusar, concluir, cancelar e acompanhar os pedidos) citam o Atendente responsável; os de manutenção de espaços, o Gestor do serviço. O catálogo de [regras de negócio](../requisitos/regras-de-negocio.md) é do Gestor do serviço. |
| **O que não muda** | O código, os testes, as migrations e o Docker: continua existindo um perfil só para quem opera e administra. Não há perfil novo, permissão nova nem tela nova. Os IDs de RF, RNF, UC, US, DEC e NS não mudam, e os enunciados dos RF seguem falando do perfil Gestor. Dois perfis no produto exigiriam um CR e implementação (fora do 1.0). |
| **Motivo** | O enunciado pede os papéis na especificação, mas as seis funcionalidades mínimas e o prazo de 20/11/2026 não comportam um segundo perfil de acesso, e a Visão descreve um só setor responsável pelos espaços, que opera e administra ([Visão, seção 2](../visao.md#2-usuários-atores-e-stakeholders)). |
| **Alternativas** | **e)** Dois perfis no sistema (um para o Atendente, um para o Gestor do serviço): exigiria um perfil novo, uma matriz de acesso nova e a divisão das permissões hoje reunidas em `ApenasGestor` e `DESTINOS_POR_PAPEL`; descartada para o 1.0. **f)** Atendente como o mesmo papel do Gestor, sem distinção na especificação: descartada, porque o enunciado §2 pede os dois papéis e porque quem decide os pedidos e quem define as regras de uso têm interesses diferentes. |
| **Responsável** | Max Zimmermann dos Reis (grupo). |
| **Prazo** | Decidida em 10/11/2026. |
| **Artefatos afetados** | [Visão](../visao.md) (tabela de atores); [glossário](../glossario.md) (Atendente responsável, Gestor do serviço e Gestor); diagrama [UCD-01](../casos-de-uso/diagrama-casos-de-uso.puml) e o [README dos casos de uso](../casos-de-uso/README.md); fichas dos casos de uso de decisão e de manutenção de espaços; histórias [US-05](../historias/US-05-cadastrar-espaco.md), [US-06](../historias/US-06-editar-espaco.md), [US-07](../historias/US-07-desativar-e-reativar-espaco.md), [US-11](../historias/US-11-acompanhar-todas-as-reservas.md), [US-14](../historias/US-14-confirmar-uma-reserva.md), [US-15](../historias/US-15-recusar-uma-reserva.md) e [US-16](../historias/US-16-concluir-uma-reserva.md); [regras de negócio](../requisitos/regras-de-negocio.md); [CR-05](../mudancas/CR-05-atendente-e-gestor-nos-artefatos-mistos.md) (artefatos de ator misto). · **REQ-06:** nenhuma história depende desta decisão no campo Decisões; 0 critérios de aceite e 0 testes de aceite a rever ([mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-25)). |
| **Origem** | Enunciado do Projeto Final de Requisitos, §2; síntese do levantamento (REQ-11), linha 7 do encaminhamento; REQ-12. |
| **Observações** | A fonte da decisão é o grupo e o enunciado §2; nenhuma resposta do professor sustenta a escolha do perfil único. Se um segundo perfil entrar, esta DEC passa a **Substituída** por uma nova e o CR correspondente muda o código. |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Criação e decisão do grupo (REQ-12). |
