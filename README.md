---
tags: [tipo/indice]
status: validado
aliases: ["Índice — Discovery Kit"]
---

# Discovery Kit

**Origem:** extraído e genericizado em 2026-10-02 a partir de um vault real de discovery, depois de um ciclo completo de uso (reuniões de elicitação, catálogos de dúvidas, veredito GO/NO-GO rastreado). O que está aqui é o que **comprovadamente** funcionou — não é um template teórico.

## BLUF

Um esqueleto de vault Obsidian + Claude Code para condução de **discovery técnico/negócio** (levantamento de requisitos, análise crítica de especificações, elicitação de stakeholders, veredito GO/NO-GO para arquitetura), com:
- Estrutura de pastas por etapa (fonte → contexto → entendimento → análise → elicitação → arquitetura → backlog)
- Convenções de frontmatter, nomenclatura e IDs (`Q-nnn`, `G-nnn`, `C-nn`, `H-nnn`, `R-nnn`, `D-nnn`)
- Um **loop de processo explícito** entre análise crítica e elicitação (ver `_WIP/GUIA-FLUXO-DISCOVERY.md`) — a lição mais cara do projeto original foi não ter esse loop fechado em tempo real
- `CLAUDE.md` + hook `SessionStart` que injeta os guias de processo automaticamente em toda sessão Claude Code
- Configuração do Obsidian (tema, plugins, grafo colorido por fase) documentada para replicação manual

## Como usar

1. **Copie esta pasta** para a raiz do novo projeto (ex.: `C:\...\OneDrive\<novo-discovery>\`).
2. **Abra como vault no Obsidian** a partir dessa pasta. Siga `docs/obsidian-config-replicar.md` para instalar tema/plugins/grafo (nada é vendorizado aqui — veja "O que foi deixado de fora" abaixo).
3. **Abra o Claude Code** com essa pasta como diretório de trabalho — `CLAUDE.md` e o hook `SessionStart` carregam automaticamente; não precisa fazer nada manual.
4. **Popule `00-fontes/`** com os documentos originais do seu discovery (specs, EDS, PRDs, etc.).
5. **Leia `_WIP/GUIA-FLUXO-DISCOVERY.md`** antes de começar — explica o loop `03-analise-critica/` ↔ `04-elicitacao/` ↔ reunião real, que é o motivo deste scaffold existir.
6. **Preencha os `README.md` de `03-analise-critica/` e `04-elicitacao/`** primeiro — eles têm os `[preencher]` que forçam você a declarar as condições de GO/NO-GO e as ondas de entrevista antes de começar a trabalhar, não depois.
7. Antes do primeiro uso real, rode `.tools/check_links.py .` para validar os wikilinks. **Esperado hoje (scaffold vazio): ~19 avisos** — a maioria é link para arquivo que você ainda vai criar (`stakeholders.md`, `contradicoes.md`, etc. — fazem parte do conteúdo do discovery, não do scaffold) ou falso-positivo do próprio script com `README.md` duplicado por pasta e `\|` escapado em célula de tabela. Rode de novo depois de criar o conteúdo real — aí os avisos restantes são genuínos.

## Estrutura

| Pasta | Etapa | Pergunta que responde |
|---|---|---|
| `00-fontes/` | — | O que foi dito/escrito, literalmente? (fonte da verdade, não editar) |
| `01-contexto/` | 0 — Contexto | O que já existe hoje? |
| `02-entendimento/` | 1 — Entendimento | O que os documentos de entrada pedem? (EDS, PRD, e-mail, ticket — o que houver) |
| `03-analise-critica/` | 2 — Análise | O que não bate, o que falta, podemos avançar? |
| `04-elicitacao/` | 2→3 — Elicitação | O que perguntar, a quem, o que já foi perguntado? |
| `05-arquitetura/` | 3 — Solução (futuro) | Como construir, dado que já podemos avançar? |
| `06-backlog/` | 4 — Plano (futuro) | O que entregar, em que ordem? |
| `_WIP/` | — | Trabalho em andamento, ordenado por dia (ver guia dentro) |
| `.tools/` | — | Scripts de apoio (extração docx, inspeção xlsx, checagem de links) |

## O que está aqui vs. o que você precisa preencher

**Pronto para usar:**
- `CLAUDE.md`, `.claude/settings.json`, `.claude/hooks/session-start.ps1` — automação de contexto, portáveis como estão.
- `_WIP/README.md`, `_WIP/GUIA-FRONTMATTER.md`, `_WIP/GUIA-FLUXO-DISCOVERY.md` — guias de processo, genéricos.
- `.tools/*.py` + `spec-citacoes.md` — scripts e convenção de citação, genéricos.
- `.obsidian/*.json` + `snippets/pastas.css` — config estrutural do Obsidian.

**Precisa preencher (`[preencher]` nos arquivos):**
- `01-contexto/README.md`, `02-entendimento/README.md`, `03-analise-critica/README.md`, `04-elicitacao/README.md` — templates com a estrutura/seções que funcionaram, mas sem conteúdo (são o produto deste discovery, não deste scaffold).

**O que foi deixado de fora (de propósito):**
- Plugins do Obsidian em si (binários/dados) e o tema Minimal — instale via *Settings → Community plugins* seguindo `docs/obsidian-config-replicar.md`. Não vendorizamos para evitar código de terceiros desatualizado e risco de credenciais salvas em `data.json` de algum plugin.
- `workspace.json` e `graph.json` do Obsidian — são estado de sessão (abas abertas, posição de nós), não configuração; recrie o grafo por cor seguindo o guia.
- Qualquer dado específico do projeto original (IDs do Confluence, nomes de pessoas/sistemas, achados reais) — os scripts e guias foram genericizados, não apagados de função.

## Decisões de genericização a revisar

Ao extrair este scaffold, algumas escolhas de "o que generalizar vs. o que preservar" foram feitas por julgamento (não há uma única forma certa). Revise antes de versionar:
- `04-elicitacao/README.md`: a "Onda 0" foi generalizada para "gates de compliance/privacidade/segurança a abrir no dia 1" — no projeto original isso era processos regulatórios específicos de uma empresa em setor regulado. Pode não se aplicar a todo projeto; ajuste ou remova a onda 0 se seu domínio não tiver gates regulatórios cedo.
- `03-analise-critica/README.md`: a tabela "Status pós-reuniões" ficou como esqueleto vazio (2 linhas de exemplo) em vez de texto explicando o conceito — decisão de mostrar a forma, não só descrever.
- `.tools/check_links.py`: a lista `SKIP` e o conjunto `NOT_CONF` (exceções de ID) foram ajustados para os nomes de pasta deste scaffold e esvaziados, respectivamente — confira se ainda fazem sentido no seu vault.
- `.tools/spec-citacoes.md`: foi o mais reescrito dos scripts/guias copiados — o original era quase todo específico do projeto (nomes de arquivo, chave de Jira). Ficou só a estrutura de 7 regras + formato de relatório; preencha os exemplos com os do seu projeto.

## Checklist de replicação do Obsidian

Ver `docs/obsidian-config-replicar.md` para o passo a passo completo (tema, plugins, cores do grafo por fase, armadilhas já vividas — ex.: `textFadeMultiplier` do grafo precisa ficar em `0`).
