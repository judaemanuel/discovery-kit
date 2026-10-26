# SPEC — Evolução do Discovery Kit (v2): do fonte ao GO, com arquitetura conceitual e PB macro estimado

**Status:** proposta para implementação · **Origem:** uso real do kit numa demanda de legado (migração de integração), primeira vez em que o fluxo foi levado além do veredito · **Escopo desta SPEC:** somente o repositório `discovery-kit`. Nenhum vault de projeto é alterado.

## 0. Adaptação à estrutura 0.3.1 (prevalece sobre os caminhos do corpo)

Esta SPEC foi escrita sobre o kit **0.1.0** (vault na raiz, `_WIP/` com os guias, `.tools/`, hook PowerShell). Desde então o repositório virou **gerador + `scaffold/`** (CHANGELOG 0.2.0 a 0.3.1). O conteúdo e as decisões D1 a D7 continuam valendo; só mudam os caminhos e dois itens. Onde o corpo e esta seção divergirem, vale esta seção.

**Caminhos** (o vault vive em `scaffold/`; o que é do gerador fica na raiz):

| No corpo da SPEC | Agora |
|---|---|
| `README.md` raiz (tabela de etapas, Log, fim do fluxo) | `scaffold/README.md` (instância). O `README.md` da raiz é do gerador |
| `CLAUDE.md` | `scaffold/CLAUDE.md` |
| `_WIP/README.md` | `scaffold/.discovery-kit/guias/GUIA-WIP.md` |
| `_WIP/GUIA-FRONTMATTER.md`, `_WIP/GUIA-FLUXO-DISCOVERY.md` | `scaffold/.discovery-kit/guias/GUIA-FRONTMATTER.md` e `GUIA-FLUXO-DISCOVERY.md` |
| `00-fontes/` a `06-backlog/` | `scaffold/00-fontes/` a `scaffold/06-backlog/` |
| `.tools/check_links.py`, `.tools/check_fluxo.py` (novo) | `scaffold/.discovery-kit/tools/check_links.py`, `check_fluxo.py` |
| `.tools/testdata/` (T9) | `tests/fixtures/` na raiz do gerador: a fixture é do gerador e não deve ser copiada para as instâncias |
| `adaptadores/` na raiz (§8) | `scaffold/adaptadores/`: o contrato consome `03`, `05` e `06` de uma instância, então pertence à instância. **Decisão do mantenedor desta adaptação, a confirmar pelo dono do kit** |
| `.claude/hooks/session-start.ps1` | não existe mais |

**Itens que mudam:**

1. **§7.3e e T6 (hook).** O hook foi removido na 0.3.1: não roda no PowerShell do Windows. Os guias entram por `@import` no `scaffold/CLAUDE.md`. Substituição: `check_fluxo.py` ganha a opção `--resumo` (no máximo 15 linhas, sem bloqueio) e o `CLAUDE.md` ganha a instrução de rodá-lo ao abrir o dia e antes de encerrá-lo. Reintroduzir um hook só para isso reabriria o problema de portabilidade. **Ponto em aberto P3 para o dono do kit.**
2. **T8 (frontmatter).** Além do guia, o validador `scaffold/.discovery-kit/tools/dk.py` tem a lista `TIPOS` fixa. Os novos `tipo/adr`, `tipo/backlog` e `tipo/estimativa` precisam entrar também nele, ou `dk.py validar` os rejeitará.

**Restrições novas vindas de ferramentas que não existiam:**

- `python3 scaffold/.discovery-kit/tools/dk.py validar scaffold` deve continuar com **0 erros** (hoje: 0 erros, 19 avisos de link). Templates e exemplos com IDs `G-nnn`/`Q-nnn` numerados falham por "referenciado sem definição": use `G-nnn` nos templates ou defina o ID no exemplo. `RF-nnn`/`RNF-nnn` não colidem com a regra de IDs.
- `bash tests/test_dk_py.sh`, `test_scaffold.sh` e `test_install.sh` devem continuar passando. `test_scaffold.sh` confere que todo caminho citado em `CLAUDE.md`/guias existe e que cada guia importado por `@` está presente.
- Windows: o executável do Python é `python` ou `py`; documentar nos novos guias e templates como já é feito no `CLAUDE.md`.
- Versão: registrar no `CHANGELOG.md` e subir `discovery-kit.json` para 0.4.0 (parte da T10). Atualizar a lista `sistema` se surgir caminho novo do gerador.

**Pendência herdada, não é desta SPEC:** `CLAUDE.md` (regra 5), `01-contexto/README.md` e a skill `dd-arch-diagrams` mandam registrar "1 linha no Log do `README.md` raiz", mas `scaffold/README.md` **não tem seção Log** (foi removida na genericização da 0.1.0). O §7.3d item 1 depende desse Log. Registrar como **P4**: ou se cria a seção `## Log` no `scaffold/README.md` (formato `data | marco | link para _resumo.md`) como parte da T5, ou se declara outro local. Decisão do dono do kit.

## 1. BLUF

O kit hoje cobre bem `00-fontes` → `04-elicitacao` e o veredito GO/NO-GO. Três problemas apareceram no uso real:

1. **O fim do fluxo é indefinido.** `05-arquitetura/` e `06-backlog/` são "futuro", sem forma nem critério de saída. O trabalho de arquitetura e de "o que entregar" acabou em `_WIP/`.
2. **O fluxo não volta.** Depois de certo ponto, decisões e artefatos novos ficam só em `_WIP/` e não retornam a `01`/`02`/`03`/`04`. Resultado: pastas definitivas desatualizadas, `atualizado:` no frontmatter errado, e o estado real do discovery só existe nos resumos diários.
3. **Conteúdo comercial contamina o núcleo.** O GO foi formulado em termos de proposta (escopo aberto/fechado, preço), o que torna o kit específico de quem vende.

Esta SPEC propõe: (a) um **fim claro** — GO em níveis → `05` conceitual → `06` PB macro com estimativa; (b) um **mecanismo de retorno** com verificação mecânica; (c) a **separação** entre núcleo (genérico) e adaptadores (comercial, apresentação).

## 2. Decisões já tomadas (não reabrir)

| # | Decisão | Origem |
|---|---|---|
| D1 | O kit passa a terminar em: GO (condicionado ou não) + `05` arquitetura **conceitual** + `06` **PB macro** com FRs, NFRs e estimativas | Dono do kit |
| D2 | Comercial (escopo aberto/fechado, modelo comercial, proposta, deck) sai do fluxo central e vira **adaptador opcional** | Dono do kit |
| D3 | Estimativa serve ao **planejamento de capacidade interno** (quem executa o discovery), não é publicada ao cliente por padrão | Dono do kit |
| D4 | Mudança só neste repositório; o kit será validado em **demandas futuras** (inclusive de natureza diferente) | Dono do kit |
| D5 | Story points ficam **fora do núcleo** (campo opcional): sem time e sem velocidade no discovery, o número não tem calibração | Revisão adversarial |
| D6 | **Quem calibra:** o arquiteto que conduz o discovery. A base da calibração pode ser (a) histórico ingerido em `00-fontes/`, (b) experiência do arquiteto em desafios equivalentes, ou (c) estimativa assistida por IA. A origem de cada faixa é sempre registrada (ver §6.3 passo 2) | Dono do kit |
| D7 | O gerador de deck fica **no kit**, em `adaptadores/deck/`, sem texto de cliente embutido | Dono do kit (aceitou a recomendação) |

## 3. Não objetivos

- Não migrar nem editar nenhum vault de projeto existente.
- Não incluir dado de cliente, nome de pessoa ou sistema no kit (a sanitização do commit `fc3a938` deve continuar valendo).
- Não automatizar julgamento semântico. Verificações mecânicas apenas (ver §7).
- Não definir backlog detalhado (histórias, critérios de aceite por história). O PB é **macro**.

## 4. Mapa de etapas (corrigir ambiguidade)

O kit usa "Etapa" (0 a 4) e número de pasta (00 a 06) com defasagem. Isso gerou confusão no uso ("etapa 5 e 6" vs "Etapa 3 e 4"). Adicionar a tabela abaixo ao `README.md` raiz, ao `GUIA-FLUXO-DISCOVERY.md` e aos READMEs de `05` e `06`.

| Pasta | Etapa | Saída |
|---|---|---|
| `00-fontes/` | — | fonte da verdade |
| `01-contexto/` | 0 | o que já existe |
| `02-entendimento/` | 1 | o que o pedido diz |
| `03-analise-critica/` | 2 | veredito + condições por nível de GO |
| `04-elicitacao/` | 2→3 | perguntas, ondas, respostas |
| `05-arquitetura/` | 3 | arquitetura conceitual (hipótese) |
| `06-backlog/` | 4 | PB macro (FR/NFR) com estimativa |

## 5. GO em níveis

Substituir o veredito único por **três níveis**, cada um com condições numeradas, status por condição e exigência de artefato (regra 6 do `CLAUDE.md` continua valendo).

| Nível | Pergunta | Libera |
|---|---|---|
| **GO-A** | Sabemos o suficiente para desenhar uma arquitetura conceitual? | abrir `05` em modo conceitual |
| **GO-B** | Sabemos o suficiente para estimar em faixa? | preencher estimativas em `06` |
| **GO-C** | Sabemos o suficiente para detalhar e construir? | handoff para fora do kit (fora de escopo) |

Regras:
- Cada nível pode ser `NO-GO`, `GO condicionado` ou `GO`. Condições de `GO condicionado` são listadas, numeradas e rastreadas a G/Q/C/R.
- Um nível posterior nunca pode estar acima de um anterior (GO-B não pode ser mais positivo que GO-A).
- `05` só abre com GO-A ≥ condicionado. `06` só recebe estimativa com GO-B ≥ condicionado; sem GO-B, o PB macro existe **sem** tamanho/horas.
- O README de `03-analise-critica/` ganha um bloco por nível (substitui o único BLUF/condições atual) e uma tabela "Status pós-reuniões" por condição.

## 6. Conteúdo de `05` e `06`

### 6.1 `05-arquitetura/` (conceitual)

- **Nível de detalhe:** contexto e contêineres (C4 níveis 1 e 2) mais fluxos principais. Nada de topologia física ou nomes de programa/classe sem fonte.
- **2 a 3 abordagens** com trade-offs explícitos (prós/contras, custo, time-to-market, risco de segurança, curva do time, impacto no negócio) e **uma recomendação** com justificativa. Nunca uma única solução direta.
- **ADRs** curtas para cada decisão que a recomendação assume.
- **`status: hipotese` obrigatório** enquanto houver condição de GO-A ou de GO-C aberta. Cada elemento do diagrama marcado ✅ evidência / 🟡 inferência / ❓ a validar.
- **Rastreabilidade:** cada decisão aponta para as G/C/R/Q que a motivam.
- Entregáveis mínimos (templates em `05-arquitetura/_templates/`): `abordagens.md`, `adr-NNN-<slug>.md`, `diagramas.md` (ou fonte do diagrama), `README.md` (índice + abordagem escolhida).
- A skill `dd-arch-diagrams` já existente deve ser a ferramenta de diagramas; a SPEC só exige que `05` aponte para a fonte do modelo.

### 6.2 `06-backlog/` (PB macro com estimativa)

Item = **requisito macro** (épico-nível), não história.

| Campo | Obrigatório | Descrição |
|---|---|---|
| `ID` | sim | `RF-nnn` ou `RNF-nnn` |
| `Tipo` | sim | FR / NFR (e categoria do NFR: segurança, desempenho, disponibilidade, compatibilidade, operação, rastreabilidade...) |
| `Descrição` | sim | uma frase testável |
| `Origem` | sim | fonte em `00-fontes` ou Q/G que sustenta o requisito |
| `Abordagem` | sim | referência à decisão em `05` que o atende |
| `Tamanho` | com GO-B | S / M / L / XL |
| `Faixa de horas` | com GO-B | `mín – provável – máx` (nunca número único) |
| `Confiança` | com GO-B | Alta / Média / Baixa (regra em §6.3) |
| `Lacunas herdadas` | com GO-B | G/Q abertas que afetam o item |
| `Premissas` | com GO-B | premissas de cenário ideal (§6.4) |
| `Pontos` | opcional | só se existir time e velocidade |

**NFR sem fonte não é omitido.** Entra como `RNF-nnn` com status `lacuna` e aponta para a G-nnn correspondente. O PB macro deve mostrar o que **não** se sabe sobre qualidade.

### 6.3 Protocolo de estimativa

1. **Tamanho primeiro** (S/M/L/XL), em relação a uma âncora declarada. A âncora (um item conhecido, ou histórico) é registrada no topo de `06` com a fonte. Sem âncora → só tamanho relativo, sem horas.
2. **Horas só como faixa**, derivada de uma tabela de calibração por projeto (`06-backlog/calibracao.md`), preenchida pelo arquiteto do discovery (D6): para cada tamanho, `mín – provável – máx` e **a origem da faixa**. Valores de partida devem ser marcados `[preencher]`, nunca inventados no template. Origens aceitas, da mais para a menos forte:
   - **Histórico:** dados de entregas anteriores ingeridos em `00-fontes/historico/` (extração literal, sem edição) e citados por arquivo. Se o histórico não existir para o contexto, a origem não pode ser declarada como histórico.
   - **Experiência do arquiteto:** analogia com times e desafios equivalentes. Registrar qual analogia e quando ocorreu (ex.: "migração de integração em legado, time de 4 pessoas").
   - **Assistida por IA:** a IA propõe a faixa a partir do PB macro, das lacunas e das âncoras. **O arquiteto revisa e assina**; a calibração registra o prompt ou a descrição do método, a data e o que o arquiteto alterou. Estimativa só de IA, sem revisão registrada, não é aceita.
   - O `calibracao.md` mostra a origem **ao lado de cada faixa**, e o `06` herda a origem mais fraca usada em cada item. Origem "assistida por IA" ou "experiência" sem histórico limita a confiança máxima do item a **Média** até a primeira medição real (ex.: após o refinamento ou a primeira entrega).
3. **Confiança ligada às lacunas.** Cada item herda as G/Q abertas que o afetam. Regra inicial (valores a calibrar, baseados no cone de incerteza): sem lacuna aberta → Alta; 1–2 lacunas não bloqueantes → Média; qualquer lacuna bloqueante ou item cujo tamanho depende de algo ainda não lido → Baixa. A faixa alarga com a confiança (multiplicador por classe, declarado em `calibracao.md`).
4. **Totais:** soma dos "provável" como valor central; soma dos "máx" como teto pessimista, rotulado como tal (máximos raramente coincidem, mas a soma deve existir). Não somar tamanhos.
5. **Rótulo obrigatório no topo de `06`:** "Estimativa de discovery, uso interno para planejamento de capacidade; não é compromisso nem preço."
6. **Regra de publicação (D3):** estimativa não sai do kit para terceiros sem decisão explícita do dono do discovery.

### 6.4 Cenário ideal e invalidação

Toda estimativa declara o **cenário-base** (premissas atendidas) e os **gatilhos de invalidação**. Se qualquer gatilho ocorrer, a estimativa muda de status para `invalidada`, deve ser **recalculada** e, se houver compromisso externo, **repactuada**.

Gatilhos mínimos (template em `06-backlog/README.md`): complexidade acima do suposto; mistura de responsabilidades que o desenho separou; ausência de uma etapa de refinamento/leitura de fonte que a estimativa pressupõe; quebra de qualquer premissa listada; mudança de escopo. Cada projeto acrescenta os seus.

`06-backlog/estimativa-status.md` (ou bloco no README) registra: versão da estimativa, data, premissas, gatilhos, status (`vigente`/`invalidada`) e motivo da última mudança.

## 7. Retorno ao fluxo (corrigir `_WIP` como destino final)

### 7.1 Diagnóstico (evidência do uso real)

- Pasta de entendimento com `atualizado:` anterior a uma mudança de escopo ocorrida duas semanas depois.
- Arquivo de riscos com itens criados em um dia e `atualizado:` com a data do dia anterior.
- `05` e `06` vazios após um GO condicionado; todo o desenho em `_WIP/`.
- O fim de ciclo de `_WIP/` (regra 4) foi "adiado" repetidamente, sem nada que o forçasse.

### 7.2 Causas

1. As regras de retorno só cobrem um gatilho: **reunião** (checklist pós-reunião). Não cobrem **decisão do usuário**, **artefato de autoria** (desenho, plano, proposta) nem **mudança de escopo**.
2. Não existe destino para artefatos derivados (arquitetura, proposta, mensagens), então "promover" não tem para onde.
3. Nada verifica `atualizado:` nem a existência do retorno; o hook só injeta contexto.

### 7.3 Mudanças

**a) Gatilhos de retorno (substituir a regra 5 do `CLAUDE.md` por uma regra 5 ampliada).** Qualquer um destes eventos exige atualizar as pastas definitivas **na mesma sessão** (ou registrar pendência explícita):

| Gatilho | Atualizar |
|---|---|
| Reunião/entrevista/DM ingerida | Q-nnn (`04`), G/C/H/R/D (`03`), Log |
| Decisão do dono do discovery | `03` (veredito/condições), `02` se alterar o pedido ou o escopo, Log |
| Mudança de escopo | `02-entendimento` (pedido), `03`, `04` (Q descartadas/novas), Log |
| Artefato de autoria concluído (desenho, plano, proposta) | destino definitivo conforme §7.3b, Log |
| Novo fato de contexto (documento, diagrama, wiki) | `01-contexto`, `_inventario-fontes` |

**b) Tabela de promoção por tipo de artefato** (adicionar a `_WIP/README.md`):

| Artefato em `_WIP/<dia>/` | Destino definitivo | Condição |
|---|---|---|
| `correcao-*` | aplicar na pasta de origem e arquivar/apagar | sempre |
| `pauta-*` | `04-elicitacao/pauta-entrevistas.md` | após a reunião |
| `plano-*` de análise | `03-analise-critica/*` | quando virar decisão |
| arquitetura/diagrama | `05-arquitetura/` com `status: hipotese` | GO-A ≥ condicionado |
| lista de requisitos/estimativa | `06-backlog/` | GO-B ≥ condicionado (estimativa), antes disso só PB sem tamanho |
| `mensagem-*` | permanece em `_WIP` e é descartada após o envio | com confirmação |
| proposta/deck/material comercial | `adaptadores/` (§8) | opcional |

**c) Seção obrigatória "Retornos ao fluxo" em `_WIP/<dia>/_resumo.md`:** tabela `artefato | destino | feito / pendente / justificado`. Item `pendente` sem justificativa por mais de 2 dias vira alerta.

**d) Verificação mecânica `.tools/check_fluxo.py`** (nova). Só heurísticas objetivas; saída em texto, exit code 0 sempre (avisos, não bloqueio):

1. Arquivos de conteúdo cujo `atualizado:` é anterior à data mais recente em que seu ID ou nome aparece em `_WIP/*/_resumo.md` ou no Log do `README.md` raiz.
2. `_WIP/<dia>/` com mais de N dias (padrão 3), arquivos não classificados na tabela "Retornos ao fluxo".
3. Veredito GO-A ≥ condicionado com `05` vazio, ou GO-B ≥ condicionado com `06` sem tamanho.
4. Arquivo de conteúdo sem frontmatter válido (reaproveitar `check_links.py` onde fizer sentido).
5. `status: validado` em arquivo sem nenhuma referência a decisão/fonte de quem tem mandato (aviso, não erro).

**e) Hook `SessionStart`:** além de injetar os guias, executar `check_fluxo.py` e injetar apenas o **resumo de avisos** (máximo 15 linhas). Sem `PreToolUse` (custo de manutenção maior que o benefício, conforme o próprio `_WIP/README.md`).

## 8. Núcleo × adaptadores

- Criar `adaptadores/` na raiz com um `README.md` que explica o contrato: "consome `03` (veredito), `05` e `06`; nunca altera o núcleo; nenhum dado de cliente".
- `adaptadores/proposta/`: esqueleto de proposta técnica/comercial (escopo, fora de escopo, premissas, riscos, abordagem) preenchido a partir do PB macro e do GO. Inclui a instrução de **não** copiar notas internas.
- `adaptadores/deck/`: gerador de apresentação (`.pptx`) a partir do mesmo modelo, com template parametrizável (cores e fontes por perfil). O gerador deve receber o conteúdo por arquivo de dados (YAML/JSON), sem texto de cliente embutido.
- Remover do núcleo qualquer referência a escopo aberto/fechado, preço, modelo comercial e proposta (`GUIA-FLUXO-DISCOVERY.md`, templates de `03` e `04`).
- A "Onda 0" de gates de compliance continua opcional (já documentado no README).

## 9. Backlog de implementação (ordem sugerida)

| # | Tarefa | Arquivos | Saída verificável |
|---|---|---|---|
| T1 | Tabela de mapa de etapas (§4) | `README.md`, `GUIA-FLUXO-DISCOVERY.md`, `05/README.md`, `06/README.md` | tabela idêntica nos 4 lugares |
| T2 | GO em níveis | `03-analise-critica/README.md`, `GUIA-FLUXO-DISCOVERY.md`, `CLAUDE.md` (regra 6) | template com 3 blocos de nível; regra "nível posterior ≤ anterior" |
| T3 | Templates de `05` | `05-arquitetura/README.md`, `_templates/*` | abordagens com trade-offs, ADR, diagramas, `status: hipotese` obrigatório |
| T4 | Templates de `06` + protocolo de estimativa | `06-backlog/README.md`, `calibracao.md`, `estimativa-status.md` | campos §6.2, regras §6.3 e §6.4, rótulo de uso interno |
| T5 | Gatilhos de retorno e tabela de promoção | `CLAUDE.md` (regra 5), `_WIP/README.md` | regra 5 ampliada; tabela §7.3b; seção "Retornos ao fluxo" no modelo de `_resumo.md` |
| T6 | `check_fluxo.py` + hook | `.tools/check_fluxo.py`, `.claude/hooks/session-start.ps1` | roda sobre o scaffold vazio sem erro; roda sobre vault de teste (T9) e reporta os casos plantados |
| T7 | Adaptadores | `adaptadores/**` | README do contrato; esqueleto de proposta; gerador de deck por arquivo de dados |
| T8 | Frontmatter | `_WIP/GUIA-FRONTMATTER.md` | tags `fase/solucao` e `fase/plano` deixam de ser "futuro"; novo `tipo/adr`, `tipo/backlog`, `tipo/estimativa` |
| T9 | Vault de teste (fixture) | `.tools/testdata/` | mini vault sintético com 4 desvios plantados: `atualizado` velho, `_WIP` não classificado, GO sem `05`, NFR sem fonte |
| T10 | README raiz e Log de mudanças do kit | `README.md` | descreve o novo fim do fluxo e o link para esta SPEC |

## 10. Critérios de aceite

1. Um discovery novo, seguindo só os guias do kit, termina com: veredito por nível, `05` conceitual com ≥ 2 abordagens e recomendação, `06` com PB macro (FR e NFR) e, se GO-B ≥ condicionado, estimativa em faixa com confiança e gatilhos de invalidação.
2. Nenhum arquivo do núcleo menciona preço, proposta, escopo aberto/fechado ou modelo comercial.
3. `check_fluxo.py` detecta os 4 desvios do vault de teste (T9) e não gera aviso no scaffold vazio.
4. Existe pelo menos um NFR com status `lacuna` no exemplo de `06`, demonstrando que o PB macro expõe o que não se sabe.
5. `.tools/check_links.py` sem avisos novos em relação à linha de base documentada (~19 no scaffold vazio).
6. Nenhum dado de cliente em qualquer arquivo novo.

## 11. Plano de validação (D4)

- **Teste 1 (obrigatório):** próxima demanda real, de natureza **diferente da que originou esta SPEC** (preferência por greenfield ou produto novo, não migração de legado). A origem foi um único caso atípico; generalizar a partir de n=1 é o risco principal desta SPEC.
- **Teste 2 (retroativo, opcional):** reaplicar o fluxo a uma demanda já encerrada, só para ver se os campos de `06` e a regra de confiança fazem sentido.
- **Pergunta de validação:** o dono do discovery conseguiu chegar ao PB macro sem criar documentos fora do fluxo? Quantos arquivos ficaram em `_WIP` sem destino ao final?

## 12. Riscos e pontos em aberto

| # | Risco / ponto | Mitigação / decisão pendente |
|---|---|---|
| R1 | Generalizar a partir de um caso só | §11 Teste 1 em demanda de natureza diferente |
| R2 | Estimativa vira âncora | rótulo obrigatório, faixa (não número), regra de publicação (D3) |
| R3 | `check_fluxo.py` gerar ruído e ser ignorado | só avisos objetivos, limite de 15 linhas no hook, sem bloqueio |
| R4 | Multiplicadores de confiança sem base | marcados "a calibrar"; ajustar com dados do Teste 1 |
| R5 | Adaptadores crescerem e puxarem o núcleo | contrato do `adaptadores/README.md` (consome, nunca altera) |
| R6 | Estimativa assistida por IA sem âncora vira palpite com aparência de método | D6: revisão do arquiteto registrada, origem visível por faixa, confiança limitada a Média sem histórico |
| ~~P1~~ | Resolvido em D6 (arquiteto calibra; histórico, experiência ou IA, sempre com origem registrada) | — |
| ~~P2~~ | Resolvido em D7 (gerador de deck no kit, em `adaptadores/deck/`) | — |
