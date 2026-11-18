from __future__ import annotations

import json
import os
import sys

APPS_DO_PROJETO = ("contas", "espacos", "reservas")
MAXIMO_DE_ENTIDADES = 6
MAXIMO_DE_COLUNAS = 8

COLUNAS_DE_NEGOCIO = {
    "contas_usuario": ("nome", "perfil", "is_active"),
    "espacos_espaco_esportivo": ("nome", "tipo", "capacidade", "ativo", "abertura_em_minutos", "fechamento_em_minutos"),
    "reservas_reserva": ("situacao", "inicio", "fim"),
    "reservas_registro_de_situacao": ("resultado", "codigo_do_erro", "situacao_pedida"),
}

REFERENCIAS_POR_ID = {
    ("reservas_reserva", "espaco_id"): "espacos_espaco_esportivo",
    ("reservas_reserva", "solicitante_usuario_id"): "contas_usuario",
    ("reservas_registro_de_situacao", "autor_usuario_id"): "contas_usuario",
}

ORDEM_DAS_TABELAS = (
    "contas_usuario",
    "espacos_espaco_esportivo",
    "reservas_reserva",
    "reservas_registro_de_situacao",
)

TIPO_NO_DESENHO = {
    "BigAutoField": "bigint",
    "BigIntegerField": "bigint",
    "ForeignKey": "bigint",
    "CharField": "varchar",
    "EmailField": "varchar",
    "PositiveIntegerField": "integer",
    "PositiveSmallIntegerField": "smallint",
    "BooleanField": "boolean",
    "DateTimeField": "timestamptz",
}

OPERADORES = {
    "gte": "≥", "gt": ">", "lte": "≤", "lt": "<", "exact": "=", "in": "∈",
}
OPERADORES_NEGADOS = {
    "gte": "<", "gt": "≤", "lte": ">", "lt": "≥", "exact": "≠", "in": "∉",
}
OPERADORES_DO_INTERVALO = {"&&": "sobrepõe (&&)", "=": "igual (=)"}


def _preparar_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    import django

    django.setup()


def _modelos():
    from django.apps import apps

    achados = {m._meta.db_table: m for m in apps.get_models() if m._meta.app_label in APPS_DO_PROJETO}
    if set(achados) != set(ORDEM_DAS_TABELAS):
        raise SystemExit(
            f"Tabelas dos models {sorted(achados)} diferem de ORDEM_DAS_TABELAS {sorted(ORDEM_DAS_TABELAS)}: "
            "um model novo ou removido precisa entrar na configuração do gerador."
        )
    if len(achados) > MAXIMO_DE_ENTIDADES:
        raise SystemExit(f"{len(achados)} entidades (máximo {MAXIMO_DE_ENTIDADES}): divida o DER em duas figuras.")
    return achados


def _colunas_do_model(modelo):
    return [c for c in modelo._meta.concrete_fields]


def _descrever_valor(valor) -> str:
    from django.db.models import F
    from django.db.models.expressions import CombinedExpression, Value

    if isinstance(valor, F):
        return valor.name
    if isinstance(valor, Value):
        return _descrever_valor(valor.value)
    if isinstance(valor, CombinedExpression):
        return f"{_descrever_valor(valor.lhs)} {valor.connector} {_descrever_valor(valor.rhs)}"
    if isinstance(valor, (list, tuple, set, frozenset)):
        return "{" + ", ".join(_descrever_valor(v) for v in valor) + "}"
    if isinstance(valor, str):
        return f'"{valor}"'
    return str(valor)


def _descrever_q(q) -> str:
    partes = []
    for filho in q.children:
        if isinstance(filho, tuple):
            caminho, valor = filho
            campo, _, busca = caminho.partition("__")
            operador = OPERADORES.get(busca or "exact")
            if operador is None:
                raise SystemExit(f"Busca '{busca}' sem descrição no gerador (condição {caminho}).")
            if q.negated and len(q.children) == 1:
                operador = OPERADORES_NEGADOS[busca or "exact"]
            texto = f"{campo} {operador} {_descrever_valor(valor)}"
        else:
            texto = _descrever_q(filho)
            if len(q.children) > 1:
                texto = f"({texto})"
        partes.append(texto)
    juncao = " E " if q.connector == "AND" else " OU "
    texto = juncao.join(partes)
    if q.negated and not (len(q.children) == 1 and isinstance(q.children[0], tuple)):
        return f"NÃO ({texto})"
    return texto


def _colunas_da_condicao(q) -> set[str]:
    achadas = set()
    for filho in q.children:
        if isinstance(filho, tuple):
            achadas.add(filho[0].partition("__")[0])
            valor = filho[1]
            if hasattr(valor, "name"):
                achadas.add(valor.name)
            elif hasattr(valor, "get_source_expressions"):
                achadas |= {e.name for e in valor.get_source_expressions() if hasattr(e, "name")}
        else:
            achadas |= _colunas_da_condicao(filho)
    return achadas


def _expressao_do_intervalo(expressao) -> tuple[str, set[str]]:
    colunas = []
    limites = ""
    for origem in expressao.get_source_expressions():
        if hasattr(origem, "name"):
            colunas.append(origem.name)
        elif hasattr(origem, "lower") and hasattr(origem, "upper"):
            limites = origem.lower + origem.upper
        else:
            raise SystemExit(f"Parte {origem!r} da expressão de intervalo sem descrição no gerador.")
    return f"{expressao.function}({', '.join(colunas)}, '{limites}')", set(colunas)


def _restricoes_do_model(tabela, modelo):
    from django.contrib.postgres.constraints import ExclusionConstraint
    from django.db.models import CheckConstraint, UniqueConstraint
    from django.db.models.functions import Lower

    saida = []
    for campo in _colunas_do_model(modelo):
        if campo.unique and not campo.primary_key:
            saida.append({
                "tipo": "único", "tabela": tabela, "colunas": [campo.column], "marca": "UK",
                "definicao": f"{campo.column} único",
                "nome": "sem nome no model (`unique=True`)",
            })
    for restricao in modelo._meta.constraints:
        if isinstance(restricao, CheckConstraint):
            saida.append({
                "tipo": "check", "tabela": tabela, "marca": "ck", "nome": restricao.name,
                "colunas": sorted(_colunas_da_condicao(restricao.condition)),
                "definicao": _descrever_q(restricao.condition),
            })
        elif isinstance(restricao, ExclusionConstraint):
            textos, colunas = [], set()
            for expressao, operador in restricao.expressions:
                if hasattr(expressao, "function"):
                    texto, usadas = _expressao_do_intervalo(expressao)
                else:
                    nome = expressao if isinstance(expressao, str) else expressao.name
                    texto, usadas = nome, {nome}
                textos.append(f"{texto} {OPERADORES_DO_INTERVALO[operador]}")
                colunas |= usadas
            condicao = restricao.condition
            colunas |= _colunas_da_condicao(condicao)
            saida.append({
                "tipo": "exclusão", "tabela": tabela, "marca": "ex", "nome": restricao.name,
                "colunas": sorted(colunas),
                "definicao": f"entre linhas com {_descrever_q(condicao)}, nenhum par pode ter ao mesmo tempo: "
                + " e ".join(textos),
            })
        elif isinstance(restricao, UniqueConstraint):
            if not restricao.expressions or not all(isinstance(e, Lower) for e in restricao.expressions):
                raise SystemExit(f"UniqueConstraint {restricao.name}: só há descrição para Lower(campo).")
            colunas = [e.get_source_expressions()[0].name for e in restricao.expressions]
            saida.append({
                "tipo": "único", "tabela": tabela, "colunas": colunas, "marca": "UK", "nome": restricao.name,
                "definicao": ", ".join(f"LOWER({c})" for c in colunas) + " único (sem diferenciar maiúsculas)",
            })
        else:
            raise SystemExit(f"Restrição {restricao.name}: tipo {type(restricao).__name__} sem descrição no gerador.")
    return saida


def _conferir_referencias(modelos):
    achadas = {
        (t, c.column)
        for t, m in modelos.items()
        for c in _colunas_do_model(m)
        if c.get_internal_type() == "BigIntegerField" and c.column.endswith("_id")
    }
    declaradas = set(REFERENCIAS_POR_ID)
    if achadas != declaradas:
        raise SystemExit(
            f"Referências por id dos models {sorted(achadas)} diferem das declaradas {sorted(declaradas)}."
        )
    for (_, _), destino in REFERENCIAS_POR_ID.items():
        if destino not in modelos:
            raise SystemExit(f"Destino {destino} da referência por id não é uma tabela do projeto.")


def montar_estrutura():
    from django.db import connection

    modelos = _modelos()
    _conferir_referencias(modelos)
    restricoes = [r for t in ORDEM_DAS_TABELAS for r in _restricoes_do_model(t, modelos[t])]

    tabelas = []
    for tabela in ORDEM_DAS_TABELAS:
        modelo = modelos[tabela]
        em_restricoes = {c for r in restricoes if r["tabela"] == tabela for c in r["colunas"]}
        desejadas = set(COLUNAS_DE_NEGOCIO[tabela])
        todas = {c.column: c for c in _colunas_do_model(modelo)}
        faltando = desejadas - set(todas)
        if faltando:
            raise SystemExit(f"{tabela}: coluna(s) {sorted(faltando)} de COLUNAS_DE_NEGOCIO não existem no model.")
        colunas = []
        for coluna in todas.values():
            obrigatoria = (
                coluna.primary_key or coluna.is_relation
                or (tabela, coluna.column) in REFERENCIAS_POR_ID
                or coluna.column in em_restricoes
            )
            if not (obrigatoria or coluna.column in desejadas):
                continue
            tipo = coluna.get_internal_type()
            if tipo not in TIPO_NO_DESENHO:
                raise SystemExit(f"{tabela}.{coluna.column}: tipo {tipo} sem nome no desenho (TIPO_NO_DESENHO).")
            marcas = []
            if coluna.primary_key:
                marcas.append("PK")
            if coluna.is_relation:
                marcas.append("FK")
            if any(r["tabela"] == tabela and coluna.column in r["colunas"] and r["marca"] == "UK" for r in restricoes):
                marcas.append("UK")
            comentarios = []
            if (tabela, coluna.column) in REFERENCIAS_POR_ID:
                comentarios.append("ref. por id")
            for marca in ("ck", "ex"):
                if any(r["tabela"] == tabela and coluna.column in r["colunas"] and r["marca"] == marca for r in restricoes):
                    comentarios.append(marca)
            colunas.append({
                "nome": coluna.column,
                "tipo_no_desenho": TIPO_NO_DESENHO[tipo],
                "tipo_do_model": tipo,
                "tipo_do_banco": coluna.db_type(connection),
                "pk": coluna.primary_key,
                "fk": coluna.related_model._meta.db_table if coluna.is_relation else None,
                "aceita_nulo": coluna.null,
                "marcas": marcas,
                "comentario": ", ".join(comentarios),
            })
        if len(colunas) > MAXIMO_DE_COLUNAS:
            raise SystemExit(
                f"{tabela}: {len(colunas)} colunas (máximo {MAXIMO_DE_COLUNAS}): corte COLUNAS_DE_NEGOCIO "
                "ou divida o DER em duas figuras."
            )
        tabelas.append({"tabela": tabela, "colunas": colunas})

    relacoes = []
    for t in tabelas:
        for c in t["colunas"]:
            if c["fk"]:
                relacoes.append({"origem": c["fk"], "destino": t["tabela"], "coluna": c["nome"], "tipo": "fk",
                                 "aceita_nulo": c["aceita_nulo"]})
            elif (t["tabela"], c["nome"]) in REFERENCIAS_POR_ID:
                relacoes.append({"origem": REFERENCIAS_POR_ID[(t["tabela"], c["nome"])], "destino": t["tabela"],
                                 "coluna": c["nome"], "tipo": "id", "aceita_nulo": c["aceita_nulo"]})
    todas_as_fks = sorted(
        (m._meta.db_table, c.column) for m in modelos.values() for c in _colunas_do_model(m) if c.is_relation
    )
    return {"tabelas": tabelas, "relacoes": relacoes, "restricoes": restricoes, "fks_dos_models": todas_as_fks}


def gerar_mmd(estrutura) -> str:
    linhas = [
        "%% Gerado por scripts/gerar_der.py a partir dos models do Django (DOC-10). NÃO edite à mão:",
        "%% mudou um model ou uma migração -> gere de novo e rode scripts/verificar_der.py.",
        "%% FK real = linha contínua; referência por id, sem FK, entre contextos = linha pontilhada.",
        "erDiagram",
        "    direction LR",  # na vertical a figura passa de 25 cm a 16 cm de largura; assim fica com ~6,4 cm
    ]
    for r in estrutura["relacoes"]:
        ligacao = "--" if r["tipo"] == "fk" else ".."
        esquerda = "|o" if r["aceita_nulo"] else "||"
        rotulo = r["coluna"] if r["tipo"] == "fk" else f"{r['coluna']}: ref. por id, sem FK"
        linhas.append(f'    {r["origem"]} {esquerda}{ligacao}o{{ {r["destino"]} : "{rotulo}"')
    for t in estrutura["tabelas"]:
        linhas.append(f"    {t['tabela']} {{")
        for c in t["colunas"]:
            marcas = f" {', '.join(c['marcas'])}" if c["marcas"] else ""
            comentario = f' "{c["comentario"]}"' if c["comentario"] else ""
            linhas.append(f"        {c['tipo_no_desenho']} {c['nome']}{marcas}{comentario}")
        linhas.append("    }")
    return "\n".join(linhas) + "\n"


def gerar_restricoes(estrutura) -> str:
    linhas = [
        "| Restrição | Tabela | Definição | Nome no model |",
        "|---|---|---|---|",
    ]
    for r in estrutura["restricoes"]:
        nome = r["nome"] if " " in r["nome"] else f"`{r['nome']}`"
        definicao = r["definicao"].replace("|", "\\|")
        linhas.append(f"| {r['tipo']} | `{r['tabela']}` | {definicao} | {nome} |")
    return "\n".join(linhas) + "\n"


def main() -> int:
    modo = sys.argv[1] if len(sys.argv) > 1 else "--mmd"
    _preparar_django()
    estrutura = montar_estrutura()
    if modo == "--mmd":
        texto = gerar_mmd(estrutura)
    elif modo == "--restricoes":
        texto = gerar_restricoes(estrutura)
    elif modo == "--json":
        estrutura["mmd"] = gerar_mmd(estrutura)
        estrutura["tabela_de_restricoes"] = gerar_restricoes(estrutura)
        texto = json.dumps(estrutura, ensure_ascii=False, indent=1) + "\n"
    else:
        print("Uso: --mmd | --restricoes | --json", file=sys.stderr)
        return 2
    sys.stdout.buffer.write(texto.encode("utf-8"))
    return 0


sys.exit(main())
