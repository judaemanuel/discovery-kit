# -*- coding: utf-8 -*-
"""Geometria do esqueleto: C1 e C2. Coordenadas em px dentro do canvas (w × h). Ver references/layout.md."""
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
        """Aresta de (src, ponto sp=(fx,fy) na caixa) até (dst, dp). Rota: reta; mid=y -> V-H-V; midx=x -> H-V-H; pts=[...] manual."""
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

# ------------------------------------------------------------------ C1
v = V('c1', 'C1 — Contexto do Sistema', 'Quem usa o sistema e com o que ele conversa', 1100, 640)
v.n('usuario', 400, 30, 200, 52)
v.n('sys', 250, 190, 500, 220)
v.n('legado', 360, 500, 280, 104)
v.e('usuario', (.5, 1), 'sys', (.5, 0), 'Usa', kind='sync')
v.e('sys', (.5, 1), 'legado', (.5, 0), 'Espelha dados', kind='async')
VIEWS['c1'] = v

# ------------------------------------------------------------------ C2
v = V('c2', 'C2 — Contêineres', 'Serviços, dados e integrações', 1100, 700)
v.n('usuario', 400, 24, 200, 52)
v.box(120, 120, 860, 400, 'Meu Sistema')
v.n('api', 160, 170, 250, 112)
v.n('core', 450, 170, 250, 124)
v.n('db', 480, 340, 130, 46)
v.n('kafka', 150, 430, 800, 40)
v.n('legado', 360, 580, 280, 104)
v.e('usuario', (.5, 1), 'api', (.5, 0), mid=100, kind='sync')
v.e('api', (1, .4), 'core', (0, .4), kind='sync')
v.e('core', (.24, 1), 'db', (.5, 0), kind='sync')
v.e('core', (.8, 1), 'kafka', (.625, 0), kind='async')
v.e('kafka', (.45, 1), 'legado', (.5, 0), 'espelho', kind='async')
VIEWS['c2'] = v
