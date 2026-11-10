# Roteiro de entrevista — Atendente responsável

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **ROT-03 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/levantamento/entrevistas/ROT-03-atendente-responsavel.md` |

Para um servidor do setor que recebe os pedidos de uso e opera os espaços esportivos do campus (o papel Atendente responsável da REQ-12). Duração: 10 a 15 minutos. Antes, leia o [guia do entrevistador](../guia-do-entrevistador.md).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Criação (REQ-09). Sem aprovação. |

## Abertura (ler em voz alta)

> Olá! Somos do Grupo 03 da disciplina de Requisitos de Software. Queremos entender como funcionam hoje os pedidos de uso dos espaços esportivos do campus e o que falta para quem os atende. Não estamos vendendo nem apresentando nada: o que importa é a sua experiência. A conversa leva de 10 a 15 minutos. Não anotamos o seu nome, cargo, setor exato nem contato, só um perfil geral, como "servidor que atende os pedidos há mais de um ano". Você pode pular qualquer pergunta ou parar quando quiser. Posso anotar as suas respostas?

Sem consentimento: agradecer e encerrar, sem anotar. **Perfil** (genérico): o que faz com os pedidos; há quanto tempo, em faixa ("menos de um ano", "mais de um ano").

## Perguntas

A coluna "O que busca" é só do entrevistador: **não ler**.

| P | Tema | Tipo | Pergunta | Aprofundamento | O que busca (interno) |
|---|---|---|---|---|---|
| P01 | Como funciona hoje | ESSENCIAL | Conte como chegou até você o último pedido de uso de um espaço e o que você fez com ele, do começo ao fim. | Quanto tempo levou para dar a resposta? Onde ficou anotado? | NS-03 e NS-09; papel do Atendente responsável (REQ-12) |
| P02 | Como funciona hoje | ESSENCIAL | Como você decide se aceita ou nega um pedido? | Conte um pedido que você negou: o que disse à pessoa? | NS-09; motivo para recusar (RF-18) |
| P03 | Problemas e consequências | ESSENCIAL | Conte a última vez em que chegaram dois pedidos para o mesmo espaço no mesmo horário. Como resolveu? | Quem ficou com o horário, e por quê? Como a outra pessoa soube? | NS-04; RF-11.4 (o primeiro pedido bloqueia o horário) |
| P04 | Problemas e consequências | SE HOUVER TEMPO | Que problemas aparecem com mais frequência no uso dos espaços? | Qual foi o último? Que consequência teve? | Problema da Visão (seção 1); NS-12 |
| P05 | Regras e exceções | ESSENCIAL | Quando e como você registra que um uso aconteceu? | O que é feito com esse registro depois? Quem o consulta? | NS-09 (registrar o uso); DEC-13 e CR-01 (concluir só depois do término) |
| P06 | Regras e exceções | ESSENCIAL | O que você faz quando alguém não aparece no horário combinado? | Que consequência isso tem para a pessoa? E para o horário que ficou vazio? | DEC-13 e CR-01 (cancelar só antes do início); não comparecimento |
| P07 | Regras e exceções | ESSENCIAL | Como funcionam os horários de cada espaço? Conte como é num espaço que você conhece bem. | O que muda de um espaço para outro? E nos fins de semana e feriados? | DEC-07 e CR-03 (horário por espaço, 07:00–00:00); P-04 |
| P08 | Regras e exceções | ESSENCIAL | Quem define as regras de uso dos espaços, como horários, duração e antecedência? | Conte a última vez que uma regra mudou: quem decidiu e como vocês souberam? | Gestor do serviço (REQ-12); cliente × usuário (Visão, seção 2); DEC-07 |
| P09 | Regras e exceções | SE HOUVER TEMPO | Quando um espaço precisa sair de uso, por manutenção ou evento, o que acontece com os usos já combinados? | Como as pessoas ficam sabendo? | DEC-06; NS-02; bloqueio de períodos (fora do escopo) |
| P10 | Informação de que precisa | SE HOUVER TEMPO | Que informações você precisa ter em mãos para decidir sobre um pedido? | Conte uma vez em que faltou informação para decidir. O que fez? | NS-08 e NS-11; finalidade do pedido (NS-03) |
| P11 | Prioridades | ESSENCIAL | Do seu trabalho com os pedidos, o que mais consome tempo hoje? | Por que isso pesa mais que o resto? | Prioridade das NS (QFD) |

## Encerramento

> Tem algo que eu não perguntei e deveria ter perguntado? … Muito obrigado pelo seu tempo, isso ajuda bastante o nosso trabalho.
