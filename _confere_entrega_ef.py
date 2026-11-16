# -*- coding: utf-8 -*-
import glob
import os

RAIZ = r'A:\Claude.ai\Materiais\Educacao-Financeira\Avaliacoes-Finais'
for p in ('6-ano', '7-ano', '8-ano', '9-ano', '1-serie-em', '2-serie-em', '3-serie-em'):
    pdf = os.path.join(RAIZ, p, 'se-liga-educacao-financeira.pdf')
    print('%-12s %8d bytes  %s' % (p, os.path.getsize(pdf) if os.path.exists(pdf) else -1, 'OK' if os.path.exists(pdf) else 'FALTA'))

print()
for slug in ('ef-6', 'ef-7', 'ef-8', 'ef-9', 'ef-1em', 'ef-2em', 'ef-3em'):
    imgs = sorted(glob.glob(os.path.join(r'A:\Claude.ai\Loja\img', slug + '-*.jpg')))
    print('%-8s %d imagens %s' % (slug, len(imgs), [os.path.basename(i) for i in imgs]))
