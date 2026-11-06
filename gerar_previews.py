# -*- coding: utf-8 -*-
"""Gera as miniaturas da loja: capa limpa + paginas internas coloridas com faixa AMOSTRA na diagonal.

- Escolhe as paginas mais coloridas (com ilustracoes) de cada PDF.
- Ate 7 imagens por produto: 1 capa + 6 internas.
- Faixa AMOSTRA diagonal (35 graus) em bordô; persianas somente na pagina de gabarito.
"""
import os
import sys

import fitz
from PIL import Image, ImageDraw, ImageFont

DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
BORDO = (122, 31, 43)
FONT = r'C:\Windows\Fonts\arialbd.ttf'
LARG = 900
MAXPAG = 7


def fonte(t):
    try:
        return ImageFont.truetype(FONT, t)
    except Exception:
        return ImageFont.load_default()


def cor_score(page):
    """Fracao de pixels coloridos (ilustracoes) na pagina."""
    pix = page.get_pixmap(dpi=28, colorspace=fitz.csRGB, alpha=False)
    im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    h, s, v = im.convert('HSV').split()
    sat = s.point(lambda x: 255 if x > 72 else 0)
    val = v.point(lambda x: 255 if x > 45 else 0)
    from PIL import ImageChops
    m = ImageChops.multiply(sat, val)
    n = m.width * m.height
    return m.histogram()[255] / float(n)


def eh_gabarito(txt):
    return 'GABARITO OFICIAL' in txt.upper()


def escolher(doc):
    n = len(doc)
    gab = None
    cand = []
    for i in range(1, n):
        if gab is None and eh_gabarito(doc[i].get_text()):
            gab = i
        if len(doc[i].get_text().strip()) < 60:
            continue
        cand.append((cor_score(doc[i]), i))
    cand.sort(reverse=True)
    escolhidas = []
    for sc, i in cand:
        if sc < 0.010:            # pagina praticamente sem cor
            continue
        if i == gab:
            continue
        if i not in escolhidas:
            escolhidas.append(i)
        if len(escolhidas) >= (MAXPAG - 1) - (1 if gab else 0):
            break
    escolhidas.sort()
    if gab:
        escolhidas.append(gab)
    return escolhidas


def faixa(img):
    w, h = img.size
    over = Image.new('RGBA', (w * 2, h * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    cy, hb = h, max(46, int(h * 0.055))
    d.rectangle((0, cy - hb // 2, w * 2, cy + hb // 2), fill=BORDO + (150,))
    d.rectangle((0, cy - hb // 2, w * 2, cy - hb // 2 + 4), fill=(255, 255, 255, 180))
    d.rectangle((0, cy + hb // 2 - 4, w * 2, cy + hb // 2), fill=(255, 255, 255, 180))
    t = 'AMOSTRA'
    f = fonte(int(hb * 0.58))
    tw = d.textlength(t, font=f)
    while tw > w * 0.62:
        f = fonte(int(f.size * 0.9))
        tw = d.textlength(t, font=f)
    d.text((w, cy), t, font=f, fill=(255, 255, 255, 245), anchor='mm')
    over = over.rotate(35, resample=Image.BICUBIC)
    cx, cyy = over.width // 2, over.height // 2
    over = over.crop((cx - w // 2, cyy - h // 2, cx - w // 2 + w, cyy - h // 2 + h))
    out = img.convert('RGBA')
    out.alpha_composite(over)
    return out.convert('RGB')


def persianas(img):
    w, h = img.size
    over = Image.new('RGBA', (w, h), (255, 255, 255, 55))
    d = ImageDraw.Draw(over)
    passo = max(52, int(h * 0.075))
    for y in range(0, h, passo):
        d.rectangle((0, y, w, y + int(passo * 0.55)), fill=(255, 255, 255, 185))
    f = fonte(max(40, int(w * 0.11)))
    d.text((w // 2, h // 2), 'AMOSTRA', font=f, fill=BORDO + (225,), anchor='mm')
    d.text((w // 2, h // 2 + int(w * 0.13)), 'GABARITO PROTEGIDO',
           font=fonte(max(18, int(w * 0.045))), fill=BORDO + (225,), anchor='mm')
    out = Image.alpha_composite(img.convert('RGBA'), over)
    return out.convert('RGB')


def render(doc, idx, larga=False):
    page = doc[idx]
    z = LARG / page.rect.width
    pix = page.get_pixmap(matrix=fitz.Matrix(z, z), colorspace=fitz.csRGB, alpha=False)
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)


def gerar(slug, pdf, capa=None):
    if not os.path.exists(pdf):
        print('FALTA', slug, pdf)
        return 0
    doc = fitz.open(pdf)
    n = 0
    # capa limpa (sem faixa)
    if capa and os.path.exists(capa):
        im = Image.open(capa).convert('RGB')
        w = LARG
        im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    else:
        im = render(doc, 0)
        if im.width > LARG:
            im = im.resize((LARG, int(im.height * LARG / im.width)), Image.LANCZOS)
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CAPAS_TRAVADAS.txt')) and '--forcar-capas' not in __import__('sys').argv:
        print('   capa -1 travada (CAPAS_TRAVADAS.txt): mantida')
    else:
        im.save(os.path.join(DEST, '%s-1.jpg' % slug), 'JPEG', quality=86, optimize=True)
    n = 1
    escolhidas = escolher(doc)
    gab_txt = 'GABARITO'
    for k, idx in enumerate(escolhidas, 2):
        im = render(doc, idx)
        if im.width > LARG:
            im = im.resize((LARG, int(im.height * LARG / im.width)), Image.LANCZOS)
        if eh_gabarito(doc[idx].get_text()):
            im = persianas(im)
        else:
            im = faixa(im)
        im.save(os.path.join(DEST, '%s-%d.jpg' % (slug, k)), 'JPEG', quality=84, optimize=True)
        n = k
    doc.close()
    print('%-28s %d imagens  paginas=%s' % (slug, n, [p + 1 for p in escolhidas]))
    return n


VOL = r'A:\Claude.ai\Materiais\Matematica\9-ano\Volumes'
PROD = r'A:\Claude.ai\produtos'
SAEB = r'A:\Claude.ai\Materiais\Matematica\Simulados-SAEB'

ITENS = {}
for slug in ('volume-cone', 'volume-cubo', 'volume-paralelepipedo', 'volume-prisma',
             'volume-esfera', 'volume-piramide', 'volume-cubo-bloco-prisma'):
    ITENS[slug] = (os.path.join(VOL, slug, 'loja', slug + '.pdf'),
                   os.path.join(PROD, 'volumes', slug, 'arte-1.png'))
ITENS['volume-cilindro'] = (os.path.join(VOL, 'volume-cilindro', 'loja', 'volume-cilindro-com-pi.pdf'),
                            os.path.join(PROD, 'volumes', 'volume-cilindro', 'arte-1.png'))

NIVEIS = {'6': '6-ano-matematica', '7': '7-ano-matematica', '8': '8-ano-matematica',
          '9': '9-ano-matematica', '1em': '1-serie-em-matematica',
          '2em': '2-serie-em-matematica', '3em': '3-serie-em-matematica'}
for k, pasta in NIVEIS.items():
    ITENS['se-liga-' + k] = (os.path.join(PROD, 'se-liga', pasta, 'material.pdf'),
                             os.path.join(PROD, 'se-liga', pasta, 'arte-1.png'))
    ITENS['sei-' + k] = (os.path.join(PROD, 'sei', pasta, 'material.pdf'),
                         os.path.join(PROD, 'sei', pasta, 'arte-1.png'))

ITENS['saeb-5'] = (os.path.join(SAEB, '5-ano', 'simulado-saeb-matematica-5ano.pdf'),
                   os.path.join(PROD, 'saeb', '5-ano', 'arte-1.png'))
ITENS['saeb-9'] = (os.path.join(SAEB, '9-ano', 'simulado-saeb-matematica-9-ano.pdf'),
                   os.path.join(PROD, 'saeb', '9-ano', 'arte-1.png'))
ITENS['saeb-3em'] = (os.path.join(SAEB, '3-ano-EM', 'simulado-saeb-matematica-3-ano-em.pdf'),
                     os.path.join(PROD, 'saeb', '3-ano-EM', 'arte-1.png'))

if __name__ == '__main__':
    alvos = [a for a in sys.argv[1:] if not a.startswith('--')]
    lista = [(s, p, c) for s, (p, c) in ITENS.items() if not alvos or s in alvos]
    total = 0
    for slug, pdf, capa in lista:
        try:
            total += gerar(slug, pdf, capa)
        except Exception as e:
            print('ERRO', slug, str(e)[:120])
    print('total de imagens:', total)
