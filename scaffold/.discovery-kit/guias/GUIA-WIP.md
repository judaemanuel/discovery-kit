# Guia de Trabalho — `_WIP/`

**Origem:** convenção adotada para separar trabalho em andamento, ordenado por dia, do conteúdo definitivo do vault.
**Status:** modelo manual-assistido — valide por uso real antes de considerar estável.

## BLUF

`_WIP/` existe para separar **trabalho em andamento, ordenado por dia**, do conteúdo definitivo do vault (`00-fontes/` a `06-backlog/`) e do descartável (`_temp/`, se você usar uma pasta assim). Cada dia tem sua própria pasta; ao final do ciclo, cada arquivo é promovido para a estrutura definitiva, mantido como ativo, ou deletado — nunca duplicado indefinidamente.

## Estrutura

```
_WIP/
├── 2026-01-01/            # pasta do dia (formato YYYY-MM-DD) — exemplo ilustrativo
│   ├── plano-exemplo.md
│   ├── pauta-1-exemplo.md
│   └── mensagem-exemplo.md
└── 2026-01-02/
```

## Ciclo de vida de um dia

1. **Início do dia** — criar pasta `YYYY-MM-DD/` nova. Se útil, pedir um resumo do que ficou pendente do dia anterior antes de começar (não é automático — peça explicitamente, ex.: "resume o que ficou aberto de ontem").
2. **Durante o dia** — todo material novo (pautas, rascunhos, mensagens, prompts de apoio) vai direto na pasta do dia corrente. Não editar pastas de dias anteriores.
3. **Fim do dia / ao resolver algo** — cada arquivo recebe uma de três decisões, nunca fica "pendurado":
   - ✅ **Resolvido** → mover para a estrutura definitiva (`00-fontes/`, `02-entendimento/`, `03-analise-critica/`, `04-elicitacao/`, etc.) e apagar da `_WIP/`.
   - 🔄 **Ainda ativo** → permanece na pasta do dia; se o dia virar, decidir se migra para a pasta nova ou se continua referenciado por link.
   - 🗑️ **Obsoleto** → apagar.
4. **Pastas antigas** — sem nada ativo e sem conteúdo migrado após ~3 dias → pasta inteira pode ser deletada. Isso só deve ser feito mediante confirmação explícita (apagar é destrutivo).
5. **Resumo do dia** → sempre em `_WIP/<data>/_resumo.md`, nunca no `README.md` raiz do vault. O `README.md` raiz leva só 1 linha concisa no Log por marco, apontando para o resumo detalhado.

## Convenções de nome observadas (manter)

| Padrão | Uso |
|---|---|
| `pauta-N-<quem>.md` | roteiro de reunião, numerado na ordem em que ocorrem |
| `plano-*.md` | plano de ação/atualização do dia |
| `correcao-*.md` | correções pontuais (ex.: transcrição) |
| `mensagem-*.md` | rascunho de mensagem a enviar a stakeholder |
| `_resumo.md` | resumo do dia, dentro da pasta do dia |
| `temp-prompt.txt` | prompt de apoio descartável, não é artefato de conteúdo |

Não inventar categorias novas sem necessidade — se o conteúdo não se encaixa em nenhum padrão acima, nomear descritivamente e decidir destino ao final do dia.

## Promoção: de `_WIP/` para a pasta definitiva

Material em `_WIP/<dia>/` não é destino final. Ao concluir um artefato, promova conforme o tipo:

| Artefato em `_WIP/<dia>/` | Destino definitivo | Condição |
|---|---|---|
| `correcao-*` | aplicar na pasta de origem e arquivar/apagar | sempre |
| `pauta-*` | `04-elicitacao/pauta-entrevistas.md` | após a reunião |
| `plano-*` de análise | `03-analise-critica/*` | quando virar decisão |
| arquitetura/diagrama | `05-arquitetura/` com `status: hipotese` | GO-A ≥ condicionado |
| lista de requisitos/estimativa | `06-backlog/` | GO-B ≥ condicionado (estimativa); antes disso, só PB sem tamanho |
| `mensagem-*` | permanece em `_WIP` e é descartada após o envio | com confirmação |
| material de apresentação para terceiros (deck, documento externo) | `adaptadores/` | opcional |

## Modelo do `_resumo.md`

Todo `_WIP/<dia>/_resumo.md` termina com a seção **"Retornos ao fluxo"**:

```markdown
## Retornos ao fluxo

| artefato | destino | situação |
|---|---|---|
| [preencher: arquivo em _WIP] | [preencher: pasta definitiva] | feito / pendente / justificado |
```

`pendente` sem justificativa por mais de 2 dias vira alerta no `check_fluxo.py`. `justificado` exige o motivo na própria linha (por exemplo, "aguarda transcript").

## O que é manual vs. o que é automático

Os guias são carregados a cada sessão por `@import` no `CLAUDE.md` (sem hook, portável entre SOs). Para bloqueio de ação (não só injeção de contexto), hooks `PreToolUse` são o mecanismo correto — mas valem o custo de manutenção só para regras mecanicamente checáveis (nome de arquivo, frontmatter obrigatório), não para julgamento semântico (ex.: "este conteúdo é um resumo de dia?").

Classificação de arquivo (resolvido/ativo/obsoleto) e qualquer exclusão devem continuar sendo decididas com confirmação explícita — nunca automáticas, para não arriscar apagar algo relevante sem revisão.

## Checklist rápido do dia

- [ ] Pasta `YYYY-MM-DD/` criada
- [ ] Resumo do dia anterior pedido (se fizer sentido)
- [ ] Arquivos novos do dia dentro da pasta certa
- [ ] Ao final: cada arquivo classificado (resolvido/ativo/obsoleto) e movido/apagado
- [ ] Pastas com +3 dias sem atividade revisadas para possível remoção
