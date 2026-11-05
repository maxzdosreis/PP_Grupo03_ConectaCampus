# Requisitos funcionais e não funcionais

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **Parte da [SRS-01](srs.md) • 0.1 • Rascunho** (índice da pasta) | Autor: Max Zimmermann dos Reis • Revisor: a definir • Aprovador: a definir | `docs/fontes/requisitos/requisitos/` |

RF-xx e RNF-xx (classificados por FURPS) do Conecta Campus, derivados das necessidades da [Visão](../visao.md#necessidades) e priorizados por QFD (REQ-02). Fichas no modelo do A4·s9, agrupadas por área. Índice da fonte oficial: [README](../README.md).

| Arquivo | Conteúdo | Situação |
|---|---|---|
| [`srs.md`](srs.md) | **SRS-01**, documento principal: introdução, descrição geral, tabela-resumo dos RF, interfaces, tabela-resumo dos RNF e restrições, rastreabilidade, análise QFD, lacunas, auditoria e checklist de revisão. | 0.1 • Rascunho |
| [`rf-espacos.md`](rf-espacos.md) | RF-01 a RF-10 (17 fichas): consultar, cadastrar, editar, desativar e reativar espaços, e as recusas. | 0.1 • Rascunho |
| [`rf-reservas.md`](rf-reservas.md) | RF-11 a RF-27 (23 fichas): pedir, consultar, mudar a situação e ver o histórico de reservas, e as recusas. | 0.1 • Rascunho |
| [`rf-agenda.md`](rf-agenda.md) | RF-28 a RF-31 (6 fichas): regras de agenda e agenda do dia. | 0.1 • Rascunho |
| [`rf-contas.md`](rf-contas.md) | RF-32 a RF-37 (11 fichas): cadastro, entrada, sessão, dados próprios, sair e criação do Gestor. | 0.1 • Rascunho |
| [`rf-gerais.md`](rf-gerais.md) | RF-38 a RF-40 (3 fichas): mensagem de resultado, dados de exemplo e verificação do sistema. | 0.1 • Rascunho |
| [`rnf.md`](rnf.md) | RNF-F01 a RNF-S06 (31 fichas, por FURPS) e as restrições REST-01 a REST-08. | 0.1 • Rascunho |

Como ler as fichas (sintaxe, decomposição em `RF-xx.n`, recusas, evidência): [SRS, seção 3](srs.md#3-requisitos-funcionais). Cada ficha tem âncora própria (`rf-11-4`, `rnf-p01`) para links estáveis.

Conferência automática da rastreabilidade, da sintaxe, dos termos vagos e dos links: `python scripts/verificar_requisitos.py`, na raiz do repositório. Desde a REQ-06, cada ficha de RF tem também o campo **Código (complementar)** (`arquivo::Símbolo`), lido pela [matriz de rastreabilidade](../rastreabilidade/matriz.md), e `python scripts/gerar_rastreabilidade.py --verificar` confere que cada símbolo existe.

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Criação (REQ-01; data do commit, o arquivo não tinha histórico). Sem aprovação. |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Cabeçalho completado (REQ-06); menção ao campo Código das fichas e à matriz gerada. Sem aprovação. |
