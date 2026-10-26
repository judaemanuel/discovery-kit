# Observações da implementação da SPEC v2

Pontos fora do escopo ou desvios de ordem registrados durante a implementação. Não alteram a SPEC.

| # | Observação | Tarefa | Decisão |
|---|---|---|---|
| O1 | T8 executada antes da T3: os templates de `05` e `06` usam `tipo/adr`, `tipo/backlog` e `tipo/estimativa`, que o `dk.py validar` rejeitava até a T8 entrar em `TIPOS`. Sem a inversão, a T3 geraria erro de validação. | T3/T8 | Ordem efetiva: T1, T2, T8, T3, T4, T5, T6, T9, T7, T10 |
| O2 | A regra de confiança da §6.3 depende de a lacuna ser "bloqueante", mas G-nnn não tem esse atributo formal no kit. | T4 | Registrar "bloqueante" como coluna no template de itens do PB e citar a regra; formalizar o atributo em G-nnn fica para o dono do kit |
| O3 | `tipo/analise` é usado para `abordagens.md` e `diagramas.md` de `05`, porque a SPEC (T8) não cria tipo próprio para eles. | T3 | Usar `tipo/analise`; revisar se o uso real pedir tipo próprio |
