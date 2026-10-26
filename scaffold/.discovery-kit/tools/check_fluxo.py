#!/usr/bin/env python3
"""Verifica se o fluxo do discovery voltou para as pastas definitivas (stdlib only).

Uso: check_fluxo.py [VAULT] [--resumo] [--dias N] [--hoje YYYY-MM-DD]
Só heurísticas objetivas. Sempre sai com código 0: são avisos, não bloqueio.
--resumo imprime no máximo 15 linhas (para ler ao abrir e ao encerrar o dia).
"""
import re
import sys
from datetime import date
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dk  # noqa: E402  (reaproveita frontmatter e validação do dk.py)

DATA_DIA = re.compile(r"^\d{4}-\d{2}-\d{2}$")
NIVEL_RE = re.compile(r"^\*\*GO-([ABC]):\*\*\s*(.+?)\s*$", re.M)
VAZIOS = {"", "-", "—", "n/a", "sem fonte", "nenhuma"}
FONTE_RE = re.compile(r"decis|00-fontes|fonte|mandato|aprovad|confirmad", re.I)


def e_data(txt):
    return bool(DATA_DIA.match(str(txt)))


def data(txt):
    return date.fromisoformat(txt) if e_data(txt) else None


def mencoes(vault):
    """Lista (data, texto) de cada _resumo.md diário e de cada linha datada do Log."""
    saida = []
    wip = vault / "_WIP"
    if wip.is_dir():
        for pasta in sorted(wip.iterdir()):
            resumo = pasta / "_resumo.md"
            if pasta.is_dir() and e_data(pasta.name) and resumo.is_file():
                saida.append((data(pasta.name), resumo.read_text(encoding="utf-8")))
    readme = vault / "README.md"
    if readme.is_file():
        em_log = False
        for linha in readme.read_text(encoding="utf-8").splitlines():
            if linha.startswith("#"):
                em_log = linha.lstrip("# ").strip().lower() == "log"
            elif em_log and linha.lstrip().startswith("|"):
                primeira = linha.strip().strip("|").split("|")[0].strip()
                if e_data(primeira):
                    saida.append((data(primeira), linha))
    return saida


def aviso_atualizado(arquivos, vault):
    """1. `atualizado:` anterior à data mais recente em que o ID ou o nome do arquivo aparece."""
    avisos, mencionados = [], mencoes(vault)
    for rel, texto, fm in arquivos:
        if "_templates" in rel.parts or not e_data(fm.get("atualizado", "")):
            continue
        atual = data(fm["atualizado"])
        ids = {f"{p}-{n}" for p, n in dk.DEF_RE.findall(texto)}
        chaves = [rf"(?<![\w-]){re.escape(rel.stem)}(?![\w-])"] + [rf"(?<![\w-]){re.escape(i)}(?![\w-])" for i in sorted(ids)]
        recentes = [d for d, t in mencionados if any(re.search(c, t) for c in chaves)]
        if recentes and max(recentes) > atual:
            avisos.append(f"[atualizado-antigo] {rel}: atualizado {atual} < {max(recentes)} (citado em resumo ou Log depois da última edição)")
    return avisos


def linhas_retornos(resumo):
    """Linhas da tabela sob o título 'Retornos ao fluxo' de um _resumo.md."""
    saida, dentro = [], False
    for linha in resumo.read_text(encoding="utf-8").splitlines():
        if linha.startswith("#"):
            dentro = "retornos ao fluxo" in linha.lower()
        elif dentro and linha.lstrip().startswith("|"):
            saida.append(linha)
    return saida


def aviso_wip(vault, hoje, dias):
    """2. _WIP/<dia>/ com mais de N dias e arquivos fora da tabela 'Retornos ao fluxo'."""
    avisos, wip = [], vault / "_WIP"
    if not wip.is_dir():
        return avisos
    for pasta in sorted(wip.iterdir()):
        if not (pasta.is_dir() and e_data(pasta.name)):
            continue
        idade = (hoje - data(pasta.name)).days
        resumo = pasta / "_resumo.md"
        linhas = linhas_retornos(resumo) if resumo.is_file() else []
        if idade > dias:
            sem = [str(p.relative_to(pasta)) for p in sorted(pasta.rglob("*"))
                   if p.is_file() and p.name != "_resumo.md" and not any(p.name in l for l in linhas)]
            if sem:
                avisos.append(f"[wip-nao-classificado] _WIP/{pasta.name}: {len(sem)} arquivo(s) sem destino em 'Retornos ao fluxo' ({', '.join(sem[:3])})")
        if idade > 2:
            pend = [l for l in linhas if "pendente" in l.lower() and "justificad" not in l.lower()]
            if pend:
                avisos.append(f"[retorno-pendente] _WIP/{pasta.name}: {len(pend)} retorno(s) pendente(s) sem justificativa há {idade} dias")
    return avisos


def nivel(valor):
    v = valor.lower()
    if "[preencher" in v:
        return None
    if v.startswith("no-go"):
        return 0
    return 1 if "condicionado" in v else 2


def aviso_go(vault):
    """3. Veredito por nível sem o artefato que ele libera, ou fora de ordem."""
    readme = vault / "03-analise-critica" / "README.md"
    if not readme.is_file():
        return []
    niveis = {k: nivel(v) for k, v in NIVEL_RE.findall(readme.read_text(encoding="utf-8"))}
    avisos = []
    for a, b in (("A", "B"), ("B", "C")):
        if niveis.get(a) is not None and niveis.get(b) is not None and niveis[b] > niveis[a]:
            avisos.append(f"[go-ordem] 03-analise-critica/README.md: GO-{b} mais positivo que GO-{a}")
    if (niveis.get("A") or 0) >= 1:
        pasta = vault / "05-arquitetura"
        conteudo = [p for p in pasta.rglob("*.md") if p.name != "README.md" and "_templates" not in p.parts] if pasta.is_dir() else []
        if not conteudo:
            avisos.append("[go-sem-artefato] 05-arquitetura: GO-A >= condicionado e a pasta não tem abordagens, ADRs nem diagramas")
    if (niveis.get("B") or 0) >= 1:
        tamanhos = re.compile(r"\|\s*(S|M|L|XL)\s*\|")
        pasta = vault / "06-backlog"
        if not any(tamanhos.search(p.read_text(encoding="utf-8")) for p in pasta.rglob("*.md") if "calibracao" not in p.name):
            avisos.append("[go-sem-artefato] 06-backlog: GO-B >= condicionado e nenhum item tem tamanho")
    return avisos


def aviso_frontmatter(arquivos):
    """4. Arquivo de conteúdo sem frontmatter válido (mesma regra do dk.py)."""
    return [f"[frontmatter] {rel}: {m}" for rel, _, fm in arquivos for m in dk.erros_frontmatter(fm)]


def aviso_validado(arquivos):
    """5. `status: validado` sem nenhuma referência a decisão ou fonte."""
    return [f"[validado-sem-fonte] {rel}: validado sem citar decisão nem fonte de quem tem mandato"
            for rel, texto, fm in arquivos
            if fm.get("status") == "validado" and "indice" not in (t.partition("/")[2] for t in fm.get("tags", []))
            and not FONTE_RE.search(texto)]


def aviso_nfr(arquivos):
    """6. RNF-nnn sem Origem e sem status `lacuna` no PB macro."""
    avisos = []
    for rel, texto, fm in arquivos:
        if "tipo/backlog" not in fm.get("tags", []):
            continue
        cab = None
        for linha in texto.splitlines():
            cel = [c.strip() for c in linha.strip().strip("|").split("|")] if linha.lstrip().startswith("|") else None
            if cel and "ID" in cel and "Origem" in cel and "Status" in cel:
                cab = cel
            elif cel and cab and re.match(r"RNF-\d+", cel[0]) and len(cel) == len(cab):
                reg = dict(zip(cab, cel))
                if reg["Status"].lower() != "lacuna" and reg["Origem"].lower() in VAZIOS:
                    avisos.append(f"[nfr-sem-fonte] {rel}: {cel[0]} sem origem e sem status lacuna")
    return avisos


def verificar(vault, hoje, dias):
    arquivos = [(r, t, dk.frontmatter(t)) for r, t in dk.conteudo(vault)]
    return (aviso_atualizado(arquivos, vault) + aviso_wip(vault, hoje, dias) + aviso_go(vault)
            + aviso_frontmatter(arquivos) + aviso_validado(arquivos) + aviso_nfr(arquivos))


def main(argv):
    opcoes, pos, i = {}, [], 0
    while i < len(argv):
        if argv[i] in ("--dias", "--hoje"):
            opcoes[argv[i]] = argv[i + 1]
            i += 2
        else:
            (opcoes.__setitem__(argv[i], True) if argv[i].startswith("--") else pos.append(argv[i]))
            i += 1
    avisos = verificar(Path(pos[0] if pos else ".").resolve(),
                       date.fromisoformat(opcoes["--hoje"]) if "--hoje" in opcoes else date.today(),
                       int(opcoes.get("--dias", 3)))
    resumo = bool(opcoes.get("--resumo"))
    limite = len(avisos) if not resumo or len(avisos) <= 14 else 13
    print(f"check_fluxo: {len(avisos)} aviso(s)")
    for a in avisos[:limite]:
        print(a)
    if len(avisos) > limite:
        print(f"... +{len(avisos) - limite} (rode sem --resumo)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
