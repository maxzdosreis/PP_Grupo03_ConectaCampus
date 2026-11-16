from __future__ import annotations

import json
import os
import secrets
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SRC = RAIZ / "src"
COMPOSE_PROD = "docker-compose.prod.yml"
NOME_ESPERADO = "conecta-campus-prod"
EXEMPLO = SRC / ".env.prod.example"
OBRIGATORIAS = (
    "DJANGO_SECRET_KEY",
    "DJANGO_ALLOWED_HOSTS",
    "DB_DATABASE",
    "DB_USER",
    "DB_PASSWORD",
)
PORTAS_PROIBIDAS = {"5432": "banco", "8000": "backend", "6379": "redis"}


def variaveis_de_teste() -> dict[str, str]:
    return {
        "DJANGO_SECRET_KEY": secrets.token_urlsafe(64),
        "DJANGO_ALLOWED_HOSTS": "localhost,127.0.0.1",
        "DB_DATABASE": "verificacao",
        "DB_USER": "verificacao",
        "DB_PASSWORD": secrets.token_urlsafe(16),
    }


def gravar_env(pasta: Path, valores: dict[str, str]) -> Path:
    caminho = pasta / "variaveis.env"
    caminho.write_text("".join(f"{k}={v}\n" for k, v in valores.items()), encoding="utf-8")
    return caminho


def compose(env_file: Path, *argumentos: str) -> subprocess.CompletedProcess:
    ambiente = {k: v for k, v in os.environ.items() if k not in OBRIGATORIAS}
    return subprocess.run(
        ["docker", "compose", "-f", COMPOSE_PROD, "--env-file", str(env_file), *argumentos],
        cwd=SRC,
        env=ambiente,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


class Relatorio:
    def __init__(self) -> None:
        self.falhas = 0

    def conferir(self, ok: bool, texto: str, detalhe: str = "") -> None:
        print(f"[{'OK' if ok else 'FALHA'}] {texto}")
        if not ok:
            self.falhas += 1
            if detalhe:
                print(f"       {detalhe}")


def configuracao(env_file: Path, relatorio: Relatorio) -> dict | None:
    resultado = compose(env_file, "config", "--format", "json")
    relatorio.conferir(
        resultado.returncode == 0,
        "(a) docker compose config com as variáveis de exemplo termina com sucesso",
        resultado.stderr.strip()[-300:],
    )
    if resultado.returncode != 0:
        return None
    return json.loads(resultado.stdout)


def segredos_obrigatorios(pasta: Path, relatorio: Relatorio) -> None:
    for nome in OBRIGATORIAS:
        valores = variaveis_de_teste()
        del valores[nome]
        resultado = compose(gravar_env(pasta, valores), "config", "--quiet")
        ok = resultado.returncode != 0 and nome in resultado.stderr and "defina" in resultado.stderr
        relatorio.conferir(
            ok,
            f"(b) sem {nome} o compose falha pedindo o valor",
            f"código {resultado.returncode}; {resultado.stderr.strip()[-200:]}",
        )
        valores[nome] = ""
        vazio = compose(gravar_env(pasta, valores), "config", "--quiet")
        relatorio.conferir(vazio.returncode != 0, f"(b) {nome} vazia também falha")


def nome_e_isolamento(config: dict, relatorio: Relatorio) -> None:
    nome = config.get("name")
    relatorio.conferir(nome == NOME_ESPERADO, f"(c) name é '{NOME_ESPERADO}'", f"veio '{nome}'")
    padrao = (SRC / "docker-compose.yml").read_text(encoding="utf-8")
    relatorio.conferir(
        f"name: {NOME_ESPERADO}\n" not in padrao,
        "(c) o name é diferente do compose de desenvolvimento",
    )
    volumes = [v.get("name", "") for v in config.get("volumes", {}).values()]
    relatorio.conferir(
        bool(volumes) and all(v.startswith(NOME_ESPERADO) for v in volumes),
        "(c) volumes com nome próprio do modo de produção",
        str(volumes),
    )
    redes = [r.get("name", "") for r in config.get("networks", {}).values()]
    relatorio.conferir(
        bool(redes) and all(r.startswith(NOME_ESPERADO) for r in redes),
        "(c) rede com nome próprio do modo de produção",
        str(redes),
    )


def portas_e_volumes(config: dict, relatorio: Relatorio) -> None:
    servicos = config["services"]
    publicadas = {
        nome: [str(p.get("published")) for p in dados.get("ports", [])]
        for nome, dados in servicos.items()
    }
    so_o_nginx = {n: p for n, p in publicadas.items() if p}
    relatorio.conferir(
        list(so_o_nginx) == ["frontend"],
        "(d) só o frontend (nginx) publica porta no host",
        str(so_o_nginx),
    )
    proibidas = [
        f"{nome}:{porta}"
        for nome, portas in publicadas.items()
        for porta in portas
        if porta in PORTAS_PROIBIDAS
    ]
    relatorio.conferir(not proibidas, "(d) nenhuma porta de banco, backend ou redis publicada", str(proibidas))
    binds = [
        f"{nome}:{v.get('source')}"
        for nome, dados in servicos.items()
        for v in dados.get("volumes", [])
        if v.get("type") == "bind"
    ]
    relatorio.conferir(not binds, "(d) nenhum bind-mount (nem do código-fonte)", str(binds))
    env_file_usado = [n for n, d in servicos.items() if d.get("env_file")]
    relatorio.conferir(not env_file_usado, "(d) nenhum serviço usa env_file", str(env_file_usado))
    dev_no_comando = [
        n
        for n, d in servicos.items()
        if any(t in " ".join(d.get("command") or []) for t in ("runserver", "--reload", "npm run dev"))
    ]
    relatorio.conferir(not dev_no_comando, "(d) nenhum serviço roda runserver, --reload ou servidor de desenvolvimento")


def gitignore(relatorio: Relatorio) -> None:
    def ignorado(caminho: str) -> bool:
        return subprocess.run(["git", "check-ignore", "-q", caminho], cwd=RAIZ).returncode == 0

    relatorio.conferir(ignorado("src/.env.prod"), "(e) src/.env.prod está no .gitignore")
    relatorio.conferir(
        not ignorado("src/.env.prod.example"), "(e) src/.env.prod.example NÃO está ignorado (é versionado)"
    )


def exemplo_sem_valores(relatorio: Relatorio) -> None:
    linhas = [
        linha.strip()
        for linha in EXEMPLO.read_text(encoding="utf-8").splitlines()
        if linha.strip() and not linha.lstrip().startswith("#")
    ]
    com_valor = [linha.split("=")[0] for linha in linhas if linha.split("=", 1)[1].strip()]
    relatorio.conferir(not com_valor, "(f) .env.prod.example só tem nomes (nenhuma variável ativa com valor)", str(com_valor))
    nomes = {linha.split("=")[0] for linha in linhas}
    relatorio.conferir(set(OBRIGATORIAS) <= nomes, "(f) .env.prod.example lista as obrigatórias")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    relatorio = Relatorio()
    with tempfile.TemporaryDirectory() as temporario:
        pasta = Path(temporario)
        config = configuracao(gravar_env(pasta, variaveis_de_teste()), relatorio)
        if config is not None:
            nome_e_isolamento(config, relatorio)
            portas_e_volumes(config, relatorio)
        segredos_obrigatorios(pasta, relatorio)
    gitignore(relatorio)
    exemplo_sem_valores(relatorio)
    print(f"\n{'Tudo certo.' if not relatorio.falhas else f'{relatorio.falhas} verificação(ões) falharam.'}")
    return 1 if relatorio.falhas else 0


if __name__ == "__main__":
    raise SystemExit(main())
