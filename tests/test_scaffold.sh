#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
fail() { echo "FAIL: $1"; exit 1; }
V=scaffold

# todo caminho .discovery-kit/.claude citado em CLAUDE.md, README e guias existe
for f in $V/CLAUDE.md $V/README.md $V/.discovery-kit/guias/*.md; do
  for p in $(grep -oE '\.(discovery|claude)/[A-Za-z0-9_./-]*[A-Za-z0-9_]' "$f" | sort -u); do
    [ -e "$V/$p" ] || fail "$f cita caminho inexistente: $p"
  done
done

# sem resíduos dos caminhos da 0.1.0
if grep -rnE '_WIP/GUIA|_WIP/README|`\.tools|session-start\.ps1' $V --include='*.md' --include='*.json' --include='*.py'; then
  fail "referência a caminho antigo no scaffold"
fi

# manifesto: versão e caminhos 'sistema' existem no scaffold
grep -q '"version"' discovery-kit.json || fail "discovery-kit.json sem version"
for p in $(grep -oE '"[^"]+"' discovery-kit.json | tr -d '"' | grep -E '^(\.|CLAUDE)'); do
  [ -e "$V/$p" ] || fail "discovery-kit.json lista 'sistema' inexistente: $p"
done

# hook: executável e emite JSON válido com os 3 guias
[ -x $V/.claude/hooks/session-start.sh ] || fail "session-start.sh não é executável"
out=$(bash $V/.claude/hooks/session-start.sh)
echo "$out" | python3 -I -c '
import json, sys
d = json.load(sys.stdin)["hookSpecificOutput"]
assert d["hookEventName"] == "SessionStart"
for g in ("GUIA-WIP.md", "GUIA-FRONTMATTER.md", "GUIA-FLUXO-DISCOVERY.md"):
    assert "## " + g in d["additionalContext"], g
' || fail "saída do hook inválida"
grep -q 'session-start.sh' $V/.claude/settings.json || fail "settings.json não aponta para session-start.sh"

# READMEs de pasta abrem com frontmatter
for f in $V/0?-*/README.md; do
  [ "$(sed -n 1p "$f")" = "---" ] || fail "$f sem frontmatter"
done
echo "PASS"
