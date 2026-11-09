# DEC-12 — Metas de desempenho

| Identificação | Responsabilidade |
|---|---|
| **DEC-12 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Decidida. Resposta do professor na Aula 7 (06/11/2026), que confirma a opção já implementada; nenhum CR. |
| **Pergunta** | Em quanto tempo a consulta de reservas e a agenda do dia precisam responder, e com quantas reservas cadastradas essa meta vale? |
| **Resposta do professor** | "Isso faz sentido, e precisamos fazer isso." (resposta dada à [DEC-08](DEC-08.md) e à DEC-12 juntas) |
| **Decisão** | Com **1.000 reservas** cadastradas: a consulta de reservas responde em até **1 s** no percentil 95 (inclusive a lista do Gestor sem critério, com todas as reservas na resposta); a agenda do dia responde em até **500 ms** no percentil 95. Medido dentro do ambiente de execução local (container do backend, com o banco no container ao lado), sem contar a rede nem o navegador. |
| **Motivo** | Nenhum documento do enunciado nem da Visão fixa tempo de resposta, e um RNF de desempenho precisa de valor-alvo mensurável (A2·s11). 1.000 reservas equivalem a cerca de um semestre de uso de cinco espaços com poucas reservas por dia; os limites são folgados para o Docker no Windows, onde o disco é lento. |
| **Alternativas** | **b)** 500 ms para a consulta e 200 ms para a agenda. **c)** 2 s e 1 s. **d)** Medir com mais reservas (10.000) ou com a consulta paginada. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor como representante do cliente. |
| **Prazo** | Decidida em 06/11/2026. |
| **Artefatos afetados** | [RNF-P01 e RNF-P02](../requisitos/rnf.md#4-desempenho-p); `scripts/medir_desempenho.py`; [SRS](../requisitos/srs.md) (seção 5 e lacunas). · **REQ-06:** nenhuma história; 0 critérios de aceite e 0 testes de aceite ([mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-12)). |
| **Origem** | REQ-02 (SRS), ao escrever os RNF de desempenho. |
| **Observações** | Medido em 04/11/2026 ([resultado e ambiente](../requisitos/rnf.md#medição)): com 1.000 reservas, p95 de 378 ms na pior consulta e de 7 ms na agenda, as duas metas atendidas. Com 5.000, a lista do Gestor sem critério chega a 1.743 ms, porque a consulta não é paginada ([lacuna L-05](../requisitos/srs.md#l-05)): se o cliente esperar mais reservas que isso, a meta e a paginação precisam ser revistas juntas. |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Registro da meta adotada na REQ-02. |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as histórias e o número de critérios e testes de aceite, a partir do [mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-12) (REQ-06). Estado e opção sem mudança. |
| 0.1 | 06/11/2026 | Max Zimmermann dos Reis | Decidida na Aula 7: resposta do professor registrada, confirmando a opção adotada (que passa ao campo Decisão); nenhum CR (GES-02). |
| 0.1 | 09/11/2026 | Max Zimmermann dos Reis | Medição nova depois da paginação da consulta (RES-10): com 1.000 e 5.000 reservas, inclusive a última página do Gestor sem critério, o pior p95 da consulta foi 45 ms (antes, 1.743 ms com 5.000); a meta não muda ([resultado e ambiente](../requisitos/rnf.md#medição); [L-05](../requisitos/srs.md#l-05) resolvida). |
