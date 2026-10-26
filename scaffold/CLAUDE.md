# CLAUDE.md — Vault [PEDIDO] (Discovery)

Guia operacional deste vault, carregado automaticamente toda sessão. Detalhes completos (não repetidos aqui) em:
- @.discovery-kit/guias/GUIA-WIP.md — ciclo de vida de `_WIP/<data>/`
- @.discovery-kit/guias/GUIA-FRONTMATTER.md — schema YAML obrigatório
- @.discovery-kit/guias/GUIA-FLUXO-DISCOVERY.md — o loop `03-analise-critica/` ↔ `04-elicitacao/` ↔ reunião, e o checklist pós-reunião

Depois de criar ou editar conteúdo, rode `python3 .discovery-kit/tools/dk.py validar` (no Windows, `python` ou `py`) e corrija os erros (frontmatter e IDs; links saem como avisos, `--estrito` os reprova).

Os 3 guias acima são importados (`@`) e carregados com este arquivo em toda sessão, em qualquer SO — isto aqui é só o resumo operacional de referência rápida.

## Regras obrigatórias

1. **Resumo do dia** → sempre em `_WIP/<YYYY-MM-DD>/_resumo.md`, nunca no `README.md` raiz. O `README.md` raiz leva só 1 linha concisa no Log por marco, apontando para o resumo detalhado.
2. **Todo arquivo de conteúdo** (fora `_WIP/`, `_temp/`, `.discovery-kit/`) abre com frontmatter: `tags: [fase/*, area/*, tipo/*]`, `status`, `atualizado` — ver `.discovery-kit/guias/GUIA-FRONTMATTER.md`.
3. **Pasta do dia em `_WIP/`**: todo material novo (pautas, rascunhos, mensagens, planos) vai em `_WIP/<data-de-hoje>/`, nunca direto na raiz de `_WIP/`. Nomes seguem `pauta-N-<quem>.md`, `plano-*.md`, `correcao-*.md`, `mensagem-*.md`.
4. **Fim de ciclo em `_WIP/`**: cada arquivo é classificado resolvido/ativo/obsoleto — nunca fica "pendurado" indefinidamente. Apagar é destrutivo → sempre confirmar com o usuário antes.
5. **Checklist pós-reunião** (ver `GUIA-FLUXO-DISCOVERY.md`): atualizar `04-elicitacao/perguntas-por-area.md` (status da Q-nnn tocada), `03-analise-critica/*` (G/C/H/R/D correspondente) e 1 linha no Log do `README.md` raiz. **Não criar documento de análise novo por conversa** — é excepcional, reservado a lotes retroativos de reuniões não planejadas.
6. **Veredito GO/NO-GO em 3 níveis** (GO-A, GO-B, GO-C, em `03-analise-critica/README.md`) só muda com artefato, não relato oral. **Um nível posterior não pode ser mais positivo que o anterior** (GO-B ≤ GO-A; GO-C ≤ GO-B). `05` só abre com GO-A ≥ condicionado; estimativa em `06` só com GO-B ≥ condicionado. Resposta de 1 pessoa sem autoridade canônica não fecha uma Q-nnn. Fontes sem transcript (DM, conversa direta, anotação) valem pela afirmação do usuário, sem exigir artefato externo; reunião gravada fica "aguardando transcript" até a ingestão.
7. **`00-fontes/`** é fonte da verdade — nunca editar o conteúdo, só a frontmatter.

## Convenções de IDs
`Q-nnn` perguntas · `G-nnn` lacunas · `C-nn` contradições · `H-nnn` hipóteses · `R-nnn` riscos · `D-nnn` dependências.
