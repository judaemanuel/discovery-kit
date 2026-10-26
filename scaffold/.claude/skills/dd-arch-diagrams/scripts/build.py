# -*- coding: utf-8 -*-
"""Gera <stem>.dsl, <stem>.drawio e <stem>-arquitetura.html a partir de um projeto (model.py + views.py).

Uso:  python -I build.py --project <pasta_do_projeto> --out <pasta_de_saida>
"""
import argparse
import os
import sys
import xml.dom.minidom


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--project', required=True, help='pasta com model.py e views.py')
    ap.add_argument('--out', required=True, help='pasta de saida')
    a = ap.parse_args()
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.abspath(a.project))
    from views import VIEWS
    from model import FLOWS, META
    import dsl
    import render_drawio
    import render_html

    os.makedirs(a.out, exist_ok=True)
    stem = META['stem']
    names = ('%s.dsl' % stem, '%s.drawio' % stem, '%s-arquitetura.html' % stem)
    open(os.path.join(a.out, names[0]), 'w', encoding='utf-8', newline='\n').write(dsl.build())
    dx = render_drawio.build([VIEWS[k] for k in META['drawio_views']], [FLOWS[k] for k in META['drawio_flows']])
    xml.dom.minidom.parseString(dx.encode('utf-8'))  # valida XML bem formado
    open(os.path.join(a.out, names[1]), 'w', encoding='utf-8', newline='\n').write(dx)
    open(os.path.join(a.out, names[2]), 'w', encoding='utf-8', newline='\n').write(render_html.build(VIEWS))
    for f in names:
        print(f, os.path.getsize(os.path.join(a.out, f)))


if __name__ == '__main__':
    main()
