# Referência candidata — Conecta Campus, Requisitos 1.0

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **BL-01 • 0.1 • Rascunho** (manifesto da baseline candidata) | Autor: Max Zimmermann dos Reis • Revisor: a definir • Aprovador: a definir | `docs/fontes/requisitos/baselines/conecta-campus-1.0-candidata.md` |

Modelo A4·s16: **baseline = manifesto + versões exatas de cada artefato + aprovação registrada + local de consulta**. Este arquivo tem o manifesto e as versões exatas; a aprovação e a referência Git ainda **não existem**. Ele é uma candidata: nada aqui está aprovado, nenhum documento mudou de estado, e salvo, commit ou push não são aprovação (A4·s14, s22–24).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Criação da referência candidata: manifesto gerado, decisões que faltam, lacunas aceitas e checklist de aprovação (REQ-06). Sem aprovação. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Respostas da Aula 7 (GES-02): nenhuma DEC aberta (o bloco gerado fica vazio), só o ponto 4 do `CLAUDE.md` segue aberto, evidência do item 2 do checklist e manifesto gerado de novo. A baseline continua candidata. Sem aprovação. |
| 0.1 | 07/11/2026 | Max Zimmermann dos Reis | AUT-08: a L-03 sai das lacunas aceitas (resolvida pelo RF-33.2 e pelo RNF-F12) e o manifesto é gerado de novo. A baseline continua candidata. Sem aprovação. |
| 0.1 | 08/11/2026 | Max Zimmermann dos Reis | Renumeração dos TAs: TA-19 e TA-20 passam a TA-20 e TA-21, e TA-21 a TA-158 passam a TA-24 a TA-161, para os TA-19, TA-22 e TA-23 novos da US-03 (revogação e troca da credencial de renovação) seguirem a ordem das histórias (AUT-09). Mudança editorial, sem nova obrigação. Sem aprovação. |

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
78 artefatos (todo `.md`, `.puml` e `.csv` de `docs/fontes/requisitos/`, menos `baselines/`). SHA-256 do conteúdo com fim de linha LF, 8 primeiros caracteres. Impressão do manifesto: `20492527`.

| Artefato | ID | Versão | Estado | Caminho (a partir de `docs/fontes/requisitos/`) | SHA-256 |
|---|---|---|---|---|---|
| Requisitos do Conecta Campus — fonte oficial | IND-01 | 0.1 | Rascunho | `README.md` | `8ea924c6` |
| Casos de uso | UCD-01 | 0.1 | Rascunho | `casos-de-uso/README.md` | `00d85e7e` |
| UC-02 · Autenticar | UC-02 | 0.1 | Rascunho | `casos-de-uso/UC-02-autenticar.md` | `9782c01f` |
| UC-04 · Solicitar reserva | UC-04 | 0.1 | Rascunho | `casos-de-uso/UC-04-solicitar-reserva.md` | `21c8cffc` |
| UC-10 · Alterar situação da reserva {abstrato} | UC-10 | 0.1 | Rascunho | `casos-de-uso/UC-10-alterar-situacao-da-reserva.md` | `90730f68` |
| UC-14 · Cadastrar espaço | UC-14 | 0.1 | Rascunho | `casos-de-uso/UC-14-cadastrar-espaco.md` | `28c30fb5` |
| Diagrama de apoio (fonte PlantUML) | UCD-02 | 0.1 | Rascunho | `casos-de-uso/diagrama-administracao.puml` | `96bc0b4a` |
| Diagrama do negócio (fonte PlantUML) | UCD-01 | 0.1 | Rascunho | `casos-de-uso/diagrama-casos-de-uso.puml` | `270b6778` |
| Fichas resumidas dos casos de uso | UCR-01 | 0.1 | Rascunho | `casos-de-uso/fichas-resumidas.md` | `c07ffe4f` |
| Fluxo de decisão de UC-04 (fonte PlantUML) | Parte de UC-04 | 0.1 | Rascunho | `casos-de-uso/fluxo-solicitar-reserva.puml` | `685dc440` |
| DEC-01 — React no frontend | DEC-01 | 0.1 | Rascunho | `decisoes/DEC-01.md` | `9dd0f8c4` |
| DEC-02 — Docker e PostgreSQL na correção | DEC-02 | 0.1 | Rascunho | `decisoes/DEC-02.md` | `779aab49` |
| DEC-03 — Arquivos do Docker na estrutura do ZIP | DEC-03 | 0.1 | Rascunho | `decisoes/DEC-03.md` | `a4f3693d` |
| DEC-04 — Autenticação e perfis de acesso | DEC-04 | 0.1 | Rascunho | `decisoes/DEC-04.md` | `9525d234` |
| DEC-05 — Histórico só com mudanças efetivas | DEC-05 | 0.1 | Rascunho | `decisoes/DEC-05.md` | `ea290c83` |
| DEC-06 — Reservas de um espaço desativado | DEC-06 | 0.1 | Rascunho | `decisoes/DEC-06.md` | `ec4d6d0a` |
| DEC-07 — Valores das regras de agenda | DEC-07 | 0.1 | Rascunho | `decisoes/DEC-07.md` | `5de23737` |
| DEC-08 — Cobertura-alvo dos testes | DEC-08 | 0.1 | Rascunho | `decisoes/DEC-08.md` | `6097c9fa` |
| DEC-09 — Formato da matrícula | DEC-09 | 0.1 | Rascunho | `decisoes/DEC-09.md` | `47e157b0` |
| DEC-10 — Nome de espaço único | DEC-10 | 0.1 | Rascunho | `decisoes/DEC-10.md` | `177a8842` |
| DEC-11 — Períodos ocupados por outras pessoas na agenda do dia | DEC-11 | 0.1 | Rascunho | `decisoes/DEC-11.md` | `afc4ac01` |
| DEC-12 — Metas de desempenho | DEC-12 | 0.1 | Rascunho | `decisoes/DEC-12.md` | `0016999a` |
| DEC-13 — Mudança de situação em relação ao horário da reserva | DEC-13 | 0.1 | Rascunho | `decisoes/DEC-13.md` | `fd3891a7` |
| DEC-14 — Alternativas e exceções nos casos de uso | DEC-14 | 0.1 | Rascunho | `decisoes/DEC-14.md` | `7d93edb1` |
| DEC-15 — Critérios de aceite em Dado/Quando/Então | DEC-15 | 0.1 | Rascunho | `decisoes/DEC-15.md` | `dafe499b` |
| DEC-16 — Rastreabilidade até o código | DEC-16 | 0.1 | Rascunho | `decisoes/DEC-16.md` | `c2a38b52` |
| DEC-17 — Convenção de versão dos documentos | DEC-17 | 0.1 | Rascunho | `decisoes/DEC-17.md` | `ca24428b` |
| DEC-18 — Index Card das histórias | DEC-18 | 0.1 | Rascunho | `decisoes/DEC-18.md` | `20cd8280` |
| DEC-19 — Outros diagramas além dos casos de uso | DEC-19 | 0.1 | Rascunho | `decisoes/DEC-19.md` | `26a250ce` |
| DEC-20 — Entrega separada dos documentos de Requisitos | DEC-20 | 0.1 | Rascunho | `decisoes/DEC-20.md` | `7ce451dc` |
| DEC-21 — Capa do modelagem.pdf | DEC-21 | 0.1 | Rascunho | `decisoes/DEC-21.md` | `9534846a` |
| DEC-22 — Modelo do contribuicoes.pdf | DEC-22 | 0.1 | Rascunho | `decisoes/DEC-22.md` | `e3cbd2cb` |
| DEC-23 — Apresentação | DEC-23 | 0.1 | Rascunho | `decisoes/DEC-23.md` | `decc0d59` |
| Decisões (DEC) | IND-02 | 0.1 | Rascunho | `decisoes/README.md` | `71027319` |
| Pauta para o professor — Aula 7 (06/11/2026) | PAU-01 | 0.1 | Rascunho | `decisoes/pauta-aula-7.md` | `6a927e94` |
| Glossário do Conecta Campus | GLO-01 | 0.1 | Rascunho | `glossario.md` | `1ae6d340` |
| Histórias de usuário e aceite | HIS-01 | 0.1 | Rascunho | `historias/README.md` | `085a44ac` |
| US-01 · Criar minha conta | US-01 | 0.1 | Rascunho | `historias/US-01-criar-minha-conta.md` | `04d56eca` |
| US-02 · Entrar no sistema | US-02 | 0.1 | Rascunho | `historias/US-02-entrar-no-sistema.md` | `574bd4d5` |
| US-03 · Manter e encerrar a sessão | US-03 | 0.1 | Rascunho | `historias/US-03-manter-e-encerrar-a-sessao.md` | `d5004272` |
| US-04 · Consultar os espaços | US-04 | 0.1 | Rascunho | `historias/US-04-consultar-os-espacos.md` | `70576408` |
| US-05 · Cadastrar espaço | US-05 | 0.1 | Rascunho | `historias/US-05-cadastrar-espaco.md` | `ebcde254` |
| US-06 · Editar espaço | US-06 | 0.1 | Rascunho | `historias/US-06-editar-espaco.md` | `362b8861` |
| US-07 · Desativar e reativar espaço | US-07 | 0.1 | Rascunho | `historias/US-07-desativar-e-reativar-espaco.md` | `0c7f1975` |
| US-08 · Solicitar reserva | US-08 | 0.1 | Rascunho | `historias/US-08-solicitar-reserva.md` | `97ea2ba9` |
| US-09 · Ver a agenda do dia antes de pedir | US-09 | 0.1 | Rascunho | `historias/US-09-ver-a-agenda-do-dia.md` | `cc8bb6a6` |
| US-10 · Acompanhar minhas reservas | US-10 | 0.1 | Rascunho | `historias/US-10-acompanhar-minhas-reservas.md` | `63920ab0` |
| US-11 · Acompanhar todas as reservas | US-11 | 0.1 | Rascunho | `historias/US-11-acompanhar-todas-as-reservas.md` | `ca762024` |
| US-12 · Ver o detalhe e o histórico de uma reserva | US-12 | 0.1 | Rascunho | `historias/US-12-ver-detalhe-e-historico.md` | `19d71d83` |
| US-13 · Cancelar uma reserva | US-13 | 0.1 | Rascunho | `historias/US-13-cancelar-uma-reserva.md` | `0c94cc48` |
| US-14 · Confirmar uma reserva | US-14 | 0.1 | Rascunho | `historias/US-14-confirmar-uma-reserva.md` | `2f2a3e82` |
| US-15 · Recusar uma reserva com motivo | US-15 | 0.1 | Rascunho | `historias/US-15-recusar-uma-reserva.md` | `afcdd770` |
| US-16 · Concluir uma reserva | US-16 | 0.1 | Rascunho | `historias/US-16-concluir-uma-reserva.md` | `81898601` |
| US-17 · Criar o primeiro Gestor | US-17 | 0.1 | Rascunho | `historias/US-17-criar-o-primeiro-gestor.md` | `c9d6b4be` |
| US-18 · Carregar os dados de exemplo | US-18 | 0.1 | Rascunho | `historias/US-18-carregar-os-dados-de-exemplo.md` | `d84907c5` |
| US-19 · Verificar se o sistema está no ar | US-19 | 0.1 | Rascunho | `historias/US-19-verificar-se-o-sistema-esta-no-ar.md` | `90700095` |
| CR-01 — Mudança de situação em relação ao horário da reserva | CR-01 | 0.1 | Rascunho | `mudancas/CR-01-situacao-e-horario-da-reserva.md` | `dde4b058` |
| CR-02 — Tentativas recusadas no histórico da reserva | CR-02 | 0.1 | Rascunho | `mudancas/CR-02-tentativas-recusadas-no-historico.md` | `b1d6812e` |
| CR-03 — Horário de funcionamento por espaço e duração sugerida | CR-03 | 0.1 | Rascunho | `mudancas/CR-03-horario-por-espaco.md` | `58751e99` |
| CR-04 — Matrícula só com dígitos | CR-04 | 0.1 | Rascunho | `mudancas/CR-04-matricula-so-digitos.md` | `5a873597` |
| Pedidos de mudança | IND-03 | 0.1 | Rascunho | `mudancas/README.md` | `b33ea02c` |
| Modelo de pedido de mudança (CR) | MCR-01 | 0.1 | Rascunho | `mudancas/modelo-cr.md` | `1352f732` |
| Rastreabilidade | RAS-01 | 0.1 | Rascunho | `rastreabilidade/README.md` | `47fe095b` |
| Cobertura da rastreabilidade | Parte da RAS-01 | 0.1 | Rascunho | `rastreabilidade/cobertura.md` | `6f316f6b` |
| Mapa de impacto por decisão (DEC) | Parte da RAS-01 | 0.1 | Rascunho | `rastreabilidade/impacto-por-dec.md` | `b547ac2b` |
| Matriz de rastreabilidade (planilha, gerada) | Parte da RAS-01 | 0.1 | Rascunho | `rastreabilidade/matriz.csv` | `64a10503` |
| Matriz de rastreabilidade (NS → RF → UC → US → CA/TA → endpoint ou tela → código) | Parte da RAS-01 | 0.1 | Rascunho | `rastreabilidade/matriz.md` | `d26070bc` |
| Rastreabilidade dos RNF (RNF → NS, RF ou DEC → forma de verificação → evidência) | Parte da RAS-01 | 0.1 | Rascunho | `rastreabilidade/rnf.md` | `74a0b8e6` |
| Rastreabilidade no sentido inverso (rota ou tela → RF → NS) | Parte da RAS-01 | 0.1 | Rascunho | `rastreabilidade/sentido-inverso.md` | `ff169372` |
| Requisitos funcionais e não funcionais | Parte da SRS-01 | 0.1 | Rascunho | `requisitos/README.md` | `d5ad6cb3` |
| Requisitos funcionais — Regras de agenda e agenda do dia | Parte da SRS-01 | 0.1 | Rascunho | `requisitos/rf-agenda.md` | `8d8d0cd4` |
| Requisitos funcionais — Contas e acesso | Parte da SRS-01 | 0.1 | Rascunho | `requisitos/rf-contas.md` | `f9343cc5` |
| Requisitos funcionais — Espaços | Parte da SRS-01 | 0.1 | Rascunho | `requisitos/rf-espacos.md` | `16cf4785` |
| Requisitos funcionais — Mensagens e operação | Parte da SRS-01 | 0.1 | Rascunho | `requisitos/rf-gerais.md` | `a549018f` |
| Requisitos funcionais — Reservas | Parte da SRS-01 | 0.1 | Rascunho | `requisitos/rf-reservas.md` | `5d86ec33` |
| Requisitos não funcionais (FURPS) e restrições | Parte da SRS-01 | 0.1 | Rascunho | `requisitos/rnf.md` | `30763109` |
| Especificação de Requisitos de Software (SRS) — Conecta Campus | SRS-01 | 0.1 | Rascunho | `requisitos/srs.md` | `213feff2` |
| Documento de Visão — Conecta Campus | VIS-01 | 0.1 | Rascunho | `visao.md` | `f75a238b` |
<!-- manifesto:fim -->

## 3. Decisões que ainda faltam

Pelo CS-07, cada DEC abaixo precisa estar **decidida** ou **aceita como premissa** antes da aprovação. Perguntas, opções e impacto: [pauta da Aula 7](../decisoes/pauta-aula-7.md).

<!-- decisoes:inicio -->
| DEC | Título | Estado | Prazo | CAs afetados | Na pauta |
|---|---|---|---|---|---|
<!-- decisoes:fim -->

Nenhuma DEC aberta: as DEC-05 a DEC-13 foram decididas na Aula 7 (06/11/2026), e os pontos a confirmar respondidos e as respostas sobre entrega e apresentação viraram as DEC-14 a DEC-23 ([resultado](../decisoes/pauta-aula-7.md#resultado)). As respostas que mudam o comportamento viraram os [CR-01 a CR-04](../mudancas/README.md#índice), aprovados e aguardando implementação. Segue aberto só o ponto 4 do `CLAUDE.md` (composição do grupo nas duas disciplinas), que não foi perguntado ([índice das decisões](../decisoes/README.md#pontos-a-confirmar-ainda-abertos)).

## 4. Lacunas aceitas

Lacunas da [SRS](../requisitos/srs.md#lacunas) com proposta "aceitar" (no todo ou em parte), que a baseline registra e com as quais convive. As de proposta "DEC" estão na seção 3.

<!-- lacunas:inicio -->
| Lacuna | Tipo | Afeta |
|---|---|---|
| [L-04](../requisitos/srs.md#l-04) | RNF ausente | RF-36; RNF-F03; RNF-F13 |
| [L-05](../requisitos/srs.md#l-05) | Comportamento | RF-12; RNF-P01 |
| [L-07](../requisitos/srs.md#l-07) | RF/RNF sem teste | RNF-R01; RF-11.4 |
| [L-08](../requisitos/srs.md#l-08) | RF sem teste | RF-40; US-19 · CA-02 (TA-160, roteiro manual, REQ-05) |
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
| 2 | Cada DEC da seção 3 **decidida** ou **aceita como premissa** (CS-07), com o estado e a data na DEC; respostas diferentes da opção adotada passaram por [CR](../mudancas/modelo-cr.md). | Em parte: decididas; os CRs ainda não foram aplicados | Max Zimmermann dos Reis • 06/11/2026 • DEC-05 a DEC-13 decididas na Aula 7 ([resultado](../decisoes/pauta-aula-7.md#resultado)); CR-01 a CR-04 aprovados, aguardando RES-11, RES-12, ESP-07 e AUT-12 |
| 3 | As lacunas da seção 4 revistas e aceitas pelo aprovador; as verificações manuais da [L-09](../requisitos/srs.md#l-09) e os TA manuais (TA-02, TA-152, TA-159) executados no ensaio e registrados. | | |
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
