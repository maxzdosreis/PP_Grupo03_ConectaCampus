import pytest

from compartilhado.api.tratador_de_erros import tratar_excecao
from compartilhado.domain.erros import CampoObrigatorioAusente
from espacos.domain.espaco_esportivo import NOME_MAXIMO_CARACTERES, EspacoEsportivo
from espacos.domain.excecoes import (
    CapacidadeInvalida,
    EspacoInativo,
    EspacoNaoEncontrado,
    NomeDeEspacoJaCadastrado,
    NomeDeEspacoMuitoLongo,
    TipoDeEspacoInvalido,
)
from espacos.domain.tipo_espaco import TipoEspaco


def _criar_espaco(**sobrescritas):
    dados = {
        "nome": "Quadra Central",
        "tipo": TipoEspaco.GINASIO,
        "capacidade": 20,
    }
    dados.update(sobrescritas)
    return EspacoEsportivo(**dados)


def test_criacao_valida_normaliza_nome_e_converte_tipo():
    # Act
    espaco = _criar_espaco(nome="  Quadra   Central ", tipo="GINASIO")

    # Assert
    assert espaco.nome == "Quadra Central"
    assert espaco.tipo is TipoEspaco.GINASIO
    assert espaco.capacidade == 20


def test_espaco_novo_comeca_ativo_e_sem_id():
    # Act
    espaco = _criar_espaco()

    # Assert
    assert espaco.ativo is True
    assert espaco.id is None


@pytest.mark.parametrize("nome", ["", "   ", None])
def test_nome_vazio_e_recusado_como_campo_obrigatorio(nome):
    # Act
    with pytest.raises(CampoObrigatorioAusente) as erro:
        _criar_espaco(nome=nome)

    # Assert
    assert erro.value.campo == "nome"


def test_nome_no_limite_de_caracteres_e_aceito():
    # Arrange
    nome = "A" * NOME_MAXIMO_CARACTERES

    # Act
    espaco = _criar_espaco(nome=nome)

    # Assert
    assert espaco.nome == nome


def test_nome_acima_do_limite_de_caracteres_e_recusado():
    # Arrange
    nome = "A" * (NOME_MAXIMO_CARACTERES + 1)

    # Act
    with pytest.raises(NomeDeEspacoMuitoLongo) as erro:
        _criar_espaco(nome=nome)

    # Assert
    assert erro.value.campo == "nome"
    assert erro.value.mensagem == (
        "O nome do espaço deve ter no máximo 100 caracteres."
    )


@pytest.mark.parametrize("tipo", [None, ""])
def test_tipo_vazio_e_recusado_como_campo_obrigatorio(tipo):
    # Act
    with pytest.raises(CampoObrigatorioAusente) as erro:
        _criar_espaco(tipo=tipo)

    # Assert
    assert erro.value.campo == "tipo"


def test_tipo_desconhecido_e_recusado_listando_os_tipos_aceitos():
    # Act
    with pytest.raises(TipoDeEspacoInvalido) as erro:
        _criar_espaco(tipo="PISCINA")

    # Assert
    assert erro.value.campo == "tipo"
    assert "Quadra poliesportiva" in erro.value.mensagem
    assert "Quadra de tênis" in erro.value.mensagem


def test_capacidade_ausente_e_recusada_como_campo_obrigatorio():
    # Act
    with pytest.raises(CampoObrigatorioAusente) as erro:
        _criar_espaco(capacidade=None)

    # Assert
    assert erro.value.campo == "capacidade"


@pytest.mark.parametrize("capacidade", [0, -1, True, "10"])
def test_capacidade_que_nao_e_inteiro_positivo_e_recusada(capacidade):
    # Act
    with pytest.raises(CapacidadeInvalida) as erro:
        _criar_espaco(capacidade=capacidade)

    # Assert
    assert erro.value.campo == "capacidade"


def test_capacidade_minima_e_aceita():
    # Act
    espaco = _criar_espaco(capacidade=1)

    # Assert
    assert espaco.capacidade == 1


def test_garantir_que_esta_ativo_passa_quando_o_espaco_esta_ativo():
    # Arrange
    espaco = _criar_espaco(ativo=True)

    # Act / Assert
    espaco.garantir_que_esta_ativo()


def test_garantir_que_esta_ativo_recusa_espaco_inativo():
    # Arrange
    espaco = _criar_espaco(ativo=False)

    # Act / Assert
    with pytest.raises(EspacoInativo):
        espaco.garantir_que_esta_ativo()


def test_espacos_com_o_mesmo_id_sao_iguais():
    # Arrange
    espaco = _criar_espaco(id=1)
    mesmo_espaco = _criar_espaco(id=1, nome="Outro nome")

    # Act / Assert
    assert espaco == mesmo_espaco
    assert hash(espaco) == hash(mesmo_espaco)


def test_espacos_com_ids_diferentes_sao_diferentes():
    # Act / Assert
    assert _criar_espaco(id=1) != _criar_espaco(id=2)


def test_espacos_sem_id_so_sao_iguais_a_si_mesmos():
    # Arrange
    espaco = _criar_espaco()

    # Act / Assert
    assert espaco == espaco
    assert espaco != _criar_espaco()
    assert len({espaco, _criar_espaco()}) == 2


def test_espaco_nao_e_igual_a_objeto_de_outro_tipo():
    # Act / Assert
    assert _criar_espaco(id=1) != 1


def test_str_mostra_nome_e_rotulo_do_tipo():
    # Act
    texto = str(_criar_espaco())

    # Assert
    assert texto == "Quadra Central (Ginásio)"


def test_repr_mostra_os_campos_para_depuracao():
    # Act
    texto = repr(_criar_espaco(id=3))

    # Assert
    assert texto.startswith("EspacoEsportivo(id=3, nome='Quadra Central'")
    assert "capacidade=20" in texto
    assert "ativo=True" in texto


def test_espaco_nao_encontrado_vira_404_dizendo_qual_espaco():
    # Act
    resposta = tratar_excecao(EspacoNaoEncontrado(7), {})

    # Assert
    assert resposta.status_code == 404
    assert resposta.data == {
        "erro": {
            "codigo": "ESPACO_NAO_ENCONTRADO",
            "mensagem": "Espaço de código 7 não encontrado.",
        }
    }


def test_espaco_inativo_vira_409():
    # Act
    resposta = tratar_excecao(EspacoInativo(), {})

    # Assert
    assert resposta.status_code == 409
    assert resposta.data["erro"]["codigo"] == "ESPACO_INATIVO"


def test_nome_de_espaco_ja_cadastrado_vira_409_marcando_o_campo():
    # Act
    resposta = tratar_excecao(NomeDeEspacoJaCadastrado(), {})

    # Assert
    mensagem = "Já existe um espaço com este nome."
    assert resposta.status_code == 409
    assert resposta.data == {
        "erro": {
            "codigo": "NOME_DE_ESPACO_JA_CADASTRADO",
            "mensagem": mensagem,
            "campos": {"nome": [mensagem]},
        }
    }


def test_capacidade_invalida_vira_400_marcando_o_campo():
    # Act
    resposta = tratar_excecao(CapacidadeInvalida(), {})

    # Assert
    mensagem = "A capacidade deve ser um número inteiro maior que zero."
    assert resposta.status_code == 400
    assert resposta.data == {
        "erro": {
            "codigo": "CAPACIDADE_INVALIDA",
            "mensagem": mensagem,
            "campos": {"capacidade": [mensagem]},
        }
    }
