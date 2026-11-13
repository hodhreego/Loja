# -*- coding: utf-8 -*-
"""Coloca os códigos de checkout do Eduzz nos produtos de Educação Financeira da loja."""
import io
import re

P = r'A:\Claude.ai\Loja\build_loja.py'
CODIGOS = {
    'ef-6': 'E0DK782N91',
    'ef-7': 'E9OG7ADAWB',
    'ef-8': '7WXGXYE40A',
    'ef-9': '8017J1G607',
    'ef-1em': 'Q9N216B101',
    'ef-2em': 'D0R8G3769Y',
    'ef-3em': '89AX8BEG0D',
}

s = io.open(P, encoding='utf-8').read()
trocas = 0
for slug, code in CODIGOS.items():
    padrao = re.compile(r'(\("%s",\s*"[^"]+",\s*"reforco",\s*)None' % re.escape(slug))
    s, n = padrao.subn(lambda m: m.group(1) + '"%s"' % code, s, count=1)
    trocas += n
    print('%-8s %s -> %s' % (slug, 'ok' if n else 'NAO TROCOU', code))

io.open(P, 'w', encoding='utf-8').write(s)
print('total trocado:', trocas)
