"""Verifica wikilinks, âncoras, notas de rodapé e citações no formato antigo do vault."""
import os, re, sys, glob

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
SKIP = ("_WIP", "_temp", ".obsidian", ".tools")
NOT_CONF = set()  # preencha com IDs numéricos a ignorar (ex.: nº de apólice, build), se aplicável
OLD = re.compile(r"\[(?:WIKI:|ANX|RAW-\d|CONF:|FIGMA|EDS-[12][^\]]*)[^\]]*\](?!\])|\bid \d{8,10}\b")

files = [f for f in glob.glob(os.path.join(ROOT, "**", "*"), recursive=True) if os.path.isfile(f)]
by_name, by_path = {}, {}
for f in files:
    rel = os.path.relpath(f, ROOT).replace("\\", "/")
    stem = rel[:-3] if rel.endswith(".md") else rel
    by_path[stem.lower()] = f
    by_name.setdefault(os.path.basename(stem).lower(), []).append(f)


def resolve(target):
    t = target.strip().lower()
    if t in by_path:
        return by_path[t], None
    hits = [f for s, f in by_path.items() if s.endswith("/" + t) or s == t]
    if len(hits) == 1:
        return hits[0], None
    cands = by_name.get(os.path.basename(t), [])
    if len(cands) == 1:
        return cands[0], None
    return None, "ambíguo" if len(cands) > 1 or len(hits) > 1 else "inexistente"


anchors = {}


def has_anchor(f, a):
    if f not in anchors:
        s = open(f, encoding="utf-8").read() if f.endswith(".md") else ""
        heads = {re.sub(r"\s+", " ", h).strip().lower() for h in re.findall(r"^#{1,6} (.+)$", s, re.M)}
        blocks = set(re.findall(r"\s\^([A-Za-z0-9-]+)\s*$", s, re.M))
        anchors[f] = (heads, blocks)
    heads, blocks = anchors[f]
    if a.startswith("^"):
        return a[1:] in blocks
    return re.sub(r"\s+", " ", a).strip().lower() in heads


problems = 0
for f in files:
    rel = os.path.relpath(f, ROOT).replace("\\", "/")
    if not rel.endswith(".md") or rel.startswith(SKIP):
        continue
    s = open(f, encoding="utf-8").read()
    body = re.sub(r"`[^`\n]*`", "", s)
    out = []
    for m in re.finditer(r"!?\[\[([^\]]+?)\]\]", body):
        inner = m.group(1).replace("\\|", "|").split("|")[0]
        target, _, anchor = inner.partition("#")
        tf, err = resolve(target) if target else (f, None)
        if err:
            out.append(f"link {err}: [[{m.group(1)}]]")
        elif anchor and not has_anchor(tf, anchor):
            out.append(f"âncora inexistente: [[{m.group(1)}]]")
    refs = set(re.findall(r"(?<!^)\[\^([^\]]+)\]", body, re.M)) | set(re.findall(r"^\[\^([^\]]+)\](?!:)", body, re.M))
    for line in body.splitlines():
        if line.lstrip().startswith("|"):
            out += [f"'|' sem escape em tabela: [[{w}]]" for w in re.findall(r"\[\[([^\]]*?[^\\]\|[^\]]*)\]\]", line)]
    defs = set(re.findall(r"^\[\^([^\]]+)\]:", body, re.M))
    out += [f"rodapé sem definição: [^{r}]" for r in sorted(refs - defs)]
    out += [f"definição sem uso: [^{d}]" for d in sorted(defs - refs)]
    if not rel.startswith("00-fontes"):
        out += [f"citação antiga: {m.group(0)[:70]}" for m in OLD.finditer(body)]
        no_url = re.sub(r"\([^)\s]*https?://[^)\s]*\)|https?://\S+|\[\[[^\]]*\]\]", "", body)
        out += [f"ID solto: {n}" for n in re.findall(r"(?<![\d.+/-])\d{9,10}(?![\d])", no_url) if n not in NOT_CONF]
    if out:
        problems += len(out)
        print(f"\n## {rel} ({len(out)})")
        for o in out:
            print("  -", o)
print(f"\nTotal de problemas: {problems}")
