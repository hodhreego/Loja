# -*- coding: utf-8 -*-
import io
import re

s = io.open(r'A:\Claude.ai\Loja\index.html', encoding='utf-8').read()
for slug in ('ef-6', 'ef-3em', 'se-liga-6'):
    m = re.search(r'"slug": "%s".*?"imgs": \[(.*?)\]' % re.escape(slug), s)
    print(slug, '->', m.group(1) if m else 'nao achei')
