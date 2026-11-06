# `exemplos` — dados de exemplo

App Django com um único comando, `carregar_dados_exemplo`, que cria usuários, espaços e reservas para a correção e a demonstração. Não é contexto: é composição, como o `config`, e é o único lugar que conhece `espacos`, `reservas` e `contas` ao mesmo tempo. Nenhum contexto o importa (contrato "Nenhum contexto depende dos dados de exemplo", no [README do backend](../README.md#regra-de-dependência-import-linter)). Não tem models nem migrations.

## O comando

Com os serviços no ar, dentro de `src`:

```bash
docker compose exec backend python manage.py carregar_dados_exemplo
```

O que ele cria (usuários com as senhas, espaços, reservas de cada situação) está no [README da raiz](../../../README.md#dados-de-exemplo), porque é o que o professor usa para testar. No fim, o comando imprime um resumo (criados e já existentes), a tabela de usuários e o horário de conflito com a data.

## Como funciona

- **Mesmas regras do sistema.** Tudo passa pelos casos de uso e pelas entidades, nunca por gravação direta no banco: solicitantes por `CadastrarSolicitante` (com a política de senha), espaços por `CadastrarEspaco` (o inativo, Quadra de Tênis 2, é cadastrado e depois desativado por `DesativarEspaco`), reservas por `CriarReserva` e `AlterarSituacaoReserva`. O Gestor não tem caso de uso: passa por `DadosDeCadastro` e pela política de senha e é criado com `create_superuser` (perfil Gestor, entra no `/admin/`). Se um dado violar uma regra, o comando falha com "Dado de exemplo inválido: ...".
- **Tudo ou nada.** A carga roda numa transação: uma falha não deixa nada pela metade.
- **Pode rodar mais de uma vez.** Usuário é reconhecido pelo e-mail e espaço pelo nome (sem diferenciar maiúsculas); as reservas só são criadas se os solicitantes de exemplo ainda não tiverem nenhuma.
- **Datas relativas ao dia em que roda.** As reservas em aberto ficam sempre no futuro (amanhã, +2 e +3 dias). Cada reserva é solicitada e alterada com um relógio fixo no momento certo, então todas têm histórico coerente: a Concluída (ontem, 18:00–19:30) foi solicitada 3 dias atrás, confirmada há 2 dias e concluída agora.
- **Trava de segurança.** Com `DJANGO_DEBUG=False` o comando recusa rodar ("Os dados de exemplo só podem ser carregados com DJANGO_DEBUG=True, porque criam usuários com senhas conhecidas."). O `.env.example` já vem com `True`.
- **Horário de conflito.** `CONFLITO_PARA_DEMONSTRACAO` (Quadra Poliesportiva Central, amanhã, 10:30–11:30) sobrepõe a reserva Solicitada e é o 409 do roteiro da demonstração.
- Os e-mails são `@exemplo.com`, mas nunca `ana@exemplo.com` nem a matrícula `2026001`, que são os do [exemplo de cadastro](../contas/README.md#cadastrar-um-solicitante): assim o exemplo funciona num banco com os dados carregados.

Para apagar tudo e carregar de novo, veja [Recomeçar do zero](../../../README.md#recomeçar-do-zero) no README da raiz.

## Onde mexer

| Para mudar… | Arquivo |
|---|---|
| Usuários, espaços, reservas e o horário de conflito | `dados.py` (só conteúdo) |
| Como cada etapa é carregada | `carga.py` (`garantir_usuarios`, `garantir_espacos`, `garantir_reservas`) |
| A trava de `DEBUG`, a transação e a saída | `management/commands/carregar_dados_exemplo.py` |

Mudou um dado? Atualize as tabelas do README da raiz no mesmo PR. O teste `exemplos/tests/test_carregar_dados_exemplo.py` roda o comando de ponta a ponta (login com cada usuário, 409 no horário de conflito pela API, histórico coerente, idempotência e a trava de `DEBUG`).
