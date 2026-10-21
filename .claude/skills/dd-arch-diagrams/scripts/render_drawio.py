# -*- coding: utf-8 -*-
"""Exportacao draw.io (mxfile com uma pagina por vista)."""
import html
from model import E, STATUS, META
from render_svg import node_data, seq_layout, wrap, KIND_LABEL, EDGE

def q(s):
    return html.escape(str(s), quote=True)

class Page:
    def __init__(self, name, w, h):
        self.name, self.w, self.h = name, w, h
        self.cells, self.n = [], 1

    def nid(self):
        self.n += 1
        return 'c%d' % self.n

    def add(self, xml):
        self.cells.append(xml)

    def vertex(self, value, style, x, y, w, h, id=None):
        id = id or self.nid()
        self.add('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="1"><mxGeometry x="%s" y="%s" width="%s" height="%s" as="geometry"/></mxCell>'
                 % (id, q(value), q(style), round(x, 1), round(y, 1), round(w, 1), round(h, 1)))
        return id

    def edge(self, style, pts, src=None, dst=None, value='', mid=None):
        id = self.nid()
        a = ' source="%s"' % src if src else ''
        b = ' target="%s"' % dst if dst else ''
        g = '<mxGeometry relative="1" as="geometry">'
        if not (src and dst):
            g += '<mxPoint x="%s" y="%s" as="sourcePoint"/><mxPoint x="%s" y="%s" as="targetPoint"/>' % (round(pts[0][0], 1), round(pts[0][1], 1), round(pts[-1][0], 1), round(pts[-1][1], 1))
        if len(pts) > 2:
            g += '<Array as="points">' + ''.join('<mxPoint x="%s" y="%s"/>' % (round(x, 1), round(y, 1)) for x, y in pts[1:-1]) + '</Array>'
        g += '</mxGeometry>'
        self.add('<mxCell id="%s" value="%s" style="%s" edge="1" parent="1"%s%s>%s</mxCell>' % (id, q(value), q(style), a, b, g))

    def xml(self, idx):
        return ('<diagram id="p%d" name="%s"><mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="0" pageScale="1" pageWidth="%s" pageHeight="%s" math="0" shadow="0">'
                '<root><mxCell id="0"/><mxCell id="1" parent="0"/>%s</root></mxGraphModel></diagram>') % (idx, q(self.name), self.w, self.h, ''.join(self.cells))


def ink_html(txt, size, color, bold=False, italic=False):
    s = 'font-size:%spx;color:%s;' % (size, color)
    t = q(txt)
    if bold:
        t = '<b>%s</b>' % t
    if italic:
        t = '<i>%s</i>' % t
    return '<span style="%s">%s</span>' % (s, t)


def node_label(d):
    k = d.get('kind', 'container')
    st = STATUS[d.get('status', 'novo')]
    if k == 'person':
        return q(d['name'])
    if k == 'db':
        return '<b style="font-size:11px">%s</b><br>%s' % (q(d['name']), ink_html(d.get('tech', ''), 9, '#64748B', italic=True))
    if k == 'bus':
        return q('%s · %s' % (d['tech'].upper(), d['name']))
    tag = KIND_LABEL.get(k, '')
    stl = {'novo': 'NOVO', 'reuso': 'REUSO', 'existente': 'EXISTENTE'}.get(d.get('status'), '')
    tag = tag + (' · ' + stl if k in ('container', 'component') and stl else '')
    parts = [ink_html(tag, 8, st['stroke'], bold=True), '<br>', ink_html(d['name'], 13, '#0F172A', bold=True)]
    if d.get('tech'):
        parts += ['<br>', ink_html(d['tech'], 10, '#64748B', italic=True)]
    if d.get('desc'):
        parts += ['<br>', ink_html(d['desc'], 10.5, '#334155')]
    return ''.join(parts)


def node_style(d):
    k = d.get('kind', 'container')
    st = STATUS[d.get('status', 'novo')]
    base = 'whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;fontColor=#0F172A;' % (st['fill'], st['stroke'])
    dash = 'dashed=1;dashPattern=6 4;' if st['dash'] else ''
    if k == 'person':
        return 'rounded=1;arcSize=50;whiteSpace=wrap;html=1;fillColor=#0F2A4A;strokeColor=#0F2A4A;fontColor=#FFFFFF;fontStyle=1;fontSize=12;'
    if k == 'db':
        return 'shape=cylinder3;boundedLbl=1;backgroundOutline=1;size=8;' + base + 'fontSize=10;strokeWidth=1.5;'
    if k == 'bus':
        return 'rounded=1;arcSize=30;whiteSpace=wrap;html=1;fillColor=#EDE9FE;strokeColor=#7C3AED;strokeWidth=2;fontColor=#4C1D95;fontStyle=1;fontSize=12;'
    if k == 'system':
        return 'rounded=1;arcSize=6;align=left;verticalAlign=top;spacing=14;strokeWidth=2.5;' + base + 'fontSize=12;'
    return 'rounded=1;arcSize=9;align=left;verticalAlign=top;spacingLeft=10;spacingTop=6;spacingRight=8;strokeWidth=1.6;' + dash + base + 'fontSize=11;'


def edge_style(e, exit_=None, entry=None):
    c = EDGE[e['kind']]
    s = 'html=1;rounded=0;endArrow=block;endFill=1;strokeColor=%s;strokeWidth=1.7;fontSize=10;fontColor=%s;labelBackgroundColor=#FFFFFF;' % (c['color'], c['color'])
    if c['dash']:
        s += 'dashed=1;dashPattern=%s;' % c['dash']
    if e.get('bi'):
        s += 'startArrow=block;startFill=1;'
    if exit_:
        s += 'exitX=%s;exitY=%s;exitDx=0;exitDy=0;' % (round(exit_[0], 4), round(exit_[1], 4))
    if entry:
        s += 'entryX=%s;entryY=%s;entryDx=0;entryDy=0;' % (round(entry[0], 4), round(entry[1], 4))
    return s


def page_block(v):
    p = Page(v.title.split(' — ')[0] + ' ' + (v.title.split(' — ')[1] if ' — ' in v.title else ''), v.w, v.h)
    p.name = v.title
    # bordas e faixas primeiro (z-order)
    for d in v.decor:
        if d['t'] == 'boundary':
            p.vertex(d['title'], 'rounded=1;arcSize=2;whiteSpace=wrap;html=1;fillColor=#F3F7FF;strokeColor=%s;strokeWidth=1.8;dashed=1;dashPattern=9 6;verticalAlign=top;align=left;spacingLeft=16;spacingTop=6;fontStyle=1;fontSize=13;fontColor=#1D4ED8;' % d['color'],
                     d['x'], d['y'], d['w'], d['h'])
    for d in v.decor:
        if d['t'] == 'label':
            sz = {'stitle': 26, 'stitle2': 26, 'ssub': 14, 'shead': 11}.get(d.get('cls', 'band'), 10)
            col = {'stitle': '#0F172A', 'stitle2': '#1D4ED8'}.get(d.get('cls'), '#64748B')
            bold = 1 if d.get('cls') in ('stitle', 'stitle2', 'shead', 'band') else 0
            wdt = 1180 if d.get('cls') in ('stitle', 'stitle2', 'ssub') else 420
            p.vertex(d['text'], 'text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=nowrap;fontSize=%s;fontColor=%s;fontStyle=%s;' % (sz, col, bold),
                     d['x'], d['y'] - sz - 4, wdt, sz + 10)
    ids = {}
    for nid, n in v.nodes.items():
        d = node_data(n)
        k = d.get('kind', 'container')
        cid = 'n_%s_%s' % (v.id, nid)
        ids[nid] = cid
        if k == 'sbox':
            st = STATUS[d.get('status', 'novo')]
            dash = 'dashed=1;dashPattern=6 4;' if st['dash'] else ''
            if d.get('small'):
                p.vertex('<b>%s</b>' % q(d['name']), 'rounded=1;arcSize=18;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;strokeWidth=1.8;fontColor=#1E3A8A;fontSize=12;' % (st['fill'], st['stroke']), n['x'], n['y'], n['w'], n['h'], cid)
            else:
                lab = ink_html(d['name'], 14, '#0F172A', bold=True) + '<br>' + ink_html(d.get('desc', ''), 11, '#334155')
                p.vertex(lab, 'rounded=1;arcSize=14;align=left;verticalAlign=top;spacingLeft=10;spacingTop=6;spacingRight=36;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=%s;strokeWidth=1.8;%s' % (st['fill'], st['stroke'], dash), n['x'], n['y'], n['w'], n['h'], cid)
            bx = n['x'] + n['w'] - 26
            for b in reversed(str(d.get('badge', '')).split()):
                p.vertex(b, 'ellipse;whiteSpace=wrap;html=1;fillColor=#DC2626;strokeColor=none;fontColor=#FFFFFF;fontStyle=1;fontSize=11;', bx, n['y'] + 5, 22, 22)
                bx -= 26
        elif k == 'scard':
            lab = ink_html(d['name'], 14, '#0F172A', bold=True) + '<br>' + ink_html(d['desc'], 11, '#334155') + '<br>' + ink_html('Quem decide: ' + d['who'], 10.5, '#B91C1C', bold=True)
            p.vertex(lab, 'rounded=1;arcSize=10;align=left;verticalAlign=top;spacingLeft=56;spacingTop=8;spacingRight=10;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#E2E8F0;strokeWidth=1.5;', n['x'], n['y'], n['w'], n['h'], cid)
            p.vertex(d['num'], 'ellipse;whiteSpace=wrap;html=1;fillColor=#DC2626;strokeColor=none;fontColor=#FFFFFF;fontStyle=1;fontSize=15;', n['x'] + 17, n['y'] + 14, 30, 30)
        else:
            p.vertex(node_label(d), node_style(d), n['x'], n['y'], n['w'], n['h'], cid)
            adr = d.get('adr')
            if adr and k in ('container', 'component', 'bus', 'ext'):
                lab = adr[0] + (' +%d' % (len(adr) - 1) if len(adr) > 1 else '')
                wd = 12 + 5.6 * len(lab)
                p.vertex(lab, 'rounded=1;arcSize=50;whiteSpace=wrap;html=1;fillColor=#FEE2E2;strokeColor=#FCA5A5;fontColor=#991B1B;fontStyle=1;fontSize=8;',
                         n['x'] + n['w'] - wd - 6, n['y'] + (-9 if k == 'bus' and n['h'] <= 60 else 6), wd, 15)
    for e in v.edges:
        st = edge_style(e, e['sp'], e['dp'])
        pts = e['path']
        p.edge(st, pts, ids[e['src']], ids[e['dst']], e['label'])
    for d in v.decor:
        if d['t'] == 'banner':
            p.vertex('<b style="font-size:11px;color:#93C5FD;letter-spacing:1px">%s</b>&nbsp;&nbsp;&nbsp;&nbsp;<span style="font-size:13px;color:#FFFFFF"><b>%s</b></span>' % (q(d['title']), q(d['text'])),
                     'rounded=1;arcSize=20;whiteSpace=wrap;html=1;fillColor=#0F2A4A;strokeColor=none;align=left;spacingLeft=20;', d['x'], d['y'], d['w'], d['h'])
        if d['t'] == 'legend':
            x = d['x']
            for lab, k in META['slide_legend']:
                st = STATUS[k]
                p.vertex('', 'rounded=1;html=1;fillColor=%s;strokeColor=%s;strokeWidth=1.5;%s' % (st['fill'], st['stroke'], 'dashed=1;' if st['dash'] else ''), x, d['y'] - 12, 20, 12)
                p.vertex(lab, 'text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=11;fontColor=#64748B;', x + 26, d['y'] - 17, 6 * len(lab) + 10, 20)
                x += 46 + 6.0 * len(lab)
            p.vertex('', 'ellipse;html=1;fillColor=#DC2626;strokeColor=none;', x, d['y'] - 12, 12, 12)
            p.vertex('Decisão a fechar no Discovery', 'text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=11;fontColor=#64748B;', x + 18, d['y'] - 17, 190, 20)
        if d['t'] == 'arrow':
            p.edge('html=1;endArrow=block;endFill=1;strokeColor=#64748B;strokeWidth=2.2;', d['pts'])
    return p


def seq_page(flow):
    L = seq_layout(flow)
    xs, W, H = L['xs'], L['W'], L['H']
    p = Page(flow['title'].split(' — ')[0], W, H)
    p.name = flow['title'].split(' — ')[0] + ' · ' + flow['title'].split(' — ')[1][:40]
    for f in [i for i in L['items'] if i['t'] == 'frame']:
        x1, x2 = 28 + 8 * f['lvl'], W - 28 - 8 * f['lvl']
        fill = '#F8FAFC' if f['kind'] == 'loop' else '#FFF7E6'
        p.vertex(('loop' if f['kind'] == 'loop' else 'alt') + ' · ' + f['lab'],
                 'rounded=1;arcSize=3;whiteSpace=wrap;html=1;fillColor=%s;strokeColor=#94A3B8;dashed=1;verticalAlign=top;align=left;spacingLeft=10;spacingTop=4;fontSize=10;fontStyle=1;fontColor=#334155;' % fill,
                 x1, f['y1'], x2 - x1, f['y2'] - f['y1'])
    for k, nm in L['parts']:
        x = xs[k]
        p.edge('html=1;endArrow=none;dashed=1;dashPattern=4 5;strokeColor=#CBD5E1;strokeWidth=1.5;', [(x, 72), (x, H - 14)])
        p.vertex('<b>%s</b>' % q(nm), 'rounded=1;arcSize=20;whiteSpace=wrap;html=1;fillColor=#0F2A4A;strokeColor=#0F2A4A;fontColor=#FFFFFF;fontSize=12;', x - 76, 22, 152, 50)
    sty = {'call': ('#334155', ''), 'ret': ('#64748B', 'dashed=1;dashPattern=5 4;'), 'async': ('#7C3AED', 'dashed=1;dashPattern=7 5;'), 'self': ('#334155', '')}
    for it in L['items']:
        if it['t'] == 'msg':
            c, da = sty[it['kind']]
            s = 'html=1;endArrow=block;endFill=1;strokeColor=%s;strokeWidth=1.7;%sfontSize=10;fontColor=%s;fontStyle=1;verticalAlign=bottom;labelBackgroundColor=#FFFFFF;spacingBottom=2;' % (c, da, c)
            p.edge(s, [(it['x1'], it['y']), (it['x2'], it['y'])], value=' '.join(it['lines']))
        elif it['t'] == 'self':
            c = sty['self'][0]
            x, y = it['x'], it['y']
            s = 'html=1;endArrow=block;endFill=1;strokeColor=%s;strokeWidth=1.7;fontSize=10;fontColor=%s;fontStyle=1;align=left;labelPosition=right;verticalLabelPosition=middle;' % (c, c)
            p.edge(s, [(x, y + 6), (x + 34, y + 6), (x + 34, y + 26), (x, y + 26)], value=' '.join(it['lines']))
        elif it['t'] == 'note':
            p.vertex(' '.join(it['lines']), 'rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#FEF9C3;strokeColor=#EAB308;fontColor=#713F12;fontSize=10;align=left;spacingLeft=8;',
                     it['x1'], it['y'], it['x2'] - it['x1'], it['h'])
    return p


def build(views, flows):
    pages = [page_block(v) for v in views] + [seq_page(f) for f in flows]
    body = ''.join(p.xml(i + 1) for i, p in enumerate(pages))
    return '<?xml version="1.0" encoding="UTF-8"?><mxfile host="app.diagrams.net" agent="' + META['agent'] + '" version="24.0.0" type="device">' + body + '</mxfile>'
