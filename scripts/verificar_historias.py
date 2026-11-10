from __future__ import annotations

import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verificar_casos_de_uso import (  # noqa: E402
    FICHAS_COMPLETAS,
    ITEM_COMPLETO,
    PASTA_UC,
    RESUMIDAS,
    _ancoras_de,
)
from verificar_requisitos import PASTA, RAIZ, fichas_de_rf, ler, relativo  # noqa: E402

PASTA_US = PASTA / "historias"
README_US = PASTA_US / "README.md"
SRS = PASTA / "requisitos" / "srs.md"
BACKEND = RAIZ / "src" / "backend"
FRONTEND = RAIZ / "src" / "frontend" / "src"

CAMPOS_DO_CARD = (
    "ID",
    "Título",
    "História",
    "Valor",
    "Origem",
    "Prioridade",
    "Estimativa (Custo em Semanas)",
    "Conversa",
    "Pronta quando",
)
LETRAS_INVEST = ("I", "N", "V", "E", "S", "T")
TIPOS_DE_CA = ("sucesso", "alternativa", "exceção", "registro", "acesso")
TAREFAS_DE_CODIGO = ("RES-11", "RES-12", "ESP-07", "AUT-12")
MARCA_PENDENTE = re.compile(r"^implementação pendente \(tarefa (?P<tarefa>[A-Z]{2,3}-\d{2})\)(?P<resto>.*)$")
RF_SEM_HISTORIA = {"RF-38": "transversal: o resultado de cada operação aparece no Então de todos os CAs"}
TERMOS_PROIBIDOS = {
    "HTTP": r"\bhttps?\b",
    "código de status": r"\b(?:200|201|400|401|403|404|405|409|500|503)\b",
    "/api/": r"/api/",
    "endpoint": r"\bendpoints?\b",
    "JSON": r"\bjson\b",
    "clica": r"\bclica",
    "botão": r"\bbot(?:ão|ões)\b",
    "tela": r"\btelas?\b",
    "toast": r"\btoasts?\b",
    "React": r"\breact\b",
    "Django": r"\bdjango\b",
    "JWT": r"\bjwt\b",
}

ARQUIVO_US = re.compile(r"^US-(\d{2})-[\w-]+\.md$")
CAMPO = re.compile(r"^\|\s*\*\*(?P<campo>[^*]+)\*\*\s*\|\s*(?P<valor>.*?)\s*\|\s*$")
INVEST = re.compile(
    r"^\|\s*\*\*(?P<letra>[A-Z])\*\*\s*·\s*[^|]+\|\s*(?P<atende>[^|]*?)\s*\|\s*(?P<justificativa>.*?)\s*\|\s*$"
)
CABECALHO_CA = re.compile(
    r'^#### <a id="(?P<ancora>us-(?P<us>\d{2})-ca-(?P<n>\d{2}))"></a>'
    r"US-(?P<us_rotulo>\d{2}) · CA-(?P<n_rotulo>\d{2}) · (?P<titulo>.+) \((?P<tipo>[^()]+)\)$"
)
PARTE_CA = re.compile(r"^- \*\*(?P<parte>Dado|Quando|Então)\*\* (?P<texto>.+)$")
CAMPO_CA = re.compile(r"^- \*\*(?P<campo>Origem|RF|TA|Depende de|Implementação):\*\* (?P<texto>.+)$")
LINHA_TA = re.compile(
    r'^\|\s*<a id="ta-(?P<ancora>\d{2,3})"></a>TA-(?P<numero>\d{2,3})\s*\|\s*\[CA-(?P<ca>\d{2})\]\((?P<alvo>[^)]*)\)'
    r"\s*\|\s*(?P<tipo>automatizado|manual|pendente)\s*\|\s*(?P<testes>.+?)\s*\|\s*$"
)
LINK_UC = re.compile(r"\]\(\.\./casos-de-uso/(?P<arquivo>[\w.-]+\.md)#(?P<ancora>[\w-]+)\)")
LINK_RF = re.compile(r"\[(?P<rf>RF-[\d.]+)\]\(\.\./requisitos/(?P<arquivo>rf-[\w-]+\.md)#(?P<ancora>rf-[\w-]+)\)")
LINK_TA = re.compile(r"\[TA-(?P<numero>\d{2,3})\]\(#ta-(?P<ancora>\d{2,3})\)")
LINK_CA = re.compile(r"\((?:\.\./historias/)?(?P<arquivo>US-\d{2}-[\w-]+\.md)#(?P<ancora>us-\d{2}-ca-\d{2})\)")
TESTE_PYTEST = re.compile(r"`(?P<arquivo>(?:\w+/)+test_\w+\.py)::(?P<nome>\w+)(?: \[[^\]`]*\])?`")
TESTE_VITEST = re.compile(r"`(?P<arquivo>(?:\w+/)*\w+\.test\.tsx?)`:\s*`(?P<descricao>[^`]+)`")


@dataclass
class CriterioDeAceite:
    ancora: str
    historia: str
    numero: int
    titulo: str
    tipo: str
    linha: int
    partes: dict[str, str] = field(default_factory=dict)
    campos: dict[str, str] = field(default_factory=dict)

    @property
    def referencia(self) -> str:
        return f"{self.historia} · CA-{self.numero:02d}"

    def rfs(self) -> list[str]:
        return [a["rf"] for a in LINK_RF.finditer(self.campos.get("RF", ""))]

    def origens(self) -> list[tuple[str, str]]:
        return [(a["arquivo"], a["ancora"]) for a in LINK_UC.finditer(self.campos.get("Origem", ""))]


@dataclass
class TesteDeAceite:
    numero: int
    ca: str
    alvo: str
    tipo: str
    testes: str
    linha: int


@dataclass
class Historia:
    arquivo: Path
    id: str
    numero: int
    card: dict[str, str] = field(default_factory=dict)
    invest: dict[str, tuple[str, str]] = field(default_factory=dict)
    criterios: list[CriterioDeAceite] = field(default_factory=list)
    testes: list[TesteDeAceite] = field(default_factory=list)

    @property
    def titulo(self) -> str:
        return self.card.get("Título", "")


def _secao(texto: str, titulo: str) -> list[str]:
    achado = re.search(rf"^## {re.escape(titulo)}\s*$(.*?)(?=^## |\Z)", texto, flags=re.M | re.S)
    return achado.group(1).splitlines() if achado else []


def ler_historia(arquivo: Path) -> Historia:
    numero = int(ARQUIVO_US.match(arquivo.name)[1])
    historia = Historia(arquivo=arquivo, id=f"US-{numero:02d}", numero=numero)
    texto = ler(arquivo)
    for linha in _secao(texto, "Index Card"):
        if campo := CAMPO.match(linha):
            historia.card[campo["campo"].strip()] = campo["valor"]
    for linha in _secao(texto, "INVEST"):
        if letra := INVEST.match(linha):
            historia.invest[letra["letra"]] = (letra["atende"], letra["justificativa"])
    atual = None
    for numero_linha, linha in enumerate(texto.splitlines(), start=1):
        if cabecalho := CABECALHO_CA.match(linha):
            atual = CriterioDeAceite(
                ancora=cabecalho["ancora"],
                historia=f"US-{cabecalho['us_rotulo']}",
                numero=int(cabecalho["n_rotulo"]),
                titulo=cabecalho["titulo"],
                tipo=cabecalho["tipo"],
                linha=numero_linha,
            )
            if cabecalho["us"] != cabecalho["us_rotulo"] or cabecalho["n"] != cabecalho["n_rotulo"]:
                atual.campos["_erro"] = f"âncora {cabecalho['ancora']} não bate com o rótulo"
            historia.criterios.append(atual)
            continue
        if linha.startswith("#"):
            atual = None
        if atual is None:
            if ta := LINHA_TA.match(linha):
                historia.testes.append(
                    TesteDeAceite(
                        numero=int(ta["numero"]),
                        ca=f"CA-{ta['ca']}",
                        alvo=ta["alvo"],
                        tipo=ta["tipo"],
                        testes=ta["testes"],
                        linha=numero_linha,
                    )
                )
                if ta["ancora"] != ta["numero"]:
                    historia.testes[-1].tipo = "_erro"
            continue
        if parte := PARTE_CA.match(linha):
            atual.partes[parte["parte"]] = parte["texto"]
        elif campo := CAMPO_CA.match(linha):
            atual.campos[campo["campo"]] = campo["texto"]
    return historia


def ler_historias() -> list[Historia]:
    arquivos = sorted(a for a in PASTA_US.glob("US-*.md") if ARQUIVO_US.match(a.name))
    return [ler_historia(arquivo) for arquivo in arquivos]


def todos_os_criterios(historias: list[Historia]) -> list[CriterioDeAceite]:
    return [ca for historia in historias for ca in historia.criterios]


def _onde(historia: Historia, linha: int | None = None) -> str:
    return f"{relativo(historia.arquivo)}" + (f":{linha}" if linha else "")


def verificar_cards_e_invest(historias: list[Historia]) -> list[str]:
    erros = []
    for historia in historias:
        faltam = [c for c in CAMPOS_DO_CARD if not historia.card.get(c)]
        if faltam:
            erros.append(f"{historia.id}: Index Card sem {', '.join(faltam)}")
        if historia.card.get("ID") != historia.id:
            erros.append(f"{historia.id}: campo ID {historia.card.get('ID')!r} ≠ nome do arquivo")
        if not re.match(r"^Como .+, quero .+ para .+\.$", historia.card.get("História", "")):
            erros.append(f"{historia.id}: História fora do formato 'Como …, quero … para ….'")
        if not re.match(r"^\d+(,\d+)? ", historia.card.get("Estimativa (Custo em Semanas)", "")):
            erros.append(f"{historia.id}: Estimativa sem o número de semanas no começo")
        for letra in LETRAS_INVEST:
            atende, justificativa = historia.invest.get(letra, ("", ""))
            if atende not in ("✓", "✗"):
                erros.append(f"{historia.id}: INVEST {letra} sem ✓ ou ✗ ({atende!r})")
            if len(justificativa) < 20:
                erros.append(f"{historia.id}: INVEST {letra} sem justificativa")
        tipos = Counter(ca.tipo for ca in historia.criterios)
        if not tipos["sucesso"]:
            erros.append(f"{historia.id}: nenhum CA de sucesso")
        if not tipos["exceção"]:
            erros.append(f"{historia.id}: nenhum CA de exceção")
        marcas = "".join("✓" if historia.invest.get(l, ("",))[0] == "✓" else "✗" for l in LETRAS_INVEST)
        print(f"{historia.id}: INVEST {marcas} ({''.join(LETRAS_INVEST)}); {len(historia.criterios)} CAs")
    return erros


def verificar_criterios(historias: list[Historia]) -> list[str]:
    erros = []
    cache: dict[Path, set[str]] = {}
    rfs_existentes = {f["id"]: f for f in fichas_de_rf()}
    for historia in historias:
        tas = {ta.numero: ta for ta in historia.testes}
        ordem = [TIPOS_DE_CA.index(ca.tipo) if ca.tipo in TIPOS_DE_CA else -1 for ca in historia.criterios]
        if ordem != sorted(ordem):
            erros.append(f"{historia.id}: CAs fora da ordem sucesso → alternativa → exceção → registro → acesso")
        for ca in historia.criterios:
            onde = f"{ca.referencia} ({_onde(historia, ca.linha)})"
            if "_erro" in ca.campos:
                erros.append(f"{onde}: {ca.campos['_erro']}")
            if ca.historia != historia.id:
                erros.append(f"{onde}: CA de outra história no arquivo")
            if ca.tipo not in TIPOS_DE_CA:
                erros.append(f"{onde}: tipo {ca.tipo!r} fora de {TIPOS_DE_CA}")
            faltam = [p for p in ("Dado", "Quando", "Então") if not ca.partes.get(p)]
            if faltam:
                erros.append(f"{onde}: sem {', '.join(faltam)}")
            origens = ca.origens()
            if not origens:
                erros.append(f"{onde}: Origem sem link para uma ficha de caso de uso")
            for arquivo, ancora in origens:
                destino = PASTA_UC / arquivo
                if not destino.exists() or ancora not in _ancoras_de(destino, cache):
                    erros.append(f"{onde}: Origem aponta para {arquivo}#{ancora}, que não existe")
            if not ca.rfs():
                erros.append(f"{onde}: sem RF")
            for achado in LINK_RF.finditer(ca.campos.get("RF", "")):
                ficha = rfs_existentes.get(achado["rf"])
                if ficha is None or ficha["arquivo"].name != achado["arquivo"]:
                    erros.append(f"{onde}: {achado['rf']} não existe em {achado['arquivo']}")
            ligados = [int(a["numero"]) for a in LINK_TA.finditer(ca.campos.get("TA", ""))]
            if len(ligados) != 1:
                erros.append(f"{onde}: esperado um TA, encontrados {len(ligados)}")
            for numero in ligados:
                ta = tas.get(numero)
                if ta is None:
                    erros.append(f"{onde}: TA-{numero:02d} não está na tabela da história")
                elif ta.alvo != f"#{ca.ancora}" or ta.ca != f"CA-{ca.numero:02d}":
                    erros.append(f"{onde}: TA-{numero:02d} aponta para {ta.ca} {ta.alvo}")
                else:
                    erros += verificar_pendencia(ca, ta, onde)
    print(f"CAs lidos: {len(todos_os_criterios(historias))}")
    return erros


def verificar_pendencia(ca: CriterioDeAceite, ta: TesteDeAceite, onde: str) -> list[str]:
    erros = []
    marca_do_ca = MARCA_PENDENTE.match(ca.campos.get("Implementação", ""))
    marca_do_ta = MARCA_PENDENTE.match(ta.testes) if ta.tipo == "pendente" else None
    if "Implementação" in ca.campos:
        if marca_do_ca is None or marca_do_ca["resto"]:
            erros.append(f"{onde}: Implementação deve ser exatamente 'implementação pendente (tarefa X)'")
        elif marca_do_ca["tarefa"] not in TAREFAS_DE_CODIGO:
            erros.append(f"{onde}: tarefa {marca_do_ca['tarefa']} fora de {TAREFAS_DE_CODIGO}")
        if ta.tipo != "pendente":
            erros.append(f"{onde}: CA com implementação pendente, mas TA-{ta.numero:02d} é {ta.tipo}")
    elif ta.tipo == "pendente":
        erros.append(f"{onde}: TA-{ta.numero:02d} é pendente, mas o CA não tem o campo Implementação")
    if ta.tipo == "pendente":
        if marca_do_ta is None:
            erros.append(f"{onde}: TA pendente deve começar com 'implementação pendente (tarefa X)'")
        elif marca_do_ca and marca_do_ta["tarefa"] != marca_do_ca["tarefa"]:
            erros.append(f"{onde}: o CA aponta para {marca_do_ca['tarefa']}, o TA para {marca_do_ta['tarefa']}")
        if TESTE_PYTEST.search(ta.testes) or TESTE_VITEST.search(ta.testes) or re.search(r"test_\w+|\.test\.tsx?", ta.testes):
            erros.append(f"{onde}: TA pendente não pode citar teste de código (os testes de hoje verificam a regra antiga)")
    return erros


def itens_das_fichas() -> list[tuple[str, str, str]]:
    itens = []
    for nome in FICHAS_COMPLETAS:
        for linha in ler(PASTA_UC / nome).splitlines():
            if item := ITEM_COMPLETO.match(linha):
                itens.append((nome, f"{item[1]}{item[2]}-{item[3]}", f"{item[4]}{item[5]}.{item[6]}"))
    for ancora, rotulo in re.findall(r'<a id="(uc\d{2}-[ae]\d+-\d+)"></a>\**([AE]\d+\.\d+)', ler(RESUMIDAS)):
        itens.append((RESUMIDAS.name, ancora, rotulo))
    return itens


def linhas_da_cobertura() -> dict[tuple[str, str], str]:
    linhas = {}
    for linha in _secao(ler(README_US), "Cobertura UC → US/CA"):
        if not linha.startswith("| ["):
            continue
        if achado := LINK_UC.search(linha):
            linhas[(achado["arquivo"], achado["ancora"])] = linha
    return linhas


def verificar_cobertura(historias: list[Historia]) -> list[str]:
    erros = []
    ancoras_de_ca = {ca.ancora: ca for ca in todos_os_criterios(historias)}
    linhas = linhas_da_cobertura()
    itens = itens_das_fichas()
    com_ca = sem_ca = 0
    for arquivo, ancora, rotulo in itens:
        linha = linhas.get((arquivo, ancora))
        if linha is None:
            erros.append(f"{arquivo} {rotulo} (#{ancora}) não aparece em 'Cobertura UC → US/CA'")
            continue
        celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
        cas = [a["ancora"] for a in LINK_CA.finditer(celulas[2] if len(celulas) > 2 else "")]
        if cas:
            com_ca += 1
            for ca in cas:
                if ca not in ancoras_de_ca:
                    erros.append(f"{arquivo} {rotulo}: cita #{ca}, que não existe")
                elif (arquivo, ancora) not in ancoras_de_ca[ca].origens():
                    erros.append(f"{arquivo} {rotulo}: {ancoras_de_ca[ca].referencia} não tem este item na Origem")
        elif "sem CA" in celulas[2] and len(celulas) > 3 and len(celulas[3]) > 10:
            sem_ca += 1
        else:
            erros.append(f"{arquivo} {rotulo}: sem CA e sem o motivo")
    for chave in sorted(set(linhas) - {(a, b) for a, b, _ in itens}):
        erros.append(f"'Cobertura UC → US/CA' cita {chave[0]}#{chave[1]}, que não é alternativa nem exceção")
    for ca in todos_os_criterios(historias):
        for origem in ca.origens():
            if origem in {(a, b) for a, b, _ in itens} and origem not in linhas:
                erros.append(f"{ca.referencia}: a Origem {origem[0]}#{origem[1]} falta na cobertura")
    print(f"Alternativas e exceções nas fichas: {len(itens)}; com CA: {com_ca}; sem CA (com motivo): {sem_ca}")
    return erros


def _cas_citados(texto: str) -> set[str]:
    return {a["ancora"] for a in LINK_CA.finditer(texto)}


def verificar_rf(historias: list[Historia]) -> list[str]:
    erros = []
    por_rf: dict[str, set[str]] = {}
    for ca in todos_os_criterios(historias):
        for rf in ca.rfs():
            por_rf.setdefault(rf, set()).add(ca.ancora)
    fichas = fichas_de_rf()
    for ficha in fichas:
        rf = ficha["id"]
        esperados = por_rf.get(rf, set())
        origem = f"{rf} ({relativo(ficha['arquivo'])}:{ficha['linha']})"
        vinculo = ficha["campos"].get("Vínculos", "")
        if rf in RF_SEM_HISTORIA:
            if esperados:
                erros.append(f"{origem}: marcado como sem história, mas citado por {sorted(esperados)}")
            if "transversal" not in vinculo.split("US")[-1]:
                erros.append(f"{origem}: Vínculos não justifica a ausência de US")
            continue
        if not esperados:
            erros.append(f"{origem}: nenhum CA cita este RF")
        if "a definir (REQ-05)" in vinculo:
            erros.append(f"{origem}: Vínculos ainda diz 'a definir (REQ-05)'")
        if _cas_citados(vinculo) != esperados:
            erros.append(f"{origem}: Vínculos cita {sorted(_cas_citados(vinculo))}, os CAs citam {sorted(esperados)}")
    ativos = len(fichas) - len(RF_SEM_HISTORIA)
    cobertos = sum(1 for f in fichas if f["id"] in por_rf)
    print(f"RF nas fichas: {len(fichas)}; citados por CA: {cobertos} de {ativos}; justificados: {sorted(RF_SEM_HISTORIA)}")
    return erros


def testes_citados(historias: list[Historia]) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    pytest, vitest = [], []
    for historia in historias:
        for ta in historia.testes:
            pytest += [(a["arquivo"], a["nome"]) for a in TESTE_PYTEST.finditer(ta.testes)]
            vitest += [(a["arquivo"], a["descricao"]) for a in TESTE_VITEST.finditer(ta.testes)]
    return list(dict.fromkeys(pytest)), list(dict.fromkeys(vitest))


def verificar_testes(historias: list[Historia]) -> list[str]:
    erros = []
    cache: dict[Path, str] = {}

    def conteudo(caminho: Path) -> str:
        if caminho not in cache:
            cache[caminho] = ler(caminho)
        return cache[caminho]

    for historia in historias:
        for ta in historia.testes:
            onde = f"TA-{ta.numero:02d} ({_onde(historia, ta.linha)})"
            if ta.tipo == "_erro":
                erros.append(f"{onde}: âncora não bate com o número")
            achados = list(TESTE_PYTEST.finditer(ta.testes)) + list(TESTE_VITEST.finditer(ta.testes))
            if ta.tipo == "automatizado" and not achados:
                erros.append(f"{onde}: automatizado sem nenhum teste citado")
            if ta.tipo == "manual" and not all(p in ta.testes for p in ("Precondição", "Passos", "Resultado esperado")):
                erros.append(f"{onde}: roteiro manual sem precondição, passos e resultado esperado")
    pytest, vitest = testes_citados(historias)
    for arquivo, nome in pytest:
        caminho = BACKEND / arquivo
        if not caminho.exists():
            erros.append(f"pytest: arquivo inexistente src/backend/{arquivo}")
        elif not re.search(rf"^\s*(?:def|class)\s+{nome}\b|^{nome}\s*=", conteudo(caminho), flags=re.M):
            erros.append(f"pytest: {arquivo}::{nome} não existe")
    for arquivo, descricao in vitest:
        caminho = FRONTEND / arquivo
        if not caminho.exists():
            erros.append(f"Vitest: arquivo inexistente src/frontend/src/{arquivo}")
        elif not any(f"{aspa}{descricao}{aspa}" in conteudo(caminho) for aspa in ("'", '"', "`")):
            erros.append(f"Vitest: {arquivo} não tem it/test {descricao!r}")
    print(f"Testes citados: {len(pytest)} pytest (em {len({a for a, _ in pytest})} arquivos), "
          f"{len(vitest)} Vitest (em {len({a for a, _ in vitest})} arquivos)")
    return erros


def verificar_ids(historias: list[Historia]) -> list[str]:
    erros = []
    numeros = [h.numero for h in historias]
    if numeros != list(range(1, len(numeros) + 1)):
        erros.append(f"US fora da sequência 1..{len(numeros)}: {numeros}")
    ancoras = Counter(ca.ancora for ca in todos_os_criterios(historias))
    erros += [f"CA repetido: {a}" for a, n in ancoras.items() if n > 1]
    for historia in historias:
        sequencia = [ca.numero for ca in historia.criterios]
        if sequencia != list(range(1, len(sequencia) + 1)):
            erros.append(f"{historia.id}: CAs fora da sequência: {sequencia}")
    tas = [ta.numero for historia in historias for ta in historia.testes]
    if tas != list(range(1, len(tas) + 1)):
        faltam = sorted(set(range(1, max(tas, default=0) + 1)) - set(tas))
        erros.append(f"TAs fora da sequência (repetidos ou buracos {faltam})")
    total_ca = len(todos_os_criterios(historias))
    if len(tas) != total_ca:
        erros.append(f"{len(tas)} TAs para {total_ca} CAs (esperado: um TA por CA)")
    print(f"US: {len(historias)}; CA: {total_ca}; TA: {len(tas)} (TA-01 a TA-{max(tas, default=0):02d})")
    return erros


def verificar_readme(historias: list[Historia]) -> list[str]:
    erros = []
    texto = ler(README_US)
    indice = _secao(texto, "Índice das histórias")
    for historia in historias:
        linha = next((l for l in indice if f"]({historia.arquivo.name})" in l), None)
        if linha is None:
            erros.append(f"{historia.id}: não está no índice das histórias")
            continue
        celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
        if str(len(historia.criterios)) not in celulas:
            erros.append(f"{historia.id}: o índice não traz o número de CAs ({len(historia.criterios)})")
    no_readme = {}
    for linha in _secao(texto, "Índice dos testes de aceite"):
        if achado := re.match(
            r"^\|\s*\[TA-(\d{2,3})\]\((US-\d{2}-[\w-]+\.md)#ta-\d{2,3}\)\s*\|\s*\[US-\d{2} · CA-(\d{2})\]"
            r"\((US-\d{2}-[\w-]+\.md)#(us-\d{2}-ca-\d{2})\)\s*\|\s*(automatizado|manual|pendente)\s*\|\s*(.+?)\s*\|\s*$",
            linha,
        ):
            no_readme[int(achado[1])] = (achado[2], achado[5], achado[6], achado[7])
    for historia in historias:
        for ta in historia.testes:
            esperado = (historia.arquivo.name, ta.alvo.lstrip("#"), ta.tipo, ta.testes)
            if no_readme.get(ta.numero) != esperado:
                erros.append(f"TA-{ta.numero:02d}: o índice do README difere da tabela de {historia.id}")
    total = sum(len(h.testes) for h in historias)
    if len(no_readme) != total:
        erros.append(f"o índice dos TAs do README tem {len(no_readme)} linhas, as histórias têm {total} TAs")
    print(f"Índice das histórias: {len(historias)} conferidas; índice dos TAs: {len(no_readme)} linhas")
    return erros


def verificar_linguagem(historias: list[Historia]) -> list[str]:
    erros = []
    lidas = 0
    for historia in historias:
        for ca in historia.criterios:
            for parte, texto in ca.partes.items():
                lidas += 1
                for termo, padrao in TERMOS_PROIBIDOS.items():
                    if re.search(padrao, texto, flags=re.I):
                        erros.append(f"{ca.referencia} ({parte}): termo {termo!r}")
    print(f"Partes Dado/Quando/Então lidas: {lidas}; termos procurados: {', '.join(TERMOS_PROIBIDOS)}")
    return erros


def imprimir_contagens(historias: list[Historia]) -> None:
    print(f"{'US':6} {'suc':>4} {'alt':>4} {'exc':>4} {'reg':>4} {'ace':>4} {'CAs':>4} {'TA aut':>7} {'TA man':>7} {'TA pen':>7}")
    totais = Counter()
    for historia in historias:
        tipos = Counter(ca.tipo for ca in historia.criterios)
        tas = Counter(ta.tipo for ta in historia.testes)
        valores = [tipos[t] for t in TIPOS_DE_CA] + [
            len(historia.criterios),
            tas["automatizado"],
            tas["manual"],
            tas["pendente"],
        ]
        totais.update(dict(zip(range(len(valores)), valores)))
        print(f"{historia.id:6} " + " ".join(f"{v:>4}" for v in valores[:6]) + f" {valores[6]:>7} {valores[7]:>7} {valores[8]:>7}")
    print(f"{'Total':6} " + " ".join(f"{totais[i]:>4}" for i in range(6)) + f" {totais[6]:>7} {totais[7]:>7} {totais[8]:>7}")


def imprimir_selecao_de_testes(historias: list[Historia]) -> None:
    pytest, vitest = testes_citados(historias)
    print("# pytest (a partir de src/backend/):")
    print(" ".join(f"{arquivo}::{nome}" for arquivo, nome in pytest))
    print("# Vitest (a partir de src/frontend/src/, arquivos):")
    print(" ".join(f"src/{arquivo}" for arquivo in dict.fromkeys(a for a, _ in vitest)))


def main() -> int:
    historias = ler_historias()
    if "--testes" in sys.argv:
        imprimir_selecao_de_testes(historias)
        return 0
    verificacoes = [
        ("1. Index Card, INVEST e tipos de CA", lambda: verificar_cards_e_invest(historias)),
        ("2. CAs: Dado/Quando/Então, Origem, RF e TA", lambda: verificar_criterios(historias)),
        ("3. Cobertura UC → US/CA (alternativas e exceções das fichas)", lambda: verificar_cobertura(historias)),
        ("4. RF → US/CA: fichas rf-*.md (a SRS 6.4 virou a matriz gerada, REQ-06)", lambda: verificar_rf(historias)),
        ("5. Testes citados nos TAs existem", lambda: verificar_testes(historias)),
        ("6. IDs de US, CA e TA", lambda: verificar_ids(historias)),
        ("7. README: índice das histórias e dos TAs", lambda: verificar_readme(historias)),
        ("8. Linguagem dos Dado/Quando/Então", lambda: verificar_linguagem(historias)),
    ]
    print("== Contagens ==")
    imprimir_contagens(historias)
    falhou = False
    for titulo, verificar in verificacoes:
        print(f"\n== {titulo} ==")
        erros = verificar()
        for erro in erros:
            print(f"  ERRO: {erro}")
        print("  OK" if not erros else f"  FALHOU ({len(erros)})")
        falhou = falhou or bool(erros)
    return 1 if falhou else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
