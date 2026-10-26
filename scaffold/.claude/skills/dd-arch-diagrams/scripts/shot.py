# -*- coding: utf-8 -*-
"""Captura de tela de abas do HTML gerado, via Chrome/Edge headless (para conferência visual).

Uso:  python -I shot.py <arquivo.html> <pasta_png> <aba1,aba2,...> [--size 1700x1050]

Notas:
- Tenta Chrome primeiro e depois Edge (em alguns ambientes corporativos o Edge headless trava).
- Usa um perfil temporário próprio e encerra o processo ao estourar o tempo (40 s por captura).
- Saída: <pasta_png>/<aba>.png — abra com a ferramenta de leitura de imagens para conferir o layout.
"""
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

CANDIDATES = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
    '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
]


def find_browser():
    for c in CANDIDATES:
        if os.path.exists(c):
            return c
    for n in ('chrome', 'google-chrome', 'chromium', 'msedge'):
        p = shutil.which(n)
        if p:
            return p
    return None


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(2)
    html, outdir, views = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
    size = '1700x1050'
    if '--size' in sys.argv:
        size = sys.argv[sys.argv.index('--size') + 1]
    w, h = size.split('x')
    exe = find_browser()
    if not exe:
        print('Nenhum Chrome/Edge encontrado.')
        sys.exit(1)
    os.makedirs(outdir, exist_ok=True)
    url = pathlib.Path(html).resolve().as_uri()
    prof = tempfile.mkdtemp(prefix='dd_arch_prof_')
    for v in views:
        png = os.path.abspath(os.path.join(outdir, v + '.png'))
        cmd = [exe, '--headless=new', '--disable-gpu', '--no-first-run', '--user-data-dir=' + prof, '--hide-scrollbars',
               '--virtual-time-budget=3000', '--screenshot=' + png, '--window-size=%s,%s' % (w, h), url + '#' + v]
        try:
            subprocess.run(cmd, timeout=40, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print('ok   ' if os.path.exists(png) else 'falha', png)
        except subprocess.TimeoutExpired:
            print('timeout', v)
    shutil.rmtree(prof, ignore_errors=True)


if __name__ == '__main__':
    main()
