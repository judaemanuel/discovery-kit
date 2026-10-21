# Spec — padronização de citações (template)

Objetivo: toda citação vira link navegável até o trecho exato. **Mude só citações** — nunca o texto, a análise, os status (✅/🟡/❓) ou os IDs (G-/C-/H-/Q-/R-/D-). Não edite `00-fontes/` nem `.tools/`. Atualize `atualizado:` do frontmatter nos arquivos alterados.

## Insumos (ajuste para o seu projeto)

- Documentos de entrada extraídos para Markdown (via `docx2md.py`), com numeração reconstruída e block IDs automáticos: `^intro-N`, `^rn-N`, `^rf-2-2-1`, `^rnf-N` (os nomes das seções/prefixos dependem do padrão numeração do seu documento de entrada — ajuste `SECTION_IDS` em `docx2md.py` se o seu documento usar outros nomes de seção).
- Fonte de conhecimento corporativo (wiki, Confluence, etc.): mapa ID → título/URL, se sua integração de busca retornar IDs numéricos em vez de links diretos.
- Tracker de tickets (Jira ou equivalente): URL base para montar o link a partir da chave do ticket.

## Regras

1. **Documento de entrada → wikilink para o block ID** (ou para o título da seção quando o trecho não é item numerado):
   - `[[documento#^rf-2-2-1|Doc RF 2.2.1]]`, `[[documento#2. Regras de Negócio|Doc §2 Regras de Negócio]]`.
   - **Resolva pelo conteúdo, não por um número de seção que você já tinha em mente.** Numeração manual feita antes da extração real frequentemente diverge do documento original. Abra o documento extraído, ache o trecho que sustenta a afirmação e use o block ID + rótulo com a numeração real.
   - IDs próprios do seu discovery (ex.: `Q-nnn`, `G-nnn`) são seus: mantenha-os como estão; converta só a citação de fonte ao lado.
   - Capa/cabeçalho/seções sem numeração → `[[documento|Doc capa]]`.
   - Imagens (`media/imageN.png`) → `[[documento/media/imageN.png|imageN]]` junto do link do item.
2. **Fonte externa (wiki corporativa, etc.) → nota de rodapé** `[^n]`. No corpo: o texto continua, o marcador vai logo após a menção. Remova IDs numéricos soltos, substituindo pelo marcador. Links inline no corpo também viram `Título[^n]`.
   - Definições no FIM do arquivo (depois de "Notas relacionadas"), numeradas na ordem da 1ª aparição, reusando o número para a mesma página: `[^3]: [Título](url) — Fonte, Espaço`.
   - **Exceção comum:** listas "Fontes" no topo das notas de contexto podem manter `[Título](url)` inline, sem rodapé, se esse for o padrão que você adotar.
3. **Tracker de tickets** → mesmo padrão de rodapé: `CHAVE-123[^5]` / `[^5]: [CHAVE-123](url) — Jira` (ou o tracker que usar).
4. **Referências internas → wikilink:** qualquer notação provisória usada durante a elicitação (ex.: `[WIKI:arquivo.md]`, `[ANX Anexo A]`, `[Reunião AAAA-MM-DD]`) deve, na padronização final, virar `[[arquivo]]` / `[[anexo#título real]]` / `[[reuniao-x|Reunião AAAA-MM-DD]]` — resolva pelo conteúdo real do arquivo, não pelo rótulo provisório.
5. **Tabelas Markdown:** dentro de célula, o `|` do alias quebra a tabela — use `\|`. Rodapés `[^n]` em células funcionam normalmente.
6. **IDs que não são da fonte de conhecimento corporativo — não mexer:** documente aqui, conforme forem aparecendo, números que parecem ID de página mas são de outro domínio (nº de apólice, nº de build, SKU, etc.) para não tentar resolvê-los como citação.
7. Títulos de âncora: copie exatamente o texto do heading de destino (sem `#`). Verifique que existe.

## Relatório final (curto)

Por arquivo: nº de citações convertidas por tipo; lista de pendências (citação que não conseguiu resolver, com linha e motivo). Nada de dump do conteúdo.
