# Cobertura da rastreabilidade

> Gerado por `scripts/gerar_rastreabilidade.py`, não edite à mão; para mudar um vínculo, mude a ficha de origem.

| Identificação | Responsabilidade |
|---|---|
| **Parte da [RAS-01](README.md) • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

Resumo da [matriz](matriz.md) para o `modelagem.pdf` (DOC-01). As contagens por NS usam todas as NS citadas na Origem de cada RF (a principal e as secundárias), por isso um RF pode contar em mais de uma NS.

## Por elo

| Elo | Com o elo | Total | % |
|---|---|---|---|
| NS com pelo menos um RF | 16 | 17 | 94% |
| NS que chegam a um TA | 16 | 17 | 94% |
| RF com NS de origem | 70 | 70 | 100% |
| RN com pelo menos um RF | 19 | 19 | 100% |
| RF com UC (sem o transversal) | 69 | 69 | 100% |
| RF com US e CA (sem o transversal) | 69 | 69 | 100% |
| CA com TA | 208 | 208 | 100% |
| TA automatizados | 205 | 208 | 99% |
| TA manuais (roteiro) | 3 | 208 | 1% |
| TA pendentes (regra decidida, código na tarefa citada) | 0 | 208 | 0% |
| RF com endpoint ou tela | 69 | 70 | 99% |
| RF com código citado | 70 | 70 | 100% |
| RF com a cadeia completa | 69 | 70 | 99% |

TA manuais: TA-04, TA-181, TA-188 (ver as lacunas de CA sem TA automatizado na [SRS](../requisitos/srs.md#lacunas)).

TA pendentes: nenhum (a especificação está adiante do código de propósito; cada um aponta para a tarefa que o implementa).

## Por necessidade (NS)

| NS | RF (principal) | RF (todas as citações) | UC | US | CA | TA (manuais) |
|---|---|---|---|---|---|---|
| [NS-01](../visao.md#ns-01) | 6 | 7 | 2 | 4 | 17 | 17 (0) |
| [NS-02](../visao.md#ns-02) | 10 | 13 | 5 | 6 | 33 | 33 (0) |
| [NS-03](../visao.md#ns-03) | 3 | 4 | 2 | 1 | 15 | 15 (0) |
| [NS-04](../visao.md#ns-04) | 1 | 1 | 1 | 1 | 2 | 2 (0) |
| [NS-05](../visao.md#ns-05) | 5 | 5 | 1 | 1 | 10 | 10 (0) |
| [NS-06](../visao.md#ns-06) | 3 | 4 | 3 | 2 | 14 | 14 (0) |
| [NS-07](../visao.md#ns-07) | 2 | 5 | 3 | 5 | 21 | 21 (0) |
| [NS-08](../visao.md#ns-08) | 4 | 5 | 2 | 3 | 17 | 17 (0) |
| [NS-09](../visao.md#ns-09) | 9 | 10 | 7 | 9 | 41 | 41 (0) |
| [NS-10](../visao.md#ns-10) | 1 | 3 | 3 | 7 | 15 | 15 (0) |
| [NS-11](../visao.md#ns-11) | 14 | 21 | 8 | 19 | 66 | 66 (1) |
| [NS-12](../visao.md#ns-12) | 1 | 1 | 1 | 7 | 15 | 15 (0) |
| [NS-13](../visao.md#ns-13) | 1 | 18 | 11 | 17 | 47 | 47 (0) |
| [NS-14](../visao.md#ns-14) | 1 | 5 | 5 | 8 | 22 | 22 (0) |
| [NS-15](../visao.md#ns-15) | 7 | 7 | 2 | 3 | 18 | 18 (1) |
| [NS-16](../visao.md#ns-16) | 2 | 2 | 2 | 2 | 8 | 8 (1) |
| [NS-17](../visao.md#ns-17) | 0 | 0 | 0 | 0 | 0 | 0 (0) |

## Por funcionalidade do enunciado (F1 a F6)

| F | Funcionalidade | RF | UC | US | CA | TA (manuais) |
|---|---|---|---|---|---|---|
| F1 | Cadastrar e listar os espaços | 5 | 2 | 3 | 12 | 12 (0) |
| F2 | Cadastrar a solicitação | 1 | 1 | 1 | 6 | 6 (0) |
| F3 | Consultar por dois ou mais critérios | 5 | 2 | 3 | 21 | 21 (0) |
| F4 | Alterar a situação | 6 | 5 | 9 | 27 | 27 (0) |
| F5 | Impedir operações inválidas | 33 | 14 | 19 | 88 | 88 (0) |
| F6 | Mensagens de sucesso e erro | 1 | 0 | 0 | 0 | 0 (0) |
| Extra | Além das seis | 19 | 11 | 18 | 72 | 72 (3) |

## RNF por forma de verificação

| Forma | RNF |
|---|---|
| automatizado | 26 |
| automatizado (comando) | 2 |
| manual | 1 |
| manual (a verificar) | 2 |
| medição | 2 |

Detalhe em [`rnf.md`](rnf.md). Total: 33 RNF.
