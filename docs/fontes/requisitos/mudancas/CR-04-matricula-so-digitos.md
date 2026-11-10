# CR-04 — Matrícula só com dígitos

| Identificação | Responsabilidade |
|---|---|
| **CR-04 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha (aprovador da fonte oficial) |

Pedido de mudança aberto a partir da resposta do professor à [DEC-09](../decisoes/DEC-09.md) na Aula 7 (06/11/2026), no [modelo de CR](modelo-cr.md). Este CR foi **aplicado na especificação em 10/11/2026 (REQ-13)** (seção 8): os RF, UC, CA e TA já trazem a regra nova, com a marca \"implementação pendente (tarefa AUT-12)\". O **código não mudou**: quem o muda é a tarefa **AUT-12**, que também cria os testes de aceite e marca o CR como implementado.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Abertura a partir da DEC-09 decidida na Aula 7 (GES-02). Aprovado pelo professor, aguardando implementação na AUT-12. |
| 0.1 | 10/11/2026 | Max Zimmermann dos Reis | Aplicado na especificação (REQ-13): RF, RN, UC, histórias, CAs e TAs com a regra nova, listados na [seção 8](#8-aplicação-na-especificação-req-13). Estado: aplicado na especificação; código pendente (tarefa AUT-12). A especificação está adiante do código de propósito, e cada CA novo leva a marca "implementação pendente (tarefa AUT-12)". Sem aprovação. |

## 1. Solicitação

| Campo | Conteúdo |
|---|---|
| **Motivo** | Resposta do professor à [DEC-09](../decisoes/DEC-09.md) na Aula 7 (06/11/2026): "São números sempre, mas não tem uma quantidade máxima e uma quantidade mínima." Decisão do grupo, nos pontos que a resposta não cobriu: só dígitos; o limite de 20 caracteres fica como limite técnico (coluna do banco), não como regra da instituição. |
| **Solicitante** | O professor, como representante do cliente. |
| **Responsável** | O grupo. |
| **Estado** | **Aplicado na especificação; código pendente (tarefa AUT-12)** (10/11/2026, REQ-13). |
| **Origem** | [DEC-09](../decisoes/DEC-09.md) e lacuna [L-06](../requisitos/srs.md#l-06). |
| **Baseline vigente** | Nenhuma aprovada: a [candidata à 1.0](../baselines/conecta-campus-1.0-candidata.md) continua candidata (aprovação na REQ-07). |
| **Tarefa que implementa** | AUT-12 |

## 2. Classificação (A4·s17)

- [ ] **Editorial:** corrige o texto e mantém a obrigação; registra-se a correção.
- [x] **Comportamental:** matrículas com letras ou símbolos, hoje aceitas, passam a ser recusadas no cadastro.

## 3. Mapa de impacto

Nos dois sentidos (A4·s19). O resumo por elo vem primeiro; depois, a seção da DEC no [mapa de impacto gerado](../rastreabilidade/impacto-por-dec.md#dec-09), copiada sem mudança em 06/11/2026, e o que a regra nova acrescenta.

| Elo | Afetados | Muda o quê |
|---|---|---|
| NS | [NS-11](../visao.md#ns-11) | A identificação de quem pede passa a seguir o formato da instituição (só dígitos). |
| RF / RNF | [RF-32](../requisitos/rf-contas.md#rf-32), [RF-32.1](../requisitos/rf-contas.md#rf-32-1); nenhum RNF | RF-32.1 recusa a matrícula que não é só de dígitos; o limite de 20 fica como limite técnico. |
| UC (passo, alternativa ou exceção) | [UC-01 E3.1](../casos-de-uso/fichas-resumidas.md#uc01-e3-1); [UC-01 passos 1 a 4](../casos-de-uso/fichas-resumidas.md#uc01-p1) sem mudança | A condição de E3.1 passa a citar caractere que não é dígito. |
| US / CA | 5 CAs em 2 histórias (lista abaixo); CA novo em [US-01](../historias/US-01-criar-minha-conta.md) | [US-01 · CA-05](../historias/US-01-criar-minha-conta.md#us-01-ca-05) muda; os demais são regressão. |
| TA | 5 TAs (lista abaixo), 1 manual (TA-04) | Revisar os 5 e criar os da seção 5. |
| Endpoint ou tela (complementar) | `POST /api/auth/cadastro/`, `/cadastro` | A recusa nova no cadastro; a dica do campo matrícula, se houver. |
| Código (complementar) | `DadosDeCadastro`, `MatriculaInvalida`, `CadastrarSolicitante.executar` | `_validar_matricula` passa a exigir só dígitos; a mensagem de `MatriculaInvalida` muda; `MATRICULA_MAXIMO_CARACTERES` fica (limite técnico). |
| DEC | [DEC-09](../decisoes/DEC-09.md) | — |

### Da DEC-09 (copiado de `impacto-por-dec.md`)

- **RF:** [RF-32](../rastreabilidade/matriz.md#rf-32), [RF-32.1](../rastreabilidade/matriz.md#rf-32-1)
- **RNF:** nenhum
- **UC (passo, alternativa ou exceção):**
  - RF-32: [UC-01](../casos-de-uso/README.md#uc-01) · fluxo principal — [UC-01 passos 1 a 4](../casos-de-uso/fichas-resumidas.md#uc01-p1)
  - RF-32.1: [UC-01](../casos-de-uso/README.md#uc-01) · exceção — [UC-01 E3.1](../casos-de-uso/fichas-resumidas.md#uc01-e3-1)
- **US:** [US-01](../historias/US-01-criar-minha-conta.md), [US-02](../historias/US-02-entrar-no-sistema.md)
- **CA que dependem da DEC:** US-01: [CA-05](../historias/US-01-criar-minha-conta.md#us-01-ca-05)
- **CA dos RF afetados (regressão):** US-01: [CA-01](../historias/US-01-criar-minha-conta.md#us-01-ca-01), [CA-04](../historias/US-01-criar-minha-conta.md#us-01-ca-04), [CA-10](../historias/US-01-criar-minha-conta.md#us-01-ca-10); US-02: [CA-03](../historias/US-02-entrar-no-sistema.md#us-02-ca-03)
- **TA:** [TA-01](../historias/US-01-criar-minha-conta.md#ta-01), [TA-04 (manual)](../historias/US-01-criar-minha-conta.md#ta-04), [TA-05](../historias/US-01-criar-minha-conta.md#ta-05), [TA-10](../historias/US-01-criar-minha-conta.md#ta-10), [TA-13](../historias/US-02-entrar-no-sistema.md#ta-13)
- **Endpoint ou tela:** `POST /api/auth/cadastro/`; `/cadastro`
- **Código:** `contas/application/casos_de_uso.py::CadastrarSolicitante.executar`, `contas/domain/cadastro.py::DadosDeCadastro`, `contas/domain/excecoes.py::MatriculaInvalida`

### Acrescentado pela regra nova

- `_validar_matricula` e `MatriculaInvalida` (`contas/domain/`): regra "só dígitos" e a mensagem; `MATRICULA_MAXIMO_CARACTERES` (20) continua, agora como limite técnico das colunas `matricula` de `contas.Usuario` e `solicitante_matricula` de `reservas` (sem migration).
- Gestor criado por `createsuperuser` e pelos dados de exemplo: passam por `DadosDeCadastro`, então seguem a mesma regra; as matrículas de exemplo (`2026900`, `2026101`, `2026102`) e a do README de contas (`2026001`) já são só dígitos.
- Documentos: glossário (matrícula), [Visão](../visao.md) (P-02, R-12), README de contas e a lacuna [L-06](../requisitos/srs.md#l-06) (fecha com a AUT-12).

## 4. Diferença

Trechos atuais e propostos. O texto proposto é a referência para a AUT-12; a redação final sai no PR dela.

| Artefato | Antes | Depois |
|---|---|---|
| [RF-32.1](../requisitos/rf-contas.md#rf-32-1), enunciado | O sistema deve impedir que o visitante se cadastre sem nome, matrícula, e-mail ou senha, com nome de mais de 150 caracteres, com matrícula de mais de 20 caracteres ou com espaço no meio, ou com e-mail em formato inválido, sem criar a conta, e informar a regra violada no campo correspondente. | O sistema deve impedir que o visitante se cadastre sem nome, matrícula, e-mail ou senha, com nome de mais de 150 caracteres, com matrícula **que não seja formada só por dígitos ou de mais de 20 caracteres (limite técnico)**, ou com e-mail em formato inválido, sem criar a conta, e informar a regra violada no campo correspondente. |
| [UC-01 E3.1](../casos-de-uso/fichas-resumidas.md#uc01-e3-1), condição | Falta um dado; o nome só tem espaços ou passa de 150 caracteres; a matrícula passa de 20 caracteres ou tem espaço; o e-mail está mal formado. | Falta um dado; o nome só tem espaços ou passa de 150 caracteres; a matrícula **tem um caractere que não é dígito** ou passa de 20 caracteres (limite técnico); o e-mail está mal formado. |

**A definir na AUT-12, sem mudar a decisão:**

- Se os espaços das pontas continuam sendo removidos antes da conferência (hoje são).
- O texto da mensagem de `MatriculaInvalida`.

## 5. Critérios de aceite

Novos ou alterados, em Dado/Quando/Então ([DEC-15](../decisoes/DEC-15.md)). Entram nas histórias na AUT-12, com o TA de cada um.

#### CR-04 · CA-01 · Matrícula com letra recusada (exceção)

- **Dado** um visitante preenchendo o cadastro com os demais dados válidos
- **Quando** ele informa a matrícula "2026A01"
- **Então** o sistema informa, junto à matrícula, que ela deve ter só dígitos, e nenhuma conta é criada
- **TA:** a criar na AUT-12, junto com o CA na história.

#### CR-04 · CA-02 · Matrícula só de dígitos aceita (sucesso)

- **Dado** um visitante preenchendo o cadastro com os demais dados válidos
- **Quando** ele informa a matrícula "2026001"
- **Então** a conta é criada com o perfil Solicitante
- **TA:** a criar na AUT-12, junto com o CA na história.

#### CR-04 · CA-03 · Sem quantidade mínima (sucesso)

- **Dado** um visitante preenchendo o cadastro com os demais dados válidos
- **Quando** ele informa a matrícula "123"
- **Então** a conta é criada
- **TA:** a criar na AUT-12, junto com o CA na história.

#### CR-04 · CA-04 · Limite técnico mantido (exceção)

- **Dado** um visitante preenchendo o cadastro com os demais dados válidos
- **Quando** ele informa uma matrícula de 21 dígitos
- **Então** o sistema recusa junto à matrícula, e nenhuma conta é criada
- **TA:** a criar na AUT-12, junto com o CA na história.

## 6. Regressão

- Rever os 5 TAs listados no mapa de impacto (seção 3); o TA-04 é roteiro manual.
- Muda: [US-01 · CA-05](../historias/US-01-criar-minha-conta.md#us-01-ca-05) (a regra da matrícula).
- Não devem mudar: a conta criada com dados válidos ([US-01 · CA-01](../historias/US-01-criar-minha-conta.md#us-01-ca-01)), a volta ao ponto em que estava ([US-01 · CA-04](../historias/US-01-criar-minha-conta.md#us-01-ca-04), TA-04 manual), a matrícula já usada ([US-01 · CA-09](../historias/US-01-criar-minha-conta.md#us-01-ca-09)), o cadastro que nunca cria Gestor ([US-01 · CA-10](../historias/US-01-criar-minha-conta.md#us-01-ca-10)), o caminho de quem ainda não tem conta ([US-02 · CA-03](../historias/US-02-entrar-no-sistema.md#us-02-ca-03)) e o carregamento dos dados de exemplo.

## 7. Decisão

| Campo | Conteúdo |
|---|---|
| **Decisão** | Aceita. |
| **Quem decidiu e quando** | O professor, como representante do cliente, na Aula 7 (06/11/2026), na resposta à [DEC-09](../decisoes/DEC-09.md); registrado pelo grupo na GES-02. |
| **Justificativa** | Regra da instituição dada pelo cliente: a matrícula é sempre numérica, sem quantidade fixa de dígitos. O limite de 20 caracteres é do armazenamento, não da instituição. |
| **Referência candidata** | O manifesto da [baseline candidata](../baselines/conecta-campus-1.0-candidata.md) foi gerado de novo com a aplicação na especificação (REQ-13); a AUT-12 só marca o CR como implementado. A [baseline candidata à 1.0](../baselines/conecta-campus-1.0-candidata.md) continua candidata; a aprovação é da REQ-07. |

## 8. Aplicação na especificação (REQ-13)

Aplicado na especificação em 10/11/2026. **O código ainda não mudou**: a especificação está adiante do código de propósito, e cada critério abaixo leva a marca "implementação pendente (tarefa AUT-12)" até a tarefa AUT-12 implementar a regra e criar o teste de aceite dele. Os testes que existem hoje verificam a regra anterior, e nenhum TA novo cita um deles.

**O que mudou:**

- RF: [RF-32.1](../requisitos/rf-contas.md#rf-32-1) (enunciado e decisão) e [RF-32](../requisitos/rf-contas.md#rf-32) (decisão e vínculos).
- RN: [RN-13](../requisitos/regras-de-negocio.md#rn-13) (vigência).
- UC: [UC-01 E3.1](../casos-de-uso/fichas-resumidas.md#uc01-e3-1) (condição).
- US/CA/TA: [US-01](../historias/US-01-criar-minha-conta.md) (Conversa, INVEST, CAs e TAs).
- Documentos: [glossário](../glossario.md) (matrícula), [Visão](../visao.md) (P-02, R-12), [SRS](../requisitos/srs.md) (auditoria e lacuna L-06).

**CAs novos (4, todos com a marca "implementação pendente (tarefa AUT-12)")**

| CA | Título | Tipo | TA | Pedido do CR | Implementação |
|---|---|---|---|---|---|
| [US-01 · CA-02](../historias/US-01-criar-minha-conta.md#us-01-ca-02) | Matrícula só de dígitos aceita | sucesso | [TA-02](../historias/US-01-criar-minha-conta.md#ta-02) | CR-04 · CA-02 | implementação pendente (tarefa AUT-12) |
| [US-01 · CA-03](../historias/US-01-criar-minha-conta.md#us-01-ca-03) | Matrícula sem quantidade mínima | sucesso | [TA-03](../historias/US-01-criar-minha-conta.md#ta-03) | CR-04 · CA-03 | implementação pendente (tarefa AUT-12) |
| [US-01 · CA-06](../historias/US-01-criar-minha-conta.md#us-01-ca-06) | Matrícula com letra recusada | exceção | [TA-06](../historias/US-01-criar-minha-conta.md#ta-06) | CR-04 · CA-01 | implementação pendente (tarefa AUT-12) |
| [US-01 · CA-07](../historias/US-01-criar-minha-conta.md#us-01-ca-07) | Limite técnico da matrícula mantido | exceção | [TA-07](../historias/US-01-criar-minha-conta.md#ta-07) | CR-04 · CA-04 | implementação pendente (tarefa AUT-12) |

**CAs antigos marcados:** [US-01 · CA-05](../historias/US-01-criar-minha-conta.md#us-01-ca-05) (substituído em parte). O texto e o TA deles ficam como estavam, com a linha Situação apontando para o CA novo: descrevem a regra anterior, que o código cumpre até a tarefa AUT-12.

**Pontos que ficam abertos para a tarefa AUT-12 (nada foi decidido aqui):**

- Se os espaços das pontas continuam sendo removidos antes da conferência (hoje são).
- O texto da mensagem de matrícula inválida (o CR só diz que informa, junto à matrícula, que ela deve ter só dígitos) e se há código de erro próprio.
