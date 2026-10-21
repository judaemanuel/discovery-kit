"""Extrai texto, tabelas e imagens de .docx para Markdown (somente stdlib)."""
import sys, zipfile, re, os
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def run_text(el):
    out = []
    for n in el.iter():
        if n.tag == W + "t":
            out.append(n.text or "")
        elif n.tag == W + "tab":
            out.append("\t")
        elif n.tag in (W + "br", W + "cr"):
            out.append(" ")
    return "".join(out)


def images(el, rels):
    return [rels.get(b.get(R + "embed")) for b in el.iter(A + "blip") if b.get(R + "embed") in rels]


def roman(n):
    out = ""
    for v, s in ((1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"),
                 (50, "l"), (40, "xl"), (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")):
        while n >= v:
            out, n = out + s, n - v
    return out


def fmt(n, kind):
    if kind == "lowerLetter":
        return chr(96 + (n - 1) % 26 + 1)
    if kind == "upperLetter":
        return chr(64 + (n - 1) % 26 + 1)
    if kind == "lowerRoman":
        return roman(n)
    if kind == "upperRoman":
        return roman(n).upper()
    return str(n)


class Numbering:
    """Reconstrói os rótulos da numeração automática do Word (1., 2.2.1., a., i.)."""

    def __init__(self, z):
        self.nums, self.levels, self.count = {}, {}, {}
        if "word/numbering.xml" not in z.namelist():
            return
        root = ET.fromstring(z.read("word/numbering.xml"))
        for a in root.findall(W + "abstractNum"):
            lv = {}
            for l in a.findall(W + "lvl"):
                g = lambda tag, d: l.find(W + tag).get(W + "val") if l.find(W + tag) is not None else d
                lv[int(l.get(W + "ilvl"))] = (int(g("start", "1")), g("numFmt", "decimal"), g("lvlText", ""))
            self.levels[a.get(W + "abstractNumId")] = lv
        for n in root.findall(W + "num"):
            self.nums[n.get(W + "numId")] = n.find(W + "abstractNumId").get(W + "val")

    def label(self, p):
        """Retorna (rótulo, caminho) — caminho = valores formatados de cada nível (ex.: ['2','2','1'])."""
        pr = p.find(f"{W}pPr/{W}numPr")
        if pr is None or pr.find(W + "numId") is None:
            return None, None
        num_id = pr.find(W + "numId").get(W + "val")
        ilvl = int(pr.find(W + "ilvl").get(W + "val")) if pr.find(W + "ilvl") is not None else 0
        a = self.nums.get(num_id)
        lv = self.levels.get(a, {})
        if ilvl not in lv:
            return None, None
        c = self.count.setdefault(a, {})
        # Como no Word: nível pai ainda não usado conta como já exibido (start)
        for k in range(ilvl):
            if k in lv:
                c.setdefault(k, lv[k][0])
        c[ilvl] = c.get(ilvl, lv[ilvl][0] - 1) + 1
        for k in [k for k in c if k > ilvl]:
            del c[k]
        start, kind, text = lv[ilvl]
        if kind == "bullet":
            return "-", None
        val = lambda k: fmt(c.get(k, lv.get(k, (1,))[0]), lv.get(k, (1, "decimal"))[1])
        label = re.sub(r"%(\d)", lambda m: val(int(m.group(1)) - 1), text)
        return label, [val(k) for k in range(ilvl + 1)]


SECTION_IDS = (("não funcionais", "rnf"), ("requisitos funcionais", "rf"), ("regras de negócio", "rn"),
               ("introdução", "intro"))


def para(p, rels, styles, numbering, ctx=None):
    style = p.find(f"{W}pPr/{W}pStyle")
    sname = styles.get(style.get(W + "val"), style.get(W + "val")) if style is not None else ""
    text = run_text(p).strip()
    imgs = [f"![img](media/{os.path.basename(i)})" for i in images(p, rels)]
    label, path = numbering.label(p) if text else (None, None)
    m = re.match(r"(?i)(heading|título|titulo)\s*(\d)", sname)
    if text and m:
        text = "#" * min(int(m.group(2)) + 1, 6) + " " + text
    elif text and sname.lower().startswith("title"):
        text = "# " + text
    elif text and re.match(r"(?i)t[íi]tulo ?eds", sname):
        # Título de seção do documento de entrada (estilo próprio do template, sem nível numérico)
        text = "## " + (f"{label} " if label and label != "-" else "") + text
        if ctx is not None:
            ctx["sec"] = next((s for k, s in SECTION_IDS if k in text.lower()), "s" + (path or ["x"])[0])
    elif text and path:
        # Item numerado (2.2.1., 12., a., i.): rótulo reconstruído + block ID para link direto
        text = f"- **{label}** " + text
        if ctx is not None:
            bid = ctx.get("sec", "s0") + "-" + "-".join(path)
            while bid in ctx.setdefault("ids", set()):
                bid += "b"
            ctx["ids"].add(bid)
            text += f" ^{bid}"
            return "\n\n".join([text] + imgs)
    elif text and p.find(f"{W}pPr/{W}numPr") is not None:
        text = "- " + text
    return "\n".join([t for t in [text] + imgs if t])


def table(t, rels, styles, numbering):
    rows = []
    for tr in t.findall(W + "tr"):
        cells = []
        for tc in tr.findall(W + "tc"):
            parts = [para(p, rels, styles, numbering) for p in tc.iter(W + "p")]
            cells.append("<br>".join(x for x in parts if x).replace("|", "\\|").replace("\n", "<br>"))
        rows.append(cells)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    lines = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * width]
    lines += ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join(lines)


def convert(src, outdir):
    os.makedirs(os.path.join(outdir, "media"), exist_ok=True)
    z = zipfile.ZipFile(src)
    rels = {}
    for rel in ET.fromstring(z.read("word/_rels/document.xml.rels")):
        if rel.get("Type", "").endswith("/image"):
            rels[rel.get("Id")] = rel.get("Target")
    styles = {}
    if "word/styles.xml" in z.namelist():
        for s in ET.fromstring(z.read("word/styles.xml")).iter(W + "style"):
            n = s.find(W + "name")
            if n is not None:
                styles[s.get(W + "styleId")] = n.get(W + "val")
    for name in z.namelist():
        if name.startswith("word/media/"):
            with open(os.path.join(outdir, "media", os.path.basename(name)), "wb") as f:
                f.write(z.read(name))
    numbering = Numbering(z)
    body = ET.fromstring(z.read("word/document.xml")).find(W + "body")
    blocks, ctx = [], {}
    for el in body:
        if el.tag == W + "p":
            b = para(el, rels, styles, numbering, ctx)
        elif el.tag == W + "tbl":
            b = table(el, rels, styles, numbering)
        else:
            continue
        if b:
            blocks.append(b)
    out = os.path.join(outdir, os.path.splitext(os.path.basename(src))[0] + ".md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"<!-- Extraído automaticamente de {os.path.basename(src)} -->\n\n" + "\n\n".join(blocks) + "\n")
    print(out, len(blocks), "blocos,", len(os.listdir(os.path.join(outdir, "media"))), "imagens")


if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
