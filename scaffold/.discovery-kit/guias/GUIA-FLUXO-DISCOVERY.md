# Guia do Fluxo de Discovery

## BLUF

O discovery é um **loop sequencial com repasse de estado**, não pastas paralelas: hipótese/veredito (`03`) → kit de pergunta (`04`) → reunião real (`00-fontes/reunioes/`) → volta para `03` e `04`. O risco mais caro observado em uso real não é a estrutura de pastas — é esse loop não ser fechado em tempo real logo depois de cada reunião, gerando reconstrução retroativa (vários documentos de análise para fazer o que seriam 2 edições diretas).

## O fluxo

```
00-fontes/           fonte da verdade, não editar (documentos originais + extrações de reunião)
   ↓
01-contexto/         Etapa 0 — wiki extraída (sistemas, termos, processos já existentes)
   ↓
02-entendimento/     Etapa 1 — leitura/resumo dos documentos de entrada originais
   ↓
03-analise-critica/  Etapa 2 — "o que sabemos e qual é o veredito"
   │                 G (lacunas) · C (contradições) · H (hipóteses) · R (riscos) · D (dependências)
   │                 + veredito GO/NO-GO com condições explícitas (README.md da pasta)
   ↓
04-elicitacao/       Etapa 2→3 — "o que falta perguntar, a quem, e como registrar a resposta"
   │                 Q-nnn (perguntas) organizadas por área + ondas de entrevista
   ↓
[reunião acontece] → cai em 00-fontes/reunioes/ (fonte bruta nova)
   ↓
   volta para 03 (atualiza G/C/H com o que a reunião confirmou/conflitou)
   e para 04 (fecha ou qualifica a Q-nnn correspondente)
   ↓
repete até as condições de GO (03-analise-critica/README.md) serem atendidas
   ↓
05-arquitetura/      Etapa 3 — só começa depois do veredito GO
06-backlog/          Etapa 4 — só começa depois de 05
```

## Papel de cada pasta (uma frase cada)

| Pasta | Pergunta que ela responde |
|---|---|
| `00-fontes/` | O que foi dito/escrito, literalmente? |
| `01-contexto/` | O que já existe hoje (sistemas, termos, processos)? |
| `02-entendimento/` | O que os documentos de entrada pedem, resumido e cruzado? |
| `03-analise-critica/` | O que não bate, o que falta, e podemos avançar? |
| `04-elicitacao/` | O que perguntar, a quem, e o que já foi perguntado? |
| `05-arquitetura/` | Como construir, dado que já podemos avançar? |
| `06-backlog/` | O que entregar, em que ordem? |

### Mapa de etapas

| Pasta | Etapa | Saída |
|---|---|---|
| `00-fontes/` | — | fonte da verdade |
| `01-contexto/` | 0 | o que já existe |
| `02-entendimento/` | 1 | o que o pedido diz |
| `03-analise-critica/` | 2 | veredito + condições por nível de GO |
| `04-elicitacao/` | 2→3 | perguntas, ondas, respostas |
| `05-arquitetura/` | 3 | arquitetura conceitual (hipótese) |
| `06-backlog/` | 4 | PB macro (FR/NFR) com estimativa |

**Não fundir `03` e `04`**: uma é retrospectiva (analisa o que já existe), a outra é prospectiva (prepara a próxima coleta). Fundir quebraria a distinção causa → efeito.

## Como trabalhar neste fluxo

### Antes de uma reunião/entrevista
1. Abrir `04-elicitacao/pauta-entrevistas.md`, achar a onda e a conversa.
2. Filtrar em `04-elicitacao/perguntas-por-area.md` as perguntas daquela área, priorizando P0.
3. Ler as G/R/H ligadas (coluna "Por que importa") para entender o motivo da pergunta antes de perguntar.

### Durante
4. Pedir o **artefato** da coluna "Resposta esperada" — resposta verbal sem artefato é 🟡, não fecha a pergunta.
5. Adversarial: é caso geral ou único? Quem é o dono da regra? Onde está escrito?

### Depois — checklist mecânico (ver `04-elicitacao/README.md`)
6. `perguntas-por-area.md`: preencher status/resposta da Q-nnn tocada.
7. `03-analise-critica/` (G/C/H correspondente): atualizar status, evidência, fonte.
8. `README.md` da raiz: uma linha no Log.

**Não criar um documento de análise novo por conversa.** Isso é excepcional — reservado para lotes de reuniões não planejadas ou retroativas. No fluxo normal onda-a-onda, as 2 edições do passo 6–7 bastam.

## Quando o veredito pode mudar

NO-GO → GO condicional só quando as condições de `03-analise-critica/README.md` tiverem artefato (não relato oral). Não é um placar automático de "quantas perguntas respondidas" — uma pergunta P0 "respondida" por 1 pessoa sem autoridade canônica continua contando como não resolvida para efeito de veredito.

## Erro já cometido (não repetir)

Registre aqui, conforme forem acontecendo, erros de processo específicos deste discovery para não repetir — esta é uma seção viva, não conteúdo fixo. Exemplo de entrada real de um projeto anterior: "4 reuniões aconteceram fora da sequência de ondas planejada e ninguém aplicou o checklist pós-conversa em tempo real, gerando múltiplos documentos de reconstrução para recuperar o que o checklist de 3 passos teria feito direto."
