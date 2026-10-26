---
tags: [fase/analise, tipo/analise, tipo/indice]
status: hipotese
aliases: ["Índice — Análise Crítica"]
---

# 03 — Análise crítica

**Etapa:** 2 | **Insumos:** `02-entendimento/*`, `01-contexto/*`, extrações brutas de `00-fontes/*`.

## BLUF

O veredito tem **três níveis**. Cada nível é `NO-GO`, `GO condicionado` ou `GO`, com condições numeradas, status por condição e artefato que sustenta (regra 6 do `CLAUDE.md`). Condições de `GO condicionado` são rastreadas a G/Q/C/R.

**Regra:** um nível posterior não pode ser mais positivo que o anterior (GO-B não pode ser mais positivo que GO-A; GO-C não pode ser mais positivo que GO-B). Ordem: `NO-GO` < `GO condicionado` < `GO`.

Mantenha as linhas `**GO-A:**`, `**GO-B:**` e `**GO-C:**` no formato abaixo: o `check_fluxo.py` as lê.

### GO-A — arquitetura conceitual

**Pergunta:** sabemos o suficiente para desenhar uma arquitetura conceitual? **Libera:** abrir `../05-arquitetura/` em modo conceitual (só abre com GO-A ≥ condicionado).

**GO-A:** [preencher — NO-GO / GO condicionado / GO]

[preencher: 1 parágrafo explicando por quê, citando os itens que travam a decisão]

**Condições para GO-A:** [preencher — numere como GO-A.1, GO-A.2..., cada uma rastreada a G/Q/C/R. Lista **explícita e numerada**: é o critério objetivo que evita um veredito "sentido".]

| Condição | Rastreio | Status |
|---|---|---|
| GO-A.1 [preencher] | G-nnn, Q-nnn | ❌ / 🟡 Parcial / ✅ |
| GO-A.2 [preencher] | G-nnn | ❌ / 🟡 Parcial / ✅ |

### GO-B — estimativa em faixa

**Pergunta:** sabemos o suficiente para estimar em faixa? **Libera:** preencher tamanho e horas em `../06-backlog/` (sem GO-B ≥ condicionado, o PB macro existe sem tamanho/horas).

**GO-B:** [preencher — NO-GO / GO condicionado / GO]

[preencher: 1 parágrafo explicando por quê]

**Condições para GO-B:** [preencher — GO-B.1, GO-B.2...]

| Condição | Rastreio | Status |
|---|---|---|
| GO-B.1 [preencher] | G-nnn, Q-nnn | ❌ / 🟡 Parcial / ✅ |

### GO-C — detalhar e construir

**Pergunta:** sabemos o suficiente para detalhar e construir? **Libera:** handoff para fora do kit (fora de escopo).

**GO-C:** [preencher — NO-GO / GO condicionado / GO]

[preencher: 1 parágrafo explicando por quê]

**Condições para GO-C:** [preencher — GO-C.1, GO-C.2...]

| Condição | Rastreio | Status |
|---|---|---|
| GO-C.1 [preencher] | G-nnn, Q-nnn | ❌ / 🟡 Parcial / ✅ |

**Status pós-reuniões:** atualize as tabelas de condição acima a cada rodada de reuniões; não crie documento novo.

## Condições do veredito após [data da rodada]

[preencher quando houver reunião ou mudança de fonte: os vereditos acima **não são alterados aqui** — esta seção lista o que mudou para a decisão do usuário sobre reavaliá-lo (regra 6: o veredito só muda com artefato).]

| Mudança | Efeito nas condições |
|---|---|
| [preencher: o que mudou, com fonte] | [preencher: condição GO-x.n sai de ❌ para 🟡; G/C/R afetados] |

Ainda abertas, por nível: [preencher]. **Decisão do usuário:** [preencher — manter os vereditos ou reavaliar algum nível, e com qual artefato].

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
