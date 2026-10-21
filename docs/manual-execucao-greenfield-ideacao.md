# Manual de Execução — Discovery Greenfield na Fase de Ideação

**Data:** 2026-10-21
**Para:** Empreendedores, product managers, arquitetos atuando na fase pré-product/market fit
**Pré-requisitos:** Nenhum — este manual assume zero documentação, zero time, zero usuários
**Antes de começar:** Preencha [`briefing-projeto-template.md`](briefing-projeto-template.md) com o que você já sabe sobre o produto. Para iniciar a sessão no Claude Code, use o [`prompt-abertura-sessao.md`](prompt-abertura-sessao.md).

---

## BLUF

Este manual descreve **exatamente o que fazer, em que ordem, com quem, por quanto tempo e produzindo quais artefatos** para conduzir discovery em um produto greenfield que ainda está na fase de ideia. São 5 semanas de trabalho. Ao final, você terá um Problem Statement validado, um ecossistema mapeado e um MVP Canvas pronto para execução.

---

## Semana 1 — Preparação e Hipóteses

### Dia 1 (2-3h)

**Objetivo:** Externalizar tudo que os empreendedores acreditam sobre o negócio.

**Atividade:** Sessão de 2-3h com os fundadores/empreendedores.

**Roteiro:**

1. Peça para cada pessoa escrever em post-its (5 min cada):
   - "Qual problema este produto resolve?"
   - "Para quem?"
   - "Como essas pessoas resolvem esse problema hoje?"
   - "Por que ninguém resolveu isso ainda?"
   - "O que faria este produto ser 10x melhor que as alternativas?"

2. Agrupe os post-its por tema e identifique:
   - **Convergências** (onde todos concordam — são as hipóteses mais fortes)
   - **Divergências** (onde discordam — são as hipóteses mais arriscadas, precisam de validação urgente)
   - **Vazios** (temas que ninguém mencionou — distribuição, monetização, regulação, etc.)

3. Documente no arquivo `hipoteses-iniciais.md`:

```markdown
# Hipóteses Iniciais

## Hipótese de Problema
[Uma frase: "Pessoas do grupo X têm o problema Y quando tentam Z"]

## Hipótese de Solução
[Uma frase: "Um produto que faça A, B e C resolve Y porque..."]

## Hipótese de Mercado
- Tamanho estimado: [N] pessoas/empresas
- Disposição a pagar: [R$ X] por [mês/uso]
- Canal de aquisição esperado: [W]

## Hipótese de Segmentos
### Segmento 1: [nome]
- Descrição: [1 parágrafo]
- Problema específico: [1 frase]
- Como resolve hoje: [1 frase]

### Segmento 2: [nome]
- ...

## Divergências não resolvidas
- [Tópico]: [Fundador A] acredita X, [Fundador B] acredita Y
```

**Artefato:** `hipoteses-iniciais.md`

---

### Dia 2 (2h)

**Objetivo:** Preparar o roteiro de entrevista.

**Atividade:** Transformar hipóteses em perguntas de entrevista.

**Regra de ouro:** NUNCA pergunte "você usaria...". SEMPRE pergunte sobre comportamento passado.

**Estrutura do roteiro (45 min de entrevista):**

```
ABERTURA (5 min)
- "Conte-me sobre você e seu [contexto relevante]"
- "Como é seu dia a dia em relação a [domínio do problema]?"

COMPORTAMENTO ATUAL (15 min)
- "Conte-me a última vez que você enfrentou [situação relacionada ao problema]"
- "O que você fez? Passo a passo."
- "O que foi mais frustrante nesse processo?"
- "Quanto tempo levou? Quanto custou?"

TENTATIVAS ANTERIORES (10 min)
- "Já tentou alguma ferramenta, app, método para resolver isso?"
- "O que funcionou? O que não funcionou?"
- "Por que parou de usar?"

REAÇÃO À IDEIA (10 min) — só aqui, no final
- "Se existisse algo que fizesse [descrição neutra, sem mencionar solução], como isso mudaria sua rotina?"
- "O que seria indispensável nessa solução para você considerar usar?"
- "O que faria você NÃO usar, mesmo que fosse de graça?"

FECHAMENTO (5 min)
- "Tem mais alguém que você acha que eu deveria entrevistar?"
- "Posso te procurar de novo se surgirem mais dúvidas?"
```

**Artefato:** `roteiro-entrevista.md`

---

### Dia 3-5 (6-8h total)

**Objetivo:** Recrutar 10-24 entrevistados.

**Canais de recrutamento:**

1. **Comunidades online** (mais eficaz):
   - Subreddits, grupos de Facebook, servidores Discord do domínio
   - Mensagem padrão: "Estou pesquisando como [pessoas do segmento] resolvem [problema]. 30 min de conversa, sem vender nada. Quer participar?"
   - Taxa de resposta típica: 5-10%

2. **Indicações** (mais qualificado):
   - Peça para cada empreendedor listar 5 pessoas que conhece no segmento
   - Peça indicação no final de cada entrevista ("tem mais alguém?")

3. **Eventos e meetups** (presencial ou online):
   - Vá onde o segmento está, não onde você está

4. **Cold outreach (LinkedIn/Twitter)** (menos eficaz, mas escala):
   - Personalize cada mensagem
   - Taxa de resposta típica: 2-5%

**Meta mínima:** 5-8 entrevistados por segmento (2 segmentos = 10-16 entrevistas).

**Ferramentas:**
- Calendly ou similar para agendamento
- Google Meet/Zoom com gravação (peça consentimento)
- Planilha de tracking: nome, segmento, status (convidado/agendado/entrevistado/agradecido)

**Artefato:** `tracking-entrevistas.csv`

---

## Semana 2 — Entrevistas (Discover)

### Todos os dias

**Objetivo:** Conduzir 2-4 entrevistas por dia e fazer debrief imediato.

**Logística:**
- Máximo de 4 entrevistas por dia (depois disso, fadiga cognitiva)
- Intervalo mínimo de 30 min entre entrevistas
- Dois participantes por entrevista: um entrevistador + um observador/síndico

**Durante a entrevista:**

- **Entrevistador:** conduz o roteiro, mantém conversa natural, explora tangentes relevantes
- **Observador:** anota frases literais, padrões, surpresas, linguagem corporal. NÃO interrompe. Anota em `notas/[segmento]-[data]-[id].md`

**Após cada entrevista (10 min de debrief):**

Preencha imediatamente:

```markdown
# Debrief — Entrevista [ID]

**Data:** YYYY-MM-DD
**Segmento:** [nome]
**Duração:** [min]

## O que confirmou hipóteses
- [Hipótese X]: "entrevistado disse Y"

## O que surpreendeu
- [Achado inesperado]

## O que contradisse hipóteses
- [Hipótese Z]: "entrevistado disse W — oposto do esperado"

## Frases literais importantes
- "[citação exata]"

## Intensidade do problema (1-5)
- Nota: [1-5]
- Evidência: "entrevistado [ação/métrica objetiva]"
```

**Artefatos diários:** `notas/[segmento]-[data]-[id].md` + entrada no debrief

---

## Semana 3 — Síntese (Define)

### Dia 1 (4h) — Transcrição e Agrupamento

1. Releia todas as notas de debrief
2. Extraia todas as frases literais para um documento único
3. Agrupe por tema (use Miro, post-its físicos ou um Markdown com headings)

### Dia 2 (3h) — Problem Statement

Com base nos agrupamentos, escreva:

```markdown
# Problem Validation Report

## Sumário executivo
- Total de entrevistas: [N]
- Segmentos entrevistados: [lista]
- Problema central confirmado: [1 frase]
- Intensidade média do problema: [X]/5
- Hipóteses confirmadas: [N]/[total]
- Hipóteses refutadas: [N]/[total]
- Hipóteses não testadas: [N]/[total]

## Hipóteses originais vs. evidência

| Hipótese | Tipo | Evidência | Veredito |
|---|---|---|---|
| [texto] | Problema | 7/8 entrevistados relataram | ✅ Confirmada |
| [texto] | Solução | 0/8 mencionaram espontaneamente | ❌ Refutada |
| [texto] | Mercado | Amostra insuficiente | ⚠️ Incerta |

## Problem Statement final
[Segmento] precisa de [necessidade] porque [insight das entrevistas].
Evidência: [N]/[total] entrevistados relataram [comportamento/frustração específica].

## O que NÃO é o problema
- Não é X, porque [evidência]
- Não é Y, porque [evidência]

## Segmentos validados
### Segmento 1: [nome]
- Tamanho na amostra: [N] entrevistados
- Padrão de comportamento: [descrição]
- Gatilho do problema: [quando/situação]
- Intensidade: [X]/5

### Segmento 2: [nome]
- ...

## Segmentos hipotéticos NÃO encontrados
### Segmento X:
- Procuramos em [canais], encontramos [N] pessoas
- [N] não se identificaram com o problema
- Veredito: segmento provavelmente não existe como imaginado

## How Might We questions (priorizadas)
1. HMW [ação] para [segmento] de forma que [resultado]? (intensidade: 4.5/5, frequência: 8/8)
2. HMW ...
```

### Dia 3 (2h) — Personas

```markdown
# Persona: [Nome]

**Fonte:** baseada em [N] entrevistas com [segmento]
**Não é:** projeção dos empreendedores

## Demografia
- Idade: [faixa real dos entrevistados]
- Localização: [regiões reais]
- Ocupação: [ocupações reais]

## Comportamento observado
- [Comportamento 1]: [frequência nos entrevistados]
- [Comportamento 2]: ...

## Frases literais
- "[citação 1]"
- "[citação 2]"

## Objetivos (derivados do comportamento, não perguntados)
- [Objetivo 1]
- [Objetivo 2]

## Frustrações (derivadas do comportamento, não perguntadas)
- [Frustração 1] — relatada por [N]/[total]

## Momento de uso
- Quando: [situação/gatilho]
- Onde: [contexto físico/digital]
- Com que frequência: [diário/semanal/mensal]

## Barreiras
- O que impede de resolver o problema hoje: [barreira principal]
```

**Artefatos de saída:** `problem-validation-report.md`, `personas.md`, `hmw-questions.md`

---

## Semana 4 — Ecossistema (Wardley Mapping)

### Dia 1 (4h) — Construção do Mapa

**Ferramenta:** Miro, draw.io, ou https://onlinewardleymaps.com

**Passo a passo:**

1. **Listar componentes (30 min):**
   Em post-its ou cards, liste TUDO que o produto precisa para funcionar — do que o usuário vê até a infraestrutura. Inclua práticas, dados, conhecimento, hardware, software, APIs, pessoas. Não julgue ainda — quantidade sobre qualidade.

2. **Posicionar no eixo Y — Cadeia de Valor (30 min):**
   - Topo: componentes visíveis ao usuário (interface, features, jornadas)
   - Meio: serviços de negócio, lógica de domínio, dados
   - Base: infraestrutura, plataforma, utilities
   - Regra: um componente depende dos que estão abaixo dele

3. **Posicionar no eixo X — Evolução (60 min):**
   Para cada componente, pergunte: "quão maduro/commoditizado é isso no mercado?"

   | Estágio | Característica | Exemplo |
   |---|---|---|
   | Genesis | Experimental, incerto, ninguém fez antes | Algoritmo proprietário de matching |
   | Custom | Sob medida, poucos fornecedores, caro | Integração com sistema legado específico |
   | Product | Existem produtos concorrentes, feature-driven | CRM vertical, busca facetada |
   | Commodity | Barato, padronizado, substituível | CDN, auth, email, pagamentos |

4. **Identificar movimentos (60 min):**
   - Setas para a direita: componentes evoluindo (Custom → Product, Product → Commodity)
   - Círculos: componentes com inércia (não evoluem mesmo com pressão de mercado)
   - Anote o que está acontecendo no mercado que acelera ou freia cada movimento

5. **Anotar decisões (60 min):**
   - Verde (construir): Genesis e Custom — diferencial competitivo
   - Amarelo (integrar): Product — use APIs/SaaS
   - Vermelho (comprar): Commodity — use serviços padrão

### Dia 2 (2h) — Documentação

```markdown
# Análise de Ecossistema

## Mapa
[imagem do Wardley Map]

## Decisões Build vs. Buy vs. Integrate

| Componente | Estágio | Decisão | Fornecedor/API | Custo estimado/mês | Risco |
|---|---|---|---|---|---|
| CDN de vídeo | Commodity | Comprar | CloudFront | $50-200 | Baixo |
| Busca full-text | Product | Integrar | Algolia/Meilisearch | $0-100 | Baixo |
| Motor de recomendação | Genesis | Construir | — | Equipe | Alto (core) |
| Autenticação | Commodity | Comprar | Auth0/Firebase Auth | $0-50 | Baixo |

## Análise Competitiva

| Player | Estágio | Forças | Fraquezas | O que fazem que é Commodity (custo desnecessário) |
|---|---|---|---|---|
| Concorrente A | Product | Base de usuários | Feature bloat | Mantêm auth própria (custo que não gera diferencial) |
| Concorrente B | Genesis | Tecnologia superior | Sem tração | — |

## Oportunidades de Movimento
- [Componente X] está migrando de Custom para Product — oportunidade de ser first-mover
- [Componente Y] é tratado como Custom pelo concorrente A, mas já existe como Product — vantagem de custo para nós
```

**Artefatos de saída:** `wardley-map.png`, `build-vs-buy.md`, `ecosystem-analysis.md`

---

## Semana 5 — MVP (Impact Mapping + Lean Inception)

Esta é a semana mais intensa. Idealmente, reserve 5 dias consecutivos com os empreendedores e quaisquer especialistas convidados (um eventual tech lead, um eventual designer).

### Dia 1 (4h) — Visão e Impact Map

**Participantes:** Empreendedores + facilitador

**Agenda:**

1. **Visão do Produto (30 min):**
   Preencher em conjunto:
   ```
   PARA [segmento primário]
   QUE [necessidade principal]
   O [nome do produto] É UM [categoria]
   QUE [diferencial principal]
   DIFERENTE DE [alternativa atual]
   NOSSO PRODUTO [característica distintiva]
   ```

2. **Goal Definition (30 min):**
   - "Em 6 meses, o que precisa ser verdade para considerarmos este produto um sucesso?"
   - Converter em métrica: "X usuários ativos", "Y% retenção D30", "Z conversões"
   - **O goal precisa ser mensurável e ter prazo**

3. **Actor Identification (30 min):**
   - Listar quem pode ajudar ou atrapalhar o goal
   - Usar as personas validadas do Estágio 1 como base
   - Adicionar atores secundários: pagantes, reguladores, parceiros

4. **Impact Mapping (90 min):**
   - Para cada ator: "que comportamento novo geraria impacto no goal?"
   - Para cada impacto: "que funcionalidade produziria esse comportamento?"
   - **Corte impiedoso:** funcionalidade sem chain → goal = fora

5. **Documentar o Impact Map:**
   - Visualmente (Miro, draw.io) ou textualmente:
   ```markdown
   ## Goal: [métrica + prazo]
   ### Ator: [nome]
   #### Impacto: [comportamento desejado]
   ##### Deliverable: [funcionalidade]
   ##### Deliverable: [funcionalidade]
   #### Impacto: [outro comportamento]
   ...
   ```

### Dia 2 (4h) — Personas e Jornadas

**Participantes:** Empreendedores + facilitador (+ designer, se houver)

1. **Apresentar personas validadas (30 min):**
   - Mostrar as personas do Estágio 1
   - Deixar o time adicionar nuances
   - Se alguém contestar: "que evidência você tem disso?" — se não tiver, prevalece a evidência das entrevistas

2. **Jornada As-Is (90 min):**
   - Como o usuário resolve o problema HOJE
   - Passo a passo, sem pular etapas
   - Anotar emoções em cada etapa: frustração, ansiedade, indiferença, satisfação
   - Identificar o "momento de maior frustração" — é aí que o produto precisa entregar mais valor

3. **Jornada To-Be com MVP (90 min):**
   - Como o usuário resolveria com o MVP proposto
   - Passo a passo usando as features priorizadas no Impact Map
   - Anotar emoções esperadas
   - Identificar riscos: "se a feature X não funcionar como esperado, o usuário abandona aqui"

### Dia 3 (4h) — Brainstorming de Features

**Participantes:** Empreendedores + facilitador + qualquer pessoa que vá construir o produto

1. **Brainstorming (60 min):**
   - Cada pessoa escreve features em silêncio (10 min)
   - Leitura em voz alta e agrupamento por afinidade (30 min)
   - Sem debate, sem crítica — todas as ideias são válidas

2. **Vinculação ao Impact Map (60 min):**
   - Cada feature precisa responder: "que impacto gera? Para qual ator? Contribui para o goal?"
   - Features órfãs (sem chain) → parking lot
   - Features duplicadas → consolidar

3. **Primeira triagem (60 min):**
   - Remover features que são claramente V3+ ou "nice to have"
   - Identificar features que precisam de spike técnico para estimar esforço

### Dia 4 (4h) — Sequenciador

**Participantes:** Empreendedores + tech lead (essencial neste dia)

**Agenda:**

1. **Estimar esforço (60 min):**
   - Cada feature: Baixo (dias), Médio (1-2 semanas), Alto (3+ semanas)
   - Se não houver tech lead, use triangulação: 3 pessoas estimam independentemente e discutem divergências > 1 nível

2. **Estimar impacto (60 min):**
   - Cada feature: Baixo (nice to have), Médio (contribui), Alto (crítico para o goal)
   - Use o Impact Map como referência — se a feature está conectada a um impacto de alto valor, o impacto é alto

3. **Estimar incerteza (30 min):**
   - Baixa: já fizemos antes, tecnologia conhecida
   - Média: já fizemos similar, mas contexto diferente
   - Alta: novo para nós, depende de fator externo, usuário pode rejeitar

4. **Classificar no sequenciador (30 min):**

   | Esforço | Impacto | Incerteza | Destino |
   |---|---|---|---|
   | Baixo | Alto | Baixa | ✅ MVP |
   | Baixo/Médio | Alto | Média | ✅ MVP (com spike) |
   | Médio | Alto | Alta | ⚠️ V2 (validar incerteza primeiro) |
   | Alto | Alto | Baixa | ⚠️ V2 (esforço alto) |
   | Baixo | Baixo | Baixa | 🅿️ Parking lot |
   | Alto | Baixo | * | ❌ Não fazer |

### Dia 5 (4h) — MVP Canvas

**Participantes:** Empreendedores + facilitador + decisores finais

**Agenda:**

1. **Preencher o MVP Canvas (90 min):**

```markdown
# MVP Canvas

## Proposta do MVP
[1 frase: o que será entregue]

## Personas priorizadas
- [Persona primária]
- [Persona secundária, se couber no MVP]

## Jornadas cobertas
- [Jornada 1]: ponta a ponta, do [início] ao [fim]
- [Jornada 2]: se couber

## Features do MVP

| Feature | Esforço | Prazo estimado | Dependências |
|---|---|---|---|
| [Feature 1] | Baixo | 3 dias | Nenhuma |
| [Feature 2] | Médio | 2 semanas | Feature 1 |
| ... | | | |

## Métricas de Sucesso
- Primária: [métrica que define se o MVP funcionou]
- Secundárias: [métricas de saúde — retenção, engajamento, NPS]
- Threshold de GO/NO-GO: "se [métrica primária] < [X] em [Y] semanas, pivotar"

## Custo e Cronograma
- Equipe necessária: [N] pessoas, [perfis]
- Tempo estimado: [N] semanas
- Custo estimado: R$ [X] (equipe + infra + ferramentas)

## Hipóteses a Validar
1. [Hipótese de problema]: "acreditamos que [segmento] tem [problema]"
   - Como validar: [métrica ou evidência]
2. [Hipótese de solução]: "acreditamos que [feature] resolve [problema]"
   - Como validar: [métrica ou evidência]
3. [Hipótese de crescimento]: "acreditamos que [canal] traz [N] usuários"
   - Como validar: [métrica ou evidência]

## Não Escopo (e por que)
- [Feature X]: impacto alto mas esforço proibitivo para MVP (V2)
- [Feature Y]: incerteza alta — precisa de validação antes de construir (V2)
- [Feature Z]: nice to have, não conectado ao goal (parking lot)
```

2. **Revisão e compromisso (60 min):**
   - Cada pessoa lê o canvas em silêncio (15 min)
   - Discussão: "o que te preocupa neste MVP?"
   - Ajustes finais
   - Compromisso explícito: "todos concordam que este é o MVP?"

3. **Próximos passos (30 min):**
   - Quem vai construir? (contratar, outsourcing, founders?)
   - Quando começa?
   - Primeira milestone de validação: data + métrica
   - Agenda de revisão: semanal? quinzenal?

**Artefatos de saída:** `impact-map.png`, `mvp-canvas.md`, `backlog-mvp.md`, `hipoteses-nao-validadas.md`

---

## Pós-Semana 5 — Transição

Com o MVP construído e em uso:

1. **Coleta de feedback vira `00-fontes/`:**
   - Analytics do MVP (eventos, funis, retenção)
   - Entrevistas de feedback com early adopters
   - Tickets de suporte/bugs

2. **Discovery Kit assume:**
   - `01-contexto/`: Wardley Map e Ecosystem Analysis já existem
   - `02-entendimento/`: Problem Validation Report e MVP Canvas
   - `03-analise-critica/`: G/C/H/R/D sobre expandir para V1
   - `04-elicitacao/`: Q-nnn para os early adopters (stakeholders reais)
   - GO/NO-GO para V1 com pré-condições mensuráveis

---

## Templates de Arquivos

### `hipoteses-iniciais.md`
Ver seção Semana 1, Dia 1.

### `roteiro-entrevista.md`
Ver seção Semana 1, Dia 2.

### `notas/[segmento]-[data]-[id].md` (debrief)
Ver seção Semana 2, após cada entrevista.

### `problem-validation-report.md`
Ver seção Semana 3, Dia 2.

### `personas.md`
Ver seção Semana 3, Dia 3.

### `ecosystem-analysis.md`
Ver seção Semana 4, Dia 2.

### `mvp-canvas.md`
Ver seção Semana 5, Dia 5.

---

## Ferramentas Recomendadas

| Atividade | Ferramenta | Custo |
|---|---|---|
| Agendamento de entrevistas | Calendly | Free tier suficiente |
| Videoconferência + gravação | Google Meet, Zoom | Free |
| Notas colaborativas | Google Docs, Notion | Free |
| Mapa visual (Wardley, Impact) | Miro, draw.io | Free tier |
| Wardley Map online | https://onlinewardleymaps.com | Free |
| Tracking de entrevistados | Google Sheets | Free |
| MVP Canvas | Qualquer editor Markdown | Free |

---

## Estimativa de Tempo Total

| Atividade | Horas |
|---|---|
| Semana 1 — Preparação | 8-12h |
| Semana 2 — Entrevistas (10-16) | 15-20h (incluindo debrief) |
| Semana 3 — Síntese | 8-10h |
| Semana 4 — Wardley Mapping | 6-8h |
| Semana 5 — Lean Inception | 20h (5 dias × 4h) |
| **Total** | **57-70h em 5 semanas** |

---

## Checklist Final

- [ ] Entrevistou pelo menos 5 pessoas por segmento?
- [ ] Pelo menos 60% dos entrevistados relataram o mesmo problema central?
- [ ] O Problem Statement é baseado em frases literais dos entrevistados?
- [ ] As personas têm dados demográficos e comportamentais reais?
- [ ] O Wardley Map identificou pelo menos 3 commodities que não precisam ser construídas?
- [ ] Cada feature do MVP tem chain até o goal no Impact Map?
- [ ] Features órfãs foram removidas do MVP?
- [ ] O MVP Canvas tem hipóteses de negócio explícitas na seção "a validar"?
- [ ] O MVP cobre pelo menos uma jornada completa ponta a ponta?
- [ ] Há métricas de sucesso com threshold de GO/NO-GO?
- [ ] O "não escopo" está documentado com justificativa?
- [ ] Todos os empreendedores concordaram explicitamente com o MVP?
- [ ] Existe data para a primeira revisão de métricas pós-lançamento?