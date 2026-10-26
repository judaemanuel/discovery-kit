---
tags: [fase/plano, tipo/indice]
status: hipotese
aliases: ["Índice — Backlog"]
---

# 06 — Backlog

> **Estimativa de discovery, uso interno para planejamento de capacidade; não é compromisso nem preço.**

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

**Etapa 4 — PB macro (FR/NFR) com estimativa.** O backlog existe a partir de `../05-arquitetura/` com abordagem escolhida. Tamanho e horas só entram com **GO-B ≥ condicionado** em `../03-analise-critica/README.md`; antes disso o PB macro existe **sem** tamanho/horas. Item = requisito macro (nível de épico), não história: sem histórias nem critérios de aceite por história.

## BLUF

PB macro: [preencher — N requisitos funcionais, M não funcionais, K com status `lacuna`]. Estimativa: [preencher — sem GO-B / vigente / invalidada]; total provável [preencher] h, teto pessimista [preencher] h.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `pb-macro.md` | Requisitos FR/NFR, âncora, estimativa por item e totais |
| `calibracao.md` | Tabela de calibração por tamanho, com a **origem de cada faixa**, e multiplicadores de confiança |
| `estimativa-status.md` | Versão, premissas, gatilhos de invalidação e status da estimativa |

## Regras

1. **Tamanho primeiro** (S / M / L / XL), em relação a uma âncora declarada em `pb-macro.md`. Sem âncora: só tamanho relativo, sem horas.
2. **Horas só como faixa** `mín – provável – máx`, nunca número único, derivada de `calibracao.md`.
3. **NFR sem fonte não é omitido.** Entra como `RNF-nnn` com status `lacuna`, apontando para a G-nnn correspondente.
4. **Totais:** soma dos "provável" como valor central; soma dos "máx" como teto pessimista, rotulado como tal. Não somar tamanhos.
5. **Publicação:** a estimativa não sai do kit para terceiros sem decisão explícita do dono do discovery.
6. **Story points** ficam fora do núcleo: coluna opcional, só se existir time e velocidade.

## Gatilhos de invalidação (mínimos)

Se qualquer um ocorrer, a estimativa vira `invalidada`, deve ser **recalculada** e, se houver compromisso externo, **repactuada**. Cada projeto acrescenta os seus em `estimativa-status.md`.

1. Complexidade acima da suposta.
2. Mistura de responsabilidades que o desenho separou.
3. Ausência de uma etapa de refinamento ou de leitura de fonte que a estimativa pressupõe.
4. Quebra de qualquer premissa listada.
5. Mudança de escopo.
