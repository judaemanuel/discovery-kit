# -*- coding: utf-8 -*-
"""Gerador do Structurizr DSL a partir do modelo unico."""
from model import E, R, R1, RC, DYN, STATUS, META

SYS = META['sys_id']
CONT = [i for i, e in E.items() if e['kind'] in ('container', 'db', 'bus') and not e['parent']]
SYS_EXT = [i for i, e in E.items() if e['kind'] == 'ext']
PERSONS = [i for i, e in E.items() if e['kind'] == 'person']


def s(x):
    return str(x).replace('\\', '/').replace('"', "'").replace('\n', ' ').strip()


def ref(i):
    e = E[i]
    if e['parent']:
        return '%s.%s.%s' % (SYS, e['parent'], i)
    if i in CONT:
        return '%s.%s' % (SYS, i)
    return i


def tags_for(i):
    e = E[i]
    t = []
    if e['kind'] == 'person':
        t.append('Pessoa')
    else:
        t.append({'novo': 'Novo', 'reuso': 'Reuso', 'existente': 'Existente'}[e['status']])
    if e['kind'] == 'db':
        t.append('Banco')
    if e['kind'] == 'bus':
        t.append('Barramento')
    if e['kind'] == 'ext':
        t.append('Externo')
    return t


def rel(src, dst, text, tech, kind, ind):
    tg = {'async': 'Assincrono', 'batch': 'Lote'}.get(kind, '')
    parts = ['%s -> %s "%s"' % (ref(src), ref(dst), s(text))]
    if tech or tg:
        parts.append('"%s"' % s(tech))
    if tg:
        parts.append('"%s"' % tg)
    return ind + ' '.join(parts)


def elem(i, ind, body=''):
    e = E[i]
    tg = ' '.join('"%s"' % t for t in tags_for(i))
    extra = ''
    if e['adr']:
        extra += '\n%s    properties {\n%s        "ADR" "%s"\n%s    }' % (ind, ind, s(', '.join(e['adr'])), ind)
    if e['kind'] == 'person':
        head = '%s%s = person "%s" "%s"' % (ind, i, s(e['name']), s(e['desc']))
    elif e['kind'] == 'ext':
        head = '%s%s = softwareSystem "%s" "%s"' % (ind, i, s(e['name']), s(e['desc']))
    elif e['kind'] == 'component':
        head = '%s%s = component "%s" "%s" "%s"' % (ind, i, s(e['name']), s(e['desc']), s(e['tech']))
    else:
        head = '%s%s = container "%s" "%s" "%s"' % (ind, i, s(e['name']), s(e['desc']), s(e['tech']))
    return '%s {\n%s    tags %s%s%s\n%s}' % (head, ind, tg, extra, body, ind)


def build():
    o = []
    o.append('workspace "%s" "%s" {' % (s(META['dsl']['workspace_name']), s(META['dsl']['workspace_desc'])))
    o.append('')
    o.append('    !identifiers hierarchical')
    o.append('    !impliedRelationships false')
    o.append('')
    o.append('    model {')
    for i in PERSONS:
        o.append(elem(i, '        '))
    o.append('')
    for i in SYS_EXT:
        o.append(elem(i, '        '))
    o.append('')
    # Sistema em desenho (contêineres e componentes aninhados)
    body = []
    for i in CONT:
        sub = ''
        comps = [c for c, e in E.items() if e['parent'] == i]
        if comps:
            sub = '\n' + '\n'.join(elem(c, '                ') for c in comps)
        body.append(elem(i, '            ', sub))
    e = E[SYS]
    o.append('        %s = softwareSystem "%s" "%s" {' % (SYS, s(e['name']), s(e['desc'])))
    o.append('            tags "Novo"')
    o.append('\n'.join(body))
    o.append('        }')
    o.append('')
    o.append('        // --- relacionamentos de nível sistema (C1) ---')
    for a, b, t, tech, k in R1:
        if SYS in (a, b):
            o.append(rel(a, b, t, tech, k, '        '))
    o.append('')
    o.append('        // --- relacionamentos entre contêineres (C2) ---')
    for a, b, t, tech, k in R:
        o.append(rel(a, b, t, tech, k, '        '))
    o.append('')
    o.append('        // --- relacionamentos entre componentes (C3) ---')
    for a, b, t, tech, k in RC:
        o.append(rel(a, b, t, tech, k, '        '))
    o.append('    }')
    o.append('')
    o.append('    views {')
    inc = '            include ' + ' '.join(PERSONS)
    o.append('        systemContext %s "C1_Contexto" "%s" {' % (SYS, s(META['dsl']['c1'])))
    o.append('            include *')
    o.append(inc)
    o.append('            autoLayout tb 110 90')
    o.append('        }')
    o.append('        container %s "C2_Conteineres" "%s" {' % (SYS, s(META['dsl']['c2'])))
    o.append('            include *')
    o.append(inc)
    o.append('            autoLayout tb 110 90')
    o.append('        }')
    for cid, vname, vdesc in META['dsl']['c3']:
        o.append('        component %s.%s "%s" "%s" {' % (SYS, cid, vname, s(vdesc)))
        o.append('            include *')
        o.append('            autoLayout lr 110 90')
        o.append('        }')
    for vid, (desc, steps) in DYN.items():
        o.append('        dynamic %s "%s" "%s" {' % (SYS, vid, s(desc)))
        for a, b, t in steps:
            o.append('            %s -> %s "%s"' % (ref(a), ref(b), s(t)))
        o.append('            autoLayout lr 110 90')
        o.append('        }')
    o.append('')
    o.append('        styles {')
    o.append('            element "Element" {\n                color #0f172a\n                fontSize 22\n            }')
    o.append('            element "Pessoa" {\n                shape Person\n                background #0f2a4a\n                color #ffffff\n                stroke #0f2a4a\n            }')
    o.append('            element "Novo" {\n                background #dce8ff\n                stroke #2563eb\n                strokeWidth 3\n            }')
    o.append('            element "Reuso" {\n                background #fff0c9\n                stroke #b45309\n                strokeWidth 3\n                border dashed\n            }')
    o.append('            element "Existente" {\n                background #eef1f5\n                stroke #64748b\n            }')
    o.append('            element "Externo" {\n                background #eef1f5\n                stroke #64748b\n                border solid\n            }')
    o.append('            element "Banco" {\n                shape Cylinder\n            }')
    o.append('            element "Barramento" {\n                shape Pipe\n                background #ede9fe\n                stroke #7c3aed\n                color #4c1d95\n            }')
    o.append('            element "Software System" {\n                width 520\n                height 300\n            }')
    o.append('            element "Container" {\n                width 520\n                height 300\n            }')
    o.append('            element "Component" {\n                width 520\n                height 300\n            }')
    o.append('            relationship "Relationship" {\n                thickness 3\n                color #334155\n                fontSize 20\n            }')
    o.append('            relationship "Assincrono" {\n                dashed true\n                color #7c3aed\n            }')
    o.append('            relationship "Lote" {\n                style dotted\n                color #0e7490\n            }')
    o.append('        }')
    o.append('    }')
    o.append('}')
    return '\n'.join(o) + '\n'
