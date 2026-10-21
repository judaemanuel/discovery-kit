# -*- coding: utf-8 -*-
"""Renderizacao SVG das vistas (diagramas de blocos e de sequencia)."""
import html
import zlib
from model import E, STATUS, ADR, META

FONT = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
INK, INK2, INK3 = '#0F172A', '#334155', '#64748B'
EDGE = {
    'sync':  dict(color='#334155', dash=''),
    'async': dict(color='#7C3AED', dash='7 5'),
    'batch': dict(color='#0E7490', dash='2 5'),
}
KIND_LABEL = {'person': 'PESSOA', 'ext': 'SISTEMA EXTERNO', 'container': 'CONTÊINER', 'component': 'COMPONENTE',
              'db': 'DADOS', 'bus': 'BARRAMENTO', 'system': 'SISTEMA'}


def esc(s):
    return html.escape(str(s), quote=True)


def wrap(text, maxw, fs=12, bold=False):
    f = fs * (0.56 if bold else 0.515)
    maxc = max(6, int(maxw / f))
    words, lines, cur = str(text).split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if len(t) <= maxc or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or ['']


def tspans(lines, x, y0, lh, anchor='start'):
    return ''.join('<tspan x="%s" y="%s">%s</tspan>' % (x, round(y0 + i * lh, 1), esc(l)) for i, l in enumerate(lines))


def text(x, y, lines, fs=12, fill=INK, weight='400', style='normal', lh=None, anchor='start', extra=''):
    lh = lh or fs * 1.25
    return '<text font-family="%s" font-size="%s" font-weight="%s" font-style="%s" fill="%s" text-anchor="%s" %s>%s</text>' % (
        FONT, fs, weight, style, fill, anchor, extra, tspans(lines, x, y, lh))


def node_data(n):
    d = dict(E.get(n['id'], {}))
    d.update(n['ov'])
    return d


def adr_pill(x, y, adr):
    if not adr:
        return ''
    label = adr[0] + (' +%d' % (len(adr) - 1) if len(adr) > 1 else '')
    w = 8 + 5.6 * len(label)
    return ('<g class="pill"><rect x="%s" y="%s" width="%s" height="15" rx="7.5" fill="#FEE2E2" stroke="#FCA5A5"/>'
            '<text x="%s" y="%s" font-family="%s" font-size="9.5" font-weight="700" fill="#991B1B" text-anchor="middle">%s</text></g>'
            % (round(x - w, 1), y, round(w, 1), round(x - w / 2, 1), y + 11, FONT, esc(label)))


def render_node(n, interactive=True):
    d = node_data(n)
    k = d.get('kind', 'container')
    x, y, w, h = n['x'], n['y'], n['w'], n['h']
    st = STATUS[d.get('status', 'novo')]
    fill, stroke = st['fill'], st['stroke']
    dash = ' stroke-dasharray="6 4"' if st['dash'] else ''
    cls = 'node k-%s' % k
    attr = ' data-id="%s" tabindex="0" role="button" aria-label="%s"' % (esc(n['id']), esc(d.get('name', ''))) if interactive and n['id'] in E else ''
    out = ['<g class="%s"%s>' % (cls, attr)]
    if k == 'person':
        out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s"/>' % (x, y, w, h, h / 2, fill, stroke))
        lines = wrap(d['name'], w - 28, 12.5, True)
        y0 = y + h / 2 - (len(lines) - 1) * 7.5 + 4.5
        out.append(text(x + w / 2, y0, lines, 12.5, '#FFFFFF', '700', lh=15, anchor='middle'))
    elif k == 'db':
        ry = 7
        out.append('<path d="M%s %s v%s a%s %s 0 0 0 %s 0 v-%s a%s %s 0 0 0 -%s 0z" fill="%s" stroke="%s" stroke-width="1.5"/>' % (
            x, y + ry, h - 2 * ry, w / 2, ry, w, h - 2 * ry, w / 2, ry, w, fill, stroke))
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" stroke="%s" stroke-width="1.5"/>' % (x + w / 2, y + ry, w / 2, ry, '#FFFFFF', stroke))
        nm = wrap(d['name'], w - 10, 10.5, True)
        ty = y + ry + 19 if h <= 60 else y + h / 2 + 2
        out.append(text(x + w / 2, ty, nm[:2], 10.5 if h <= 60 else 12, INK, '700', lh=11.5, anchor='middle'))
        out.append(text(x + w / 2, y + h - 5 if h <= 60 else ty + 18, [d.get('tech', '')[:24 if h <= 60 else 40]], 8.6 if h <= 60 else 10, INK3, '400', 'italic', anchor='middle'))
    elif k == 'bus':
        out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="#EDE9FE" stroke="#7C3AED" stroke-width="1.8"/>' % (x, y, w, h, min(h / 2, 20)))
        if h <= 60:
            out.append(text(x + w / 2, y + h / 2 + 4.5, ['%s  ·  %s   —   %s' % (d['tech'].upper(), d['name'], d['desc'])], 12.5, '#4C1D95', '600', anchor='middle'))
        else:
            out.append(text(x + w / 2, y + 36, [d['tech'].upper()], 13, '#4C1D95', '800', anchor='middle'))
            out.append(text(x + w / 2, y + 56, wrap(d['name'], w - 20, 12, True), 12, '#4C1D95', '700', anchor='middle'))
            out.append(text(x + w / 2, y + 76, wrap(d['desc'], w - 24, 10.5), 10.5, '#5B21B6', anchor='middle', lh=12.5))
        out.append(adr_pill(x + w - 8, y + 3, d.get('adr')) if h > 60 else adr_pill(x + w - 10, y - 9, d.get('adr')))
    elif k == 'system':
        out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="16" fill="%s" stroke="%s" stroke-width="2.4"/>' % (x, y, w, h, fill, stroke))
        out.append(text(x + 22, y + 32, ['SISTEMA · NOVO'], 10, '#1D4ED8', '700', extra='letter-spacing="1.2"'))
        out.append(text(x + 22, y + 60, [d['name']], 24, INK, '800'))
        out.append(text(x + 22, y + 80, [d['tech']], 11.5, INK3, '400', 'italic'))
        out.append(text(x + 22, y + 102, wrap(d['desc'], w - 44, 12.5), 12.5, INK2, lh=15))
        chips = META['chips']
        cx0, cy0 = x + 22, y + 146
        for c in chips:
            cw = 14 + 6.4 * len(c)
            if cx0 + cw > x + w - 20:
                cx0, cy0 = x + 22, cy0 + 32
            out.append('<rect x="%s" y="%s" width="%s" height="24" rx="12" fill="#FFFFFF" stroke="#93B4F0"/>' % (round(cx0, 1), cy0, round(cw, 1)))
            out.append(text(round(cx0 + cw / 2, 1), cy0 + 16, [c], 11, '#1E3A8A', '600', anchor='middle'))
            cx0 += cw + 8
    elif k == 'sbox':
        out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="10" fill="%s" stroke="%s" stroke-width="1.8"%s/>' % (x, y, w, h, fill, stroke, dash))
        if d.get('small'):
            out.append(text(x + w / 2, y + h / 2 + 4.5, [d['name']], 12.5, '#1E3A8A', '700', anchor='middle'))
        else:
            nm = wrap(d['name'], w - 50, 14, True)
            out.append(text(x + 14, y + 23, nm, 14, INK, '700', lh=16))
            out.append(text(x + 14, y + 23 + len(nm) * 16 + 1, wrap(d.get('desc', ''), w - 28, 11.5), 11.5, INK2, lh=13.5))
        bx = x + w - 14
        for b in reversed(str(d.get('badge', '')).split()):
            out.append('<circle cx="%s" cy="%s" r="11" fill="#DC2626"/>' % (bx, y + 16))
            out.append(text(bx, y + 20.5, [b], 12, '#FFFFFF', '800', anchor='middle'))
            bx -= 26
    elif k == 'scard':
        out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>' % (x, y, w, h))
        out.append('<rect x="%s" y="%s" width="6" height="%s" rx="3" fill="#DC2626"/>' % (x, y + 8, h - 16))
        out.append('<circle cx="%s" cy="%s" r="15" fill="#DC2626"/>' % (x + 32, y + 30))
        out.append(text(x + 32, y + 36, [d['num']], 16, '#FFFFFF', '800', anchor='middle'))
        nm = wrap(d['name'], w - 86, 14.5, True)
        out.append(text(x + 58, y + 26, nm, 14.5, INK, '700', lh=16.5))
        yy = y + 26 + len(nm) * 16.5 - 2
        ds = wrap(d['desc'], w - 72, 11.5)
        out.append(text(x + 58, yy + 8, ds, 11.5, INK2, lh=13.5))
        out.append(text(x + 58, y + h - 10, ['Quem decide: ' + d['who']], 11, '#B91C1C', '700'))
    else:  # container, component, ext
        sw = 1.6
        out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="10" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x, y, w, h, fill, stroke, sw, dash))
        tag = KIND_LABEL.get(k, '')
        stl = {'novo': 'NOVO', 'reuso': 'REUSO', 'existente': 'EXISTENTE'}.get(d.get('status'), '')
        tagtxt = tag + (' · ' + stl if k in ('container', 'component') and stl else '')
        out.append(text(x + 12, y + 17, [tagtxt], 8.6, stroke, '700', extra='letter-spacing="0.9"'))
        nm = wrap(d['name'], w - 24, 13.5, True)
        yy = y + 36
        out.append(text(x + 12, yy, nm, 13.5, INK, '700', lh=15.5))
        yy += len(nm) * 15.5 - 1
        if d.get('tech'):
            tl = wrap(d['tech'], w - 24, 10.2)
            out.append(text(x + 12, yy, tl[:1], 10.2, INK3, '400', 'italic'))
            yy += 14
        maxl = max(1, int((y + h - yy - 6) / 13))
        dl = wrap(d.get('desc', ''), w - 24, 11)
        if len(dl) > maxl:
            dl = dl[:maxl]
            dl[-1] = dl[-1].rstrip('., ') + '…'
        out.append(text(x + 12, yy + 2, dl, 11, INK2, lh=13))
        out.append(adr_pill(x + w - 7, y + 6, d.get('adr')))
    out.append('</g>')
    return ''.join(out)


def path_d(pts):
    return 'M' + ' L'.join('%s %s' % (round(x, 1), round(y, 1)) for x, y in pts)


def label_pos(e):
    if e.get('lab'):
        return e['lab']
    best, bl = None, -1
    p = e['path']
    for i in range(len(p) - 1):
        l = abs(p[i + 1][0] - p[i][0]) + abs(p[i + 1][1] - p[i][1])
        if l > bl:
            bl, best = l, ((p[i][0] + p[i + 1][0]) / 2, (p[i][1] + p[i + 1][1]) / 2)
    return best


def defs():
    m = ''
    for k, c in EDGE.items():
        m += ('<marker id="ar-%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
              '<path d="M0 0 L10 5 L0 10 z" fill="%s"/></marker>' % (k, c['color']))
    m += ('<marker id="ar-slide" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
          '<path d="M0 0 L10 5 L0 10 z" fill="#64748B"/></marker>')
    return '<defs>%s</defs>' % m


def render_edge(e, interactive=True):
    c = EDGE[e['kind']]
    da = ' stroke-dasharray="%s"' % c['dash'] if c['dash'] else ''
    ms = ' marker-start="url(#ar-%s)"' % e['kind'] if e['bi'] else ''
    attr = ' data-src="%s" data-dst="%s"' % (esc(e['src']), esc(e['dst']))
    out = '<g class="edge"%s><path d="%s" fill="none" stroke="%s" stroke-width="1.7"%s marker-end="url(#ar-%s)"%s/>' % (
        attr, path_d(e['path']), c['color'], da, e['kind'], ms)
    if e['label']:
        lx, ly = label_pos(e)
        ln = e['label']
        wd = 6.0 * len(ln) + 8
        out += ('<rect x="%s" y="%s" width="%s" height="15" rx="4" fill="#FFFFFF" fill-opacity=".92"/>' % (round(lx - wd / 2, 1), round(ly - 11, 1), round(wd, 1)))
        out += text(round(lx, 1), round(ly, 1), [ln], 10.5, c['color'], '600', anchor='middle')
    return out + '</g>'


def render_decor(d):
    t = d['t']
    if t == 'boundary':
        return ('<rect x="%s" y="%s" width="%s" height="%s" rx="18" fill="#F3F7FF" stroke="%s" stroke-width="1.8" stroke-dasharray="9 6"/>' % (
            d['x'], d['y'], d['w'], d['h'], d['color'])) + text(d['x'] + 18, d['y'] + 26, [d['title']], 14, '#1D4ED8', '800')
    if t == 'label':
        c = d.get('cls', 'band')
        if c == 'stitle':
            return text(d['x'], d['y'], [d['text']], 27, INK, '800')
        if c == 'stitle2':
            return text(d['x'], d['y'], [d['text']], 27, '#1D4ED8', '800')
        if c == 'ssub':
            return text(d['x'], d['y'], [d['text']], 14, INK3, '400')
        if c == 'shead':
            return text(d['x'], d['y'], [d['text']], 11.5, INK3, '800', extra='letter-spacing="1.3"')
        return text(d['x'], d['y'], [d['text']], 10, INK3, '700', extra='letter-spacing="1.4"')
    if t == 'banner':
        x, y, w, h = d['x'], d['y'], d['w'], d['h']
        return ('<rect x="%s" y="%s" width="%s" height="%s" rx="12" fill="#0F2A4A"/>' % (x, y, w, h)
                + text(x + 22, y + h / 2 + 4, [d['title']], 11.5, '#93C5FD', '800', extra='letter-spacing="1.3"')
                + text(x + 232, y + h / 2 + 5, [d['text']], 13.5, '#FFFFFF', '600'))
    if t == 'legend':
        o, x, y = '', d['x'], d['y']
        for lab, k in META['slide_legend']:
            st = STATUS[k]
            o += '<rect x="%s" y="%s" width="20" height="12" rx="3" fill="%s" stroke="%s" stroke-width="1.5"%s/>' % (x, y - 10, st['fill'], st['stroke'], ' stroke-dasharray="4 3"' if st['dash'] else '')
            o += text(x + 28, y, [lab], 11, INK3)
            x += 46 + 6.0 * len(lab)
        o += '<circle cx="%s" cy="%s" r="7" fill="#DC2626"/>' % (x + 6, y - 4) + text(x + 20, y, ['Decisão a fechar no Discovery'], 11, INK3)
        return o
    if t == 'arrow':
        return '<path d="%s" stroke="#64748B" stroke-width="2.2" fill="none" marker-end="url(#ar-slide)"/>' % path_d(d['pts'])
    return ''


def svg_view(v, interactive=True, legend=True):
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" width="%s" height="%s" role="img" aria-label="%s" data-view="%s">' % (
        v.w, v.h + (0 if v.id == 'slide' else 0), v.w, v.h, esc(v.title), v.id), defs(),
        '<rect width="%s" height="%s" fill="%s"/>' % (v.w, v.h, '#FFFFFF')]
    for d in v.decor:
        if d['t'] in ('boundary',):
            parts.append(render_decor(d))
    for d in v.decor:
        if d['t'] != 'boundary':
            parts.append(render_decor(d))
    for e in v.edges:
        parts.append(render_edge(e, interactive))
    for n in v.nodes.values():
        parts.append(render_node(n, interactive))
    parts.append('</svg>')
    return uniq(''.join(parts), v.id)


def uniq(s, vid):
    return s.replace('url(#ar-', 'url(#%s-ar-' % vid).replace('id="ar-', 'id="%s-ar-' % vid)


# ============================================================ sequencia
def seq_layout(flow):
    parts = flow['parts']
    step = 178
    left = 40
    xs = {k: left + step / 2 + i * step for i, (k, _) in enumerate(parts)}
    W = left * 2 + step * len(parts)
    y = 100
    items, stack, num = [], [], 0
    for m in flow['msgs']:
        t = m[0]
        if t in ('alt', 'loop'):
            if t == 'alt' and stack and stack[-1]['kind'] == 'alt':
                f = stack.pop(); f['y2'] = y - 6; items.append(f)
            y += 6
            stack.append(dict(t='frame', kind=t, y1=y, lab=m[1], lvl=len(stack)))
            y += 28
            continue
        if t == 'end':
            f = stack.pop(); f['y2'] = y - 4; items.append(f); y += 10
            continue
        if t == 'note':
            a, b, txt = m[1], m[2], m[3]
            x1, x2 = min(xs[a], xs[b]) - 70, max(xs[a], xs[b]) + 70
            lines = wrap(txt, x2 - x1 - 20, 11)
            hh = 14 + 14 * len(lines)
            items.append(dict(t='note', x1=x1, x2=x2, y=y, h=hh, lines=lines))
            y += hh + 18
            continue
        a, b, txt, kind = m
        num += 1
        if a == b:
            lines = wrap('%d. %s' % (num, txt), 150, 11)
            items.append(dict(t='self', x=xs[a], y=y, lines=lines, kind=kind))
            y += max(34, 16 + 13 * len(lines)) + 14
        else:
            span = abs(xs[b] - xs[a]) - 14
            lines = wrap('%d. %s' % (num, txt), span, 11)
            items.append(dict(t='msg', x1=xs[a], x2=xs[b], y=y + 13 * (len(lines) - 1) + 20, lines=lines, kind=kind))
            y += 13 * (len(lines) - 1) + 20 + 22
    while stack:
        f = stack.pop(); f['y2'] = y; items.append(f)
    H = y + 30
    return dict(xs=xs, W=W, H=H, items=items, parts=parts, title=flow['title'])


SEQ_STYLE = {
    'call':  dict(color='#334155', dash='', end='sync'),
    'ret':   dict(color='#64748B', dash='5 4', end='sync'),
    'async': dict(color='#7C3AED', dash='7 5', end='async'),
    'self':  dict(color='#334155', dash='', end='sync'),
}


def seq_svg(flow):
    L = seq_layout(flow)
    xs, W, H = L['xs'], L['W'], L['H']
    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" width="%s" height="%s" role="img" aria-label="%s" data-view="seq">' % (W, H, W, H, esc(L['title'])),
         defs(), '<rect width="%s" height="%s" fill="#FFFFFF"/>' % (W, H)]
    for f in [i for i in L['items'] if i['t'] == 'frame']:
        ins = 14 + 8 * f['lvl']
        x1, x2 = 28 + 8 * f['lvl'], W - 28 - 8 * f['lvl']
        o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="8" fill="%s" fill-opacity=".5" stroke="#94A3B8" stroke-dasharray="5 4"/>' % (
            x1, f['y1'], x2 - x1, f['y2'] - f['y1'], '#F8FAFC' if f['kind'] == 'loop' else '#FFF7E6'))
        lab = ('loop' if f['kind'] == 'loop' else 'alt') + ' · ' + f['lab']
        o.append('<rect x="%s" y="%s" width="%s" height="18" rx="6" fill="#E2E8F0"/>' % (x1 + 8, f['y1'] + 5, 10 + 6.1 * len(lab)))
        o.append(text(x1 + 14, f['y1'] + 18, [lab], 10.5, INK2, '700'))
    for k, nm in L['parts']:
        x = xs[k]
        lines = wrap(nm, 136, 12, True)
        o.append('<line x1="%s" y1="72" x2="%s" y2="%s" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="4 5"/>' % (x, x, H - 14))
        o.append('<rect x="%s" y="22" width="152" height="50" rx="10" fill="#0F2A4A"/>' % (x - 76))
        o.append(text(x, 47 - (len(lines) - 1) * 7 + 4, lines, 12, '#FFFFFF', '700', anchor='middle', lh=14))
    for it in L['items']:
        if it['t'] == 'msg':
            s = SEQ_STYLE[it['kind']]
            x1, x2, y = it['x1'], it['x2'], it['y']
            d = 1 if x2 > x1 else -1
            o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1.7"%s marker-end="url(#ar-%s)"/>' % (
                x1, y, x2 - d * 2, y, s['color'], ' stroke-dasharray="%s"' % s['dash'] if s['dash'] else '', s['end']))
            n = len(it['lines'])
            o.append(text(round((x1 + x2) / 2, 1), y - 7 - 13 * (n - 1), it['lines'], 11, s['color'], '600', anchor='middle', lh=13))
        elif it['t'] == 'self':
            s = SEQ_STYLE['self']
            x, y = it['x'], it['y']
            o.append('<path d="M%s %s h34 v20 h-34" fill="none" stroke="%s" stroke-width="1.7" marker-end="url(#ar-sync)"/>' % (x, y + 6, s['color']))
            o.append(text(x + 42, y + 14, it['lines'], 11, s['color'], '600', lh=13))
        elif it['t'] == 'note':
            o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="#FEF9C3" stroke="#EAB308"/>' % (it['x1'], it['y'], it['x2'] - it['x1'], it['h']))
            o.append(text(it['x1'] + 10, it['y'] + 18, it['lines'], 11, '#713F12', '500', lh=14))
    o.append('</svg>')
    return uniq(''.join(o), 'seq%d' % zlib.crc32(flow['title'].encode('utf-8')))
