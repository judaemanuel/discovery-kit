# Layout manual (`views.py`)

Cada vista é um objeto `V(id, título, subtítulo, largura, altura)` registrado em `VIEWS['<chave>']`. Coordenadas em pixels; origem no canto superior esquerdo.

## API

| Chamada | Efeito |
|---|---|
| `v.n(id, x, y, w, h, **ov)` | posiciona a entidade `id`; `ov` sobrescreve campos (usado no slide) |
| `v.e(src, (fx,fy), dst, (fx,fy), label='', kind=None, mid=None, midx=None, pts=None, bi=False, lab=None)` | aresta entre **pontos de fração** das caixas; `(0.5,1)` = meio da borda inferior |
| `v.box(x, y, w, h, título)` | borda tracejada do sistema (fronteira) |
| `v.label(x, y, texto, cls)` | texto solto; `cls`: `band` (padrão), `shead`, `stitle`, `stitle2`, `ssub` |
| `v.decor.append(dict(t='arrow', pts=[...]))` | seta simples (slide) |
| `v.decor.append(dict(t='banner', x,y,w,h,title,text))` e `dict(t='legend', x,y)` | faixa e legenda do slide |

### Rotas
- sem parâmetro → reta (se não for horizontal/vertical, vira diagonal);
- `mid=y` → vertical–horizontal–vertical passando por `y` (canal horizontal);
- `midx=x` → horizontal–vertical–horizontal passando por `x`;
- `pts=[(x,y), ...]` → pontos intermediários manuais;
- `bi=True` → seta nas duas pontas; `lab=(x,y)` fixa a posição do rótulo.

## Receita do C2 (a que funcionou)

Camadas de cima para baixo, todas alinhadas em **5 colunas** (`x = 200 + 290·i`, largura 250):

1. pessoas (chips de 52 px) → sistemas externos de entrada;
2. fronteira do sistema contendo: **Experiência** (API, centralizada) → **Núcleo** (serviços; altura 124) → **Dados** (cilindros 46 px logo abaixo de seu dono, à esquerda) → **Barramento** (barra de 40 px, largura total) → **Integração/ACL** (adaptadores; altura 118);
3. sistemas externos de saída, alinhados sob seus adaptadores;
4. pessoas de saída.

Regras que evitaram retrabalho:
- **Ordene o núcleo pelo grafo de dependências**: o serviço mais conectado no meio; o que recebe agendador à direita; o somente-leitura à esquerda.
- **Canais horizontais** entre camadas para as arestas "da API para os serviços" (`mid=` distintos, 8 px de diferença).
- **Portas diferentes para arestas diferentes** na mesma borda (frações 0.24, 0.5, 0.8…), nunca duas no mesmo ponto.
- **Barramento**: serviços que publicam/consomem ligam-se por seta vertical bidirecional na parte direita da caixa (não atravessa o cilindro); quem só é síncrono **não** liga ao barramento — isso comunica a arquitetura.
- **Rótulo só onde cabe**: vãos entre caixas < 60 px não comportam rótulo (corte-o e deixe o inspetor explicar).
- Setas entre caixas adjacentes: saem de frações diferentes (0.3 e 0.75) para não se sobrepor.

## Capacidade de texto de um bloco

| Tipo | Tamanho sugerido | Cabe |
|---|---|---|
| contêiner / componente | 250 × 124 (componente: 240 × 104) | nome (2 linhas) + tecnologia (1) + descrição (3) |
| externo | 250 × 108 | nome (até 2 linhas) + tecnologia + descrição (3) |
| pessoa | 190 × 52 (nome até 2 linhas) | só o nome |
| db | 120–160 × 46 | nome curto + tecnologia |

Descrição que não cabe é cortada com "…" no desenho (o inspetor mostra inteira). Prefira encurtar o texto a esticar a caixa.

## Slide executivo (16:9, 1280 × 720)

Tipos de nó: `kind='sbox'` (nome, desc, `status`, `badge='1 2'` para selos vermelhos numerados), `kind='scard'` (cartão de decisão: `num`, `name`, `desc`, `who`). Quatro colunas — quem usa · o sistema · sistemas existentes · decisões — e uma faixa `banner` embaixo. Os selos numerados ligam cada decisão ao ponto da solução que ela afeta. Não ponha números não confirmados (volumes, prazos, valores).

## Conferência (checklist visual)

- nenhuma linha atravessa o interior de uma caixa;
- nenhum rótulo sobre uma caixa ou sobre outra linha;
- nenhum texto cortado em nome/tecnologia;
- setas com cabeça visível nos dois sentidos quando `bi=True`;
- aba "Slide": nada fora dos 1280 × 720.
