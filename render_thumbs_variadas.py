# -*- coding: utf-8 -*-
"""Miniaturas 2-5 sem repetir paginas genericas (Como aplicar, Analise da turma, gabarito-tabela).
2,3 = 2 paginas de questoes mais ilustradas; 4 = pagina de resolucoes mais colorida; 5 = Memorex
(ou, se nao houver, a 3a pagina de questoes mais ilustrada)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import fitz
from render_thumbs_seliga import cor_score, render, salva, OUT
RM = r'A:\Claude.ai\Materiais'
ALVOS = {}
for s, p in {'ef-6':'6-ano','ef-7':'7-ano','ef-8':'8-ano','ef-9':'9-ano','ef-1em':'1-serie-em','ef-2em':'2-serie-em','ef-3em':'3-serie-em'}.items():
    ALVOS[s] = RM + r'\Educacao-Financeira\Avaliacoes-Finais\%s\se-liga-educacao-financeira.pdf' % p
for s, p in {'se-liga-6':'6-ano-matematica','se-liga-7':'7-ano-matematica','se-liga-8':'8-ano-matematica','se-liga-9':'9-ano-matematica','se-liga-1em':'1-serie-em-matematica','se-liga-2em':'2-serie-em-matematica','se-liga-3em':'3-serie-em-matematica'}.items():
    a = RM + r'\Matematica\Avaliacoes-Finais\%s\se-liga-2026-atualizado.pdf' % p
    ALVOS[s] = a if os.path.exists(a) else RM + r'\Matematica\Avaliacoes-Finais\%s\se-liga-2026.pdf' % p
for slug, pdf in ALVOS.items():
    d = fitz.open(pdf)
    tx = [(d[i].get_text() or '').upper() for i in range(len(d))]
    ca = next((i for i in range(len(d)) if 'COMO APLICAR' in tx[i]), len(d))
    q = [i for i in range(1, ca) if 'INSTRU' not in tx[i][:300]]
    res = [i for i in range(len(d)) if 'RESOLU' in tx[i] and 'PASSO' in tx[i]]
    mem = [i for i in range(len(d)) if 'MEMOREX' in tx[i] and 'RELEMBRE' in tx[i]]
    sq = sorted(((cor_score(d[i]) + min(len(d[i].get_drawings()), 120) / 4000., i) for i in q), reverse=True)
    esc = [i for _, i in sq[:2]]
    rs = sorted(((cor_score(d[i]), i) for i in res), reverse=True)
    quarta = rs[0][1] if rs else (sq[2][1] if len(sq) > 2 else sq[0][1])
    quinta = mem[0] if (mem and not slug.startswith('ef-')) else (sq[3][1] if len(sq) > 3 else sq[-1][1])
    pg = sorted(esc) + [quarta, quinta]
    for k, i in enumerate(pg, 2):
        salva(render(d, i), slug, k)
    print(slug, [i + 1 for i in pg])
