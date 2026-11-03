from dataclasses import asdict, replace
from typing import NamedTuple

import pytest
from hypothesis import assume, given, reject
from hypothesis import strategies as st
from hypothesis.stateful import (
    RuleBasedStateMachine,
    initialize,
    invariant,
    precondition,
    rule,
)

from compartilhado.domain.erros import CampoObrigatorioAusente, ErroDeDominio
from espacos.application.casos_de_uso import CadastrarEspaco
from espacos.domain.espaco_esportivo import (
    CAPACIDADE_MINIMA,
    NOME_MAXIMO_CARACTERES,
    EspacoEsportivo,
)
from espacos.domain.excecoes import (
    CapacidadeInvalida,
    EspacoJaAtivo,
    EspacoJaInativo,
    NenhumaAlteracaoInformada,
    NomeDeEspacoJaCadastrado,
    NomeDeEspacoMuitoLongo,
    TipoDeEspacoInvalido,
)
from espacos.domain.tipo_espaco import TipoEspaco
from espacos.tests.fakes import RepositorioEspacosEmMemoria, novo_espaco


class Gerado(NamedTuple):
    valor: object
    esperado: object = None
    erro: type[ErroDeDominio] | None = None


_ESPACOS_EM_BRANCO = " \t\n  　"
_LETRA = st.characters(exclude_categories=("Z", "C")).filter(
    lambda letra: not letra.isspace()
)
_PALAVRA = st.text(_LETRA, min_size=1, max_size=15)


def _espacos(*, min_size=0):
    return st.text(_ESPACOS_EM_BRANCO, min_size=min_size, max_size=3)


@st.composite
def _nomes_validos(draw):
    palavras = draw(
        st.lists(_PALAVRA, min_size=1, max_size=10).filter(
            lambda palavras: len(" ".join(palavras)) <= NOME_MAXIMO_CARACTERES
        )
    )
    meio = "".join(draw(_espacos(min_size=1)) + palavra for palavra in palavras[1:])
    entrada = draw(_espacos()) + palavras[0] + meio + draw(_espacos())
    return Gerado(entrada, esperado=" ".join(palavras))


@st.composite
def _nomes_longos(draw):
    palavra = draw(
        st.text(
            _LETRA,
            min_size=NOME_MAXIMO_CARACTERES + 1,
            max_size=NOME_MAXIMO_CARACTERES + 30,
        )
    )
    entrada = draw(_espacos()) + palavra + draw(_espacos())
    return Gerado(entrada, erro=NomeDeEspacoMuitoLongo)


_NOMES_INFORMADOS = st.one_of(
    _nomes_validos(),
    _nomes_longos(),
    _espacos().map(lambda vazio: Gerado(vazio, erro=CampoObrigatorioAusente)),
)
_NOMES = st.one_of(
    _NOMES_INFORMADOS, st.just(Gerado(None, erro=CampoObrigatorioAusente))
)


_VALORES_DE_TIPO = [tipo.value for tipo in TipoEspaco]
_TIPOS_VALIDOS = st.sampled_from(
    [Gerado(tipo, esperado=tipo) for tipo in TipoEspaco]
    + [Gerado(tipo.value, esperado=tipo) for tipo in TipoEspaco]
)
_TIPOS_INFORMADOS = st.one_of(
    _TIPOS_VALIDOS,
    st.just(Gerado("", erro=CampoObrigatorioAusente)),
    st.sampled_from(_VALORES_DE_TIPO).map(
        lambda valor: Gerado(valor.lower(), erro=TipoDeEspacoInvalido)
    ),
    st.text(min_size=1)
    .filter(lambda valor: valor not in _VALORES_DE_TIPO)
    .map(lambda valor: Gerado(valor, erro=TipoDeEspacoInvalido)),
)
_TIPOS = st.one_of(
    _TIPOS_INFORMADOS, st.just(Gerado(None, erro=CampoObrigatorioAusente))
)


_CAPACIDADES_VALIDAS = st.integers(min_value=CAPACIDADE_MINIMA).map(
    lambda valor: Gerado(valor, esperado=valor)
)
_CAPACIDADES_INFORMADAS = st.one_of(
    _CAPACIDADES_VALIDAS,
    st.one_of(
        st.integers(max_value=CAPACIDADE_MINIMA - 1), st.booleans(), st.text()
    ).map(lambda valor: Gerado(valor, erro=CapacidadeInvalida)),
)
_CAPACIDADES = st.one_of(
    _CAPACIDADES_INFORMADAS, st.just(Gerado(None, erro=CampoObrigatorioAusente))
)


def _criar(nome, tipo, capacidade, **extras):
    return EspacoEsportivo(
        nome=nome.valor, tipo=tipo.valor, capacidade=capacidade.valor, **extras
    )


def _primeiro_erro(gerados):
    return next(
        ((campo, gerado.erro) for campo, gerado in gerados.items() if gerado.erro),
        None,
    )


def _verificar_invariantes(espaco):
    nome = espaco.nome
    assert 0 < len(nome) <= NOME_MAXIMO_CARACTERES
    assert not nome[0].isspace()
    assert not nome[-1].isspace()
    assert "  " not in nome
    assert all(letra == " " or not letra.isspace() for letra in nome)
    assert isinstance(espaco.tipo, TipoEspaco)
    assert type(espaco.capacidade) is int
    assert espaco.capacidade >= CAPACIDADE_MINIMA


@given(
    nome=_nomes_validos(),
    tipo=_TIPOS_VALIDOS,
    capacidade=_CAPACIDADES_VALIDAS,
    ativo=st.booleans(),
)
def test_entrada_valida_cria_espaco_que_respeita_todas_as_invariantes(
    nome, tipo, capacidade, ativo
):
    # Act
    espaco = _criar(nome, tipo, capacidade, ativo=ativo)

    # Assert
    _verificar_invariantes(espaco)
    assert (espaco.nome, espaco.tipo, espaco.capacidade, espaco.ativo) == (
        nome.esperado,
        tipo.esperado,
        capacidade.esperado,
        ativo,
    )


@given(nome=_NOMES, tipo=_TIPOS, capacidade=_CAPACIDADES)
def test_entrada_invalida_lanca_so_o_erro_de_dominio_do_primeiro_campo_invalido(
    nome, tipo, capacidade
):
    # Arrange
    primeiro = _primeiro_erro({"nome": nome, "tipo": tipo, "capacidade": capacidade})
    assume(primeiro is not None)
    campo, excecao = primeiro

    # Act
    with pytest.raises(ErroDeDominio) as erro:
        _criar(nome, tipo, capacidade)

    # Assert
    assert type(erro.value) is excecao
    assert erro.value.campo == campo


@given(nome=st.text(max_size=NOME_MAXIMO_CARACTERES * 2))
def test_normalizar_o_nome_e_idempotente(nome):
    # Arrange
    try:
        normalizado = novo_espaco(nome=nome).nome
    except ErroDeDominio:
        reject()

    # Act
    de_novo = novo_espaco(nome=normalizado).nome

    # Assert
    assert de_novo == normalizado


class MaquinaDoEspaco(RuleBasedStateMachine):
    @initialize(
        nome=_nomes_validos(),
        tipo=_TIPOS_VALIDOS,
        capacidade=_CAPACIDADES_VALIDAS,
        ativo=st.booleans(),
    )
    def criar(self, nome, tipo, capacidade, ativo):
        self.espaco = _criar(nome, tipo, capacidade, ativo=ativo)
        self.origem = self.espaco.estado_de_origem

    @rule(
        nome=st.none() | _nomes_validos(),
        tipo=st.none() | _TIPOS_VALIDOS,
        capacidade=st.none() | _CAPACIDADES_VALIDAS,
    )
    def alterar_dados_validos(self, nome, tipo, capacidade):
        informados = _informados(nome=nome, tipo=tipo, capacidade=capacidade)
        assume(informados)
        antes = self.espaco.estado

        self.espaco.alterar_dados(**_valores(informados))

        esperados = {campo: gerado.esperado for campo, gerado in informados.items()}
        assert self.espaco.estado == replace(antes, **esperados)

    @rule(
        nome=st.none() | _NOMES_INFORMADOS,
        tipo=st.none() | _TIPOS_INFORMADOS,
        capacidade=st.none() | _CAPACIDADES_INFORMADAS,
    )
    def alterar_dados_com_algum_invalido(self, nome, tipo, capacidade):
        informados = _informados(nome=nome, tipo=tipo, capacidade=capacidade)
        primeiro = _primeiro_erro(informados)
        assume(primeiro is not None)
        antes = self.espaco.estado

        with pytest.raises(primeiro[1]):
            self.espaco.alterar_dados(**_valores(informados))

        assert self.espaco.estado == antes

    @rule()
    def alterar_sem_nenhum_campo(self):
        antes = self.espaco.estado

        with pytest.raises(NenhumaAlteracaoInformada):
            self.espaco.alterar_dados()

        assert self.espaco.estado == antes

    @precondition(lambda self: self.espaco.ativo)
    @rule()
    def desativar_ativo(self):
        antes = self.espaco.estado

        self.espaco.desativar()

        assert self.espaco.estado == replace(antes, ativo=False)

    @precondition(lambda self: not self.espaco.ativo)
    @rule()
    def desativar_inativo(self):
        antes = self.espaco.estado

        with pytest.raises(EspacoJaInativo):
            self.espaco.desativar()

        assert self.espaco.estado == antes

    @precondition(lambda self: not self.espaco.ativo)
    @rule()
    def ativar_inativo(self):
        antes = self.espaco.estado

        self.espaco.ativar()

        assert self.espaco.estado == replace(antes, ativo=True)

    @precondition(lambda self: self.espaco.ativo)
    @rule()
    def ativar_ativo(self):
        antes = self.espaco.estado

        with pytest.raises(EspacoJaAtivo):
            self.espaco.ativar()

        assert self.espaco.estado == antes

    @invariant()
    def continua_valido(self):
        _verificar_invariantes(self.espaco)
        EspacoEsportivo(**asdict(self.espaco.estado))

    @invariant()
    def estado_de_origem_so_muda_ao_gravar(self):
        assert self.espaco.estado_de_origem == self.origem


def _informados(**gerados):
    return {campo: gerado for campo, gerado in gerados.items() if gerado is not None}


def _valores(gerados):
    return {campo: gerado.valor for campo, gerado in gerados.items()}


TestMaquinaDoEspaco = MaquinaDoEspaco.TestCase


_IDS = st.none() | st.integers(min_value=1, max_value=3)


@st.composite
def _dados_validos(draw):
    return {
        "nome": draw(_nomes_validos()).valor,
        "tipo": draw(_TIPOS_VALIDOS).valor,
        "capacidade": draw(_CAPACIDADES_VALIDAS).valor,
        "ativo": draw(st.booleans()),
    }


@st.composite
def _espacos_validos(draw):
    return EspacoEsportivo(id=draw(_IDS), **draw(_dados_validos()))


@given(a=_espacos_validos(), b=_espacos_validos())
def test_dois_espacos_sao_iguais_so_quando_tem_o_mesmo_id(a, b):
    # Act
    iguais = a == b

    # Assert
    assert iguais is (a.id is not None and a.id == b.id)


@given(espaco=_espacos_validos())
def test_todo_espaco_e_igual_a_si_mesmo(espaco):
    # Act / Assert
    assert espaco == espaco


@given(
    espaco_id=st.integers(min_value=1),
    dados_a=_dados_validos(),
    dados_b=_dados_validos(),
)
def test_espacos_com_o_mesmo_id_tem_o_mesmo_hash_mesmo_com_dados_diferentes(
    espaco_id, dados_a, dados_b
):
    # Arrange
    a = EspacoEsportivo(id=espaco_id, **dados_a)
    b = EspacoEsportivo(id=espaco_id, **dados_b)

    # Act / Assert
    assert hash(a) == hash(b)


def _variar_caixa(draw, texto):
    return "".join(
        draw(st.sampled_from([letra.lower(), letra.upper()]))
        if len(letra.lower()) == len(letra.upper()) == 1
        else letra
        for letra in texto
    )


@st.composite
def _nomes_com_repeticoes(draw):
    bases = draw(st.lists(_nomes_validos(), min_size=1, max_size=4))
    escolhidas = draw(st.lists(st.sampled_from(bases), min_size=1, max_size=12))
    return [_variar_caixa(draw, base.valor) for base in escolhidas]


@given(lista_de_nomes=_nomes_com_repeticoes())
def test_cadastrar_varios_nomes_termina_com_nomes_unicos_sem_diferenciar_caixa(
    lista_de_nomes,
):
    # Arrange
    repositorio = RepositorioEspacosEmMemoria()
    cadastrar = CadastrarEspaco(repositorio)
    ja_usados = set()

    # Act / Assert
    for nome in lista_de_nomes:
        chave = novo_espaco(nome=nome).nome.casefold()
        if chave in ja_usados:
            with pytest.raises(NomeDeEspacoJaCadastrado):
                cadastrar.executar(nome=nome, tipo="GINASIO", capacidade=10)
        else:
            cadastrar.executar(nome=nome, tipo="GINASIO", capacidade=10)
            ja_usados.add(chave)

    # Assert
    chaves = [espaco.nome.casefold() for espaco in repositorio.listar()]
    assert len(chaves) == len(set(chaves)) == len(ja_usados)
