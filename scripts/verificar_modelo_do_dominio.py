from __future__ import annotations

import argparse
import ast
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import verificar_visao_do_sistema as visao  # noqa: E402

RAIZ = visao.RAIZ
BACKEND = visao.BACKEND
GLOSSARIO = RAIZ / "docs" / "fontes" / "requisitos" / "glossario.md"
SETTINGS = BACKEND / "config" / "settings.py"
CONTEXTOS = ("espacos", "reservas", "contas")
DESCRICAO = "DOC-02: confere o modelo do domínio e a máquina de estados (docs/fontes/modelagem/*.mmd) contra o código."

ESTEREOTIPOS = {
    "entidade": "classe",
    "raiz do agregado": "classe",
    "objeto de valor": "dataclass",
    "enumeration": "enum",
    "Django model": "django",
}
CAMPOS_DJANGO = {
    "CharField": "str",
    "EmailField": "str",
    "BigIntegerField": "int",
    "PositiveIntegerField": "int",
    "IntegerField": "int",
    "BooleanField": "bool",
    "DateTimeField": "datetime",
}
CAMPOS_DE_RELACAO = ("ForeignKey", "OneToOneField", "ManyToManyField")
OCUPA = "ocupa o horário"

ANOTACAO = re.compile(r"^%%\s*(classe|referencia-por-id|nota|papel|motivo):\s*(.*)$")
CLASSE = re.compile(r"^class\s+(\w+)\s*(\{)?$")
NAMESPACE = re.compile(r"^namespace\s+(\w+)\s*\{$")
METODO = re.compile(r"^[+\-#~]?(\w+)\((.*?)\)([$*])?\s*(.*)$")
ATRIBUTO = re.compile(r"^[+\-#~]?(\w+)\s*:\s*(.+)$")
VALOR = re.compile(r"^(\w+)$")
RELACAO = re.compile(
    r'^(\w+)\s*(?:"([^"]*)")?\s*(\*--|-->|\.\.>|\.\.|<--|--|<\|--|o--)\s*(?:"([^"]*)")?\s*(\w+)\s*(?::\s*(.*))?$'
)
TRANSICAO = re.compile(r"^(\[\*\]|\w+)\s*-->\s*(\[\*\]|\w+)(?:\s*:\s*(.*))?$")
COMPOSTO = re.compile(r'^state\s+"([^"]*)"\s+as\s+(\w+)\s*\{$')
ESTADO_COM_ROTULO = re.compile(r'^state\s+"([^"]*)"\s+as\s+(\w+)$')
DESCRICAO_DE_ESTADO = re.compile(r"^(\w+)\s*:\s*(.+)$")
IGNORAR = re.compile(r"^(classDiagram|stateDiagram(-v2)?|direction\b|classDef\b|class\s+\w+\s+\w+$|style\b|note\b)")


def normalizar_tipo(tipo: str) -> str:
    return re.sub(r"\s+", "", tipo).replace("'", "").replace('"', "")


@dataclass
class Membro:
    nome: str
    tipo: str
    linha: int
    parametros: list[str] | None = None
    de_classe: bool = False


@dataclass
class ClasseDoDiagrama:
    nome: str
    linha: int
    namespace: str | None
    estereotipo: str | None = None
    atributos: list[Membro] = field(default_factory=list)
    metodos: list[Membro] = field(default_factory=list)
    valores: list[Membro] = field(default_factory=list)


@dataclass
class Relacao:
    origem: str
    seta: str
    destino: str
    rotulo: str
    linha: int


@dataclass
class DiagramaDeClasses:
    nome: str
    classes: dict[str, ClasseDoDiagrama] = field(default_factory=dict)
    relacoes: list[Relacao] = field(default_factory=list)
    mapeamento: dict[str, str] = field(default_factory=dict)
    referencias: list[tuple[str, str, str, str]] = field(default_factory=list)
    notas: list[tuple[str, str, str]] = field(default_factory=list)


@dataclass
class Transicao:
    origem: str
    destino: str
    rotulo: str
    linha: int


@dataclass
class DiagramaDeEstados:
    nome: str
    transicoes: list[Transicao] = field(default_factory=list)
    compostos: dict[str, tuple[str, list[str]]] = field(default_factory=dict)
    descricoes: dict[str, str] = field(default_factory=dict)
    estados: set[str] = field(default_factory=set)
    papeis: dict[str, str] = field(default_factory=dict)
    motivo: str | None = None


def tipo_do_diagrama(caminho: Path) -> str | None:
    for bruta in caminho.read_text(encoding="utf-8").splitlines():
        linha = bruta.strip()
        if linha and not linha.startswith("%%"):
            if linha.startswith("classDiagram"):
                return "classes"
            if linha.startswith("stateDiagram"):
                return "estados"
            return None
    return None


def ler_diagrama_de_classes(caminho: Path, resultado: visao.Resultado) -> DiagramaDeClasses:
    figura = DiagramaDeClasses(caminho.name)
    namespace: str | None = None
    atual: ClasseDoDiagrama | None = None
    for numero, bruta in enumerate(caminho.read_text(encoding="utf-8").splitlines(), start=1):
        linha = bruta.strip()
        onde = f"{figura.nome}:{numero}"
        if not linha or linha.startswith("%%{"):
            continue
        if anotacao := ANOTACAO.match(linha):
            ler_anotacao_de_classes(figura, anotacao.group(1), anotacao.group(2).strip(), onde, resultado)
            continue
        if linha.startswith("%%"):
            continue
        if atual is not None:
            if linha == "}":
                atual = None
            else:
                ler_membro(atual, linha, numero, onde, resultado)
            continue
        if linha == "}":
            if namespace is None:
                resultado.erro(f"{onde}: '}}' sem namespace nem classe aberta")
            namespace = None
            continue
        if ns := NAMESPACE.match(linha):
            namespace = ns.group(1)
            continue
        if cl := CLASSE.match(linha):
            classe = ClasseDoDiagrama(cl.group(1), numero, namespace)
            figura.classes[classe.nome] = classe
            atual = classe if cl.group(2) else None
            continue
        if rel := RELACAO.match(linha):
            origem, _, seta, _, destino, rotulo = rel.groups()
            figura.relacoes.append(Relacao(origem, seta, destino, (rotulo or "").strip(), numero))
            continue
        if IGNORAR.match(linha):
            continue
        resultado.erro(f"{onde}: linha não reconhecida: {linha}")
    if atual is not None or namespace is not None:
        resultado.erro(f"{figura.nome}: classe ou namespace sem '}}'")
    return figura


def ler_anotacao_de_classes(figura: DiagramaDeClasses, chave: str, valor: str, onde: str,
                            resultado: visao.Resultado) -> None:
    if chave == "classe":
        nome, igual, alvo = valor.partition("=")
        if not igual:
            resultado.erro(f"{onde}: anotação 'classe' sem '='")
            return
        figura.mapeamento[nome.strip()] = alvo.strip()
    elif chave == "referencia-por-id":
        casado = re.fullmatch(r"(\w+)\.(\w+)\s*->\s*(\w+)\s*\|\s*([\w.]+)", valor)
        if not casado:
            resultado.erro(f"{onde}: anotação 'referencia-por-id' fora do formato")
            return
        figura.referencias.append(casado.groups())
    elif chave == "nota":
        partes = [p.strip() for p in valor.split("|")]
        if len(partes) != 3:
            resultado.erro(f"{onde}: anotação 'nota' fora do formato (Classe | arquivo | trecho)")
            return
        figura.notas.append(tuple(partes))
    else:
        resultado.erro(f"{onde}: anotação '{chave}' não vale num classDiagram")


def ler_membro(classe: ClasseDoDiagrama, linha: str, numero: int, onde: str, resultado: visao.Resultado) -> None:
    if est := re.fullmatch(r"<<(.+)>>", linha):
        classe.estereotipo = est.group(1).strip()
    elif met := METODO.match(linha):
        nome, parametros, modificador, retorno = met.groups()
        lista = [p.strip() for p in parametros.split(",") if p.strip()]
        classe.metodos.append(Membro(nome, retorno.strip(), numero, lista, modificador == "$"))
    elif atr := ATRIBUTO.match(linha):
        classe.atributos.append(Membro(atr.group(1), atr.group(2).strip(), numero))
    elif val := VALOR.match(linha):
        classe.valores.append(Membro(val.group(1), "", numero))
    else:
        resultado.erro(f"{onde}: membro não reconhecido em {classe.nome}: {linha}")


def ler_diagrama_de_estados(caminho: Path, resultado: visao.Resultado) -> DiagramaDeEstados:
    figura = DiagramaDeEstados(caminho.name)
    composto: str | None = None
    em_nota = False
    for numero, bruta in enumerate(caminho.read_text(encoding="utf-8").splitlines(), start=1):
        linha = bruta.strip()
        onde = f"{figura.nome}:{numero}"
        if em_nota:
            em_nota = linha != "end note"
            continue
        if not linha or linha.startswith("%%{"):
            continue
        if anotacao := ANOTACAO.match(linha):
            chave, valor = anotacao.group(1), anotacao.group(2).strip()
            if chave == "papel":
                nome, _, texto = valor.partition("=")
                figura.papeis[nome.strip()] = texto.strip()
            elif chave == "motivo":
                figura.motivo = valor
            else:
                resultado.erro(f"{onde}: anotação '{chave}' não vale num stateDiagram")
            continue
        if linha.startswith("%%"):
            continue
        if linha.startswith("note ") and not linha.startswith("note \""):
            em_nota = ":" not in linha
            continue
        if linha == "}":
            if composto is None:
                resultado.erro(f"{onde}: '}}' sem estado composto aberto")
            composto = None
            continue
        if comp := COMPOSTO.match(linha):
            composto = comp.group(2)
            figura.compostos[composto] = (comp.group(1), [])
            continue
        if ESTADO_COM_ROTULO.match(linha):
            continue
        if tr := TRANSICAO.match(linha):
            origem, destino, rotulo = tr.groups()
            figura.transicoes.append(Transicao(origem, destino, (rotulo or "").strip(), numero))
            figura.estados.update(e for e in (origem, destino) if e != "[*]")
            continue
        if composto is not None and VALOR.match(linha):
            figura.compostos[composto][1].append(linha)
            figura.estados.add(linha)
            continue
        if IGNORAR.match(linha):
            continue
        if desc := DESCRICAO_DE_ESTADO.match(linha):
            figura.descricoes[desc.group(1)] = desc.group(2)
            figura.estados.add(desc.group(1))
            continue
        resultado.erro(f"{onde}: linha não reconhecida: {linha}")
    return figura


@dataclass
class Simbolo:
    tipo: str | None
    linha: int
    parametros: list[str] = field(default_factory=list)
    de_classe: bool = False


@dataclass
class ClasseDoCodigo:
    nome: str
    arquivo: str
    linha: int
    tipo: str
    atributos: dict[str, Simbolo] = field(default_factory=dict)
    metodos: dict[str, Simbolo] = field(default_factory=dict)
    privados: set[str] = field(default_factory=set)
    valores: list[tuple[str, int]] = field(default_factory=list)
    campos_django: dict[str, tuple[str, int]] = field(default_factory=dict)


_ARVORES: dict[Path, ast.Module] = {}


def arvore(arquivo: Path) -> ast.Module:
    if arquivo not in _ARVORES:
        _ARVORES[arquivo] = ast.parse(arquivo.read_text(encoding="utf-8"))
    return _ARVORES[arquivo]


def arquivo_do_modulo(modulo: str) -> Path:
    return BACKEND.joinpath(*modulo.split(".")).with_suffix(".py")


def nome_do_decorador(no: ast.expr) -> str:
    alvo = no.func if isinstance(no, ast.Call) else no
    return ast.unparse(alvo)


def tipo_da_classe(no: ast.ClassDef) -> str:
    bases = {ast.unparse(b) for b in no.bases}
    if bases & {"StrEnum", "Enum", "IntEnum", "enum.Enum", "enum.StrEnum"}:
        return "enum"
    if bases & {"models.Model", "AbstractUser", "AbstractBaseUser"}:
        return "django"
    for decorador in no.decorator_list:
        if nome_do_decorador(decorador) == "dataclass":
            congelada = isinstance(decorador, ast.Call) and any(
                k.arg == "frozen" and isinstance(k.value, ast.Constant) and k.value.value is True
                for k in decorador.keywords
            )
            return "dataclass" if congelada else "dataclass-mutavel"
    return "classe"


def parametros_de(funcao: ast.FunctionDef) -> list[ast.arg]:
    todos = [*funcao.args.posonlyargs, *funcao.args.args, *funcao.args.kwonlyargs]
    return [a for a in todos if a.arg not in ("self", "cls")]


def tipo_da_expressao(valor: ast.expr, parametros: dict[str, str], funcoes: dict[str, ast.FunctionDef]) -> str | None:
    if isinstance(valor, ast.Name) and valor.id in parametros:
        return parametros[valor.id]
    if isinstance(valor, ast.Call) and isinstance(valor.func, ast.Name):
        funcao = funcoes.get(valor.func.id)
        if funcao is not None and funcao.returns is not None:
            return ast.unparse(funcao.returns)
        if valor.args and isinstance(valor.args[0], ast.Name) and valor.args[0].id in parametros:
            return parametros[valor.args[0].id]
    return None


def ler_classe(modulo_e_classe: str) -> ClasseDoCodigo | None:
    modulo, _, nome = modulo_e_classe.rpartition(".")
    arquivo = arquivo_do_modulo(modulo)
    if not arquivo.is_file():
        return None
    modulo_ast = arvore(arquivo)
    funcoes = {n.name: n for n in modulo_ast.body if isinstance(n, ast.FunctionDef)}
    no = next((n for n in modulo_ast.body if isinstance(n, ast.ClassDef) and n.name == nome), None)
    if no is None:
        return None
    classe = ClasseDoCodigo(nome, arquivo.relative_to(BACKEND).as_posix(), no.lineno, tipo_da_classe(no))
    for item in no.body:
        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
            classe.atributos[item.target.id] = Simbolo(ast.unparse(item.annotation), item.lineno)
        elif isinstance(item, ast.Assign) and len(item.targets) == 1 and isinstance(item.targets[0], ast.Name):
            ler_atribuicao_de_classe(classe, item.targets[0].id, item)
        elif isinstance(item, ast.FunctionDef):
            ler_funcao(classe, item, funcoes)
    return classe


def ler_atribuicao_de_classe(classe: ClasseDoCodigo, nome: str, item: ast.Assign) -> None:
    if classe.tipo == "enum" and not nome.startswith("_"):
        classe.valores.append((nome, item.lineno))
    elif classe.tipo == "django" and isinstance(item.value, ast.Call):
        campo = ast.unparse(item.value.func).rpartition(".")[2]
        classe.campos_django[nome] = (campo, item.lineno)
        if campo in CAMPOS_DJANGO:
            classe.atributos[nome] = Simbolo(CAMPOS_DJANGO[campo], item.lineno)


def ler_funcao(classe: ClasseDoCodigo, item: ast.FunctionDef, funcoes: dict[str, ast.FunctionDef]) -> None:
    decoradores = {nome_do_decorador(d) for d in item.decorator_list}
    retorno = ast.unparse(item.returns) if item.returns is not None else None
    if "property" in decoradores:
        classe.atributos[item.name] = Simbolo(retorno, item.lineno)
        return
    if item.name == "__init__":
        anotados = {a.arg: ast.unparse(a.annotation) for a in parametros_de(item) if a.annotation is not None}
        for no in ast.walk(item):
            if isinstance(no, ast.Assign):
                for alvo in no.targets:
                    if isinstance(alvo, ast.Attribute) and isinstance(alvo.value, ast.Name) and alvo.value.id == "self":
                        if not alvo.attr.startswith("_") and alvo.attr not in classe.atributos:
                            tipo = tipo_da_expressao(no.value, anotados, funcoes)
                            classe.atributos[alvo.attr] = Simbolo(tipo, no.lineno)
        return
    if item.name.startswith("_"):
        classe.privados.add(item.name)
        return
    de_classe = bool(decoradores & {"classmethod", "staticmethod"})
    classe.metodos[item.name] = Simbolo(retorno, item.lineno, [a.arg for a in parametros_de(item)], de_classe)


def auto_field_do_settings() -> tuple[str, int] | None:
    for numero, linha in enumerate(SETTINGS.read_text(encoding="utf-8").splitlines(), start=1):
        if casado := re.match(r'^DEFAULT_AUTO_FIELD\s*=\s*"([^"]+)"', linha):
            return casado.group(1), numero
    return None


def verificar_classes(figura: DiagramaDeClasses, resultado: visao.Resultado,
                      evidencia: list[tuple[str, str, str]]) -> dict[str, ClasseDoCodigo]:
    codigo: dict[str, ClasseDoCodigo] = {}
    for nome in figura.mapeamento:
        if nome not in figura.classes:
            resultado.erro(f"{figura.nome}: '%% classe: {nome}' cita uma classe que não está na figura")
    for nome, classe in figura.classes.items():
        onde = f"{figura.nome}:{classe.linha}"
        alvo = figura.mapeamento.get(nome)
        if alvo is None:
            resultado.erro(f"{onde}: a classe {nome} não tem '%% classe: {nome} = modulo.Classe'")
            continue
        modulo, _, nome_no_codigo = alvo.rpartition(".")
        if nome_no_codigo != nome:
            resultado.erro(f"{onde}: a figura chama de {nome} a classe {nome_no_codigo} de {modulo}: use o nome do código")
        lida = ler_classe(alvo)
        if lida is None:
            resultado.erro(f"{onde}: a classe {nome} não existe em {modulo} ({arquivo_do_modulo(modulo).relative_to(RAIZ).as_posix()})")
            continue
        codigo[nome] = lida
        evidencia.append((figura.nome, f"classe {nome}", f"{lida.arquivo}:{lida.linha}"))
        contexto = modulo.split(".")[0]
        if classe.namespace != contexto:
            resultado.erro(f"{onde}: {nome} está no namespace '{classe.namespace}', mas o módulo é de '{contexto}'")
        verificar_estereotipo(classe, lida, onde, resultado)
        verificar_atributos(figura, classe, lida, resultado, evidencia)
        verificar_metodos(figura, classe, lida, resultado, evidencia)
        verificar_valores(figura, classe, lida, resultado, evidencia)
    return codigo


def verificar_estereotipo(classe: ClasseDoDiagrama, lida: ClasseDoCodigo, onde: str, resultado: visao.Resultado) -> None:
    if classe.estereotipo is None:
        resultado.erro(f"{onde}: {classe.nome} sem «estereótipo»")
        return
    esperado = ESTEREOTIPOS.get(classe.estereotipo)
    if esperado is None:
        resultado.erro(f"{onde}: estereótipo «{classe.estereotipo}» sem regra (use um de: {', '.join(ESTEREOTIPOS)})")
    elif esperado != lida.tipo:
        resultado.erro(f"{onde}: {classe.nome} é «{classe.estereotipo}» na figura, mas no código é '{lida.tipo}' "
                       f"({lida.arquivo}:{lida.linha})")


def verificar_atributos(figura: DiagramaDeClasses, classe: ClasseDoDiagrama, lida: ClasseDoCodigo,
                        resultado: visao.Resultado, evidencia: list[tuple[str, str, str]]) -> None:
    for atributo in classe.atributos:
        onde = f"{figura.nome}:{atributo.linha}"
        simbolo = lida.atributos.get(atributo.nome)
        if simbolo is None and atributo.nome == "id" and lida.tipo == "django" and "id" not in lida.campos_django:
            auto = auto_field_do_settings()
            if auto and normalizar_tipo(atributo.tipo) == "int":
                evidencia.append((figura.nome, f"{classe.nome}.id: int", f"config/settings.py:{auto[1]} ({auto[0]})"))
                continue
        if simbolo is None:
            resultado.erro(f"{onde}: {classe.nome}.{atributo.nome} não existe em {lida.arquivo} "
                           "(campo, property ou self.x no __init__)")
            continue
        if simbolo.tipo is None:
            resultado.erro(f"{onde}: {classe.nome}.{atributo.nome} não tem tipo anotado no código ({lida.arquivo}:{simbolo.linha})")
        elif normalizar_tipo(simbolo.tipo) != normalizar_tipo(atributo.tipo):
            resultado.erro(f"{onde}: {classe.nome}.{atributo.nome} é '{atributo.tipo}' na figura e "
                           f"'{simbolo.tipo}' no código ({lida.arquivo}:{simbolo.linha})")
        evidencia.append((figura.nome, f"{classe.nome}.{atributo.nome}: {atributo.tipo}", f"{lida.arquivo}:{simbolo.linha}"))


def verificar_metodos(figura: DiagramaDeClasses, classe: ClasseDoDiagrama, lida: ClasseDoCodigo,
                      resultado: visao.Resultado, evidencia: list[tuple[str, str, str]]) -> None:
    for metodo in classe.metodos:
        onde = f"{figura.nome}:{metodo.linha}"
        if metodo.nome.startswith("_"):
            resultado.erro(f"{onde}: {classe.nome}.{metodo.nome} é privado ou dunder: a figura só mostra métodos públicos")
            continue
        simbolo = lida.metodos.get(metodo.nome)
        if simbolo is None:
            motivo = "é uma property (vai entre os atributos)" if metodo.nome in lida.atributos else "não existe"
            resultado.erro(f"{onde}: o método {classe.nome}.{metodo.nome} {motivo} em {lida.arquivo}")
            continue
        listados = metodo.parametros or []
        if listados != ["…"] and listados != simbolo.parametros:
            resultado.erro(f"{onde}: {classe.nome}.{metodo.nome}({', '.join(listados)}) na figura; no código os "
                           f"parâmetros são ({', '.join(simbolo.parametros)})")
        if normalizar_tipo(simbolo.tipo or "") != normalizar_tipo(metodo.tipo):
            resultado.erro(f"{onde}: {classe.nome}.{metodo.nome} devolve '{metodo.tipo}' na figura e '{simbolo.tipo}' no código")
        if metodo.de_classe != simbolo.de_classe:
            resultado.erro(f"{onde}: {classe.nome}.{metodo.nome}: '$' (método de classe) não bate com o decorador do código")
        evidencia.append((figura.nome, f"{classe.nome}.{metodo.nome}()", f"{lida.arquivo}:{simbolo.linha}"))


def verificar_valores(figura: DiagramaDeClasses, classe: ClasseDoDiagrama, lida: ClasseDoCodigo,
                      resultado: visao.Resultado, evidencia: list[tuple[str, str, str]]) -> None:
    if lida.tipo != "enum":
        for valor in classe.valores:
            resultado.erro(f"{figura.nome}:{valor.linha}: membro '{valor.nome}' sem tipo em {classe.nome}, que não é enum")
        return
    na_figura = [v.nome for v in classe.valores]
    no_codigo = [nome for nome, _ in lida.valores]
    if na_figura != no_codigo:
        resultado.erro(f"{figura.nome}:{classe.linha}: valores de {classe.nome} na figura {na_figura}; "
                       f"no código {no_codigo} ({lida.arquivo}:{lida.linha})")
    for nome, linha in lida.valores:
        if nome in na_figura:
            evidencia.append((figura.nome, f"{classe.nome}.{nome}", f"{lida.arquivo}:{linha}"))


def verificar_relacoes(figura: DiagramaDeClasses, codigo: dict[str, ClasseDoCodigo], resultado: visao.Resultado,
                       evidencia: list[tuple[str, str, str]]) -> None:
    referencias = {(o, a, d): coluna for o, a, d, coluna in figura.referencias}
    desenhadas = set()
    for rel in figura.relacoes:
        onde = f"{figura.nome}:{rel.linha} {rel.origem} {rel.seta} {rel.destino}"
        if rel.origem not in figura.classes or rel.destino not in figura.classes:
            resultado.erro(f"{onde}: liga uma classe que não está na figura")
            continue
        if rel.seta == "..":
            desenhadas.add((rel.origem, rel.rotulo, rel.destino))
        origem = codigo.get(rel.origem)
        if origem is None:
            continue
        if rel.seta in ("*--", "-->"):
            verificar_atributo_da_relacao(figura.nome, rel, origem, onde, resultado, evidencia)
        elif rel.seta == "..":
            verificar_referencia_por_id(figura, rel, origem, referencias, onde, resultado, evidencia)
        else:
            resultado.erro(f"{onde}: tipo de linha '{rel.seta}' sem regra nesta figura (use *--, --> ou ..)")
    for chave in referencias:
        if chave not in desenhadas:
            resultado.erro(f"{figura.nome}: referencia-por-id {chave[0]}.{chave[1]} -> {chave[2]} sem a linha tracejada")


def verificar_atributo_da_relacao(nome_da_figura: str, rel: Relacao, origem: ClasseDoCodigo, onde: str, resultado: visao.Resultado,
                                  evidencia: list[tuple[str, str, str]]) -> None:
    simbolo = origem.atributos.get(rel.rotulo)
    if simbolo is None:
        resultado.erro(f"{onde}: o rótulo '{rel.rotulo}' não é atributo de {rel.origem} no código")
        return
    if not re.search(rf"\b{rel.destino}\b", simbolo.tipo or ""):
        resultado.erro(f"{onde}: {rel.origem}.{rel.rotulo} é '{simbolo.tipo}' no código, não um {rel.destino}")
        return
    tipo = "composição" if rel.seta == "*--" else "associação"
    evidencia.append((nome_da_figura, f"{rel.origem} → {rel.destino} ({tipo}, {rel.rotulo})",
                      f"{origem.arquivo}:{simbolo.linha} `{simbolo.tipo}`"))


def verificar_referencia_por_id(figura: DiagramaDeClasses, rel: Relacao, origem: ClasseDoCodigo,
                                referencias: dict[tuple[str, str, str], str], onde: str,
                                resultado: visao.Resultado, evidencia: list[tuple[str, str, str]]) -> None:
    coluna = referencias.get((rel.origem, rel.rotulo, rel.destino))
    if coluna is None:
        resultado.erro(f"{onde}: linha tracejada sem '%% referencia-por-id: {rel.origem}.{rel.rotulo} -> {rel.destino} | coluna'")
        return
    simbolo = origem.atributos.get(rel.rotulo)
    if not rel.rotulo.endswith("_id") or simbolo is None or normalizar_tipo(simbolo.tipo or "") != "int":
        resultado.erro(f"{onde}: '{rel.rotulo}' não é um atributo *_id: int de {rel.origem} no código")
        return
    if figura.classes[rel.origem].namespace == figura.classes[rel.destino].namespace:
        resultado.erro(f"{onde}: referência por id dentro do mesmo contexto; use composição ou associação")
    modelo = ler_classe(coluna.rpartition(".")[0])
    campo = coluna.rpartition(".")[2]
    if modelo is None or campo not in modelo.campos_django:
        resultado.erro(f"{onde}: a coluna {coluna} não existe")
        return
    tipo_do_campo, linha = modelo.campos_django[campo]
    if tipo_do_campo != "BigIntegerField":
        resultado.erro(f"{onde}: a coluna {coluna} é {tipo_do_campo}; uma referência por id entre contextos é BigIntegerField")
        return
    evidencia.append((figura.nome, f"{rel.origem}.{rel.rotulo} ‥ {rel.destino} (por id)",
                      f"{origem.arquivo}:{simbolo.linha}; {modelo.arquivo}:{linha} BigIntegerField"))


def verificar_notas(figura: DiagramaDeClasses, resultado: visao.Resultado, evidencia: list[tuple[str, str, str]]) -> None:
    for classe, arquivo, trecho in figura.notas:
        if classe not in figura.classes:
            resultado.erro(f"{figura.nome}: '%% nota: {classe}' cita uma classe que não está na figura")
        caminho = RAIZ / arquivo
        if not caminho.is_file():
            resultado.erro(f"{figura.nome}: a nota de {classe} cita '{arquivo}', que não existe")
            continue
        linhas = caminho.read_text(encoding="utf-8").splitlines()
        numero = next((i for i, t in enumerate(linhas, 1) if trecho in t), None)
        if numero is None:
            resultado.erro(f"{figura.nome}: o trecho '{trecho}' da nota de {classe} não está em {arquivo}")
            continue
        evidencia.append((figura.nome, f"nota de {classe}", f"{arquivo}:{numero} `{trecho}`"))


def app_do_alvo(alvo: ast.expr, app: str, imports: dict[str, str], locais: set[str]) -> str | None:
    if isinstance(alvo, ast.Constant) and isinstance(alvo.value, str):
        return app if "." not in alvo.value else alvo.value.split(".")[0]
    nome = ast.unparse(alvo)
    if nome in locais:
        return app
    return imports.get(nome, "?").split(".")[0]


def verificar_chaves_estrangeiras(resultado: visao.Resultado, evidencia: list[tuple[str, str, str]]) -> None:
    for app in CONTEXTOS:
        arquivo = BACKEND / app / "infrastructure" / "models.py"
        modulo = arvore(arquivo)
        locais = {n.name for n in modulo.body if isinstance(n, ast.ClassDef)}
        imports = {a.asname or a.name: f"{n.module}.{a.name}" for n in modulo.body
                   if isinstance(n, ast.ImportFrom) and n.module for a in n.names}
        for no in ast.walk(modulo):
            if not (isinstance(no, ast.Call) and ast.unparse(no.func).rpartition(".")[2] in CAMPOS_DE_RELACAO):
                continue
            alvo = no.args[0] if no.args else next((k.value for k in no.keywords if k.arg == "to"), None)
            destino = app_do_alvo(alvo, app, imports, locais) if alvo is not None else "?"
            rel = arquivo.relative_to(BACKEND).as_posix()
            if destino != app:
                resultado.erro(f"{rel}:{no.lineno}: chave estrangeira de '{app}' para '{destino}' "
                               "(entre contextos): a figura só mostra referências por id")
            else:
                evidencia.append(("(banco)", f"FK dentro de {app}: {ast.unparse(alvo)}", f"{rel}:{no.lineno}"))


def nomes_do_glossario() -> set[str]:
    nomes: set[str] = set()
    coluna = None
    for linha in GLOSSARIO.read_text(encoding="utf-8").splitlines():
        if not linha.startswith("|"):
            coluna = None
            continue
        celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
        if "Nome no código" in celulas:
            coluna = celulas.index("Nome no código")
            continue
        if coluna is not None and coluna < len(celulas):
            for trecho in re.findall(r"`([^`]+)`", celulas[coluna]):
                nomes.update(re.findall(r"[A-Za-z_]\w*", trecho))
    return nomes


def verificar_glossario(figura: DiagramaDeClasses, resultado: visao.Resultado) -> None:
    nomes = nomes_do_glossario()
    for nome in figura.classes:
        if nome not in nomes:
            resultado.avisos.append(f"{nome} não aparece na coluna 'Nome no código' do glossário: registre a pendência "
                                    "no README da modelagem (o glossário não muda nesta tarefa)")


def importar_dominio_de_reservas():
    sys.path.insert(0, str(BACKEND))
    from reservas.domain import ator, situacao  # noqa: PLC0415

    return ator, situacao


def linhas_das_tabelas() -> dict[str, int]:
    arquivo = BACKEND / "reservas" / "domain" / "situacao.py"
    linhas: dict[str, int] = {}
    for no in arvore(arquivo).body:
        alvo = no.target if isinstance(no, ast.AnnAssign) else (no.targets[0] if isinstance(no, ast.Assign) else None)
        if isinstance(alvo, ast.Name):
            linhas[alvo.id] = no.lineno
            if isinstance(no.value, ast.Dict):
                for chave in no.value.keys:
                    if chave is not None:
                        linhas[f"{alvo.id}[{ast.unparse(chave)}]"] = chave.lineno
    return linhas


def estado_inicial_do_codigo() -> tuple[str | None, int]:
    classe = next(n for n in arvore(BACKEND / "reservas" / "domain" / "reserva.py").body
                  if isinstance(n, ast.ClassDef) and n.name == "Reserva")
    solicitar = next(n for n in classe.body if isinstance(n, ast.FunctionDef) and n.name == "solicitar")
    for no in ast.walk(solicitar):
        if isinstance(no, ast.Call) and ast.unparse(no.func) == "cls":
            for k in no.keywords:
                if k.arg == "situacao" and isinstance(k.value, ast.Attribute):
                    return k.value.attr, k.value.lineno
    return None, solicitar.lineno


def partes_do_rotulo(rotulo: str) -> list[str]:
    return [p.strip() for p in re.split(r"\s*·\s*|<br\s*/?>", rotulo) if p.strip()]


def verificar_estados(figura: DiagramaDeEstados, resultado: visao.Resultado,
                      evidencia: list[tuple[str, str, str]]) -> None:
    ator, situacao = importar_dominio_de_reservas()
    Situacao, Papel = situacao.SituacaoReserva, ator.PapelDoAtor
    arquivo = "reservas/domain/situacao.py"
    linhas = linhas_das_tabelas()
    nomes = {s.name for s in Situacao}

    for estado in sorted(figura.estados - nomes):
        resultado.erro(f"{figura.nome}: o estado {estado} não é um valor de SituacaoReserva")
    if set(figura.papeis) != {p.name for p in Papel}:
        resultado.erro(f"{figura.nome}: '%% papel:' cobre {sorted(figura.papeis)}; PapelDoAtor tem {[p.name for p in Papel]}")
        return
    if not figura.motivo:
        resultado.erro(f"{figura.nome}: falta '%% motivo: <texto>' (o texto de 'motivo obrigatório' nos rótulos)")
        return

    esperadas = {(a.name, b.name) for a, destinos in situacao.TRANSICOES_PERMITIDAS.items() for b in destinos}
    desenhadas = {(t.origem, t.destino): t for t in figura.transicoes if "[*]" not in (t.origem, t.destino)}
    for par in sorted(set(desenhadas) - esperadas):
        t = desenhadas[par]
        resultado.erro(f"{figura.nome}:{t.linha}: a transição {par[0]} → {par[1]} não está em TRANSICOES_PERMITIDAS "
                       f"({arquivo}:{linhas['TRANSICOES_PERMITIDAS']})")
    for par in sorted(esperadas - set(desenhadas)):
        resultado.erro(f"{figura.nome}: falta a transição {par[0]} → {par[1]} de TRANSICOES_PERMITIDAS "
                       f"({arquivo}:{linhas[f'TRANSICOES_PERMITIDAS[SituacaoReserva.{par[0]}]']})")
    for par in sorted(set(desenhadas) & esperadas):
        verificar_rotulo(figura, desenhadas[par], Situacao[par[1]], situacao, Papel, resultado)
        evidencia.append((figura.nome, f"{par[0]} → {par[1]}: {desenhadas[par].rotulo}",
                          f"{arquivo}:{linhas[f'TRANSICOES_PERMITIDAS[SituacaoReserva.{par[0]}]']}; "
                          f"rótulo {arquivo}:{linhas[f'_ROTULOS_DAS_ACOES[SituacaoReserva.{par[1]}]']}; "
                          f"papéis {arquivo}:{linhas['DESTINOS_POR_PAPEL']}"))

    verificar_inicio_e_fim(figura, Situacao, resultado, evidencia, arquivo, linhas)
    verificar_ocupa_o_horario(figura, situacao, resultado, evidencia, arquivo, linhas)


def verificar_rotulo(figura: DiagramaDeEstados, t: Transicao, destino, situacao, Papel, resultado: visao.Resultado) -> None:
    onde = f"{figura.nome}:{t.linha} {t.origem} → {t.destino}"
    partes = partes_do_rotulo(t.rotulo)
    acao = destino.rotulo_da_acao
    papeis = " ou ".join(figura.papeis[p.name] for p in Papel if destino in situacao.DESTINOS_POR_PAPEL[p])
    esperado = [acao, papeis] + ([figura.motivo] if destino in situacao.SITUACOES_QUE_EXIGEM_MOTIVO else [])
    if partes[:1] != [acao]:
        resultado.erro(f"{onde}: a ação é '{partes[0] if partes else ''}'; rotulo_da_acao de {destino.name} é '{acao}'")
    if partes[1:2] != [papeis]:
        resultado.erro(f"{onde}: quem pode é '{partes[1] if len(partes) > 1 else ''}'; por DESTINOS_POR_PAPEL é '{papeis}'")
    tem_motivo = figura.motivo in partes
    exige = destino in situacao.SITUACOES_QUE_EXIGEM_MOTIVO
    if tem_motivo != exige:
        estado = "exige" if exige else "não exige"
        resultado.erro(f"{onde}: '{figura.motivo}' {'falta' if exige else 'sobra'} no rótulo: {destino.name} {estado} "
                       "motivo (SITUACOES_QUE_EXIGEM_MOTIVO)")
    if partes != esperado and partes[:1] == [acao] and partes[1:2] == [papeis] and tem_motivo == exige:
        resultado.erro(f"{onde}: rótulo '{t.rotulo}'; esperado '{' · '.join(esperado)}'")


def verificar_inicio_e_fim(figura: DiagramaDeEstados, Situacao, resultado: visao.Resultado,
                           evidencia: list[tuple[str, str, str]], arquivo: str, linhas: dict[str, int]) -> None:
    iniciais = [t for t in figura.transicoes if t.origem == "[*]"]
    inicial, linha = estado_inicial_do_codigo()
    if [t.destino for t in iniciais] != [inicial]:
        resultado.erro(f"{figura.nome}: o estado inicial é {[t.destino for t in iniciais]}; "
                       f"Reserva.solicitar cria em {inicial} (reservas/domain/reserva.py:{linha})")
    else:
        evidencia.append((figura.nome, f"[*] → {inicial}", f"reservas/domain/reserva.py:{linha} Reserva.solicitar"))
    finais = {t.origem for t in figura.transicoes if t.destino == "[*]"}
    esperados = {s.name for s in Situacao if s.eh_final}
    if finais != esperados:
        resultado.erro(f"{figura.nome}: estados → [*] na figura {sorted(finais)}; com eh_final no código {sorted(esperados)}")
    else:
        evidencia.append((figura.nome, f"{', '.join(sorted(finais))} → [*]",
                          f"{arquivo}:{linhas['TRANSICOES_PERMITIDAS']} (eh_final: sem destinos)"))


def verificar_ocupa_o_horario(figura: DiagramaDeEstados, situacao, resultado: visao.Resultado,
                              evidencia: list[tuple[str, str, str]], arquivo: str, linhas: dict[str, int]) -> None:
    grupos = [membros for rotulo, membros in figura.compostos.values() if OCUPA in rotulo.lower()]
    destacados = {e for e, d in figura.descricoes.items() if OCUPA in d.lower()}
    if not grupos and not destacados:
        resultado.erro(f"{figura.nome}: falta o grupo '{OCUPA}' (estado composto ou descrição dos estados)")
        return
    na_figura = set(grupos[0]) if grupos else destacados
    esperado = {s.name for s in situacao.SITUACOES_QUE_OCUPAM_HORARIO}
    if na_figura != esperado:
        resultado.erro(f"{figura.nome}: '{OCUPA}' agrupa {sorted(na_figura)}; SITUACOES_QUE_OCUPAM_HORARIO é {sorted(esperado)}")
    else:
        evidencia.append((figura.nome, f"grupo '{OCUPA}': {', '.join(sorted(na_figura))}",
                          f"{arquivo}:{linhas['SITUACOES_QUE_OCUPAM_HORARIO']}"))


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=DESCRICAO)
    parser.add_argument("--pasta", type=Path, default=visao.PASTA_PADRAO, help="pasta com os .mmd")
    pasta = parser.parse_args().pasta.resolve()

    resultado = visao.Resultado()
    evidencia: list[tuple[str, str, str]] = []
    fontes = {f: tipo_do_diagrama(f) for f in sorted(pasta.glob("*.mmd"))}
    classes = [ler_diagrama_de_classes(f, resultado) for f, t in fontes.items() if t == "classes"]
    estados = [ler_diagrama_de_estados(f, resultado) for f, t in fontes.items() if t == "estados"]
    if not classes or not estados:
        print(f"É preciso ao menos um classDiagram e um stateDiagram em {pasta}")
        return 1

    for figura in classes:
        codigo = verificar_classes(figura, resultado, evidencia)
        verificar_relacoes(figura, codigo, resultado, evidencia)
        verificar_notas(figura, resultado, evidencia)
        verificar_glossario(figura, resultado)
    verificar_chaves_estrangeiras(resultado, evidencia)
    for figura in estados:
        verificar_estados(figura, resultado, evidencia)

    avisos_de_imagem = visao.Resultado()
    visao.verificar_imagens(pasta, avisos_de_imagem)
    minhas = {f.stem for f, t in fontes.items() if t}
    resultado.avisos += [a for a in avisos_de_imagem.avisos if a.split(".")[0] in minhas]

    print(f"Figuras: {', '.join(f.name for f, t in fontes.items() if t)}\n")
    print("| Figura | Elemento do diagrama | Onde está no código (src/backend/, arquivo:linha) |")
    print("|---|---|---|")
    for nome, elemento, onde in evidencia:
        celulas = [c.replace("|", r"\|").removeprefix("src/backend/") for c in (nome, elemento, onde)]
        print(f"| {' | '.join(celulas)} |")
    print()
    for aviso in resultado.avisos:
        print(f"AVISO: {aviso}")
    if resultado.erros:
        print(f"\n{len(resultado.erros)} pendência(s):")
        for erro in resultado.erros:
            print(f"- {erro}")
        return 1
    print(f"OK: {len(evidencia)} elementos conferidos contra o código.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
