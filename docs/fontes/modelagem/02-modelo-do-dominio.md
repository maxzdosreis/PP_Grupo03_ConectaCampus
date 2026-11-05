## 2. Modelo do domínio

![Figura 3 — Modelo do domínio](modelo-do-dominio.png)

**Figura 3 — Modelo do domínio.** Classes de cada contexto, com os nomes do código.

![Figura 4 — Estados da reserva](estados-da-reserva.png)

**Figura 4 — Estados da reserva.** Exatamente as transições de `TRANSICOES_PERMITIDAS`.

| Legenda | ◆ composição · → associação · tracejada sem seta: referência por id · «…» papel da classe · 1, 0..* multiplicidade · sublinhado: método de classe |
|---|---|

**O que cada classe garante sozinha.** `EspacoEsportivo` nunca tem nome vazio, tipo fora de `TipoEspaco` nem capacidade abaixo de `CAPACIDADE_MINIMA`, e só muda pelos métodos da figura; inativo, recusa reservas novas (DEC-06). O construtor da `Reserva`, público, exige o que vale em qualquer situação (como o motivo em Recusada e Cancelada); início no futuro, regras de agenda e o registro inicial só existem em `Reserva.solicitar`, e passar por ele é convenção da aplicação: só `CriarReserva` cria, e o repositório só reconstitui. `alterar_situacao` aceita apenas o que a tabela e o papel do `Ator` permitem e gera um `RegistroDeSituacao` a cada mudança; `acoes_permitidas_para` usa a mesma regra. `IntervaloDeHorario` sempre termina depois de começar; o conflito entre reservas fica na função `garantir_horario_livre`. `Usuario.eh_gestor` delega a `PerfilUsuario.eh_gestor`.

**Decisões de modelagem.**

- **Referência por id entre contextos**, sem chave estrangeira; o espaço é conferido por `espacos.publico`.
- **`Solicitante` é cópia** de id, nome e matrícula no momento do pedido: a lista e o histórico mostram quem pediu mesmo que o cadastro mude.
- **`PapelDoAtor` ≠ `PerfilUsuario`**, pelo contrato `reservas não importa contas`; a API monta o `Ator` a partir de `request.user`.
- **`RegistroDeSituacao` sai da `Reserva`**, gravado na mesma transação e só nas mudanças aceitas (DEC-05). As transições não dependem do horário (DEC-13).

**No banco** repetem-se `ExclusionConstraint`, `UniqueConstraint(Lower("nome"))` e `CheckConstraint`. **Fora do diagrama:** `EstadoDoEspaco`, `DadosDeCadastro`, exceções, repositórios, `*Model`.
