# Referência candidata — Conecta Campus, Requisitos 1.0

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **BL-01 • 0.1 • Rascunho** (manifesto da baseline candidata) | Autor: Max Zimmermann dos Reis • Revisor: a definir • Aprovador: a definir | `docs/fontes/requisitos/baselines/conecta-campus-1.0-candidata.md` |

Modelo A4·s16: **baseline = manifesto + versões exatas de cada artefato + aprovação registrada + local de consulta**. Este arquivo tem o manifesto e as versões exatas; a aprovação e a referência Git ainda **não existem**. Ele é uma candidata: nada aqui está aprovado, nenhum documento mudou de estado, e salvo, commit ou push não são aprovação (A4·s14, s22–24).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Criação da referência candidata: manifesto gerado, decisões que faltam, lacunas aceitas e checklist de aprovação (REQ-06). Sem aprovação. |

## 1. Identificação

| Campo | Conteúdo |
|---|---|
| **Baseline** | Conecta Campus — Requisitos 1.0 |
| **Estado** | Candidata, aguardando aprovação |
| **Escopo** | Toda a fonte oficial `docs/fontes/requisitos/`: Visão, glossário, SRS e fichas de RF e RNF, casos de uso, histórias, decisões, mudanças e rastreabilidade (seção 2). |
| **Critério de sucesso** | CS-07 da [Visão](../visao.md#critérios-de-sucesso): os documentos chegam à versão 1.0 antes de 20/11/2026, com cada DEC decidida ou aceita como premissa. |
| **Baseline anterior** | Nenhuma (primeira baseline). |

## 2. Manifesto

Gerado por `python scripts/gerar_rastreabilidade.py --manifesto` entre os marcadores abaixo; não edite à mão. O `--verificar` acusa qualquer artefato que mude depois do manifesto, e a versão acordada é a que tem este hash, não "o arquivo mais novo". Na aprovação, todos os documentos devem estar na versão e no estado aprovados (1.0 • Aprovado), e o manifesto é gerado de novo.

<!-- manifesto:inicio -->
64 artefatos (todo `.md`, `.puml` e `.csv` de `docs/fontes/requisitos/`, menos `baselines/`). SHA-256 do conteúdo com fim de linha LF, 8 primeiros caracteres. Impressão do manifesto: `3adad9fc`.

| Artefato | ID | Versão | Estado | Caminho (a partir de `docs/fontes/requisitos/`) | SHA-256 |
|---|---|---|---|---|---|
| Requisitos do Conecta Campus — fonte oficial | IND-01 | 0.1 | Rascunho | `README.md` | `4298be3a` |
| Casos de uso | UCD-01 | 0.1 | Rascunho | `casos-de-uso/README.md` | `b5894962` |
| UC-02 · Autenticar | UC-02 | 0.1 | Rascunho | `casos-de-uso/UC-02-autenticar.md` | `2e600f5f` |
| UC-04 · Solicitar reserva | UC-04 | 0.1 | Rascunho | `casos-de-uso/UC-04-solicitar-reserva.md` | `2a5336c7` |
| UC-10 · Alterar situação da reserva {abstrato} | UC-10 | 0.1 | Rascunho | `casos-de-uso/UC-10-alterar-situacao-da-reserva.md` | `90730f68` |
| UC-14 · Cadastrar espaço | UC-14 | 0.1 | Rascunho | `casos-de-uso/UC-14-cadastrar-espaco.md` | `28c30fb5` |
| Diagrama de apoio (fonte PlantUML) | UCD-02 | 0.1 | Rascunho | `casos-de-uso/diagrama-administracao.puml` | `96bc0b4a` |
| Diagrama do negócio (fonte PlantUML) | UCD-01 | 0.1 | Rascunho | `casos-de-uso/diagrama-casos-de-uso.puml` | `270b6778` |
| Fichas resumidas dos casos de uso | UCR-01 | 0.1 | Rascunho | `casos-de-uso/fichas-resumidas.md` | `b32c63f9` |
| Fluxo de decisão de UC-04 (fonte PlantUML) | Parte de UC-04 | 0.1 | Rascunho | `casos-de-uso/fluxo-solicitar-reserva.puml` | `2764e318` |
| DEC-01 — React no frontend | DEC-01 | 0.1 | Rascunho | `decisoes/DEC-01.md` | `99a1f5ec` |
| DEC-02 — Docker e PostgreSQL na correção | DEC-02 | 0.1 | Rascunho | `decisoes/DEC-02.md` | `779aab49` |
| DEC-03 — Arquivos do Docker na estrutura do ZIP | DEC-03 | 0.1 | Rascunho | `decisoes/DEC-03.md` | `a4f3693d` |
| DEC-04 — Autenticação e perfis de acesso | DEC-04 | 0.1 | Rascunho | `decisoes/DEC-04.md` | `c7f32c72` |
| DEC-05 — Histórico só com mudanças efetivas | DEC-05 | 0.1 | Rascunho | `decisoes/DEC-05.md` | `7b81db50` |
| DEC-06 — Reservas de um espaço desativado | DEC-06 | 0.1 | Rascunho | `decisoes/DEC-06.md` | `84c47696` |
| DEC-07 — Valores das regras de agenda | DEC-07 | 0.1 | Rascunho | `decisoes/DEC-07.md` | `8d989d60` |
| DEC-08 — Cobertura-alvo dos testes | DEC-08 | 0.1 | Rascunho | `decisoes/DEC-08.md` | `b99f1b98` |
| DEC-09 — Formato da matrícula | DEC-09 | 0.1 | Rascunho | `decisoes/DEC-09.md` | `4e2cb2cc` |
| DEC-10 — Nome de espaço único | DEC-10 | 0.1 | Rascunho | `decisoes/DEC-10.md` | `f46e97da` |
| DEC-11 — Períodos ocupados por outras pessoas na agenda do dia | DEC-11 | 0.1 | Rascunho | `decisoes/DEC-11.md` | `708e0ee9` |
| DEC-12 — Metas de desempenho | DEC-12 | 0.1 | Rascunho | `decisoes/DEC-12.md` | `b250ffcc` |
| DEC-13 — Mudança de situação em relação ao horário da reserva | DEC-13 | 0.1 | Rascunho | `decisoes/DEC-13.md` | `a43208c8` |
| Decisões (DEC) | IND-02 | 0.1 | Rascunho | `decisoes/README.md` | `b6c80b96` |
| Pauta para o professor — Aula 7 (06/11/2026) | PAU-01 | 0.1 | Rascunho | `decisoes/pauta-aula-7.md` | `ae8de763` |
| Glossário do Conecta Campus | GLO-01 | 0.1 | Rascunho | `glossario.md` | `99471b6b` |
| Histórias de usuário e aceite | HIS-01 | 0.1 | Rascunho | `historias/README.md` | `195a2fae` |
| US-01 · Criar minha conta | US-01 | 0.1 | Rascunho | `historias/US-01-criar-minha-conta.md` | `04d56eca` |
| US-02 · Entrar no sistema | US-02 | 0.1 | Rascunho | `historias/US-02-entrar-no-sistema.md` | `31b10c0b` |
| US-03 · Manter e encerrar a sessão | US-03 | 0.1 | Rascunho | `historias/US-03-manter-e-encerrar-a-sessao.md` | `18c69f49` |
| US-04 · Consultar os espaços | US-04 | 0.1 | Rascunho | `historias/US-04-consultar-os-espacos.md` | `0534fae6` |
| US-05 · Cadastrar espaço | US-05 | 0.1 | Rascunho | `historias/US-05-cadastrar-espaco.md` | `2723c216` |
| US-06 · Editar espaço | US-06 | 0.1 | Rascunho | `historias/US-06-editar-espaco.md` | `efde3c76` |
| US-07 · Desativar e reativar espaço | US-07 | 0.1 | Rascunho | `historias/US-07-desativar-e-reativar-espaco.md` | `0802693e` |
| US-08 · Solicitar reserva | US-08 | 0.1 | Rascunho | `historias/US-08-solicitar-reserva.md` | `79b7befc` |
| US-09 · Ver a agenda do dia antes de pedir | US-09 | 0.1 | Rascunho | `historias/US-09-ver-a-agenda-do-dia.md` | `a951d909` |
| US-10 · Acompanhar minhas reservas | US-10 | 0.1 | Rascunho | `historias/US-10-acompanhar-minhas-reservas.md` | `3ea73593` |
| US-11 · Acompanhar todas as reservas | US-11 | 0.1 | Rascunho | `historias/US-11-acompanhar-todas-as-reservas.md` | `eb7a884c` |
| US-12 · Ver o detalhe e o histórico de uma reserva | US-12 | 0.1 | Rascunho | `historias/US-12-ver-detalhe-e-historico.md` | `b83946a0` |
| US-13 · Cancelar uma reserva | US-13 | 0.1 | Rascunho | `historias/US-13-cancelar-uma-reserva.md` | `db71b540` |
| US-14 · Confirmar uma reserva | US-14 | 0.1 | Rascunho | `historias/US-14-confirmar-uma-reserva.md` | `069e869e` |
| US-15 · Recusar uma reserva com motivo | US-15 | 0.1 | Rascunho | `historias/US-15-recusar-uma-reserva.md` | `da6a0cca` |
| US-16 · Concluir uma reserva | US-16 | 0.1 | Rascunho | `historias/US-16-concluir-uma-reserva.md` | `53ff3dfb` |
| US-17 · Criar o primeiro Gestor | US-17 | 0.1 | Rascunho | `historias/US-17-criar-o-primeiro-gestor.md` | `a1d33d4c` |
| US-18 · Carregar os dados de exemplo | US-18 | 0.1 | Rascunho | `historias/US-18-carregar-os-dados-de-exemplo.md` | `dbd4e5ea` |
| US-19 · Verificar se o sistema está no ar | US-19 | 0.1 | Rascunho | `historias/US-19-verificar-se-o-sistema-esta-no-ar.md` | `e040cc35` |
| Pedidos de mudança | IND-03 | 0.1 | Rascunho | `mudancas/README.md` | `349252dd` |
| Modelo de pedido de mudança (CR) | MCR-01 | 0.1 | Rascunho | `mudancas/modelo-cr.md` | `34f1a420` |
| Rastreabilidade | RAS-01 | 0.1 | Rascunho | `rastreabilidade/README.md` | `75ff3b11` |
| Cobertura da rastreabilidade | Parte da RAS-01 | 0.1 | Rascunho | `rastreabilidade/cobertura.md` | `e2377700` |
| Mapa de impacto por decisão (DEC) | Parte da RAS-01 | 0.1 | Rascunho | `rastreabilidade/impacto-por-dec.md` | `f059ef97` |
| Matriz de rastreabilidade (planilha, gerada) | Parte da RAS-01 | 0.1 | Rascunho | `rastreabilidade/matriz.csv` | `fb012d27` |
| Matriz de rastreabilidade (NS → RF → UC → US → CA/TA → endpoint ou tela → código) | Parte da RAS-01 | 0.1 | Rascunho | `rastreabilidade/matriz.md` | `38f8d385` |
| Rastreabilidade dos RNF (RNF → NS, RF ou DEC → forma de verificação → evidência) | Parte da RAS-01 | 0.1 | Rascunho | `rastreabilidade/rnf.md` | `2047720d` |
| Rastreabilidade no sentido inverso (rota ou tela → RF → NS) | Parte da RAS-01 | 0.1 | Rascunho | `rastreabilidade/sentido-inverso.md` | `b37d636f` |
| Requisitos funcionais e não funcionais | Parte da SRS-01 | 0.1 | Rascunho | `requisitos/README.md` | `d5ad6cb3` |
| Requisitos funcionais — Regras de agenda e agenda do dia | Parte da SRS-01 | 0.1 | Rascunho | `requisitos/rf-agenda.md` | `1dda723d` |
| Requisitos funcionais — Contas e acesso | Parte da SRS-01 | 0.1 | Rascunho | `requisitos/rf-contas.md` | `e8c07d00` |
| Requisitos funcionais — Espaços | Parte da SRS-01 | 0.1 | Rascunho | `requisitos/rf-espacos.md` | `5ab26ddf` |
| Requisitos funcionais — Mensagens e operação | Parte da SRS-01 | 0.1 | Rascunho | `requisitos/rf-gerais.md` | `cdbfc521` |
| Requisitos funcionais — Reservas | Parte da SRS-01 | 0.1 | Rascunho | `requisitos/rf-reservas.md` | `bafa05f6` |
| Requisitos não funcionais (FURPS) e restrições | Parte da SRS-01 | 0.1 | Rascunho | `requisitos/rnf.md` | `2d4a4494` |
| Especificação de Requisitos de Software (SRS) — Conecta Campus | SRS-01 | 0.1 | Rascunho | `requisitos/srs.md` | `43fcaee4` |
| Documento de Visão — Conecta Campus | VIS-01 | 0.1 | Rascunho | `visao.md` | `9574b097` |
<!-- manifesto:fim -->

## 3. Decisões que ainda faltam

Pelo CS-07, cada DEC abaixo precisa estar **decidida** ou **aceita como premissa** antes da aprovação. Perguntas, opções e impacto: [pauta da Aula 7](../decisoes/pauta-aula-7.md).

<!-- decisoes:inicio -->
| DEC | Título | Estado | Prazo | CAs afetados | Na pauta |
|---|---|---|---|---|---|
| [DEC-05](../decisoes/DEC-05.md) | Histórico só com mudanças efetivas | Adotada provisoriamente | 06/11/2026 (Aula 7). | [10](../rastreabilidade/impacto-por-dec.md#dec-05) | [pauta](../decisoes/pauta-aula-7.md#dec-05) |
| [DEC-06](../decisoes/DEC-06.md) | Reservas de um espaço desativado | Adotada provisoriamente | 06/11/2026 (Aula 7). | [14](../rastreabilidade/impacto-por-dec.md#dec-06) | [pauta](../decisoes/pauta-aula-7.md#dec-06) |
| [DEC-07](../decisoes/DEC-07.md) | Valores das regras de agenda | Adotada provisoriamente | 06/11/2026 (Aula 7). | [10](../rastreabilidade/impacto-por-dec.md#dec-07) | [pauta](../decisoes/pauta-aula-7.md#dec-07) |
| [DEC-08](../decisoes/DEC-08.md) | Cobertura-alvo dos testes | Adotada provisoriamente | 13/11/2026. | [0](../rastreabilidade/impacto-por-dec.md#dec-08) | [pauta](../decisoes/pauta-aula-7.md#dec-08) |
| [DEC-09](../decisoes/DEC-09.md) | Formato da matrícula | Adotada provisoriamente | 06/11/2026 (Aula 7). | [5](../rastreabilidade/impacto-por-dec.md#dec-09) | [pauta](../decisoes/pauta-aula-7.md#dec-09) |
| [DEC-10](../decisoes/DEC-10.md) | Nome de espaço único | Adotada provisoriamente | 06/11/2026 (Aula 7). | [6](../rastreabilidade/impacto-por-dec.md#dec-10) | [pauta](../decisoes/pauta-aula-7.md#dec-10) |
| [DEC-11](../decisoes/DEC-11.md) | Períodos ocupados por outras pessoas na agenda do dia | Adotada provisoriamente | 06/11/2026 (Aula 7). | [5](../rastreabilidade/impacto-por-dec.md#dec-11) | [pauta](../decisoes/pauta-aula-7.md#dec-11) |
| [DEC-12](../decisoes/DEC-12.md) | Metas de desempenho | Adotada provisoriamente | 13/11/2026. | [0](../rastreabilidade/impacto-por-dec.md#dec-12) | [pauta](../decisoes/pauta-aula-7.md#dec-12) |
| [DEC-13](../decisoes/DEC-13.md) | Mudança de situação em relação ao horário da reserva | Adotada provisoriamente | 06/11/2026 (Aula 7). | [21](../rastreabilidade/impacto-por-dec.md#dec-13) | [pauta](../decisoes/pauta-aula-7.md#dec-13) |
<!-- decisoes:fim -->

Também abertos: os pontos a confirmar 4, 5, 6, 10 e 13 de `.claude/requisitos.md` e 4 e 5 de `CLAUDE.md` ([índice das decisões](../decisoes/README.md#pontos-a-confirmar-ainda-abertos)).

## 4. Lacunas aceitas

Lacunas da [SRS](../requisitos/srs.md#lacunas) com proposta "aceitar" (no todo ou em parte), que a baseline registra e com as quais convive. As de proposta "DEC" estão na seção 3.

<!-- lacunas:inicio -->
| Lacuna | Tipo | Afeta |
|---|---|---|
| [L-03](../requisitos/srs.md#l-03) | RNF ausente | RF-33; NS-11 |
| [L-04](../requisitos/srs.md#l-04) | RNF ausente | RF-36; RNF-F03 |
| [L-05](../requisitos/srs.md#l-05) | Comportamento | RF-12; RNF-P01 |
| [L-07](../requisitos/srs.md#l-07) | RF/RNF sem teste | RNF-R01; RF-11.4 |
| [L-08](../requisitos/srs.md#l-08) | RF sem teste | RF-40; US-19 · CA-02 (TA-156, roteiro manual, REQ-05) |
| [L-09](../requisitos/srs.md#l-09) | RNF sem verificação automática | RNF-U02 a RNF-U05, RNF-S01, RNF-S06 |
| [L-10](../requisitos/srs.md#l-10) | Comportamento sem NS | RNF-F11; RF-37; RF-11, RF-12; Visão |
| [L-12](../requisitos/srs.md#l-12) | RF × comportamento | RF-11, RF-11.1; UC-04 |
| [L-13](../requisitos/srs.md#l-13) | RF incompleto | RF-17, RF-19, RF-26; UC-10 |
| [L-14](../requisitos/srs.md#l-14) | Comportamento sem RF | RF-33, RF-33.1; UC-02 |
| [L-15](../requisitos/srs.md#l-15) | CA sem TA automatizado | RF-32; UC-01 A1.1; US-01 |
| [L-16](../requisitos/srs.md#l-16) | CA sem TA automatizado | RF-37; UC-20 E2.1; US-17 |
| [L-17](../requisitos/srs.md#l-17) | Comportamento sem RF | Telas; NS-13 |
<!-- lacunas:fim -->

## 5. Checklist de aprovação

Preenchido por pessoas; nada aqui é marcado por um script. Itens do A4·s28 ("antes de chamar de versão oficial").

| # | Item | Feito? | Quem • Data • Evidência |
|---|---|---|---|
| 1 | Revisão por pares de cada documento feita (checklists da [Visão](../visao.md#5-checklist-de-revisão-por-pares) e da [SRS](../requisitos/srs.md#10-checklist-de-revisão-por-pares)), e cada documento passou para **0.2 • Em revisão** com a linha no histórico. | | |
| 2 | Cada DEC da seção 3 **decidida** ou **aceita como premissa** (CS-07), com o estado e a data na DEC; respostas diferentes da opção adotada passaram por [CR](../mudancas/modelo-cr.md). | | |
| 3 | As lacunas da seção 4 revistas e aceitas pelo aprovador; as verificações manuais da [L-09](../requisitos/srs.md#l-09) e os TA manuais (TA-02, TA-149, TA-156) executados no ensaio e registrados. | | |
| 4 | Verificações passando: `python scripts/verificar_requisitos.py`, `python scripts/verificar_casos_de_uso.py`, `python scripts/verificar_historias.py` e `python scripts/gerar_rastreabilidade.py --verificar`. | | |
| 5 | Documentos em **1.0 • Aprovado**, manifesto gerado de novo (`--manifesto`) e conferido. | | |
| 6 | Aprovação registrada: quem aprovou (aprovador da fonte oficial), quando e a referência (seção 6). | | |

## 6. Aprovação e local de consulta

| Campo | Conteúdo |
|---|---|
| **Aprovado por** | a preencher |
| **Data** | a preencher |
| **Referência da aprovação** | a preencher (ex.: ata, mensagem registrada ou PR aprovado) |
| **Referência Git** | a preencher no merge (hash do commit de merge na `main` e tag, se houver) |
| **Local de consulta** | Este diretório da fonte oficial no repositório e, na entrega, a cópia que for no ZIP (DOC-07); os PDFs gerados daqui servem só para consulta e mostram a versão e a origem. |

Quando uma baseline aprovada for substituída, esta fica preservada e marcada como **Substituída**, com o link para a nova (A4·s26).
