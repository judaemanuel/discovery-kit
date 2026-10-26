---
tags: [fase/plano, area/preencher, tipo/estimativa]
status: hipotese
atualizado: 2026-01-01
---

# Calibração da estimativa

> **Estimativa de discovery, uso interno para planejamento de capacidade; não é compromisso nem preço.**

**Quem calibra:** o arquiteto que conduz o discovery. Nenhum valor abaixo vem do kit: tudo é `[preencher]` por projeto, e a **origem de cada faixa** é sempre registrada ao lado dela.

## Origens aceitas (da mais forte para a mais fraca)

| Origem | O que exige |
|---|---|
| Histórico | Dados de entregas anteriores em `../00-fontes/historico/`, extração literal, citados por arquivo. Sem histórico para o contexto, a origem **não** pode ser declarada como histórico |
| Experiência | Analogia com times e desafios equivalentes. Registre qual analogia e quando ocorreu (ex.: tipo de projeto, tamanho do time) |
| Assistida por IA | A IA propõe a faixa a partir do PB macro, das lacunas e das âncoras. **O arquiteto revisa e assina**; registre o método ou prompt, a data e o que o arquiteto alterou |

Estimativa só de IA, sem revisão do arquiteto registrada, **não é aceita**.

## Faixas por tamanho

Âncora: [preencher — ver `pb-macro.md`].

| Tamanho | Mín | Provável | Máx | Origem | Fonte ou analogia |
|---|---|---|---|---|---|
| S | [preencher] | [preencher] | [preencher] | [preencher: histórico / experiência / IA] | [preencher: arquivo de `historico/`, analogia ou descrição do método] |
| M | [preencher] | [preencher] | [preencher] | [preencher] | [preencher] |
| L | [preencher] | [preencher] | [preencher] | [preencher] | [preencher] |
| XL | [preencher] | [preencher] | [preencher] | [preencher] | [preencher] |

Valores em horas. O item de `pb-macro.md` herda a origem **mais fraca** usada nele.

## Limite de confiança sem histórico

Origem "IA" ou "experiência" **sem histórico** limita a confiança máxima do item a **Média** até a primeira medição real (por exemplo, depois do refinamento ou da primeira entrega). Só a medição real, registrada aqui, remove o limite.

## Revisão do arquiteto (obrigatória para origem IA)

| Faixa (tamanho) | Método ou prompt | Data | O que o arquiteto alterou | Assinado por |
|---|---|---|---|---|
| [preencher] | [preencher] | [preencher: YYYY-MM-DD] | [preencher] | [preencher] |

## Confiança e multiplicadores

A confiança do item vem das lacunas abertas que o afetam. A faixa alarga com a confiança, por multiplicador por classe. **Valores a calibrar** com dados reais; o kit não fornece números.

| Confiança | Regra inicial | Multiplicador sobre a faixa |
|---|---|---|
| Alta | sem lacuna aberta | [preencher] |
| Média | 1 a 2 lacunas não bloqueantes | [preencher] |
| Baixa | qualquer lacuna bloqueante, ou tamanho depende de algo ainda não lido | [preencher] |

## Medições reais

| Data | Item | Estimado (provável) | Realizado | Efeito na calibração |
|---|---|---|---|---|
| [preencher] | RF-001 | [preencher] | [preencher] | [preencher] |
