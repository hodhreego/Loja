# -*- coding: utf-8 -*-
"""Miniaturas dos produtos novos de Consciencia Negra (14/11/2026):
1 = capa; 2 e 3 = paginas com tarja AMOSTRA (25% da area); 4 = TODAS as folhas de gabarito empilhadas
(um pedaco de cada aparece) com 3 tarjas AMOSTRA."""
import os, sys
import fitz
from PIL import Image, ImageDraw, ImageFilter
from tarja_forte_cn import PDFS, IMG, M, tarja_forte, render
NOVOS = ['cn-da-africa-ao-brasil','cn-portugues-autoria-negra','cn-cientistas-negras','cn-negros-mundo','cn-direitos-civis-eua','cn-apartheid','cn-portugues-3ano','cn-historia-3ano','cn-matematica-3ano']
W, H = 827, 1171

def empilhar(pgs):
    cv = Image.new('RGB', (W, H), (243, 233, 220))
    n = len(pgs); lw = 640
    for i, p in enumerate(pgs):
        im = p.resize((lw, int(lw * p.height / p.width)))
        x = 18 + i * int((W - lw - 36) / max(1, n - 1)); y = 24 + i * int((H - 24 - 330) / max(1, n - 1))
        sh = Image.new('RGBA', (im.width + 30, im.height + 30), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle((15, 15, im.width + 15, im.height + 15), fill=(0, 0, 0, 120))
        sh = sh.filter(ImageFilter.GaussianBlur(7))
        cv.paste(sh, (x - 15 + 6, y - 15 + 6), sh)
        ImageDraw.Draw(im).rectangle((0, 0, im.width - 1, im.height - 1), outline=(90, 60, 30), width=2)
        cv.paste(im, (x, y))
    return cv

for slug in NOVOS:
    if len(sys.argv) > 1 and slug not in sys.argv[1:]: continue
    doc = fitz.open(os.path.join(M, PDFS[slug]))
    n = len(doc); gab = list(range(n - 3, n))   # 3 ultimas paginas = gabarito
    tarja_forte(render(doc, 1)).save(os.path.join(IMG, f'{slug}-2.jpg'), 'JPEG', quality=86, optimize=True)
    tarja_forte(render(doc, 2)).save(os.path.join(IMG, f'{slug}-3.jpg'), 'JPEG', quality=86, optimize=True)
    st = empilhar([render(doc, i) for i in gab])
    tarja_forte(st, frac=0.105, offs=(-0.30, 0, 0.30)).save(os.path.join(IMG, f'{slug}-4.jpg'), 'JPEG', quality=86, optimize=True)
    f5 = os.path.join(IMG, f'{slug}-5.jpg')
    if os.path.exists(f5): os.remove(f5)
    print('ok', slug)
