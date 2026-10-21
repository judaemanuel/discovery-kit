# -*- coding: utf-8 -*-
"""Teste de regressão do gerador: reconstrói o exemplo e compara os hashes com tests/golden.json.

Uso:  python -I selftest.py            # compara
      python -I selftest.py --update   # grava novos hashes (só depois de mudança INTENCIONAL no motor)

Se falhar sem você ter mexido no motor, o ambiente mudou (versão do Python?) — reporte antes de seguir.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
PROJ = os.path.join(SKILL, 'templates', 'exemplo')
GOLD = os.path.join(SKILL, 'tests', 'golden.json')


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
    out = tempfile.mkdtemp(prefix='dd_arch_self_')
    r = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'build.py'), '--project', PROJ, '--out', out],
                       capture_output=True, text=True)
    if r.returncode:
        print(r.stdout, r.stderr)
        sys.exit(1)
    got = {f: sha(os.path.join(out, f)) for f in sorted(os.listdir(out))}
    c = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'check.py'), out], capture_output=True, text=True)
    print(c.stdout.strip())
    if c.returncode:
        sys.exit(1)
    if '--update' in sys.argv:
        os.makedirs(os.path.dirname(GOLD), exist_ok=True)
        json.dump(got, open(GOLD, 'w'), indent=2)
        print('golden atualizado:', GOLD)
        return
    gold = json.load(open(GOLD))
    ok = True
    for f, h in gold.items():
        same = got.get(f) == h
        ok &= same
        print(('IDÊNTICO ' if same else 'DIFERENTE ') + f)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
