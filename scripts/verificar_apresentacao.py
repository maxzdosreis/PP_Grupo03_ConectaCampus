#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FONTE = RAIZ / "docs" / "fontes" / "requisitos"
ENTREGA = FONTE / "entrega"
PASTA = ENTREGA / "apresentacao"
SPEC = ENTREGA / "RS_Grupo03_Especificacao.md"
ROTEIRO = PASTA / "APRESENTACAO_Grupo03_Roteiro.md"
PERGUNTAS = PASTA / "APRESENTACAO_Grupo03_Perguntas.md"
ENSAIO = PASTA / "APRESENTACAO_Grupo03_Ensaio.md"

PALAVRAS_POR_MINUTO = 130
LIMITE_DE_FALA_S = 9 * 60 + 15
MINIMO_POR_FALANTE_S = 60
MAX_LINHAS_SLIDE = 4
MAX_PALAVRAS_SLIDE = 60
NOMES_PERMITIDOS = ["Max Zimmermann dos Reis", "Matheus Cezar Santos", "Eduardo Almeida da Cunha"]
INTERFACE = re.compile(r"\b(tela|telas|botão|botões|clique|print|screenshot|demonstra\w*|demo)\b", re.IGNORECASE)
MARCADOR = re.compile(r"\[(PENDENTE|INTEGRANTE \d|A DEFINIR|CONFIRMAR|PREENCHER)[^\]]*\]")

erros: list[str] = []
avisos: list[str] = []


def ler(caminho: Path) -> str:
    return caminho.read_text(encoding="utf-8").replace("\r\n", "\n")


def palavras(texto: str) -> int:
    return len(re.findall(r"\S+", texto))


def tempo(segundos: float) -> str:
    s = round(segundos)
    return f"{s // 60}:{s % 60:02d}"


def segundos(n_palavras: int) -> float:
    return n_palavras / PALAVRAS_POR_MINUTO * 60


def ler_slides(roteiro: str) -> list[dict]:
    partes = re.split(r"^### Slide (\d+) — (.*)$", roteiro, flags=re.M)
    slides = []
    for i in range(1, len(partes) - 2, 3):
        corpo = partes[i + 2]
        falante = re.search(r"\*\*Falante:\*\* (.+)", corpo)
        conteudo = re.search(r"\*\*Conteúdo do slide\*\*\n(.*?)\*\*Fala\*\*", corpo, re.S)
        fala = [ln[2:] for ln in corpo.splitlines() if ln.startswith("> ")]
        declarado = re.search(r"Palavras: (\d+) · Tempo: (\d+) s", corpo)
        slides.append(
            {
                "n": int(partes[i]),
                "titulo": partes[i + 1].strip(),
                "falante": falante.group(1).strip() if falante else "",
                "conteudo": conteudo.group(1) if conteudo else "",
                "fala": " ".join(fala),
                "declarado": (int(declarado.group(1)), int(declarado.group(2))) if declarado else None,
            }
        )
    return slides


def tempos(slides: list[dict], roteiro: str) -> None:
    print("== 1. Tempo de fala (130 palavras por minuto) ==")
    total = 0
    por_falante: dict[str, int] = {}
    print("  slide | falante        | palavras | tempo")
    for s in slides:
        n = palavras(s["fala"])
        total += n
        por_falante[s["falante"]] = por_falante.get(s["falante"], 0) + n
        print(f"  {s['n']:>5} | {s['falante']:<14} | {n:>8} | {tempo(segundos(n))}")
        if not s["fala"]:
            erros.append(f"slide {s['n']}: sem fala")
        if s["declarado"] is None:
            erros.append(f"slide {s['n']}: falta a linha 'Palavras: N · Tempo: S s'")
        elif s["declarado"] != (n, round(segundos(n))):
            erros.append(
                f"slide {s['n']}: declarado {s['declarado']}, real ({n}, {round(segundos(n))}); "
                f"escreva 'Palavras: {n} · Tempo: {round(segundos(n))} s'"
            )
    print(f"  total | {'':<14} | {total:>8} | {tempo(segundos(total))} (limite de fala {tempo(LIMITE_DE_FALA_S)})")
    if segundos(total) > LIMITE_DE_FALA_S:
        erros.append(f"fala total {tempo(segundos(total))} passa de {tempo(LIMITE_DE_FALA_S)}")
    print("  por falante:")
    tabela = re.findall(r"^\| (\d+) \| [^|]+ \| (\d+:\d\d) \| ([^|]+) \|$", roteiro, re.M)
    falantes_da_tabela = {f.strip() for _, _, f in tabela}
    for f, n in sorted(por_falante.items()):
        print(f"    {f}: {n} palavras, {tempo(segundos(n))}")
        if segundos(n) < MINIMO_POR_FALANTE_S:
            erros.append(f"{f} fala menos de 1 minuto")
    if falantes_da_tabela != set(por_falante):
        erros.append(f"falantes da tabela de abertura {sorted(falantes_da_tabela)} diferem dos slides {sorted(por_falante)}")
    if por_falante:
        menor, maior = min(por_falante.values()), max(por_falante.values())
        print(f"    maior/menor = {maior / menor:.2f}")
        if maior >= 3 * menor:
            erros.append("desequilíbrio: um falante fala 3 vezes o tempo de outro")
    by_slide = {s["n"]: s for s in slides}
    for n, t, f in tabela:
        s = by_slide.get(int(n))
        if s is None:
            erros.append(f"tabela de abertura cita o slide {n}, que não existe")
            continue
        if f.strip() != s["falante"]:
            erros.append(f"slide {n}: falante da tabela ({f.strip()}) difere do slide ({s['falante']})")
        m, sec = t.split(":")
        esperado = round(segundos(palavras(s["fala"])))
        if abs(int(m) * 60 + int(sec) - esperado) > 6:
            avisos.append(f"slide {n}: tempo da tabela de abertura {t} difere do estimado {tempo(esperado)}")
    if not 9 <= len(slides) <= 11:
        erros.append(f"{len(slides)} slides; o pedido é de 9 a 11")


def limites_de_slide(slides: list[dict]) -> None:
    print("\n== 2. Limites dos slides e termos de interface ==")
    for s in slides:
        linhas = [
            ln.strip()
            for ln in s["conteudo"].splitlines()
            if ln.strip() and not ln.strip().startswith("|") and not ln.strip().startswith("Figura")
        ]
        n_palavras = sum(palavras(ln) for ln in linhas)
        print(f"  slide {s['n']}: {len(linhas)} linhas, {n_palavras} palavras (sem tabela)")
        if len(linhas) > MAX_LINHAS_SLIDE:
            erros.append(f"slide {s['n']}: {len(linhas)} linhas (máximo {MAX_LINHAS_SLIDE})")
        if n_palavras > MAX_PALAVRAS_SLIDE:
            erros.append(f"slide {s['n']}: {n_palavras} palavras (máximo {MAX_PALAVRAS_SLIDE})")
        for onde, texto in (("conteúdo", s["conteudo"]), ("fala", s["fala"])):
            achado = INTERFACE.search(texto)
            if achado:
                erros.append(f"slide {s['n']} ({onde}): termo de interface ou demonstração '{achado.group(0)}'")


def dados_da_fonte() -> dict:
    spec = ler(SPEC)
    rf = re.findall(r"^\| RF(\d+(?:\.\d+)?) \|", spec, re.M)
    rnf = re.findall(r"^\| (RNF\d+) \| (\w+) \|", spec, re.M)
    temas = {
        "espaços": (1, 10),
        "reservas": (11, 16),
        "situação": (17, 27),
        "agenda": (28, 31),
        "contas": (32, 37),
        "transversais": (38, 40),
    }
    por_tema = {k: sum(1 for i in rf if a <= int(i.split(".")[0]) <= b) for k, (a, b) in temas.items()}
    classes: dict[str, int] = {}
    for _, classe in rnf:
        classes[classe] = classes.get(classe, 0) + 1
    ncr = len(list((FONTE / "mudancas").glob("CR-*.md")))
    ndec = len(list((FONTE / "decisoes").glob("DEC-*.md")))
    sintese = ler(FONTE / "levantamento" / "sintese-evidencia-1pag.md")
    return {
        "spec": spec,
        "rf": rf,
        "rnf": len(rnf),
        "rn": len(re.findall(r"^\| RN\d+ \|", spec, re.M)),
        "us": len(re.findall(r"^\| US-\d+ \|", spec, re.M)),
        "dec": ndec,
        "cr": ncr,
        "temas": por_tema,
        "classes": classes,
        "sintese": sintese,
    }


def numeros(texto: str, d: dict) -> None:
    print("\n== 3. Números citados × origem ==")
    sint = d["sintese"]
    esperado = [
        ("RF (identificadores)", r"(\d+) identificadores", len(d["rf"]), "especificação, seção 5 (linhas RFnn)"),
        ("RF de espaços", r"espaços, com (\d+)", d["temas"]["espaços"], "especificação, RF01 a RF10"),
        ("RF de reservas", r"consultar reservas, (\d+)", d["temas"]["reservas"], "especificação, RF11 a RF16"),
        ("RF de situação", r"histórico, (\d+)", d["temas"]["situação"], "especificação, RF17 a RF27"),
        ("RF de agenda", r"agenda do dia, (\d+)", d["temas"]["agenda"], "especificação, RF28 a RF31"),
        ("RF de contas", r"contas e acesso, (\d+)", d["temas"]["contas"], "especificação, RF32 a RF37"),
        ("RNF", r"São (\d+), organizados", d["rnf"], "especificação, seção 6"),
        ("RNF funcionalidade", r"(\d+) de funcionalidade", d["classes"].get("Funcionalidade"), "especificação, seção 6"),
        ("RNF usabilidade", r"(\d+) de usabilidade", d["classes"].get("Usabilidade"), "especificação, seção 6"),
        ("RNF confiabilidade", r"(\d+) de confiabilidade", d["classes"].get("Confiabilidade"), "especificação, seção 6"),
        ("RNF desempenho", r"(\d+) de desempenho", d["classes"].get("Desempenho"), "especificação, seção 6"),
        ("RNF suportabilidade", r"(\d+) de suportabilidade", d["classes"].get("Suportabilidade"), "especificação, seção 6"),
        ("RN", r"As (\d+) regras de negócio", d["rn"], "especificação, seção 7"),
        ("US", r"(\d+) histórias", d["us"], "especificação, seção 9"),
        ("DEC", r"(\d+) decisões registradas", d["dec"], "fonte oficial, decisoes/DEC-*.md"),
        ("CR", r"(\d+) pedidos de mudança", d["cr"], "fonte oficial, mudancas/CR-*.md"),
        ("respostas do questionário", r"(\d+) respostas", 18, "levantamento, QST-01 (N = 18)"),
    ]
    for nome, padrao, valor, origem in esperado:
        achados = re.findall(padrao, texto)
        if not achados:
            erros.append(f"número não encontrado no roteiro: {nome} (padrão {padrao})")
            continue
        ok = all(int(a) == valor for a in achados)
        print(f"  {nome}: roteiro {sorted(set(achados))} × {valor} ({origem}) {'ok' if ok else 'DIVERGE'}")
        if not ok:
            erros.append(f"{nome}: roteiro {achados}, fonte {valor}")
    soma = sum(d["temas"].values())
    print(f"  soma dos temas de RF: {soma} × {len(d['rf'])}")
    if soma != len(d["rf"]):
        erros.append("a soma dos temas de RF não bate com o total")
    for fato in ("14 de 18", "12 de 18"):
        ok = fato in sint
        print(f"  '{fato}': {'ok' if ok else 'AUSENTE'} (sintese-evidencia-1pag.md)")
        if fato in texto and not ok:
            erros.append(f"'{fato}' não está na síntese do levantamento")
    for palavra, valor in (("quatro entrevistados", 4), ("três papéis", 3)):
        if palavra in texto:
            print(f"  '{palavra}': conferido com {valor} (especificação, seção 4)")


def ids(arquivos: dict[str, str], d: dict) -> None:
    print("\n== 4. IDs citados existem ==")
    spec = d["spec"]
    visao = ler(FONTE / "visao.md")
    ids_spec_rf = {f"RF{i}" for i in d["rf"]}
    ids_rnf = {f"RNF{n:02d}" for n in range(1, d["rnf"] + 1)}
    ids_rn = {f"RN{n:02d}" for n in range(1, d["rn"] + 1)}
    ucs = set(re.findall(r"UC-\d+", spec))
    uss = set(re.findall(r"^\| (US-\d+) \|", spec, re.M))
    nss = set(re.findall(r"NS-\d+", visao))
    uc04 = spec.split("### 8.1 UC-04")[1].split("### 8.2")[0]
    pares = set(re.findall(r"^- ([AE]\d+\.\d+) \(", uc04, re.M))
    contagem: dict[str, int] = {}
    for arquivo, texto in arquivos.items():
        for m in sorted(set(re.findall(r"\bRNF\d{2}\b", texto))):
            contagem["RNF"] = contagem.get("RNF", 0) + 1
            if m not in ids_rnf:
                erros.append(f"{arquivo}: {m} não existe")
        for m in sorted(set(re.findall(r"\bRN\d{2}\b", texto))):
            contagem["RN"] = contagem.get("RN", 0) + 1
            if m not in ids_rn:
                erros.append(f"{arquivo}: {m} não existe")
        for m in sorted(set(re.findall(r"\bRF\d{2}(?:\.\d)?\b", texto))):
            contagem["RF"] = contagem.get("RF", 0) + 1
            if m not in ids_spec_rf:
                erros.append(f"{arquivo}: {m} não existe")
        for m in sorted(set(re.findall(r"\bUC-\d{2}\b", texto))):
            contagem["UC"] = contagem.get("UC", 0) + 1
            if m not in ucs:
                erros.append(f"{arquivo}: {m} não existe")
        for m in sorted(set(re.findall(r"\bUS-\d{2}\b", texto))):
            contagem["US"] = contagem.get("US", 0) + 1
            if m not in uss:
                erros.append(f"{arquivo}: {m} não existe")
        for m in sorted(set(re.findall(r"\bNS-\d{2}\b", texto))):
            contagem["NS"] = contagem.get("NS", 0) + 1
            if m not in nss:
                erros.append(f"{arquivo}: {m} não existe")
        for m in sorted(set(re.findall(r"\bDEC-\d{2}\b", texto))):
            contagem["DEC"] = contagem.get("DEC", 0) + 1
            if not (FONTE / "decisoes" / f"{m}.md").exists():
                erros.append(f"{arquivo}: {m} não existe")
        for m in sorted(set(re.findall(r"\bCR-\d{2}\b", texto))):
            contagem["CR"] = contagem.get("CR", 0) + 1
            if not list((FONTE / "mudancas").glob(f"{m}-*.md")):
                erros.append(f"{arquivo}: {m} não existe")
        for m in sorted(set(re.findall(r"\bENT-\d{2}\b", texto))):
            contagem["ENT"] = contagem.get("ENT", 0) + 1
            if not list((FONTE / "levantamento" / "entrevistas").glob(f"{m}-*.md")):
                erros.append(f"{arquivo}: {m} não existe")
        for m in sorted(set(re.findall(r"\b[AE]\d+\.\d+\b", texto))):
            contagem["A/E"] = contagem.get("A/E", 0) + 1
            if m not in pares:
                erros.append(f"{arquivo}: {m} não é alternativa nem exceção do UC-04")
    print("  IDs distintos conferidos por tipo e arquivo: " + ", ".join(f"{k} {v}" for k, v in sorted(contagem.items())))


def valores_das_regras(arquivos: dict[str, str], spec: str) -> None:
    print("\n== 5. Valores das regras × especificação ==")
    fatos = [
        ("funcionamento 07:00 às 00:00", r"07:00 às 00:00"),
        ("duração sugerida de 1 hora", r"duração sugerida \(1 hora\)|sugere a duração de 1 hora"),
        ("duração mínima 30 minutos e máxima 3 horas", r"no mínimo 30 minutos e no máximo 3 horas"),
        ("antecedência de 30 dias", r"até 30 dias de antecedência"),
        ("20 caracteres como limite técnico", r"20 caracteres são só um limite técnico"),
    ]
    for nome, padrao in fatos:
        ok = re.search(padrao, spec) is not None
        print(f"  {nome}: {'na especificação' if ok else 'AUSENTE na especificação'}")
        if not ok:
            erros.append(f"a especificação não traz: {nome}")
    for arquivo, texto in arquivos.items():
        for velho in ("22:00", "às 22 ", "07:00 às 22"):
            if velho in texto:
                erros.append(f"{arquivo}: valor antigo '{velho}' (a DEC-07 mudou para 07:00 às 00:00)")
    print("  nenhum valor antigo (22:00) nos arquivos de apresentação")


def marcadores(arquivos: dict[str, str]) -> None:
    print("\n== 6. Marcadores ==")
    total = 0
    for arquivo, texto in arquivos.items():
        for i, linha in enumerate(texto.splitlines(), 1):
            for m in MARCADOR.finditer(linha):
                total += 1
                print(f"  {arquivo}:{i}: {m.group(0)}")
    print(f"  total: {total}")


def dados_pessoais(arquivos: dict[str, str]) -> None:
    print("\n== 7. Dados pessoais ==")
    achou = False
    for arquivo, texto in arquivos.items():
        limpo = texto
        for nome in NOMES_PERMITIDOS:
            limpo = limpo.replace(nome, "")
        for rotulo, padrao in (
            ("e-mail", r"[\w.+-]+@[\w-]+\.[\w.]+"),
            ("6 ou mais dígitos", r"(?<![\d./-])\d{6,}(?![\d./-])"),
            ("telefone", r"\(?\d{2}\)?\s?9?\d{4}-\d{4}"),
        ):
            for m in re.finditer(padrao, limpo):
                achou = True
                erros.append(f"{arquivo}: possível {rotulo}: {m.group(0)}")
    print("  nenhum achado (nomes dos três integrantes, da capa dos documentos, são permitidos)" if not achou else "  ACHADOS")


def perguntas(texto: str) -> None:
    print("\n== 8. Material de perguntas ==")
    blocos = re.split(r"^### (P\d+)\. ", texto, flags=re.M)
    qs = [(blocos[i], blocos[i + 1]) for i in range(1, len(blocos) - 1, 2)]
    print(f"  perguntas: {len(qs)}")
    if not 14 <= len(qs) <= 18:
        erros.append(f"{len(qs)} perguntas; o pedido é de 14 a 18")
    for codigo, corpo in qs:
        for campo in ("**Resposta:**", "**Origem:**", "**Quem responde:** [A DEFINIR]"):
            if campo not in corpo:
                erros.append(f"{codigo}: falta {campo}")
    for secao in ("o que não sabemos", "contribuição individual"):
        if secao.lower() not in texto.lower():
            erros.append(f"falta o bloco '{secao}'")
    n = texto.count("[PREENCHER PELO INTEGRANTE]")
    print(f"  '[PREENCHER PELO INTEGRANTE]': {n}")
    if n < 12:
        erros.append("o bloco de contribuição precisa de 3 linhas para cada um dos 4 integrantes")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    for caminho in (SPEC, ROTEIRO, PERGUNTAS, ENSAIO):
        if not caminho.exists():
            print(f"FALTA: {caminho.relative_to(RAIZ)}")
            return 1
    roteiro = ler(ROTEIRO)
    perg = ler(PERGUNTAS)
    ens = ler(ENSAIO)
    arquivos = {p.name: ler(p) for p in (ROTEIRO, PERGUNTAS, ENSAIO)}
    slides = ler_slides(roteiro)
    d = dados_da_fonte()
    tempos(slides, roteiro)
    limites_de_slide(slides)
    numeros("\n".join(s["conteudo"] + "\n" + s["fala"] for s in slides), d)
    ids(arquivos, d)
    valores_das_regras(arquivos, d["spec"])
    marcadores(arquivos)
    dados_pessoais(arquivos)
    perguntas(perg)
    if "tempo real" not in ens.lower():
        erros.append("o ensaio não tem a coluna 'tempo real'")
    print("\n== Resultado ==")
    for a in avisos:
        print(f"  AVISO: {a}")
    for e in erros:
        print(f"  ERRO: {e}")
    print("  OK" if not erros else f"  {len(erros)} erro(s)")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
