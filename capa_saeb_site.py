# -*- coding: utf-8 -*-
"""Capas SAEB SO PARA O SITE (Loja/img/saeb-<slug>-1.jpg/.webp). Estilo baralho do Se Liga, outro esquema de cores
(noite + dourado + glow), 'SAEB' gigante a esquerda. Nao altera os cadernos."""
import os, fitz
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
B = r'A:\Claude.ai\Materiais\Matematica\Simulados-SAEB'; OUT = r'A:\Claude.ai\Loja\img'
SER = {'9': (B + r'\9-ano\simulado-saeb-matematica-9-ano', '9º', 'ANO', '9º ano'),
       '3em': (B + r'\3-ano-EM\simulado-saeb-matematica-3-ano-em', '3ª', 'SÉRIE EM', '3ª série EM')}
S = 1000; GOLD = (255, 200, 40); CY = (34, 211, 238); MG = (236, 40, 120)
def F(sz): return ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', sz)
def fundo():
    bg = Image.new('RGB', (S, S)); d = ImageDraw.Draw(bg)
    for y in range(S):
        t = y / S; d.line([(0, y), (S, y)], fill=(int(10 + 28 * t), int(8 + 6 * t), int(40 + 55 * t)))
    return bg.convert('RGBA')
def glow(base, silhueta, cor, raio, forca=1.0, off=(0, 0)):
    """halo colorido a partir da silhueta (imagem RGBA/L do tamanho do canvas)"""
    m = silhueta.convert('L').filter(ImageFilter.GaussianBlur(raio)); m = m.point(lambda v: min(255, int(v * forca)))
    cam = Image.new('RGBA', base.size, cor + (0,)); cam.putalpha(m); base.alpha_composite(cam)
def cartao(bg, im, w, ang, pos, cor):
    h = int(im.height * w / im.width); im = im.convert('RGB').resize((w, h), Image.LANCZOS)
    c = Image.new('RGBA', (w + 12, h + 12), (255, 255, 255, 255)); c.paste(im, (6, 6))
    c = c.rotate(ang, expand=True, resample=Image.BICUBIC)
    sil = Image.new('L', bg.size, 0); sil.paste(c.split()[3], pos)
    glow(bg, sil, cor, 24, 1.15); glow(bg, sil, cor, 7, 0.7)
    bg.alpha_composite(c, pos)
def texto_glow(bg, xy, t, sz, fill, cor, anchor='lm'):
    sil = Image.new('L', bg.size, 0); ImageDraw.Draw(sil).text(xy, t, font=F(sz), fill=255, anchor=anchor)
    glow(bg, sil, cor, 18, 1.1); glow(bg, sil, cor, 5, 0.7)
    ImageDraw.Draw(bg).text(xy, t, font=F(sz), fill=fill, anchor=anchor)
def pg(doc, n, dpi=130):
    p = doc[max(0, min(n - 1, len(doc) - 1))].get_pixmap(dpi=dpi, alpha=False); return Image.frombytes('RGB', (p.width, p.height), p.samples)
def gerar(slug):
    base, s1, s2, nome = SER[slug]
    doc = fitz.open(base + '.pdf'); secs = BeautifulSoup(open(base + '.html', encoding='utf-8').read(), 'html.parser').select('section.pagina')
    figs = sorted([(len(s.find_all(['svg', 'img'])), i) for i, s in enumerate(secs, 1) if 'prova' in (s.get('class') or [])], reverse=True)
    q1, q2 = figs[0][1], figs[1][1]
    bg = fundo()
    cartao(bg, pg(doc, q2), 400, -9, (-18, 300), CY); cartao(bg, pg(doc, q1), 400, 8, (590, 300), MG)
    cartao(bg, pg(doc, 1), 450, -2, (245, 270), GOLD)
    d = ImageDraw.Draw(bg)
    texto_glow(bg, (36, 128), 'SAEB', 205, (255, 226, 110), GOLD)             # gigante, canto esquerdo
    d.text((640, 62), 'LOJA DE MATEMÁTICA', font=F(26), fill=GOLD, anchor='lm')
    d.text((640, 118), 'SIMULADO', font=F(54), fill='white', anchor='lm')
    d.text((640, 172), 'de Matemática', font=F(40), fill=(220, 232, 255), anchor='lm')
    d.text((640, 218), nome, font=F(36), fill=CY, anchor='lm')
    def selo(cx, cy, r, fill, fg, l1, l2, a, b, halo):
        sil = Image.new('L', bg.size, 0); ImageDraw.Draw(sil).ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
        glow(bg, sil, halo, 18, 1.1)
        dd = ImageDraw.Draw(bg); dd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill, outline='white', width=5)
        dd.text((cx, cy - (a // 3 if l2 else 0)), l1, font=F(a), fill=fg, anchor='mm')
        if l2: dd.text((cx, cy + a // 1.6), l2, font=F(b), fill=fg, anchor='mm')
    selo(112, 740, 98, GOLD, (30, 12, 70), s1, s2, 90 if len(s2) <= 3 else 78, 36 if len(s2) <= 3 else 25, GOLD)
    selo(890, 620, 76, MG, 'white', 'COM', 'GABARITO', 34, 24, MG)
    selo(890, 770, 72, CY, (8, 20, 50), '50', 'QUESTÕES', 44, 20, CY)
    d.rounded_rectangle((40, 878, 960, 936), radius=18, fill=(8, 6, 30), outline=GOLD, width=3)
    d.text((500, 907), '50 questões  •  gabarito  •  resoluções passo a passo  •  %d páginas' % len(doc), font=F(25), fill='white', anchor='mm')
    d.text((500, 960), 'Prof. Rodrigo  •  PDF pronto para imprimir', font=F(28), fill=GOLD, anchor='mm')
    d.text((500, 988), 'Veja as páginas por dentro  >>', font=F(19), fill=(220, 232, 255), anchor='mm')
    c = bg.convert('RGB'); c.save(os.path.join(OUT, 'saeb-%s-1.jpg' % slug), quality=92); c.save(os.path.join(OUT, 'saeb-%s-1.webp' % slug), quality=88)
    print('ok', slug, q1, q2, len(doc))
if __name__ == '__main__':
    import sys
    for s in (sys.argv[1:] or SER): gerar(s)
