# Guia de Frontmatter — Discovery Kit

**Como usar este guia:** no início de cada discovery novo, ajuste a seção `area/*` para os domínios reais do projeto. O resto do schema (tags, status, atualizado) é estável entre projetos.

## BLUF

Todo arquivo de conteúdo (fora de `_WIP/`, `_temp/`, `.tools/`) deve abrir com:

```yaml
---
tags: [fase/<fase>, area/<area>, tipo/<tipo>]
status: <status>
atualizado: YYYY-MM-DD
---
```

`aliases` é opcional, só para índices (`README.md` de cada pasta). `area/*` pode repetir (0 a N valores); `fase/*` e `tipo/<categoria-principal>` costumam ser únicos.

## Campo `tags`

Três namespaces, sempre `namespace/valor`, sem numeração — a ordem de trabalho real está no `README.md` raiz (seção "Estrutura"), não no nome da tag:

### `fase/*` — em que etapa do discovery o conteúdo foi produzido

| Tag | Pasta correspondente | Significado |
|---|---|---|
| `fase/contexto` | `01-contexto/` | Wiki/base de conhecimento extraída (sistemas, termos, processos já existentes) |
| `fase/entendimento` | `00-fontes/`, `02-entendimento/` | Leitura/resumo dos documentos de entrada originais |
| `fase/analise` | `03-analise-critica/` | Lacunas, contradições, hipóteses × evidências, riscos |
| `fase/elicitacao` | `04-elicitacao/`, reuniões em `00-fontes/reunioes/` | Perguntas, pautas, stakeholders, extrações de reunião |
| `fase/solucao` | `05-arquitetura/` (futuro) | Ainda não usado até o veredito GO |
| `fase/plano` | `06-backlog/` (futuro) | Ainda não usado |

**Nuance:** a tag reflete a *natureza da atividade que gerou o conteúdo*, não necessariamente a pasta física do arquivo (ex.: uma análise de reunião de kickoff pode levar `fase/elicitacao` mesmo estando guardada em `02-entendimento/`, se o conteúdo é elicitação).

### `area/*` — qual domínio de negócio/sistema o conteúdo toca (pode ter várias)

`area/*` é **livre por projeto** — defina os domínios de negócio/sistema relevantes ao abrir o discovery, e documente a lista aqui assim que decidir (ex., no projeto original que gerou este kit: `area/regras-negocio`, `area/app-cliente`, `area/integracoes`, `area/governanca`, `area/seguranca`).

Sem área definida = só `tipo/indice` ou `tipo/glossario` (documentos estruturais, não substantivos).

### `tipo/*` — natureza do documento (define o quanto "editar" ou "confiar")

| Tag | Significado | Onde aparece |
|---|---|---|
| `tipo/fonte-bruta` | Extração quase literal de gravação/transcrição — **não editar o conteúdo**, só a frontmatter | `00-fontes/reunioes/` |
| `tipo/reuniao` | Documento originado de uma reunião (bruto ou analisado) | `00-fontes/reunioes/`, `02-entendimento/` |
| `tipo/entrada` | Insumo original (e-mail, transcrição, documento) ou seu resumo/estrutura, ainda sem análise crítica | `00-fontes/`, `02-entendimento/` |
| `tipo/anexo-calculo` | Anexo técnico de cálculo dentro de um documento de entrada | `00-fontes/` |
| `tipo/wiki` | Página de conhecimento de contexto | `01-contexto/` |
| `tipo/glossario` | Glossário de termos | `01-contexto/glossario.md` |
| `tipo/inventario` | Catálogo/listagem (ex.: inventário de fontes) | `01-contexto/` |
| `tipo/analise` | Lacunas, contradições, dependências, riscos, hipóteses | `03-analise-critica/` |
| `tipo/duvidas-tecnicas` | Dúvidas técnicas específicas de arquitetura | `03-analise-critica/` |
| `tipo/elicitacao` | Perguntas por área, pauta de entrevistas, stakeholders | `04-elicitacao/` |
| `tipo/indice` | README/índice de uma pasta | qualquer `README.md` interno |

**Regra prática:** fontes brutas de reunião levam `tipo/reuniao` **+** `tipo/fonte-bruta` junto. Uma análise *derivada* de uma reunião leva só `tipo/reuniao`, sem `fonte-bruta`, porque já é interpretação (com marcação de confiança ✅/🟡/❓), não transcrição.

## Campo `status`

| Valor | Significado | Quando usar |
|---|---|---|
| `rascunho` | Conteúdo bruto ou estrutura inicial, ainda não interpretado/analisado | `tipo/fonte-bruta`; documentos de entrada originais; documentos de `04-elicitacao/` ainda sendo preenchidos |
| `hipotese` | Conteúdo interpretado/estruturado por nós, mas **não validado pelos stakeholders reais** | a maioria dos documentos analíticos (`fase/contexto`, `fase/entendimento`, `fase/analise`) |
| `validado` | Confirmado por quem decide, ou documento estrutural estável (índice, glossário) | `README.md`, guias de leitura, índices de pasta |
| `em-aberto` | Documento é um backlog vivo de itens pendentes — o status reflete o conteúdo (tem itens abertos), não a maturidade do texto | catálogos de dúvidas técnicas |

**Alerta adversarial:** `hipotese` tende a ser o valor default de fato — é fácil usá-lo sem pensar. Antes de marcar algo como `validado`, pergunte: *alguém com mandato confirmou isso, ou só parece estável porque ninguém contestou?*

## Campo `atualizado`

Data (`YYYY-MM-DD`) da última edição substantiva do **conteúdo** do arquivo — não é a data da reunião/fonte quando o arquivo é uma análise derivada. Para `tipo/fonte-bruta`, geralmente coincide com a data de extração.

## Campo `aliases` (opcional)

Só em `README.md` de pasta: `aliases: ["Índice — <Nome da Pasta>"]`. Facilita busca/backlink no Obsidian pelo nome amigável em vez do literal `README`.

## Checklist para aplicar frontmatter a um arquivo

1. Em que pasta ele está → já sugere `fase/*` candidato (ver tabela), mas confirme pelo *conteúdo*, não só pela pasta.
2. Qual(is) domínio(s) de negócio/sistema ele toca → `area/*` (pode ser 0, 1 ou várias — ver seção `area/*` acima).
3. É transcrição quase literal de reunião/gravação? → `tipo/fonte-bruta` + `tipo/reuniao`, `status: rascunho`.
   É análise derivada (com interpretação, confiança, BLUF)? → `tipo/reuniao` só, `status: hipotese` (ou outro `tipo/*` da tabela, conforme o conteúdo).
4. Alguém com mandato de decisão já validou o conteúdo? Não → `hipotese`. Documento é bruto/incompleto? → `rascunho`. É backlog de itens abertos? → `em-aberto`. Só então → `validado`.
5. `atualizado` = data de hoje (ou da última edição real, se retroativa).
6. Índice de pasta (`README.md`)? Adicione `aliases`.
