#!/usr/bin/env python3
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FONTE = RAIZ / "docs" / "fontes" / "requisitos"
LEV = FONTE / "levantamento"
DOC = FONTE / "entrega" / "RS_Grupo03_Evidencias.md"
LIMITE_DE_PAGINAS = 8
META_DE_PAGINAS = 7.5
CARACTERES_POR_LINHA = 92
LINHAS_POR_PAGINA = 46

erros: list[str] = []
avisos: list[str] = []


def ler(caminho: Path) -> str:
    return caminho.read_text(encoding="utf-8").replace("\r\n", "\n")


def norm(texto: str) -> str:
    """Normaliza espaços e quebras, e tira o realce (**, *, `) e a marca de lista."""
    texto = re.sub(r"[*`]", "", texto)
    texto = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", texto)
    return re.sub(r"\s+", " ", texto).strip()


def linhas_de_tabela(texto: str) -> list[list[str]]:
    saida = []
    for linha in texto.splitlines():
        if linha.startswith("|") and not re.match(r"^\|[-| ]+\|$", linha):
            saida.append([c.strip() for c in linha.strip().strip("|").split("|")])
    return saida


def secoes(texto: str, nivel: str = "## ") -> dict[str, str]:
    partes = re.split(rf"^({re.escape(nivel)}.*)$", texto, flags=re.M)
    return {partes[i].strip(): partes[i + 1] for i in range(1, len(partes) - 1, 2)}


def contagens(doc: str) -> None:
    print("== 1. Contagens ==")
    na_fonte = sorted(p.name[:6] for p in (LEV / "entrevistas").glob("ENT-*.md"))
    no_doc = sorted(set(re.findall(r"^\*\*(ENT-\d\d) —", doc, re.M)))
    print(f"  entrevistas na fonte: {len(na_fonte)} {na_fonte}; no documento: {len(no_doc)} {no_doc}")
    if na_fonte != no_doc:
        erros.append("entrevistas do documento diferem das ENT-* da fonte")

    resultados = ler(LEV / "questionario" / "QST-01-resultados.md")
    n_fonte = int(re.search(r"\| Respostas \(N\) \| \*\*(\d+)\*\*", resultados).group(1))
    ns_doc = set(re.findall(r"N = (\d+) respostas", doc))
    print(f"  N na fonte: {n_fonte}; N no documento: {sorted(ns_doc)}")
    if ns_doc != {str(n_fonte)}:
        erros.append("N do questionário no documento difere de QST-01-resultados.md")

    instrumentos = re.findall(r"^### (ROT-0[123]|QST-01) —", doc, re.M)
    print(f"  instrumentos no documento: {len(instrumentos)} {instrumentos}")
    if instrumentos != ["ROT-01", "ROT-02", "ROT-03", "QST-01"]:
        erros.append("os instrumentos devem ser exatamente ROT-01, ROT-02, ROT-03 e QST-01")


def confere(rotulo: str, trecho: str, alvo_norm: str, onde: str, diferencas: list[str]) -> None:
    if norm(trecho) not in alvo_norm:
        diferencas.append(f"{rotulo}: não encontrado em {onde}:\n      origem: {norm(trecho)[:300]}")


def fidelidade(doc: str) -> None:
    print("== 2. Fidelidade dos instrumentos ==")
    secao = secoes(doc, "### ")
    for rot, arquivo in [
        ("ROT-01", "ROT-01-representante-do-cliente.md"),
        ("ROT-02", "ROT-02-solicitante.md"),
        ("ROT-03", "ROT-03-atendente-responsavel.md"),
    ]:
        origem = ler(LEV / "entrevistas" / arquivo)
        alvo = norm(next(v for k, v in secao.items() if k.startswith(f"### {rot}")))
        dif: list[str] = []
        n = 0
        for linha in linhas_de_tabela(origem):
            if not re.fullmatch(r"P\d\d", linha[0]):
                continue
            n += 1
            if rot == "ROT-01":
                pergunta = linha[2]
                confere(f"{rot} {linha[0]} pergunta", pergunta, alvo, "documento", dif)
                confere(f"{rot} {linha[0]} assunto", linha[1], alvo, "documento", dif)
            else:
                confere(f"{rot} {linha[0]} pergunta", linha[3], alvo, "documento", dif)
                confere(f"{rot} {linha[0]} aprofundamento", linha[4], alvo, "documento", dif)
                if linha[2] == "SE HOUVER TEMPO" and not re.search(rf"{linha[0]}\*\* \[se houver tempo\]", secao[next(k for k in secao if k.startswith(f'### {rot}'))]):
                    dif.append(f"{rot} {linha[0]}: falta a marca [se houver tempo]")
        for bloco in re.findall(r"^> (.+)$", origem, re.M):
            confere(f"{rot} abertura/encerramento", bloco.replace("…", "…"), alvo, "documento", dif)
        print(f"  {rot}: {n} perguntas conferidas; diferenças: {len(dif)}")
        for d in dif:
            print("    -", d)
        erros.extend(f"fidelidade: {d.splitlines()[0]}" for d in dif)

    impressa = ler(LEV / "questionario" / "QST-01-versao-impressa.md")
    completo = norm(ler(LEV / "questionario" / "QST-01-questionario.md"))
    alvo = norm(next(v for k, v in secao.items() if k.startswith("### QST-01")))
    dif = []
    perguntas = re.findall(r"^\*\*(P\d\d\..+)$", impressa, re.M)
    for p in perguntas:
        confere(f"QST-01 {p[:3]}", "**" + p, alvo, "documento", dif)
        # cada opção da versão impressa precisa existir no questionário completo
        opcoes = re.findall(r"(?:\( \)|\[ \])\s*([^(\[]+?)(?=\s*(?:\( \)|\[ \]|$))", p)
        for o in opcoes:
            o = o.strip().rstrip(":_ ").strip()
            if o and o.startswith("Outra"):
                continue
            if o and norm(o).replace(" min", " minutos").replace(" h", " hora") not in completo and norm(o) not in completo:
                avisos.append(f"QST-01 {p[:3]}: opção '{o}' da versão impressa difere do QST-01 completo (forma abreviada?)")
    introducao = re.search(r"^\*(Somos do Grupo 03.+)\*$", impressa, re.M).group(1)
    confere("QST-01 introdução", introducao, alvo, "documento", dif)
    print(f"  QST-01: {len(perguntas)} perguntas conferidas com as opções; diferenças: {len(dif)}")
    for d in dif:
        print("    -", d)
    erros.extend(f"fidelidade: {d.splitlines()[0]}" for d in dif)
    if len(perguntas) != 11:
        erros.append("QST-01 deve ter 11 perguntas")


def somas(doc: str) -> None:
    print("== 3. Soma das contagens por pergunta ==")
    n = int(re.search(r"N = (\d+) respostas", doc).group(1))
    esperado = {"P03": ("várias", 36), "P04": ("uma", n), "P05": ("uma", n), "P06": ("uma", n),
                "P07": ("várias", 41), "P08": ("uma", n), "P09": ("várias", 38)}
    tabela = {l[0][:3]: l[1] for l in linhas_de_tabela(doc[doc.index("## 4."):]) if re.match(r"P\d\d", l[0])}
    for p, (tipo, soma_fonte) in esperado.items():
        contagens = [int(x) for x in re.findall(r"(\d+) de " + str(n), tabela.get(p, ""))]
        soma = sum(contagens)
        ok = soma == n if tipo == "uma" else (soma >= n and soma == soma_fonte)
        extra = f" (limite 3×N = {3 * n})" if p == "P09" else ""
        print(f"  {p}: {len(contagens)} opções, soma {soma}; {'uma opção, deve ser N' if tipo == 'uma' else 'várias, igual à fonte ' + str(soma_fonte)}{extra} -> {'ok' if ok else 'ERRO'}")
        if not ok:
            erros.append(f"{p}: soma {soma} fora do esperado")
        if p == "P09" and soma > 3 * n:
            erros.append("P09: soma passa de 3 × N")
    perfil = doc[doc.index("Perfil, P01:"):doc.index("P03, P07")]
    for rotulo, padrao in [("vínculo", r"P01:.*?Outro 0 de 18"), ("uso", r"P02:.*?Nunca usei 2 de 18")]:
        soma = sum(int(x) for x in re.findall(r"(\d+) de 18", re.search(padrao, perfil, re.S).group(0)))
        print(f"  perfil ({rotulo}): soma {soma} -> {'ok' if soma == n else 'ERRO'}")
        if soma != n:
            erros.append(f"perfil ({rotulo}): soma {soma} diferente de N")
    fonte = ler(LEV / "questionario" / "QST-01-resultados.md")
    cont_fonte = re.findall(r"\| (?:P\d\d [^|]*|) *\| ([^|]+) \| (\d+) de 18 \|", fonte)
    faltam = [(o, c) for o, c in cont_fonte if f"{o.strip()}: {c} de 18" not in doc and f"{o.strip()} {c} de 18" not in doc and not _no_perfil(o, c, doc)]
    print(f"  contagens da fonte ausentes ou diferentes no documento: {len(faltam)}")
    for o, c in faltam:
        print(f"    - {o.strip()}: {c} de 18")
        erros.append(f"contagem da fonte ausente: {o.strip()} {c} de 18")


def _no_perfil(opcao: str, contagem: str, doc: str) -> bool:
    o = opcao.strip().lower()
    return bool(re.search(rf"{re.escape(o)}[^.;]*? {contagem} de 18|{re.escape(o)} {contagem} de 18", doc.lower()))


def pendencias_ids_dados(doc: str) -> None:
    print("== 4. Marcadores [PENDENTE] ==")
    secao_atual = ""
    achou = 0
    for linha in doc.splitlines():
        if linha.startswith("#"):
            secao_atual = linha.lstrip("# ").strip()
        for m in re.finditer(r"\[PENDENTE[^\]]*\]", linha):
            achou += 1
            ok = re.fullmatch(r"\[PENDENTE: [^\]]+\]", m.group(0))
            print(f"  [{secao_atual or 'cabeçalho'}] {m.group(0)}" + ("" if ok else "  <- formato inválido"))
            if not ok:
                erros.append(f"marcador fora do formato: {m.group(0)}")
    print(f"  total: {achou}")

    print("== 5. IDs no formato da fonte ==")
    ruins = sorted(set(re.findall(r"\b(?:RF|RNF|RN)-[A-Z]?\d[\d.]*", doc)))
    print(f"  RF-/RNF-/RN- encontrados: {ruins or 'nenhum'}")
    if ruins:
        erros.append(f"IDs no formato da fonte: {ruins}")

    print("== 6. Dados pessoais e links ==")
    padroes = {
        "e-mail": r"[\w.+-]+@[\w-]+\.[\w.]+",
        "6 ou mais dígitos": r"\d{6,}",
        "telefone": r"\(?\d{2}\)?[\s-]?9?\d{4}[\s-]?\d{4}",
        "'meu nome'": r"(?i)meu nome",
        "link ou caminho": r"\]\(|https?://|[A-Za-z]:\\|docs/fontes",
    }
    for rotulo, regex in padroes.items():
        achados = re.findall(regex, doc)
        print(f"  {rotulo}: {achados or 'nenhum'}")
        if achados:
            erros.append(f"{rotulo} no documento: {achados}")
    if re.search(r"[\U0001F300-\U0001FAFF☀-➿]", doc):
        erros.append("emoji no documento")


def linhas_do_bloco(bloco: str) -> float:
    total = 0.0
    for linha in bloco.splitlines():
        if not linha.strip():
            continue
        if re.match(r"^\|[-| ]+\|$", linha):
            continue
        texto = norm(linha)
        if linha.startswith("|"):
            total += math.ceil(len(texto) / (CARACTERES_POR_LINHA * 0.85)) + 0.3  # célula e respiro da tabela
        elif linha.startswith("- "):
            total += math.ceil(len(texto) / CARACTERES_POR_LINHA) + 0.15
        else:
            total += math.ceil(len(texto) / CARACTERES_POR_LINHA) + 0.6  # espaço entre parágrafos
    return total


def paginas(doc: str) -> None:
    print("== 7. Estimativa de páginas ==")
    print(f"  critério: A4, 11 pt, margens de 2,5 cm, {CARACTERES_POR_LINHA} caracteres por linha, {LINHAS_POR_PAGINA} linhas por página")
    cabecalho, resto = doc.split("\n## 1.", 1)
    resto = "## 1." + resto
    partes = [("Título e cabeçalho", cabecalho)]
    for titulo, corpo in secoes(resto, "## ").items():
        subs = secoes(corpo, "### ")
        if subs and titulo.startswith("## 2."):
            partes.append((titulo + " (introdução)", corpo.split("### ", 1)[0]))
            partes.extend((t, c) for t, c in subs.items())
        else:
            partes.append((titulo, corpo))
    total = 0.0
    for titulo, corpo in partes:
        linhas = linhas_do_bloco(corpo) + (3 if titulo.startswith("##") else 0)  # título e espaço
        palavras = len(corpo.split())
        total += linhas
        print(f"  {titulo.lstrip('# ')[:62]:<62} {palavras:>5} palavras {linhas / LINHAS_POR_PAGINA:>5.2f} pág.")
    pag = total / LINHAS_POR_PAGINA
    print(f"  TOTAL: {len(doc.split())} palavras, {pag:.2f} páginas estimadas (meta {META_DE_PAGINAS}, limite {LIMITE_DE_PAGINAS}); margem {LIMITE_DE_PAGINAS - pag:.2f}")
    if pag > LIMITE_DE_PAGINAS:
        erros.append(f"estimativa de {pag:.2f} páginas passa do limite de {LIMITE_DE_PAGINAS}")
    elif pag > META_DE_PAGINAS:
        avisos.append(f"estimativa de {pag:.2f} páginas passa da meta de {META_DE_PAGINAS}")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    doc = ler(DOC)
    contagens(doc)
    fidelidade(doc)
    somas(doc)
    pendencias_ids_dados(doc)
    paginas(doc)
    print("== Resultado ==")
    for a in avisos:
        print("  AVISO:", a)
    for e in erros:
        print("  ERRO:", e)
    print("  OK" if not erros else f"  {len(erros)} erro(s)")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
