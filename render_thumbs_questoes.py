# -*- coding: utf-8 -*-
"""Miniaturas 2,3,4 = 3 paginas de QUESTOES (as mais ilustradas) com tarja AMOSTRA; 5 = Memorex com tarja.
Vale para se-liga-*, sei-* (recomposicao) e saeb-*. A capa (1) nao e mexida."""
import os, re, sys, shutil
import fitz
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerar_previews as g
from tarja_forte_cn import tarja_forte, render, IMG
from render_thumbs_seliga import cor_score
from cor_produto import cor_produto
BKP = os.path.join(IMG, 'versao-anterior-miniaturas-questoes'); os.makedirs(BKP, exist_ok=True)
def salva(im, slug, k):
    for e in ('jpg', 'webp'):
        f = os.path.join(IMG, '%s-%d.%s' % (slug, k, e))
        if os.path.exists(f) and not os.path.exists(os.path.join(BKP, os.path.basename(f))): shutil.copy(f, BKP)
    im.save(os.path.join(IMG, '%s-%d.jpg' % (slug, k)), 'JPEG', quality=86, optimize=True)
    im.save(os.path.join(IMG, '%s-%d.webp' % (slug, k)), 'WEBP', quality=84, method=6)
QUE = re.compile(r'^\s*\d+\s+(D\d+|E[FM]\d)')
def main(alvos):
    for slug in g.ITENS:
        if not re.match(r'(se-liga|sei|saeb)-', slug): continue
        if alvos and slug not in alvos: continue
        C = cor_produto(slug); doc = fitz.open(g.ITENS[slug][0]); cand = []; memo = None; fim = False
        for i in range(1, len(doc)):
            t = doc[i].get_text() or ''
            if QUE.match(t) and 'ZipGrade' not in t[:200] and 'Baixe' not in t[:200] and 'Gabarito:' not in t and not fim: cand.append(i)
            elif cand: fim = True
            if memo is None and 'MEMOREX' in t[:120].upper(): memo = i
        top = sorted(sorted(cand, key=lambda i: -cor_score(doc[i]))[:3])
        if len(top) < 3: print('POUCAS', slug, cand); continue
        for k, idx in zip((2, 3, 4), top): salva(tarja_forte(render(doc, idx), cor=C[0], borda=C[1]), slug, k)
        if memo is not None: salva(tarja_forte(render(doc, memo), cor=C[0], borda=C[1]), slug, 5)
        print('ok', slug, 'questoes', top, 'memorex', memo)
if __name__ == '__main__': main(sys.argv[1:])
