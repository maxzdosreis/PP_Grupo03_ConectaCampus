from reservas.domain.situacao import SituacaoReserva


def verificar_historico_coerente(registros, situacao_atual) -> None:
    aceitas = [registro for registro in registros if not _foi_recusada(registro)]
    pares = [_anterior_e_nova(registro) for registro in aceitas]
    assert pares, "o histórico não pode ser vazio"
    assert pares[0] == (None, SituacaoReserva.SOLICITADA.value)
    for (_, nova_de_antes), (anterior, _) in zip(pares, pares[1:], strict=False):
        assert anterior == nova_de_antes
    assert pares[-1][1] == SituacaoReserva(situacao_atual).value


def _anterior_e_nova(registro):
    if isinstance(registro, dict):
        return registro["situacao_anterior"], registro["situacao_nova"]
    anterior = registro.situacao_anterior
    return (anterior.value if anterior else None), registro.situacao_nova.value


def _foi_recusada(registro) -> bool:
    if isinstance(registro, dict):
        return registro.get("resultado") == "RECUSADA"
    return registro.resultado.value == "RECUSADA"
