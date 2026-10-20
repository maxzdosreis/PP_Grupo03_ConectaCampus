from django.db import IntegrityError, transaction

from espacos.application.repositorio import RepositorioEspacos
from espacos.domain.espaco_esportivo import EspacoEsportivo
from espacos.domain.excecoes import EspacoNaoEncontrado, NomeDeEspacoJaCadastrado
from espacos.domain.tipo_espaco import TipoEspaco
from espacos.infrastructure.models import CONSTRAINT_NOME_UNICO, EspacoEsportivoModel


class RepositorioEspacosDjango(RepositorioEspacos):
    def salvar(self, espaco: EspacoEsportivo) -> EspacoEsportivo:
        try:
            with transaction.atomic():
                model = _obter_model_para_salvar(espaco)
                _aplicar_no_model(espaco, model)
                model.save()
        except IntegrityError as erro:
            if CONSTRAINT_NOME_UNICO in str(erro):
                raise NomeDeEspacoJaCadastrado() from erro
            raise
        return _para_entidade(model)

    def obter_por_id(self, espaco_id: int) -> EspacoEsportivo | None:
        model = EspacoEsportivoModel.objects.filter(pk=espaco_id).first()
        return _para_entidade(model) if model else None

    def listar(
        self, *, apenas_ativos: bool = False, tipo: TipoEspaco | None = None
    ) -> list[EspacoEsportivo]:
        consulta = EspacoEsportivoModel.objects.order_by("nome")
        if apenas_ativos:
            consulta = consulta.filter(ativo=True)
        if tipo is not None:
            consulta = consulta.filter(tipo=tipo)
        return [_para_entidade(model) for model in consulta]

    def existe_com_nome(self, nome: str, *, ignorar_id: int | None = None) -> bool:
        consulta = EspacoEsportivoModel.objects.filter(nome__iexact=nome)
        if ignorar_id is not None:
            consulta = consulta.exclude(pk=ignorar_id)
        return consulta.exists()


def _obter_model_para_salvar(espaco: EspacoEsportivo) -> EspacoEsportivoModel:
    if espaco.id is None:
        return EspacoEsportivoModel()
    try:
        return EspacoEsportivoModel.objects.get(pk=espaco.id)
    except EspacoEsportivoModel.DoesNotExist:
        raise EspacoNaoEncontrado(espaco.id) from None


def _para_entidade(model: EspacoEsportivoModel) -> EspacoEsportivo:
    return EspacoEsportivo(
        id=model.pk,
        nome=model.nome,
        tipo=model.tipo,
        capacidade=model.capacidade,
        ativo=model.ativo,
    )


def _aplicar_no_model(entidade: EspacoEsportivo, model: EspacoEsportivoModel) -> None:
    model.nome = entidade.nome
    model.tipo = entidade.tipo.value
    model.capacidade = entidade.capacidade
    model.ativo = entidade.ativo
