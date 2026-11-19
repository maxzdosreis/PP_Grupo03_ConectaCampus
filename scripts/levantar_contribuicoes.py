#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

INTEGRANTES = (
    "Eduardo Almeida da Cunha",
    "Kelvin Fraga da Silva",
    "Matheus Cezar Santos",
    "Max Zimmermann dos Reis",
)

FRENTES_GIT = {
    "Requisitos (docs/fontes/requisitos)": ["docs/fontes/requisitos"],
    "Modelagem (docs/fontes/modelagem)": ["docs/fontes/modelagem"],
    "Backend (src/backend)": ["src/backend"],
    "Frontend (src/frontend)": ["src/frontend"],
    "Infraestrutura (compose, .env.example, Dockerfiles)": [
        "src/docker-compose.yml",
        "src/.env.example",
        "src/backend/Dockerfile",
        "src/frontend/Dockerfile",
    ],
    "Documentação (docs, README)": ["docs", "README.md"],
}


def _sem_acento(texto: str) -> str:
    base = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in base if c.isascii() and not unicodedata.combining(c))


def _ler_csv(caminho: Path) -> list[dict[str, str]]:
    bruto = caminho.read_bytes()
    for codificacao in ("utf-8-sig", "cp1252"):
        try:
            texto = bruto.decode(codificacao)
            break
        except UnicodeDecodeError:
            continue
    else:  # pragma: no cover
        texto = bruto.decode("latin-1")
    return list(csv.DictReader(texto.splitlines()))


def _chave_da_frente(frente: str) -> str:
    """Chave só com letras ASCII, para tolerar acentos perdidos no CSV."""
    return "".join(c for c in _sem_acento(frente) if c.isalpha()) or "?"


def levantar_backlog(linhas: list[dict[str, str]]) -> None:
    por_pessoa: dict[str, list[dict[str, str]]] = defaultdict(list)
    for linha in linhas:
        por_pessoa[linha["responsavel"].strip()].append(linha)

    print(f"BACKLOG: {len(linhas)} tarefas, "
          f"{sum(int(x['pontos'] or 0) for x in linhas)} pontos")
    print("\nPor responsável registrado no backlog (nomes exatamente como estão):")
    for nome in sorted(por_pessoa, key=lambda n: (n == "", n)):
        tarefas = por_pessoa[nome]
        pontos = sum(int(t["pontos"] or 0) for t in tarefas)
        feitas = sum(t["status"] == "feito" for t in tarefas)
        rotulo = nome or "(sem responsável)"
        print(f"  {rotulo}: {len(tarefas)} tarefas, {pontos} pontos, {feitas} feitas")
        por_frente = Counter(_chave_da_frente(t["frente"]) for t in tarefas)
        print("    frentes: " + ", ".join(f"{k}={v}" for k, v in sorted(por_frente.items())))
        if not nome:
            print("    códigos: " + ", ".join(t["codigo"] for t in tarefas))

    print("\nIntegrantes sem nenhuma tarefa como responsável no backlog:")
    sem = [n for n in INTEGRANTES if n not in por_pessoa]
    print("  " + (", ".join(sem) if sem else "(todos aparecem)"))
    print("  Observação: o backlog usa um nome curto; nomes que não coincidem "
          "com o nome completo não são associados a ninguém por este script.")


def _autores(caminhos: list[str], raiz: Path, filtro: str = "--no-merges") -> Counter:
    saida = subprocess.run(
        ["git", "log", filtro, "--format=%an", *(["--", *caminhos] if caminhos else [])],
        cwd=raiz, capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout
    return Counter(l.strip() for l in saida.splitlines() if l.strip())


def levantar_git(raiz: Path) -> None:
    print("\nGIT: commits registrados em nome de cada nome de autor "
          "(sem merges; só nomes, nunca e-mails)")
    for frente, caminhos in FRENTES_GIT.items():
        autores = _autores(caminhos, raiz)
        total = sum(autores.values())
        print(f"\n  {frente}: {total} commits")
        if not autores:
            print("    sem registro")
        for nome, n in autores.most_common():
            marca = "" if nome in INTEGRANTES else "  (nome de autor que não é um dos quatro nomes completos)"
            print(f"    {n:4d}  {nome}{marca}")
    print("\n  Commits de merge (todo o repositório; o autor do merge pode diferir dos autores dos commits):")
    for nome, n in _autores([], raiz, "--merges").most_common():
        print(f"    {n:4d}  {nome}")
    print("\n  Integrantes sem nenhum commit (com ou sem merge) registrado em seu nome completo:")
    todos = _autores([], raiz) + _autores([], raiz, "--merges")
    sem = [n for n in INTEGRANTES if n not in todos]
    print("    " + (", ".join(sem) if sem else "(todos aparecem)"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--csv", required=True, type=Path, help="backlog-tarefas.csv (fora do repositório)")
    args = ap.parse_args()
    raiz = Path(__file__).resolve().parent.parent
    levantar_backlog(_ler_csv(args.csv))
    levantar_git(raiz)
    return 0


if __name__ == "__main__":
    sys.exit(main())
