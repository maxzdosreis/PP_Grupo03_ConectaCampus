# DEC-10 — Nome de espaço único

| Identificação | Responsabilidade |
|---|---|
| **DEC-10 • 0.1 • Rascunho** | Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |

| Campo | Conteúdo |
|---|---|
| **Estado da decisão** | Adotada provisoriamente (o código e o banco já garantem a regra abaixo; falta a confirmação). |
| **Pergunta** | Dois espaços esportivos podem ter o mesmo nome? Se não, "Ginásio A" e "ginásio a" contam como o mesmo nome? |
| **Opção adotada hoje** | O nome é único sem diferenciar maiúsculas de minúsculas, comparado depois de removidos os espaços das pontas e os repetidos. Cadastrar ou renomear para um nome já usado é recusado. |
| **Motivo** | O nome é como as pessoas identificam o espaço nas listas e nos pedidos; dois espaços com o mesmo nome confundiriam quem pede e quem decide. |
| **Alternativas** | Permitir nomes repetidos; único diferenciando maiúsculas; único ignorando também acentos ("Ginásio" = "Ginasio"). |
| **Responsável** | Max Zimmermann dos Reis (grupo), com o professor como representante do cliente. |
| **Prazo sugerido** | 06/11/2026 (Aula 7). |
| **Artefatos afetados** | `EspacoEsportivo` (normalização do nome); `CadastrarEspaco` e `EditarEspaco`; `RepositorioEspacos.existe_com_nome`; `NomeDeEspacoJaCadastrado`; constraint `espacos_espaco_esportivo_nome_unico_sem_caixa` (migration, se mudar); [Glossário](../glossario.md#espaco-esportivo); [Visão](../visao.md) (R-13); fichas de [UC-14](../casos-de-uso/UC-14-cadastrar-espaco.md#questões-em-aberto) (E6.1 e E7.1) e de [UC-15](../casos-de-uso/fichas-resumidas.md#uc-15) (REQ-04). · **REQ-06:** histórias [US-05](../historias/US-05-cadastrar-espaco.md), [US-06](../historias/US-06-editar-espaco.md); 6 critérios de aceite e 6 testes de aceite ([mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-10)). |
| **Origem** | ESP-02 (regra implementada sem DEC registrada). |
| **Observações** | ID novo. Hoje, nomes que só diferem por acento são considerados diferentes. |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Registro da decisão tomada na ESP-02 (REQ-01). |
| 0.1 | 04/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as fichas de caso de uso que dependem desta decisão (REQ-04). |
| 0.1 | 05/11/2026 | Max Zimmermann dos Reis | Artefatos afetados: as histórias e o número de critérios e testes de aceite, a partir do [mapa de impacto](../rastreabilidade/impacto-por-dec.md#dec-10) (REQ-06). Estado e opção sem mudança. |
