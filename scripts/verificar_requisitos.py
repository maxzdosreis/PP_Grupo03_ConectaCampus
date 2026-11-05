"""Confere a fonte oficial de requisitos (docs/fontes/requisitos/).

Verificações:
  1. Rastreabilidade: toda NS da Visão é origem principal de pelo menos um RF,
     e todo RF tem uma NS de origem que existe.
  2. Sintaxe: todo enunciado de RF começa com "O sistema deve permitir ao";
     os de recusa (F5) começam com "O sistema deve impedir que".
  3. Termos vagos nos enunciados e textos da SRS, das fichas de RF e dos RNF.
  4. Links relativos e âncoras de todos os .md da pasta.

Uso, na raiz do repositório:  python scripts/verificar_requisitos.py
Sai com código 1 se alguma verificação falhar. Não depende de pacotes externos.
"""

from __future__ import annotations

import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "docs" / "fontes" / "requisitos"
PASTA_RF = PASTA / "requisitos"

SINTAXE_RF = "O sistema deve permitir ao"
SINTAXE_RF_FEMININO = "O sistema deve permitir à"
SINTAXE_RECUSA = "O sistema deve impedir que"

TERMOS_VAGOS = {
    "rapidamente": r"rapidamente",
    "rápido": r"r[aá]pid[oa]s?\b",
    "fácil": r"f[aá]ce?i[ls]",
    "adequad": r"adequad",
    "amigável": r"amig[aá]vel",
    "disponíve": r"dispon[ií]ve",
    "etc": r"\betc\b",
    "avisar": r"\bavis(ar|a|am|ou|ará|aria)\b",
    "com sucesso": r"com sucesso",
}
EXCECOES_DE_TERMO = [r"aç(ão|ões) dispon[ií]ve(l|is)"]

ANCORA_FICHA = re.compile(r'<a id="(r(?:n)?f-[\w-]+)"></a>((?:RF|RNF)-[\w.]+)')
LINHA_DA_FICHA = re.compile(r"^\|\s*\*\*(?P<campo>[^*]+)\*\*\s*\|\s*(?P<valor>.*)\|\s*$")
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
ID_HTML = re.compile(r'<a id="([^"]+)"')
TITULO = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def ler(caminho: Path) -> str:
    return caminho.read_text(encoding="utf-8")


def relativo(caminho: Path) -> str:
    return caminho.relative_to(RAIZ).as_posix()


def fichas(arquivo: Path) -> list[dict]:
    resultado = []
    atual = None
    for numero, linha in enumerate(ler(arquivo).splitlines(), start=1):
        achado = ANCORA_FICHA.search(linha)
        if achado and linha.lstrip().startswith("#"):
            atual = {"id": achado.group(2), "arquivo": arquivo, "linha": numero, "campos": {}}
            resultado.append(atual)
            continue
        if atual is None:
            continue
        campo = LINHA_DA_FICHA.match(linha)
        if campo:
            atual["campos"][campo.group("campo").strip()] = campo.group("valor").strip()
    return resultado


def fichas_de_rf() -> list[dict]:
    return [f for arquivo in sorted(PASTA_RF.glob("rf-*.md")) for f in fichas(arquivo)]


def fichas_de_rnf() -> list[dict]:
    return fichas(PASTA_RF / "rnf.md")


def necessidades_da_visao() -> list[str]:
    encontradas = re.findall(r'^\|\s*(?:<a id="ns-\d{2}"></a>)?(NS-\d{2})\s*\|', ler(PASTA / "visao.md"), flags=re.M)
    return list(dict.fromkeys(encontradas))


def verificar_rastreabilidade(rfs: list[dict]) -> list[str]:
    erros = []
    necessidades = necessidades_da_visao()
    origem_principal: dict[str, list[str]] = defaultdict(list)
    for ficha in rfs:
        origem = ficha["campos"].get("Origem", "")
        citadas = re.findall(r"NS-\d{2}", origem)
        if not citadas:
            erros.append(f"{ficha['id']} sem NS de origem ({relativo(ficha['arquivo'])}:{ficha['linha']})")
            continue
        for ns in citadas:
            if ns not in necessidades:
                erros.append(f"{ficha['id']} cita {ns}, que não existe na Visão")
        origem_principal[citadas[0]].append(ficha["id"])

    print("NS → RF (origem principal):")
    for ns in necessidades:
        rfs_da_ns = origem_principal.get(ns, [])
        print(f"  {ns}: {', '.join(rfs_da_ns) if rfs_da_ns else '— NENHUM'}")
        if not rfs_da_ns:
            erros.append(f"{ns} não é origem principal de nenhum RF")
    print(f"  {len(necessidades)} NS na Visão; {len(rfs)} RF com origem.")
    return erros


def verificar_sintaxe(rfs: list[dict]) -> list[str]:
    erros = []
    grupos: dict[str, list[str]] = defaultdict(list)
    for ficha in rfs:
        enunciado = ficha["campos"].get("Enunciado", "")
        for sintaxe in (SINTAXE_RF, SINTAXE_RF_FEMININO, SINTAXE_RECUSA):
            if enunciado.startswith(sintaxe):
                grupos[sintaxe].append(ficha["id"])
                break
        else:
            erros.append(f"{ficha['id']}: enunciado fora das sintaxes: {enunciado[:60]!r}")
    print(f'Começam com "{SINTAXE_RF}": {len(grupos[SINTAXE_RF])}')
    print(f'Começam com "{SINTAXE_RF_FEMININO}" (ator no feminino): {len(grupos[SINTAXE_RF_FEMININO])}')
    print(f"  {', '.join(grupos[SINTAXE_RF_FEMININO])}")
    print(f'Recusas (F5), com "{SINTAXE_RECUSA}" (justificativa na SRS, seção 3): {len(grupos[SINTAXE_RECUSA])}')
    print(f"  {', '.join(grupos[SINTAXE_RECUSA])}")
    return erros


def _sem_trechos_literais(linha: str) -> str:
    linha = re.sub(r"`[^`]*`", " ", linha)
    linha = re.sub(r"\]\([^)]*\)", "] ", linha)
    linha = re.sub(r'"[^"]*"', " ", linha)
    linha = re.sub(r"“[^”]*”", " ", linha)
    for excecao in EXCECOES_DE_TERMO:
        linha = re.sub(excecao, " ", linha, flags=re.I)
    return linha


def verificar_termos_vagos() -> list[str]:
    erros = []
    arquivos = [PASTA_RF / "srs.md", PASTA_RF / "rnf.md", *sorted(PASTA_RF.glob("rf-*.md"))]
    ignoradas = Counter()
    for arquivo in arquivos:
        for numero, linha in enumerate(ler(arquivo).splitlines(), start=1):
            limpa = _sem_trechos_literais(linha)
            for termo, padrao in TERMOS_VAGOS.items():
                total = len(re.findall(padrao, linha, flags=re.I))
                fora = len(re.findall(padrao, limpa, flags=re.I))
                if total > fora:
                    ignoradas[termo] += total - fora
                if fora:
                    erros.append(f"{relativo(arquivo)}:{numero}: termo vago {termo!r}")
    if ignoradas:
        print("Ocorrências aceitas (dentro de código, de mensagem literal do sistema entre aspas")
        print('ou no termo do glossário "ação disponível"):')
        for termo, quantidade in sorted(ignoradas.items()):
            print(f"  {termo}: {quantidade}")
    print(f"Arquivos lidos: {len(arquivos)}; termos vagos fora dessas exceções: {len(erros)}")
    return erros


def _slug(titulo: str) -> str:
    titulo = re.sub(r"<[^>]+>", "", titulo)
    titulo = re.sub(r"`", "", titulo)
    titulo = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", titulo)
    titulo = titulo.strip().lower()
    permitido = []
    for caractere in titulo:
        categoria = unicodedata.category(caractere)
        if caractere in "-_ " or categoria[0] in "LN":
            permitido.append(caractere)
    return "".join(permitido).replace(" ", "-")


def ancoras(arquivo: Path) -> set[str]:
    encontradas = set()
    repetidas = Counter()
    dentro_de_codigo = False
    for linha in ler(arquivo).splitlines():
        if linha.strip().startswith("```"):
            dentro_de_codigo = not dentro_de_codigo
            continue
        if dentro_de_codigo:
            continue
        encontradas.update(ID_HTML.findall(linha))
        titulo = TITULO.match(linha)
        if titulo:
            base = _slug(titulo.group(2))
            sufixo = f"-{repetidas[base]}" if repetidas[base] else ""
            repetidas[base] += 1
            encontradas.add(base + sufixo)
    return encontradas


def verificar_links() -> list[str]:
    erros = []
    cache: dict[Path, set[str]] = {}
    total = 0
    arquivos = sorted(PASTA.rglob("*.md"))
    for arquivo in arquivos:
        dentro_de_codigo = False
        for numero, linha in enumerate(ler(arquivo).splitlines(), start=1):
            if linha.strip().startswith("```"):
                dentro_de_codigo = not dentro_de_codigo
            if dentro_de_codigo:
                continue
            for alvo in LINK.findall(re.sub(r"`[^`]*`", "", linha)):
                if re.match(r"^[a-z]+:", alvo):
                    continue
                total += 1
                caminho, _, ancora = alvo.partition("#")
                destino = (arquivo.parent / caminho).resolve() if caminho else arquivo
                origem = f"{relativo(arquivo)}:{numero}"
                if not destino.exists():
                    erros.append(f"{origem}: arquivo inexistente {alvo}")
                    continue
                if ancora and destino.suffix == ".md":
                    if destino not in cache:
                        cache[destino] = ancoras(destino)
                    if ancora not in cache[destino]:
                        erros.append(f"{origem}: âncora inexistente {alvo}")
    print(f"Arquivos .md: {len(arquivos)}; links relativos conferidos: {total}; quebrados: {len(erros)}")
    return erros


def imprimir_contagens(rfs: list[dict], rnfs: list[dict]) -> None:
    por_arquivo = Counter(f["arquivo"].stem for f in rfs)
    principais = sum(1 for f in rfs if "." not in f["id"])
    print(f"RF: {len(rfs)} fichas ({principais} principais, {len(rfs) - principais} filhos)")
    for arquivo, quantidade in sorted(por_arquivo.items()):
        print(f"  {arquivo}: {quantidade}")
    por_furps = Counter(f["id"].split("-")[1][0] for f in rnfs)
    nomes = {"F": "Funcionalidade", "U": "Usabilidade", "R": "Confiabilidade", "P": "Desempenho", "S": "Suportabilidade"}
    print(f"RNF: {len(rnfs)}")
    for letra in "FURPS":
        print(f"  {letra} ({nomes[letra]}): {por_furps[letra]}")
    print("QFD:", dict(Counter(_qfd(f) for f in rfs)))
    print("Funcionalidade:", dict(sorted(Counter(_funcionalidade(f) for f in rfs).items())))


def _qfd(ficha: dict) -> str:
    return ficha["campos"].get("Prioridade (QFD)", "?").split(" ")[0]


def _funcionalidade(ficha: dict) -> str:
    valor = ficha["campos"].get("Funcionalidade", "?")
    return "Extra" if valor.startswith("Extra") else valor.split(" ")[0]


def main() -> int:
    rfs = fichas_de_rf()
    rnfs = fichas_de_rnf()
    verificacoes = [
        ("1. Rastreabilidade NS ↔ RF", lambda: verificar_rastreabilidade(rfs)),
        ("2. Sintaxe dos enunciados", lambda: verificar_sintaxe(rfs)),
        ("3. Termos vagos", verificar_termos_vagos),
        ("4. Links e âncoras", verificar_links),
    ]
    print("== Contagens ==")
    imprimir_contagens(rfs, rnfs)
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
