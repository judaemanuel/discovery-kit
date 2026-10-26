#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
fail() { echo "FAIL: $1"; exit 1; }
A=scaffold/adaptadores
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# contrato e esqueletos existem
grep -qi "nunca altera o núcleo" $A/README.md || fail "contrato sem a regra de não alterar o núcleo"
grep -qi "nenhum dado de cliente" $A/README.md || fail "contrato sem a regra de dados de cliente"
for f in proposta/esqueleto.md deck/gerar_deck.py deck/perfis.json deck/exemplo-dados.json deck/README.md; do
  [ -f $A/$f ] || fail "$f ausente"
done

# dk.py ignora adaptadores/ (arquivo sem frontmatter não reprova)
rm -rf "$TMP/v"; cp -r scaffold "$TMP/v"
echo "sem frontmatter" > "$TMP/v/adaptadores/proposta/livre.md"
python3 -I "$TMP/v/.discovery-kit/tools/dk.py" validar "$TMP/v" >/dev/null || fail "adaptadores/ não deveria ser validado"

# --validar: exemplo com [preencher] pendente reprova; dados completos passam
G=$A/deck/gerar_deck.py
set +e; python3 -I $G $A/deck/exemplo-dados.json --validar >/dev/null; rc=$?; set -e
[ "$rc" -eq 1 ] || fail "exemplo com [preencher] deveria reprovar na validação"
cat > "$TMP/ok.json" <<'JSON'
{"perfil": "padrao", "titulo": "Teste", "slides": [{"titulo": "A", "bullets": ["x"]}, {"titulo": "B", "tabela": {"cabecalho": ["c"], "linhas": [["v"]]}}]}
JSON
python3 -I $G "$TMP/ok.json" --validar >/dev/null || fail "dados completos deveriam validar"
sed -i 's/"padrao"/"inexistente"/' "$TMP/ok.json"
set +e; python3 -I $G "$TMP/ok.json" --validar >/dev/null; rc=$?; set -e
[ "$rc" -eq 1 ] || fail "perfil inexistente deveria reprovar"

# geração do .pptx só se python-pptx estiver instalado
if python3 -c "import pptx" 2>/dev/null; then
  sed -i 's/"inexistente"/"escuro"/' "$TMP/ok.json"
  python3 -I $G "$TMP/ok.json" "$TMP/saida.pptx"
  [ -s "$TMP/saida.pptx" ] || fail ".pptx não gerado"
else
  echo "(aviso) python-pptx ausente: geração do .pptx não testada"
fi
echo "PASS"
