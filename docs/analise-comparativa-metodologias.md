# Discovery Kit vs. Mercado — Análise Comparativa

**Data:** 2026-10-21
**Escopo:** Discovery Kit (este projeto) × BMAD Method × 12 metodologias alternativas
**Critérios:** qualidade do output, eficiência de tokens, cobertura de cenários, maturidade, curva de aprendizado

> **Nota (0.2.0):** esta análise descreve o kit na versão 0.1.0. Desde então o hook virou bash (`session-start.sh`, cross-platform) e os guias passaram para `.discovery/guias/` (`_WIP/README.md` virou `GUIA-WIP.md`). Os trechos abaixo mantêm os nomes antigos como registro da época.

---

## 1. BLUF

**Discovery Kit ocupa um nicho específico e válido — discovery técnico/negócio com veredito GO/NO-GO rastreado por artefato — que nenhum concorrente cobre integralmente.** Ele não compete com BMAD (que é um framework de ciclo completo de desenvolvimento), mas é complementar a ele. BMAD cobre o "depois do GO"; o Discovery Kit cobre o "antes do GO" com um rigor epistemológico (hipótese × validado, artefato × relato oral) que os demais métodos delegam ao julgamento humano.

**A maior fragilidade é o desenho single-practitioner e a injeção incondicional de ~2.450 tokens por sessão.** Nenhum concorrente resolve isso também — é um problema de arquitetura de harness, não de metodologia.

**A maior força é o loop fechado de elicitação com checklist pós-reunião que nasceu de uma falha real documentada**, não de design teórico. Isso é raro.

---

## 2. Posicionamento no Mercado

### 2.1 Mapa conceitual

```
PRÉ-DESCOBERTA          DESCOBERTA / ELICITAÇÃO             PÓS-GO (CONSTRUÇÃO)
(ideia, visão)          (entendimento → análise → GO/NO-GO)  (arquitetura → backlog → código)

Double Diamond ────────►
Wardley Mapping ────────►
                        Discovery Kit ──────────────────────► (para no GO/NO-GO)
                        EventStorming ──────────────────────►
                        Domain Storytelling ────────────────►
                        Impact Mapping ─────────────────────►
                        Example Mapping ────────────────────►
                        Lean Inception ─────────────────────►
                                                             BMAD ──────────────────────► (ciclo completo)
                                                             RUP ────────────────────────► (ciclo completo)
                                                             TOGAF ──────────────────────► (enterprise)
```

**Discovery Kit começa onde a maioria dos métodos ágeis termina** (no entendimento documentado) **e termina onde o BMAD começa** (no GO/NO-GO para arquitetura). Isso não é um defeito — é um escopo deliberado.

### 2.2 O que faz e o que não faz

| Camada | Discovery Kit | BMAD | EventStorming | Lean Inception |
|---|---|---|---|---|
| Análise de documentos-fonte | ✅ Core (00-fontes, 02-entendimento) | ✅ Analyst persona | ❌ | ❌ |
| Catálogo de lacunas/contradições/hipóteses | ✅ IDs próprios (G/C/H/R/D) | ❌ (delega ao PRD) | ✅ Hotspots | ❌ |
| Elicitação estruturada com ondas | ✅ Core (04-elicitacao) | ❌ (não tem onda) | ❌ | ✅ Personas + jornadas |
| Veredito GO/NO-GO com pré-condições | ✅ Central | ✅ Gate entre fases | ❌ | ⚠️ MVP Canvas implícito |
| Rastreabilidade fonte→análise→decisão | ✅ Wikilinks + citações | ✅ Design Spine | ❌ | ❌ |
| Geração de backlog | ❌ (06-backlog é placeholder) | ✅ Story files + Ralph loop | ❌ | ✅ MVP Canvas → backlog |
| Geração de arquitetura | ⚠️ Skill dd-arch-diagrams (pré-GO, hipóteses) | ✅ Architect persona + ADRs | ❌ | ❌ |
| Implementação | ❌ | ✅ Developer + QA + Ralph loop | ❌ | ❌ |

---

## 3. Análise por Cenário

### Cenário 1: Novo produto com Especificação de Software entregue

**Contexto:** Greenfield. Documento de especificação existe, veio do cliente/stakeholder. Time precisa entender, validar e decidir GO/NO-GO.

| Método | Resultado | Tokens | Pontos positivos | Pontos negativos |
|---|---|---|---|---|
| **Discovery Kit** | ⭐⭐⭐⭐⭐ | Médio (2.450 fixos + docs fonte) | Loop 03↔04 fecha gaps da spec em tempo real; veredito com pré-condições declaradas | Overhead se a spec já for madura e não houver contradições |
| **BMAD** | ⭐⭐⭐ | Alto (PRD + arquitetura full) | Transforma spec em PRD executável; bom se o próximo passo for implementar | Fase de Analysis redundante se a spec já existe; a parte de discovery é o elo mais fraco do BMAD |
| **Example Mapping** | ⭐⭐⭐⭐ | Baixo | Converte spec em cenários concretos; barato e rápido; as red cards são as Q-nnn do kit | Só cobre a validação da spec, não cobre contexto, stakeholders, riscos arquiteturais |
| **Impact Mapping** | ⭐⭐⭐ | Baixo | Valida se a spec está alinhada com os goals de negócio; evita construir features sem impacto | Não substitui análise arquitetural nem levantamento de riscos técnicos |
| **TOGAF ADM** | ⭐⭐ | Muito alto | Cobre governança e stakeholders | Desproporcional para um produto novo com spec já entregue |

**Veredito:** Discovery Kit é a melhor opção quando a spec existe mas precisa ser escrutinada antes de avançar. Example Mapping é o complemento ideal para a validação funcional (regras de negócio, cenários de borda).

---

### Cenário 2: Produto brownfield com arquitetura distribuída e Especificação

**Contexto:** Sistema legado multi-serviço. Existe especificação do que se quer construir (nova feature ou modernização). O desafio é entender o legado, validar impacto e decidir.

| Método | Resultado | Tokens | Pontos positivos | Pontos negativos |
|---|---|---|---|---|
| **Discovery Kit** | ⭐⭐⭐ | Médio–Alto (docs fonte + docs legado) | 01-contexto foi desenhado pra isso (wiki local de contexto); C4 via dd-arch-diagrams gera baseline visual do legado | O loop 03↔04 assume ondas de entrevista estruturadas — brownfield muitas vezes exige exploração contínua do código, não entrevistas |
| **BMAD brownfield** | ⭐⭐⭐⭐ | Alto | `*document-project` gera baseline do legado; brownfield templates com regression risk; Test Architect role é relevante | O baseline é gerado por um agente — se o código é confuso, o baseline também será; a parte de discovery do BMAD ainda é o elo fraco |
| **EventStorming + arc42** | ⭐⭐⭐⭐⭐ | Baixo–Médio (workshop humano; AI pós-processa) | EventStorming como knowledge harvesting do legado; arc42 seção 11 captura riscos e dívida técnica; combinação madura e testada | Requer facilitador experiente; não é AI-first — o workshop é humano-dependente |
| **Context Mapping** | ⭐⭐⭐⭐ | Baixo | Desenhado para isso: Anti-Corruption Layer, Conformist, etc. são padrões de integração com legado; produz mapa de dependências entre serviços | Requer DDD literacy; não substitui a descoberta do que construir — complementa |
| **Agentic Discovery (codebase analysis)** | ⭐⭐⭐⭐⭐ | Médio | AI lê o código legado, extrai arquitetura implícita, gera C4/arc42 baseline; mais rápido que qualquer método humano | Risco de alucinação na análise de código; requer verificação humana; prática emergente, não padronizada |

**Veredito:** Discovery Kit sozinho não é a melhor opção para brownfield. A combinação ideal é **Agentic Discovery (baseline do legado via AI) → Discovery Kit (loop de elicitação + veredito)** ou **EventStorming + Context Mapping + arc42** se houver facilitador experiente disponível.

---

### Cenário 3: Grande plataforma (backend + frontend + mobile), TI consolidada, sem especificação

**Contexto:** Cliente enterprise com departamento de TI maduro, práticas estruturadas. A demanda existe mas não há spec — precisa descobrir o que construir, validar com stakeholders e então propor arquitetura.

| Método | Resultado | Tokens | Pontos positivos | Pontos negativos |
|---|---|---|---|---|
| **Discovery Kit** | ⭐⭐⭐⭐ | Médio–Alto | Brilha aqui: a estrutura de ondas de elicitação + Q-nnn + veredito GO/NO-GO foi feita para este cenário; TI consolidada = stakeholders disponíveis para entrevistas | Assume single-practitioner — TI consolidada tem múltiplos arquitetos, conflito de edição no vault |
| **BMAD Full Stack** | ⭐⭐⭐⭐ | Alto | Cobre a cadeia completa: Analysis (descobrir) → PRD → Arquitetura → Story files; as personas são o "time virtual" | Overhead da fase de Analysis é redundante com o discovery; TI consolidada já tem PM — o BMAD PM agent compete com o PM real |
| **Lean Inception** | ⭐⭐⭐⭐ | Baixo (workshop de 1 semana) | Time-boxed; produz MVP Canvas + backlog; TI consolidada se beneficia da estrutura de workshop | Produz backlog, não análise arquitetural; não cobre stakeholders técnicos (infra, segurança, operações) |
| **Double Diamond + C4** | ⭐⭐⭐ | Médio | Diamond 1 (Discover + Define) captura a descoberta; C4 estrutura os achados técnicos | Diamond é pesado em UX, leve em arquitetura; TI consolidada tem preocupações de infra/segurança que o Double Diamond não cobre |
| **RUP Elaboration** | ⭐⭐ | Muito alto | Cobre tudo — requisitos + arquitetura + riscos + plano | Sobrecarga de documentação; TI consolidada já tem processos, o RUP competiria com eles em vez de complementar |
| **Discovery Kit + BMAD (combinados)** | ⭐⭐⭐⭐⭐ | Alto (mas com separação de fases) | O Kit cobre o discovery até GO; BMAD assume do GO em diante (arquitetura → backlog → implementação); complementaridade natural | Custo de contexto de dois frameworks; requer disciplina para a transição no ponto GO/NO-GO |

**Veredito:** **Discovery Kit + BMAD combinados** é a combinação de maior cobertura. O Kit cobre o "descobrir o que construir" (o gap deste cenário); BMAD cobre o "construir o que foi decidido" (onde a TI consolidada já tem capacidade, mas se beneficia da estruturação).

---

### Cenário 4: Produto greenfield em fase de ideação (empreendedores/investidores)

**Contexto:** Ideia inicial, empreendedores ainda levantando o conceito e validando o mercado. Domínio B2C ou B2B ainda não mapeado — pode ser um marketplace, uma plataforma de conexão entre dois lados, um SaaS vertical. Zero documentação formal, zero time técnico, zero usuários. O que existe são hipóteses dos fundadores sobre o problema e o mercado.

| Método | Resultado | Tokens | Pontos positivos | Pontos negativos |
|---|---|---|---|---|
| **Discovery Kit** | ⭐⭐ | Médio | Poderia estruturar o que se sabe e o que não se sabe | **Não foi feito para isso.** O Kit pressupõe stakeholders reais, documentos-fonte e uma decisão GO/NO-GO iminente. Na fase de ideia, não há stakeholders com autoridade canônica — há visionários com hipóteses |
| **BMAD Phase 1 (Analysis)** | ⭐⭐⭐⭐ | Médio | Analyst persona + PRFAQs + Opportunity summaries; feito para explorar o problema antes de comprometer recursos | As personas (Mary, John) são proxies — não substituem conversas reais com o mercado |
| **Double Diamond** | ⭐⭐⭐⭐⭐ | Baixo (workshops leves) | Diamond 1 é literalmente "Discover + Define"; pesquisa com usuários, "How Might We", reframing do problema; empreendedores entendem essa linguagem | Não gera backlog de produto; precisa ser complementado |
| **Wardley Mapping** | ⭐⭐⭐⭐ | Baixo | Mapeia o ecossistema do negócio: players existentes, commoditizáveis, diferenciais; revela onde construir vs. integrar vs. comprar | Não gera backlog nem spec; é uma ferramenta de estratégia, não de discovery tático |
| **Impact Mapping + Lean Inception** | ⭐⭐⭐⭐⭐ | Baixo | Impact Map conecta funcionalidades a outcomes de negócio; Lean Inception entrega MVP Canvas em 1 semana; ritmo certo para empreendedores | Não cobre arquitetura — mas na fase de ideia, arquitetura é prematura |
| **BMAD Quick Flow** | ⭐⭐⭐ | Baixo | Caminho leve do BMAD; Technical Spec → implementação direta para validar hipótese | Bom para protótipo, não para estruturar a descoberta do produto |

**Veredito:** Discovery Kit **não é adequado** para este cenário. Ele pressupõe maturidade de discovery que uma ideia em fase de concepção não tem. A combinação ideal: **Double Diamond (explorar o problema) → Wardley Mapping (entender o ecossistema) → Impact Mapping + Lean Inception (definir MVP)**. O Discovery Kit entra no ciclo seguinte, quando a ideia tiver virado uma demanda com stakeholders reais. Um guia detalhado para este cenário está em `docs/discovery-ideia-greenfield.md`.

---

### Cenários adicionais

#### Cenário 5: Modernização de legacy crítico (mainframe → cloud)

| Método | Resultado | Por quê |
|---|---|---|
| **Agentic Discovery + arc42** | ⭐⭐⭐⭐⭐ | AI analisa o código legado; arc42 seções 9-11 capturam decisões, qualidade e dívida técnica; TOGAF ADM governa a transição |
| **Discovery Kit** | ⭐⭐ | Não foi desenhado para código legado como fonte primária; 01-contexto cobre documentação, não codebase |
| **BMAD brownfield** | ⭐⭐⭐⭐ | `*document-project` + brownfield templates; mas a qualidade depende da clareza do código legado |

#### Cenário 6: Compliance-driven (regulatório manda, não negocia)

| Método | Resultado | Por quê |
|---|---|---|
| **Discovery Kit** | ⭐⭐⭐⭐ | "Onda 0" foi desenhada para gates regulatórios; rastreabilidade Q-nnn → evidência → veredito é trilha de auditoria natural |
| **TOGAF + Example Mapping** | ⭐⭐⭐⭐⭐ | TOGAF governa; Example Mapping valida regras de negócio regulatórias como cenários Gherkin |
| **BMAD** | ⭐⭐⭐ | Approval gates são estruturais, mas a documentação regulatória não é especializada |

#### Cenário 7: Startup com time de 3 devs, sem PM/BA/QA dedicados

| Método | Resultado | Por quê |
|---|---|---|
| **BMAD Quick Flow** | ⭐⭐⭐⭐⭐ | Sem overhead de PRD completo; Technical Spec → código rápido |
| **Example Mapping + ADRs** | ⭐⭐⭐⭐ | Leve, mantém decisões rastreáveis sem processo pesado |
| **Discovery Kit** | ⭐ | Overkill: ondas de elicitação, frontmatter, WIP lifecycle, veredito GO/NO-GO — para 3 devs na mesma sala, isso é cerimônia desnecessária |

---

## 4. Comparação Direta: Discovery Kit × BMAD

### 4.1 Tabela comparativa

| Dimensão | Discovery Kit | BMAD Method |
|---|---|---|
| **Escopo** | Discovery técnico/negócio até GO/NO-GO | Ciclo completo: análise → planejamento → arquitetura → implementação |
| **Origem** | Extraído de 1 projeto real (BeR), genericizado | Framework comunitário, múltiplas iterações (V4→V6→V7 alpha) |
| **Maturidade** | V0 (extraído em 2026-10-02, primeiro commit hoje) | V6.12 estável, V7 em preview; comunidade ativa no GitHub |
| **Paradigma** | Vault + Claude Code como motor de raciocínio | Personas de agentes especializados + artifact chain |
| **Público-alvo** | Arquiteto de soluções como practitioner único | Times de desenvolvimento usando AI como acelerador |
| **Gate principal** | GO/NO-GO com pré-condições declaradas, baseado em artefato | Approval gates entre fases (PRD, arquitetura), com revisão humana |
| **Tratamento de incerteza** | IDs explícitos (G-nnn, C-nn, H-nnn) + status epistemológico (hipotese/validado) | Delega ao PRD e à fase de Analysis; sem taxonomia de incerteza |
| **Rastreabilidade** | Wikilinks + citações numeradas + ADRs com IDs do vault | Design Spine + artifact chain sequencial |
| **Arquitetura** | dd-arch-diagrams (C4 + Structurizr DSL, pré-GO, hipóteses) | Architect persona "Winston" + ADRs (pós-PRD, especificação) |
| **Implementação** | Não cobre | Developer + QA + Scrum Master + Ralph loop autônomo |
| **Multi-agente** | Não (single session) | Sim (12+ personas, orquestração, party mode) |
| **Token efficiency** | ~2.450 fixos/sessão (hook incondicional) + docs on-demand | Variável por track: Quick Flow (baixo), Enterprise (alto); document sharding reduz custo |
| **Brownfield** | Suporte implícito (01-contexto como wiki local) | Explícito (`*document-project`, templates dedicados) |
| **Multi-practitioner** | ❌ (single-session, sem merge) | ⚠️ Parcial (artifacts em Markdown versionado, mas personas são single-agent) |
| **Cross-platform** | ❌ Windows-only (.ps1 hook) | ✅ Node.js (npx), cross-platform |
| **Licença** | Proprietária (não declarada) | MIT (open source) |

### 4.2 Onde o Discovery Kit é melhor

1. **Rigor epistemológico:** A distinção `hipotese` × `validado` com a pergunta adversarial ("alguém com mandato confirmou, ou só parece estável porque ninguém contestou?") é mais sofisticada que qualquer mecanismo equivalente no BMAD. BMAD delega julgamento de confiança ao revisor humano; o Kit torna isso estrutural.

2. **Discovery puro:** BMAD trata discovery como preliminar à construção — sua fase de Analysis é o elo conceitualmente mais fraco do framework. O Discovery Kit é 100% focado nisso, com taxonomia de lacunas/contradições/hipóteses/riscos/dependências que o BMAD não tem.

3. **Custo de entrada:** Discovery Kit é uma pasta. BMAD requer `npx bmad-method install`, Node.js 20.12+, aprendizado de 12+ personas e todo o artifact chain. Para um arquiteto fazendo discovery sozinho, o Kit é dramaticamente mais leve.

4. **Honestidade operacional:** O GUIA-FLUXO-DISCOVERY.md documenta a falha real que o processo foi desenhado para prevenir. BMAD descreve o happy path.

### 4.3 Onde o BMAD é melhor

1. **Cobertura de ciclo completo:** BMAD não para no GO/NO-GO. Quem faz discovery com o Kit e decide GO ainda precisa de um método para executar — e o BMAD é o complemento natural.

2. **Maturidade e comunidade:** V6.12 com múltiplas iterações, comunidade ativa, módulos oficiais, MIT license. O Kit tem 1 dia de git.

3. **Orquestração multi-agente:** Party mode, Ralph loop, handoff chain. O Kit é single-session — se você quiser revisão adversarial, precisa fazer manualmente.

4. **Escalabilidade de time:** BMAD foi desenhado para times (personas = papéis). O Kit foi desenhado para um arquiteto operando o vault.

5. **Cross-platform:** Node.js roda em qualquer lugar. O hook `.ps1` do Kit é Windows-only.

### 4.4 Complementaridade

A arquitetura ideal para um projeto completo:

```
Discovery Kit                    BMAD Method
├── 00-fontes/                   │
├── 01-contexto/                 │
├── 02-entendimento/             │
├── 03-analise-critica/          │
│   ├── G-nnn (lacunas)          │
│   ├── C-nn (contradições)      │
│   ├── H-nnn (hipóteses)        │
│   ├── R-nnn (riscos)           │
│   └── D-nnn (dependências)     │
├── 04-elicitacao/               │
│   ├── Q-nnn (perguntas)        │
│   └── ondas de entrevista      │
│                                ├── Phase 2: Planning (PRD)
│                                ├── Phase 3: Solutioning
│                                │   ├── Architect "Winston"
│                                │   └── ADRs
│                                ├── Phase 4: Implementation
│                                │   ├── Story files
│                                │   ├── Scrum Master
│                                │   └── Ralph loop
│                                └── QA / Test Architect
└── GO/NO-GO ───────────────────► (transição natural)
```

---

## 5. Eficiência de Tokens — Comparação Quantitativa

| Método | Custo fixo por sessão | Custo variável (docs) | Mecanismo de contenção |
|---|---|---|---|
| Discovery Kit | ~2.450 tokens | Fontes + análises | Nenhum (injeção incondicional) |
| BMAD Quick Flow | ~500 tokens | Technical spec | Track selection (menos fases = menos docs) |
| BMAD Standard | ~1.500-2.500 tokens | PRD + arquitetura | Document sharding; agentes com escopo restrito |
| BMAD Enterprise | ~3.000-5.000 tokens | Full stack + módulos | Sharding + fan-out + Ralph loop (agentes cold-start) |
| Example Mapping | ~200 tokens | Gherkin scenarios | Muito leve; sessões curtas e focadas |
| Agentic Discovery Pipeline | ~1.000-2.000 tokens | Codebase + docs | Fan-out + tiered models (Haiku→Sonnet→Opus) + RAG |
| EventStorming + C4 | 0 tokens (workshop humano) | Event timeline + C4 DSL | AI entra só no pós-processamento |

**Conclusão:** Discovery Kit tem o pior perfil de custo fixo entre os métodos comparáveis. A correção é simples: split do hook em "sempre injetar" (loop + checklist) e "sob demanda" (WIP lifecycle, frontmatter schema). Isso reduziria o baseline em ~40-50%.

---

## 6. Recomendações para o Discovery Kit

### 6.1 Correções imediatas (alta prioridade)

1. **Hook cross-platform:** Adicionar bash equivalente ao `.ps1` ou um runner Python. Windows-only é inaceitável para um scaffold que se apresenta como portável.

2. **Split de injeção de contexto:** Separar os 3 guias em tiers:
   - **Tier 1 (sempre):** GUIA-FLUXO-DISCOVERY.md (o loop é relevante para toda interação)
   - **Tier 2 (on-demand):** GUIA-FRONTMATTER.md (só ao criar arquivos), _WIP/README.md (só em operações de gestão do dia)

3. **Declarar licença:** MIT ou Apache 2.0. Sem licença explícita, ninguém adota.

4. **Documentar limitações de escopo:** O README deve dizer explicitamente "este kit cobre discovery até GO/NO-GO; para implementação, considere BMAD ou similar."

### 6.2 Evoluções estruturais (média prioridade)

5. **Suporte multi-practitioner:** Modelo de conflito/merge para vault compartilhado (git-based, Obsidian Sync, ou convenção de branches por pessoa).

6. **PreToolUse hook para 00-fontes/:** Bloquear edição acidental da pasta de fontes com hook mecânico — a regra 6 do CLAUDE.md é declarativa demais.

7. **Guia de integração com BMAD:** Documentar a transição Discovery Kit → BMAD no ponto GO/NO-GO. Isso posiciona o Kit como "fase 0 do BMAD" e resolve a limitação de escopo.

8. **Frontmatter linter:** Script Python que valida frontmatter obrigatório em arquivos de conteúdo — similar ao `check_links.py` existente.

### 6.3 Diferenciais estratégicos (longo prazo)

9. **Catálogo de perguntas padrão por domínio:** Um conjunto de Q-nnn canônicas para domínios comuns (e-commerce, seguros, banking, saúde) — acelera o bootstrap de novos discoveries.

10. **Modo brownfield dedicado:** `*document-project` style — agente que lê código legado e popula automaticamente `01-contexto/` com baseline de arquitetura existente.

---

## 7. Matriz de Decisão por Cenário

| Cenário | Melhor método | Segundo melhor | Discovery Kit adequado? |
|---|---|---|---|
| Novo produto com spec | Discovery Kit + Example Mapping | BMAD (pular Analysis) | ✅ Ideal |
| Brownfield com spec | EventStorming + arc42 + Context Mapping | Agentic Discovery + Discovery Kit | ⚠️ Parcial (complementar) |
| Grande plataforma sem spec | Discovery Kit → BMAD (combinados) | Lean Inception + C4 | ✅ Ideal |
| Ideia greenfield sem spec (empreendedores) | Double Diamond + Wardley + Lean Inception | BMAD Phase 1 (Analysis) | ❌ Prematuro — ver docs/discovery-ideia-greenfield.md |
| Modernização legacy crítico | Agentic Discovery + arc42 + TOGAF | BMAD brownfield | ❌ Não cobre |
| Compliance-driven | Discovery Kit + TOGAF + Example Mapping | BMAD Enterprise | ✅ Ideal |
| Startup 3 devs | BMAD Quick Flow | Example Mapping + ADRs | ❌ Overkill |
| Discovery multi-arquiteto | EventStorming + C4 + ADRs | BMAD (party mode) | ❌ Single-practitioner |

---

## 8. Conclusão

**Discovery Kit é o método mais focado em discovery puro com rigor epistemológico — e também o menos maduro, mais restrito em plataforma e mais caro em tokens fixos por sessão.** Estas quatro afirmações são simultaneamente verdadeiras e definem o roadmap.

Ele não compete com BMAD — compete com a **ausência de método**. Seu adversário real é o discovery ad-hoc: arquiteto lendo documento, anotando num caderno, fazendo pergunta em reunião sem registrar resposta, perdendo o fio entre uma semana e outra. Contra esse adversário, mesmo com os gaps identificados, o Discovery Kit é uma melhoria radical.

A pergunta estratégica não é "Discovery Kit ou BMAD?" — é **"Discovery Kit como fase 0 do BMAD?"**. Essa integração, se documentada e suportada, posicionaria o Kit como o elo de discovery que o ecossistema BMAD atualmente não tem, e daria ao BMAD a profundidade de elicitação que sua fase de Analysis não entrega.