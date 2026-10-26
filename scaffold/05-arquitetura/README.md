---
tags: [fase/solucao, tipo/indice]
status: hipotese
aliases: ["Índice — Arquitetura"]
---

# 05 — Arquitetura

## Mapa de etapas

| Pasta | Etapa | Saída |
|---|---|---|
| `00-fontes/` | — | fonte da verdade |
| `01-contexto/` | 0 | o que já existe |
| `02-entendimento/` | 1 | o que o pedido diz |
| `03-analise-critica/` | 2 | veredito + condições por nível de GO |
| `04-elicitacao/` | 2→3 | perguntas, ondas, respostas |
| `05-arquitetura/` | 3 | arquitetura conceitual (hipótese) |
| `06-backlog/` | 4 | PB macro (FR/NFR) com estimativa |

**Etapa 3 — arquitetura conceitual.** Só abre com **GO-A ≥ condicionado** em `../03-analise-critica/README.md`. Nunca desenhe arquitetura sobre bloqueantes P0 ainda não resolvidos com artefato.

## BLUF

Abordagem escolhida: [preencher — nome da abordagem recomendada em `abordagens.md`, ou "ainda não escolhida"]. Condições de GO-A ou GO-C ainda abertas: [preencher — GO-A.n / GO-C.n, ou "nenhuma"].

**Regra de status:** todo arquivo desta pasta fica com `status: hipotese` enquanto houver condição de GO-A ou de GO-C aberta. Só vira `validado` quando quem tem mandato confirmar.

## Nível de detalhe

Conceitual: contexto e contêineres (C4 níveis 1 e 2) mais os fluxos principais. Sem topologia física e sem nomes de programa ou classe que não tenham fonte.

## O que esta pasta contém

Templates em `_templates/` (copie para esta pasta, sem o prefixo de template):

| Arquivo | Conteúdo |
|---|---|
| `abordagens.md` | 2 a 3 abordagens com trade-offs explícitos e **uma** recomendação justificada. Nunca uma única solução direta |
| `adr-NNN-<slug>.md` | ADR curta, uma por decisão que a recomendação assume |
| `diagramas.md` | Fonte do modelo dos diagramas e a marcação de evidência de cada elemento |

## Regras

- **Rastreabilidade:** cada decisão aponta para as G/C/R/Q que a motivam.
- **Evidência por elemento:** cada elemento do diagrama é marcado ✅ evidência / 🟡 inferência / ❓ a validar.
- **Diagramas:** use a skill `dd-arch-diagrams` (`.claude/skills/dd-arch-diagrams/`); esta pasta só aponta para a fonte do modelo.
- **Estimativa não é feita aqui.** Tamanho e horas ficam em `../06-backlog/`.
