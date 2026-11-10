from __future__ import annotations

import ast
import hashlib
import posixpath
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verificar_casos_de_uso import tabela_rf_uc, uc_principal  # noqa: E402
from verificar_historias import BACKEND, FRONTEND, ler_historias, todos_os_criterios  # noqa: E402
from verificar_requisitos import PASTA, RAIZ, fichas_de_rf, fichas_de_rnf, ler, necessidades_da_visao, necessidades_fora_do_1_0  # noqa: E402

PASTA_RAS = PASTA / "rastreabilidade"
SRS = PASTA / "requisitos" / "srs.md"
MATRIZ_DE_ACESSO = RAIZ / "docs" / "fontes" / "matriz_de_acesso.md"
APP_TSX = FRONTEND / "App.tsx"
URLS_DO_CONFIG = BACKEND / "config" / "urls.py"
PASTA_DEC = PASTA / "decisoes"
PAUTA = PASTA_DEC / "pauta-aula-7.md"
CANDIDATA = PASTA / "baselines" / "conecta-campus-1.0-candidata.md"
README_RAS = PASTA_RAS / "README.md"
CATALOGO_RN = PASTA / "requisitos" / "regras-de-negocio.md"

AVISO = (
    "> Gerado por `scripts/gerar_rastreabilidade.py`, não edite à mão; para mudar um vínculo, "
    "mude a ficha de origem."
)
JUSTIFICADOS = {
    "RF-38": "transversal, o resultado de cada operação aparece no Então de todos os CAs e em todas as rotas "
    "([decisão a da REQ-05](../historias/README.md#decisao-a))"
}
ORDEM_DE_IMPACTO = ["DEC-13", "DEC-05", "DEC-07"]
ARTEFATO_DO_PUML = {
    "diagrama-casos-de-uso.puml": ("Diagrama do negócio (fonte PlantUML)", "UCD-01"),
    "diagrama-administracao.puml": ("Diagrama de apoio (fonte PlantUML)", "UCD-02"),
    "fluxo-solicitar-reserva.puml": ("Fluxo de decisão de UC-04 (fonte PlantUML)", "Parte de UC-04"),
}
NOMES_DAS_FUNCIONALIDADES = {
    "F1": "Cadastrar e listar os espaços",
    "F2": "Cadastrar a solicitação",
    "F3": "Consultar por dois ou mais critérios",
    "F4": "Alterar a situação",
    "F5": "Impedir operações inválidas",
    "F6": "Mensagens de sucesso e erro",
    "Extra": "Além das seis",
}

ID_RF = re.compile(r"RF-\d{2}(?:\.\d+)?")
ID_NS = re.compile(r"NS-\d{2}")
ID_DEC = re.compile(r"DEC-\d{2}")
ID_RN = re.compile(r"RN-\d{2}")
LINHA_RN = re.compile(r'^\|\s*<a id="rn-\d{2}"></a>(?P<id>RN-\d{2})\s*\|(?P<celulas>.*)\|\s*$')
ID_US = re.compile(r"US-\d{2}")
FAIXA_RF = re.compile(r"(RF-\d{2}(?:\.\d+)?) a (RF-\d{2}(?:\.\d+)?)")
ID_RNF = re.compile(r"RNF-[FURPS]\d{2}")
FAIXA_RNF = re.compile(r"(RNF-[FURPS]\d{2}) a (RNF-[FURPS]\d{2})")
CAMPO = re.compile(r"^\|\s*\*\*(?P<campo>[^*]+)\*\*\s*\|\s*(?P<valor>.*?)\s*\|\s*$")
ROTA_API = re.compile(r"\b(GET|POST|PATCH|PUT|DELETE) (/api/[^\s`?]*)")
TRECHO = re.compile(r"`([^`]+)`")
COMANDO = re.compile(r"python manage\.py (\w+)")
SIMBOLO = re.compile(r"`(?P<arquivo>[\w./-]+\.(?:py|tsx?))::(?P<simbolo>[\w.]+)`")
TESTE = re.compile(r"`(?P<arquivo>(?:\w+/)+test_\w+\.py)?::(?P<nome>\w+)(?: \[[^\]`]*\])?`")
CABECALHO_DOC = re.compile(r"^\|\s*\*\*(?P<id>[^*]+?) • (?P<versao>\d+\.\d+) • (?P<estado>[^*]+?)\*\*")
LINK_MD = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)\)")


def normalizar(texto: str) -> str:
    return texto.replace("\r\n", "\n")


def chave(identificador: str) -> tuple:
    return tuple(int(n) for n in re.findall(r"\d+", identificador))


def ordenar(ids) -> list[str]:
    return sorted(set(ids), key=lambda i: (re.sub(r"[\d.-]+$", "", i), chave(i)))


def expandir(texto: str, todos: list[str], padrao=ID_RF, faixa=FAIXA_RF) -> list[str]:
    encontrados = set(padrao.findall(texto))
    for inicio, fim in faixa.findall(texto):
        encontrados |= {i for i in todos if chave(inicio) <= chave(i) <= chave(fim)}
    return ordenar(i for i in encontrados if i in todos)


def ancora_rf(rf: str) -> str:
    return rf.lower().replace(".", "-")


def sha8(caminho: Path) -> str:
    return hashlib.sha256(normalizar(ler(caminho)).encode("utf-8")).hexdigest()[:8]


def campos_da_tabela(texto: str) -> dict[str, str]:
    return {a["campo"].strip(): a["valor"] for linha in texto.splitlines() if (a := CAMPO.match(linha))}


def secao(texto: str, titulo_regex: str) -> str:
    achado = re.search(rf"^(#{{2,3}}) {titulo_regex}.*?$(.*?)(?=^#{{2,3}} |\Z)", texto, flags=re.M | re.S)
    return achado.group(2) if achado else ""


def relinkar(texto: str, pasta_origem: str) -> str:
    def troca(achado: re.Match) -> str:
        rotulo, alvo = achado.groups()
        if re.match(r"^[a-z]+:", alvo):
            return achado.group(0)
        caminho, _, ancora = alvo.partition("#")
        if not caminho:
            return achado.group(0)
        novo = posixpath.relpath(posixpath.normpath(posixpath.join(pasta_origem, caminho)), "rastreabilidade")
        return f"[{rotulo}]({novo}{'#' + ancora if ancora else ''})"

    return LINK_MD.sub(troca, texto)


def sem_links(texto: str) -> str:
    return re.sub(r"<[^>]+>", "", LINK_MD.sub(lambda a: a.group(1), texto)).replace("`", "")


def testes_do_texto(texto: str) -> list[tuple[str, str]]:
    achados, atual = [], None
    for achado in TESTE.finditer(texto):
        atual = achado["arquivo"] or atual
        if atual:
            achados.append((atual, achado["nome"]))
    return list(dict.fromkeys(achados))


def teste_existe(arquivo: str, nome: str, cache: dict[Path, str]) -> bool:
    caminho = BACKEND / arquivo
    if not caminho.exists():
        return False
    if caminho not in cache:
        cache[caminho] = ler(caminho)
    return bool(re.search(rf"^\s*(?:def|class)\s+{nome}\b|^{nome}\s*=", cache[caminho], flags=re.M))


@dataclass
class Rota:
    tipo: str  # api | tela | comando
    chave: str  # "GET /api/espacos/" | "/espacos" | "carregar_dados_exemplo"
    nome: str = ""  # nome da rota da API, componente da página
    linha: dict = field(default_factory=dict)


def rotas_da_api() -> list[Rota]:
    rotas = []
    for linha in ler(MATRIZ_DE_ACESSO).splitlines():
        celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
        if len(celulas) != 8 or not celulas[0].startswith("`"):
            continue
        caminho = celulas[1].strip("`").split("?")[0]
        rotas.append(
            Rota(
                "api",
                f"{celulas[2]} {caminho}",
                celulas[0].strip("`"),
                dict(zip(("anonimo", "dono", "outro", "gestor"), celulas[4:]), corpo=celulas[3]),
            )
        )
    return rotas


def paginas_do_frontend() -> list[Rota]:
    paginas = []
    for achado in re.finditer(r"<Route (index|path=\"([^\"]+)\") element=\{<(\w+) />\}", ler(APP_TSX)):
        caminho = "/" if achado[1] == "index" else ("*" if achado[2] == "*" else "/" + achado[2])
        paginas.append(Rota("tela", caminho, achado[3]))
    if 'path("admin/"' in ler(URLS_DO_CONFIG):
        paginas.append(Rota("tela", "/admin/", "Django admin (config/urls.py)"))
    return paginas


@dataclass
class Requisito:
    id: str
    titulo: str
    arquivo: Path
    campos: dict
    f: str = ""
    ns: list[str] = field(default_factory=list)
    pai: str | None = None
    uc: str | None = None
    como_entra: str = ""
    decs: list[str] = field(default_factory=list)
    rns: list[str] = field(default_factory=list)
    cas: list = field(default_factory=list)
    rotas: list[str] = field(default_factory=list)
    protegidas: list[str] = field(default_factory=list)
    rotas_herdadas: str = ""
    codigo: list[tuple[str, str]] = field(default_factory=list)
    lacunas: list[str] = field(default_factory=list)

    @property
    def link(self) -> str:
        return f"../requisitos/{self.arquivo.name}#{ancora_rf(self.id)}"


def tabela_resumo() -> dict[str, tuple[str, str]]:
    linhas = {}
    padrao = re.compile(r"^\| \[(RF-[\d.]+)\]\([^)]*\) \| ([^|]+?) \| (NS-\d{2}) \| ([^|]+?) \|")
    for linha in ler(SRS).splitlines():
        if achado := padrao.match(linha):
            linhas[achado[1]] = (achado[2], achado[4])
    return linhas


def lacunas_da_srs(todos: list[str]) -> dict[str, dict]:
    lacunas = {}
    for linha in ler(SRS).splitlines():
        if achado := re.match(r'^\|\s*<a id="(l-\d{2})"></a>(L-\d{2})\s*\|', linha):
            celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
            lacunas[achado[2]] = {
                "ancora": achado[1],
                "tipo": celulas[1],
                "texto": celulas[2],
                "afeta": celulas[3],
                "proposta": celulas[4],
                "rfs": expandir(celulas[3], todos),
            }
    return lacunas


def rotas_do_texto(texto: str, conhecidas: set[str]) -> tuple[list[str], list[str]]:
    rotas, desconhecidas = [], []
    for metodo, caminho in ROTA_API.findall(texto):
        (rotas if f"{metodo} {caminho}" in conhecidas else desconhecidas).append(f"{metodo} {caminho}")
    for trecho in TRECHO.findall(texto):
        trecho = trecho.split("?")[0]
        if trecho.startswith("/") and not trecho.startswith("/api/") and re.fullmatch(r"/[\w/:.-]*", trecho):
            (rotas if trecho in conhecidas else desconhecidas).append(trecho)
    rotas += [f"comando {c}" for c in COMANDO.findall(texto)]
    return list(dict.fromkeys(rotas)), desconhecidas


@dataclass
class Modelo:
    rfs: dict[str, Requisito]
    ordem: list[str]
    historias: list
    criterios: list
    rotas: list[Rota]
    lacunas: dict[str, dict]
    decs: dict[str, dict]
    rns: dict[str, dict]
    rnfs: list[dict]
    ns: list[str]
    rotas_desconhecidas: list[str]
    ras: tuple[str, str]


def _estado_da_decisao(texto: str) -> str:
    achado = re.match(r"(Decidida|Adotada provisoriamente|Pendente|Substituída)", texto)
    return achado.group(1) if achado else texto


def ler_decs() -> dict[str, dict]:
    decs = {}
    for arquivo in sorted(PASTA_DEC.glob("DEC-*.md")):
        texto = ler(arquivo)
        campos = campos_da_tabela(texto)
        titulo = re.search(r"^# (DEC-\d{2}) — (.+)$", texto, flags=re.M)
        decs[titulo[1]] = {
            "titulo": titulo[2].strip(),
            "arquivo": arquivo,
            "campos": campos,
            "estado": _estado_da_decisao(campos.get("Estado da decisão", "")),
            "historico": bool(re.search(r"^## Histórico", texto, flags=re.M)),
        }
    return decs


def ler_rns() -> dict[str, dict]:
    rns: dict[str, dict] = {}
    if not CATALOGO_RN.exists():
        return rns
    for linha in ler(CATALOGO_RN).splitlines():
        achado = LINHA_RN.match(linha)
        if not achado:
            continue
        celulas = [c.strip() for c in achado["celulas"].split("|")]
        regra, fonte, rfs, excecao, vigencia = (celulas + [""] * 5)[:5]
        rns[achado["id"]] = {
            "regra": regra,
            "fonte": fonte,
            "rfs": ordenar(ID_RF.findall(sem_links(rfs))),
            "excecao": excecao,
            "vigencia": vigencia,
        }
    return rns


def ler_cabecalho(caminho: Path) -> tuple[str, str, str] | None:
    for linha in ler(caminho).splitlines()[:12]:
        if achado := CABECALHO_DOC.match(linha):
            return sem_links(achado["id"]).strip(), achado["versao"], achado["estado"].strip()
    return None


def carregar() -> Modelo:
    resumo = tabela_resumo()
    fichas = fichas_de_rf()
    ordem = ordenar(f["id"] for f in fichas)
    rotas = rotas_da_api() + paginas_do_frontend()
    conhecidas = {r.chave for r in rotas}
    rf_uc = tabela_rf_uc()
    rfs: dict[str, Requisito] = {}
    desconhecidas = []
    for ficha in fichas:
        campos = ficha["campos"]
        titulo, f = resumo.get(ficha["id"], ("?", "?"))
        requisito = Requisito(ficha["id"], titulo, ficha["arquivo"], campos, f=f)
        requisito.ns = list(dict.fromkeys(ID_NS.findall(campos.get("Origem", ""))))
        pai = ID_RF.search(campos.get("Pai", ""))
        requisito.pai = pai.group(0) if pai else None
        requisito.protegidas = expandir(campos.get("Operações protegidas", ""), ordem)
        linha_uc = rf_uc.get(ficha["id"], [{}])[0]
        requisito.uc = uc_principal(linha_uc.get("uc", ""))
        requisito.como_entra = linha_uc.get("como", "")
        requisito.decs = ordenar(ID_DEC.findall(campos.get("Decisões", "")))
        requisito.rns = ordenar(ID_RN.findall(campos.get("Regras de negócio", "")))
        requisito.rotas, fora = rotas_do_texto(campos.get("Evidência (complementar)", ""), conhecidas)
        desconhecidas += [f"{ficha['id']}: {r}" for r in fora]
        requisito.codigo = [(a["arquivo"], a["simbolo"]) for a in SIMBOLO.finditer(campos.get("Código (complementar)", ""))]
        rfs[ficha["id"]] = requisito
    for requisito in rfs.values():
        origens = [requisito.pai] if requisito.pai else requisito.protegidas
        if not requisito.rotas and origens:
            requisito.rotas = list(dict.fromkeys(r for o in origens for r in rfs[o].rotas))
            requisito.rotas_herdadas = ", ".join(origens)
    historias = ler_historias()
    criterios = todos_os_criterios(historias)
    for ca in criterios:
        for rf in ca.rfs():
            if rf in rfs:
                rfs[rf].cas.append(ca)
    lacunas = lacunas_da_srs(ordem)
    for identificador, lacuna in lacunas.items():
        for rf in lacuna["rfs"]:
            rfs[rf].lacunas.append(identificador)
    ras = ler_cabecalho(README_RAS) if README_RAS.exists() else None
    return Modelo(
        rfs=rfs,
        ordem=ordem,
        historias=historias,
        criterios=criterios,
        rotas=rotas,
        lacunas=lacunas,
        decs=ler_decs(),
        rns=ler_rns(),
        rnfs=fichas_de_rnf(),
        ns=necessidades_da_visao(),
        rotas_desconhecidas=desconhecidas,
        ras=(ras[1], ras[2]) if ras else ("0.1", "Rascunho"),
    )


def ta_de(ca, historias_por_id) -> object | None:
    historia = historias_por_id[ca.historia]
    numeros = [int(n) for n in re.findall(r"TA-(\d{2,3})", ca.campos.get("TA", ""))]
    return next((ta for ta in historia.testes if ta.numero in numeros), None)


def link_ca(ca, historias_por_id) -> str:
    return f"../historias/{historias_por_id[ca.historia].arquivo.name}#{ca.ancora}"


def link_ta(ta, historia) -> str:
    return f"../historias/{historia.arquivo.name}#ta-{ta.numero:02d}"


def faltas(requisito: Requisito, historias_por_id) -> list[str]:
    faltando = []
    if not requisito.ns:
        faltando.append("NS")
    if requisito.uc is None:
        faltando.append("UC")
    if not requisito.cas:
        faltando += ["US", "CA"]
    elif any(ta_de(ca, historias_por_id) is None for ca in requisito.cas):
        faltando.append("TA")
    if not requisito.rotas:
        faltando.append("endpoint ou tela")
    if not requisito.codigo:
        faltando.append("código")
    return faltando


def situacao(requisito: Requisito, modelo: Modelo, historias_por_id) -> tuple[str, bool]:
    faltando = faltas(requisito, historias_por_id)
    lacunas = ", ".join(
        f"[{lid}](../requisitos/srs.md#{modelo.lacunas[lid]['ancora']})" for lid in requisito.lacunas
    )
    de_ausencia = ", ".join(
        f"[{lid}](../requisitos/srs.md#{modelo.lacunas[lid]['ancora']})"
        for lid in requisito.lacunas
        if " sem " in f" {modelo.lacunas[lid]['tipo']} "
    )
    manuais = [
        f"TA-{ta.numero:02d}"
        for ca in requisito.cas
        if (ta := ta_de(ca, historias_por_id)) and ta.tipo == "manual"
    ]
    pendentes = [
        f"TA-{ta.numero:02d}"
        for ca in requisito.cas
        if (ta := ta_de(ca, historias_por_id)) and ta.tipo == "pendente"
    ]
    if not faltando:
        texto = "completa"
        if manuais:
            texto += f", com TA manual ({', '.join(manuais)})"
        if pendentes:
            texto += f", com TA pendente da tarefa de código ({', '.join(pendentes)})"
        return (texto + (f"; ver {lacunas}" if lacunas else ""), True)
    if requisito.id in JUSTIFICADOS:
        return (f"sem {', '.join(faltando)} — {JUSTIFICADOS[requisito.id]}", True)
    if de_ausencia:
        return (f"falta {', '.join(faltando)}: {de_ausencia}", True)
    return (f"falta {', '.join(faltando)}, sem lacuna que justifique", False)


def como_entra_relinkado(requisito: Requisito) -> str:
    if requisito.uc is None:
        return requisito.como_entra or "—"
    principal = f"[{requisito.uc}](../casos-de-uso/README.md#{requisito.uc.lower()})"
    return f"{principal} · {relinkar(requisito.como_entra, 'casos-de-uso')}"


def agrupar_cas(cas, historias_por_id, com_links=True) -> str:
    grupos: dict[str, list] = {}
    for ca in sorted(cas, key=lambda c: (c.historia, c.numero)):
        grupos.setdefault(ca.historia, []).append(ca)
    partes = []
    for us, lista in grupos.items():
        if com_links:
            itens = ", ".join(f"[CA-{ca.numero:02d}]({link_ca(ca, historias_por_id)})" for ca in lista)
        else:
            itens = ", ".join(f"CA-{ca.numero:02d}" for ca in lista)
        partes.append(f"{us}: {itens}")
    return "; ".join(partes) or "—"


def lista_us(cas, historias_por_id, com_links=True) -> str:
    us = sorted({ca.historia for ca in cas})
    if not com_links:
        return ", ".join(us) or "—"
    return ", ".join(f"[{u}](../historias/{historias_por_id[u].arquivo.name})" for u in us) or "—"


def lista_tas(cas, historias_por_id, com_links=True) -> str:
    itens = []
    for ca in sorted(cas, key=lambda c: (c.historia, c.numero)):
        ta = ta_de(ca, historias_por_id)
        if ta is None:
            continue
        rotulo = f"TA-{ta.numero:02d}" + {"manual": " (manual)", "pendente": " (pendente)"}.get(ta.tipo, "")
        itens.append(f"[{rotulo}]({link_ta(ta, historias_por_id[ca.historia])})" if com_links else rotulo)
    return ", ".join(dict.fromkeys(itens)) or "—"


def texto_das_rotas(requisito: Requisito, com_crase=True) -> str:
    if not requisito.rotas:
        return "—"
    itens = [f"`{r}`" if com_crase else r for r in requisito.rotas]
    origem = "do pai" if requisito.pai else "das operações protegidas"
    return "; ".join(itens) + (f" ({origem})" if requisito.rotas_herdadas else "")


def texto_do_codigo(requisito: Requisito, com_crase=True) -> str:
    itens = [f"{a}::{s}" for a, s in requisito.codigo]
    return ", ".join(f"`{i}`" if com_crase else i for i in itens) or "—"


def cabecalho_gerado(titulo: str, modelo: Modelo, descricao: str) -> list[str]:
    versao, estado = modelo.ras
    return [
        f"# {titulo}",
        "",
        AVISO,
        "",
        "| Identificação | Responsabilidade |",
        "|---|---|",
        f"| **Parte da [RAS-01](README.md) • {versao} • {estado}** | "
        "Autor: Max Zimmermann dos Reis • Revisor: Matheus Cezar Santos • Aprovador: Eduardo Almeida da Cunha |",
        "",
        descricao,
        "",
    ]


COLUNAS = ["NS", "RF (título)", "F", "RN", "UC (passo, alternativa ou exceção)", "US", "CA", "TA", "DEC",
           "Endpoint ou tela", "Código", "Situação"]


def linhas_da_matriz(modelo: Modelo, com_links: bool) -> list[list[str]]:
    por_id = {h.id: h for h in modelo.historias}
    linhas = []
    for rf in modelo.ordem:
        r = modelo.rfs[rf]
        if com_links:
            ns = ", ".join(f"[{n}](../visao.md#{n.lower()})" for n in r.ns)
            ns = ns.replace(")", ") (principal)", 1) if len(r.ns) > 1 else ns
            titulo = f'<a id="{ancora_rf(rf)}"></a>[{rf}]({r.link}) {r.titulo}'
            decs = ", ".join(f"[{d}](../decisoes/{d}.md)" for d in r.decs) or "—"
            rns = ", ".join(f"[{n}](../requisitos/regras-de-negocio.md#{n.lower()})" for n in r.rns) or "—"
            uc = como_entra_relinkado(r)
        else:
            ns = ", ".join(r.ns)
            titulo = f"{rf} {r.titulo}"
            decs = ", ".join(r.decs) or "—"
            rns = ", ".join(r.rns) or "—"
            uc = sem_links(f"{r.uc or '—'} · {r.como_entra}")
        texto_situacao, _ = situacao(r, modelo, por_id)
        linhas.append([
            ns or "—",
            titulo,
            r.f,
            rns,
            uc,
            lista_us(r.cas, por_id, com_links),
            agrupar_cas(r.cas, por_id, com_links),
            lista_tas(r.cas, por_id, com_links),
            decs,
            texto_das_rotas(r, com_links),
            texto_do_codigo(r, com_links),
            texto_situacao if com_links else sem_links(texto_situacao),
        ])
    return linhas


def gerar_matriz(modelo: Modelo) -> str:
    saida = cabecalho_gerado(
        "Matriz de rastreabilidade (NS → RF → UC → US → CA/TA → endpoint ou tela → código)",
        modelo,
        f"Uma linha por RF ({len(modelo.ordem)}, com os filhos). A cadeia do professor vai de NS a TA; "
        "\"Endpoint ou tela\" e \"Código\" são o elo complementar do grupo (ponto 13 em aberto). "
        "Como ler: [README](README.md#como-ler-a-matriz). Mesmas linhas em [`matriz.csv`](matriz.csv).",
    )
    saida += ["| " + " | ".join(COLUNAS) + " |", "|" + "---|" * len(COLUNAS)]
    saida += ["| " + " | ".join(c.replace("|", "\\|") for c in linha) + " |" for linha in linhas_da_matriz(modelo, True)]
    return "\n".join(saida) + "\n"


def gerar_csv(modelo: Modelo) -> str:
    def celula(texto: str) -> str:
        return '"' + texto.replace('"', '""') + '"' if re.search(r'[;"\n]', texto) else texto

    linhas = [COLUNAS] + linhas_da_matriz(modelo, False)
    return "﻿" + "\n".join(";".join(celula(c) for c in linha) for linha in linhas) + "\n"


def contagens(rfs: list[Requisito], historias_por_id) -> dict:
    cas = {ca.ancora: ca for r in rfs for ca in r.cas}
    tas = [ta for ca in cas.values() if (ta := ta_de(ca, historias_por_id))]
    return {
        "rf": len(rfs),
        "uc": len({r.uc for r in rfs if r.uc}),
        "us": len({ca.historia for ca in cas.values()}),
        "ca": len(cas),
        "ta": len({t.numero for t in tas}),
        "ta_manual": len({t.numero for t in tas if t.tipo == "manual"}),
    }


def pct(parte: int, total: int) -> str:
    return f"{100 * parte / total:.0f}%".replace(".", ",") if total else "—"


VITEST = re.compile(r"`((?:\w+/)*\w+\.test\.tsx?)`")
COMANDO_DE_VERIFICACAO = re.compile(r"`(docker compose exec [^`]+)`")


def _eh_medicao(texto: str) -> bool:
    return bool(re.search(r"medir_desempenho|\[Medição\]|\*\*Medido\*\*", texto))


def _comandos(texto: str) -> list[str]:
    return [c for c in COMANDO_DE_VERIFICACAO.findall(texto) if "medir_desempenho" not in c and "pytest config/tests" not in c]


def forma_de_verificacao(rnf: dict) -> str:
    texto = rnf["campos"].get("Como verificar", "")
    formas = []
    if testes_do_texto(texto) or VITEST.search(texto):
        formas.append("automatizado")
    elif _comandos(texto):
        formas.append("automatizado (comando)")
    if _eh_medicao(texto):
        formas.append("medição")
    if texto.startswith("A verificar") or "a verificar" in rnf["campos"].get("Revisão / estado", "").lower():
        formas.append("manual (a verificar)")
    return " + ".join(formas) or "manual"


def gerar_cobertura(modelo: Modelo) -> str:
    por_id = {h.id: h for h in modelo.historias}
    todos = [modelo.rfs[rf] for rf in modelo.ordem]
    tas_todos = [ta for h in modelo.historias for ta in h.testes]
    ns_com_rf = [n for n in modelo.ns if any(n in r.ns for r in todos)]
    ns_com_ta = [n for n in modelo.ns if any(n in r.ns and r.cas for r in todos)]
    sem_transversal = [r for r in todos if r.id not in JUSTIFICADOS]
    completos = [r for r in todos if not faltas(r, por_id)]
    cas_com_ta = [ca for ca in modelo.criterios if ta_de(ca, por_id)]
    manuais = [ta for ta in tas_todos if ta.tipo == "manual"]
    pendentes = [ta for ta in tas_todos if ta.tipo == "pendente"]
    linhas = [
        ("NS com pelo menos um RF", len(ns_com_rf), len(modelo.ns)),
        ("NS que chegam a um TA", len(ns_com_ta), len(modelo.ns)),
        ("RF com NS de origem", sum(1 for r in todos if r.ns), len(todos)),
        ("RN com pelo menos um RF", sum(1 for rn in modelo.rns.values() if rn["rfs"]), len(modelo.rns)),
        ("RF com UC (sem o transversal)", sum(1 for r in sem_transversal if r.uc), len(sem_transversal)),
        ("RF com US e CA (sem o transversal)", sum(1 for r in sem_transversal if r.cas), len(sem_transversal)),
        ("CA com TA", len(cas_com_ta), len(modelo.criterios)),
        ("TA automatizados", len(tas_todos) - len(manuais) - len(pendentes), len(tas_todos)),
        ("TA manuais (roteiro)", len(manuais), len(tas_todos)),
        ("TA pendentes (regra decidida, código na tarefa citada)", len(pendentes), len(tas_todos)),
        ("RF com endpoint ou tela", sum(1 for r in todos if r.rotas), len(todos)),
        ("RF com código citado", sum(1 for r in todos if r.codigo), len(todos)),
        ("RF com a cadeia completa", len(completos), len(todos)),
    ]
    saida = cabecalho_gerado(
        "Cobertura da rastreabilidade",
        modelo,
        "Resumo da [matriz](matriz.md) para o `modelagem.pdf` (DOC-01). As contagens por NS usam todas as NS "
        "citadas na Origem de cada RF (a principal e as secundárias), por isso um RF pode contar em mais de uma NS.",
    )
    saida += ["## Por elo", "", "| Elo | Com o elo | Total | % |", "|---|---|---|---|"]
    saida += [f"| {nome} | {parte} | {total} | {pct(parte, total)} |" for nome, parte, total in linhas]
    saida += [
        "",
        f"TA manuais: {', '.join(f'TA-{t.numero:02d}' for t in manuais) or 'nenhum'} "
        "(ver as lacunas de CA sem TA automatizado na [SRS](../requisitos/srs.md#lacunas)).",
        "",
        f"TA pendentes: {', '.join(f'TA-{t.numero:02d}' for t in pendentes) or 'nenhum'} "
        "(a especificação está adiante do código de propósito; cada um aponta para a tarefa que o implementa).",
        "",
        "## Por necessidade (NS)",
        "",
        "| NS | RF (principal) | RF (todas as citações) | UC | US | CA | TA (manuais) |",
        "|---|---|---|---|---|---|---|",
    ]
    for ns in modelo.ns:
        rfs = [r for r in todos if ns in r.ns]
        c = contagens(rfs, por_id)
        principal = sum(1 for r in rfs if r.ns[0] == ns)
        saida.append(
            f"| [{ns}](../visao.md#{ns.lower()}) | {principal} | {c['rf']} | {c['uc']} | {c['us']} | {c['ca']} | "
            f"{c['ta']} ({c['ta_manual']}) |"
        )
    saida += ["", "## Por funcionalidade do enunciado (F1 a F6)", "",
              "| F | Funcionalidade | RF | UC | US | CA | TA (manuais) |", "|---|---|---|---|---|---|---|"]
    for f, nome in NOMES_DAS_FUNCIONALIDADES.items():
        rfs = [r for r in todos if r.f == f]
        c = contagens(rfs, por_id)
        saida.append(f"| {f} | {nome} | {c['rf']} | {c['uc']} | {c['us']} | {c['ca']} | {c['ta']} ({c['ta_manual']}) |")
    formas = Counter(forma_de_verificacao(r) for r in modelo.rnfs)
    saida += ["", "## RNF por forma de verificação", "", "| Forma | RNF |", "|---|---|"]
    saida += [f"| {forma} | {n} |" for forma, n in sorted(formas.items())]
    saida += ["", f"Detalhe em [`rnf.md`](rnf.md). Total: {len(modelo.rnfs)} RNF."]
    return "\n".join(saida) + "\n"


def lacunas_da_rota(rota: Rota, modelo: Modelo) -> list[str]:
    caminho = rota.chave.split(" ")[-1]
    return [lid for lid, lacuna in modelo.lacunas.items() if f"`{caminho}`" in lacuna["texto"]]


def explicacao_da_rota(rota: Rota, rfs: list[Requisito], modelo: Modelo) -> tuple[str, bool]:
    lacunas = lacunas_da_rota(rota, modelo)
    if rfs:
        citadas = ", ".join(f"[{lid}](../requisitos/srs.md#{modelo.lacunas[lid]['ancora']})" for lid in lacunas)
        return (f"ver {citadas}" if citadas else "", True)
    if rota.tipo == "api" and all(rota.linha.get(p) == "405" for p in ("dono", "outro", "gestor")):
        if rota.chave.startswith("DELETE"):
            return ("operação inexistente, provada pela matriz: [RNF-R05](../requisitos/rnf.md#rnf-r05) (nada é excluído)", True)
        return ("método não implementado, provado pela matriz: [RNF-F04](../requisitos/rnf.md#rnf-f04) (toda rota e método com regra)", True)
    for lid in lacunas:
        return (f"sem RF: [{lid}](../requisitos/srs.md#{modelo.lacunas[lid]['ancora']})", True)
    return ("sem RF, sem RNF e sem lacuna", False)


def inverso(modelo: Modelo) -> list[tuple[Rota, list[Requisito], str, bool]]:
    resultado = []
    comandos = sorted({r for req in modelo.rfs.values() for r in req.rotas if r.startswith("comando ")})
    rotas = modelo.rotas + [Rota("comando", c, c.split(" ", 1)[1]) for c in comandos]
    for rota in rotas:
        rfs = [modelo.rfs[rf] for rf in modelo.ordem if rota.chave in modelo.rfs[rf].rotas and not modelo.rfs[rf].rotas_herdadas]
        texto, ok = explicacao_da_rota(rota, rfs, modelo)
        resultado.append((rota, rfs, texto, ok))
    return resultado


def gerar_inverso(modelo: Modelo) -> str:
    saida = cabecalho_gerado(
        "Rastreabilidade no sentido inverso (rota ou tela → RF → NS)",
        modelo,
        "Prova de que nenhum comportamento existe sem necessidade: cada rota da [matriz de acesso](../../matriz_de_acesso.md), "
        "cada página do frontend e cada comando citado nas fichas aparece com os RF cuja evidência a cita (os filhos que só "
        "herdam a rota do pai não entram) e as NS de origem deles. Rota sem RF aparece marcada, com o RNF ou a lacuna que a explica.",
    )
    titulos = {"api": "## Rotas da API", "tela": "## Telas", "comando": "## Comandos"}
    for tipo, titulo in titulos.items():
        saida += [titulo, "", "| Rota | Nome | RF | NS | Observação |", "|---|---|---|---|---|"]
        for rota, rfs, texto, _ in inverso(modelo):
            if rota.tipo != tipo:
                continue
            ligacoes = ", ".join(f"[{r.id}](matriz.md#{ancora_rf(r.id)})" for r in rfs) or "**sem RF**"
            ns = ", ".join(f"[{n}](../visao.md#{n.lower()})" for n in ordenar(n for r in rfs for n in r.ns)) or "—"
            nome = f"`{rota.nome}`" if tipo == "api" else rota.nome
            if rota.linha.get("corpo", "—") != "—":
                nome += f" (corpo: {rota.linha['corpo']})"
            saida.append(f"| `{rota.chave}` | {nome} | {ligacoes} | {ns} | {texto or '—'} |")
        saida.append("")
    return "\n".join(saida)


def gerar_rnf(modelo: Modelo) -> str:
    saida = cabecalho_gerado(
        "Rastreabilidade dos RNF (RNF → NS, RF ou DEC → forma de verificação → evidência)",
        modelo,
        "Gerado das [fichas de RNF](../requisitos/rnf.md) (campos Origem, Como verificar e Revisão / estado): "
        "nenhum vínculo é escrito aqui. \"Automatizado\" = cita testes; \"medição\" = `scripts/medir_desempenho.py`; "
        "\"manual\" = verificação no ensaio ([L-09](../requisitos/srs.md#l-09)).",
    )
    saida += ["| RNF | Origem | Forma de verificação | Evidência | Estado |", "|---|---|---|---|---|"]
    for rnf in modelo.rnfs:
        campos = rnf["campos"]
        ancora = rnf["id"].lower()
        titulo = re.search(rf'<a id="{ancora}"></a>{rnf["id"]} · (.+)$', ler(rnf["arquivo"]), flags=re.M)
        origem = relinkar(campos.get("Origem", ""), "requisitos")
        origem = ID_NS.sub(lambda a: f"[{a.group(0)}](../visao.md#{a.group(0).lower()})", origem)
        testes = testes_do_texto(campos.get("Como verificar", ""))
        texto = campos.get("Como verificar", "")
        itens = [f"`{a}::{n}`" for a, n in testes]
        itens += [f"`{v}` (Vitest)" for v in dict.fromkeys(VITEST.findall(texto))]
        itens += [f"`{c}`" for c in _comandos(texto)]
        if _eh_medicao(texto):
            itens.append("`scripts/medir_desempenho.py`" if "medir_desempenho" in texto or "RNF-P01" in texto else "medição registrada na ficha")
        evidencia = ", ".join(itens)
        evidencia = evidencia or f"roteiro na [ficha](../requisitos/rnf.md#{ancora})"
        saida.append(
            f"| [{rnf['id']}](../requisitos/rnf.md#{ancora}) {titulo[1] if titulo else ''} | {origem} | "
            f"{forma_de_verificacao(rnf)} | {evidencia} | {relinkar(campos.get('Revisão / estado', ''), 'requisitos')} |"
        )
    return "\n".join(saida) + "\n"


@dataclass
class Impacto:
    dec: str
    rfs: list[str]
    rnfs: list[str]
    diretos: list
    por_rf: list

    @property
    def cas(self) -> list:
        vistos = {}
        for ca in self.diretos + self.por_rf:
            vistos[ca.ancora] = ca
        return sorted(vistos.values(), key=lambda c: (c.historia, c.numero))


def impactos(modelo: Modelo) -> dict[str, Impacto]:
    todos_rnf = [r["id"] for r in modelo.rnfs]
    resultado = {}
    for dec in modelo.decs:
        rfs = [rf for rf in modelo.ordem if dec in modelo.rfs[rf].decs]
        rnfs = [r["id"] for r in modelo.rnfs if dec in ID_DEC.findall(r["campos"].get("Origem", ""))]
        diretos = [ca for ca in modelo.criterios if dec in ID_DEC.findall(ca.campos.get("Depende de", ""))]
        ids_diretos = {ca.ancora for ca in diretos}
        por_rf = [ca for ca in modelo.criterios if set(ca.rfs()) & set(rfs) and ca.ancora not in ids_diretos]
        resultado[dec] = Impacto(dec, rfs, ordenar(set(rnfs) & set(todos_rnf)), diretos, por_rf)
    return resultado


def ordem_das_decs(modelo: Modelo) -> list[str]:
    abertas = [d for d in modelo.decs if modelo.decs[d]["estado"] != "Decidida" and d not in ORDEM_DE_IMPACTO]
    decididas = [d for d in modelo.decs if modelo.decs[d]["estado"] == "Decidida"]
    return [d for d in ORDEM_DE_IMPACTO if d in modelo.decs] + abertas + decididas


def tipo_de_mudanca(modelo: Modelo, impacto: Impacto) -> str:
    if modelo.decs[impacto.dec]["estado"] == "Decidida":
        return "decidida: outra resposta só por CR (comportamental)"
    if impacto.rfs or impacto.cas:
        return "comportamental (muda regra, RF e aceite)"
    if impacto.rnfs:
        return "comportamental (muda a meta de um RNF)"
    return "editorial"


def gerar_impacto(modelo: Modelo) -> str:
    por_id = {h.id: h for h in modelo.historias}
    tudo = impactos(modelo)
    saida = cabecalho_gerado(
        "Mapa de impacto por decisão (DEC)",
        modelo,
        "Para cada DEC, tudo o que muda se a resposta for diferente da opção adotada: RF (campo Decisões das fichas), RNF "
        "(Origem), UC e passos (dos RF), US e CA (os que dependem da DEC e os que verificam os RF afetados), TA, endpoints, "
        "telas e código. A regressão estimada é o número de TAs a rever. Pronto para virar a seção \"Mapa de impacto\" de um "
        "[CR](../mudancas/modelo-cr.md). Ordem: DEC-13, DEC-05 e DEC-07 primeiro (maior impacto), depois as demais adotadas "
        "provisoriamente e, no fim, as decididas.",
    )
    saida += ["| DEC | Estado | RF | RNF | US | CA | TA (manuais) | Tipo de mudança |", "|---|---|---|---|---|---|---|---|"]
    for dec in ordem_das_decs(modelo):
        i = tudo[dec]
        c = contagens([modelo.rfs[r] for r in i.rfs], por_id)
        tas = [ta_de(ca, por_id) for ca in i.cas]
        manuais = sum(1 for ta in tas if ta and ta.tipo == "manual")
        saida.append(
            f"| [{dec}](#{dec.lower()}) | {modelo.decs[dec]['estado']} | {len(i.rfs)} | {len(i.rnfs)} | "
            f"{len({ca.historia for ca in i.cas})} | {len(i.cas)} | {len([t for t in tas if t])} ({manuais}) | "
            f"{tipo_de_mudanca(modelo, i)} |"
        )
        del c
    saida.append("")
    for dec in ordem_das_decs(modelo):
        i = tudo[dec]
        d = modelo.decs[dec]
        campos = d["campos"]
        rfs = [modelo.rfs[r] for r in i.rfs]
        rotas = list(dict.fromkeys(rota for r in rfs for rota in r.rotas))
        codigo = list(dict.fromkeys(f"{a}::{s}" for r in rfs for a, s in r.codigo))
        ucs = [f"- {r.id}: {como_entra_relinkado(r)}" for r in rfs]
        tas = [ta for ca in i.cas if (ta := ta_de(ca, por_id))]
        opcao = campos.get("Opção adotada hoje") or campos.get("Decisão", "")
        saida += [
            f'## <a id="{dec.lower()}"></a>{dec} · {d["titulo"]}',
            "",
            "| Campo | Conteúdo |",
            "|---|---|",
            f"| **Estado** | {d['estado']} ([ficha](../decisoes/{dec}.md)) |",
            f"| **Pergunta** | {relinkar(campos.get('Pergunta', ''), 'decisoes')} |",
            f"| **Opção adotada** | {relinkar(opcao, 'decisoes')} |",
            f"| **Responsável** | {campos.get('Responsável', '')} |",
            f"| **Prazo** | {campos.get('Prazo sugerido') or campos.get('Prazo', '')} |",
            f"| **Tipo de mudança se a resposta for outra** | {tipo_de_mudanca(modelo, i)} |",
            f"| **Regressão estimada** | {len(tas)} TAs a rever ({sum(1 for t in tas if t.tipo == 'manual')} manuais), "
            f"de {len(i.cas)} CAs em {len({ca.historia for ca in i.cas})} histórias: {len(i.diretos)} CAs dependem "
            f"diretamente da DEC e {len(i.por_rf)} verificam os RF afetados |",
            "",
            f"- **RF:** {', '.join(f'[{r.id}](matriz.md#{ancora_rf(r.id)})' for r in rfs) or 'nenhum'}",
            f"- **RNF:** {', '.join(f'[{r}](../requisitos/rnf.md#{r.lower()})' for r in i.rnfs) or 'nenhum'}",
            "- **UC (passo, alternativa ou exceção):**" + ("" if ucs else " nenhum"),
            *[f"  {u}" for u in ucs],
            f"- **US:** {lista_us(i.cas, por_id)}",
            f"- **CA que dependem da DEC:** {agrupar_cas(i.diretos, por_id)}",
            f"- **CA dos RF afetados (regressão):** {agrupar_cas(i.por_rf, por_id)}",
            f"- **TA:** {lista_tas(i.cas, por_id)}",
            f"- **Endpoint ou tela:** {'; '.join(f'`{r}`' for r in rotas) or 'nenhum'}",
            f"- **Código:** {', '.join(f'`{c}`' for c in codigo) or 'nenhum'}",
            "",
        ]
    return "\n".join(saida)


def gerar_regras(modelo: Modelo) -> str:
    por_id = {h.id: h for h in modelo.historias}
    saida = cabecalho_gerado(
        "Rastreabilidade das regras de negócio (RN → RF → UC → US → CA)",
        modelo,
        f"Uma linha por regra de negócio do [catálogo](../requisitos/regras-de-negocio.md) ({len(modelo.rns)} RN). "
        "Os RF vêm da coluna \"RFs ligados\" do catálogo e batem com o campo \"Regras de negócio\" de cada ficha; "
        "UC, US e CA são os dos RF ligados. Como ler: [README](README.md#como-ler-a-matriz).",
    )
    saida += ["| RN | Regra | RF | UC | US | CA | Vigência |", "|---|---|---|---|---|---|---|"]
    for identificador, rn in modelo.rns.items():
        rfs = [modelo.rfs[rf] for rf in rn["rfs"] if rf in modelo.rfs]
        cas = list({ca.ancora: ca for r in rfs for ca in r.cas}.values())
        ucs = ordenar(r.uc for r in rfs if r.uc)
        saida.append(
            "| " + " | ".join(c.replace("|", "\\|") for c in [
                f'<a id="{identificador.lower()}"></a>[{identificador}](../requisitos/regras-de-negocio.md#{identificador.lower()})',
                rn["regra"],
                ", ".join(f"[{r.id}]({r.link})" for r in rfs) or "—",
                ", ".join(f"[{u}](../casos-de-uso/README.md#{u.lower()})" for u in ucs) or "—",
                lista_us(cas, por_id, True),
                agrupar_cas(cas, por_id, True),
                rn["vigencia"],
            ]) + " |"
        )
    return "\n".join(saida) + "\n"


def arquivos_gerados(modelo: Modelo) -> dict[Path, str]:
    return {
        PASTA_RAS / "matriz.md": gerar_matriz(modelo),
        PASTA_RAS / "matriz.csv": gerar_csv(modelo),
        PASTA_RAS / "cobertura.md": gerar_cobertura(modelo),
        PASTA_RAS / "sentido-inverso.md": gerar_inverso(modelo),
        PASTA_RAS / "rnf.md": gerar_rnf(modelo),
        PASTA_RAS / "regras-de-negocio.md": gerar_regras(modelo),
        PASTA_RAS / "impacto-por-dec.md": gerar_impacto(modelo),
    }


def artefatos_do_manifesto() -> list[Path]:
    return sorted(
        (a for a in PASTA.rglob("*") if a.suffix in (".md", ".puml", ".csv") and a.relative_to(PASTA).parts[0] != "baselines"),
        key=lambda a: a.relative_to(PASTA).as_posix(),
    )


def linha_do_manifesto(arquivo: Path) -> str:
    caminho = arquivo.relative_to(PASTA).as_posix()
    if arquivo.suffix == ".puml":
        nome, identificador = ARTEFATO_DO_PUML.get(arquivo.name, (arquivo.name, "—"))
        readme = ler_cabecalho(PASTA / "casos-de-uso" / "README.md")
        versao, estado = readme[1], readme[2]
    elif arquivo.suffix == ".csv":
        nome, identificador = "Matriz de rastreabilidade (planilha, gerada)", "Parte da RAS-01"
        cabecalho = ler_cabecalho(README_RAS)
        versao, estado = cabecalho[1], cabecalho[2]
    else:
        titulo = re.search(r"^# (.+)$", ler(arquivo), flags=re.M)
        nome = titulo[1].strip() if titulo else arquivo.name
        cabecalho = ler_cabecalho(arquivo) or ("sem cabeçalho", "—", "—")
        identificador, versao, estado = cabecalho
    return f"| {nome} | {identificador} | {versao} | {estado} | `{caminho}` | `{sha8(arquivo)}` |"


def bloco_manifesto() -> str:
    linhas = [linha_do_manifesto(a) for a in artefatos_do_manifesto()]
    impressao = hashlib.sha256("\n".join(linhas).encode("utf-8")).hexdigest()[:8]
    return "\n".join(
        [
            f"{len(linhas)} artefatos (todo `.md`, `.puml` e `.csv` de `docs/fontes/requisitos/`, menos `baselines/`). "
            f"SHA-256 do conteúdo com fim de linha LF, 8 primeiros caracteres. Impressão do manifesto: `{impressao}`.",
            "",
            "| Artefato | ID | Versão | Estado | Caminho (a partir de `docs/fontes/requisitos/`) | SHA-256 |",
            "|---|---|---|---|---|---|",
            *linhas,
        ]
    )


def bloco_decisoes(modelo: Modelo) -> str:
    tudo = impactos(modelo)
    linhas = ["| DEC | Título | Estado | Prazo | CAs afetados | Na pauta |", "|---|---|---|---|---|---|"]
    for dec in sorted(modelo.decs):
        d = modelo.decs[dec]
        if d["estado"] == "Decidida":
            continue
        prazo = d["campos"].get("Prazo sugerido") or d["campos"].get("Prazo", "")
        linhas.append(
            f"| [{dec}](../decisoes/{dec}.md) | {d['titulo']} | {d['estado']} | {prazo} | "
            f"[{len(tudo[dec].cas)}](../rastreabilidade/impacto-por-dec.md#{dec.lower()}) | "
            f"[pauta](../decisoes/pauta-aula-7.md#{dec.lower()}) |"
        )
    return "\n".join(linhas)


def bloco_lacunas(modelo: Modelo) -> str:
    linhas = ["| Lacuna | Tipo | Afeta |", "|---|---|---|"]
    for lid, lacuna in modelo.lacunas.items():
        if re.search(r"\*\*aceitar\*\*", lacuna["proposta"], flags=re.I):
            afeta = relinkar(lacuna["afeta"], "requisitos").replace("../requisitos/", "../requisitos/")
            linhas.append(f"| [{lid}](../requisitos/srs.md#{lacuna['ancora']}) | {lacuna['tipo']} | {sem_links(afeta)} |")
    return "\n".join(linhas)


def blocos_da_candidata(modelo: Modelo) -> dict[str, str]:
    return {"manifesto": bloco_manifesto(), "decisoes": bloco_decisoes(modelo), "lacunas": bloco_lacunas(modelo)}


def aplicar_blocos(texto: str, blocos: dict[str, str]) -> str:
    for nome, conteudo in blocos.items():
        texto = re.sub(
            rf"(<!-- {nome}:inicio -->)\n(?:.*?\n)?(<!-- {nome}:fim -->)",
            lambda a: f"{a.group(1)}\n{conteudo}\n{a.group(2)}",
            texto,
            flags=re.S,
        )
    return texto


def verificar_cadeia(modelo: Modelo) -> list[str]:
    por_id = {h.id: h for h in modelo.historias}
    erros = []
    for ns in modelo.ns:
        if ns in necessidades_fora_do_1_0():
            continue
        if not any(ns in r.ns and r.cas for r in modelo.rfs.values()):
            erros.append(f"{ns} não chega a nenhum TA")
    justificados = 0
    for rf in modelo.ordem:
        texto, ok = situacao(modelo.rfs[rf], modelo, por_id)
        if not ok:
            erros.append(f"{rf}: {texto}")
        elif texto != "completa" and not texto.startswith("completa"):
            justificados += 1
    completos = sum(1 for rf in modelo.ordem if not faltas(modelo.rfs[rf], por_id))
    print(f"NS que chegam a um TA: {len(modelo.ns) - sum(1 for e in erros if e.startswith('NS'))} de {len(modelo.ns)}")
    print(f"RF com a cadeia completa: {completos} de {len(modelo.ordem)}; com elo faltante justificado: {justificados}")
    return erros


def verificar_testes_citados(modelo: Modelo) -> list[str]:
    por_id = {h.id: h for h in modelo.historias}
    erros = []
    sem_ta = [ca.referencia for ca in modelo.criterios if ta_de(ca, por_id) is None]
    erros += [f"{ref}: sem TA" for ref in sem_ta]
    cache: dict[Path, str] = {}
    citados = []
    for h in modelo.historias:
        for ta in h.testes:
            citados += [(f"TA-{ta.numero:02d}", a, n) for a, n in testes_do_texto(ta.testes)]
            if ta.tipo == "automatizado" and not testes_do_texto(ta.testes) and ".test.ts" not in ta.testes:
                erros.append(f"TA-{ta.numero:02d}: automatizado sem teste citado")
    for rnf in modelo.rnfs:
        texto = rnf["campos"].get("Como verificar", "")
        citados += [(rnf["id"], a, n) for a, n in testes_do_texto(texto)]
        erros += [f"{rnf['id']}: src/frontend/src/{v} não existe" for v in VITEST.findall(texto) if not (FRONTEND / v).exists()]
    for linha in secao(ler(SRS), r"6\.4").splitlines():
        if achado := re.match(r"^\|\s*(RF-[\d.]+)\s*\|(.*)\|\s*$", linha):
            citados += [(f"SRS 6.4 {achado[1]}", a, n) for a, n in testes_do_texto(achado[2])]
    for origem, arquivo, nome in citados:
        if not teste_existe(arquivo, nome, cache):
            erros.append(f"{origem}: {arquivo}::{nome} não existe")
    print(f"CAs com TA: {len(modelo.criterios) - len(sem_ta)} de {len(modelo.criterios)}; "
          f"testes pytest conferidos (TA, RNF e SRS 6.4): {len(set((a, n) for _, a, n in citados))}")
    return erros


def _rfs_da_celula(celula: str, todos: list[str]) -> set[str]:
    rfs = set(expandir(celula, todos))
    if "e filhos" in celula:
        rfs |= {i for i in todos for base in ID_RF.findall(celula) if i.startswith(base + ".")}
    return rfs


def verificar_inverso(modelo: Modelo) -> list[str]:
    erros = [f"rota citada na evidência e desconhecida: {r}" for r in modelo.rotas_desconhecidas]
    resultado = inverso(modelo)
    for rota, rfs, texto, ok in resultado:
        if not ok:
            erros.append(f"{rota.chave} ({rota.nome}): {texto}")
    texto_srs = ler(SRS)
    derivadas = {r.chave: {req.id for req in modelo.rfs.values() if r.chave in req.rotas} for r in modelo.rotas}
    for linha in secao(texto_srs, r"4\.2").splitlines():
        celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
        if len(celulas) != 2 or not celulas[0].startswith("`"):
            continue
        for metodo_caminho, rfs in zip(celulas[0].split(" · "), celulas[1].split(" · ")):
            chave_rota = metodo_caminho.strip("` ").split("?")[0]
            esperados = _rfs_da_celula(rfs, modelo.ordem)
            faltam = esperados - derivadas.get(chave_rota, set())
            if chave_rota not in derivadas:
                erros.append(f"SRS 4.2 cita {chave_rota}, que não está na matriz de acesso")
            elif faltam:
                erros.append(f"SRS 4.2 liga {chave_rota} a {ordenar(faltam)}, mas a evidência desses RF não cita a rota")
    for linha in secao(texto_srs, r"4\.1").splitlines():
        celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
        caminhos = [t for t in TRECHO.findall(celulas[0])] if celulas and celulas[0] != "Tela" else []
        if len(celulas) != 4 or not caminhos:
            continue
        esperados = _rfs_da_celula(celulas[3], modelo.ordem)
        for caminho in caminhos:
            if not esperados & derivadas.get(caminho, set()):
                erros.append(f"SRS 4.1: nenhum RF de {ordenar(esperados)} cita a tela {caminho} na evidência")
    tipos = Counter(r.tipo for r, *_ in resultado)
    sem_rf = sum(1 for _, rfs, _, _ in resultado if not rfs)
    print(f"Rotas da API: {tipos['api']}; telas: {tipos['tela']}; comandos: {tipos['comando']}; sem RF (com RNF ou lacuna): {sem_rf}")
    return erros


def _simbolo_existe(arquivo: str, simbolo: str, cache: dict) -> bool:
    if arquivo.endswith(".py"):
        caminho = BACKEND / arquivo
        if not caminho.exists():
            return False
        if caminho not in cache:
            cache[caminho] = ast.parse(ler(caminho))
        nomes = simbolo.split(".")
        corpo = cache[caminho].body
        for nome in nomes:
            achado = None
            for no in corpo:
                if isinstance(no, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and no.name == nome:
                    achado = no
                elif isinstance(no, ast.Assign) and any(isinstance(a, ast.Name) and a.id == nome for a in no.targets):
                    achado = no
                elif isinstance(no, ast.AnnAssign) and isinstance(no.target, ast.Name) and no.target.id == nome:
                    achado = no
            if achado is None:
                return False
            corpo = getattr(achado, "body", [])
        return True
    caminho = FRONTEND / arquivo
    if not caminho.exists():
        return False
    return bool(re.search(rf"\b(?:function|const|let|class)\s+{re.escape(simbolo)}\b", ler(caminho)))


def verificar_codigo(modelo: Modelo) -> list[str]:
    erros, cache, total = [], {}, 0
    for rf in modelo.ordem:
        texto = modelo.rfs[rf].campos.get("Código (complementar)", "")
        if not texto:
            erros.append(f"{rf}: sem o campo 'Código (complementar)'")
        citados = TRECHO.findall(texto)
        for trecho in citados:
            if not SIMBOLO.fullmatch(f"`{trecho}`"):
                erros.append(f"{rf}: {trecho!r} fora do formato arquivo::Símbolo")
        for arquivo, simbolo in modelo.rfs[rf].codigo:
            total += 1
            if not _simbolo_existe(arquivo, simbolo, cache):
                erros.append(f"{rf}: {arquivo}::{simbolo} não existe")
    print(f"Símbolos de código conferidos: {total} (em {len(cache)} arquivos Python e os de TypeScript)")
    return erros


def _numeros_da_pauta() -> dict[str, tuple[int, int]]:
    if not PAUTA.exists():
        return {}
    numeros = {}
    for achado in re.finditer(r'<a id="(dec-\d{2})"></a>(.*?)(?=<a id="dec-\d{2}"></a>|^## |\Z)', ler(PAUTA), flags=re.S | re.M):
        contagem = re.search(r"(\d+) CAs? e (\d+) TAs?", achado[2])
        if contagem:
            numeros[achado[1].upper()] = (int(contagem[1]), int(contagem[2]))
    return numeros


def verificar_decs(modelo: Modelo, gerado_impacto: str) -> list[str]:
    erros = []
    por_id = {h.id: h for h in modelo.historias}
    tudo = impactos(modelo)
    pauta = _numeros_da_pauta()
    for dec, d in modelo.decs.items():
        campos = d["campos"]
        exigidos = {
            "Pergunta": campos.get("Pergunta"),
            "Opção adotada ou Decisão": campos.get("Opção adotada hoje") or campos.get("Decisão"),
            "Responsável": campos.get("Responsável"),
            "Prazo": campos.get("Prazo sugerido") or campos.get("Prazo"),
            "Artefatos afetados": campos.get("Artefatos afetados"),
        }
        erros += [f"{dec}: sem {nome}" for nome, valor in exigidos.items() if not valor]
        if not d["historico"]:
            erros.append(f"{dec}: sem histórico")
        if f'<a id="{dec.lower()}"></a>' not in gerado_impacto:
            erros.append(f"{dec}: não aparece em impacto-por-dec.md")
        artefatos = campos.get("Artefatos afetados", "")
        i = tudo[dec]
        us_esperadas = {ca.historia for ca in i.cas}
        trecho = artefatos.split("**REQ-06:**")[-1] if "**REQ-06:**" in artefatos else ""
        if not trecho:
            erros.append(f"{dec}: Artefatos afetados sem o trecho das histórias e CAs (REQ-06)")
        else:
            if set(ID_US.findall(trecho)) != us_esperadas:
                erros.append(f"{dec}: Artefatos afetados cita {sorted(set(ID_US.findall(trecho)))}, o impacto dá {sorted(us_esperadas)}")
            numero = re.search(r"(\d+) critérios? de aceite", trecho)
            if not numero or int(numero[1]) != len(i.cas):
                erros.append(f"{dec}: Artefatos afetados diz {numero[1] if numero else '?'} CAs, o impacto dá {len(i.cas)}")
        if dec in pauta:
            tas = len([t for ca in i.cas if (t := ta_de(ca, por_id))])
            if pauta[dec] != (len(i.cas), tas):
                erros.append(f"pauta-aula-7.md {dec}: diz {pauta[dec][0]} CAs e {pauta[dec][1]} TAs, o impacto dá {len(i.cas)} e {tas}")
    pendentes = [d for d, v in modelo.decs.items() if v["estado"] != "Decidida"]
    erros += [f"pauta-aula-7.md: {d} sem a contagem 'N CAs e M TAs'" for d in pendentes if PAUTA.exists() and d not in pauta]
    for linha in secao(ler(SRS), r"6\.3").splitlines():
        if achado := re.match(r"^\| \[(DEC-\d{2})\]\([^)]*\) \| [^|]+ \| ([^|]*) \|", linha):
            na_srs = set(expandir(achado[2], modelo.ordem))
            if achado[1] in tudo and na_srs != set(tudo[achado[1]].rfs):
                erros.append(f"SRS 6.3 {achado[1]}: {ordenar(na_srs)}; campo Decisões das fichas: {tudo[achado[1]].rfs}")
    print(f"DECs conferidas: {len(modelo.decs)}; na pauta com contagem: {len(pauta)}")
    return erros


def verificar_regras(modelo: Modelo) -> list[str]:
    erros = []
    if not modelo.rns:
        return ["catálogo de regras de negócio ausente ou sem linhas RN-xx"]
    citados = {}
    for r in modelo.rfs.values():
        for rn in r.rns:
            citados.setdefault(rn, set()).add(r.id)
            if rn not in modelo.rns:
                erros.append(f"{r.id}: cita {rn}, que não está no catálogo")
    numeros = sorted(chave(i)[0] for i in modelo.rns)
    if numeros != list(range(1, len(numeros) + 1)):
        erros.append("IDs do catálogo fora de sequência ou repetidos (um RN nunca é reutilizado)")
    for identificador, rn in modelo.rns.items():
        if not rn["rfs"]:
            erros.append(f"{identificador}: não cita nenhum RF")
        if not ID_DEC.search(sem_links(rn["fonte"])) and "glossário" not in rn["fonte"] and "RF-" not in sem_links(rn["fonte"]):
            erros.append(f"{identificador}: sem fonte (glossário, RF ou DEC)")
        for rf in rn["rfs"]:
            if rf not in modelo.rfs:
                erros.append(f"{identificador}: cita {rf}, que não existe")
            elif identificador not in modelo.rfs[rf].rns:
                erros.append(f"{identificador}: lista {rf}, mas a ficha do {rf} não cita {identificador} em 'Regras de negócio'")
        for rf in citados.get(identificador, set()) - set(rn["rfs"]):
            erros.append(f"{rf}: cita {identificador}, que não lista o {rf} no catálogo")
    print(f"Regras de negócio: {len(modelo.rns)}; RF que citam alguma: {len({rf for v in citados.values() for rf in v})}")
    return erros


def documentos_da_fonte() -> list[Path]:
    return sorted(PASTA.rglob("*.md"), key=lambda a: a.relative_to(PASTA).as_posix())


def verificar_cabecalhos() -> list[str]:
    erros = []
    gerados = {p.name for p in (PASTA_RAS / n for n in ("matriz.md", "cobertura.md", "sentido-inverso.md", "rnf.md", "impacto-por-dec.md", "regras-de-negocio.md"))}
    for arquivo in documentos_da_fonte():
        texto = ler(arquivo)
        caminho = arquivo.relative_to(PASTA).as_posix()
        if ler_cabecalho(arquivo) is None:
            erros.append(f"{caminho}: sem '**ID • versão • estado**'")
        if not re.search(r"Autor:.*Revisor:.*Aprovador:", texto):
            erros.append(f"{caminho}: sem 'Autor • Revisor • Aprovador'")
        if arquivo.parent == PASTA_RAS and arquivo.name in gerados:
            if AVISO not in texto or "Parte da [RAS-01]" not in texto:
                erros.append(f"{caminho}: arquivo gerado sem o aviso ou sem 'Parte da RAS-01'")
            continue
        historico = re.search(r"^## Histórico[^\n]*\n+\|[^\n]*Versão[^\n]*\|\n\|[-|]+\|\n\|", texto, flags=re.M)
        if not historico:
            erros.append(f"{caminho}: sem '## Histórico' com tabela")
    print(f"Documentos da fonte conferidos: {len(documentos_da_fonte())}")
    return erros


def verificar_candidata(modelo: Modelo) -> list[str]:
    if not CANDIDATA.exists():
        return [f"{CANDIDATA.name} não existe"]
    texto = normalizar(ler(CANDIDATA))
    blocos = blocos_da_candidata(modelo)
    erros = []
    for nome, conteudo in blocos.items():
        achado = re.search(rf"<!-- {nome}:inicio -->\n((?:.*?\n)?)<!-- {nome}:fim -->", texto, flags=re.S)
        if not achado:
            erros.append(f"candidata: sem os marcadores do bloco {nome}")
        elif achado[1] != conteudo + "\n":
            if nome == "manifesto":
                antigos = set(achado[1].splitlines())
                for linha in conteudo.splitlines():
                    if linha.startswith("| ") and linha not in antigos and "`" in linha:
                        erros.append(f"manifesto desatualizado: {linha.split('`')[1]} (rode --manifesto)")
                if not any(e.startswith("manifesto") for e in erros):
                    erros.append("manifesto desatualizado (artefato removido ou cabeçalho mudou; rode --manifesto)")
            else:
                erros.append(f"candidata: bloco {nome} desatualizado (rode --manifesto)")
    print(f"Artefatos no manifesto: {len(artefatos_do_manifesto())}")
    return erros


def verificar_gerados(gerados: dict[Path, str]) -> list[str]:
    erros = []
    for caminho, conteudo in gerados.items():
        if not caminho.exists():
            erros.append(f"{caminho.relative_to(RAIZ).as_posix()} não existe: rode o gerador")
        elif normalizar(ler(caminho)) != conteudo:
            erros.append(f"{caminho.relative_to(RAIZ).as_posix()} está desatualizado em relação às fichas: rode o gerador")
    print(f"Arquivos gerados conferidos: {len(gerados)}")
    return erros
    

def escrever(caminho: Path, conteudo: str) -> bool:
    if caminho.exists() and normalizar(ler(caminho)) == conteudo:
        return False
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="utf-8", newline="\n") as saida:
        saida.write(conteudo)
    return True


def main() -> int:
    modelo = carregar()
    gerados = arquivos_gerados(modelo)
    if "--manifesto" in sys.argv:
        texto = normalizar(ler(CANDIDATA))
        mudou = escrever(CANDIDATA, aplicar_blocos(texto, blocos_da_candidata(modelo)))
        print(f"{CANDIDATA.relative_to(RAIZ).as_posix()}: {'atualizado' if mudou else 'sem mudança'}")
        return 0
    if "--verificar" not in sys.argv:
        alterados = [c for c, conteudo in gerados.items() if escrever(c, conteudo)]
        for caminho in gerados:
            print(f"{caminho.relative_to(RAIZ).as_posix()}: {'atualizado' if caminho in alterados else 'sem mudança'}")
        print(f"{len(alterados)} arquivos alterados")
        return 0
    verificacoes = [
        ("0. Arquivos gerados batem com as fontes", lambda: verificar_gerados(gerados)),
        ("a. NS → TA e RF com UC, US e CA (ou lacuna)", lambda: verificar_cadeia(modelo)),
        ("b. CA com TA e testes citados existem", lambda: verificar_testes_citados(modelo)),
        ("c. Sentido inverso: rotas e telas com RF, RNF ou lacuna", lambda: verificar_inverso(modelo)),
        ("d. Símbolos de código existem", lambda: verificar_codigo(modelo)),
        ("e. DECs completas e no mapa de impacto", lambda: verificar_decs(modelo, gerados[PASTA_RAS / "impacto-por-dec.md"])),
        ("f. Cabeçalho e histórico de todos os documentos", verificar_cabecalhos),
        ("g. Manifesto da baseline candidata", lambda: verificar_candidata(modelo)),
        ("h. Regras de negócio ligadas aos RF", lambda: verificar_regras(modelo)),
    ]
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
