# Prompt — Implementar a SPEC v2 do Discovery Kit

Cole o bloco abaixo como **primeira mensagem** de uma sessão do Claude Code aberta na raiz do repositório `discovery-kit` (a raiz do gerador, não `scaffold/`). Este prompt foi adaptado à estrutura 0.3.1 (gerador + `scaffold/`); o original foi escrito sobre a 0.1.0. Sugestão de modelo: Sonnet com esforço médio para T1–T5, T8, T10; Opus com esforço alto só para a revisão final (§ "Fechamento").

---

## Prompt (copie a partir daqui)

```
Você vai implementar a SPEC docs/SPEC-evolucao-v2-fluxo-ate-pb-macro.md neste repositório (discovery-kit).

CONTEXTO
- Este repositório é o GERADOR (`install.sh`, `discovery-kit.json`, `CHANGELOG.md`, `docs/`, `tests/`) de um scaffold genérico de vault Obsidian + Claude Code para discovery; o vault em si vive em `scaffold/`. Ele foi extraído de um projeto real e sanitizado. Nenhum dado de cliente, nome de pessoa ou nome de sistema real pode entrar em qualquer arquivo novo.
- A SPEC resolve três problemas observados no uso real: (1) o fluxo não tem fim definido (05 e 06 são "futuro"); (2) o fluxo não volta das pastas de trabalho (_WIP) para as definitivas; (3) conteúdo comercial contamina o núcleo.
- As decisões D1 a D7 da SPEC já foram tomadas. Não as reabra. P1 e P2 foram resolvidos em D6 e D7. A seção 0 da SPEC (adaptação à 0.3.1) traz os caminhos novos e registra P3 (substituto do hook) e P4 (seção Log ausente) como pontos em aberto: aplique o padrão que a seção 0 indica, sinalize-os no resumo final e não os decida além disso. Se surgir outro ponto em aberto, registre-o como pendência.
- A SPEC foi escrita sobre a 0.1.0. A seção 0 PREVALECE sobre os caminhos do corpo. Em qualquer divergência entre o corpo e a seção 0, siga a seção 0.

ANTES DE ESCREVER QUALQUER ARQUIVO
1. Leia a SPEC inteira (começando pela seção 0), depois README.md e CHANGELOG.md (gerador), scaffold/README.md, scaffold/CLAUDE.md, scaffold/.discovery-kit/guias/GUIA-WIP.md, GUIA-FRONTMATTER.md, GUIA-FLUXO-DISCOVERY.md, scaffold/03-analise-critica/README.md, scaffold/04-elicitacao/README.md, scaffold/05-arquitetura/README.md, scaffold/06-backlog/README.md, scaffold/.discovery-kit/tools/check_links.py e dk.py, e tests/test_scaffold.sh. Não existe mais hook SessionStart: os guias entram por @import no scaffold/CLAUDE.md.
2. Liste de volta, em uma tabela curta, as convenções que você extraiu (frontmatter, nomes de arquivo, IDs, tom, formato de tabela, uso de [preencher]). Siga-as estritamente nos arquivos novos.
3. Rode `git status` e `git log --oneline -5`. Crie uma branch `feat/spec-v2` a partir da branch atual. Se a árvore estiver suja, pare e avise. Rode também `bash tests/test_dk_py.sh && bash tests/test_scaffold.sh && bash tests/test_install.sh` e `python3 -I scaffold/.discovery-kit/tools/dk.py validar scaffold` para registrar a linha de base (esperado: 3 PASS e 0 erros, 19 avisos de link). Se a linha de base já falhar, pare e avise.

COMO TRABALHAR
- Siga a ordem do backlog da SPEC (§9): T1, T2, T3, T4, T5, T6, T8, T9, T7, T10. T9 (vault de teste) vem antes de T7 porque T6 precisa dele para ser verificado.
- Um commit por tarefa, mensagem no formato `feat(spec-v2): T<n> <resumo>`. Não faça push.
- Mudanças cirúrgicas: toque só no que a tarefa exige. Não "melhore" texto adjacente. Se notar um problema fora do escopo, anote em docs/spec-v2-observacoes.md e siga. Arquivos novos do vault ficam em scaffold/; fixtures e testes ficam na raiz do gerador (tests/).
- Templates: use [preencher] onde o conteúdo depende de um projeto. NUNCA invente valores numéricos de calibração (horas por tamanho, multiplicadores): marque [preencher] e cite a regra da SPEC §6.3.
- Se uma instrução da SPEC for ambígua ou conflitar com um arquivo existente, pergunte antes de decidir.

VERIFICAÇÃO (obrigatória por tarefa)
- T1: a tabela de mapa de etapas é idêntica nos 4 arquivos (diff mecânico).
- T2: o template de 03 tem 3 blocos de nível (GO-A, GO-B, GO-C) e a regra "nível posterior não pode ser mais positivo que o anterior" aparece em 03, no guia de fluxo e no CLAUDE.md.
- T4 (calibração): `calibracao.md` tem coluna de origem por faixa (histórico / experiência / IA), a regra de revisão do arquiteto para origem IA, a pasta `00-fontes/historico/` documentada, e o limite de confiança Média sem histórico (SPEC §6.3 passo 2).
- T3/T4: todos os campos de §6.1 e §6.2 existem nos templates; o rótulo "uso interno, não é compromisso nem preço" está no topo de 06; o exemplo de 06 contém ao menos um RNF com status `lacuna`.
- T6: rode `python3 -I scaffold/.discovery-kit/tools/check_fluxo.py scaffold` no scaffold vazio (zero avisos) e na fixture de T9 em tests/fixtures/ (os 4 desvios plantados detectados, e só eles). Mostre a saída. Crie tests/test_check_fluxo.sh que automatiza isso, no estilo dos testes existentes.
- T6 (substituto do hook, ver P3): `check_fluxo.py --resumo` imprime no máximo 15 linhas, nunca bloqueia (exit 0) e o scaffold/CLAUDE.md manda rodá-lo ao abrir e ao encerrar o dia. Não recrie hook nem settings.json.
- T8: dk.py aceita os novos tipo/adr, tipo/backlog e tipo/estimativa (atualize TIPOS e cubra com caso novo em tests/test_dk_py.sh).
- Todas: rode `python3 -I scaffold/.discovery-kit/tools/dk.py validar scaffold` (0 erros; avisos de link iguais à linha de base, ~19) e os 3 testes de tests/. Não pode haver erro nem aviso novo causado por você. Templates e exemplos não podem usar IDs numerados sem definição (use G-nnn, Q-nnn): dk.py acusa. No Windows o executável é `python` ou `py`.
- T10: subir discovery-kit.json para 0.4.0 e registrar no CHANGELOG.md; atualizar o README do gerador e o scaffold/README.md.
- Critério de aceite final: SPEC §10, itens 1 a 6 (com o item 5 lido como dk.py validar acima), cada um com a evidência (comando + saída ou arquivo + trecho).

FECHAMENTO
1. Procure no repositório por: preço, proposta, escopo aberto, escopo fechado, modelo comercial, cliente, nomes próprios. Fora de scaffold/adaptadores/ não pode sobrar nada (docs/ do gerador, CHANGELOG e esta SPEC ficam fora da busca).
2. Entregue uma tabela final: tarefa | commit | verificação executada | resultado | pendências.
3. Liste as pendências novas que surgiram e o que precisa ser decidido pelo dono do kit. Herdadas: P3 (substituto do hook), P4 (seção Log ausente) e a localização de adaptadores/ em scaffold/ (seção 0). P1 e P2 estão resolvidos.
4. Não faça merge nem push. Pare e aguarde.

COMECE agora pelo passo "ANTES DE ESCREVER QUALQUER ARQUIVO". Responda com a tabela de convenções e peça confirmação antes da T1.
```
