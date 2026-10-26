# Como editar o modelo (`model.py`)

O motor importa `model.py` e `views.py` da pasta passada em `--project`. Os nomes abaixo são **contrato**: o motor os exige.

## 1. Entidades — `ent(id, kind, name, tech, desc, status, parent, adr, open, refs)`

| `kind` | O que é | Regras |
|---|---|---|
| `person` | Pessoa ou papel | `status='pessoa'`; não use nome próprio |
| `ext` | Sistema externo ao seu | vira `softwareSystem` no DSL |
| `system` | **O** sistema em desenho | exatamente 1; seu id vai em `META['sys_id']` |
| `container` | Serviço/aplicação dentro do sistema | filho implícito do `system` |
| `db` | Banco/repositório dentro do sistema | desenhado como cilindro |
| `bus` | Barramento de eventos | desenhado como barra roxa |
| `component` | Peça interna de um contêiner | exige `parent='<id do contêiner>'` |

- **Ids**: letras, números e `_` (ex.: `core`, `o_engine`). Viram identificadores do DSL.
- **`status`**: `novo` (azul) · `reuso` (âmbar tracejado: reaproveita padrão/serviço, **a validar**) · `existente` (cinza) · `pessoa` (navy). Use `reuso`/`existente` só com evidência.
- **`adr`**: lista de ids de ADR (ex.: `['ADR-02']`) — vira selo vermelho no bloco e link no inspetor.
- **`open`**: lista de perguntas em aberto — aparecem em vermelho no inspetor.
- **`desc`**: uma frase (o bloco trunca em ~3 linhas; o inspetor mostra completo).
- Textos não devem conter aspas duplas (o DSL as troca por aspas simples).

## 2. Relações

Formato de cada tupla: `(origem, destino, texto, tecnologia, tipo)`; `tipo` ∈ `sync` | `async` | `batch`.

| Lista | Nível | Observações |
|---|---|---|
| `R` | entre contêineres, externos e pessoas (C2) | uma entrada por **direção**; o par (origem, destino, texto) não pode se repetir |
| `R1` | nível sistema (C1) | use o id do `system` no lugar dos contêineres; relações pessoa↔externo podem repetir as de `R`: o DSL só emite as que envolvem o sistema |
| `RC` | entre componentes e contêineres (C3) | concatene as listas por contêiner: `RC = RC_A + RC_B` |

O `tipo` define a linha: `sync` contínua cinza-escura, `async` tracejada roxa, `batch` pontilhada azul-petróleo. A aresta desenhada em `views.py` herda o tipo da relação com os mesmos (origem, destino); passe `kind=` para forçar.

## 3. Decisões — `ADR` e `ADR_STATE`

`ADR = [(id, decisão proposta, alternativas, depende de, estado, nota)]` com estado ∈ `aberto` | `tend` | `nossa`.
`ADR_STATE` traduz o estado para o rótulo da tabela (copie do exemplo).

## 4. Fluxos de sequência — `FLOWS`

```python
FLOWS = {'f_chave': dict(title='Fluxo 1 — ...', parts=[('S','Rótulo'), ...], msgs=[...])}
```

Mensagens em `msgs` (as setas são numeradas automaticamente):

| Item | Significado |
|---|---|
| `('A','B','texto','call')` | chamada síncrona (linha contínua) |
| `('B','A','texto','ret')` | retorno (tracejada cinza) |
| `('A','B','texto','async')` | evento/mensagem assíncrona (tracejada roxa) |
| `('A','A','texto','self')` | auto-chamada |
| `('note','A','B','texto')` | nota amarela cobrindo as colunas A–B |
| `('alt','rótulo')` / `('loop','rótulo')` | abre um quadro; um `alt` novo fecha o `alt` anterior do mesmo nível |
| `('end',)` | fecha o quadro aberto mais recente |

## 5. Vistas dynamic do Structurizr — `DYN`

`DYN = {'Nome_Sem_Acento': ('descrição', [(origem, destino, 'texto'), ...])}`. **Cada par (origem, destino) precisa existir em `R`** — `check.py` acusa o contrário. Pode ser `{}`.

## 6. `META` — metadados que o motor não conhece

| Chave | Uso |
|---|---|
| `stem` | prefixo dos arquivos: `<stem>.dsl`, `<stem>.drawio`, `<stem>-arquitetura.html` |
| `sys_id` | id da entidade `system` |
| `agent`, `download_prefix` | assinatura do draw.io; prefixo do nome dos SVG baixados |
| `page_title`, `title`, `badge`, `subtitle` | `<title>` e cabeçalho da página (o `&` é escapado pelo motor) |
| `chips` | rótulos dentro do bloco do sistema no C1 |
| `flow_hint` | legenda sob cada fluxo |
| `slide_legend` | itens da legenda do slide: `[(rótulo, status)]` |
| `tabs` | `[(chave, rótulo, tipo)]`, tipo ∈ `blk` (vista em `VIEWS`), `seq` (fluxo em `FLOWS`), `doc` (`adr` e `sobre`) |
| `drawio_views`, `drawio_flows` | quais vistas e fluxos viram páginas do draw.io, em ordem |
| `open_limits` | `[(título, motivo)]` — "O que este desenho não resolve" |
| `adr_sub`, `principles` | subtítulo da aba Decisões (HTML) e lista de princípios (`<li>…</li>`) |
| `sobre` | `dict(sub=..., cards=[(título, [<li>…</li>])])` |
| `dsl` | `workspace_name`, `workspace_desc`, `c1`, `c2` e `c3=[(id_do_contêiner, nome_da_vista, descrição)]` |

A chave de aba `slide` é tratada de forma especial (vista 16:9 sem inspetor). `adr` e `sobre` são seções geradas; não precisam de vista.

## 7. Erros comuns

- Relação duplicada em `R` → o Structurizr rejeita o modelo (`check.py` avisa).
- `DYN` com par que não existe em `R`.
- `component` sem `parent` ou com `parent` que não é contêiner.
- Esquecer `RC = ...` (o motor importa `RC`, mesmo vazio).
- Aba em `META['tabs']` sem a vista correspondente em `VIEWS`/`FLOWS`.
