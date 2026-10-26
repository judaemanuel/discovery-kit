---
tags: [fase/analise, tipo/analise, tipo/indice]
status: hipotese
aliases: ["Índice — Análise Crítica"]
---

# 03 — Análise crítica

**Etapa:** 2 | **Insumos:** `02-entendimento/*`, `01-contexto/*`, extrações brutas de `00-fontes/*`.

## BLUF

**Recomendação: [preencher — GO / NO-GO / GO condicional] para a Etapa 3 (arquitetura).** [preencher: 1 parágrafo explicando por quê, citando os principais itens que travam a decisão]

**Condições para GO:** [preencher — numere as condições críticas, ex.: (1) modelo canônico de X; (2) sponsor e KPI formal; (3) processo as-is de Y confirmado com artefato; (4) ...]. Mantenha esta lista **explícita e numerada** — é o critério objetivo que evita um veredito "sentido", e permite rastrear status condição-por-condição depois de cada reunião.

**Status pós-reuniões (atualize esta tabela a cada rodada de reuniões, não crie documento novo):**

| Condição | Status |
|---|---|
| (1) [preencher] | ❌ / 🟡 Parcial / ✅ |
| (2) [preencher] | ❌ / 🟡 Parcial / ✅ |

## Condições do veredito após [data da rodada]

[preencher quando houver reunião ou mudança de fonte: o veredito acima **não é alterado aqui** — esta seção lista o que mudou para a decisão do usuário sobre reavaliá-lo (regra 6: o veredito só muda com artefato).]

| Mudança | Efeito nas condições |
|---|---|
| [preencher: o que mudou, com fonte] | [preencher: condição (n) sai de ❌ para 🟡; G/C/R afetados] |

Ainda abertas para o GO: [preencher]. **Decisão do usuário:** [preencher — manter o veredito ou reavaliar, e com qual artefato].

## Top-N achados (priorizados)

[preencher: 1 linha por achado, do mais crítico ao menos crítico, com refs aos IDs correspondentes (G/C/H/R/D). Mantenha o selo ✅ evidência / 🟡 inferência / ❓ a validar em cada achado.]

| # | Achado | Status | Refs |
|---|---|---|---|
| 1 | [preencher] | ✅/🟡/❓ | G-xxx, C-xx |

## Contagens

| Artefato | Total | Críticos |
|---|---|---|
| Lacunas (G) | [preencher] | [preencher] bloqueantes |
| Contradições (C) | [preencher] | [preencher] graves |
| Riscos (R) | [preencher] | [preencher] com probabilidade e impacto altos |
| Dependências (D) | [preencher] | [preencher] pré-arquitetura |
| Hipóteses (H) | [preencher] | [preencher] confirmadas |

## Arquivos

- `lacunas-ambiguidades.md`: G-001..
- `contradicoes.md`: C-01..
- `riscos.md`: R-001..
- `dependencias.md`: D-001..
- `hipoteses-vs-evidencias.md`: H-001..
- Visão de ponta a ponta: `../02-entendimento/visao-consolidada.md`
- Elicitação: `../04-elicitacao/`

## Limitações desta análise

[preencher: o que esta análise NÃO cobre ainda — ex.: nenhuma entrevista realizada, cobertura parcial de alguma fonte, dado sensível não aberto]

## Notas relacionadas

- [[lacunas-ambiguidades|Lacunas e ambiguidades]]
- [[contradicoes|Contradições]]
- [[riscos|Riscos]]
- [[dependencias|Dependências]]
- [[hipoteses-vs-evidencias|Hipóteses × evidências]]
- [[../02-entendimento/visao-consolidada|Visão consolidada]]
- [[../04-elicitacao/pauta-entrevistas|Pauta de entrevistas]]
