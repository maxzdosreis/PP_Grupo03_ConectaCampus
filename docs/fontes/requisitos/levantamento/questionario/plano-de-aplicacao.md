# Plano de aplicação do questionário QST-01

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **QST-01 • 0.1 • Rascunho** (plano de aplicação) | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/levantamento/questionario/plano-de-aplicacao.md` |

Como o [QST-01](QST-01-questionario.md) será aplicado. Este plano é do grupo e não contém resultados.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Criação (REQ-10). Sem aprovação. |

## Público e meta

| Item | Definição |
|---|---|
| **Público** | Solicitantes: estudantes e servidores que usam, ou já quiseram usar, espaços esportivos do campus. Atendente responsável e Gestor do serviço ficam com as entrevistas ([ROT-03](../entrevistas/ROT-03-atendente-responsavel.md)). |
| **Meta de respostas** | No mínimo **15**. É meta do grupo, **não** regra do enunciado. Sem 15 respostas, a síntese sai igual, com o n real e a limitação dita. |
| **Participantes** | Anônimos. Registramos só o vínculo e a frequência de uso (P01 e P02), nunca nome, e-mail, matrícula, curso ou turma. |

## Canais de divulgação

Descritos de forma genérica, sem nomear pessoas ou grupos:

- grupos de mensagens das turmas dos integrantes;
- murais do campus onde a divulgação for permitida;
- convite pessoal a colegas e servidores que usam os espaços.

A mensagem de divulgação repete só a abertura do formulário e o link; não adianta o que o grupo pensa dos espaços nem do sistema.

## Período

| Etapa | Quando |
|---|---|
| Piloto com 2 colegas | 09/11/2026 ou 10/11/2026, antes de divulgar |
| Aplicação | De **10/11/2026** até **12:00 de 12/11/2026** (o formulário é fechado nesse horário) |
| Síntese e entrada no PDF de evidências | Tarde de 12/11/2026; entrega em 13/11/2026 |

## Piloto

Antes de divulgar, 2 colegas que não escreveram o questionário respondem em condição real. Registrar, sem nomes:

| O que medir | Registro |
|---|---|
| Tempo para responder (cronometrado) | ___ min ___ s e ___ min ___ s |
| Dúvidas de entendimento (pergunta e o que não ficou claro) | |
| Opção que faltou ou que se repetiu | |
| Ajustes feitos no texto e a nova versão do QST-01 | |

As respostas do piloto **não entram** na síntese; o formulário é limpo antes de divulgar.

## Tempo de resposta

Estimativa **a confirmar no piloto**, não medida:

| Parte | Conta | Tempo |
|---|---|---|
| Leitura da abertura | — | 15 s |
| 6 perguntas de uma opção (P01, P02, P04, P05, P06, P08) | 6 × 10 s | 60 s |
| 3 perguntas de várias opções (P03, P07, P09) | 3 × 20 s | 60 s |
| **Só as obrigatórias** | | **2 min 15 s** |
| P10 (aberta, curta) | 1 × 40 s | 40 s |
| P11 (aberta, curta) | 1 × 10 s | 10 s |
| **Todas as 11** | | **≈ 3 min 05 s** |

Regra de corte: se o piloto passar de 3 minutos, **P11 sai primeiro** (fica 10 perguntas); depois, as opções "Não se aplica" repetidas. Qualquer corte vira nova versão do QST-01 (0.2) e é registrado no histórico.

## Configurações do formulário

| Configuração | Valor |
|---|---|
| Coletar e-mails | **Não** |
| Limitar a uma resposta por pessoa | **Não exige login** (exigi-lo identificaria a conta de quem responde, contra o anonimato); aceitamos o risco de resposta duplicada e o dizemos nas limitações |
| Obrigatoriedade | P01 a P09 obrigatórias; P10 e P11 opcionais |
| Ordem das opções | **Fixa** (não embaralhar) |
| P09 | Validação "selecionar no máximo 3" |
| P03 e P07 | Caixas de seleção; P01, P02, P04, P05, P06 e P08, uma opção |
| Confirmação | Mensagem de agradecimento, sem pedir contato |
| Mostrar resumo/gráficos aos respondentes | Não |

## Dados brutos

O arquivo exportado do formulário (CSV) **nunca entra no repositório**. Fica fora do Git, na pasta `levantamento/questionario/brutos/`, que o `.gitignore` da raiz ignora. No repositório vão só a síntese (contagens e temas) e o instrumento. As respostas abertas são resumidas por tema na síntese, sem transcrever trecho que identifique alguém.

## Limitações assumidas

- **Amostra por conveniência, não estatística.** Respondem as pessoas que o grupo alcança; não há sorteio nem garantia de representar o campus.
- **Viés de quem escolhe responder.** Quem tem um problema com os espaços, ou usa muito, tende a responder mais.
- **Resultados indicam tendências, não probabilidades.** Com amostra pequena, mostramos contagens ("n de N"), nunca percentuais como se fossem do campus inteiro.
- **Resposta duplicada possível**, porque o formulário não exige login.
- **Respostas de memória** (P04 cobre 3 meses) podem errar.
