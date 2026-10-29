from typing import Protocol

from espacos.domain.espaco_esportivo import EspacoEsportivo
from espacos.domain.tipo_espaco import TipoEspaco


class RepositorioEspacos(Protocol):
    def salvar(self, espaco: EspacoEsportivo) -> EspacoEsportivo:
        """Insere quando o id é None e atualiza quando já existe.

        Devolve a entidade com id. Atualizar um id inexistente lança
        EspacoNaoEncontrado; nome repetido lança NomeDeEspacoJaCadastrado.
        Atualizar exige que o estado gravado seja o estado_de_origem da entidade:
        se outra operação alterou o espaço depois da leitura, lança
        EspacoDesatualizado sem gravar. Depois de gravar, marca a entidade como
        gravada.
        """

    def obter_por_id(self, espaco_id: int) -> EspacoEsportivo | None:
        """Devolve o espaço ou None; o caso de uso decide se a ausência é erro."""

    def listar(
        self, *, apenas_ativos: bool = False, tipo: TipoEspaco | None = None
    ) -> list[EspacoEsportivo]:
        """Lista os espaços ordenados por nome, com filtros opcionais."""

    def existe_com_nome(self, nome: str, *, ignorar_id: int | None = None) -> bool:
        """Diz se outro espaço já usa o nome, sem diferenciar maiúsculas.

        O nome chega já normalizado pela entidade. ignorar_id exclui o próprio
        espaço da busca, para a edição.
        """
