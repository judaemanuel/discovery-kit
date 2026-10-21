# -*- coding: utf-8 -*-
"""ESQUELETO mínimo do dd-arch-diagrams: 1 pessoa, 1 sistema externo, 1 sistema, 2 contêineres e o barramento.

Copie esta pasta (model.py + views.py) para o seu projeto, renomeie ids/textos e acrescente entidades.
Para recursos completos (C3, fluxos de sequência, slide), parta de templates/exemplo.
"""

STATUS = {
    'novo':      dict(label='Novo (a construir)',                     fill='#DCE8FF', stroke='#2563EB', dash=False),
    'reuso':     dict(label='Reaproveita padrão/serviço (a validar)', fill='#FFF0C9', stroke='#B45309', dash=True),
    'existente': dict(label='Existente na organização',               fill='#EEF1F5', stroke='#64748B', dash=False),
    'pessoa':    dict(label='Pessoa / papel',                         fill='#0F2A4A', stroke='#0F2A4A', dash=False),
}

E = {}
def ent(id, kind, name, tech='', desc='', status='novo', parent=None, adr=(), open=(), refs=()):
    E[id] = dict(id=id, kind=kind, name=name, tech=tech, desc=desc, status=status, parent=parent,
                 adr=list(adr), open=list(open), refs=list(refs))

ent('usuario', 'person', 'Usuário', desc='Quem usa o sistema', status='pessoa')
ent('legado', 'ext', 'Sistema legado', 'Tecnologia (existente)', 'O que ele faz para o negócio', status='existente',
    open=['Pergunta em aberto sobre o legado'])
ent('sys', 'system', 'Meu Sistema', 'Bounded context "Meu Contexto"', 'Responsabilidade do sistema em uma frase', status='novo')
ent('api', 'container', 'API', 'REST / BFF', 'Expõe as jornadas aos canais', adr=['ADR-01'])
ent('core', 'container', 'Serviço de Domínio', 'Serviço (linguagem?)', 'Regras de negócio e fonte da verdade', adr=['ADR-01'])
ent('kafka', 'bus', 'Barramento de Eventos', 'Kafka', 'Eventos de domínio e filas de exceção', status='existente')
ent('db', 'db', 'Banco', 'PostgreSQL', 'Dados do serviço de domínio')

R = [   # (origem, destino, texto, tecnologia, tipo: sync | async | batch)
 ('usuario', 'api', 'Usa', 'HTTPS', 'sync'),
 ('api', 'core', 'Comanda', 'HTTPS', 'sync'),
 ('core', 'db', 'Lê / escreve', 'JDBC', 'sync'),
 ('core', 'kafka', 'Publica eventos', 'Evento', 'async'),
 ('kafka', 'legado', 'Espelha dados', 'Evento', 'async'),
]
R1 = [  # relações de nível sistema (C1): use o id do sistema ('sys') no lugar dos contêineres
 ('usuario', 'sys', 'Usa', 'HTTPS', 'sync'),
 ('sys', 'legado', 'Espelha dados', 'Evento', 'async'),
]
RC = []                       # relações entre componentes (C3); vazio neste esqueleto
FLOWS = {}                    # fluxos de sequência; vazio neste esqueleto
DYN = {}                      # vistas dynamic do Structurizr; vazio neste esqueleto

ADR = [
 ('ADR-01', 'Decisão proposta em uma frase', 'Alternativas consideradas', 'Q-01', 'aberto', 'Nota curta'),
]
ADR_STATE = {'aberto': 'Em aberto', 'tend': 'Tendência / hipótese', 'nossa': 'Proposta nossa'}

META = dict(
    stem='meu-sistema', sys_id='sys', agent='dd-arch-diagrams', download_prefix='meu-sistema-',
    page_title='Meu Sistema · Arquitetura conceitual v1',
    title='Meu Sistema — Arquitetura conceitual v1',
    badge='HIPÓTESE DE TRABALHO · NÃO VALIDADA',
    subtitle='Modelo C4 · AAAA-MM-DD · autoria',
    chips=['API', 'Serviço de Domínio', 'Kafka'],          # chips mostrados dentro do bloco do sistema no C1
    flow_hint='Sequência conceitual · setas tracejadas roxas = eventos (Kafka)',
    slide_legend=[('Novo', 'novo'), ('Aproveita padrão existente (a validar)', 'reuso'), ('Existente na organização', 'existente')],
    tabs=[('c1', 'C1 · Contexto', 'blk'), ('c2', 'C2 · Contêineres', 'blk'), ('adr', 'Decisões', 'doc'), ('sobre', 'Sobre', 'doc')],
    drawio_views=['c1', 'c2'], drawio_flows=[],
    open_limits=[('O que este desenho não resolve', 'Motivo / quem precisa responder')],
    adr_sub='Todas são <b>propostas</b>. Nenhuma foi validada pelas áreas técnicas.',
    principles=['<li><b>Princípio 1</b>: explicação curta.</li>'],
    sobre=dict(sub='Meu Sistema · arquitetura conceitual v1',
               cards=[('O que é', ['<li>Desenho conceitual (C4) do provável caminho de solução.</li>']),
                      ('Como usar', ['<li>Clique nos blocos para ver decisões e pontos em aberto.</li>'])]),
    dsl=dict(workspace_name='Meu Sistema — Arquitetura conceitual v1', workspace_desc='Desenho conceitual (C4); hipótese de trabalho.',
             c1='C1 — Contexto do Meu Sistema', c2='C2 — Contêineres do Meu Sistema', c3=[]),
)
