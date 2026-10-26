# CLAUDE.md — Vault [PEDIDO] (Discovery)

Guia operacional deste vault, carregado automaticamente toda sessão. Detalhes completos (não repetidos aqui) em:
- @.discovery-kit/guias/GUIA-WIP.md — ciclo de vida de `_WIP/<data>/`
- @.discovery-kit/guias/GUIA-FRONTMATTER.md — schema YAML obrigatório
- @.discovery-kit/guias/GUIA-FLUXO-DISCOVERY.md — o loop `03-analise-critica/` ↔ `04-elicitacao/` ↔ reunião, e o checklist pós-reunião

Depois de criar ou editar conteúdo, rode `python3 .discovery-kit/tools/dk.py validar` (no Windows, `python` ou `py`) e corrija os erros (frontmatter e IDs; links saem como avisos, `--estrito` os reprova).

**Ao abrir o dia e antes de encerrá-lo**, rode `python3 .discovery-kit/tools/check_fluxo.py --resumo` (no Windows, `python` ou `py`): mostra no máximo 15 linhas de avisos de retorno ao fluxo (`atualizado:` defasado, `_WIP` sem destino, GO sem `05`/`06`, NFR sem fonte). Nunca bloqueia; para cada aviso, atualize a pasta definitiva ou registre a pendência em `_WIP/<dia>/_resumo.md`. Sem hook: a execução é por esta regra.

Os 3 guias acima são importados (`@`) e carregados com este arquivo em toda sessão, em qualquer SO — isto aqui é só o resumo operacional de referência rápida.

## Regras obrigatórias

1. **Resumo do dia** → sempre em `_WIP/<YYYY-MM-DD>/_resumo.md`, nunca no `README.md` raiz. O `README.md` raiz leva só 1 linha concisa no Log por marco, apontando para o resumo detalhado.
2. **Todo arquivo de conteúdo** (fora `_WIP/`, `_temp/`, `.discovery-kit/`) abre com frontmatter: `tags: [fase/*, area/*, tipo/*]`, `status`, `atualizado` — ver `.discovery-kit/guias/GUIA-FRONTMATTER.md`.
3. **Pasta do dia em `_WIP/`**: todo material novo (pautas, rascunhos, mensagens, planos) vai em `_WIP/<data-de-hoje>/`, nunca direto na raiz de `_WIP/`. Nomes seguem `pauta-N-<quem>.md`, `plano-*.md`, `correcao-*.md`, `mensagem-*.md`.
4. **Fim de ciclo em `_WIP/`**: cada arquivo é classificado resolvido/ativo/obsoleto — nunca fica "pendurado" indefinidamente. Apagar é destrutivo → sempre confirmar com o usuário antes.
5. **Retorno ao fluxo**: qualquer evento abaixo exige atualizar as pastas definitivas **na mesma sessão** (ou registrar a pendência em `_WIP/<dia>/_resumo.md`, seção "Retornos ao fluxo"). O que fica só em `_WIP/` não conta como feito.

   | Gatilho | Atualizar |
   |---|---|
   | Reunião/entrevista/DM ingerida | Q-nnn (`04`), G/C/H/R/D (`03`), Log |
   | Decisão do dono do discovery | `03` (veredito/condições), `02` se alterar o pedido ou o escopo, Log |
   | Mudança de escopo | `02-entendimento` (pedido), `03`, `04` (Q descartadas/novas), Log |
   | Artefato de autoria concluído (desenho, plano, documento de apresentação) | destino definitivo da tabela de promoção em `GUIA-WIP.md`, Log |
   | Novo fato de contexto (documento, diagrama, wiki) | `01-contexto`, `_inventario-fontes` |

   O Log é a seção `## Log` do `README.md` raiz (1 linha por marco: `data | marco | link para _resumo.md`). **Não criar documento de análise novo por conversa** — é excepcional, reservado a lotes retroativos de reuniões não planejadas. Checklist pós-reunião em `GUIA-FLUXO-DISCOVERY.md`.
6. **Veredito GO/NO-GO em 3 níveis** (GO-A, GO-B, GO-C, em `03-analise-critica/README.md`) só muda com artefato, não relato oral. **Um nível posterior não pode ser mais positivo que o anterior** (GO-B ≤ GO-A; GO-C ≤ GO-B). `05` só abre com GO-A ≥ condicionado; estimativa em `06` só com GO-B ≥ condicionado. Resposta de 1 pessoa sem autoridade canônica não fecha uma Q-nnn. Fontes sem transcript (DM, conversa direta, anotação) valem pela afirmação do usuário, sem exigir artefato externo; reunião gravada fica "aguardando transcript" até a ingestão.
7. **`00-fontes/`** é fonte da verdade — nunca editar o conteúdo, só a frontmatter.

## Convenções de IDs
`Q-nnn` perguntas · `G-nnn` lacunas · `C-nn` contradições · `H-nnn` hipóteses · `R-nnn` riscos · `D-nnn` dependências.
