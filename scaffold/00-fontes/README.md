---
tags: [tipo/indice]
status: validado
aliases: ["Índice — Fontes"]
---

# 00 — Fontes

Documentos originais e extrações literais. **Fonte da verdade — nunca editar o conteúdo, só a frontmatter.**

Subpastas sugeridas (renomeie livremente):
- `entrada/` (ou o nome que os insumos tiverem no seu projeto — e-mail, contrato, RFP, EDS, PRD, briefing...)
- `reunioes/` — extrações de gravação/transcrição, com `tipo/fonte-bruta` no frontmatter.
- `historico/` — dados de entregas anteriores para calibrar a estimativa (ver `historico/README.md`); opcional.

## Convenção de citação

- Documento de entrada → wikilink para o block ID do item na extração.
- Fonte externa (wiki corporativa, ticket, etc.) → nota de rodapé `[^n]`, com `[^n]: [Título](url) — Fonte, Espaço` no fim do arquivo.
- Notas do vault → `[[nota#seção|rótulo]]`.
