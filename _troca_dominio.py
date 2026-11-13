# -*- coding: utf-8 -*-
"""Troca o endereço antigo (hodhreego.github.io/Loja) pelo domínio próprio eduloja.com."""
import io
import os

RAIZ = r'A:\Claude.ai\Loja'
NOVO = 'https://eduloja.com'
ANTIGO = 'https://hodhreego.github.io/Loja'
ANTIGO2 = 'https://hodhreego.github.io/Loja/'

ARQUIVOS = ['sitemap.xml', 'robots.txt', 'gerar_produtos.py']

for nome in ARQUIVOS:
    p = os.path.join(RAIZ, nome)
    if not os.path.exists(p):
        print('sem arquivo:', nome)
        continue
    s = io.open(p, encoding='utf-8').read()
    antes = s.count(ANTIGO)
    s = s.replace(ANTIGO2, NOVO + '/').replace(ANTIGO, NOVO)
    io.open(p, 'w', encoding='utf-8').write(s)
    print('%-20s %d ocorrências trocadas' % (nome, antes))
