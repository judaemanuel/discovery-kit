#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
fail() { echo "FAIL: $1"; exit 1; }

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
PWD_REPO="$(pwd)"

# Caso 1: alvo novo, script chamado por caminho absoluto de outro cwd
( cd /tmp && bash "$PWD_REPO/install.sh" "$TMP/fresh" >/dev/null )
for p in README.md CLAUDE.md 03-analise-critica/README.md _WIP .discovery/guias/GUIA-FLUXO-DISCOVERY.md .discovery/tools/check_links.py .claude/hooks/session-start.sh .claude/skills/dd-arch-diagrams/SKILL.md .obsidian/app.json; do
  [ -e "$TMP/fresh/$p" ] || fail "install.sh não copiou $p"
done
[ -d "$TMP/fresh/.git" ] || fail "install.sh não inicializou git no alvo"
commits=$(git -C "$TMP/fresh" log --oneline | wc -l)
[ "$commits" -eq 1 ] || fail "esperado exatamente 1 commit no alvo, encontrado $commits"
[ ! -e "$TMP/fresh/docs" ] || fail "docs/ do gerador não deve ir para a instância"
[ ! -e "$TMP/fresh/install.sh" ] || fail "install.sh não deve ir para a instância"
manifest_version=$(grep -o '"version"[^,}]*' discovery-kit.json | grep -o '[0-9][0-9.]*')
grep -q "$manifest_version" "$TMP/fresh/.discovery-kit-version.json" || fail ".discovery-kit-version.json não reflete a version de discovery-kit.json"
grep -q '"instalado_em"' "$TMP/fresh/.discovery-kit-version.json" || fail ".discovery-kit-version.json sem campo instalado_em"

# Caso 2: alvo com conteúdo -> aborta sem apagar nada
mkdir -p "$TMP/existing"
echo "conteudo do usuario" > "$TMP/existing/nota-real.md"
set +e
bash "$PWD_REPO/install.sh" "$TMP/existing" 2>/dev/null
rc=$?
set -e
[ "$rc" -ne 0 ] || fail "install.sh deveria falhar quando o alvo já tem conteúdo"
[ -f "$TMP/existing/nota-real.md" ] || fail "install.sh apagou conteúdo real do usuário"
echo "PASS"
