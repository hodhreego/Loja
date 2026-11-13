# -*- coding: utf-8 -*-
"""Cobre com tarjas diagonais AMOSTRA as miniaturas da vitrine que mostram gabarito/resolucoes.
Idempotente: parte sempre de img/limpa/<slug>-<k>.jpg (guarda a copia limpa na 1a vez).
Uso: python tarjar_gabaritos.py [slug ...]   (sem args = todos)"""
import os, sys, json, re
import fitz
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__)); IMG = os.path.join(HERE, 'img'); LIMPA = os.path.join(IMG, 'limpa')
BORDO = (122, 31, 43)
EF = r'A:\Claude.ai\Materiais\Educacao-Financeira\Avaliacoes-Finais'
EFP = {'ef-6': '6-ano', 'ef-7': '7-ano', 'ef-8': '8-ano', 'ef-9': '9-ano', 'ef-1em': '1-serie-em', 'ef-2em': '2-serie-em', 'ef-3em': '3-serie-em'}
def fonte(t): return ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', t)
def fontes():
    import gerar_previews as g
    out = dict(g.ITENS)
    for s, p in EFP.items(): out[s] = (os.path.join(EF, p, 'se-liga-educacao-financeira.pdf'), None)
    return out
def eh_resposta(txt):
    u = txt.upper()
    return ('GABARITO OFICIAL' in u or 'RESOLUÇÕES PASSO A PASSO' in u or 'RESOLUCOES PASSO A PASSO' in u
            or re.search(r'\bGABARITO\b', u[:300]) is not None)
def tarjas(img):
    w, h = img.size
    S = max(w, h) * 2
    over = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(over)
    bh = max(60, int(h * 0.07)); passo = int(bh * 1.8)
    f = fonte(int(bh * 0.6)); t = 'AMOSTRA  •  AMOSTRA  •  AMOSTRA  •  AMOSTRA  •  AMOSTRA  •  AMOSTRA'
    y = 0
    while y < S:
        d.rectangle((0, y, S, y + bh), fill=BORDO + (205,))
        d.rectangle((0, y, S, y + 3), fill=(255, 255, 255, 190)); d.rectangle((0, y + bh - 3, S, y + bh), fill=(255, 255, 255, 190))
        d.text((S // 2, y + bh // 2), t, font=f, fill=(255, 255, 255, 235), anchor='mm')
        y += passo
    over = over.rotate(35, resample=Image.BICUBIC)
    cx, cy = over.width // 2, over.height // 2
    over = over.crop((cx - w // 2, cy - h // 2, cx - w // 2 + w, cy - h // 2 + h))
    out = img.convert('RGBA'); out.alpha_composite(Image.new('RGBA', (w, h), (255, 255, 255, 40))); out.alpha_composite(over)
    return out.convert('RGB')
def main(alvos):
    pag = json.load(open(os.path.join(IMG, '_paginas.json'), encoding='utf-8')); F = fontes(); feitos = []
    os.makedirs(LIMPA, exist_ok=True)
    for slug, info in pag.items():
        if alvos and slug not in alvos: continue
        if slug not in F or not os.path.exists(F[slug][0]): print('sem pdf', slug); continue
        doc = fitz.open(F[slug][0])
        for k, n in enumerate(info['usadas'], 1):
            if k == 1 or n - 1 >= len(doc): continue
            if not eh_resposta(doc[n - 1].get_text()): continue
            jp = os.path.join(IMG, '%s-%d.jpg' % (slug, k)); lp = os.path.join(LIMPA, '%s-%d.jpg' % (slug, k))
            if not os.path.exists(jp): continue
            if not os.path.exists(lp):
                if slug.startswith(('se-liga', 'ef-')) or True:
                    import shutil; shutil.copyfile(jp, lp)
            base = Image.open(lp).convert('RGB'); out = tarjas(base)
            out.save(jp, 'JPEG', quality=84, optimize=True); out.save(jp[:-4] + '.webp', 'WEBP', quality=80)
            feitos.append('%s-%d(p%d)' % (slug, k, n))
        doc.close()
    print(len(feitos), 'tarjadas:', ' '.join(feitos))
if __name__ == '__main__': main([a for a in sys.argv[1:]])
