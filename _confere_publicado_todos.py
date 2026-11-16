# -*- coding: utf-8 -*-
"""Confere as prévias publicadas dos 7 cadernos Se Liga (imagens 2 e 3)."""
import hashlib
import os
import urllib.request

IMG = r'A:\Claude.ai\Loja\img'
SLUGS = ['se-liga-6', 'se-liga-7', 'se-liga-8', 'se-liga-9',
         'se-liga-1em', 'se-liga-2em', 'se-liga-3em']


def sha(b):
    return hashlib.sha256(b).hexdigest()[:12]


for slug in SLUGS:
    linha = []
    for k in (2, 3):
        nome = '%s-%d.jpg' % (slug, k)
        local = open(os.path.join(IMG, nome), 'rb').read()
        req = urllib.request.Request('https://eduloja.com/img/' + nome,
                                     headers={'User-Agent': 'Mozilla/5.0'})
        remoto = urllib.request.urlopen(req, timeout=30).read()
        linha.append('p%d %s' % (k, 'igual' if sha(local) == sha(remoto) else 'DIFERENTE'))
    print('%-11s %s' % (slug, ' · '.join(linha)))
