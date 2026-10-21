# Discovery em Produto Greenfield na Fase de Ideação

**Data:** 2026-10-21
**Escopo:** Como conduzir discovery técnico/de-negócio quando o produto ainda é uma ideia — sem stakeholders, sem documentação, sem time, sem usuários
**Método:** Double Diamond → Wardley Mapping → Impact Mapping + Lean Inception

---

## 1. BLUF

**Discovery Kit e BMAD pressupõem maturidade de discovery que uma ideia em fase de concepção não tem.** Ambos assumem stakeholders com autoridade canônica, documentos-fonte, e uma decisão GO/NO-GO iminente. Na fase de ideação, o problema é o oposto: validar se o problema existe, entender quem são os usuários reais, e mapear o ecossistema antes de decidir o que construir.

**A jornada recomendada tem 3 estágios, usando métodos complementares que cobrem o que o Discovery Kit e o BMAD não cobrem.** O Discovery Kit entra no ciclo seguinte, quando a ideia tiver virado uma demanda validada com stakeholders reais.

---

## 2. Por que os métodos tradicionais falham neste cenário

### 2.1 Discovery Kit

O Kit tem três pré-condições estruturais que a fase de ideia não atende:

| Pré-condição do Kit | Realidade da fase de ideia |
|---|---|
| Stakeholders com autoridade canônica (regra 6 do CLAUDE.md: "resposta de 1 pessoa sem autoridade canônica não fecha uma Q-nnn") | Não há autoridade canônica — há visionários com hipóteses sobre o mercado, não conhecimento validado |
| Fontes documentais como ponto de partida (`00-fontes/` como "fonte da verdade, não editar") | Não há PRD, EDS, ata de reunião com cliente, spec de integração. O que existe são anotações de brainstorming e talvez uma pesquisa preliminar |
| Veredito GO/NO-GO binário com pré-condições declaradas | A decisão não é binária — é iterativa: "essa hipótese sobrevive a 20 entrevistas? Se não, pivotamos para o quê?" |

### 2.2 BMAD Method

BMAD Phase 1 (Analysis) é o mais próximo do que se precisa, mas:

- As personas (Mary - Business Analyst, John - Product Manager) geram **proxies sintéticos de pesquisa de mercado**, não pesquisa real com usuários
- O output esperado é um Product Brief e PRFAQs — documentos internos de alinhamento, não validação externa
- A fase de Analysis foi desenhada para "problem definition is unclear", mas ainda dentro de um contexto onde já existe um projeto — não para ideação pré-projeto

### 2.3 Métodos ágeis tradicionais (Scrum, Story Mapping)

- User Story Mapping pressupõe que você sabe **quem** são os usuários e **o que** eles precisam — na fase de ideia, ambos são hipóteses
- Scrum pressupõe um Product Owner com visão clara — aqui, os empreendedores estão construindo essa visão

---

## 3. A Jornada em 3 Estágios

```
SEMANA 1-3           SEMANA 4           SEMANA 5           APÓS MVP
Double Diamond       Wardley Mapping     Lean Inception     Discovery Kit
──────────►          ──────────►         ──────────►        ──────────►
Descobrir  Definir   Mapear              MVP + Backlog      GO/NO-GO
problema   problema  ecossistema         + Hipóteses        para v1
```

---

## 4. Estágio 1 — Double Diamond (Semanas 1-3)

### Objetivo

Sair da ideia ("vamos construir X para Y") para um **Problem Statement validado** baseado em evidência real de usuários, não em intuição dos empreendedores.

### O método

Double Diamond (British Design Council, 2004) organiza a descoberta em dois momentos de divergência e convergência:

```
DIVERGIR              CONVERGIR             DIVERGIR              CONVERGIR
(Discover)            (Define)              (Develop)             (Deliver)
────────────►         ──────────►           ────────────►         ──────────►
Pesquisa com          Síntese dos           Ideação de            Seleção do
usuários reais        achados em            soluções para         conceito
Entrevistas           Problem Statement     o problema            a prototipar
Observação            "How Might We"        validado
Análise de mercado    Personas reais
```

Nesta fase, usamos apenas a **primeira metade (Discover + Define)**. A segunda metade (Develop + Deliver) é coberta pelo Lean Inception no Estágio 3.

### Como executar

#### Semana 1 — Preparação

1. **Definir as hipóteses centrais do negócio** — o que os empreendedores *acreditam* que é verdade:
   - Hipótese de problema: "pessoas do grupo X têm o problema Y"
   - Hipótese de solução: "um produto que faça Z resolve Y"
   - Hipótese de mercado: "existem N pessoas dispostas a pagar por isso"
   - Hipótese de adoção: "elas chegariam ao produto via canal W"

2. **Mapear os segmentos de usuário hipotéticos:**
   - Quem são os potenciais usuários? (2-3 segmentos no máximo)
   - Quem são os potenciais pagantes? (pode ser diferente dos usuários)
   - Quem são os influenciadores? (quem não usa mas decide)

3. **Preparar o roteiro de entrevista:**
   - **NUNCA** pergunte "você usaria um app que faz X?" — isso produz falsos positivos
   - Pergunte sobre **comportamento atual**: "como você resolve o problema Y hoje?"
   - Pergunte sobre **última ocorrência**: "conte-me a última vez que você enfrentou Y — o que fez?"
   - Pergunte sobre **tentativas anteriores**: "já tentou alguma ferramenta ou método para resolver Y? O que aconteceu?"

4. **Recrutar 5-8 entrevistados por segmento** (total 10-24 entrevistas):
   - Fontes: redes sociais, comunidades online, indicações, eventos do setor
   - Incentivo: acesso antecipado ao produto, gift card, ou simplesmente "ajudar a construir algo melhor"
   - Perfil: diversidade dentro do segmento (idade, região, nível de experiência)

#### Semana 2 — Discover (divergir)

5. **Conduzir as entrevistas** (30-45 min cada):
   - Gravar (com consentimento) para revisão posterior
   - Um entrevistador + um observador (os dois empreendedores, idealmente)
   - O observador anota padrões, surpresas, frases literais
   - Após cada entrevista: 10 min de debrief (o que confirmou, o que surpreendeu, o que contradisse hipóteses anteriores)

6. **Observar o contexto real de uso** (opcional, mas transformador):
   - Se o produto resolve um problema do dia a dia, observe alguém tentando resolver esse problema hoje
   - Anote: ferramentas usadas, passos manuais, workarounds, momentos de frustração

7. **Analisar o mercado existente:**
   - Quem são os competidores diretos? (mesmo problema, mesma solução)
   - Quem são os competidores indiretos? (mesmo problema, solução diferente)
   - Quem são os substitutos? (o que as pessoas usam hoje que não é um "produto" — planilha, grupo de WhatsApp, caderno)

#### Semana 3 — Define (convergir)

8. **Sintetizar os achados em um Problem Statement:**
   - Formato: "[Segmento] precisa de [necessidade] porque [insight]"
   - Deve ser específico: "jovens profissionais precisam de uma forma de encontrar mentores na sua área porque indicações informais favorecem quem já tem rede de contatos"
   - Valide: o problema aparece em pelo menos 60% das entrevistas? As pessoas sentem esse problema com intensidade (não é "seria legal resolver", é "isso me frustra regularmente")?

9. **Criar personas baseadas em dados reais, não em hipóteses:**
   - Dados demográficos reais dos entrevistados
   - Comportamentos observados (não perguntados)
   - Frases literais (a linguagem real dos usuários)
   - Objetivos e frustrações derivados das entrevistas
   - **Importante:** se dois segmentos hipotéticos colapsaram em um (comportamentos indistinguíveis), una-os. Se um segmento hipotético não apareceu nas entrevistas, marque como "não validado"

10. **Gerar "How Might We" questions:**
    - Derivadas diretamente dos insights das entrevistas
    - Formato: "Como poderíamos [ação] para [segmento] de forma que [resultado desejado]?"
    - Priorizar por: frequência do problema nas entrevistas × intensidade da frustração

11. **Produzir o Problem Validation Report:**
    - Hipóteses originais dos empreendedores
    - O que foi confirmado (com evidência: "7/8 entrevistados relataram X")
    - O que foi refutado (com evidência: "0/8 entrevistados mencionaram Y espontaneamente")
    - O que permanece incerto (amostra pequena, segmento não alcançado)
    - Problem Statement final + personas + HMW questions

**Artefatos de saída do Estágio 1:**
- `problem-validation-report.md` — o documento completo
- `personas.md` — 1 ficha por persona validada
- `hmw-questions.md` — priorizadas por evidência
- `entrevistas/` — notas e gravações (com consentimento)

---

## 5. Estágio 2 — Wardley Mapping (Semana 4)

### Objetivo

Mapear o ecossistema do negócio para decidir **onde construir vs. onde integrar vs. onde comprar**, antes de gastar um centavo em desenvolvimento.

### O método

Wardley Mapping (Simon Wardley, ~2005) posiciona componentes em duas dimensões:
- **Eixo Y (Cadeia de Valor):** do usuário (topo) à infraestrutura (base)
- **Eixo X (Evolução):** Genesis → Custom → Product/Rental → Commodity/Utility

A pergunta central: **este componente é diferencial competitivo ou commodity que deveria ser comprada?**

### Como executar

1. **Listar todos os componentes necessários para o produto funcionar:**
   - Comece pelo topo: o que o usuário final vê e usa?
   - Desça: o que é necessário para entregar isso?
   - Inclua: práticas, dados, conhecimento, hardware, software, APIs, pessoas

2. **Posicionar cada componente no eixo de evolução:**
   - **Genesis:** ninguém fez antes, incerto, experimental, caro
   - **Custom:** feito sob medida, poucos fornecedores, conhecimento especializado
   - **Product/Rental:** existem produtos concorrentes, feature-driven, pago por uso
   - **Commodity/Utility:** barato, padronizado, substituível (ex.: CDN, email, auth)

3. **Para cada componente, decidir:**
   - **Genesis/Custom → Construir:** é aqui que está o diferencial competitivo
   - **Product → Integrar:** use APIs/SaaS existentes, não recrie
   - **Commodity → Comprar:** use serviços padrão de mercado

4. **Identificar movimentos no mapa:**
   - O que está evoluindo de Custom para Product? (oportunidade de ser o primeiro)
   - O que está em Product mas os concorrentes tratam como Custom? (ineficiência deles = vantagem sua)
   - O que os concorrentes estabelecidos tratam como diferencial mas já é Commodity? (custo desnecessário que você evita)

5. **Documentar decisões estratégicas:**
   - Componentes "build" → justificativa de diferencial competitivo
   - Componentes "integrate" → qual API/SaaS, qual o custo, qual o risco de vendor lock-in
   - Componentes "buy" → qual provedor, custo mensal estimado

**Artefatos de saída do Estágio 2:**
- `wardley-map.png` — o mapa visual (use draw.io, Miro, ou onlinewardleymaps.com)
- `build-vs-buy.md` — tabela de decisão por componente
- `ecosystem-analysis.md` — análise de players existentes, movimentos, inércias

---

## 6. Estágio 3 — Impact Mapping + Lean Inception (Semana 5)

### Objetivo

Com o problema validado e o ecossistema mapeado, **definir o MVP** — o mínimo que entrega valor e testa as hipóteses de negócio remanescentes.

### Por que combinar Impact Mapping + Lean Inception

- **Impact Mapping** (Gojko Adzic, 2012) garante que **cada feature do backlog esteja conectada a um outcome de negócio** — evita construir coisas que não geram impacto
- **Lean Inception** (Paulo Caroli, 2018) estrutura a semana de workshop que produz o **MVP Canvas**
- Juntos, eles respondem: "o que entra no MVP?" com critérios de negócio, não com opinião

### Como executar

#### Dia 1 — Visão do Produto e Impact Map

1. **Definir o Goal (objetivo de negócio mensurável):**
   - Formato: "Alcançar [métrica] até [data]"
   - Exemplo: "Alcançar 500 usuários ativos com perfil completo em 6 meses"
   - Deve ser SMART: específico, mensurável, atingível, relevante, temporal

2. **Listar os Actors (quem pode ajudar ou atrapalhar o goal):**
   - Atores primários: usuários finais (use as personas do Estágio 1)
   - Atores secundários: pagantes, influenciadores, reguladores
   - Para cada ator: "como eles ajudam o goal?" e "como eles atrapalham?"

3. **Definir Impacts (mudanças de comportamento necessárias):**
   - Para cada ator: "que comportamento precisa mudar para atingir o goal?"
   - Impactos devem ser observáveis: "criar perfil em <15 min" não "gostar do produto"

4. **Propor Deliverables (funcionalidades que geram os impacts):**
   - Para cada impacto: "o que podemos construir que produz esse impacto?"
   - Um deliverable só existe se estiver conectado a um impacto → um impacto → um ator → o goal
   - **Corte impiedosamente** deliverables sem chain até o goal (são gold-plating)

#### Dia 2 — Personas e Jornadas

5. **Refinar personas com o time:**
   - Apresentar as personas do Estágio 1
   - O time (empreendedores + eventuais especialistas convidados) adiciona nuance
   - Se houver stakeholders novos na sala, validar ou refutar com eles

6. **Mapear jornadas dos atores principais:**
   - Jornada "as-is" (como resolvem hoje, com base nas entrevistas)
   - Jornada "to-be" (como resolveriam com o produto)
   - Identificar momentos de frustração, delight e abandono

#### Dia 3 — Brainstorming de Funcionalidades

7. **Gerar features sem censura:**
   - Cada pessoa escreve features em post-its (físico ou Miro)
   - Sem debate, sem crítica — quantidade sobre qualidade
   - Agrupar por afinidade

8. **Vincular cada feature ao Impact Map:**
   - Cada feature deve responder: "que impacto isso gera? Para qual ator? Contribui para o goal?"
   - Features sem chain clara vão para o "parking lot"

#### Dia 4 — Sequenciador

9. **Avaliar cada feature em 4 dimensões:**
   - **Esforço:** quanto tempo/esforço técnico? (Baixo/Médio/Alto)
   - **Impacto no goal:** quanto aproxima do objetivo? (Baixo/Médio/Alto)
   - **Incerteza:** quanto confiamos nessa estimativa? (Baixa/Média/Alta)
   - **Dependência:** depende de outra feature? Qual?

10. **Classificar features no sequenciador:**
    - **MVP:** baixo esforço, alto impacto, baixa incerteza → FAZER AGORA
    - **V2:** médio/alto esforço, alto impacto, média incerteza → PRÓXIMO
    - **V3+:** alto esforço, baixo impacto, alta incerteza → NÃO FAZER ou REAVALIAR DEPOIS

#### Dia 5 — MVP Canvas

11. **Preencher o MVP Canvas:**

```
┌─────────────────────────────────────────────────────────┐
│ MVP CANVAS                                              │
├─────────────────────────┬───────────────────────────────┤
│ NOME DO MVP:            │ DATA:                         │
├─────────────────────────┼───────────────────────────────┤
│ PROPOSTA DO MVP         │ PERSONAS                      │
│ (o que será entregue,   │ (para quem, segmentos         │
│  em uma frase)          │  priorizados)                 │
├─────────────────────────┼───────────────────────────────┤
│ JORNADAS                │ FEATURES (MVP)                │
│ (quais jornadas o MVP   │ (funcionalidades que entram   │
│  cobre, ponta a ponta)  │  no MVP, priorizadas)         │
├─────────────────────────┼───────────────────────────────┤
│ MÉTRICAS DE SUCESSO     │ CUSTO E CRONOGRAMA            │
│ (como saber se o MVP    │ (estimativa de esforço,       │
│  funcionou)             │  timeline, equipe necessária) │
├─────────────────────────┴───────────────────────────────┤
│ HIPÓTESES DE NEGÓCIO A VALIDAR                          │
│ (o que precisa ser verdade para o MVP funcionar)        │
├─────────────────────────────────────────────────────────┤
│ NÃO ESCOPO (o que NÃO entra no MVP — e por que)         │
└─────────────────────────────────────────────────────────┘
```

**Artefatos de saída do Estágio 3:**
- `impact-map.png` — o mapa completo (goal → atores → impactos → deliverables)
- `mvp-canvas.md` — canvas preenchido e validado pelos empreendedores
- `backlog-mvp.md` — backlog priorizado do MVP
- `hipoteses-nao-validadas.md` — hipóteses que o MVP precisa testar

---

## 7. O Que Vem Depois: Transição para o Discovery Kit

O MVP foi construído, lançado, e os primeiros usuários estão usando. Agora:

1. **Stakeholders reais existem** — os early adopters são fontes canônicas de feedback
2. **Fontes documentais existem** — analytics do MVP, entrevistas de feedback, tickets de suporte = material para `00-fontes/`
3. **A decisão é genuinamente GO/NO-GO** — "expandir para a versão completa?" é uma decisão de investimento real com pré-condições verificáveis
4. **As perguntas são respondíveis** — não mais "existe mercado?" mas "a feature X do MVP está sendo usada como esperado?"

Neste ponto, **o Discovery Kit opera sobre dados reais**, não sobre hipóteses dos empreendedores:

```
Feedback do MVP ──► 00-fontes/ (analytics, entrevistas, tickets)
                         │
                         ▼
                    01-contexto/ (ecossistema já mapeado no Wardley)
                         │
                         ▼
                    02-entendimento/ (o que o MVP ensinou)
                         │
                         ▼
                    03-analise-critica/ (G/C/H/R/D sobre expandir)
                         │
                         ▼
                    04-elicitacao/ (Q-nnn para stakeholders reais)
                         │
                         ▼
                    GO/NO-GO para V1 ──► BMAD (implementação)
```

E, se desejado, o BMAD assume daí em diante com a cadeia completa: PRD → Arquitetura → Story Files → Ralph Loop → QA.

---

## 8. Resumo de Artefatos por Estágio

| Estágio | Semana | Artefatos | Método principal |
|---|---|---|---|
| 1. Descobrir o problema | 1-3 | Problem Validation Report, Personas, HMW Questions, Notas de entrevista | Double Diamond (Discover + Define) |
| 2. Mapear o ecossistema | 4 | Wardley Map, Build-vs-Buy, Ecosystem Analysis | Wardley Mapping |
| 3. Definir o MVP | 5 | Impact Map, MVP Canvas, Backlog MVP, Hipóteses a validar | Impact Mapping + Lean Inception |
| Pós-MVP | 6+ | Discovery Kit completo → BMAD | Discovery Kit → BMAD |

---

## 9. Armadilhas Comuns

### 9.1 Pular o Double Diamond e ir direto pro código

**Sintoma:** "já sabemos o que construir, vamos validar com MVP."
**Realidade:** se você não entrevistou 10+ usuários, não sabe. O MVP valida solução, não problema. Construir a solução errada é mais caro que 3 semanas de entrevistas.

### 9.2 Tratar personas hipotéticas como reais

**Sintoma:** personas criadas em workshop interno, sem entrevistas.
**Realidade:** personas de workshop refletem o viés dos empreendedores, não o mercado. Se a persona "Maria" nunca foi entrevistada, "Maria" é uma hipótese — trate como tal.

### 9.3 Pular Wardley Mapping e construir tudo

**Sintoma:** "vamos construir a plataforma completa: auth, CDN, busca, notificações, analytics..."
**Realidade:** auth é commodity (Auth0), CDN é commodity (CloudFront), notificações são commodity (OneSignal). Construir commodities queima tempo e dinheiro que deveriam ir para o diferencial competitivo.

### 9.4 Confundir Lean Inception com waterfall disfarçado

**Sintoma:** tratar o MVP Canvas como especificação final e imutável.
**Realidade:** o MVP Canvas é uma **hipótese documentada**. A primeira semana de uso real vai invalidar partes dele — isso é sucesso, não fracasso. O Canvas serve para ter uma baseline contra a qual comparar o aprendizado real.

### 9.5 Entrar no Discovery Kit cedo demais

**Sintoma:** "vamos estruturar o discovery com Q-nnn e frontmatter."
**Realidade:** se não há stakeholders com autoridade canônica, as Q-nnn não têm resposta — você está organizando o vácuo. O Kit pressupõe que existem pessoas que sabem as respostas; na fase de ideia, ninguém sabe.

---

## 10. Checklist de Saúde do Processo

- [ ] Entrevistou pelo menos 10 pessoas de 2+ segmentos?
- [ ] Pelo menos 60% dos entrevistados relataram o mesmo problema central?
- [ ] O Problem Statement é baseado em frases literais dos entrevistados?
- [ ] As personas têm dados reais (não são projeções dos empreendedores)?
- [ ] O Wardley Map identificou pelo menos 3 commodities que não precisam ser construídas?
- [ ] Cada feature do MVP tem chain até o goal no Impact Map?
- [ ] Features sem chain até o goal foram removidas ou movidas para o parking lot?
- [ ] O MVP Canvas tem hipóteses de negócio explícitas na seção "a validar"?
- [ ] O MVP cobre pelo menos uma jornada completa ponta a ponta?
- [ ] Há métricas de sucesso definidas (não "usuários gostarem", mas "taxa de retenção D7 > 40%")?
- [ ] O "não escopo" do MVP está documentado com justificativa?

---

## 11. Referências

- **Double Diamond:** British Design Council (2004). https://www.designcouncil.org.uk/our-resources/the-double-diamond/
- **Wardley Mapping:** Simon Wardley. https://learnwardleymapping.com/ — livro gratuito e comunidade
- **Impact Mapping:** Gojko Adzic, *Impact Mapping* (Provoking Thoughts, 2012). https://www.impactmapping.org/
- **Lean Inception:** Paulo Caroli, *Lean Inception* (Caroli.org, 2018). https://www.caroli.org/lean-inception/
- **Discovery Kit:** https://github.com/judaemanuel/discovery-kit — usar após o MVP, quando houver stakeholders reais
- **BMAD Method:** https://bmadcode.com — usar na fase de implementação pós-GO