# adaptadores/

Saídas **opcionais** para terceiros, derivadas do núcleo do discovery. Nada aqui é necessário para concluir o fluxo (`00` a `06`).

## Contrato

1. **Consome** o veredito de `03-analise-critica/` e o conteúdo de `05-arquitetura/` e `06-backlog/`. **Nunca altera o núcleo.**
2. **Nenhum dado de cliente** embutido no gerador ou nos esqueletos: o conteúdo entra por arquivo de dados ou é preenchido na instância, nunca versionado no kit.
3. **Não copie notas internas** (`_WIP/`, análises com marcação ✅/🟡/❓, nomes de pessoas citados em reunião) para o material externo.
4. **A estimativa de `06-backlog/` é de uso interno.** Ela só aparece em material externo com decisão explícita do dono do discovery, registrada no `_resumo.md` do dia.
5. Escopo aberto ou fechado, modelo comercial e preço ficam **aqui**, nunca no núcleo.

`dk.py validar` e `check_fluxo.py` ignoram esta pasta: os arquivos daqui não seguem o frontmatter do vault.

| Adaptador | O que gera | Entrada |
|---|---|---|
| `proposta/` | Esqueleto de proposta técnica: escopo, fora de escopo, premissas, riscos, abordagem | `03`, `05`, `06` |
| `deck/` | Apresentação `.pptx` a partir de um arquivo de dados JSON, com perfis de cor e fonte | JSON preenchido a partir de `03`, `05`, `06` |
