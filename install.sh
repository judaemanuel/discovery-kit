#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-$SCRIPT_DIR/../discovery-instance}"

if [ -e "$TARGET" ] && [ -n "$(ls -A "$TARGET" 2>/dev/null)" ]; then
  echo "Erro: o alvo '$TARGET' já existe e não está vazio. Escolha outro diretório ou remova o conteúdo existente." >&2
  exit 1
fi

mkdir -p "$TARGET"
cp -r "$SCRIPT_DIR/scaffold/." "$TARGET/"

version=$(grep -o '"version"[^,}]*' "$SCRIPT_DIR/discovery-kit.json" | grep -o '[0-9][0-9.]*' | head -1)
instalado_em=$(date -Iseconds)

cat > "$TARGET/.discovery-kit-version.json" <<EOF
{"version": "$version", "instalado_em": "$instalado_em"}
EOF

git -C "$TARGET" init -q -b main
git -C "$TARGET" add -A
git -C "$TARGET" -c user.name="Discovery Kit Installer" -c user.email="discovery-kit@localhost" commit -q -m "chore: scaffold instance from discovery-kit"

echo "Instância criada com sucesso em: $TARGET"
