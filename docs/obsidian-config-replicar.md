# Configuração do Obsidian — scaffold de vault de discovery

Resumo da configuração de `.obsidian/` deste scaffold, para replicar em um vault novo ou em outro dispositivo.

**Pré-requisito de sincronização:** se o seu vault vive dentro de uma pasta sincronizada (OneDrive, Dropbox, etc.), basta abrir o vault a partir dessa mesma pasta no novo dispositivo — não é necessário Obsidian Sync pago (o core plugin `sync: true` pode estar marcado só por padrão do Obsidian, não é o mecanismo usado).

---

## 1. Tema e aparência (`appearance.json`)

- Tema base: **Minimal** (community theme, não vem instalado por padrão — baixar em *Settings → Appearance → Themes*)
- `theme`: `system` (segue claro/escuro do SO)
- `baseFontSize`: 17
- CSS snippet ativo: `pastas` (ver seção 5)

## 2. Core plugins ligados (`core-plugins.json`)

Além dos defaults do Obsidian, confirme que estes estão **ativos**:
- File explorer, Search, Switcher, Graph, Backlink, Outgoing links, Tag pane, Properties, Page preview, Daily notes, Templates, Note composer, Command palette, Bookmarks, Outline, Word count, File recovery, Canvas, **Bases**

Desligados (defaults, não precisa tocar): Footnotes, Slash command, Markdown importer, ZK prefixer, Random note, Slides, Audio recorder, Workspaces, Publish, Webviewer.

## 3. Plugins de comunidade (`community-plugins.json`)

Instalar via *Settings → Community plugins → Browse*, nesta ordem não importa:

| Plugin | Versão testada | Função |
|---|---|---|
| **Minimal Theme Settings** | 9.0.0 | painel de controle do tema Minimal |
| **Style Settings** | 1.0.9 | expõe variáveis CSS de tema/snippets |
| **Iconize** (`obsidian-icon-folder`) | 2.14.7 | ícones custom em pastas/arquivos |
| **Lean Terminal** | 1.4.0 | terminal embutido (xterm.js/node-pty) |

Opcionais, dependendo do fluxo de IA que você usar neste vault (não incluídos no `community-plugins.json` deste scaffold por padrão — adicione se fizer sentido):
- **Claudian** — Claude Code embutido no vault
- **Copilot** — chat/agentes de IA no vault, com suas próprias credenciais de LLM por dispositivo

### 3.1 Minimal Theme Settings — config específica
Defaults do plugin, **exceto**:
- `fullWidthMedia`: true
- `bordersToggle`: true
- `minimalStatus`: true
- `underlineInternal` / `underlineExternal`: true
- `folding`: true
- `readableLineLength`: true
- `colorfulHeadings/Frame/ActiveStates`: false (mantidos off)

### 3.2 Style Settings — toggles do tema Minimal
- Row stripes (`row-alt`): on
- Row lines: on
- Column lines: on
- Table lines: on
- Column stripes (`col-alt`): off

### 3.3 Iconize — regras por pasta

Ícone + cor fixados por nome de pasta (recriar em *Iconize settings → Rules*):

| Pasta (regex) | Ícone (Lucide) | Cor |
|---|---|---|
| `00-fontes` | `LiArchive` | `#8a8a8a` |
| `01-contexto` | `LiLayers` | `#4a90d9` |
| `02-entendimento` | `LiBookOpen` | `#3fae6a` |
| `03-analise-critica` | `LiSearch` | `#e0a030` |
| `04-elicitacao` | `LiHelpCircle` | `#d9534f` |
| `.tools` | `LiWrench` | (sem cor) |
| `_WIP` | `LiClock` | `#6a6a6a` |

Demais configs do Iconize em default (emoji style: native, font size 16, ícones em notas e links ligados).

### 3.4 Lean Terminal
Sem customização — configuração default de instalação.

### 3.5 Se usar um plugin de IA (Copilot, Claudian, etc.)
Não salve chaves de API no vault — cada dispositivo configura suas próprias credenciais de LLM. Como ponto de partida, caso use o plugin Copilot: `contextTurns: 15`, `autoAddActiveContentToContext: true`, `enableInlineCitations: true` funcionaram bem neste tipo de vault.

## 4. Grafo — visual "galáxia" (`graph.json`)

Grupos de cor por tag (*Graph view → Groups*), com os hex usados:

| Tag | Hex | Cor |
|---|---|---|
| `tag:#fase/contexto` | `#3B82F6` | azul |
| `tag:#fase/entendimento` | `#22D3EE` | ciano |
| `tag:#fase/analise` | `#A78BFA` | violeta |
| `tag:#fase/elicitacao` | `#FBBF24` | âmbar |

Física "espalhada" (efeito galáxia): `nodeSizeMultiplier`: 1.4, `lineSizeMultiplier`: 0.5, `repelStrength`: 18, `linkDistance`: 320, `centerStrength`: 0.2, `linkStrength`: 1.

Outros: `showTags`: true, `showAttachments`: false, `showOrphans`: true, `showArrow`: false.

> ⚠️ **Armadilha conhecida:** `textFadeMultiplier` **precisa ficar em `0`**. Setá-lo para qualquer valor >0 (ex.: 1.6) esconde o nome dos nós conforme o zoom/distância. Se em algum device os nomes "desaparecerem" no grafo, é esse o parâmetro a checar primeiro.
>
> ⚠️ O painel de filtros do Graph view tem um botão de reset que **zera `colorGroups` e a física**. Evite clicar em "restore defaults" ali sem necessidade.

### 4.1 Local Graph (painel fixado na sidebar) — configuração separada

**Importante:** o Local Graph guarda suas opções **independentemente** do grafo principal, num bloco próprio dentro de `.obsidian/workspace.json` (dentro do leaf `"type": "localgraph"`), não em `graph.json`. Copiar `graph.json` não é suficiente para replicar uma visão fixada na sidebar — as mesmas cores/física precisam ser reaplicadas manualmente lá também, se você usar esse painel:
1. `Ctrl+P → "Graph view: Open local graph"` e arrastar para a sidebar.
2. Abrir o painel de filtros do Local Graph e aplicar manualmente os mesmos grupos de cor + física da seção 4.

## 4.2 Pré-requisito das cores por fase: convenção de tags

As cores do grafo (seção 4) só funcionam porque as tags de fase seguem um padrão único no vault:

- Uma única fonte por nota: array `tags:` no frontmatter. **Não** usar campos soltos `fase:`/`area:`/`tipo:` em paralelo — causam inconsistência.
- Sem prefixo numérico: `fase/contexto`, `fase/entendimento`, `fase/analise`, `fase/elicitacao` — não `fase/0-contexto`, `fase/1-entendimento` etc.
- Trade-off aceito: o painel de tags do Obsidian ordena alfabeticamente (`analise, contexto, elicitacao, entendimento` — não é a ordem real do processo). Documente esse aviso no `README.md` da raiz (ver seção "Ordem das fases" nos templates deste scaffold).

## 5. CSS Snippet (`snippets/pastas.css`)

Ativar em *Settings → Appearance → CSS snippets*. Colore o nome das pastas no file explorer — já incluído em `.obsidian/snippets/pastas.css` deste scaffold.

## 6. Layout de sidebars (`workspace.json`)

Sugestão de ponto de partida (não incluído neste scaffold — `workspace.json` é estado de sessão, não config reutilizável):

**Sidebar esquerda** (abas): File explorer → Search → Bookmarks

**Sidebar direita** (abas): Backlinks → Outgoing links → Tags → All properties → (chat de IA, se usar)

**Área principal**: split vertical com 2 abas markdown lado a lado funciona bem para comparar fonte × análise.

## 7. O que normalmente não precisa customização

- `app.json`: pode ficar vazio — sem vim mode, sem hotkeys customizados.
- Nenhum icon pack extra é necessário — ícones nativos Lucide bastam via Iconize.

---

## Checklist de replicação rápida

1. Abrir o vault a partir da pasta sincronizada (se aplicável) no novo dispositivo.
2. Instalar tema **Minimal**.
3. Instalar os plugins de comunidade da seção 3 e ativá-los.
4. Ativar o CSS snippet `pastas`.
5. Recriar as regras de ícone/cor do Iconize (seção 3.3).
6. Recriar os grupos de cor por tag no Graph view, com física espalhada e `textFadeMultiplier: 0` (seção 4).
7. Confirmar que as notas usam a convenção de tags sem prefixo numérico (seção 4.2) — sem isso, as cores do grafo não pegam.
8. Configurar credenciais de LLM no plugin de IA escolhido, se for usá-lo.
9. (Opcional) Reabrir o Local Graph, fixar na sidebar e reaplicar manualmente as mesmas cores/física (seção 4.1) — não é herdado do `graph.json`.
