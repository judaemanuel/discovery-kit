#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
fail() { echo "FAIL: $1"; exit 1; }
V=scaffold

# todo caminho .discovery-kit/.claude citado em CLAUDE.md, README e guias existe
for f in $V/CLAUDE.md $V/README.md $V/.discovery-kit/guias/*.md; do
  for p in $(grep -oE '\.(discovery-kit|claude)/[A-Za-z0-9_./-]*[A-Za-z0-9_]' "$f" | sort -u); do
    [ -e "$V/$p" ] || fail "$f cita caminho inexistente: $p"
  done
done

# sem resíduos dos caminhos da 0.1.0
if grep -rnE '_WIP/GUIA|_WIP/README|`\.tools|session-start\.(ps1|sh)' $V --include='*.md' --include='*.json' --include='*.py'; then
  fail "referência a caminho antigo no scaffold"
fi

# manifesto: versão e caminhos 'sistema' existem no scaffold
grep -q '"version"' discovery-kit.json || fail "discovery-kit.json sem version"
for p in $(grep -oE '"[^"]+"' discovery-kit.json | tr -d '"' | grep -E '^(\.|CLAUDE)'); do
  [ -e "$V/$p" ] || fail "discovery-kit.json lista 'sistema' inexistente: $p"
done

# os 3 guias são importados (@) no CLAUDE.md e os arquivos existem; sem hook
for g in GUIA-WIP GUIA-FRONTMATTER GUIA-FLUXO-DISCOVERY; do
  grep -qE "^- @\.discovery-kit/guias/$g\.md " $V/CLAUDE.md || fail "CLAUDE.md não importa $g"
  [ -f $V/.discovery-kit/guias/$g.md ] || fail "$g.md ausente"
done
for p in $(grep -oE '^- @[^ ]+' $V/CLAUDE.md | cut -c4-); do
  [ -f "$V/$p" ] || fail "@import quebrado: $p"
done
[ ! -e $V/.claude/hooks ] && [ ! -e $V/.claude/settings.json ] || fail "hook/settings não deveriam existir"

# READMEs de pasta abrem com frontmatter
for f in $V/0?-*/README.md; do
  [ "$(sed -n 1p "$f")" = "---" ] || fail "$f sem frontmatter"
done
echo "PASS"
