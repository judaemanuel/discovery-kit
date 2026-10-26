# discovery-kit

Gerador de um vault Obsidian + Claude Code para **discovery técnico/negócio** (levantamento de requisitos, análise crítica de especificações, elicitação de stakeholders, veredito GO/NO-GO para arquitetura). A partir de `scaffold/` ele cria uma instância pronta para uso e já versionada em git. O guia de uso da instância está em `scaffold/README.md`.

**Origem:** extraído e genericizado em 2026-10-02 a partir de um vault real, depois de um ciclo completo de uso (reuniões de elicitação, catálogos de dúvidas, veredito GO/NO-GO rastreado). O que está aqui é o que **comprovadamente** funcionou — não é um template teórico.

## Como instalar uma instância

```bash
./install.sh [caminho-do-destino]
```

Sem argumento, a instância é criada em `../discovery-instance`. O script copia `scaffold/` para o destino, grava `.discovery-kit-version.json` (versão do gerador e data) e faz o commit inicial. O destino precisa estar vazio ou não existir.

Requisitos: `bash`, `git` e `python3` (usado pelo hook `SessionStart` e pelos scripts de `.discovery/tools/`).

## Estrutura do repositório

| Caminho | O que é |
|---|---|
| `scaffold/` | Espelho exato de uma instância (vault, `.claude/`, `.discovery/`, `.obsidian/`) |
| `install.sh` | Cria uma instância a partir do scaffold |
| `discovery-kit.json` | Versão do gerador e lista `sistema` |
| `docs/` | Material do método (comparativo de metodologias, trilha greenfield, briefing, prompt de abertura). **Não** é copiado para a instância |
| `tests/` | Testes do gerador e do scaffold |

## Sem update automático

Instâncias já criadas não são atualizadas quando o gerador muda. Para portar uma mudança, compare a versão de `.discovery-kit-version.json` da instância com `discovery-kit.json` e copie de `scaffold/` os caminhos da lista `sistema`, atualizando `version` na instância. Todo o resto é conteúdo ou configuração do operador e nunca deve ser sobrescrito: notas, READMEs de pasta preenchidos e `.obsidian/`.

## Decisões de genericização a revisar

Ao extrair o scaffold, algumas escolhas de "o que generalizar vs. o que preservar" foram feitas por julgamento:
- `scaffold/04-elicitacao/README.md`: a "Onda 0" foi generalizada para "gates de compliance/privacidade/segurança a abrir no dia 1". Pode não se aplicar a todo projeto; ajuste ou remova se seu domínio não tiver gates regulatórios cedo.
- `scaffold/03-analise-critica/README.md`: a tabela "Status pós-reuniões" ficou como esqueleto vazio (2 linhas de exemplo), para mostrar a forma e não só descrevê-la.
- `.discovery/tools/check_links.py`: a lista `SKIP` e o conjunto `NOT_CONF` (exceções de ID) foram ajustados para este scaffold e esvaziados, respectivamente.
- `.discovery/tools/spec-citacoes.md`: o mais reescrito dos arquivos copiados; ficou só a estrutura de 7 regras e o formato de relatório.

## O que foi deixado de fora (de propósito)

- Plugins do Obsidian (binários/dados) e o tema Minimal: instale pelo *Community plugins* seguindo `scaffold/.discovery/guias/obsidian-config-replicar.md`. Não são vendorizados, para evitar código de terceiros desatualizado e credenciais salvas em `data.json`.
- `workspace.json` e `graph.json` do Obsidian: são estado de sessão, não configuração.
- Qualquer dado específico do projeto original (IDs de Confluence, nomes de pessoas/sistemas, achados reais).

## Versionamento

A versão do gerador é a fonte da verdade em `discovery-kit.json`. Histórico em `CHANGELOG.md`.
