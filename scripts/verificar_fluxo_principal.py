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
DESCRICAO = "DOC-03: confere os diagramas de sequência do fluxo principal (docs/fontes/modelagem/*.mmd) contra o código."
PACOTES = ("config", "compartilhado", "espacos", "reservas", "contas")
PASTAS_IGNORADAS = ("tests", "migrations", "__pycache__")
TRATADOR = "compartilhado.api.tratador_de_erros"
RESPOSTAS = "compartilhado.api.respostas"
URLS_RAIZ = BACKEND / "config" / "urls.py"
SECAO_DA_TABELA = "Passo → código → teste"

NAO_SEGUIR = {
    "obter_por_id": "lê uma reserva ou um espaço já gravado",
    "listar": "lê reservas já gravadas",
    "listar_que_ocupam_horario": "lê reservas já gravadas",
    "listar_historico": "lê registros já gravados",
    "_para_entidade": "reconstitui a entidade a partir do model",
    "_para_registro": "reconstitui o registro a partir do model",
    "__str__": "só texto",
    "__repr__": "só texto",
}
VALIDACAO = ("ValidationError", "DADOS_INVALIDOS", 400, "corpo_de_erro(DadosInvalidos.codigo")

ANOTACAO = re.compile(r"^%%\s*(participante|rota|campo):\s*(.*)$")
PARTICIPANTE = re.compile(r"^(participant|actor)\s+(\w+)(?:\s+as\s+(.*))?$")
MENSAGEM = re.compile(r"^(\w+)\s*(->>|-->>|--x|-x|->|-->|-\))\s*([+-]?)(\w+)\s*:\s*(.*)$")
NOTA = re.compile(r"^note\s+(?:over|left of|right of)\s+([\w,\s]+?)\s*:\s*(.*)$", re.IGNORECASE)
BLOCO = re.compile(r"^(alt|else|opt|loop|par|and|critical|break|rect)\b(.*)$")
IGNORAR = re.compile(r"^(sequenceDiagram|autonumber|end)\b")
CHAMADA = re.compile(r"^(?:(\w+)\.)?(\w+)\(")
HTTP = re.compile(r"^(GET|POST|PUT|PATCH|DELETE)\s+(/\S*)")
STATUS_CODIGO = re.compile(r"\b([1-5]\d\d)\s+([A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+)\b")
CITACAO = re.compile(r"“([^”]*)”")
ITEM_DA_NOTA = re.compile(r"→\s*([1-5]\d\d)\s+([A-Z][A-Z0-9_]+)")
TESTE_NA_TABELA = re.compile(r"`([\w./-]+\.py)::(\w+)(?:::(\w+))?`")


def texto(rotulo: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<br\s*/?>", " ", rotulo)).strip()


@dataclass
class Funcao:
    qualificado: str
    no: ast.FunctionDef
    modulo: "Modulo"
    classe: "Classe | None" = None

    @property
    def onde(self) -> str:
        return f"{self.modulo.arquivo}:{self.no.lineno}"

    @property
    def parametros(self) -> list[str]:
        a = self.no.args
        return [p.arg for p in (*a.posonlyargs, *a.args, *a.kwonlyargs) if p.arg not in ("self", "cls")]


@dataclass
class Classe:
    nome: str
    no: ast.ClassDef
    modulo: "Modulo"
    metodos: dict[str, Funcao] = field(default_factory=dict)

    @property
    def bases(self) -> list[str]:
        return [ast.unparse(b) for b in self.no.bases]

    @property
    def eh_protocol(self) -> bool:
        return "Protocol" in self.bases

    def atributo(self, nome: str) -> ast.expr | None:
        for item in self.no.body:
            if isinstance(item, ast.Assign) and any(isinstance(t, ast.Name) and t.id == nome for t in item.targets):
                return item.value
        return None


@dataclass
class Modulo:
    nome: str
    arquivo: str
    arvore: ast.Module
    funcoes: dict[str, Funcao] = field(default_factory=dict)
    classes: dict[str, Classe] = field(default_factory=dict)
    imports: dict[str, str] = field(default_factory=dict)

    @property
    def pacote(self) -> str:
        return self.nome.split(".")[0]


class Indice:
    def __init__(self) -> None:
        self.modulos: dict[str, Modulo] = {}
        for pacote in PACOTES:
            for arquivo in sorted((BACKEND / pacote).rglob("*.py")):
                if any(p in arquivo.parts for p in PASTAS_IGNORADAS):
                    continue
                self._ler(arquivo)

    def _ler(self, arquivo: Path) -> None:
        relativo = arquivo.relative_to(BACKEND)
        partes = list(relativo.with_suffix("").parts)
        if partes[-1] == "__init__":
            partes.pop()
        modulo = Modulo(".".join(partes), relativo.as_posix(), ast.parse(arquivo.read_text(encoding="utf-8")))
        for no in modulo.arvore.body:
            if isinstance(no, ast.FunctionDef):
                modulo.funcoes[no.name] = Funcao(f"{modulo.nome}.{no.name}", no, modulo)
            elif isinstance(no, ast.ClassDef):
                classe = Classe(no.name, no, modulo)
                for item in no.body:
                    if isinstance(item, ast.FunctionDef):
                        classe.metodos[item.name] = Funcao(f"{modulo.nome}.{no.name}.{item.name}", item, modulo, classe)
                modulo.classes[no.name] = classe
            elif isinstance(no, ast.ImportFrom) and no.module and no.level == 0:
                for apelido in no.names:
                    modulo.imports[apelido.asname or apelido.name] = f"{no.module}.{apelido.name}"
            elif isinstance(no, ast.Import):
                for apelido in no.names:
                    modulo.imports[apelido.asname or apelido.name] = apelido.name
        self.modulos[modulo.nome] = modulo

    def simbolo(self, qualificado: str) -> Modulo | Classe | Funcao | None:
        if qualificado in self.modulos:
            return self.modulos[qualificado]
        modulo, _, nome = qualificado.rpartition(".")
        if modulo in self.modulos:
            m = self.modulos[modulo]
            return m.classes.get(nome) or m.funcoes.get(nome)
        classe = self.simbolo(modulo) if modulo else None
        if isinstance(classe, Classe):
            return classe.metodos.get(nome)
        return None

    def nome_no_modulo(self, modulo: Modulo, nome: str) -> Modulo | Classe | Funcao | None:
        if nome in modulo.classes:
            return modulo.classes[nome]
        if nome in modulo.funcoes:
            return modulo.funcoes[nome]
        if nome in modulo.imports:
            return self.simbolo(modulo.imports[nome])
        return None

    def classe_base(self, classe: Classe, nome: str) -> Classe | None:
        alvo = self.nome_no_modulo(classe.modulo, nome)
        return alvo if isinstance(alvo, Classe) else None

    def hierarquia(self, classe: Classe) -> list[Classe]:
        ordem, pendentes = [], [classe]
        while pendentes:
            atual = pendentes.pop(0)
            if atual in ordem:
                continue
            ordem.append(atual)
            pendentes += [b for b in (self.classe_base(atual, n) for n in atual.bases) if b is not None]
        return ordem

    def codigo_da_excecao(self, classe: Classe) -> str | None:
        for c in self.hierarquia(classe):
            valor = c.atributo("codigo")
            if isinstance(valor, ast.Constant) and isinstance(valor.value, str):
                return valor.value
        return None

    def excecoes(self) -> list[Classe]:
        return [c for m in self.modulos.values() for c in m.classes.values() if self.codigo_da_excecao(c)]

    def candidatos_por_metodo(self, nome: str, pacote: str) -> list[Funcao]:
        todos = [c.metodos[nome] for m in self.modulos.values() if ".api." not in f"{m.nome}."
                 for c in m.classes.values() if nome in c.metodos and not c.eh_protocol]
        mesmo_pacote = [f for f in todos if f.modulo.pacote == pacote]
        return mesmo_pacote or todos


@dataclass
class Evento:
    tipo: str  # "chamada" ou "excecao"
    nome: str
    arquivo: str
    linha: int
    alvo: Funcao | None = None
    classe: Classe | None = None
    codigo: str | None = None
    campo: str | None = None


class Rastreador:
    def __init__(self, indice: Indice) -> None:
        self.indice = indice

    def rastrear(self, funcao: Funcao) -> list[Evento]:
        eventos: list[Evento] = []
        self._funcao(funcao, eventos, [])
        return eventos

    def _funcao(self, funcao: Funcao, eventos: list[Evento], pilha: list[str]) -> None:
        if funcao.qualificado in pilha:
            return
        pilha.append(funcao.qualificado)
        for comando in funcao.no.body:
            self._comando(comando, funcao, eventos, pilha)
        pilha.pop()

    def _comando(self, no: ast.stmt, funcao: Funcao, eventos: list[Evento], pilha: list[str]) -> None:
        if isinstance(no, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            return
        if isinstance(no, ast.Raise):
            if no.exc is not None:
                self._expressao(no.exc, funcao, eventos, pilha)
                self._excecao(no.exc, funcao, eventos)
            return
        for campo, valor in ast.iter_fields(no):
            for filho in valor if isinstance(valor, list) else [valor]:
                if isinstance(filho, ast.stmt):
                    self._comando(filho, funcao, eventos, pilha)
                elif isinstance(filho, ast.excepthandler):
                    for interno in filho.body:
                        self._comando(interno, funcao, eventos, pilha)
                elif isinstance(filho, (ast.expr, ast.withitem)):
                    self._expressao(filho, funcao, eventos, pilha)

    def _expressao(self, no: ast.AST, funcao: Funcao, eventos: list[Evento], pilha: list[str]) -> None:
        if isinstance(no, ast.Lambda):
            return
        if not isinstance(no, ast.Call):
            for filho in ast.iter_child_nodes(no):
                self._expressao(filho, funcao, eventos, pilha)
            return
        alvo_da_chamada = no.func.value if isinstance(no.func, ast.Attribute) else None
        if alvo_da_chamada is not None:
            self._expressao(alvo_da_chamada, funcao, eventos, pilha)
        for argumento in [*no.args, *(k.value for k in no.keywords)]:
            self._expressao(argumento, funcao, eventos, pilha)
        nome = no.func.attr if isinstance(no.func, ast.Attribute) else ast.unparse(no.func)
        destinos = self._resolver(no, funcao)
        eventos.append(Evento("chamada", nome, funcao.modulo.arquivo, no.lineno, destinos[0] if destinos else None))
        if nome == "is_valid" and any(k.arg == "raise_exception" for k in no.keywords):
            eventos.append(Evento("excecao", VALIDACAO[0], funcao.modulo.arquivo, no.lineno, codigo=VALIDACAO[1]))
        if nome in NAO_SEGUIR:
            return
        for destino in destinos:
            self._funcao(destino, eventos, pilha)

    def _excecao(self, no: ast.expr, funcao: Funcao, eventos: list[Evento]) -> None:
        nome = ast.unparse(no.func if isinstance(no, ast.Call) else no)
        classe = self.indice.nome_no_modulo(funcao.modulo, nome)
        if isinstance(classe, Classe):
            codigo = self.indice.codigo_da_excecao(classe)
            if codigo:
                eventos.append(Evento("excecao", nome, funcao.modulo.arquivo, no.lineno, classe=classe, codigo=codigo,
                                      campo=self._campo(no, classe)))

    def _campo(self, no: ast.expr, classe: Classe) -> str | None:
        if isinstance(no, ast.Call):
            for k in no.keywords:
                if k.arg == "campo":
                    return k.value.value if isinstance(k.value, ast.Constant) else None
            init = next((c.metodos["__init__"] for c in self.indice.hierarquia(classe) if "__init__" in c.metodos), None)
            if init is not None and init.parametros[:1] == ["campo"]:
                primeiro = no.args[0] if no.args else None
                return primeiro.value if isinstance(primeiro, ast.Constant) else None
        for c in self.indice.hierarquia(classe):
            valor = c.atributo("campo")
            if isinstance(valor, ast.Constant):
                return valor.value
        return None

    def _inicializacao(self, classe: Classe) -> list[Funcao]:
        return [classe.metodos[m] for m in ("__init__", "__post_init__") if m in classe.metodos]

    def _resolver(self, no: ast.Call, funcao: Funcao) -> list[Funcao]:
        indice, modulo = self.indice, funcao.modulo
        if isinstance(no.func, ast.Name):
            if no.func.id == "cls" and funcao.classe is not None:
                return self._inicializacao(funcao.classe)
            alvo = indice.nome_no_modulo(modulo, no.func.id)
            if isinstance(alvo, Classe):
                return self._inicializacao(alvo)
            return [alvo] if isinstance(alvo, Funcao) else []
        if not isinstance(no.func, ast.Attribute):
            return []
        metodo, dono = no.func.attr, no.func.value
        if isinstance(dono, ast.Name) and dono.id == "self" and funcao.classe is not None:
            return [funcao.classe.metodos[metodo]] if metodo in funcao.classe.metodos else []
        if isinstance(dono, ast.Name):
            alvo = indice.nome_no_modulo(modulo, dono.id)
            if isinstance(alvo, Classe):
                return [alvo.metodos[metodo]] if metodo in alvo.metodos else []
            if isinstance(alvo, Modulo):
                return [alvo.funcoes[metodo]] if metodo in alvo.funcoes else []
        if isinstance(dono, ast.Call):
            classe = self._classe_produzida(dono, funcao)
            if classe is not None:
                return [classe.metodos[metodo]] if metodo in classe.metodos else []
        candidatos = indice.candidatos_por_metodo(metodo, modulo.pacote)
        return candidatos if len(candidatos) == 1 else []

    def _classe_produzida(self, chamada: ast.Call, funcao: Funcao) -> Classe | None:
        destinos = self._resolver(chamada, funcao)
        if isinstance(chamada.func, ast.Name):
            alvo = self.indice.nome_no_modulo(funcao.modulo, chamada.func.id)
            if isinstance(alvo, Classe):
                return alvo
        for destino in destinos:
            if destino.no.returns is not None:
                retorno = self.indice.nome_no_modulo(destino.modulo, ast.unparse(destino.no.returns))
                if isinstance(retorno, Classe):
                    return retorno
        return None


@dataclass
class Mensagem:
    numero: int
    origem: str
    seta: str
    destino: str
    rotulo: str
    linha: int

    @property
    def eh_chamada(self) -> bool:
        return self.seta in ("->>", "->", "-x", "-)")

    @property
    def eh_excecao(self) -> bool:
        return self.seta in ("--x", "-x")


@dataclass
class Nota:
    rotulo: str
    linha: int


@dataclass
class Diagrama:
    nome: str
    participantes: dict[str, tuple[str, int]] = field(default_factory=dict)
    simbolos: dict[str, list[str]] = field(default_factory=dict)
    rotas: list[tuple[str, str, int]] = field(default_factory=list)
    campos: dict[str, str] = field(default_factory=dict)
    mensagens: list[Mensagem] = field(default_factory=list)
    notas: list[Nota] = field(default_factory=list)


def eh_sequencia(caminho: Path) -> bool:
    for bruta in caminho.read_text(encoding="utf-8").splitlines():
        linha = bruta.strip()
        if linha and not linha.startswith("%%"):
            return linha.startswith("sequenceDiagram")
    return False


def ler_diagrama(caminho: Path, resultado: visao.Resultado) -> Diagrama:
    figura = Diagrama(caminho.name)
    for numero, bruta in enumerate(caminho.read_text(encoding="utf-8").splitlines(), start=1):
        linha = bruta.strip()
        onde = f"{figura.nome}:{numero}"
        if not linha or linha.startswith("%%{"):
            continue
        if anotacao := ANOTACAO.match(linha):
            chave, valor = anotacao.group(1), anotacao.group(2).strip()
            if chave == "participante":
                nome, igual, alvos = valor.partition("=")
                if not igual:
                    resultado.erro(f"{onde}: anotação 'participante' sem '='")
                    continue
                figura.simbolos[nome.strip()] = [a.strip() for a in alvos.split(",") if a.strip()]
            elif chave == "campo":
                codigo, _, campo = valor.partition("=")
                figura.campos[codigo.strip()] = campo.strip()
            else:
                metodo, _, rota = valor.partition(" ")
                figura.rotas.append((metodo.strip().upper(), rota.strip(), numero))
            continue
        if linha.startswith("%%") or IGNORAR.match(linha) or BLOCO.match(linha):
            continue
        if p := PARTICIPANTE.match(linha):
            figura.participantes[p.group(2)] = (texto(p.group(3) or p.group(2)), numero)
        elif m := MENSAGEM.match(linha):
            figura.mensagens.append(Mensagem(len(figura.mensagens) + 1, m.group(1), m.group(2), m.group(4),
                                             texto(m.group(5)), numero))
        elif n := NOTA.match(linha):
            figura.notas.append(Nota(texto(n.group(2)), numero))
        else:
            resultado.erro(f"{onde}: linha não reconhecida: {linha}")
    return figura


@dataclass
class Contexto:
    indice: Indice
    rastreador: Rastreador
    status_por_categoria: dict[str, tuple[int, int]]
    templates: dict[str, list[tuple[re.Pattern, str]]]
    status_padrao_de_sucesso: int


def status_por_categoria(indice: Indice) -> dict[str, tuple[int, int]]:
    tratador = indice.modulos[TRATADOR]
    for no in tratador.arvore.body:
        if isinstance(no, ast.Assign) and ast.unparse(no.targets[0]) == "_STATUS_POR_CATEGORIA":
            return {ast.unparse(k): (int(re.search(r"HTTP_(\d{3})", ast.unparse(v)).group(1)), k.lineno)
                    for k, v in zip(no.value.keys, no.value.values)}
    raise SystemExit("_STATUS_POR_CATEGORIA não encontrado no tratador de erros")


def status_da_excecao(ctx: Contexto, classe: Classe) -> tuple[int, str, int] | None:
    for c in ctx.indice.hierarquia(classe):
        if c.nome in ctx.status_por_categoria:
            status, linha = ctx.status_por_categoria[c.nome]
            return status, c.nome, linha
    return None


def para_regex(no: ast.expr) -> str | None:
    if isinstance(no, ast.Constant) and isinstance(no.value, str):
        return re.escape(no.value)
    if isinstance(no, ast.JoinedStr):
        return "".join(re.escape(p.value) if isinstance(p, ast.Constant) else ".+?" for p in no.values)
    return None


def templates_das_excecoes(indice: Indice) -> dict[str, list[tuple[re.Pattern, str]]]:
    templates: dict[str, list[tuple[re.Pattern, str]]] = {}
    for classe in indice.excecoes():
        codigo = indice.codigo_da_excecao(classe)
        lista = templates.setdefault(codigo, [])
        for c in indice.hierarquia(classe):
            valor = c.atributo("mensagem_padrao")
            if valor is not None and (regex := para_regex(valor)):
                lista.append((re.compile(regex), f"{c.modulo.arquivo}:{valor.lineno}"))
                break
        if "__init__" in classe.metodos:
            for no in ast.walk(classe.metodos["__init__"].no):
                if isinstance(no, ast.Call) and ast.unparse(no.func) == "super().__init__" and no.args:
                    if regex := para_regex(no.args[0]):
                        lista.append((re.compile(regex), f"{classe.modulo.arquivo}:{no.lineno}"))
    return templates


def status_padrao(indice: Indice) -> int:
    funcao = indice.modulos[RESPOSTAS].funcoes["resposta_sucesso"].no
    nomes = [a.arg for a in funcao.args.args]
    padrao = funcao.args.defaults[nomes.index("status") - (len(nomes) - len(funcao.args.defaults))]
    return int(ast.literal_eval(padrao))


def verificar_participantes(figura: Diagrama, ctx: Contexto, resultado: visao.Resultado) -> None:
    for nome, (_, linha) in figura.participantes.items():
        if nome not in figura.simbolos:
            resultado.erro(f"{figura.nome}:{linha}: o participante {nome} não tem '%% participante: {nome} = símbolo'")
    for nome, alvos in figura.simbolos.items():
        if nome not in figura.participantes:
            resultado.erro(f"{figura.nome}: '%% participante: {nome}' cita um participante que não está na figura")
        for alvo in alvos:
            if "/" in alvo:
                if not (RAIZ / alvo).is_file():
                    resultado.erro(f"{figura.nome}: o participante {nome} aponta para '{alvo}', que não existe")
            elif ctx.indice.simbolo(alvo) is None:
                resultado.erro(f"{figura.nome}: o participante {nome} aponta para '{alvo}', que não existe em src/backend")
        rotulo = figura.participantes.get(nome, ("", 0))[0]
        for alvo in alvos:
            simbolo = ctx.indice.simbolo(alvo) if "/" not in alvo else None
            if isinstance(simbolo, Classe) and simbolo.nome not in rotulo and alvo == alvos[0]:
                resultado.erro(f"{figura.nome}: o rótulo de {nome} ('{rotulo}') não traz o nome real {simbolo.nome}")


def metodos_do_participante(figura: Diagrama, ctx: Contexto, participante: str) -> dict[str, Funcao]:
    metodos: dict[str, Funcao] = {}
    for alvo in figura.simbolos.get(participante, []):
        simbolo = ctx.indice.simbolo(alvo) if "/" not in alvo else None
        if isinstance(simbolo, Classe):
            metodos.update({n: f for n, f in simbolo.metodos.items() if not n.startswith("__")})
        elif isinstance(simbolo, Funcao):
            metodos[simbolo.no.name] = simbolo
        elif isinstance(simbolo, Modulo):
            metodos.update(simbolo.funcoes)
    return metodos


def classes_do_participante(figura: Diagrama, ctx: Contexto, participante: str) -> list[Classe]:
    return [s for a in figura.simbolos.get(participante, []) if "/" not in a
            and isinstance(s := ctx.indice.simbolo(a), Classe)]


def verificar_metodos(figura: Diagrama, ctx: Contexto, resultado: visao.Resultado) -> dict[int, Funcao]:
    chamados: dict[int, Funcao] = {}
    for m in figura.mensagens:
        if not m.eh_chamada or HTTP.match(m.rotulo):
            continue
        onde = f"{figura.nome}:{m.linha} (passo {m.numero})"
        casado = CHAMADA.match(m.rotulo)
        if not casado:
            resultado.erro(f"{onde}: a chamada '{m.rotulo}' não começa pelo nome de um método")
            continue
        prefixo, nome = casado.groups()
        metodos = metodos_do_participante(figura, ctx, m.destino)
        funcao = metodos.get(nome)
        if funcao is None:
            resultado.erro(f"{onde}: '{nome}' não é método nem função de {m.destino} "
                           f"({', '.join(figura.simbolos.get(m.destino, []))})")
            continue
        if prefixo and (funcao.classe is None or funcao.classe.nome != prefixo):
            resultado.erro(f"{onde}: '{prefixo}.{nome}': {nome} não é da classe {prefixo}")
        argumentos = m.rotulo[casado.end():]
        for chave in re.findall(r"\b(\w+)=(?!=)", argumentos):
            if chave not in funcao.parametros:
                resultado.erro(f"{onde}: {nome} não tem o parâmetro '{chave}' (tem: {', '.join(funcao.parametros)})")
        chamados[m.numero] = funcao
    return chamados


@dataclass
class Rota:
    metodo: str
    nome: str
    caminho: str
    classe: Classe
    linha: int


def ler_rota(ctx: Contexto, metodo: str, nome: str) -> Rota | str:
    app, _, nome_da_rota = nome.partition(":")
    prefixos = {}
    for no in ast.walk(ast.parse(URLS_RAIZ.read_text(encoding="utf-8"))):
        if isinstance(no, ast.Call) and ast.unparse(no.func) == "path" and len(no.args) == 2:
            inclusao = no.args[1]
            if isinstance(inclusao, ast.Call) and ast.unparse(inclusao.func) == "include":
                prefixos[inclusao.args[0].value] = no.args[0].value
    modulo_urls = f"{app}.api.urls"
    urls = ctx.indice.modulos.get(modulo_urls)
    if urls is None or modulo_urls not in prefixos:
        return f"o app '{app}' não tem {modulo_urls} incluído em config/urls.py"
    for no in ast.walk(urls.arvore):
        if not (isinstance(no, ast.Call) and ast.unparse(no.func) == "path"):
            continue
        if any(k.arg == "name" and k.value.value == nome_da_rota for k in no.keywords):
            view = no.args[1]
            classe_nome = ast.unparse(view.func.value) if isinstance(view, ast.Call) else ast.unparse(view)
            classe = ctx.indice.nome_no_modulo(urls, classe_nome)
            if not isinstance(classe, Classe):
                return f"a view {classe_nome} da rota {nome} não foi encontrada"
            if metodo.lower() not in classe.metodos:
                return f"a view {classe.nome} da rota {nome} não implementa {metodo}"
            caminho = "/" + prefixos[modulo_urls] + no.args[0].value
            return Rota(metodo, nome, re.sub(r"<[^>]+>", "{id}", caminho), classe, no.lineno)
    return f"a rota {nome} não existe em {urls.arquivo}"


def verificar_rotas(figura: Diagrama, ctx: Contexto, resultado: visao.Resultado) -> list[Rota]:
    rotas = []
    pedidos = [m for m in figura.mensagens if m.eh_chamada and HTTP.match(m.rotulo)]
    if not figura.rotas:
        resultado.erro(f"{figura.nome}: falta '%% rota: MÉTODO app:nome'")
    for metodo, nome, linha in figura.rotas:
        rota = ler_rota(ctx, metodo, nome)
        if isinstance(rota, str):
            resultado.erro(f"{figura.nome}:{linha}: {rota}")
            continue
        rotas.append(rota)
        pedido = next((m for m in pedidos if HTTP.match(m.rotulo).groups() == (metodo, rota.caminho)), None)
        if pedido is None:
            resultado.erro(f"{figura.nome}: nenhuma mensagem '{metodo} {rota.caminho}' (rota {nome})")
            continue
        if rota.classe not in classes_do_participante(figura, ctx, pedido.destino):
            resultado.erro(f"{figura.nome}:{pedido.linha}: {metodo} {rota.caminho} vai para {pedido.destino}, "
                           f"mas a rota {nome} é atendida por {rota.classe.nome}")
    for m in pedidos:
        metodo, caminho = HTTP.match(m.rotulo).groups()
        if not any((r.metodo, r.caminho) == (metodo, caminho) for r in rotas):
            resultado.erro(f"{figura.nome}:{m.linha}: '{metodo} {caminho}' sem '%% rota:' correspondente")
    return rotas


def subsequencia(procurados: list, eventos: list[Evento], casa) -> tuple[list[Evento | None], int | None]:
    posicao, achados = 0, []
    for indice, item in enumerate(procurados):
        achado = next((i for i in range(posicao, len(eventos)) if casa(item, eventos[i])), None)
        if achado is None:
            return achados, indice
        achados.append(eventos[achado])
        posicao = achado + 1
    return achados, None


def verificar_ordem_das_chamadas(figura: Diagrama, eventos: list[Evento], chamados: dict[int, Funcao],
                                 resultado: visao.Resultado) -> dict[int, Evento]:
    mensagens = [m for m in figura.mensagens if m.numero in chamados]
    achados, falha = subsequencia(mensagens, eventos,
                                  lambda m, e: e.tipo == "chamada" and e.alvo is chamados[m.numero])
    if falha is not None:
        m = mensagens[falha]
        anterior = f" depois de '{mensagens[falha - 1].rotulo}' (passo {mensagens[falha - 1].numero})" if falha else ""
        real = [e.nome for e in eventos if e.tipo == "chamada" and any(e.alvo is f for f in chamados.values())]
        resultado.erro(f"{figura.nome}:{m.linha}: a chamada '{CHAMADA.match(m.rotulo).group(0)}…' (passo {m.numero}) "
                       f"não acontece{anterior} no código; ordem real: {' → '.join(real)}")
    return {m.numero: e for m, e in zip(mensagens, achados)}


def verificar_codigos(figura: Diagrama, ctx: Contexto, resultado: visao.Resultado) -> None:
    textos = [(m.linha, m.rotulo) for m in figura.mensagens] + [(n.linha, n.rotulo) for n in figura.notas]
    for linha, rotulo in textos:
        for status, codigo in STATUS_CODIGO.findall(rotulo):
            esperado = status_do_codigo(ctx, codigo)
            if not esperado:
                resultado.erro(f"{figura.nome}:{linha}: o código {codigo} não existe em nenhuma exceção")
            elif int(status) not in esperado:
                resultado.erro(f"{figura.nome}:{linha}: {codigo} aparece com {status}, mas o tratador de erros dá "
                               f"{' ou '.join(map(str, sorted(esperado)))}")


def status_do_codigo(ctx: Contexto, codigo: str) -> set[int]:
    if codigo == VALIDACAO[1]:
        return {VALIDACAO[2]}
    return {s[0] for c in ctx.indice.excecoes() if ctx.indice.codigo_da_excecao(c) == codigo
            and (s := status_da_excecao(ctx, c))}


def verificar_ordem_das_verificacoes(figura: Diagrama, eventos: list[Evento],
                                     resultado: visao.Resultado) -> None:
    notas = [n for n in figura.notas if n.rotulo.startswith("Verificações")]
    if len(notas) != 1:
        resultado.erro(f"{figura.nome}: precisa de exatamente uma nota que comece por 'Verificações' (tem {len(notas)})")
        return
    codigos = [codigo for _, codigo in ITEM_DA_NOTA.findall(notas[0].rotulo)]
    excecoes = [e for e in eventos if e.tipo == "excecao"]
    blocos: list[tuple[str, set[str]]] = []
    for e in excecoes:
        if blocos and blocos[-1][0] == e.codigo:
            blocos[-1][1].add(e.campo or "")
        else:
            blocos.append((e.codigo, {e.campo or ""}))
    for codigo in dict.fromkeys(codigos):
        campos = sorted({e.campo for e in excecoes if e.codigo == codigo and e.campo})
        distintos = {frozenset(c) for cod, c in blocos if cod == codigo}
        if len(distintos) > 1 and campos and codigo not in figura.campos:
            resultado.erro(f"{figura.nome}:{notas[0].linha}: {codigo} é lançado em pontos diferentes, para campos "
                           f"diferentes ({', '.join(campos)}): diga qual com '%% campo: {codigo} = <campo>'")
        elif codigo in figura.campos and figura.campos[codigo] not in campos:
            resultado.erro(f"{figura.nome}: '%% campo: {codigo} = {figura.campos[codigo]}', mas o código só lança "
                           f"{codigo} para {', '.join(campos) or 'nenhum campo'}")
    itens = [(c, figura.campos.get(c)) for c in codigos]
    _, falha = subsequencia(itens, excecoes, lambda item, e: e.codigo == item[0] and item[1] in (None, e.campo))
    if falha is None:
        return
    codigo = itens[falha][0]
    anterior = itens[falha - 1][0] if falha else None
    lancadas = [e for e in excecoes if e.codigo == codigo and itens[falha][1] in (None, e.campo)]
    if not lancadas:
        resultado.erro(f"{figura.nome}:{notas[0].linha}: a nota cita {codigo}, que esta requisição nunca lança")
        return
    primeira = lancadas[0]
    resultado.erro(f"{figura.nome}:{notas[0].linha}: a nota põe {codigo} depois de {anterior}, mas o código lança "
                   f"{codigo} antes ({primeira.arquivo}:{primeira.linha}); ordem real: "
                   f"{' → '.join(dict.fromkeys(e.codigo for e in excecoes))}")


def verificar_mensagens(figura: Diagrama, ctx: Contexto, rotas: list[Rota], resultado: visao.Resultado) -> dict[int, str]:
    provas: dict[int, str] = {}
    for m in figura.mensagens:
        onde = f"{figura.nome}:{m.linha} (passo {m.numero})"
        for citado in CITACAO.findall(m.rotulo):
            codigos = STATUS_CODIGO.findall(m.rotulo)
            if codigos:
                codigo = codigos[0][1]
                prova = next((o for r, o in ctx.templates.get(codigo, []) if r.fullmatch(citado)), None)
                if prova is None:
                    resultado.erro(f"{onde}: a mensagem “{citado}” não é a de {codigo} no código")
                else:
                    provas[m.numero] = prova
                continue
            prova = verificar_sucesso(figura, ctx, rotas, m, citado, onde, resultado)
            if prova:
                provas[m.numero] = prova
        if m.eh_excecao:
            verificar_excecao_citada(figura, ctx, m, onde, resultado)
    return provas


def verificar_sucesso(figura: Diagrama, ctx: Contexto, rotas: list[Rota], m: Mensagem, citado: str, onde: str,
                      resultado: visao.Resultado) -> str | None:
    status = re.match(r"^(\d{3})\b", m.rotulo)
    for rota in rotas:
        funcao = rota.classe.metodos[rota.metodo.lower()]
        for no in ast.walk(funcao.no):
            if isinstance(no, ast.Call) and ast.unparse(no.func) == "resposta_sucesso" and no.args:
                regex = para_regex(no.args[0])
                if regex and re.fullmatch(regex, citado):
                    real = next((int(re.search(r"\d{3}", ast.unparse(k.value)).group(0))
                                 for k in no.keywords if k.arg == "status"), ctx.status_padrao_de_sucesso)
                    if status is None or int(status.group(1)) != real:
                        resultado.erro(f"{onde}: “{citado}” sai com {real} em {funcao.onde}, não "
                                       f"{status.group(1) if status else 'sem status'}")
                    return f"{rota.classe.modulo.arquivo}:{no.lineno}"
    resultado.erro(f"{onde}: a mensagem de sucesso “{citado}” não está em resposta_sucesso de {figura.nome}")
    return None


def verificar_excecao_citada(figura: Diagrama, ctx: Contexto, m: Mensagem, onde: str, resultado: visao.Resultado) -> None:
    nome = re.match(r"^(\w+)", m.rotulo).group(1)
    classe = next((c for c in ctx.indice.excecoes() if c.nome == nome), None)
    if classe is None:
        resultado.erro(f"{onde}: '{nome}' não é uma exceção de domínio")
        return
    seguinte = next((x for x in figura.mensagens if x.numero == m.numero + 1), None)
    codigo = ctx.indice.codigo_da_excecao(classe)
    if seguinte is None or codigo not in seguinte.rotulo:
        resultado.erro(f"{onde}: {nome} tem o código {codigo}, que não aparece na resposta seguinte")


def verificar_tabela(pasta: Path, resultado: visao.Resultado) -> int:
    readme = pasta / "README.md"
    if not readme.is_file():
        resultado.erro(f"{readme.name} não existe")
        return 0
    linhas = readme.read_text(encoding="utf-8").splitlines()
    inicio = next((i for i, linha in enumerate(linhas) if linha.startswith("#") and SECAO_DA_TABELA in linha), None)
    if inicio is None:
        resultado.erro(f"README.md: falta a seção '{SECAO_DA_TABELA}'")
        return 0
    conferidos = 0
    for linha in linhas[inicio + 1:]:
        if linha.startswith("#"):
            break
        for arquivo, nome, metodo in TESTE_NA_TABELA.findall(linha):
            caminho = BACKEND / arquivo
            if "/tests/" not in f"/{arquivo}":
                continue
            conferidos += 1
            if not caminho.is_file():
                resultado.erro(f"README.md: o teste '{arquivo}' não existe em src/backend")
                continue
            arvore = ast.parse(caminho.read_text(encoding="utf-8"))
            definido = next((n for n in arvore.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == nome), None)
            if definido is None or (metodo and not any(isinstance(x, ast.FunctionDef) and x.name == metodo
                                                       for x in getattr(definido, "body", []))):
                resultado.erro(f"README.md: o teste '{arquivo}::{nome}{'::' + metodo if metodo else ''}' não existe")
    if not conferidos:
        resultado.erro(f"README.md: a seção '{SECAO_DA_TABELA}' não cita nenhum teste")
    return conferidos


def codigo_do_passo(figura: Diagrama, ctx: Contexto, m: Mensagem, rotas: list[Rota], chamadas: dict[int, Evento],
                    provas: dict[int, str], eventos: list[Evento]) -> str:
    if http := HTTP.match(m.rotulo):
        rota = next((r for r in rotas if (r.metodo, r.caminho) == http.groups()), None)
        if rota:
            urls = ctx.indice.modulos[f"{rota.nome.partition(':')[0]}.api.urls"].arquivo
            return f"{urls}:{rota.linha} → {rota.classe.nome}.{rota.metodo.lower()} {rota.classe.metodos[rota.metodo.lower()].onde}"
    if m.numero in chamadas:
        evento = chamadas[m.numero]
        return f"chamada {evento.arquivo}:{evento.linha} → def {evento.alvo.onde}"
    if m.eh_excecao:
        nome = re.match(r"^(\w+)", m.rotulo).group(1)
        lancada = next((e for e in eventos if e.tipo == "excecao" and e.nome == nome), None)
        return f"raise {lancada.arquivo}:{lancada.linha}" if lancada else "—"
    codigos = STATUS_CODIGO.findall(m.rotulo)
    if codigos:
        classe = next(c for c in ctx.indice.excecoes() if ctx.indice.codigo_da_excecao(c) == codigos[0][1])
        status, categoria, linha = status_da_excecao(ctx, classe)
        tratador = ctx.indice.modulos[TRATADOR].arquivo
        return f"{tratador}:{linha} ({categoria} → {status}); mensagem {provas.get(m.numero, '—')}"
    if m.numero in provas:
        return f"resposta_sucesso {provas[m.numero]}"
    anterior = max((n for n in chamadas if n < m.numero and figura.mensagens[n - 1].destino == m.origem), default=None)
    if anterior is not None:
        alvo = chamadas[anterior].alvo
        retornos = [r for r in ast.walk(alvo.no) if isinstance(r, ast.Return)]
        linha = retornos[-1].lineno if retornos else alvo.no.lineno
        return f"retorno de {alvo.no.name}: {alvo.modulo.arquivo}:{linha}"
    return "—"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=DESCRICAO)
    parser.add_argument("--pasta", type=Path, default=visao.PASTA_PADRAO, help="pasta com os .mmd e o README.md")
    pasta = parser.parse_args().pasta.resolve()

    resultado = visao.Resultado()
    fontes = [f for f in sorted(pasta.glob("*.mmd")) if eh_sequencia(f)]
    if not fontes:
        print(f"Nenhum sequenceDiagram em {pasta}")
        return 1
    indice = Indice()
    ctx = Contexto(indice, Rastreador(indice), status_por_categoria(indice), templates_das_excecoes(indice),
                   status_padrao(indice))
    tratador = (BACKEND / indice.modulos[TRATADOR].arquivo).read_text(encoding="utf-8")
    if VALIDACAO[3] not in tratador:
        resultado.erro(f"o tratador de erros não traduz mais ValidationError com '{VALIDACAO[3]}'")

    tabela: list[tuple[str, int, str, str]] = []
    for caminho in fontes:
        figura = ler_diagrama(caminho, resultado)
        verificar_participantes(figura, ctx, resultado)
        chamados = verificar_metodos(figura, ctx, resultado)
        rotas = verificar_rotas(figura, ctx, resultado)
        eventos: list[Evento] = []
        for rota in rotas:
            eventos += ctx.rastreador.rastrear(rota.classe.metodos[rota.metodo.lower()])
        chamadas = verificar_ordem_das_chamadas(figura, eventos, chamados, resultado)
        verificar_codigos(figura, ctx, resultado)
        verificar_ordem_das_verificacoes(figura, eventos, resultado)
        provas = verificar_mensagens(figura, ctx, rotas, resultado)
        for m in figura.mensagens:
            resumo = m.rotulo if len(m.rotulo) <= 70 else m.rotulo[:67] + "…"
            tabela.append((figura.nome, m.numero, resumo, codigo_do_passo(figura, ctx, m, rotas, chamadas, provas, eventos)))
    testes = verificar_tabela(pasta, resultado)

    avisos = visao.Resultado()
    visao.verificar_imagens(pasta, avisos)
    minhas = {f.stem for f in fontes}
    resultado.avisos += [a for a in avisos.avisos if a.split(".")[0] in minhas]

    print(f"Figuras: {', '.join(f.name for f in fontes)}\n")
    print("| Figura | Passo | Mensagem | Código (src/backend/, arquivo:linha) |")
    print("|---|---|---|---|")
    for nome, numero, resumo, onde in tabela:
        print(f"| {nome} | {numero} | {resumo.replace('|', chr(92) + '|')} | {onde} |")
    print("\nNão seguido no rastreio, de propósito:")
    for nome, motivo in NAO_SEGUIR.items():
        print(f"- {nome}: {motivo}")
    print()
    for aviso in resultado.avisos:
        print(f"AVISO: {aviso}")
    if resultado.erros:
        print(f"\n{len(resultado.erros)} pendência(s):")
        for erro in resultado.erros:
            print(f"- {erro}")
        return 1
    print(f"OK: {len(tabela)} passos e {testes} testes citados conferidos contra o código.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
