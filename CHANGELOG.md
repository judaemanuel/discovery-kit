# Changelog

## 0.2.0

Separação gerador/instância, no padrão do `catalisa`. **Incompatível com a 0.1.0**: recrie a instância com `install.sh`.

- O vault passa a viver em `scaffold/` (espelho exato de uma instância). A raiz do repositório é só o gerador: `install.sh`, `discovery-kit.json`, `CHANGELOG.md`, `docs/` e `tests/`.
- `install.sh` copia o scaffold, grava `.discovery-kit-version.json` e inicializa git na instância.
- Infraestrutura da instância em `.discovery/`: `guias/` (antes em `_WIP/` e `docs/`) e `tools/` (antes `.tools/`). `_WIP/` fica só com o trabalho diário. `_WIP/README.md` virou `.discovery/guias/GUIA-WIP.md`.
- Hook `SessionStart` reescrito em bash (`.claude/hooks/session-start.sh`, usa `python3` da stdlib). O hook PowerShell foi removido.
- `discovery-kit.json`: `version` e `sistema`, a lista de caminhos do gerador que uma atualização manual pode sobrescrever.

## 0.1.0

Scaffold extraído e genericizado em 2026-10-02 de um vault real de discovery: pastas `00-fontes` a `06-backlog`, guias de processo, frontmatter, hook PowerShell, scripts `.tools/`, skill `dd-arch-diagrams` e configuração do Obsidian.
