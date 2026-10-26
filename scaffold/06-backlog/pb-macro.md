---
tags: [fase/plano, area/preencher, tipo/backlog]
status: hipotese
atualizado: 2026-01-01
---

# PB macro

> **Estimativa de discovery, uso interno para planejamento de capacidade; não é compromisso nem preço.**

**Template:** ajuste `area/preencher` e `atualizado`. Sem GO-B ≥ condicionado, preencha só a tabela "Requisitos" e deixe a tabela "Estimativa" vazia.

## Âncora

Item conhecido ou histórico usado como referência de tamanho: [preencher — item ou arquivo de `../00-fontes/historico/`]. Fonte: [preencher]. **Sem âncora, só tamanho relativo, sem horas.**

## Requisitos

| ID | Tipo | Descrição | Origem | Abordagem | Status |
|---|---|---|---|---|---|
| RF-001 | FR | [preencher: uma frase testável] | [preencher: arquivo de `00-fontes` ou Q-nnn / G-nnn] | [preencher: `adr-NNN-slug.md` em `05-arquitetura`] | ativo |
| RNF-001 | NFR ([preencher: segurança, desempenho, disponibilidade, compatibilidade, operação, rastreabilidade...]) | [preencher: sem fonte para este requisito] | G-nnn | [preencher] | lacuna |

Um NFR sem fonte **não é omitido**: entra como `RNF-nnn` com status `lacuna` e aponta para a G-nnn correspondente. Status válidos: `ativo`, `lacuna`, `descartado`.

## Estimativa (com GO-B ≥ condicionado)

| ID | Tamanho | Faixa de horas (mín – provável – máx) | Origem da faixa | Confiança | Lacunas herdadas | Bloqueante? | Premissas | Pontos (opcional) |
|---|---|---|---|---|---|---|---|---|
| RF-001 | [preencher: S / M / L / XL] | [preencher] – [preencher] – [preencher] | [preencher: histórico / experiência / IA] | [preencher: Alta / Média / Baixa] | G-nnn, Q-nnn | [preencher: sim / não] | [preencher: premissas de cenário ideal] | [preencher, só se houver time e velocidade] |

- **Origem da faixa:** cada item herda a origem **mais fraca** usada nele. Origem "IA" ou "experiência" sem histórico limita a confiança máxima a **Média** (ver `calibracao.md`).
- **Confiança:** regra e multiplicadores em `calibracao.md`.

## Totais

| Total | Valor | Leitura |
|---|---|---|
| Provável (soma dos "provável") | [preencher] h | valor central |
| Máximo (soma dos "máx") | [preencher] h | **teto pessimista**: máximos raramente coincidem |

Não some tamanhos.
