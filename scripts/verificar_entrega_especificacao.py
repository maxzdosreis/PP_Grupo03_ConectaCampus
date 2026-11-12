#!/usr/bin/env python3
"""REQ-08: confere o texto da especificação de entrega (RS_Grupo03_Especificacao.md) contra a fonte oficial.

Somente leitura, sem dependências. Roda no host, na raiz do repositório:

    python scripts/verificar_entrega_especificacao.py

Confere: contagens de RF, RNF, RN, UC e US; IDs no formato do documento e a tabela de
correspondência (Anexo A); classe FURPS+ de cada RNF; RF das RN; UC ou US de cada RF; valores
substituídos pelos CRs; marcas de implementação pendente no corpo; marcadores [PENDENTE: ...];
dados pessoais; e estima as páginas do corpo. Não gera PDF.
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FONTE = RAIZ / "docs" / "fontes" / "requisitos"
DOC = FONTE / "entrega" / "RS_Grupo03_Especificacao.md"
LIMITE_DE_PAGINAS = 18
META_DE_PAGINAS = 16.5

CLASSES_FURPS = {"Funcionalidade", "Usabilidade", "Confiabilidade", "Desempenho", "Suportabilidade"}
INTERFACE = re.compile(r"\b(tela|telas|botão|botões|clica|url|endpoint|toast)\b", re.IGNORECASE)
PENDENTE = re.compile(r"\[PENDENTE: ([^\]]+)\]")
MARCA_DE_CODIGO = re.compile(r"implementação pendente|código pendente|tarefa [A-Z]{3}-\d{2}", re.IGNORECASE)
TRECHOS_ANTIGOS = [
    "espaço no meio",
    "Nenhuma transição depende do horário",
    "Só as mudanças aceitas são registradas",
    "nenhuma tentativa recusada vira registro",
    "Sem condição de horário",
]

erros: list[str] = []
avisos: list[str] = []


def ler(caminho: Path) -> str:
    return caminho.read_text(encoding="utf-8").replace("\r\n", "\n")


def corpo_e_anexos(texto: str) -> tuple[str, str]:
    i = texto.index("\n# Anexos")
    return texto[:i], texto[i:]


def secao(texto: str, titulo: str) -> str:
    m = re.search(r"^## " + re.escape(titulo) + r".*?$(.*?)(?=^## |^# |\Z)", texto, re.M | re.S)
    return m.group(1) if m else ""


def linhas_de_tabela(bloco: str) -> list[list[str]]:
    saida = []
    for linha in bloco.splitlines():
        if linha.startswith("|") and not re.match(r"^\|[-| ]+\|$", linha):
            saida.append([c.strip() for c in linha.strip().strip("|").split("|")])
    return saida[1:]  # sem o cabeçalho


# ---------- fonte oficial ----------
def ids_da_fonte() -> dict[str, list[str]]:
    rf = []
    for arq in ["rf-espacos", "rf-reservas", "rf-agenda", "rf-contas", "rf-gerais"]:
        rf += re.findall(r'^#{3,4} <a id="rf-[^"]+"></a>(RF-[\d.]+) · ', ler(FONTE / "requisitos" / f"{arq}.md"), re.M)
    rnf = re.findall(r'^### <a id="rnf-[^"]+"></a>(RNF-[FURPS]\d\d) · ', ler(FONTE / "requisitos" / "rnf.md"), re.M)
    rn = re.findall(r'^\| <a id="rn-\d+"></a>(RN-\d+) \|', ler(FONTE / "requisitos" / "regras-de-negocio.md"), re.M)
    us = sorted(p.name[:5] for p in (FONTE / "historias").glob("US-*.md"))
    uc = sorted(set(re.findall(r"\bUC-\d\d\b", ler(FONTE / "casos-de-uso" / "README.md"))))
    return {"RF": rf, "RNF": rnf, "RN": rn, "US": us, "UC": uc}


def id_do_documento(id_fonte: str, posicao: int | None = None) -> str:
    if id_fonte.startswith("RNF-"):
        return f"RNF{posicao:02d}"
    if id_fonte.startswith("RF-"):
        inteiro, _, resto = id_fonte[3:].partition(".")
        return "RF" + inteiro.zfill(2) + ("." + resto if resto else "")
    return id_fonte.replace("RN-", "RN")


def valores_antigos() -> list[str]:
    """Horários citados na coluna 'Antes' dos CR e ausentes da coluna 'Depois'."""
    antigos: set[str] = set()
    for cr in sorted((FONTE / "mudancas").glob("CR-0[1-4]-*.md")):
        for linha in ler(cr).splitlines():
            partes = [p.strip() for p in linha.strip().strip("|").split("|")]
            if linha.startswith("|") and len(partes) == 3:
                antes, depois = partes[1], partes[2]
                for h in re.findall(r"\b\d\d:\d\d\b", antes):
                    if h not in depois:
                        antigos.add(h)
    return sorted(antigos)


# ---------- verificações ----------
def verificar_contagens(corpo: str, anexos: str, fonte: dict[str, list[str]]) -> None:
    doc_rf = len(linhas_de_tabela(secao(corpo, "5. Requisitos funcionais")))
    doc_rnf = len(linhas_de_tabela(secao(corpo, "6. Requisitos não funcionais")))
    doc_rn = len(linhas_de_tabela(secao(corpo, "7. Regras de negócio")))
    doc_us = len(linhas_de_tabela(secao(corpo, "9. Histórias de usuário")))
    doc_uc = sorted(set(re.findall(r"\bUC-\d\d\b", corpo + anexos)))
    print("\n1. Contagens (documento x fonte oficial)")
    for nome, doc, src in [("RF", doc_rf, len(fonte["RF"])), ("RNF", doc_rnf, len(fonte["RNF"])),
                           ("RN", doc_rn, len(fonte["RN"])), ("US", doc_us, len(fonte["US"])),
                           ("UC citados", len(doc_uc), len(fonte["UC"]))]:
        marca = "ok" if doc == src else "DIVERGE"
        print(f"   {nome:<11} documento {doc:>3} | fonte {src:>3}  {marca}")
        if doc != src:
            erros.append(f"contagem de {nome}: documento {doc}, fonte {src}")


def verificar_ids(corpo: str, anexos: str, fonte: dict[str, list[str]]) -> None:
    print("\n2. Identificadores e Anexo A")
    esperado = {id_do_documento(i): i for i in fonte["RF"]}
    esperado |= {id_do_documento(i, n): i for n, i in enumerate(fonte["RNF"], 1)}
    esperado |= {id_do_documento(i): i for i in fonte["RN"]}
    anexo_a = anexos.split("## Anexo B")[0]
    pares = {}
    for celulas in linhas_de_tabela(anexo_a[anexo_a.index("| Fonte"):]):
        for k in range(0, len(celulas), 2):
            if celulas[k]:
                pares[celulas[k + 1]] = celulas[k]
    if pares != esperado:
        faltam = sorted(set(esperado) - set(pares))
        sobram = sorted(set(pares) - set(esperado))
        erros.append(f"Anexo A diverge da fonte: faltam {faltam}, sobram {sobram}")
    print(f"   Anexo A: {len(pares)} linhas, fonte {len(esperado)}")
    usados = set(re.findall(r"\b(?:RNF\d\d|RF\d\d(?:\.\d+)?|RN\d\d)\b", corpo))
    fora = sorted(usados - set(esperado))
    if fora:
        erros.append(f"IDs do corpo ausentes no Anexo A: {fora}")
    antigos = re.findall(r"\b(?:RF-\d+(?:\.\d+)?|RNF-[A-Z]?\d+|RN-\d+)\b", corpo)
    if antigos:
        erros.append(f"IDs no formato antigo no corpo: {sorted(set(antigos))}")
    print(f"   IDs do corpo: {len(usados)} distintos, {len(fora)} fora do Anexo A, {len(set(antigos))} no formato antigo")


def verificar_referencias(corpo: str, fonte: dict[str, list[str]]) -> None:
    print("\n3. Referências cruzadas")
    rf_validos = {id_do_documento(i) for i in fonte["RF"]}
    sem_classe = [c[0] for c in linhas_de_tabela(secao(corpo, "6. Requisitos não funcionais")) if c[1] not in CLASSES_FURPS]
    sem_rf = [c[0] for c in linhas_de_tabela(secao(corpo, "7. Regras de negócio"))
              if not c[2] or any(x.strip() not in rf_validos for x in c[2].split(","))]
    sem_uc_us = []
    for c in linhas_de_tabela(secao(corpo, "5. Requisitos funcionais")):
        refs = re.findall(r"\b(?:UC|US)-\d\d\b", c[3])
        if not refs and "Transversal" not in c[3]:
            sem_uc_us.append(c[0])
        elif any(r not in fonte["UC"] + fonte["US"] for r in refs):
            sem_uc_us.append(c[0])
    for rotulo, lista in [("RNF sem classe FURPS+", sem_classe), ("RN sem RF existente", sem_rf), ("RF sem UC/US existente", sem_uc_us)]:
        print(f"   {rotulo}: {len(lista)}")
        if lista:
            erros.append(f"{rotulo}: {lista}")
    for nome, bloco in [("RF", secao(corpo, "5. Requisitos funcionais")), ("RN", secao(corpo, "7. Regras de negócio"))]:
        achados = sorted({m.group(0).lower() for m in INTERFACE.finditer(bloco)})
        if achados:
            avisos.append(f"termos de interface vindos da fonte nas descrições de {nome}: {achados} (a fonte não foi alterada)")


def verificar_valores(corpo: str) -> None:
    print("\n4. Valores substituídos pelos CRs")
    proibidos = valores_antigos() + TRECHOS_ANTIGOS
    achados = [p for p in proibidos if p in corpo]
    print(f"   procurados: {proibidos}")
    print(f"   encontrados no corpo: {achados or 'nenhum'}")
    if achados:
        erros.append(f"valores antigos no corpo: {achados}")
    marcas = MARCA_DE_CODIGO.findall(corpo)
    print(f"   marcas de implementação pendente no corpo: {len(marcas)}")
    if marcas:
        erros.append(f"marcas de implementação pendente no corpo: {sorted(set(marcas))}")


def verificar_pendencias(texto: str) -> None:
    print("\n5. Marcadores [PENDENTE: ...]")
    secao_atual = "Capa"
    total = 0
    for linha in texto.splitlines():
        m = re.match(r"^#{1,3} (.+)$", linha)
        if m:
            secao_atual = m.group(1)
        for p in PENDENTE.findall(linha):
            total += 1
            print(f"   {secao_atual}: {p}")
    print(f"   total: {total}")
    soltos = [m for m in re.findall(r"\[PENDENTE[^\]]*\]", texto) if not PENDENTE.fullmatch(m)]
    if soltos:
        erros.append(f"marcadores fora do formato: {soltos}")


def verificar_dados_pessoais(texto: str) -> None:
    print("\n6. Dados pessoais")
    sem_puml = texto.split("## Anexo C")[0]
    achados = {
        "e-mail": re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", sem_puml),
        "sequência de 6 ou mais dígitos": re.findall(r"\b\d{6,}\b", sem_puml),
        "telefone": re.findall(r"\(?\b\d{2}\)?[ -]?9?\d{4}[- ]?\d{4}\b", sem_puml),
    }
    for nome, lista in achados.items():
        exemplos = [x for x in lista if x.lower().endswith("@exemplo.com") or x == "2026001"]
        lista = [x for x in lista if x not in exemplos]
        print(f"   {nome}: {len(lista)}" + (f" (mais {len(exemplos)} valores fictícios dos critérios de aceitação: {exemplos})" if exemplos else ""))
        if lista:
            erros.append(f"possível dado pessoal ({nome}): {lista[:3]}")


# ---------- estimativa de páginas ----------
def palavras(texto: str) -> int:
    return len(re.findall(r"\S+", re.sub(r"[|#]|-{3,}", " ", texto)))


CENARIOS = {
    "padrão (corpo 11 pt, tabelas 9 pt, margens 2,5 cm)": {"palavras": 500, "largura": 16.0, "cm": 6.2, "linhas": 50},
    "compacto (corpo 10 pt, tabelas 8 pt, margens 2,0 cm)": {"palavras": 600, "largura": 17.0, "cm": 7.0, "linhas": 58},
}


def paginas_de_tabela(bloco: str, c: dict) -> float:
    linhas = [[c.strip() for c in l.strip().strip("|").split("|")] for l in bloco.splitlines()
              if l.startswith("|") and not re.match(r"^\|[-| ]+\|$", l)]
    if not linhas:
        return 0.0
    colunas = len(linhas[0])
    media = [max(6, sum(len(l[k]) for l in linhas if k < len(l)) / len(linhas)) for k in range(colunas)]
    cm = [c['largura'] * m / sum(media) for m in media]
    total = 0.0
    for l in linhas:
        total += 0.4 + max(math.ceil(len(x) / (cm[k] * c['cm'])) for k, x in enumerate(l) if k < colunas)
    return total / c['linhas']


def estimar(corpo: str) -> None:
    print("\n7. Estimativa de páginas do corpo (sem capa e sem anexos)")
    cortes = [m for m in re.finditer(r"^## (\d+\. .+)$", corpo, re.M)]
    for nome, c in CENARIOS.items():
        total = 0.0
        print(f"   Cenário {nome}")
        for i, m in enumerate(cortes):
            fim = cortes[i + 1].start() if i + 1 < len(cortes) else len(corpo)
            bloco = corpo[m.end():fim]
            tabelas = "\n".join(l for l in bloco.splitlines() if l.startswith("|"))
            prosa = "\n".join(l for l in bloco.splitlines() if not l.startswith("|") and not l.startswith("!["))
            p_tab = paginas_de_tabela(tabelas, c) if tabelas else 0.0
            p_prosa = palavras(prosa) / c["palavras"]
            p_fig = 0.7 if "![Figura" in bloco else 0.0
            subtotal = p_tab + p_prosa + p_fig
            total += subtotal
            print(f"     {m.group(1)[:40]:<40} prosa {palavras(prosa):>5} pal. | tabela {p_tab:4.1f} | figura {p_fig:3.1f} | {subtotal:4.1f} pág.")
        folga = LIMITE_DE_PAGINAS - total
        print(f"     TOTAL: {total:.1f} páginas; limite {LIMITE_DE_PAGINAS}; folga {folga:+.1f}; meta {META_DE_PAGINAS}")
        if total > LIMITE_DE_PAGINAS:
            avisos.append(f"cenário {nome.split(' (')[0]}: {total:.1f} páginas, acima do limite de {LIMITE_DE_PAGINAS}")
        elif total > META_DE_PAGINAS:
            avisos.append(f"cenário {nome.split(' (')[0]}: {total:.1f} páginas, acima da meta de {META_DE_PAGINAS}")


def main() -> int:
    if not DOC.exists():
        print(f"Não achei {DOC.relative_to(RAIZ)}.")
        return 1
    texto = ler(DOC)
    corpo, anexos = corpo_e_anexos(texto)
    fonte = ids_da_fonte()
    print(f"Documento: {DOC.relative_to(RAIZ)} ({palavras(texto)} palavras no total; corpo {palavras(corpo)})")
    verificar_contagens(corpo, anexos, fonte)
    verificar_ids(corpo, anexos, fonte)
    verificar_referencias(corpo, fonte)
    verificar_valores(corpo)
    verificar_pendencias(texto)
    verificar_dados_pessoais(texto)
    estimar(corpo)
    print()
    for a in avisos:
        print("AVISO:", a)
    for e in erros:
        print("ERRO:", e)
    print("Resultado:", "FALHOU" if erros else "sem erros")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
