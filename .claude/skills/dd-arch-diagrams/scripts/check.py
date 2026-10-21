# -*- coding: utf-8 -*-
"""Verificações estáticas das saídas do gerador (sem dependências externas).

Uso:  python -I check.py <pasta_de_saida>

Confere: (DSL) chaves balanceadas, endpoints definidos, relações duplicadas, passos das vistas dynamic;
         (draw.io) XML bem formado, ids únicos, source/target existentes;
         (HTML) placeholder não resolvido, JSON embutido válido, seções por aba.
Não substitui abrir o DSL no Structurizr nem o .drawio no draw.io.
"""
import collections
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET


def check_dsl(path):
    errs = []
    d = open(path, encoding='utf-8').read()
    if d.count('{') != d.count('}'):
        errs.append('chaves desbalanceadas')
    defs = set(re.findall(r'^\s*(\w+) = (?:person|softwareSystem|container|component)', d, re.M))
    cut = re.search(r'^\s*views \{', d, re.M)
    model = d[:cut.start()] if cut else d
    rels = re.findall(r'^\s*([\w.]+) -> ([\w.]+) "([^"]*)"', model, re.M)
    for a, b, _ in rels:
        for x in (a, b):
            if x.split('.')[-1] not in defs:
                errs.append('endpoint indefinido: %s' % x)
    dup = [k for k, v in collections.Counter(rels).items() if v > 1]
    if dup:
        errs.append('relações duplicadas (Structurizr rejeita): %s' % dup[:5])
    pairs = {(a, b) for a, b, _ in rels}
    for name, body in re.findall(r'dynamic \w+ "(\w+)" .*?\{(.*?)autoLayout', d, re.S):
        miss = [(a, b) for a, b, _ in re.findall(r'([\w.]+) -> ([\w.]+) "([^"]*)"', body) if (a, b) not in pairs]
        if miss:
            errs.append('vista dynamic %s usa passos sem relação no modelo: %s' % (name, miss[:5]))
    return errs, '%d elementos, %d relações' % (len(defs), len(rels))


def check_drawio(path):
    errs = []
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        return ['XML inválido: %s' % e], ''
    n = 0
    for dg in root.findall('diagram'):
        ids = [c.get('id') for c in dg.iter('mxCell')]
        n += 1
        if len(ids) != len(set(ids)):
            errs.append('ids duplicados na página %s' % dg.get('name'))
        s = set(ids)
        for c in dg.iter('mxCell'):
            for k in ('source', 'target'):
                if c.get(k) and c.get(k) not in s:
                    errs.append('%s inexistente (%s) na página %s' % (k, c.get(k), dg.get('name')))
    return errs, '%d páginas' % n


def check_html(path):
    errs = []
    h = open(path, encoding='utf-8').read()
    if '__PFX__' in h:
        errs.append('placeholder __PFX__ não resolvido')
    m = re.search(r'<script id="data" type="application/json">(.*?)</script>', h, re.S)
    if not m:
        errs.append('JSON de dados ausente')
    else:
        try:
            data = json.loads(m.group(1).replace('<\\/', '</'))
            ents = len(data['ent'])
        except Exception as e:  # noqa
            errs.append('JSON inválido: %s' % e)
            ents = 0
    tabs = re.findall(r'<button data-t="([^"]+)"', h)
    secs = set(re.findall(r'<section class="view" id="v-([^"]+)"', h))
    for t in tabs:
        if t not in secs:
            errs.append('aba sem seção: %s' % t)
    return errs, '%d abas, %d entidades' % (len(tabs), ents if m else 0)


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
    out = sys.argv[1]
    bad = 0
    for pat, fn in (('*.dsl', check_dsl), ('*.drawio', check_drawio), ('*-arquitetura.html', check_html)):
        for p in glob.glob(os.path.join(out, pat)):
            errs, info = fn(p)
            print(('FALHA ' if errs else 'ok    ') + os.path.basename(p) + '  (' + info + ')')
            for e in errs:
                print('   -', e)
            bad += len(errs)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
