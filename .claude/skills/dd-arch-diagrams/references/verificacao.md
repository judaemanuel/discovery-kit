# Verificação e reprodutibilidade

## Comandos (a partir da pasta da skill)

```
python -I scripts/selftest.py                                   # regressão do motor (3 hashes)
python -I scripts/build.py --project <src> --out <saida>        # gera DSL, draw.io e HTML
python -I scripts/check.py <saida>                              # integridade estática
python -I scripts/shot.py <saida>/<stem>-arquitetura.html <pngs> c1,c2,slide --size 1700x1050
```

Use sempre `python -I` (modo isolado): impede que um `json.py` ou similar na pasta de trabalho seja importado no lugar da biblioteca padrão.

## O que cada verificação cobre

| Verificação | Pega | Não pega |
|---|---|---|
| `selftest.py` | mudança acidental no motor; ambiente diferente | erros de conteúdo do seu projeto |
| `check.py` (DSL) | chaves, endpoints indefinidos, **relações duplicadas**, passos `dynamic` sem relação | erros de semântica do Structurizr |
| `check.py` (draw.io) | XML malformado, ids duplicados, `source`/`target` inexistentes | o desenho abrir "bonito" |
| `check.py` (HTML) | placeholder não resolvido, JSON do inspetor inválido, aba sem seção | layout |
| `shot.py` + olhar o PNG | truncamentos, linhas atravessando caixas, rótulos sobrepostos | comportamento do JavaScript (clique/zoom) |

**Não validado por esta skill:** abrir o `.dsl` no Structurizr (Lite, CLI ou online) e o `.drawio` no draw.io. Se o ambiente não os tem, diga isso ao usuário ao entregar.

## Teste de comportamento do HTML (opcional)

Para conferir o inspetor sem navegador interativo: gere uma cópia do HTML com um `<script>` final que dispara `click` em um nó e escreve o resultado em `document.title`, e rode `chrome --headless=new --dump-dom <arquivo>#c2`. Se o título trouxer o nome da entidade e a contagem de selos de ADR, o JS está íntegro.

## Golden e mudanças no motor

- `tests/golden.json` guarda os hashes do exemplo. Mudança **intencional** no motor → `selftest.py --update` + nota do motivo no commit/log.
- Mudança de conteúdo no `templates/exemplo` também altera o golden; trate como mudança de motor.
- Se `selftest.py` falhar sem mudança alguma, suspeite do ambiente (versão do Python, locale) antes de mexer no motor.

## Proveniência

O motor foi extraído de um conjunto de diagramas real, depois de **refatorado para separar motor e projeto**. A refatoração foi validada reconstruindo o projeto original com o motor novo: os três arquivos saíram **idênticos byte a byte** (SHA-256) aos gerados antes da refatoração. O conteúdo do projeto original não faz parte desta skill; `templates/exemplo` é totalmente fictício.

## Armadilhas já encontradas

- **Chrome headless** funcionou; o **Edge headless travou** em um ambiente corporativo — `shot.py` tenta Chrome primeiro e usa timeout de 40 s.
- `<defs>` de marcadores SVG dentro de uma aba oculta (`display:none`) não renderizam no Chrome: cada SVG usa ids de marcador únicos (o motor já faz isso).
- PowerShell 5.1: `Set-Content -Encoding UTF8` grava BOM; prefira editar com Python (`encoding='utf-8'`) para não mudar hashes.
- Console do Windows em cp1252 mostra acentos quebrados na saída dos scripts; os arquivos gerados estão corretos (UTF-8).
