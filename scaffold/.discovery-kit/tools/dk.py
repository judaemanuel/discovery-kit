#!/usr/bin/env python3
"""Validação do vault Discovery Kit (stdlib only).

Uso: dk.py validar [VAULT] [--estrito]
Checa frontmatter (GUIA-FRONTMATTER), IDs (Q/G/C/H/R/D) e links (check_links.py).
Erros de frontmatter/ID reprovam; avisos de link só reprovam com --estrito.
"""
import re
import subprocess
import sys
from pathlib import Path

IGNORAR = {"_WIP", "_temp", ".discovery-kit", ".claude", ".obsidian", ".git"}
FASES = {"contexto", "entendimento", "analise", "elicitacao", "solucao", "plano"}
TIPOS = {"fonte-bruta", "reuniao", "entrada", "anexo-calculo", "wiki", "glossario",
         "inventario", "analise", "duvidas-tecnicas", "elicitacao", "indice",
         "adr", "backlog", "estimativa"}
STATUS = {"rascunho", "hipotese", "validado", "em-aberto"}
DATA_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# prefixo -> mínimo de dígitos (Q-nnn, G-nnn, C-nn, H-nnn, R-nnn, D-nnn)
IDS = {"Q": 3, "G": 3, "C": 2, "H": 3, "R": 3, "D": 3}
ID_RE = re.compile(r"(?<![\w-])([QGCHRD])-(\d+)(?![\w-])")
DEF_RE = re.compile(r"^\s*(?:\|\s*|#{1,6}\s+)\**([QGCHRD])-(\d+)\b", re.M)


def frontmatter(texto):
    linhas = texto.splitlines()
    if not linhas or linhas[0].strip() != "---":
        return {}
    fm, chave = {}, None
    for linha in linhas[1:]:
        if linha.strip() == "---":
            break
        item = re.match(r"^\s+-\s*(.*)$", linha)
        if item and chave:
            fm[chave].append(item.group(1).strip().strip("\"'"))
            continue
        par = re.match(r"^([A-Za-z_]+):\s*(.*)$", linha)
        if not par:
            continue
        chave, valor = par.group(1), par.group(2).strip()
        if valor.startswith("[") and valor.endswith("]"):
            fm[chave] = [v.strip().strip("\"'") for v in valor[1:-1].split(",") if v.strip()]
        elif valor == "":
            fm[chave] = []
        else:
            fm[chave] = valor.strip("\"'")
    return fm


def conteudo(vault):
    for p in sorted(vault.rglob("*.md")):
        rel = p.relative_to(vault)
        if rel.parts[0] in IGNORAR or rel == Path("CLAUDE.md"):
            continue
        yield rel, p.read_text(encoding="utf-8")


def erros_frontmatter(fm):
    if not fm:
        return ["sem frontmatter"]
    tags = fm.get("tags")
    if not isinstance(tags, list) or not tags:
        return ["tags ausente ou vazia"]
    e, ns = [], {"fase": set(), "area": set(), "tipo": set()}
    for t in tags:
        n, _, v = t.partition("/")
        if n not in ns or not v:
            e.append(f"tag '{t}' fora do formato fase/*, area/*, tipo/*")
        else:
            ns[n].add(v)
    e += [f"fase/{v} desconhecida" for v in sorted(ns["fase"] - FASES)]
    e += [f"tipo/{v} desconhecido" for v in sorted(ns["tipo"] - TIPOS)]
    tipos = ns["tipo"]
    if not tipos:
        e.append("tags sem tipo/*")
    indice = "indice" in tipos
    if not ns["fase"] and not indice:
        e.append("tags sem fase/* (só tipo/indice dispensa)")
    if not ns["area"] and not tipos & {"indice", "glossario"}:
        e.append("tags sem area/* (só tipo/indice ou tipo/glossario dispensam)")
    status = fm.get("status", "")
    if status not in STATUS:
        e.append(f"status '{status}' inválido (válidos: {' | '.join(sorted(STATUS))})")
    elif "fonte-bruta" in tipos and status != "rascunho":
        e.append("tipo/fonte-bruta exige status rascunho")
    data = fm.get("atualizado")
    if data is None:
        if not indice:
            e.append("atualizado ausente")
    elif not DATA_RE.match(str(data)):
        e.append(f"atualizado '{data}' fora do formato YYYY-MM-DD")
    return e


def erros_ids(arquivos):
    """arquivos: lista de (rel, texto, fm). Devolve {rel: [msg]}."""
    saida, defs = {}, {}
    vistos = [(r, t, fm) for r, t, fm in arquivos if r.parts[0] != "00-fontes"]
    for rel, texto, _ in vistos:
        for m in DEF_RE.finditer(texto):
            defs.setdefault((m.group(1), int(m.group(2))), []).append((str(rel), m.group(2)))
    for rel, texto, fm in vistos:
        e = saida.setdefault(str(rel), [])
        indice = "tipo/indice" in (fm.get("tags") or [])
        for p, n in sorted({m.groups() for m in ID_RE.finditer(texto)}):
            if len(n) < IDS[p]:
                e.append(f"ID {p}-{n} fora do formato (mínimo {IDS[p]} dígitos)")
            elif not indice and (p, int(n)) not in defs:
                e.append(f"{p}-{n} referenciado sem definição")
    for (p, n), locais in defs.items():
        if len(locais) > 1:
            onde = ", ".join(sorted({r for r, _ in locais}))
            for r in {r for r, _ in locais}:
                saida.setdefault(r, []).append(f"{p}-{locais[0][1]} definido mais de uma vez ({onde})")
    return saida


def avisos_links(vault):
    script = Path(__file__).with_name("check_links.py")
    r = subprocess.run([sys.executable, "-I", str(script), str(vault)], capture_output=True, text=True)
    m = re.search(r"Total de problemas: (\d+)", r.stdout)
    return int(m.group(1)) if m else 0, r.stdout


def validar(vault, estrito=False):
    arquivos = [(r, t, frontmatter(t)) for r, t in conteudo(vault)]
    falhas = []
    for rel, _, fm in arquivos:
        falhas += [f"{rel}: {m}" for m in erros_frontmatter(fm)]
    for rel, msgs in sorted(erros_ids(arquivos).items()):
        falhas += [f"{rel}: {m}" for m in msgs]
    for m in falhas:
        print(m)
    n_links, detalhe = avisos_links(vault)
    if n_links:
        print(f"\n## Links ({n_links} aviso(s), via check_links.py)")
        print(detalhe.rsplit("Total de problemas", 1)[0].rstrip())
    print(f"\n{len(falhas)} erro(s), {n_links} aviso(s) de link")
    return 1 if falhas or (estrito and n_links) else 0


def main(argv):
    if not argv or argv[0] != "validar":
        print(__doc__.strip())
        return 2
    estrito = "--estrito" in argv
    resto = [a for a in argv[1:] if a != "--estrito"]
    return validar(Path(resto[0] if resto else ".").resolve(), estrito)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
