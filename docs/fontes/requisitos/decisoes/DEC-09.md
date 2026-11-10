# DEC-09 — Formato da matrícula

| Identificação | Responsabilidade |
|---|---|
| **DEC-09 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Decidida. Resposta do professor na Aula 7 (06/11/2026); a resposta muda o comportamento implementado e segue pelo [CR-04](../mudancas/CR-04-matricula-so-digitos.md). |
| **Pergunta** | Qual é o formato da matrícula na instituição (quantidade de caracteres, só dígitos, prefixo)? Ela precisa ser conferida com o cadastro acadêmico? |
| **Opção implementada até o CR-04** | [Matrícula](../glossario.md#matricula) obrigatória, única, com até 20 caracteres e sem espaços (os das pontas são removidos). Não é conferida com a instituição. |
| **Resposta do professor** | "São números sempre, mas não tem uma quantidade máxima e uma quantidade mínima." |
| **Decisão do grupo** | Só dígitos. O limite de 20 caracteres fica como limite técnico (coluna do banco), não como regra da instituição. |
| **Decisão** | A matrícula é obrigatória, única e formada só por dígitos, sem quantidade mínima ou máxima definida pela instituição; o limite de 20 caracteres continua apenas como limite técnico do armazenamento. |
| **Implementação** | [CR-04](../mudancas/CR-04-matricula-so-digitos.md), tarefa AUT-12. Até ela, o código continua com a regra acima. |
| **Motivo** | O formato real não foi informado. A regra provisória aceita qualquer formato plausível e fica isolada numa função, para mudar sem afetar o resto. |
| **Alternativas** | Só dígitos, com uma quantidade fixa; um padrão com prefixo (definido por expressão regular); conferência com o cadastro acadêmico (fora do escopo: integração institucional). A decisão é só dígitos, sem quantidade fixa e sem conferência. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor. |
| **Prazo** | Decidida em 06/11/2026. |
| **Artefatos afetados** | `_validar_matricula`, `MatriculaInvalida` e `MATRICULA_MAXIMO_CARACTERES` (`contas/domain/`); coluna `matricula` de `contas.Usuario` e `solicitante_matricula` de `reservas` (migration, se o tamanho mudar); dados de exemplo; README (usuários de teste); [Visão](../visao.md) (P-02, R-12); critérios de aceite do cadastro (REQ-04). · **REQ-06:** histórias [US-01](../historias/US-01-criar-minha-conta.md), [US-02](../historias/US-02-entrar-no-sistema.md); 9 critérios de aceite e 9 testes de aceite ([mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-09)). |
| **Origem** | AUT-04, decisão e ("O formato real fica para uma DEC" no `CLAUDE.md`). |
| **Observações** | ID novo: o `CLAUDE.md` citava a decisão sem número. As matrículas dos dados de exemplo e do README já são só dígitos. O [CR-04](../mudancas/CR-04-matricula-so-digitos.md) traz o impacto e o aceite; a AUT-12 aplica o CR no mesmo PR do código. |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Registro da decisão pendente da AUT-04 (REQ-01). |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as histórias e o número de critérios e testes de aceite, a partir do [mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-09) (REQ-06). Estado e opção sem mudança. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Decidida na Aula 7: resposta do professor e decisão do grupo registradas; a regra atual passa a "implementada até o CR-04"; CR-04 aberto, implementação na AUT-12 (GES-02). |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Artefatos afetados com 9 critérios e 9 testes de aceite, depois de aplicar o CR-04 na especificação, com os CAs novos da US-01 (REQ-13). Estado e opção sem mudança. Sem aprovação. |
