# -*- coding: utf-8 -*-
import io

s = io.open(r'A:\Claude.ai\Loja\index.html', encoding='utf-8').read()
i = s.find('"slug": "se-liga-6"')
print(s[i:i + 320])
print('--- canonical ---')
j = s.find('rel="canonical"')
print(s[j - 20:j + 70] if j > 0 else 'SEM CANONICAL')
print('--- quantas prévias se-liga-6 ---')
import re
m = re.search(r'"slug": "se-liga-6".*?"imgs": \[(.*?)\]', s)
print(m.group(1) if m else 'nao achei')
