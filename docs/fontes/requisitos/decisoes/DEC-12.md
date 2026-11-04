# DEC-12 — Metas de desempenho

| Identificação | Responsabilidade |
|---|---|
| **DEC-12 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Adotada provisoriamente (meta definida pelo grupo ao escrever a SRS; falta a confirmação). |
| **Pergunta** | Em quanto tempo a consulta de reservas e a agenda do dia precisam responder, e com quantas reservas cadastradas essa meta vale? |
| **Opção adotada hoje** | Com **1.000 reservas** cadastradas: a consulta de reservas responde em até **1 s** no percentil 95 (inclusive a lista do Gestor sem critério, com todas as reservas na resposta); a agenda do dia responde em até **500 ms** no percentil 95. Medido dentro do ambiente de execução local (container do backend, com o banco no container ao lado), sem contar a rede nem o navegador. |
| **Motivo** | Nenhum documento do enunciado nem da Visão fixa tempo de resposta, e um RNF de desempenho precisa de valor-alvo mensurável (A2·s11). 1.000 reservas equivalem a cerca de um semestre de uso de cinco espaços com poucas reservas por dia; os limites são folgados para o Docker no Windows, onde o disco é lento. |
| **Alternativas** | **b)** 500 ms para a consulta e 200 ms para a agenda. **c)** 2 s e 1 s. **d)** Medir com mais reservas (10.000) ou com a consulta paginada. |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor como representante do cliente. |
| **Prazo sugerido** | 13/11/2026. |
| **Artefatos afetados** | [RNF-P01 e RNF-P02](../requisitos/rnf.md#4-desempenho-p); `scripts/medir_desempenho.py`; [SRS](../requisitos/srs.md) (seção 5 e lacunas). |
| **Origem** | REQ-02 (SRS), ao escrever os RNF de desempenho. |
| **Observações** | Medido em 04/11/2026 ([resultado e ambiente](../requisitos/rnf.md#medição)): com 1.000 reservas, p95 de 378 ms na pior consulta e de 7 ms na agenda, as duas metas atendidas. Com 5.000, a lista do Gestor sem critério chega a 1.743 ms, porque a consulta não é paginada ([lacuna L-05](../requisitos/srs.md#l-05)): se o cliente esperar mais reservas que isso, a meta e a paginação precisam ser revistas juntas. |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Registro da meta adotada na REQ-02. |
