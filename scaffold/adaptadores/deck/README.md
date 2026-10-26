# adaptadores/deck

Gera uma apresentação `.pptx` a partir de um **arquivo de dados JSON**. O gerador não tem texto de cliente embutido: todo o conteúdo vem do JSON, preenchido por você a partir de `03`, `05` e `06`. Ver o contrato em `../README.md` (a estimativa de `06` não entra sem decisão explícita do dono do discovery).

## Uso

```bash
python3 adaptadores/deck/gerar_deck.py meus-dados.json saida.pptx --perfil padrao
python3 adaptadores/deck/gerar_deck.py meus-dados.json --validar
```

No Windows, `python` ou `py`. Copie `exemplo-dados.json`, preencha os `[preencher]` e valide antes de gerar: o gerador recusa dados com `[preencher` pendente.

## Dependência

`--validar` usa só a stdlib. Gerar o `.pptx` exige `pip install python-pptx` — dependência **opcional, só deste adaptador**; o resto do kit continua só com stdlib.

## Perfis

`perfis.json` define fonte e cores (`cor_fundo`, `cor_titulo`, `cor_texto`, em hexadecimal) por perfil. Acrescente perfis sem mexer no código; escolha com `--perfil`.

## Formato dos dados

```json
{
  "perfil": "padrao",
  "titulo": "...",
  "slides": [
    {"titulo": "...", "bullets": ["..."]},
    {"titulo": "...", "tabela": {"cabecalho": ["..."], "linhas": [ ["..."] ]}}
  ]
}
```
