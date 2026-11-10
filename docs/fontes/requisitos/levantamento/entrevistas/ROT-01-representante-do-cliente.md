# Roteiro de entrevista — Representante do cliente

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **ROT-01 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/levantamento/entrevistas/ROT-01-representante-do-cliente.md` |

Instrumento usado na [ENT-01](ENT-01-representante-do-cliente.md), na Aula 7 (06/11/2026), com o professor no papel de representante do cliente ([premissa P-01](../../visao.md#premissas)). É a reprodução do que existiu, **sem reescrita**: P01 a P16 são as perguntas da [pauta da Aula 7](../../decisoes/pauta-aula-7.md), com o texto da pauta; P17 a P20 são as quatro perguntas sobre a entrega, feitas fora da pauta escrita e registradas no campo "Pergunta" de cada DEC. Na pauta, cada pergunta das DECs levava também a opção adotada, o porquê e o impacto se a resposta fosse outra (ver a pauta). A pauta não tinha abertura nem encerramento escritos.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Criação a partir da pauta da Aula 7 (PAU-01) e das DEC-20 a DEC-23, sem mudar o texto das perguntas (REQ-09). Sem aprovação. |

## Perguntas

| P | Assunto | Pergunta | Origem |
|---|---|---|---|
| P01 | Mudança de situação × horário da reserva | concluir, confirmar, recusar e cancelar devem depender do horário da reserva (e o que acontece com um pedido que ninguém decidiu até a data passar)? | [Pauta, DEC-13](../../decisoes/pauta-aula-7.md#dec-13) |
| P02 | Histórico só com mudanças efetivas | uma tentativa recusada de mudar a situação precisa ficar registrada? Onde e para quem? | [Pauta, DEC-05](../../decisoes/pauta-aula-7.md#dec-05) |
| P03 | Valores das regras de agenda | quais são o horário de funcionamento, a duração mínima e máxima e a antecedência máxima? São iguais para todos os espaços e dias? | [Pauta, DEC-07](../../decisoes/pauta-aula-7.md#dec-07) |
| P04 | Reservas de um espaço desativado | quando o Gestor desativa um espaço, o que acontece com as reservas que ele já tem? | [Pauta, DEC-06](../../decisoes/pauta-aula-7.md#dec-06) |
| P05 | Formato da matrícula | qual é o formato real da matrícula, e ela precisa ser conferida com a instituição? | [Pauta, DEC-09](../../decisoes/pauta-aula-7.md#dec-09) |
| P06 | Nome de espaço único | dois espaços podem ter o mesmo nome? "Ginásio A" e "ginásio a" são o mesmo? | [Pauta, DEC-10](../../decisoes/pauta-aula-7.md#dec-10) |
| P07 | Períodos ocupados por outras pessoas na agenda do dia | o Solicitante pode ver, antes de pedir, os períodos ocupados por reservas de outras pessoas? Com quais dados? | [Pauta, DEC-11](../../decisoes/pauta-aula-7.md#dec-11) |
| P08 | Cobertura-alvo dos testes (se houver tempo) | que meta de testes o grupo adota, já que a disciplina não exige testes? | [Pauta, DEC-08](../../decisoes/pauta-aula-7.md#dec-08) |
| P09 | Metas de desempenho (se houver tempo) | em quanto tempo a consulta de reservas e a agenda do dia precisam responder, e com quantas reservas? | [Pauta, DEC-12](../../decisoes/pauta-aula-7.md#dec-12) |
| P10 | Outros diagramas | Outros diagramas (sequência, C4, DER, raias) serão exigidos? | [Pauta, pontos a confirmar](../../decisoes/pauta-aula-7.md#pontos-a-confirmar) (ponto 4 de `.claude/requisitos.md`) |
| P11 | Numeração de exceções | Exceções numeradas com `E` ou tudo com `A`? | Idem (ponto 5 de `.claude/requisitos.md`) |
| P12 | Index Card | Campos do "Index Card padrão"; o custo em semanas aceita fração? | Idem (ponto 6 de `.claude/requisitos.md`) |
| P13 | Convenção de versão | A convenção de versão 0.1 → 0.2 → 1.0 vale? | Idem (ponto 10 de `.claude/requisitos.md`) |
| P14 | Rastreabilidade até o código | A rastreabilidade deve ir até o código? | Idem (ponto 13 de `.claude/requisitos.md`) |
| P15 | Grupo nas duas disciplinas | O grupo atende às regras das duas disciplinas? | Idem (ponto 4 do `CLAUDE.md`) |
| P16 | Formato dos critérios de aceite | Dado/Quando/Então atende como formato de critério de aceite? | Idem (ponto 5 do `CLAUDE.md`) |
| P17 | Entrega dos documentos de Requisitos | Como os documentos de Requisitos são entregues? | Fora da pauta escrita; [DEC-20](../../decisoes/DEC-20.md) |
| P18 | Capa do `modelagem.pdf` | A capa conta nas 6 páginas do `modelagem.pdf`, e precisa ser uma capa formal? | Fora da pauta escrita; [DEC-21](../../decisoes/DEC-21.md) |
| P19 | Modelo do `contribuicoes.pdf` | Há um modelo para o `contribuicoes.pdf`? | Fora da pauta escrita; [DEC-22](../../decisoes/DEC-22.md) |
| P20 | Apresentação | Como e onde é a apresentação do sistema? | Fora da pauta escrita; [DEC-23](../../decisoes/DEC-23.md) |
