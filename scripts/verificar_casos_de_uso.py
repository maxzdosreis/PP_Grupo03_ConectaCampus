from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verificar_requisitos import PASTA, fichas_de_rf, ler, relativo  # noqa: E402

PASTA_UC = PASTA / "casos-de-uso"
README_UC = PASTA_UC / "README.md"
SRS = PASTA / "requisitos" / "srs.md"
DIAGRAMAS = sorted(PASTA_UC.glob("*.puml"))

ID_UC = re.compile(r"UC-\d{2}")
ATOR = re.compile(r'^\s*actor\s+(?:"(?P<rotulo>[^"]+)"\s+as\s+)?(?P<alias>\w+)\s*$')
CASO = re.compile(r'^\s*usecase\s+"(?P<rotulo>[^"]+)"\s+as\s+(?P<alias>\w+)(?:\s+<<(?P<estereotipo>[^>]+)>>)?\s*$')
NOTA = re.compile(r'^\s*note\s+"[^"]*"\s+as\s+(?P<alias>\w+)\s*$')
LIGACAO = re.compile(r"^\s*(?P<origem>\w+)\s+(?P<seta><?\|?[-.]+(?:\[\w+\][-.]+)?\|?>?)\s+(?P<destino>\w+)\s*(?::\s*(?P<rotulo>.*))?$")
PONTO_CITADO = re.compile(r"<<extend>>\\n\((?P<ponto>[^)]+)\)")
LINHA_DO_INDICE = re.compile(r'^\|\s*<a id="(?P<ancora>uc-\d{2})"></a>(?P<id>UC-\d{2})\s*\|\s*(?P<nome>[^|]+?)\s*\|')
LINHA_RF_UC = re.compile(r"^\|\s*\[(?P<rf>RF-[\d.]+)\]\([^)]*\)\s*\|\s*(?P<titulo>[^|]+?)\s*\|\s*(?P<uc>[^|]+?)\s*\|\s*(?P<como>[^|]+?)\s*\|\s*(?P<tambem>[^|]+?)\s*\|")
LINHA_DO_RESUMO = re.compile(r"^\|\s*\[(?P<rf>RF-[\d.]+)\]\([^)]*\)\s*\|\s*(?P<titulo>[^|]+?)\s*\|\s*NS-")
LINHA_DA_64 = re.compile(r"^\|\s*(?P<rf>RF-[\d.]+)\s*\|\s*`?[^|]*\|\s*(?P<uc>[^|]*?)\s*\|\s*[^|]*\|\s*[^|]*\|\s*$")
COMO_ENTRA = ("fluxo principal", "alternativa", "exceção", "transversal")


@dataclass
class CasoDeUso:
    id: str
    nome: str
    alias: str
    diagrama: str
    subfuncao: bool
    pontos_de_extensao: list[str] = field(default_factory=list)


@dataclass
class Ligacao:
    origem: str
    destino: str
    tipo: str
    rotulo: str
    linha: str


@dataclass
class Diagrama:
    arquivo: Path
    atores: dict[str, str] = field(default_factory=dict)
    casos: dict[str, CasoDeUso] = field(default_factory=dict)
    notas: set[str] = field(default_factory=set)
    ligacoes: list[Ligacao] = field(default_factory=list)


def _nome_e_pontos(rotulo: str) -> tuple[str, str, list[str]]:
    partes = rotulo.split("\\n--\\n")
    titulo = partes[0].split("\\n")[0].replace("//", "").strip()
    identificador = ID_UC.match(titulo)
    if not identificador:
        raise ValueError(f"caso de uso sem ID visível: {rotulo!r}")
    nome = titulo[identificador.end() :].strip()
    pontos = []
    if len(partes) > 1:
        linhas = [linha.strip() for linha in partes[1].split("\\n")]
        pontos = [linha for linha in linhas if linha and not linha.lower().startswith("pontos de extensão")]
    return identificador.group(0), nome, pontos


def _tipo_da_seta(seta: str, rotulo: str) -> str:
    if "[hidden]" in seta:
        return "invisivel"
    if "|>" in seta or "<|" in seta:
        return "generalizacao"
    if "." in seta:
        if "<<include>>" in rotulo:
            return "include"
        if "<<extend>>" in rotulo:
            return "extend"
        return "pontilhada"
    if ">" in seta or "<" in seta:
        return "outra"
    return "associacao"


def ler_diagrama(arquivo: Path) -> Diagrama:
    diagrama = Diagrama(arquivo)
    dentro_da_legenda = False
    for linha in ler(arquivo).splitlines():
        if linha.strip().startswith("'"):
            continue
        if linha.strip().startswith("legend"):
            dentro_da_legenda = True
        if dentro_da_legenda:
            dentro_da_legenda = not linha.strip().startswith("endlegend")
            continue
        if achado := ATOR.match(linha):
            diagrama.atores[achado["alias"]] = achado["rotulo"] or achado["alias"]
        elif achado := CASO.match(linha):
            identificador, nome, pontos = _nome_e_pontos(achado["rotulo"])
            diagrama.casos[achado["alias"]] = CasoDeUso(
                identificador, nome, achado["alias"], arquivo.name, achado["estereotipo"] == "subfunção", pontos
            )
        elif achado := NOTA.match(linha):
            diagrama.notas.add(achado["alias"])
        elif achado := LIGACAO.match(linha):
            seta, rotulo = achado["seta"], (achado["rotulo"] or "").strip()
            origem, destino = achado["origem"], achado["destino"]
            if seta.startswith("<"):
                origem, destino = destino, origem
            diagrama.ligacoes.append(Ligacao(origem, destino, _tipo_da_seta(seta, rotulo), rotulo, linha.strip()))
    for ligacao in diagrama.ligacoes:
        if ligacao.tipo not in ("invisivel",) and diagrama.notas & {ligacao.origem, ligacao.destino}:
            ligacao.tipo = "nota"
    return diagrama


def casos_dos_diagramas(diagramas: list[Diagrama]) -> list[CasoDeUso]:
    return [caso for diagrama in diagramas for caso in diagrama.casos.values()]


def indice_do_readme() -> dict[str, str]:
    indice = {}
    for linha in ler(README_UC).splitlines():
        if achado := LINHA_DO_INDICE.match(linha):
            nome = achado["nome"].replace("*", "").replace("{abstrato}", "").strip()
            if achado["ancora"] != achado["id"].lower():
                raise ValueError(f"âncora {achado['ancora']} não bate com {achado['id']}")
            indice[achado["id"]] = nome
    return indice


def verificar_ucs(diagramas: list[Diagrama]) -> list[str]:
    erros = []
    casos = casos_dos_diagramas(diagramas)
    indice = indice_do_readme()
    vistos: dict[str, str] = {}
    for caso in casos:
        if caso.id in vistos:
            erros.append(f"{caso.id} aparece em {vistos[caso.id]} e em {caso.diagrama}")
        vistos[caso.id] = caso.diagrama
        if caso.id not in indice:
            erros.append(f"{caso.id} ({caso.diagrama}) não está no índice do README")
        elif indice[caso.id] != caso.nome:
            erros.append(f"{caso.id}: nome no diagrama {caso.nome!r} ≠ no índice {indice[caso.id]!r}")
    for identificador in sorted(set(indice) - set(vistos)):
        erros.append(f"{identificador} está no índice do README, mas em nenhum diagrama")
    for diagrama in diagramas:
        ids = sorted(caso.id for caso in diagrama.casos.values())
        print(f"{diagrama.arquivo.name}: {len(diagrama.atores)} atores, {len(ids)} casos de uso ({ids[0]} a {ids[-1]})")
    print(f"Índice do README: {len(indice)} casos de uso")
    return erros


def resumo_da_srs() -> dict[str, str]:
    return {a["rf"]: a["titulo"] for linha in ler(SRS).splitlines() if (a := LINHA_DO_RESUMO.match(linha))}


def tabela_rf_uc() -> dict[str, list[dict]]:
    tabela: dict[str, list[dict]] = {}
    for linha in ler(README_UC).splitlines():
        if achado := LINHA_RF_UC.match(linha):
            tabela.setdefault(achado["rf"], []).append(achado.groupdict())
    return tabela


def uc_principal(celula: str) -> str | None:
    achado = ID_UC.search(celula)
    return achado.group(0) if achado else None


def verificar_rf_uc(diagramas: list[Diagrama]) -> list[str]:
    erros = []
    existentes = {caso.id for caso in casos_dos_diagramas(diagramas)}
    resumo = resumo_da_srs()
    tabela = tabela_rf_uc()
    for rf, titulo in resumo.items():
        linhas = tabela.get(rf, [])
        if len(linhas) != 1:
            erros.append(f"{rf} aparece {len(linhas)} vezes na tabela RF → UC (esperado: 1)")
            continue
        linha = linhas[0]
        if linha["titulo"] != titulo:
            erros.append(f"{rf}: título {linha['titulo']!r} ≠ SRS {titulo!r}")
        if not linha["como"].startswith(COMO_ENTRA):
            erros.append(f"{rf}: 'como entra' fora de {COMO_ENTRA}: {linha['como']!r}")
        uc = uc_principal(linha["uc"])
        if uc is None and not linha["como"].startswith("transversal"):
            erros.append(f"{rf}: sem UC e sem ser transversal")
        if uc and uc not in existentes:
            erros.append(f"{rf}: cita {uc}, que não existe nos diagramas")
    for rf in sorted(set(tabela) - set(resumo)):
        erros.append(f"{rf} está na tabela RF → UC, mas não na tabela-resumo da SRS")
    citados = {uc for linhas in tabela.values() for uc in ID_UC.findall(linhas[0]["uc"] + linhas[0]["tambem"])}
    for uc in sorted(existentes - citados):
        erros.append(f"{uc} não cobre nenhum RF (nem como principal, nem em 'também em')")
    papeis = {}
    for linhas in tabela.values():
        papel = linhas[0]["como"].split(" (")[0]
        papeis[papel] = papeis.get(papel, 0) + 1
    print(f"RF na tabela-resumo da SRS: {len(resumo)}; na tabela RF → UC: {len(tabela)}")
    print("Como entram:", ", ".join(f"{papel} {n}" for papel, n in sorted(papeis.items())))
    return erros


def verificar_fichas_e_srs() -> list[str]:
    erros = []
    tabela = {rf: uc_principal(ls[0]["uc"]) for rf, ls in tabela_rf_uc().items()}
    fichas = fichas_de_rf()
    for ficha in fichas:
        vinculo = ficha["campos"].get("Vínculos", "")
        origem = f"{ficha['id']} ({relativo(ficha['arquivo'])}:{ficha['linha']})"
        if "a definir (REQ-03" in vinculo or not vinculo.startswith("UC:"):
            erros.append(f"{origem}: UC não preenchido no campo Vínculos")
            continue
        uc = uc_principal(vinculo)
        if uc != tabela.get(ficha["id"]):
            erros.append(f"{origem}: UC {uc} ≠ tabela RF → UC {tabela.get(ficha['id'])}")
        if uc is None and "transversal" not in vinculo:
            erros.append(f"{origem}: sem UC e sem ser transversal")
    linhas_64 = {a["rf"]: a["uc"] for linha in ler(SRS).splitlines() if (a := LINHA_DA_64.match(linha))}
    for rf, uc_tabela in tabela.items():
        celula = linhas_64.get(rf)
        if celula is None:
            erros.append(f"{rf}: sem linha na SRS, seção 6.4")
        elif not celula:
            erros.append(f"{rf}: coluna UC vazia na SRS, seção 6.4")
        elif uc_principal(celula) != uc_tabela:
            erros.append(f"{rf}: SRS 6.4 diz {celula!r}, a tabela RF → UC diz {uc_tabela}")
    print(f"Fichas com UC: {len(fichas)}; linhas da SRS 6.4 com UC: {sum(1 for c in linhas_64.values() if c)}")
    return erros


def verificar_notacao(diagramas: list[Diagrama]) -> list[str]:
    erros = []
    contagem: dict[str, int] = {}
    for diagrama in diagramas:
        nome = diagrama.arquivo.name
        casos, atores = diagrama.casos, diagrama.atores
        ligados: set[str] = set()
        associados: set[str] = set()
        for ligacao in diagrama.ligacoes:
            contagem[ligacao.tipo] = contagem.get(ligacao.tipo, 0) + 1
            if ligacao.tipo in ("invisivel", "nota"):
                continue
            ponta = {ligacao.origem, ligacao.destino}
            desconhecidas = ponta - set(casos) - set(atores)
            if desconhecidas:
                erros.append(f"{nome}: ligação com elemento desconhecido {sorted(desconhecidas)}: {ligacao.linha}")
                continue
            ligados |= ponta
            entre_casos = ponta <= set(casos)
            entre_atores = ponta <= set(atores)
            if entre_casos and ligacao.tipo not in ("include", "extend", "generalizacao"):
                erros.append(f"{nome}: seta entre casos de uso fora de include, extend ou generalização: {ligacao.linha}")
            elif entre_atores and ligacao.tipo != "generalizacao":
                erros.append(f"{nome}: ligação entre atores que não é generalização: {ligacao.linha}")
            elif not entre_casos and not entre_atores:
                if ligacao.tipo != "associacao":
                    erros.append(f"{nome}: ator e caso de uso ligados por algo que não é associação: {ligacao.linha}")
                associados |= ponta & set(casos)
            if ligacao.tipo == "extend":
                erros += _conferir_extend(nome, ligacao, casos)
        for alias, caso in casos.items():
            if alias not in ligados:
                erros.append(f"{nome}: {caso.id} solto, sem ator nem relação")
            if caso.subfuncao and alias in associados:
                erros.append(f"{nome}: {caso.id} é subfunção e não pode ter ator próprio")
            if caso.pontos_de_extensao and not any(
                ligacao.tipo == "extend" and ligacao.destino == alias for ligacao in diagrama.ligacoes
            ):
                erros.append(f"{nome}: {caso.id} declara ponto de extensão sem nenhum extend")
    print("Ligações por tipo:", ", ".join(f"{tipo} {n}" for tipo, n in sorted(contagem.items())))
    print("  (invisivel = só de layout, ignorada; nota = ligação de nota UML)")
    return erros


def _conferir_extend(nome: str, ligacao: Ligacao, casos: dict[str, CasoDeUso]) -> list[str]:
    citado = PONTO_CITADO.search(ligacao.rotulo)
    base = casos[ligacao.destino]
    if not citado:
        return [f"{nome}: extend sem ponto de extensão nomeado: {ligacao.linha}"]
    if citado["ponto"] not in base.pontos_de_extensao:
        return [f"{nome}: extend cita {citado['ponto']!r}, que {base.id} não declara ({base.pontos_de_extensao})"]
    print(f"  extend {casos[ligacao.origem].id} → {base.id} no ponto {citado['ponto']!r}: declarado")
    return []


def _ligacoes_do_svg(svg: str) -> set[frozenset[str]]:
    return {frozenset(par) for par in re.findall(r"<!--(?:reverse )?link (\w+) to (\w+)-->", svg)}


def verificar_imagens(diagramas: list[Diagrama]) -> list[str]:
    erros = []
    for diagrama in diagramas:
        svg_arquivo = diagrama.arquivo.with_suffix(".svg")
        png_arquivo = diagrama.arquivo.with_suffix(".png")
        for imagem in (svg_arquivo, png_arquivo):
            if not imagem.exists():
                erros.append(f"{relativo(imagem)} não existe: gere as imagens (README da pasta)")
        if not svg_arquivo.exists():
            continue
        svg = ler(svg_arquivo)
        entidades = set(re.findall(r"<!--entity (\w+)-->", svg))
        esperadas = set(diagrama.casos) | set(diagrama.atores)
        visiveis = {frozenset((lig.origem, lig.destino)) for lig in diagrama.ligacoes if lig.tipo != "invisivel"}
        if entidades != esperadas or visiveis != _ligacoes_do_svg(svg):
            erros.append(f"{relativo(svg_arquivo)} está desatualizado em relação ao .puml: gere as imagens de novo")
        elif not all(caso.id in svg for caso in diagrama.casos.values()):
            erros.append(f"{relativo(svg_arquivo)} não mostra todos os IDs: gere as imagens de novo")
        else:
            print(f"{svg_arquivo.name}: {len(entidades)} elementos e {len(visiveis)} ligações, iguais ao .puml")
    return erros


def main() -> int:
    diagramas = [ler_diagrama(arquivo) for arquivo in DIAGRAMAS]
    verificacoes = [
        ("1. Casos de uso: diagramas ↔ índice do README", lambda: verificar_ucs(diagramas)),
        ("2. RF → UC: tabela-resumo da SRS ↔ tabela do README", lambda: verificar_rf_uc(diagramas)),
        ("3. UC nas fichas rf-*.md e na SRS (seção 6.4)", verificar_fichas_e_srs),
        ("4. Notação UML dos diagramas", lambda: verificar_notacao(diagramas)),
        ("5. Imagens geradas", lambda: verificar_imagens(diagramas)),
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
