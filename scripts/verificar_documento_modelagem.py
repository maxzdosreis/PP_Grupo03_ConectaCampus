from __future__ import annotations

import argparse
import ast
import json
import re
import shutil
import struct
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verificar_visao_do_sistema as visao  # noqa: E402

RAIZ = visao.RAIZ
BACKEND = visao.BACKEND
SRC = RAIZ / "src"
FRONTEND = SRC / "frontend"
FRONTEND_SRC = visao.FRONTEND_SRC
PASTA = visao.PASTA_PADRAO
DOCUMENTO = PASTA / "modelagem.md"
DECISOES = RAIZ / "docs" / "fontes" / "requisitos" / "decisoes"

INICIO_DO_CORPO = "<!-- corpo:inicio -->"
FIM_DO_CORPO = "<!-- corpo:fim -->"
MARCADORES = ("[PENDENTE", "[CONFIRMAR COM O GRUPO")

TECNOLOGIAS: frozenset[str] = frozenset()

PALAVRAS_POR_PAGINA = 500
LINHAS_DE_TABELA_POR_PAGINA = 28
ALTURA_UTIL_CM = 24.7
LARGURA_UTIL_CM = 16.0
ESPACO_POR_FIGURA_CM = 0.6
ALVO_DE_PAGINAS = 5.5
LIMITE_DE_PAGINAS = 6.0

ARQUIVOS_DE_AMBIENTE = (
    SRC / ".env.example",
    SRC / ".env.prod.example",
    SRC / "docker-compose.yml",
    SRC / "docker-compose.prod.yml",
    BACKEND / "Dockerfile",
    BACKEND / "Dockerfile.prod",
    FRONTEND / "Dockerfile",
    FRONTEND / "Dockerfile.prod",
)
COMPOSES = (SRC / "docker-compose.yml", SRC / "docker-compose.prod.yml")
DOCKERFILES = (BACKEND / "Dockerfile", BACKEND / "Dockerfile.prod", FRONTEND / "Dockerfile", FRONTEND / "Dockerfile.prod")
RAIZES_DE_CAMINHO = (RAIZ, SRC, BACKEND, FRONTEND, FRONTEND_SRC, PASTA)
PASTAS_IGNORADAS = {"__pycache__", "node_modules", "mutants", ".git", "dist"}
CAMADAS = ("api", "application", "domain", "infrastructure")
NUMEROS_POR_EXTENSO = {"dois": 2, "três": 3, "quatro": 4, "cinco": 5, "seis": 6, "dez": 10}

CRASE = re.compile(r"`([^`]+)`")
IMAGEM = re.compile(r"^!\[Figura (\d+) — ([^\]]+)\]\(([^)]+)\)$")
LARGURA = re.compile(r"^<!--\s*largura:\s*([\d.,]+)\s*cm\s*-->$")
VERSAO_NO_TEXTO = re.compile(r"\b(Python|Django|PostgreSQL|Redis|Node|React|TypeScript|Vite|Vitest|gunicorn|nginx) (\d+(?:\.\d+)*)\b")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
TELEFONE = re.compile(r"\(?\b\d{2}\)?\s?9?\d{4}-\d{4}\b")
SEIS_DIGITOS = re.compile(r"\d{6,}")


@dataclass
class Secao:
    titulo: str
    linhas: list[str] = field(default_factory=list)


def ler_corpo(documento: Path, resultado: visao.Resultado) -> list[Secao]:
    texto = documento.read_text(encoding="utf-8")
    if INICIO_DO_CORPO not in texto or FIM_DO_CORPO not in texto:
        resultado.erro(f"{documento.name}: faltam os marcadores {INICIO_DO_CORPO} e {FIM_DO_CORPO}")
        return []
    corpo = texto.split(INICIO_DO_CORPO, 1)[1].split(FIM_DO_CORPO, 1)[0]
    secoes = [Secao("0. Título e nomes")]
    for linha in corpo.splitlines():
        if linha.startswith("## "):
            secoes.append(Secao(linha[3:].strip()))
        secoes[-1].linhas.append(linha)
    return secoes


# ---------------------------------------------------------------- 1. nomes


@dataclass
class IndiceDoCodigo:
    simbolos: dict[str, str] = field(default_factory=dict)
    metodos: dict[str, set[str]] = field(default_factory=dict)
    importados: dict[str, str] = field(default_factory=dict)
    textos: dict[str, str] = field(default_factory=dict)
    testes_e_migrations: dict[str, str] = field(default_factory=dict)


def arquivos(raiz: Path, padroes: tuple[str, ...]) -> list[Path]:
    encontrados = []
    for padrao in padroes:
        for arquivo in raiz.rglob(padrao):
            if not PASTAS_IGNORADAS.intersection(arquivo.relative_to(raiz).parts):
                encontrados.append(arquivo)
    return sorted(encontrados)


def codigo_antes_dos_testes(arquivo: Path) -> tuple[bool, str]:
    partes = arquivo.relative_to(BACKEND).parts
    return ("tests" in partes or "migrations" in partes, str(arquivo))


def indexar_testes_e_migrations(arquivo: Path, indice: IndiceDoCodigo) -> None:
    onde = visao.relativo(arquivo)
    for no in ast.walk(ast.parse(arquivo.read_text(encoding="utf-8"))):
        nomes: list[str] = []
        if isinstance(no, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            nomes = [no.name]
        elif isinstance(no, ast.ImportFrom):
            nomes = [n.asname or n.name for n in no.names]
        elif isinstance(no, ast.Constant) and isinstance(no.value, str) and re.fullmatch(r"[\w.-]+", no.value):
            nomes = [no.value]
        for nome in nomes:
            indice.testes_e_migrations.setdefault(nome, f"em {onde}:{no.lineno}")


def indexar_backend() -> IndiceDoCodigo:
    indice = IndiceDoCodigo()
    for arquivo in sorted(arquivos(BACKEND, ("*.py",)), key=codigo_antes_dos_testes):
        if codigo_antes_dos_testes(arquivo)[0]:
            indexar_testes_e_migrations(arquivo, indice)
            continue
        onde = visao.relativo(arquivo)
        arvore = ast.parse(arquivo.read_text(encoding="utf-8"))
        for no in ast.walk(arvore):
            if isinstance(no, ast.ClassDef):
                indice.simbolos.setdefault(no.name, f"classe em {onde}:{no.lineno}")
                metodos = indice.metodos.setdefault(no.name, set())
                metodos.update(f.name for f in no.body if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef)))
            elif isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef)):
                indice.simbolos.setdefault(no.name, f"função em {onde}:{no.lineno}")
            elif isinstance(no, (ast.Assign, ast.AnnAssign)):
                alvos = no.targets if isinstance(no, ast.Assign) else [no.target]
                for alvo in alvos:
                    if isinstance(alvo, ast.Name):
                        indice.simbolos.setdefault(alvo.id, f"constante em {onde}:{no.lineno}")
            elif isinstance(no, ast.ImportFrom):
                for nome in no.names:
                    indice.importados.setdefault(nome.asname or nome.name, f"importado em {onde}:{no.lineno}")
            elif isinstance(no, ast.Constant) and isinstance(no.value, str) and re.fullmatch(r"[\w.-]+", no.value):
                indice.textos.setdefault(no.value, f"texto em {onde}:{no.lineno}")
    return indice


def contratos() -> list[str]:
    return visao.contratos_do_pyproject()


def servicos() -> dict[str, str]:
    encontrados: dict[str, str] = {}
    for compose in COMPOSES:
        dentro = False
        for numero, linha in enumerate(compose.read_text(encoding="utf-8").splitlines(), start=1):
            if re.match(r"^\S", linha):
                dentro = linha.startswith("services:")
                continue
            casamento = re.match(r"^  ([a-z][\w-]*):\s*$", linha)
            if dentro and casamento:
                encontrados.setdefault(casamento.group(1), f"serviço em {visao.relativo(compose)}:{numero}")
    return encontrados


def imagens_docker() -> dict[str, str]:
    encontradas: dict[str, str] = {}
    for arquivo in (*COMPOSES, *DOCKERFILES):
        for numero, linha in enumerate(arquivo.read_text(encoding="utf-8").splitlines(), start=1):
            casamento = re.match(r"^\s*(?:FROM|image:)\s+(\S+:\S+)", linha)
            if casamento:
                encontradas.setdefault(casamento.group(1), f"imagem em {visao.relativo(arquivo)}:{numero}")
    return encontradas


def variaveis_de_ambiente() -> dict[str, str]:
    encontradas: dict[str, str] = {}
    for arquivo in ARQUIVOS_DE_AMBIENTE:
        if not arquivo.exists():
            continue
        for numero, linha in enumerate(arquivo.read_text(encoding="utf-8").splitlines(), start=1):
            for nome in re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", linha):
                encontradas.setdefault(nome, f"variável em {visao.relativo(arquivo)}:{numero}")
    return encontradas


def achar_caminho(nome: str) -> str | None:
    for raiz in RAIZES_DE_CAMINHO:
        if (raiz / nome).exists():
            return f"arquivo {visao.relativo(raiz / nome)}"
    if "/" not in nome:
        achados = [a for a in arquivos(SRC, (nome,)) if a.name == nome]
        if achados:
            extra = f" (+{len(achados) - 1})" if len(achados) > 1 else ""
            return f"arquivo {visao.relativo(achados[0])}{extra}"
    return None


def eh_caminho(nome: str) -> bool:
    return "/" in nome or bool(re.search(r"\.(py|ts|tsx|ya?ml|conf|md|png|svg|json|toml|pdf)$", nome))


def achar_no_frontend(nome: str) -> str | None:
    for arquivo in arquivos(FRONTEND_SRC, ("*.ts", "*.tsx", "*.css")):
        if re.search(rf"\b{re.escape(nome)}\b", arquivo.read_text(encoding="utf-8")):
            return f"texto em {visao.relativo(arquivo)}"
    return None


class Resolvedor:
    def __init__(self) -> None:
        self.indice = indexar_backend()
        self.contratos = contratos()
        self.servicos = servicos()
        self.imagens = imagens_docker()
        self.variaveis = variaveis_de_ambiente()

    def resolver(self, nome: str) -> str | None:
        if nome in TECNOLOGIAS:
            return "exceção (TECNOLOGIAS)"
        if nome in self.contratos:
            return "contrato do import-linter em src/backend/pyproject.toml"
        if nome in self.imagens:
            return self.imagens[nome]
        if eh_caminho(nome):
            return achar_caminho(nome)
        if re.fullmatch(r"[a-z_]+(\.[a-z_]+)+", nome):
            modulo = BACKEND.joinpath(*nome.split("."))
            if modulo.with_suffix(".py").exists() or (modulo / "__init__.py").exists():
                return f"módulo {visao.relativo(modulo)}"
            return None
        if re.fullmatch(r"[A-Z]\w*\.\w+", nome):
            classe, metodo = nome.split(".")
            if metodo in self.indice.metodos.get(classe, set()):
                return f"método de {self.indice.simbolos[classe]}"
            return None
        if (BACKEND / nome).is_dir() and list((BACKEND / nome).glob("*.py")):
            return f"pacote src/backend/{nome}"
        if nome in self.servicos:
            return self.servicos[nome]
        origens = (self.indice.simbolos, self.indice.textos, self.variaveis, self.indice.importados,
                   self.indice.testes_e_migrations)
        for origem in origens:
            if nome in origem:
                return origem[nome]
        return achar_no_frontend(nome)


def verificar_nomes(secoes: list[Secao], resultado: visao.Resultado) -> list[tuple[str, str, str]]:
    resolvedor = Resolvedor()
    tabela = []
    for secao in secoes:
        for linha in secao.linhas:
            if IMAGEM.match(linha):
                continue
            for nome in CRASE.findall(linha):
                onde = resolvedor.resolver(nome)
                tabela.append((secao.titulo, nome, onde or "NÃO ENCONTRADO"))
                if onde is None:
                    resultado.erro(f"seção '{secao.titulo}': `{nome}` não existe no repositório")
    return tabela


def ler(caminho: Path) -> str:
    return caminho.read_text(encoding="utf-8")


def do_requirements(pacote: str) -> tuple[str, str]:
    caminho = BACKEND / "requirements.txt"
    casamento = re.search(rf"^{re.escape(pacote)}(?:\[\w+\])?==(\S+)", ler(caminho), re.MULTILINE | re.IGNORECASE)
    return (casamento.group(1) if casamento else "?", f"{visao.relativo(caminho)} ({pacote})")


def do_package_lock(pacote: str) -> tuple[str, str]:
    caminho = FRONTEND / "package-lock.json"
    pacotes = json.loads(ler(caminho))["packages"]
    return (pacotes.get(f"node_modules/{pacote}", {}).get("version", "?"), f"{visao.relativo(caminho)} ({pacote})")


def da_imagem(arquivos_: tuple[Path, ...], imagem: str) -> tuple[str, str]:
    for caminho in arquivos_:
        casamento = re.search(rf"(?:FROM|image:)\s+{re.escape(imagem)}:(\d+(?:\.\d+)*)", ler(caminho))
        if casamento:
            return (casamento.group(1), f"{visao.relativo(caminho)} ({imagem})")
    return ("?", f"imagem {imagem} não encontrada")


FONTES_DE_VERSAO = {
    "Python": lambda: da_imagem((BACKEND / "Dockerfile",), "python"),
    "Django": lambda: do_requirements("Django"),
    "Django REST Framework": lambda: do_requirements("djangorestframework"),
    "Simple JWT": lambda: do_requirements("djangorestframework-simplejwt"),
    "PostgreSQL": lambda: da_imagem(COMPOSES, "postgres"),
    "Redis": lambda: da_imagem(COMPOSES, "redis"),
    "Node": lambda: da_imagem((FRONTEND / "Dockerfile",), "node"),
    "React": lambda: do_package_lock("react"),
    "TypeScript": lambda: do_package_lock("typescript"),
    "Vite": lambda: do_package_lock("vite"),
    "Vitest": lambda: do_package_lock("vitest"),
    "gunicorn": lambda: do_requirements("gunicorn"),
    "nginx": lambda: da_imagem((FRONTEND / "Dockerfile.prod",), "nginx"),
}


def compativel(citada: str, real: str) -> bool:
    return real == citada or real.startswith(citada + ".")


def verificar_versoes(secoes: list[Secao], resultado: visao.Resultado) -> list[tuple[str, str, str, str]]:
    citacoes: list[tuple[str, str]] = []
    for secao in secoes:
        for linha in secao.linhas:
            celulas = [c.strip() for c in linha.strip().strip("|").split("|")] if linha.startswith("|") else []
            if len(celulas) >= 2 and celulas[0] in FONTES_DE_VERSAO:
                versao = re.match(r"\d+(?:\.\d+)*", celulas[1])
                if versao:
                    citacoes.append((celulas[0], versao.group(0)))
            elif not celulas:
                citacoes += VERSAO_NO_TEXTO.findall(linha)
    tabela = []
    for tecnologia, citada in citacoes:
        real, origem = FONTES_DE_VERSAO[tecnologia]()
        situacao = "ok" if compativel(citada, real) else "DIVERGE"
        tabela.append((tecnologia, citada, f"{real} — {origem}", situacao))
        if situacao != "ok":
            resultado.erro(f"versão de {tecnologia}: o documento diz {citada}, o repositório tem {real} ({origem})")
    versoes_python = {da_imagem((d,), "python")[0] for d in (BACKEND / "Dockerfile", BACKEND / "Dockerfile.prod")}
    if len(versoes_python) > 1:
        resultado.erro(f"os Dockerfiles do backend usam Pythons diferentes: {sorted(versoes_python)}")
    return tabela


def dimensoes_do_png(caminho: Path) -> tuple[int, int]:
    cabecalho = caminho.read_bytes()[:24]
    return struct.unpack(">II", cabecalho[16:24])


@dataclass
class FiguraCitada:
    numero: int
    titulo: str
    arquivo: str
    secao: str
    largura_cm: float
    altura_cm: float = 0.0


def figuras_do_corpo(secoes: list[Secao]) -> list[FiguraCitada]:
    figuras = []
    for secao in secoes:
        largura = LARGURA_UTIL_CM
        for linha in secao.linhas:
            casamento_largura = LARGURA.match(linha.strip())
            if casamento_largura:
                largura = float(casamento_largura.group(1).replace(",", "."))
                continue
            casamento = IMAGEM.match(linha.strip())
            if casamento:
                figuras.append(FiguraCitada(int(casamento.group(1)), casamento.group(2), casamento.group(3), secao.titulo, largura))
                largura = LARGURA_UTIL_CM
    return figuras


def verificar_figuras(secoes: list[Secao], resultado: visao.Resultado) -> list[FiguraCitada]:
    figuras = figuras_do_corpo(secoes)
    corpo = "\n".join(linha for secao in secoes for linha in secao.linhas)
    for esperado, figura in enumerate(figuras, start=1):
        if figura.numero != esperado:
            resultado.erro(f"Figura {figura.numero} fora da sequência: esperava a Figura {esperado}")
        imagem = PASTA / figura.arquivo
        if not imagem.exists():
            resultado.erro(f"Figura {figura.numero}: {figura.arquivo} não existe em {visao.relativo(PASTA)}")
            continue
        if not imagem.with_suffix(".mmd").exists():
            resultado.erro(f"Figura {figura.numero}: {figura.arquivo} não tem a fonte {imagem.with_suffix('.mmd').name}")
        if f"Figura {figura.numero} — {figura.titulo}." not in corpo:
            resultado.erro(f"Figura {figura.numero}: falta a legenda 'Figura {figura.numero} — {figura.titulo}. ...'")
        largura_px, altura_px = dimensoes_do_png(imagem)
        figura.altura_cm = figura.largura_cm * altura_px / largura_px
    avisos = visao.Resultado()
    visao.verificar_imagens(PASTA, avisos)
    citadas = {Path(f.arquivo).stem for f in figuras}
    resultado.avisos += [a for a in avisos.avisos if a.split(".")[0] in citadas]
    return figuras


def avaliar(no: ast.AST, nomes: dict[str, float]) -> float:
    if isinstance(no, ast.Constant) and isinstance(no.value, (int, float)):
        return no.value
    if isinstance(no, ast.Name):
        return nomes[no.id]
    if isinstance(no, ast.BinOp) and isinstance(no.op, (ast.Mult, ast.Add)):
        esquerda, direita = avaliar(no.left, nomes), avaliar(no.right, nomes)
        return esquerda * direita if isinstance(no.op, ast.Mult) else esquerda + direita
    if isinstance(no, ast.Call) and getattr(no.func, "id", "") == "timedelta":
        fatores = {"days": 1440, "hours": 60, "minutes": 1}
        return sum(avaliar(k.value, nomes) * fatores[k.arg] for k in no.keywords)
    raise ValueError(f"expressão não suportada: {ast.dump(no)}")


def constantes(caminho: Path) -> dict[str, float]:
    valores: dict[str, float] = {}
    for no in ast.parse(ler(caminho)).body:
        if isinstance(no, ast.Assign) and len(no.targets) == 1 and isinstance(no.targets[0], ast.Name):
            try:
                valores[no.targets[0].id] = avaliar(no.value, valores)
            except (ValueError, KeyError):
                continue
    return valores


def hora(minutos: float) -> str:
    minutos = int(minutos) % 1440
    return f"{minutos // 60:02d}:{minutos % 60:02d}"


def valor_do_env(nome: str) -> str:
    casamento = re.search(rf"^{nome}=(\S+)", ler(SRC / ".env.example"), re.MULTILINE)
    return casamento.group(1) if casamento else "?"


def contextos_com_as_camadas() -> list[str]:
    return sorted(p.name for p in BACKEND.iterdir() if p.is_dir() and all((p / c).is_dir() for c in CAMADAS))


def numero(texto: str) -> int:
    return NUMEROS_POR_EXTENSO.get(texto, int(texto) if texto.isdigit() else -1)


def regras_de_numeros() -> list[tuple[str, re.Pattern[str], callable, str]]:
    agenda = constantes(BACKEND / "reservas" / "domain" / "regras_de_agenda.py")
    horario = constantes(BACKEND / "espacos" / "domain" / "horario_de_funcionamento.py")
    cadastro = constantes(BACKEND / "contas" / "domain" / "cadastro.py")
    dec08 = ler(DECISOES / "DEC-08.md")
    fail_under = re.search(r"^fail_under\s*=\s*(\d+)", ler(BACKEND / "pyproject.toml"), re.MULTILINE).group(1)
    origem_agenda = "src/backend/reservas/domain/regras_de_agenda.py"
    return [
        ("duração sugerida", re.compile(r"(\d+) h sugerida"), lambda m: int(m[1]) * 60 == agenda["DURACAO_SUGERIDA"],
         f"DURACAO_SUGERIDA = {agenda['DURACAO_SUGERIDA']:.0f} min ({origem_agenda})"),
        ("duração mínima e máxima", re.compile(r"de (\d+) min a (\d+) h"),
         lambda m: int(m[1]) == agenda["DURACAO_MINIMA"] and int(m[2]) * 60 == agenda["DURACAO_MAXIMA"],
         f"DURACAO_MINIMA = {agenda['DURACAO_MINIMA']:.0f} min, DURACAO_MAXIMA = {agenda['DURACAO_MAXIMA']:.0f} min ({origem_agenda})"),
        ("antecedência", re.compile(r"(\d+) dias de antecedência"), lambda m: int(m[1]) == agenda["ANTECEDENCIA_MAXIMA_EM_DIAS"],
         f"ANTECEDENCIA_MAXIMA_EM_DIAS = {agenda['ANTECEDENCIA_MAXIMA_EM_DIAS']:.0f} ({origem_agenda})"),
        ("funcionamento padrão", re.compile(r"das (\d\d:\d\d) às (\d\d:\d\d)"),
         lambda m: (m[1], m[2]) == (hora(horario["ABERTURA_PADRAO_EM_MINUTOS"]), hora(horario["FECHAMENTO_PADRAO_EM_MINUTOS"])),
         f"ABERTURA_PADRAO_EM_MINUTOS = {horario['ABERTURA_PADRAO_EM_MINUTOS']:.0f}, FECHAMENTO_PADRAO_EM_MINUTOS = "
         f"{horario['FECHAMENTO_PADRAO_EM_MINUTOS']:.0f} (src/backend/espacos/domain/horario_de_funcionamento.py)"),
        ("matrícula", re.compile(r"até (\d+) dígitos"), lambda m: int(m[1]) == cadastro["MATRICULA_MAXIMO_CARACTERES"],
         f"MATRICULA_MAXIMO_CARACTERES = {cadastro['MATRICULA_MAXIMO_CARACTERES']:.0f} (src/backend/contas/domain/cadastro.py)"),
        ("cobertura das camadas", re.compile(r"(\d+)% de linhas e ramos"), lambda m: f"{m[1]}% de linhas e ramos" in dec08,
         "DEC-08: '100% de linhas e ramos nas camadas domain e application de espacos e reservas'"),
        ("cobertura total", re.compile(r"no total, (\d+)%"), lambda m: m[1] == fail_under and f"no mínimo {m[1]}%" in dec08,
         f"fail_under = {fail_under} (src/backend/pyproject.toml) e DEC-08"),
        ("token de acesso", re.compile(r"acesso dura (\d+) minutos"), lambda m: m[1] == valor_do_env("JWT_ACCESS_MINUTES"),
         f"JWT_ACCESS_MINUTES={valor_do_env('JWT_ACCESS_MINUTES')} (src/.env.example)"),
        ("token de renovação", re.compile(r"renovação, (\d+) dia"), lambda m: m[1] == valor_do_env("JWT_REFRESH_DAYS"),
         f"JWT_REFRESH_DAYS={valor_do_env('JWT_REFRESH_DAYS')} (src/.env.example)"),
        ("contextos e camadas", re.compile(r"(\w+) contextos com as mesmas (\w+) camadas"),
         lambda m: (numero(m[1]), numero(m[2])) == (len(contextos_com_as_camadas()), len(CAMADAS)),
         f"{len(contextos_com_as_camadas())} pastas de src/backend com {', '.join(CAMADAS)}: {', '.join(contextos_com_as_camadas())}"),
        ("contratos do import-linter", re.compile(r"(\w+) contratos"), lambda m: numero(m[1]) == len(contratos()),
         f"{len(contratos())} contratos em src/backend/pyproject.toml"),
    ]


def verificar_numeros(secoes: list[Secao], resultado: visao.Resultado) -> list[tuple[str, str, str, str]]:
    corpo = " ".join(linha for secao in secoes for linha in secao.linhas)
    tabela = []
    for nome, padrao, confere, fonte in regras_de_numeros():
        casamentos = list(padrao.finditer(corpo))
        if not casamentos:
            tabela.append((nome, "não citado", fonte, "—"))
        for casamento in casamentos:
            situacao = "ok" if confere(casamento) else "DIVERGE"
            tabela.append((nome, casamento.group(0), fonte, situacao))
            if situacao != "ok":
                resultado.erro(f"{nome}: o documento diz '{casamento.group(0)}', a fonte diz {fonte}")
    return tabela


def marcadores(secoes: list[Secao]) -> list[tuple[str, str]]:
    achados = []
    for secao in secoes:
        for linha in secao.linhas:
            for casamento in re.finditer(r"\[(PENDENTE|CONFIRMAR COM O GRUPO):[^\]]*\]", linha):
                achados.append((secao.titulo, casamento.group(0)))
    return achados


@dataclass
class Medida:
    secao: str
    palavras: int = 0
    linhas_de_tabela: int = 0
    figuras_cm: float = 0.0

    def paginas(self) -> float:
        return (
            self.palavras / PALAVRAS_POR_PAGINA
            + self.linhas_de_tabela / LINHAS_DE_TABELA_POR_PAGINA
            + self.figuras_cm / ALTURA_UTIL_CM
        )


def medir(secoes: list[Secao], figuras: list[FiguraCitada]) -> list[Medida]:
    medidas = []
    for secao in secoes:
        medida = Medida(secao.titulo)
        for linha in secao.linhas:
            limpa = linha.strip()
            if not limpa or limpa.startswith("<!--") or IMAGEM.match(limpa):
                continue
            if limpa.startswith("|"):
                if not re.fullmatch(r"\|[\s|:-]+\|", limpa):
                    medida.linhas_de_tabela += 1
                continue
            medida.palavras += len(re.sub(r"^#+\s*", "", limpa).split())
        medida.figuras_cm = sum(f.altura_cm + ESPACO_POR_FIGURA_CM for f in figuras if f.secao == secao.titulo)
        medidas.append(medida)
    return medidas


def dados_pessoais(documento: Path) -> list[str]:
    achados = []
    for numero_da_linha, linha in enumerate(ler(documento).splitlines(), start=1):
        for padrao, tipo in ((EMAIL, "e-mail"), (TELEFONE, "telefone"), (SEIS_DIGITOS, "6 ou mais dígitos")):
            achados += [f"linha {numero_da_linha}: {tipo} '{m}'" for m in padrao.findall(linha)]
    return achados


def caminho_para_mostrar(caminho: Path) -> str:
    try:
        return visao.relativo(caminho)
    except ValueError:
        return str(caminho)


def imprimir_tabela(cabecalho: tuple[str, ...], linhas: list[tuple]) -> None:
    print("| " + " | ".join(cabecalho) + " |")
    print("|" + "---|" * len(cabecalho))
    for linha in linhas:
        print("| " + " | ".join(str(c).replace("|", r"\|") for c in linha) + " |")
    print()


def verificar(documento: Path, *, silencioso: bool = False) -> visao.Resultado:
    resultado = visao.Resultado()
    secoes = ler_corpo(documento, resultado)
    if not secoes:
        return resultado
    nomes = verificar_nomes(secoes, resultado)
    versoes = verificar_versoes(secoes, resultado)
    figuras = verificar_figuras(secoes, resultado)
    numeros = verificar_numeros(secoes, resultado)
    pendencias = marcadores(secoes)
    medidas = medir(secoes, figuras)
    pessoais = dados_pessoais(documento)
    for achado in pessoais:
        resultado.erro(f"dado pessoal possível: {achado}")
    total = sum(m.paginas() for m in medidas)
    if total > LIMITE_DE_PAGINAS:
        resultado.erro(f"estimativa de {total:.2f} páginas passa do limite de {LIMITE_DE_PAGINAS:.0f}")
    elif total > ALVO_DE_PAGINAS:
        resultado.avisos.append(f"estimativa de {total:.2f} páginas passa do alvo de {ALVO_DE_PAGINAS}")
    if silencioso:
        return resultado

    print(f"Documento: {caminho_para_mostrar(documento)}\n")
    print(f"1) Nomes entre crases ({len(nomes)})\n")
    imprimir_tabela(("Seção", "Nome", "Onde existe"), nomes)
    print("2) Versões\n")
    imprimir_tabela(("Tecnologia", "No documento", "No repositório — origem", "Situação"), versoes)
    print("3) Figuras\n")
    imprimir_tabela(
        ("Figura", "Arquivo", "Fonte", "Seção", "Largura (cm)", "Altura (cm)"),
        [(f.numero, f.arquivo, Path(f.arquivo).with_suffix(".mmd").name, f.secao, f"{f.largura_cm:.1f}", f"{f.altura_cm:.1f}") for f in figuras],
    )
    print("4) Números\n")
    imprimir_tabela(("Regra", "No documento", "Fonte", "Situação"), numeros)
    print(f"5) Marcadores ({len(pendencias)})\n")
    imprimir_tabela(("Seção", "Marcador"), pendencias)
    print("6) Tamanho (A4, margens de 2,5 cm, corpo 11 pt, espaçamento simples; "
          f"{PALAVRAS_POR_PAGINA} palavras, {LINHAS_DE_TABELA_POR_PAGINA} linhas de tabela e "
          f"{ALTURA_UTIL_CM} cm de figura por página; {ESPACO_POR_FIGURA_CM} cm de espaço por figura)\n")
    imprimir_tabela(
        ("Seção", "Palavras", "Linhas de tabela", "Figuras (cm)", "Páginas"),
        [(m.secao, m.palavras, m.linhas_de_tabela, f"{m.figuras_cm:.1f}", f"{m.paginas():.2f}") for m in medidas]
        + [("Total", sum(m.palavras for m in medidas), sum(m.linhas_de_tabela for m in medidas),
            f"{sum(m.figuras_cm for m in medidas):.1f}", f"{total:.2f}")],
    )
    print(f"Margem até {LIMITE_DE_PAGINAS:.0f} páginas: {LIMITE_DE_PAGINAS - total:.2f}; até o alvo de {ALVO_DE_PAGINAS}: "
          f"{ALVO_DE_PAGINAS - total:.2f}. Cabe em 6 páginas: {'sim' if total <= LIMITE_DE_PAGINAS else 'não'}.\n")
    print(f"7) Dados pessoais: {'nenhum' if not pessoais else len(pessoais)}\n")
    return resultado


def teste_negativo(documento: Path) -> int:
    original = ler(documento)
    trocado = "ConflitoDeHorario"
    inventado = "ConflitoInventadoDeHorario"
    if f"`{trocado}`" not in original:
        print(f"O teste negativo precisa de `{trocado}` no documento.")
        return 1
    pasta = Path(tempfile.mkdtemp(prefix="verificar_documento_modelagem_"))
    copia = pasta / documento.name
    try:
        copia.write_text(original.replace(f"`{trocado}`", f"`{inventado}`", 1), encoding="utf-8")
        print(f"Cópia temporária: {copia} (`{trocado}` trocado por `{inventado}`)")
        resultado = verificar(copia, silencioso=True)
    finally:
        shutil.rmtree(pasta)
    print(f"Cópia descartada: {not pasta.exists()}")
    for erro in resultado.erros:
        print(f"ERRO (esperado): {erro}")
    if any(inventado in erro for erro in resultado.erros):
        print("OK: o verificador falha com um nome que não existe.")
        return 0
    print("FALHOU: o nome inventado passou pela verificação.")
    return 1


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--arquivo", type=Path, default=DOCUMENTO, help="documento a verificar")
    parser.add_argument("--negativo", action="store_true", help="prova, numa cópia temporária, que um nome inventado falha")
    argumentos = parser.parse_args()
    documento = argumentos.arquivo.resolve()
    if argumentos.negativo:
        return teste_negativo(documento)
    resultado = verificar(documento)
    for aviso in resultado.avisos:
        print(f"AVISO: {aviso}")
    for erro in resultado.erros:
        print(f"ERRO: {erro}")
    if resultado.erros:
        print(f"\nFALHOU: {len(resultado.erros)} problema(s).")
        return 1
    print("OK: nomes, versões, figuras, números e tamanho conferidos contra o repositório.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
