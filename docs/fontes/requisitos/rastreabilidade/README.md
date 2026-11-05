# Rastreabilidade

| Identificação | Responsabilidade | Fonte oficial |
|---|---|---|
| **RAS-01 • 0.1 • Rascunho** (este README e os arquivos gerados desta pasta) | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha | `docs/fontes/requisitos/rastreabilidade/` |

Matriz de rastreabilidade do Conecta Campus, nos dois sentidos, da necessidade ao teste e até o código (A3·s8, A3·s25): `NS → RF → UC → US → CA/TA → endpoint ou tela → código`. Ela responde às três perguntas do professor: **impacto** (que artefatos uma mudança afeta?), **cobertura** (todo requisito tem teste?) e **justificativa** (que necessidade originou cada comportamento?). Índice da fonte oficial: [README](../README.md).

## Histórico de revisões

| Versão | Data | Autor | Alteração e referência da aprovação |
|---|---|---|---|
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Criação: matriz, cobertura, sentido inverso, RNF e mapa de impacto por DEC, gerados por `scripts/gerar_rastreabilidade.py`; decisões a) a f) e o exemplo de NS-04 (REQ-06). Sem aprovação. |

## Arquivos

Só este README é escrito à mão. Os demais são **gerados** e começam com o aviso "não edite à mão".

| Arquivo | O que mostra | Uso |
|---|---|---|
| [`matriz.md`](matriz.md) | Uma linha por RF (os 60, com os filhos): NS, RF, F1–F6, UC (passo, alternativa ou exceção), US, CA, TA, DEC, endpoint ou tela, código e a situação da cadeia. | Consulta de um requisito; "de onde veio e onde aparece". |
| [`matriz.csv`](matriz.csv) | As mesmas linhas, sem links, separadas por `;` (UTF-8 com BOM, para abrir direto numa planilha). | Tabela do `modelagem.pdf` (DOC-01) ou planilha. |
| [`cobertura.md`](cobertura.md) | Totais e percentuais por elo, por NS e por funcionalidade F1–F6; RNF por forma de verificação. | Resumo para o `modelagem.pdf` (DOC-01). |
| [`sentido-inverso.md`](sentido-inverso.md) | Cada rota da [matriz de acesso](../../matriz_de_acesso.md), cada página do frontend e cada comando → RF → NS. | Prova de que nenhum comportamento existe sem necessidade. |
| [`rnf.md`](rnf.md) | RNF → NS, RF ou DEC → forma de verificação (automatizado, medição ou manual) → evidência. | Cobertura dos RNF. |
| [`impacto-por-dec.md`](impacto-por-dec.md) | Para cada DEC: RF, RNF, UC e passos, US, CA, TA, endpoints, telas e código que mudam se a resposta for outra, com a regressão estimada. | [Pauta da Aula 7](../decisoes/pauta-aula-7.md) e seção "Mapa de impacto" de um [CR](../mudancas/modelo-cr.md). |

## Como ler a matriz

- **NS:** a primeira é a origem principal do RF; as outras são origens secundárias (campo Origem da ficha).
- **UC:** o caso de uso principal e o "como entra" exato (fluxo principal, alternativa, exceção ou transversal, com o passo, a alternativa ou a exceção da ficha), copiados da [rastreabilidade RF → UC](../casos-de-uso/README.md#rastreabilidade-rf--uc).
- **US, CA, TA:** os critérios de aceite que citam o RF, agrupados por história, e o TA de cada um; "(manual)" marca um roteiro manual.
- **Endpoint ou tela:** as rotas citadas no campo Evidência da ficha. "(do pai)" = o filho herda a rota do RF pai; "(das operações protegidas)" = a recusa comum herda as rotas das operações que ela protege.
- **Código:** o campo Código (complementar) da ficha, como `arquivo::Símbolo` (a partir de `src/backend/` para `.py`, de `src/frontend/src/` para `.ts`/`.tsx`).
- **Situação:** "completa" quando todos os elos existem; senão, qual elo falta e a lacuna ou a decisão que justifica. "ver L-xx" aponta uma lacuna da [SRS](../requisitos/srs.md#lacunas) que afeta o RF sem quebrar a cadeia.

## Exemplo de cadeia completa: NS-04 "Nunca dois usos no mesmo período"

É o exemplo da apresentação, o equivalente do `NS-01 → RF-04 → UC-01 → US-07 → CA-01…04 / TA-18…21` do professor.

| Elo | Artefato | O que diz |
|---|---|---|
| Necessidade | [NS-04](../visao.md#ns-04) | Um espaço nunca fica comprometido com dois usos que tenham algum momento em comum. |
| Requisito | [RF-11.4](../requisitos/rf-reservas.md#rf-11-4) · Recusar pedido em conflito de horário (filho do [RF-11](../requisitos/rf-reservas.md#rf-11), F5, Normal) | O sistema impede o pedido que tenha algum momento em comum com uma reserva Solicitada ou Confirmada do mesmo espaço, sem gravar nada, e informa a data, o horário e a situação da reserva que ocupa o período, sem dizer quem a pediu. |
| Caso de uso | [UC-05 Verificar disponibilidade do horário](../casos-de-uso/README.md#uc-05), incluído por UC-04: exceções [E9.1](../casos-de-uso/UC-04-solicitar-reserva.md#e9-1) (conflito com uma reserva que ocupa o horário) e [E10.1](../casos-de-uso/UC-04-solicitar-reserva.md#e10-1) (conflito descoberto na gravação, por um pedido simultâneo) | A meta não é alcançada; nenhuma reserva é criada. |
| História | [US-08 Solicitar reserva](../historias/US-08-solicitar-reserva.md) | "Como Solicitante, quero pedir um espaço … sem chocar com outro pedido." |
| Critérios de aceite | [US-08 · CA-18](../historias/US-08-solicitar-reserva.md#us-08-ca-18) e [US-08 · CA-19](../historias/US-08-solicitar-reserva.md#us-08-ca-19) | Dado/Quando/Então do conflito e do pedido simultâneo. |
| Testes de aceite | [TA-75](../historias/US-08-solicitar-reserva.md#ta-75) e [TA-76](../historias/US-08-solicitar-reserva.md#ta-76) | Automatizados. |
| Endpoint e tela (complementar) | `POST /api/reservas/` → 409 `CONFLITO_DE_HORARIO`; tela `/reservas/nova` | A [agenda do dia](../requisitos/rf-agenda.md#rf-29) mostra o período ocupado antes do envio. |
| Código (complementar) | `reservas/domain/conflito_de_horario.py::garantir_horario_livre` (a regra pura), `reservas/domain/intervalo_de_horario.py::IntervaloDeHorario.sobrepoe` (intervalo semiaberto: encostar não é conflito), `reservas/application/casos_de_uso.py::CriarReserva.executar` (consulta as reservas do dia e aplica a regra antes de gravar), `reservas/infrastructure/models.py::ReservaModel` (restrição de exclusão `reservas_reserva_sem_sobreposicao_no_espaco` no banco) e `reservas/infrastructure/repositorio_django.py::RepositorioReservasDjango.salvar` (traduz a violação da restrição para o mesmo erro do domínio) | Defesa em profundidade: a regra no domínio e a garantia final no banco, contra dois pedidos simultâneos. |
| Testes (a partir de `src/backend/`) | `reservas/tests/test_api_reservas.py::test_horario_ocupado_responde_409_e_preserva_as_reservas`, `reservas/tests/test_conflito_de_horario.py::test_sobreposicao_com_reserva_que_ocupa_horario_e_conflito`, `reservas/tests/test_repositorio_reservas.py::test_banco_barra_sobreposicao_que_escapou_da_checagem_em_codigo` e `exemplos/tests/test_carregar_dados_exemplo.py::test_horario_de_conflito_documentado_responde_409` | O último é o conflito da demonstração. A lacuna [L-07](../requisitos/srs.md#l-07) registra que o pedido simultâneo é provado por uma corrida simulada, não por duas threads. |

A linha completa está em [`matriz.md`](matriz.md#rf-11-4); no [sentido inverso](sentido-inverso.md), `POST /api/reservas/` volta para o [RF-11](matriz.md#rf-11) e a [NS-03](../visao.md#ns-03), e o RF-11.4 aparece pela herança do pai.

## Decisões de organização (REQ-06)

- <a id="decisao-a"></a>**a) Uma fonte, uma matriz gerada.** A matriz não é escrita à mão: `scripts/gerar_rastreabilidade.py` (fora do ZIP) a monta a partir dos vínculos que já estão nas fichas de RF (Origem, Decisões, Evidência e Código), na tabela RF → UC de [`casos-de-uso/`](../casos-de-uso/README.md#rastreabilidade-rf--uc), nas [histórias](../historias/README.md) (RF e TA de cada CA), na [matriz de acesso](../../matriz_de_acesso.md), nas rotas de `App.tsx` e na tabela de [lacunas](../requisitos/srs.md#lacunas). Para mudar um vínculo, muda-se a ficha de origem e roda-se o gerador. O modo `--verificar` regenera em memória e falha se um arquivo commitado estiver desatualizado: atualizar uma ficha e esquecer a matriz vira um erro apontado pelo script (o erro crítico da A4·s25).
- <a id="decisao-b"></a>**b) O elo → código é complementar.** Os slides param em CA/TA, e a pergunta se o elo até o código é esperado segue aberta (ponto 13 dos pontos a confirmar). Por isso "Endpoint ou tela" e "Código" são colunas separadas da cadeia do professor, como a Evidência das fichas. O código é citado por `arquivo::Símbolo` ou `arquivo::Classe.metodo`, no nível do caso de uso da aplicação e da regra do domínio (e da infraestrutura, quando a garantia é do banco), nunca por número de linha. A fonte é o campo **Código (complementar)** de cada ficha de RF, criado nesta tarefa, e o script confere que cada símbolo existe (com `ast` no Python e pela declaração no TypeScript).
- <a id="decisao-c"></a>**c) Os dois sentidos.** Para a frente, NS → … → TA prova que toda necessidade chega a um teste. Para trás, rota, tela ou comando → RF → NS prova que nenhum comportamento existe sem necessidade. Uma rota sem RF aparece marcada: as linhas da matriz de acesso que só existem para provar uma ausência (405 em `DELETE` ou num método não implementado) apontam para o [RNF-R05](../requisitos/rnf.md#rnf-r05) ou o [RNF-F04](../requisitos/rnf.md#rnf-f04); qualquer outra precisa de uma lacuna que cite o caminho (a tela de endereço desconhecido virou a [L-17](../requisitos/srs.md#l-17)), e nunca de um vínculo inventado.
- <a id="decisao-d"></a>**d) RNF também é rastreado**, num arquivo **gerado** ([`rnf.md`](rnf.md)), porque tudo o que ele precisa já está nas [fichas de RNF](../requisitos/rnf.md): Origem (NS, RF ou DEC) e Como verificar. A forma de verificação sai do texto: "automatizado" quando cita testes, "medição" quando usa `scripts/medir_desempenho.py` e "manual" quando está "a verificar" (a [L-09](../requisitos/srs.md#l-09)).
- <a id="decisao-e"></a>**e) Baseline: só a candidata.** Esta tarefa não aprova nada. Ela produz a [referência candidata](../baselines/conecta-campus-1.0-candidata.md): manifesto, versões exatas, decisões que faltam e o checklist de aprovação. A aprovação, a passagem para 0.2 e 1.0 e a referência Git (o commit do merge) são preenchidas por pessoas, depois.
- <a id="decisao-f"></a>**f) Versões exatas pelo conteúdo.** O manifesto traz, para cada artefato, o ID, a versão, o estado, o caminho e os 8 primeiros caracteres do SHA-256 do conteúdo, calculados pelo script. O hash é do texto com fim de linha LF, para dar o mesmo resultado no Windows (que faz o checkout em CRLF) e no Linux. O `--verificar` acusa um arquivo que mudou depois do manifesto. Assim "qual conteúdo foi acordado" não depende de "o arquivo mais novo" (A4·s2). O manifesto cobre todo `.md`, `.puml` e `.csv` da fonte oficial, menos a pasta `baselines/` (uma baseline não pode conter o próprio hash) e as imagens dos diagramas, que são geradas do `.puml` e conferidas por `scripts/verificar_casos_de_uso.py`.

Os arquivos gerados são determinísticos: mesma entrada, mesma saída, em ordem natural de ID e sem data nem hora no conteúdo; o gerador só reescreve um arquivo se o conteúdo mudou. Eles não têm histórico próprio: são "Parte da RAS-01", e o histórico é o deste README.

## Como regenerar e verificar

Na raiz do repositório (Python 3.12 ou mais novo, sem pacotes externos):

```
python scripts/gerar_rastreabilidade.py               # escreve os arquivos gerados desta pasta
python scripts/gerar_rastreabilidade.py --verificar   # regenera em memória e confere tudo
python scripts/gerar_rastreabilidade.py --manifesto   # reescreve os blocos da baseline candidata
```

O `--verificar` sai com código 1 se alguma destas falhar:

0. os arquivos gerados batem com as fontes;
1. (a) toda NS chega a pelo menos um TA, e todo RF tem UC, US e CA, ou uma justificativa registrada (lacuna ou decisão);
2. (b) todo CA tem TA, e todo teste citado num TA, num RNF ou no teste representativo da [SRS 6.4](../requisitos/srs.md#64-rf--evidência-uc-us-e-ca) existe;
3. (c) toda rota da matriz de acesso e toda página do frontend aparecem no sentido inverso com RF, RNF ou lacuna, e as tabelas de interfaces da [SRS 4.1 e 4.2](../requisitos/srs.md#4-interfaces) batem com a evidência das fichas;
4. (d) todo símbolo de código citado existe;
5. (e) toda DEC tem pergunta, opção adotada, responsável, prazo, artefatos afetados e histórico, aparece no mapa de impacto, e as histórias e o número de CAs citados nela, a [SRS 6.3](../requisitos/srs.md#63-rf-e-rnf--dec) e as contagens da [pauta](../decisoes/pauta-aula-7.md) batem com o impacto;
6. (f) todo documento da fonte oficial tem `ID • versão • estado`, autor, revisor e aprovador, e a tabela de histórico;
7. (g) os SHA-256, as versões e os estados do manifesto da candidata batem com os arquivos.

Ao mudar uma ficha, uma história ou um caso de uso: rode o gerador, depois `--verificar`, e os outros três verificadores (`verificar_requisitos.py`, `verificar_casos_de_uso.py`, `verificar_historias.py`). Ao mudar qualquer documento depois do manifesto, rode `--manifesto`: a diferença no manifesto mostra exatamente quais artefatos mudaram.
