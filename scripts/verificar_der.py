from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verificar_visao_do_sistema as visao  # noqa: E402

GERADOR = visao.RAIZ / "scripts" / "gerar_der.py"
ARQUIVO_MMD = "der-do-banco.mmd"
ARQUIVO_TEXTO = "05-der-do-banco.md"
INICIO_DA_TABELA = "<!-- der:restricoes:inicio -->"
FIM_DA_TABELA = "<!-- der:restricoes:fim -->"

TIPOS_COMPATIVEIS = {
    "bigint": ("bigint", "bigserial"),
    "varchar": ("varchar",),
    "integer": ("integer",),
    "smallint": ("smallint",),
    "boolean": ("boolean", "bool"),
    "timestamptz": ("timestamp with time zone", "timestamptz"),
}

RE_ENTIDADE = re.compile(r"^\s{4}(\w+) \{$")
RE_COLUNA = re.compile(r'^\s{8}(\w+) (\w+)((?: (?:PK|FK|UK)(?:, (?:PK|FK|UK))*)?)(?: "([^"]*)")?$')
RE_RELACAO = re.compile(r'^\s{4}(\w+) (\|o|\|\|)(--|\.\.)o\{ (\w+) : "([^"]*)"$')


def ler_texto(caminho: Path) -> str:
    return caminho.read_text(encoding="utf-8").replace("\r\n", "\n")


def estrutura_dos_models(arquivo_json: Path | None) -> dict:
    if arquivo_json is not None:
        return json.loads(arquivo_json.read_text(encoding="utf-8"))
    comando = ["docker", "compose", "exec", "-T", "backend", "python", "-", "--json"]
    with GERADOR.open("rb") as script:
        pronto = subprocess.run(comando, cwd=visao.RAIZ / "src", stdin=script, capture_output=True)
    if pronto.returncode != 0:
        raise SystemExit(
            "O gerador falhou (o container do backend precisa estar no ar: `docker compose up -d`):\n"
            + pronto.stderr.decode("utf-8", "replace")
        )
    return json.loads(pronto.stdout.decode("utf-8"))


def ler_desenho(texto: str) -> tuple[dict, list]:
    tabelas: dict[str, dict] = {}
    relacoes = []
    atual = None
    for linha in texto.splitlines():
        if atual is None:
            if (m := RE_ENTIDADE.match(linha)):
                atual = m.group(1)
                tabelas[atual] = {}
            elif (m := RE_RELACAO.match(linha)):
                relacoes.append((m.group(1), m.group(3), m.group(4), m.group(5)))
        elif linha.strip() == "}":
            atual = None
        elif (m := RE_COLUNA.match(linha)):
            marcas = [x.strip() for x in m.group(3).split(",") if x.strip()]
            tabelas[atual][m.group(2)] = (m.group(1), marcas, m.group(4) or "")
    return tabelas, relacoes


def tabela_do_texto(texto: str) -> str | None:
    if INICIO_DA_TABELA not in texto or FIM_DA_TABELA not in texto:
        return None
    meio = texto.split(INICIO_DA_TABELA, 1)[1].split(FIM_DA_TABELA, 1)[0]
    return meio.strip("\n") + "\n"


def verificar(pasta: Path, estrutura: dict, resultado: visao.Resultado) -> list[tuple[str, str]]:
    evidencia: list[tuple[str, str]] = []
    mmd = pasta / ARQUIVO_MMD
    texto_md = pasta / ARQUIVO_TEXTO
    for arquivo in (mmd, texto_md):
        if not arquivo.is_file():
            resultado.erro(f"{arquivo.name} não existe em {pasta}")
    if resultado.erros:
        return evidencia
    conteudo = ler_texto(mmd)

    if conteudo != estrutura["mmd"]:
        resultado.erro(f"{ARQUIVO_MMD} difere do que o gerador produz a partir dos models: gere de novo (README)")
    tabela_no_texto = tabela_do_texto(ler_texto(texto_md))
    if tabela_no_texto is None:
        resultado.erro(f"{ARQUIVO_TEXTO} não tem a tabela entre {INICIO_DA_TABELA} e {FIM_DA_TABELA}")
    elif tabela_no_texto != estrutura["tabela_de_restricoes"]:
        resultado.erro(f"a tabela de restrições de {ARQUIVO_TEXTO} difere da gerada a partir dos models")

    desenho, relacoes = ler_desenho(conteudo)
    models = {t["tabela"]: {c["nome"]: c for c in t["colunas"]} for t in estrutura["tabelas"]}

    for tabela, colunas in desenho.items():
        if tabela not in models:
            resultado.erro(f"tabela {tabela} do desenho não existe nos models")
            continue
        for nome, (tipo, _, _) in colunas.items():
            if nome not in models[tabela]:
                resultado.erro(f"coluna {tabela}.{nome} do desenho não existe no model")
                continue
            banco = models[tabela][nome]["tipo_do_banco"]
            if not banco.startswith(TIPOS_COMPATIVEIS.get(tipo, ("?",))):
                resultado.erro(f"{tabela}.{nome}: o desenho diz {tipo}, o model dá {banco}")
        evidencia.append((f"tabela {tabela}", f"{len(colunas)} colunas conferidas com o model"))
    for tabela in models:
        if tabela not in desenho:
            resultado.erro(f"tabela {tabela} dos models não aparece no desenho")

    solidas = {(o, d, r) for o, j, d, r in relacoes if j == "--"}
    pontilhadas = {(o, d, r.split(":")[0]) for o, j, d, r in relacoes if j == ".."}
    for tabela, coluna in estrutura["fks_dos_models"]:
        destino = next((c["fk"] for c in models.get(tabela, {}).values() if c["nome"] == coluna and c["fk"]), None)
        if destino is None:
            resultado.erro(f"{tabela}.{coluna} é ForeignKey no model, mas a coluna não está no desenho")
        elif (destino, tabela, coluna) not in solidas:
            resultado.erro(f"a ForeignKey {tabela}.{coluna} → {destino} não é relação sólida no desenho")
        else:
            evidencia.append((f"FK {tabela}.{coluna}", f"relação sólida com {destino}"))
    fks = {(t, c) for t, c in estrutura["fks_dos_models"]}
    for origem, destino, rotulo in solidas:
        if (destino, rotulo) not in fks:
            resultado.erro(f"relação sólida {origem} → {destino} ('{rotulo}') sem ForeignKey no model")
    ids = {(r["origem"], r["destino"], r["coluna"]) for r in estrutura["relacoes"] if r["tipo"] == "id"}
    for o, d, c in sorted(pontilhadas):
        coluna = models.get(d, {}).get(c)
        if coluna is None or coluna["fk"] or coluna["tipo_do_model"] != "BigIntegerField":
            resultado.erro(f"relação pontilhada {o} → {d} ('{c}') não é um BigIntegerField sem FK")
        elif (o, d, c) not in ids:
            resultado.erro(f"relação pontilhada {o} → {d} ('{c}') não está nas referências por id do gerador")
        else:
            evidencia.append((f"ref. por id {d}.{c}", f"pontilhada para {o}, BigIntegerField sem FK"))
    for o, d, c in sorted(ids - pontilhadas):
        resultado.erro(f"a referência por id {d}.{c} → {o} não é relação pontilhada no desenho")

    linhas = (tabela_no_texto or "").splitlines()[2:]
    na_tabela: set[tuple[str, str]] = set()
    for x in linhas:
        m = re.match(r"\| (\S+) \| `(\w+)` \| (.+) \| ([^|]+) \|$", x)
        if m:
            na_tabela.add((m.group(2), m.group(3).replace("\\|", "|")))
    nos_models = {(r["tabela"], r["definicao"]) for r in estrutura["restricoes"]}
    for tabela, definicao in sorted(nos_models - na_tabela):
        resultado.erro(f"restrição do model sem linha na tabela: {tabela}: {definicao}")
    for tabela, definicao in sorted(na_tabela - nos_models):
        resultado.erro(f"linha da tabela sem restrição no model: {tabela}: {definicao}")
    for r in estrutura["restricoes"]:
        if (r["tabela"], r["definicao"]) in na_tabela:
            evidencia.append((f"restrição {r['tipo']}", f"{r['tabela']}: {r['nome']}"))

    # (e) colunas obrigatórias
    exigidas: dict[str, set[str]] = {t: set() for t in models}
    for t, colunas in models.items():
        for c in colunas.values():
            if c["pk"] or c["fk"]:
                exigidas[t].add(c["nome"])
    for r in estrutura["relacoes"]:
        exigidas[r["destino"]].add(r["coluna"])
    for r in estrutura["restricoes"]:
        exigidas[r["tabela"]] |= set(r["colunas"])
    for tabela, colunas in exigidas.items():
        for coluna in sorted(colunas - set(desenho.get(tabela, {}))):
            resultado.erro(f"{tabela}.{coluna} é obrigatória no desenho (PK, FK, referência por id ou restrição)")

    # (f) imagens
    for extensao in (".svg", ".png"):
        imagem = mmd.with_suffix(extensao)
        if not imagem.is_file():
            resultado.erro(f"{imagem.name} não existe: gere as imagens (README.md da pasta)")
        elif imagem.stat().st_mtime < mmd.stat().st_mtime:
            resultado.avisos.append(f"{imagem.name} é mais antigo que {mmd.name}: gere as imagens de novo")
    return evidencia


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--pasta", type=Path, default=visao.PASTA_PADRAO, help="pasta com o .mmd e o texto")
    parser.add_argument("--gerado", type=Path, help="JSON do gerador (--json), em vez de chamar o container")
    argumentos = parser.parse_args()

    resultado = visao.Resultado()
    estrutura = estrutura_dos_models(argumentos.gerado)
    evidencia = verificar(argumentos.pasta.resolve(), estrutura, resultado)

    print("| O que foi conferido | Resultado |")
    print("|---|---|")
    for o_que, quanto in evidencia:
        print(f"| {o_que} | {quanto} |")
    print()
    for aviso in resultado.avisos:
        print(f"AVISO: {aviso}")
    if resultado.erros:
        print(f"\n{len(resultado.erros)} pendência(s):")
        for erro in resultado.erros:
            print(f"- {erro}")
        return 1
    print(f"OK: {len(evidencia)} itens do DER conferidos contra os models.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
