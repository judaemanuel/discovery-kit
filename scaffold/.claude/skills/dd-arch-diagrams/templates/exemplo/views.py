# -*- coding: utf-8 -*-
"""Geometria (layout manual) de cada vista. Fonte unica para HTML e draw.io."""
from model import E, R, R1, RC


class V:
    def __init__(s, id, title, sub, w, h):
        s.id, s.title, s.sub, s.w, s.h = id, title, sub, w, h
        s.nodes, s.edges, s.decor = {}, [], []

    def n(s, id, x, y, w, h, **ov):
        s.nodes[id] = dict(id=id, x=x, y=y, w=w, h=h, ov=ov)

    def pt(s, id, fx, fy):
        n = s.nodes[id]
        return (n['x'] + fx * n['w'], n['y'] + fy * n['h'])

    def e(s, src, sp, dst, dp, label='', kind=None, mid=None, midx=None, pts=None, bi=False, lab=None):
        a, b = s.pt(src, *sp), s.pt(dst, *dp)
        if pts is not None:
            path = [a] + list(pts) + [b]
        elif mid is not None:
            path = [a, (a[0], mid), (b[0], mid), b]
        elif midx is not None:
            path = [a, (midx, a[1]), (midx, b[1]), b]
        else:
            path = [a, b]
        if kind is None:
            kind = 'sync'
            for (x, y, _l, _t, k) in R + R1 + RC:
                if x == src and y == dst:
                    kind = k
                    break
        s.edges.append(dict(src=src, dst=dst, sp=sp, dp=dp, label=label, kind=kind, path=path, bi=bi, lab=lab))

    def box(s, x, y, w, h, title, color='#2563EB', kind='boundary'):
        s.decor.append(dict(t=kind, x=x, y=y, w=w, h=h, title=title, color=color))

    def label(s, x, y, text, cls='band'):
        s.decor.append(dict(t='label', x=x, y=y, text=text, cls=cls))


VIEWS = {}
COLS = [200 + 290 * i for i in range(5)]
CW = 250
def cx(i): return COLS[i] + CW / 2

# =========================================================== C1
v = V('c1', 'C1 — Contexto do Sistema', 'Quem usa a plataforma e com quais sistemas ela conversa', 1560, 840)
v.n('assinante', 70, 30, 190, 52); v.n('convidado', 290, 30, 190, 52); v.n('parceiro', 570, 30, 190, 52)
v.n('analista', 940, 30, 190, 52); v.n('suporte', 1160, 30, 190, 52)
v.n('app_cli', 70, 150, 410, 104); v.n('portal_par', 520, 150, 290, 104); v.n('crm', 930, 150, 430, 104)
v.n('sys', 430, 330, 700, 220)
v.n('sched', 70, 350, 260, 80); v.n('financeiro', 70, 470, 260, 52); v.n('idp', 1230, 350, 260, 80)
v.n('erp', 70, 670, 300, 104); v.n('gateway', 420, 670, 300, 104); v.n('notif', 770, 670, 300, 104); v.n('fisco', 1120, 670, 300, 104)
v.e('assinante', (.5, 1), 'app_cli', (.2317, 0)); v.e('convidado', (.5, 1), 'app_cli', (.768, 0))
v.e('parceiro', (.5, 1), 'portal_par', (.5, 0))
v.e('analista', (.5, 1), 'crm', (.244, 0)); v.e('suporte', (.5, 1), 'crm', (.756, 0))
v.e('app_cli', (.9, 1), 'sys', (.1857, 0), 'Contratação, simulação, consulta', mid=286, kind='sync')
v.e('portal_par', (.5, 1), 'sys', (.3357, 0), 'Contratação via parceiro', kind='sync')
v.e('crm', (.3023, 1), 'sys', (.9, 0), 'Preço, aprovação, consulta', kind='sync')
v.e('sys', (1, .2727), 'idp', (0, .5), 'OIDC', kind='sync')
v.e('sched', (1, .5), 'sys', (0, .2727), 'Ciclo diário', kind='sync')
v.e('financeiro', (1, .5), 'sys', (0, .7545), 'Valida regras', kind='sync')
v.e('sys', (.1, 1), 'erp', (.5, 0), 'Espelho de assinatura e faturas', mid=610, kind='async')
v.e('sys', (.2, 1), 'gateway', (.5, 0), 'Ordem de cobrança / retorno', kind='sync')
v.e('sys', (.7, 1), 'notif', (.5, 0), 'Comunicados', kind='async')
v.e('sys', (.9, 1), 'fisco', (.5, 0), 'Dados fiscais', mid=610, kind='batch')
VIEWS['c1'] = v

# =========================================================== C2
v = V('c2', 'C2 — Contêineres', 'Serviços, dados e integrações da Plataforma de Assinaturas', 1900, 1180)
v.n('assinante', 200, 24, 190, 52); v.n('convidado', 410, 24, 190, 52); v.n('parceiro', 725, 24, 190, 52)
v.n('app_cli', 200, 110, 400, 104); v.n('portal_par', 630, 110, 380, 104); v.n('idp', 1360, 110, 250, 104)
v.box(150, 250, 1510, 630, 'Plataforma de Assinaturas  ·  bounded context "Assinaturas"')
v.label(166, 318, 'EXPERIÊNCIA'); v.label(166, 426, 'NÚCLEO DE NEGÓCIO'); v.label(166, 652, 'BARRAMENTO'); v.label(166, 732, 'INTEGRAÇÃO (ACL)')
v.n('api', 725, 290, 360, 100)
for i, k in enumerate(['qry', 'preco', 'orq', 'core', 'cobr']):
    v.n(k, COLS[i], 434, CW, 124)
v.n('qryDb', 200, 584, 120, 46); v.n('precoDb', 490, 584, 160, 46); v.n('coreDb', 1070, 584, 120, 46)
v.n('kafka', 180, 662, 1450, 40)
for i, k in enumerate(['aCrm', 'aErp', 'aGw', 'aNotif', 'aFisco']):
    v.n(k, COLS[i], 744, CW, 118)
for i, k in enumerate(['crm', 'erp', 'gateway', 'notif', 'fisco']):
    v.n(k, COLS[i], 946, CW, 108)
v.n('analista', 200, 1092, 120, 52); v.n('suporte', 330, 1092, 120, 52); v.n('financeiro', 1360, 1092, 250, 52)
v.n('sched', 1700, 434, 160, 112)
def bx(x): return ((x - 180) / 1450.0, 0)
v.e('assinante', (.5, 1), 'app_cli', (.2375, 0)); v.e('convidado', (.5, 1), 'app_cli', (.7625, 0))
v.e('parceiro', (.5, 1), 'portal_par', (.5, 0))
v.e('app_cli', (.9, 1), 'api', (.1528, 0), 'HTTPS / JSON', mid=234)
v.e('portal_par', (.75, 1), 'api', (.5278, 0))
v.e('api', (1, .3), 'idp', (.5, 1), 'OIDC', midx=1485)
v.e('api', (.0972, 1), 'qry', (.5, 0), mid=398, label='consulta', lab=(400, 396))
v.e('api', (.264, 1), 'preco', (.5, 0), mid=406, label='simula', lab=(690, 404))
v.e('api', (.736, 1), 'core', (.5, 0), mid=414, label='comando', lab=(1095, 412))
v.e('orq', (.9, 0), 'cobr', (.5, 0), mid=424, label='ordem de cobrança', lab=(1340, 422))
v.e('orq', (0, .3), 'preco', (1, .3))
v.e('orq', (1, .3), 'core', (0, .3))
v.e('cobr', (0, .75), 'core', (1, .75))
v.e('preco', (.24, 1), 'precoDb', (.5, 0)); v.e('core', (.24, 1), 'coreDb', (.5, 0)); v.e('qry', (.24, 1), 'qryDb', (.5, 0))
v.e('orq', (.7, 1), 'kafka', (bx(955)[0], 0), bi=True, kind='async')
v.e('core', (.8, 1), 'kafka', (bx(1270)[0], 0), bi=True, kind='async')
v.e('cobr', (.76, 1), 'kafka', (bx(1550)[0], 0), bi=True, kind='async')
v.e('kafka', (bx(410)[0], 1), 'qry', (.84, 1), kind='async')
v.e('kafka', (bx(325)[0], 1), 'aCrm', (.5, 0), bi=True, kind='async')
v.e('kafka', (bx(615)[0], 1), 'aErp', (.5, 0), kind='async')
v.e('kafka', (bx(905)[0], 1), 'aGw', (.5, 0), bi=True, kind='async')
v.e('kafka', (bx(1195)[0], 1), 'aNotif', (.5, 0), kind='async')
v.e('kafka', (bx(1485)[0], 1), 'aFisco', (.5, 0), kind='async')
v.e('aCrm', (.5, 1), 'crm', (.5, 0), 'resultado / pedido', bi=True, kind='sync')
v.e('aErp', (.3, 1), 'erp', (.3, 0), 'espelho', kind='async')
v.e('aGw', (.16, 1), 'erp', (.7, 0), 'A · via ERP', mid=904, kind='sync')
v.e('aGw', (.5, 1), 'gateway', (.5, 0), 'B · ordem / retorno', bi=True, kind='sync')
v.e('aNotif', (.5, 1), 'notif', (.5, 0), kind='async')
v.e('aFisco', (.5, 1), 'fisco', (.5, 0), kind='batch')
v.e('sched', (0, .5), 'cobr', (1, .5), 'job diário', lab=(1655, 478))
v.e('analista', (.5, 0), 'crm', (.24, 1)); v.e('suporte', (.5, 0), 'crm', (.76, 1))
v.e('financeiro', (.5, 0), 'fisco', (.5, 1))
VIEWS['c2'] = v

# =========================================================== C3 Orquestrador
v = V('c3o', 'C3 — Orquestrador de Processo', 'Componentes internos (conceitual)', 1500, 680)
v.n('kafka', 40, 290, 200, 104)
v.box(300, 60, 920, 560, 'Orquestrador de Processo')
v.n('o_defs', 610, 110, 240, 104); v.n('o_human', 880, 110, 240, 104)
v.n('o_listener', 340, 290, 240, 104); v.n('o_engine', 610, 290, 240, 104)
v.n('o_state', 340, 470, 240, 104); v.n('o_comp', 610, 470, 240, 104); v.n('o_retry', 880, 470, 240, 104)
v.n('preco', 1290, 100, 190, 124); v.n('core', 1290, 290, 190, 124); v.n('cobr', 1290, 480, 190, 124)
v.e('kafka', (1, .5), 'o_listener', (0, .5), kind='async')
v.e('o_listener', (1, .5), 'o_engine', (0, .5))
v.e('o_engine', (.5, 0), 'o_defs', (.5, 1))
v.e('o_engine', (.8, 0), 'o_human', (.3, 1), mid=252)
v.e('o_engine', (.17, 1), 'o_state', (.5, 0), mid=432)
v.e('o_engine', (.5, 1), 'o_comp', (.5, 0))
v.e('o_engine', (.83, 1), 'o_retry', (.5, 0), mid=432)
v.e('o_engine', (1, .25), 'preco', (0, .5), 'calcula', midx=1140, kind='sync')
v.e('o_engine', (1, .5), 'core', (0, .5), 'comanda', midx=1160, kind='sync')
v.e('o_engine', (1, .75), 'cobr', (0, .5), 'ordena cobrança', midx=1180, kind='sync')
VIEWS['c3o'] = v

# =========================================================== C3 Motor
v = V('c3p', 'C3 — Serviço de Precificação', 'Componentes internos (conceitual)', 1500, 700)
v.n('api', 40, 220, 220, 104); v.n('orq', 40, 370, 220, 104)
v.box(320, 60, 890, 560, 'Serviço de Precificação')
v.n('p_guard', 640, 110, 240, 104)
v.n('p_endpoint', 360, 290, 240, 104); v.n('p_resolver', 640, 290, 240, 104)
v.n('p_tax', 360, 470, 240, 104); v.n('p_engine', 640, 470, 240, 104); v.n('p_memo', 920, 470, 240, 104)
v.n('precoDb', 1260, 330, 200, 110)
v.e('api', (1, .5), 'p_endpoint', (0, .3), 'simula', midx=290)
v.e('orq', (1, .5), 'p_endpoint', (0, .7), 'calcula', midx=320)
v.e('p_endpoint', (.5, 0), 'p_guard', (0, .5), pts=[(480, 162)])
v.e('p_endpoint', (1, .5), 'p_resolver', (0, .5))
v.e('p_endpoint', (.9, 1), 'p_engine', (.1, 0))
v.e('p_resolver', (1, .5), 'precoDb', (0, .3), midx=1230)
v.e('p_engine', (0, .5), 'p_tax', (1, .5)); v.e('p_engine', (1, .5), 'p_memo', (0, .5))
v.e('p_memo', (1, .5), 'precoDb', (.5, 1), pts=[(1360, 522)])
VIEWS['c3p'] = v

# =========================================================== Slide executivo (16:9)
v = V('slide', 'Slide executivo — caminho de solução', 'Proposta de slide único (16:9) · 1280 × 720', 1280, 720)
v.label(40, 54, 'Já enxergamos o caminho da solução.', 'stitle')
v.label(40, 92, 'O Discovery valida as 4 decisões que definem prazo e custo.', 'stitle2')
v.label(40, 120, 'Arquitetura conceitual da Plataforma de Assinaturas — hipótese de trabalho, ainda não validada com as áreas técnicas', 'ssub')
v.label(40, 170, 'QUEM USA', 'shead')
A = [('a1', 'Assinante e convidado', 'App e Site do Assinante'), ('a2', 'Parceiro', 'Portal do Parceiro'),
     ('a3', 'Analista de Cobrança', 'CRM (casos e aprovações)'), ('a4', 'Suporte ao Cliente', 'Consulta de faturas')]
for i, (k, t, s_) in enumerate(A):
    v.n(k, 40, 190 + i * 104, 190, 88, kind='sbox', name=t, desc=s_, status='existente')
v.box(260, 174, 340, 440, 'Plataforma de Assinaturas  ·  nova', color='#2563EB')
B = [('b1', 'Registro da assinatura', 'Uma única fonte da verdade', 'novo', '2 4'),
     ('b2', 'Cálculo do preço', 'Regras do Financeiro, versionadas', 'novo', '3'),
     ('b3', 'Coordenação do processo', 'Ativação, faturas e exceções', 'novo', ''),
     ('b4', 'Cobrança recorrente automática', 'Aproveita padrão existente', 'reuso', '1'),
     ('b5', 'Acompanhamento de faturas', 'Extrato para cliente e suporte', 'novo', '')]
for i, (k, t, s_, st, bd) in enumerate(B):
    v.n(k, 276, 210 + i * 70, 308, 60, kind='sbox', name=t, desc=s_, status=st, badge=bd)
v.n('b6', 276, 566, 308, 36, kind='sbox', name='Integrações com os sistemas existentes', desc='', status='novo', small=True)
v.label(640, 170, 'SISTEMAS EXISTENTES', 'shead')
C = [('c1', 'ERP', 'Contratos e contas a receber', ''), ('c2', 'CRM', 'Atendimento e aprovações', ''),
     ('c3', 'Gateway de Pagamento', 'Cartão, Pix e boleto', '1'), ('c4', 'Notificação', 'E-mail e SMS ao assinante', ''),
     ('c5', 'Fiscal e Contábil', 'Notas e conciliação', '')]
for i, (k, t, s_, bd) in enumerate(C):
    v.n(k, 640, 190 + i * 84, 190, 70, kind='sbox', name=t, desc=s_, status='existente', badge=bd)
for i in range(4):
    v.decor.append(dict(t='arrow', pts=[(232, 234 + i * 104), (262, 234 + i * 104)]))
for i in range(5):
    v.decor.append(dict(t='arrow', pts=[(602, 225 + i * 84), (638, 225 + i * 84)]))
v.label(860, 170, '4 DECISÕES DO DISCOVERY', 'shead')
D = [('d1', '1', 'Como cobrar todo mês', 'Direto no gateway de pagamento ou via ERP existente', 'Financeiro · Arquitetura'),
     ('d2', '2', 'Onde fica a assinatura', 'E o que precisa voltar ao ERP a cada fatura paga', 'Time do ERP'),
     ('d3', '3', 'Regras oficiais de preço', 'Tabelas, descontos, impostos e arredondamento', 'Financeiro · Fiscal'),
     ('d4', '4', 'Migração da base atual', 'Convivência ou corte único das assinaturas legadas', 'Produto · Operações')]
for i, (k, num, t, s_, who) in enumerate(D):
    v.n(k, 860, 190 + i * 106, 380, 100, kind='scard', num=num, name=t, desc=s_, who=who)
v.decor.append(dict(t='banner', x=40, y=636, w=1200, h=54, title='O QUE SAI DO DISCOVERY',
                    text='Arquitetura validada com as áreas técnicas · backlog priorizado · plano de migração · estimativa · time dimensionado'))
v.decor.append(dict(t='legend', x=40, y=710))
VIEWS['slide'] = v
