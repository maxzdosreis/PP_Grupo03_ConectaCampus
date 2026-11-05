# DEC-09 — Formato da matrícula

| Identificação | Responsabilidade |
|---|---|
| **DEC-09 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Adotada provisoriamente (o código já implementa a regra abaixo; falta a confirmação). |
| **Pergunta** | Qual é o formato da matrícula na instituição (quantidade de caracteres, só dígitos, prefixo)? Ela precisa ser conferida com o cadastro acadêmico? |
| **Opção adotada hoje** | [Matrícula](../glossario.md#matricula) obrigatória, única, com até 20 caracteres e sem espaços (os das pontas são removidos). Não é conferida com a instituição. |
| **Motivo** | O formato real não foi informado. A regra provisória aceita qualquer formato plausível e fica isolada numa função, para mudar sem afetar o resto. |
| **Alternativas** | Só dígitos, com uma quantidade fixa; um padrão com prefixo (definido por expressão regular); conferência com o cadastro acadêmico (fora do escopo: integração institucional). |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor. |
| **Prazo sugerido** | 06/11/2026 (Aula 7). |
| **Artefatos afetados** | `_validar_matricula`, `MatriculaInvalida` e `MATRICULA_MAXIMO_CARACTERES` (`contas/domain/`); coluna `matricula` de `contas.Usuario` e `solicitante_matricula` de `reservas` (migration, se o tamanho mudar); dados de exemplo; README (usuários de teste); [Visão](../visao.md) (P-02, R-12); critérios de aceite do cadastro (REQ-04). · **REQ-06:** histórias [US-01](../historias/US-01-criar-minha-conta.md), [US-02](../historias/US-02-entrar-no-sistema.md); 5 critérios de aceite e 5 testes de aceite ([mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-09)). |
| **Origem** | AUT-04, decisão e ("O formato real fica para uma DEC" no `CLAUDE.md`). |
| **Observações** | ID novo: o `CLAUDE.md` citava a decisão sem número. |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Registro da decisão pendente da AUT-04 (REQ-01). |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as histórias e o número de critérios e testes de aceite, a partir do [mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-09) (REQ-06). Estado e opção sem mudança. |
