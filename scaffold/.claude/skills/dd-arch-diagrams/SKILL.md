---
name: dd-arch-diagrams
description: Gera diagramas de arquitetura C4 conceituais a partir de UM modelo em Python (model.py + views.py), em 3 formatos consistentes entre si - Structurizr DSL, draw.io (uma página por vista) e um HTML autocontido com abas (C1, C2, C3, fluxos de sequência, decisões/ADR, slide executivo 16:9), inspetor de blocos e download de SVG. Use quando o usuário pedir desenho/diagrama de arquitetura (C4), arquitetura conceitual, caminho provável de solução, ADRs visuais, slide de arquitetura para sponsors, ou para reproduzir/atualizar diagramas já gerados por esta skill. Não use para diagramas de código real (UML de classes), fluxogramas de negócio livres ou diagramas que precisem de autolayout.
---

# dd-arch-diagrams — diagramas C4 conceituais reproduzíveis

## BLUF

Você descreve a arquitetura **uma vez** (entidades, relações, decisões, fluxos, coordenadas) e o motor em `scripts/` gera os três formatos, sempre iguais entre si e **byte a byte reproduzíveis** (mesma entrada → mesmo hash). O layout é **manual** (coordenadas escritas à mão em `views.py`), porque é isso que dá o resultado legível; a skill ensina a calcular e a conferir.

Para quem é: Discovery / pré-venda técnica — material para discutir o *provável caminho de solução*, não arquitetura validada.

## Quando usar / quando não usar

| Use | Não use |
|---|---|
| Desenho conceitual C4 (C1 contexto, C2 contêineres, C3 componentes) com status novo / reuso / existente | Diagrama do código ou do banco real |
| Fluxos de sequência de sagas/eventos, tabela de decisões (ADR) com estado (aberto, tendência, proposta nossa) | Fluxo de processo de negócio (BPMN) |
| Slide único para sponsors com "o que já sabemos × o que o Discovery decide" | Diagrama que precise de autolayout (muitas dezenas de nós) |
| Reproduzir ou atualizar um conjunto já gerado | Arquitetura **validada** — esta skill rotula tudo como hipótese por padrão |

## Premissas e entradas (confirme com o usuário antes de gerar)

Antes de escrever o modelo, liste em tabela cada entrada com a coluna **origem** (`lido de arquivo` × `assumido`). Não preencha o modelo com suposições silenciosas.

| Entrada | Como obter |
|---|---|
| Sistemas, pessoas e papéis | Ler as fontes do vault (`00-fontes`, `01-contexto`, `03-analise-critica`); perguntar o que faltar |
| O que existe × o que é novo × o que é reuso | Só marcar `existente` / `reuso` com evidência citada; sem evidência, é `novo` ou "a validar" |
| Decisões (ADR) e pontos em aberto | De `03-analise-critica`/`04-elicitacao` (G-, D-, Q-, R-) — referencie os IDs em `ADR.depende` e `open` |
| Fluxos relevantes (2–4) | Escolha os que mostram dinheiro, compensação ou integração com legado |
| Slide para sponsors? (4 decisões + quem decide) | Perguntar; tem implicação de tom (expõe lacunas do cliente) |
| Data, autoria, rótulos (`META`) | Do usuário |

## Fluxo de trabalho

1. **Ler** `references/como-editar-o-modelo.md` e `references/layout.md` (uma vez por sessão).
2. **Partir de um molde.** `templates/exemplo/` (completo: C1, C2, 2×C3, 3 fluxos, slide) ou `templates/esqueleto/` (C1 + C2). Copie a pasta para `_WIP/<data>/arquitetura-vN-src/` (o projeto-fonte) e edite `model.py` e `views.py`.
3. **Modelar primeiro, desenhar depois.** Preencha entidades, relações (`R`, `R1`, `RC`), `ADR`, `FLOWS`, `DYN` e `META`. Só então ajuste as coordenadas.
4. **Gerar:** `python -I scripts/build.py --project <pasta-fonte> --out <pasta-saida>` → `<stem>.dsl`, `<stem>.drawio`, `<stem>-arquitetura.html`.
5. **Verificar (obrigatório):**
   - `python -I scripts/check.py <pasta-saida>` — DSL, draw.io e HTML íntegros;
   - `python -I scripts/shot.py <html> <pasta-png> c1,c2,...` e **abrir os PNGs** para olhar o layout (nós truncados, linhas cruzando caixas, rótulos sobrepostos);
   - corrigir `views.py` e repetir. Ver `references/verificacao.md`.
6. **Dizer o que não foi validado**: o DSL só é de fato validado no Structurizr e o `.drawio` abrindo no draw.io — sem isso, relate como "não validado nas ferramentas".
7. **Guardar** conforme as regras do vault: rascunho em `_WIP/<data>/arquitetura-vN/` (+ `-src/`); ao fim do ciclo, promover para `05-arquitetura/` (com `INDEX.md` de frontmatter) e registrar 1 linha no Log do `README.md` raiz. Apagar versões antigas exige confirmação.

## Regras de conteúdo (disciplina, não estilo)

- **Evidência × hipótese separadas.** Cor sólida = existe/confirmado; âmbar tracejado = reuso a validar; azul = novo. Tudo que nenhuma área técnica validou leva o selo "HIPÓTESE DE TRABALHO" (`META.badge`) — não remova.
- **Cada decisão aberta vira ADR** com estado (`aberto` / `tend` / `nossa`) e referência a lacunas do vault. Decisão central sem evidência deve ser dita assim ("sem evidência para recomendar"), não disfarçada.
- **`open` por entidade** guarda o que impede de chamar aquilo de decidido; o inspetor do HTML os exibe. Escreva a pergunta, não a resposta.
- **Aba "O que este desenho não resolve"** (`META.open_limits`) é parte da entrega, não opcional.
- Não cite pessoas por nome nos diagramas; use papéis. Não ponha números não confirmados (volumes, prazos, valores) no slide.
- Se o usuário só fez uma pergunta ("é possível…?"), responda antes de gerar.

## Reprodutibilidade

- `python -I scripts/selftest.py` reconstrói `templates/exemplo` e compara com `tests/golden.json` (3 hashes SHA-256). Rode antes de confiar no ambiente (testado em Python 3.13; só biblioteca padrão) e **sempre que alterar o motor**.
- `--update` só depois de mudança **intencional** no motor, e registre o motivo.
- Os arquivos de um projeto também são reproduzíveis: guarde `model.py` + `views.py` junto das saídas; regenerar dá o mesmo HTML.
- O motor não faz rede nem lê nada fora de `--project`. Dependências: apenas a biblioteca padrão do Python; Chrome/Edge só para `shot.py`.

## Limites conhecidos

- Layout manual: ~40–60 elementos por vista é o razoável; acima disso, divida a vista.
- Mermaid C4 não é gerado (use o DSL ou o draw.io).
- O draw.io é gerado em XML plano (um `mxfile` multipágina); abre e edita, mas não é "inteligente" (sem containers aninhados).
- Os textos do motor estão em português; os do projeto vêm de `META`.

## Mapa da skill

```
SKILL.md
scripts/      build.py (entrada) · dsl.py · render_svg.py · render_drawio.py · render_html.py · check.py · shot.py · selftest.py
templates/    exemplo/ (completo, fictício) · esqueleto/ (mínimo)
references/   como-editar-o-modelo.md · layout.md · verificacao.md
tests/        golden.json
```
