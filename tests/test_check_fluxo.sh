#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
fail() { echo "FAIL: $1"; exit 1; }

CF=scaffold/.discovery-kit/tools/check_fluxo.py
FIX=tests/fixtures/vault-desvios
roda() { python3 -I "$CF" "$@"; }

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# scaffold vazio: zero avisos, exit 0
out=$(roda scaffold) || fail "check_fluxo deve sair com 0 no scaffold"
echo "$out" | grep -qF "0 aviso(s)" || fail "scaffold vazio deveria ter 0 avisos"$'\n'"$out"

# fixture: exatamente os 4 desvios plantados, exit 0
out=$(roda "$FIX" --hoje 2026-03-10) || fail "check_fluxo nunca deve bloquear (exit 0)"
[ "$(echo "$out" | grep -c '^\[')" -eq 4 ] || fail "esperado exatamente 4 avisos"$'\n'"$out"
for c in atualizado-antigo wip-nao-classificado go-sem-artefato nfr-sem-fonte; do
  echo "$out" | grep -qF "[$c]" || fail "desvio não detectado: $c"$'\n'"$out"
done

# console cp1252 (PowerShell do Windows) não pode quebrar a saída
PYTHONIOENCODING=cp1252:strict python3 "$CF" "$FIX" --hoje 2026-03-10 >/dev/null 2>&1 || fail "saída quebra em console cp1252"

# corrigir um desvio remove só o aviso dele
cp -r "$FIX" "$TMP/v"
sed -i 's/atualizado: 2026-03-01/atualizado: 2026-03-10/' "$TMP/v/04-elicitacao/perguntas-por-area.md"
out=$(roda "$TMP/v" --hoje 2026-03-10)
echo "$out" | grep -qF "[atualizado-antigo]" && fail "aviso persiste após corrigir atualizado"
[ "$(echo "$out" | grep -c '^\[')" -eq 3 ] || fail "esperado 3 avisos após a correção"$'\n'"$out"

# --resumo: no máximo 15 linhas, mesmo com muitos avisos, e exit 0
for i in $(seq 1 20); do echo "sem frontmatter" > "$TMP/v/04-elicitacao/n$i.md"; done
out=$(roda "$TMP/v" --hoje 2026-03-10 --resumo) || fail "--resumo deve sair com 0"
[ "$(echo "$out" | wc -l)" -le 15 ] || fail "--resumo passou de 15 linhas"$'\n'"$out"
echo "$out" | grep -qF "rode sem --resumo" || fail "--resumo deveria indicar avisos omitidos"
echo "PASS"
