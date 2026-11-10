# Questionário — Uso de espaços esportivos do campus

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **QST-01 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/levantamento/questionario/QST-01-questionario.md` |

Instrumento da segunda técnica de levantamento do grupo (REQ-10), para **Solicitantes** (estudantes e servidores que usam, ou já quiseram usar, espaços esportivos do campus). Aplicação em [`plano-de-aplicacao.md`](plano-de-aplicacao.md); síntese em [`modelo-sintese-questionario.md`](modelo-sintese-questionario.md); versão para o PDF de evidências em [`QST-01-versao-impressa.md`](QST-01-versao-impressa.md). Este arquivo ainda **não tem respostas**.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Criação do instrumento: 11 perguntas, 9 obrigatórias (REQ-10). Piloto ainda não feito. Sem aprovação. |

## 1. Texto de abertura (copiar como descrição do formulário)

> **Uso de espaços esportivos do campus**
>
> Somos do Grupo 03 da disciplina de Requisitos de Software. Queremos entender como você consegue um espaço esportivo hoje. Não é avaliação de ninguém: não existe resposta certa ou errada.
>
> O formulário é **anônimo**: não pedimos nome, e-mail, matrícula, curso nem turma. As respostas são usadas só no trabalho da disciplina. Leva cerca de 3 minutos.

## 2. Perguntas (copiar para o formulário, na ordem)

Convenções: **uma opção** = marcar uma só; **várias** = caixas de seleção. A ordem das opções é fixa (não embaralhar). Onde há "Outro", o formulário oferece o campo de texto da própria opção.

### Seu perfil

**QST-01-P01 — Qual é o seu vínculo com o campus?** (obrigatória • uma opção)
- Estudante de graduação
- Estudante de pós-graduação
- Servidor técnico-administrativo
- Docente
- Outro

**QST-01-P02 — Com que frequência você usa quadras ou outros espaços esportivos do campus?** (obrigatória • uma opção)
- Toda semana
- Algumas vezes por mês
- Raramente
- Nunca usei

### Como é hoje

**QST-01-P03 — Como você costuma conseguir um espaço esportivo hoje?** (obrigatória • várias; marque todas que se aplicam)
- Vou até lá e vejo se está livre
- Peço pessoalmente a um servidor
- Combino por mensagem ou telefone
- Peço por e-mail ou formulário
- Outro
- Nunca precisei

**QST-01-P04 — Nos últimos 3 meses, quantas vezes você chegou a um espaço esportivo do campus e ele estava ocupado ou fechado sem que você soubesse antes?** (obrigatória • uma opção)
- Nunca
- 1 ou 2 vezes
- 3 vezes ou mais
- Não se aplica

**QST-01-P05 — Com quanta antecedência você costuma precisar saber se terá o espaço?** (obrigatória • uma opção)
- No mesmo dia
- Com 1 ou 2 dias
- De 3 a 7 dias
- Mais de 7 dias, até 30 dias
- Mais de 30 dias
- Varia muito
- Não se aplica

**QST-01-P06 — Quanto dura, em geral, o seu uso de um espaço?** (obrigatória • uma opção)
- Até 30 minutos
- Mais de 30 minutos, até 1 hora
- Mais de 1 hora, até 2 horas
- Mais de 2 horas, até 3 horas
- Mais de 3 horas
- Varia muito
- Não se aplica

**QST-01-P07 — Em que períodos você mais usa os espaços?** (obrigatória • várias; marque todos que se aplicam)
- Manhã (até 12 h)
- Tarde (das 12 h às 18 h)
- Início da noite (das 18 h às 22 h)
- Noite tardia (depois das 22 h)
- Não se aplica

**QST-01-P08 — Quando você precisa desistir de um uso combinado ou não pode comparecer, o que costuma acontecer?** (obrigatória • uma opção)
- Aviso alguém
- Não aviso
- Não sei a quem avisar
- Nunca aconteceu

### O que importa para você

**QST-01-P09 — Antes de ir ao espaço, quais destas informações são mais importantes para você? Escolha até 3.** (obrigatória • várias, no máximo 3)
- Saber se o horário está livre
- Saber se meu pedido foi aceito
- Saber quem decidiu e por quê
- Ser avisado se algo mudar
- Conhecer as regras do espaço
- Outra (descreva)

### Em suas palavras (opcionais)

**QST-01-P10 — Qual é o maior problema que você enfrenta hoje para usar um espaço esportivo do campus?** (opcional • resposta curta)
Dica sob a pergunta: *Descreva a situação, sem citar nomes de pessoas.*

**QST-01-P11 — Há algo que não perguntamos e que você acha importante?** (opcional • resposta curta)
Dica sob a pergunta: *Sem citar nomes de pessoas.*

## 3. Tabela interna — o que cada pergunta busca

**Não aparece no formulário.** Liga cada pergunta ao que ela pode confirmar ou contestar. Os IDs são os de [`visao.md`](../../visao.md#necessidades) e de [`decisoes/`](../../decisoes/README.md). "Possível necessidade nova" marca o que não tem NS hoje; a NS só nasce, se nascer, na REQ-11.

| Pergunta | Tipo | Obrigatória | O que busca |
|---|---|---|---|
| P01 | Uma opção | Sim | Contexto: quem responde (stakeholder Solicitante). Testa a [premissa P-02](../../visao.md#premissas) e a [DEC-09](../../decisoes/DEC-09.md) (servidor e docente também têm matrícula?). Não confirma NS. |
| P02 | Uma opção | Sim | Contexto: segmenta os achados por frequência de uso. Mede o quanto [NS-03](../../visao.md#necessidades) pesa para quem responde. Não confirma NS por si. |
| P03 | Várias | Sim | Prática atual para [NS-03](../../visao.md#necessidades) (pedir o uso) e [NS-05](../../visao.md#necessidades) (saber o que está livre); [DEC-11](../../decisoes/DEC-11.md). Compara com ROT-02 P01 e P02. |
| P04 | Uma opção | Sim | [NS-04](../../visao.md#necessidades) (dois usos no mesmo horário), [NS-05](../../visao.md#necessidades) e [NS-13](../../visao.md#necessidades) (saber o que impediu); [DEC-11](../../decisoes/DEC-11.md) (ver o ocupado antes de pedir). Compara com ROT-02 P04. |
| P05 | Uma opção | Sim | [DEC-07](../../decisoes/DEC-07.md): antecedência máxima de 30 dias (as opções separam "até 30 dias" de "mais de 30"); [NS-06](../../visao.md#necessidades). Compara com ROT-02 P06. |
| P06 | Uma opção | Sim | [DEC-07](../../decisoes/DEC-07.md): duração padrão de 1 h, mínimo de 30 min e máximo de 3 h (as opções separam cada limite); [NS-06](../../visao.md#necessidades). Compara com ROT-02 P05. |
| P07 | Várias | Sim | [DEC-07](../../decisoes/DEC-07.md): funcionamento das 07:00 às 00:00 por espaço ([CR-03](../../mudancas/CR-03-horario-por-espaco.md)); a opção "depois das 22 h" mostra se a noite tardia faz diferença; [NS-06](../../visao.md#necessidades). Compara com ROT-02 P07. |
| P08 | Uma opção | Sim | [NS-10](../../visao.md#necessidades) (desistir do pedido), [DEC-13](../../decisoes/DEC-13.md) e [CR-01](../../mudancas/CR-01-situacao-e-horario-da-reserva.md). "Não sei a quem avisar" e "Não aviso" indicam **possível necessidade nova** (aviso de desistência a quem decide). Compara com ROT-02 P08. |
| P09 | Várias (até 3) | Sim | "Horário livre": [NS-05](../../visao.md#necessidades) e [DEC-11](../../decisoes/DEC-11.md). "Pedido aceito": [NS-07](../../visao.md#necessidades). "Quem decidiu e por quê": [NS-07](../../visao.md#necessidades) (motivo), [NS-11](../../visao.md#necessidades) e [NS-12](../../visao.md#necessidades). "Regras do espaço": [NS-06](../../visao.md#necessidades). "Ser avisado se algo mudar": **contesta o fora do escopo** (notificações, [Visão, seção 3](../../visao.md#fora-do-escopo)) e é **possível necessidade nova**. Compara com ROT-02 P09 e P10. |
| P10 | Aberta | Não | **Possível necessidade nova**; prioridade entre as NS (QFD). Compara com ROT-02 P11. |
| P11 | Aberta | Não | **Possível necessidade nova**: o que o grupo não perguntou. |

Contagem: **11 perguntas**, 9 obrigatórias (P01 a P09) e 2 opcionais (P10 e P11); 9 fechadas e 2 abertas. O tempo estimado e a regra de corte (P11 sai primeiro se passar de 3 minutos) estão no [plano de aplicação](plano-de-aplicacao.md#tempo-de-resposta).

## 4. Decisões de escrita

- **a) Situação e necessidade, não solução.** Nenhuma pergunta cita tela, aplicativo, site ou tecnologia. A opção "Peço por e-mail ou formulário" (P03) descreve como as pessoas pedem **hoje**, e não o sistema do grupo.
- **b) Opções que cobrem os casos.** Toda pergunta fechada tem "Outro", "Não se aplica", "Nunca" ou "Varia muito" onde cabe, para ninguém ser forçado a uma opção que não é a sua.
- **c) Faixas de P05 e P06 alinhadas às regras, sem citá-las.** As opções separam os limites já adotados (30 dias; 30 min, 1 h e 3 h) para a resposta mostrar se eles batem com o uso real. Nenhuma pergunta menciona regra nem número do sistema.
- **d) Horas explícitas em P07**, para as faixas não se sobreporem.
- **e) Sem ramificação.** Quem marcou "Nunca usei" em P02 responde as demais com "Nunca", "Não se aplica" ou "Nunca precisei"; isso mantém o tempo previsível. Esses respondentes são contados à parte na síntese.
- **f) Uma resposta contraditória em P03** (por exemplo "Nunca precisei" junto com outra opção) é contada como inconsistente na síntese, e não corrigida.
