#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
fail() { echo "FAIL: $1"; exit 1; }

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
V="$TMP/vault"
cp -r scaffold "$V"
DK="$V/.discovery-kit/tools/dk.py"
[ -f "$DK" ] || fail "$DK ausente"

note() { mkdir -p "$(dirname "$V/$1")"; cat > "$V/$1"; }
roda() { python3 -I "$DK" validar "$V" "$@"; }
# espera falha (exit 1) com uma mensagem
espera() { # arquivo-a-remover msg
  set +e; out=$(roda); rc=$?; set -e
  [ "$rc" -eq 1 ] || fail "esperado exit 1 para: $2 (rc=$rc)"
  echo "$out" | grep -qF "$2" || fail "mensagem ausente: $2"$'\n'"$out"
  rm -f "$V/$1"
}
OK='---
tags: [fase/analise, area/seguranca, tipo/analise]
status: hipotese
atualizado: 2026-10-26
---'

# vault limpo: sem erros, avisos de link não reprovam; --estrito reprova
roda >/dev/null || fail "vault limpo deveria validar"
set +e; roda --estrito >/dev/null; rc=$?; set -e
[ "$rc" -eq 1 ] || fail "--estrito deveria reprovar com avisos de link"

# arquivo válido, com definição e referência de ID, e CRLF
printf '%s\r\n\r\n| G-001 | lacuna |\r\n\r\nver G-001\r\n' "${OK//$'\n'/$'\r\n'}" > "$V/03-analise-critica/ok.md"
roda >/dev/null || fail "arquivo válido (CRLF, ID definido) deveria validar"
rm "$V/03-analise-critica/ok.md"

note 03-analise-critica/a.md <<<"sem frontmatter";                                    espera 03-analise-critica/a.md "sem frontmatter"
note 03-analise-critica/a.md <<<"${OK/hipotese/palpite}";                             espera 03-analise-critica/a.md "status 'palpite' inválido"
note 03-analise-critica/a.md <<<"${OK/fase\/analise, /}";                             espera 03-analise-critica/a.md "sem fase/*"
note 03-analise-critica/a.md <<<"${OK/area\/seguranca, /}";                           espera 03-analise-critica/a.md "sem area/*"
note 03-analise-critica/a.md <<<"${OK/, tipo\/analise/}";                             espera 03-analise-critica/a.md "sem tipo/*"
note 03-analise-critica/a.md <<<"${OK/tipo\/analise/tipo\/inventada}";                espera 03-analise-critica/a.md "tipo/inventada desconhecido"
note 03-analise-critica/a.md <<<"${OK/2026-10-26/26-10-2026}";                        espera 03-analise-critica/a.md "fora do formato YYYY-MM-DD"
note 03-analise-critica/a.md <<<"${OK/atualizado: 2026-10-26/}";                      espera 03-analise-critica/a.md "atualizado ausente"
note 00-fontes/a.md <<<"${OK/tipo\/analise/tipo\/fonte-bruta}";                       espera 00-fontes/a.md "exige status rascunho"
note 03-analise-critica/a.md <<<"$OK"$'\n\n'"ver Q-12";                               espera 03-analise-critica/a.md "Q-12 fora do formato"
note 03-analise-critica/a.md <<<"$OK"$'\n\n'"ver R-009";                              espera 03-analise-critica/a.md "R-009 referenciado sem definição"
note 03-analise-critica/a.md <<<"$OK"$'\n\n| G-001 | x |'
note 03-analise-critica/b.md <<<"$OK"$'\n\n| G-001 | y |'
set +e; out=$(roda); rc=$?; set -e
[ "$rc" -eq 1 ] && echo "$out" | grep -qF "G-001 definido mais de uma vez" || fail "ID duplicado não detectado"$'\n'"$out"
rm "$V/03-analise-critica/a.md" "$V/03-analise-critica/b.md"

# tipos da fase de solução/plano: adr, backlog, estimativa
for t in adr backlog estimativa; do
  novo="${OK/fase\/analise/fase\/solucao}"
  note 05-arquitetura/novo.md <<<"${novo/tipo\/analise/tipo\/$t}"
  roda >/dev/null || fail "tipo/$t deveria validar"
  rm "$V/05-arquitetura/novo.md"
done

# arquivos fora do escopo não são validados
note _WIP/2026-10-26/plano-x.md <<<"sem frontmatter, R-9"
roda >/dev/null || fail "_WIP não deveria ser validado"
echo "PASS"
