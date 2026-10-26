---
tags: [tipo/indice]
status: validado
aliases: ["Índice — Discovery Kit"]
---

# Discovery Kit

## BLUF

Um esqueleto de vault Obsidian + Claude Code para condução de **discovery técnico/negócio** (levantamento de requisitos, análise crítica de especificações, elicitação de stakeholders, veredito GO/NO-GO para arquitetura), com:
- Estrutura de pastas por etapa (fonte → contexto → entendimento → análise → elicitação → arquitetura → backlog)
- Convenções de frontmatter, nomenclatura e IDs (`Q-nnn`, `G-nnn`, `C-nn`, `H-nnn`, `R-nnn`, `D-nnn`)
- Um **loop de processo explícito** entre análise crítica e elicitação (ver `.discovery/guias/GUIA-FLUXO-DISCOVERY.md`) — a lição mais cara do projeto original foi não ter esse loop fechado em tempo real
- `CLAUDE.md` + hook `SessionStart` que injeta os guias de processo automaticamente em toda sessão Claude Code
- Configuração do Obsidian (tema, plugins, grafo colorido por fase) documentada para replicação manual

## Como usar

1. **Esta pasta é uma instância** criada pelo `install.sh` do gerador (versão em `.discovery-kit-version.json`).
2. **Abra como vault no Obsidian** a partir dessa pasta. Siga `.discovery/guias/obsidian-config-replicar.md` para instalar tema/plugins/grafo (plugins e tema não são vendorizados: instale pelo *Community plugins*).
3. **Abra o Claude Code** com essa pasta como diretório de trabalho — `CLAUDE.md` e o hook `SessionStart` carregam automaticamente; não precisa fazer nada manual.
4. **Popule `00-fontes/`** com os documentos originais do seu discovery (specs, EDS, PRDs, etc.).
5. **Leia `.discovery/guias/GUIA-FLUXO-DISCOVERY.md`** antes de começar — explica o loop `03-analise-critica/` ↔ `04-elicitacao/` ↔ reunião real, que é o motivo deste scaffold existir.
6. **Preencha os `README.md` de `03-analise-critica/` e `04-elicitacao/`** primeiro — eles têm os `[preencher]` que forçam você a declarar as condições de GO/NO-GO e as ondas de entrevista antes de começar a trabalhar, não depois.
7. Antes do primeiro uso real, rode `python3 .discovery/tools/check_links.py .` para validar os wikilinks. **Esperado hoje (scaffold vazio): ~19 avisos** — a maioria é link para arquivo que você ainda vai criar (`stakeholders.md`, `contradicoes.md`, etc. — fazem parte do conteúdo do discovery, não do scaffold) ou falso-positivo do próprio script com `README.md` duplicado por pasta e `\|` escapado em célula de tabela. Rode de novo depois de criar o conteúdo real — aí os avisos restantes são genuínos.

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
| `.discovery/` | — | Guias de processo (`guias/`) e scripts de apoio (`tools/`: extração docx, inspeção xlsx, checagem de links) |

## Checklist de replicação do Obsidian

Ver `.discovery/guias/obsidian-config-replicar.md` para o passo a passo completo (tema, plugins, cores do grafo por fase, armadilhas já vividas — ex.: `textFadeMultiplier` do grafo precisa ficar em `0`).
