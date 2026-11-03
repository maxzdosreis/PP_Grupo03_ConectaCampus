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
| **Artefatos afetados** | `EspacoEsportivo` (normalização do nome); `CadastrarEspaco` e `EditarEspaco`; `RepositorioEspacos.existe_com_nome`; `NomeDeEspacoJaCadastrado`; constraint `espacos_espaco_esportivo_nome_unico_sem_caixa` (migration, se mudar); [Glossário](../glossario.md#espaco-esportivo); [Visão](../visao.md) (R-13). |
| **Origem** | ESP-02 (regra implementada sem DEC registrada). |
| **Observações** | ID novo. Hoje, nomes que só diferem por acento são considerados diferentes. |

## Histórico

| Versão | Data | Autor | Alteração |
|---|---|---|---|
| 0.1 | 03/11/2026 | Max Zimmermann dos Reis | Registro da decisão tomada na ESP-02 (REQ-01). |
