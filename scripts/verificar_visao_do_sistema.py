from __future__ import annotations

import argparse
import ast
import os
import re
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BACKEND = RAIZ / "src" / "backend"
FRONTEND_SRC = RAIZ / "src" / "frontend" / "src"
COMPOSE = RAIZ / "src" / "docker-compose.yml"
PYPROJECT = BACKEND / "pyproject.toml"
PASTA_PADRAO = RAIZ / "docs" / "fontes" / "modelagem"
TEXTOS = ("01-visao-do-sistema.md", "README.md")
RAIZES_PYTHON = ("config", "compartilhado", "espacos", "reservas", "contas", "exemplos")
PASTAS_IGNORADAS = ("tests", "migrations", "__pycache__")

IGNORADOS = {
    "espacos.models": "reexporta espacos/infrastructure/models.py para o Django descobrir os models",
    "reservas.models": "reexporta reservas/infrastructure/models.py para o Django descobrir os models",
    "contas.models": "reexporta contas/infrastructure/models.py para o Django descobrir os models",
    "contas.admin": "administração do Django (/admin/), fora da API e da arquitetura em camadas",
}
FRONTEND_IGNORADOS = {
    "src/frontend/src/configuracaoDosTestes.ts": "configuração do Vitest (setupFiles)",
}
EXCECOES: list[tuple[str, str, str]] = []

SETA = re.compile(r'^(\w+)\s*(-->|-\.->|==>|~~~)\s*(?:\|"([^"]*)"\|\s*)?(\w+)$')
NO = re.compile(r'^(\w+)\s*[\[\(\{]+"(.*)"[\]\)\}]+(?::::\w+)?$')
SUBGRAFO = re.compile(r'^subgraph\s+(\w+)(?:\s*\["(.*)"\])?$')
ANOTACAO = re.compile(r"^%%\s*(modulo|caminho|servico|imagem|sem-import|somente|contrato|contextos):\s*(.*)$")
IGNORAR_LINHA = re.compile(r"^(flowchart\b|graph\b|classDef\b|class\b|style\b|linkStyle\b|direction\b|%%)")
CONTRATO_NO_TEXTO = re.compile(r"contrato `([^`]+)`")
TESTE_NO_TEXTO = re.compile(r"`((?:[\w.-]+/)+test_\w+\.py)(?:::\w+)?`")
REF_CONTRATO = re.compile(r"\bC(\d+)\b")
TIPOS = {"-->": "depende", "-.->": "implementa", "==>": "rede", "~~~": "layout"}

IMPORT_TS = re.compile(
    r"^(import|export)\s+(type\s+)?(?:\{[^}]*\}|\*\s+as\s+\w+|\w+(?:\s*,\s*\{[^}]*\})?)\s+from\s+['\"]([^'\"]+)['\"]",
    re.MULTILINE,
)
IMPORT_TS_EFEITO = re.compile(r"^import\s+['\"]([^'\"]+)['\"]", re.MULTILINE)


@dataclass
class Seta:
    figura: str
    origem: str
    destino: str
    tipo: str
    rotulo: str
    linha: int


@dataclass
class Figura:
    nome: str
    texto: str
    rotulos: dict[str, str] = field(default_factory=dict)
    ancestrais: dict[str, list[str]] = field(default_factory=dict)
    subgrafos: dict[str, str] = field(default_factory=dict)
    setas: list[Seta] = field(default_factory=list)
    modulos: dict[str, str] = field(default_factory=dict)
    caminhos: dict[str, tuple[list[str], list[str]]] = field(default_factory=dict)
    servicos: dict[str, str] = field(default_factory=dict)
    imagens: dict[str, str] = field(default_factory=dict)
    sem_import: dict[tuple[str, str], list[tuple[str, str]]] = field(default_factory=dict)
    somente: dict[tuple[str, str], str] = field(default_factory=dict)
    contratos: dict[str, str] = field(default_factory=dict)
    contextos: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Import:
    origem: str
    destino: str
    arquivo: str
    linha: int


@dataclass(frozen=True)
class Heranca:
    origem: str
    destino: str
    classe: str
    base: str
    arquivo: str
    linha: int


@dataclass
class Resultado:
    erros: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)

    def erro(self, texto: str) -> None:
        self.erros.append(texto)


def relativo(caminho: Path) -> str:
    return caminho.resolve().relative_to(RAIZ).as_posix()


def nao_representa_codigo(no: str) -> bool:
    return no.startswith(("LEG_", "NOTA_"))


def primeira_linha(rotulo: str) -> str:
    return re.split(r"<br\s*/?>", rotulo)[0].strip()


def ler_figura(caminho: Path, resultado: Resultado) -> Figura:
    figura = Figura(nome=caminho.name, texto=caminho.read_text(encoding="utf-8"))
    pilha: list[str] = []
    for numero, bruta in enumerate(figura.texto.splitlines(), start=1):
        linha = bruta.strip()
        onde = f"{figura.nome}:{numero}"
        if not linha or linha.startswith("%%{"):
            continue
        if anotacao := ANOTACAO.match(linha):
            ler_anotacao(figura, anotacao.group(1), anotacao.group(2).strip(), onde, resultado)
            continue
        if linha == "end":
            if not pilha:
                resultado.erro(f"{onde}: 'end' sem subgraph aberto")
            else:
                pilha.pop()
            continue
        if sub := SUBGRAFO.match(linha):
            figura.subgrafos[sub.group(1)] = sub.group(2) or sub.group(1)
            figura.ancestrais[sub.group(1)] = list(pilha)
            pilha.append(sub.group(1))
            continue
        if seta := SETA.match(linha):
            origem, simbolo, rotulo, destino = seta.groups()
            figura.setas.append(Seta(figura.nome, origem, destino, TIPOS[simbolo], rotulo or "", numero))
            continue
        if no := NO.match(linha):
            figura.rotulos[no.group(1)] = no.group(2)
            figura.ancestrais[no.group(1)] = list(pilha)
            continue
        if IGNORAR_LINHA.match(linha):
            continue
        resultado.erro(f"{onde}: linha não reconhecida (use uma seta ou um nó por linha, rótulo entre aspas): {linha}")
    if pilha:
        resultado.erro(f"{figura.nome}: subgraph sem 'end': {', '.join(pilha)}")
    return figura


def ler_anotacao(figura: Figura, chave: str, valor: str, onde: str, resultado: Resultado) -> None:
    if chave == "contextos":
        figura.contextos = [c.strip() for c in valor.split(",") if c.strip()]
        return
    if chave in ("sem-import", "somente"):
        partes = [p.strip() for p in valor.split("|")]
        par = re.fullmatch(r"(\w+)\s*->\s*(\w+)", partes[0])
        esperado = 3 if chave == "sem-import" else 2
        if not par or len(partes) != esperado:
            resultado.erro(f"{onde}: anotação '{chave}' fora do formato")
            return
        if chave == "sem-import":
            figura.sem_import.setdefault(par.groups(), []).append((partes[1], partes[2]))
        else:
            figura.somente[par.groups()] = partes[1]
        return
    nome, igual, alvo = valor.partition("=")
    if not igual:
        resultado.erro(f"{onde}: anotação '{chave}' sem '='")
        return
    nome, alvo = nome.strip(), alvo.strip()
    if chave == "modulo":
        figura.modulos[nome] = alvo
    elif chave == "caminho":
        incluidos, _, excluidos = alvo.partition(" - ")
        figura.caminhos[nome] = (separar(incluidos), separar(excluidos))
    elif chave == "servico":
        figura.servicos[nome] = alvo
    elif chave == "imagem":
        figura.imagens[nome] = alvo
    elif chave == "contrato":
        figura.contratos[nome] = alvo


def separar(texto: str) -> list[str]:
    return [p.strip().rstrip("/") for p in texto.split(",") if p.strip()]


def modulo_do_arquivo(arquivo: Path) -> str:
    partes = list(arquivo.relative_to(BACKEND).with_suffix("").parts)
    if partes[-1] == "__init__":
        partes.pop()
    return ".".join(partes)


def existe_modulo(modulo: str) -> bool:
    base = BACKEND.joinpath(*modulo.split("."))
    return base.is_dir() or base.with_suffix(".py").is_file()


def arquivos_python() -> list[Path]:
    arquivos = []
    for raiz in RAIZES_PYTHON:
        for arquivo in sorted((BACKEND / raiz).rglob("*.py")):
            if not any(p in PASTAS_IGNORADAS for p in arquivo.relative_to(BACKEND).parts):
                arquivos.append(arquivo)
    return arquivos


def nos_de_type_checking(arvore: ast.AST) -> set[int]:
    dentro: set[int] = set()
    for no in ast.walk(arvore):
        if isinstance(no, ast.If) and "TYPE_CHECKING" in ast.unparse(no.test):
            for filho in no.body:
                dentro.update(id(n) for n in ast.walk(filho))
    return dentro


def resolver_from(modulo_atual: str, no: ast.ImportFrom) -> str:
    if not no.level:
        return no.module or ""
    base = modulo_atual.split(".")[: -no.level] if no.level else []
    return ".".join([*base, no.module] if no.module else base)


def primeira_parte(modulo: str) -> bool:
    return modulo.split(".")[0] in RAIZES_PYTHON


def grafo_do_backend() -> tuple[list[Import], list[Heranca], list[str]]:
    imports: list[Import] = []
    herancas: list[Heranca] = []
    type_checking: list[str] = []
    for arquivo in arquivos_python():
        origem = modulo_do_arquivo(arquivo)
        caminho = arquivo.relative_to(BACKEND).as_posix()
        arvore = ast.parse(arquivo.read_text(encoding="utf-8"))
        ignorar = nos_de_type_checking(arvore)
        nomes: dict[str, str] = {}
        for no in ast.walk(arvore):
            if id(no) in ignorar:
                if isinstance(no, (ast.Import, ast.ImportFrom)):
                    type_checking.append(f"{caminho}:{no.lineno}")
                continue
            if isinstance(no, ast.Import):
                for alias in no.names:
                    if primeira_parte(alias.name):
                        imports.append(Import(origem, alias.name, caminho, no.lineno))
            elif isinstance(no, ast.ImportFrom):
                pacote = resolver_from(origem, no)
                if not primeira_parte(pacote):
                    continue
                for alias in no.names:
                    submodulo = f"{pacote}.{alias.name}"
                    destino = submodulo if existe_modulo(submodulo) else pacote
                    nomes[alias.asname or alias.name] = destino
                    imports.append(Import(origem, destino, caminho, no.lineno))
        for no in ast.walk(arvore):
            if isinstance(no, ast.ClassDef):
                for base in no.bases:
                    if isinstance(base, ast.Name) and base.id in nomes:
                        herancas.append(Heranca(origem, nomes[base.id], no.name, base.id, caminho, no.lineno))
    return sorted(set(imports), key=lambda i: (i.arquivo, i.linha, i.destino)), herancas, type_checking


def arquivos_do_frontend() -> list[Path]:
    arquivos = []
    for arquivo in sorted(FRONTEND_SRC.rglob("*.ts*")):
        rel = relativo(arquivo)
        if ".test." in arquivo.name or "testes" in arquivo.relative_to(FRONTEND_SRC).parts:
            continue
        if rel in FRONTEND_IGNORADOS or arquivo.suffix not in (".ts", ".tsx"):
            continue
        arquivos.append(arquivo)
    return arquivos


def resolver_ts(arquivo: Path, especificador: str) -> Path | None:
    alvo = Path(os.path.normpath(arquivo.parent / especificador))
    for candidato in (alvo, alvo.with_name(alvo.name + ".ts"), alvo.with_name(alvo.name + ".tsx"),
                      alvo / "index.ts", alvo / "index.tsx"):
        if candidato.is_file():
            return candidato
    return None


def grafo_do_frontend(resultado: Resultado) -> tuple[list[Import], int]:
    imports: list[Import] = []
    so_tipos = 0
    for arquivo in arquivos_do_frontend():
        texto = arquivo.read_text(encoding="utf-8")
        encontrados = [(m.start(), bool(m.group(2)), m.group(3)) for m in IMPORT_TS.finditer(texto)]
        encontrados += [(m.start(), False, m.group(1)) for m in IMPORT_TS_EFEITO.finditer(texto)]
        for inicio, e_tipo, especificador in encontrados:
            if not especificador.startswith("."):
                continue
            alvo = resolver_ts(arquivo, especificador)
            linha = texto.count("\n", 0, inicio) + 1
            if alvo is None:
                resultado.erro(f"{relativo(arquivo)}:{linha}: import '{especificador}' não resolvido")
                continue
            if alvo.suffix not in (".ts", ".tsx"):
                continue
            if e_tipo:
                so_tipos += 1
                continue
            imports.append(Import(relativo(arquivo), relativo(alvo), relativo(arquivo), linha))
    return imports, so_tipos


def concretos(figura: Figura, padrao: str) -> list[tuple[str, str | None]]:
    if "{ctx}" not in padrao:
        return [(padrao, None)]
    return [(padrao.replace("{ctx}", ctx), ctx) for ctx in figura.contextos]


def contexto_de(modulo: str) -> str | None:
    primeira = modulo.split(".")[0]
    return primeira if primeira in ("espacos", "reservas", "contas") else None


def folhas(figura: Figura, no: str) -> list[str]:
    if no in figura.subgrafos:
        return [n for n in figura.rotulos if no in figura.ancestrais.get(n, [])]
    return [no]


def no_contem(figura: Figura, no: str, alvo: str) -> list[str | None] | None:
    ligacoes: list[str | None] = []
    for folha in folhas(figura, no):
        if folha in figura.modulos:
            for concreto, ctx in concretos(figura, figura.modulos[folha]):
                if alvo == concreto or alvo.startswith(concreto + "."):
                    ligacoes.append(ctx if ctx is not None else contexto_de(concreto))
        elif folha in figura.caminhos:
            incluidos, excluidos = figura.caminhos[folha]
            if dentro(alvo, incluidos) and not dentro(alvo, excluidos):
                ligacoes.append(None)
    return ligacoes or None


def dentro(alvo: str, caminhos: list[str]) -> bool:
    return any(alvo == c or alvo.startswith(c + "/") for c in caminhos)


def generico(figura: Figura, no: str) -> bool:
    return any("{ctx}" in figura.modulos.get(f, "") for f in folhas(figura, no))


def seta_cobre(figura: Figura, seta: Seta, origem: str, destino: str) -> bool:
    ligacoes_o = no_contem(figura, seta.origem, origem)
    ligacoes_d = no_contem(figura, seta.destino, destino)
    if ligacoes_o is None or ligacoes_d is None:
        return False
    if not (generico(figura, seta.origem) or generico(figura, seta.destino)):
        return True
    return any(o is None or d is None or o == d for o in ligacoes_o for d in ligacoes_d)


def mapeado(figuras: list[Figura], alvo: str) -> bool:
    return any(no_contem(f, n, alvo) for f in figuras for n in [*f.modulos, *f.caminhos])


def mesmo_no(figuras: list[Figura], origem: str, destino: str) -> bool:
    for figura in figuras:
        for no in [*figura.modulos, *figura.caminhos]:
            o, d = no_contem(figura, no, origem), no_contem(figura, no, destino)
            if o and d and (not generico(figura, no) or set(o) & set(d)):
                return True
    return False


def verificar_estrutura(figuras: list[Figura], resultado: Resultado) -> None:
    for figura in figuras:
        declarados = set(figura.rotulos) | set(figura.subgrafos)
        for seta in figura.setas:
            for no in (seta.origem, seta.destino):
                if no not in declarados:
                    resultado.erro(f"{figura.nome}:{seta.linha}: nó '{no}' usado na seta e não declarado")
            if nao_representa_codigo(seta.origem) != nao_representa_codigo(seta.destino):
                resultado.erro(f"{figura.nome}:{seta.linha}: seta liga a legenda a um nó de código")
            if seta.tipo != "depende" and seta.tipo != "layout" and (
                seta.origem in figura.subgrafos or seta.destino in figura.subgrafos
            ):
                resultado.erro(f"{figura.nome}:{seta.linha}: seta '{seta.tipo}' só pode ligar nós, não subgraphs")
        mapeados = set(figura.modulos) | set(figura.caminhos) | set(figura.servicos)
        for no in figura.rotulos:
            if not nao_representa_codigo(no) and no not in mapeados:
                resultado.erro(f"{figura.nome}: nó '{no}' sem %% modulo, %% caminho ou %% servico")
        for no in mapeados - declarados:
            resultado.erro(f"{figura.nome}: o mapeamento cita o nó '{no}', que não existe na figura")
        for no, padrao in figura.modulos.items():
            for concreto, _ in concretos(figura, padrao):
                if not existe_modulo(concreto):
                    resultado.erro(f"{figura.nome}: nó '{no}' aponta para '{concreto}', que não existe em src/backend")
        for no, (incluidos, excluidos) in figura.caminhos.items():
            for caminho in incluidos + excluidos:
                if not (RAIZ / caminho).exists():
                    resultado.erro(f"{figura.nome}: nó '{no}' aponta para '{caminho}', que não existe")


def servicos_do_compose() -> dict[str, str | None]:
    servicos: dict[str, str | None] = {}
    atual = None
    em_servicos = False
    for linha in COMPOSE.read_text(encoding="utf-8").splitlines():
        if re.match(r"^\S", linha):
            em_servicos = linha.startswith("services:")
            continue
        if not em_servicos:
            continue
        if nome := re.match(r"^  ([\w-]+):\s*$", linha):
            atual = nome.group(1)
            servicos[atual] = None
        elif atual and (imagem := re.match(r"^    image:\s*(\S+)", linha)):
            servicos[atual] = imagem.group(1)
    return servicos


def verificar_compose(figuras: list[Figura], resultado: Resultado) -> None:
    compose = servicos_do_compose()
    citados = {s for f in figuras for s in f.servicos.values()}
    for figura in figuras:
        for no, servico in figura.servicos.items():
            if servico not in compose:
                resultado.erro(f"{figura.nome}: nó '{no}' cita o serviço '{servico}', que não está no docker-compose.yml")
        for servico, imagem in figura.imagens.items():
            if compose.get(servico) != imagem:
                resultado.erro(
                    f"{figura.nome}: imagem de '{servico}' é '{imagem}' na figura e '{compose.get(servico)}' no compose"
                )
    if citados:
        for servico in compose:
            if servico not in citados:
                resultado.erro(f"o serviço '{servico}' do docker-compose.yml não aparece em nenhuma figura")


def contratos_do_pyproject() -> list[str]:
    dados = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    return [c["name"] for c in dados["tool"]["importlinter"]["contracts"]]


def verificar_contratos(figuras: list[Figura], textos: dict[str, str], resultado: Resultado) -> None:
    existentes = set(contratos_do_pyproject())
    declarados: set[str] = set()
    for figura in figuras:
        for codigo, nome in figura.contratos.items():
            declarados.add(nome)
            if nome not in existentes:
                resultado.erro(f"{figura.nome}: o contrato {codigo} '{nome}' não existe no pyproject.toml")
            notas = " ".join(r for n, r in figura.rotulos.items() if n.startswith("NOTA_"))
            if f"{codigo} {nome}" not in notas:
                resultado.erro(f"{figura.nome}: a nota da figura não traz '{codigo} {nome}'")
        rotulos = [*figura.rotulos.values(), *figura.subgrafos.values(), *(s.rotulo for s in figura.setas)]
        for rotulo in rotulos:
            for numero in REF_CONTRATO.findall(rotulo):
                if f"C{numero}" not in figura.contratos:
                    resultado.erro(f"{figura.nome}: o rótulo cita C{numero}, que não tem %% contrato")
    if any(f.contratos for f in figuras):
        for nome in sorted(existentes - declarados):
            resultado.erro(f"o contrato '{nome}' do pyproject.toml não aparece em nenhuma figura")
    for arquivo, texto in textos.items():
        for nome in CONTRATO_NO_TEXTO.findall(texto):
            if nome not in existentes:
                resultado.erro(f"{arquivo}: cita o contrato '{nome}', que não existe no pyproject.toml")
        for teste in TESTE_NO_TEXTO.findall(texto):
            if not (BACKEND / teste).is_file():
                resultado.erro(f"{arquivo}: cita o teste '{teste}', que não existe em src/backend")


def verificar_sem_import(figura: Figura, seta: Seta, resultado: Resultado) -> list[str]:
    provas = []
    for arquivo, trecho in figura.sem_import.get((seta.origem, seta.destino), []):
        caminho = RAIZ / arquivo
        if not caminho.is_file():
            resultado.erro(f"{figura.nome}: sem-import {seta.origem} -> {seta.destino} cita '{arquivo}', que não existe")
        elif trecho not in caminho.read_text(encoding="utf-8"):
            resultado.erro(f"{figura.nome}: o trecho '{trecho}' não está em {arquivo}")
        else:
            linha = next(i for i, t in enumerate(caminho.read_text(encoding="utf-8").splitlines(), 1) if trecho in t)
            provas.append(f"sem import: {arquivo}:{linha} `{trecho}`")
    return provas


def verificar_setas(
    figuras: list[Figura], imports: list[Import], herancas: list[Heranca], resultado: Resultado
) -> list[tuple[Seta, list[str]]]:
    tabela = []
    for figura in figuras:
        for par in figura.sem_import:
            if not any((s.origem, s.destino) == par for s in figura.setas):
                resultado.erro(f"{figura.nome}: anotação sem-import {par[0]} -> {par[1]} sem a seta correspondente")
        for seta in figura.setas:
            if seta.tipo == "layout" or nao_representa_codigo(seta.origem):
                continue
            sustentam = [i for i in imports if seta_cobre(figura, seta, i.origem, i.destino)]
            provas = verificar_sem_import(figura, seta, resultado)
            onde = f"{figura.nome}:{seta.linha} {seta.origem} -> {seta.destino}"
            if seta.tipo == "implementa":
                classes = [h for h in herancas if seta_cobre(figura, seta, h.origem, h.destino)]
                if not classes:
                    resultado.erro(f"{onde}: seta 'implementa' sem classe que herde uma porta do destino")
                provas = [f"{h.arquivo}:{h.linha} {h.classe}({h.base})" for h in classes] + provas
            elif seta.tipo == "rede":
                if not provas:
                    resultado.erro(f"{onde}: seta de rede sem %% sem-import com o trecho que a prova")
            elif not sustentam and not provas:
                resultado.erro(f"{onde}: seta 'depende de' sem nenhum import real que a sustente")
            if seta.tipo != "rede":
                provas += [f"{i.arquivo}:{i.linha}" for i in sustentam]
            if (seta.origem, seta.destino) in figura.somente:
                sufixo = figura.somente[(seta.origem, seta.destino)]
                for i in sustentam:
                    if not i.arquivo.endswith(sufixo):
                        resultado.erro(f"{onde}: import em {i.arquivo}:{i.linha}, mas só '{sufixo}' pode tê-lo")
            tabela.append((seta, provas))
    return tabela


def verificar_cobertura(figuras: list[Figura], imports: list[Import], resultado: Resultado) -> list[str]:
    ignorados_usados = set()
    for i in imports:
        if mesmo_no(figuras, i.origem, i.destino):
            continue
        faltando = [m for m in (i.origem, i.destino) if not mapeado(figuras, m)]
        ignorado = [m for m in faltando if m in IGNORADOS]
        if ignorado:
            ignorados_usados.update(ignorado)
            continue
        if faltando:
            resultado.erro(f"{i.arquivo}:{i.linha}: '{faltando[0]}' não está em nenhum nó nem em IGNORADOS")
            continue
        if any(s.tipo in ("depende", "implementa") and seta_cobre(f, s, i.origem, i.destino)
               for f in figuras for s in f.setas):
            continue
        if any(i.origem.startswith(o) and i.destino.startswith(d) for o, d, _ in EXCECOES):
            continue
        resultado.erro(f"{i.arquivo}:{i.linha}: import {i.origem} → {i.destino} sem seta em nenhuma figura")
    return sorted(ignorados_usados)


def verificar_imagens(pasta: Path, resultado: Resultado) -> None:
    for fonte in sorted(pasta.glob("*.mmd")):
        for extensao in (".svg", ".png"):
            imagem = fonte.with_suffix(extensao)
            if not imagem.is_file():
                resultado.avisos.append(f"{imagem.name} não existe: gere as imagens (README.md da pasta)")
            elif imagem.stat().st_mtime < fonte.stat().st_mtime:
                resultado.avisos.append(f"{imagem.name} é mais antigo que {fonte.name}: gere as imagens de novo")


def rotulo(figura: Figura, no: str) -> str:
    if no in figura.subgrafos:
        return f"[{figura.subgrafos[no]}]"
    return primeira_linha(figura.rotulos.get(no, no))


def imprimir_tabela(tabela: list[tuple[Seta, list[str]]], figuras: dict[str, Figura]) -> None:
    print("| Figura | Seta | Tipo | Sustentada por (arquivo:linha) |")
    print("|---|---|---|---|")
    for seta, provas in tabela:
        figura = figuras[seta.figura]
        resumo = "; ".join(provas[:3]) + (f" (+{len(provas) - 3})" if len(provas) > 3 else "")
        print(f"| {seta.figura} | {rotulo(figura, seta.origem)} → {rotulo(figura, seta.destino)} "
              f"| {seta.tipo} | {resumo or '—'} |")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pasta", type=Path, default=PASTA_PADRAO, help="pasta com os .mmd")
    args = parser.parse_args()
    pasta = args.pasta.resolve()

    resultado = Resultado()
    fontes = sorted(pasta.glob("*.mmd"))
    if not fontes:
        print(f"Nenhum .mmd em {pasta}")
        return 1
    figuras = [ler_figura(f, resultado) for f in fontes]
    textos = {t: (pasta / t).read_text(encoding="utf-8") for t in TEXTOS if (pasta / t).is_file()}

    imports_py, herancas, type_checking = grafo_do_backend()
    imports_ts, so_tipos = grafo_do_frontend(resultado)
    imports = imports_py + imports_ts

    verificar_estrutura(figuras, resultado)
    verificar_compose(figuras, resultado)
    verificar_contratos(figuras, textos, resultado)
    tabela = verificar_setas(figuras, imports, herancas, resultado)
    ignorados = verificar_cobertura(figuras, imports, resultado)
    verificar_imagens(pasta, resultado)

    print(f"Figuras: {', '.join(f.nome for f in figuras)}")
    print(f"Imports lidos: {len(imports_py)} no backend, {len(imports_ts)} no frontend\n")
    imprimir_tabela(tabela, {f.nome: f for f in figuras})
    print("\nIgnorado de propósito:")
    print(f"- pastas {', '.join(PASTAS_IGNORADAS)} do backend; *.test.ts(x) e testes/ do frontend")
    print(f"- imports dentro de 'if TYPE_CHECKING:' ({len(type_checking)}): {', '.join(type_checking) or 'nenhum'}")
    print(f"- imports 'import type' do frontend (só tipos, somem no build): {so_tipos}")
    for modulo in ignorados:
        print(f"- {modulo}: {IGNORADOS[modulo]}")
    for arquivo, motivo in FRONTEND_IGNORADOS.items():
        print(f"- {arquivo}: {motivo}")
    print("Exceções (imports sem seta aceitos):", "nenhuma" if not EXCECOES else "")
    for origem, destino, motivo in EXCECOES:
        print(f"- {origem} → {destino}: {motivo}")
    for aviso in resultado.avisos:
        print(f"AVISO: {aviso}")
    if resultado.erros:
        print(f"\n{len(resultado.erros)} pendência(s):")
        for erro in resultado.erros:
            print(f"- {erro}")
        return 1
    print(f"\nOK: {len(tabela)} setas conferidas, todo import entre nós mapeados tem seta.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
