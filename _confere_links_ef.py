# -*- coding: utf-8 -*-
"""Confere se os produtos de EF na loja estão com link de checkout e capa."""
import io
import re

s = io.open(r'A:\Claude.ai\Loja\index.html', encoding='utf-8').read()
for slug in ('ef-6', 'ef-7', 'ef-8', 'ef-9', 'ef-1em', 'ef-2em', 'ef-3em'):
    m = re.search(r'"slug": "%s".*?"link": (null|"[^"]+")' % re.escape(slug), s)
    print('%-8s %s' % (slug, m.group(1) if m else 'nao achei'))
