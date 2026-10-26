#!/usr/bin/env bash
# Injeta o conteudo integral dos guias operacionais do vault no inicio de cada
# sessao (SessionStart), para nao depender de o agente lembrar de ir le-los.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

exec python3 -I - "$ROOT/.discovery/guias" <<'PY'
import json, sys
from pathlib import Path

guias = Path(sys.argv[1])
nomes = ("GUIA-WIP.md", "GUIA-FRONTMATTER.md", "GUIA-FLUXO-DISCOVERY.md")
partes = [f"## {n}\n\n" + (guias / n).read_text(encoding="utf-8") for n in nomes if (guias / n).is_file()]
if partes:
    contexto = "# Guias operacionais do vault (injetados automaticamente)\n\n" + "\n\n---\n\n".join(partes)
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": contexto}}, ensure_ascii=False))
PY
