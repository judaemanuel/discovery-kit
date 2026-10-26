# Changelog

## 0.3.1

Portabilidade (Linux, macOS e Windows/PowerShell) e nome da pasta de infraestrutura.

- `.discovery/` renomeada para `.discovery-kit/` (combina com `.discovery-kit-version.json` e `discovery-kit.json`).
- Hook `SessionStart` removido (`.claude/hooks/` e `.claude/settings.json`): dependia de `bash` e `python3`, que o PowerShell do Windows não oferece por padrão. Os 3 guias agora entram por `@import` no `CLAUDE.md` da instância, sem script.
- Documentado `python` ou `py` no Windows para rodar `dk.py` e `check_links.py`.
- `tests/test_scaffold.sh`: o teste de caminhos citados não cobria `.discovery-kit/`; corrigido. Novo teste de que os `@import` do `CLAUDE.md` existem e de que não há hook.

## 0.3.0

Validador do vault.

- `.discovery/tools/dk.py validar [VAULT] [--estrito]` (python3 stdlib): confere o frontmatter conforme `GUIA-FRONTMATTER` (tags `fase/area/tipo`, `status`, `atualizado`) e os IDs `Q/G/C/H/R/D` (formato, definição duplicada, referência sem definição). Os links são checados via `check_links.py`: viram avisos e só reprovam com `--estrito`.
- `tipo/indice` passa a dispensar `atualizado` (os READMEs do scaffold nunca tiveram o campo). Documentado em `GUIA-FRONTMATTER`.
- `03-analise-critica/README.md`: `H-01..` corrigido para `H-001..` (convenção `H-nnn`).
- `CLAUDE.md` da instância manda rodar o validador depois de editar conteúdo.
- Novo `tests/test_dk_py.sh`.

## 0.2.0

Separação gerador/instância, no padrão do `catalisa`. **Incompatível com a 0.1.0**: recrie a instância com `install.sh`.

- O vault passa a viver em `scaffold/` (espelho exato de uma instância). A raiz do repositório é só o gerador: `install.sh`, `discovery-kit.json`, `CHANGELOG.md`, `docs/` e `tests/`.
- `install.sh` copia o scaffold, grava `.discovery-kit-version.json` e inicializa git na instância.
- Infraestrutura da instância em `.discovery/`: `guias/` (antes em `_WIP/` e `docs/`) e `tools/` (antes `.tools/`). `_WIP/` fica só com o trabalho diário. `_WIP/README.md` virou `.discovery/guias/GUIA-WIP.md`.
- Hook `SessionStart` reescrito em bash (`.claude/hooks/session-start.sh`, usa `python3` da stdlib). O hook PowerShell foi removido.
- `discovery-kit.json`: `version` e `sistema`, a lista de caminhos do gerador que uma atualização manual pode sobrescrever.

## 0.1.0

Scaffold extraído e genericizado em 2026-10-02 de um vault real de discovery: pastas `00-fontes` a `06-backlog`, guias de processo, frontmatter, hook PowerShell, scripts `.tools/`, skill `dd-arch-diagrams` e configuração do Obsidian.
