# -*- coding: utf-8 -*-
import io

s = io.open(r'A:\Claude.ai\Loja\index.html', encoding='utf-8').read()
for slug in ('ef-6', 'ef-8', 'ef-3em'):
    i = s.find('"slug": "%s"' % slug)
    print(slug, '->', s[i:i + 260].replace('\n', ' '))
print('ocorrencias "Educação Financeira":', s.count('Educação Financeira'))
print('tipo se-liga em ef:', '"tipo": "se-liga"' in s)
